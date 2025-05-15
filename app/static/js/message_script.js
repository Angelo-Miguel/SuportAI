/* Faz com que a scroll bar do chat começe para baixo "invertido" */
window.addEventListener("DOMContentLoaded", function () {
	const msg = document.getElementById("messages");
	if (msg) {
		msg.scrollTop = msg.scrollHeight;
	}
});
