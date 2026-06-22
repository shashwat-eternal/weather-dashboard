# 🌤 Weather Dashboard

A Weather Analytics Dashboard built using **Python, Streamlit, Open-Meteo API, Pandas, and Matplotlib**. This application provides real-time weather information, 7-day forecasts, temperature trend analysis, and weather data visualization through an interactive web interface.

---

## 🚀 Features

* 🌍 Search weather by city name
* 🌡 Real-time temperature monitoring
* 💧 Humidity tracking
* 🌬 Wind speed information
* 📅 7-Day weather forecast
* 📊 Temperature trend visualization
* 📥 Export forecast data to CSV
* 📱 Interactive and user-friendly dashboard

---

## 🛠 Tech Stack

| Technology     | Purpose                      |
| -------------- | ---------------------------- |
| Python         | Core programming language    |
| Streamlit      | Web application framework    |
| Open-Meteo API | Weather data provider        |
| Pandas         | Data processing and analysis |
| Matplotlib     | Data visualization           |

---

## 📂 Project Structure

```text
weather-dashboard/
│
├── app.py
├── weather.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/shashwat-eternal/weather-dashboard.git
cd weather-dashboard
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will start locally at:

```text
http://localhost:8501
```

---

## 📊 Dashboard Preview

The dashboard displays:

* Current Temperature
* Relative Humidity
* Wind Speed
* 7-Day Forecast Table
* Temperature Trend Graph
* CSV Download Option

---

## 🔄 API Integration

This project uses the **Open-Meteo API** for weather forecasting and geolocation services.

### Geocoding API

Converts city names into geographic coordinates.

### Forecast API

Provides:

* Current weather conditions
* Temperature data
* Humidity data
* Wind speed data
* Daily forecast information

---

## 🎯 Learning Outcomes

Through this project, I learned:

* API Integration using Python
* JSON Data Processing
* Data Analysis with Pandas
* Data Visualization with Matplotlib
* Building Interactive Dashboards using Streamlit
* Version Control using Git & GitHub

---

## 🔮 Future Enhancements

* Air Quality Index (AQI)
* UV Index Monitoring
* Hourly Weather Forecast
* Weather Icons and Themes
* Multiple City Comparison
* Deployment on Streamlit Cloud
* Historical Weather Analytics

---

## 👨‍💻 Author

**Shashwat Shukla**

B.Tech CSE | Python Developer | Data Analytics Enthusiast

GitHub: https://github.com/shashwat-eternal
