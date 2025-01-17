from .models import MyMovieList
import pandas as pd

import requests

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


# https://developer.themoviedb.org/reference/discover-movie

API_KEY = "20b8ac581ae40eadf1488dfcda82471c"
BASE_URL = "https://api.themoviedb.org/3"


def fetch_movie_details(movie_id, api_key, language="pt-BR"):
    movie_details_endpoint = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": api_key, "language": language}
    response = requests.get(movie_details_endpoint, params=params)

    movie_data = response.json()

    genres = movie_data.get("genres", [])
    movie_data["genre_ids"] = [genre["id"] for genre in genres]

    movie_data.pop("genres", None)

    return movie_data


def get_movies(genre_ids=None, favorites=None):
    """Fetches movies based on genres and favorites."""
    # Fetch filtered movies
    endpoint = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "language": "pt-BR",
        "sort_by": "vote_average.desc",
        "vote_count.gte": 1000,
    }
    if genre_ids:
        params["with_genres"] = genre_ids

    response = requests.get(endpoint, params=params)
    filtered_movies = response.json().get("results", [])

    # Fetch favorite movies
    favorite_movies = [
        fetch_movie_details(movie_id, API_KEY)
        for movie_id in favorites or []
        if fetch_movie_details(movie_id, API_KEY) is not None
    ]

    return favorite_movies + filtered_movies


def create_user_list(user, selected_genres, favorites):
    movies = get_movies(selected_genres, favorites)

    movie_instances = []
    for movie in movies:
        movie_instances.append(
            MyMovieList(
                movie_id=movie["id"],
                title=movie["title"],
                poster_path=movie.get("poster_path", ""),
                vote_average=movie["vote_average"],
                genre_ids=",".join(map(str, movie["genre_ids"])),
                overview=movie.get("overview", ""),
                release_date=movie.get("release_date", "1900-01-01"),
                user=user,
                rating="LIKE" if movie["id"] in favorites else "NONE",
            )
        )

    if movie_instances:
        MyMovieList.objects.bulk_create(movie_instances)
        return f"{len(movie_instances)} movies saved to the database."
    else:
        return "No new movies to add."


def recommend_movies(user):
    user_id = user.id

    movies = MyMovieList.objects.all().values()
    df_user_list = pd.DataFrame(data=movies)

    priority_map = {
        "LIKE": 1,
        "NONE": 2,
        "DISLIKE": 3,
    }

    # classificar prioridade
    df_user_list["priority"] = df_user_list["rating"].map(priority_map)
    # verificar se pertence a lista do usuario
    df_user_list["is_user"] = (df_user_list["user_id"] == user_id).astype(int)

    liked_movies = df_user_list[
        (df_user_list["rating"] == "LIKE") & (df_user_list["user_id"] == user_id)
    ]
    df_user_list["genre_ids"] = df_user_list["genre_ids"].astype(str)

    # criar vetores para o sklearn calcular a similaridade de gêneros
    vectorizer = CountVectorizer(token_pattern=r"[^,]+", binary=True)
    genre_matrix = vectorizer.fit_transform(df_user_list["genre_ids"])

    # Adicionar coluna para o ano de lançamento e normalizar
    df_user_list["release_year"] = pd.to_datetime(df_user_list["release_date"]).dt.year
    max_year = df_user_list["release_year"].max()
    min_year = df_user_list["release_year"].min()
    df_user_list["normalized_release_year"] = (
        df_user_list["release_year"] - min_year
    ) / (max_year - min_year)

    liked_movies = df_user_list[
        (df_user_list["rating"] == "LIKE") & (df_user_list["user_id"] == user_id)
    ]
    if not liked_movies.empty:
        # Similaridade de gêneros
        liked_genres = vectorizer.transform(liked_movies["genre_ids"])
        genre_similarity_scores = cosine_similarity(genre_matrix, liked_genres).mean(
            axis=1
        )

        # Similaridade de datas
        liked_years = liked_movies["normalized_release_year"].values
        date_similarity_scores = 1 - (
            df_user_list["normalized_release_year"].apply(
                lambda x: abs(x - liked_years).mean()
            )
        )

        # Combinar similaridade de gêneros e datas com pesos
        genre_weight = 0.8
        date_weight = 0.2
        similarity_scores = (
            genre_weight * genre_similarity_scores
            + date_weight * date_similarity_scores
        )
    else:
        # caso o usuário não tenha marcado nada como "gostei", definir similaridade padrão
        similarity_scores = [0] * len(df_user_list["genre_ids"])

    df_user_list["genre_similarity"] = similarity_scores

    # Ordenar os filmes com base nas prioridades:
    # 1. Filmes do usuário atual
    # 2. Similaridade de gêneros
    # 3. vote_average
    # 4. priority
    recommend_movies = (
        df_user_list.sort_values(
            by=["is_user", "genre_similarity", "vote_average", "priority"],
            ascending=[False, False, False, True],
        )
        .drop_duplicates(subset=["movie_id"])
        .loc[
            :,
            [
                "movie_id",
                "user_id",
                "title",
                "rating",
                "genre_ids",
                "vote_average",
                "poster_path",
            ],
        ]
        .to_dict(orient="records")
    )

    voted_movies = (
        df_user_list.sort_values(
            by=["vote_average"],
            ascending=[False],
        )
        .drop_duplicates(subset=["movie_id"])
        .loc[
            :,
            [
                "movie_id",
                "user_id",
                "title",
                "rating",
                "genre_ids",
                "vote_average",
                "poster_path",
            ],
        ]
        .to_dict(orient="records")
    )

    my_movies = (
        liked_movies.drop_duplicates(subset=["movie_id"])
        .loc[
            :,
            [
                "movie_id",
                "user_id",
                "title",
                "rating",
                "genre_ids",
                "vote_average",
                "poster_path",
            ],
        ]
        .to_dict(orient="records")
    )

    return recommend_movies, voted_movies, my_movies
