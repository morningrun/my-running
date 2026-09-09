import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# PAGE CONFIG
st.set_page_config(page_title="내 무료 러닝 모니터", page_icon="🏃", layout="centered")

# --- INTERVALS.ICU API 설정 ---
API_KEY = st.secrets.get("INTERVALS_API_KEY", "YOUR_API_KEY")
ATHLETE_ID = st.secrets.get("INTERVALS_ATHLETE_ID", "YOUR_ATHLETE_ID")

@st.cache_data(ttl=300)  # 5분마다 데이터 자동 갱신
def get_intervals_data():
    if API_KEY == "YOUR_API_KEY" or ATHLETE_ID == "YOUR_ATHLETE_ID":
        return None

    now = datetime.now()
    oldest_date = f"{now.year}-01-01"
    
    url = f"https://intervals.icu/api/v1/athlete/{ATHLETE_ID}/events?oldest={oldest_date}"
    headers = {"Authorization": f"Basic {requests.auth._basic_auth_str('API_KEY', API_KEY)}"}

    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return None

    events = res.json()
    data = []
    
    for ev in events:
        if ev.get('type') == 'Run' and ev.get('distance'):
            start_date = datetime.strptime(ev['start_date_local'][:10], "%Y-%m-%d")
            dist_km = round(ev['distance'] / 1000, 2)
            moving_sec = ev.get('moving_time', 0)
            
            pace_str = "-"
            if dist_km > 0 and moving_sec > 0:
                sec_per_km = moving_sec / dist_km
                p_min = int(sec_per_km // 60)
                p_sec = int(sec_per_km % 60)
                pace_str = f"{p_min}'{p_sec:02d}\""

            data.append({
                'date': start_date,
                'year': start_date.year,
                'month': start_date.strftime("%Y-%m"),
                'day': start_date.strftime("%Y-%m-%d"),
                'name': ev.get('name', '러닝'),
                'distance_km': dist_km,
                'pace': pace_str,
                'avg_hr': int(ev.get('average_heartrate', 0)) if ev.get('average_heartrate') else "-"
            })

    return pd.DataFrame(data)

# --- 메인 앱 UI ---
st.title("🏃 Running Dashboard")

df = get_intervals_data()

if df is None or df.empty:
    st.info("💡 Intervals.icu 연동 설정을 완료해 주세요. (Streamlit Secrets 설정 필요)")
else:
    now = datetime.now()
    current_month_str = now.strftime("%Y-%m")
    current_year = now.year

    # 1. 이번 달 200km 목표 진행률
    st.subheader(f"🎯 {now.month}월 목표 달성 현황 (목표: 200km)")
    month_df = df[df['month'] == current_month_str]
    current_km = round(month_df['distance_km'].sum(), 1) if not month_df.empty else 0.0
    target_km = 200.0
    
    progress = min(current_km / target_km, 1.0)
    pct = round((current_km / target_km) * 100, 1)

    st.progress(progress)
    col1, col2, col3 = st.columns(3)
    col1.metric("현재 누적", f"{current_km} km")
    col2.metric("목표 달성률", f"{pct}%")
    col3.metric("남은 거리", f"{max(round(target_km - current_km, 1), 0)} km")

    st.markdown("---")

    # 2. 월별/연간 러닝 횟수
    st.subheader("📊 러닝 횟수 통계")
    year_df = df[df['year'] == current_year]
    
    c1, c2 = st.columns(2)
    c1.metric("이번 달 운동 횟수", f"{len(month_df)} 회")
    c2.metric(f"{current_year}년 총 운동 횟수", f"{len(year_df)} 회")

    # 그래프
    monthly_counts = year_df.groupby('month').size().reset_index(name='운동횟수')
    fig = px.bar(
        monthly_counts, 
        x='month', 
        y='운동횟수', 
        text='운동횟수',
        title=f"{current_year}년 월별 러닝 횟수",
        color_discrete_sequence=['#4CAF50']
    )
    fig.update_layout(xaxis_title="월", yaxis_title="횟수", margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # 3. 최근 운동 목록
    st.subheader("📋 최근 운동 기록")
    recent = df.sort_values(by='date', ascending=False).head(10)
    recent_display = recent[['day', 'name', 'distance_km', 'pace', 'avg_hr']]
    recent_display.columns = ['날짜', '활동명', '거리(km)', '페이스', '평균심박']
    st.dataframe(recent_display, use_container_width=True, hide_index=True)
