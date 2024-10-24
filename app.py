import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi

# Streamlit에서 제목 표시
st.title("방사형 차트 예시")

# 데이터 프레임 생성 (사용자 데이터는 달라질 수 있음)
data = {
    'S1': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.65, 0.54, 0.546, 0.54, 0.54],
    'S2': [1.0, 0.7, 1.0,0.7,0.7,0.7,1.3,0.7,0.7,0.7,0.7,0.7],
    'S3': [0.54, 0.45, 0.65, 0.75, 0.65, 0.65, 0.35, 0.75, 0.24, 0.78, 0.95, 0.54],
}

index = ['A28.1', 'A34.5', 'A58.5', 'A90.5', 'A105.5', 'A182.2', 'A195.7', 'A225.5', 'A278.2', 'A320.1', 'A356.1', 'A360.0']
df = pd.DataFrame(data, index=index)

# 변수 개수
categories = df.index
N = len(categories)

# 차트 크기 설정
chart_size = (3, 3)  # 각 차트의 크기 (너비, 높이)

# 3개씩 방사형 차트 표시
columns_per_row = 3
cols = st.columns(columns_per_row)

# 비율로 기준 값을 계산 (0도, 90도, 180도, 270도에 해당하는 비율)
angle_ratios = [0, 0.25, 0.5, 0.75]

for i, col in enumerate(df.columns):
    # 각 차트 크기 설정
    fig = plt.figure(figsize=chart_size)

    # 방사형 그래프 각도 설정 (첫 번째 인덱스를 맨 위로)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # 시작점과 끝점 연결

    # 각도 배열 반전 (좌우 반전)
    angles = angles[::-1]

    # 방사형 차트 초기화
    ax = plt.subplot(111, polar=True)

    # 그래프 회전 (첫 번째 축을 위쪽으로)
    ax.set_theta_offset(pi / 2)  # 90도 회전

    # 각 축에 인덱스 값 추가
    plt.xticks(angles[:-1], categories[::])  # 인덱스도 반전 할려면 [::-1]

    # 해당 컬럼의 값 가져오기
    values = df[col].values.flatten().tolist()
    values += values[:1]  # 시작점과 끝점 연결

    # 데이터 값의 스케일을 0~1로 맞추기
    ax.set_ylim(0, 1.2)  # 축의 범위를 통일 (0에서 최대 값 1.2까지 설정)
    plt.yticks(np.arange(0.0, 1.2, 0.2))  # Y축 눈금을 0.2 간격으로 설정

    # 데이터 그리기
    ax.plot(angles, values, linewidth=2, linestyle='solid')

    # 영역 채우기
    ax.fill(angles, values, 'b', alpha=0.1)

    # 각 컬럼의 평균값을 구하여 빨간색 방사형 그래프 그리기
    mean_value = [df[col].mean()] * N  # 각 컬럼의 평균값
    mean_value += mean_value[:1]  # 시작점과 끝점 연결

    ax.plot(angles, mean_value, linewidth=2, linestyle='solid', color='red')

    # 그래프 제목 (컬럼 이름)
    plt.title(col, size=15, color='b', y=1.1)

    # 비율에 따라 0도, 90도, 180도, 270도에 해당하는 값 추출
    differences = {}
    for ratio in angle_ratios:
        idx = int(ratio * N)  # 비율에 따른 인덱스 계산
        differences[categories[idx]] = values[idx] - mean_value[idx]

    # 표준편차 및 분산 계산
    std_dev = df[col].std()  # 표준편차
    variance = df[col].var()  # 분산

    # 차이, 표준편차 및 분산 출력
    st.write(f"{col} 그래프에서 0도, 90도, 180도, 270도의 차이:", differences)
    st.write(f"{col} 컬럼의 표준편차: {std_dev:.4f}, 분산: {variance:.4f}")

    # 현재 열에 차트 표시
    cols[i % columns_per_row].pyplot(fig)

    # 3개의 차트가 그려질 때마다 새로운 열 생성
    if (i + 1) % columns_per_row == 0 and (i + 1) < len(df.columns):
        cols = st.columns(columns_per_row)


# #탭 만들기
# import streamlit as st

# # 탭 생성
# tab1, tab2, tab3 = st.tabs(["탭 1", "탭 2", "탭 3"])

# # 첫 번째 탭 내용
# with tab1:
#     st.header("탭 1")
#     st.write("이것은 첫 번째 탭의 내용입니다.")

# # 두 번째 탭 내용
# with tab2:
#     st.header("탭 2")
#     st.write("이것은 두 번째 탭의 내용입니다.")

# # 세 번째 탭 내용
# with tab3:
#     st.header("탭 3")
#     st.write("이것은 세 번째 탭의 내용입니다.")
