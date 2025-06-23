# DDW Services

DDW Services는 다양한 디지털 서비스를 제공하는 포트폴리오 웹사이트입니다.

## 🌟 서비스 목록

- **✈️ Travelee**: 스마트한 여행 계획 및 일정 관리 서비스
- **🐱 Go Kitty**: 귀여운 고양이와 함께하는 무한 러닝 게임 (출시 예정)

## 🌍 다국어 지원

- 🇺🇸 English (기본)
- 🇰🇷 한국어

## 📁 프로젝트 구조

```
ddw/
├── index.html (언어 감지 & 리다이렉트)
├── en/ (영어 버전)
│   ├── index.html (메인 서비스 목록)
│   ├── travelee/
│   │   ├── index.html (서비스 소개)
│   │   ├── support/index.html (지원 센터)
│   │   └── privacy/
│   │       ├── index.html (개인정보처리방침)
│   │       └── history/index.html (방침 히스토리)
│   └── gokitty/
│       ├── index.html (게임 소개)
│       ├── support/index.html (지원 센터)
│       └── privacy/
│           ├── index.html (개인정보처리방침)
│           └── history/index.html (방침 히스토리)
├── ko/ (한국어 버전)
│   └── [영어와 동일한 구조]
├── scripts/ (개발 도구)
│   ├── md-to-html.py (Markdown → HTML 변환기)
│   └── build.sh (일괄 변환 스크립트)
├── docs/ (Markdown 소스 파일들)
└── requirements.txt (Python 패키지 의존성)
```

## 🛠️ Markdown to HTML 변환 도구

개인정보처리방침이나 지원 문서를 Markdown으로 작성하고 자동으로 예쁜 HTML로 변환할 수 있는 도구를 제공합니다.

### 설치


```bash
# Python 패키지 설치
pip3 install -r requirements.txt

# 스크립트 실행 권한 부여
chmod +x scripts/build.sh scripts/md-to-html.py
```

### 개별 파일 변환

```bash
# 가상환경 활성화
source venv/bin/activate

# 기본 사용법
python3 scripts/md-to-html.py <markdown_file> --type <privacy|support> --lang <en|ko> --service <travelee|gokitty>

# 예시
python3 scripts/md-to-html.py docs/travelee-privacy-ko.md --type privacy --lang ko --service travelee
python3 scripts/md-to-html.py docs/gokitty-support-en.md --type support --lang en --service gokitty
python3 scripts/md-to-html.py docs/travelee-support-ko.md --type support --lang ko --service travelee
```

### 일괄 변환

```bash
# docs/ 폴더의 모든 Markdown 파일을 한 번에 변환
./scripts/build.sh
```

### 파일명 규칙

`docs/` 폴더에 다음 규칙으로 Markdown 파일을 작성하세요:

```
{service}-{type}-{lang}.md
```

- **service**: `travelee`, `gokitty`
- **type**: `privacy` (개인정보처리방침), `support` (지원센터)
- **lang**: `en` (영어), `ko` (한국어)

#### 예시 파일명
```
docs/
├── travelee-privacy-ko.md
├── travelee-privacy-en.md
├── travelee-support-ko.md
├── travelee-support-en.md
├── gokitty-privacy-ko.md
├── gokitty-privacy-en.md
├── gokitty-support-ko.md
└── gokitty-support-en.md
```

### 변환 결과

변환된 HTML 파일은 자동으로 올바른 위치에 저장됩니다:

- `docs/travelee-privacy-ko.md` → `ko/travelee/privacy/index.html`
- `docs/gokitty-support-en.md` → `en/gokitty/support/index.html`

### Markdown 작성 가이드

#### 개인정보처리방침 (`privacy`)
```markdown
# 개인정보처리방침

## 1. 개인정보의 처리목적
서비스 제공을 위한 개인정보 처리 목적을 설명합니다.

## 2. 개인정보의 처리 및 보유기간
| 항목 | 보유기간 | 근거 |
|------|----------|------|
| 회원정보 | 회원탈퇴 시까지 | 서비스 제공 |

> **중요한 내용**은 인용구를 사용해 강조할 수 있습니다.
```

#### 지원센터 (`support`)
```markdown
# 지원센터

## 🎮 시작하기
게임 사용법을 설명합니다.

### 자주 묻는 질문
#### 문제가 발생했을 때는?
1. 첫 번째 해결책
2. 두 번째 해결책

## 📞 문의하기
추가 도움이 필요하면 연락주세요.
```

### 지원되는 Markdown 기능

- **제목**: `#`, `##`, `###`
- **강조**: `**굵게**`, `*기울임*`
- **목록**: `1.`, `-`, `*`
- **표**: `| 열1 | 열2 |`
- **인용구**: `> 인용 내용`
- **코드**: `` `인라인 코드` ``, ``` 코드 블록 ```
- **링크**: `[텍스트](URL)`

## 🚀 배포

GitHub Pages를 사용하여 자동 배포됩니다.

1. `main` 브랜치에 코드 푸시
2. GitHub Actions가 자동으로 빌드 및 배포
3. `https://username.github.io/ddw`에서 확인

## 🔧 개발

### 새 서비스 추가하기

1. `scripts/md-to-html.py`의 `SERVICE_CONFIG`에 새 서비스 추가:
```python
SERVICE_CONFIG = {
    'newservice': {
        'icon': '🆕',
        'name': 'New Service',
        'brand_color': '#FF6B6B',
        'brand_color_hover': '#FF5252',
        'brand_color_light': '#FFB3B3'
    }
}
```

2. 각 언어별 메인 페이지에 서비스 카드 추가
3. Markdown 파일 작성 및 변환

### 새 언어 추가하기

1. 새 언어 폴더 생성 (예: `fr/`)
2. `scripts/md-to-html.py`의 `TEXTS`에 새 언어 추가
3. `index.html`의 언어 감지 로직 업데이트

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
