from infrastructure.databases.mssql import init_mssql
from infrastructure.models import pods_model, roles_model,bookings_model, users_model,locations_model

def init_db(app):
    init_mssql(app)
    
from infrastructure.databases.mssql import Base