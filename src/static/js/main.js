function getMovies() {
    const TMDB_API_KEY = '20b8ac581ae40eadf1488dfcda82471c';
    let selectedMovies = [];
    let movies = [];

    async function fetchMovies() {
        try {
            const response = await fetch(`https://api.themoviedb.org/3/movie/popular?api_key=${TMDB_API_KEY}&language=en-US&page=1`);
            const data = await response.json();
            movies = data.results;

            const emblaContainer = document.querySelector('.embla__container');
            emblaContainer.innerHTML = '';

            movies.forEach(movie => {
                const slideEl = document.createElement('div');
                slideEl.classList.add('embla__slide');
                slideEl.innerHTML = `
                    <div class="relative flex flex-col items-center space-y-2 gap-5">
                       <label class="relative block cursor-pointer w-full h-60">
                            <input
                                type="checkbox"
                                class="absolute top-0 left-0 mt-3 ml-3 bg-white peer"
                                value="${movie.id}"
                                onChange="toggleMovie(${movie.id})"
                            />
                            <div class="peer-checked:border peer-checked:border-white rounded-sm w-full h-full relative">
                                <img
                                    src="https://image.tmdb.org/t/p/w780/${movie.backdrop_path}"
                                    alt="${movie.title} poster"
                                    class="w-full h-full object-cover rounded-md shadow-md"
                                />
                            </div>
                        </label>
                        <div class="flex flex-col justify-center items-center gap-2 mt-4">
                            <h2 class="text-lg font-semibold truncate text-center">${movie.title}</h2>
                            <p class="text-sm text-gray-600 text-center line-clamp-2">${movie.overview}</p>
                        </div>
                    </div>
                `;
                emblaContainer.appendChild(slideEl);
            });
        } catch (error) {
            console.error('Error fetching movies:', error);
            alert('Failed to load movies. Please try again later.');
        }
    }

    function toggleMovie(movieId) {
        const saveButton = document.getElementById('saveButton');

        if (selectedMovies.includes(movieId)) {
            selectedMovies = selectedMovies.filter(id => id !== movieId);
        } else {
            selectedMovies.push(movieId);
        }

        saveButton.disabled = selectedMovies.length < 3;
    }

    async function submitMovies() {
        const selectedGenres = new Set();
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        selectedMovies.forEach(movieId => {
            const movie = movies.find(m => m.id === movieId);
            if (movie) {
                movie.genre_ids.forEach(genreId => selectedGenres.add(genreId));
            }
        });

        try {
            const response = await fetch("submit-genres/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    genres: Array.from(selectedGenres)
                })
            });

            if (response.ok) {
                window.location.href = "mylist";
            } else {
                alert('Algo deu errado.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Algo deu errado.');
        }
    }

    document.addEventListener('DOMContentLoaded', fetchMovies);

    window.submitMovies = submitMovies;
    window.toggleMovie = toggleMovie;
}

getMovies()