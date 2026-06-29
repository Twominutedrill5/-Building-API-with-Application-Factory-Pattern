from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Mechanic
from .schemas import mechanic_schema, mechanics_schema
from app.extensions import limiter, cache

mechanics_bp = Blueprint('mechanics', __name__)


@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    data = request.get_json() or {}
    required = ['name', 'email']
    missing = [k for k in required if not data.get(k)]
    if missing:
        return jsonify({'error': 'missing_fields', 'missing': missing}), 400
    if Mechanic.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'email_exists'}), 409

    mechanic = Mechanic(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        address=data.get('address'),
        salary=data.get('salary')
    )
    db.session.add(mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 201


@mechanics_bp.route('/', methods=['GET'])
@cache.cached(timeout=60)  # Cache the response for 60 seconds
@limiter.limit("3 per hour")
def get_mechanics():
    return mechanics_schema.jsonify(Mechanic.query.all()), 200


@mechanics_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    m = Mechanic.query.get_or_404(id)
    data = request.get_json() or {}
    m.name = data.get('name', m.name)
    m.email = data.get('email', m.email)
    m.phone = data.get('phone', m.phone)
    m.address = data.get('address', m.address)
    m.salary = data.get('salary', m.salary)
    db.session.commit()
    return mechanic_schema.jsonify(m), 200


@mechanics_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    m = Mechanic.query.get_or_404(id)
    db.session.delete(m)
    db.session.commit()
    return jsonify({'message': f'Mechanic {id} deleted.'}), 200
