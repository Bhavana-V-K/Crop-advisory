import streamlit as st
import joblib
import pandas as pd

model = joblib.load("crop_model.pkl")

st.set_page_config(page_title="AgriSmart Crop Advisor", page_icon="🌱", layout="centered")

st.markdown("""
<style>
.stApp {
    background-color: #F5FAF6;
}
.hero {
    background: linear-gradient(135deg, #1B5E20, #43A047);
    padding: 28px;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 25px;
}
.hero h1 {
    font-size: 38px;
    margin-bottom: 5px;
}
.hero p {
    font-size: 16px;
    opacity: 0.95;
}
.result-card {
    background-color: #E8F5E9;
    border-left: 6px solid #2E7D32;
    padding: 20px;
    border-radius: 16px;
    margin-top: 20px;
}
.advisory-card {
    background-color: #FFFFFF;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #C8E6C9;
    margin-top: 18px;
}
.stButton > button {
    background-color: #2E7D32;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 24px;
    font-weight: 600;
}
.stButton > button:hover {
    background-color: #1B5E20;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🌱 AgriSmart Crop Advisor</h1>
    <p>Data-driven crop recommendation and advisory system for modern agriculture</p>
</div>
""", unsafe_allow_html=True)

st.subheader("Soil & Weather Input")

col1, col2 = st.columns(2)

with col1:
    N = st.slider("Nitrogen (N)", 0, 200, 50)
    P = st.slider("Phosphorus (P)", 0, 200, 50)
    K = st.slider("Potassium (K)", 0, 200, 50)
    ph = st.slider("Soil pH", 0.0, 14.0, 6.5)

with col2:
    temperature = st.slider("Temperature (°C)", 0.0, 60.0, 25.0)
    humidity = st.slider("Humidity (%)", 0.0, 100.0, 60.0)
    rainfall = st.slider("Rainfall (mm)", 0.0, 500.0, 100.0)

objective = st.radio(
    "Farming Objective",
    ["High Yield", "Low Water Usage", "Organic Farming", "Profit Maximization"],
    horizontal=True
)

if st.button("Generate Crop Advisory"):
    data = pd.DataFrame(
        [[N, P, K, temperature, humidity, ph, rainfall]],
        columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    )

    crop = model.predict(data)[0]

    st.markdown(f"""
    <div class="result-card">
        <h2>Recommended Crop: {crop.upper()}</h2>
        <p>This crop is selected based on soil nutrients, climate conditions, pH, and rainfall.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="advisory-card">
        <h3>Advisory Report</h3>

        <p><b>Objective:</b> {objective}</p>

        <p><b>Irrigation:</b> Plan irrigation based on rainfall and humidity. Avoid both water stress and waterlogging.</p>

        <p><b>Fertilizer:</b> Use NPK values to guide fertilizer application and maintain balanced soil nutrition.</p>

        <p><b>Pest Management:</b> Monitor crop growth regularly and identify early signs of pests or diseases.</p>

        <p><b>Seasonal Planning:</b> Follow suitable sowing, irrigation, and harvesting schedules for <b>{crop}</b>.</p>

        <p><b>Final Recommendation:</b> <b>{crop.upper()}</b> is suitable for the given soil and weather conditions.</p>
    </div>
    """, unsafe_allow_html=True)
