import base6s
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components

# 오늘 날짜 및 요일 자동 계산 (현재 날짜 기준 연동)
now = datetime.now()
year = now.strftime("%Y")
month_num = now.strftime("%m")

# 영문 월 표시 (JAN ~ DEC)
month_names = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
current_month_str = month_names[now.month - 1]
current_day = now.day

# 요일 매핑
week_days = ['일', '월', '화', '수', '목', '금', '토']
current_weekday = week_days[now.weekday()]
date_text = f"{year}.{month_num}.{current_day:02d} ({current_weekday})"

# local mascot.png 파일을 읽어서 base64로 인코딩 (이미지 깨짐 방지)
try:
    with open("mascot.png", "rb") as img_file:
        encoded_img = base64.b64encode(img_file.read()).decode("utf-8")
        avatar_src = f"data:image/png;base64,{encoded_img}"
except FileNotFoundError:
    avatar_src = ""  # 파일이 없을 경우의 예외 처리

# 독립된 HTML/CSS 컴포넌트 코드
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body {{
    background-color: transparent;
    margin: 0;
    padding: 5px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }}
  .dashboard-card {{
    background-color: #ffffff;
    width: 100%;
    max-width: 400px;
    border-radius: 20px;
    padding: 16px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
    margin: 0 auto;
    box-sizing: border-box;
  }}
  .header-container {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
  }}
  .crew-title {{
    font-size: 20px;
    font-weight: 800;
    color: #111827;
    letter-spacing: -0.5px;
  }}
  .date-badge {{
    display: flex;
    align-items: center;
    background-color: #f3f4f6;
    padding: 4px 10px;
    border-radius: 20px;
    gap: 6px;
  }}
  .calendar-icon {{
    position: relative;
    width: 22px;
    height: 22px;
    background-color: #ef4444;
    border-radius: 4px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    box-shadow: 0 1px 2px rgba(0,0,0,0.1);
  }}
  .cal-month {{
    font-size: 5px;
    font-weight: bold;
    color: #ffffff;
    text-transform: uppercase;
    line-height: 1;
    margin-top: 2px;
  }}
  .cal-day {{
    font-size: 9px;
    font-weight: 800;
    color: #1f2937;
    background-color: #ffffff;
    width: 100%;
    text-align: center;
    flex-grow: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
  }}
  .date-text {{
    font-size: 11px;
    font-weight: 600;
    color: #374151;
    letter-spacing: -0.3px;
  }}
  .stats-card {{
    background-color: #111827;
    border-radius: 16px;
    padding: 16px;
    color: #ffffff;
    position: relative;
  }}
  .goal-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    padding-right: 50px; 
  }}
  .goal-label-wrapper {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .target-icon {{
    color: #ef4444;
    font-size: 16px;
    font-weight: bold;
  }}
  .goal-text {{
    font-size: 15px;
    font-weight: 600;
    color: #d1d5db;
  }}
  .goal-value {{
    font-size: 24px;
    font-weight: 800;
    color: #38bdf8;
    letter-spacing: -0.5px;
  }}
  .avatar-container {{
    position: absolute;
    top: 14px;
    right: 14px;
    width: 44px;
    height: 44px;
    background-color: #ffffff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  }}
  .avatar-container img {{
    width: 38px;
    height: 38px;
    border-radius: 50%;
    object-fit: cover;
  }}
  .divider {{
    height: 1px;
    background-color: rgba(255, 255, 255, 0.1);
    margin-bottom: 16px;
  }}
  .achievement-row {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }}
  .achieved-km {{
    font-size: 36px;
    font-weight: 900;
    letter-spacing: -1px;
    line-height: 1;
  }}
  .achieved-km span {{
    font-size: 14px;
    font-weight: 600;
    color: #9ca3af;
    margin-left: 4px;
  }}
  .percentage-badge {{
    background-color: #0284c7;
    color: #ffffff;
    font-size: 16px;
    font-weight: 700;
    padding: 8px 16px;
    border-radius: 30px;
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4);
  }}
</style>
</head>
<body>
  <div class="dashboard-card">
    <div class="header-container">
      <div class="crew-title">이실권 200CREW</div>
      <div class="date-badge">
        <div class="calendar-icon">
          <span class="cal-month">{current_month_str}</span>
          <span class="cal-day">{current_day}</span>
        </div>
        <span class="date-text">{date_text}</span>
      </div>
    </div>
    <div class="stats-card">
      <div class="avatar-container">
        <img src="{avatar_src}" alt="Mascot">
      </div>
      <div class="goal-row">
        <div class="goal-label-wrapper">
          <span class="target-icon">🎯</span>
          <span class="goal-text">월간 목표</span>
        </div>
        <div class="goal-value">200 km</div>
      </div>
      <div class="divider"></div>
      <div class="achievement-row">
        <div class="achieved-km">
          68.3<span>km 달성</span>
        </div>
        <div class="percentage-badge">
          34.2%
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""

components.html(html_code, height=340, scrolling=True)
