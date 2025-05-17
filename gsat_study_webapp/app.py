import streamlit as st
import json
import os

DATA_FILE = 'study_data.json'
WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MEMBERS = ["혜진", "민희", "진희", "영민"]

def init_data():
    if not os.path.exists(DATA_FILE):
        data = {
            name: {"checks": [False] * 7, "memos": [""] * 7}
            for name in MEMBERS
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f)

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# 초기화
init_data()
data = load_data()

st.title("📅 GSAT 스터디 주간 체크")

# 사용자 선택
selected_member = st.selectbox("🙋‍♀️ 이름을 선택하세요", MEMBERS)

# 선택한 사용자 정보
user_data = data[selected_member]
st.subheader(f"📝 {selected_member}님의 주간 계획")

# 체크박스 및 메모 입력
checks = []
memos = []

for i, day in enumerate(WEEKDAYS):
    col1, col2 = st.columns([1, 4])
    with col1:
        checked = st.checkbox(day, value=user_data["checks"][i], key=f"check_{selected_member}_{i}")
    with col2:
        memo = st.text_input(f"{day} 메모", value=user_data["memos"][i], key=f"memo_{selected_member}_{i}")
    checks.append(checked)
    memos.append(memo)

# 저장 버튼
if st.button("💾 저장하기"):
    data[selected_member]["checks"] = checks
    data[selected_member]["memos"] = memos
    save_data(data)
    st.success("저장되었습니다! 🎉")

# 성공 횟수 표시
st.metric(label="✅ 달성한 요일 수", value=f"{checks.count(True)} / 7")

