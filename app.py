import base64
import calendar
from datetime import datetime
import os
from zoneinfo import ZoneInfo
import plotly.express as px
import pandas as pd
import requests
import streamlit as st

# 이미지 base64 변환 함수 (마스코트 공용)
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# 마스코트 이미지 로드
mascot_base64 = get_image_base64("mascot.png")

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="이실권 200CREW",
    page_icon="🏃",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 화면 스타일 CSS
css_styles = """
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

* {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif !important;
}

header {visibility: hidden;}

.stApp {
    background-color: #F8FAFC;
}

.block-container {
    padding-top: 0.8rem !important;
    padding-bottom: 1.5rem !important;
    padding-left: 0.8rem !important;
    padding-right: 0.8rem !important;
}

.crew-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
    padding: 0 4px;
}

.crew-title {
    font-size: 1.45rem !important;
    font-weight: 900;
    letter-spacing: -0.6px;
    background: linear-gradient(135deg, #0F172A 0%, #0284C7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    white-space: nowrap;
}

.crew-subtitle {
    font-size: 0.75rem;
    color: #64748B;
    font-weight: 600;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    padding: 4px 10px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    gap: 5px;
    white-space: nowrap;
}

.hero-card {
    background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
    border-radius: 22px;
    padding: 20px 22px;
    color: #FFFFFF;
    box-shadow: 0 12px 28px -6px rgba(15, 23, 42, 0.25);
    margin-bottom: 16px;
}

.hero-top-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 12px;
    margin-bottom: 14px;
}
.hero-goal-title {
    font-size: 0.95rem;
    color: #94A3B8;
    font-weight: 700;
    letter-spacing: 0.3px;
}
.hero-goal-target {
    font-size: 1.45rem !important;
    color: #38BDF8;
    font-weight: 900;
}

.hero-bottom-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.hero-km-highlight {
    font-size: 2.3rem;
    font-weight: 900;
    color: #FFFFFF !important;
    line-height: 1;
}
.hero-km-label {
    font-size: 1rem;
    font-weight: 600;
    color: #94A3B8 !important;
    margin-left: 2px;
}
.hero-percent-tag {
    background: linear-gradient(135deg, #38BDF8 0%, #0284C7 100%);
    color: #FFFFFF;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.95rem;
    font-weight: 800;
    box-shadow: 0 4px 12px rgba(56, 189, 248, 0.35);
    display: inline-block;
    text-align: center;
}

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
.sub-value { font-size: 1.1rem; font-weight: 900; color: #0F172A; }

.sub-value-large { font-size: 1.45rem !important; font-weight: 900; }
.sub-accent { color: #0284C7; }

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #38BDF8 0%, #0284C7 100%);
    border-radius: 10px;
}

.custom-table {
    width: 100%;
    border-collapse: collapse;
    background-color: #FFFFFF;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #E2E8F0;
    font-size: 0.85rem;
}
.custom-table th {
    background-color: #F1F5F9;
    color: #0F172A;
    font-weight: 700;
    text-align: center;
    padding: 7px 6px;
    border-bottom: 1px solid #E2E8F0;
    line-height: 1.3;
}
.custom-table td {
    text-align: center;
    padding: 7px 6px;
    color: #334155;
    border-bottom: 1px solid #F1F5F9;
    line-height: 1.3;
}
.custom-table tr:last-child td {
    border-bottom: none;
}
</style>
"""
st.markdown(css_styles, unsafe_allow_html=True)

# 3. Secrets 보안 설정 확인
master_api_key = st.secrets.get("INTERVALS_API_KEY", "")
athlete_id_val = st.secrets.get("INTERVALS_ATHLETE_ID", "")

CREW_MEMBERS = {
    "이실권": athlete_id_val,
}

# 상단 로그인/선택 화면 (사이드바)
st.sidebar.markdown("## 🏃‍♂️ 200CREW 멤버 선택")
selected_member = st.sidebar.selectbox("크루원을 선택하세요", list(CREW_MEMBERS.keys()))
ATHLETE_ID = CREW_MEMBERS[selected_member]
API_KEY = master_api_key

if st.sidebar.button("🔄 데이터 새로고침"):
    st.cache_data.clear()
    st.rerun()

# 한국 시간(KST) 기준 현재 시간 설정
KST = ZoneInfo("Asia/Seoul")
now = datetime.now(KST)

# 4. 데이터 로딩
@st.cache_data(ttl=300)
def fetch_running_data(athlete_id, api_key, start_date_str):
    if not athlete_id or not api_key:
        return []
    url = f"https://intervals.icu/api/v1/athlete/{athlete_id}/activities?oldest={start_date_str}"
    try:
        response = requests.get(url, auth=("API_KEY", api_key), timeout=10)
