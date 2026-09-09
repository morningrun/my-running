import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import calendar

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="이실권 200CREW",
    page_icon="🏃",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 입체적 글래스모피즘 & 마스코트 스타일 CSS
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    * {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif !important;
    }

    header {visibility: hidden;}
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
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .crew-subtitle {
        font-size: 0.78rem;
        color: #64748B;
        font-weight: 600;
        background: #F1F5F9;
        padding: 4px 10px;
        border-radius: 12px;
    }

    /* 3D 히어로 카드 (마스코트 포함) */
    .hero-card {
        background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
        border-radius: 22px;
        padding: 20px;
        color: #FFFFFF;
        box-shadow: 0 12px 28px -6px rgba(15, 23, 42, 0.35);
        margin-bottom: 16px;
        position: relative;
        overflow: hidden;
    }

    .hero-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .hero-label {
        font-size: 0.8rem;
        color: #38BDF8;
        font-weight: 800;
        letter-spacing: 0.8px;
    }
    
    /* 마스코트 이미지 크기 및 둥근 스타일 */
    .mascot-img {
        width: 65px;
        height: 65px;
        border-radius: 50%;
        border: 2px solid #38BDF8;
        object-fit: cover;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }

    .hero-main-row {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        margin-top: 10px;
        margin-bottom: 8px;
    }
    .hero-km-highlight {
        font-size: 2.5rem;
        font-weight: 900;
        color: #FFFFFF;
        line-height: 1;
    }
    .hero-km-total {
        font-size: 1.2rem;
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
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 16px;
        padding: 12px 14px;
        box-shadow: 0 6px 16px -4px rgba(148, 163, 184, 0.15);
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
    url = f"https://intervals.icu/api/v1/athlete/{ATHLETE_ID}/activities?oldest={start_date}"
    
    response = requests.get(url, auth=("API_KEY", API_KEY))
    if response.status_code == 200:
        return response.json()
    return []

activities = fetch_running_data()

# 4. 데이터 전처리
running_records = []
if activities:
    for act in activities:
        if act.get("type") == "Run":
            distance_km = round(act.get("distance", 0) / 1000, 2)
            start_date_local = act.get("start_date_local", "")[:10]
            running_records.append({
                "Date": start_date_local,
                "Distance": distance_km
            })

df = pd.DataFrame(running_records)

# 날짜 및 목표 계산
now = datetime.now()
days_in_month = calendar.monthrange(now.year, now.month)[1]
current_day = now.day
remaining_days = max(1, days_in_month - current_day + 1)

GOAL_KM = 200.0

# 상단 헤더
st.markdown(f'''
    <div class="crew-header">
        <div class="crew-title">이실권 200CREW</div>
        <div class="crew-subtitle">📅 {now.strftime("%Y.%m")}</div>
    </div>
''', unsafe_allow_html=True)

if not df.empty:
    total_km = round(df["Distance"].sum(), 1)
    run_count = len(df)
    remaining_km = max(0.0, round(GOAL_KM - total_km, 1))
    progress = min(1.0, total_km / GOAL_KM)
    percent = round(progress * 100, 1)
    
    daily_required_km = round(remaining_km / remaining_days, 1) if remaining_km > 0 else 0.0
    expected_total_km = round((total_km / current_day) * days_in_month, 1)

    # 마스코트 이미지 파일명이 mascot.png 가 아닐 경우 아래 파일 경로를 바꿔주세요
    mascot_path = "mascot.png"

    # 메인 카드 (마스코트 배치)
    col_text, col_img = st.columns([3, 1])
    
    hero_html = f"""
    <div class="hero-card">
        <div class="hero-top">
            <div class="hero-label">MONTHLY GOAL</div>
        </div>
        <div class="hero-main-row">
            <div>
                <span class="hero-km-highlight">{total_km}</span>
                <span class="hero-km-total"> / {int(GOAL_KM)} km</span>
            </div>
            <div class="hero-percent-tag">{percent}%</div>
        </div>
    </div>
    """
    st.markdown(hero_html, unsafe_allow_html=True)

    # 2. 입체 프로그레스 바
    st.progress(progress)
    st.caption(f"🔥 이번 달 총 **{run_count}회** 달리셨어요!")

    st.write("")

    # 3. 서브 카드
    sub_cards_html = f"""
    <div class="grid-container">
        <div class="sub-card">
            <div class="sub-card-header">
                <span class="sub-icon">🎯</span>
                <span class="sub-label">부족분</span>
            </div>
            <div class="sub-value sub-accent">{remaining_km} km</div>
        </div>
        <div class="sub-card">
            <div class="sub-card-header">
                <span class="sub-icon">⚡</span>
                <span class="sub-label">하루 필요</span>
            </div>
            <div
