import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. 페이지 기본 설정 및 모바일 CSS 적용
st.set_page_config(
    page_title="Monthly Running",
    page_icon="🏃",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 모바일 화면 맞춤 커스텀 CSS
st.markdown("""
    <style>
    /* 상단 기본 헤더 및 여백 줄이기 */
    header {visibility: hidden;}
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }
    
    /* 제목 스타일 모바일 맞춤 축소 */
    .mobile-title {
        font-size: 1.3rem !important;
        font-weight: 800;
        margin-bottom: 2px;
        color: #111;
    }
    .mobile-sub {
        font-size: 0.8rem;
        color: #666;
        margin-bottom: 12px;
    }
    
    /* 가로 3분할 카드 스타일 */
    .card-container {
        display: flex;
        justify-content: space-between;
        gap: 6px;
        margin-bottom: 12px;
    }
    .card-box {
        flex: 1;
        background-color: #F8F9FA;
        border: 1px solid #E9ECEF;
        border-radius: 10px;
        padding: 10px 4px;
        text-align: center;
    }
    .card-title {
        font-size: 0.72rem;
        color: #6C757D;
        font-weight: 600;
        margin-bottom: 2px;
    }
    .card-num {
        font-size: 1.15rem;
        color: #111;
        font-weight: 700;
    }
    .card-unit {
        font-size: 0.75rem;
        font-weight: 400;
        color: #555;
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

# 5. 화면 출력
st.markdown('<div class="mobile-title">🏃 월간 러닝 대시보드</div>', unsafe_allow_html=True)
st.markdown(f'<div class="mobile-sub">📅 {datetime.now().strftime("%Y년 %m월")} 현황</div>', unsafe_allow_html=True)

GOAL_KM = 200.0

if not df.empty:
    total_km = round(df["Distance"].sum(), 1)
    run_count = len(df)
    remaining_km = max(0.0, round(GOAL_KM - total_km, 1))
    progress = min(1.0, total_km / GOAL_KM)
    percent = int(progress * 100)

    # 가로 3열 카드 직접 배치 (HTML/CSS)
    cards_html = f"""
    <div class="card-container">
        <div class="card-box">
            <div class="card-title">누적 거리</div>
            <div class="card-num">{total_km}<span class="card-unit"> km</span></div>
        </div>
        <div class="card-box">
            <div class="card-title">달성률</div>
            <div class="card-num">{percent}<span class="card-unit"> %</span></div>
        </div>
        <div class="card-box">
            <div class="card-title">남은 거리</div>
            <div class="card-num">{remaining_km}<span class="card-unit"> km</span></div>
        </div>
    </div>
    """
    st.markdown(cards_html, unsafe_allow_html=True)

    # 진행률 프로그레스 바
    st.progress(progress)
    st.caption(f"목표 200km 중 {total_km}km 달성 (총 {run_count}회 러닝)")

    # 일자별 차트
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
        cliponaxis=False
    )
    
    fig.update_layout(
        title=dict(text="<b>일별 러닝 (km)</b>", font=dict(size=14)),
        margin=dict(l=5, r=5, t=30, b=5),
        height=260,
        xaxis_title=None,
        yaxis_title=None,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=True, gridcolor="#F0F2F6")
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

else:
    st.info("이번 달 러닝 데이터가 없습니다.")
