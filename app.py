import streamlit as st
import time

# 경고메시지 제거
st.set_page_config(page_title="My Streamlit App", layout="wide")

# 버튼 함수
# 각 버튼에 연결할 함수 정의
def add_function():
    st.write("ADD 버튼이 눌렸습니다!")

def refresh_function():
    st.write("REFRESH 버튼이 눌렸습니다!")

def combobox_function(selection):
    st.write(f"콤보박스 선택: {selection}")

def radiobox_function(selection):
    st.write(f"라디오 박스 선택: {selection}")

#다른 페이지

# 사이드바 메뉴
st.sidebar.title("사이드바입니다.")
if st.sidebar.button("메뉴 1"):
    st.write("사이드바의 메뉴 1 버튼이 눌렸습니다!")

if st.sidebar.button("메뉴 3"):
    st.write("사이드바의 메뉴 2 버튼이 눌렸습니다!")

if st.sidebar.button("메뉴 4"):
    st.write("사이드바의 메뉴 1 버튼이 눌렸습니다!")

if st.sidebar.button("메뉴 5"):
    st.write("사이드바의 메뉴 2 버튼이 눌렸습니다!")

# 상단의 버튼들
st.write("### ")
st.write("### 이곳은 김종호의 공간입니다.")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("ADD"):
        add_function()

with col2:
    if st.button("REFRESH"):
        refresh_function()

with col3:
    combobox_selection = st.selectbox("콤보박스", ["옵션 1", "옵션 2", "옵션 3"], key='combobox')
    combobox_function(combobox_selection)

with col4:
    radiobox_selection = st.radio("라디오 박스", ["옵션 A", "옵션 B"], key='radiobox')
    radiobox_function(radiobox_selection)

# 데이터 테이블 표시
st.write("### ")
st.write("DATA TABLE 표시")
data = {
    '열1': [1, 2, 4],
    '열2': [4, 5, 6],
    '열3': [7, 8, 9]
}
st.table(data)

