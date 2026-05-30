import streamlit as st
import joblib
import pandas as pd
from datetime import date

model = joblib.load("crop_model.pkl")

st.set_page_config(
    page_title="AgriSmart Crop Advisor",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=DM+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {
    --soil:  #3D2B1F;
    --earth: #6B4226;
    --moss:  #2D5016;
    --leaf:  #4A7C2F;
    --sage:  #7AAE5C;
    --mist:  #D6E8C4;
    --cream: #F7F2E8;
    --wheat: #E8D5A3;
    --gold:  #C8960C;
    --sun:   #F2A30F;
}
* { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background-color: var(--cream); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── HERO ── */
.hero-wrap {
    position: relative; overflow: hidden;
    background: linear-gradient(160deg, var(--soil) 0%, var(--moss) 55%, var(--leaf) 100%);
    padding: 60px 48px 52px;
}
.hero-wrap::before {
    content: ""; position: absolute; inset: 0;
    background:
        radial-gradient(ellipse 60% 50% at 85% 20%, rgba(74,124,47,.35) 0%, transparent 60%),
        radial-gradient(ellipse 40% 60% at 10% 80%, rgba(200,150,12,.18) 0%, transparent 55%);
    pointer-events: none;
}
.hero-grid {
    display: grid; grid-template-columns: 1fr auto;
    align-items: center; gap: 24px;
    position: relative; z-index: 1;
    max-width: 1100px; margin: 0 auto;
}
.hero-tag {
    display: inline-block;
    background: rgba(242,163,15,.22); border: 1px solid rgba(242,163,15,.55);
    color: var(--sun); font-size: 11px; font-weight: 600;
    letter-spacing: 2.5px; text-transform: uppercase;
    padding: 5px 14px; border-radius: 20px; margin-bottom: 14px;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(30px, 4vw, 50px); font-weight: 800;
    color: #fff; line-height: 1.12; margin: 0 0 12px;
}
.hero-title span { color: var(--sun); }
.hero-sub { color: rgba(255,255,255,.72); font-size: 15px; font-weight: 300; max-width: 520px; line-height: 1.6; margin: 0; }
.hero-badge {
    background: rgba(255,255,255,.08); border: 1px solid rgba(255,255,255,.18);
    border-radius: 20px; padding: 20px 28px; text-align: center;
    backdrop-filter: blur(8px); white-space: nowrap;
}
.hero-badge .big { font-family:'Playfair Display',serif; font-size:38px; color:var(--sun); display:block; }
.hero-badge .sm  { font-size:12px; color:rgba(255,255,255,.6); letter-spacing:1px; text-transform:uppercase; }

/* ── BODY ── */
.body-wrap { max-width: 1100px; margin: 0 auto; padding: 36px 24px 60px; }

/* ── SECTION LABEL ── */
.section-label {
    font-size: 11px; font-weight: 600; letter-spacing: 2.5px;
    text-transform: uppercase; color: var(--leaf);
    margin-bottom: 18px; display: flex; align-items: center; gap: 10px;
}
.section-label::after {
    content: ""; flex: 1; height: 1px;
    background: linear-gradient(90deg, var(--mist), transparent);
}

/* ── COL HEADERS ── */
.col-header {
    font-size: 13px; font-weight: 600; color: var(--earth);
    letter-spacing: .5px; margin-bottom: 16px;
    display: flex; align-items: center; gap: 7px;
}

/* ── TEXT INPUTS ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    border: 1.5px solid #C8D9A8 !important;
    border-radius: 10px !important;
    background: #fff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
    transition: border-color .18s !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: var(--leaf) !important;
    box-shadow: 0 0 0 3px rgba(74,124,47,.12) !important;
}

/* ── SELECT BOX ── */
[data-testid="stSelectbox"] > div > div {
    border: 1.5px solid #C8D9A8 !important;
    border-radius: 10px !important;
    background: #fff !important;
}

/* ── SLIDERS ── */
[data-testid="stSlider"] .rc-slider-track { background-color: var(--leaf) !important; }
[data-testid="stSlider"] .rc-slider-handle {
    border-color: var(--leaf) !important;
    box-shadow: 0 0 0 4px rgba(74,124,47,.2) !important;
}

/* ── OBJECTIVE CARDS ── */
[data-testid="stRadio"] > div {
    display: grid !important;
    grid-template-columns: repeat(4, 1fr) !important;
    gap: 14px !important;
}
[data-testid="stRadio"] label {
    background: linear-gradient(145deg, #0F2608, #1E3D0D) !important;
    border: 2px solid #3A6B1A !important;
    border-radius: 18px !important;
    padding: 24px 16px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    color: #C8E8A0 !important;
    cursor: pointer !important;
    transition: all .2s !important;
    text-align: center !important;
    min-height: 90px !important;
    box-shadow: 0 4px 18px rgba(0,0,0,.45) !important;
    line-height: 1.5 !important;
    justify-content: center !important;
}
[data-testid="stRadio"] label:hover {
    background: linear-gradient(145deg, #1E3D0D, #2D5C16) !important;
    border-color: var(--sage) !important;
    color: #fff !important;
    transform: translateY(-4px) !important;
    box-shadow: 0 10px 28px rgba(0,0,0,.55) !important;
}
[data-testid="stRadio"] [data-baseweb="radio"] > div:first-child { display:none !important; }

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, var(--moss), var(--leaf)) !important;
    color: #fff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 16px !important; font-weight: 700 !important;
    letter-spacing: .5px !important; border: none !important;
    border-radius: 14px !important; padding: 16px 40px !important;
    width: 100% !important;
    box-shadow: 0 6px 20px rgba(45,80,22,.35) !important;
    transition: all .2s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 28px rgba(45,80,22,.45) !important;
    background: linear-gradient(135deg, #0F2608, var(--moss)) !important;
}

/* ── RESULT HERO ── */
.result-hero {
    background: linear-gradient(135deg, var(--moss) 0%, var(--leaf) 100%);
    border-radius: 24px; padding: 40px 44px;
    position: relative; overflow: hidden; margin-bottom: 20px;
}
.result-hero::after {
    content: "🌾"; position: absolute; right: 32px; top: 50%;
    transform: translateY(-50%); font-size: 96px; opacity: .15; pointer-events: none;
}
.result-tag { font-size:11px; font-weight:600; letter-spacing:2px; text-transform:uppercase; color:rgba(255,255,255,.65); margin-bottom:10px; }
.result-crop {
    font-family: 'Playfair Display', serif;
    font-size: clamp(36px, 5vw, 58px); font-weight: 800; color: #fff;
    margin: 0 0 10px; line-height: 1; text-transform: uppercase; letter-spacing: 2px;
}
.result-desc { color: rgba(255,255,255,.75); font-size: 14px; font-weight: 300; max-width: 500px; }

/* ── METRICS ROW ── */
.metrics-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 20px; }
.metric-chip {
    background: #fff; border: 1px solid #DDE8C8;
    border-radius: 14px; padding: 16px 14px; text-align: center;
    box-shadow: 0 2px 10px rgba(45,80,22,.06);
}
.metric-chip .val { font-family:'Playfair Display',serif; font-size:22px; font-weight:700; color:var(--moss); display:block; }
.metric-chip .lbl { font-size:10px; font-weight:600; text-transform:uppercase; letter-spacing:1.5px; color:#9AAD88; }

/* ── INFO GRID ── */
.info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px,1fr)); gap: 16px; margin-bottom: 20px; }
.info-tile {
    background: #fff; border: 1px solid #E5EDD8; border-radius: 18px;
    padding: 24px 26px; position: relative; overflow: hidden;
    box-shadow: 0 2px 14px rgba(45,80,22,.06);
    transition: transform .2s, box-shadow .2s;
}
.info-tile:hover { transform: translateY(-3px); box-shadow: 0 8px 28px rgba(45,80,22,.12); }
.info-tile::before {
    content:""; position:absolute; top:0; left:0; right:0;
    height:4px; border-radius:18px 18px 0 0;
}
.info-tile.c1::before { background: linear-gradient(90deg,#3D9A5C,#7AAE5C); }
.info-tile.c2::before { background: linear-gradient(90deg,#C8960C,#F2A30F); }
.info-tile.c3::before { background: linear-gradient(90deg,#2D72B8,#5BA4D8); }
.info-tile.c4::before { background: linear-gradient(90deg,#8B3A9B,#C46FD4); }
.info-tile.c5::before { background: linear-gradient(90deg,#D64B2B,#F27B5C); }
.info-tile.c6::before { background: linear-gradient(90deg,#1A7A5E,#3DBF96); }
.tile-icon { font-size:26px; margin-bottom:10px; display:block; line-height:1; }
.tile-label { font-size:10px; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:#9AAD88; margin-bottom:8px; }
.tile-text  { font-size:13.5px; line-height:1.65; color:var(--soil); }
.tile-text b { color:var(--moss); font-weight:600; }

hr.fancy { border:none; height:1px; background:linear-gradient(90deg,transparent,#C8D9B0,transparent); margin:28px 0; }
</style>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
  <div class="hero-grid">
    <div>
      <div class="hero-tag">✦ AI-Powered · Precision Agriculture</div>
      <h1 class="hero-title">AgriSmart<br><span>Crop Advisor</span></h1>
      <p class="hero-sub">
        Enter your farmer profile, soil nutrients, and climate data to receive
        an intelligent crop recommendation with a full personalised advisory report.
      </p>
    </div>
    <div class="hero-badge">
      <span class="big">22+</span>
      <span class="sm">Crops Modelled</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="body-wrap">', unsafe_allow_html=True)

# ── FARMER PROFILE ────────────────────────────────────
st.markdown('<div class="section-label">👨‍🌾 &nbsp;Farmer Profile</div>', unsafe_allow_html=True)

fp1, fp2, fp3, fp4 = st.columns([2, 2, 1, 1])
with fp1:
    farmer_name = st.text_input("Farmer Name", placeholder="e.g. Ravi Kumar")
with fp2:
    location = st.text_input("Location / Village", placeholder="e.g. Tumkur, Karnataka")
with fp3:
    farm_size = st.number_input("Farm Size (acres)", 0.1, 100.0, 1.0, step=0.5)
with fp4:
    season = st.selectbox("Season", ["Kharif", "Rabi", "Summer"])

prev_col, _ = st.columns([2, 3])
with prev_col:
    previous_crop = st.text_input("Previous Crop Grown", placeholder="e.g. Wheat")

# ── SOIL & WEATHER ────────────────────────────────────
st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
st.markdown('<div class="section-label">🌱 &nbsp;Soil & Weather Data</div>', unsafe_allow_html=True)

col_l, col_r = st.columns(2, gap="large")
with col_l:
    st.markdown('<div class="col-header">🧪 Soil Nutrients & pH</div>', unsafe_allow_html=True)
    N  = st.slider("Nitrogen (N) — kg/ha",   0,   200, 50)
    P  = st.slider("Phosphorus (P) — kg/ha", 0,   200, 50)
    K  = st.slider("Potassium (K) — kg/ha",  0,   200, 50)
    ph = st.slider("Soil pH",               0.0, 14.0, 6.5, step=0.1)
with col_r:
    st.markdown('<div class="col-header">🌤️ Climate Conditions</div>', unsafe_allow_html=True)
    temperature = st.slider("Temperature (°C)", 0.0,  60.0,  25.0, step=0.5)
    humidity    = st.slider("Humidity (%)",      0.0, 100.0,  60.0, step=0.5)
    rainfall    = st.slider("Rainfall (mm)",     0.0, 500.0, 100.0, step=1.0)

# ── OBJECTIVE ─────────────────────────────────────────
st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
st.markdown('<div class="section-label">🎯 &nbsp;Farming Objective</div>', unsafe_allow_html=True)

objective = st.radio(
    "objective",
    ["🌾  High Yield", "💧  Low Water Usage", "🌿  Organic Farming", "💰  Profit Maximisation"],
    horizontal=True,
    label_visibility="collapsed"
)

# ── GENERATE BUTTON ───────────────────────────────────
st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
run = st.button("🔍  Analyse & Generate Full Advisory Report")


# ── LOGIC ─────────────────────────────────────────────
def pest_disease_advice(crop):
    advice = {
        "rice":       "Monitor stem borer, leaf folder, and blast disease. Maintain proper water level and avoid overcrowding.",
        "maize":      "Watch for fall armyworm and leaf blight. Use balanced fertilisation and regular field monitoring.",
        "cotton":     "Monitor bollworm and whitefly. Use pheromone traps and avoid excessive pesticide use.",
        "banana":     "Watch for leaf spot and Panama wilt. Maintain clean field conditions and proper drainage.",
        "grapes":     "Monitor powdery mildew and downy mildew. Ensure good air circulation and avoid excess humidity.",
        "mango":      "Watch for fruit fly, anthracnose, and hopper insects. Use orchard sanitation and timely spraying.",
        "papaya":     "Monitor papaya ring spot virus, mealybugs, and fungal infection. Remove infected plants early.",
        "muskmelon":  "Watch for powdery mildew, aphids, and fruit rot. Avoid waterlogging.",
        "watermelon": "Monitor fruit fly, aphids, and downy mildew. Maintain field hygiene.",
        "coffee":     "Watch for coffee leaf rust and berry borer. Maintain shade and regular inspection.",
    }
    return advice.get(crop.lower(),
        "Monitor the crop regularly for pests, fungal infections, leaf spots, and abnormal growth patterns.")

def seasonal_plan(crop, season):
    steps = [
        ("Prepare land properly before sowing.", "🌱"),
        (f"Use quality seeds suited for the <b>{season}</b> season.", "🌾"),
        ("Apply fertiliser based on soil nutrient status (NPK).", "⚗️"),
        ("Monitor rainfall and schedule supplemental irrigation.", "💧"),
        ("Inspect the crop weekly for pest and disease symptoms.", "🔍"),
        (f"Plan harvesting of <b>{crop.title()}</b> based on maturity and market demand.", "📦"),
    ]
    html = '<ol style="padding-left:18px;margin:0">'
    for text, icon in steps:
        html += f'<li style="margin-bottom:10px;font-size:13.5px;color:#3D2B1F;line-height:1.6">{icon} {text}</li>'
    html += "</ol>"
    return html


# ── RESULTS ───────────────────────────────────────────
if run:
    data = pd.DataFrame(
        [[N, P, K, temperature, humidity, ph, rainfall]],
        columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    )
    crop = model.predict(data)[0]
    obj_clean = objective.split("  ", 1)[-1].strip()

    st.markdown("<hr class='fancy'>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">✅ &nbsp;Recommendation</div>', unsafe_allow_html=True)

    # Result banner
    st.markdown(f"""
    <div class="result-hero">
      <div class="result-tag">Recommended Crop</div>
      <div class="result-crop">{crop}</div>
      <div class="result-desc">
        Based on soil profile (N·P·K), pH, temperature, humidity, and rainfall —
        <b style="color:#fff">{crop.title()}</b> offers the best agronomic fit for your conditions.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Metrics row
    st.markdown(f"""
    <div class="metrics-row">
      <div class="metric-chip"><span class="val">{ph}</span><span class="lbl">Soil pH</span></div>
      <div class="metric-chip"><span class="val">{temperature}°C</span><span class="lbl">Temperature</span></div>
      <div class="metric-chip"><span class="val">{humidity}%</span><span class="lbl">Humidity</span></div>
      <div class="metric-chip"><span class="val">{rainfall}mm</span><span class="lbl">Rainfall</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Advisory tiles
    st.markdown('<div class="section-label">📑 &nbsp;Full Advisory Report</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="info-grid">

      <div class="info-tile c1">
        <span class="tile-icon">👨‍🌾</span>
        <div class="tile-label">Farmer Profile</div>
        <div class="tile-text">
          <b>Name:</b> {farmer_name if farmer_name else "—"}<br>
          <b>Location:</b> {location if location else "—"}<br>
          <b>Farm Size:</b> {farm_size} acres<br>
          <b>Previous Crop:</b> {previous_crop if previous_crop else "—"}
        </div>
      </div>

      <div class="info-tile c2">
        <span class="tile-icon">💧</span>
        <div class="tile-label">Irrigation</div>
        <div class="tile-text">
          Rainfall is <b>{rainfall} mm</b> with <b>{humidity}% humidity</b>.
          Plan supplemental irrigation carefully and avoid both water stress and waterlogging.
        </div>
      </div>

      <div class="info-tile c3">
        <span class="tile-icon">⚗️</span>
        <div class="tile-label">Fertiliser</div>
        <div class="tile-text">
          NPK: <b>{N}·{P}·{K} kg/ha</b>, pH <b>{ph}</b>.
          Apply fertiliser based on nutrient deficiency and the uptake profile of {crop.title()}.
        </div>
      </div>

      <div class="info-tile c4">
        <span class="tile-icon">🐛</span>
        <div class="tile-label">Pest & Disease</div>
        <div class="tile-text">{pest_disease_advice(crop)}</div>
      </div>

      <div class="info-tile c5">
        <span class="tile-icon">📅</span>
        <div class="tile-label">Seasonal Plan — {season}</div>
        <div class="tile-text">
          {seasonal_plan(crop, season)}
        </div>
      </div>

      <div class="info-tile c6">
        <span class="tile-icon">🎯</span>
        <div class="tile-label">Objective — {obj_clean}</div>
        <div class="tile-text">
          Optimising for <b>{obj_clean}</b>: fine-tune variety selection,
          input intensity, and market timing to maximise your target outcome with <b>{crop.title()}</b>.
          <br><br><b>Report Date:</b> {date.today().strftime("%d %b %Y")}
        </div>
      </div>

    </div>
    """, unsafe_allow_html=True)

    # Final summary bar
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0F2608,#1E3D0D);border-radius:18px;
                padding:28px 36px;margin-top:4px;
                border:1.5px solid #3A6B1A;
                box-shadow:0 6px 24px rgba(0,0,0,.35);">
      <div style="font-size:11px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;
                  color:#7AAE5C;margin-bottom:10px;">✦ Final Recommendation</div>
      <div style="font-family:'Playfair Display',serif;font-size:28px;font-weight:800;
                  color:#fff;margin-bottom:10px;letter-spacing:1px;">{crop.upper()}</div>
      <div style="color:rgba(255,255,255,.72);font-size:14px;font-weight:300;line-height:1.7;max-width:700px;">
        <b style="color:#C8E8A0">{crop.title()}</b> is the optimal crop for your soil and climate conditions.
        This advisory covers irrigation, fertilisation, pest control, and seasonal planning to help you
        make better decisions and achieve your <b style="color:#F2A30F">{obj_clean}</b> goal.
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
