import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import calendar

# 1. 페이지 기본 설정 (모바일 최적화)
st.set_page_config(
    page_title="200CREW Dashboard",
    page_icon="🏃",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 고급 모바일 UI 디자인 커스텀 CSS (모던 인디고 & 프리미엄 카드)
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
        align-items: flex-end;
        margin-bottom: 12px;
    }
    .crew-title {
        font-size: 1.6rem !important;
        font-weight: 900;
        letter-spacing: -0.5px;
        color: #1A1D20;
        margin: 0;
        line-height: 1.0;
    }
    .crew-subtitle {
        font-size: 0.75rem;
        color: #6C757D;
        font-weight: 500;
    }

    /* 메인 히어로 카드 (고급 다크 스레이트 & 모던 그라데이션) */
    .hero-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border-radius: 18px;
        padding: 20px 18px;
        color: #FFFFFF;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.15);
        margin-bottom: 14px;
    }
    .hero-label {
        font-size: 0.78rem;
        color: #94A3B8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .hero-main-row {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        margin-top: 6px;
        margin-bottom: 12px;
    }
    .hero-km-highlight {
        font-size: 2.3rem;
        font-weight: 900;
        color: #38BDF8; /* 세련된 인디고/블루 포인트 */
        line-height: 1;
    }
    .hero-km-total {
        font-size: 1.2rem;
        font-weight: 600;
        color: #94A3B8;
    }
    .hero-percent-tag {
        background-color: rgba(56, 189, 248, 0.15);
        color: #38BDF8;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
    }

    /* 상세 지표 2x2 카드 (차분한 아이보리/그레이 톤) */
    .grid-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
        margin-bottom: 14px;
    }
    .sub-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 12px 14px;
    }
    .sub-label {
        font-size: 0.72rem;
        color: #64748B;
        font-weight: 600;
        margin-bottom: 3px;
    }
    .sub-value {
        font-size: 1.1rem;
        font-weight: 800;
        color: #0F172A;
    }
    .sub-accent {
        color: #0EA5E9;
    }

    /* 프로그레스 바 커스텀 */
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
        <div class="crew-title">200CREW</div>
        <div class="crew-subtitle">📅 {now.strftime("%Y.%m")} Target</div>
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

    # 1. 메인 200km 히어로 카드 (달성도 & 현재 거리 최우선 강조)
    hero_html = f"""
    <div class="hero-card">
        <div class="hero-label">CURRENT PROGRESS</div>
        <div class="hero-main-row">
            <div>
                <span class="hero-km-highlight">{total_km}</span>
                <span class="hero-km-total"> / {int(GOAL_KM)} km</span>
            </div>
            <div class="hero-percent-tag">{percent}% 완료</div>
        </div>
    </div>
    """
    st.markdown(hero_html, unsafe_allow_html=True)

    # 2. 프로그레스 바
    st.progress(progress)
    st.caption(f"총 **{run_count}회** 러닝 진행 중")

    st.write("")

    # 3. 고급스러운 2x2 상세 지표 카드
    sub_cards_html = f"""
    <div class="grid-container">
        <div class="sub-card">
            <div class="sub-label">부족분 (남은 거리)</div>
            <div class="sub-value sub-accent">{remaining_km} km</div>
        </div>
        <div class="sub-card">
            <div class="sub-label">하루 필요 거리</div>
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

    # 4. 차분한 톤의 고정형 일별 참고 차트
    st.markdown("<p style='font-size:0.8rem; font-weight:700; color:#475569; margin-bottom:4px;'>📊 일별 러닝 기록 (km)</p>", unsafe_allow_html=True)
    
    daily_df = df.groupby("Date", as_index=False)["Distance"].sum()

    fig = px.bar(
        daily_df,
        x="Date",
        y="Distance",
        text_auto=".1f"
    )
    
    fig.update_traces(
        marker_color="#64748B", # 차분한 딥 그레이/슬레이트
        textposition="outside",
        cliponaxis=False,
        hoverinfo="none"
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=15, b=0),
        height=160,
        xaxis_title=None,
        yaxis_title=None,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(fixedrange=True, showgrid=False, tickfont=dict(size=9, color="#94A3B8")),
        yaxis=dict(fixedrange=True, showgrid=True, gridcolor="#F1F5F9", tickfont=dict(size=9, color="#94A3B8")),
        font=dict(size=10, color="#64748B")
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'scrollZoom': False, 'staticPlot': True})

else:
    st.info("이번 달 등록된 러닝 기록이 없습니다.")
