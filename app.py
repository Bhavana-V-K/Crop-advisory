import streamlit as st
import joblib
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="AgriSmart Crop Advisor",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

model = joblib.load("crop_model.pkl")

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

st.subheader("👨‍🌾 Farmer Profile")

farmer_name = st.text_input("Farmer Name")
location = st.text_input("Location / Village")
farm_size = st.number_input("Farm Size (in acres)", 0.1, 100.0, 1.0)
season = st.selectbox("Current Season", ["Kharif", "Rabi", "Summer"])
previous_crop = st.text_input("Previous Crop Grown")

st.subheader("🌱 Soil & Weather Input")

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

def pest_disease_advice(crop):
    crop = crop.lower()

    advice = {
        "rice": "Monitor stem borer, leaf folder, and blast disease. Maintain proper water level and avoid overcrowding.",
        "maize": "Watch for fall armyworm and leaf blight. Use balanced fertilization and regular field monitoring.",
        "cotton": "Monitor bollworm and whitefly. Use pheromone traps and avoid excessive pesticide use.",
        "banana": "Watch for leaf spot and Panama wilt. Maintain clean field conditions and proper drainage.",
        "grapes": "Monitor powdery mildew and downy mildew. Ensure good air circulation and avoid excess humidity.",
        "mango": "Watch for fruit fly, anthracnose, and hopper insects. Use orchard sanitation and timely spraying.",
        "papaya": "Monitor papaya ring spot virus, mealybugs, and fungal infection. Remove infected plants early.",
        "muskmelon": "Watch for powdery mildew, aphids, and fruit rot. Avoid waterlogging.",
        "watermelon": "Monitor fruit fly, aphids, and downy mildew. Maintain field hygiene.",
        "coffee": "Watch for coffee leaf rust and berry borer. Maintain shade and regular inspection."
    }

    return advice.get(
        crop,
        "Monitor the crop regularly for pests, fungal infections, leaf spots, and abnormal growth."
    )

def seasonal_plan(crop, season):
    return f"""
For **{crop}** during **{season} season**:

- Prepare land properly before sowing.
- Use quality seeds suitable for local climate.
- Apply fertilizer based on soil nutrient status.
- Monitor rainfall and irrigation requirements.
- Inspect crop weekly for pest and disease symptoms.
- Plan harvesting based on crop maturity and market demand.
"""

if st.button("Generate Crop Advisory"):
    data = pd.DataFrame(
        [[N, P, K, temperature, humidity, ph, rainfall]],
        columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    )

    crop = model.predict(data)[0]

    st.markdown(f"""
    <div class="result-card">
        <h2>✅ Recommended Crop: {crop.upper()}</h2>
        <p>This crop is selected based on soil nutrients, climate conditions, pH, and rainfall.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="advisory-card">
        <h3>👨‍🌾 Farmer Profile</h3>
        <p><b>Name:</b> {farmer_name if farmer_name else "Not provided"}</p>
        <p><b>Location:</b> {location if location else "Not provided"}</p>
        <p><b>Farm Size:</b> {farm_size} acres</p>
        <p><b>Previous Crop:</b> {previous_crop if previous_crop else "Not provided"}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="advisory-card">
        <h3>🌱 Personalized Crop Advisory</h3>
        <p><b>Farming Objective:</b> {objective}</p>
        <p><b>Irrigation:</b> Rainfall is {rainfall} mm and humidity is {humidity}%. Plan irrigation carefully and avoid both water stress and waterlogging.</p>
        <p><b>Fertilizer:</b> Current NPK values are N={N}, P={P}, K={K}. Apply fertilizer based on nutrient deficiency and crop requirement.</p>
        <p><b>Soil pH:</b> Current pH is {ph}. Maintain soil pH close to the suitable range for healthy crop growth.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="advisory-card">
        <h3>🐛 Pest & Disease Management</h3>
        <p>{pest_disease_advice(crop)}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="advisory-card">
        <h3>📅 Seasonal Planning Report</h3>
        <p><b>Date:</b> {date.today()}</p>
        <p><b>Season:</b> {season}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(seasonal_plan(crop, season))

    st.markdown(f"""
    <div class="advisory-card">
        <h3>🌾 Final Recommendation</h3>
        <p><b>{crop.upper()}</b> is suitable for the given soil and weather conditions.</p>
        <p>This advisory helps farmers make better decisions for crop selection, irrigation, fertilizer use, pest control, and seasonal planning.</p>
    </div>
    """, unsafe_allow_html=True)
