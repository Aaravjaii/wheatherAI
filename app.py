import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
API_KEY = os.getenv("OPENWEATHER_API_KEY")

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    error = None

    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                weather = {
                    'city': city.title(),
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'].capitalize(),
                    'icon': data['weather'][0]['icon']
                }
            else:
                error = f"City '{city}' not found. Try again."

    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(debug=True)
