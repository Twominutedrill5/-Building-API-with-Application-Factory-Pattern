 ############     Schemas
from app.extensions import ma
from app.models import Customer 
from app.models import Customer


class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        include_relationships = True
        load_instance = True
customer_schema = MemberSchema()
customers_schema = MemberSchema(many=True)