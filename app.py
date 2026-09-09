import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import calendar

# 1. 페이지 기본 설정 (모바일 최적화 및 상단 여백 최소화)
st.set_page_config(
    page_title="200CREW Dashboard",
    page_icon="🏃",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 모바일 전용 커스텀 CSS (카드 디자인, 폰트, 여백 최적화)
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
    
    /* 헤더 스타일 */
    .crew-title {
        font-size: 1.8rem !important;
        font-weight: 900;
        letter-spacing: -0.5px;
        color: #111;
        margin-bottom: 0px;
        line-height: 1.1;
    }
    .crew-subtitle {
        font-size: 0.8rem;
        color: #666;
        font-weight: 500;
        margin-bottom: 14px;
    }

    /* 메인 히어로 카드 (200km 목표 중심) */
    .hero-card {
        background: linear-gradient(135deg, #FF4B4B 0%, #FF2E2E 100%);
        border-radius: 16px;
        padding: 16px 18px;
        color: white;
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.25);
        margin-bottom: 12px;
    }
    .hero-label {
        font-size: 0.8rem;
        opacity: 0.9;
        font-weight: 600;
    }
    .hero-main {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        margin: 6px 0 10px 0;
    }
    .hero-percent {
        font-size: 2.6rem;
        font-weight: 900;
        line-height: 1;
    }
    .hero-km {
        font-size: 1.1rem;
        font-weight: 600;
        opacity: 0.95;
    }

    /* 서브 정보 grid */
    .grid-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
        margin-bottom: 12px;
    }
    .sub-card {
        background-color: #F8F9FA;
        border: 1px solid #E9ECEF;
        border-radius: 12px;
        padding: 10px 12px;
    }
    .sub-label {
        font-size: 0.72rem;
        color: #6C757D;
        font-weight: 600;
        margin-bottom: 2px;
    }
    .sub-value {
        font-size: 1.15rem;
        font-weight: 800;
        color: #212529;
    }
    .sub-highlight {
        color: #FF4B4B;
    }

    /* 프로그레스 바 영역 */
    .stProgress > div > div > div > div {
        background-color: #FF4B4B;
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

# 타이틀 헤더
st.markdown('<div class="crew-title">🏃 200CREW</div>', unsafe_allow_html=True)
st.markdown(f'<div class="crew-subtitle">📅 {now.strftime("%Y년 %m월")} 목표 달성 프로젝트</div>', unsafe_allow_html=True)

if not df.empty:
    total_km = round(df["Distance"].sum(), 1)
    run_count = len(df)
    remaining_km = max(0.0, round(GOAL_KM - total_km, 1))
    progress = min(1.0, total_km / GOAL_KM)
    percent = round(progress * 100, 1)
    
    # 일평균 필요 거리 계산
    daily_required_km = round(remaining_km / remaining_days, 1) if remaining_km > 0 else 0.0
    
    # 현재 페이스 기준 월 예상 누적 거리
    expected_total_km = round((total_km / current_day) * days_in_month, 1)

    # 1. 메인 200km 히어로 카드
    hero_html = f"""
    <div class="hero-card">
        <div class="hero-label">월간 200km 달성률</div>
        <div class="hero-main">
            <div class="hero-percent">{percent}%</div>
            <div class="hero-km">{total_km} / {int(GOAL_KM)} km</div>
        </div>
    </div>
    """
    st.markdown(hero_html, unsafe_allow_html=True)

    # 2. 프로그레스 바
    st.progress(progress)
    st.caption(f"🎯 목표 200km 중 **{total_km}km** 달성 (총 {run_count}회 러닝)")

    st.write("")

    # 3. 상세 지표 2x2 카드
    sub_cards_html = f"""
    <div class="grid-container">
        <div class="sub-card">
            <div class="sub-label">부족분 (남은 거리)</div>
            <div class="sub-value sub-highlight">{remaining_km} km</div>
        </div>
        <div class="sub-card">
            <div class="sub-label">남은 하루 필요 거리</div>
            <div class="sub-value">{daily_required_km} km/일</div>
        </div>
        <div class="sub-card">
            <div class="sub-label">남은 기간</div>
            <div class="sub-value">{remaining_days} 일</div>
        </div>
        <div class="sub-card">
            <div class="sub-label">월 예상 누적</div>
            <div class="sub-value">{expected_total_km} km</div>
        </div>
    </div>
    """
    st.markdown(sub_cards_html, unsafe_allow_html=True)

    st.divider()

    # 4. 고정형 소형 참고용 차트 (터치 시 흔들림/확대 방지 설정 적용)
    st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#333; margin-bottom:4px;'>📊 일별 참고 기록 (km)</p>", unsafe_allow_html=True)
    
    daily_df = df.groupby("Date", as_index=False)["Distance"].sum()

    fig = px.bar(
        daily_df,
        x="Date",
        y="Distance",
        text_auto=".1f"
    )
    
    fig.update_traces(
        marker_color="#FF4B4B",
        textposition="outside",
        cliponaxis=False,
        hoverinfo="none" # 터치 반응 최소화
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=15, b=0),
        height=180, # 차트 크기 축소 (컴팩트)
        xaxis_title=None,
        yaxis_title=None,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(fixedrange=True, showgrid=False), # 확대/이동 고정
        yaxis=dict(fixedrange=True, showgrid=True, gridcolor="#F0F2F6"), # 확대/이동 고정
        font=dict(size=10)
    )
    
    # Streamlit 터치/이동 툴바 제거 (static plot 모드)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'scrollZoom': False, 'staticPlot': True})

else:
    st.info("이번 달 등록된 러닝 기록이 없습니다.")
