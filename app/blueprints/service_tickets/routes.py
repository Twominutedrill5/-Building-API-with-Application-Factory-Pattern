from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import ServiceTicket, Mechanic, Vehicle
from .schemas import service_ticket_schema, service_tickets_schema

service_tickets_bp = Blueprint('service_tickets', __name__)


@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    data = request.get_json() or {}
    required = ['vehicle_id', 'service_desc']
    missing = [k for k in required if not data.get(k)]
    if missing:
        return jsonify({'error': 'missing_fields', 'missing': missing}), 400
    if not Vehicle.query.get(data['vehicle_id']):
        return jsonify({'error': 'vehicle_not_found'}), 404

    ticket = ServiceTicket(
        vehicle_id=data['vehicle_id'],
        service_desc=data['service_desc'],
        price=data.get('price'),
        status=data.get('status', 'pending')
    )
    db.session.add(ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 201


@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    return service_tickets_schema.jsonify(ServiceTicket.query.all()), 200


@service_tickets_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    t = ServiceTicket.query.get_or_404(ticket_id)
    m = Mechanic.query.get_or_404(mechanic_id)
    if m in t.mechanics:
        return jsonify({'error': 'mechanic_already_assigned'}), 409
    t.mechanics.append(m)
    db.session.commit()
    return service_ticket_schema.jsonify(t), 200


@service_tickets_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    t = ServiceTicket.query.get_or_404(ticket_id)
    m = Mechanic.query.get_or_404(mechanic_id)
    if m not in t.mechanics:
        return jsonify({'error': 'mechanic_not_assigned'}), 404
    t.mechanics.remove(m)
    db.session.commit()
    return service_ticket_schema.jsonify(t), 200
