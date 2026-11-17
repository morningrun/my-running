<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>복사골 통합 접수시스템</title>
    
    <!-- 카카오톡 대회/행사 접수 미리보기 -->
    <meta property="og:title" content="복사골 통합 접수시스템">
    <meta property="og:description" content="복사골 통합 접수시스템에서 대회 및 행사 참가 현황을 확인하세요!">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://morningrun.github.io/boksakol_TOTAL/">
    <meta property="og:image" content="https://morningrun.github.io/boksakol_TOTAL/BOKSAKOL_TOTAL.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">

    <!-- 스마트폰 홈 화면 추가 아이콘 및 앱 설정 -->
    <link rel="apple-touch-icon" href="https://morningrun.github.io/boksakol_TOTAL/BOKSAKOL_TOTAL.png">
    <link rel="icon" type="image/png" href="https://morningrun.github.io/boksakol_TOTAL/BOKSAKOL_TOTAL.png">
    <link rel="manifest" href="./manifest.json">

    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="theme-color" content="#1e293b">

    <style>
        :root {
            --primary: #0f172a;        
            --accent: #2563eb;          
            --accent-hover: #1d4ed8;
            --success: #059669;        
            --danger: #dc2626;          
            --bg-color: #f8fafc;       
            --card-bg: #ffffff;
            --text-main: #1e293b;
            --text-sub: #334155;        
            --border: #cbd5e1;
        }

        html {
            scroll-behavior: smooth;
        }

        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg-color); margin: 0; padding: 10px; color: var(--text-main); -webkit-tap-highlight-color: transparent; }
        .container { max-width: 650px; margin: 0 auto; background: var(--card-bg); padding: 18px; border-radius: 16px; box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06); border: 1px solid #e2e8f0; }
        
        .main-title-box { text-align: center; margin: 6px 0 14px 0; }
        .main-title { font-size: 1.6rem; font-weight: 800; color: var(--primary); letter-spacing: -0.5px; }

        .sticky-tab-group {
            position: sticky;
            top: 0;
            z-index: 100;
            background: var(--card-bg);
            padding-top: 4px;
            padding-bottom: 8px;
        }

        .tab-group { display: flex; gap: 6px; background: #cbd5e1; padding: 4px; border-radius: 12px; backdrop-filter: blur(8px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        .tab-btn { flex: 1; padding: 11px 4px; font-size: 0.85rem; border: none; background: transparent; color: var(--text-sub); font-weight: 700; border-radius: 9px; cursor: pointer; transition: all 0.2s; text-align: center; white-space: nowrap; }
        .tab-btn.active { background: var(--card-bg); color: var(--accent); box-shadow: 0 3px 10px rgba(0,0,0,0.08); font-weight: 800; }

        .search-box { margin-bottom: 8px; }
        .search-input { width: 100%; padding: 7px 10px; font-size: 0.85rem; border: 1.5px solid var(--border); border-radius: 8px; background: #ffffff; outline: none; box-sizing: border-box; transition: border-color 0.2s; font-weight: 600; }
        .search-input:focus { border-color: var(--accent); }

        .content-card-box { background: #f8fafc; border: 1.5px solid #cbd5e1; border-radius: 14px; padding: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.02); }
        .race-content-card-box { background: #eff6ff; border: 1.5px solid #bfdbfe; border-radius: 14px; padding: 14px; margin-bottom: 16px; box-shadow: 0 2px 6px rgba(37,99,235,0.04); }

        .swipe-wrapper { overflow: hidden; width: 100%; position: relative; transition: height 0.2s ease-out; }
        .swipe-container { display: flex; width: 300%; transition: transform 0.25s cubic-bezier(0.25, 1, 0.5, 1); will-change: transform; align-items: flex-start; }
        
        .swipe-pane { width: 33.3333%; flex-shrink: 0; box-sizing: border-box; opacity: 0; transition: opacity 0.15s ease; pointer-events: none; height: 0; overflow: hidden; padding: 0; background: transparent; border: none; }
        .swipe-pane.active-pane { opacity: 1; pointer-events: auto; height: auto; overflow: visible; }

        #race-card-container { display: flex; flex-direction: column; gap: 8px; }

        .race-card-item { 
            background: #ffffff; 
            border: 2px solid #cbd5e1; 
            border-radius: 12px; 
            overflow: hidden; 
            transition: transform 0.35s cubic-bezier(0.25, 1, 0.5, 1), border-color 0.3s ease, background-color 0.3s ease, box-shadow 0.3s ease; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.02); 
            will-change: transform;
        }
        
        .race-card-item.selected-target { 
            border-color: var(--accent) !important; 
            box-shadow: 0 6px 16px rgba(37,99,235,0.12); 
            background: #f8fafc; 
        }

        .race-card-item:not(.selected-target) {
            border-color: #d1d5db !important;
            background: #fcfcfc;
            opacity: 0.9;
        }
        .race-card-item:not(.selected-target):hover {
            opacity: 1;
            border-color: #9ca3af !important;
        }

        .race-card-item.ended-race { 
            background: #f1f5f9 !important; 
            border-color: #cbd5e1 !important; 
            opacity: 0.75; 
        }
        .race-card-item.ended-race .race-card-header {
            background: #e2e8f0 !important;
        }
        
        .race-card-header { padding: 12px 14px; display: flex; justify-content: space-between; align-items: center; cursor: pointer; user-select: none; background: #ffffff; }
        .race-card-item.selected-target .race-card-header { background: #eff6ff; }
        .race-card-item:not(.selected-target) .race-card-header { background: #fafafa; }

        .race-card-title-area { font-size: 1.02rem; font-weight: 800; display: flex; align-items: center; gap: 6px; line-height: 1.3; color: #1e293b; flex-wrap: wrap; }
        
        .badge-type-race { font-size: 0.76rem; padding: 2px 8px; border-radius: 6px; font-weight: 800; background: #dbeafe; color: #1d4ed8; border: 1px solid #bfdbfe; }
        .badge-type-event { font-size: 0.76rem; padding: 2px 8px; border-radius: 6px; font-weight: 800; background: #fae8ff; color: #86198f; border: 1px solid #f5d0fe; }

        .status-badge { font-size: 0.72rem; padding: 2px 7px; border-radius: 6px; font-weight: 800; white-space: nowrap; background: #f1f5f9; color: #64748b; border: 1px solid #cbd5e1; }
        .status-badge.active-badge { background: #dcfce7; color: #15803d; border: 1px solid #86efac; }
        .status-badge.ended { background: #e2e8f0; color: #475569; border: 1px solid #cbd5e1; }

        .dday-badge { font-size: 0.72rem; padding: 2px 7px; border-radius: 6px; font-weight: 800; white-space: nowrap; background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; }
        .dday-badge.d-day { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }

        .race-toggle-icon { font-size: 0.8rem; color: #64748b; transition: transform 0.2s ease; flex-shrink: 0; padding-left: 8px; }
        .race-card-item.expanded .race-toggle-icon { transform: rotate(180deg); }

        .race-card-body { padding: 0 14px 12px 14px; display: none; border-top: 1px solid #e2e8f0; margin-top: 2px; padding-top: 10px; background: #ffffff; }
        .race-card-item.expanded .race-card-body { display: flex; flex-direction: column; gap: 4px; }
        .race-card-item.ended-race.expanded .race-card-body { background: #f1f5f9; }

        .ended-section-container { margin-top: 10px; border: 2px dashed #94a3b8; border-radius: 12px; background: #ffffff; overflow: hidden; padding: 6px; }
        .ended-section-header { padding: 10px 12px; display: flex; justify-content: space-between; align-items: center; cursor: pointer; font-weight: 800; font-size: 0.9rem; color: #475569; background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 8px; user-select: none; }
        .ended-section-body { padding: 8px 4px 4px 4px; display: none; flex-direction: column; gap: 6px; }
        .ended-section-container.expanded .ended-section-body { display: flex; }
        .ended-section-container.expanded .ended-toggle-icon { transform: rotate(180deg); }

        .member-card { display: flex; flex-direction: column; padding: 4px 8px; margin-bottom: 3px; background: #ffffff; border: 1.5px solid var(--border); border-radius: 6px; gap: 2px; box-shadow: 0 1px 2px rgba(0,0,0,0.02); }
        .member-info { display: flex; justify-content: space-between; align-items: center; gap: 4px; min-height: 22px; }
        .member-name-area { font-weight: 800; font-size: 0.85rem; color: var(--primary); display: flex; align-items: center; gap: 4px; overflow: hidden; }
        
        .applied-badge { font-size: 0.68rem; padding: 1px 5px; border-radius: 4px; font-weight: 800; display: inline-flex; align-items: center; gap: 2px; white-space: nowrap; }
        .applied-badge.style-full { background: #f3e8ff; color: #6b21a8; border: 1px solid #e9d5ff; }
        .applied-badge.style-half { background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }
        .applied-badge.style-10k { background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; }
        .applied-badge.style-5k { background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
        .applied-badge.style-attend { background: #e0f2fe; color: #0284c7; border: 1px solid #bae6fd; }
        .applied-badge.style-family { background: #f3e8ff; color: #9333ea; border: 1px solid #e9d5ff; }
        .applied-badge.style-etc { background: #fce7f3; color: #be185d; border: 1px solid #fbcfe8; }

        .btn-group { display: flex; gap: 3px; width: 100%; flex-wrap: wrap; margin-bottom: 2px; }
        .btn-group button { flex: 1; min-width: 60px; padding: 3px 2px; font-size: 0.72rem; border: 1.5px solid var(--border); border-radius: 4px; cursor: pointer; font-weight: 800; text-align: center; }
        
        .style-full { color: #6b21a8 !important; }
        .style-half { color: #b45309 !important; }
        .style-10k { color: #0369a1 !important; }
        .style-5k { color: #15803d !important; }
        .style-attend { color: #0284c7 !important; }         
        .style-family { color: #9333ea !important; }         
        .style-etc { color: #be185d !important; }

        .course-btn-style { background: #ffffff; color: var(--text-main); border-color: #cbd5e1; }
        .course-btn-style:hover { background: #f8fafc; border-color: var(--accent); color: var(--accent); }

        button.selected-course { font-weight: 800; flex: 1.5 !important; cursor: default; font-size: 0.72rem !important; background: rgba(255,255,255,0.95); padding: 3px 2px !important; }
        button.btn-cancel { background: #fef2f2 !important; color: var(--danger) !important; border-color: #fecaca !important; font-weight: 800; flex: 0.5 !important; padding: 3px 2px !important; }

        .admin-panel { background: var(--primary); color: white; padding: 16px; border-radius: 14px; margin-top: 24px; margin-bottom: 12px; box-shadow: 0 10px 25px rgba(15, 23, 42, 0.2); }
        .admin-panel h3 { margin: 12px 0 8px 0; font-size: 0.95rem; color: #38bdf8; }
        .admin-input-group { display: flex; flex-direction: column; gap: 6px; margin-bottom: 10px; }
        .admin-input-group input, .admin-input-group select { padding: 9px 12px; border-radius: 8px; border: none; font-size: 0.88rem; outline: none; }
        
        .course-setting-grid { display: flex; flex-direction: column; gap: 6px; background: #1e293b; padding: 12px; border-radius: 10px; border: 1px solid #334155; margin-bottom: 6px; }
        .course-row { display: flex; align-items: center; justify-content: space-between; gap: 8px; font-size: 0.82rem; font-weight: 700; }
        .course-row label { display: flex; align-items: center; gap: 6px; cursor: pointer; min-width: 70px; }
        .course-row input[type="text"] { padding: 4px 8px; border-radius: 4px; border: 1px solid #475569; background: #0f172a; color: white; font-size: 0.8rem; text-align: right; width: 90px; }
        
        .race-admin-row, .member-admin-row { background: #1e293b; padding: 10px; border-radius: 8px; margin-bottom: 8px; border: 1px solid #334155; display: flex; justify-content: space-between; align-items: center; }
        
        .excel-down-btn { background: var(--success); color: white; border: none; width: 100%; padding: 12px; border-radius: 8px; font-weight: 800; cursor: pointer; font-size: 0.95rem; margin-top: 10px; box-shadow: 0 4px 12px rgba(5,150,105,0.25); transition: background 0.2s; }
        .excel-down-btn:hover { background: #047857; }
        .sync-loading { text-align: center; font-size: 0.82rem; color: var(--accent); font-weight: 800; margin-bottom: 8px; }

        .footer-setting-box { display: flex; justify-content: flex-end; margin-top: 24px; padding-top: 14px; border-top: 1.5px solid var(--border); }
        .admin-gear-icon-btn { background: #ffffff; border: 1.5px solid var(--border); font-size: 1.2rem; cursor: pointer; padding: 8px; color: var(--text-sub); border-radius: 50%; transition: all 0.2s; box-shadow: 0 2px 5px rgba(0,0,0,0.03); }
        .admin-gear-icon-btn:hover { background: #f1f5f9; color: var(--accent); border-color: var(--accent); }

        .hidden { display: none; }
    </style>
</head>
<body>

<div class="container">
    <div class="main-title-box">
        <div class="main-title">복사골 통합 접수시스템</div>
        <div id="sync-status" class="sync-loading" style="display:none;"></div>
    </div>
    
    <!-- 1. 안내 카드 영역 -->
    <div class="race-content-card-box" id="race-selector-wrapper">
        <div id="race-card-container"></div>
    </div>

    <!-- 2. 탭 버튼 영역 (상단 고정 Sticky) -->
    <div class="sticky-tab-group">
        <div class="tab-group">
            <button class="tab-btn active" id="tab-status-btn">접수 현황</button>
            <button class="tab-btn" id="tab-apply-btn">참가 신청</button>
            <button class="tab-btn" id="tab-members-btn">전체 회원현황</button>
        </div>
    </div>

    <!-- 3. 패널 영역 -->
    <div class="content-card-box">
        <div class="swipe-wrapper" id="swipe-wrapper" style="height: auto;">
            <div id="swipe-container" class="swipe-container">
                <!-- 1번 패널: 접수 현황 -->
                <div class="swipe-pane active-pane" id="pane-status">
                    <div id="status-summary-box" style="margin-bottom: 8px;"></div>
                    <div class="search-box">
                        <input type="text" id="status-search-input" class="search-input" placeholder="🔍 신청자 이름 검색 (예: 홍길동)" oninput="renderStatusTab()">
                    </div>
                    <div id="status-detail-list" style="margin-top: 6px;"></div>
                </div>
                <!-- 2번 패널: 참가 신청 -->
                <div class="swipe-pane" id="pane-apply">
                    <div class="search-box">
                        <input type="text" id="apply-search-input" class="search-input" placeholder="🔍 회원 이름 검색 (예: 홍길동)" oninput="renderMemberList()">
                    </div>
                    <div id="member-list-wrapper"></div>
                </div>
                <!-- 3번 패널: 전체 회원현황 -->
                <div class="swipe-pane" id="pane-members">
                    <div id="member-stats-summary"></div>
                    <div class="search-box" style="margin-top: 10px;">
                        <input type="text" id="members-search-input" class="search-input" placeholder="🔍 전체 회원 이름 검색 (예: 홍길동)" oninput="renderAllMembersTab()">
                    </div>
                    <div id="all-member-list-wrapper" style="margin-top: 10px;"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- 관리자 통합 패널 -->
    <div id="admin-panel" class="admin-panel hidden">
        <h3>통합 관리자 설정 (마라톤 대회 및 행사 관리)</h3>
        
        <div style="background:#1e293b; padding:12px; border-radius:10px; border:1px solid #334155; margin-bottom:14px;">
            <h3 style="margin:0 0 8px 0; color:#38bdf8;">현재 선택 항목 신청자 명부 엑셀 다운로드</h3>
            <button class="excel-down-btn" id="excel-down-action-btn" style="margin-top:0;">현재 선택된 항목 엑셀(CSV) 다운로드</button>
        </div>

        <h3 id="race-form-title" style="margin-top:6px;">새 항목 등록 (마라톤 대회 / 행사)</h3>
        <div class="admin-input-group">
            <input type="hidden" id="edit-race-id" value="">
            
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                <label style="font-size:0.85rem; font-weight:700; color:#38bdf8;">등록 구분:</label>
                <select id="new-item-type" onchange="toggleItemTypeFields()" style="flex:1; padding:7px; border-radius:6px; background:#0f172a; color:white; font-weight:700;">
                    <option value="race">🏃‍♂️ 마라톤 대회</option>
                    <option value="event">🎉 일반 행사 (송년회, 야유회 등)</option>
                </select>
            </div>

            <input type="text" id="new-race-name" placeholder="명칭 (예: 2026 삼척황영조마라톤 / 송년의 밤 행사)">
            <input type="text" id="new-race-location" placeholder="장소 (예: 삼척시민운동장 / 대회의실)">
            <input type="text" id="new-race-date" placeholder="일자 및 요일 (예: 2026.04.13(일))">
            <input type="text" id="new-race-deadline" placeholder="마감일 (예: 2026.03.15까지 / 선착순 / 미지정)">
            
            <div style="display:flex; align-items:center; gap:8px; margin-top:4px;">
                <label style="font-size:0.85rem; font-weight:700; color:#38bdf8;">진행 상태:</label>
                <select id="new-race-status" style="padding:6px 10px; border-radius:6px; background:#0f172a; color:white; font-weight:700;">
                    <option value="자동(날짜기준)">자동 (대회일 지나면 자동 종료)</option>
                    <option value="강제마감">🔴 강제 접수마감 (조기마감/선착순완료)</option>
                    <option value="진행중">항상 진행중 (수동)</option>
                    <option value="종료">완전 종료 (대회 종료)</option>
                </select>
            </div>
            
            <!-- 마라톤 코스 설정 영역 -->
            <div id="race-course-setting-wrapper">
                <div style="font-size:0.82rem; font-weight:700; color:#38bdf8; margin-top:6px;">마라톤 코스 및 참가비 설정</div>
                <div class="course-setting-grid">
                    <div class="course-row">
                        <label><input type="checkbox" class="race-course-chk" value="5km" checked> 5km</label>
                        <input type="text" id="price-5km" placeholder="참가비" value="50,000">
                    </div>
                    <div class="course-row">
                        <label><input type="checkbox" class="race-course-chk" value="10km" checked> 10km</label>
                        <input type="text" id="price-10km" placeholder="참가비" value="50,000">
                    </div>
                    <div class="course-row">
                        <label><input type="checkbox" class="race-course-chk" value="하프" checked> 하프</label>
                        <input type="text" id="price-half" placeholder="참가비" value="50,000">
                    </div>
                    <div class="course-row">
                        <label><input type="checkbox" class="race-course-chk" value="풀코스" checked> 풀코스</label>
                        <input type="text" id="price-full" placeholder="참가비" value="50,000">
                    </div>
                    <div class="course-row">
                        <label><input type="checkbox" class="race-course-chk" value="기타1" id="chk-custom-1"> 기타1:</label>
                        <input type="text" id="custom-course-1-name" placeholder="명칭" style="width:70px; text-align:left;" disabled>
                        <input type="text" id="price-custom-1" placeholder="참가비" value="50,000" disabled>
                    </div>
                    <div class="course-row">
                        <label><input type="checkbox" class="race-course-chk" value="기타2" id="chk-custom-2"> 기타2:</label>
                        <input type="text" id="custom-course-2-name" placeholder="명칭" style="width:70px; text-align:left;" disabled>
                        <input type="text" id="price-custom-2" placeholder="참가비" value="50,000" disabled>
                    </div>
                </div>
            </div>

            <!-- 일반 행사 항목 설정 영역 -->
            <div id="event-option-setting-wrapper" class="hidden">
                <div style="font-size:0.82rem; font-weight:700; color:#38bdf8; margin-top:6px;">행사 선택 항목 및 참가비 설정</div>
                <div class="course-setting-grid">
                    <div class="course-row">
                        <label><input type="checkbox" class="event-opt-chk" value="참석" checked> 기본1</label>
                        <input type="text" id="event-opt-1" value="참석" placeholder="항목명" style="width:110px; text-align:left;">
                        <input type="text" id="price-ev-1" value="0" placeholder="참가비">
                    </div>
                    <div class="course-row">
                        <label><input type="checkbox" class="event-opt-chk" value="참석(가족동반)" checked> 기본2</label>
                        <input type="text" id="event-opt-2" value="참석(가족동반)" placeholder="항목명" style="width:110px; text-align:left;">
                        <input type="text" id="price-ev-2" value="0" placeholder="참가비">
                    </div>
                    <div class="course-row">
                        <label><input type="checkbox" class="event-opt-chk" value="여분1" id="chk-ev-custom-1"> 기타1:</label>
                        <input type="text" id="ev-custom-1-name" placeholder="명칭" style="width:110px; text-align:left;" disabled>
                        <input type="text" id="price-ev-custom-1" placeholder="참가비" value="0" disabled>
                    </div>
                    <div class="course-row">
                        <label><input type="checkbox" class="event-opt-chk" value="여분2" id="chk-ev-custom-2"> 기타2:</label>
                        <input type="text" id="ev-custom-2-name" placeholder="명칭" style="width:110px; text-align:left;" disabled>
                        <input type="text" id="price-ev-custom-2" placeholder="참가비" value="0" disabled>
                    </div>
                </div>
            </div>

            <div style="display:flex; gap:6px; margin-top:6px;">
                <button id="race-save-btn" style="flex:1; background:#2563eb; color:white; border:none; padding:10px; border-radius:8px; font-weight:800; cursor:pointer;">항목 추가하기</button>
                <button id="race-cancel-btn" style="background:#475569; color:white; border:none; padding:10px 12px; border-radius:8px; font-weight:800; cursor:pointer; display:none;">취소</button>
            </div>
        </div>

        <h3 style="margin-top:14px;">등록된 대회 및 행사 목록 관리 (수정/삭제)</h3>
        <div id="admin-race-list"></div>

        <h3 style="margin-top:16px;">신규 회원 직접 추가</h3>
        <div class="admin-input-group">
            <input type="text" id="admin-add-name" placeholder="이름">
            <input type="text" id="admin-add-phone" placeholder="핸드폰번호 (예: 010-0000-0000)">
            <input type="text" id="admin-add-birth" placeholder="생년월일 (예: 68.08.10)">
            <select id="admin-add-gender">
                <option value="남">남성</option>
                <option value="여">여성</option>
            </select>
            <input type="text" id="admin-add-join" placeholder="가입년월 (예: 07년 5월)">
            <select id="admin-add-size">
                <option value="90">90호</option>
                <option value="95" selected>95호</option>
                <option value="100">100호</option>
                <option value="105">105호</option>
                <option value="110">110호</option>
            </select>
            <button id="member-add-btn" style="background:#059669; color:white; border:none; padding:10px; border-radius:8px; font-weight:800; cursor:pointer;">회원 등록하기</button>
        </div>

        <h3 style="margin-top:16px;">전체 회원 정보 관리 (수정/삭제)</h3>
        <div id="admin-member-list" style="max-height:250px; overflow-y:auto; margin-top:6px;"></div>

        <h3 style="margin-top:16px;">관리자 비밀번호 변경</h3>
        <div style="display:flex; gap:6px;">
            <input type="password" id="new-admin-password" placeholder="새 비밀번호 입력" style="flex:1; padding:9px; border-radius:8px; border:none;">
            <button id="pwd-change-btn" style="background:#059669; color:white; border:none; padding:9px 12px; border-radius:8px; font-weight:800; cursor:pointer;">변경</button>
        </div>

        <button id="admin-close-btn" style="width:100%; margin-top:16px; background:#475569; color:white; border:none; padding:11px; border-radius:8px; cursor:pointer; font-weight:800;">관리자 설정 닫기</button>
    </div>

    <!-- 하단 오른쪽 구석 톱니바퀴 아이콘 -->
    <div class="footer-setting-box">
        <button class="admin-gear-icon-btn" id="admin-open-btn" title="관리자 설정">⚙️</button>
    </div>
</div>

<script>
    const API_URL = "https://script.google.com/macros/s/AKfycbxk2ZwIvgIc6FtzgrmF63V_YicWzLawgWL5gBshtfHT4yopmdsFHo_t0HsAIY8tKvJN/exec";

    let globalMembers = [];
    let globalRaces = [];
    let globalApplications = {};
    let adminPassword = "1234";
    let selectedRaceId = localStorage.getItem('boksagol_selected_race_v25') || "";
    let activePaneIndex = 0;

    const courseRank = { "풀코스": 1, "하프": 2, "10km": 3, "5km": 4, "참석(가족동반)": 1, "참석": 2, "불참": 3 };

    function getCourseRank(course) {
        if (!course) return 99;
        for (let key in courseRank) {
            if (course.includes(key)) return courseRank[key];
        }
        return 5;
    }

    function getCourseStyleClass(course) {
        if (!course) return '';
        if (course.includes('풀코스')) return 'style-full';
        if (course.includes('하프')) return 'style-half';
        if (course.includes('10k')) return 'style-10k';
        if (course.includes('5k')) return 'style-5k';
        if (course.includes('참석(가족동반)')) return 'style-family';  
        if (course.includes('참석')) return 'style-attend';             
        return 'style-etc';
    }

    function parseCourses(coursesStr) {
        if (!coursesStr) return [];
        let rawList = coursesStr.split(',');
        let result = [];
        let temp = "";
        
        rawList.forEach(item => {
            item = item.trim();
            if (!item) return; 
            if (temp) {
                temp += ", " + item;
            } else {
                temp = item;
            }
            let openCount = (temp.match(/\(/g) || []).length;
            let closeCount = (temp.match(/\)/g) || []).length;
            if (openCount === closeCount) {
                result.push(temp);
                temp = "";
            }
        });
        if (temp) result.push(temp);
        return result.filter(c => c.trim().length > 0);
    }

    function calculateDDay(dateStr) {
        if (!dateStr) return "";
        const match = dateStr.match(/(\d{4})[./-](\d{1,2})[./-](\d{1,2})/);
        if (!match) return "";

        const year = parseInt(match[1], 10);
        const month = parseInt(match[2], 10) - 1;
        const day = parseInt(match[3], 10);

        const targetDate = new Date(year, month, day);
        targetDate.setHours(0, 0, 0, 0);

        const today = new Date();
        today.setHours(0, 0, 0, 0);

        const diffTime = targetDate - today;
        const diffDays = Math.round(diffTime / (1000 * 60 * 60 * 24));

        if (diffDays === 0) return "D-Day";
        if (diffDays > 0) return `D-${diffDays}`;
        return `D+${Math.abs(diffDays)}`;
    }

    function calculateAge(member) {
        let birthStr = member.birth;
        if (!birthStr || birthStr === "-" || birthStr === "undefined" || birthStr === "null") return null;
        let clean = String(birthStr).replace(/[^0-9]/g, "");
        if (clean.length < 6) return null;

        let yy = parseInt(clean.substring(0, 2), 10);
        let mm = parseInt(clean.substring(2, 4), 10) || 1;
        let dd = parseInt(clean.substring(4, 6), 10) || 1;

        let fullYear = yy >= 50 ? 1900 + yy : 2000 + yy;

        const today = new Date();
        let currentYear = today.getFullYear();
        let currentMonth = today.getMonth() + 1;
        let currentDay = today.getDate();

        let age = currentYear - fullYear;
        if (currentMonth < mm || (currentMonth === mm && currentDay < dd)) {
            age--;
        }
        return age;
    }

    function calculateAgeGroup(member) {
        let age = calculateAge(member);
        if (age === null) return "기타/미지정";
        if (age < 30) return "기타/미지정";
        if (age < 40) return "30대";
        if (age < 50) return "40대";
        if (age < 60) return "50대";
        if (age < 70) return "60대";
        return "70대 이상";
    }

    function isRaceEnded(race) {
        const status = race.status || "";
        if (status === "강제마감" || status === "종료") return true;
        if (status === "진행중") return false;

        const name = race.name || "";
        if (name.includes("[종료]") || name.includes("종료")) return true;

        const dateStr = race.date || "";
        const match = dateStr.match(/(\d{4})[./-](\d{1,2})[./-](\d{1,2})/);
        if (match) {
            const year = parseInt(match[1], 10);
            const month = parseInt(match[2], 10) - 1;
            const day = parseInt(match[3], 10);
            const raceDate = new Date(year, month, day);

            const today = new Date();
            today.setHours(0, 0, 0, 0);

            raceDate.setDate(raceDate.getDate() + 1);
            if (today >= raceDate) {
                return true;
            }
        }
        return false;
    }

    async function fetchServerData(silent = false) {
        try {
            const response = await fetch(API_URL + "?action=getData");
            const data = await response.json();
            
            globalMembers = data.members || [];
            globalRaces = data.races || [];
            globalApplications = data.applications || {};
            
            if (data.adminPassword) {
                adminPassword = data.adminPassword;
            }

            if (globalRaces.length > 0 && !selectedRaceId) {
                const activeRaces = globalRaces.filter(r => !isRaceEnded(r));
                if (activeRaces.length > 0) {
                    selectedRaceId = activeRaces[0].id;
                } else {
                    selectedRaceId = globalRaces[0].id;
                }
            }

            refreshUI();
        } catch (error) {
            console.error("데이터 동기화 실패:", error);
        }
    }

    function refreshUI() {
        renderRaceCards();
        renderMemberList();
        renderStatusTab();
        renderAllMembersTab();
        updateSwipeWrapperHeight();
        if(!document.getElementById('admin-panel').classList.contains('hidden')) {
            renderAdminRaceList();
            renderAdminMemberList();
        }
    }

    function updateSwipeWrapperHeight() {
        requestAnimationFrame(() => {
            const wrapper = document.getElementById('swipe-wrapper');
            const panes = [
                document.getElementById('pane-status'),
                document.getElementById('pane-apply'),
                document.getElementById('pane-members')
            ];
            if (wrapper && panes[activePaneIndex]) {
                const targetPane = panes[activePaneIndex];
                const targetHeight = targetPane.scrollHeight;
                if (targetHeight > 0) {
                    wrapper.style.height = targetHeight + 'px';
                }
            }
        });
    }

    function switchTab(index) {
        activePaneIndex = index;
        const container = document.getElementById('swipe-container');
        
        document.getElementById('tab-status-btn').classList.remove('active');
        document.getElementById('tab-apply-btn').classList.remove('active');
        document.getElementById('tab-members-btn').classList.remove('active');

        document.getElementById('pane-status').classList.remove('active-pane');
        document.getElementById('pane-apply').classList.remove('active-pane');
        document.getElementById('pane-members').classList.remove('active-pane');

        if (index === 0) {
            container.style.transform = 'translateX(0%)';
            document.getElementById('tab-status-btn').classList.add('active');
            document.getElementById('pane-status').classList.add('active-pane');
            renderStatusTab();
        } else if (index === 1) {
            container.style.transform = 'translateX(-33.3333%)';
            document.getElementById('tab-apply-btn').classList.add('active');
            document.getElementById('pane-apply').classList.add('active-pane');
            renderMemberList();
        } else if (index === 2) {
            container.style.transform = 'translateX(-66.6666%)';
            document.getElementById('tab-members-btn').classList.add('active');
            document.getElementById('pane-members').classList.add('active-pane');
            renderAllMembersTab();
        }
        updateSwipeWrapperHeight();
    }

    function renderRaceCards() {
        const container = document.getElementById('race-card-container');
        if (!container) return;
        
        if (globalRaces.length === 0) {
            container.innerHTML = "<div style='font-size:0.85rem; color:#dc2626; font-weight:700; padding:6px;'>⚠️ 등록된 대회 및 행사가 없습니다. 관리자 설정(⚙️)에서 등록해주세요!</div>";
            return;
        }

        const prevRects = {};
        container.querySelectorAll('.race-card-item').forEach(el => {
            const id = el.getAttribute('data-race-id');
            if (id) prevRects[id] = el.getBoundingClientRect();
        });

        container.innerHTML = '';

        let sortedRaces = [...globalRaces].sort((a, b) => {
            if (a.id === selectedRaceId) return -1;
            if (b.id === selectedRaceId) return 1;
            return 0;
        });

        const activeRaces = [];
        const endedRaces = [];

        sortedRaces.forEach((race) => {
            if (isRaceEnded(race)) {
                endedRaces.push(race);
            } else {
                activeRaces.push(race);
            }
        });

        activeRaces.forEach((race) => {
            const card = createRaceCardElement(race, false);
            container.appendChild(card);
        });

        if (endedRaces.length > 0) {
            const endedSection = document.createElement('div');
            endedSection.className = 'ended-section-container';
            
            const tempWrapper = document.createElement('div');
            tempWrapper.style.display = 'flex';
            tempWrapper.style.flexDirection = 'column';
            tempWrapper.style.gap = '6px';

            endedRaces.forEach((race) => {
                const card = createRaceCardElement(race, true);
                tempWrapper.appendChild(card);
            });

            endedSection.innerHTML = `
                <div class="ended-section-header" onclick="this.parentElement.classList.toggle('expanded');">
                    <div style="display:flex; align-items:center; gap:6px;">
                        <span>🏁 종료된 목록 (${endedRaces.length}개)</span>
                    </div>
                    <div class="ended-toggle-icon" style="transition: transform 0.2s;">▼</div>
                </div>
            `;

            const bodyDiv = document.createElement('div');
            bodyDiv.className = 'ended-section-body';
            bodyDiv.appendChild(tempWrapper);
            endedSection.appendChild(bodyDiv);

            container.appendChild(endedSection);
        }

        requestAnimationFrame(() => {
            container.querySelectorAll('.race-card-item').forEach(el => {
                const id = el.getAttribute('data-race-id');
                if (prevRects[id]) {
                    const newRect = el.getBoundingClientRect();
                    const deltaY = prevRects[id].top - newRect.top;

                    if (deltaY !== 0) {
                        el.style.transform = `translateY(${deltaY}px)`;
                        el.style.transition = 'none';

                        requestAnimationFrame(() => {
                            el.style.transition = 'transform 0.4s cubic-bezier(0.25, 1, 0.5, 1), border-color 0.3s ease, background-color 0.3s ease, box-shadow 0.3s ease';
                            el.style.transform = 'translateY(0)';
                        });
                    }
                }
            });
        });
    }

    function createRaceCardElement(race, isEnded) {
        const card = document.createElement('div');
        const isSelected = (race.id === selectedRaceId);
        
        card.setAttribute('data-race-id', race.id);

        let cardClasses = ['race-card-item'];
        if (isEnded) cardClasses.push('ended-race');
        else cardClasses.push('active-race');
        
        if (isSelected) cardClasses.push('selected-target expanded');

        card.className = cardClasses.join(' ');
        
        let coursesHtml = '';
        if (race.courses) {
            const courseList = parseCourses(race.courses);
            courseList.forEach(c => {
                if(c.trim()) {
                    coursesHtml += `<div style="font-size: 0.82rem; font-weight: 700; color: #1e293b; margin-top: 2px;">- ${c}</div>`;
                }
            });
        }

        let badgeText = "진행중";
        let badgeClass = "active-badge";
        if (race.status === "강제마감") {
            badgeText = "강제마감";
            badgeClass = "ended";
        } else if (isEnded) {
            badgeText = "마감됨";
            badgeClass = "ended";
        }

        const badgeHtml = `<span class="status-badge ${badgeClass}">${badgeText}</span>`;

        const typeBadge = race.itemType === 'event' 
            ? `<span class="badge-type-event">🎉 행사</span>` 
            : `<span class="badge-type-race">🏃‍♂️ 대회</span>`;

        const ddayText = calculateDDay(race.date);
        let ddayBadgeHtml = "";
        if (ddayText) {
            const isDDay = (ddayText === "D-Day");
            ddayBadgeHtml = `<span class="dday-badge ${isDDay ? 'd-day' : ''}">${ddayText}</span>`;
        }

        card.innerHTML = `
            <div class="race-card-header">
                <div class="race-card-title-area">
                    ${badgeHtml}
                    ${typeBadge}
                    ${ddayBadgeHtml}
                    <span>${race.name}</span>
                </div>
                <div class="race-toggle-icon" style="transform: ${isSelected ? 'rotate(180deg)' : 'rotate(0deg)'};">▼</div>
            </div>
            <div class="race-card-body">
                <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.85rem; color: #1e293b; font-weight: 700;">
                    <div>• 일자: ${race.date}</div>
                    <div>• 장소: ${race.location || '장소 미정'}</div>
                    <div style="margin-top: 1px;">
                        <div>• 항목 및 참가비</div>
                        <div style="padding-left: 12px; margin-top: 1px;">
                            ${coursesHtml || '<div style="font-size: 0.82rem; color: #1e293b;">- 참석</div>'}
                        </div>
                    </div>
                    <div style="margin-top: 1px;">• 마감일: ${race.deadline}</div>
                </div>
            </div>
        `;
        
        const header = card.querySelector('.race-card-header');
        header.onclick = function(e) {
            e.stopPropagation();
            selectedRaceId = race.id;
            localStorage.setItem('boksagol_selected_race_v25', selectedRaceId);
            refreshUI();
        };

        return card;
    }

    function renderMemberList() {
        const wrapper = document.getElementById('member-list-wrapper');
        if (!wrapper) return;
        wrapper.innerHTML = '';

        if (globalRaces.length === 0 || !selectedRaceId) {
            wrapper.innerHTML = "<div style='text-align:center; padding:30px; color:#94a3b8; font-weight:700;'>관리자 모드에서 대회나 행사를 먼저 등록해주세요.</div>";
            updateSwipeWrapperHeight();
            return;
        }

        const currentRace = globalRaces.find(r => r.id === selectedRaceId);
        if (!currentRace) return;

        const ended = isRaceEnded(currentRace);
        if (ended) {
            const reason = currentRace.status === "강제마감" ? "관리자에 의해 강제 접수 마감된 항목입니다." : "접수 기한이 마감되었거나 종료된 항목입니다.";
            wrapper.innerHTML = `<div style='text-align:center; padding:12px; color:#dc2626; font-weight:700; background:#fef2f2; border-radius:6px; margin-bottom:8px; font-size:0.82rem;'>🔒 ${reason}</div>`;
        }

        const raceApps = globalApplications[selectedRaceId] || {};
        const availableCourses = parseCourses(currentRace.courses).map(c => c.replace(/\s*\(.*?\)/g, "").trim()).filter(c => c.length > 0);

        const searchInput = document.getElementById('apply-search-input');
        const keyword = searchInput ? searchInput.value.trim().toLowerCase() : "";

        const courseGroups = {};
        availableCourses.forEach(c => courseGroups[c] = []);
        const unappliedMembers = [];

        globalMembers.forEach(member => {
            const name = String(member.name || "").trim();
            if (keyword && !name.toLowerCase().includes(keyword)) return;

            const appliedCourseRaw = raceApps[name];
            if (appliedCourseRaw) {
                const cleanCourse = appliedCourseRaw.replace(/\s*\(.*?\)/g, "").trim();
                if (courseGroups[cleanCourse]) {
                    courseGroups[cleanCourse].push(member);
                } else {
                    if (availableCourses.length > 0) {
                        courseGroups[availableCourses[0]].push(member);
                    }
                }
            } else {
                if (!keyword) {
                    unappliedMembers.push(member);
                }
            }
        });

        let htmlContent = "";

        availableCourses.forEach(courseName => {
            const membersInCourse = courseGroups[courseName] || [];
            if (membersInCourse.length === 0 && keyword) return;

            const badgeStyle = getCourseStyleClass(courseName);

            htmlContent += `
                <div style="margin-bottom: 12px; background: #f8fafc; border: 1.5px solid #cbd5e1; border-radius: 10px; padding: 8px;">
                    <div style="font-weight: 800; font-size: 0.9rem; color: var(--primary); margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1.5px solid #cbd5e1; padding-bottom: 4px;">
                        <span class="${badgeStyle}">• ${courseName}</span>
                        <span style="font-size: 0.75rem; background: #e2e8f0; color: #334155; padding: 1px 6px; border-radius: 4px;">${membersInCourse.length}명</span>
                    </div>
            `;

            if (membersInCourse.length === 0) {
                htmlContent += `<div style="text-align:center; padding:8px; color:#94a3b8; font-size:0.8rem;">신청자가 없습니다.</div>`;
            } else {
                membersInCourse.sort((a, b) => a.name.localeCompare(b.name, 'ko'));

                membersInCourse.forEach((member, index) => {
                    const appliedCourse = raceApps[member.name];
                    const cardStyleClass = getCourseStyleClass(appliedCourse);
                    const displayApplied = appliedCourse.replace(/\s*\(.*?원\)/g, "").trim();
                    
                    let btnGroupHtml = `<div class="btn-group">`;

                    // [안전장치] 이미 접수한 회원은 실수로 취소하지 못하도록 고정 확정 표시
                    if (!ended) {
                        btnGroupHtml += `
                            <button class="selected-course ${cardStyleClass}" style="flex: 2 !important; background: #f0fdf4; border-color: #86efac; color: #15803d;" disabled>✅ 최종 신청완료 (확정)</button>
                        `;
                    } else {
                        btnGroupHtml += `<button class="selected-course ${cardStyleClass}" style="flex: 2 !important;" disabled>신청완료 (접수 마감됨)</button>`;
                    }
                    btnGroupHtml += `</div>`;

                    htmlContent += `
                        <div class="member-card">
                            <div class="member-info">
                                <div class="member-name-area">
                                    <span style="color:#64748b; font-weight:700; min-width:18px;">${index + 1}.</span> 
                                    <strong style="font-size:0.85rem; white-space:nowrap;">${member.name}</strong>
                                </div>
                                <div><span class="applied-badge ${cardStyleClass}">✅ ${displayApplied}</span></div>
                            </div>
                            ${btnGroupHtml}
                        </div>
                    `;
                });
            }

            htmlContent += `</div>`;
        });

        if (!keyword && unappliedMembers.length > 0) {
            unappliedMembers.sort((a, b) => a.name.localeCompare(b.name, 'ko'));
            
            htmlContent += `
                <div style="margin-top: 16px; background: transparent; border: 1.5px solid #cbd5e1; border-radius: 10px; padding: 8px;">
                    <div style="font-weight: 800; font-size: 0.9rem; color: #475569; margin-bottom: 6px; border-bottom: 1.5px solid #cbd5e1; padding-bottom: 4px;">
                        • 미신청 회원 (${unappliedMembers.length}명)
                    </div>
            `;

            const availableCoursesWithPrice = parseCourses(currentRace.courses);

            unappliedMembers.forEach((member, index) => {
                let btnGroupHtml = `<div class="btn-group">`;
                if (!ended) {
                    availableCoursesWithPrice.forEach(courseWithPrice => {
                        if(!courseWithPrice.trim()) return;
                        let displayBtnText = courseWithPrice.replace(/\s*\(.*?원\)/g, "").trim();
                        btnGroupHtml += `<button class="course-btn-style" onclick="confirmAndApply('${member.name}', '${courseWithPrice}')">${displayBtnText}</button>`;
                    });
                } else {
                    btnGroupHtml += `<button style="background:#f1f5f9; color:#dc2626; font-weight:800;" disabled>접수 마감됨</button>`;
                }
                btnGroupHtml += `</div>`;

                htmlContent += `
                    <div class="member-card" style="background:#ffffff;">
                        <div class="member-info">
                            <div class="member-name-area">
                                <span style="color:#94a3b8; font-weight:700; min-width:18px;">${index + 1}.</span> 
                                <strong style="font-size:0.85rem; white-space:nowrap;">${member.name}</strong>
                            </div>
                            <div><span style="font-size:0.68rem; background:#f1f5f9; color:#64748b; padding:1px 4px; border-radius:4px; font-weight:700;">미신청</span></div>
                        </div>
                        ${btnGroupHtml}
                    </div>
                `;
            });

            htmlContent += `</div>`;
        }

        wrapper.innerHTML = htmlContent;
        updateSwipeWrapperHeight();
    }

    function confirmAndApply(memberName, courseWithPrice) {
        const currentRace = globalRaces.find(r => r.id === selectedRaceId);
        if (!currentRace || isRaceEnded(currentRace)) return;

        let message = "";
        const isEvent = (currentRace.itemType === 'event');

        let cleanCourseName = courseWithPrice.replace(/\s*\(.*?원\)/g, "").trim();
        if (isEvent) {
            message = `[${currentRace.name}]\n\n${memberName}님을 [${cleanCourseName}] 항목으로 참석(신청)하시겠습니까?`;
        } else {
            message = `[${currentRace.name}]\n\n${memberName}님을 [${cleanCourseName}] 코스로 참가 신청하시겠습니까?`;
        }

        if (confirm(message)) {
            handleApply(memberName, courseWithPrice);
        }
    }

    async function handleApply(memberName, course) {
        const currentRace = globalRaces.find(r => r.id === selectedRaceId);
        if (!currentRace || isRaceEnded(currentRace)) {
            alert("접수가 마감되어 신청할 수 없습니다.");
            return;
        }

        if (!globalApplications[selectedRaceId]) {
            globalApplications[selectedRaceId] = {};
        }

        globalApplications[selectedRaceId][memberName] = course;

        refreshUI();

        try {
            const url = `${API_URL}?action=applyRace&raceId=${encodeURIComponent(selectedRaceId)}&memberName=${encodeURIComponent(memberName)}&course=${encodeURIComponent(course)}`;
            fetch(url);
        } catch(e) {
            console.error("서버 반영 오류:", e);
        }
    }

    function renderStatusTab() {
        const summaryBox = document.getElementById('status-summary-box');
        const detailList = document.getElementById('status-detail-list');

        if (!summaryBox || !detailList) return;
        summaryBox.innerHTML = '';
        detailList.innerHTML = '';

        if (globalRaces.length === 0 || !selectedRaceId) {
            summaryBox.innerHTML = "<div style='text-align:center; padding:30px; color:#94a3b8; font-weight:700;'>등록된 항목이 없습니다.</div>";
            updateSwipeWrapperHeight();
            return;
        }

        const currentRace = globalRaces.find(r => r.id === selectedRaceId);
        if (!currentRace) return;

        const raceApps = globalApplications[selectedRaceId] || {};
        const totalCount = Object.keys(raceApps).length;

        const availableCourses = parseCourses(currentRace.courses).map(c => {
            return c.replace(/\s*\(.*?\)/g, "").trim();
        }).filter(c => c.length > 0);

        const searchInput = document.getElementById('status-search-input');
        const keyword = searchInput ? searchInput.value.trim().toLowerCase() : "";

        const courseGroups = {};
        availableCourses.forEach(c => courseGroups[c] = []);

        Object.keys(raceApps).forEach(memberName => {
            if (keyword && !memberName.toLowerCase().includes(keyword)) {
                return;
            }
            let course = raceApps[memberName];
            if (course) {
                course = course.replace(/\s*\(.*?\)/g, "").trim();
                if (!courseGroups[course]) {
                    courseGroups[course] = [];
                }
                courseGroups[course].push(memberName);
            }
        });

        let activeCourses = availableCourses.filter(cName => {
            return (courseGroups[cName] || []).length > 0;
        });

        if (activeCourses.length === 0) {
            activeCourses = availableCourses;
        }

        let courseSummaryTextArr = [];
        activeCourses.forEach(cName => {
            let cCount = (courseGroups[cName] || []).length;
            courseSummaryTextArr.push(`${cName} ${cCount}명`);
        });
        let courseSummaryStr = `(${courseSummaryTextArr.join(' / ')})`;

        let summaryHtml = `
            <div style="background: transparent; border: none; padding: 2px 8px; text-align: center; margin-bottom: 2px;">
                <div style="font-weight: 800; font-size: 1.0rem; color: var(--primary); margin-bottom: 2px;">[${currentRace.name}]</div>
                <div style="font-size: 0.92rem; font-weight: 700; color: #1e293b; margin-bottom: 2px;">
                    총신청인원 <strong style="color: var(--accent); font-size: 1.1rem;">${totalCount}</strong>명
                </div>
                <div style="font-size: 0.8rem; font-weight: 700; color: #334155;">
                    ${courseSummaryStr}
                </div>
            </div>
        `;
        summaryBox.innerHTML = summaryHtml;

        let detailHtml = `<div style="font-weight:800; font-size:0.9rem; margin-top:4px; margin-bottom:4px; color:var(--primary);">항목별 신청 현황</div>`;
        detailHtml += `<div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(105px, 1fr)); gap:6px;">`;

        activeCourses.forEach(courseName => {
            const membersInCourse = courseGroups[courseName] || [];
            if (membersInCourse.length === 0) return;

            const badgeStyle = getCourseStyleClass(courseName);

            let membersTagsHtml = "";
            membersInCourse.sort((a, b) => a.localeCompare(b, 'ko')).forEach((mName, idx) => {
                membersTagsHtml += `
                    <div style="display:flex; align-items:center; background:#ffffff; border:1px solid #cbd5e1; padding:3px 5px; border-radius:4px; font-size:0.77rem; font-weight:800; color:var(--text-main); margin-bottom:2px;">
                        <span style="color:#64748b; font-weight:700; min-width:16px;">${idx + 1}.</span> 
                        <span style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${mName}</span>
                    </div>
                `;
            });

            detailHtml += `
                <div style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:8px; padding:6px; display:flex; flex-direction:column; gap:4px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1.5px solid #e2e8f0; padding-bottom:3px;">
                        <span style="font-weight:800; font-size:0.8rem;" class="${badgeStyle}">• ${courseName}</span>
                        <span style="font-size:0.68rem; font-weight:800; background:#e2e8f0; color:#334155; padding:1px 4px; border-radius:3px;">${membersInCourse.length}명</span>
                    </div>
                    <div style="display:flex; flex-direction:column; gap:2px;">
                        ${membersTagsHtml}
                    </div>
                </div>
            `;
        });

        detailHtml += `</div>`;
        detailList.innerHTML = detailHtml;
        updateSwipeWrapperHeight();
    }

    function renderAllMembersTab() {
        const summaryBox = document.getElementById('member-stats-summary');
        const listWrapper = document.getElementById('all-member-list-wrapper');
        if (!summaryBox || !listWrapper) return;

        const totalCount = globalMembers.length;
        let maleCount = 0, femaleCount = 0;
        const ageGroupCounts = { "30대": 0, "40대": 0, "50대": 0, "60대": 0, "70대 이상": 0, "기타/미지정": 0 };
        let unassignedMembers = [];
        let totalAgeSum = 0;
        let validAgeCount = 0;

        globalMembers.forEach(m => {
            if (m.gender === "남") maleCount++;
            else if (m.gender === "여") femaleCount++;

            let age = calculateAge(m);
            if (age !== null) {
                totalAgeSum += age;
                validAgeCount++;
            }

            let group = calculateAgeGroup(m);
            if (ageGroupCounts[group] !== undefined) {
                ageGroupCounts[group]++;
            } else {
                ageGroupCounts["기타/미지정"]++;
                unassignedMembers.push(m.name);
            }
        });

        const averageAge = validAgeCount > 0 ? (totalAgeSum / validAgeCount).toFixed(1) : "0.0";
        const now = new Date();
        const baseDateString = `${now.getFullYear()}년 ${now.getMonth() + 1}월 현재 기준`;

        let ageGridHtml = "";
        const targetAgeGroups = ["30대", "40대", "50대", "60대", "70대 이상", "기타/미지정"];
        
        targetAgeGroups.forEach(ag => {
            let count = ageGroupCounts[ag] || 0;
            let isDanger = (ag === "기타/미지정" && count > 0);
            ageGridHtml += `
                <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:6px; padding:5px 4px; text-align:center; display:flex; flex-direction:column; gap:1px;">
                    <div style="font-size:0.71rem; font-weight:700; color:var(--text-sub);">${ag}</div>
                    <div style="font-size:0.9rem; font-weight:800; color:${isDanger ? 'var(--danger)' : 'var(--primary)'};">${count}명</div>
                </div>
            `;
        });

        let unassignedAlertHtml = "";
        if (unassignedMembers.length > 0) {
            unassignedAlertHtml = `
                <div style="background:#fee2e2; border:1.5px solid #fca5a5; border-radius:6px; padding:6px 8px; margin-top:4px; font-size:0.78rem; color:#991b1b; font-weight:700; line-height:1.3; text-align:left;">
                    ⚠️ 생년월일 미지정 회원 (${unassignedMembers.length}명): <span style="font-weight:800; color:#b91c1c;">${unassignedMembers.join(', ')}</span>
                </div>
            `;
        }

        summaryBox.innerHTML = `
            <div style="display:flex; flex-direction:column; gap:6px; margin-bottom:2px;">
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:6px;">
                    <div class="stat-box" style="background:#ffffff; border:1.5px solid var(--border); padding:8px; text-align:center; border-radius:8px;">
                        <div class="stat-box-title" style="font-size:0.78rem; color:var(--text-sub); font-weight:800;">총 회원수</div>
                        <div class="stat-box-val" style="font-size:1.15rem; color:var(--accent); font-weight:800;">${totalCount}명</div>
                    </div>
                    <div class="stat-box" style="background:#ffffff; border:1.5px solid var(--border); padding:8px; text-align:center; border-radius:8px;">
                        <div class="stat-box-title" style="font-size:0.78rem; color:var(--text-sub); font-weight:800;">성별 분포</div>
                        <div class="stat-box-val" style="font-size:0.98rem; color:var(--primary); font-weight:800;">남 ${maleCount} / 여 ${femaleCount}</div>
                    </div>
                </div>

                <div style="background:#ffffff; border:1.5px solid var(--border); border-radius:8px; padding:8px; text-align:center;">
                    <div style="font-size:0.8rem; font-weight:800; color:var(--primary); margin-bottom:1px;">연대별 인원 분포</div>
                    <div style="font-size:0.7rem; font-weight:700; color:var(--accent); margin-bottom:4px;">(${baseDateString} 만 나이 기준)</div>
                    <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:4px; margin-bottom:4px;">
                        ${ageGridHtml}
                    </div>
                    <div style="border-top:1.5px solid #e2e8f0; padding-top:4px; margin-top:3px; font-size:0.82rem; font-weight:800; color:var(--text-main);">
                        전체 회원 평균 나이: <span style="color:var(--accent); font-size:0.95rem;">만 ${averageAge}세</span>
                    </div>
                    ${unassignedAlertHtml}
                </div>
            </div>
        `;

        const searchInput = document.getElementById('members-search-input');
        const keyword = searchInput ? searchInput.value.trim().toLowerCase() : "";

        const filteredMembers = globalMembers.filter(m => {
            const name = String(m.name || "").trim();
            return name.toLowerCase().includes(keyword);
        });

        let listHtml = `<div style="font-weight:800; font-size:0.9rem; margin-bottom:4px; color:var(--primary);">회원 명부 검색 결과 (${filteredMembers.length}명)</div>`;

        if (filteredMembers.length === 0) {
            listHtml += `<div style='text-align:center; padding:15px; color:#64748b; font-weight:700; font-size:0.85rem;'>검색된 회원이 없습니다.</div>`;
        } else {
            filteredMembers.forEach((m, index) => {
                let age = calculateAge(m);
                let ageDisplay = age !== null ? `<span style="font-size:0.7rem; font-weight:700; color:#1d4ed8; background:#eff6ff; border:1px solid #bfdbfe; padding:1px 3px; border-radius:3px; margin-left:3px;">만 ${age}세</span>` : '';

                listHtml += `
                    <div style="display:flex; flex-direction:column; background:#ffffff; padding:6px 8px; border-radius:6px; margin-bottom:4px; border:1.5px solid #cbd5e1; gap:1px;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div style="display:flex; align-items:center; gap:4px; flex-wrap:wrap;">
                                <span style="color:#64748b; font-weight:700; min-width:18px;">${index + 1}.</span>
                                <strong style="font-size:0.88rem; color:var(--primary);">${m.name}</strong>
                                ${ageDisplay}
                            </div>
                            <div style="font-weight:800; color:var(--accent); background:#eff6ff; padding:1px 5px; border-radius:3px; font-size:0.7rem; white-space:nowrap;">
                                👕 ${m.size}호
                            </div>
                        </div>
                        <div style="font-size:0.72rem; color:#475569; font-weight:700; padding-left:22px; display:flex; gap:6px; flex-wrap:wrap; line-height:1.2;">
                            <span>생일: ${m.birth}</span>
                            <span>성별: ${m.gender}</span>
                            <span>연락처: ${m.phone}</span>
                            <span>가입: ${m.join}</span>
                        </div>
                    </div>
                `;
            });
        }

        listWrapper.innerHTML = listHtml;
        updateSwipeWrapperHeight();
    }

    function downloadExcel() {
        const currentRace = globalRaces.find(r => r.id === selectedRaceId);
        if (!currentRace) {
            alert("다운로드할 항목을 선택해주세요.");
            return;
        }

        const raceApps = globalApplications[selectedRaceId] || {};
        const appliedMembersList = globalMembers.filter(m => raceApps[m.name]);

        if (appliedMembersList.length === 0) {
            alert("신청한 회원이 없어 다운로드할 데이터가 없습니다.");
            return;
        }

        appliedMembersList.sort((a, b) => {
            const courseA = raceApps[a.name] || "";
            const courseB = raceApps[b.name] || "";
            const rankA = getCourseRank(courseA);
            const rankB = getCourseRank(courseB);
            
            if (rankA !== rankB) {
                return rankA - rankB;
            }
            return a.name.localeCompare(b.name, 'ko');
        });

        let csvContent = "\uFEFF번호,신청항목,이름,핸드폰번호,성별,옷사이즈,명칭\n";
        let courseCounts = {};

        appliedMembersList.forEach((m, idx) => {
            const rawCourse = raceApps[m.name] || "";
            let cleanCourse = rawCourse.replace(/\s*\(.*?원\)/g, "").trim();
            
            courseCounts[cleanCourse] = (courseCounts[cleanCourse] || 0) + 1;

            csvContent += `${idx + 1},${cleanCourse},${m.name},${m.phone},${m.gender},${m.size},${currentRace.name}\n`;
        });

        csvContent += `\n[코스별 합계 집계]\n`;
        for (let courseName in courseCounts) {
            csvContent += `${courseName},${courseCounts[courseName]}명,,,,,\n`;
        }
        csvContent += `전체 총인원,${appliedMembersList.length}명,,,,,\n`;

        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.setAttribute("href", url);
        link.setAttribute("download", `복사골통합접수_${currentRace.name}_신청명부.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    function toggleAdminMode() {
        const panel = document.getElementById('admin-panel');
        if (!panel) return;

        if (panel.classList.contains('hidden')) {
            const pwd = prompt("관리자 비밀번호를 입력하세요:");
            if (pwd === adminPassword) {
                panel.classList.remove('hidden');
                renderAdminRaceList();
                renderAdminMemberList();
                panel.scrollIntoView({ behavior: 'smooth' });
            } else if (pwd !== null) {
                alert("비밀번호가 틀렸습니다!");
            }
        } else {
            panel.classList.add('hidden');
        }
        updateSwipeWrapperHeight();
    }

    function toggleItemTypeFields() {
        const itemType = document.getElementById('new-item-type').value;
        const raceWrapper = document.getElementById('race-course-setting-wrapper');
        const eventWrapper = document.getElementById('event-option-setting-wrapper');

        if (itemType === 'event') {
            raceWrapper.classList.add('hidden');
            eventWrapper.classList.remove('hidden');
        } else {
            raceWrapper.classList.remove('hidden');
            eventWrapper.classList.add('hidden');
        }
    }

    function renderAdminRaceList() {
        const listDiv = document.getElementById('admin-race-list');
        if (!listDiv) return;
        listDiv.innerHTML = '';
        if (globalRaces.length === 0) {
            listDiv.innerHTML = "<div style='font-size:0.82rem; color:#94a3b8;'>등록된 항목이 없습니다.</div>";
            return;
        }

        globalRaces.forEach(race => {
            const ended = isRaceEnded(race);
            let statusLabel = "진행중(자동)";
            if (race.status === "강제마감") statusLabel = "🔴 강제마감됨";
            else if (race.status === "종료") statusLabel = "종료(수동)";
            else if (race.status === "진행중") statusLabel = "진행중(수동)";
            else if (ended) statusLabel = "종료(날짜지남)";

            const typeLabel = race.itemType === 'event' ? '[행사]' : '[대회]';

            const isForceClosed = (race.status === "강제마감");
            const toggleBtnText = isForceClosed ? "🟢 접수 재개하기" : "🔴 강제 접수마감";
            const toggleBtnBg = isForceClosed ? "#059669" : "#dc2626";

            const row = document.createElement('div');
            row.className = 'race-admin-row';
            row.innerHTML = `
                <div style="font-size:0.85rem;"><strong>${typeLabel} ${race.name}</strong> <span style="font-size:0.7rem; color:${isForceClosed?'#fca5a5':'#38bdf8'};">[${statusLabel}]</span><br><span style="font-size:0.72rem; color:#cbd5e1;">내용: ${race.courses}</span><br><span style="font-size:0.7rem; color:#94a3b8;">${race.date} / 마감: ${race.deadline}</span></div>
                <div style="display:flex; gap:4px; flex-direction:column; align-items:flex-end;">
                    <div style="display:flex; gap:4px;">
                        <button class="race-edit-btn" data-id="${race.id}" style="background:#2563eb; color:white; border:none; padding:4px 7px; border-radius:4px; cursor:pointer; font-size:0.72rem; font-weight:700;">수정</button>
                        <button class="race-del-btn" data-id="${race.id}" style="background:#475569; color:white; border:none; padding:4px 7px; border-radius:4px; cursor:pointer; font-size:0.72rem; font-weight:700;">삭제</button>
                    </div>
                    <button class="race-force-close-btn" data-id="${race.id}" style="background:${toggleBtnBg}; color:white; border:none; padding:4px 7px; border-radius:4px; cursor:pointer; font-size:0.72rem; font-weight:700; margin-top:2px;">${toggleBtnText}</button>
                </div>
            `;
            listDiv.appendChild(row);
        });

        listDiv.querySelectorAll('.race-edit-btn').forEach(btn => {
            btn.onclick = () => editRace(btn.getAttribute('data-id'));
        });
        listDiv.querySelectorAll('.race-del-btn').forEach(btn => {
            btn.onclick = () => removeRace(btn.getAttribute('data-id'));
        });
        listDiv.querySelectorAll('.race-force-close-btn').forEach(btn => {
            btn.onclick = () => toggleForceCloseRace(btn.getAttribute('data-id'));
        });
    }

    async function toggleForceCloseRace(raceId) {
        const race = globalRaces.find(r => r.id === raceId);
        if (!race) return;

        if (race.status === "강제마감") {
            race.status = "자동(날짜기준)";
            alert(`[${race.name}] 항목의 강제 마감이 해제되었습니다. (접수 재개)`);
        } else {
            race.status = "강제마감";
            alert(`[${race.name}] 항목이 강제 접수마감 처리되었습니다. (대회일정 유지, 신청 불가)`);
        }

        refreshUI();

        try {
            const url = `${API_URL}?action=saveRace&raceId=${encodeURIComponent(race.id)}&itemType=${encodeURIComponent(race.itemType || 'race')}&raceName=${encodeURIComponent(race.name)}&location=${encodeURIComponent(race.location || '')}&date=${encodeURIComponent(race.date)}&deadline=${encodeURIComponent(race.deadline)}&courses=${encodeURIComponent(race.courses)}&status=${encodeURIComponent(race.status)}`;
            fetch(url).then(() => fetchServerData(true));
        } catch(e) {
            console.error("강제마감 서버 저장 오류:", e);
        }
    }

    function editRace(raceId) {
        const race = globalRaces.find(r => r.id === raceId);
        if (!race) return;

        document.getElementById('edit-race-id').value = race.id;
        document.getElementById('new-item-type').value = race.itemType || 'race';
        toggleItemTypeFields();

        document.getElementById('new-race-name').value = race.name;
        document.getElementById('new-race-location').value = race.location || "";
        document.getElementById('new-race-date').value = race.date;
        document.getElementById('new-race-deadline').value = race.deadline;
        document.getElementById('new-race-status').value = race.status || "자동(날짜기준)";

        if (race.itemType === 'event') {
            const parts = parseCourses(race.courses || "");
            const chks = document.querySelectorAll('.event-opt-chk');
            chks.forEach(c => c.checked = false);
            document.getElementById('event-opt-1').value = "참석";
            document.getElementById('price-ev-1').value = "0";
            document.getElementById('event-opt-2').value = "참석(가족동반)";
            document.getElementById('price-ev-2').value = "0";
            document.getElementById('chk-ev-custom-1').checked = false;
            document.getElementById('ev-custom-1-name').value = "";
            document.getElementById('price-ev-custom-1').value = "0";
            document.getElementById('ev-custom-1-name').disabled = true;
            document.getElementById('price-ev-custom-1').disabled = true;
            document.getElementById('chk-ev-custom-2').checked = false;
            document.getElementById('ev-custom-2-name').value = "";
            document.getElementById('price-ev-custom-2').value = "0";
            document.getElementById('ev-custom-2-name').disabled = true;
            document.getElementById('price-ev-custom-2').disabled = true;

            parts.forEach((part, index) => {
                const match = part.match(/^(.+?)\s*\(([^)]+)\)$/);
                let pName = part.trim();
                let pPrice = "0";

                if (match) {
                    pName = match[1].trim();
                    pPrice = match[2].trim().replace("원", "");
                }

                if (index === 0) {
                    chks[0].checked = true;
                    document.getElementById('event-opt-1').value = pName;
                    document.getElementById('price-ev-1').value = pPrice;
                } else if (index === 1) {
                    chks[1].checked = true;
                    document.getElementById('event-opt-2').value = pName;
                    document.getElementById('price-ev-2').value = pPrice;
                } else if (index === 2) {
                    chks[2].checked = true;
                    document.getElementById('ev-custom-1-name').value = pName;
                    document.getElementById('ev-custom-1-name').disabled = false;
                    document.getElementById('price-ev-custom-1').value = pPrice;
                    document.getElementById('price-ev-custom-1').disabled = false;
                } else if (index === 3) {
                    chks[3].checked = true;
                    document.getElementById('ev-custom-2-name').value = pName;
                    document.getElementById('ev-custom-2-name').disabled = false;
                    document.getElementById('price-ev-custom-2').value = pPrice;
                    document.getElementById('price-ev-custom-2').disabled = false;
                }
            });
        } else {
            const chks = document.querySelectorAll('.race-course-chk');
            chks.forEach(chk => chk.checked = false);
            document.getElementById('price-5km').value = "50,000";
            document.getElementById('price-10km').value = "50,000";
            document.getElementById('price-half').value = "50,000";
            document.getElementById('price-full').value = "50,000";
            document.getElementById('custom-course-1-name').value = "";
            document.getElementById('custom-course-1-name').disabled = true;
            document.getElementById('price-custom-1').value = "50,000";
            document.getElementById('price-custom-1').disabled = true;
            document.getElementById('custom-course-2-name').value = "";
            document.getElementById('custom-course-2-name').disabled = true;
            document.getElementById('price-custom-2').value = "50,000";
            document.getElementById('price-custom-2').disabled = true;

            const parts = parseCourses(race.courses || "");
            parts.forEach(part => {
                const match = part.match(/^(.+?)\s*\(([^)]+)\)$/);
                let cName = part;
                let cPrice = "50,000";

                if (match) {
                    cName = match[1].trim();
                    cPrice = match[2].trim().replace("원", "");
                }

                let matched = false;
                chks.forEach(chk => {
                    if (chk.value === cName) {
                        chk.checked = true;
                        matched = true;
                        if (cName === '5km') document.getElementById('price-5km').value = cPrice;
                        if (cName === '10km') document.getElementById('price-10km').value = cPrice;
                        if (cName === '하프') document.getElementById('price-half').value = cPrice;
                        if (cName === '풀코스') document.getElementById('price-full').value = cPrice;
                    }
                });

                if (!matched) {
                    if (!document.getElementById('custom-course-1-name').value && !chks[4].checked) {
                        chks[4].checked = true;
                        document.getElementById('custom-course-1-name').value = cName;
                        document.getElementById('custom-course-1-name').disabled = false;
                        document.getElementById('price-custom-1').value = cPrice;
                        document.getElementById('price-custom-1').disabled = false;
                    } else if (!document.getElementById('custom-course-2-name').value && !chks[5].checked) {
                        chks[5].checked = true;
                        document.getElementById('custom-course-2-name').value = cName;
                        document.getElementById('custom-course-2-name').disabled = false;
                        document.getElementById('price-custom-2').value = cPrice;
                        document.getElementById('price-custom-2').disabled = false;
                    }
                }
            });
        }

        document.getElementById('race-form-title').textContent = "항목 정보 수정";
        document.getElementById('race-save-btn').textContent = "수정 완료하기";
        document.getElementById('race-cancel-btn').style.display = 'block';

        document.getElementById('admin-panel').scrollIntoView({ behavior: 'smooth' });
    }

    function resetRaceForm() {
        document.getElementById('edit-race-id').value = "";
        document.getElementById('new-item-type').value = "race";
        toggleItemTypeFields();
        document.getElementById('new-race-name').value = "";
        document.getElementById('new-race-location').value = "";
        document.getElementById('new-race-date').value = "";
        document.getElementById('new-race-deadline').value = "";
        document.getElementById('new-race-status').value = "자동(날짜기준)";
        
        const chks = document.querySelectorAll('.race-course-chk');
        chks.forEach((chk, idx) => {
            chk.checked = (idx < 4);
        });
        document.getElementById('price-5km').value = "50,000";
        document.getElementById('price-10km').value = "50,000";
        document.getElementById('price-half').value = "50,000";
        document.getElementById('price-full').value = "50,000";
        document.getElementById('custom-course-1-name').value = "";
        document.getElementById('custom-course-1-name').disabled = true;
        document.getElementById('price-custom-1').value = "50,000";
        document.getElementById('price-custom-1').disabled = true;
        document.getElementById('custom-course-2-name').value = "";
        document.getElementById('custom-course-2-name').disabled = true;
        document.getElementById('price-custom-2').value = "50,000";
        document.getElementById('price-custom-2').disabled = true;

        document.getElementById('event-opt-1').value = "참석";
        document.getElementById('price-ev-1').value = "0";
        document.getElementById('event-opt-2').value = "참석(가족동반)";
        document.getElementById('price-ev-2').value = "0";
        document.getElementById('chk-ev-custom-1').checked = false;
        document.getElementById('ev-custom-1-name').value = "";
        document.getElementById('price-ev-custom-1').value = "0";
        document.getElementById('ev-custom-1-name').disabled = true;
        document.getElementById('price-ev-custom-1').disabled = true;
        document.getElementById('chk-ev-custom-2').checked = false;
        document.getElementById('ev-custom-2-name').value = "";
        document.getElementById('price-ev-custom-2').value = "0";
        document.getElementById('ev-custom-2-name').disabled = true;
        document.getElementById('price-ev-custom-2').disabled = true;

        document.getElementById('race-form-title').textContent = "새 항목 등록 (마라톤 대회 / 행사)";
        document.getElementById('race-save-btn').textContent = "항목 추가하기";
        document.getElementById('race-cancel-btn').style.display = 'none';
    }

    async function saveRaceAction() {
        const raceId = document.getElementById('edit-race-id').value.trim();
        const itemType = document.getElementById('new-item-type').value;
        const name = document.getElementById('new-race-name').value.trim();
        const location = document.getElementById('new-race-location').value.trim();
        const date = document.getElementById('new-race-date').value.trim();
        const deadline = document.getElementById('new-race-deadline').value.trim();
        const status = document.getElementById('new-race-status').value;

        if (!name || !date) {
            alert("명칭과 일자는 필수 입력입니다.");
            return;
        }

        let selectedCourses = [];

        if (itemType === 'event') {
            const chks = document.querySelectorAll('.event-opt-chk');
            chks.forEach((chk, idx) => {
                if (chk.checked) {
                    let optName = "";
                    let optPrice = "0";

                    if (idx === 0) {
                        optName = document.getElementById('event-opt-1').value.trim() || "참석";
                        optPrice = document.getElementById('price-ev-1').value.trim() || "0";
                    } else if (idx === 1) {
                        optName = document.getElementById('event-opt-2').value.trim() || "참석(가족동반)";
                        optPrice = document.getElementById('price-ev-2').value.trim() || "0";
                    } else if (idx === 2) {
                        optName = document.getElementById('ev-custom-1-name').value.trim();
                        optPrice = document.getElementById('price-ev-custom-1').value.trim() || "0";
                    } else if (idx === 3) {
                        optName = document.getElementById('ev-custom-2-name').value.trim();
                        optPrice = document.getElementById('price-ev-custom-2').value.trim() || "0";
                    }

                    if (optName) {
                        selectedCourses.push(`${optName}(${optPrice}원)`);
                    }
                }
            });
        } else {
            const chks = document.querySelectorAll('.race-course-chk');
            chks.forEach((chk, idx) => {
                if (chk.checked) {
                    let courseName = "";
                    let coursePrice = "50,000";

                    if (idx === 0) {
                        courseName = "5km";
                        coursePrice = document.getElementById('price-5km').value.trim() || "50,000";
                    } else if (idx === 1) {
                        courseName = "10km";
                        coursePrice = document.getElementById('price-10km').value.trim() || "50,000";
                    } else if (idx === 2) {
                        courseName = "하프";
                        coursePrice = document.getElementById('price-half').value.trim() || "50,000";
                    } else if (idx === 3) {
                        courseName = "풀코스";
                        coursePrice = document.getElementById('price-full').value.trim() || "50,000";
                    } else if (idx === 4) {
                        courseName = document.getElementById('custom-course-1-name').value.trim();
                        coursePrice = document.getElementById('price-custom-1').value.trim() || "50,000";
                    } else if (idx === 5) {
                        courseName = document.getElementById('custom-course-2-name').value.trim();
                        coursePrice = document.getElementById('price-custom-2').value.trim() || "50,000";
                    }

                    if (courseName) {
                        selectedCourses.push(`${courseName}(${coursePrice}원)`);
                    }
                }
            });
        }

        if (selectedCourses.length === 0) {
            alert("최소 하나 이상의 항목을 선택해주세요.");
            return;
        }

        const coursesStr = selectedCourses.join(', ');

        if (!raceId) {
            const tempId = "race_" + Date.now();
            globalRaces.push({ id: tempId, itemType, name: name, location: location, date: date, deadline: deadline || "마감일 미정", courses: coursesStr, status: status });
            selectedRaceId = tempId;
        } else {
            const target = globalRaces.find(r => r.id === raceId);
            if (target) {
                target.itemType = itemType;
                target.name = name;
                target.location = location;
                target.date = date;
                target.deadline = deadline;
                target.courses = coursesStr;
                target.status = status;
            }
        }

        refreshUI();
        resetRaceForm();
        alert(raceId ? "정보가 수정되었습니다." : `[${name}] 항목이 성공적으로 등록되었습니다.`);

        try {
            const url = `${API_URL}?action=saveRace&raceId=${encodeURIComponent(raceId || '')}&itemType=${encodeURIComponent(itemType)}&raceName=${encodeURIComponent(name)}&location=${encodeURIComponent(location)}&date=${encodeURIComponent(date)}&deadline=${encodeURIComponent(deadline || "마감일 미정")}&courses=${encodeURIComponent(coursesStr)}&status=${encodeURIComponent(status)}`;
            fetch(url).then(() => fetchServerData(true));
        } catch(e) {
            console.error("서버 저장 오류:", e);
        }
    }

    async function removeRace(raceId) {
        if (!confirm("정말 이 항목을 삭제하시겠습니까? 신청된 기록도 함께 삭제됩니다.")) return;
        
        globalRaces = globalRaces.filter(r => r.id !== raceId);
        if (globalRaces.length > 0) selectedRaceId = globalRaces[0].id;
        else selectedRaceId = "";
        
        refreshUI();
        alert("항목이 삭제되었습니다.");

        try {
            const url = `${API_URL}?action=deleteRace&raceId=${encodeURIComponent(raceId)}`;
            fetch(url).then(() => fetchServerData(true));
        } catch(e) {
            console.error("서버 삭제 오류:", e);
        }
    }

    async function addNewMemberByAdmin() {
        const name = document.getElementById('admin-add-name').value.trim();
        const phone = document.getElementById('admin-add-phone').value.trim();
        const birth = document.getElementById('admin-add-birth').value.trim();
        const gender = document.getElementById('admin-add-gender').value;
        const join = document.getElementById('admin-add-join').value.trim();
        const size = document.getElementById('admin-add-size').value;

        if (!name) {
            alert("회원 이름은 필수 입력입니다.");
            return;
        }

        globalMembers.push({ name, phone: phone||"-", birth: birth||"-", gender, join: join||"-", size });
        refreshUI();

        document.getElementById('admin-add-name').value = '';
        document.getElementById('admin-add-phone').value = '';
        document.getElementById('admin-add-birth').value = '';
        document.getElementById('admin-add-join').value = '';
        alert(`[${name}] 회원이 추가되었습니다.`);

        try {
            const url = `${API_URL}?action=saveMember&oldName=${encodeURIComponent(name)}&name=${encodeURIComponent(name)}&phone=${encodeURIComponent(phone || "-")}&birth=${encodeURIComponent(birth || "-")}&gender=${encodeURIComponent(gender)}&join=${encodeURIComponent(join || "-")}&size=${encodeURIComponent(size)}`;
            fetch(url).then(() => fetchServerData(true));
        } catch(e) {
            console.error("회원 추가 서버 오류:", e);
        }
    }

    function renderAdminMemberList() {
        const listDiv = document.getElementById('admin-member-list');
        if (!listDiv) return;
        listDiv.innerHTML = '';

        if (globalMembers.length === 0) {
            listDiv.innerHTML = "<div style='font-size:0.8rem; color:#94a3b8; padding:6px;'>등록된 회원이 없습니다.</div>";
            return;
        }

        globalMembers.forEach(m => {
            const row = document.createElement('div');
            row.className = 'member-admin-row';
            row.innerHTML = `
                <div style="font-size:0.82rem;">
                    <strong>${m.name}</strong> (${m.gender}, ${m.birth}, 👕${m.size})<br>
                    <span style="font-size:0.7rem; color:#38bdf8;">📞 ${m.phone}</span> / <span style="font-size:0.7rem; color:#94a3b8;">가입: ${m.join}</span>
                </div>
                <div style="display:flex; gap:4px;">
                    <button class="member-edit-btn" data-name="${m.name}" style="background:#2563eb; color:white; border:none; padding:4px 8px; border-radius:4px; cursor:pointer; font-size:0.72rem; font-weight:700;">수정</button>
                    <button class="member-del-btn" data-name="${m.name}" style="background:#dc2626; color:white; border:none; padding:4px 8px; border-radius:4px; cursor:pointer; font-size:0.72rem; font-weight:700;">삭제</button>
                </div>
            `;
            listDiv.appendChild(row);
        });

        listDiv.querySelectorAll('.member-edit-btn').forEach(btn => {
            btn.onclick = () => editMember(btn.getAttribute('data-name'));
        });
        listDiv.querySelectorAll('.member-del-btn').forEach(btn => {
            btn.onclick = () => removeMember(btn.getAttribute('data-name'));
        });
    }

    async function editMember(oldName) {
        const m = globalMembers.find(item => item.name === oldName);
        if (!m) return;

        const newName = prompt("이름 수정:", m.name);
        if (newName === null) return;
        const newBirth = prompt("생년월일 수정 (예: 69.11.08):", m.birth);
        if (newBirth === null) return;
        const newPhone = prompt("핸드폰 번호 수정 (예: 010-1234-5678):", m.phone);
        if (newPhone === null) return;
        const newGender = prompt("성별 수정 (남 또는 여):", m.gender);
        if (newGender === null) return;
        const newSize = prompt("옷 사이즈 수정 (90, 95, 100, 105, 110 중 입력):", m.size);
        if (newSize === null) return;

        m.name = newName.trim() || m.name;
        m.birth = newBirth.trim() || m.birth;
        m.phone = newPhone.trim() || m.phone;
        m.gender = newGender.trim() || m.gender;
        m.size = newSize.trim() || m.size;

        refreshUI();
        alert("회원 정보가 수정되었습니다.");

        try {
            const url = `${API_URL}?action=saveMember&oldName=${encodeURIComponent(oldName)}&name=${encodeURIComponent(m.name)}&phone=${encodeURIComponent(m.phone)}&birth=${encodeURIComponent(m.birth)}&gender=${encodeURIComponent(m.gender)}&join=${encodeURIComponent(m.join)}&size=${encodeURIComponent(m.size)}`;
            fetch(url).then(() => fetchServerData(true));
        } catch(e) {
            console.error("회원 수정 서버 오류:", e);
        }
    }

    async function removeMember(name) {
        if (!confirm(`[${name}] 회원을 정말 명부에서 삭제하시겠습니까?`)) return;
        
        globalMembers = globalMembers.filter(m => m.name !== name);
        refreshUI();
        alert("회원이 삭제되었습니다.");

        try {
            const url = `${API_URL}?action=deleteMember&name=${encodeURIComponent(name)}`;
            fetch(url).then(() => fetchServerData(true));
        } catch(e) {
            console.error("회원 삭제 서버 오류:", e);
        }
    }

    async function changePassword() {
        const input = document.getElementById('new-admin-password');
        const newPwd = input ? input.value.trim() : "";
        if (!newPwd) {
            alert("새 비밀번호를 입력해주세요.");
            return;
        }
        if (confirm("관리자 비밀번호를 변경하시겠습니까?")) {
            adminPassword = newPwd;
            if (input) input.value = '';
            alert("관리자 비밀번호가 변경되었습니다.");

            try {
                const url = `${API_URL}?action=saveAdminPassword&password=${encodeURIComponent(newPwd)}`;
                await fetch(url);
                fetchServerData(true);
            } catch(e) {
                console.error("비밀번호 서버 저장 오류:", e);
            }
        }
    }

    function initEventBindings() {
        document.getElementById('tab-status-btn').onclick = () => switchTab(0);
        document.getElementById('tab-apply-btn').onclick = () => switchTab(1);
        document.getElementById('tab-members-btn').onclick = () => switchTab(2);
        
        document.getElementById('excel-down-action-btn').onclick = downloadExcel;
        
        document.getElementById('race-save-btn').onclick = saveRaceAction;
        document.getElementById('race-cancel-btn').onclick = resetRaceForm;
        
        document.getElementById('member-add-btn').onclick = addNewMemberByAdmin;
        document.getElementById('pwd-change-btn').onclick = changePassword;
        
        document.getElementById('admin-open-btn').onclick = toggleAdminMode;
        document.getElementById('admin-close-btn').onclick = toggleAdminMode;

        document.getElementById('chk-custom-1').onchange = () => toggleCustomInput('course', 1);
        document.getElementById('chk-custom-2').onchange = () => toggleCustomInput('course', 2);
        document.getElementById('chk-ev-custom-1').onchange = () => toggleCustomInput('event', 1);
        document.getElementById('chk-ev-custom-2').onchange = () => toggleCustomInput('event', 2);

        const swipeContainer = document.getElementById('swipe-container');
        let startX = 0;
        let isSwiping = false;

        swipeContainer.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            isSwiping = true;
        }, { passive: true });

        swipeContainer.addEventListener('touchend', (e) => {
            if (!isSwiping) return;
            isSwiping = false;

            let endX = e.changedTouches[0].clientX;
            let diff = startX - endX;

            if (Math.abs(diff) > 40) {
                if (diff > 0 && activePaneIndex < 2) {
                    switchTab(activePaneIndex + 1);
                } else if (diff < 0 && activePaneIndex > 0) {
                    switchTab(activePaneIndex - 1);
                }
            }
        });
    }

    function toggleCustomInput(type, num) {
        if (type === 'course') {
            const chk = document.getElementById(`chk-custom-${num}`);
            const nameInput = document.getElementById(`custom-course-${num}-name`);
            const priceInput = document.getElementById(`price-custom-${num}`);
            if (chk && nameInput && priceInput) {
                nameInput.disabled = !chk.checked;
                priceInput.disabled = !chk.checked;
                if (chk.checked) nameInput.focus();
            }
        } else if (type === 'event') {
            const chk = document.getElementById(`chk-ev-custom-${num}`);
            const nameInput = document.getElementById(`ev-custom-${num}-name`);
            const priceInput = document.getElementById(`price-ev-custom-${num}`);
            if (chk && nameInput && priceInput) {
                nameInput.disabled = !chk.checked;
                priceInput.disabled = !chk.checked;
                if (chk.checked) nameInput.focus();
            }
        }
    }

    function initApp() {
        initEventBindings();
        fetchServerData(false);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initApp);
    } else {
        initApp();
    }
</script>

</body>
</html>
