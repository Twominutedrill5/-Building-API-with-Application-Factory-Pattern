from datetime import date
from app.extensions import db

# ── Join table (Many-to-Many: mechanics ↔ service_tickets) ──────────────────
mechanic_tickets = db.Table(
    'mechanic_tickets',
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanics.mechanic_id'), primary_key=True),
    db.Column('ticket_id',   db.Integer, db.ForeignKey('service_tickets.ticket_id'), primary_key=True)
)

# ── Customer ─────────────────────────────────────────────────────────────────
class Customer(db.Model):
    __tablename__ = 'customers'

    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name  = db.Column(db.String(50),  nullable=False)
    last_name   = db.Column(db.String(50),  nullable=False)
    email       = db.Column(db.String(100), nullable=False, unique=True)
    phone       = db.Column(db.String(20))
    address     = db.Column(db.String(200))

    vehicles = db.relationship('Vehicle', back_populates='customer', cascade='all, delete-orphan')

# ── Vehicle ───────────────────────────────────────────────────────────────────
class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    vehicle_id  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    vin         = db.Column(db.String(17), nullable=False, unique=True)
    year        = db.Column(db.Integer,    nullable=False)
    make        = db.Column(db.String(50), nullable=False)
    model       = db.Column(db.String(50), nullable=False)

    customer        = db.relationship('Customer', back_populates='vehicles')
    service_tickets = db.relationship('ServiceTicket', back_populates='vehicle', cascade='all, delete-orphan')

# ── ServiceTicket ─────────────────────────────────────────────────────────────
class ServiceTicket(db.Model):
    __tablename__ = 'service_tickets'

    ticket_id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vehicle_id   = db.Column(db.Integer, db.ForeignKey('vehicles.vehicle_id'), nullable=False)
    service_date = db.Column(db.Date,    nullable=False, default=date.today)
    service_desc = db.Column(db.Text,    nullable=False)
    price        = db.Column(db.Float)
    status       = db.Column(db.String(20), default='pending')

    vehicle   = db.relationship('Vehicle', back_populates='service_tickets')
    mechanics = db.relationship('Mechanic', secondary=mechanic_tickets, back_populates='service_tickets')

# ── Mechanic ──────────────────────────────────────────────────────────────────
class Mechanic(db.Model):
    __tablename__ = 'mechanics'

    mechanic_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name        = db.Column(db.String(100), nullable=False)
    email       = db.Column(db.String(100), nullable=False, unique=True)
    phone       = db.Column(db.String(20))
    address     = db.Column(db.String(200))
    salary      = db.Column(db.Float)

    service_tickets = db.relationship('ServiceTicket', secondary=mechanic_tickets, back_populates='mechanics')