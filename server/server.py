from flask import Flask, request, jsonify
import util

app = Flask(__name__)

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    try:
        locations = util.get_location_names()
        response = jsonify({
            'locations': locations
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])

        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        response = jsonify({
            'estimated_price': estimated_price
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except KeyError as e:
        return jsonify({'error': f'Missing parameter: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': 'Invalid input data'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    try:
        util.load_saved_artifacts()
    except Exception as e:
        print(f"Error loading artifacts: {str(e)}")
        exit(1)
    
    app.run(debug=True)  # Use debug=True for development