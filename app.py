from datetime import datetime
import streamlit as st

# 오늘 날짜 및 요일 자동 계산
now = datetime.now()
year = now.strftime("%Y")
month_num = now.strftime("%m")
current_day = now.day

month_names = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
current_month_str = month_names[now.month - 1]

week_days = ['일', '월', '화', '수', '목', '금', '토']
current_weekday = week_days[now.weekday()]
date_text = f"{year}.{month_num}.{current_day:02d} ({current_weekday})"

# 화면 구성
st.markdown(f"""
<div style="background-color: #ffffff; padding: 20px; border-radius: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); max-width: 400px; margin: 0 auto;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <h3 style="margin: 0; color: #111827; font-size: 20px; font-weight: 800;">이실권 200CREW</h3>
        <span style="font-size: 12px; color: #4b5563; background-color: #f3f4f6; padding: 4px 10px; border-radius: 12px; font-weight: 600;">📅 {date_text}</span>
    </div>
    <div style="background-color: #111827; color: #ffffff; padding: 20px; border-radius: 16px; position: relative;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <div>
                <span style="color: #ef4444; font-size: 14px; font-weight: bold;">🎯 월간 목표</span>
                <div style="font-size: 22px; font-weight: 800; color: #38bdf8; margin-top: 4px;">200 km</div>
            </div>
        </div>
        <hr style="border: none; height: 1px; background-color: rgba(255,255,255,1); margin: 16px 0;">
        <div style="display: flex; justify-content: space-between; align-items: flex-end;">
            <div>
                <span style="font-size: 14px; color: #9ca3af; font-weight: 600;">km 달성</span>
                <div style="font-size: 36px; font-weight: 900; line-height: 1.1;">68.3</div>
            </div>
            <div style="background-color: #0284c7; color: #ffffff; font-size: 15px; font-weight: 700; padding: 6px 14px; border-radius: 20px;">
                34.2%
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
