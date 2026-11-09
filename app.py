<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>토달 출석부</title>
    
    <!-- 📱 스마트폰 홈 화면 추가 시 앱처럼 보이게 해주는 설정 -->
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="토달출석부">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="theme-color" content="#2c3e50">

    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f0f2f5; margin: 0; padding: 10px; color: #333; -webkit-tap-highlight-color: transparent; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 15px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
        
        .main-title-box { text-align: center; margin: 10px 0 5px 0; }
        .main-title { font-size: 1.8rem; font-weight: 800; color: #1e293b; }
        .subtitle { text-align: center; font-size: 0.85rem; color: #7f8c8d; margin-bottom: 15px; }
        
        .tab-group { display: flex; gap: 6px; margin-bottom: 15px; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px; position: sticky; top: 0; background: white; z-index: 10; }
        .tab-btn { flex: 1; padding: 10px 4px; font-size: 0.95rem; border: none; background: #f1f5f9; color: #64748b; font-weight: bold; border-radius: 8px; cursor: pointer; transition: all 0.2s; text-align: center; }
        .tab-btn.active { background: #2c3e50; color: white; }

        .month-filter { display: flex; gap: 6px; overflow-x: auto; padding-bottom: 10px; margin-bottom: 15px; -webkit-overflow-scrolling: touch; }
        .month-btn { padding: 8px 14px; font-size: 0.9rem; border: 1px solid #cbd5e1; border-radius: 8px; background: white; cursor: pointer; font-weight: bold; color: #64748b; white-space: nowrap; }
        .month-btn.active { background: #0284c7; color: white; border-color: #0284c7; }

        .saturday-list-box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; margin-bottom: 15px; }
        .saturday-list-title { font-size: 0.9rem; font-weight: bold; color: #475569; margin-bottom: 8px; }
        .saturday-vertical-group { display: flex; flex-direction: column; gap: 6px; max-height: 200px; overflow-y: auto; }
        
        .saturday-item-btn { padding: 10px 14px; background: white; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 0.95rem; font-weight: bold; color: #334155; cursor: pointer; text-align: left; transition: all 0.2s; display: flex; justify-content: space-between; align-items: center; }
        .saturday-item-btn.active { background: #2563eb; color: white; border-color: #2563eb; box-shadow: 0 2px 4px rgba(37,99,235,0.2); }
        .saturday-item-btn.disabled { background: #e2e8f0; color: #94a3b8; border-color: #cbd5e1; cursor: not-allowed; opacity: 0.7; }

        .member-card { display: flex; flex-direction: column; padding: 12px; margin-bottom: 10px; background: #ffffff; border: 1px solid #e1e8ed; border-radius: 10px; transition: all 0.2s; gap: 8px; }
        .member-card.checked-10 { background-color: #e8f8f5 !important; border-color: #2ecc71 !important; border-left: 5px solid #2ecc71 !important; }
        .member-card.checked-5  { background-color: #ebf5fb !important; border-color: #3498db !important; border-left: 5px solid #3498db !important; }
        .member-card.checked-comp { background-color: #fef5e7 !important; border-color: #f39c12 !important; border-left: 5px solid #f39c12 !important; }

        .member-info { display: flex; justify-content: space-between; align-items: center; }
        .member-name { font-weight: bold; font-size: 1.05rem; color: #2c3e50; white-space: nowrap; }
        .badge { font-size: 0.85rem; font-weight: bold; padding: 2px 8px; border-radius: 4px; }
        
        .btn-group { display: flex; gap: 4px; width: 100%; }
        .btn-group button { flex: 1; padding: 10px 2px; font-size: 0.85rem; border: 1px solid #cbd5e1; border-radius: 6px; cursor: pointer; font-weight: bold; background: #ffffff; color: #64748b; text-align: center; transition: all 0.2s; }
        
        button.selected-10 { background: #2ecc71 !important; color: white !important; border-color: #2ecc71 !important; }
        button.selected-5  { background: #3498db !important; color: white !important; border-color: #3498db !important; }
        button.selected-comp { background: #f39c12 !important; color: white !important; border-color: #f39c12 !important; }
        button.btn-cancel { background: #fff5f5; color: #e74c3c; border-color: #fab6b6; }

        .rank-card { display: flex; justify-content: space-between; align-items: center; padding: 12px 15px; margin-bottom: 8px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; }
        .rank-number { font-weight: bold; color: #3b82f6; width: 45px; font-size: 0.95rem; }
        .rank-name { font-weight: bold; flex: 1; font-size: 1rem; color: #1e293b; }
        .rank-detail { font-size: 0.78rem; color: #64748b; margin-right: 8px; }
        .rank-score { font-weight: bold; font-size: 1.1rem; color: #059669; }

        .hidden { display: none; }
        .loading { text-align: center; color: #888; padding: 20px; }
    </style>
</head>
<body>

<div class="container">
    <div class="main-title-box">
        <div class="main-title">🏃‍♂️ 토달 출석부 👟</div>
    </div>
    <div class="subtitle">매주 토요일 운동모임 출석 & 누적 현황</div>
    
    <div class="tab-group">
        <button class="tab-btn active" id="tab-checkin-btn" onclick="switchTab('checkin')">📅 출석체크</button>
        <button class="tab-btn" id="tab-stats-btn" onclick="switchTab('stats')">🏆 <span id="current-year-text">2026</span>년 누적현황</button>
    </div>

    <!-- 출석체크 탭 -->
    <div id="tab-checkin">
        <div class="month-filter" id="checkin-month-buttons"></div>
        
        <div class="saturday-list-box">
            <div class="saturday-list-title" id="saturday-list-header">📅 2026년 11월 토달 출석현황</div>
            <div class="saturday-vertical-group" id="saturday-vertical-wrapper"></div>
        </div>

        <div id="member-list" class="loading">회원 명단 불러오는 중...</div>
    </div>

    <!-- 누적현황 탭 -->
    <div id="tab-stats" class="hidden">
        <div class="month-filter" id="stats-month-buttons"></div>
        <div id="stats-list" class="loading">누적 데이터 계산 중...</div>
    </div>
</div>

<script>
    // 💡 여기에 구글 웹 앱 URL을 넣어주세요!
    const API_URL = "여기에_구글_웹_앱_URL을_넣으세요https://script.google.com/macros/s/AKfycbyPD-g3-AhImPFdQk_wBokuFr4iT8uWJN4U44xl6RqBbfkFBgGWe7Vz-csyv3GEbbE-4A/exec";

    let globalMembers = [];
    let globalLogs = [];
    let selectedDateStr = "";
    let checkinSelectedMonth = String(new Date().getMonth() + 1) + "월";
    let statsSelectedMonth = "전체";

    const currentYear = new Date().getFullYear();
    document.getElementById('current-year-text').innerText = currentYear;

    function formatDateToString(dateObj) {
        const years = dateObj.getFullYear();
        const months = dateObj.getMonth() + 1;
        const days = dateObj.getDate();
        const weekDays = ['일요일', '월요일', '화요일', '수요일', '목요일', '금요일', '토요일'];
        return `${years}년 ${months}월 ${days}일 ${weekDays[dateObj.getDay()]}`;
    }

    function getAllSaturdaysOfCurrentYear() {
        const saturdays = [];
        let d = new Date(currentYear, 0, 1);
        while (d.getDay() !== 6) {
            d.setDate(d.getDate() + 1);
        }
        while (d.getFullYear() === currentYear) {
            saturdays.push(formatDateToString(new Date(d)));
            d.setDate(d.getDate() + 7);
        }
        return saturdays;
    }

    const allSaturdays = getAllSaturdaysOfCurrentYear();

    function initCheckinMonthButtons() {
        const wrapper = document.getElementById('checkin-month-buttons');
        wrapper.innerHTML = '';
        const months = ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"];
        
        months.forEach(m => {
            const btn = document.createElement('button');
            btn.className = `month-btn ${m === checkinSelectedMonth ? 'active' : ''}`;
            btn.innerText = m;
            btn.onclick = () => {
                document.querySelectorAll('#checkin-month-buttons .month-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                checkinSelectedMonth = m;
                renderSaturdayVerticalList();
            };
            wrapper.appendChild(btn);
        });
    }

    function initStatsMonthButtons() {
        const wrapper = document.getElementById('stats-month-buttons');
        wrapper.innerHTML = '';
        const months = ["전체", "1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"];
        
        months.forEach(m => {
            const btn = document.createElement('button');
            btn.className = `month-btn ${m === statsSelectedMonth ? 'active' : ''}`;
            btn.innerText = m;
            btn.onclick = () => {
                document.querySelectorAll('#stats-month-buttons .month-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                statsSelectedMonth = m; 
                renderStats();     
            };
            wrapper.appendChild(btn);
        });
    }

    function renderSaturdayVerticalList() {
        const wrapper = document.getElementById('saturday-vertical-wrapper');
        const header = document.getElementById('saturday-list-header');
        wrapper.innerHTML = '';

        header.innerText = `📅 ${currentYear}년 ${checkinSelectedMonth} 토달 출석현황`;

        const filteredSaturdays = allSaturdays.filter(dStr => {
            const mMatch = dStr.match(/(\d+)월/);
            return mMatch && (mMatch[1] + "월") === checkinSelectedMonth;
        });

        if (filteredSaturdays.length === 0) {
            wrapper.innerHTML = "<div style='padding:10px; color:#888; font-size:0.9rem;'>해당 월에 토요일이 없습니다.</div>";
            return;
        }

        const today = new Date();
        today.setHours(0, 0, 0, 0);

        const validSaturdays = filteredSaturdays.filter(dStr => {
            const tDate = new Date(dStr.replace(/년|월/g, '-').replace(/일.*/, '').trim());
            tDate.setHours(0, 0, 0, 0);
            return tDate <= today;
        });

        let defaultDate = validSaturdays.length > 0 ? validSaturdays[validSaturdays.length - 1] : filteredSaturdays[0];

        if (!selectedDateStr || !filteredSaturdays.includes(selectedDateStr)) {
            selectedDateStr = defaultDate;
        }

        filteredSaturdays.forEach(dStr => {
            const btn = document.createElement('button');
            const cleanDateStr = dStr.replace(/년|월/g, '-').replace(/일.*/, '').trim();
            const targetDate = new Date(cleanDateStr);
            targetDate.setHours(0, 0, 0, 0);
            
            const isFuture = targetDate > today;
            const isSelected = (dStr === selectedDateStr);

            if (isFuture) {
                btn.className = 'saturday-item-btn disabled';
                btn.innerHTML = `<span>🔒 ${dStr.replace(/^\d{4}년\s*/, '')} (예정)</span>`;
                btn.onclick = () => {
                    alert("아직 다가오지 않은 미래 날짜는 출석을 체크할 수 없습니다!");
                };
            } else {
                btn.className = `saturday-item-btn ${isSelected ? 'active' : ''}`;
                btn.innerText = dStr.replace(/^\d{4}년\s*/, '');
                btn.onclick = () => {
                    document.querySelectorAll('.saturday-item-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    selectedDateStr = dStr;
                    renderCheckinList();
                };
            }
            wrapper.appendChild(btn);
        });

        const selTargetDate = new Date(selectedDateStr.replace(/년|월/g, '-').replace(/일.*/, '').trim());
        selTargetDate.setHours(0, 0, 0, 0);
        if (selTargetDate > today && validSaturdays.length > 0) {
            selectedDateStr = validSaturdays[validSaturdays.length - 1];
        }

        renderCheckinList();
    }

    function switchTab(tabName) {
        if (tabName === 'checkin') {
            document.getElementById('tab-checkin').classList.remove('hidden');
            document.getElementById('tab-stats').classList.add('hidden');
            document.getElementById('tab-checkin-btn').classList.add('active');
            document.getElementById('tab-stats-btn').classList.remove('active');
        } else {
            document.getElementById('tab-checkin').classList.add('hidden');
            document.getElementById('tab-stats').classList.remove('hidden');
            document.getElementById('tab-checkin-btn').classList.remove('active');
            document.getElementById('tab-stats-btn').classList.add('active');
            renderStats(); 
        }
    }

    function loadData() {
        fetch(API_URL + "?t=" + new Date().getTime(), { redirect: "follow" })
            .then(res => res.json())
            .then(data => {
                globalMembers = data.members || [];
                globalLogs = data.logs || []; 
                renderSaturdayVerticalList();
                if (!document.getElementById('tab-stats').classList.contains('hidden')) {
                    renderStats();
                }
            })
            .catch(err => {
                console.error(err);
                document.getElementById('member-list').innerHTML = "<div style='color:#e74c3c; font-weight:bold;'>데이터 연결 대기 중... 웹 앱 URL을 확인해 주세요.</div>";
            });
    }

    function renderCheckinList() {
        const listDiv = document.getElementById('member-list');
        listDiv.innerHTML = '';
        if(globalMembers.length === 0) return;

        const dayAttendance = {};
        globalLogs.forEach(log => {
            if (log.date && log.date.trim() === selectedDateStr.trim() && Number(log.score) > 0) {
                dayAttendance[log.name] = Number(log.score);
            }
        });

        globalMembers.forEach(member => {
            const name = member.name;
            const score = dayAttendance[name] || 0;
            const isChecked = score > 0;

            const card = document.createElement('div');
            let cardClass = 'member-card';
            if (isChecked) {
                if (score === 10) cardClass += ' checked-10';
                else if (score === 5) cardClass += ' checked-5';
                else if (score === 99) cardClass += ' checked-comp';
            }
            card.className = cardClass;
            
            let badgeHtml = '';
            if (isChecked) {
                if (score === 10) badgeHtml = '<span class="badge" style="background:#2ecc71; color:white;">🟢 출석</span>';
                else if (score === 5) badgeHtml = '<span class="badge" style="background:#3498db; color:white;">🔵 지각</span>';
                else if (score === 99) badgeHtml = '<span class="badge" style="background:#f39c12; color:white;">🟠 대회</span>';
            }

            card.innerHTML = `
                <div class="member-info">
                    <div class="member-name">${name}</div>
                    <div>${badgeHtml}</div>
                </div>
                <div class="btn-group">
                    <button class="${isChecked && score === 10 ? 'selected-10' : ''}" onclick="checkIn('${name}', 10)">출석(+10)</button>
                    <button class="${isChecked && score === 5 ? 'selected-5' : ''}" onclick="checkIn('${name}', 5)">지각(+5)</button>
                    <button class="${isChecked && score === 99 ? 'selected-comp' : ''}" onclick="checkIn('${name}', 99)">대회(+10)</button>
                    ${isChecked ? `<button class="btn-cancel" onclick="cancelCheckIn('${name}')">취소</button>` : ''}
                </div>
            `;
            listDiv.appendChild(card);
        });
    }

    function renderStats() {
        const statsDiv = document.getElementById('stats-list');
        statsDiv.innerHTML = '';
        if (globalMembers.length === 0) return;

        const userMonthlyData = {};
        globalMembers.forEach(m => {
            userMonthlyData[m.name] = {
                score: {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0},
                att:   {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0},
                tardy: {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0},
                comp:  {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}
            };
        });

        globalLogs.forEach(log => {
            const name = log.name;
            const score = Number(log.score);
            const m = Number(log.month);
            if (score <= 0 || !userMonthlyData[name] || m < 1 || m > 12) return;

            if (score === 10) {
                userMonthlyData[name].score[m] += 10;
                userMonthlyData[name].att[m] += 1;
            } else if (score === 5) {
                userMonthlyData[name].score[m] += 5;
                userMonthlyData[name].tardy[m] += 1;
            } else if (score === 99) {
                userMonthlyData[name].score[m] += 10;
                userMonthlyData[name].comp[m] += 1;
            }
        });

        let displayList = [];
        globalMembers.forEach(member => {
            const name = member.name;
            let targetScore = 0, targetAtt = 0, targetTardy = 0, targetComp = 0;

            if (statsSelectedMonth === "전체") {
                for (let m = 1; m <= 12; m++) {
                    targetScore += userMonthlyData[name].score[m];
                    targetAtt   += userMonthlyData[name].att[m];
                    targetTardy += userMonthlyData[name].tardy[m];
                    targetComp  += userMonthlyData[name].comp[m];
                }
            } else {
                const mNum = parseInt(statsSelectedMonth.replace(/[^0-9]/g, ""), 10);
                targetScore = userMonthlyData[name].score[mNum];
                targetAtt   = userMonthlyData[name].att[mNum];
                targetTardy = userMonthlyData[name].tardy[mNum];
                targetComp  = userMonthlyData[name].comp[mNum];
            }

            // 💡 점수가 0점보다 큰 (활동 기록이 있는) 회원만 목록에 추가
            if (targetScore > 0) {
                displayList.push({ name, score: targetScore, att: targetAtt, tardy: targetTardy, comp: targetComp });
            }
        });

        if (displayList.length === 0) {
            statsDiv.innerHTML = "<div style='text-align:center; padding:30px; color:#94a3b8; font-weight:bold;'>해당 기간에 출석 기록이 있는 회원이 없습니다.</div>";
            return;
        }

        displayList.sort((a, b) => (b.score !== a.score) ? b.score - a.score : a.name.localeCompare(b.name));

        let currentRank = 1;
        displayList.forEach((item, index) => {
            if (index > 0 && item.score < displayList[index - 1].score) currentRank = index + 1;

            const card = document.createElement('div');
            card.className = 'rank-card';
            let rankBadge = (currentRank === 1 ? '🥇 1위' : (currentRank === 2 ? '🥈 2위' : (currentRank === 3 ? '🥉 3위' : `${currentRank}위`)));

            card.innerHTML = `
                <div class="rank-number">${rankBadge}</div>
                <div class="rank-name">${item.name}</div>
                <div class="rank-detail">출석${item.att} · 지각${item.tardy} · 대회${item.comp}</div>
                <div class="rank-score">${item.score}점</div>
            `;
            statsDiv.appendChild(card);
        });
    }

    function checkIn(name, score) {
        let already = globalLogs.find(l => l.name === name && l.date.trim() === selectedDateStr.trim() && Number(l.score) > 0);
        if (already) {
            alert(`[${name}]님은 이미 이날 출석이 완료되었습니다. 변경하려면 [취소] 후 다시 선택해 주세요.`);
            return;
        }
        let label = (score === 5) ? '지각(+5점)' : '출석(+10점)';
        if(!confirm(`[${selectedDateStr.replace(/^\d{4}년\s*/, '')}] [${name}]님을 [${label}]으로 기록하시겠습니까?`)) return;

        globalLogs = globalLogs.filter(l => !(l.name === name && l.date.trim() === selectedDateStr.trim()));
        let mMatch = selectedDateStr.match(/(\d+)월/);
        globalLogs.push({ date: selectedDateStr, name, month: mMatch ? parseInt(mMatch[1], 10) : 0, score });

        renderCheckinList();
        fetch(API_URL, {
            method: 'POST', mode: 'no-cors', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, score, date: selectedDateStr })
        }).catch(err => console.error(err));
    }

    function cancelCheckIn(name) {
        if(!confirm(`[${selectedDateStr.replace(/^\d{4}년\s*/, '')}] [${name}]님의 출석을 취소하시겠습니까?`)) return;

        globalLogs = globalLogs.filter(l => !(l.name === name && l.date.trim() === selectedDateStr.trim()));
        renderCheckinList();

        fetch(API_URL, {
            method: 'POST', mode: 'no-cors', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, score: 0, date: selectedDateStr })
        }).catch(err => console.error(err));
    }

    initCheckinMonthButtons();
    initStatsMonthButtons();
    loadData();
</script>

</body>
</html>
