import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="러닝 대시보드 (200km)", page_icon="🏃", layout="centered")

st.title("🏃 Running Dashboard")

# 1. Secrets 안전하게 읽기 (대소문자 및 키 명칭 호환성 처리)
def get_secret(key):
    if key in st.secrets:
        return st.secrets[key]
    # 대소문자 차이나 변수명 차이 대응
    lower_key = key.lower()
    for k, v in st.secrets.items():
        if k.lower() == lower_key:
            return v
    return None

api_key = get_secret("INTERVALS_API_KEY")
athlete_id = get_secret("INTERVALS_ATHLETE_ID")

if not api_key or not athlete_id:
    st.info("💡 Intervals.icu 연동 설정을 완료해 주세요. (Streamlit Secrets 설정 필요)")
    st.stop()

# 2. Intervals.icu API 데이터 호출
@st.cache_data(ttl=300)
def fetch_running_data(api_key, athlete_id):
    now = datetime.now()
    oldest = now.replace(day=1).strftime("%Y-%m-%d")
    newest = now.strftime("%Y-%m-%d")
    
    url = f"https://intervals.icu/api/v1/athlete/{athlete_id}/activities?oldest={oldest}&newest={newest}"
    
    try:
        response = requests.get(url, auth=("API_KEY", api_key), timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"데이터를 가져오는데 실패했습니다. (응답 코드: {response.status_code})")
            return []
    except Exception as e:
        st.error(f"API 연결 오류: {e}")
        return []

activities = fetch_running_data(api_key, athlete_id)

# 3. 러닝 데이터 정제
runs = [act for act in activities if act.get("type") in ["Run", "VirtualRun", "Treadmill"]]

total_distance_m = sum(act.get("distance", 0) for act in runs)
total_distance_km = round(total_distance_m / 1000, 2)
target_km = 200.0
progress_pct = min(round((total_distance_km / target_km) * 100, 1), 100.0)

# 4. 대시보드 UI 구성
col1, col2 = st.columns(2)
with col1:
    st.metric("이번 달 누적 거리", f"{total_distance_km} km", f"목표 {target_km} km")
with col2:
    st.metric("러닝 횟수", f"{len(runs)} 회")

st.write("### 🎯 월간 목표 달성률 (200km)")
st.progress(progress_pct / 100)
st.caption(f"현재 달성률: {progress_pct}%")

if runs:
    st.write("### 🏃 최근 러닝 기록")
    df_data = []
    for run in runs:
        df_data.append({
            "날짜": run.get("start_date_local", "")[:10],
            "제목": run.get("name", "러닝"),
            "거리(km)": round(run.get("distance", 0) / 1000, 2),
            "시간(분)": round(run.get("moving_time", 0) / 60, 1)
        })
    df = pd.DataFrame(df_data)
    
    fig = px.bar(df, x="날짜", y="거리(km)", title="일자별 러닝 거리 (km)", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(df, use_container_width=True)
else:
    st.info("이번 달 등록된 러닝 기록이 없습니다.")
