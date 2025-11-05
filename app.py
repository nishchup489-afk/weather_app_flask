from flask import Flask, request, url_for , render_template , redirect
from datetime import datetime
from PIL import Image, ImageTk
from dotenv import load_dotenv
import os
app = Flask(__name__)



load_dotenv()
API = os.getenv("OPENWEATHER_API_KEY")



@app.route('/' , methods=['POST' , 'GET'])
def homepage():
    if request.method  == 'POST':
        return redirect(url_for('home'))
    else:
        return render_template('homepage.html')
    
@app.route('/create_account' , methods=['POST' , 'GET'])
def ca():
    return render_template('result.html')

@app.route('/result', methods=['POST' , 'GET'])
def home():
    city = None
    weather = None
    weather_url = None
    error_messege = None
    time = None
    country = None
    flag = None
    sunset = None
    sunrise = None
    country_name = None
    
    if request.method == 'POST':
        city = request.form.get('city_name')
        if city:
            import requests
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API}"
            geo_response = requests.get(geo_url).json()
            if geo_response:
                 lat = geo_response[0]['lat']
                 lon = geo_response[0]['lon']
                 weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API}&units=metric"
                 weather = requests.get(weather_url).json()
                 tz_offset = weather.get('timezone' , 0)
                 sunrise_utc = weather['sys']['sunrise']
                 sunset_utc  = weather['sys']['sunset']
                 sunrise = datetime.utcfromtimestamp(sunrise_utc + tz_offset).strftime("%I : %M : %S %p")
                 sunset  = datetime.utcfromtimestamp(sunset_utc + tz_offset).strftime("%I : %M : %S %p")
                 country = weather['sys']['country']
                 flag = f"https://flagcdn.com/w80/{country.lower()}.png"

                 if country:
                    country_name_get_url = f"https://restcountries.com/v3.1/alpha/{country}"
                    country_name_get = requests.get(country_name_get_url).json()
                    country_name = (country_name_get[0]['name']['common'])
                    country_name = country_name.title() if country_name.islower() else country_name
  
                 else:
                     country_name = {}
                 if not weather:
                    weather = {}
            else:
                error_messege = f"{city} not found"
        else:
            error_messege = f"{city} not found"
            

    return render_template("index.html" , country_name = country_name ,flag = flag ,  sunset = sunset , sunrise = sunrise ,city_name = city , weather_url = weather_url , weather = weather , error_messege=error_messege)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run( host='0.0.0.0', port=port)