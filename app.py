import streamlit as st
import joblib
import pandas as pd

model = joblib.load("crop_model.pkl")

st.set_page_config(
    page_title="AgriSmart Crop Advisor",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>
:root {
    --soil:       #3D2B1F;
    --earth:      #6B4226;
    --moss:       #2D5016;
    --leaf:       #4A7C2F;
    --sage:       #7AAE5C;
    --mist:       #D6E8C4;
    --cream:      #F7F2E8;
    --wheat:      #E8D5A3;
    --sky:        #B8D4E8;
    --gold:       #C8960C;
    --sun:        #F2A30F;
}

* { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--cream);
}

/* ── Remove Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ──────────── HERO ──────────── */
.hero-wrap {
    position: relative;
    overflow: hidden;
    background: linear-gradient(160deg, var(--soil) 0%, var(--moss) 55%, var(--leaf) 100%);
    padding: 64px 48px 56px;
    margin-bottom: 0;
}

.hero-wrap::before {
    content: "";
    position: absolute;
    inset: 0;
    background:
        radial-gradient(ellipse 60% 50% at 85% 20%, rgba(74,124,47,.35) 0%, transparent 60%),
        radial-gradient(ellipse 40% 60% at 10% 80%, rgba(200,150,12,.18) 0%, transparent 55%);
    pointer-events: none;
}

.hero-grid {
    display: grid;
    grid-template-columns: 1fr auto;
    align-items: center;
    gap: 24px;
    position: relative;
    z-index: 1;
    max-width: 1100px;
    margin: 0 auto;
}

.hero-tag {
    display: inline-block;
    background: rgba(242,163,15,.22);
    border: 1px solid rgba(242,163,15,.55);
    color: var(--sun);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 20px;
    margin-bottom: 16px;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(32px, 4vw, 52px);
    font-weight: 800;
    color: #fff;
    line-height: 1.12;
    margin: 0 0 14px;
}

.hero-title span { color: var(--sun); }

.hero-sub {
    color: rgba(255,255,255,.72);
    font-size: 16px;
    font-weight: 300;
    max-width: 540px;
    line-height: 1.6;
    margin: 0;
}

.hero-badge {
    background: rgba(255,255,255,.08);
    border: 1px solid rgba(255,255,255,.18);
    border-radius: 20px;
    padding: 20px 28px;
    text-align: center;
    backdrop-filter: blur(8px);
    white-space: nowrap;
}

.hero-badge .big { font-family: 'Playfair Display', serif; font-size: 38px; color: var(--sun); display: block; }
.hero-badge .sm  { font-size: 12px; color: rgba(255,255,255,.6); letter-spacing: 1px; text-transform: uppercase; }

/* ──────────── BODY ──────────── */
.body-wrap {
    max-width: 1100px;
    margin: 0 auto;
    padding: 36px 24px 60px;
}

/* ──────────── SECTION LABEL ──────────── */
.section-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: var(--leaf);
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--mist), transparent);
}

/* ──────────── INPUT CARD ──────────── */
.card {
    background: #fff;
    border: 1px solid #E5EDD8;
    border-radius: 20px;
    padding: 32px 36px;
    margin-bottom: 24px;
    box-shadow: 0 2px 24px rgba(45,80,22,.07);
    transition: box-shadow .25s;
}

.card:hover { box-shadow: 0 6px 36px rgba(45,80,22,.12); }

