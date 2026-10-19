@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

* { 
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif !important; 
}

header { visibility: hidden; }

.stApp { background-color: #F8FAFC; }

.block-container { 
    padding-top: 0.8rem !important; 
    padding-bottom: 1.5rem !important; 
    padding-left: 0.8rem !important; 
    padding-right: 0.8rem !important; 
}

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

/* st.expander 디자인 및 글자 깨짐 방지 */
div[data-testid="stExpander"] { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; margin-bottom: 14px; box-shadow: 0 4px 12px -2px rgba(148, 163, 184, 0.08); overflow: hidden; }
div[data-testid="stExpander"] summary { font-weight: 900 !important; color: #0F172A !important; font-size: 1.05rem !important; }

.custom-table { width: 100%; border-collapse: collapse; background-color: #FFFFFF; border-radius: 10px; overflow: hidden; border: 1px solid #E2E8F0; font-size: 0.85rem; }
.custom-table th { background-color: #F1F5F9; color: #0F172A; font-weight: 700; text-align: center; padding: 7px 6px; border-bottom: 1px solid #E2E8F0; line-height: 1.3; }
.custom-table td { text-align: center; padding: 7px 6px; color: #334155; border-bottom: 1px solid #F1F5F9; line-height: 1.3; }
.custom-table tr:last-child td { border-bottom: none; }
import base64
import calendar
from datetime import datetime
import os
from zoneinfo import ZoneInfo
import plotly.express as px
import pandas as pd
import requests
import streamlit as st

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

mascot_base64 = get_image_base64("mascot.png")

st.set_page_config(
    page_title="이실권 200CREW",
    page_icon="🏃",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 외부 style.css 안전하게 불러오기
if os.path.exists("style.css"):
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

MASTER_API_KEY = st.secrets["INTERVALS_API_KEY"]
CREW_MEMBERS = {"이실권": st.secrets["INTERVALS_ATHLETE_ID"]}

st.sidebar.markdown("## 🏃‍♂️ 200CREW 멤버 선택")
selected_member = st.sidebar.selectbox("크루원을 선택하세요", list(CREW_MEMBERS.keys()))
ATHLETE_ID = CREW_MEMBERS[selected_member]
API_KEY = MASTER_API_KEY

KST = ZoneInfo("Asia/Seoul")
now = datetime.now(KST)

@st.cache_data(ttl=300)
def fetch_running_data(athlete_id, api_key, start_date_str):
    url = f"https://intervals.icu/api/v1/athlete/{athlete_id}/activities?oldest={start_date_str}"
    response = requests.get(url, auth=("API_KEY", api_key))
    if response.status_code == 200:
        return response.json()
    return []

past_year_start = f"{now.year - 2}-01-01"
activities = fetch_running_data(ATHLETE_ID, API_KEY, past_year_start)

running_records = []
if activities:
    for act in activities:
        if act.get("type") == "Run":
            distance_km = round(act.get("distance", 0) / 1000, 2)
            start_date_local = act.get("start_date_local", "")[:10]
            running_records.append({"Date": start_date_local, "Distance": distance_km})

df_all = pd.DataFrame(running_records)
if not df_all.empty:
    df_all["Month"] = df_all["Date"].str[:7]

year = now.strftime("%Y")
month_num = now.strftime("%m")
current_day = now.day
today_date_str = now.strftime("%Y-%m-%d")
week_days = ['월', '화', '수', '목', '금', '토', '일']
current_weekday = week_days[now.weekday()]
date_text = f"{year}.{month_num}.{current_day:02d} ({current_weekday})"

header_html = (
    '<div class="crew-header">'
    '<div class="crew-title">이실권 200CREW</div>'
    f'<div class="crew-subtitle"><span>🗓️</span> {date_text}</div>'
    '</div>'
)
st.markdown(header_html, unsafe_allow_html=True)

current_month_str = now.strftime("%Y-%m")
df_current = df_all[(df_all["Month"] == current_month_str)] if not df_all.empty else pd.DataFrame()

days_in_month = calendar.monthrange(now.year, now.month)[1]
remaining_days = max(1, days_in_month - current_day + 1)
GOAL_KM = 200.0

if not df_current.empty:
    total_km = round(df_current["Distance"].sum(), 2)
    run_count = len(df_current)
    remaining_km = max(0.0, round(GOAL_KM - total_km, 2))
    df_today = df_current[df_current["Date"] == today_date_str]
    today_km = round(df_today["Distance"].sum(), 2) if not df_today.empty else 0.0
    progress = total_km / GOAL_KM
    percent = round(progress * 100, 1)
    expected_total_km = round((total_km / current_day) * days_in_month, 2)
else:
    total_km, run_count, remaining_km, today_km, progress, percent = 0.0, 0, GOAL_KM, 0.0, 0.0, 0.0
    expected_total_km = 0.0

if mascot_base64:
    mascot_html = f'<img src="data:image/png;base64,{mascot_base64}" style="width: 56px; height: 56px; border-radius: 50%; border: 2px solid #38BDF8; object-fit: contain; background-color: #FFFFFF; padding: 3px; display: block; margin-left: auto;">'
else:
    mascot_html = '<span style="font-size: 1.8rem; display: block; text-align: right;">🏃💨</span>'

dynamic_goal_title = f"🎯 {now.strftime('%y년 %m월')} 목표"

hero_html = (
    '<div class="hero-card">'
    '<div class="hero-top-row">'
    '<div>'
    f'<span class="hero-goal-title">{dynamic_goal_title}</span>'
    f'<span class="hero-goal-target" style="margin-left: 8px;">{int(GOAL_KM)} km</span>'
    '</div>'
    f'<div style="width: 56px;">{mascot_html}</div>'
    '</div>'
    '<div class="hero-bottom-row">'
    '<div>'
    f'<span class="hero-km-highlight">{total_km:.2f}</span>'
    '<span class="hero-km-label">km 달성</span>'
    '</div>'
    '<div>'
    f'<span class="hero-percent-tag">{percent}%</span>'
    '</div>'
    '</div>'
    '</div>'
)
st.markdown(hero_html, unsafe_allow_html=True)

bar_width = min(100.0, percent)
custom_progress_html = (
    '<div class="progress-wrapper">'
    '<div class="custom-progress-container">'
    f'<div class="custom-progress-bar" style="width: {bar_width}%;"></div>'
    f'<div class="custom-progress-badge" style="left: {bar_width}%;">{percent}%</div>'
    '</div>'
    '</div>'
)
st.markdown(custom_progress_html, unsafe_allow_html=True)

if progress > 1.0:
    msg = f"🔥 목표 달성 완료! 현재 {percent}% 달성 중 (총 {run_count}회)"
else:
    msg = f"🔥 이번 달 총 {run_count}회 달리셨어요!"

st.markdown(f"<p style='font-size:0.85rem; font-weight:800; color:#0F172A; margin-top:4px;'>{msg}</p>", unsafe_allow_html=True)
st.write("")

sub_cards_html = (
    '<div class="grid-container">'
    '<div class="sub-card">'
    '<div class="sub-card-header"><span class="sub-icon">🏅</span><span class="sub-label">오늘 운동 거리</span></div>'
    f'<div class="sub-value sub-value-large sub-accent">{today_km:.2f} km</div>'
    '</div>'
    '<div class="sub-card">'
    '<div class="sub-card-header"><span class="sub-icon">🎯</span><span class="sub-label">남은 거리</span></div>'
    f'<div class="sub-value sub-value-large sub-accent-red">{remaining_km:.2f} km</div>'
    '</div>'
    '<div class="sub-card">'
    '<div class="sub-card-header"><span class="sub-icon">⏳</span><span class="sub-label">남은 기간</span></div>'
    f'<div class="sub-value sub-value-large">{remaining_days} 일</div>'
    '</div>'
    '<div class="sub-card">'
    '<div class="sub-card-header"><span class="sub-icon">📈</span><span class="sub-label">월 예상 거리</span></div>'
    f'<div class="sub-value sub-value-large">{expected_total_km:.2f} km</div>'
    '</div>'
    '</div>'
)
st.markdown(sub_cards_html, unsafe_allow_html=True)

# 1. 이번 달 운동 현황 (접고 펼치기 익스팬더 적용)
with st.expander(f"📊 {now.month}월 운동 현황", expanded=True):
    _, last_day = calendar.monthrange(now.year, now.month)
    all_dates_current = [f"{now.year}-{now.month:02d}-{day:02d}" for day in range(1, last_day + 1)]
    full_dates_df_current = pd.DataFrame({"Date": all_dates_current})

    if not df_current.empty:
        daily_df_current = df_current.groupby("Date", as_index=False)["Distance"].sum()
        merged_current = pd.merge(full_dates_df_current, daily_df_current, on="Date", how="left").fillna(0)
    else:
        merged_current = full_dates_df_current
        merged_current["Distance"] = 0.0

    merged_current["Date_Label"] = [str(int(d.split("-")[2])) for d in merged_current["Date"]]

    fig_curr = px.bar(merged_current, x="Date_Label", y="Distance")
    fig_curr.update_traces(marker_color="#0284C7", cliponaxis=False, hoverinfo="x+y")

    tick_vals_list = [str(d) for d in range(1, last_day + 1) if (d - 1) % 3 == 0 or d == last_day]

    fig_curr.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        height=140,
        xaxis_title=None,
        yaxis_title=None,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(fixedrange=True, showgrid=False, tickmode="array", tickvals=tick_vals_list, ticktext=tick_vals_list, tickfont=dict(size=10, color="#64748B")),
        yaxis=dict(fixedrange=True, showgrid=True, gridcolor="#E2E8F0", tickfont=dict(size=10, color="#64748B"), rangemode="tozero"),
        font=dict(size=10, color="#475569")
    )
    st.plotly_chart(fig_curr, use_container_width=True, key="chart_current_month", config={'displayModeBar': False, 'scrollZoom': False, 'staticPlot': True})

def get_past_12_months():
    months = []
    curr_y = now.year
    curr_m = now.month
    for _ in range(12):
        months.append(f"{curr_y}-{curr_m:02d}")
        curr_m -= 1
        if curr_m == 0:
            curr_m = 12
            curr_y -= 1
    months.reverse()
    return months

past_12_months_list = get_past_12_months()
full_12m_df = pd.DataFrame({"Month": past_12_months_list})

if not df_all.empty:
    monthly_summary_full = df_all.groupby("Month", as_index=False).agg(
        Total_Distance=("Distance", "sum"),
        Run_Count=("Distance", "count")
    )
    monthly_summary_12m = pd.merge(full_12m_df, monthly_summary_full, on="Month", how="left").fillna({
        "Total_Distance": 0.0,
        "Run_Count": 0
    })
else:
    monthly_summary_12m = full_12m_df.copy()
    monthly_summary_12m["Total_Distance"] = 0.0
    monthly_summary_12m["Run_Count"] = 0

monthly_summary_12m["Run_Count"] = monthly_summary_12m["Run_Count"].astype(int)

def format_month_label(m_str):
    parts = m_str.split("-")
    if len(parts) == 2:
        yy = parts[0][2:]
        mm = int(parts[1])
        return f"{yy}-{mm}월"
    return m_str

monthly_summary_12m["Month_Label"] = monthly_summary_12m["Month"].apply(format_month_label)

current_yyyymm = now.strftime("%Y-%m")

def get_bar_color(row):
    if row["Month"] == current_yyyymm:
        return "#34D399" 
    elif row["Total_Distance"] >= GOAL_KM:
        return "#1E3A8A" 
    else:
        return "#94A3B8" 

monthly_summary_12m["Color"] = monthly_summary_12m.apply(get_bar_color, axis=1)

# 2. 최근 12개월 운동 현황 (접고 펼치기 익스팬더 적용)
with st.expander("📈 최근 12개월 운동 현황", expanded=True):
    fig_all_months = px.bar(
        monthly_summary_12m,
        x="Month_Label",
        y="Total_Distance"
    )

    fig_all_months.update_traces(
        marker_color=monthly_summary_12m["Color"],
        cliponaxis=False,
        hoverinfo="none"
    )

    fig_all_months.add_hline(
        y=GOAL_KM, 
        line_dash="dot", 
        line_color="#64748B", 
        line_width=1.5
    )

    annotations_list = []
    for idx, row in monthly_summary_12m.iterrows():
        val_str = f"{row['Total_Distance']:.1f}"
        annotations_list.append(dict(
            x=row["Month_Label"],
            y=row["Total_Distance"],
            text=val_str,
            showarrow=False,
            xanchor="center",
            yanchor="bottom",
            yshift=2,
            font=dict(size=9, color="#0F172A", family="Pretendard")
        ))

    fig_all_months.update_layout(
        annotations=annotations_list,
        margin=dict(l=10, r=10, t=10, b=0),
        height=220,
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(fixedrange=True, showgrid=False, tickfont=dict(size=8, color="#64748B")),
        yaxis=dict(
            fixedrange=True, 
            showgrid=True, 
            gridcolor="#E2E8F0", 
            tickfont=dict(size=10, color="#64748B"), 
            rangemode="tozero"
        ),
        font=dict(size=10, color="#475569")
    )
    st.plotly_chart(fig_all_months, use_container_width=True, key="chart_all_months", config={'displayModeBar': False, 'scrollZoom': False, 'staticPlot': True})

# 3. 월별 현황 요약 (접고 펼치기 익스팬더 적용)
with st.expander("📋 월별 현황 요약", expanded=False):
    display_df = monthly_summary_12m.sort_values("Month", ascending=False).copy()
    display_df["총 거리 (km)"] = display_df["Total_Distance"].apply(lambda x: f"{x:.2f}")
    display_df["러닝 횟수"] = display_df["Run_Count"].astype(str) + "회"
    display_df["목표 달성률"] = (display_df["Total_Distance"] / GOAL_KM * 100).round(1).astype(str) + "%"

    display_df = display_df.rename(columns={
        "Month_Label": "조회 월"
    })[["조회 월", "총 거리 (km)", "러닝 횟수", "목표 달성률"]].reset_index(drop=True)

    table_html = "<table class='custom-table'><thead><tr>"
    for col in display_df.columns:
        table_html += f"<th>{col}</th>"
    table_html += "</tr></thead><tbody>"

    for _, row in display_df.iterrows():
        table_html += "<tr>"
        for val in row:
            table_html += f"<td>{val}</td>"
        table_html += "</tr>"
    table_html += "</tbody></table>"

    st.markdown(table_html, unsafe_allow_html=True)
