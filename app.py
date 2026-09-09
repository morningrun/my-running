import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import calendar
import os
import base64

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="이실권 200CREW",
    page_icon="🏃",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 화이트 톤 배경 & 대형 마스코트 스타일 CSS
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    * {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif !important;
    }

    header {visibility: hidden;}
    
    /* 전체 배경 화이트 톤 */
    .stApp {
        background-color: #F8FAFC;
    }

    .block-container {
        padding-top: 0.8rem !important;
        padding-bottom: 1.5rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }
    
    /* 타이틀 헤더 */
    .crew-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 14px;
        padding: 0 4px;
    }
    .crew-title {
        font-size: 1.5rem !important;
        font-weight: 900;
        letter-spacing: -0.5px;
        color: #0F172A;
        margin: 0;
    }
    .crew-subtitle {
        font-size: 0.78rem;
        color: #64748B;
        font-weight: 600;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 4px 10px;
        border-radius: 12px;
    }

    /* 3D 히어로 카드 */
    .hero-card {
        background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
        border-radius: 22px;
        padding: 20px;
        color: #FFFFFF;
        box-shadow: 0 12px 28px -6px rgba(15, 23, 42, 0.25);
        margin-bottom: 16px;
        position: relative;
        overflow: visible; /* 마스코트가 카드를 살짝 넘치도록 허용 */
    }

    .hero-top-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    .hero-label {
        font-size: 0.8rem;
        color: #38BDF8;
        font-weight: 800;
        letter-spacing: 0.8px;
    }

    /* 마스코트 대형 스타일 (얼굴/상체 중심, 카드를 넘치는 연출) */
    .mascot-large {
        width: 130px;
        height: 130px;
        border-radius: 50%;
        border: 4px solid #38BDF8;
        object-fit: cover;
        object-position: 50% 20%; /* 얼굴과 상체 위주로 확대 */
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
        background-color: #FFFFFF;
        display: block;
        margin-top: -15px; /* 위로 살짝 올라오게 배치 */
    }

    .hero-main-row {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
    }
    .hero-km-highlight {
        font-size: 2.3rem;
        font-weight: 900;
        color: #FFFFFF;
        line-height: 1;
    }
    .hero-km-total {
        font-size: 1.1rem;
        font-weight: 600;
        color: #94A3B8;
    }
    .hero-percent-tag {
        background: linear-gradient(135deg, #38BDF8 0%, #0284C7 100%);
        color: #FFFFFF;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 800;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.35);
    }

    /* 서브 카드 */
    .grid-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin-bottom: 16px;
    }
    .sub-card {
        background: #FFFFFF;
        border: 1px solid rgba(226, 232, 240, 0.9);
        border-radius: 16px;
        padding: 12px 14px;
        box-shadow: 0 4px 12px -2px rgba(148, 163, 184, 0.1);
    }
    .sub-card-header {
        display: flex;
        align-items: center;
        gap: 4px;
        margin-bottom: 4px;
    }
    .sub-icon { font-size: 0.9rem; }
    .sub-label { font-size: 0.73rem; color: #64748B; font-weight: 700; }
    .sub-value { font-size: 1.15rem; font-weight: 900; color: #0F172A; }
    .sub-accent { color: #0284C7; }

    /* 입체 프로그레스 바 */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #38BDF8 0%, #0284C7 100%);
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Secrets 수집
API_KEY = st.secrets["INTERVALS_API_KEY"]
ATHLETE_ID = st.secrets["INTERVALS_ATHLETE_ID"]

# 3. 데이터 로딩
@st.cache_data(ttl=300)
def fetch_running_data():
    now = datetime.now()
    start_date = now.strftime("%Y-%m-01")
    url = f"
