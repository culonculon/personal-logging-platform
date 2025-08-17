# App Tracker - macOS 앱 사용 추적기

Personal Logging Platform의 앱 추적 모듈입니다. macOS에서 실행되는 앱들의 사용 패턴을 수집하고 분석합니다.

## 🎯 주요 기능

- **실시간 앱 모니터링**: 현재 실행 중인 앱 목록 수집
- **프로세스 사용량 분석**: CPU, 메모리 사용률 수집
- **카테고리 자동 분류**: 개발, 업무, 엔터테인먼트 등 8개 카테고리
- **생산성 점수 계산**: 앱 사용 패턴 기반 생산성 측정
- **시간대별 패턴 분석**: 언제 어떤 앱을 사용하는지 분석

## 🛠 시스템 요구사항

- **운영체제**: macOS 10.14 이상
- **Python**: 3.9 이상
- **권한**: 앱 접근 권한 (시스템 환경설정에서 설정)

## 📦 설치

```bash
# 1. 가상환경 활성화
conda activate personal-logging

# 2. 의존성 설치
cd app-tracker
pip install -r requirements.txt

# 3. 권한 설정 (필요시)
# 시스템 환경설정 > 보안 및 개인 정보 보호 > 개인 정보 보호 > 접근성
# Terminal 또는 Python 앱에 권한 부여
```

## 🚀 사용법

### 기본 실행
```bash
cd src
python main.py
```

### 테스트 실행
```bash
cd src
python test_app_tracker.py
```

## 📁 프로젝트 구조

```
app-tracker/
├── src/
│   ├── collectors/
│   │   ├── __init__.py
│   │   └── app_collector.py          # 앱 데이터 수집기
│   ├── analyzers/
│   │   ├── __init__.py
│   │   └── app_category_analyzer.py  # 카테고리 분석기
│   ├── main.py                       # 메인 실행 파일
│   └── test_app_tracker.py          # 테스트 파일
├── output/                           # 수집된 데이터 저장
├── requirements.txt                  # 의존성 목록
└── README.md
```

## 📊 출력 데이터

### 1. 완전 데이터 (JSON)
```json
{
  "collection_info": {
    "timestamp": "2024-08-17T16:30:00",
    "collector": "AppCollector",
    "platform": "macOS"
  },
  "running_apps": [...],
  "process_usage": [...],
  "app_history": [...],
  "usage_stats": {...}
}
```

### 2. 요약 데이터 (JSON)
- 카테고리별 분석 결과
- 생산성 점수
- 상위 사용 앱 목록

### 3. 카테고리 리포트 (TXT)
- 읽기 쉬운 텍스트 형태의 분석 리포트
- 생산성 해석 및 권장사항

## 🏷 앱 카테고리

| 카테고리 | 설명 | 예시 앱 |
|---------|------|--------|
| `developer` | 개발 도구 | VS Code, Xcode, Terminal |
| `browser` | 웹 브라우저 | Chrome, Safari, Firefox |
| `productivity` | 업무/생산성 | Word, Notion, Bear |
| `communication` | 커뮤니케이션 | Slack, Zoom, Discord |
| `entertainment` | 미디어/오락 | Spotify, Netflix, Photoshop |
| `system` | 시스템 유틸리티 | Finder, Activity Monitor |
| `gaming` | 게임 | Steam, Epic Games |
| `other` | 기타 | 분류되지 않은 앱 |

## 🎯 생산성 점수 계산

생산성 점수는 다음 가중치를 사용하여 계산됩니다:

- **Developer**: 1.0 (최고 생산성)
- **Productivity**: 0.9 (높은 생산성)
- **Communication**: 0.7 (업무 관련)
- **Browser**: 0.5 (중간, 작업/오락 겸용)
- **System**: 0.3 (시스템 관리)
- **Entertainment**: 0.1 (낮은 생산성)
- **Gaming**: 0.0 (비생산적)

## 🔧 문제 해결

### 앱 수집이 안 되는 경우
1. 시스템 환경설정 > 보안 및 개인 정보 보호
2. 개인 정보 보호 > 접근성
3. Terminal/Python 앱에 체크 표시

### PyObjC 설치 실패
```bash
# Xcode Command Line Tools 설치
xcode-select --install

# 다시 설치 시도
pip install pyobjc-framework-Cocoa
```

## 🔄 브라우저 수집기와 통합

```python
# 향후 통합 예시
from browser_collector import BrowserCollector
from app_tracker import AppCollector

browser_data = BrowserCollector().collect_all_data()
app_data = AppCollector().collect_all_data()

# 통합 분석...
```

## 📈 향후 개발 계획

- [ ] 실시간 모니터링 (백그라운드 데몬)
- [ ] 웹 앱 vs 네이티브 앱 구분
- [ ] 앱 윈도우 제목 수집
- [ ] 사용 패턴 기반 알림
- [ ] 캘린더 데이터와 연관 분석

## 🤝 브라우저 수집기 연동

이 앱 추적기는 브라우저 수집기와 함께 사용하도록 설계되었습니다:

```bash
# 브라우저 + 앱 데이터 동시 수집
cd ../browser-collector/src && python main.py
cd ../app-tracker/src && python main.py
```

---

**Personal Logging Platform** 프로젝트의 일부  
🎯 목표: 데이터 엔지니어링 + 클라우드 인프라 경험 쌓기
