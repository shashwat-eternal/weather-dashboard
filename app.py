import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from weather import (
    get_location,
    get_weather_data,
    weather_code_to_text,
    weather_code_to_icon,
    build_hourly_dataframe,
    build_daily_dataframe
)

st.set_page_config(
    page_title="Premium Weather Dashboard",
    page_icon="🌦️",
    layout="wide"
)

# ---------- Premium CSS ----------
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1350px;
}
.hero-card {
    background: linear-gradient(135deg, #1d4ed8, #7c3aed);
    border-radius: 22px;
    padding: 26px 30px;
    color: white;
    box-shadow: 0 18px 45px rgba(0,0,0,0.18);
    margin-bottom: 20px;
}
.metric-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}
.section-card {
    background: #111827;
    border-radius: 20px;
    padding: 22px;
    color: white;
    box-shadow: 0 16px 40px rgba(0,0,0,0.18);
    margin-top: 18px;
}
.small-label {
    font-size: 13px;
    opacity: 0.85;
}
.big-temp {
    font-size: 48px;
    font-weight: 800;
    line-height: 1.1;
}
.city-chip {
    display:inline-block;
    padding:8px 14px;
    background:#1f2937;
    border-radius:999px;
    margin-right:8px;
    margin-bottom:8px;
    color:white;
    font-size:14px;
}
.forecast-card {
    background: #0f172a;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 16px;
    text-align: center;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
st.sidebar.title("🌦️ Weather Dashboard")
st.sidebar.write("Premium weather analytics using **Open-Meteo API**")

quick_cities = ["Lucknow", "Delhi", "Mumbai", "Bangalore", "London", "New York"]
selected_quick_city = st.sidebar.selectbox("Quick City", [""] + quick_cities)

default_city = "Lucknow"
city_input = st.sidebar.text_input("Search city", value=selected_quick_city or default_city)

st.sidebar.markdown("---")
st.sidebar.markdown("### Features")
st.sidebar.markdown("""
- Current weather overview  
- 24-hour forecast  
- 7-day forecast  
- Weather charts  
- CSV export  
""")

# ---------- Fetch weather ----------
city = city_input.strip()

if not city:
    st.warning("Please enter a city name.")
    st.stop()

location = get_location(city)

if not location:
    st.error("City not found. Try another city.")
    st.stop()

weather = get_weather_data(
    location["latitude"],
    location["longitude"],
    location["timezone"]
)

current = weather["current"]
hourly_df = build_hourly_dataframe(weather)
daily_df = build_daily_dataframe(weather)

# Next 24 hours from now in API order
hourly_24 = hourly_df.head(24).copy()

weather_text = weather_code_to_text(current["weather_code"])
weather_icon = weather_code_to_icon(current["weather_code"])

# ---------- Hero ----------
st.markdown(f"""
<div class="hero-card">
    <div style="display:flex; justify-content:space-between; align-items:center; gap:20px; flex-wrap:wrap;">
        <div>
            <div class="small-label">Current Weather</div>
            <h1 style="margin:8px 0 4px 0;">{location['name']}, {location['country']}</h1>
            <div style="font-size:18px; opacity:0.92;">{weather_icon} {weather_text}</div>
            <div class="big-temp">{current['temperature_2m']}°C</div>
            <div style="opacity:0.9;">Feels like {current['apparent_temperature']}°C</div>
        </div>
        <div style="min-width:280px;">
            <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:14px;">
                <div class="metric-card"><div class="small-label">Humidity</div><h3>{current['relative_humidity_2m']}%</h3></div>
                <div class="metric-card"><div class="small-label">Wind Speed</div><h3>{current['wind_speed_10m']} km/h</h3></div>
                <div class="metric-card"><div class="small-label">Pressure</div><h3>{current['surface_pressure']} hPa</h3></div>
                <div class="metric-card"><div class="small-label">Precipitation</div><h3>{current['precipitation']} mm</h3></div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- Quick summary cards ----------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Temperature", f"{current['temperature_2m']}°C")
col2.metric("Feels Like", f"{current['apparent_temperature']}°C")
col3.metric("Humidity", f"{current['relative_humidity_2m']}%")
col4.metric("Wind", f"{current['wind_speed_10m']} km/h")

# ---------- Hourly forecast ----------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("⏱️ Next 24 Hours Forecast")

hourly_display = hourly_24.copy()
hourly_display["time"] = hourly_display["time"].dt.strftime("%d %b | %I:%M %p")
st.dataframe(
    hourly_display.rename(columns={
        "time": "Time",
        "temperature": "Temperature (°C)",
        "humidity": "Humidity (%)",
        "rain_probability": "Rain Probability (%)",
        "wind_speed": "Wind Speed (km/h)"
    }),
    use_container_width=True,
    hide_index=True
)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- 7-day forecast cards ----------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("📅 7-Day Forecast")

forecast_cols = st.columns(7)
for idx, row in daily_df.iterrows():
    with forecast_cols[idx]:
        icon = weather_code_to_icon(int(row["weather_code"]))
        st.markdown(f"""
        <div class="forecast-card">
            <div style="font-weight:700;">{pd.to_datetime(row['date']).strftime('%a')}</div>
            <div style="font-size:28px; margin:10px 0;">{icon}</div>
            <div style="font-size:14px;">{pd.to_datetime(row['date']).strftime('%d %b')}</div>
            <div style="margin-top:8px;"><b>{row['max_temp']}°C</b> / {row['min_temp']}°C</div>
            <div style="font-size:13px; opacity:0.85; margin-top:6px;">Rain: {row['precipitation_sum']} mm</div>
        </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- Charts ----------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("📈 Weather Analytics")

c1, c2 = st.columns(2)

with c1:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(daily_df["date"], daily_df["max_temp"], marker="o", label="Max Temp")
    ax.plot(daily_df["date"], daily_df["min_temp"], marker="o", label="Min Temp")
    ax.set_title("7-Day Temperature Trend")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    plt.xticks(rotation=30)
    st.pyplot(fig)

with c2:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(daily_df["date"].astype(str), daily_df["precipitation_sum"])
    ax.set_title("7-Day Precipitation")
    ax.set_ylabel("Precipitation (mm)")
    plt.xticks(rotation=30)
    st.pyplot(fig)

c3, c4 = st.columns(2)

with c3:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(hourly_24["time"], hourly_24["temperature"], marker="o")
    ax.set_title("Next 24 Hours Temperature")
    ax.set_ylabel("Temperature (°C)")
    plt.xticks(rotation=60)
    st.pyplot(fig)

with c4:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(hourly_24["time"].dt.strftime("%H:%M"), hourly_24["wind_speed"])
    ax.set_title("Next 24 Hours Wind Speed")
    ax.set_ylabel("Wind Speed (km/h)")
    plt.xticks(rotation=60)
    st.pyplot(fig)

st.markdown('</div>', unsafe_allow_html=True)

# ---------- Forecast table + download ----------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("📄 Forecast Data Table")

download_df = daily_df.copy()
download_df["condition"] = download_df["weather_code"].apply(weather_code_to_text)

st.dataframe(
    download_df.rename(columns={
        "date": "Date",
        "max_temp": "Max Temp (°C)",
        "min_temp": "Min Temp (°C)",
        "precipitation_sum": "Precipitation (mm)",
        "wind_speed_max": "Max Wind (km/h)",
        "sunrise": "Sunrise",
        "sunset": "Sunset",
        "condition": "Condition"
    }),
    use_container_width=True,
    hide_index=True
)

csv = download_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download Forecast CSV",
    data=csv,
    file_name=f"{location['name'].lower().replace(' ', '_')}_forecast.csv",
    mime="text/csv"
)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- Footer ----------
st.caption("Built with Streamlit + Open-Meteo API + Pandas + Matplotlib")