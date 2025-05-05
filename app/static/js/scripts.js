/* LOGIN - Função para alternar a visibilidade da senha*/
function changePasswordVisibility() {
	const icon = document.getElementById("eye-icon");
	const inputPassword = document.getElementById("password");

	icon.classList.toggle("fa-eye-slash");
	icon.classList.toggle("fa-eye");

	const isPassword = inputPassword.type === "password";
	inputPassword.type = isPassword ? "text" : "password";
}

/* GERAL - Troca o display entre none e outro que desejar */
function openAndClose(elementId, displayType) {
	const element = document.getElementById(elementId);
	if (element.style.display === "none" || element.style.display === "") {
		element.style.display = displayType;
	} else {
		element.style.display = "none";
	}
}

/* DEBUG liveserver jinja*/
document.addEventListener("DOMContentLoaded", function () {
	const jinjaSpans = document.querySelectorAll(".jinja")

	// Verifica se há algum conteúdo nas mensagens
	jinjaSpans.forEach(jinja => {
		if (jinja && !(jinja.innerHTML.includes("{"))) {
			jinja.style.display = "block"; // Mostra as mensagens
		}
	});

});
