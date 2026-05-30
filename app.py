import streamlit as st
import joblib
import pandas as pd

model = joblib.load("crop_model.pkl")

st.title("🌾 Smart Crop Advisory Assistant")
st.write("Enter soil and weather values:")

N = st.slider("Nitrogen", 0, 200, 50)
P = st.slider("Phosphorus", 0, 200, 50)
K = st.slider("Potassium", 0, 200, 50)
temperature = st.slider("Temperature", 0.0, 60.0, 25.0)
humidity = st.slider("Humidity", 0.0, 100.0, 60.0)
ph = st.slider("pH", 0.0, 14.0, 6.5)
rainfall = st.slider("Rainfall", 0.0, 500.0, 100.0)

objective = st.radio(
    "Farming Objective",
    ["High Yield", "Low Water Usage", "Organic Farming", "Profit Maximization"]
)

if st.button("Predict Crop"):

    data = pd.DataFrame(
        [[N, P, K, temperature, humidity, ph, rainfall]],
        columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    )

    crop = model.predict(data)[0]

    st.success(f"🌾 Recommended Crop: {crop}")

    st.markdown(f"""
## 🌱 Smart Farming Advisory

### 🎯 Objective
**{objective}**

### 🌧️ Irrigation Recommendation
Plan irrigation based on the current rainfall and humidity conditions. Maintain adequate soil moisture and avoid overwatering.

### 🌿 Fertilizer Recommendation
Apply fertilizers according to the Nitrogen (N), Phosphorus (P), and Potassium (K) levels. Regular soil testing is recommended.

### 🐛 Pest & Disease Management
Monitor crops regularly for pests, fungal infections, and diseases. Early detection helps reduce crop losses.

### 📅 Seasonal Planning
Follow the recommended sowing and harvesting schedule for **{crop}**.

### 📈 Expected Benefits
✅ Improved crop yield  
✅ Better resource utilization  
✅ Reduced pest-related losses  
✅ Enhanced soil health

### 🌾 Final Recommendation
Based on the provided soil and weather conditions, **{crop.upper()}** is the most suitable crop for cultivation.
""")
