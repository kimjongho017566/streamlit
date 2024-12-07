import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
import streamlit.components.v1 as components

# 샘플 데이터 생성
data = {
    'X': [1, 2, 3, 4, 5],
    'Y': [10, 20, 15, 25, 30],
    'Z': [5, 15, 10, 20, 25]
}
df = pd.DataFrame(data)

# Streamlit 제목
st.title("Copy Chart and Table to Clipboard")

# 1. Matplotlib 차트 생성
fig, ax = plt.subplots()
ax.plot(df['X'], df['Y'], label='Y Values', marker='o')
ax.plot(df['X'], df['Z'], label='Z Values', marker='s')
ax.set_title("Line Chart Example")
ax.set_xlabel("X Axis")
ax.set_ylabel("Y/Z Values")
ax.legend()

# 차트를 Streamlit에 표시
st.pyplot(fig)

# 2. 차트를 Base64로 변환
img_buffer = io.BytesIO()
fig.savefig(img_buffer, format='png')
img_buffer.seek(0)
img_base64 = base64.b64encode(img_buffer.read()).decode()

# 3. 데이터프레임을 HTML로 변환
table_html = df.to_html(index=False, border=0)

# 4. JavaScript와 버튼 생성 (Streamlit Components 사용)
custom_js = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        button {{
            padding: 10px 20px;
            font-size: 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
            border-radius: 5px;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <button onclick="copyToClipboard()">Copy to Clipboard</button>

    <script>
        function copyToClipboard() {{
            const imgBase64 = "data:image/png;base64,{img_base64}";
            const tableHTML = `{table_html}`;
            const fullContent = `<b>Image (Base64):</b><br><img src="${{imgBase64}}" alt="Chart"><br><br><b>Table (HTML):</b><br>${{tableHTML}}`;

            const tempElement = document.createElement("div");
            tempElement.innerHTML = fullContent;
            document.body.appendChild(tempElement);

            const range = document.createRange();
            range.selectNode(tempElement);
            window.getSelection().removeAllRanges();
            window.getSelection().addRange(range);

            try {{
                document.execCommand("copy");
                alert("Chart and Table copied to clipboard!");
            }} catch (err) {{
                alert("Failed to copy content. Please try again.");
            }}

            window.getSelection().removeAllRanges();
            document.body.removeChild(tempElement);
        }}
    </script>
</body>
</html>
"""

# Streamlit Components로 HTML 삽입
components.html(custom_js, height=300)
