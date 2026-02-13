import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import requests
from PIL import Image
import io
import base64

# Page configuration
st.set_page_config(
    page_title="FarmErgoDesign",
    page_icon="🚜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* Header styling */
    .header-container {
        background: linear-gradient(90deg, #84cc16 0%, #65a30d 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }

    .header-title {
        color: white;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .header-subtitle {
        color: #b8d4f0;
        font-size: 1.2rem;
        margin-bottom: 0;
    }

    /* Card styling */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 5px solid #667eea;
    }

    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    /* Compact image styling */
    .compact-image {
        border-radius: 10px;
        margin: 5px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    /* Image container styling */
    .image-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        margin: 1rem 0;
        text-align: center;
    }

    .image-title {
        color: #1e3c72;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
    }

    /* Enhanced iframe styling */
    .responsive-iframe {
        border: 2px solid #667eea;
        border-radius: 10px;
        width: 100%;
        height: 450px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    .image-fallback {
        background: #f8f9fa;
        border: 2px dashed #dee2e6;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }

    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: white;
        border-radius: 10px;
        padding: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 8px;
        color: #1e3c72;
        font-weight: bold;
    }

    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }

    /* Success/Info boxes */
    .success-box {
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }

    .info-box {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Data dictionaries
male_parameter_data_links = {
    "TRICEP SKINFOLD THICKNESS": "https://docs.google.com/spreadsheets/d/1ZCmaGYd3qkSsp752Vg6YtLuFnkRFvfGR/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "SUPRA ILIAC SKINFOLD THICKNESS": "https://docs.google.com/spreadsheets/d/18SBxbeWA4oRZ85surgCNLqkNKCcUaw80/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "SUBSCAPULAR SKINFOLD THICKNESS": "https://docs.google.com/spreadsheets/d/1prYTlEELDEtXKQ5_QqS_pNMP-e7LN6Sw/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "INDEX FINGER DIAMETER": "https://docs.google.com/spreadsheets/d/1MoU_bTbWUaXEW2JVlvBWR5zHZE4R6hPe/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "HAND GRIP TORQUE (PREFERRED HAND)": "https://docs.google.com/spreadsheets/d/1EnwuVU9x80tOD0WIR8VPz9eg6k8FvDQc/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "BICEP SKINFOLD THICKNESS": "https://docs.google.com/spreadsheets/d/1vQASrXuLBLgJxpwXTaFH0zs4uQhM2AMI/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "TORQUE STRENGTH (BOTH HANDS) SITTING": "https://docs.google.com/spreadsheets/d/1RGwJrnUaAE-zE4SXqBixxSH9f4CdwZxe/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "TORQUE STRENGTH (BOTH HANDS) STANDING": "https://docs.google.com/spreadsheets/d/1LpfVecrj-L4JElmeXxOcbR7AtAVEpzg3/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "TORQUE STRENGTH (PREFERRED HAND) STANDING": "https://docs.google.com/spreadsheets/d/1ReWYA_OSQiiLaBCu6nZMIEN7mKUiIe--/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "FOOT STRENGTH (LEFT) SITTING": "https://docs.google.com/spreadsheets/d/1pwkA1-3LxXio6mR9N0fRD5j59ZHLWVoL/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "LEG STRENGTH (LEFT) SITTING": "https://docs.google.com/spreadsheets/d/1IZ8snaOZNzM8nRjRR6CQhi8cPNgh1m63/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "FOOT STRENGTH (RIGHT) SITTING": "https://docs.google.com/spreadsheets/d/1DhkyTvaUEbNIuC0RJ5wWI07Jiocti3Qk/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "LEG STRENGTH (RIGHT) SITTING": "https://docs.google.com/spreadsheets/d/1z6FrQeTdEnQ7THaxvQ6tmVDi_HrOmptp/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "PULL STRENGTH (RIGHT HAND) SITTING": "https://docs.google.com/spreadsheets/d/1iZh_UEbg0e4CVBu7GnsX7ky_FSdB0Zyd/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "PUSH STRENGTH (RIGHT HAND) SITTING": "https://docs.google.com/spreadsheets/d/1mOHJxI41-3aBI3eBkIRzvjbUUU8b_wmI/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "PULL STRENGTH (LEFT HAND) SITTING": "https://docs.google.com/spreadsheets/d/1tg7VADYTETjX38mhBv49xd91uSpzEsDa/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "PUSH STRENGTH (LEFT HAND) SITTING": "https://docs.google.com/spreadsheets/d/1zK8WbYfyYQsq617__YZ7dytNlQZXLWHW/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "PULL STRENGTH (BOTH HANDS) STANDING": "https://docs.google.com/spreadsheets/d/1clOjgt5mlJQuhanA5f22a5GYnbvvxX-X/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "PUSH STRENGTH (BOTH HANDS) STANDING": "https://docs.google.com/spreadsheets/d/1CxkNIO46fwZ6tx18vknQIl8zW9FOhpLw/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "HAND GRIP STRENGTH (LEFT)": "https://docs.google.com/spreadsheets/d/1dDGfVDUVVSbvRR5nTU34OVOoFnRPkDMA/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "HAND GRIP STRENGTH (RIGHT)": "https://docs.google.com/spreadsheets/d/1sV0cSUug0YqsUS5RZ5LlqVBJEYfoajHD/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "FUNCTIONAL LEG LENGTH": "https://docs.google.com/spreadsheets/d/1Z3jl2QRRUhEUSt5iMgG2qNNrUNGpBN7U/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "FOOT BREADTH (BALL OF THE FOOT)": "https://docs.google.com/spreadsheets/d/1el3sfpgzM_qy99Z7vHRjJsOudZMizoVA/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "INSTEP LENGTH": "https://docs.google.com/spreadsheets/d/1L8XWK5hp9O2ZL5wDV0ByAXcKajsSLPfL/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "FOOT LENGTH": "https://docs.google.com/spreadsheets/d/1taDD5XAHYMLJ4i9S2yGWn5BxaVj2SiMq/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "KNEE-KNEE BREADTH": "https://docs.google.com/spreadsheets/d/1oyXggrQERdpEezbQbdL4P8RSQNMlIyGZ/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "ELBOW-ELBOW BREADTH SITTING": "https://docs.google.com/spreadsheets/d/189IsU0I9lENImTiUq35sue47lfBM8Wr2/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "HIP BREADTH SITTING": "https://docs.google.com/spreadsheets/d/1h2deEehr7yViTDXMIT-x8MS2_XZzCET5/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "ABDOMINAL DEPTH SITTING": "https://docs.google.com/spreadsheets/d/1TV03RyP-i-Id3m6a1BQ3hisaM0c2PR7u/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "BUTTOCK POPLITEAL LENGTH": "https://docs.google.com/spreadsheets/d/1AGkiXISyf6LPfB__mLM_hE2gTto6alei/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "BUTTOCK KNEE LENGTH": "https://docs.google.com/spreadsheets/d/1qFm8UYkHExsok_4CnMw5Ss4Y6H0d1pIy/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "HAND BREADTH": "https://docs.google.com/spreadsheets/d/11o4NvGBwt6Ezj-YQMpXaM51BE7gdC21f/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "HAND BREADTH ACROSS THUMB": "https://docs.google.com/spreadsheets/d/1z6v2bCOLvkA5OF_UWbFSEykmIJCz45rK/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "PALM LENGTH": "https://docs.google.com/spreadsheets/d/1QlUkGJ9pqINDt7CJx7haofyX2KiCVhn2/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "HAND LENGTH": "https://docs.google.com/spreadsheets/d/1oUEHIbn3M7xFFkR-g4TNgGQ-pBOPC52v/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "ELBOW GRIP LENGTH": "https://docs.google.com/spreadsheets/d/1VoBIch1m-Fq9Cx_jCAfHhGXpnh2FumyO/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "FOREARM HAND LENGTH": "https://docs.google.com/spreadsheets/d/1MRAY-pD6kBRchOO39xwcklClsjRe32c0/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "CORONOID FOSSA TO HAND LENGTH": "https://docs.google.com/spreadsheets/d/16rL886ivZyvDyLvAwfHq9SGMg9dicUqS/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "HEAD BREADTH": "https://docs.google.com/spreadsheets/d/1JF_5YQN2XQKEwQcmRByjPAjqetq-fzmB/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "HEAD LENGTH": "https://docs.google.com/spreadsheets/d/1oUEHIbn3M7xFFkR-g4TNgGQ-pBOPC52v/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "MAXIMUM GRIP LENGTH": "https://docs.google.com/spreadsheets/d/18H7dNES7iV7iVDwKxMLCrRgNCW7NlzST/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "GRIP SPAN": "https://docs.google.com/spreadsheets/d/1ccceJILRkIqCYgLefDWJJnbMRHCDaS8n/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "FIRST PHALANX DIGIT III LENGTH": "https://docs.google.com/spreadsheets/d/16wv7bRBjhSKApyZfJo204FiyOQGOWn1O/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "HAND THICKNESS AT METACARPAL III": "https://docs.google.com/spreadsheets/d/1pUBxfJGv0s0yClrRyiXsT9ciweXuozCm/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "POPLITEAL HEIGHT SITTING": "https://docs.google.com/spreadsheets/d/1FDgQcg_Km8sbxBiEP38P5QUG4LIHgyYO/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "KNEE HEIGHT SITTING": "https://docs.google.com/spreadsheets/d/1kcgb3tz3m_8n8XHVWVb4fnQMZyxe48Ze/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "THIGH CLEARANCE HEIGHT SITTING": "https://docs.google.com/spreadsheets/d/16PxGce7y87JEEwWFQwKkbP9GiU0QPusF/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "ELBOW REST HEIGHT": "https://docs.google.com/spreadsheets/d/1llfMrRjqFNLSUfh2d_bizOxiCgjTgHow/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "SITTING ACROMIAL HEIGHT": "https://docs.google.com/spreadsheets/d/1XUSsRJt4FD-xbX6AwYLIQAAfZrISEPm9/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "SITTING EYE HEIGHT": "https://docs.google.com/spreadsheets/d/1gmTDJHybTtO0la4qjjvp4f8mMxQqzt9R/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "SITTING HEIGHT": "https://docs.google.com/spreadsheets/d/1NCzQBlJxoFTCS6IPqych3Ai_Jk6K2uLd/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "VERTICAL GRIP REACH SITTING": "https://docs.google.com/spreadsheets/d/1NCzQBlJxoFTCS6IPqych3Ai_Jk6K2uLd/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "MIDDLE FINGER PALM GRIP DIAMETER": "https://docs.google.com/spreadsheets/d/1GNTiPw1fYoAIa4lwTkkeH-zgJVVwOIHn/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "GRIP DIAMETER (OUTSIDE)": "https://docs.google.com/spreadsheets/d/16Iz-F6wSv21McwtwrHynJdZbJ6MC4MZE/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "GRIP DIAMETER (INSIDE)": "https://docs.google.com/spreadsheets/d/1AZdGwQR6fu3kTEdepiq2QpE95oiAicCG/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "WRIST CIRCUMFERENCE": "https://docs.google.com/spreadsheets/d/1qa-Lnvi9EkI8fEoknj-nHJlYHjA26oLd/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "CALF CIRCUMFERENCE": "https://docs.google.com/spreadsheets/d/1yZlMJkPVS4YpWq0hof-R0RrLuYyxuKwv/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "THIGH CIRCUMFERENCE": "https://docs.google.com/spreadsheets/d/1hZ0AUUtPmlXI7BeoUmyB5qqYNq1DjKN8/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "WAIST CIRCUMFERENCE": "https://docs.google.com/spreadsheets/d/1X4kOQCbPWMS9JEsus10HaefVufgexJX8/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "CHEST CIRCUMFERENCE": "https://docs.google.com/spreadsheets/d/1B1pFhcvTgl0WpndWiRqDJYjmiiEJhmrM/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "BIMALLELOLAR BREADTH": "https://docs.google.com/spreadsheets/d/1kJ6txrIVmYMJOn5r-gqXEm1VsZINdaot/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "HEEL BREADTH": "https://docs.google.com/spreadsheets/d/1jmle2wSSGS5dnnI-H8jGpFk80JhmWWAg/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "HIP BREADTH": "https://docs.google.com/spreadsheets/d/1DDOBKZP9F_mP07nFQkGMWIAl8woGNqpm/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "WAIST BREADTH": "https://docs.google.com/spreadsheets/d/1fwckFwaGPY9DRq-1QTWHXBZrjSTc7BKm/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "INTERSCYE BREADTH": "https://docs.google.com/spreadsheets/d/1NiDN8oCTSCIe1uHHANE1hWJyGC7R_K5J/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "CHEST BREADTH": "https://docs.google.com/spreadsheets/d/1mHQFjJRO983rZzKnRBYCDvE7vpBU6cmk/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "BIDELTOID BREADTH": "https://docs.google.com/spreadsheets/d/12QtJQqh9QHHp5ae8W_tPCvb91JQUGnlQ/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "BIACROMIAL BREADTH": "https://docs.google.com/spreadsheets/d/1ThS4SEWDEr2Aag1GarCGCkDgJuwbir0i/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "CHEST DEPTH": "https://docs.google.com/spreadsheets/d/17wnjapJueqKnqaJSiRDZmZd7Q3Ainc4E/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "ABDOMINAL EXTENSION TO WALL": "https://docs.google.com/spreadsheets/d/10T2NB-eeFp3zYSJVVy0I2T9ez-OrnMK4/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "WALL TO LUMBOSACRAL DISTANCE": "https://docs.google.com/spreadsheets/d/1-9XRWFpF91QUPw9ovl-eW6PLdF6iRoho/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "WALL TO ACROMION DISTANCE": "https://docs.google.com/spreadsheets/d/1CvKZ8CYGiAd8cHF4swuncVxyAS94G6Xb/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "SHOULDER GRIP LENGTH": "https://docs.google.com/spreadsheets/d/1sB2JE31WZU0Dz_y9w4yjyXYi126FKvYJ/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "THUMB TIP REACH": "https://docs.google.com/spreadsheets/d/1rehSX0_e1noAM8Cf0vP-a2dcSqueXyMX/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "ARM REACH FROM THE WALL": "https://docs.google.com/spreadsheets/d/1ME0sYrJ6zCMdfNqc3xHE_UmlzbdL7g-Z/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "SPAN AKIMBO": "https://docs.google.com/spreadsheets/d/1PrYRrhq6Oi6MYpHvxL0Yaoks7jRNupAE/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "SPAN": "https://docs.google.com/spreadsheets/d/1_gB-Pp_ofPkSdt0vgaZub2VDVOd-udbg/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "SCAPULA TO WAIST BACK LENGTH": "https://docs.google.com/spreadsheets/d/153TH707Zr5Ko9x6-ni6d1hyThJsnsb0-/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "WAIST BACK LENGTH": "https://docs.google.com/spreadsheets/d/1B8-iIGJjl9DeQaBNDFgxFaf0840Vx8L7/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "MENTON TO TOP OF HEAD": "https://docs.google.com/spreadsheets/d/1kKLzOZlwWPrwAm3W869bkX62S5m7fnGr/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "LATERAL MALLEOLUS HEIGHT": "https://docs.google.com/spreadsheets/d/1MvKTIkrnypMn4kMHCUh-Rxn0PQBSVK4L/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "MEDIAL MALLEOLUS HEIGHT": "https://docs.google.com/spreadsheets/d/1r4Uy2E-AJ3b74OH0BeSmq93kYnLtjUYw/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "KNEE HEIGHT": "https://docs.google.com/spreadsheets/d/1Nt4GOs2Jz3BJ04OZ8gD4g94NKcSqhNhR/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "METACARPAL III HEIGHT": "https://docs.google.com/spreadsheets/d/1eho8rsa_Z7J-PrY8Z9iOxup8blCUQ5W_/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "TROCHANTERIC HEIGHT": "https://docs.google.com/spreadsheets/d/1QogxWwY3LUc60cdMnE5EXgILBhn3vYxe/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "ILLIOSPINALE HEIGHT": "https://docs.google.com/spreadsheets/d/1wve9ARaGPdO19PIsWfLl_ylV1qXpClzx/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "ILLIOCRYSTALE HEIGHT": "https://docs.google.com/spreadsheets/d/1jUc137sJBwuE1EiP0UBogJdIFXCuUGBX/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "OLECRANON HEIGHT": "https://docs.google.com/spreadsheets/d/1EdSGoIBBBoj7YhY2dBPEkF-HK2RqfCCe/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "ELBOW HEIGHT": "https://docs.google.com/spreadsheets/d/1DfIUriBHfXkBy9o0iGgVzuRPkCfzFXJc/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "ACROMIAL HEIGHT": "https://docs.google.com/spreadsheets/d/1WrEHWCBPJVKAiTA9iPvZsNYZP0RJdSrA/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "EYE HEIGHT": "https://docs.google.com/spreadsheets/d/1DfIUriBHfXkBy9o0iGgVzuRPkCfzFXJc/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "VERTICAL GRIP REACH": "https://docs.google.com/spreadsheets/d/1OxQ9sxzQEKNuWPzap7JPCG4gdeea9yI6/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "VERTICAL REACH": "https://docs.google.com/spreadsheets/d/13ce8_xmXvZ_dvnzIquohRt1y9p41oumC/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "STATURE": "https://docs.google.com/spreadsheets/d/1bbI7eVFnumvT7mSgEdcbFn4cDnbx9quw/edit?usp=sharing&ouid=115534766381035648538&rtpof=true&sd=true",
    "WEIGHT": "https://docs.google.com/spreadsheets/d/1_tBQFCf9X0JApJqzdJ1eQbGBVUdn90Qt/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true"
}

female_parameter_data_links = {
    "ABDOMINAL DEPTH SITTING": "https://docs.google.com/spreadsheets/d/19cjtJ-r_dlUUKRsC3A8S0exfuoK_VaBD/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "ABDOMINAL EXTENSION TO WALL": "https://docs.google.com/spreadsheets/d/1L_MPt_OVqnQj3FM7okxlR-6OxvBqN2Fl/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "ACROMIAL HEIGHT": "https://docs.google.com/spreadsheets/d/1Lb8kX2giwklOxj9XFvH9KfcoJ7LuKtqi/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "ARM REACH FROM THE WALL": "https://docs.google.com/spreadsheets/d/1q4pvVDHSRp_2pJCZM26h07aItdaC8rM9/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "BIACROMIAL BREADTH": "https://docs.google.com/spreadsheets/d/11IrX91q5EKHAvXL8UTc9VZolpNIwrHBY/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "BICEP SKINFOLD THICKNESS": "https://docs.google.com/spreadsheets/d/1xH03W3yw_CUHgqThDADwYNPwq5HkQhTW/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "BIDELTOID BREADTH": "https://docs.google.com/spreadsheets/d/1-HwMz0o_BuoAZ11JJ2KHlxcRx0DLMLZC/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "BIMALLELOLAR BREADTH": "https://docs.google.com/spreadsheets/d/1ln2UKzQimvZLrud0ArbSOG-OP51ta5oP/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "BUTTOCK KNEE LENGTH": "https://docs.google.com/spreadsheets/d/1xtr-V0yXKyP218P170LuJdbdTMmLhgOh/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "BUTTOCK POPLITEAL LENGTH": "https://docs.google.com/spreadsheets/d/1xHniifcTNgCmaRpd9fBHRmbLeJvdmvEY/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "CALF CIRCUMFERENCE": "https://docs.google.com/spreadsheets/d/1tg5v_vLZTPSiFEVHzk8oZ9k3bvRVsKJx/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "CHEST BREADTH": "https://docs.google.com/spreadsheets/d/1nJxhV2D3aJjAr0J1VL5IvL_I8EE7dOlR/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "CHEST CIRCUMFERENCE": "https://docs.google.com/spreadsheets/d/1HdiV1wVami8M9fN_DB15slcH6buIzwfK/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "CHEST DEPTH": "https://docs.google.com/spreadsheets/d/10q2-dkwGf06rcsPlZtSPY1Q9U-h1KK0Z/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "CORONOID FOSSA TO HAND LENGTH": "https://docs.google.com/spreadsheets/d/156VBv7FuZK23EFaRpcqVNGUxFE136_u_/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "ELBOW GRIP LENGTH": "https://docs.google.com/spreadsheets/d/1GnF-yh2pusZzjKlcZiN8NCG2Svma9Jzk/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "ELBOW HEIGHT": "https://docs.google.com/spreadsheets/d/1MhWuIFmFR3mEMRhL7t_SvI9oqxdFmDti/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "ELBOW REST HEIGHT": "https://docs.google.com/spreadsheets/d/1CkqVe3JG0QB3W21cfLrMzsHj6FJLrC1l/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "ELBOW-ELBOW BREADTH SITTING": "https://docs.google.com/spreadsheets/d/1D_d4qriUFHLvf_b2cJfEfK8i33lCHECD/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "EYE HEIGHT": "https://docs.google.com/spreadsheets/d/1U6ilG09ttmhc6GPeCSsu6FSaat3MiUqQ/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "FIRST PHALANX DIGIT III LENGTH": "https://docs.google.com/spreadsheets/d/1VwnEu2XN0w2ZAk1SR4vvZYk11Q1pRDHt/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "FOOT BREADTH (BALL OF THE FOOT)": "https://docs.google.com/spreadsheets/d/1ug-n2e9RAWH8PfIPStFL9MGzec8PE6LA/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "FOOT LENGTH": "https://docs.google.com/spreadsheets/d/1KBbasE9aUNXbVAVayP7CYUywFq6NTOx7/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "FOOT STRENGTH (LEFT) SITTING": "https://docs.google.com/spreadsheets/d/1ME_MBDS19ooctLXk84XcFLVTA9a7yzgV/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "FOOT STRENGTH (RIGHT) SITTING": "https://docs.google.com/spreadsheets/d/1rYvir-fnBtWEO43XlRHIEOe4XLt9x3X4/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "FOREARM HAND LENGTH": "https://docs.google.com/spreadsheets/d/1tUVgLJUJOCvAVAIpy4DgbeC_HsabeFsW/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "FUNCTIONAL LEG LENGTH": "https://docs.google.com/spreadsheets/d/10YXvEoPhTz1ivraWbLWOyaRcfixB8ZeW/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "GRIP DIAMETER (INSIDE)": "https://docs.google.com/spreadsheets/d/1e9-9dNs9CKEtgPM3jjL_EOij8hayrZQd/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "GRIP DIAMETER (OUTSIDE)": "https://docs.google.com/spreadsheets/d/1HpSIBCNae9QSkSyrmZlBfUM2LCTUsC0c/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "GRIP SPAN": "https://docs.google.com/spreadsheets/d/1Dk644kLozAgfFBlu8kImfXccUUOnhpQM/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "HAND BREADTH ACROSS THUMB": "https://docs.google.com/spreadsheets/d/1stwPcKnV9j9qafpMMubrVLE_kezHpQG7/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "HAND BREADTH": "https://docs.google.com/spreadsheets/d/17lOqEPEowc2QrlL0U_4aSrW_Q-AWDXvb/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "HAND GRIP STRENGTH (LEFT)": "https://docs.google.com/spreadsheets/d/1zxv8XAUNE3CnyCkSDyh08KwsYFEDKPlI/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "HAND GRIP STRENGTH (RIGHT)": "https://docs.google.com/spreadsheets/d/1_jK6PCjBLb3beQpW_olgw0OOxMP_VGVU/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "HAND GRIP TORQUE (PREFERRED HAND)": "https://docs.google.com/spreadsheets/d/1d164WKcj_COn28uXL61y-P0kboDCwUfd/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "HAND LENGTH": "https://docs.google.com/spreadsheets/d/1p2TEk3HP7I6CkkSuOyegNJA_faEs5Vb9/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "HAND THICKNESS AT METACARPAL III": "https://docs.google.com/spreadsheets/d/1HWI0nx2zsEqmw93cLnLKTvMC5e0fbREP/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "HEAD BREADTH": "https://docs.google.com/spreadsheets/d/11GCD8iy1b_Cqz3iTFfRZSVUK-yH7TIuR/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "HEAD LENGTH": "https://docs.google.com/spreadsheets/d/13Wpq6XiMBcCQe5sMsLysEfqSUN09zwz_/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "HEEL BREADTH": "https://docs.google.com/spreadsheets/d/1rupvOQvaTNiEjrQ-lmMmrrd4-c-4nj3k/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "HIP BREADTH SITTING": "https://docs.google.com/spreadsheets/d/1nXhooX5jp_soP_3A-mVfBbb1_6FVd4Ia/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "HIP BREADTH": "https://docs.google.com/spreadsheets/d/1GKWPQJ_TGEG774XjckC1zT47InA6HLCC/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "ILLIOCRYSTALE HEIGHT": "https://docs.google.com/spreadsheets/d/1syuzXhHtUrXF7dcofU57hi1FBxqtAIju/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "ILLIOSPINALE HEIGHT": "https://docs.google.com/spreadsheets/d/1_voPnkAsJ7J4enaCLUFn4SS-eSOI7C96/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "INDEX FINGER DIAMETER": "https://docs.google.com/spreadsheets/d/1tavZnu5toWAs1GJKHgffyOTinqs6eqwj/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "INSTEP LENGTH": "https://docs.google.com/spreadsheets/d/1jhe3NBLZhVmqANPJXnYMxJAmkaFk-G6_/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "INTERSCYE BREADTH": "https://docs.google.com/spreadsheets/d/12WTFnMQ7ug3Fp6B48WStlOYYq1WiNcIM/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "KNEE HEIGHT SITTING": "https://docs.google.com/spreadsheets/d/1WYvyj6ZrUtUJVq4RD1F5P5LLAPmOodEC/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "KNEE HEIGHT": "https://docs.google.com/spreadsheets/d/1o7Z97H-pTurevBPqZAk1SR4vvZYk11Q1pRDHt/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "KNEE-KNEE BREADTH": "https://docs.google.com/spreadsheets/d/1UgcjYNCDK7Le_B3GawFVvqRywCzZdUA_/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "LATERAL MALLEOLUS HEIGHT": "https://docs.google.com/spreadsheets/d/1fs5mcW3xcnwqUDchZy438RCjn4Ve2EOR/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "LEG STRENGTH (LEFT) SITTING": "https://docs.google.com/spreadsheets/d/1NWdNHpqD8_nTEgPzPvEoG1GfCsAsiR2f/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "LEG STRENGTH (RIGHT) SITTING": "https://docs.google.com/spreadsheets/d/17PHMGySBIj4YIicXUCpFSAL459FpxXVC/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "MAXIMUM GRIP LENGTH": "https://docs.google.com/spreadsheets/d/1GsHFJ7j71bmxRCXzunBEiN_u14nm3iBQ/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "MEDIAL MALLEOLUS HEIGHT": "https://docs.google.com/spreadsheets/d/1jW-oYFw_tWRp2gb3Zv2N9fGXgh2Uev8u/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "MENTON TO TOP OF HEAD": "https://docs.google.com/spreadsheets/d/1pBpyE5i3u04RN4FHjbJI-ugG1hGkacWq/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "METACARPAL III HEIGHT": "https://docs.google.com/spreadsheets/d/1yGAxe67gKBAt8T-ZDuGIrVAEiQQF7Sn_/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "MIDDLE FINGER PALM GRIP DIAMETER": "https://docs.google.com/spreadsheets/d/1kdeiwjTbneRVIuHhWnd8xu389JTEuh4r/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "OLECRANON HEIGHT": "https://docs.google.com/spreadsheets/d/1mY05v2l5wKMoBxkeouuoBiy5tRYRlhiU/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "PALM LENGTH": "https://docs.google.com/spreadsheets/d/12FMeE0eVwvT2TJpsh10SUFeFlDw25XBL/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "POPLITEAL HEIGHT SITTING": "https://docs.google.com/spreadsheets/d/15alEFCma1Rz7Fvf4UDKpOyDXp4ZXgjUB/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "PULL STRENGTH (BOTH HANDS) STANDING": "https://docs.google.com/spreadsheets/d/1yzu1JgyWgqR3QdEW6NM4J1Yxsav8YQig/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "PULL STRENGTH (LEFT HAND) SITTING": "https://docs.google.com/spreadsheets/d/1WcetlGrJgNAxeH_hZJ8W9v5lXsGxRuZc/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "PULL STRENGTH (RIGHT HAND) SITTING": "https://docs.google.com/spreadsheets/d/1lwdvNtHD5m58KuU2KcDCnK7Z94WBFfMQ/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "PUSH STRENGTH (BOTH HANDS) STANDING": "https://docs.google.com/spreadsheets/d/1KCtJ3IlMjqltSb2Rm9k4GSNRizOaaPk9/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "PUSH STRENGTH (LEFT HAND) SITTING": "https://docs.google.com/spreadsheets/d/1F2KJIdnGK0007bEWVVZ1-wAzPH0wbShL/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "PUSH STRENGTH (RIGHT HAND) SITTING": "https://docs.google.com/spreadsheets/d/1P3RCN1iHTIWueMNJJKZ7KIRxAAKo07WB/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "SCAPULA TO WAIST BACK LENGTH": "https://docs.google.com/spreadsheets/d/18DI-tmnQBnYhy2ybx2UtZ8RoAyDGb0ZS/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "SHOULDER GRIP LENGTH": "https://docs.google.com/spreadsheets/d/1UD_fFZ0AN2t-JbFz4ryN6TkLKibTXxr3/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "SITTING ACROMIAL HEIGHT": "https://docs.google.com/spreadsheets/d/1fGGfTkzpy2Z6QAf1mgF-me24b3xBSm-O/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "SITTING EYE HEIGHT": "https://docs.google.com/spreadsheets/d/1Ic73aJKo6y9wPq0YpL3TJZcO0CqWm7AR/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "SITTING HEIGHT": "https://docs.google.com/spreadsheets/d/1A8MRjH0LMZ8UxZdQ5Z-4WxPNnXRYCLS3/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "SPAN AKIMBO": "https://docs.google.com/spreadsheets/d/1EF9FR6tglrlGbedFBELBSK7LopyqyUMd/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "SPAN": "https://docs.google.com/spreadsheets/d/1IPBywbKlDkDyXKK84gPtMed_hA9iqeUm/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "STATURE": "https://docs.google.com/spreadsheets/d/1ZdTEWE9zZjnGUFOMoasKlYKa8kx5-3Rz/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "SUBSCAPULAR SKINFOLD THICKNESS": "https://docs.google.com/spreadsheets/d/1ykvz8VszFTe33_jXGegHPxxUqUSJOfUt/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "SUPRA ILIAC SKINFOLD THICKNESS": "https://docs.google.com/spreadsheets/d/1xLWHyrMer7IVD3bxjLvPoof151NoIcSH/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "THIGH CIRCUMFERENCE": "https://docs.google.com/spreadsheets/d/1yepVwwq7X94FoG0pSE4uwgfQq7Xzfze9/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "THIGH CLEARANCE HEIGHT SITTING": "https://docs.google.com/spreadsheets/d/1QukA-cDdaxx4onhRn9Lqt29pSsSYV4r0/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "THUMB TIP REACH": "https://docs.google.com/spreadsheets/d/1iG1uZ9mUc1-bpIZQh2a2IrKeV8YS8M4U/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "TORQUE STRENGTH (BOTH HANDS) SITTING": "https://docs.google.com/spreadsheets/d/1fBaH-gufJ7yzr4IzUEKuni4R-AKwezwG/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "TORQUE STRENGTH (BOTH HANDS) STANDING": "https://docs.google.com/spreadsheets/d/1YhK55dnPPwCcNvmrLjJQ4QzQJod4CsaT/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "TORQUE STRENGTH (PREFERRED HAND) STANDING": "https://docs.google.com/spreadsheets/d/1uto2Bt0ZgAFN-LN8s6TAIDvfS-h1gU_u/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "TRICEP SKINFOLD THICKNESS": "https://docs.google.com/spreadsheets/d/1ZtWfEZevErCcXGlqP9ZuVkI_cGAuc6cp/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "TROCHANTERIC HEIGHT": "https://docs.google.com/spreadsheets/d/1YWMWyuA1VaDgRPqWw7pqB7tmAWKSGpwp/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "VERTICAL GRIP REACH SITTING": "https://docs.google.com/spreadsheets/d/1l3CVjKGP2LU-LEBW44E_yiBif6tDBHVv/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "VERTICAL GRIP REACH": "https://docs.google.com/spreadsheets/d/1inEndCiYAuK4GdZLTuv_78Us-bGDDedR/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "VERTICAL REACH": "https://docs.google.com/spreadsheets/d/1p1T4wCsY8j6xvyQOdkRD8xAain8Ekdbv/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "WAIST BACK LENGTH": "https://docs.google.com/spreadsheets/d/1gdz-aQOl3Px_9fYg0lOwVCwiqQXCKnYG/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "WAIST BREADTH": "https://docs.google.com/spreadsheets/d/1uJywR9MzhLY_FkUzvCTkkUlwUTRm8BUY/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "WAIST CIRCUMFERENCE": "https://docs.google.com/spreadsheets/d/1zK53JoX0qivrwuMUoRmoy-h-H4xDIcke/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "WALL TO ACROMION DISTANCE": "https://docs.google.com/spreadsheets/d/13mWsIp3FJxtBKSsMoHOmMXKycCynJuHg/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "WALL TO LUMBOSACRAL DISTANCE": "https://docs.google.com/spreadsheets/d/18rZ_hdL5SCZBgzDBRES_FqyV4HXJ1zvU/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "WEIGHT": "https://docs.google.com/spreadsheets/d/1wRLiivIBFsaf_x7I94SUdsgqgsSXlKRk/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true",
    "WRIST CIRCUMFERENCE": "https://docs.google.com/spreadsheets/d/1j9z3MLFwPh0kJUNxCvZbQRP27y-CNAFg/edit?usp=drive_link&ouid=115534766381035648538&rtpof=true&sd=true"
}




application_data = {
    "WEIGHT": [
        "General body description",
        "comparison of different populations",
        "calculation of BMI",
        "estimation of strength values",
        "estimation of safe load to be carried",
        "calculation of lean body mass"
    ],

    "STATURE": [
        "General body description",
        "comparison of different populations",
        "estimation of other linear parameters",
        "vertical clearance from ground",
        "supine clearance in lying posture",
        "workplace design"
    ],

    "VERTICLE REACH": [
        "Workplace layout",
        "design of controls"
    ],

    "VERTICLE GRIP REACH": [
        "Workplace layout",
        "design of controls"
    ],

    "EYE HEIGHT": [
        "Design of controls and displays",
        "workplace layout design"
    ],

    "ACROMIAL HEIGHT": [
        "General body description",
        "workplace layout",
        "body linkages",
        "for deciding feeding chute height",
        "for lifting studies",
        "for use in force application studies"
    ],

    "ELBOW HEIGHT": [
        "General body description",
        "workplace layout",
        "body linkages"
    ],

    "OLECRANON HEIGHT": [
        "Workplace layout",
        "body linkages",
        "platform height for work to be done in standing posture like in workshop",
        "kitchen"
    ],

    "ILLIOCRYSTALE HEIGHT": [
        "Body linkages",
        "safety harness design",
        "safety belt design",
        "material handling height recommendation"
    ],

    "ILLIOSPINALE HEIGHT": [
        "Body linkages",
        "safety harness design",
        "safety belt design"
    ],

    "TROCHANTERIC HEIGHT": [
        "Body linkages",
        "biomechanics study",
        "setting limit for leg lifting in sagittal plane"
    ],

    "METACARPAL III HEIGHT": [
        "Control panel design",
        "handle height of manual as well as animal drawn equipment",
        "handle height of manually operated rotary equipment"
    ],

    "KNEE HEIGHT": [
        "Body linkages",
        "workplace design",
        "step height in tractors",
        "height of platform for thresher design"
    ],

    "MEDIAL MALLEOLUS HEIGHT": [
        "Safety shoe design",
        "foot control design",
        "foot rest design",
        "biomechanics study"
    ],

    "LATERAL MALLEOLUS HEIGHT": [
        "Safety shoe design",
        "foot control design",
        "foot rest design"
    ],

    "MENTON TO TOP OF HEAD": [
        "Safety head gear design (helmet)",
        "protection head cover for face during spraying operation and for protection against honey bees"
    ],

    "WAIST BACK LENGTH": [
        "Knapsack",
        "rucksack and haversack equipment design"
    ],

    "SCAPULA TO WAIST BACK LENGTH": [
        "Knapsack sprayer design",
        "harness strap design (length of belt in knapsack sprayer)",
        "carrying basket in tea gardens"
    ],

    "SPAN": [
        "Workplace design",
        "design of controls",
        "for material handling packages"
    ],

    "SPAN AKIMBO": [
        "Workplace design",
        "design of controls",
        "for material handling packages"
    ],

    "ARM REACH FROM THE WALL": [
        "Body linkages",
        "design of control and display panel",
        "workplace layout",
        "clearance in work cabin"
    ],

    "THUMB TIP REACH": [
        "Control panel design",
        "workplace layout"
    ],

    "SHOULDER GRIP LENGTH": [
        "Body linkages",
        "control panel design",
        "workplace layout",
        "reach envelope",
        "biomechanics study"
    ],

    "WALL TO ACROMION DISTANCE": [
        "Body linkages",
        "reach envelope",
        "knapsack design",
        "biomechanics study"
    ],

    "WALL TO LUMBOSACRAL DISTANCE": [
        "Biomechanics study",
        "seat design",
        "workplace design"
    ],

    "ABDOMINAL EXTENSION TO WALL": [
        "Access design of control panel",
        "biomechanics study",
        "personal protective clothing design"
    ],

    "CHEST DEPTH": [
        "General body description",
        "personal protective clothing design"
    ],

    "BIACROMIAL BREADTH": [
        "General body description",
        "workplace layout",
        "handle design",
        "body linkages"
    ],

    "BIDELTOID BREADTH": [
        "General body description",
        "workplace layout",
        "door width",
        "handle design",
        "body linkages",
        "access opening"
    ],

    "CHEST BREADTH": [
        "General body description",
        "workplace layout",
        "handle design",
        "deciding width of front mounted equipment"
    ],

    "INTERSCYE BREADTH": [
        "Body linkages",
        "crutch design",
        "knapsack design",
        "deciding width of knapsack equipment"
    ],

    "WAIST BREADTH": [
        "Seat design",
        "workplace layout",
        "personal protective clothing design"
    ],

    "HIP BREADTH": [
        "General body description",
        "seat design",
        "workplace layout"
    ],

    "HEEL BREADTH": [
        "Footrest design",
        "safety shoe design",
        "pedal design",
        "workplace layout"
    ],

    "BIMALLELOLAR BREADTH": [
        "Safety shoe design",
        "foot rest design"
    ],

    "CHEST CIRCUMFERENCE": [
        "General body description",
        "health index",
        "comparison of different populations",
        "personal protective clothing design"
    ],

    "WAIST CIRCUMFERENCE": [
        "Personal protective clothing design",
        "seat design",
        "waist harness design for backpack"
    ],

    "THIGH CIRCUMFERENCE": [
        "General body description",
        "personal protective clothing design"
    ],

    "CALF CIRCUMFERENCE": [
        "General body description",
        "personal protective clothing design",
        "gumboot/safety shoe design"
    ],

    "WRIST CIRCUMFERENCE": [
        "Biomechanics",
        "gloves design",
        "wrist band design"
    ],

    "GRIP DIAMETER (INSIDE)": [
        "Handle design",
        "control grip design",
        "hand tool design"
    ],

    "GRIP DIAMETER (OUTSIDE)": [
        "Handle design",
        "control grip design",
        "clearance for maintenance purpose"
    ],

    "MIDDLE FINGER PALM GRIP DIAMETER": [
        "Handle design",
        "control grip design",
        "hand tool design"
    ],

    "VERTICAL GRIP REACH SITTING": [
        "Control panel design",
        "workplace layout"
    ],

    "SITTING HEIGHT": [
        "General body description",
        "comparison of different populations",
        "control panel layout",
        "workplace layout"
    ],

    "SITTING EYE HEIGHT": [
        "Display",
        "seat and control panel design",
        "optimum visual field determination in tractors and self-propelled machines"
    ],

    "SITTING ACROMIAL HEIGHT": [
        "Body linkages",
        "control panel layout",
        "workplace layout",
        "hand reach envelopes",
        "seat design"
    ],

    "ELBOW REST HEIGHT": [
        "Seat handle design",
        "control design",
        "control panel design",
        "workspace layout"
    ],

    "THIGH CLEARANCE HEIGHT SITTING": [
        "General body description",
        "workplace layout",
        "seat design",
        "clearance between seat and steering wheel",
        "sitting surface and inner table height"
    ],

    "KNEE HEIGHT SITTING": [
        "General body description",
        "workplace layout",
        "seat design",
        "vertical clearance from floor to underside of work surface"
    ],

    "POPLITEAL HEIGHT SITTING": [
        "General body description",
        "seat design",
        "design of chairs and stools",
        "height of seating surface",
        "workplace layout"
    ],

    "HAND THICKNESS AT METACARPAL III": [
        "Handle design",
        "control panel design",
        "hand tool design",
        "safety guard design",
        "maintenance space design",
        "safety gloves design"
    ],

    "FIRST PHALANX DIGIT III LENGTH": [
        "Handle design",
        "control panel design",
        "hand tool design",
        "maintenance space design",
        "space requirement for control knobs"
    ],

    "GRIP SPAN": [
        "Design of hand tools",
        "design of sprayer lid diameter",
        "design of horticultural tools like secateurs and scissors"
    ],

    "MAXIMUM GRIP LENGTH": [
        "Handle design",
        "control grip design",
        "lid design of sprayer containers",
        "control panel design"
    ],

    "INDEX FINGER DIAMETER": [
        "Design of controls",
        "push button design"
    ],

    "HEAD LENGTH": [
        "Safety head gear design",
        "cap design"
    ],

    "HEAD BREADTH": [
        "Safety head gear design",
        "cap design"
    ],

    "CORONOID FOSSA TO HAND LENGTH": [
        "Control panel design",
        "thresher feeding chute design",
        "chaff cutter feeding chute design"
    ],

    "FOREARM HAND LENGTH": [
        "Control panel design",
        "biomechanics study",
        "handle design",
        "feeding chutes of threshers and chaff cutters"
    ],

    "ELBOW GRIP LENGTH": [
        "Body linkages",
        "control panel design",
        "workplace layout",
        "biomechanics study"
    ],

    "HAND LENGTH": [
        "Handle design",
        "control panel design",
        "hand tool design",
        "safety gloves design"
    ],

    "PALM LENGTH": [
        "Handle design",
        "hand tool design",
        "design of push controls",
        "biomechanics study"
    ],

    "HAND BREADTH ACROSS THUMB": [
        "Handle design",
        "control panel design",
        "hand tool design",
        "safety gloves design",
        "hand grip design",
        "knapsack sprayer trigger design"
    ],

    "HAND BREADTH": [
        "Handle design",
        "control panel design",
        "hand tool design",
        "hand grip design",
        "knapsack sprayer trigger design"
    ],

    "BUTTOCK KNEE LENGTH": [
        "Body linkages",
        "seat design",
        "workplace layout",
        "horizontal clearance between seat and work surface",
        "biomechanics study"
    ],

    "BUTTOCK POPLITEAL LENGTH": [
        "Body linkages",
        "seat depth design",
        "workplace layout",
        "biomechanics study"
    ],

    "ABDOMINAL DEPTH SITTING": [
        "Seat design",
        "workplace layout",
        "clearance space for steering/other controls/work surfaces"
    ],

    "HIP BREADTH SITTING": [
        "General body description",
        "seat width design",
        "workplace layout"
    ],

    "ELBOW-ELBOW BREADTH SITTING": [
        "Body linkages",
        "seat arm rest design",
        "seat design",
        "clearance in workplace",
        "handle width in manually operated equipment"
    ],

    "KNEE-KNEE BREADTH": [
        "Comparison of different populations",
        "workplace design",
        "general body description"
    ],

    "FOOT LENGTH": [
        "General body description",
        "comparison of different populations",
        "body linkages",
        "foot control design",
        "pedal design",
        "workplace layout",
        "safety shoe design"
    ],

    "INSTEP LENGTH": [
        "Safety shoe design",
        "foot rest design",
        "foot control design especially brake",
        "clutch and accelerator pedals"
    ],

    "FOOT BREADTH (BALL OF THE FOOT)": [
        "Width of foot controls",
        "pedal design like brake",
        "clutch and accelerator pedals",
        "workplace layout"
    ],

    "FUNCTIONAL LEG LENGTH": [
        "Comparison of population",
        "foot pedal design",
        "leg control design",
        "biomechanics study"
    ],

    "BICEP SKINFOLD THICKNESS": [
        "Comparison of populations",
        "determination of lean body mass",
        "estimation of body fat"
    ],

    "TRICEP SKINFOLD THICKNESS": [
        "Comparison of populations",
        "determination of lean body mass",
        "estimation of body fat"
    ],

    "SUBSCAPULAR SKINFOLD THICKNESS": [
        "Comparison of populations",
        "determination of lean body mass",
        "estimation of body fat"
    ],

    "SUPRA ILIAC SKINFOLD THICKNESS": [
        "Comparison of populations",
        "determination of lean body mass",
        "estimation of body fat"
    ],

    "HAND GRIP STRENGTH (RIGHT)": [
        "Design of hand control lever",
        "hand clutch",
        "hand brake",
        "sprayer trigger"
    ],

    "HAND GRIP STRENGTH (LEFT)": [
        "Design of hand control lever",
        "hand clutch",
        "hand brake",
        "sprayer trigger"
    ],

    "PUSH STRENGTH (BOTH HANDS) STANDING": [
        "Design of manually operated equipment like wheel hoe, cono weeder, lawn mower, manual harvester",
        "hanging type cleaner",
        "push carts",
        "material handling equipment"
    ],

    "PULL STRENGTH (BOTH HANDS) STANDING": [
        "Design of manually operated equipment like wheel hoe, lawn mower, hand ridger, long handled hoes",
        "rice transplanter",
        "rice drum seeder",
        "seed drill",
        "material handling equipment"
    ],

    "PUSH STRENGTH (LEFT HAND) SITTING": [
        "Design of gear shift lever",
        "handle lever",
        "PTO lever",
        "high-low speed lever",
        "various push type controls in control panel"
    ],

    "PULL STRENGTH (LEFT HAND) SITTING": [
        "Design of gear shift lever",
        "handle lever",
        "parking brake",
        "various pull type controls in control panel"
    ],

    "PUSH STRENGTH (RIGHT HAND) SITTING": [
        "Design of gear shift lever",
        "handle lever",
        "position control and draft control levers on tractor",
        "various push type controls in control panel"
    ],

    "PULL STRENGTH (RIGHT HAND) SITTING": [
        "Design of gear shift lever",
        "handle lever",
        "various pull type controls in control panel"
    ],

    "LEG STRENGTH (RIGHT) SITTING": [
        "Design of leg-operated controls like brake pedal",
        "differential lock",
        "other pedal operated machines as sewing machine",
        "pedal operated thresher",
        "pedal operated cleaner grader"
    ],

    "FOOT STRENGTH (RIGHT) SITTING": [
        "Design of accelerator pedal and other foot operated controls"
    ],

    "LEG STRENGTH (LEFT) SITTING": [
        "Design of leg-operated controls like clutch pedal",
        "pedal operated thresher",
        "other pedal operated machines as sewing machine",
        "pedal operated cleaner grader"
    ],

    "FOOT STRENGTH (LEFT) SITTING": [
        "Design of accelerator pedal and other foot operated controls"
    ],

    "TORQUE STRENGTH (PREFERRED HAND) STANDING": [
        "Design of manually operated equipment like chaff cutter",
        "sugarcane crusher",
        "rotary maize sheller",
        "hand winnower and other equipment operated by hand in rotary mode"
    ],

    "TORQUE STRENGTH (BOTH HANDS) STANDING": [
        "Design of manually operated equipment like chaff cutter",
        "sugarcane crusher",
        "rotary maize sheller",
        "hand winnower and other equipment operated by hand in rotary mode"
    ],

    "TORQUE STRENGTH (BOTH HANDS) SITTING": [
        "Design of wheel type controls like steering wheel"
    ],

    "HAND GRIP TORQUE (PREFERRED HAND)": [
        "Design of knob controls",
        "sprayer and fuel tank lids",
        "opening cover of service point"
    ]
}

definition_data = {
    "WEIGHT": "Body weight as measured on a calibrated weighing scale",

    "STATURE": "The vertical distance from the standing surface to the vertex of the head when the subject stands erect and looks straight forward",

    "VERTICLE REACH": "The vertical distance from the standing surface to the height of the middle finger when arm, hand and fingers are extended vertically.",

    "VERTICLE GRIP REACH": "The vertical distance from the Standing surface to the height of the pointer held horizontal to the subjects’ fist when the arm is maximally extended upward. The subject stands erect and looks straight forward",

    "EYE HEIGHT": "The vertical distance from the standing surface to the external canthus of the eye when the subject stands erect and looks straight forward",

    "ACROMIAL HEIGHT": "The vertical distance from the standing surface to the acromion. The subject stands erect and looks straight forward",

    "ELBOW HEIGHT": "The vertical distance from the standing surface to the top of the radiale when the subject stands erect and looks straight forward",

    "OLECRANON HEIGHT": "The vertical distance from the Standing surface to the height of the undersurface of the elbow. Measured with the arm flexed 90 degrees and the upper arm vertical. The subject stands erect and looks straight forward.",

    "ILLIOCRYSTALE HEIGHT": "The vertical distance from the standing surface to the top of the ilium in the mid-axillary plane. The subject stands erect and looks straight forward. This is also known as waist height.",

    "ILLIOSPINALE HEIGHT": "The vertical distance from the standing surface to the height of the illiospinale. The subject stands erect and looks straight forward.",

    "TROCHANTERIC HEIGHT": "The vertical distance from the standing surface to the height of the trochanterion. The subject stands erect and looks straight forward.",

    "METACARPAL III HEIGHT": "The vertical distance from the standing surface to the height of the knuckle where the middle finger joins the palm. The subject stands erect and looks straight forward.",

    "KNEE HEIGHT": "The vertical distance from the standing surface to the midpoint of the kneecap. The subject stands erect and looks straight forward.",

    "MEDIAL MALLEOLUS HEIGHT": "The height of the most medially projecting point of the medial ankle bone from the ground surface.",

    "LATERAL MALLEOLUS HEIGHT": "The height of the most lateral projecting point of the lateral ankle bone from the ground surface.",

    "MENTON TO TOP OF HEAD": "The distance from the lower edge of the tip of the chin to the level of the vertex of the head.",

    "WAIST BACK LENGTH": "The vertical distance along the spine from the waist level to the cervical (the tip of the seventh cervical vertebra). The subject stands erect and looks straight forward.",

    "SCAPULA TO WAIST BACK LENGTH": "The surface distance from the superior angle of the scapula to the back at the waist level. The tape starts from the middle of the superior angle of the scapula, passes through the armpit, and ends at the back at the waist level on the same vertical axis.",

    "SPAN": "The distance between the tips of the right and left middle fingers when the subject's arms are maximally extended laterally.",

    "SPAN AKIMBO": "The distance between the elbow points measured with the arms flexed and held horizontally, palms down, fingers straight and together, and palms and thumbs touching the chest at the nipple level.",

    "ARM REACH FROM THE WALL": "The distance from the wall to the tip of the middle finger measured with the subject's shoulder against the wall, hand, and arm extended forward.",

    "THUMB TIP REACH": "The distance from the wall to the tip of the thumb measured with the shoulder against the wall, arm extended forward, and index finger touching the tip of the thumb.",

    "SHOULDER GRIP LENGTH": "The horizontal distance from a pointer held in the subject's fist to a wall against which they stand, measured with the arms extended horizontally.",

    "WALL TO ACROMION DISTANCE": "The horizontal perpendicular distance from the wall to the acromion measured when the subject stands erect against a wall.",

    "WALL TO LUMBOSACRAL DISTANCE": "The transverse distance from the wall to the posterior superior iliac spine. The subject stands erect against the wall and looks straight forward.",

    "ABDOMINAL EXTENSION TO WALL": "The vertical distance from the most laterally protruding point of the abdomen to a wall against which the subject stands erect with minimal wall-buttock contact and looking straight forward.",

    "CHEST DEPTH": "The maximum depth of the torso measured at the nipple level. The subject stands erect and looks straight forward.",

    "BIACROMIAL BREADTH": "The transverse distance across the shoulder from right to left acromion. The subject stands erect and looks straight forward.",

    "BIDELTOID BREADTH": "The horizontal distance across the maximum lateral protrusion of the right and left deltoid muscles. The subject stands erect and looks straight forward.",

    "CHEST BREADTH": "The breadth of the torso measured at the nipple level. The subject stands erect and looks straight forward.",

    "INTERSCYE BREADTH": "The distance across the back between the posterior axillary folds at the lower level of the armpit.",

    "WAIST BREADTH": "The breadth of the torso at the waist level. The subject stands erect and looks straight forward.",

    "HIP BREADTH": "The maximum breadth of the lower torso. The subject stands erect and looks straight forward.",

    "HEEL BREADTH": "The maximum breadth of the heel as measured below the projection of the ankle bones.",

    "BIMALLELOLAR BREADTH": "The distance across the protrusion of the medial and lateral malleolus bone.",

    "CHEST CIRCUMFERENCE": "The circumference of the torso measured at the nipple level. The subject stands erect and looks straight forward.",

    "WAIST CIRCUMFERENCE": "The circumference of the torso at the waist level. The subject stands erect and looks straight forward.",

    "THIGH CIRCUMFERENCE": "The circumference of the upper leg measured as high in the crotch as possible.",

    "CALF CIRCUMFERENCE": "The maximum circumference of the gastrocnemius muscle in the lower leg. The subject stands erect and looks straight forward.",

    "WRIST CIRCUMFERENCE": "The circumference of the wrist at the level of the tip of the styloid process of the radius.",

    "GRIP DIAMETER (INSIDE)": "The diameter of the widest level of a cone which the subject can grasp with his thumb and middle finger touching each other.",

    "GRIP DIAMETER (OUTSIDE)": "The distance between the joint of the 1st and 2nd phalanges of the thumb and knuckles of the middle finger measured with the hand to the grip of a cone.",

    "MIDDLE FINGER PALM GRIP DIAMETER": "The diameter of the widest level of the cylinder which the subject can grasp with his palm and middle finger touching each other.",

    "VERTICAL GRIP REACH SITTING": "The height above the sitting surface of a pointer held horizontal in the subject's fist when the arm is maximally extended upward.",

    "SITTING HEIGHT": "The height from the sitting surface to the vertex of the head. The subject sits erect and looks straight forward.",

    "SITTING EYE HEIGHT": "The height from the sitting surface to the external canthus. The subject sits erect and looks straight forward.",

    "SITTING ACROMIAL HEIGHT": "The height from the sitting surface to the top of the acromion. The subject sits erect and looks straight forward.",

    "ELBOW REST HEIGHT": "The height of the bottom of the tip of the elbow above the sitting surface.",

    "THIGH CLEARANCE HEIGHT SITTING": "The height of the highest point of the thigh above the sitting surface. The subject sits erect and looks straight forward.",

    "KNEE HEIGHT SITTING": "The height from the footrest surface of the musculature just above the knee. The subject sits erect and looks straight forward.",

    "POPLITEAL HEIGHT SITTING": "The height of the underside of the upper leg above the footrest surface. The subject sits erect and looks straight forward.",

    "HAND THICKNESS AT METACARPAL III": "The thickness of the metacarpal phalangeal joint of the middle finger.",

    "FIRST PHALANX DIGIT III LENGTH": "The length of the first segment of the middle finger measured across the surfaces of the third metacarpal and second phalanx while the hand is held in a fist.",

    "GRIP SPAN": "The maximum distance between the palm and the tip of the middle finger when fingers are in grip position.",

    "MAXIMUM GRIP LENGTH": "The maximum length between the tip of the index finger and the tip of the thumb while the palm, thumb, and fingers are in grip position.",

    "INDEX FINGER DIAMETER": "The diameter of the index finger of the right hand measured at the joint of the 1st and 2nd phalanges of the index finger.",

    "HEAD LENGTH": "The maximum length of the head as measured from glabella to the back of the head.",

    "HEAD BREADTH": "The maximum breadth of the head.",

    "CORONOID FOSSA TO HAND LENGTH": "The distance from the tip of the middle finger to the coronoid fossa with the arms bent at 90 degrees with the upper arm.",

    "FOREARM HAND LENGTH": "The distance from the tip of the elbow to the top of the middle finger measured along the long axis of the arm.",

    "ELBOW GRIP LENGTH": "The distance from the tip of the bent elbow to the corner of the clenched fist.",

    "HAND LENGTH": "The distance from the base of the hand to the top of the middle finger measured along the long axis of the hand.",

    "PALM LENGTH": "The distance from the base of the hand to the furrow where the middle finger folds upon the palm.",

    "HAND BREADTH ACROSS THUMB": "The breadth of the hand as measured at the level of the distal end of the 1st metacarpal of the thumb.",

    "HAND BREADTH": "The breadth of the hand as measured across the distal ends of the metacarpal bones.",

    "BUTTOCK KNEE LENGTH": "The horizontal distance from the rear-most surface of the buttock to the front of the kneecap.",

    "BUTTOCK POPLITEAL LENGTH": "The horizontal distance from the rear-most surface of the buttock to the back of the lower leg.",

    "ABDOMINAL DEPTH SITTING": "The distance from the rear-most surface of the waist to the front of the umbilicus.",

    "HIP BREADTH SITTING": "The breadth of the body as measured across the widest portion of the hips. The subject sits erect looking straight forward.",

    "ELBOW-ELBOW BREADTH SITTING": "The distance across the lateral surfaces of the elbows flexed at 90 degrees with the upper arm and resting lightly against the body.",

    "KNEE-KNEE BREADTH": "The maximum horizontal distance across the lateral surfaces of the knees measured with knees gently touching.",

    "FOOT LENGTH": "The length of the foot measured parallel to its long axis.",

    "INSTEP LENGTH": "The distance from the plane of the heel to the point of maximum medial protuberance of the foot.",

    "FOOT BREADTH (BALL OF THE FOOT)": "The maximum breadth of the foot as measured at right angles to its long axis.",

    "FUNCTIONAL LEG LENGTH": "The distance from the back at the waist level to the heel measured along the long axis of the leg with the subject sitting erect on the edge of a chair, leg extended forward with the knee straightened.",

    "BICEP SKINFOLD THICKNESS": "The thickness of the skin fold picked up parallel to the arm on the bicep between the acromion and the elbow.",

    "TRICEP SKINFOLD THICKNESS": "The thickness of the skin fold on the back of the arm halfway between the acromion and the tip of the elbow picked up parallel to the long axis of the upper arm.",

    "SUBSCAPULAR SKINFOLD THICKNESS": "The thickness of the skin fold picked up just the inferior angle of the right scapula and parallel to the tension lines of the skin.",

    "SUPRA ILIAC SKINFOLD THICKNESS": "The thickness of the skin fold picked up in the mid-axillary line at the level of the crest of the ilium.",

    "HAND GRIP STRENGTH (RIGHT)": "The grip strength of the right hand measured with a handgrip dynamometer when the subject stands erect with arms hanging downwards.",

    "HAND GRIP STRENGTH (LEFT)": "The grip strength of the left hand measured with a handgrip dynamometer when the subject stands erect with arms hanging downwards.",

    "PUSH STRENGTH (BOTH HANDS) STANDING": "The maximum push force applied with both hands on load cell in standing posture on the strength measurement setup with left leg forward, bent at the knee, and right leg backward, straight.",

    "PULL STRENGTH (BOTH HANDS) STANDING": "The maximum pull force applied with both hands on load cell in standing posture on the strength measurement setup with left leg forward, straight, and right leg backward bent at the knee.",

    "PUSH STRENGTH (LEFT HAND) SITTING": "Design of gear shift lever, handle lever, PTO lever, high-low speed lever, various push type controls in control panel.",

    "PULL STRENGTH (LEFT HAND) SITTING": "Design of gear shift lever, handle lever, parking brake, various pull type controls in control panel.",

    "PUSH STRENGTH (RIGHT HAND) SITTING": "The maximum push force applied with right hand on load cell in sitting posture on the strength measurement setup in horizontal plane at seat height.",

    "PULL STRENGTH (RIGHT HAND) SITTING": "The maximum pull force applied with right hand on load cell in sitting posture on the strength measurement setup in horizontal plane at seat height.",

    "LEG STRENGTH (RIGHT) SITTING": "The maximum force applied by the right leg on load cell in erect sitting posture on the strength measurement setup with knee flexed at an angle between 90 - 110 degrees. The horizontal distance of the pedal being 45% of stature from SRP and vertical distance being 19% of stature from SRP.",

    "FOOT STRENGTH (RIGHT) SITTING": "The maximum force applied by the right foot on load cell, keeping the heel on the ground as fulcrum, in erect sitting posture on the strength measurement setup with knee flexed at an angle between 90 -110 degrees.",

    "LEG STRENGTH (LEFT) SITTING": "The maximum force applied by the left leg on load cell in erect sitting posture on the strength measurement setup with knee flexed at an angle between 90 - 110 degrees. The horizontal distance of the pedal being 45% of stature from SRP and vertical distance being 19% of stature from SRP.",

    "FOOT STRENGTH (LEFT) SITTING": "The maximum force applied by the left foot on load cell, keeping the heel on the ground as fulcrum, in erect sitting posture on the strength measurement setup with knee flexed at an angle between 90 - 110 degrees.",

    "TORQUE STRENGTH (PREFERRED HAND) STANDING": "The maximum torque applied by the preferred hand in vertical plane on the crank of the strength measurement setup in standing posture, looking straight with right leg forward, bent at the knee, and left leg backward, straight, for right-handed subjects. Position of the legs vice-versa in the case of left-handed subjects.",

    "TORQUE STRENGTH (BOTH HANDS) STANDING": "The maximum torque applied by both hands in vertical plane on the crank of the strength measurement setup in standing posture, looking straight with left leg forward, bent at the knee, and right leg backward, straight.",

    "TORQUE STRENGTH (BOTH HANDS) SITTING": "The maximum torque applied by both hands in a clockwise direction on the steering wheel with load cell attached tangentially to the steering wheel in erect sitting posture on the strength measurement setup.",

    "HAND GRIP TORQUE (PREFERRED HAND)": "The maximum grip torque applied by preferred hand in an anticlockwise direction on the center grip of the steering wheel with load cell attached tangentially to the steering wheel in erect sitting posture."
}


design_guide_data = {
    "WEIGHT": "For calculation of safe load carrying limit 5th percentile value of the user population is to be considered. For checking the strength of seat 95th percentile value of user population is to be considered",

    "STATURE": "For clearance purpose, 95th percentile value of user population is to be considered",

    "VERTICLE REACH": "For calculation of reach, 5th percentile value of user population is to be considered.",

    "VERTICLE GRIP REACH": "For calculation of reach, 5th percentile value of user population is to be considered.",

    "EYE HEIGHT": "For visibility purpose, 5th percentile value of user population is to be considered.",

    "ACROMIAL HEIGHT": "For design purpose, 5th percentile value of user population is to be considered.",

    "ELBOW HEIGHT": "For design purpose, 5th percentile value of user population is to be considered.",

    "OLECRANON HEIGHT": "For design purpose, 5th percentile value of user population is to be considered.",

    "ILLIOCRYSTALE HEIGHT": "For design purpose, 5th percentile value of user population is to be considered.",

    "ILLIOSPINALE HEIGHT": "Depending upon the design requirement, the percentile value of user population may be selected.",

    "TROCHANTERIC HEIGHT": "Depending upon the design requirement, the percentile value of user population may be selected.",

    "METACARPAL III HEIGHT": "Generally for design purpose, 5th percentile value of user population is to be considered.",

    "KNEE HEIGHT": "Generally for design purpose, 5th percentile value of user population is to be considered.",

    "MEDIAL MALLEOLUS HEIGHT": "Depending upon the design requirement, the percentile value of user population may be selected.",

    "LATERAL MALLEOLUS HEIGHT": "Depending upon the design requirement, the percentile value of user population may be selected.",

    "MENTON TO TOP OF HEAD": "Generally for design purpose, 95th percentile value of user population is to be considered.",

    "WAIST BACK LENGTH": "For design purpose, 5th percentile value of user population is to be considered.",

    "SCAPULA TO WAIST BACK LENGTH": "For design purpose, 5th percentile value of user population is to be considered.",

    "SPAN": "For reach purpose, 5th percentile value of user population is to be considered.",

    "SPAN AKIMBO": "For reach purpose, 5th percentile value of user population is to be considered.",

    "ARM REACH FROM THE WALL": "For reach purpose, 5th percentile value of user population is to be considered. For clearance purpose, 95th percentile value of user population is to be considered.",

    "THUMB TIP REACH": "For design purpose, 5th percentile value of user population is to be considered.",

    "SHOULDER GRIP LENGTH": "For reach purpose, 5th percentile value of user population is to be considered. For clearance purpose, 95th percentile value of user population is to be considered.",

    "WALL TO ACROMION DISTANCE": "Depending upon the design requirement, the percentile value of user population may be selected.",

    "WALL TO LUMBOSACRAL DISTANCE": "Depending upon the design requirement, the percentile value of user population may be selected.",

    "ABDOMINAL EXTENSION TO WALL": "For design purpose, 95th percentile value of user population is to be considered.",

    "CHEST DEPTH": "For design purpose, 95th percentile value of user population is to be considered.",

    "BIACROMIAL BREADTH": "Depending upon the design requirement, the percentile value of user population may be selected.",

    "BIDELTOID BREADTH": "For design purpose, 95th percentile value of user population is to be considered.",

    "CHEST BREADTH": "Generally for design purpose, 5th percentile value of user population is to be considered.",

    "INTERSCYE BREADTH": "Generally for design purpose, 5th percentile value of user population is to be considered.",

    "WAIST BREADTH": "Depending upon the design requirement, the percentile value of user population may be selected.",

    "HIP BREADTH": "Generally for design purpose, 95th percentile value of user population is to be considered.",

    "HEEL BREADTH": "Generally for design purpose, 95th percentile value of user population is to be considered.",

    "BIMALLELOLAR BREADTH": "Generally for design purpose, 95th percentile value of user population is to be considered.",

    "CHEST CIRCUMFERENCE": "Depending upon the design requirement, the percentile value of user population may be selected. Generally for safety cloth design purpose, 95th percentile value of user population is to be considered.",

    "WAIST CIRCUMFERENCE": "Generally for safety cloth design purpose, 95th percentile value of user population is to be considered and adjustment for reducing the size may be provided.",

    "THIGH CIRCUMFERENCE": "Generally for safety cloth design purpose, 95th percentile value of user population is to be considered. However, for specific cloth design requirement, appropriate percentile value of the user population may be used.",

    "CALF CIRCUMFERENCE": "Generally for design purpose, 95th percentile value of user population is to be considered.",

    "WRIST CIRCUMFERENCE": "Generally for design purpose, 95th percentile value of user population is to be considered and adjustment for reducing the size may be provided.",

    "GRIP DIAMETER (INSIDE)": "Generally for design purpose, 5th percentile value of user population is to be considered.",

    "GRIP DIAMETER (OUTSIDE)": "Generally for design purpose, 95th percentile value of user population is to be considered.",

    "MIDDLE FINGER PALM GRIP DIAMETER": "Generally for design purpose, 95th percentile value of user population is to be considered.",

    "VERTICAL GRIP REACH SITTING": "Generally for deciding control locations, 5th percentile value of user population is to be considered. For clearance purpose, 95th percentile value of user population is to be considered.",

    "SITTING HEIGHT": "For clearance purpose, 95th percentile value of user population is to be considered.",

    "SITTING EYE HEIGHT": "Generally for design purpose, 5th percentile value of user population is to be considered.",

    "SITTING ACROMIAL HEIGHT": "Both 5th and 95th percentile values of the user population are used for development of hand reach envelope. For design purpose where reach is concerned, 5th percentile value of user population is to be considered.",

    "ELBOW REST HEIGHT": "Generally for design purpose, 5th percentile value of user population is to be considered.",

    "THIGH CLEARANCE HEIGHT SITTING": "Generally for design purpose, 95th percentile value of user population is to be considered.",

    "KNEE HEIGHT SITTING": "Generally for design purpose, 95th percentile value of user population is to be considered.",

    "POPLITEAL HEIGHT SITTING": "Generally for design purpose, 5th percentile value of user population is to be considered.",

    "HAND THICKNESS AT METACARPAL III": "Depending upon the design requirement, the percentile value of user population may be selected. For clearance purpose, 95th percentile value of user population is to be considered. For safety guard design, 5th percentile value of user population is to be considered. For gloves design, 95th percentile value of user population is to be considered.",

    "FIRST PHALANX DIGIT III LENGTH": "For clearance purpose, 95th percentile value of user population is to be considered.",

    "GRIP SPAN": "Generally for design purpose, 5th percentile value of user population is to be considered.",

    "MAXIMUM GRIP LENGTH": "Generally for design purpose, 5th percentile value of user population is to be considered.",

    "INDEX FINGER DIAMETER": "Generally for design purpose, 95th percentile value of user population is to be considered.",

    "HEAD LENGTH": "Generally for design purpose, 95th percentile value of user population is to be considered. However, depending upon the design requirement, the percentile value of user population may be selected.",

    "HEAD BREADTH": "Generally for design purpose, 95th percentile value of user population is to be considered. However, depending upon the design requirement, the percentile value of user population may be selected.",

    "CORONOID FOSSA TO HAND LENGTH": "For clearance purpose, 95th percentile value of user population is to be considered. For reach purpose, 5th percentile value of user population is to be considered.",

    "FOREARM HAND LENGTH": "For clearance purpose, 95th percentile value of user population is to be considered. For reach purpose, 5th percentile value of user population is to be considered.",

    "ELBOW GRIP LENGTH": "For reach purpose, 5th percentile value of user population is to be considered.",

    "HAND LENGTH": "For clearance purpose, 95th percentile value of user population is to be considered. For reach purpose, 5th percentile value of user population is to be considered.",

    "PALM LENGTH": "Generally for design purpose, 5th percentile value of user population is to be considered.",

    "HAND BREADTH ACROSS THUMB": "Depending upon the design requirement, the percentile value of user population may be selected.",

    "HAND BREADTH": "Depending upon the design requirement, the percentile value of user population may be selected.",

    "BUTTOCK KNEE LENGTH": "For clearance purpose, 95th percentile value of user population is to be considered. Depending upon the design requirement, the percentile value of user population may be selected.",

    "BUTTOCK POPLITEAL LENGTH": "Generally for seat depth design, 5th percentile value of user population is to be considered. Depending upon the design requirement, the percentile value of user population may be selected.",

    "ABDOMINAL DEPTH SITTING": "Generally for design purpose, 95th percentile value of user population is to be considered.",

    "HIP BREADTH SITTING": "Generally for design purpose, 95th percentile value of user population is to be considered.",

    "ELBOW-ELBOW BREADTH SITTING": "Generally for design purpose, 95th percentile value of user population is to be considered.",

    "KNEE-KNEE BREADTH": "Generally for design purpose, 95th percentile value of user population is to be considered.",

    "FOOT LENGTH": "Generally for design purpose, 95th percentile value of user population is to be considered. Depending upon the design requirement, the percentile value of user population may be selected.",

    "INSTEP LENGTH": "Depending upon the design requirement, the percentile value of user population may be selected.",

    "FOOT BREADTH (BALL OF THE FOOT)": "Generally for design purpose, 5th percentile value of user population is to be considered.",

    "FUNCTIONAL LEG LENGTH": "Generally for design purpose, 95th percentile value of user population is to be considered. Depending upon the design requirement, the percentile value of user population may be selected.",

    "BICEP SKINFOLD THICKNESS": "This skinfold thickness value is used to calculate body density, body fat and finally lean body mass as given in Annexure V.",

    "TRICEP SKINFOLD THICKNESS": "This skinfold thickness value is used to calculate body density, body fat and finally lean body mass as given in Annexure V.",

    "SUBSCAPULAR SKINFOLD THICKNESS": "This skinfold thickness value is used to calculate body density, body fat and finally lean body mass as given in Annexure V.",

    "SUPRA ILIAC SKINFOLD THICKNESS": "This skinfold thickness value is used to calculate body density, body fat and finally lean body mass as given in Annexure V.",

    "HAND GRIP STRENGTH (RIGHT)": "Generally the operating resistance of a control should be within the capacity of weaker member of the user population i.e. 5th percentile. Up to 60% of an individual's maximum strength is acceptable for occasional exertion. Up to 30% of an individual's maximum strength is acceptable for frequent exertion.",

    "HAND GRIP STRENGTH (LEFT)": "Generally the operating resistance of a control should be within the capacity of weaker member of the user population i.e. 5th percentile. Up to 60% of an individual's maximum strength is acceptable for occasional exertion. Up to 30% of an individual's maximum strength is acceptable for frequent exertion.",

    "PUSH STRENGTH (BOTH HANDS) STANDING": "Generally the operating resistance of a control should be within the capacity of weaker member of the user population i.e. 5th percentile. Up to 60% of an individual's maximum strength is acceptable for occasional exertion. Up to 30% of an individual's maximum strength is acceptable for frequent exertion.",

    "PULL STRENGTH (BOTH HANDS) STANDING": "Generally the operating resistance of a control should be within the capacity of weaker member of the user population i.e. 5th percentile. Up to 60% of an individual's maximum strength is acceptable for occasional exertion. Up to 30% of an individual's maximum strength is acceptable for frequent exertion.",

    "PUSH STRENGTH (LEFT HAND) SITTING": "Generally the operating resistance of a control should be within the capacity of weaker member of the user population i.e. 5th percentile. Up to 60% of an individual's maximum strength is acceptable for occasional exertion. Up to 30% of an individual's maximum strength is acceptable for frequent exertion.",

    "PULL STRENGTH (LEFT HAND) SITTING": "Generally the operating resistance of a control should be within the capacity of weaker member of the user population i.e. 5th percentile. Up to 60% of an individual's maximum strength is acceptable for occasional exertion. Up to 30% of an individual's maximum strength is acceptable for frequent exertion.",

    "PUSH STRENGTH (RIGHT HAND) SITTING": "Generally the operating resistance of a control should be within the capacity of weaker member of the user population i.e. 5th percentile. Up to 60% of an individual's maximum strength is acceptable for occasional exertion. Up to 30% of an individual's maximum strength is acceptable for frequent exertion.",

    "PULL STRENGTH (RIGHT HAND) SITTING": "Generally the operating resistance of a control should be within the capacity of weaker member of the user population i.e. 5th percentile. Up to 60% of an individual's maximum strength is acceptable for occasional exertion. Up to 30% of an individual's maximum strength is acceptable for frequent exertion.",

    "LEG STRENGTH (RIGHT) SITTING": "Generally the operating resistance of a control should be within the capacity of weaker member of the user population i.e. 5th percentile. Up to 60% of an individual's maximum strength is acceptable for occasional exertion. Up to 30% of an individual's maximum strength is acceptable for frequent exertion.",

    "FOOT STRENGTH (RIGHT) SITTING": "Generally the operating resistance of a control should be within the capacity of weaker member of the user population i.e. 5th percentile. Up to 60% of an individual's maximum strength is acceptable for occasional exertion. Up to 30% of an individual's maximum strength is acceptable for frequent exertion.",

    "LEG STRENGTH (LEFT) SITTING": "Generally the operating resistance of a control should be within the capacity of weaker member of the user population i.e. 5th percentile. Up to 60% of an individual's maximum strength is acceptable for occasional exertion. Up to 30% of an individual's maximum strength is acceptable for frequent exertion.",

    "FOOT STRENGTH (LEFT) SITTING": "Generally the operating resistance of a control should be within the capacity of weaker member of the user population i.e. 5th percentile. Up to 60% of an individual's maximum strength is acceptable for occasional exertion. Up to 30% of an individual's maximum strength is acceptable for frequent exertion.",

    "TORQUE STRENGTH (PREFERRED HAND) STANDING": "Generally the operating resistance of a control should be within the capacity of weaker member of the user population i.e. 5th percentile. Up to 60% of an individual's maximum strength is acceptable for occasional exertion. Up to 30% of an individual's maximum strength is acceptable for frequent exertion.",

    "TORQUE STRENGTH (BOTH HANDS) STANDING": "Generally the operating resistance of a control should be within the capacity of weaker member of the user population i.e. 5th percentile. Up to 60% of an individual's maximum strength is acceptable for occasional exertion. Up to 30% of an individual's maximum strength is acceptable for frequent exertion.",

    "TORQUE STRENGTH (BOTH HANDS) SITTING": "Generally the operating resistance of a control should be within the capacity of weaker member of the user population i.e. 5th percentile. Up to 60% of an individual's maximum strength is acceptable for occasional exertion. Up to 30% of an individual's maximum strength is acceptable for frequent exertion.",

    "HAND GRIP TORQUE (PREFERRED HAND)": "Generally the operating resistance of a control should be within the capacity of weaker member of the user population i.e. 5th percentile. Up to 60% of an individual's maximum strength is acceptable for occasional exertion. Up to 30% of an individual's maximum strength is acceptable for frequent exertion."
}

#######################################################################################################
# Updated image file IDs - using direct Google Drive file IDs

male_image_data_links = {
    "ABDOMINAL DEPTH SITTING": "1BD83y4lJiT57vwGrolwvVxWRIILS0g1j",
    "ABDOMINAL EXTENSION TO WALL": "1r7CtdbEzFmlIOFE8T8HWD06gpLV200TL",
    "ACROMIAL HEIGHT": "1P-YnZR2glFLz80MD79RwWhy3DY3mo3-m",
    "ARM REACH FROM THE WALL": "110SP3icQ0-84aD79TFyGylfnt2weiTBn",
    "BIACROMIAL BREADTH": "14_qbVJ_ylei25PGdxKNV7_MNNPLbztwm",
    "BICEP SKINFOLD THICKNESS": "1gpw-Xjmp6KpIhCkLZ8AocHUUw5Cjs9Kj",
    "BIDELTOID BREADTH": "1kXzL5zYUkqMBnaOPUSwa4y2WidNMiMZN",
    "BIMALLELOLAR BREADTH": "1BYYYLmKHvNyV-0VZMpiV7mOU_BOrXUbG",
    "BUTTOCK KNEE LENGTH": "1q-l--Cuuj_mR8G8owQ7w3S2zMZ_W1puV",
    "BUTTOCK POPLITEAL LENGTH": "1GdA4y5EiqatDxP0EG0Lc10-D-AbIjzNn",
    "CALF CIRCUMFERENCE": "1uHDUiahgPoTQcVpmwPgvmSTxlMG8w3a9",
    "CHEST BREADTH": "1GzLZEae2XcnWy_oGQ-N4RDV5Dpfcm4MF",
    "CHEST CIRCUMFERENCE": "1Xj5Rqo1ouki2tTuJaF2InZuVS50EGzUI",
    "CHEST DEPTH": "1u4BLvX4arcoVW3pXrTNCnL5Z0QVBTg8G",
    "SUBSCAPULAR SKINFOLD THICKNESS": "1Ndw7m9vaYiprnoNVmahZIamf8ITHnR-d",
    "SUPRA ILIAC SKINFOLD THICKNESS": "11nwulislna4LvAhPglkxIhyJozLAfIJk",
    "TRICEP SKINFOLD THICKNESS": "1S5V692SQjin5VMQ2gDbbbijJRCpxHDGb",
    "CORONOID FOSSA TO HAND LENGTH": "1IdRqkA9EtEx2dtwKDPzll9zjQKs3ZJwm",
    "ELBOW GRIP LENGTH": "1cFVM-C5CAlbOTAf5qHYrh_yohwE6YpKQ",
    "ELBOW HEIGHT": "1OGIUvK25lNz7wvQHCPkCuQeT070vROdd",
    "ELBOW REST HEIGHT": "1Pqh4TaEl3xbllxF5_vUzB9dhzY_Urxu5",
    "ELBOW-ELBOW BREADTH SITTING": "15WKOiRQGwkIbD_B6hSbGd4bGbK-ZHxHU",
    "EYE HEIGHT": "1jXn3UdYc5vBS04n9miocOeHHf6lOVzz3",
    "FIRST PHALANX DIGIT III LENGTH": "1vt41DhkPNRsIgeunh_-NsA_9wEtb5qik",
    "FOOT BREADTH (BALL OF THE FOOT)": "1DnvD2CDCvv9zieyAjD5OjyUFuqn-w0LC",
    "FOOT LENGTH": "1W66noyyN06ca5teLtf5NegVbySCoJHNK",
    "FOOT STRENGTH (LEFT) SITTING": "1LCoiFoGr5xCd-lrcHt9TGZNu0MeoemjX",
    "FOOT STRENGTH (RIGHT) SITTING": "1QFMCV_qVUjff_5RLzB1S4ksyf700o1p0",
    "FOREARM HAND LENGTH": "1wN7cAp5pjLCt7_x7iSFKgpGyGKZgl5av",
    "FUNCTIONAL LEG LENGTH": "1YN5IVecbtpQeg3JHeT1DH6f4oPfjODjJ",
    "GRIP SPAN": "1Cy7UEc5_eVXkEoG1XB9jYSEaEZZWTEva",
    "GRIP DIAMETER (INSIDE)": "10-yxNnQHbNcqNV6gd-QD1evv3AVf4SnJ",
    "GRIP DIAMETER (OUTSIDE)": "1YNA9hh3gXa0ZN-ah18KWH3zDPESWZ3yc",
    "HAND BREADTH": "1jUCYD2abyVAvD1THPua2-J5gS9Eb0e2g",
    "HAND BREADTH ACROSS THUMB": "1BXubqP0ILngOyxWjjO5BePAnya6UAPDX",
    "HAND GRIP STRENGTH (LEFT)": "1FzUCNA9r0FebD6zanphrECLkYG1sePAz",
    "HAND GRIP STRENGTH (RIGHT)": "1RdUduxtURYEUcOd98eTZKO_tc5Wp0mNP",
    "HAND GRIP TORQUE (PREFERRED HAND)": "12TpVwQH2tLzq0KnmymqMGPJx3yBD1i_B",
    "HAND LENGTH": "1S2E9Xv_sztQf7tTbpqaAntLVulCIIMcz",
    "HAND THICKNESS AT METACARPAL III": "1PaF2uMS6veG74_lJMUJxGFV-uQqu3FrL",
    "HEAD BREADTH": "1u3P4m6MUlXk9qsc4ghhe5U0Q6C-nvgxw",
    "HEAD LENGTH": "1GXUacOpLW1p_IZJ5Gt9tyP7i5ECNnDkH",
    "HEEL BREADTH": "17J6KnzXfWSt4rBNPs6fYDny4nZJ3kSLw",
    "HIP BREADTH SITTING": "1Cg51Oyejs312aaUm0KM3Uw1j-cIioLX-",
    "HIP BREADTH": "1gNtVRoSQ-_jFytFli1sSm0DpWL9FVWjA",
    "ILLIOCRYSTALE HEIGHT": "1JUCUQkpDOkGm4W0uj8WrgvWODQ8Tr01H",
    "ILLIOSPINALE HEIGHT": "1V6ip0cm9hTu1RKxRKJMCOMAv6ZxwycPO",
    "INDEX FINGER DIAMETER": "1gf5z4k_t7foKruSnDU7_lrSp9TSVAI9-",
    "INSTEP LENGTH": "1dBHm5A3VElU1rakDeVsw1uTn72_Cd1Oy",
    "INTERSCYE BREADTH": "12oIPkc7oMpcMcls8k_leCJ7DiLQtNSjc",
    "KNEE HEIGHT SITTING": "1jDVG7apUDnRUs-0sV5tPzw1ZzKwjlgxb",
    "KNEE HEIGHT": "16RUaAYwthsLDLbCb0kCw-JZa0L1ZjHwF",
    "KNEE-KNEE BREADTH": "1-LJ6vgfr6Mavf-6Ac_KDHYvmbPE6IXuI",
    "LATERAL MALLEOLUS HEIGHT": "1jvuwhCyGhLQiBq00oX2e_iYafTjDVaVH",
    "LEG STRENGTH (LEFT) SITTING": "1TlzQbEFGtj-TUA-GpHhZZmNPanCFeSFu",
    "LEG STRENGTH (RIGHT) SITTING": "1vg7bAt7vgYyfBSlR302HowKplxjlsvA8",
    "MAXIMUM GRIP LENGTH": "16qItz5hdgK3SUSIHWf27ENYZU2inlbdQ",
    "TORQUE STRENGTH (BOTH HANDS) STANDING": "1IqJsn0D0RdoUxEf4Ucz_m0L_us9_PhWm",
    "MEDIAL MALLEOLUS HEIGHT": "1zm8QaWjg03ZdFXSYFxAJx1UKG53K_-Br",
    "MENTON TO TOP OF HEAD": "1lSQ7twMxHe7g2KxC0as0pSIKgB4b9IST",
    "METACARPAL III HEIGHT": "1LUEvTq8PBTG99jR-BFSqdI5S6ugCPSjw",
    "MIDDLE FINGER PALM GRIP DIAMETER": "1gYg5xSNNxdyRCisVz1pDvQ-Z5YdETEhb",
    "OLECRANON HEIGHT": "1tjVtNY-sF2aU8FOCyc_qWqTgzADxOaiY",
    "PALM LENGTH": "1Dja-KakNI7uVL-zclFPIjUWaC4ZvWRY9",
    "POPLITEAL HEIGHT SITTING": "1pIIAur-ndtuFAWK06Xl9lw9BauJmmgYO",
    "PULL STRENGTH (BOTH HANDS) STANDING": "1IILCfg_jCpoUgWcrSZWBFnxqlt2cZmSc",
    "PULL STRENGTH (LEFT HAND) SITTING": "1SdOnr6yBWLhH-rzjA9Eh4O_fvwE9OPF7",
    "PULL STRENGTH (RIGHT HAND) SITTING": "157dtSaTe4aprMqU9vgPiy_EWVF-JVtHf",
    "PUSH STRENGTH (BOTH HANDS) STANDING": "1fiHmBhnRVaXCAPEiAj_TkxZ41khJRsxR",
    "PUSH STRENGTH (LEFT HAND) SITTING": "1AswLQecXZzxQov4zTWNxJ1sBhVWluycZ",
    "PUSH STRENGTH (RIGHT HAND) SITTING": "1d_VqfbeuCrRtC0ODJt4EsE2f1u34vawY",
    "SCAPULA TO WAIST BACK LENGTH": "15VPV8Bw-85XpkFpN3Qy06qR9Bt9kiX6X",
    "SHOULDER GRIP LENGTH": "1HZlVcJ_49g5kQAijidlLCvzVT_GBs7VL",
    "SITTING ACROMIAL HEIGHT": "1U2IiK6mzSefTsMUKWVGeQHc81Ocq_2mc",
    "SITTING EYE HEIGHT": "1MWtY6qR5Y0DHJSXINZ06UlOiEFKaV1TH",
    "SITTING HEIGHT": "1T_tgBmeSoo4hfVy1Is1_OsIkvghUzPw6",
    "SPAN AKIMBO": "1kNvyxBc7fqvLvF1Sz9ZGzlQ-EyIqdwin",
    "SPAN": "1vOEqkA_b4e2RtOc3mY0deMvHiGTSCmq5",
    "STATURE": "19uNjtlHpBmxQVuhqZ7blG481Le2LS1Pv",
    "SUBSCAPULAR SKINFOLD THICKNESS": "1VzXFaRDPBr5K8TgbioxIKAw8cF8MwwWd",
    "SUPRA ILIAC SKINFOLD THICKNESS": "1SXRMKoMgeHSd5ZExn5aztIf_8hvOzdlN",
    "THIGH CIRCUMFERENCE": "113EO40hDuFjoozvPo7Irbu_oC3yJ7lwe",
    "THIGH CLEARANCE HEIGHT SITTING": "1pbqzwnPmnbrlBZSPayMjOK0Fa-_6DA1W",
    "THUMB TIP REACH": "16lNO6RX8U8AlzhpR-7RHwdRmiQXcndfI",
    "TORQUE STRENGTH (BOTH HANDS) SITTING": "1nRB8me5FMrmJ609x9W-ILYrzG9Imho6c",
    "TORQUE STRENGTH (BOTH HANDS) STANDING": "1y6_kvTLmjbr-J8u3nQgTodJXXM41xH3L",
    "TORQUE STRENGTH (PREFERRED HAND) STANDING": "1CsDiClg-r86duYsoSMk10g0S5RfsKuBe",
    "TRICEP SKINFOLD THICKNESS": "15FfjGiLCRMXOFhP4tVNKlXwaZTkqCOkD",
    "TROCHANTERIC HEIGHT": "1GUfm0J37J8243q0Ggx885DATCgKTeMmP",
    "VERTICAL GRIP REACH SITTING": "11Qmz-IgjVN5pfR-D-sP6drU-pt6IToK-",
    "VERTICAL GRIP REACH": "1DcCMDbhiUU0LtIqDPylbdnWW97q-176F",
    "VERTICAL REACH": "12jQORoxUW1VMDuk_WsGH1ZyUbapYWxHF",
    "WAIST BREADTH": "19-Ia8Um0fl68_Y-LYa4OxQmx6JdXsMjm",
    "WAIST CIRCUMFERENCE": "1FPX4z4T4lucS2bscm_KxclsWKWLMfDL1",
    "WALL TO LUMBOSACRAL DISTANCE": "1oWkqZHWfXfe44Od3udjVbaVCxUW_yIX7",
    "WALL TO ACROMION DISTANCE": "1IHRgxSoQHIIKRjV1Ig4iR7z_qqqwS1FF",
    "WEIGHT": "1E-ejOucXFO8-rnFB8bnH8lQ3WDEpOXIU",
    "WAIST BACK LENGTH": "19tst62Hmyg2IV3Sk9wwl6b5EHV2UR7VG",
    "WRIST CIRCUMFERENCE": "1O3CPH-vkpiFPn5oYe8WtSFgbQ1bRSu4G"
}





female_image_data_links = {
    "ABDOMINAL DEPTH SITTING": "1uujcvgtFdBzEumqo1GWYaZeRCM1MgYxG",
    "ABDOMINAL EXTENSION TO WALL": "1HqCiYUt9OhnfRrfWDtFBso19DN1lqVYh",
    "ACROMIAL HEIGHT": "17ZrxxcSvPWKKEi0s0eScd4kGAJxzz9HO",
    "ARM REACH FROM THE WALL": "1OqCLuVQ-52u7wlRsryaFhx31MvpkAHPv",
    "BIACROMIAL BREADTH": "1jrbeP28qe7HInegC4C4lDc2MAGOB9E1j",
    "BICEP SKINFOLD THICKNESS": "1NAx6XYXhQv2FlMAyZcYJlXJKi9UBSWOh",
    "BIDELTOID BREADTH": "1v3h9sjDq9Ritl_fAXpB9b4GeIIS_SSVq",
    "BIMALLELOLAR BREADTH": "10DaRqc1bVPdrhxmBvHYdZaScnA4Qj6Xw",
    "BUTTOCK KNEE LENGTH": "1dItOnaZn6nWStbrntbXS3HG1OpUZdEqK",
    "BUTTOCK POPLITEAL LENGTH": "1Uf6cFLW01r9UTYfXSvAzKQ2WhRC3xl2p",
    "CALF CIRCUMFERENCE": "1n4CUKAXYcx-1C7WgGbEsebGirbKF5fYs",
    "CHEST BREADTH": "1Q0iZLTPLXuM9AITzPyTIpK7aVetD72EL",
    "CHEST CIRCUMFERENCE": "16aFibKlhFp1UscUcvaEY3SOOM2ZfrBCr",
    "CHEST DEPTH": "1RXohvwoFbE0SmqvJK7NpQF2NS1raSzgY",
    "CORONOID FOSSA TO HAND LENGTH": "1Y3SBiFpBpijngV0YJGZmVoK_eDaB5-pE",
    "ELBOW GRIP LENGTH": "1RnRqy_JcmhzkijWvL3FmNdBMLE-6S4hz",
    "ELBOW HEIGHT": "1iwZ92MQr_uaWUGGgDY7EhJgeID_FJSPQ",
    "ELBOW REST HEIGHT": "16tKwCnKgP1cSHAXZwvsAPrdTgUdspfUP",
    "ELBOW-ELBOW BREADTH SITTING": "1rz8CdDqVn7u1S9LLi3D6xW1NFVKdbxdh",
    "EYE HEIGHT": "1GnEQiWqVYFyx73sh_cn8un_mzCZFkXRg",
    "FIRST PHALANX DIGIT III LENGTH": "1KbKSf-YokD1Gr2HPEAyXGh_6P1k6pDtc",
    "FOOT BREADTH (BALL OF THE FOOT)": "1weOSLZQ_GUvvWn0w-PltKr2zYq9DXUSc",
    "FOOT LENGTH": "1aJIc_4SSGAZ5eZGjcsV_sv1uCJGO59-v",
    "FOOT STRENGTH (LEFT) SITTING": "1hb2UfTXvoj0BPYi2XqNrCsx7quB3ayok",
    "FOOT STRENGTH (RIGHT) SITTING": "1TBZoVoWpAmDjNcjoc4SSCelMn31Ab4hs",
    "FOREARM HAND LENGTH": "1vqExc2Rpn9AQ1SHx2apyQJ75CUFaGN5E",
    "FUNCTIONAL LEG LENGTH": "1ZuBqGA8pUyrJb65B1awQ10-OLSGhQC7y",
    "GRIP SPAN": "155d0iwldvmWKe6PtOn2OxMfsbBWoCRqU",
    "GRIP DIAMETER (INSIDE)": "1qctBQQgCNm0xsx9cW3nwRiB3M4qQQ8vT",
    "GRIP DIAMETER (OUTSIDE)": "13yLK6J5iqkRyrwtXubIqlRukmWw2B7RD",
    "HAND BREADTH": "1xTYfh3P9Y5YfMGvhL7egZXeICiDsrI0f",
    "HAND BREADTH ACROSS THUMB": "1_6LUHAcOR2sVVZ6fOk-VoyizqnJw9oKO",
    "HAND GRIP STRENGTH (LEFT)": "1Ezo_PL-3Sp4cdzslcueMUR0aCta1GRiG",
    "HAND GRIP STRENGTH (RIGHT)": "1P79fWBplcCKPK1fKLDT8dP_roPmLasmQ",
    "HAND GRIP TORQUE (PREFERRED HAND)": "1tyHd5ejvcGeafF0K2bR2EwG1OSyxQd1N",
    "HAND LENGTH": "1MpaRBVZoT2GUMFaLQPuxmcvd1TvfqkEN",
    "HAND THICKNESS AT METACARPAL III": "1LrEG8ErqxQoU7zLn4PL73COpn1CmQhwq",
    "HEAD BREADTH": "1xw9jorsJkDrclVb2n6tSiwiLJBvKi8N2",
    "HEAD LENGTH": "1cdv6Uim8vweTpUYskST5bNJdBVqIiQMr",
    "HEEL BREADTH": "1bJePgnjdJh7DrEgNarIB4OEm1iLzInbN",
    "HIP BREADTH": "14bF8hnn58irA7HWcNKgJPkIfWgbFij9a",
    "HIP BREADTH SITTING": "12Zru9397Sqp4VUgJFOEWtl_fOcyWMwq6",
    "ILLIOCRYSTALE HEIGHT": "1JuToWOu7ZM1qv0nUX97tCTJ6ZTd5N92_",
    "ILLIOSPINALE HEIGHT": "161ByJ08yUSVazY-fi1YVIycAN6oT0lo_",
    "INDEX FINGER DIAMETER": "1TBBddrzNpIEMx9zRvMx3N6PsRIrGP4Fa",
    "INSTEP LENGTH": "1PbnZvIBbLHAkM-CO6400KPJlRtj55HBh",
    "INTERSCYE BREADTH": "1L_bvRV0_WyEkqWol7vWYkOGZNY6TcAy6",
    "KNEE HEIGHT": "1uDXkaz4MT_lkoJ9TNpRb1C-_uVW3UZrS",
    "KNEE HEIGHT SITTING": "1mPoOVihM5n9uYGTBhcGkADLPSTsOeZRn",
    "KNEE-KNEE BREADTH": "15quOaMQ3n-f081MbAaV6QvD75GWzqyOx",
    "LATERAL MALLEOLUS HEIGHT": "1Boaj2PA19ahjPFsyGVWwcPk9dss7kNvw",
    "LEG STRENGTH (LEFT) SITTING": "1YHloKqaqF50idux-3HSpZkE-1My77Ikq",
    "LEG STRENGTH (RIGHT) SITTING": "1oxcNOffS7NrZ3HAGgFPCQsPo39zf7guf",
    "MAXIMUM GRIP LENGTH": "1HeqgcnPHiZ8q3bu3MQB6_NS-W-5vZX72",
    "MEDIAL MALLEOLUS HEIGHT": "1n2tW-Gq_6ZSsfg3jyNB9IkgcIrm749fa",
    "MENTON TO TOP OF HEAD": "1cJFhQT0ZY87OkOIwrpII9fVMMxCV-PI1",
    "METACARPAL III HEIGHT": "1cP_GEu7qsmc_EpWvBmQikpi6pYA2jIt7",
    "MIDDLE FINGER PALM GRIP DIAMETER": "1WcGl8Rq3jAD5cvH2Ns9PKcQvnPR0_7Fg",
    "OLECRANON HEIGHT": "1YNjquoQT2xUFs2-PLPv0cCR2mzFsLr_v",
    "PALM LENGTH": "1vN3g0LbcceeNQxm0h0dpEDpt0w6KRhR3",
    "POPLITEAL HEIGHT SITTING": "1XSe7QMrg1VGBHJlq71uTgrZVNV_OPnFS",
    "PULL STRENGTH (BOTH HANDS) STANDING": "13tyOpd2eeNFvO_bsUm7odYF2Qokmr36v",
    "PULL STRENGTH (LEFT HAND) SITTING": "1F8b5ErTE0ota1z-9Ej8hb8DkEMYnlt6W",
    "PULL STRENGTH (RIGHT HAND) SITTING": "1AO9xb5fA6mTHFTg6Zn3KowbICwtVkTL3",
    "PUSH STRENGTH (BOTH HANDS) STANDING": "1WGqBhF29hynnJmE9JwnBz2y1MJ17aCA0",
    "PUSH STRENGTH (LEFT HAND) SITTING": "1YlW9KkGZ211C5KdVswICKmYnaa-OE_RH",
    "PUSH STRENGTH (RIGHT HAND) SITTING": "1BEhBC5PwDfNlUsv0N1ne9Tp3dTv3V3I0",
    "SCAPULA TO WAIST BACK LENGTH": "1uwICmyTXcmnAjwSgk1bxgIYmFJjwA0WX",
    "SHOULDER GRIP LENGTH": "1M4-TZ_2KGoVW2Gb9ZLEOLoEF86lsiCI1",
    "SITTING ACROMIAL HEIGHT": "1cUnMTANBfAsVK0MJsDm6YJDl0BR5ozLy",
    "SITTING EYE HEIGHT": "1dRRvxwSeJ5vTfAfW5Tepq1k3n_Tu1NNv",
    "SITTING HEIGHT": "1jvUhcB_8wH52bn5mQa3VJHW_aLOuS9LR",
    "SPAN": "1wDawR1QuvwnyU15b21ACgTpKrmT9np7R",
    "SPAN AKIMBO": "13VEdjgmIlBaJydKCLGWT01jF0p9Szb8O",
    "STATURE": "1ETACV-9syY2lqtL4B9GR4iuG0SRkMwXm",
    "SUBSCAPULAR SKINFOLD THICKNESS": "1Rm5bmNUQVkBw5pJVB7yLf6qPNUytezfh",
    "SUPRA ILIAC SKINFOLD THICKNESS": "1qFQ8-DbTXRHiujTjjDCHwv4EuiZmf2dZ",
    "THIGH CIRCUMFERENCE": "1iH5jSmkXfkdu12WYgP3J64iMF9RZR4DT",
    "THIGH CLEARANCE HEIGHT SITTING": "1pJ1n0zS_KbJBMKlWIa9OflqcvG7lDdJx",
    "THUMB TIP REACH": "1KflzBw758fjC7ZeMF-zIk4Y03RTfNI7x",
    "TORQUE STRENGTH (BOTH HANDS) SITTING": "16uNxUAXnC4-1n6f4zlavwxGsPOtiOQXJ",
    "TORQUE STRENGTH (BOTH HANDS) STANDING": "1BhPU6gCVBsQGPgSZ4Z9lGNsWEYwVTWuM",
    "TORQUE STRENGTH (PREFERRED HAND) STANDING": "1myDMUblBIxoH9ZMTzjoUnlV4ofVCEJ9M",
    "TRICEP SKINFOLD THICKNESS": "1tZmgq-0UXKJyE5nHLp_hN0eRXKhHbHUx",
    "TROCHANTERIC HEIGHT": "1skQIwAnFcNg8HQR4clyAPgzeJA3RP705",
    "VERTICAL GRIP REACH": "1mXznRBz_OPBewLjS0ctYEi3z_Tgbft8T",
    "VERTICAL GRIP REACH SITTING": "1W73ECV67Dndhxnthhvyw9dUYeeIZpMGT",
    "VERTICAL REACH": "1WtkognvwKCIvhCfJdQokXM8P9cSNV72u",
    "WAIST BREADTH": "1OwgmR_CHwerqWbVpBlu0z-Ckx3ExRPF2",
    "WAIST CIRCUMFERENCE": "10lcsIqAoi3xSuy2Wqb4lEHEfzkrUsGoG",
    "WALL TO LUMBOSACRAL DISTANCE": "1OTdgvwKx7GQ7RMOuKsKbmLgWfVttfJfF",
    "WALL TO ACROMION DISTANCE": "1k2Jf--Ya--YMGTo2VTwUWovEAaMkRfJc",
    "WEIGHT": "1LjOPe7Zbu5ErVSlrkQG_Un_aGr9n2cow",
    "WAIST BACK LENGTH": "1zFThCoic0A_DkXvtV0DsHCKQG1vX6K0W",
    "WRIST CIRCUMFERENCE": "1oSSxDPmQa95l7u6fx0WMxICWxdwBoTJC"
}


parameters = list(application_data.keys())
regions = ['All India', 'Arunachal Pradesh', 'Gujarat', 'Jammu & Kashmir', 'Madhya Pradesh', 'Maharashtra',
           'Meghalaya', 'Mizoram', 'Orissa', 'Punjab', 'Tamil Nadu', 'Uttar Pradesh', 'West Bengal']


# Password protected download function
def protected_download(data, filename, label):
    """Create a password-protected download button"""
    if st.button(label, key=f"download_{filename}"):
        password = st.text_input("Enter password to download:", type="password", key=f"pwd_{filename}")
        if password:
            if password == "farmergo":
                st.download_button(
                    label="✅ Download CSV",
                    data=data,
                    file_name=filename,
                    mime="text/csv",
                    key=f"confirmed_{filename}"
                )
                st.success("Password correct! You can now download the file.")
            else:
                st.error("Incorrect password. Please try again.")


# Compact image display function for Quick Stats
def display_compact_images(male_file_id, female_file_id, parameter):
    """Display compact male and female images side by side"""
    try:
        # Male image
        male_preview_url = f"https://drive.google.com/file/d/{male_file_id}/preview"
        st.markdown(f"""
        <iframe src="{male_preview_url}" width="100%" height="200" frameborder="0" 
                style="border-radius: 8px; margin-bottom: 10px;"></iframe>
        """, unsafe_allow_html=True)

        # Female image
        female_preview_url = f"https://drive.google.com/file/d/{female_file_id}/preview"
        st.markdown(f"""
        <iframe src="{female_preview_url}" width="100%" height="200" frameborder="0" 
                style="border-radius: 8px;"></iframe>
        """, unsafe_allow_html=True)
    except:
        st.info("Images not available")


# IMPROVED: Robust image display function with multiple fallback methods
@st.cache_data(show_spinner=False)
def fetch_google_drive_image(file_id):
    """Attempt to fetch image from Google Drive with multiple URL formats"""
    urls_to_try = [
        f"https://drive.google.com/uc?export=view&id={file_id}",
        f"https://lh3.googleusercontent.com/d/{file_id}",
        f"https://drive.google.com/uc?id={file_id}&export=download",
        f"https://docs.google.com/uc?id={file_id}&export=download"
    ]

    for url in urls_to_try:
        try:
            response = requests.get(url, timeout=10, stream=True)
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '').lower()
                # Check if it's an image and has reasonable size
                if ('image' in content_type or len(response.content) > 5000):
                    return response.content
        except Exception:
            continue

    return None


def display_parameter_image(image_links, parameter, gender, context="tab"):
    """Display parameter image with comprehensive fallback system"""
    if parameter not in image_links:
        st.markdown(f"""
        <div class="image-fallback">
            <h4>📊 {gender} Population - {parameter}</h4>
            <p>⚠️ Image data not available for this parameter</p>
        </div>
        """, unsafe_allow_html=True)
        return False

    file_id = image_links[parameter]

    # Create styled container
    st.markdown(f"""
    <div class="image-container">
        <div class="image-title">📊 {gender} Population - {parameter}</div>
    </div>
    """, unsafe_allow_html=True)

    # Method 1: Try to fetch and display image directly
    image_data = fetch_google_drive_image(file_id)
    if image_data:
        try:
            image = Image.open(io.BytesIO(image_data))
            st.image(image, use_container_width=True, caption=f"{parameter} - {gender} Population Data")
            return True
        except Exception as e:
            st.warning(f"⚠️ Error processing image data: {str(e)}")

    # Method 2: Embed using iframe (most reliable for Google Drive)
    try:
        preview_url = f"https://drive.google.com/file/d/{file_id}/preview"
        st.markdown(f"""
        <div style="text-align: center;">
            <iframe src="{preview_url}" class="responsive-iframe" frameborder="0">
                Your browser does not support iframes.
            </iframe>
        </div>
        """, unsafe_allow_html=True)

        # Provide additional access options
        view_url = f"https://drive.google.com/file/d/{file_id}/view"
        st.markdown(f"""
        <div style="text-align: center; margin-top: 10px;">
            <a href="{view_url}" target="_blank" style="color: #667eea; text-decoration: none; font-weight: bold;">
                🔗 Open image in new tab for better viewing
            </a>
        </div>
        """, unsafe_allow_html=True)

        return True

    except Exception as e:
        # Method 3: Final fallback - show links and error info
        st.markdown(f"""
        <div class="image-fallback">
            <h4>📊 {gender} Population - {parameter}</h4>
            <p>❌ Unable to display image directly</p>
            <p><strong>File ID:</strong> {file_id}</p>
        </div>
        """, unsafe_allow_html=True)

        # Provide multiple access options
        view_url = f"https://drive.google.com/file/d/{file_id}/view"
        direct_url = f"https://drive.google.com/uc?export=view&id={file_id}"

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**[📖 View in Google Drive]({view_url})**")
        with col2:
            st.markdown(f"**[📥 Direct Image Link]({direct_url})**")

        return False


# Enhanced function to fetch data from Google Sheets
@st.cache_data
def fetch_google_sheet_data(sheet_url):
    try:
        sheet_id = sheet_url.split('/')[5]
        sheet_url_csv = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        df = pd.read_csv(sheet_url_csv)
        df = clean_data(df)
        return df
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return pd.DataFrame()


# Data cleaning function
def clean_data(df):
    """Clean and convert data types for proper analysis"""
    try:
        df_clean = df.copy()
        numeric_columns = ['5th Percentile', 'Mean', '95th Percentile']
        existing_numeric_cols = [col for col in numeric_columns if col in df_clean.columns]

        if not existing_numeric_cols:
            potential_cols = [col for col in df_clean.columns if any(
                keyword in str(col).lower() for keyword in ['percentile', 'mean', 'average', '5th', '95th']
            )]

            if len(potential_cols) >= 3:
                existing_numeric_cols = potential_cols[:3]
                if len(potential_cols) >= 3:
                    df_clean = df_clean.rename(columns={
                        potential_cols[0]: '5th Percentile',
                        potential_cols[1]: 'Mean',
                        potential_cols[2]: '95th Percentile'
                    })
                    existing_numeric_cols = ['5th Percentile', 'Mean', '95th Percentile']

        for col in existing_numeric_cols:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].astype(str)
                df_clean[col] = df_clean[col].str.replace(r'[^\d.-]', '', regex=True)
                df_clean[col] = df_clean[col].replace('', np.nan)
                df_clean[col] = df_clean[col].replace('-', np.nan)
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

        if existing_numeric_cols:
            df_clean = df_clean.dropna(subset=existing_numeric_cols, how='all')

        if 'State' not in df_clean.columns:
            potential_state_cols = [col for col in df_clean.columns if any(
                keyword in str(col).lower() for keyword in ['state', 'region', 'location', 'area']
            )]
            if potential_state_cols:
                df_clean = df_clean.rename(columns={potential_state_cols[0]: 'State'})

        return df_clean

    except Exception as e:
        st.warning(f"Data cleaning warning: {str(e)}")
        return df


# Enhanced bar plot function
def create_enhanced_bar_plot(df, selected_states, title, color_scheme="viridis"):
    if "All India" not in selected_states:
        selected_states.insert(0, "All India")

    if 'State' not in df.columns:
        st.error("State column not found in data")
        return None

    filtered_data = df[df['State'].isin(selected_states)].copy()

    if filtered_data.empty:
        st.warning("No data available for the selected regions.")
        return None

    required_cols = ['5th Percentile', 'Mean', '95th Percentile']
    missing_cols = [col for col in required_cols if col not in filtered_data.columns]

    if missing_cols:
        st.error(f"Missing columns in data: {', '.join(missing_cols)}")
        st.info(f"Available columns: {', '.join(filtered_data.columns.tolist())}")
        return None

    filtered_data = filtered_data.dropna(subset=required_cols, how='all')

    if filtered_data.empty:
        st.warning("No valid numeric data available for the selected regions.")
        return None

    fig = make_subplots(rows=1, cols=1, subplot_titles=[title])

    colors = ['#10b981', '#f59e0b', '#ef4444']
    percentiles = ['5th Percentile', 'Mean', '95th Percentile']

    for i, percentile in enumerate(percentiles):
        y_values = filtered_data[percentile].fillna(0)

        fig.add_trace(
            go.Bar(
                name=percentile,
                x=filtered_data['State'],
                y=y_values,
                marker_color=colors[i],
                text=[f'{val:.1f}' if not pd.isna(val) else 'N/A' for val in filtered_data[percentile]],
                textposition='outside',
                hovertemplate=f'<b>{percentile}</b><br>' +
                              'State: %{x}<br>' +
                              'Value: %{y:.2f}<br>' +
                              '<extra></extra>'
            )
        )

    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=20, color='#1e3c72')),
        xaxis_title="",
        yaxis_title="Value",
        barmode='group',
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=50, r=50, t=80, b=50)
    )

    fig.update_xaxes(tickangle=-45, showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')

    return fig


# Enhanced radar chart function
def create_radar_chart(df, selected_states, title):
    if len(selected_states) > 6:
        selected_states = selected_states[:6]
        st.warning("Showing only first 6 regions for better readability in radar chart.")

    if 'State' not in df.columns:
        st.error("State column not found in data")
        return None

    filtered_data = df[df['State'].isin(selected_states)].copy()

    if filtered_data.empty:
        return None

    required_cols = ['5th Percentile', 'Mean', '95th Percentile']
    missing_cols = [col for col in required_cols if col not in filtered_data.columns]

    if missing_cols:
        st.warning(f"Cannot create radar chart. Missing columns: {', '.join(missing_cols)}")
        return None

    filtered_data = filtered_data.dropna(subset=required_cols, how='all')

    if filtered_data.empty:
        st.warning("No valid numeric data available for radar chart.")
        return None

    fig = go.Figure()
    colors = px.colors.qualitative.Set3

    try:
        for i, (_, row) in enumerate(filtered_data.iterrows()):
            r_values = [
                row['5th Percentile'] if not pd.isna(row['5th Percentile']) else 0,
                row['Mean'] if not pd.isna(row['Mean']) else 0,
                row['95th Percentile'] if not pd.isna(row['95th Percentile']) else 0
            ]

            fig.add_trace(go.Scatterpolar(
                r=r_values,
                theta=['5th Percentile', 'Mean', '95th Percentile'],
                fill='toself',
                name=row['State'],
                line_color=colors[i % len(colors)],
                fillcolor=colors[i % len(colors)],
                opacity=0.6
            ))

        max_val = 0
        for col in required_cols:
            col_max = filtered_data[col].max(skipna=True)
            if not pd.isna(col_max):
                max_val = max(max_val, col_max)

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, max_val * 1.1 if max_val > 0 else 100])),
            showlegend=True,
            title=dict(text=title, x=0.5, font=dict(size=18, color='#1e3c72')),
            height=500,
            paper_bgcolor='rgba(0,0,0,0)'
        )

        return fig

    except Exception as e:
        st.warning(f"Error creating radar chart: {str(e)}")
        return None


