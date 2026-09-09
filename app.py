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

# 입체적 글래스모피즘 & 3D 런너 커스텀 CSS
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

    /* 3D 히어로 카드 (깊이감 있는 입체 입체 그라데이션 + 귀여운 캐릭터) */
    .hero-card {
        background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
        border-radius: 22px;
        padding: 22px 20px;
        color: #FFFFFF;
        box-shadow: 0 12px 28px -6px rgba(15, 23, 42, 0.35), inset 0 1px 1px rgba(255, 255, 255, 0.15);
        margin-bottom: 16px;
        position: relative;
        overflow: hidden;
    }
    
    /* 입체 아우라 배경 이펙트 */
    .hero-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -30%;
        width: 180px;
        height: 180px;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.25) 0%, rgba(0,0,0,0) 70%);
        border-radius: 50%;
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
    .hero-avatar {
        font-size: 1.8rem;
        filter: drop-shadow(0 4px 6px rgba(0,0,0,0.3));
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
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
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

    /* 입체 입체 서브 카드 (3D 입체 그림자 적용) */
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
        transition: transform 0.2s;
    }
    .sub-card-header {
        display: flex;
        align-items: center;
        gap: 4px;
        margin-bottom: 4px;
    }
    .sub-icon {
        font-size: 0.9rem;
    }
    .sub-label {
        font-size: 0.73rem;
        color: #64748B;
        font-weight: 700;
    }
    .sub-value {
        font-size: 1.15rem;
        font-weight: 900;
        color: #0F172A;
    }
    .sub-accent {
        color: #0284C7;
    }

    /* 입체 프로그레스 바 */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #38BDF8 0%, #0284C7 100%);
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(2, 132, 199, 0.3);
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
        <div class="crew-title">🏃‍♂️ 이실권 200CREW</div>
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

    # 1. 3D 입체 히어로 카드 (귀여운 3D 런너 캐릭터 연출)
    hero_html = f"""
    <div class="hero-card">
        <div class="hero-top">
            <div class="hero-label">MONTHLY GOAL</div>
            <div class="hero-avatar">🏃💨</div>
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

    # 3. 귀여운 아이콘이 들어간 입체 서브 카드
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
            <div class="sub-value">{daily_required_km} km</div>
        </div>
        <div class="sub-card">
            <div class="sub-card-header">
                <span class="sub-icon">⏳</span>
                <span class="sub-label">남은 기간</span>
            </div>
            <div class="sub-value">{remaining_days} 일</div>
        </div>
        <div class="sub-card">
            <div class="sub-card-header">
                <span class="sub-icon">📈</span>
                <span class="sub-label">월 예상</span>
            </div>
            <div class="sub-value">{expected_total_km} km</div>
        </div>
    </div>
    """
    st.markdown(sub_cards_html, unsafe_allow_html=True)

    # 4. 차분하고 은은한 미니 일별 그래프
    st.markdown("<p style='font-size:0.82rem; font-weight:800; color:#334155; margin-bottom:6px;'>📊 일별 참고 기록 (km)</p>", unsafe_allow_html=True)
    
    daily_df = df.groupby("Date", as_index=False)["Distance"].sum()

    fig = px.bar(
        daily_df,
        x="Date",
        y="Distance",
        text_auto=".1f"
    )
    
    fig.update_traces(
        marker_color="#0284C7", # 고급스러운 밝은 아쿠아 블루
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
        yaxis=dict(fixedrange=True, showgrid=True, gridcolor="#F1F5F9", tickfont=dict(size=9, color="#64748B")),
        font=dict(size=10, color="#475569")
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'scrollZoom': False, 'staticPlot': True})

else:
    st.info("이번 달 등록된 러닝 기록이 없습니다.")
