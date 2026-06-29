from flask import Blueprint, jsonify, request   # removed 'app' — it's not importable from flask
from app.models import Customer, Vehicle, ServiceTicket, Mechanic
from app.extensions import db
from .schemas import customer_schema, customers_schema

members_bp = Blueprint('members', __name__)     # define it here only, never import it into itself


@members_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'})

# ── CUSTOMERS ─────────────────────────────────────────────────────────────────

@members_bp.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json() or {}
    required = ['first_name', 'last_name', 'email']
    missing = [k for k in required if not data.get(k)]
    if missing:
        return jsonify({'error': 'missing_fields', 'missing': missing}), 400
    if Customer.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'email_exists'}), 409
    customer = Customer(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data.get('phone'),
        address=data.get('address')
    )
    db.session.add(customer)
    db.session.commit()
    return customer_schema.jsonify(customer), 201

@members_bp.route('/customers', methods=['GET'])
def get_customers():
    return customers_schema.jsonify(Customer.query.all()), 200

@members_bp.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    return customer_schema.jsonify(Customer.query.get_or_404(customer_id)), 200

@members_bp.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    c = Customer.query.get_or_404(customer_id)
    data = request.get_json() or {}
    c.first_name = data.get('first_name', c.first_name)
    c.last_name  = data.get('last_name',  c.last_name)
    c.email      = data.get('email',      c.email)
    c.phone      = data.get('phone',      c.phone)
    c.address    = data.get('address',    c.address)
    db.session.commit()
    return customer_schema.jsonify(c), 200

@members_bp.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    c = Customer.query.get_or_404(customer_id)
    db.session.delete(c)
    db.session.commit()
    return jsonify({'message': f'Customer {customer_id} deleted.'}), 200

# ── VEHICLES ──────────────────────────────────────────────────────────────────

@members_bp.route('/vehicles', methods=['POST'])
def create_vehicle():
    data = request.get_json() or {}
    required = ['customer_id', 'vin', 'year', 'make', 'model']
    missing = [k for k in required if not data.get(k)]
    if missing:
        return jsonify({'error': 'missing_fields', 'missing': missing}), 400
    if not Customer.query.get(data['customer_id']):
        return jsonify({'error': 'customer_not_found'}), 404
    if Vehicle.query.filter_by(vin=data['vin']).first():
        return jsonify({'error': 'vin_already_exists'}), 409
    vehicle = Vehicle(
        customer_id=data['customer_id'],
        vin=data['vin'], year=data['year'],
        make=data['make'], model=data['model']
    )
    db.session.add(vehicle)
    db.session.commit()
    return jsonify({'vehicle_id': vehicle.vehicle_id}), 201

@members_bp.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([{
        'vehicle_id': v.vehicle_id, 'customer_id': v.customer_id,
        'vin': v.vin, 'year': v.year, 'make': v.make, 'model': v.model
    } for v in vehicles]), 200

@members_bp.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    v = Vehicle.query.get_or_404(vehicle_id)
    return jsonify({
        'vehicle_id': v.vehicle_id, 'customer_id': v.customer_id,
        'vin': v.vin, 'year': v.year, 'make': v.make, 'model': v.model
    }), 200

@members_bp.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    v = Vehicle.query.get_or_404(vehicle_id)
    data = request.get_json() or {}
    v.vin   = data.get('vin',   v.vin)
    v.year  = data.get('year',  v.year)
    v.make  = data.get('make',  v.make)
    v.model = data.get('model', v.model)
    db.session.commit()
    return jsonify({'message': f'Vehicle {vehicle_id} updated.'}), 200

@members_bp.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    v = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(v)
    db.session.commit()
    return jsonify({'message': f'Vehicle {vehicle_id} deleted.'}), 200

# ── MECHANICS ─────────────────────────────────────────────────────────────────

@members_bp.route('/mechanics', methods=['POST'])
def create_mechanic():
    data = request.get_json() or {}
    required = ['name', 'email']
    missing = [k for k in required if not data.get(k)]
    if missing:
        return jsonify({'error': 'missing_fields', 'missing': missing}), 400
    if Mechanic.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'email_exists'}), 409
    mechanic = Mechanic(
        name=data['name'], email=data['email'],
        phone=data.get('phone'), address=data.get('address'), salary=data.get('salary')
    )
    db.session.add(mechanic)
    db.session.commit()
    return jsonify({'mechanic_id': mechanic.mechanic_id}), 201

@members_bp.route('/mechanics', methods=['GET'])
def get_mechanics():
    mechanics = Mechanic.query.all()
    return jsonify([{
        'mechanic_id': m.mechanic_id, 'name': m.name, 'email': m.email,
        'phone': m.phone, 'address': m.address, 'salary': m.salary
    } for m in mechanics]), 200

