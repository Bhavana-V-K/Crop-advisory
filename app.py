import streamlit as st
import joblib
import pandas as pd
import requests
from datetime import date

st.set_page_config(page_title="AgriSmart Crop Advisor", page_icon="🌾", layout="wide")

model = joblib.load("crop_model(1).pkl")

st.markdown("""
<style>
.stApp { background-color: #F5FAF6; color: #1B1B1B; }
h1, h2, h3, h4, p, label, span { color: #1B1B1B !important; }

.hero {
    background: linear-gradient(135deg, #1B5E20, #43A047);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 25px;
}
.hero h1, .hero p { color: white !important; }

.card {
    background-color: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #C8E6C9;
    margin-top: 18px;
}

.result-card {
    background-color: #E8F5E9;
    border-left: 6px solid #2E7D32;
    padding: 22px;
    border-radius: 16px;
    margin-top: 20px;
}

.stTextInput input,
.stNumberInput input {
    background-color: #FFF8E7 !important;
    color: #1B1B1B !important;
    border: 2px solid #8BC34A !important;
    border-radius: 10px !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    background-color: #FFF8E7 !important;
    color: #1B1B1B !important;
    border: 2px solid #8BC34A !important;
    border-radius: 10px !important;
}

.stButton > button {
    background-color: #2E7D32;
    color: white !important;
    border-radius: 10px;
    border: none;
    padding: 10px 24px;
    font-weight: 600;
}
.stButton > button:hover {
    background-color: #1B5E20;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def get_live_weather(city, api_key):
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if response.status_code != 200:
            return None, None, None, data.get("message", "Unable to fetch weather")

        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        rainfall = data.get("rain", {}).get("1h", 0)

        return temperature, humidity, rainfall, None

    except Exception as e:
        return None, None, None, str(e)


def login_page():
    st.markdown("""
    <div class="hero">
        <h1>🌾 AgriSmart Crop Advisor</h1>
        <p>Login to access smart crop recommendation dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🔐 Farmer Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "farmer" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")

    st.info("Demo Login: username = farmer, password = 1234")


def pesticide_recommendation(crop):
    crop = crop.lower()

    pesticide_data = {
        "rice": {
            "pests": "Stem borer, leaf folder, brown plant hopper",
            "recommendation": "Use neem-based biopesticide or recommended insecticides. Maintain proper water level."
        },
        "maize": {
            "pests": "Fall armyworm, stem borer, leaf blight",
            "recommendation": "Use pheromone traps and neem oil. Apply recommended pesticide only when infestation is high."
        },
        "cotton": {
            "pests": "Bollworm, whitefly, aphids",
            "recommendation": "Use pheromone traps, neem oil, and integrated pest management practices."
        },
        "banana": {
            "pests": "Banana aphid, nematodes, leaf spot",
            "recommendation": "Use disease-free suckers, proper drainage, and recommended fungicide if leaf spot appears."
        },
        "grapes": {
            "pests": "Powdery mildew, downy mildew, mealybugs",
            "recommendation": "Maintain airflow, avoid excess humidity, and use recommended fungicide if symptoms appear."
        },
        "mango": {
            "pests": "Fruit fly, mango hopper, anthracnose",
            "recommendation": "Use fruit fly traps, orchard sanitation, and timely spraying."
        },
        "papaya": {
            "pests": "Mealybug, fruit fly, papaya ring spot virus",
            "recommendation": "Remove infected plants early and use organic pest control methods."
        },
        "muskmelon": {
            "pests": "Aphids, powdery mildew, fruit fly",
            "recommendation": "Avoid waterlogging, use neem oil, and monitor leaves regularly."
        },
        "watermelon": {
            "pests": "Fruit fly, aphids, downy mildew",
            "recommendation": "Use field sanitation, traps, and organic pesticides when needed."
        },
        "coffee": {
            "pests": "Coffee berry borer, leaf rust",
            "recommendation": "Maintain shade, prune regularly, and use recommended fungicide for rust."
        }
    }

    return pesticide_data.get(
        crop,
        {
            "pests": "Common pests, fungal infections, leaf spots",
            "recommendation": "Monitor the crop weekly and use organic or recommended pesticides only when symptoms appear."
        }
    )


def fertilizer_advice(N, P, K):
    advice = []

    if N < 50:
        advice.append("Nitrogen is low. Use nitrogen-rich fertilizer such as urea or compost.")
    elif N > 120:
        advice.append("Nitrogen is high. Avoid excess nitrogen fertilizer.")
    else:
        advice.append("Nitrogen level is moderate.")

    if P < 40:
        advice.append("Phosphorus is low. Use phosphorus fertilizer to support root growth.")
    elif P > 100:
        advice.append("Phosphorus is high. Avoid extra phosphorus application.")
    else:
        advice.append("Phosphorus level is suitable.")

    if K < 40:
        advice.append("Potassium is low. Use potassium fertilizer for better crop quality.")
    elif K > 120:
        advice.append("Potassium is high. Avoid excess potassium fertilizer.")
    else:
        advice.append("Potassium level is suitable.")

    return advice


def irrigation_advice(rainfall, humidity):
    if rainfall < 50:
        return "Rainfall is low. Frequent irrigation is required."
    elif rainfall < 150:
        return "Rainfall is moderate. Provide irrigation based on soil moisture."
    else:
        return "Rainfall is high. Avoid overwatering and ensure proper drainage."


def seasonal_plan(crop, season):
    return f"""
For **{crop}** during **{season} season**:

- Prepare land before sowing.
- Use quality seeds suitable for local climate.
- Apply fertilizer based on soil nutrient status.
- Monitor rainfall and irrigation requirements.
- Inspect crop weekly for pests and diseases.
- Harvest based on crop maturity and market demand.
"""


def dashboard():
    st.markdown("""
    <div class="hero">
        <h1>🌱 AgriSmart Crop Advisor</h1>
        <p>Smart crop recommendation, live weather integration, pesticide guidance, and seasonal advisory system</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.subheader("👨‍🌾 Farmer Profile")

    colA, colB = st.columns(2)

    with colA:
        farmer_name = st.text_input("Farmer Name")
        location = st.text_input("Location / Village / City", placeholder="Example: Hubli")
        farm_size = st.number_input("Farm Size (in acres)", 0.1, 100.0, 1.0)

    with colB:
        season = st.selectbox("Current Season", ["Kharif", "Rabi", "Summer"])
        previous_crop = st.text_input("Previous Crop Grown")
        crop_type = st.selectbox(
            "Crop Type",
            ["Cereal", "Pulse", "Fruit", "Vegetable", "Cash Crop", "Plantation Crop"]
        )

    st.subheader("🌱 Soil Input")

    col1, col2 = st.columns(2)

    with col1:
        N = st.slider("Nitrogen (N)", 0, 200, 50)
        P = st.slider("Phosphorus (P)", 0, 200, 50)
        K = st.slider("Potassium (K)", 0, 200, 50)

    with col2:
        ph = st.slider("Soil pH", 0.0, 14.0, 6.5)

    st.subheader("🌦️ Weather Information")

    api_key = st.text_input("OpenWeatherMap API Key", type="password")
    use_live_weather = st.checkbox("Use Live Weather Data")

    weather_city = location.strip() if location else ""

    if use_live_weather:
        if api_key and weather_city:
            temp_live, hum_live, rain_live, error = get_live_weather(weather_city, api_key)

            if error:
                st.error(f"Weather Error: {error}")
                temperature = st.slider("Temperature (°C)", 0.0, 60.0, 25.0)
                humidity = st.slider("Humidity (%)", 0.0, 100.0, 60.0)
                rainfall = st.slider("Rainfall (mm)", 0.0, 500.0, 100.0)
            else:
                st.success(f"Live weather fetched for {weather_city}")

                temperature = st.slider("Temperature (°C)", 0.0, 60.0, float(temp_live))
                humidity = st.slider("Humidity (%)", 0.0, 100.0, float(hum_live))
                rainfall = st.slider("Rainfall (mm)", 0.0, 500.0, float(rain_live))

        elif not weather_city:
            st.warning("Enter Location / City to fetch live weather.")
            temperature = st.slider("Temperature (°C)", 0.0, 60.0, 25.0)
            humidity = st.slider("Humidity (%)", 0.0, 100.0, 60.0)
            rainfall = st.slider("Rainfall (mm)", 0.0, 500.0, 100.0)

        else:
            st.warning("Enter OpenWeatherMap API key to use live weather.")
            temperature = st.slider("Temperature (°C)", 0.0, 60.0, 25.0)
            humidity = st.slider("Humidity (%)", 0.0, 100.0, 60.0)
            rainfall = st.slider("Rainfall (mm)", 0.0, 500.0, 100.0)

    else:
        temperature = st.slider("Temperature (°C)", 0.0, 60.0, 25.0)
        humidity = st.slider("Humidity (%)", 0.0, 100.0, 60.0)
        rainfall = st.slider("Rainfall (mm)", 0.0, 500.0, 100.0)

    objective = st.radio(
        "🎯 Farming Objective",
        ["High Yield", "Low Water Usage", "Organic Farming", "Profit Maximization"],
        horizontal=True
    )

    if st.button("Generate Crop Advisory"):
        data = pd.DataFrame(
            [[N, P, K, temperature, humidity, ph, rainfall]],
            columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        )

        crop = model.predict(data)[0]

        pesticide = pesticide_recommendation(crop)
        fert_advice = fertilizer_advice(N, P, K)
        irrigation = irrigation_advice(rainfall, humidity)

        st.markdown(f"""
        <div class="result-card">
            <h2>✅ Recommended Crop: {crop.upper()}</h2>
            <p>This crop is recommended based on soil nutrients, weather conditions, pH, rainfall, and farming objective.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <h3>👨‍🌾 Farmer Information</h3>
            <p><b>Name:</b> {farmer_name if farmer_name else "Not provided"}</p>
            <p><b>Location:</b> {location if location else "Not provided"}</p>
            <p><b>Farm Size:</b> {farm_size} acres</p>
            <p><b>Season:</b> {season}</p>
            <p><b>Previous Crop:</b> {previous_crop if previous_crop else "Not provided"}</p>
            <p><b>Crop Type:</b> {crop_type}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <h3>🌦️ Weather Summary</h3>
            <p><b>Temperature:</b> {temperature} °C</p>
            <p><b>Humidity:</b> {humidity}%</p>
            <p><b>Rainfall:</b> {rainfall} mm</p>
            <p><b>Weather Source:</b> {"OpenWeatherMap API" if use_live_weather and api_key and weather_city else "Manual Input"}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <h3>🌱 Personalized Crop Advisory</h3>
            <p><b>Objective:</b> {objective}</p>
            <p><b>Irrigation Advice:</b> {irrigation}</p>
            <p><b>Soil pH:</b> Current pH is {ph}. Maintain suitable pH for healthy crop growth.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='card'><h3>🌿 Fertilizer Recommendation</h3>", unsafe_allow_html=True)
        for item in fert_advice:
            st.markdown(f"<p>• {item}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <h3>🐛 Pesticide & Disease Management</h3>
            <p><b>Likely Pests/Diseases:</b> {pesticide["pests"]}</p>
            <p><b>Recommendation:</b> {pesticide["recommendation"]}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <h3>📅 Seasonal Planning Report</h3>
            <p><b>Date:</b> {date.today()}</p>
            <p><b>Season:</b> {season}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(seasonal_plan(crop, season))

        st.markdown(f"""
        <div class="card">
            <h3>🌾 Final Recommendation</h3>
            <p><b>{crop.upper()}</b> is suitable for the given soil and weather conditions.</p>
            <p>This advisory supports crop selection, irrigation planning, fertilizer use, pesticide management, weather-based decision-making, and seasonal planning.</p>
        </div>
        """, unsafe_allow_html=True)


if st.session_state.logged_in:
    dashboard()
else:
    login_page()
