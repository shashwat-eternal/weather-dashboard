import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from weather import get_weather, forecast_dataframe

st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌤",
    layout="wide"
)

st.title("🌤 Weather Dashboard")

city = st.text_input(
    "Enter City Name",
    placeholder="Lucknow"
)

if st.button("Get Weather"):

    weather = get_weather(city)

    if weather is None:
        st.error("City not found")
        st.stop()

    location = weather["location"]
    current = weather["current"]
    daily = weather["daily"]

    st.success(
        f"Weather for {location['name']}, {location['country']}"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Temperature",
            f"{current['temperature_2m']} °C"
        )

    with col2:
        st.metric(
            "Humidity",
            f"{current['relative_humidity_2m']} %"
        )

    with col3:
        st.metric(
            "Wind Speed",
            f"{current['wind_speed_10m']} km/h"
        )

    st.subheader("7-Day Forecast")

    df = forecast_dataframe(daily)

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader("Temperature Trend")

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.plot(
        df["Date"],
        df["Max Temp"],
        marker="o",
        label="Max Temp"
    )

    ax.plot(
        df["Date"],
        df["Min Temp"],
        marker="o",
        label="Min Temp"
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()

    plt.xticks(rotation=45)

    st.pyplot(fig)

    csv = df.to_csv(index=False)

    st.download_button(
        label="Download Forecast CSV",
        data=csv,
        file_name="weather_forecast.csv",
        mime="text/csv"
    )