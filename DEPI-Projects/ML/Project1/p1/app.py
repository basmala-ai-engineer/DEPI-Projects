
import os

# Reduce OpenBLAS thread usage to avoid memory allocation errors
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

from pathlib import Path

import joblib
import numpy as np
import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Boston Housing | Price Predictor",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "boston_model.pkl"

HOUSE_IMAGE_URL = (
    "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9"
    "?auto=format&fit=crop&w=1200&q=85"
)

MEAN_PRICE = 454342.94
MIN_PRICE = 105000
MAX_PRICE = 1024800


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)


try:
    model = load_model()
    model_error = None
except Exception as exc:
    model = None
    model_error = str(exc)


# =========================================================
# THEME
# =========================================================

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

dark_mode = st.session_state.dark_mode

if dark_mode:
    bg = "#171522"
    surface = "#211e30"
    text = "#f6f1ff"
    muted = "#b8afcc"
    border = "#39324d"
    input_bg = "#29243b"
else:
    bg = "#f7f5fc"
    surface = "#ffffff"
    text = "#29213e"
    muted = "#777087"
    border = "#e8e1f2"
    input_bg = "#ffffff"


# =========================================================
# STYLING
# =========================================================

st.markdown(
    f"""
    <style>
    @import url(
      'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background: {bg};
        color: {text};
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    [data-testid="stToolbar"] {{
        visibility: hidden;
        height: 0%;
    }}

    #MainMenu, footer {{
        visibility: hidden;
    }}

    .block-container {{
        max-width: 1250px;
        padding-top: 1.4rem;
        padding-bottom: 3rem;
    }}

    .hero {{
        background: linear-gradient(120deg, #51417f 0%, #7965ad 60%, #a99ad0 100%);
        padding: 30px;
        border-radius: 24px;
        color: #ffffff;
        margin-bottom: 24px;
        box-shadow: 0 12px 32px rgba(77, 58, 119, 0.17);
    }}

    .eyebrow {{
        font-size: 12px;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-weight: 700;
        color: #f0dca0;
        margin-bottom: 10px;
    }}

    .hero h1 {{
        font-size: clamp(28px, 4vw, 42px);
        font-weight: 800;
        line-height: 1.15;
        margin: 0 0 12px 0;
        color: #ffffff;
    }}

    .hero p {{
        font-size: 15px;
        line-height: 1.7;
        color: #f0ebfb;
        margin: 0;
        max-width: 700px;
    }}

    .section-title {{
        color: {text};
        font-size: 20px;
        font-weight: 800;
        margin: 8px 0 5px 0;
    }}

    .section-subtitle {{
        color: {muted};
        font-size: 13px;
        margin-bottom: 18px;
    }}

    .panel {{
        background: {surface};
        border: 1px solid {border};
        border-radius: 20px;
        padding: 23px;
        margin-bottom: 20px;
        box-shadow: 0 5px 20px rgba(44, 31, 76, 0.035);
    }}

    .result-label {{
        color: {muted};
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 8px;
    }}

    .price {{
        color: #8870bd;
        font-size: clamp(30px, 4vw, 43px);
        font-weight: 800;
        line-height: 1.2;
        overflow-wrap: anywhere;
    }}

    .gold-line {{
        height: 4px;
        border-radius: 8px;
        background: linear-gradient(90deg, #c6a65b, #f0dca0);
        margin: 17px 0;
    }}

    .small-note {{
        color: {muted};
        font-size: 12px;
        line-height: 1.6;
    }}

    .tag {{
        display: inline-block;
        padding: 6px 11px;
        border-radius: 999px;
        background: rgba(137, 112, 189, 0.13);
        color: #a18acc;
        font-size: 11px;
        font-weight: 700;
        margin-bottom: 10px;
    }}

    .footer {{
        color: {muted};
        font-size: 12px;
        text-align: center;
        padding-top: 15px;
    }}

    div[data-testid="stSlider"] label,
    div[data-testid="stNumberInput"] label {{
        color: {text};
        font-weight: 600;
    }}

    div[data-testid="stMetric"] {{
        background: {surface};
        border: 1px solid {border};
        padding: 16px;
        border-radius: 15px;
    }}

    div[data-testid="stMetricLabel"] {{
        color: {muted};
    }}

    div[data-testid="stMetricValue"] {{
        color: {text};
    }}

    .stButton button {{
        border-radius: 12px;
        border: 1px solid {border};
        font-weight: 600;
    }}

    div[data-testid="stImage"] img {{
        border-radius: 17px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# TOP BAR
# =========================================================

top_left, top_right = st.columns([5, 1])

with top_left:
    st.markdown(
        f"""
        <div style="font-size:14px;font-weight:800;color:{text};">
            <span style="color:#a18acc;">◆</span>
            BOSTON HOUSING
            <span style="color:{muted};font-weight:500;">
                &nbsp; / &nbsp; Price Intelligence
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with top_right:
    theme_label = "☀️ Light mode" if dark_mode else "🌙 Dark mode"
    if st.button(theme_label, use_container_width=True):
        st.session_state.dark_mode = not dark_mode
        st.rerun()


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">AI · REAL ESTATE ANALYTICS</div>
        <h1>Find the value of your next home.</h1>
        <p>
            Explore estimated housing prices using machine learning.
            Adjust the property characteristics and discover how
            the predicted value changes.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# PROPERTY IMAGE AND INPUTS
# =========================================================

left_col, right_col = st.columns([1.03, 1.0], gap="large")

with left_col:
    st.markdown(
        '<div class="section-title">Property overview</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle">A visual introduction to your property analysis.</div>',
        unsafe_allow_html=True,
    )

    try:
        st.image(
            HOUSE_IMAGE_URL,
            use_container_width=True,
        )
    except Exception:
        st.markdown(
            """
            <div class="panel" style="text-align:center;padding:70px 20px;">
                <div style="font-size:45px;">⌂</div>
                <div style="font-weight:700;">Boston Housing</div>
                <div class="small-note">Property image is unavailable.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="panel">
            <span class="tag">PROPERTY ANALYSIS</span>
            <div style="font-size:18px;font-weight:800;color:{text};">
                Your home, analyzed with AI
            </div>
            <p class="small-note">
                Modify the available characteristics to calculate
                an estimate from your trained machine-learning model.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


with right_col:
    st.markdown(
        '<div class="section-title">Adjust property details</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle">Move the sliders to explore different scenarios.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="panel">',
        unsafe_allow_html=True,
    )

    rm = st.slider(
        "Average number of rooms (RM)",
        min_value=4.0,
        max_value=8.0,
        value=6.0,
        step=0.1,
        help="Average number of rooms per dwelling.",
    )

    lstat = st.slider(
        "Lower-status population indicator (LSTAT)",
        min_value=2.0,
        max_value=38.0,
        value=12.0,
        step=0.5,
        help="The LSTAT feature from the dataset; it is a statistical indicator, not a judgment about an individual.",
    )

    ptratio = st.slider(
        "Pupil-teacher ratio (PTRATIO)",
        min_value=12.5,
        max_value=22.0,
        value=18.0,
        step=0.5,
        help="Pupil-teacher ratio used by the model.",
    )

    st.markdown("</div>", unsafe_allow_html=True)

    predict_clicked = st.button(
        "Calculate estimated price  →",
        type="primary",
        use_container_width=True,
    )


# =========================================================
# PREDICTION
# =========================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">Prediction dashboard</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-subtitle">Estimated value and comparison with the dataset average.</div>',
    unsafe_allow_html=True,
)

if model is None:
    st.error(
        "The trained model could not be loaded. "
        "Make sure boston_model.pkl is in the same folder as app.py."
    )
    if model_error:
        st.caption(
            "There is a model-loading issue. Check the Python environment "
            "and the scikit-learn version used to save the model."
        )
    st.stop()


# Use the three features selected for this project.
features = np.array([[rm, lstat, ptratio]], dtype=float)

try:
    raw_prediction = float(model.predict(features)[0])

    # If the model predicts the original Boston target in thousands
    # of dollars, convert it to dollars for display.
    predicted_price = (
        raw_prediction * 1000
        if abs(raw_prediction) < 2000
        else raw_prediction
    )

except Exception:
    st.error(
        "The model could not calculate a prediction from these inputs. "
        "Check that the model was trained using exactly these three "
        "features in this order: RM, LSTAT, PTRATIO."
    )
    st.stop()


predicted_price = max(0, predicted_price)
difference = predicted_price - MEAN_PRICE
difference_pct = (difference / MEAN_PRICE) * 100 if MEAN_PRICE else 0

if predicted_price > MEAN_PRICE:
    comparison_text = f"{abs(difference_pct):.1f}% above the dataset average"
elif predicted_price < MEAN_PRICE:
    comparison_text = f"{abs(difference_pct):.1f}% below the dataset average"
else:
    comparison_text = "Equal to the dataset average"


# =========================================================
# RESULTS CARDS
# =========================================================

result_left, result_right = st.columns([1.15, 1], gap="large")

with result_left:
    st.markdown(
        f"""
        <div class="panel">
            <div class="result-label">ESTIMATED PROPERTY VALUE</div>
            <div class="price">${predicted_price:,.0f}</div>
            <div class="gold-line"></div>
            <div style="font-size:14px;font-weight:700;color:{text};">
                {comparison_text}
            </div>
            <p class="small-note">
                This is a machine-learning estimate, not a formal appraisal
                or a guaranteed market selling price.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with result_right:
    st.markdown(
        f"""
        <div class="panel">
            <div class="result-label">DATASET REFERENCE</div>
            <div class="price" style="font-size:32px;">
                ${MEAN_PRICE:,.0f}
            </div>
            <div class="gold-line"></div>
            <div style="font-size:14px;font-weight:700;color:{text};">
                Average reference value
            </div>
            <p class="small-note">
                Comparison baseline configured for this dashboard.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# PRICE INDICATOR
# =========================================================

bounded_price = min(max(predicted_price, MIN_PRICE), MAX_PRICE)
progress = (
    (bounded_price - MIN_PRICE) / (MAX_PRICE - MIN_PRICE)
    if MAX_PRICE > MIN_PRICE
    else 0
)
progress_pct = max(0, min(100, progress * 100))

st.markdown(
    f"""
    <div class="panel">
        <div class="section-title" style="font-size:17px;">
            Price position
        </div>
        <p class="small-note">
            Where the estimated value falls within the configured
            reference range.
        </p>
        <div style="
            height:12px;
            background:{border};
            border-radius:20px;
            overflow:hidden;
            margin:18px 0 10px 0;">
            <div style="
                width:{progress_pct:.2f}%;
                height:100%;
                border-radius:20px;
                background:linear-gradient(90deg,#7965ad,#c6a65b);">
            </div>
        </div>
        <div style="
            display:flex;
            justify-content:space-between;
            gap:12px;
            color:{muted};
            font-size:12px;">
            <span>${MIN_PRICE:,.0f}</span>
            <span>${MAX_PRICE:,.0f}</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# INPUT SUMMARY
# =========================================================

st.markdown(
    '<div class="section-title">Your selected characteristics</div>',
    unsafe_allow_html=True,
)

m1, m2, m3 = st.columns(3)

m1.metric("Average rooms (RM)", f"{rm:.1f}")
m2.metric("LSTAT indicator", f"{lstat:.1f}")
m3.metric("Pupil-teacher ratio", f"{ptratio:.1f}")

st.markdown(
    f"""
    <div class="footer">
        Boston Housing Price Predictor · Built with Python, Streamlit and Machine Learning
        <br>
        Estimates depend on the training data and model quality.
    </div>
    """,
    unsafe_allow_html=True,
)
