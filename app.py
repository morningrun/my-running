from pathlib import Path
import re

src_path = Path("/mnt/data/붙여넣은 텍스트(1).txt")
html = src_path.read_text(encoding="utf-8")

# Add pending-state tracking after global variables.
needle = '    let globalLogs = [];\n'
addition = '''    let globalLogs = [];

    // 출석 저장 중인 회원·날짜 조합을 잠가 중복 클릭 방지
    const pendingCheckins = new Set();

    function getCheckinKey(name, date) {
        return strictYMD(date) + "|" + String(name).trim();
    }
'''
assert needle in html
html = html.replace(needle, addition, 1)

new_load = r'''    async function loadData() {
        const cacheBuster = Date.now();

        try {
            const response = await fetch(
                API_URL + "?action=load&t=" + cacheBuster,
                { method: "GET", cache: "no-store" }
            );

            if (!response.ok) throw new Error("서버 응답 오류");

            const data = await response.json();

            if (data.success === false) {
                throw new Error(data.message || "데이터 불러오기 실패");
            }

            globalMembers = Array.isArray(data.members) ? data.members : [];

            // 서버 데이터를 유일한 기준으로 사용합니다.
            // 로컬 배열과 병합하지 않아 취소 기록이 되살아나는 일을 방지합니다.
            globalLogs = Array.isArray(data.logs) ? data.logs : [];

            renderSaturdayVerticalList();

            if (!document.getElementById('tab-stats').classList.contains('hidden')) {
                renderStats();
            }

            return true;

        } catch (err) {
            console.error("데이터 로드 오류:", err);
            document.getElementById('member-list').innerHTML =
                "<div style='color:#e74c3c; text-align:center; padding:20px;'>데이터 연결 오류. 새로고침해 주세요.</div>";
            return false;
        }
    }'''
html, n = re.subn(r'    function loadData\(\) \{.*?\n    \}', new_load, html, count=1, flags=re.S)
assert n == 1, n

new_render = r'''    function renderCheckinList() {
        const listDiv = document.getElementById('member-list');
        listDiv.innerHTML = '';

        if (globalMembers.length === 0) {
            listDiv.innerHTML = "<div style='text-align:center; color:#888; padding:20px;'>등록된 회원이 없습니다.</div>";
            return;
        }

        const dayAttendance = {};
        const targetYMD = strictYMD(selectedDateStr);

        globalLogs.forEach(log => {
            if (log.date && strictYMD(log.date) === targetYMD && Number(log.score) > 0) {
                dayAttendance[String(log.name).trim()] = Number(log.score);
            }
        });

        globalMembers.forEach(member => {
            const name = String(member.name).trim();
            const score = dayAttendance[name] || 0;
            const isChecked = score > 0;
            const isPending = pendingCheckins.has(getCheckinKey(name, selectedDateStr));
            const isLocked = isChecked || isPending;

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
            } else if (isPending) {
                badgeHtml = '<span class="badge" style="background:#94a3b8; color:white;">저장 중</span>';
            }

            // HTML 속성에 회원명을 직접 삽입하지 않고 안전하게 이벤트를 연결합니다.
            const info = document.createElement('div');
            info.className = 'member-info';

            const nameDiv = document.createElement('div');
            nameDiv.className = 'member-name';
            nameDiv.textContent = name;

            const badgeDiv = document.createElement('div');
            badgeDiv.innerHTML = badgeHtml;

            info.appendChild(nameDiv);
            info.appendChild(badgeDiv);

            const buttonGroup = document.createElement('div');
            buttonGroup.className = 'btn-group';

            const makeButton = (label, buttonScore, className, disabled) => {
                const button = document.createElement('button');
                button.textContent = label;
                button.className = className || '';
                button.disabled = disabled;
                if (disabled) {
                    button.style.opacity = '0.6';
                    button.style.cursor = 'not-allowed';
                }
                button.addEventListener('click', () => handleCheckIn(name, buttonScore));
                buttonGroup.appendChild(button);
            };

            makeButton('출석(+10)', 10, score === 10 ? 'selected-10' : '', isLocked);
            makeButton('지각(+5)', 5, score === 5 ? 'selected-5' : '', isLocked);
            makeButton('대회(+10)', 99, score === 99 ? 'selected-comp' : '', isLocked);

            if (isChecked) {
                makeButton('취소', 0, 'btn-cancel', isPending);
            }

            card.appendChild(info);
            card.appendChild(buttonGroup);
            listDiv.appendChild(card);
        });
    }'''
html, n = re.subn(r'    function renderCheckinList\(\) \{.*?\n    \}', new_render, html, count=1, flags=re.S)
assert n == 1, n

