
/* LOGIN - Função para alternar a visibilidade da senha*/
function changePasswordVisibility() {
  const icon = document.getElementById("eye-icon");
  const inputPassword = document.getElementById("password");

  icon.classList.toggle("fa-eye-slash");
  icon.classList.toggle("fa-eye");

  const isPassword = inputPassword.type === "password";
  inputPassword.type = isPassword ? "text" : "password";
}

/* DEBUG liveserver jinja*/
document.addEventListener("DOMContentLoaded", function () {
  const jinja = document.querySelector(".jinja");
  const jinjaAlerts = document.querySelectorAll(".login-alert");

  // Verifica se há algum conteúdo nas mensagens
  if (jinja && jinjaAlerts[0].innerHTML !== "{{ message }}") {
    jinja.style.display = "block"; // Mostra as mensagens
  }
});
