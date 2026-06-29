from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Customer, Vehicle
from .schemas import customer_schema, customers_schema

customers_bp = Blueprint('customers', __name__)


@customers_bp.route('/', methods=['POST'])
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


@customers_bp.route('/', methods=['GET'])
def get_customers():
    return customers_schema.jsonify(Customer.query.all()), 200


@customers_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    return customer_schema.jsonify(Customer.query.get_or_404(customer_id)), 200


@customers_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    c = Customer.query.get_or_404(customer_id)
    data = request.get_json() or {}
    c.first_name = data.get('first_name', c.first_name)
    c.last_name = data.get('last_name', c.last_name)
    c.email = data.get('email', c.email)
    c.phone = data.get('phone', c.phone)
    c.address = data.get('address', c.address)
    db.session.commit()
    return customer_schema.jsonify(c), 200


@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    c = Customer.query.get_or_404(customer_id)
    db.session.delete(c)
    db.session.commit()
    return jsonify({'message': f'Customer {customer_id} deleted.'}), 200


@customers_bp.route('/vehicles', methods=['POST'])
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
        vin=data['vin'],
        year=data['year'],
        make=data['make'],
        model=data['model']
    )
    db.session.add(vehicle)
    db.session.commit()
    return jsonify({'vehicle_id': vehicle.vehicle_id}), 201


@customers_bp.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([{
        'vehicle_id': v.vehicle_id,
        'customer_id': v.customer_id,
        'vin': v.vin,
        'year': v.year,
        'make': v.make,
        'model': v.model
    } for v in vehicles]), 200


@customers_bp.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    v = Vehicle.query.get_or_404(vehicle_id)
    return jsonify({
        'vehicle_id': v.vehicle_id,
        'customer_id': v.customer_id,
        'vin': v.vin,
        'year': v.year,
        'make': v.make,
        'model': v.model
    }), 200


@customers_bp.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    v = Vehicle.query.get_or_404(vehicle_id)
    data = request.get_json() or {}
    v.vin = data.get('vin', v.vin)
    v.year = data.get('year', v.year)
    v.make = data.get('make', v.make)
    v.model = data.get('model', v.model)
    db.session.commit()
    return jsonify({'message': f'Vehicle {vehicle_id} updated.'}), 200


@customers_bp.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    v = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(v)
    db.session.commit()
    return jsonify({'message': f'Vehicle {vehicle_id} deleted.'}), 200