# Initialize session state for data caching
if 'male_data_cache' not in st.session_state:
    st.session_state.male_data_cache = {}
if 'female_data_cache' not in st.session_state:
    st.session_state.female_data_cache = {}

# Header
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🚜 FarmErgoDesign</h1>
    <p class="header-subtitle">Indian Agriculture Population's Anthropometric Data Viewer</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🔍 Search Parameters")

    st.markdown("### 📊 Parameter Selection")
    search_term = st.text_input("🔎 Search for a Parameter:", placeholder="Type to search...")
    filtered_parameters = [param for param in parameters if search_term.lower() in param.lower()]
    selected_parameter = st.selectbox(
        "Select a Parameter:",
        options=filtered_parameters,
        help="Choose an anthropometric parameter to analyze"
    )

    st.markdown("### 🎯 Application Selection")
    search_application = st.text_input("🔎 Search for an Application:", placeholder="Type to search...")
    all_applications = [app for sublist in application_data.values() for app in sublist]
    filtered_applications = [app for app in all_applications if search_application.lower() in app.lower()]
    selected_application = st.selectbox(
        "Select an Application:",
        options=[""] + filtered_applications,
        help="Choose an application area"
    )

    st.markdown("### 🌍 Region Selection")
    select_all = st.checkbox("Select All Regions")
    if select_all:
        selected_regions = st.multiselect("Regions:", regions, default=regions)
    else:
        selected_regions = st.multiselect("Regions:", regions, default=["All India"])

    st.markdown("---")
    fetch_data = st.button("🚀 Fetch Data", help="Click to load data for analysis")

