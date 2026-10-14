import base64
import calendar
from datetime import datetime
import os
from zoneinfo import ZoneInfo
import plotly.express as px
import pandas as pd
import requests
import streamlit as st

# 1. 페이지 설정
st.set_page_config(
    page_title="이실권 200CREW",
    page_icon="🏃",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 스타일 CSS 적용
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    * { font-family: 'Pretendard', sans-serif !important; }
    header { visibility: hidden; }
    .stApp { background-color: #F8FAFC; }
    .block-container { padding: 0.8rem !important; }
    
    .crew-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; padding: 0 4px; }
    .crew-title { font-size: 1.45rem !important; font-weight: 900; background: linear-gradient(135deg, #0F172A 0%, #0284C7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; }
    .crew-subtitle { font-size: 0.75rem; color: #64748B; font-weight: 600; background: #FFFFFF; border: 1px solid #E2E8F0; padding: 4px 10px; border-radius: 12px; }
    
    .hero-card { background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%); border-radius: 22px; padding: 20px 22px; color: #FFFFFF; box-shadow: 0 12px 28px -6px rgba(15, 23, 42, 0.25); margin-bottom: 16px; }
    .hero-top-row { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding-bottom: 12px; margin-bottom: 14px; }
    .hero-goal-title { font-size: 0.95rem; color: #94A3B8; font-weight: 700; }
    .hero-goal-target { font-size: 1.45rem !important; color: #38BDF8; font-weight: 900; }
    .hero-bottom-row { display: flex; align-items: center; justify-content: space-between; }
    .hero-km-highlight { font-size: 2.3rem; font-weight: 900; color: #FFFFFF !important; line-height: 1; }
    .hero-km-label { font-size: 1rem; font-weight: 600; color: #94A3B8 !important; margin-left: 2px; }
    .hero-percent-tag { background: linear-gradient(135deg, #38BDF8 0%, #0284C7 100%); color: #FFFFFF; padding: 6px 14px; border-radius: 20px; font-size: 0.95rem; font-weight: 800; }

    .grid-container { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 16px; }
    .sub-card { background: #FFFFFF; border: 1px solid rgba(226, 232, 240, 0.9); border-radius: 16px; padding: 12px 14px; box-shadow: 0 4px 12px -2px rgba(148, 163, 184, 0.1); }
    .sub-card-header { display: flex; align-items: center; gap: 4px; margin-bottom: 4px; }
    .sub-label { font-size: 0.73rem; color: #64748B; font-weight: 700; }
    .sub-value { font-size: 1.1rem; font-weight: 900; color: #0F172A; }
    .sub-value-large { font-size: 1.45rem !important; font-weight: 900; }
    .sub-accent { color: #0284C7; }

    .custom-table { width: 100%; border-collapse: collapse; background-color: #FFFFFF; border-radius: 10px; overflow: hidden; border: 1px solid #E2E8F0; font-size: 0.85rem; }
    .custom-table th { background-color: #F1F5F9; color: #0F172A; font-weight: 700; text-align: center; padding: 7px 6px; border-bottom: 1px solid #E2E8F0; }
    .custom-table td { text-align: center; padding: 7px 6px; color: #334155; border-bottom: 1px solid #F1F5F9; }
    </style>
""", unsafe_allow_html=True)

# 3. 마스코트 및 비밀키 설정
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

mascot_base64 = get_image_base64("mascot.png")
MASTER_API_KEY = st.secrets.get("INTERVALS_API_KEY", "")
ATHLETE_ID = st.secrets.get("INTERVALS_ATHLETE_ID", "")

st.sidebar.markdown("## 🏃‍♂️ 200CREW 관리")
if st.sidebar.button("🔄 데이터 새로고침"):
    st.cache_data.clear()
    st.rerun()

KST = ZoneInfo("Asia/Seoul")
now = datetime.now(KST)

# 4. 데이터 로딩 함수
@st.cache_data(ttl=300)
def fetch_running_data(athlete_id, api_key, start_date_str):
    if not athlete_id or not api_key:
        return []
    url = f"https://intervals.icu/api/v1/athlete/{athlete_id}/activities?oldest={start_date_str}"
    try:
        res = requests.get(url, auth=("API_KEY", api_key), timeout=10)
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return []

activities = fetch_running_data(ATHLETE_ID, MASTER_API_KEY, f"{now.year - 2}-01-01")

running_records = []
if isinstance(activities, list):
    for act in activities:
        if isinstance(act, dict) and act.get("type") == "Run":
            dist = round(act.get("distance", 0) / 1000, 2)
            date_str = str(act.get("start_date_local", ""))[:10]
            if date_str:
                running_records.append({"Date": date_str, "Distance": dist})

df_all = pd.DataFrame(running_records)
if not df_all.empty:
    df_all["Month"] = df_all["Date"].str[:7]

# 날짜 계산
current_day = now.day
today_str = now.strftime("%Y-%m-%d")
week_days = ['월', '화', '수', '목', '금', '토', '일']
date_text = f"{now.strftime('%Y.%m.%d')} ({week_days[now.weekday()]})"

# 상단 헤더
st.markdown(f"""
    <div class="crew-header">
        <div class="crew-title">이실권 200CREW</div>
        <div class="crew-subtitle">🗓️ {date_text}</div>
    </div>
""", unsafe_allow_html=True)

if not MASTER_API_KEY or not ATHLETE_ID:
    st.warning("⚠️ Streamlit Secrets 설정을 확인해주세요.")

# 이번 달 데이터 계산
current_month_str = now.strftime("%Y-%m")
df_current = df_all[df_all["Month"] == current_month_str] if not df_all.empty else pd.DataFrame()

days_in_month = calendar.monthrange(now.year, now.month)[1]
remaining_days = max(1, days_in_month - current_day + 1)
GOAL_KM = 200.0

if not df_current.empty:
    total_km = round(float(df_current["Distance"].sum()), 2)
    run_count = len(df_current)
    remaining_km = max(0.0, round(GOAL_KM - total_km, 2))
    df_today = df_current[df_current["Date"] == today_str]
    today_km = round(float(df_today["Distance"].sum()), 2) if not df_today.empty else 0.0
    progress = total_km / GOAL_KM
    percent = round(progress * 100, 1)
    expected_total_km = round((total_km / current_day) * days_in_month, 2)
else:
    total_km, run_count, remaining_km, today_km, progress, percent = 0.0, 0, GOAL_KM, 0.0, 0.0, 0.0
    expected_total_km = 0.0

mascot_html = f'<img src="data:image/png;base64,{mascot_base64}" style="width: 56px; height: 56px; border-radius: 50%; border: 2px solid #38BDF8; object-fit: contain; background: #FFF; padding: 3px; display: block; margin-left: auto;">' if mascot_base64 else '🏃💨'

# 히어로 카드
st.markdown(f"""
    <div class="hero-card">
        <div class="hero-top-row">
            <div>
                <span class="hero-goal-title">🎯 {now.strftime('%y년 %m월')} 목표</span>
                <span class="hero-goal-target" style="margin-left: 8px;">{int(GOAL_KM)} km</span>
            </div>
            <div style="width: 56px;">{mascot_html}</div>
        </div>
        <div class="hero-bottom-row">
            <div>
                <span class="hero-km-highlight">{total_km:.2f}</span>
                <span class="hero-km-label">km 달성</span>
            </div>
            <div>
                <span class="hero-percent-tag">{percent}%</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.progress(min(1.0, float(progress)))
st.markdown(f"<p style='font-size:0.85rem; font-weight:800; color:#0F172A; margin-top:4px;'>🔥 이번 달 총 {run_count}회 달리셨어요!</p>", unsafe_allow_html=True)
st.write("")

# 서브 카드
st.markdown(f"""
<div class="grid-container">
    <div class="sub-card">
        <div class="sub-card-header"><span class="sub-label">🏅 오늘 운동 거리</span></div>
        <div class="sub-value sub-value-large sub-accent">{today_km:.2f} km</div>
    </div>
    <div class="sub-card">
        <div class="sub-card-header"><span class="sub-label">🎯 남은 거리</span></div>
        <div class="sub-value sub-value-large">{remaining_km:.2f} km</div>
