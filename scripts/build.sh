#!/bin/bash

# DDW Services - Markdown to HTML Batch Converter
# 여러 Markdown 파일을 한 번에 HTML로 변환하는 스크립트

set -e  # 에러 발생 시 스크립트 종료

echo "🚀 DDW Services - Markdown to HTML 일괄 변환 시작"
echo "================================================"

# Python 환경 확인
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3가 설치되어 있지 않습니다."
    exit 1
fi

# 가상 환경 확인 및 활성화
if [ ! -d "venv" ]; then
    echo "❌ 가상 환경이 설정되지 않았습니다."
    echo "   다음 명령어로 먼저 환경을 설정해주세요:"
    echo "   ./scripts/setup.sh"
    exit 1
fi

echo "📦 가상 환경 활성화 중..."
source venv/bin/activate

# 변환할 파일들이 있는 디렉토리
DOCS_DIR="docs"

# docs 디렉토리가 없으면 생성
if [ ! -d "$DOCS_DIR" ]; then
    mkdir -p "$DOCS_DIR"
    echo "📁 docs 디렉토리를 생성했습니다."
    echo "   Markdown 파일들을 docs/ 폴더에 넣어주세요."
    echo ""
    echo "예시 파일 구조:"
    echo "docs/"
    echo "├── travelee-privacy-ko.md"
    echo "├── travelee-privacy-en.md"
    echo "├── travelee-support-ko.md"
    echo "├── travelee-support-en.md"
    echo "├── gokitty-privacy-ko.md"
    echo "├── gokitty-privacy-en.md"
    echo "├── gokitty-support-ko.md"
    echo "└── gokitty-support-en.md"
    echo ""
    echo "파일명 규칙: {service}-{type}-{lang}.md"
    echo "- service: travelee, gokitty"
    echo "- type: privacy, support"
    echo "- lang: ko, en"
    exit 0
fi

echo "🔍 Markdown 파일 검색 중..."

# 변환 카운터
converted_count=0
failed_count=0

# docs 디렉토리에서 .md 파일들을 찾아서 변환
for md_file in "$DOCS_DIR"/*.md; do
    # 파일이 존재하는지 확인
    if [ ! -f "$md_file" ]; then
        continue
    fi
    
    # 파일명에서 정보 추출
    filename=$(basename "$md_file" .md)
    
    # 파일명 패턴: {service}-{type}-{lang}.md
    if [[ $filename =~ ^([^-]+)-([^-]+)-([^-]+)$ ]]; then
        service="${BASH_REMATCH[1]}"
        type="${BASH_REMATCH[2]}"
        lang="${BASH_REMATCH[3]}"
        
        echo "🔄 변환 중: $filename"
        echo "   서비스: $service, 타입: $type, 언어: $lang"
        
        # Python 스크립트 실행 (가상 환경에서)
        if python scripts/md-to-html.py "$md_file" --type "$type" --lang "$lang" --service "$service"; then
            ((converted_count++))
            echo "   ✅ 성공"
        else
            ((failed_count++))
            echo "   ❌ 실패"
        fi
        echo ""
    else
        echo "⚠️  파일명 패턴이 맞지 않습니다: $filename"
        echo "   올바른 패턴: {service}-{type}-{lang}.md"
        echo "   예시: travelee-privacy-ko.md"
        echo ""
    fi
done

echo "================================================"
echo "🎉 변환 완료!"
echo "   성공: $converted_count 개"
echo "   실패: $failed_count 개"

if [ $failed_count -gt 0 ]; then
    echo ""
    echo "❌ 일부 파일 변환에 실패했습니다. 위의 오류 메시지를 확인해주세요."
    exit 1
fi

echo ""
echo "✨ 모든 파일이 성공적으로 변환되었습니다!" 