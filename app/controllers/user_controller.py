# app/controllers/user_controller.py
from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.services.ticket_service import TicketService

user_bp = Blueprint("user", __name__)
ticket_service = TicketService()


@user_bp.route("/user")
def dashboard():
    # Mostra a página do dashborad para o usuario e carrega os tickets
    if "user" not in session:
        return redirect(url_for("auth.login_page"))

    try:
        tickets = ticket_service.get_tickets_by_user_id(session["user"]["id"])
    except Exception as e:
        flash("Erro ao carregar tickets.", "error")
        tickets = []
        
    return render_template("dashboard.html", user=session["user"], tickets=tickets)
