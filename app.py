import base64
import calendar
from datetime import datetime
import os
from zoneinfo import ZoneInfo
import plotly.express as px
import pandas as pd
import requests
import streamlit as st

# 이미지 base64 변환 함수 (마스코트 공용)
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# 마스코트 이미지 로드
mascot_base64 = get_image_base64("mascot.png")

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
        font-size: 1.45rem !important;
        font-weight: 900;
        letter-spacing: -0.6px;
        background: linear-gradient(135deg, #0F172A 0%, #0284C7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        white-space: nowrap;
    }

    .crew-subtitle {
        font-size: 0.75rem;
        color: #64748B;
        font-weight: 600;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 4px 10px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        gap: 5px;
        white-space: nowrap;
    }

    .hero-card {
        background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
        border-radius: 22px;
        padding: 20px 22px;
        color: #FFFFFF;
        box-shadow: 0 12px 28px -6px rgba(15, 23, 42, 0.25);
        margin-bottom: 16px;
    }

    .hero-top-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 12px;
        margin-bottom: 14px;
    }
    .hero-goal-title {
        font-size: 0.95rem;
        color: #94A3B8;
        font-weight: 700;
        letter-spacing: 0.3px;
    }
    .hero-goal-target {
        font-size: 1.45rem !important;
        color: #38BDF8;
        font-weight: 900;
    }

    .hero-bottom-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .hero-km-highlight {
        font-size: 2.3rem;
        font-weight: 900;
        color: #FFFFFF !important;
        line-height: 1;
    }
    .hero-km-label {
        font-size: 1rem;
        font-weight: 600;
        color: #94A3B8 !important;
        margin-left: 2px;
    }
    .hero-percent-tag {
        background: linear-gradient(135deg, #38BDF8 0%, #0284C7 100%);
        color: #FFFFFF;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.95rem;
        font-weight: 800;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.35);
        display: inline-block;
        text-align: center;
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
    .sub-value { font-size: 1.1rem; font-weight: 900; color: #0F172A; }
    
    .sub-value-large { font-size: 1.45rem !important; font-weight: 900; }
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

# 한국 시간(KST) 기준 현재 시간 설정
KST = ZoneInfo("Asia/Seoul")
now = datetime.now(KST)

# 4. 데이터 로딩
@st.cache_data(ttl=300)
def fetch_running_data(start_date_str):
    url = f"https://intervals.icu/api/v1/athlete/{ATHLETE_ID}/activities?oldest={start_date_str}"
    response = requests.get(url, auth=("API_KEY", API_KEY))
    if response.status_code == 200:
        return response.json()
    return []

past_year_start = f"{now.year - 3}-01-01"
activities = fetch_running_data(past_year_start)

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

df_all = pd.DataFrame(running_records)
if not df_all.empty:
    df_all["Month"] = df_all["Date"].str[:7]

# 날짜 및 요일 연동 계산
year = now.strftime("%Y")
month_num = now.strftime("%m")
current_day = now.day
week_days = ['월', '화', '수', '목', '금', '토', '일']
current_weekday = week_days[now.weekday()]
date_text = f"{year}.{month_num}.{current_day:02d} ({current_weekday})"
calendar_icon_html = f"🗓️"

# 상단 헤더 출력
header_html = """
    <div class="crew-header">
        <div class="crew-title">이실권 200CREW</div>
        <div class="crew-subtitle"><span>{cal_icon}</span> {date_str}</div>
    </div>
""".format(cal_icon=calendar_icon_html, date_str=date_text)
st.markdown(header_html, unsafe_allow_html=True)

# 이번 달(현재) 데이터 필터링
current_month_str = now.strftime("%Y-%m")
df_current = df_all[df_all["Month"] == current_month_str] if not df_all.empty else pd.DataFrame()

days_in_month = calendar.monthrange(now.year, now.month)[1]
remaining_days = max(1, days_in_month - current_day + 1)
GOAL_KM = 200.0

if not df_current.empty:
    total_km = round(df_current["Distance"].sum(), 2)
    run_count = len(df_current)
    remaining_km = max(0.0, round(GOAL_KM - total_km, 2))
    
    progress = total_km / GOAL_KM
    percent = round(progress * 100, 1)
    
    daily_required_km = round(remaining_km / remaining_days, 2) if remaining_km > 0 else 0.0
    expected_total_km = round((total_km / current_day) * days_in_month, 2)
else:
    total_km, run_count, remaining_km, progress, percent = 0.0, 0, GOAL_KM, 0.0, 0.0
    daily_required_km = round(GOAL_KM / days_in_month, 2)
    expected_total_km = 0.0

# 마스코트 이미지 출력 세팅
if mascot_base64:
    mascot_html = f'<img src="data:image/png;base64,{mascot_base64}" style="width: 56px; height: 56px; border-radius: 50%; border: 2px solid #38BDF8; object-fit: contain; background-color: #FFFFFF; padding: 3px; display: block; margin-left: auto;">'
else:
    mascot_html = '<span style="font-size: 1.8rem; display: block; text-align: right;">🏃💨</span>'

dynamic_goal_title = f"🎯 {now.strftime('%y년 %m월')} 목표"

# 1. 메인 히어로 카드
hero_html = """
    <div class="hero-card">
        <div class="hero-top-row">
            <div>
                <span class="hero-goal-title">{goal_title}</span>
                <span class="hero-goal-target" style="margin-left: 8px;">{goal} km</span>
            </div>
            <div style="width: 56px;">{mascot}</div>
        </div>
        <div class="hero-bottom-row">
            <div>
                <span class="hero-km-highlight">{total:.2f}</span>
                <span class="hero-km-label">km 달성</span>
            </div>
            <div>
                <div class="hero-percent-tag">{pct}%</div>
            </div>
        </div>
    </div>
""".format(
    goal_title=dynamic_goal_title,
    mascot=mascot_html,
    total=total_km,
    goal=int(GOAL_KM),
    pct=percent
)
st.markdown(hero_html, unsafe_allow_html=True)

# 2. 프로그레스 바 및 안내 문구
st.progress(min(1.0, progress))
if progress > 1.0:
    st.markdown(f"<p style='font-size:0.85rem; font-weight:800; color:#0F172A; margin-top:4px;'>🔥 목표 달성 완료! 현재 {percent}% 달성 중 (총 {run_count}회)</p>", unsafe_allow_html=True)
else:
    st.markdown(f"<p style='font-size:0.85rem; font-weight:800; color:#0F172A; margin-top:4px;'>🔥 이번 달 총 {run_count}회 달리셨어요!</p>", unsafe_allow_html=True)
st.write("")

# 3. 서브 카드 출력
sub_cards_html = """
<div class="grid-container">
    <div class="sub-card">
        <div class="sub-card-header">
            <span class="sub-icon">🎯</span>
            <span class="sub-label">남은 거리</span>
        </div>
        <div class="sub-value sub-value-large sub-accent">{rem_km:.2f} km</div>
    </div>
    <div class="sub-card">
        <div class="sub-card-header">
            <span class="sub-icon">⚡</span>
            <span class="sub-label">예상 하루 운동 거리</span>
        </div>
        <div class="sub-value">{daily_km:.2f} km</div>
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
            <span class="sub-label">월 예상 거리</span>
        </div>
        <div class="sub-value">{exp_km:.2f} km</div>
    </div>
</div>
""".format(
    rem_km=remaining_km,
    daily_km=daily_required_km,
    rem_days=remaining_days,
    exp_km=expected_total_km
)
st.markdown(sub_cards_html, unsafe_allow_html=True)

# 4. 이번 달 일별 차트
current_month_title_str = f"📊 {now.month}월 일별 운동 거리 (km)"
st.markdown(f"<p style='font-size:0.82rem; font-weight:800; color:#334155; margin-bottom:6px;'>{current_month_title_str}</p>", unsafe_allow_html=True)

_, last_day = calendar.monthrange(now.year, now.month)
all_dates_current = [f"{now.year}-{now.month:02d}-{day:02d}" for day in range(1, last_day + 1)]
full_dates_df_current = pd.DataFrame({"Date": all_dates_current})

if not df_current.empty:
    daily_df_current = df_current.groupby("Date", as_index=False)["Distance"].sum()
    merged_current = pd.merge(full_dates_df_current, daily_df_current, on="Date", how="left").fillna(0)
else:
    merged_current = full_dates_df_current
    merged_current["Distance"] = 0.0

# X축 표시용 '월/일' 형식 (예: 10/1, 10/2 ...) 컬럼 생성
merged_current["Date_Label"] = pd.to_datetime(merged_current["Date"]).dt.strftime(f"{now.month}/%-d")

fig_curr = px.bar(merged_current, x="Date_Label", y="Distance")
fig_curr.update_traces(
    text=[f"{v:.2f}" if v > 0 else "" for v in merged_current["Distance"]],
    textposition="outside",
    marker_color="#0284C7",
    cliponaxis=False,
    hoverinfo="none",
    textfont=dict(size=9, color="#475569", family="Pretendard")
)
fig_curr.update_layout(
    margin=dict(l=0, r=0, t=25, b=0),
    height=160,
    xaxis_title=None,
    yaxis_title=None,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(fixedrange=True, showgrid=False, tickfont=dict(size=8, color="#64748B")),
    yaxis=dict(fixedrange=True, showgrid=True, gridcolor="#E2E8F0", tickfont=dict(size=9, color="#64748B")),
    font=dict(size=10, color="#475569")
)
st.plotly_chart(fig_curr, use_container_width=True, key="chart_current_month", config={'displayModeBar': False, 'scrollZoom': False, 'staticPlot': True})


# ==========================================
# 5. 월별 현황 비교 섹션
# ==========================================
st.markdown("<hr style='margin: 30px 0 20px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

if not df_all.empty:
    monthly_summary_full = df_all.groupby("Month", as_index=False).agg(
        Total_Distance=("Distance", "sum"),
        Run_Count=("Distance", "count")
    )
    monthly_summary_full["Total_Distance"] = monthly_summary_full["Total_Distance"].round(2)
    monthly_summary_full = monthly_summary_full.sort_values("Month")

    monthly_summary_12m = monthly_summary_full.sort_values("Month", ascending=False).head(12).sort_values("Month")

    # X축 표시용 포맷 변환 컬럼 추가 (예: "2026-03" -> "26-3월")
    def format_month_label(m_str):
        parts = m_str.split("-")
        if len(parts) == 2:
            yy = parts[0][2:]  # 연도 뒤 두 자리 (예: '26')
            mm = int(parts[1]) # 월 (예: 3)
            return f"{yy}-{mm}월"
        return m_str

    monthly_summary_12m["Month_Label"] = monthly_summary_12m["Month"].apply(format_month_label)
    monthly_summary_full["Month_Label"] = monthly_summary_full["Month"].apply(format_month_label)

    monthly_summary_12m["Color"] = monthly_summary_12m["Total_Distance"].apply(
        lambda x: "#1E3A8A" if x >= GOAL_KM else "#94A3B8"
    )

    st.markdown("<p style='font-size:1.1rem; font-weight:900; color:#0F172A; margin-bottom:12px;'>📈 최근 12개월 운동 현황 비교</p>", unsafe_allow_html=True)

    # X축에 변환된 "Month_Label" 컬럼 적용
    fig_all_months = px.bar(
        monthly_summary_12m,
        x="Month_Label",
        y="Total_Distance",
        color="Color",
        color_discrete_map="identity"
    )
    
    # 두 그래프 모두 상단 글씨 크기를 9로 통일 (textfont size=9)
    fig_all_months.update_traces(
        text=[f"{v:.2f}" for v in monthly_summary_12m["Total_Distance"]],
        textposition="outside",
        cliponaxis=False,
        hoverinfo="none",
        textfont=dict(size=9, color="#475569", family="Pretendard")
    )
    
    # 200km 기준선(점선) 추가 (문구 제거)
    fig_all_months.add_hline(
        y=GOAL_KM, 
        line_dash="dot", 
        line_color="#64748B", 
        line_width=1.5
    )

    fig_all_months.update_layout(
        margin=dict(l=0, r=0, t=25, b=0),
        height=185,
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(fixedrange=True, showgrid=False, tickfont=dict(size=9, color="#64748B")),
        yaxis=dict(fixedrange=True, showgrid=True, gridcolor="#E2E8F0", tickfont=dict(size=9, color="#64748B")),
        font=dict(size=10, color="#475569")
    )
    st.plotly_chart(fig_all_months, use_container_width=True, key="chart_all_months", config={'displayModeBar': False, 'scrollZoom': False, 'staticPlot': True})

    st.write("")
    st.markdown("<p style='font-size:0.85rem; font-weight:800; color:#334155; margin-bottom:6px;'>📋 전체 월별 상세 기록 요약</p>", unsafe_allow_html=True)
    
    display_df = monthly_summary_full.rename(columns={
        "Month_Label": "조회 월",
        "Total_Distance": "총 거리 (km)",
        "Run_Count": "러닝 횟수"
    }).sort_values("조회 월", ascending=False).reset_index(drop=True)
    
    display_df["목표 달성률"] = (display_df["총 거리 (km)"] / GOAL_KM * 100).round(1).astype(str) + "%"
    display_df = display_df[["조회 월", "총 거리 (km)", "러닝 횟수", "목표 달성률"]]
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)

else:
    st.info("조회 가능한 러닝 기록이 없습니다.")
