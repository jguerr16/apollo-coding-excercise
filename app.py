from flask import Flask, jsonify, request
from db_setup import init_db, db
from models import Vehicle

app = Flask(__name__)
init_db(app)

@app.route('/vehicle', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([v.serialize() for v in vehicles]), 200

@app.route('/vehicle', methods=['POST'])
def add_vehicle():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON"}), 400

        # Check required fields
        required_fields = ['vin', 'manufacturer', 'horse_power', 'model_name', 'model_year', 'purchase_price', 'fuel_type']
        for field in required_fields:
            if field not in data or data[field] is None:
                return jsonify({"error": f"Missing field: {field}"}), 422

        vehicle = Vehicle(**data)
        db.session.add(vehicle)
        db.session.commit()
        return jsonify(vehicle.serialize()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/vehicle/<vin>', methods=['GET'])
def get_vehicle(vin):
    vehicle = Vehicle.query.get(vin)
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    return jsonify(vehicle.serialize()), 200

@app.route('/vehicle/<vin>', methods=['PUT'])
def update_vehicle(vin):
    vehicle = Vehicle.query.get(vin)
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    try:
        data = request.get_json()
        for key, value in data.items():
            setattr(vehicle, key, value)
        db.session.commit()
        return jsonify(vehicle.serialize()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/vehicle/<vin>', methods=['DELETE'])
def delete_vehicle(vin):
    vehicle = Vehicle.query.get(vin)
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    db.session.delete(vehicle)
    db.session.commit()
    return '', 204

if __name__ == "__main__":
    app.run(debug=True)
