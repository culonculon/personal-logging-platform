# Personal Logging Platform - Browser Collector

> 브라우저 히스토리를 자동으로 수집하고 분석하여 Obsidian Daily Notes를 생성하는 프로젝트

## 🎯 프로젝트 목표

- **자동화**: 브라우저, 앱, 캘린더 데이터를 자동으로 수집
- **분석**: 수집된 데이터를 의미있는 인사이트로 변환
- **통합**: Obsidian Daily Notes로 일일 활동 요약 자동 생성
- **학습**: 데이터 엔지니어링 + 클라우드 인프라 경험 쌓기

## 📁 프로젝트 구조

```
personal-logging-platform/
├── browser-collector/          ← 현재 완료된 모듈
│   ├── src/
│   │   ├── collectors/        # 브라우저 히스토리 수집기
│   │   │   ├── chrome_collector.py
│   │   │   ├── safari_collector.py
│   │   │   └── browser_collector.py
│   │   ├── analyzers/         # 데이터 분석기
│   │   │   ├── search_analyzer.py
│   │   │   └── category_analyzer.py
│   │   ├── main.py           # 메인 실행 파일
│   │   └── test_chrome.py    # 테스트 파일
│   ├── output/               # 생성된 데이터 파일들
│   └── requirements.txt
├── app-tracker/              # 다음 개발 예정
├── calendar-integrator/      # 다음 개발 예정
└── data-aggregator/          # 다음 개발 예정
```

## 🚀 브라우저 수집기 기능

### ✅ 완료된 기능

1. **멀티 브라우저 지원**
   - Chrome 히스토리 수집
   - Safari 히스토리 수집
   - 통합 데이터 병합

2. **고급 분석 기능**
   - 검색어 추출 및 패턴 분석
   - 웹사이트 카테고리 자동 분류
   - 시간대별 활동 패턴 분석
   - 브라우저별 사용 통계

3. **지원하는 검색 엔진**
   - Google, Naver, YouTube, Bing, DuckDuckGo, Yahoo, Baidu

4. **카테고리 분류**
   - Social, Work, News, Entertainment, Shopping
   - Education, Developer, Finance, Travel, Health

5. **데이터 출력**
   - 완전한 JSON 데이터셋
   - 일일 요약 리포트
   - 카테고리 분석 텍스트 리포트

## 🛠️ 설치 및 실행

### 1. 요구사항
- Python 3.7+
- macOS (Chrome/Safari 지원)
- 브라우저 히스토리 접근 권한

### 2. 설치
```bash
cd /Users/admin/Documents/GitHub/personal-logging-platform/browser-collector
# Python 내장 라이브러리만 사용하므로 별도 설치 불필요
```

### 3. 실행
```bash
cd src
python3 main.py
```

### 4. 테스트 (Chrome만)
```bash
cd src
python3 test_chrome.py
```

## 📊 출력 예시

### 콘솔 출력
```
🌐 Personal Logging Platform - Browser Collector (Enhanced)
============================================================
📚 사용 가능한 브라우저: chrome, safari
📅 수집 날짜: 2025-08-17 16:30:45

==============================
📥 1단계: 브라우저 데이터 수집
==============================
✅ Chrome: 45개 기록 수집
✅ Safari: 23개 기록 수집
✅ 총 68개의 통합 기록 생성

==============================
🔍 2단계: 검색어 분석
==============================
✅ 12개의 검색어 추출

🔎 검색 분석 결과:
  • 총 검색: 12회
  • 고유 검색어: 10개
  • 평균 검색어 길이: 8.3자
  • 주요 검색 엔진: google (8회)

💡 검색 인사이트:
  • 보통 수준의 검색 활동: 총 12회 검색
  • 주요 검색 엔진: google (8회)
  • 다양한 주제의 검색
```

### 생성되는 파일들
- `browser_complete_YYYYMMDD_HHMMSS.json` - 완전한 원시 데이터
- `browser_summary_YYYYMMDD.json` - 일일 요약 데이터
- `category_report_YYYYMMDD.txt` - 카테고리 분석 리포트

## 🔍 주요 기능 상세

### 1. Chrome 수집기 (`chrome_collector.py`)
- WebKit timestamp 변환
- SQLite DB 안전한 복사 (락 방지)
- 오늘 날짜 기준 필터링
- 검색어 URL 파라미터 파싱

### 2. Safari 수집기 (`safari_collector.py`)
- Core Data timestamp 변환
- Safari 특화 DB 스키마 처리
- Chrome과 동일한 인터페이스 제공

### 3. 검색어 분석기 (`search_analyzer.py`)
- 7개 주요 검색 엔진 지원
- 검색어 카테고리 자동 분류
- 시간별/브라우저별 검색 패턴 분석
- 검색 다양성 및 행동 인사이트

### 4. 카테고리 분석기 (`category_analyzer.py`)
- 10개 주요 카테고리 자동 분류
- 도메인 + 키워드 매칭
- 시간대별 카테고리 활동 패턴
- 활동 다양성 분석

## 🎯 다음 단계

### 1. 앱 추적기 개발 (예정)
- macOS 앱 사용 시간 추적
- NSWorkspace API 활용
- 앱 카테고리 분류

### 2. 캘린더 통합 (예정)
- EventKit API 연동
- 일정과 실제 활동 매칭
- 시간 효율성 분석

### 3. 데이터 통합 서비스 (예정)
- 모든 데이터 소스 통합
- Obsidian Daily Notes 생성
- PostgreSQL 데이터베이스 연동

## 🛡️ 보안 및 프라이버시

- 모든 데이터는 로컬에서만 처리
- 개인 정보는 외부로 전송되지 않음
- 브라우저 DB는 임시 복사 후 즉시 삭제
- 생성된 JSON 파일은 사용자 관리

## 🚨 문제 해결

### 권한 오류
```bash
# 터미널에 전체 디스크 접근 권한 부여 필요
System Preferences → Security & Privacy → Privacy → Full Disk Access
```

### 브라우저 락 오류
- Chrome/Safari 완전 종료 후 재실행
- 시스템 재시작

### Python 모듈 오류
```bash
# Python 경로 확인
which python3
# 스크립트 실행 디렉토리 확인
pwd
```

## 📈 성능

- Chrome 히스토리 (1MB): ~2초
- Safari 히스토리 (500KB): ~1초
- 데이터 분석 및 저장: ~1초
- **총 실행 시간: 3-5초**

## 🔧 개발자 정보

- **기술 스택**: Python 3.7+, SQLite, JSON
- **API 사용**: macOS Native APIs
- **의존성**: Python 내장 라이브러리만 사용
- **테스트**: macOS 14+ Chrome/Safari

---

**📝 참고**: 이 프로젝트는 개인 데이터 자동화 및 데이터 엔지니어링 학습을 위한 프로젝트입니다.
