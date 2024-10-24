import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi
from io import BytesIO
import base64

# Streamlit에서 제목 표시
st.title("방사형 차트 예시")

# 데이터 프레임 생성
data = {
    'S1': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.65, 0.54, 0.546, 0.54, 0.54],
    'S2': [1.0, 0.7, 1.0, 0.7, 0.7, 0.7, 1.3, 0.7, 0.7, 0.7, 0.7, 0.7],
    'S3': [0.54, 0.45, 0.65, 0.75, 0.65, 0.65, 0.35, 0.75, 0.24, 0.78, 0.95, 0.54],
}

index = ['A28.1', 'A34.5', 'A58.5', 'A90.5', 'A105.5', 'A182.2', 'A195.7', 'A225.5', 'A278.2', 'A320.1', 'A356.1', 'A360.0']
df = pd.DataFrame(data, index=index)

# 조건부 스타일 지정 함수 (0.8 이상일 때 배경은 노란색, 글씨는 빨간색)
def highlight_above_threshold(val):
    color = 'color: red;' if val > 0.8 else ''
    background = 'background-color: yellow;' if val > 0.8 else ''
    return f'{color} {background}'

# 데이터프레임 스타일 지정 + 컬럼 및 인덱스 배경색 설정
df_style = df.style.applymap(highlight_above_threshold).set_table_styles(
    [
        {'selector': 'td', 'props': [('border', '1px solid black'), ('padding', '5px'), ('font-size', '14px')]},  # 셀 스타일
        {'selector': 'th.col_heading', 'props': [('background-color', '#ADD8E6'), ('font-size', '15px'), ('text-align', 'center'), ('border', '1px solid black')]},  # 컬럼 헤더 배경색
        {'selector': 'th.row_heading', 'props': [('background-color', '#FFA07A'), ('font-size', '15px'), ('text-align', 'center'), ('border', '1px solid black')]},  # 인덱스 배경색
        {'selector': 'thead th.blank', 'props': [('background-color', '#E6E6FA'), ('border', '1px solid black')]},  # 빈칸(교차 헤더) 색상 변경
        #{'selector': 'th', 'props': [('border', '1px solid black'), ('background-color', '#f2f2f2'), ('font-size', '15px'), ('text-align', 'center'), ('padding', '5px')]},  # 헤더 스타일(컬럼과,열 통합)
        {'selector': 'table', 'props': [('border-collapse', 'collapse'), ('width', '100%')]}  # 셀 간격 제거 및 테이블 크기 조정
    ]
)



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

# 그래프들을 저장할 리스트
all_figs_base64 = []

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

    # 데이터 값의 스케일을 0~1.2로 맞추기
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

    # 현재 열에 차트 표시
    cols[i % columns_per_row].pyplot(fig)

    # 차트 밑에 추가적인 내용 표시
    cols[i % columns_per_row].write(f"{col} 컬럼의 표준편차: {std_dev:.4f}, 분산: {variance:.4f}")
    cols[i % columns_per_row].write(f"{col} 그래프에서 0도, 90도, 180도, 270도의 차이: {differences}")

    # 3개의 차트가 그려질 때마다 새로운 열 생성
    if (i + 1) % columns_per_row == 0 and (i + 1) < len(df.columns):
        cols = st.columns(columns_per_row)

    ########################################################
    # 차트를 메모리에 저장하고 Base64로 인코딩
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    all_figs_base64.append(f'<img src="data:image/png;base64,{img_base64}" />')

    # 3개의 차트가 그려질 때마다 새로운 열 생성
    if (i + 1) % columns_per_row == 0 and (i + 1) < len(df.columns):
        cols = st.columns(columns_per_row)

st.markdown(df_style.to_html(),unsafe_allow_html=True)
# Styler 객체로 변환된 데이터프레임을 HTML로 렌더링
df_html = df_style.to_html()

# HTML 코드와 Base64 인코딩된 이미지 및 테이블 포함
html_content = ''.join(all_figs_base64) + df_html

# 복사 버튼 추가
copy_button_code = f"""
<button id="copyButton">Copy HTML (including charts and table) to Clipboard</button>

<script>
    document.getElementById('copyButton').addEventListener('click', function() {{
        const htmlContent = `{html_content}`;
        const textarea = document.createElement('textarea');
        textarea.value = htmlContent;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        alert('HTML content including charts and table copied to clipboard!');
    }});
</script>
"""

# Streamlit에 HTML 복사 버튼 추가
st.components.v1.html(copy_button_code, height=100)
