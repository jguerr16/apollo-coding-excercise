from db_setup import db

class Vehicle(db.Model):
    vin = db.Column(db.String(17), primary_key=True, unique=True, nullable=False)
    manufacturer = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    horse_power = db.Column(db.Integer, nullable=False)
    model_name = db.Column(db.String(80), nullable=False)
    model_year = db.Column(db.Integer, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    fuel_type = db.Column(db.String(50), nullable=False)

    def serialize(self):
        return {
            'vin': self.vin,
            'manufacturer': self.manufacturer,
            'description': self.description,
            'horse_power': self.horse_power,
            'model_name': self.model_name,
            'model_year': self.model_year,
            'purchase_price': self.purchase_price,
            'fuel_type': self.fuel_type
        }
