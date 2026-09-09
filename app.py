<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>200CREW Dashboard</title>
  <style>
    /* 전체 페이지 배경 및 폰트 설정 */
    body {
      background-color: #f0f2f5;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }

    /* 전체 카드 컨테이너 */
    .dashboard-card {
      background-color: #ffffff;
      width: 420px;
      border-radius: 24px;
      padding: 24px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
    }

    /* 상단 헤더 영역 (이름 + 날짜 배지) */
    .header-container {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
    }

    .crew-title {
      font-size: 22px;
      font-weight: 800;
      color: #111827;
      letter-spacing: -0.5px;
    }

    /* 우측 상단 날짜 및 달력 컴포넌트 배지 */
    .date-badge {
      display: flex;
      align-items: center;
      background-color: #f3f4f6;
      padding: 6px 12px;
      border-radius: 20px;
      gap: 8px;
    }

    .calendar-icon {
      position: relative;
      width: 24px;
      height: 24px;
      background-color: #ef4444; /* 달력 상단 빨간 포인트 바 */
      border-radius: 4px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }

    .cal-month {
      font-size: 6px;
      font-weight: bold;
      color: #ffffff;
      text-transform: uppercase;
      line-height: 1;
      margin-top: 2px;
    }

    .cal-day {
      font-size: 10px;
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
    }

    .date-text {
      font-size: 12px;
      font-weight: 600;
      color: #374151;
      letter-spacing: -0.3px;
    }

    /* 메인 통계 박스 (어두운 카드) */
    .stats-card {
      background-color: #111827;
      border-radius: 20px;
      padding: 24px;
      color: #ffffff;
      position: relative;
      overflow: hidden;
    }

    /* 월간 목표 행 */
    .goal-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
    }

    .goal-label-wrapper {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .target-icon {
      color: #ef4444;
      font-size: 18px;
      font-weight: bold;
    }

    .goal-text {
      font-size: 16px;
      font-weight: 600;
      color: #d1d5db;
    }

    .goal-value {
      font-size: 26px;
      font-weight: 800;
      color: #38bdf8;
      letter-spacing: -0.5px;
    }

    /* 캐릭터 아바타 원형 */
    .avatar-container {
      position: absolute;
      top: 20px;
      right: 20px;
      width: 52px;
      height: 52px;
      background-color: #38bdf8;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 2px solid rgba(255, 255, 255, 0.2);
    }

    .avatar-container img {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      object-fit: cover;
    }

    /* 구분선 */
    .divider {
      height: 1px;
      background-color: rgba(255, 255, 255, 0.1);
      margin-bottom: 24px;
    }

    /* 하단 달성 현황 행 */
    .achievement-row {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
    }

    .achieved-km {
      font-size: 44px;
      font-weight: 900;
      letter-spacing: -1px;
      line-height: 1;
    }

    .achieved-km span {
      font-size: 16px;
      font-weight: 600;
      color: #9ca3af;
      margin-left: 4px;
    }

    .percentage-badge {
      background-color: #0284c7;
      color: #ffffff;
      font-size: 18px;
      font-weight: 700;
      padding: 10px 20px;
      border-radius: 30px;
      box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4);
    }
  </style>
</head>
<body>

  <div class="dashboard-card">
    
    <!-- 상단 헤더 -->
    <div class="header-container">
      <div class="crew-title">이실권 200CREW</div>
      
      <!-- 실시간 연동되는 우측 상단 달력 및 날짜 표시 -->
      <div class="date-badge">
        <div class="calendar-icon">
          <span class="cal-month" id="calMonth">SEP</span>
          <span class="cal-day" id="calDay">9</span>
        </div>
        <span class="date-text" id="dateText">2026.09.09 (수)</span>
      </div>
    </div>

    <!-- 메인 통계 카드 -->
    <div class="stats-card">
      
      <!-- 아바타 (필요시 이미지 경로 변경 가능) -->
      <div class="avatar-container">
        <span style="font-size: 24px;">🏃‍♂️</span>
      </div>

      <!-- 월간 목표 -->
      <div class="goal-row">
        <div class="goal-label-wrapper">
          <span class="target-icon">🎯</span>
          <span class="goal-text">월간 목표</span>
        </div>
        <div class="goal-value">200 km</div>
      </div>

      <div class="divider"></div>

      <!-- 달성 현황 -->
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

  <script>
    // 시스템 날짜를 가져와서 달력 아이콘과 날짜 텍스트를 실시간으로 동기화하는 함수
    function updateHeaderDate() {
      const now = new Date(); // 실행되는 시점의 시스템 날짜 (예: 2026년 9월 9일)
      
      const year = now.getFullYear();
      const month = String(now.getMonth() + 1).padStart(2, '0');
      const day = now.getDate();
      
      // 달력 아이콘에 표시할 영문 월 (JAN ~ DEC)
      const monthNames = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
      const currentMonthStr = monthNames[now.getMonth()];
      
      // 요일 표시
      const weekDays = ['일', '월', '화', '수', '목', '금', '토'];
      const currentDayOfWeek = weekDays[now.getDay()];

      // HTML 요소에 값 주입
      document.getElementById('calMonth').innerText = currentMonthStr;
      document.getElementById('calDay').innerText = day;
      document.getElementById('dateText').innerText = `${year}.${month}.${day} (${currentDayOfWeek})`;
    }

    // 페이지가 로드될 때 실행
    updateHeaderDate();
  </script>

</body>
</html>
