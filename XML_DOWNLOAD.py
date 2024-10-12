import ftplib
import os
import re

# FTP 서버 정보 설정
ftp_server = "ftp.example.com"
ftp_user = "username"
ftp_password = "password"

# 저장할 로컬 경로
local_download_dir = "./downloads"
search_keyword = "store"  # 원하는 경로에 포함된 문자열

# xml 파일만 다운로드하는 함수
def download_xml_files(ftp, path):
    try:
        ftp.cwd(path)
        file_list = ftp.nlst()

        # 검색 키워드가 경로에 포함되어 있을 때만 진행
        if search_keyword in path:
            print(f"Searching in: {path}")
            for file in file_list:
                # 디렉토리인지 파일인지 확인
                try:
                    ftp.cwd(file)  # 디렉토리이면 오류 발생하지 않음
                    ftp.cwd('..')  # 상위 디렉토리로 다시 이동
                    # 재귀적으로 디렉토리 탐색
                    download_xml_files(ftp, f"{path}/{file}")
                except ftplib.error_perm as e:
                    if "550" in str(e):
                        # 550 오류는 파일이라는 뜻
                        if file.endswith(".xml"):
                            local_file_path = os.path.join(local_download_dir, file)
                            with open(local_file_path, "wb") as f:
                                ftp.retrbinary(f"RETR {file}", f.write)
                            print(f"Downloaded: {local_file_path}")
                    else:
                        print(f"Error: {e}")
        else:
            # 검색 키워드가 포함되지 않으면 패스
            print(f"Skipping directory: {path}")
    except Exception as e:
        print(f"Failed to access {path}: {e}")

# FTP 접속 및 파일 다운로드 실행
with ftplib.FTP(ftp_server) as ftp:
    ftp.login(ftp_user, ftp_password)
    download_xml_files(ftp, "/")  # 루트 디렉토리부터 탐색 시작
