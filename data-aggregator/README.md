# Data Aggregator - Personal Logging Platform

브라우저와 앱 데이터를 통합하여 아름다운 옵시디언 Daily Notes를 자동 생성하는 모듈입니다.

## 🎯 주요 기능

- **데이터 통합**: 브라우저 수집기와 앱 추적기 데이터를 하나로 통합
- **마크다운 생성**: 옵시디언 Daily Notes 형식의 예쁜 마크다운 생성
- **생산성 분석**: 디지털 활동 패턴과 생산성 점수 측정
- **옵시디언 연동**: Vault에 직접 노트 생성
- **템플릿 시스템**: 다양한 스타일의 노트 템플릿 지원

## 🏗️ 구조

```
data-aggregator/
├── src/
│   ├── integrators/      # 데이터 통합 로직
│   ├── generators/       # 옵시디언 노트 생성기
│   └── analyzers/        # 종합 분석기 (향후 확장)
├── templates/            # 마크다운 템플릿들
├── output/              # 생성된 노트와 데이터 파일들
├── main.py             # 메인 실행기
└── requirements.txt    # 의존성 패키지
```

## 🚀 사용법

### 기본 실행 (전체 파이프라인)
```bash
# 최신 데이터로 Daily Note 생성
python main.py

# 특정 날짜 데이터 처리
python main.py --date 2025-08-24

# 옵시디언 Vault에 직접 저장
python main.py --vault-path ~/Documents/MyObsidianVault
```

### 단계별 실행
```bash
# 사용 가능한 데이터 확인
python main.py --list

# 데이터 통합만 실행
python main.py --integration-only --date 2025-08-24

# 기존 통합 데이터로 노트 생성
python main.py --note-from-file output/integrated_data_20250824_143052.json
```

### 고급 옵션
```bash
# 커스텀 템플릿 사용
python main.py --template my_custom_template.md

# 프로젝트 루트 직접 지정
python main.py --project-root /path/to/personal-logging-platform
```

## 📝 생성되는 Daily Note 예시

```markdown
# 2025-08-24 Daily Log

## 📊 활동 요약
- **총 브라우저 방문**: 121회
- **데이터 풍부도**: 🟡 Medium
- **생산성 점수**: 🟢 85/100
- **주요 활동**: 개발

## 🌐 웹 브라우징 분석
### 🔗 주요 방문 사이트
| 사이트 | 방문 횟수 |
|-------|----------|
| github.com | 58회 |
| www.google.com | 14회 |

### 🔍 주요 검색어
1. `python data analysis`
2. `macOS NSWorkspace API`
3. `react hooks tutorial`

### 📊 활동 카테고리
| 카테고리 | 횟수 | 비율 |
|----------|------|------|
| developer | 68회 | 56.2% |
| other | 44회 | 36.4% |

## 💡 인사이트 & 추천
1. 새벽 시간대(1시) 활동이 많습니다. 충분한 수면을 위해 취침 시간을 앞당기는 것을 고려해보세요.
2. 검색 활동이 활발합니다. 찾은 정보를 정리해서 나중에 참고할 수 있도록 문서화해보세요.

## 🏷️ 태그
#daily-log #browser-activity #coding #development #high-productivity

---
*자동 생성됨 by Personal Logging Platform | 2025-08-24 14:30:52*
```

## 🔧 설정 및 커스터마이징

### 템플릿 커스터마이징
`templates/` 디렉토리에 새로운 템플릿을 만들어 사용할 수 있습니다:

```markdown
# ${date} 맞춤형 일지

## 나의 하루
${activity_summary}

## 배운 것들
${insights_recommendations}

## 내일 할 일
- [ ] 새로운 목표 설정
```

### 생산성 점수 가중치 조정
`src/integrators/data_integrator.py`에서 생산성 계산 로직을 수정할 수 있습니다.

## 📋 요구사항

- Python 3.9+
- 기존 브라우저 수집기 데이터
- 선택사항: 앱 추적기 데이터
- 선택사항: 옵시디언 Vault

## 🔄 데이터 플로우

1. **데이터 로드**: 브라우저/앱 수집기의 JSON 출력 파일 읽기
2. **데이터 통합**: 두 데이터 소스를 하나의 통합 구조로 결합
3. **분석 수행**: 생산성, 패턴, 인사이트 분석
4. **템플릿 렌더링**: 마크다운 템플릿에 데이터 주입
5. **노트 생성**: 최종 Daily Note 파일 생성
6. **Vault 연동**: (선택사항) 옵시디언 Vault에 직접 저장

## 🎛️ 확장 가능성

- 새로운 데이터 소스 추가 (예: 캘린더, 이메일)
- AI 기반 인사이트 생성
- 주/월간 요약 리포트
- 대시보드 웹 인터페이스
- 자동 실행 스케줄링
- 데이터 시각화 차트 생성
