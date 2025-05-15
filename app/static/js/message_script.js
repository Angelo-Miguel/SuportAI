/* TODO: terminar o scroll do chat */
/* FIXME: está ficando um espaço no final */
window.addEventListener('DOMContentLoaded', function () {
    const msg = document.getElementById("messages");
    if (msg) {
      msg.scrollTop = msg.scrollHeight;
    }
  });