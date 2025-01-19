function sendRating(movie_id, ratingType, containerId, section) {
    uniqueContainer = `${containerId}-${section}`
    const container = document.getElementById(uniqueContainer);
    if (container) {
        container.innerHTML = `
        <button class="bg-gray-800 text-white px-4 py-2 rounded-md shadow-md cursor-not-allowed">
        Avaliado
        </button>
        `;
    }
    
    const url = `/rate-movie/${movie_id}/?type=${ratingType}`;

    fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw new Error("Erro ao enviar avaliação.");
      })
      .then((data) => {
        if (data.message) {
          console.log(data.message);
        } else if (data.error) {
          console.error(data.error);
        }
      })
      .catch((error) => {
        console.error("Erro ao enviar avaliação:", error);
      });
  }