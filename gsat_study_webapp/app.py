import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client

# 🔐 Supabase 연결 정보
SUPABASE_URL = "https://qdnjyjbyibdfrxydtrgn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFkbmp5amJ5aWJkZnJ4eWR0cmduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc0ODc2MjUsImV4cCI6MjA2MzA2MzYyNX0.c46vVrMNUUVOyYmbAzqsWbO7U83_12HQYrCQx-qBxaM"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 📅 요일과 사용자 리스트
WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MEMBERS = ["혜진", "민희", "진희", "영민"]

# ✅ Supabase에서 데이터 불러오기
def load_from_supabase(name):
    res = supabase.table("study_check").select("*").eq("name", name).execute()
    rows = res.data if res.data else []

    checks = []
    memos = []

    for day in WEEKDAYS:
        record = next((r for r in rows if r["day"] == day and r["name"] == name), None)
        if record:
            checks.append(record.get("checked", False))
            memos.append(record.get("memo", ""))
        else:
            checks.append(False)
            memos.append("")
    return checks, memos

# ✅ Supabase에 데이터 저장
def save_to_supabase(name, checks, memos):
    # 기존 기록 삭제
    supabase.table("study_check").delete().eq("name", name).execute()

    # 새 기록 삽입
    for i, day in enumerate(WEEKDAYS):
        supabase.table("study_check").insert({
            "name": name,
            "day": day,
            "checked": checks[i],
            "memo": memos[i],
            "timestamp": datetime.now().isoformat()
        }).execute()

# ✅ UI 시작
st.title("📅 GSAT 스터디 주간 체크")

# 사용자 선택
selected_member = st.selectbox("🙋‍♀️ 이름을 선택하세요", MEMBERS)

# 데이터 불러오기
checks, memos = load_from_supabase(selected_member)
st.subheader(f"📝 {selected_member}님의 주간 계획")

# 체크박스 및 메모 입력
updated_checks = []
updated_memos = []

for i, day in enumerate(WEEKDAYS):
    col1, col2 = st.columns([1, 4])
    with col1:
        checked = st.checkbox(day, value=checks[i], key=f"check_{selected_member}_{i}")
    with col2:
        memo = st.text_input(f"{day} 메모", value=memos[i], key=f"memo_{selected_member}_{i}")
    updated_checks.append(checked)
    updated_memos.append(memo)

# 저장 버튼
if st.button("💾 저장하기"):
    save_to_supabase(selected_member, updated_checks, updated_memos)
    st.success("저장되었습니다! 🎉")

# 성공 횟수 표시
st.metric(label="✅ 달성한 요일 수", value=f"{updated_checks.count(True)} / 7")
