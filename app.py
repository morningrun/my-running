import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import calendar
import os
import base64

# 이미지 base64 변환 함수
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# 아이콘 및 앱 이름 메타 태그 생성 (mascot.png 활용)
icon_base64 = get_image_base64("mascot.png")
icon_meta_tag = ""
if icon_base64:
    icon_meta_tag = f"""
        <link rel="apple-touch-icon" href="data:image/png;base64,{icon_base64}">
        <link rel="icon" type="image/png" href="data:image/png;base64,{icon_base64}">
    """

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="200CREW",
    page_icon="🏃",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 화면 스타일 및 모바일 앱 메타 태그 CSS
st.markdown(f"""
    <head>
        <title>200CREW</title>
        <meta name="apple-mobile-web-app-title" content="200CREW">
        <meta name="application-name" content="200CREW">
        {icon_meta_tag}
    </head>
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    * {{
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif !important;
    }}

    header {{visibility: hidden;}}
    
    .stApp {{
        background-color: #F8FAFC;
    }}

    .block-container {{
        padding-top: 0.8rem !important;
        padding-bottom: 1.5rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }}
    
    .crew-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 14px;
        padding: 0 4px;
    }}
    .crew-title {{
        font-size: 1.5rem !important;
        font-weight: 900;
        letter-spacing: -0.5px;
        color: #0F172A;
        margin: 0;
    }}
    .crew-subtitle {{
        font-size: 0.78rem;
        color: #64748B;
        font-weight: 600;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 4px 10px;
        border-radius: 12px;
    }}

    .hero-card {{
        background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
        border-radius: 22px;
        padding: 20px 22px;
        color: #FFFFFF;
        box-shadow: 0 12px 28px -6px rgba(15, 23, 42, 0.25);
        margin-bottom: 16px;
    }}

    .hero-top-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 12px;
        margin-bottom: 14px;
    }}
    .hero-goal-title {{
        font-size: 0.82rem;
        color: #94A3B8;
        font-weight: 700;
        letter-spacing: 0.5px;
    }}
    .hero-goal-target {{
        font-size: 1.05rem;
        color: #38BDF8;
        font-weight: 900;
    }}

    .hero-bottom-row {{
        display: flex;
        align-items: baseline;
        justify-content: space-between;
    }}
    .hero-km-highlight {{
        font-size: 2.5rem;
        font-weight: 900;
        color: #FFFFFF !important;
        line-height: 1;
    }}
    .hero-km-label {{
        font-size: 1rem;
        font-weight: 600;
        color: #94A3B8 !important;
        margin-left: 2px;
    }}
    .hero-percent-tag {{
        background: linear-gradient(135deg, #38BDF8 0%, #0284C7 100%);
        color: #FFFFFF;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.95rem;
        font-weight: 800;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.35);
    }}

    .grid-container {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin-bottom: 16px;
    }}
    .sub-card {{
        background: #FFFFFF;
        border: 1px solid rgba(226, 232, 240, 0.9);
        border-radius: 16px;
        padding: 12px 14px;
        box-shadow: 0 4px 12px -2px rgba(148, 163, 184, 0.1);
    }}
    .sub-card-header {{
        display: flex;
        align-items: center;
        gap: 4px;
        margin-bottom: 4px;
    }}
    .sub-icon {{ font-size: 0.9rem; }}
    .sub-label {{ font-size: 0.73rem; color: #64748B; font-weight: 700; }}
    .sub-value {{ font-size: 1.15rem; font-weight: 900; color: #0F172A; }}
    .sub-accent {{ color: #0284C7; }}

    .stProgress > div > div > div > div {{
        background: linear-gradient(90deg, #38BDF8 0%, #0284C7 100%);
        border-radius: 10px;
    }}
    </style>
""", unsafe_allow_html=True)
