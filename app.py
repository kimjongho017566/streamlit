import pandas as pd

# 예시 데이터프레임 생성
data = {'name': ['kjh', 'asdf', 'adfdf'],
        'date': [2024, 2024, 2024],
        'id': [2, 5, 6],
        'str': ['s1=34,s2=54,s3=5423.4,s4=65,sum=dfdf',
                's1=50,s27=54,s3=54,s4=6225,sum=dfdf',
                't1=0.4,t2=45,t3=54,s4=65,avg=23']}

df = pd.DataFrame(data)


# 각 셀의 문자열을 파이썬 딕셔너리로 변환하는 함수
def parse_data(cell):
    # ','와 '=' 기준으로 나눈 후 딕셔너리로 변환
    try:
        return dict(item.split('=') for item in cell.split(','))
    except:
        return {}

# 각 셀을 파싱하여 딕셔너리로 변환
df['parsed'] = df['str'].apply(parse_data)

# 딕셔너리 데이터를 여러 컬럼으로 변환
df_parsed = df['parsed'].apply(pd.Series)

# 원래 데이터프레임과 병합
df_final = pd.concat([df.drop(columns=['parsed']), df_parsed], axis=1)

print(df_final)


########################################
import pandas as pd
import ast

# 예시 데이터프레임 생성
data = {'name': ['kjh', 'asdf', 'adfdf'],
        'date': [2024, 2024, 2024],
        'id': [2, 5, 6],
        'str': ['s1=34,s2=54,s3=5423.4,s4=65,sum=dfdf',
                's1=50,s27=54,s3=54,s4=6225,sum=dfdf',
                't1=0.4,t2=45,t3=54,s4=65,avg=23']}

df = pd.DataFrame(data)

# 각 셀의 문자열을 파이썬 딕셔너리로 변환하는 함수
def parse_data(cell):
    formatted_cell = cell.replace('=', ':')  # '='을 ':'로 변경
    formatted_cell = '{' + formatted_cell + '}'  # 중괄호로 감싸서 딕셔너리 형식으로 변경
    
    # 딕셔너리로 변환
    try:
        return ast.literal_eval(formatted_cell)
    except:
        return {}

# 각 셀을 파싱하여 딕셔너리로 변환
df['parsed'] = df['str'].apply(parse_data)

# 딕셔너리 데이터를 여러 컬럼으로 변환
df_parsed = df['parsed'].apply(pd.Series)

# 원래 데이터프레임과 병합
df_final = pd.concat([df.drop(columns=['parsed']), df_parsed], axis=1)

print(df_final)

