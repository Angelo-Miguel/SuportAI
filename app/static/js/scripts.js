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

function pintarEstrelas(){
    for (let i = 0; i < estrelas.length; i++) { /* Funcionamento das estrelas Antes de serem clicadas */
        estrelas[i].addEventListener('mouseover', function pintar(){
            if(bloquear_estrelas == false){
                for (let j = 0; j < i+1; j++) {
                    estrelas[j].classList.remove("fa-regular", "fa-star")
                    estrelas[j].classList.add("fa-solid", "fa-star")          
                    /* Remove as estrelas vaziar e adiciona estrelas solid ao passar o mouse na estrela */
                }
            }
        })
        estrelas[i].addEventListener('mouseout', function apagar(){
            if (bloquear_estrelas == false) { /* Ver linha 53 */
                for (let j = 0; j <i+1; j++) {
                    estrelas[j].classList.remove("fa-solid", "fa-star")
                    estrelas[j].classList.add("fa-regular", "fa-star")          
                    /* Remove estrelas solid e adiciona estrelas vazias ao tirar o mouse da estrela */
                }
            }
        })
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