# Main content with tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📋 Parameter Info", "👨 Male Population", "👩 Female Population", "🔄 Compare Data", "ℹ️ About"])

# Tab 1: Parameter Information - UPDATED LOGIC
with tab1:
    # Show Parameter Information when parameter is selected AND no application is selected
    if selected_parameter and not selected_application:
        st.markdown("## 📊 Parameter Information")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"### 🔬 {selected_parameter}")
            st.markdown(
                f'<div class="info-card"><strong>Definition:</strong><br>{definition_data[selected_parameter]}</div>',
                unsafe_allow_html=True)

            st.markdown("#### 🎯 Applications:")
            applications_html = "<ul>"
            for app in application_data[selected_parameter]:
                applications_html += f"<li>{app}</li>"
            applications_html += "</ul>"
            st.markdown(f'<div class="info-card">{applications_html}</div>', unsafe_allow_html=True)

            st.markdown("#### 📐 Design Guide:")
            st.markdown(f'<div class="info-card">{design_guide_data[selected_parameter]}</div>', unsafe_allow_html=True)

        with col2:
            st.markdown("#### 📈 Quick Stats")
            st.markdown(f'''
            <div class="metric-card">
                <h4>Applications Count</h4>
                <h2>{len(application_data[selected_parameter])}</h2>
            </div>
            ''', unsafe_allow_html=True)

            # Display compact images only
            if selected_parameter in male_image_data_links and selected_parameter in female_image_data_links:
                display_compact_images(
                    male_image_data_links[selected_parameter],
                    female_image_data_links[selected_parameter],
                    selected_parameter
                )

    # Show Parameters for Application when application is selected
    elif selected_application:
        st.markdown(f"## 🎯 Parameters for: {selected_application}")

        matched_parameters = {param: apps for param, apps in application_data.items() if selected_application in apps}

        if matched_parameters:
            for param in matched_parameters.keys():
                with st.expander(f"📊 {param}", expanded=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Definition:** {definition_data[param]}")
                    with col2:
                        st.markdown(f"**Design Guide:** {design_guide_data[param]}")

    # Show default message when nothing is selected
    else:
        st.info("👈 Please select a parameter or application from the sidebar to view information")

# Tab 2: Male Population
with tab2:
    if selected_parameter:
        st.markdown(f"## 👨 Male Population Data - {selected_parameter}")

        # Interactive Analysis Section
        st.markdown("### 📈 Interactive Analysis")

        if fetch_data and selected_parameter in male_parameter_data_links:
            with st.spinner('🔄 Loading male population data...'):
                male_data = fetch_google_sheet_data(male_parameter_data_links[selected_parameter])
                st.session_state.male_data_cache[selected_parameter] = male_data

            if not male_data.empty:
                # Create columns for summary stats and image
                col1, col2 = st.columns([2, 1])

                with col1:
                    numeric_cols = ['5th Percentile', 'Mean', '95th Percentile']
                    valid_cols = [col for col in numeric_cols if
                                  col in male_data.columns and not male_data[col].isna().all()]

                    if len(valid_cols) >= 3:
                        st.markdown("#### 📊 Summary Statistics")
                        col1_1, col1_2, col1_3 = st.columns(3)
                        with col1_1:
                            avg_5th = male_data['5th Percentile'].mean(skipna=True)
                            st.metric("Avg 5th", f"{avg_5th:.2f}" if not pd.isna(avg_5th) else "N/A")
                        with col1_2:
                            avg_mean = male_data['Mean'].mean(skipna=True)
                            st.metric("Avg Mean", f"{avg_mean:.2f}" if not pd.isna(avg_mean) else "N/A")
                        with col1_3:
                            avg_95th = male_data['95th Percentile'].mean(skipna=True)
                            st.metric("Avg 95th", f"{avg_95th:.2f}" if not pd.isna(avg_95th) else "N/A")
                    else:
                        st.warning("⚠️ Some data columns may contain non-numeric values.")

                with col2:
                    # Display image on the right side
                    if selected_parameter in male_image_data_links:
                        file_id = male_image_data_links[selected_parameter]
                        preview_url = f"https://drive.google.com/file/d/{file_id}/preview"
                        st.markdown(f"""
                        <iframe src="{preview_url}" width="100%" height="300" frameborder="0" 
                                style="border-radius: 8px;"></iframe>
                        """, unsafe_allow_html=True)

        else:
            st.info("👆 Click 'Fetch Data' to load interactive analysis")

        # Interactive Charts Section
        if fetch_data and selected_parameter and selected_parameter in male_parameter_data_links:
            male_data = fetch_google_sheet_data(male_parameter_data_links[selected_parameter])

            if not male_data.empty:
                st.markdown("### 📊 Interactive Charts")

                selected_data = male_data[male_data['State'].isin(selected_regions)] if selected_regions else male_data

                bar_fig = create_enhanced_bar_plot(selected_data, selected_regions.copy(),
                                                   f"Male Population - {selected_parameter}")
                if bar_fig:
                    st.plotly_chart(bar_fig, use_container_width=True)

                radar_fig = create_radar_chart(selected_data, selected_regions.copy(),
                                               f"Male Population Radar - {selected_parameter}")
                if radar_fig:
                    st.plotly_chart(radar_fig, use_container_width=True)

                st.markdown("### 📋 Complete Data Table")
                st.dataframe(
                    male_data.style.highlight_max(axis=0, color='lightgreen')
                    .highlight_min(axis=0, color='lightcoral')
                    .format({'5th Percentile': '{:.2f}', 'Mean': '{:.2f}', '95th Percentile': '{:.2f}'}),
                    use_container_width=True
                )

                # Password protected download
                csv = male_data.to_csv(index=False)
                protected_download(
                    csv,
                    f"male_{selected_parameter.lower().replace(' ', '_')}_data.csv",
                    "💾 Download Male Data as CSV"
                )
    else:
        st.info("👈 Please select a parameter from the sidebar to view male population data")

# Tab 3: Female Population
with tab3:
    if selected_parameter:
        st.markdown(f"## 👩 Female Population Data - {selected_parameter}")

        # Interactive Analysis Section
        st.markdown("### 📈 Interactive Analysis")

        if fetch_data and selected_parameter in female_parameter_data_links:
            with st.spinner('🔄 Loading female population data...'):
                female_data = fetch_google_sheet_data(female_parameter_data_links[selected_parameter])
                st.session_state.female_data_cache[selected_parameter] = female_data

            if not female_data.empty:
                # Create columns for summary stats and image
                col1, col2 = st.columns([2, 1])

                with col1:
                    numeric_cols = ['5th Percentile', 'Mean', '95th Percentile']
                    valid_cols = [col for col in numeric_cols if
                                  col in female_data.columns and not female_data[col].isna().all()]

                    if len(valid_cols) >= 3:
                        st.markdown("#### 📊 Summary Statistics")
                        col1_1, col1_2, col1_3 = st.columns(3)
                        with col1_1:
                            avg_5th = female_data['5th Percentile'].mean(skipna=True)
                            st.metric("Avg 5th", f"{avg_5th:.2f}" if not pd.isna(avg_5th) else "N/A")
                        with col1_2:
                            avg_mean = female_data['Mean'].mean(skipna=True)
                            st.metric("Avg Mean", f"{avg_mean:.2f}" if not pd.isna(avg_mean) else "N/A")
                        with col1_3:
                            avg_95th = female_data['95th Percentile'].mean(skipna=True)
                            st.metric("Avg 95th", f"{avg_95th:.2f}" if not pd.isna(avg_95th) else "N/A")
                    else:
                        st.warning("⚠️ Some data columns may contain non-numeric values.")

                with col2:
                    # Display image on the right side
                    if selected_parameter in female_image_data_links:
                        file_id = female_image_data_links[selected_parameter]
                        preview_url = f"https://drive.google.com/file/d/{file_id}/preview"
                        st.markdown(f"""
                        <iframe src="{preview_url}" width="100%" height="300" frameborder="0" 
                                style="border-radius: 8px;"></iframe>
                        """, unsafe_allow_html=True)

        else:
            st.info("👆 Click 'Fetch Data' to load interactive analysis")

        # Interactive Charts Section
        if fetch_data and selected_parameter and selected_parameter in female_parameter_data_links:
            female_data = fetch_google_sheet_data(female_parameter_data_links[selected_parameter])

            if not female_data.empty:
                st.markdown("### 📊 Interactive Charts")

                selected_data = female_data[
                    female_data['State'].isin(selected_regions)] if selected_regions else female_data

                bar_fig = create_enhanced_bar_plot(selected_data, selected_regions.copy(),
                                                   f"Female Population - {selected_parameter}")
                if bar_fig:
                    st.plotly_chart(bar_fig, use_container_width=True)

                radar_fig = create_radar_chart(selected_data, selected_regions.copy(),
                                               f"Female Population Radar - {selected_parameter}")
                if radar_fig:
                    st.plotly_chart(radar_fig, use_container_width=True)

                st.markdown("### 📋 Complete Data Table")
                st.dataframe(
                    female_data.style.highlight_max(axis=0, color='lightgreen')
                    .highlight_min(axis=0, color='lightcoral')
                    .format({'5th Percentile': '{:.2f}', 'Mean': '{:.2f}', '95th Percentile': '{:.2f}'}),
                    use_container_width=True
                )

                # Password protected download
                csv = female_data.to_csv(index=False)
                protected_download(
                    csv,
                    f"female_{selected_parameter.lower().replace(' ', '_')}_data.csv",
                    "💾 Download Female Data as CSV"
                )
    else:
        st.info("👈 Please select a parameter from the sidebar to view female population data")

# Tab 4: Compare Male vs Female Data
with tab4:
    st.markdown("## 🔄 Gender Comparison")

    if selected_parameter:
        st.markdown(f"### Comparing Male vs Female Data - {selected_parameter}")

        if (selected_parameter in male_parameter_data_links and
                selected_parameter in female_parameter_data_links):

            if st.button("🔄 Load Comparison Data", help="Click to compare male vs female data",
                         key="comparison_button"):
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### 👨 Male Population")
                    display_parameter_image(male_image_data_links, selected_parameter, "Male")

                with col2:
                    st.markdown("### 👩 Female Population")
                    display_parameter_image(female_image_data_links, selected_parameter, "Female")

                with st.spinner('Loading comparison data...'):
                    if selected_parameter in st.session_state.male_data_cache:
                        male_data = st.session_state.male_data_cache[selected_parameter]
                    else:
                        male_data = fetch_google_sheet_data(male_parameter_data_links[selected_parameter])
                        st.session_state.male_data_cache[selected_parameter] = male_data

                    if selected_parameter in st.session_state.female_data_cache:
                        female_data = st.session_state.female_data_cache[selected_parameter]
                    else:
                        female_data = fetch_google_sheet_data(female_parameter_data_links[selected_parameter])
                        st.session_state.female_data_cache[selected_parameter] = female_data

                if not male_data.empty and not female_data.empty:
                    st.markdown("### 📊 Statistical Comparison")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.markdown("#### 5th Percentile")
                        male_5th = male_data['5th Percentile'].mean(skipna=True)
                        female_5th = female_data['5th Percentile'].mean(skipna=True)

                        if not pd.isna(male_5th) and not pd.isna(female_5th):
                            diff_5th = male_5th - female_5th
                            st.metric("Male", f"{male_5th:.2f}")
                            st.metric("Female", f"{female_5th:.2f}", f"{diff_5th:+.2f}")
                        else:
                            st.warning("Data not available for comparison")

                    with col2:
                        st.markdown("#### Mean")
                        male_mean = male_data['Mean'].mean(skipna=True)
                        female_mean = female_data['Mean'].mean(skipna=True)

                        if not pd.isna(male_mean) and not pd.isna(female_mean):
                            diff_mean = male_mean - female_mean
                            st.metric("Male", f"{male_mean:.2f}")
                            st.metric("Female", f"{female_mean:.2f}", f"{diff_mean:+.2f}")
                        else:
                            st.warning("Data not available for comparison")

                    with col3:
                        st.markdown("#### 95th Percentile")
                        male_95th = male_data['95th Percentile'].mean(skipna=True)
                        female_95th = female_data['95th Percentile'].mean(skipna=True)

                        if not pd.isna(male_95th) and not pd.isna(female_95th):
                            diff_95th = male_95th - female_95th
                            st.metric("Male", f"{male_95th:.2f}")
                            st.metric("Female", f"{female_95th:.2f}", f"{diff_95th:+.2f}")
                        else:
                            st.warning("Data not available for comparison")

                    st.markdown("### 📊 Comparative Visualization")

                    if selected_regions:
                        male_filtered = male_data[male_data['State'].isin(selected_regions)]
                        female_filtered = female_data[female_data['State'].isin(selected_regions)]
                    else:
                        male_filtered = male_data
                        female_filtered = female_data

                    col1, col2 = st.columns(2)

                    with col1:
                        male_fig = create_enhanced_bar_plot(male_filtered,
                                                            selected_regions.copy() if selected_regions else [
                                                                'All India'],
                                                            f"Male - {selected_parameter}")
                        if male_fig:
                            st.plotly_chart(male_fig, use_container_width=True)

                    with col2:
                        female_fig = create_enhanced_bar_plot(female_filtered,
                                                              selected_regions.copy() if selected_regions else [
                                                                  'All India'],
                                                              f"Female - {selected_parameter}")
                        if female_fig:
                            st.plotly_chart(female_fig, use_container_width=True)

                    st.markdown("### 📊 Combined Comparison Chart")

                    try:
                        combined_fig = go.Figure()

                        combined_fig.add_trace(go.Bar(
                            name='Male - 5th Percentile',
                            x=male_filtered['State'],
                            y=male_filtered['5th Percentile'],
                            marker_color='lightblue',
                            opacity=0.4
                        ))

                        combined_fig.add_trace(go.Bar(
                            name='Female - 5th Percentile',
                            x=female_filtered['State'],
                            y=female_filtered['5th Percentile'],
                            marker_color='pink',
                            opacity=0.7
                        ))

                        combined_fig.add_trace(go.Bar(
                            name='Male - Mean',
                            x=male_filtered['State'],
                            y=male_filtered['Mean'],
                            marker_color='blue'
                        ))

                        combined_fig.add_trace(go.Bar(
                            name='Female - Mean',
                            x=female_filtered['State'],
                            y=female_filtered['Mean'],
                            marker_color='red'
                        ))

                        combined_fig.add_trace(go.Bar(
                            name='Male - 95th Percentile',
                            x=male_filtered['State'],
                            y=male_filtered['95th Percentile'],
                            marker_color='darkblue',
                            opacity=0.7
                        ))

                        combined_fig.add_trace(go.Bar(
                            name='Female - 95th Percentile',
                            x=female_filtered['State'],
                            y=female_filtered['95th Percentile'],
                            marker_color='darkred',
                            opacity=0.7
                        ))

                        combined_fig.update_layout(
                            title=f'Male vs Female Comparison - {selected_parameter}',
                            barmode='group',
                            height=600,
                            xaxis_title="State",
                            yaxis_title="Value"
                        )

                        st.plotly_chart(combined_fig, use_container_width=True)

                    except Exception as e:
                        st.error(f"Error creating combined chart: {str(e)}")
                        st.info("Individual charts are still available above")

                else:
                    st.error("Unable to load data for comparison. Please try again.")

            else:
                st.info("👆 Click the button above to load and compare male vs female data")

                st.markdown("#### 📋 Comparison Preview")
                st.markdown(f"""
                **Parameter:** {selected_parameter}

                **Data Sources Available:**
                - ✅ Male population data
                - ✅ Female population data

                **Comparison will include:**
                - Statistical metrics (5th percentile, mean, 95th percentile)
                - Side-by-side visualizations
                - Combined comparison charts
                - Gender difference analysis
                """)

        else:
            st.warning("⚠️ Comparison data not available for the selected parameter")

    else:
        st.info("👈 Please select a parameter from the sidebar to enable comparison")

# Tab 5: About
with tab5:
    st.markdown("## ℹ️ About FarmErgoDesign")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ### 🙏 Acknowledgement

       We gratefully acknowledge the **Central Institute of Agricultural Engineering (CIAE)**, Bhopal, for compiling and publishing the valuable reference titled *“Anthropometric and Strength Data of Indian Agricultural Workers for Farm Equipment Design”*(2009)*.
         

        We also sincerely acknowledge **Dr. L. P. Gite, Former Project Coordinator, AICRP on ESA** and his team for his significant contribution in preparing and compiling the Anthropometric and Strength Data of Indian Agricultural Workers, which serves as the foundational source for this web application.

        We further express our sincere gratitude to Tamil Nadu Agricultural University (TNAU) for providing the opportunity and institutional support to develop this web-based application for the benefit of designers, researchers and students.

       We also acknowledge Dr. Sukhbir Singh, Project Coordinator, AICRP on ESAAS, Dr. Vikumarkumar V, Ph.D. scholar, Er. Nithin Joel and Er. Pranav Krishna, Research scholars for their valuable assistance and contribution in the development of this web-based application

       The dataset is based on extensive surveys conducted by various research organizations under the *National Agricultural Research System (NARS)*. This pioneering work has greatly contributed to the ergonomic design and development of farm equipment suited to Indian agricultural workers.

       All rights and ownership of the original data remain with the respective copyright holder.

      ### 🔬 Book Publication Details:

        - Book No. CIAE/2009/4
        - ISBN 978-81-909305-0-5
        - Publisher: Central Institute of Agricultural Engineering (CIAE), Bhopal, India (2009)

        ### 📧 Contact Information

        For any information and suggestions, kindly contact at: 
        TNAU Centre, Coimbatore
        **Email:** [Email: esaas.cbe@tnau.ac.in](mailto:Email: esaas.cbe@tnau.ac.in)

       

    with col2:
        st.markdown('''
        <div class="info-box">
            <h4>🎯 App Features</h4>
            <ul>
                <li>🔐 Secure data downloads</li>
                <li>📊 Dynamic content switching</li>
                <li>📈 Optimized image layouts</li>
                <li>🌍 Multi-region comparison</li>
                <li>🔍 Enhanced search capabilities</li>
                <li>💾 Protected data exports</li>
                <li>📱 Responsive design</li>
                <li>🔄 Comprehensive analysis tools</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown('''
        <div class="success-box">
            <h4>📊 Available Parameters</h4>
            <ul>
                <li>⚖️ Weight measurements</li>
                <li>💪 Tricep skinfold thickness</li>
                <li>📏 Subscapular skinfold thickness</li>
                <li>📐 Supra iliac skinfold thickness</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown('''
        <div class="info-box">
            <h4>🛡️ Security Features</h4>
            <ul>
                <li>🔐 Password-protected downloads</li>
                <li>🔒 Data access control</li>
                <li>🛡️ Secure file handling</li>
                <li>🔑 Authentication system</li>
                <li>📋 Download verification</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 2rem;'>"
    "🚜 FarmErgoDesign © 2024 | Enhanced Anthropometric Data Viewer with Security & Improved UX"
    "</div>",
    unsafe_allow_html=True
)
