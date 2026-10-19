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

st.set_page_config(page_title="이실권 200CREW", page_icon="🏃", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

/* 스트림릿 익스팬더 내부 아이콘 영역을 제외한 곳에만 Pretendard 적용 */
.crew-title, .crew-subtitle, .hero-card, .sub-card, .custom-table, .stMarkdown p { 
    font-family: 'Pretendard', sans-serif !important; 
}

header { visibility: hidden; }
.stApp { background-color: #F8FAFC; }
.block-container { padding: 0.8rem !important; }
.crew-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; padding: 0 4px; }
.crew-title { font-size: 1.45rem !important; font-weight: 900; background: linear-gradient(135deg, #0F172A 0%, #0284C7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; }
.crew-subtitle { font-size: 0.75rem; color: #64748B; font-weight: 600; background: #FFFFFF; border: 1px solid #E2E8F0; padding: 4px 10px; border-radius: 12px; display: flex; align-items: center; gap: 5px; }
.hero-card { background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%); border-radius: 22px; padding: 20px 22px; color: #FFFFFF; box-shadow: 0 12px 28px -6px rgba(15, 23, 42, 0.25); margin-bottom: 16px; }
.hero-top-row { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding-bottom: 12px; margin-bottom: 14px; }
.hero-goal-title { font-size: 0.95rem; color: #94A3B8; font-weight: 700; }
.hero-goal-target { font-size: 1.45rem !important; color: #38BDF8; font-weight: 900; }
.hero-bottom-row { display: flex; align-items: center; justify-content: space-between; }
.hero-km-highlight { font-size: 2.3rem; font-weight: 900; color: #FFFFFF !important; line-height: 1; }
.hero-km-label { font-size: 1rem; font-weight: 600; color: #94A3B8 !important; margin-left: 2px; }
.hero-percent-tag { background: linear-gradient(135deg, #38BDF8 0%, #0284C7 100%); color: #FFFFFF; padding: 6px 14px; border-radius: 20px; font-size: 0.95rem; font-weight: 800; }
.progress-wrapper { margin-top: 26px; margin-bottom: 12px; padding-top: 18px; }
.custom-progress-container { position: relative; width: 100%; background-color: #E2E8F0; border-radius: 10px; height: 12px; }
.custom-progress-bar { height: 100%; background: linear-gradient(90deg, #38BDF8 0%, #0284C7 100%); border-radius: 10px; }
.custom-progress-badge { position: absolute; top: -22px; transform: translateX(-50%); background: #0284C7; color: #FFFFFF; font-size: 0.68rem; font-weight: 800; padding: 1px 6px; border-radius: 6px; white-space: nowrap; }
.grid-container { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 16px; }
.sub-card { background: #FFFFFF; border: 1px solid rgba(226, 232, 240, 0.9); border-radius: 16px; padding: 12px 14px; box-shadow: 0 4px 12px -2px rgba(148, 163, 184, 0.1); }
.sub-card-header { display: flex; align-items: center; gap: 4px; margin-bottom: 4px; }
.sub-icon { font-size: 0.9rem; }
.sub-label { font-size: 0.73rem; color: #64748B; font-weight: 700; }
.sub-value { font-size: 1.1rem; font-weight: 900; color: #0F172A; }
.sub-value-large { font-size: 1.45rem !important; font-weight: 900; color: #0F172A; }
.sub-accent { color: #0284C7; }
.sub-accent-red { color: #E11D48; }

/* 스트림릿 기본 익스팬더 디자인 및 굵은 제목 설정 */
div[data-testid="stExpander"] { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; margin-bottom: 14px; box-shadow: 0 4px 12px -2px rgba(148, 163, 184, 0.08); overflow: hidden; }
div[data-testid="stExpander"] summary { font-weight: 900 !important; color: #0F172A !important; font-size: 1.05rem !important; font-family: 'Pretendard', sans-serif !important; }

.custom-table { width: 100%; border-collapse: collapse; background-color: #FFFFFF; border-radius: 10px; overflow: hidden; border: 1px solid #E2E8F0; font-size: 0.85rem; font-weight: normal !important; }
.custom-table th { background-color: #F1F5F9; color: #0F172A; font-weight: 700; text-align: center; padding: 7px 6px; border-bottom: 1px solid #E2E8F0; }
.custom-table td { text-align: center; padding: 7px 6px; color: #334155; border-bottom: 1px solid #F1F5F9; font-weight: normal !important; }
</style>
""", unsafe_allow_html=True)

API_KEY = st.secrets["INTERVALS_API_KEY"]
ATHLETE_ID = st.secrets["INTERVALS_ATHLETE_ID"]
KST = ZoneInfo("Asia/Seoul")
now = datetime.now(KST)

@st.cache_data(ttl=300)
def fetch_data(a_id, key, start):
    url = f"https://intervals.icu/api/v1/athlete/{a_id}/activities?oldest={start}"
    res = requests.get(url, auth=("API_KEY", key))
    return res.json() if res.status_code == 200 else []

activities = fetch_data(ATHLETE_ID, API_KEY, f"{now.year - 2}-01-01")
records = [{"Date": a.get("start_date_local", "")[:10], "Distance": round(a.get("distance", 0) / 1000, 2)} for a in activities if a.get("type"] == "Run"]

df_all = pd.DataFrame(records)
if not df_all.empty:
    df_all["Month"] = df_all["Date"].str[:7]

cur_day = now.day
today_str = now.strftime("%Y-%m-%d")
date_text = f"{now.year}.{now.month:02d}.{cur_day:02d} ({['월','화','수','목','금','토','일'][now.weekday()]})"

st.markdown(f'<div class="crew-header"><div class="crew-title">이실권 200CREW</div><div class="crew-subtitle"><span>🗓️</span> {date_text}</div></div>', unsafe_allow_html=True)

cur_m_str = now.strftime("%Y-%m")
df_curr = df_all[df_all["Month"] == cur_m_str] if not df_all.empty else pd.DataFrame()

days_in_m = calendar.monthrange(now.year, now.month)[1]
rem_days = max(1, days_in_m - cur_day + 1)
GOAL_KM = 200.0

if not df_curr.empty:
    tot_km = round(df_curr["Distance"].sum(), 2)
    run_cnt = len(df_curr)
    rem_km = max(0.0, round(GOAL_KM - tot_km, 2))
    today_km = round(df_curr[df_curr["Date"] == today_str]["Distance"].sum(), 2) if not df_curr[df_curr["Date"] == today_str].empty else 0.0
    pct = round((tot_km / GOAL_KM) * 100, 1)
    exp_km = round((tot_km / cur_day) * days_in_m, 2)
else:
    tot_km, run_cnt, rem_km, today_km, pct, exp_km = 0.0, 0, GOAL_KM, 0.0, 0.0, 0.0

mascot_html = f'<img src="data:image/png;base64,{mascot_b64}" style="width: 56px; height: 56px; border-radius
