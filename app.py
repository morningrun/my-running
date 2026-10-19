import base64
import calendar
from datetime import datetime
import os
from zoneinfo import ZoneInfo
import plotly.express as px
import pandas as pd
import requests
import streamlit as st

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

mascot_b64 = get_base64("mascot.png")

st.set_page_config(
    page_title="이실권 200CREW",
    page_icon="🏃",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

.crew-title, .crew-subtitle, .hero-card, .sub-card, .custom-table, .stMarkdown p { 
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif !important; 
}

header { visibility: hidden; }
.stApp { background-color: #F8FAFC; }
.block-container { padding-top: 0.8rem !important; padding-bottom: 1.5rem !important; padding-left: 0.8rem !important; padding-right: 0.8rem !important; }

.crew-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; padding: 0 4px; }
.crew-title { font-size: 1.45rem !important; font-weight: 900; letter-spacing: -0.6px; background: linear-gradient(135deg, #0F172A 0%, #0284C7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; white-space: nowrap; }
.crew-subtitle { font-size: 0.75rem; color: #64748B; font-weight: 600; background: #FFFFFF; border: 1px solid #E2E8F0; padding: 4px 10px; border-radius: 12px; display: flex; align-items: center; gap: 5px; white-space: nowrap; }

.hero-card { background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%); border-radius: 22px; padding: 20px 22px; color: #FFFFFF; box-shadow: 0 12px 28px -6px rgba(15, 23, 42, 0.25); margin-bottom: 16px; }
.hero-top-row { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding-bottom: 12px; margin-bottom: 14px; }
.hero-goal-title { font-size: 0.95rem; color: #94A3B8; font-weight: 700; letter-spacing: 0.3px; }
.hero-goal-target { font-size: 1.45rem !important; color: #38BDF8; font-weight: 900; }
.hero-bottom-row { display: flex; align-items: center; justify-content: space-between; }
.hero-km-highlight { font-size: 2.3rem; font-weight: 900; color: #FFFFFF !important; line-height: 1; }
.hero-km-label { font-size: 1rem; font-weight: 600; color: #94A3B8 !important; margin-left: 2px; }
.hero-percent-tag { background: linear-gradient(135deg, #38BDF8 0%, #0284C7 100%); color: #FFFFFF; padding: 6px 14px; border-radius: 20px; font-size: 0.95rem; font-weight: 800; box-shadow: 0 4px 12px rgba(56, 189, 248, 0.35); display: inline-block; text-align: center; }

.progress-wrapper { margin-top: 26px; margin-bottom: 12px; padding-top: 18px; }
.custom-progress-container { position: relative; width: 100%; background-color: #E2E8F0; border-radius: 10px; height: 12px; }
.custom-progress-bar { height: 100%; background: linear-gradient(90deg, #38BDF8 0%, #0284C7 100%); border-radius: 10px; }
.custom-progress-badge { position: absolute; top: -22px; transform: translateX(-50%); background: #0284C7; color: #FFFFFF; font-size: 0.68rem; font-weight: 800; padding: 1px 6px; border-radius: 6px; white-space: nowrap; box-shadow: 0 2px 6px rgba(2, 132, 199, 0.3); }

.grid-container { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 16px; }
.sub-card { background: #FFFFFF; border: 1px solid rgba(226, 232, 240, 0.9); border-radius: 16px; padding: 12px 14px; box-shadow: 0 4px 12px -2px rgba(148, 163, 184, 0.1); }
.sub-card-header { display: flex; align-items: center; gap: 4px; margin-bottom: 4px; }
.sub-icon { font-size: 0.9rem; }
.sub-label { font-size: 0.73rem; color: #64748B; font-weight: 700; }
.sub-value { font-size: 1.1rem; font-weight: 900; color: #0F172A; }
.sub-value-large { font-size: 1.45rem !important; font-weight: 900; color: #0F172A; }
.sub-accent { color: #0284C7; }
.sub-accent-red { color: #E11D48; }

div[data-testid="stExpander"] { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; margin-bottom: 14px; box-shadow: 0 4px 12px -2px rgba(148, 163, 184, 0.08); overflow: hidden; }
div[data-testid="stExpander"] summary { font-weight: 900 !important; color: #0F172A !important; font-size: 1.05rem !important; font-family: 'Pretendard', sans-serif !important; }

.custom-table { width: 100%; border-collapse: collapse; background-color: #FFFFFF; border-radius: 10px; overflow: hidden; border: 1px solid #E2E8F0; font-size: 0.85rem; }
.custom-table th { background-color: #F1F5F9; color: #0F172A; font-weight: 700; text-align: center; padding: 7px 6px; border-bottom: 1px solid #E2E8F0; line-height: 1.3; }
.custom-table td { text-align: center; padding: 7px 6px; color: #334155; border-bottom: 1px solid #F1F5F9; line-height: 1.3; }
.custom-table tr:last-child td { border-bottom: none; }
</style>
""", unsafe_allow_html=True)

MASTER_API_KEY = st.secrets["INTERVALS_API_KEY"]
CREW_MEMBERS = {"이실권": st.secrets["INTERVALS_ATHLETE_ID"]}

st.sidebar.markdown("## 🏃‍♂️ 200CREW 멤버 선택")
selected_member = st.sidebar.selectbox("크루원을 선택하세요", list(CREW_MEMBERS.keys()))
ATHLETE_ID = CREW_MEMBERS[selected_member]

KST = ZoneInfo("Asia/Seoul")
now = datetime.now(KST)

@st.cache_data(ttl=300)
def fetch_data(athlete_id, api_key, start_date):
    url = f"https://intervals.icu/api/v1/athlete/{athlete_id}/activities?oldest={start_date}"
    res = requests.get(url, auth=("API_KEY", api_key))
    return res.json() if res.status_code == 200 else []

activities = fetch_data(ATHLETE_ID, MASTER_API_KEY, f"{now.year - 2}-01-01")

records = []
if activities:
    for act in activities:
        if act.get("type") == "Run":
            dist = round(act.get("distance", 0) / 1000, 2)
            date_str = act.get("start_date_local", "")[:10]
            records.append({"Date": date_str, "Distance": dist})

df_all = pd.DataFrame(records)
if not df_all.empty:
    df_all["Month"] = df_all["Date"].str[:7]

current_day = now.day
today_str = now.strftime("%Y-%m-%d")
week_days = ['월', '화', '수', '목', '금', '토', '일']
date_text = f"{now.year}.{now.month:02d}.{current_day:02d} ({week_days[now.weekday()]})"

st.markdown(f"""
<div class="crew-header">
    <div class="crew-title">이실권 200CREW</div>
    <div class="crew-subtitle"><span>🗓️</span> {date_text}</div>
</div>
""", unsafe_allow_html=True)

curr_month_str = now.strftime("%Y-%m")
df_current = df_all[df_all["Month"] == curr_month_str] if not df_all.empty else pd.DataFrame()

days_in_month = calendar.monthrange(now.year, now.month)[1]
remaining_days = max(1, days_in_month - current_day + 1)
GOAL_KM = 200.0

if not df_current.empty:
    total_km = round(df_current["Distance"].sum(), 2)
    run_count = len(df_current)
    remaining_km = max(0.0, round(GOAL_KM - total_km, 2))
    df_today = df_current[df_current["Date"] == today_str]
    today_km = round(df_today["Distance"].sum(), 2) if not df_today.empty else 0.0
    progress = total_km / GOAL_KM
    percent = round(progress * 100, 1)
    expected_total_km = round((total_km / current_day) * days_in_month, 2)
else:
    total_km, run_count, remaining_km, today_km, progress, percent = 0.0, 0, GOAL_KM, 0.0, 0.0, 0.0
    expected_total_km = 0.0

mascot_html = f'<img src="data:image/png;base64,{mascot_b64}" style="width: 56px; height: 56px; border-radius: 50%; border: 2px solid #38BDF8; object-fit: contain; background-color: #FFFFFF; padding: 3px; display: block; margin-left: auto;">' if mascot_b64 else '<span style="font-size: 1.8rem; display: block; text-align: right;">🏃💨</span>'

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

bar_width = min(100.0, percent)
st.markdown(f"""
<div class="progress-wrapper">
    <div class="custom-progress-container">
        <div class="custom-progress-bar" style="width: {bar_width}%;"></div>
        <div class="custom-progress-badge" style="left: {bar_width}%;">{percent}%</div>
    </div>
</div>
""", unsafe_allow_html=True)

msg = f"🔥 목표 달성 완료! 현재 {percent}% 달성 중 (총 {run_count}회)" if progress > 1.0 else f"🔥 이번 달 총 {run_count}회 달리셨어요!"
st.markdown(f"<p style='font-size:0.85rem; font-weight:800; color:#0F172A; margin-top:4px;'>{msg}</p>", unsafe_allow_html=True)
st.write("")

st.markdown(f"""
<div class="grid-container">
    <div class="sub-card">
        <div class="sub-card-header"><span class="sub-icon">🏅</span><span class="sub-label">오늘 운동 거리</span></div>
        <div class="sub-value sub-value-large sub-accent">{today_km:.2f} km</div>
    </div>
    <div class="sub-card">
        <div class="sub-card-header"><span class="sub-icon">🎯</span><span class="sub-label">남은 거리</span></div>
        <div class="sub-value sub-value-large sub-accent-red">{remaining_km:.2f} km</div>
    </div>
    <div class="sub-card">
        <div class="sub-card-header"><span class="sub-icon">⏳</span><span class="sub-label">남은 기간</span></div>
        <div class="sub-value sub-value-large">{remaining_days} 일</div>
    </div>
    <div class="sub-card">
        <div class="sub-card-header"><span class="sub-icon">📈</span><span class="sub-label">월 예상 거리</span></div>
        <div class="sub-value sub-value-large">{expected_total_km:.2f} km</div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.expander(f"{now.month}월 운동 현황", expanded=True):
    _, last_day = calendar.monthrange(now.year, now.month)
    full_dates = pd.DataFrame({"Date": [f"{now.year}-{now.month:02d}-{d:02d}" for d in range(1, last_day + 1)]})
    
    if not df_current.empty:
        daily = df_current.groupby("Date", as_index=False)["Distance"].sum()
        merged_curr = pd.merge(full_dates, daily, on="Date", how="left").fillna(0)
    else:
        merged_curr = full_dates
        merged_curr["Distance"] = 0.0

    merged_curr["Date_Label"] = [str(int(d.split("-")[2])) for d in merged_curr["Date"]]
    fig_curr = px.bar(merged_curr, x="Date_Label", y="Distance")
    fig_curr.update_
