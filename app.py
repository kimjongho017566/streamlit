

target_folder = '/NNG4876_3/'
target_path_pattern = '/wind/mmcg02' #찾고자하는 최종 폴더 패턴
file_extension = '.text' #찾고자하는 파일

ftp = FTP(ftp_host)
ftp.encoding = 'cp949'
ftp.login(ftp_user, ftp_pass)

# 특정 폴더에서 tar 파일을 찾는 재귀 함수
def search_tar_files(ftp, current_folder):
    try:
        ftp.cwd(current_folder)
        items = ftp.nlst()  # 현재 폴더의 모든 항목 목록 가져오기
        print(current_folder,"현재위치")
        for item in items:
            item_path = f"{current_folder}/{item}"
            
            try:
                ftp.cwd(item_path)  # 폴더로 이동이 가능한지 확인 (폴더인 경우)
                search_tar_files(ftp, item_path)  # 하위 폴더 재귀 탐색
                ftp.cwd("..")  # 탐색 후 상위 폴더로 이동
            except Exception as e:
                # 이동 불가시 (즉, 파일일 때)
                if current_folder.endswith(target_path_pattern):
                    print(f"파일 발견: {item_path}")
                    
    except Exception as e:
        print(f"오류 발생: {e}")

# 탐색 시작
search_tar_files(ftp, target_folder)

# FTP 연결 종료
ftp.quit()
