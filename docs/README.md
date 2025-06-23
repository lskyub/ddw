# Markdown 파일 작성 가이드

이 폴더에 Markdown 파일을 작성하면 자동으로 HTML로 변환할 수 있습니다.

## 파일명 규칙

```
{service}-{type}-{lang}.md
```

- **service**: `travelee`, `gokitty`
- **type**: `privacy` (개인정보처리방침), `support` (지원센터)
- **lang**: `en` (영어), `ko` (한국어)

## 예시 파일명

- `travelee-privacy-ko.md` → `ko/travelee/privacy/index.html`
- `gokitty-support-en.md` → `en/gokitty/support/index.html`
- `travelee-support-ko.md` → `ko/travelee/support/index.html`
- `gokitty-privacy-en.md` → `en/gokitty/privacy/index.html`

## 변환 방법

### 1. 처음 사용하는 경우
```bash
# 개발 환경 설정
./scripts/setup.sh
```

### 2. 개별 파일 변환
```bash
# 가상 환경 활성화
source venv/bin/activate

# 파일 변환
python scripts/md-to-html.py docs/travelee-privacy-ko.md --type privacy --lang ko --service travelee
```

### 3. 모든 파일 일괄 변환
```bash
# 한 번에 모든 .md 파일 변환
./scripts/build.sh
```

## Markdown 작성 팁

### 개인정보처리방침 (`privacy`)
- 법적 요구사항을 충족하는 내용 작성
- 표를 활용해 정보 정리
- 중요한 내용은 인용구(`>`) 사용

### 지원센터 (`support`)
- FAQ 형식으로 구성
- 이모지를 활용해 시각적 구분
- 단계별 설명 제공

## 지원되는 Markdown 문법

- **제목**: `#`, `##`, `###`
- **강조**: `**굵게**`, `*기울임*`
- **목록**: `1.`, `-`, `*`
- **표**: `| 열1 | 열2 |`
- **인용구**: `> 인용 내용`
- **코드**: `` `인라인 코드` ``
- **링크**: `[텍스트](URL)`

## 템플릿

이 폴더에 있는 예시 파일들을 참고해서 작성하세요:
- `travelee-privacy-ko.md` - 개인정보처리방침 예시
- `gokitty-support-en.md` - 지원센터 예시 