.card-title {
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    color: var(--soil);
    margin: 0 0 6px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.card-sub {
    font-size: 13px;
    color: #8A9B7A;
    margin: 0 0 28px;
}

/* ──────────── SLIDER TWEAKS ──────────── */
[data-testid="stSlider"] > div > div {
    padding: 0 2px;
}

[data-testid="stSlider"] .rc-slider-track,
[data-testid="stSlider"] .st-emotion-cache-1xbz5gf {
    background-color: var(--leaf) !important;
}

[data-testid="stSlider"] .rc-slider-handle {
    border-color: var(--leaf) !important;
    box-shadow: 0 0 0 4px rgba(74,124,47,.2) !important;
}

/* ──────────── OBJECTIVE PILLS ──────────── */
[data-testid="stRadio"] > div {
    display: flex !important;
    flex-wrap: wrap;
    gap: 12px !important;
}

[data-testid="stRadio"] label {
    background: var(--mist) !important;
    border: 1.5px solid #C2D9A8 !important;
    border-radius: 30px !important;
    padding: 8px 20px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: var(--moss) !important;
    cursor: pointer;
    transition: all .18s;
}

[data-testid="stRadio"] label:hover {
    background: var(--leaf) !important;
    color: #fff !important;
    border-color: var(--leaf) !important;
}

/* ──────────── BUTTON ──────────── */
.stButton > button {
    background: linear-gradient(135deg, var(--moss), var(--leaf)) !important;
    color: #fff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: .5px !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 14px 40px !important;
    width: 100% !important;
    box-shadow: 0 6px 20px rgba(45,80,22,.3) !important;
    transition: all .2s !important;
    margin-top: 8px;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 28px rgba(45,80,22,.4) !important;
    background: linear-gradient(135deg, var(--soil), var(--moss)) !important;
}

/* ──────────── RESULT ──────────── */
.result-hero {
    background: linear-gradient(135deg, var(--moss) 0%, var(--leaf) 100%);
    border-radius: 24px;
    padding: 40px 44px;
    position: relative;
    overflow: hidden;
    margin-bottom: 20px;
}

.result-hero::after {
    content: "🌾";
    position: absolute;
    right: 32px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 96px;
    opacity: .15;
    pointer-events: none;
}

.result-tag {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(255,255,255,.65);
    margin-bottom: 10px;
}

.result-crop {
    font-family: 'Playfair Display', serif;
    font-size: clamp(36px, 5vw, 58px);
    font-weight: 800;
    color: #fff;
    margin: 0 0 10px;
    line-height: 1;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.result-desc {
    color: rgba(255,255,255,.75);
    font-size: 14px;
    font-weight: 300;
    max-width: 480px;
}

/* ──────────── ADVISORY GRID ──────────── */
.advisory-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 16px;
    margin-top: 4px;
}

.adv-tile {
    background: #fff;
    border: 1px solid #E5EDD8;
    border-radius: 18px;
    padding: 24px 26px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 2px 16px rgba(45,80,22,.06);
    transition: transform .2s, box-shadow .2s;
}

.adv-tile:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 28px rgba(45,80,22,.12);
}

.adv-tile::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    border-radius: 18px 18px 0 0;
}

