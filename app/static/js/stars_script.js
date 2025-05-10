const stars = Array.from(document.querySelectorAll(".fa-star"));
const inputFeedback = document.getElementById("feedback-grade");
let starsLocked = false;


function updateStars(limit) {
    // Função para atualizar as estrelas visualmente
	stars.forEach((star, i) => {
		const isFilled = (i <= limit);
		star.classList.replace(
			isFilled ? "fa-regular" : "fa-solid",
			isFilled ? "fa-solid" : "fa-regular"
		);
	});
}

// Eventos
document.addEventListener("mouseover", (e) => {
	if (!starsLocked && e.target.classList.contains("fa-star")) {
		updateStars(stars.indexOf(e.target));
	}
});

document.addEventListener("mouseout", (e) => {
	if (!starsLocked && e.target.classList.contains("fa-star")) {
		updateStars(-1); // Reseta todas as estrelas se não estiverem bloqueadas
	}
});

document.addEventListener("click", (e) => {
	if (e.target.classList.contains("fa-star")) {
		const i = stars.indexOf(e.target);
		starsLocked = true;
		inputFeedback.value = i + 1;
		updateStars(i);
	}
});
