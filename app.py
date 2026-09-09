import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import calendar
import os

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="이실권 200CREW",
    page_icon="🏃",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 화면 스타일 CSS
st.markdown("""
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

    .hero-card {
        background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
        border-radius: 22px;
        padding: 20px;
        color: #FFFFFF;
        box-shadow: 0 12px 28px -6px rgba(15, 23, 42, 0.25);
        margin-bottom: 16px;
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

    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #38BDF8 0%, #0284C7 100%);
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Secrets 수집
API_KEY = st.secrets["INTERVALS_API_KEY"]
ATHLETE_ID = st.secrets["INTERVALS_ATHLETE_ID"]

# 4. 데이터 로딩
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

# 5. 데이터 전처리
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

# 상단 헤더 출력
header_html = """
    <div class="crew-header">
        <div class="crew-title">이실권 200CREW</div>
        <div class="crew-subtitle">📅 {date_str}</div>
    </div>
""".format(date_str=now.strftime("%Y.%m"))
st.markdown(header_html, unsafe_allow_html=True)

if not df.empty:
    total_km = round(df["Distance"].sum(), 1)
    run_count = len(df)
    remaining_km = max(0.0, round(GOAL_KM - total_km, 1))
    progress = min(1.0, total_km / GOAL_KM)
    percent = round(progress * 100, 1)
    
    daily_required_km = round(remaining_km / remaining_days, 1) if remaining_km > 0 else 0.0
    expected_total_km = round((total_km / current_day) * days_in_month, 1)

    # 1. 메인 히어로 카드 레이아웃 (컬럼 분할로 이미지 안정적 배치)
    hero_card_container = st.container()
    with hero_card_container:
        st.markdown('<div class="hero-card">', unsafe_allow_html=True)
        
        # 카드 내부 상단 행 (라벨과 마스코트 이미지)
        col_top1, col_top2 = st.columns([4, 1])
        with col_top1:
            st.markdown('<div class="hero-label">MONTHLY GOAL</div>', unsafe_allow_html=True)
        with col_top2:
            if os.path.exists("mascot.png"):
                st.image("mascot.png", width=60)
            else:
                st.markdown("🏃💨")
        
        # 카드 내부 메인 행 (총 거리와 퍼센트)
        hero_main_html = """
            <div class="hero-main-row" style="margin-top: 8px;">
                <div>
                    <span class="hero-km-highlight">{total}</span>
                    <span class="hero-km-total"> / {goal} km</span>
                </div>
                <div class="hero-percent-tag">{pct}%</div>
            </div>
        """.format(total=total_km, goal=int(GOAL_KM), pct=percent)
        st.markdown(hero_main_html, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. 프로그레스 바
    st.progress(progress)
    st.caption(f"🔥 이번 달 총 {run_count}회 달리셨어요!")

    st.write("")

    # 3. 서브 카드 출력
    sub_cards_html = """
    <div class="grid-container">
        <div class="sub-card">
            <div class="sub-card-header">
                <span class="sub-icon">🎯</span>
                <span class="sub-label">부족분</span>
            </div>
            <div class="sub-value sub-accent">{rem_km} km</div>
        </div>
        <div class="sub-card">
            <div class="sub-card-header">
                <span class="sub-icon">⚡</span>
                <span class="sub-label">하루 필요</span>
            </div>
            <div class="sub-value">{daily_km} km</div>
        </div>
        <div class="sub-card">
            <div class="sub-card-header">
                <span class="sub-icon">⏳</span>
                <span class="sub-label">남은 기간</span>
            </div>
            <div class="sub-value">{rem_days} 일</div>
        </div>
        <div class="sub-card">
            <div class="sub-card-header">
                <span class="sub-icon">📈</span>
                <span class="sub-label">월 예상</span>
            </div>
            <div class="sub-value">{exp_km} km</div>
        </div>
    </div>
    """.format(
        rem_km=remaining_km,
        daily_km=daily_required_km,
        rem_days=remaining_days,
        exp_km=expected_total_km
    )
    st.markdown(sub_cards_html, unsafe_allow_html=True)

    # 4. 차트
    st.markdown("<p style='font-size:0.82rem; font-weight:800; color:#334155; margin-bottom:6px;'>📊 일별 참고 기록 (km)</p>", unsafe_allow_html=True)
    
    daily_df = df.groupby("Date", as_index=False)["Distance"].sum()

    fig = px.bar(
        daily_df,
        x="Date",
        y="Distance",
        text_auto=".1f"
    )
    
    fig.update_traces(
        marker_color="#0284C7",
        textposition="outside",
        cliponaxis=False,
        hoverinfo="none"
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=15, b=0),
        height=150,
        xaxis_title=None,
        yaxis_title=None,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(fixedrange=True, showgrid=False, tickfont=dict(size=9, color="#64748B")),
        yaxis=dict(fixedrange=True, showgrid=True, gridcolor="#E2E8F0", tickfont=dict(size=9, color="#64748B")),
        font=dict(size=10, color="#475569")
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'scrollZoom': False, 'staticPlot': True})

else:
    st.info("이번 달 등록된 러닝 기록이 없습니다.")
