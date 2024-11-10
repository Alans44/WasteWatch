import streamlit as st
import helper
import settings
from pathlib import Path

st.set_page_config(
    page_title="Waste Detection",
    layout="wide"
)
st.markdown(
    """
    <style>
        /* Remove padding and margins */
        .block-container {
            padding: 0;
        }
        /* Full-screen webcam feed */
        #full-screen-video > img {
            width: 100%;
            height: 100vh;
            object-fit: cover;
        }
        /* Detection Log Styling */
        .stRecyclable {
            background-color: #A8E6CF; /* Light green */
            padding: 1rem;
            border-radius: 0.5rem;
            font-size: 1rem;
            margin-bottom: 1rem;
        }
        .stNonRecyclable {
            background-color: #FFD3B6; /* Light orange */
            padding: 1rem;
            border-radius: 0.5rem;
            font-size: 1rem;
            margin-bottom: 1rem;
        }
        .stHazardous {
            background-color: #FF8B94; /* Light red */
            padding: 1rem;
            border-radius: 0.5rem;
            font-size: 1rem;
            margin-bottom: 1rem;
        }
        /* Hide Streamlit's default header and footer */
        header, footer {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True
)

hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    </style>
    """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Load model
model_path = Path(settings.DETECTION_MODEL)
try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

# Start Detection
if st.button('Start Detection'):
    st.session_state['detection_started'] = True

if 'detection_started' in st.session_state and st.session_state['detection_started']:
    # Full-screen webcam feed
    st_frame = st.empty()
    st_frame.markdown('<div id="full-screen-video"></div>', unsafe_allow_html=True)
    helper.play_webcam(model, st_frame)
else:
    st.markdown("<h1 style='text-align: center;'>Intelligent Waste Segregation System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Click the button below to start object detection.</p>", unsafe_allow_html=True)

# Detection Log (Collapsible Sidebar)
with st.sidebar:
    st.markdown("<h2>Detection Log</h2>", unsafe_allow_html=True)
    if 'recyclable_placeholder' not in st.session_state:
        st.session_state['recyclable_placeholder'] = st.empty()
    if 'non_recyclable_placeholder' not in st.session_state:
        st.session_state['non_recyclable_placeholder'] = st.empty()
    if 'hazardous_placeholder' not in st.session_state:
        st.session_state['hazardous_placeholder'] = st.empty()