@members_bp.route('/mechanics/<int:mechanic_id>', methods=['GET'])
def get_mechanic(mechanic_id):
    m = Mechanic.query.get_or_404(mechanic_id)
    return jsonify({
        'mechanic_id': m.mechanic_id, 'name': m.name, 'email': m.email,
        'phone': m.phone, 'address': m.address, 'salary': m.salary
    }), 200

@members_bp.route('/mechanics/<int:mechanic_id>', methods=['PUT'])
def update_mechanic(mechanic_id):
    m = Mechanic.query.get_or_404(mechanic_id)
    data = request.get_json() or {}
    m.name    = data.get('name',    m.name)
    m.email   = data.get('email',   m.email)
    m.phone   = data.get('phone',   m.phone)
    m.address = data.get('address', m.address)
    m.salary  = data.get('salary',  m.salary)
    db.session.commit()
    return jsonify({'message': f'Mechanic {mechanic_id} updated.'}), 200

@members_bp.route('/mechanics/<int:mechanic_id>', methods=['DELETE'])
def delete_mechanic(mechanic_id):
    m = Mechanic.query.get_or_404(mechanic_id)
    db.session.delete(m)
    db.session.commit()
    return jsonify({'message': f'Mechanic {mechanic_id} deleted.'}), 200

# ── SERVICE TICKETS ───────────────────────────────────────────────────────────

@members_bp.route('/service_tickets', methods=['POST'])
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
    return jsonify({'ticket_id': ticket.ticket_id}), 201

@members_bp.route('/service_tickets', methods=['GET'])
def get_service_tickets():
    tickets = ServiceTicket.query.all()
    return jsonify([{
        'ticket_id': t.ticket_id, 'vehicle_id': t.vehicle_id,
        'service_date': str(t.service_date), 'service_desc': t.service_desc,
        'price': t.price, 'status': t.status,
        'mechanics': [{'mechanic_id': m.mechanic_id, 'name': m.name} for m in t.mechanics]
    } for t in tickets]), 200

@members_bp.route('/service_tickets/<int:ticket_id>', methods=['GET'])
def get_service_ticket(ticket_id):
    t = ServiceTicket.query.get_or_404(ticket_id)
    return jsonify({
        'ticket_id': t.ticket_id, 'vehicle_id': t.vehicle_id,
        'service_date': str(t.service_date), 'service_desc': t.service_desc,
        'price': t.price, 'status': t.status,
        'mechanics': [{'mechanic_id': m.mechanic_id, 'name': m.name} for m in t.mechanics]
    }), 200

@members_bp.route('/service_tickets/<int:ticket_id>', methods=['PUT'])
def update_service_ticket(ticket_id):
    t = ServiceTicket.query.get_or_404(ticket_id)
    data = request.get_json() or {}
    t.service_desc = data.get('service_desc', t.service_desc)
    t.price        = data.get('price',        t.price)
    t.status       = data.get('status',       t.status)
    if 'mechanic_ids' in data:
        t.mechanics = Mechanic.query.filter(Mechanic.mechanic_id.in_(data['mechanic_ids'])).all()
    db.session.commit()
    return jsonify({'message': f'Ticket {ticket_id} updated.'}), 200

@members_bp.route('/service_tickets/<int:ticket_id>', methods=['DELETE'])
def delete_service_ticket(ticket_id):
    t = ServiceTicket.query.get_or_404(ticket_id)
    db.session.delete(t)
    db.session.commit()
    return jsonify({'message': f'Ticket {ticket_id} deleted.'}), 200

@members_bp.route('/service_tickets/<int:ticket_id>/mechanics/<int:mechanic_id>', methods=['POST'])
def assign_mechanic(ticket_id, mechanic_id):
    t = ServiceTicket.query.get_or_404(ticket_id)
    m = Mechanic.query.get_or_404(mechanic_id)
    if m in t.mechanics:
        return jsonify({'error': 'mechanic_already_assigned'}), 409
    t.mechanics.append(m)
    db.session.commit()
    return jsonify({'message': f'Mechanic {mechanic_id} assigned to ticket {ticket_id}.'}), 200

@members_bp.route('/service_tickets/<int:ticket_id>/mechanics/<int:mechanic_id>', methods=['DELETE'])
def remove_mechanic(ticket_id, mechanic_id):
    t = ServiceTicket.query.get_or_404(ticket_id)
    m = Mechanic.query.get_or_404(mechanic_id)
    if m not in t.mechanics:
        return jsonify({'error': 'mechanic_not_assigned'}), 404
    t.mechanics.remove(m)
    db.session.commit()
    return jsonify({'message': f'Mechanic {mechanic_id} removed from ticket {ticket_id}.'}), 200