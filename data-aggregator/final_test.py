#!/usr/bin/env python3
"""
Personal Logging Platform - 최종 실행 테스트

실제 브라우저 데이터를 사용해서 완전한 파이프라인을 테스트합니다.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# 경로 설정
PROJECT_ROOT = Path('/Users/admin/Documents/GitHub/personal-logging-platform')
DATA_AGGREGATOR_ROOT = PROJECT_ROOT / 'data-aggregator'

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DATA_AGGREGATOR_ROOT))

def main():
    """메인 실행 함수"""
    
    print("🚀 Personal Logging Platform - 최종 테스트")
    print("=" * 60)
    
    # 1. 프로젝트 구조 확인
    print("\n📁 프로젝트 구조 확인...")
    
    required_paths = [
        PROJECT_ROOT,
        PROJECT_ROOT / 'browser-collector' / 'output',
        DATA_AGGREGATOR_ROOT / 'src' / 'integrators',
        DATA_AGGREGATOR_ROOT / 'src' / 'generators',
        DATA_AGGREGATOR_ROOT / 'templates',
        DATA_AGGREGATOR_ROOT / 'output'
    ]
    
    for path in required_paths:
        status = "✅" if path.exists() else "❌"
        print(f"   {status} {path.name}: {path}")
        if not path.exists() and 'output' in str(path):
            path.mkdir(parents=True, exist_ok=True)
            print(f"      📁 생성됨: {path}")
    
    # 2. 브라우저 데이터 확인
    browser_output = PROJECT_ROOT / 'browser-collector' / 'output'
    browser_files = list(browser_output.glob('browser_summary_*.json'))
    
    print(f"\n📊 브라우저 데이터 확인...")
    print(f"   데이터 파일: {len(browser_files)}개")
    
    if not browser_files:
        print("❌ 브라우저 데이터가 없습니다!")
        print("   먼저 browser-collector를 실행해서 데이터를 수집하세요.")
        return False
    
    # 가장 최신 파일 사용
    latest_file = max(browser_files, key=os.path.getctime)
    print(f"   📄 사용할 파일: {latest_file.name}")
    
    # 3. 데이터 로드 및 분석
    print(f"\n🔄 데이터 통합 및 분석...")
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        browser_data = json.load(f)
    
    print(f"   날짜: {browser_data['date']}")
    print(f"   총 방문: {browser_data['summary']['total_visits']}회")
    print(f"   주요 카테고리: {browser_data['highlights']['top_categories'][0][0]}")
    
    # 4. 통합 데이터 생성
    integrated_data = create_integrated_data(browser_data, str(latest_file))
    
    # 통합 데이터 저장
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    date_str = browser_data['date'].replace('-', '')
    integration_file = DATA_AGGREGATOR_ROOT / 'output' / f'integrated_data_{date_str}_{timestamp}.json'
    
    with open(integration_file, 'w', encoding='utf-8') as f:
        json.dump(integrated_data, f, ensure_ascii=False, indent=2)
    
    print(f"   💾 통합 데이터 저장: {integration_file.name}")
    
    # 5. Daily Note 생성
    print(f"\n📝 Daily Note 생성...")
    
    daily_note_content = generate_daily_note(integrated_data)
    
    date_str_formatted = browser_data['date']
    note_file = DATA_AGGREGATOR_ROOT / 'output' / f'{date_str_formatted} - Daily Log.md'
    
    with open(note_file, 'w', encoding='utf-8') as f:
        f.write(daily_note_content)
    
    print(f"   📄 Daily Note 저장: {note_file.name}")
    
    # 6. 결과 요약
    print(f"\n🎉 파이프라인 실행 완료!")
    print(f"=" * 60)
    
    analysis = integrated_data['analysis']
    print(f"📅 처리 날짜: {integrated_data['date']}")
    print(f"📊 총 브라우저 방문: {analysis['activity_overview']['total_browser_visits']}회")
    print(f"💪 생산성 점수: {analysis['productivity_insights']['productivity_score']}/100")
    print(f"🎯 주요 집중 영역: {', '.join(analysis['productivity_insights']['main_focus_areas'])}")
    
    print(f"\n📁 생성된 파일:")
    print(f"   🔗 통합 데이터: {integration_file}")
    print(f"   📝 Daily Note: {note_file}")
    
    print(f"\n💡 오늘의 인사이트:")
    for i, rec in enumerate(analysis['recommendations'][:3], 1):
        print(f"   {i}. {rec}")
    
    print(f"\n✨ Personal Logging Platform이 성공적으로 실행되었습니다! 🌟")
    
    return True


def create_integrated_data(browser_data, source_file_path):
    """통합 데이터 생성"""
    
    # 생산성 점수 계산
    def calculate_productivity_score():
        score = 50
        total_visits = browser_data['summary']['total_visits']
        productive_visits = 0
        
        for category, count in browser_data['highlights']['top_categories']:
            if category in ['developer', 'work', 'education']:
                productive_visits += count
        
        if total_visits > 0:
            productivity_ratio = productive_visits / total_visits
            score += int(productivity_ratio * 40)
        
        return min(100, max(0, score))
    
    # 생산성 비율 계산
    def calculate_productivity_ratio():
        total_visits = browser_data['summary']['total_visits']
        productive_visits = 0
        
        for category, count in browser_data['highlights']['top_categories']:
            if category in ['developer', 'work', 'education']:
                productive_visits += count
        
        return round(productive_visits / total_visits, 3) if total_visits > 0 else 0
    
    # 집중 영역 추출
    def extract_focus_areas():
        focus_areas = []
        for category, count in browser_data['highlights']['top_categories'][:3]:
            if category == 'developer':
                focus_areas.append('개발')
            elif category == 'education':
                focus_areas.append('학습')
            elif category == 'work':
                focus_areas.append('업무')
            else:
                focus_areas.append(category)
        return focus_areas
    
    # 추천사항 생성
    def generate_recommendations():
        recommendations = []
        peak_hour = browser_data['highlights']['peak_hour']
        
        if peak_hour < 6:
            recommendations.append(f"새벽 시간대({peak_hour}시) 활동이 많습니다. 충분한 수면을 위해 취침 시간을 앞당기는 것을 고려해보세요.")
        
        search_count = browser_data['summary']['search_count']
        if search_count > 10:
            recommendations.append("검색 활동이 활발합니다. 찾은 정보를 정리해서 나중에 참고할 수 있도록 문서화해보세요.")
        
        dev_ratio = next((count for cat, count in browser_data['highlights']['top_categories'] if cat == 'developer'), 0)
        if dev_ratio > browser_data['summary']['total_visits'] * 0.5:
            recommendations.append("개발 활동에 집중한 생산적인 하루였습니다. 이런 패턴을 유지하세요!")
        
        return recommendations
    
    return {
        'date': browser_data['date'],
        'timestamp': datetime.now().isoformat(),
        'data_sources': {'browser': True, 'app': False},
        'browser_data': {
            'type': 'browser',
            'date': browser_data['date'],
            'summary': browser_data,
            'complete': None,
            'source_files': {'summary': source_file_path, 'complete': None}
        },
        'app_data': None,
        'analysis': {
            'activity_overview': {
                'total_browser_visits': browser_data['summary']['total_visits'],
                'total_app_sessions': 0,
                'data_richness': 'medium'
            },
            'productivity_insights': {
                'productivity_score': calculate_productivity_score(),
                'main_focus_areas': extract_focus_areas(),
                'browser_productivity_ratio': calculate_productivity_ratio()
            },
            'time_patterns': {
                'browser_peak_hour': browser_data['highlights']['peak_hour'],
                'activity_distribution': f"브라우저 활동 피크: {browser_data['highlights']['peak_hour']}시"
            },
            'category_breakdown': {
                'browser_categories': browser_data['highlights']['top_categories'][:5],
                'top_domains': browser_data['highlights']['top_domains'][:5]
            },
            'recommendations': generate_recommendations()
        }
    }


def generate_daily_note(integrated_data):
    """Daily Note 마크다운 생성"""
    
    browser_data = integrated_data['browser_data']['summary']
    analysis = integrated_data['analysis']
    
    # 생산성 점수에 따른 이모지
    score = analysis['productivity_insights']['productivity_score']
    score_emoji = '🟢' if score >= 80 else '🟡' if score >= 60 else '🔴'
    
    # 피크 시간에 따른 설명
    peak_hour = browser_data['highlights']['peak_hour']
    if peak_hour < 6:
        time_desc = f"🌙 새벽 시간대({peak_hour}시)에 가장 활발한 활동을 보였습니다."
    elif peak_hour < 12:
        time_desc = f"🌅 오전 시간대({peak_hour}시)에 가장 활발한 활동을 보였습니다."
    elif peak_hour < 18:
        time_desc = f"☀️ 오후 시간대({peak_hour}시)에 가장 활발한 활동을 보였습니다."
    else:
        time_desc = f"🌆 저녁 시간대({peak_hour}시)에 가장 활발한 활동을 보였습니다."
    
    # 생산성 비율 설명
    productivity_ratio = analysis['productivity_insights']['browser_productivity_ratio']
    percentage = round(productivity_ratio * 100, 1)
    
    if percentage >= 70:
        productivity_desc = "🎯 웹 브라우징이 주로 업무/학습 목적으로 이루어졌습니다."
    elif percentage >= 40:
        productivity_desc = "⚖️ 업무와 개인 브라우징이 적절히 균형을 이뤘습니다."
    else:
        productivity_desc = "🎮 여가/오락 목적의 웹 활동이 많았습니다."
    
    content = f"""# {integrated_data['date']} Daily Log