new_handle = r'''    async function handleCheckIn(name, score) {
        const cleanName = String(name).trim();
        const targetDate = selectedDateStr;
        const targetYMD = strictYMD(targetDate);
        const key = getCheckinKey(cleanName, targetDate);

        // 같은 회원·날짜의 요청이 처리 중이면 추가 클릭 차단
        if (pendingCheckins.has(key)) return;

        const existing = globalLogs.find(log =>
            String(log.name).trim() === cleanName &&
            strictYMD(log.date) === targetYMD &&
            Number(log.score) > 0
        );

        if (score > 0 && existing) {
            alert(`[${cleanName}]님은 이미 출석 체크가 완료되었습니다.`);
            return;
        }

        if (score === 0) {
            if (!existing) return;

            if (!confirm(
                `[${targetDate.replace(/^\\d{4}년\\s*/, '')}] [${cleanName}]님의 출석을 취소하시겠습니까?`
            )) return;

        } else {
            const label = score === 5 ? '지각(+5점)' :
                          score === 99 ? '대회(+10점)' : '출석(+10점)';

            if (!confirm(
                `[${targetDate.replace(/^\\d{4}년\\s*/, '')}] [${cleanName}]님을 [${label}]으로 기록하시겠습니까?`
            )) return;
        }

        pendingCheckins.add(key);
        renderCheckinList();

        try {
            const params = new URLSearchParams({
                action: 'save',
                name: cleanName,
                score: String(score),
                date: targetDate,
                t: String(Date.now())
            });

            const response = await fetch(API_URL + '?' + params.toString(), {
                method: 'GET',
                cache: 'no-store'
            });

            if (!response.ok) throw new Error('서버 저장 요청 실패');

            const result = await response.json();

            if (!result.success) {
                throw new Error(result.message || '서버 저장 실패');
            }

            // 화면을 임의로 누적하지 않고 서버 저장 결과를 다시 읽습니다.
            const loaded = await loadData();
            if (!loaded) throw new Error('저장 후 서버 데이터 확인 실패');

            if (result.duplicate) {
                alert(`${cleanName}님은 이미 서버에 출석 기록이 있습니다.`);
            }

        } catch (err) {
            console.error('출석 저장 오류:', err);
            alert('서버 저장 또는 확인에 실패했습니다. 인터넷 연결과 서버를 확인해 주세요.');
            await loadData();

        } finally {
            pendingCheckins.delete(key);
            renderCheckinList();
        }
    }'''
html, n = re.subn(r'    function handleCheckIn\(name, score\) \{.*?\n    \}', new_handle, html, count=1, flags=re.S)
assert n == 1, n

# Keep the existing API URL; add a clear configuration comment.
html = html.replace(
    '    const API_URL = "https://script.google.com/macros/s/AKfycbzxSJMeaibxAkF9fZNOXgWuiVKY8ohYdFkEtX_Idj3gJbfVFQu1QCk-6G2isTUANpV-fQ/exec";',
    '    // Google Apps Script 웹 앱 배포 URL을 입력하세요.\n    const API_URL = "https://script.google.com/macros/s/AKfycbzxSJMeaibxAkF9fZNOXgWuiVKY8ohYdFkEtX_Idj3gJbfVFQu1QCk6G2isTUANpV-fQ/exec";'
)
# Correct exact URL back to source's known value (avoid accidental typo in explanatory replacement).
html = html.replace(
    'https://script.google.com/macros/s/AKfycbzxSJMeaibxAkF9fZNOXgWuiVKY8ohYdFkEtX_Idj3gJbfVFQu1QCk6G2isTUANpV-fQ/exec',
    'https://script.google.com/macros/s/AKfycbzxSJMeaibxAkF9fZNOXgWuiVKY8ohYdFkEtX_Idj3gJbfVFQu1QCk6G2isTUANpV-fQ/exec'
)
# The source URL is preserved verbatim if the above target didn't match.
if 'const API_URL = "https://script.google.com/macros/s/' not in html:
    raise ValueError("API_URL missing")

html_path = Path("/mnt/data/토달_출석부_전체_HTML.html")
html_path.write_text(html, encoding="utf-8")

