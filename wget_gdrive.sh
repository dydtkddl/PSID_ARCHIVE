#!/bin/bash

# 입력: Google Drive 링크 및 저장할 파일 이름
GDRIVE_LINK="$1"
OUTPUT_FILENAME="$2"

# Google Drive 링크에서 FILEID 추출
FILEID=$(echo "$GDRIVE_LINK" | grep -oP '(?<=/file/d/)[^/]+')

# 파일 다운로드 함수
download_file() {
  local fileid="$1"
  local filename="$2"

  echo "Downloading file with ID: $fileid"

  # wget 명령으로 다운로드
  wget --no-check-certificate "https://drive.google.com/uc?export=download&id=$fileid" -O "$filename"
}

# 다운로드 실행
echo "Starting download process..."
download_file "$FILEID" "$OUTPUT_FILENAME"

echo "Download completed: $OUTPUT_FILENAME"
