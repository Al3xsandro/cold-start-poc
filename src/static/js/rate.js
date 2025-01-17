function likeMovie(movie_id) {
    sendRating(movie_id, "LIKE");
}

function dislikeMovie(movie_id) {
    sendRating(movie_id, "DISLIKE");
}

function sendRating(movie_id, ratingType) {
    const url = `/rate-movie/${movie_id}/?type=${ratingType}`;
    
    fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
    .then(response => {
        if (response.ok) {
            return response.json()
        }
        throw new Error("Erro ao enviar avaliação.");
    })
    .then(data => {
        if (data.message) {
            alert(data.message)
            return
        } else if (data.error) {
            alert(data.message)
            return
        }
    })
    .catch(error => {
        console.error("Erro ao enviar avaliação:", error);
    });
}
