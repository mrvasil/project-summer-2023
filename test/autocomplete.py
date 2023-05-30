from flask import Flask, request, render_template
import json

app = Flask(__name__)

CITIES = [
    'Moscow',
    "Saint Petersburg",
    'Ekaterinburg',
    'Magadan',
]

@app.route("/")
def root():
    return render_template('index.html')

@app.route("/search")
def search():
    query = request.args['query'].lower()
    filtered_cities = []
    for city in CITIES:
        if city.lower().startswith(query):
            filtered_cities.append(city)
    return json.dumps(filtered_cities)

app.run()