.adv-tile.t1::before { background: linear-gradient(90deg, #3D9A5C, #7AAE5C); }
.adv-tile.t2::before { background: linear-gradient(90deg, #C8960C, #F2A30F); }
.adv-tile.t3::before { background: linear-gradient(90deg, #2D72B8, #5BA4D8); }
.adv-tile.t4::before { background: linear-gradient(90deg, #8B3A9B, #C46FD4); }
.adv-tile.t5::before { background: linear-gradient(90deg, #D64B2B, #F27B5C); }

.adv-icon {
    font-size: 28px;
    margin-bottom: 12px;
    display: block;
    line-height: 1;
}

.adv-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #9AAD88;
    margin-bottom: 8px;
}

.adv-text {
    font-size: 14px;
    line-height: 1.65;
    color: var(--soil);
    font-weight: 400;
}

.adv-text b { color: var(--moss); font-weight: 600; }

/* ──────────── METRICS ROW ──────────── */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 20px;
}

.metric-chip {
    background: var(--cream);
    border: 1px solid #DDE8C8;
    border-radius: 14px;
    padding: 16px 20px;
    text-align: center;
}

.metric-chip .val {
    font-family: 'Playfair Display', serif;
    font-size: 26px;
    font-weight: 700;
    color: var(--moss);
    display: block;
}

.metric-chip .lbl {
    font-size: 11px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #9AAD88;
}

/* ──────────── DIVIDER ──────────── */
hr.fancy {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #C8D9B0, transparent);
    margin: 32px 0;
}

/* ──────────── COLUMN HEADERS ──────────── */
.col-header {
    font-size: 13px;
    font-weight: 600;
    color: var(--earth);
    letter-spacing: .5px;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 7px;
}

</style>
""", unsafe_allow_html=True)


# ── HERO ──────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
  <div class="hero-grid">
    <div>
      <div class="hero-tag">✦ AI-Powered · Precision Agriculture</div>
      <h1 class="hero-title">AgriSmart<br><span>Crop Advisor</span></h1>
      <p class="hero-sub">
        Enter your soil nutrient levels and local climate data to receive
        an intelligent crop recommendation with a full agronomic advisory report.
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

# ── INPUT SECTION ─────────────────────────────────────
st.markdown('<div class="section-label">📋 &nbsp;Input Parameters</div>', unsafe_allow_html=True)

with st.container():
    st.markdown("""
    <div style="background:#fff;border:1px solid #E5EDD8;border-radius:20px;
                padding:32px 36px 8px;margin-bottom:4px;
                box-shadow:0 2px 24px rgba(45,80,22,.07)">
    """, unsafe_allow_html=True)

    col_l, col_r = st.columns(2, gap="large")

    with col_l:
        st.markdown('<div class="col-header">🧪 Soil Nutrients & pH</div>', unsafe_allow_html=True)
        N  = st.slider("Nitrogen (N) — kg/ha",    0,   200, 50, help="Available nitrogen in the soil")
        P  = st.slider("Phosphorus (P) — kg/ha",  0,   200, 50, help="Available phosphorus in the soil")
        K  = st.slider("Potassium (K) — kg/ha",   0,   200, 50, help="Available potassium in the soil")
        ph = st.slider("Soil pH",                0.0, 14.0, 6.5, step=0.1)

    with col_r:
        st.markdown('<div class="col-header">🌤️ Climate Conditions</div>', unsafe_allow_html=True)
        temperature = st.slider("Temperature (°C)",  0.0,  60.0, 25.0, step=0.5)
        humidity    = st.slider("Humidity (%)",       0.0, 100.0, 60.0, step=0.5)
        rainfall    = st.slider("Rainfall (mm)",      0.0, 500.0, 100.0, step=1.0)

    st.markdown("</div>", unsafe_allow_html=True)

# ── OBJECTIVE ─────────────────────────────────────────
st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
st.markdown('<div class="section-label">🎯 &nbsp;Farming Objective</div>', unsafe_allow_html=True)

st.markdown("""
<div style="background:#fff;border:1px solid #E5EDD8;border-radius:20px;
            padding:24px 36px 28px;margin-bottom:4px;
            box-shadow:0 2px 24px rgba(45,80,22,.07)">
""", unsafe_allow_html=True)

objective = st.radio(
    "Choose what you want to optimise for",
    ["🌾 High Yield", "💧 Low Water Usage", "🌿 Organic Farming", "💰 Profit Maximisation"],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("</div>", unsafe_allow_html=True)

# ── BUTTON ────────────────────────────────────────────
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
run = st.button("🔍 &nbsp; Analyse & Generate Advisory Report")

# ── RESULTS ───────────────────────────────────────────
if run:
    data = pd.DataFrame(
        [[N, P, K, temperature, humidity, ph, rainfall]],
        columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    )
    crop = model.predict(data)[0]
    obj_clean = objective.split(" ", 1)[-1]          # strip emoji

    st.markdown("<hr class='fancy'>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">✅ &nbsp;Recommendation</div>', unsafe_allow_html=True)

    # ── Result hero banner ──
    st.markdown(f"""
    <div class="result-hero">
      <div class="result-tag">Recommended Crop</div>
      <div class="result-crop">{crop}</div>
      <div class="result-desc">
        Based on your soil profile (N·P·K), pH, temperature, humidity,
        and rainfall — <b style="color:#fff">{crop.title()}</b> offers the
        best agronomic fit for your field conditions.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Quick metrics ──
    st.markdown(f"""
    <div class="metrics-row">
      <div class="metric-chip">
        <span class="val">{ph}</span>
        <span class="lbl">Soil pH</span>
      </div>
      <div class="metric-chip">
        <span class="val">{temperature}°</span>
        <span class="lbl">Temperature</span>
      </div>
      <div class="metric-chip">
        <span class="val">{rainfall}mm</span>
        <span class="lbl">Rainfall</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Advisory tiles ──
    st.markdown('<div class="section-label">📑 &nbsp;Full Advisory Report</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="advisory-grid">

      <div class="adv-tile t1">
        <span class="adv-icon">💧</span>
        <div class="adv-label">Irrigation</div>
        <div class="adv-text">
          With <b>{rainfall} mm</b> rainfall and <b>{humidity}% humidity</b>, plan
          supplemental irrigation carefully. Avoid waterlogging — {crop.title()} is
          sensitive to root saturation during early growth.
        </div>
      </div>

      <div class="adv-tile t2">
        <span class="adv-icon">⚗️</span>
        <div class="adv-label">Fertiliser</div>
        <div class="adv-text">
          Current N·P·K stands at <b>{N}·{P}·{K} kg/ha</b>. Balance applications
          to meet the nutrient uptake profile of {crop.title()} and prevent
          nutrient lock-out at pH <b>{ph}</b>.
        </div>
      </div>

      <div class="adv-tile t3">
        <span class="adv-icon">🐛</span>
        <div class="adv-label">Pest & Disease</div>
        <div class="adv-text">
          Monitor {crop.title()} weekly for early pest or fungal symptoms —
          especially at <b>{humidity}% humidity</b>, which raises disease pressure.
          Apply preventive biological controls where possible.
        </div>
      </div>

      <div class="adv-tile t4">
        <span class="adv-icon">📅</span>
        <div class="adv-label">Seasonal Planning</div>
        <div class="adv-text">
          Follow the standard sowing, irrigation, and harvest calendar for
          <b>{crop.title()}</b>. Align sowing with the onset of the expected
          rainfall window to minimise irrigation costs.
        </div>
      </div>

      <div class="adv-tile t5">
        <span class="adv-icon">🎯</span>
        <div class="adv-label">Objective — {obj_clean}</div>
        <div class="adv-text">
          Optimising for <b>{obj_clean}</b>: fine-tune variety selection,
          input intensity, and market timing to maximise the specific
          outcome you are targeting with <b>{crop.title()}</b>.
        </div>
      </div>

    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)   # close body-wrap
