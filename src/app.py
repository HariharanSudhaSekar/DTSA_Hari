#!/usr/bin/env python3

from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import requests

app = Flask(__name__)

# Configure the database URI for the weather data
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(base_dir), 'Weather.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Weather database model (MUST BE IDENTICAL TO collect_weather_data.py)
class Weather(db.Model):
    __tablename__ = "weather_data"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entry_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    temperature_celsius = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Weather(Time: {self.entry_time}, Temp: {self.temperature_celsius}°C)>"

# --- Web Application Routes ---

@app.route("/")
def index():
    # Fetch the latest temperature
    latest_temp_entry = Weather.query.order_by(Weather.entry_time.desc()).first()
    latest_temp = latest_temp_entry.temperature_celsius if latest_temp_entry else "N/A"
    latest_time = latest_temp_entry.entry_time.strftime("%Y-%m-%d %H:%M:%S") if latest_temp_entry else "N/A"

    # Fetch all historical temperatures for analysis (e.g., last 50 entries)
    all_historical_temps = Weather.query.order_by(Weather.entry_time.desc()).limit(50).all()

    # --- Data Analysis ---
    average_temp = "N/A"
    if all_historical_temps:
        temperatures_list = [entry.temperature_celsius for entry in all_historical_temps]
        if temperatures_list:
            average_temp = round(sum(temperatures_list) / len(temperatures_list), 2)
        else:
            average_temp = "No data for average"

    # Fetch only the 10 most recent for display in the list
    display_historical_temps = Weather.query.order_by(Weather.entry_time.desc()).limit(10).all()

    # Generate HTML using a simple string template
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Weather Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f4; color: #333; }}
            .container {{ max-width: 800px; margin: auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            h1 {{ color: #0056b3; text-align: center; margin-bottom: 30px; }}
            h2 {{ color: #0056b3; border-bottom: 1px solid #eee; padding-bottom: 5px; margin-top: 25px; }}
            .current-temp-section {{ text-align: center; margin-bottom: 25px; }}
            .current-temp {{ font-size: 3em; color: #dc3545; font-weight: bold; }}
            .timestamp {{ font-size: 0.9em; color: #6c757d; display: block; margin-top: 5px; }}
            .analysis {{ font-size: 1.2em; color: #28a745; margin-top: 15px; text-align: center; border: 1px solid #e9ecef; padding: 10px; border-radius: 5px; background-color: #eafbea; }}
            ul {{ list-style-type: none; padding: 0; }}
            li {{ margin-bottom: 8px; padding: 10px; border: 1px solid #e9ecef; background-color: #f8f9fa; border-radius: 4px; display: flex; justify-content: space-between; align-items: center; }}
            li span.temp {{ font-weight: bold; color: #007bff; }}
            .health-link {{ margin-top: 25px; display: block; text-align: center; color: #007bff; text-decoration: none; }}
            .health-link:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Simple Weather Dashboard</h1>
            
            <div class="current-temp-section">
                <h2>Current Temperature:</h2>
                <p class="current-temp">{latest_temp}°C</p>
                <p class="timestamp">As of: {latest_time} (UTC)</p>
            </div>

            <div class="analysis">
                <h2>Analysis:</h2>
                <p>Average of last {len(all_historical_temps) if all_historical_temps else 0} recorded temperatures: {average_temp}°C</p>
            </div>

            <div>
                <h2>Recent Readings:</h2>
                <ul>