from flask import Flask, jsonify, request
from flask_cors import CORS
from weather_api import fetch_current_weather

app = Flask(__name__)
CORS(app)

@app.route('/weather', methods=['GET'])
def get_weather():
    cities = request.args.get('cities', '').split(',')
    weather_data = {}
    for city in cities:
        weather_data[city] = fetch_current_weather(city)
    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(debug=True)