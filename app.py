import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. 페이지 기본 설정 (모바일 최적화)
st.set_page_config(
    page_title="Monthly Running Dashboard",
    page_icon="🏃",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 커스텀 CSS (깔끔한 카드 스타일 및 여백 정리)
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    .metric-card {
        background-color: #F8F9FA;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-title { font-size: 0.85rem; color: #6C757D; font-weight: 600; margin-bottom: 4px; }
    .metric-value { font-size: 1.6rem; color: #212529; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

# 2. Secrets 수집
API_KEY = st.secrets["INTERVALS_API_KEY"]
ATHLETE_ID = st.secrets["INTERVALS_ATHLETE_ID"]

# 3. 데이터 로딩 함수
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

# 4. 러닝 데이터 전처리
running_records = []
if activities:
    for act in activities:
        if act.get("type") == "Run":
            distance_km = round(act.get("distance", 0) / 1000, 2)
            start_date_local = act.get("start_date_local", "")[:10]
            moving_time_min = round(act.get("moving_time", 0) / 60, 1)
            running_records.append({
                "Date": start_date_local,
                "Distance": distance_km,
                "Time": moving_time_min
            })

df = pd.DataFrame(running_records)

# 5. 메인 대시보드 화면 구성
st.title("🏃 월간 러닝 대시보드")
st.caption(f"📅 {datetime.now().strftime('%Y년 %m월')} 진행 상황")

GOAL_KM = 200.0

if not df.empty:
    total_km = round(df["Distance"].sum(), 1)
    run_count = len(df)
    remaining_km = max(0.0, round(GOAL_KM - total_km, 1))
    progress = min(1.0, total_km / GOAL_KM)

    # 상단 메트릭 카드 3개 배치
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-title">누적 거리</div><div class="metric-value">{total_km}<span style="font-size:1rem;"> km</span></div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-title">달성률</div><div class="metric-value">{int(progress * 100)}<span style="font-size:1rem;"> %</span></div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-title">남은 거리</div><div class="metric-value">{remaining_km}<span style="font-size:1rem;"> km</span></div></div>', unsafe_allow_html=True)

    st.write("")
    
    # 진행률 프로그레스 바
    st.progress(progress)
    st.caption(f"목표 200km 중 **{total_km}km** 완료 (총 {run_count}회 러닝)")

    st.divider()

    # 일자별 거리 차트 (Plotly 사용)
    st.subheader("📊 일별 러닝 기록")
    daily_df = df.groupby("Date", as_index=False)["Distance"].sum()

    fig = px.bar(
        daily_df,
        x="Date",
        y="Distance",
        labels={"Date": "날짜", "Distance": "거리 (km)"},
        text_auto=".1f"
    )
    
    fig.update_traces(
        marker_color="#FF4B4B",
        textposition="outside",
        cliponaxis=False
    )
    
    fig.update_layout(
        xaxis_title=None,
        yaxis_title="km",
        margin=dict(l=10, r=10, t=20, b=10),
        height=300,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=True, gridcolor="#F0F2F6")
    )
    
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("이번 달 등록된 러닝 데이터가 없습니다.")
