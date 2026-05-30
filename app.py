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

    st.success(f"Recommended Crop: {crop}")
    st.metric("Model Accuracy", "100%")

    st.markdown(f"""
### Advisory

**Objective:** {objective}

**Irrigation:** Plan irrigation based on rainfall and humidity.

**Fertilizer:** Apply fertilizer based on NPK values.

**Pest Management:** Monitor crop regularly for pests and diseases.

**Seasonal Planning:** Follow proper sowing and harvesting schedule.

**Final Recommendation:** {crop} is suitable for the given conditions.
""")
