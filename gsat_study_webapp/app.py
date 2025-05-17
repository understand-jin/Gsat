import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MEMBERS = ["혜진", "민희", "진희", "영민"]

# 구글 시트 연결 함수
def connect_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("GSAT App").sheet1  # 시트 이름
    return sheet

# 시트에 저장하는 함수
def save_to_sheet(name, checks, memos):
    sheet = connect_gsheet()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for i in range(7):
        sheet.append_row([name, WEEKDAYS[i], checks[i], memos[i], now])

# Streamlit UI
st.title("📅 GSAT 스터디 주간 체크")
selected_member = st.selectbox("🙋‍♀️ 이름을 선택하세요", MEMBERS)

checks = []
memos = []
for i, day in enumerate(WEEKDAYS):
    col1, col2 = st.columns([1, 4])
    with col1:
        checked = st.checkbox(day, key=f"check_{i}")
    with col2:
        memo = st.text_input(f"{day} 메모", key=f"memo_{i}")
    checks.append(checked)
    memos.append(memo)

if st.button("💾 저장하기"):
    save_to_sheet(selected_member, checks, memos)
    st.success("✅ Google Sheets에 저장 완료!")
