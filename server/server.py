from flask import Flask, request, jsonify
from flask_cors import CORS
import util
import os

app = Flask(__name__)
CORS(app)

# Ensure artifacts are loaded at the start
util.load_saved_artifacts()

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    return response

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        data = request.get_json()
        total_sqft = float(data['total_sqft'])
        location = data['location']
        beds = int(data['beds'])
        bath = int(data['bath'])

        estimated_price = util.get_estimated_price(location, total_sqft, beds, bath)

        response = jsonify({
            'estimated_price': estimated_price
        })
        return response

    except KeyError as e:
        return jsonify({'error': f'Missing parameter: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': f'Invalid data type for parameter: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import util

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Ensure artifacts are loaded at the start
# util.load_saved_artifacts()

# @app.route('/get_location_names', methods=['GET'])
# def get_location_names():
#     response = jsonify({
#         'locations': util.get_location_names()
#     })
#     response.headers.add('Access-Control-Allow-Origin', '*')

#     return response

# @app.route('/predict_home_price', methods=['POST'])
# def predict_home_price():
#     if request.is_json:  # If the content type is JSON
#         data = request.get_json()
#         try:
#             total_sqft = float(data['total_sqft'])
#             location = data['location']
#             beds = int(data['beds'])
#             bath = int(data['bath'])
#         except (KeyError, ValueError) as e:
#             return jsonify({'error': f'Invalid data: {str(e)}'}), 400
#     else:  # Handle form-data
#         try:
#             total_sqft = float(request.form['total_sqft'])
#             location = request.form['location']
#             beds = int(request.form['beds'])
#             bath = int(request.form['bath'])
#         except (KeyError, ValueError) as e:
#             return jsonify({'error': f'Invalid data: {str(e)}'}), 400

#     response = jsonify({
#         'estimated_price': util.get_estimated_price(location, total_sqft, beds, bath)
#     })
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response



# if __name__ == "__main__":
#     print("Starting Python Flask Server For Home Price Prediction...")
#     print("Available locations:", util.get_location_names())  # Ensure locations are loaded
#     app.run(debug=True)

