# app/controllers/ticket_controller.py
from flask import Blueprint, request, session, redirect, url_for, flash
from app.models.ticket import Ticket
from app.services.ticket_service import TicketService

ticket_bp = Blueprint("ticket", __name__)

ticket_service = TicketService()


@ticket_bp.route("/new-ticket", methods=["POST"])
def new_ticket():
    # Cria um novo Ticket
    if "user" not in session:
        return redirect(url_for("auth.login_page"))

    title = request.form.get("title")
    category = request.form.get("category")
    description = request.form.get("description")

    if not title or not category or not description:
        flash("Todos os campos são obrigatórios.", "error")
        return redirect(url_for("user.dashboard"))

    try:
        ticket = Ticket(
            {
                "title": title,
                "category": category,
                "description": description,
                "user_id": session["user"]["id"],
            }
        )
        ticket_id = ticket_service.new_ticket(ticket)

        # Primeira msg do usuario
        session["first_user_message"] = {
            "message": description,
            "user_id": session["user"]["id"],
            "ticket_id": ticket_id,
        }
        return redirect(url_for("chat.chat", ticket_id=ticket_id))
    except Exception as e:
        flash("Erro ao criar ticket.", "error")
        return redirect(url_for("user.dashboard"))


@ticket_bp.route("/open-ticket", methods=["POST"])
def open_ticket():
    if "user" not in session:
        return redirect(url_for("auth.login_page"))

    ticket_id = request.form.get("ticket_id")
    if not ticket_id:
        flash("ID do ticket não informado.", "error")
        return redirect(url_for("user.dashboard"))

    ticket = ticket_service.get_ticket_by_id(ticket_id)
    if ticket:
        return redirect(url_for("chat.chat", ticket_id=ticket_id))
    else:
        flash("Ticket não encontrado.", "error")
        return redirect(url_for("user.dashboard"))
