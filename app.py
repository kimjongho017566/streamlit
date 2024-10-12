import streamlit as st
from datetime import datetime, date
import pandas as pd

# 경고메시지 제거 및 아이콘 및 페이지 이름 설정
st.set_page_config(
    page_title="환영해요",  # 페이지 이름 설정
    page_icon="🌟",  # 원하는 아이콘 이모지 또는 이미지 경로 설정
    layout="wide"
)

# 스타일 설정
st.markdown("""
    <style>
    .main-title {
        font-size:50px !important;
        color: #000000; /* 검정색 */
        text-align: center;
        font-weight: bold;
        font-family: 'Arial', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🌟공간에 오신 것을 환영합니다 🌟</p>', unsafe_allow_html=True)
st.markdown("[여기를 눌러 Manual로 이동하세요](https://github.com/)")

# 초기 세션 상태 설정
if "current_page" not in st.session_state:
    st.session_state.current_page = "데이터 검색"
    st.session_state.saved_data = pd.DataFrame()  # 저장된 데이터를 위한 빈 데이터프레임 초기화

# 사이드바에 버튼 추가
st.sidebar.markdown("### 페이지 선택")
if st.sidebar.button("홈"):
    st.session_state.current_page = "홈"
if st.sidebar.button("데이터 검색"):
    st.session_state.current_page = "데이터 검색"
if st.sidebar.button("기타 정보"):
    st.session_state.current_page = "기타 정보"

# 페이지에 따른 콘텐츠 표시
if st.session_state.current_page == "홈":
    st.write("홈 페이지에 오신 것을 환영합니다!")
    st.write("여기에서 전체 개요와 안내를 확인할 수 있습니다.")

elif st.session_state.current_page == "데이터 검색":

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        combo_menu = st.selectbox('**아래 Option Menu를 선택해주세요**', ['2', 'E3)', 'W2E', 'T5R', 'X23234'], key='menu')

    with col2:
        combo_line = st.selectbox('**23**', ['23', '16423'], key='line')

    with col3:
        combo_eqpid = st.selectbox('**232323**', ['2323', '42323'], key='eqpid')

    with col4:
        selected_date = st.date_input("**계측완료 날짜**", value=date.today())

    _, _, col1 = st.columns([3, 0.4, 0.3])

    with col1:
        search_button = st.button("SEARCH")

    st.markdown("---")

    if search_button:
        data_df = pd.DataFrame(
            {
                "EQP_ID": ["설비1", "설비2", "설비3", "설비4"],
                "계측완료시간": ["2024-10-10-12:00", "2024-10-10-12:00", "2024-10-10-12:00", "2024-10-10-12:00"],
                "정리할 DATA 선택(1개만)": [True, False, False, True],
                "SPEC 설정": ["정상", "정상", "오류", "오류"]
            }
        )

        filtered_data = data_df[data_df['계측완료시간'].str.contains(str(selected_date))]

        st.session_state.filtered_data = filtered_data

    if  "filtered_data" in st.session_state and not st.session_state.filtered_data.empty:
             
        st.write(f"필터링된 데이터 : {combo_menu}, {combo_line} , {combo_eqpid} , {selected_date} || 검색 시간 : {datetime.now()}")

        edited_data = st.data_editor(
            st.session_state.filtered_data,
            column_config={
                "정리할 DATA 선택(1개만)": st.column_config.CheckboxColumn(
                    "DATA는 1개만 선택하세요",
                    help="원하는 데이터를 선택하세요",
                    default=False,
                ),
                "SPEC 설정": st.column_config.SelectboxColumn(
                    "SPEC 설정",
                    options=["정상", "오류", "점검 중"],
                    help="상태를 선택하세요",
                )
            },
            disabled=["EQP_ID", "계측완료시간"],
            hide_index=True,
        )    

        _, _, col1 = st.columns([3, 0.4, 0.5])

        with col1:
            save_button = st.button("DATA 저장하기")

    elif  "filtered_data" not in st.session_state or st.session_state.filtered_data.empty:
        st.markdown("**DATA가 존재하지 않습니다**")
        st.markdown("**다시 시도하거나, 담당자에게 문의 부탁드립니다.**")

    
    # 저장 버튼이 눌리면 "정리할 DATA 선택(1개만)" 컬럼에서 True로 체크된 데이터만 필터링하여 저장
    if 'save_button' in locals() and save_button:
        selected_data = edited_data[edited_data["정리할 DATA 선택(1개만)"] == True]  # 체크된 데이터만 선택
        if not selected_data.empty:
            st.session_state.saved_data = pd.concat([st.session_state.saved_data, selected_data], ignore_index=True)
            st.success("선택된 데이터가 저장되었습니다!")
        else:
            st.warning("선택된 데이터가 없습니다. 데이터를 선택 후 저장하세요.")

    st.markdown("---")
    st.write("현재 저장된 데이터:")

    # 저장된 데이터가 있는 경우에만 표시
    if "saved_data" in st.session_state and not st.session_state.saved_data.empty:
        edited_saved_data = st.data_editor(
            st.session_state.saved_data,
            column_config={
                "정리할 DATA 선택(1개만)": st.column_config.CheckboxColumn(
                    "DATA 선택",
                    help="삭제할 데이터를 선택하세요",
                    default=False,
                ),
                "SPEC 설정": st.column_config.SelectboxColumn(
                    "SPEC 설정",
                    options=["정상", "오류", "점검 중"],
                    help="상태를 선택하세요",
                )
            },
            disabled=["EQP_ID", "계측완료시간"],
            hide_index=True,
        )    

        # 제거할 데이터 선택 후 버튼을 눌러 선택된 데이터 삭제 & 초기화 버튼
        delete_button = st.button("선택된 데이터 삭제")
        initial_button = st.button("데이터 초기화")
        
        # 선택된 데이터 삭제 기능
        if delete_button:
            selected_to_delete = edited_saved_data[edited_saved_data["정리할 DATA 선택(1개만)"] == True]
            if not selected_to_delete.empty:
                st.session_state.saved_data = st.session_state.saved_data.drop(selected_to_delete.index).reset_index(drop=True)
                st.rerun()
            else:
                st.warning("삭제할 데이터를 선택하세요.")
        
        # 데이터 초기화 버튼
        if initial_button:
            st.session_state.saved_data = pd.DataFrame()  # 저장된 데이터 초기화
            # st.rerun()
            
    elif "saved_data" not in st.session_state or st.session_state.saved_data.empty:
        st.write("저장된 데이터가 없습니다.")

elif st.session_state.current_page == "기타 정보":
    st.write("기타 정보 페이지에 오신 것을 환영합니다.")
    st.write("이곳에서 추가적인 정보를 확인할 수 있습니다.")

print('********filtered_data******************',datetime.now(),st.session_state.filtered_data,sep='\n')
print('********edited******************',datetime.now(),st.session_state.saved_data,sep='\n')
