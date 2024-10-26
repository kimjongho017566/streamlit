from ftplib import FTP
import fnmatch
import os

ftp_host = ''
ftp_user = ''
ftp_pass = ''

start_folder = '' # /로 시작하고 /로 끝나야함

# 여러 개의 패턴을 리스트로 지정
target_path_patterns = ['/WIND/2024-10/MPCG02', '/WIND/2024-10/MPCG04']  # 여러 패턴 예시, 찾고자 하는 폴더들 #/로 시작하고 /없이 끝나야함
target_file_pattern = '*.txt'  # 파일 이름 패턴 (예: *.txt 형식)

# FTP 연결 설정
ftp = FTP(ftp_host)
ftp.encoding = 'cp949'
ftp.login(ftp_user, ftp_pass)

# 특정 폴더에서 파일을 찾는 재귀 함수
def search_files(ftp, current_folder):
    found_files = []  # 발견된 파일들을 저장할 리스트
    try:
        ftp.cwd(current_folder)
        items = ftp.nlst()  # 현재 폴더의 모든 항목 목록 가져오기

        for item in items:
            item_path = f"{current_folder}/{item}"
            
            try:
                ftp.cwd(item_path)  # 폴더인지 확인 후 이동 시도
                found_files.extend(search_files(ftp, item_path))  # 하위 폴더 탐색 결과 추가
                ftp.cwd("..")  # 상위 폴더로 이동
            except:
                # 최종 패턴 리스트에 있는 패턴 중 하나와 일치하는 폴더에 있는 파일만 확인
                if any(current_folder.endswith(pattern) for pattern in target_path_patterns):
                    print(f"현재 위치: {current_folder}")
                    if fnmatch.fnmatch(item, target_file_pattern):  # 파일명 패턴이 일치하는지 확인
                        print(f"파일 발견: {item_path}")
                        found_files.append(item_path)  # 발견된 파일을 리스트에 추가
    except Exception as e:
        print(f"오류 발생: {e}")
    
    return found_files  # 최종적으로 발견된 파일 리스트 반환

# 탐색 시작
found_files = search_files(ftp, start_folder)
print("\n발견된 파일 목록:")
print(found_files)

# FTP 연결 종료
ftp.quit()
