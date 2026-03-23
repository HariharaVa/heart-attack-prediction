import streamlit as st
import pickle
import numpy as np
import time

# Load model
model = pickle.load(open('model.pkl', 'rb'))

# ---------- SESSION ----------
if "page" not in st.session_state:
    st.session_state.page = "home"

# ---------- COMMON CSS ----------
st.markdown("""
<style>
.stApp {
    background-color: #e6f2ff;
}

/* Button styling */
div.stButton > button {
    display: block;
    margin: auto;
    background-color: #ff4d6d;
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 220px;
    font-size: 16px;
}

/* Floating circles */
.circle {
    position: fixed;
    border-radius: 50%;
    opacity: 0.25;
    animation: float 8s infinite ease-in-out;
}

.circle1 {width:120px;height:120px;background:pink;left:10%;top:20%;}
.circle2 {width:150px;height:150px;background:#ffeb99;left:80%;top:30%;}
.circle3 {width:100px;height:100px;background:plum;left:50%;top:70%;}
.circle4 {width:130px;height:130px;background:#ffeb99;left:30%;top:60%;}
.circle5 {width:110px;height:110px;background:plum;left:70%;top:80%;}
.circle6 {width:140px;height:140px;background:pink;left:20%;top:80%;}
.circle7 {width:120px;height:120px;background:plum;left:85%;top:10%;}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-30px); }
    100% { transform: translateY(0px); }
}
</style>

<div class="circle circle1"></div>
<div class="circle circle2"></div>
<div class="circle circle3"></div>
<div class="circle circle4"></div>
<div class="circle circle5"></div>
<div class="circle circle6"></div>
<div class="circle circle7"></div>
""", unsafe_allow_html=True)

# ---------- HOME PAGE ----------
if st.session_state.page == "home":

    # ❤️ ECG ANIMATION (4 WAVES)
    st.markdown("""
    <style>
    .ecg-line {
        position: fixed;
        width: 100%;
        height: 100px;
        top: 40%;
        left: 0;
        z-index: 0;
    }

    .ecg-line svg {
        width: 100%;
        height: 100px;
    }

    .ecg-path {
        fill: none;
        stroke: #ff4d6d;
        stroke-width: 3;
        stroke-dasharray: 2000;
        stroke-dashoffset: 2000;
        animation: ecg 4s linear infinite;
    }

    @keyframes ecg {
        0% { stroke-dashoffset: 2000; }
        100% { stroke-dashoffset: 0; }
    }
    </style>

    <div class="ecg-line">
        <svg viewBox="0 0 1000 100">
            <path class="ecg-path"
            d="
            M0,50 L80,50 L100,20 L120,80 L140,50
            L250,50 L270,20 L290,80 L310,50
            L420,50 L440,20 L460,80 L480,50
            L590,50 L610,20 L630,80 L650,50
            L1000,50
            "/>
        </svg>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center; color:#ff4d6d;'> Heart Attack Analysis</h1>", unsafe_allow_html=True)

    st.markdown("""
    <h3 style='text-align:center; color:#555;'>
    Using Machine Learning, we can predict the risk of a heart attack
    </h3>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # PERFECT CENTER BUTTON
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("🔍 Go to Prediction"):
            st.session_state.page = "prediction"
            st.rerun()

# ---------- PREDICTION PAGE ----------
elif st.session_state.page == "prediction":

    st.markdown("<h1 style='text-align:center; color:#ff4d6d;'> Heart Attack Prediction</h1>", unsafe_allow_html=True)

    st.subheader("Enter patient details")

    # Inputs
    age = st.number_input("Age", min_value=1)
    sex = st.selectbox("Sex (0=F,1=M)", [0,1])
    cp = st.selectbox("Chest Pain (0-3)", [0,1,2,3])
    trestbps = st.number_input("Blood Pressure")
    chol = st.number_input("Cholesterol")
    fbs = st.selectbox("FBS", [0,1])
    restecg = st.selectbox("ECG", [0,1,2])
    thalach = st.number_input("Heart Rate")
    exang = st.selectbox("Exercise Angina", [0,1])
    oldpeak = st.number_input("Oldpeak")

    st.markdown("<br>", unsafe_allow_html=True)

    # CENTER PREDICT BUTTON
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        predict_btn = st.button("Predict")

    if predict_btn:
        with st.spinner("Analyzing patient data..."):
            time.sleep(2)

            data = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak]])
            prob = model.predict_proba(data)
            risk = prob[0][1] * 100

        st.markdown("---")

        st.write(f"### Risk: {risk:.2f}%")

        if risk < 30:
            st.success("✅ Low Risk")
        elif risk < 70:
            st.warning("⚠️ Moderate Risk")
        else:
            st.error("🚨 High Risk")

        st.write(f"No Risk: {prob[0][0]*100:.2f}%")
        st.write(f"Heart Risk: {prob[0][1]*100:.2f}%")

    st.markdown("---")

    # CENTER BACK BUTTON
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        back_btn = st.button("⬅ Back to Home")

    if back_btn:
        st.session_state.page = "home"
        st.rerun()

    # CHATBOT
    st.markdown("## 🤖 Health Assistant")

    questions = {
        "What is a heart attack?": "Blockage of blood flow to heart.",
        "Symptoms?": "Chest pain, sweating, breathlessness.",
        "Causes?": "Cholesterol, BP, smoking.",
        "Prevention?": "Healthy lifestyle.",
        "High BP effect?": "Increases risk.",
        "Cholesterol?": "Fat affecting arteries.",
        "Exercise helps?": "Yes, reduces risk.",
        "ECG?": "Heart activity test.",
        "Risk factors?": "Age, diabetes, smoking.",
        "When to see doctor?": "If chest pain occurs."
    }

    q = st.selectbox("Ask a question", list(questions.keys()))

    if q:
        st.info(questions[q])