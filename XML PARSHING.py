import os
import xml.etree.ElementTree as ET
import pandas as pd

# XML 파일을 재귀적으로 파싱하는 함수
def parse_element(element, parent_path="", tag_to_parse=""):
    data = {}
    # 현재 태그 경로
    current_path = f"{parent_path}/{element.tag}" if parent_path else element.tag

    # 동적으로 지정된 태그 경로만 필터링하여 처리
    if tag_to_parse in current_path:
        if element.attrib:
            data[current_path] = element.attrib  # 속성도 함께 저장

        # 자식 요소가 없는 경우 텍스트를 저장
        if element.text and element.text.strip():
            data[current_path] = element.text.strip()
    
    # 자식 요소가 있는 경우 재귀적으로 처리
    for child in element:
        data.update(parse_element(child, current_path, tag_to_parse))
    
    return data

# 특정 경로에서 모든 XML 파일을 탐색하는 함수
def find_xml_files(directory):
    xml_files = []
    # os.walk를 사용해 하위 폴더까지 모두 탐색
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xml'):  # 확장자가 .xml인 파일만 찾음
                xml_files.append(os.path.join(root, file))
    return xml_files

# 여러 XML 파일을 파싱하고 데이터를 DataFrame으로 변환하는 함수
def parse_xml_files_to_dataframe(directory, tag_to_parse):
    xml_files = find_xml_files(directory)
    all_data = []

    # 각 XML 파일을 파싱하여 데이터 수집
    for xml_file in xml_files:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        parsed_data = parse_element(root, tag_to_parse=tag_to_parse)
        
        # 파일 이름과 함께 데이터를 저장
        for path, value in parsed_data.items():
            all_data.append({'File': xml_file, 'Path': path, 'Value': value})

    # DataFrame 생성
    df = pd.DataFrame(all_data)
    return df

# XML 파일이 있는 폴더 경로 지정 (탐색할 최상위 폴더)
directory_to_search = '.'

# 동적으로 파싱할 태그 경로를 지정 (예: 'Library')
tag_to_parse = "Store/Offers"

# XML 파일들을 파싱해서 데이터프레임 생성
df = parse_xml_files_to_dataframe(directory_to_search, tag_to_parse)

# DataFrame 출력
print(df, "dataframe을 출력하였습니다", sep="\n")

# DataFrame을 CSV로 저장
df.to_csv('parsed_xml_data.csv', index=False)

print("모든 XML 파일이 파싱되고 CSV로 저장되었습니다.")
