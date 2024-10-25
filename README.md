# City Weather Dashboard with Streamlit

A real-time, interactive weather dashboard built using **Python** and **Streamlit**. This app allows users to enter a city name and get real-time weather updates, including temperature, humidity, and wind speed, for the next 12 to 48 hours. The data is pulled from the **Open-Meteo** API, with city name geolocation provided by **Nominatim (OpenStreetMap)**.

![Weather Dashboard Screenshot](Screenshot.png)

## 📋 Features

- **Real-Time Weather Data**: Fetches hourly temperature, humidity, and wind speed data.
- **City Search**: Users can enter any city name to get weather data.
- **Customizable Graphs**: Select forecast duration and display only chosen weather parameters.
- **Clean Summary View**: Presents the latest temperature, humidity, and wind speed in a metric format.

## 🚀 Getting Started

### Prerequisites

Ensure you have **Python 3.7+** and **pip** installed.

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/manikolbe/city_weather_dashboard_streamlit_example.git
   cd city_weather_dashboard_streamlit_example
   ```

2. **Install Required Packages**

   ```bash
   pip install -r requirements.txt
   ```

   > **Note**: If there’s no `requirements.txt`, create one by listing the dependencies:
   >
   > ```plaintext
   > streamlit
   > requests
   > pandas
   > ```

### Run the App

In the project directory, run:

```bash
streamlit run city_weather_dashboard.py
```

The app will open in a new browser tab at `http://localhost:8501`.

## 🌎 Usage

1. **Enter a City Name**: Type the city name (e.g., "San Francisco") in the input field.
2. **Select Forecast Duration**: Use the slider to choose between 12 to 48 hours.
3. **Choose Parameters**: Select which weather metrics to display: temperature, humidity, or wind speed.
4. **Get Results**: Press "Get Weather Data" to fetch and display data.

The app will show:

- Line charts for each selected metric over the chosen duration.
- A real-time summary of the current temperature, humidity, and wind speed.

## 📚 Project Structure

- **weather_dashboard.py**: Main app code.
- **requirements.txt**: List of Python dependencies.
- **README.md**: Project documentation.

## 📦 APIs Used

- **[Open-Meteo API](https://open-meteo.com/)**: For real-time weather data.
- **[Nominatim API (OpenStreetMap)](https://nominatim.org/)**: For converting city names to coordinates.

## 🎉 Acknowledgments

- **OpenStreetMap & Nominatim** for their free and open geolocation API.
- **Open-Meteo** for providing real-time weather data.

## 🙌 Contributions

Feel free to open issues or submit pull requests if you’d like to contribute or suggest improvements!