gas = r'''/**
 * 토달 출석부 - Google Apps Script 서버 코드
 *
 * 스프레드시트 구성(첫 행은 제목):
 * 1) 회원 시트: A열 = 회원명 (A2부터 회원 이름)
 * 2) 출석기록 시트: A열 = 날짜, B열 = 회원명, C열 = 월, D열 = 점수
 *
 * 시트 이름이나 열 구성이 다르면 아래 상수와 열 번호를 실제 파일에 맞게 수정하세요.
 */

const MEMBER_SHEET_NAME = '회원';
const LOG_SHEET_NAME = '출석기록';

// 스프레드시트에 연결된 Apps Script 프로젝트라면 null 유지.
// 독립형 Apps Script라면 스프레드시트 ID를 입력하세요.
const SPREADSHEET_ID = null;

function getSpreadsheet_() {
  return SPREADSHEET_ID
    ? SpreadsheetApp.openById(SPREADSHEET_ID)
    : SpreadsheetApp.getActiveSpreadsheet();
}

function doGet(e) {
  const action = (e && e.parameter && e.parameter.action)
    ? e.parameter.action
    : 'load';

  try {
    if (action === 'load') return loadAttendance_();
    if (action === 'save') return saveAttendance_(e.parameter || {});

    return json_({
      success: false,
      message: '지원하지 않는 요청입니다.'
    });
  } catch (err) {
    return json_({
      success: false,
      message: String(err && err.message ? err.message : err)
    });
  }
}

function json_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function normalizeDate_(value) {
  if (value === null || value === undefined || value === '') return '';

  if (Object.prototype.toString.call(value) === '[object Date]' &&
      !isNaN(value.getTime())) {
    return Utilities.formatDate(
      value,
      Session.getScriptTimeZone(),
      'yyyy-M-d'
    );
  }

  const m = String(value).match(/(\d{4}).*?(\d+).*?(\d+)/);
  if (!m) return '';

  return Number(m[1]) + '-' + Number(m[2]) + '-' + Number(m[3]);
}

function loadAttendance_() {
  const ss = getSpreadsheet_();
  if (!ss) throw new Error('스프레드시트에 연결되지 않았습니다.');

  const memberSheet = ss.getSheetByName(MEMBER_SHEET_NAME);
  const logSheet = ss.getSheetByName(LOG_SHEET_NAME);

  if (!memberSheet) {
    throw new Error('회원 시트를 찾을 수 없습니다: ' + MEMBER_SHEET_NAME);
  }
  if (!logSheet) {
    throw new Error('출석기록 시트를 찾을 수 없습니다: ' + LOG_SHEET_NAME);
  }

  const memberLastRow = memberSheet.getLastRow();
  const members = memberLastRow >= 2
    ? memberSheet.getRange(2, 1, memberLastRow - 1, 1)
        .getDisplayValues()
        .flat()
        .map(v => String(v).trim())
        .filter(Boolean)
        .map(name => ({ name: name }))
    : [];

  const logLastRow = logSheet.getLastRow();
  let logs = [];

  if (logLastRow >= 2) {
    // getValues()를 사용해 날짜 셀이 날짜 형식이어도 표준화합니다.
    const rows = logSheet.getRange(2, 1, logLastRow - 1, 4).getValues();

    logs = rows
      .filter(row => row[0] !== '' && row[1] !== '')
      .map(row => ({
        date: normalizeDate_(row[0]),
        name: String(row[1]).trim(),
        month: Number(row[2]) || Number(normalizeDate_(row[0]).split('-')[1]) || 0,
        score: Number(row[3]) || 0
      }));
  }

  return json_({
    success: true,
    members: members,
    logs: logs
  });
}

function saveAttendance_(p) {
  const name = String(p.name || '').trim();
  const date = normalizeDate_(p.date);
  const score = Number(p.score);

  if (!name) throw new Error('회원명이 없습니다.');
  if (!date) throw new Error('날짜 형식이 올바르지 않습니다.');
  if ([0, 5, 10, 99].indexOf(score) === -1) {
    throw new Error('점수 값이 올바르지 않습니다.');
  }

  const lock = LockService.getScriptLock();
  lock.waitLock(30000);

  try {
    const ss = getSpreadsheet_();
    if (!ss) throw new Error('스프레드시트에 연결되지 않았습니다.');

    const sheet = ss.getSheetByName(LOG_SHEET_NAME);
    if (!sheet) throw new Error('출석기록 시트를 찾을 수 없습니다.');

    const lastRow = sheet.getLastRow();
    const matchingRows = [];

    if (lastRow >= 2) {
      const rows = sheet.getRange(2, 1, lastRow - 1, 4).getValues();

      rows.forEach((row, i) => {
        const rowDate = normalizeDate_(row[0]);
        const rowName = String(row[1] || '').trim();

        if (rowDate === date && rowName === name) {
          matchingRows.push(i + 2);
        }
      });
    }

    // 취소: 해당 회원·날짜의 기록을 전부 제거해 누적점수에서도 빠지게 합니다.
    if (score === 0) {
      matchingRows.sort((a, b) => b - a).forEach(rowNumber => {
        sheet.deleteRow(rowNumber);
      });

      return json_({
        success: true,
        cancelled: true,
        removed: matchingRows.length
      });
    }

    // 출석/지각/대회 어떤 유형이든 해당 날짜에 이미 기록이 있으면 중복 저장 금지.
    if (matchingRows.length > 0) {
      return json_({
        success: true,
        duplicate: true,
        message: '이미 해당 날짜의 출석 기록이 있습니다.'
      });
    }

    const month = Number(date.split('-')[1]);

    // 날짜를 문자열로 저장하여 지역/시간대에 따른 날짜 변형을 방지합니다.
    sheet.appendRow([date, name, month, score]);

    return json_({
      success: true,
      saved: true
    });

  } finally {
    lock.releaseLock();
  }
}
'''

gas_path = Path("/mnt/data/토달_출석부_Apps_Script_Code.gs")
gas_path.write_text(gas, encoding="utf-8")

print("생성 완료:")
print(html_path, html_path.stat().st_size, "bytes")
print(gas_path, gas_path.stat().st_size, "bytes")
