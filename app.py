import streamlit as st
import pandas as pd
import pickle
st.markdown("""
<style>

/* ===== GLOBAL BACKGROUND ===== */
.stApp {
    background: radial-gradient(circle at top, #1f4037, #0f2027);
    overflow: hidden;
}

/* ===== GLASS CONTAINER ===== */
.block-container {
    background: rgba(255,255,255,0.06);
    padding: 2rem;
    border-radius: 25px;
    backdrop-filter: blur(15px);
    box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

/* ===== MOVING SKY (PARALLAX) ===== */
.sky {
    position: fixed;
    width: 200%;
    height: 100%;
    background: url('https://www.transparenttextures.com/patterns/stardust.png');
    animation: skyMove 60s linear infinite;
    z-index: -3;
    opacity: 0.3;
}

@keyframes skyMove {
    from { transform: translateX(0); }
    to { transform: translateX(-50%); }
}

/* ===== ROAD ===== */
.road {
    position: fixed;
    bottom: 0;
    width: 100%;
    height: 150px;
    background: #1c1c1c;
    z-index: -1;
}

/* ROAD LINES */
.road::before {
    content: "";
    position: absolute;
    width: 300%;
    height: 6px;
    background: repeating-linear-gradient(
        to right,
        white 0px,
        white 50px,
        transparent 50px,
        transparent 100px
    );
    top: 70px;
    animation: roadMove 1.2s linear infinite;
}

@keyframes roadMove {
    from { transform: translateX(0); }
    to { transform: translateX(-60%); }
}

/* ===== CAR ===== */
.car {
    position: fixed;
    bottom: 50px;
    left: -250px;
    width: 200px;
    height: 90px;
    background: url('https://cdn-icons-png.flaticon.com/512/744/744465.png') no-repeat center;
    background-size: contain;
    animation: drive 6s linear infinite;
    filter: drop-shadow(0 0 20px rgba(255,0,0,0.8));
}

/* SPEED GLOW TRAIL */
.car::after {
    content: "";
    position: absolute;
    left: -80px;
    top: 30px;
    width: 80px;
    height: 20px;
    background: linear-gradient(to right, rgba(255,0,0,0.6), transparent);
    filter: blur(10px);
}

/* CAR MOVEMENT */
@keyframes drive {
    0% { left: -250px; }
    100% { left: 120%; }
}

/* ===== TITLE ===== */
h1 {
    text-align: center;
    font-size: 40px;
    color: white;
    text-shadow: 0 0 15px #00f2ff, 0 0 30px #0072ff;
}

/* ===== BUTTON ===== */
.stButton>button {
    background: linear-gradient(135deg, #00f2ff, #0072ff);
    color: white;
    border-radius: 12px;
    padding: 12px 25px;
    border: none;
    transition: 0.3s ease;
    font-weight: bold;
}

.stButton>button:hover {
    transform: scale(1.08);
    box-shadow: 0 0 20px #00f2ff;
}

/* ===== INPUT STYLING ===== */
.stNumberInput input, .stSelectbox div {
    border-radius: 10px !important;
}

/* ===== RESULT CARD ===== */
.result-box {
    margin-top: 20px;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    font-size: 24px;
    color: white;
    background: rgba(0,255,200,0.1);
    box-shadow: 0 0 25px rgba(0,255,200,0.4);
    animation: fadeIn 1s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

</style>

<div class="sky"></div>
<div class="road"></div>
<div class="car"></div>

""", unsafe_allow_html=True)
# 🔹 Load model
with open("model_pipeline.pkl", "rb") as f:
    model = pickle.load(f)

st.set_page_config(page_title="Car Price Predictor", layout="centered")

st.title("🚗 Car Price Predictor")
st.write("Enter car details to predict price")

# 🔹 User Inputs

symboling = st.selectbox("Symboling", [-3, -2, -1, 0, 1, 2, 3])

carbody = st.selectbox("Car Body", ["sedan", "hatchback", "wagon", "hardtop", "convertible"])

drivewheel = st.selectbox("Drive Wheel", ["fwd", "rwd", "4wd"])

enginelocation = st.selectbox("Engine Location", ["front", "rear"])

wheelbase = st.number_input("Wheelbase", min_value=80.0, max_value=120.0, value=95.0)

carlength = st.number_input("Car Length", min_value=140.0, max_value=210.0, value=170.0)

carwidth = st.number_input("Car Width", min_value=60.0, max_value=80.0, value=65.0)

carheight = st.number_input("Car Height", min_value=45.0, max_value=60.0, value=52.0)

enginetype = st.selectbox("Engine Type", ["ohc", "ohcf", "ohcv", "dohc", "l", "rotor"])

cylindernumber = st.selectbox("Cylinder Number", ["two", "three", "four", "five", "six", "eight", "twelve"])

enginesize = st.number_input("Engine Size", min_value=50, max_value=350, value=120)

horsepower = st.number_input("Horsepower", min_value=40, max_value=300, value=100)

citympg = st.number_input("City MPG", min_value=10, max_value=60, value=25)

# 🔹 Predict button
if st.button("Predict Price 💰"):

    input_data = pd.DataFrame({
        "symboling": [symboling],
        "carbody": [carbody],
        "drivewheel": [drivewheel],
        "enginelocation": [enginelocation],
        "wheelbase": [wheelbase],
        "carlength": [carlength],
        "carwidth": [carwidth],
        "carheight": [carheight],
        "enginetype": [enginetype],
        "cylindernumber": [cylindernumber],
        "enginesize": [enginesize],
        "horsepower": [horsepower],
        "citympg": [citympg]
    })

    prediction = model.predict(input_data)[0]

    st.success(f"💰 Estimated Car Price: $ {round(prediction, 2)}")