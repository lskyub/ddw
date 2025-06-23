#!/bin/bash

# DDW Services - 개발 환경 설정 스크립트
# Markdown to HTML 변환 도구를 사용하기 위한 환경을 설정합니다.

set -e

echo "🚀 DDW Services 개발 환경 설정 시작"
echo "========================================"

# Python 설치 확인
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3가 설치되어 있지 않습니다."
    echo "   macOS: brew install python3"
    echo "   Ubuntu: sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

echo "✅ Python 3 설치 확인됨: $(python3 --version)"

# 가상 환경 생성
if [ ! -d "venv" ]; then
    echo "📦 가상 환경 생성 중..."
    python3 -m venv venv
    echo "✅ 가상 환경 생성 완료"
else
    echo "✅ 가상 환경이 이미 존재합니다"
fi

# 가상 환경 활성화 및 패키지 설치
echo "📦 필요한 패키지 설치 중..."
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo "✅ 패키지 설치 완료"

# 스크립트 실행 권한 부여
echo "🔧 스크립트 권한 설정 중..."
chmod +x scripts/build.sh scripts/md-to-html.py scripts/setup.sh
echo "✅ 스크립트 권한 설정 완료"

# docs 디렉토리 생성
if [ ! -d "docs" ]; then
    mkdir -p docs
    echo "📁 docs 디렉토리 생성 완료"
fi

echo ""
echo "🎉 설정이 완료되었습니다!"
echo ""
echo "이제 다음과 같이 사용할 수 있습니다:"
echo ""
echo "1. 개별 파일 변환:"
echo "   source venv/bin/activate"
echo "   python3 scripts/md-to-html.py docs/파일명.md --type privacy --lang ko --service travelee"
echo ""
echo "2. 일괄 변환:"
echo "   ./scripts/build.sh"
echo ""
echo "3. 도움말:"
echo "   source venv/bin/activate"
echo "   python3 scripts/md-to-html.py --help"
echo ""
echo "📁 docs/ 폴더에 Markdown 파일을 넣고 변환해보세요!"
echo "   파일명 형식: {service}-{type}-{lang}.md"
echo "   예시: travelee-privacy-ko.md, gokitty-support-en.md" 