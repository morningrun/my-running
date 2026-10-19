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
.crew-title, .crew-subtitle, .hero-card, .sub-card, .custom-table, .custom-toggle, .stMarkdown p { font-family: 'Pretendard', sans-serif !important; }
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

.custom-toggle { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; margin-bottom: 14px; padding: 14px 18px; font-weight: 900; font-size: 1.05rem; color: #0F172A; box-shadow: 0 4px 12px -2px rgba(148, 163, 184, 0.08); }
.custom-toggle summary { cursor: pointer; outline: none; list-style: none; display: flex; justify-content: space-between; align-items: center; }
.custom-toggle summary::-webkit-details-marker { display: none; }
.custom-toggle summary::after { content: '▼'; font-size: 0.8rem; color: #64748B; transition: transform 0.2s ease; }
.custom-toggle[open] summary::after { transform: rotate(180deg); }
.custom-toggle-content { margin-top: 14px; padding-top: 12px; border-top: 1px solid #F1F5F9; }

.custom-table { width: 100%; border-collapse: collapse; background-color: #FFFFFF; border-radius: 10px; overflow: hidden; border: 1px solid #E2E8F0; font-size: 0.85rem; }
.custom-table th { background-color: #F1F5F9; color: #0F172A; font-weight: 700; text-align: center; padding: 7px 6px; border-bottom: 1px solid #E2E8F0; }
.custom-table td { text-align: center; padding: 7px 6px; color: #334155; border-bottom: 1px solid #F1F5F9; }
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
records = [{"Date": a.get("start_date_local", "")[:10], "Distance": round(a.get("distance", 0) / 1000, 2)} for a in activities if a.get("type") == "Run"]

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

mascot_html = f'<img src="data:image/png;base64,{mascot_b64}" style="width: 56px; height: 56px; border-radius: 50%; border: 2px solid #38BDF8; object-fit: contain; background: #FFFFFF; padding: 3px; display: block; margin-left: auto;">' if mascot_b64 else '<span style="font-size: 1.8rem; display: block; text-align: right;">🏃💨</span>'

st.markdown(f'''
<div class="hero-card">
    <div class="hero-top-row">
        <div><span class="hero-goal-title">🎯 {now.strftime('%y년 %m월')} 목표</span><span class="hero-goal-target" style="margin-left: 8px;">{int(GOAL_KM)} km</span></div>
        <div style="width: 56px;">{mascot_html}</div>
    </div>
    <div class="hero-bottom-row">
        <div><span class="hero-km-highlight">{tot_km:.2f}</span><span class="hero-km-label">km 달성</span></div>
        <div><span class="hero-percent-tag">{pct}%</span></div>
    </div>
</div>
''', unsafe_allow_html=True)

bar_w = min(100.0, pct)
st.markdown(f'<div class="progress-wrapper"><div class="custom-progress-container"><div class="custom-progress-bar" style="width: {bar_w}%;"></div><div class="custom-progress-badge" style="left: {bar_w}%;">{pct}%</div></div></div>', unsafe_allow_html=True)

msg = f"🔥 목표 달성 완료! 현재 {pct}% 달성 중 (총 {run_cnt}회)" if tot_km >= GOAL_KM else f"🔥 이번 달 총 {run_cnt}회 달리셨어요!"
st.markdown(f"<p style='font-size:0.85rem; font-weight:800; color:#0F172A; margin-top:4px;'>{msg}</p>", unsafe_allow_html=True)
st.write("")

st.markdown(f'''
<div class="grid-container">
    <div class="sub-card"><div class="sub-card-header"><span class="sub-icon">🏅</span><span class="sub-label">오늘 운동 거리</span></div><div class="sub-value sub-value-large sub-accent">{today_km:.2f} km</div></div>
    <div class="sub-card"><div class="sub-card-header"><span class="sub-icon">🎯</span><span class="sub-label">남은 거리</span></div><div class="sub-value sub-value-large sub-accent-red">{rem_km:.2f} km</div></div>
    <div class="sub-card"><div class="sub-card-header"><span class="sub-icon">⏳</span><span class="sub-label">남은 기간</span></div><div class="sub-value sub-value-large">{rem_days} 일</div></div>
    <div class="sub-card"><div class="sub-card-header"><span class="sub-icon">📈</span><span class="sub-label">월 예상 거리</span></div><div class="sub-value sub-value-large">{exp_km:.2f} km</div></div>
</div>
''', unsafe_allow_html=True)

# 1. 이번 달 운동 현황 (기호 이모지 추가)
full_dates = pd.DataFrame({"Date": [f"{now.year}-{now.month:02d}-{d:02d}" for d in range(1, days_in_m + 1)]})
merged_curr = pd.merge(full_dates, df_curr.groupby("Date", as_index=False)["Distance"].sum(), on="Date", how="left").fillna(0) if not df_curr.empty else full_dates.assign(Distance=0.0)
merged_curr["Date_Label"] = [str(int(d.split("-")[2])) for d in merged_curr["Date"]]

fig_c = px.bar(merged_curr, x="Date_Label", y="Distance")
fig_c.update_traces(marker_color="#0284C7", cliponaxis=False, hoverinfo="x+y")
tick_v = [str(d) for d in range(1, days_in_m + 1) if (d - 1) % 3 == 0 or d == days_in_m]
fig_c.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=140, xaxis_title=None, yaxis_title=None, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", xaxis=dict(fixedrange=True, showgrid=False, tickmode="array", tickvals=tick_v, ticktext=tick_v, tickfont=dict(size=10, color="#64748B")), yaxis=dict(fixedrange=True, showgrid=True, gridcolor="#E2E8F0", tickfont=dict(size=10, color="#64748B"), rangemode="tozero"), font=dict(size=10, color="#475569"))

st.markdown(f'''
<details class="custom-toggle" open>
    <summary>📊 {now.month}월 운동 현황</summary>
    <div class="custom-toggle-content">
''', unsafe_allow_html=True)
st.plotly_chart(fig_c, use_container_width=True, key="chart_c", config={'displayModeBar': False, 'staticPlot': True})
st.markdown('</div></details>', unsafe_allow_html=True)

def get_12m():
    y, m = now.year, now.month
    res = []
    for _ in range(12):
        res.append(f"{y}-{m:02d}")
        m -= 1
        if m == 0:
            m = 12
            y -= 1
    res.reverse()
    return res

df_12 = pd.DataFrame({"Month": get_12m()})
if not df_all.empty:
    m_sum = df_all.groupby("Month", as_index=False).agg(Total_Distance=("Distance", "sum"), Run_Count=("Distance", "count"))
    df_12 = pd.merge(df_12, m_sum, on="Month", how="left").fillna({"Total_Distance": 0.0, "Run_Count": 0})
else:
    df_12["Total_Distance"] = 0.0
    df_12["Run_Count"] = 0

df_12["Run_Count"] = df_12["Run_Count"].astype(int)
df_12["Month_Label"] = df_12["Month"].apply(lambda x: f"{x[2:]}월")
df_12["Color"] = df_12.apply(lambda r: "#34D399" if r["Month"] == cur_m_str else ("#1E3A8A" if r["Total_Distance"] >= GOAL_KM else "#94A3B8"), axis=1)

# 2. 최근 12개월 운동 현황 (기호 이모지 추가)
fig_12 = px.bar(df_12, x="Month_Label", y="Total_Distance")
fig_12.update_traces(marker_color=df_12["Color"], cliponaxis=False, hoverinfo="none")
fig_12.add_hline(y=GOAL_KM, line_dash="dot", line_color="#64748B", line_width=1.5)

ann = [dict(x=r["Month_Label"], y=r["Total_Distance"], text=f"{r['Total_Distance']:.1f}", showarrow=False, xanchor="center", yanchor="bottom", yshift=2, font=dict(size=9, color="#0F172A", family="Pretendard")) for _, r in df_12.iterrows()]
fig_12.update_layout(annotations=ann, margin=dict(l=10, r=10, t=10, b=0), height=220, xaxis_title=None, yaxis_title=None, showlegend=False, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", xaxis=dict(fixedrange=True, showgrid=False, tickfont=dict(size=8, color="#64748B")), yaxis=dict(fixedrange=True, showgrid=True, gridcolor="#E2E8F0", tickfont=dict(size=10, color="#64748B"), rangemode="tozero"), font=dict(size=10, color="#475569"))

st.markdown('''
<details class="custom-toggle" open>
    <summary>📈 최근 12개월 운동 현황</summary>
    <div class="custom-toggle-content">
''', unsafe_allow_html=True)
st.plotly_chart(fig_12, use_container_width=True, key="chart_12", config={'displayModeBar': False, 'staticPlot': True})
st.markdown('</div></details>', unsafe_allow_html=True)

# 3. 월별 현황 요약 (기호 이모지 추가)
t_df = df_12.sort_values("Month", ascending=False).copy()
t_df["조회 월"] = t_df["Month_Label"]
t_df["총 거리 (km)"] = t_df["Total_Distance"].apply(lambda x: f"{x:.2f}")
t_df["러닝 횟수"] = t_df["Run_Count"].astype(str) + "회"
t_df["목표 달성률"] = (t_df["Total_Distance"] / GOAL_KM * 100).round(1).astype(str) + "%"

disp = t_df[["조회 월", "총 거리 (km)", "러닝 횟수", "목표 달성률"]].reset_index(drop=True)
html = "<table class='custom-table'><thead><tr>" + "".join([f"<th>{c}</th>" for c in disp.columns]) + "</tr></thead><tbody>"
for _, row in disp.iterrows():
    html += "<tr>" + "".join([f"<td>{v}</td>" for v in row]) + "</tr>"
html += "</tbody></table>"

st.markdown(f'''
<details class="custom-toggle">
    <summary>📋 월별 현황 요약</summary>
    <div class="custom-toggle-content">
        {html}
    </div>
</details>
''', unsafe_allow_html=True)
