import dash
from dash import dcc, html, Input, Output
import requests
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objs as go

# Function to get coordinates from city name using Nominatim
def get_coordinates(city_name):
    url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json&limit=1"
    headers = {
        "User-Agent": "WeatherDashboardApp/1.0 (contact@example.com)"  # Replace with your app name and contact info
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        location_data = response.json()
        if location_data:
            location = location_data[0]
            return float(location['lat']), float(location['lon'])
        else:
            return None, None
    else:
        return None, None

# Function to get weather data from Open-Meteo
def get_weather_data(lat, lon, hours):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m&forecast_days=2"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Dash app initialization
app = dash.Dash(__name__)
app.title = "Real-Time Weather Dashboard"
app.external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# App layout
app.layout = html.Div([
    html.Div(
        className="banner",
        children=[
            html.H1("Real-Time Weather Dashboard", style={'textAlign': 'center', 'color': '#ffffff'}),
            html.P("Get real-time weather updates and visualize temperature, humidity, and wind speed trends by city.",
                   style={'textAlign': 'center', 'color': '#ffffff'})
        ],
        style={
            'backgroundColor': '#212A31',
            'padding': '10px'
        }
    ),
    html.Div(
        className="user-input",
        children=[
            html.Div([
                html.Label("Enter City Name", style={'fontWeight': 'bold'}),
                dcc.Input(id='city-name', type='text', value='San Francisco', style={'width': '100%'}),
            ], style={'margin-bottom': '20px'}),
            html.Div([
                html.Label("Select forecast duration (hours)", style={'fontWeight': 'bold'}),
                dcc.Slider(id='forecast-duration', min=12, max=48, value=24, step=12,
                           marks={12: '12h', 24: '24h', 36: '36h', 48: '48h'},
                           tooltip={'always_visible': True, 'placement': 'bottom'})
            ], style={'margin-bottom': '20px'}),
            html.Div([
                html.Label("Choose weather parameters to display:", style={'fontWeight': 'bold'}),
                dcc.Checklist(id='parameter-options',
                              options=[
                                  {'label': "Temperature (°C)", 'value': "Temperature (°C)"},
                                  {'label': "Humidity (%)", 'value': "Humidity (%)"},
                                  {'label': "Wind Speed (m/s)", 'value': "Wind Speed (m/s)"}
                              ],
                              value=["Temperature (°C)", "Humidity (%)"],
                              inputStyle={'margin-right': '5px', 'margin-left': '10px'})
            ], style={'margin-bottom': '20px'}),
            html.Button('Get Weather Data', id='get-weather-data', n_clicks=0,
                        style={'backgroundColor': '#212A31', 'color': '#ffffff', 'fontWeight': 'bold', 'border': 'none', 'padding': '10px 20px', 'cursor': 'pointer'})
        ],
        style={
            'backgroundColor': '#f9f9f9',
            'padding': '20px',
            'borderRadius': '10px',
            'boxShadow': '0px 0px 15px rgba(0, 0, 0, 0.1)'
        }
    ),
    html.Div(id='current-weather-summary', style={'margin-top': '20px'}),
    html.Div(id='temperature-graph', style={'margin-top': '20px'}),
    html.Div(id='humidity-graph', style={'margin-top': '20px'}),
    html.Div(id='wind-speed-graph', style={'margin-top': '20px'})
], style={'maxWidth': '800px', 'margin': '0 auto'})

# Callback to update weather data
@app.callback(
    [Output('current-weather-summary', 'children'),
     Output('temperature-graph', 'children'),
     Output('humidity-graph', 'children'),
     Output('wind-speed-graph', 'children')],
    [Input('get-weather-data', 'n_clicks')],
    [Input('city-name', 'value'),
     Input('forecast-duration', 'value'),
     Input('parameter-options', 'value')]
)
def update_weather(n_clicks, city_name, forecast_duration, parameter_options):
    if n_clicks > 0:
        lat, lon = get_coordinates(city_name)
        if lat is not None and lon is not None:
            data = get_weather_data(lat, lon, forecast_duration)
            if data:
                times = [datetime.now() + timedelta(hours=i) for i in range(forecast_duration)]
                df = pd.DataFrame({"Time": times})

                # Current weather summary
                current_summary = html.Div([
                    html.H3("Current Weather Summary", style={'textAlign': 'center', 'color': '#212A31'}),
                    html.Div([
                        html.Div([html.H4("✨ Temperature"), html.P(f"{data['hourly']['temperature_2m'][0]} °C")],
                                 style={'textAlign': 'center','display': 'inline-block', 'margin-right': '20px', 'backgroundColor': '#f9f9f9', 'padding': '10px', 'borderRadius': '10px', 'boxShadow': '0px 0px 10px rgba(0, 0, 0, 0.1)'}),
                        html.Div([html.H4("💧 Humidity"), html.P(f"{data['hourly']['relative_humidity_2m'][0]} %")],
                                 style={'textAlign': 'center','display': 'inline-block', 'margin-right': '20px', 'backgroundColor': '#f9f9f9', 'padding': '10px', 'borderRadius': '10px', 'boxShadow': '0px 0px 10px rgba(0, 0, 0, 0.1)'}),
                        html.Div([html.H4("🌬️ Wind Speed"), html.P(f"{data['hourly']['wind_speed_10m'][0]} m/s")],
                                 style={'textAlign': 'center','display': 'inline-block', 'backgroundColor': '#f9f9f9', 'padding': '10px', 'borderRadius': '10px', 'boxShadow': '0px 0px 10px rgba(0, 0, 0, 0.1)'})
                    ], style={'textAlign': 'center'})
                ])

                # Temperature graph
                temperature_graph = html.Div()
                if "Temperature (°C)" in parameter_options:
                    df["Temperature (°C)"] = data['hourly']['temperature_2m'][:forecast_duration]
                    temperature_graph = dcc.Graph(
                        figure={
                            'data': [go.Scatter(x=df['Time'], y=df["Temperature (°C)"], mode='lines', name='Temperature (°C)', line=dict(color='#212A31', width=2))],
                            'layout': go.Layout(title='Temperature Forecast', xaxis={'title': 'Time'}, yaxis={'title': 'Temperature (°C'},
                                                paper_bgcolor='#f9f9f9', plot_bgcolor='#f9f9f9',
                                                xaxis_tickangle=-45, title_x=0.5, title_font={'size': 24, 'color': '#212A31'})
                        }
                    )

                # Humidity graph
                humidity_graph = html.Div()
                if "Humidity (%)" in parameter_options:
                    df["Humidity (%)"] = data['hourly']['relative_humidity_2m'][:forecast_duration]
                    humidity_graph = dcc.Graph(
                        figure={
                            'data': [go.Scatter(x=df['Time'], y=df["Humidity (%)"], mode='lines', name='Humidity (%)', line=dict(color='#ff7f0e', width=2))],
                            'layout': go.Layout(title='Humidity Forecast', xaxis={'title': 'Time'}, yaxis={'title': 'Humidity'},
                                                paper_bgcolor='#f9f9f9', plot_bgcolor='#f9f9f9',
                                                xaxis_tickangle=-45, title_x=0.5, title_font={'size': 24, 'color': '#212A31'})
                        }
                    )

                # Wind speed graph
                wind_speed_graph = html.Div()
                if "Wind Speed (m/s)" in parameter_options:
                    df["Wind Speed (m/s)"] = data['hourly']['wind_speed_10m'][:forecast_duration]
                    wind_speed_graph = dcc.Graph(
                        figure={
                            'data': [go.Scatter(x=df['Time'], y=df["Wind Speed (m/s)"], mode='lines', name='Wind Speed (m/s)', line=dict(color='#2ca02c', width=2))],
                            'layout': go.Layout(title='Wind Speed Forecast', xaxis={'title': 'Time'}, yaxis={'title': 'Wind Speed'},
                                                paper_bgcolor='#f9f9f9', plot_bgcolor='#f9f9f9',
                                                xaxis_tickangle=-45, title_x=0.5, title_font={'size': 24, 'color': '#212A31'})
                        }
                    )

                return current_summary, temperature_graph, humidity_graph, wind_speed_graph
    return html.Div(), html.Div(), html.Div(), html.Div()

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
