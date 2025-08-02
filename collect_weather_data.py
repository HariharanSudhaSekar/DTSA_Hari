<<<<<<< HEAD
#!/usr/bin/env python3
=======
>>>>>>> 9d3298a0fc4471010b3582b13b777fa2be732a12
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

<<<<<<< HEAD
# Create a dummy Flask app just to get the SQLAlchemy context
app = Flask(__name__)
=======
# Create a minimal Flask app instance just for SQLAlchemy to connect
# This app is not run as a web server, but provides the context for DB operations
app = Flask(__name__)

# Configure the database URI
>>>>>>> 9d3298a0fc4471010b3582b13b777fa2be732a12
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'Weather.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
<<<<<<< HEAD
class Weather(db.Model):
    __tablename__ = "weather_data" 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entry_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # We might want to store more than just temperature, e.g., location, humidity
    temperature_celsius = db.Column(db.Float, nullable=False) # Changed to Float for decimal temperatures
    # Optional: Add columns for latitude and longitude if you want to store location
    # latitude = db.Column(db.Float)
    # longitude = db.Column(db.Float)
=======

# Define the Weather database model (MUST BE IDENTICAL TO src/app.py)
class Weather(db.Model):
    __tablename__ = "weather_data"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entry_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    temperature_celsius = db.Column(db.Float, nullable=False)
>>>>>>> 9d3298a0fc4471010b3582b13b777fa2be732a12

    def __repr__(self):
        return f"<Weather(Time: {self.entry_time}, Temp: {self.temperature_celsius}°C)>"

<<<<<<< HEAD
def get_temperature():
    # Open-Meteo API endpoint for current weather in London
    # You can change latitude and longitude for a different city
    API_URL = "https://api.open-meteo.com/v1/forecast?latitude=51.5074&longitude=0.1278&current_weather=true"
    response = requests.get(API_URL)
    response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

    data = response.json()

    # Access the temperature (in Celsius by default) from the current_weather object
    # The API returns 'temperature', not 'temp' or 'c'
    temperature = data["current_weather"]["temperature"]
    return temperature

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        try:
            current_temperature = get_temperature()
            new_entry = Weather(temperature_celsius=current_temperature) # Use the new column name
            db.session.add(new_entry)
            db.session.commit()
            print(f"Successfully added temperature {current_temperature}°C at {datetime.utcnow()} to Weather.sqlite3")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching temperature: {e}")
            db.session.rollback()
        except KeyError as e:
            print(f"Error parsing API response: {e}. Check API response structure.")
            print(f"Full response: {data}") # Print full data for debugging KeyError
            db.session.rollback()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            db.session.rollback()
=======
# Function to fetch temperature from Open-Meteo API
def get_temperature():
    # Using London's coordinates as an example (Latitude: 51.5074, Longitude: 0.1278)
    api_url = "https://api.open-meteo.com/v1/forecast?latitude=51.5074&longitude=0.1278&current_weather=true"
    
    try:
        response = requests.get(api_url, timeout=10) # Added a timeout
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        
        current_temperature = data['current_weather']['temperature']
        return current_temperature
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Open-Meteo API: {e}")
        return None

# Main execution block
if __name__ == "__main__":
    with app.app_context():
        # Ensure the database table exists (will create if it doesn't)
        db.create_all()

        current_temperature = get_temperature()

        if current_temperature is not None:
            new_weather_entry = Weather(temperature_celsius=current_temperature)
            db.session.add(new_weather_entry)
            try:
                db.session.commit()
                # DeprecationWarning fix: datetime.datetime.now(datetime.timezone.utc)
                print(f"Successfully added temperature {current_temperature}°C at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} to Weather.sqlite3")
            except Exception as e:
                db.session.rollback()
                print(f"Error saving data to database: {e}")
        else:
            print("Failed to get temperature, not saving to database.")
>>>>>>> 9d3298a0fc4471010b3582b13b777fa2be732a12