## 📊 활동 요약
- **총 브라우저 방문**: {browser_data['summary']['total_visits']}회
- **고유 도메인**: {browser_data['summary']['unique_domains']}개
- **검색 횟수**: {browser_data['summary']['search_count']}회
- **데이터 풍부도**: 🟡 Medium
- **생산성 점수**: {score_emoji} {score}/100
- **주요 활동**: {', '.join(analysis['productivity_insights']['main_focus_areas'])}

## 🌐 웹 브라우징 분석

### 🔗 주요 방문 사이트
| 사이트 | 방문 횟수 |
|-------|----------|"""

    for domain, count in browser_data['highlights']['top_domains'][:5]:
        content += f"\n| {domain} | {count}회 |"

    content += f"""

### 🔍 주요 검색어"""
    
    unique_searches = list(dict.fromkeys(browser_data['highlights']['top_searches'][:10]))
    for i, search in enumerate(unique_searches, 1):
        if search.strip():
            content += f"\n{i}. `{search}`"
    
    content += f"""

### 📊 활동 카테고리
| 카테고리 | 횟수 | 비율 |
|----------|------|------|"""

    total_visits = browser_data['summary']['total_visits']
    for category, count in browser_data['highlights']['top_categories']:
        percentage = round((count / total_visits) * 100, 1) if total_visits > 0 else 0
        content += f"\n| {category} | {count}회 | {percentage}% |"
    
    content += f"""

## 🕒 시간대별 활동

### ⏰ 브라우저 활동 패턴
- **피크 시간**: {peak_hour}시
- {time_desc}

## 📈 생산성 분석

### 📊 생산성 측정
- **생산성 점수**: {score}/100
- {'🎉 **매우 생산적인** 하루를 보내셨습니다!' if score >= 80 else '👍 **생산적인** 하루였습니다.' if score >= 60 else '💪 내일은 더 집중해서 생산성을 높여보세요.'}

### 🌐 브라우저 생산성
- **생산적인 웹 활동 비율**: {percentage}%
- {productivity_desc}

## 💡 인사이트 & 추천

### 💡 개인화된 인사이트"""

    for i, rec in enumerate(analysis['recommendations'], 1):
        content += f"\n{i}. {rec}"
    
    # 태그 생성
    tags = ['#daily-log', '#browser-activity']
    
    # 카테고리 기반 태그
    for category, count in browser_data['highlights']['top_categories'][:3]:
        if category == 'developer':
            tags.extend(['#coding', '#development'])
        elif category == 'education':
            tags.append('#learning')
        elif category == 'work':
            tags.append('#work')
    
    # 생산성 기반 태그
    if score >= 80:
        tags.append('#high-productivity')
    elif score >= 60:
        tags.append('#productive')
    
    # 검색 활동 기반 태그
    if browser_data['summary']['search_count'] > 15:
        tags.append('#research')
    
    content += f"""

## 🏷️ 태그
{' '.join(sorted(set(tags)))}

---
*자동 생성됨 by Personal Logging Platform | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    return content


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
