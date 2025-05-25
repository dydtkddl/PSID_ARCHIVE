import os

def copy_directory_structure(src_root, dst_root):
    for dirpath, dirnames, filenames in os.walk(src_root):
        # 상대 경로 계산
        rel_path = os.path.relpath(dirpath, src_root)
        target_dir = os.path.join(dst_root, rel_path)
        print(target_dir)
        os.makedirs(target_dir, exist_ok=True)

# 실행 예시
src = os.getcwd()  # 현재 디렉토리
dst = os.path.join(src, "")  # copy라는 폴더 생성
copy_directory_structure(src, dst)

print(f"✅ 디렉터리 구조만 '{dst}'에 복사 완료")