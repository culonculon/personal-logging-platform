#!/usr/bin/env python3
"""
Personal Logging Platform - Browser Collector (Enhanced)
브라우저 히스토리를 수집하고 심화 분석하는 메인 실행 파일
"""

import sys
import os
from datetime import datetime
import json

# 현재 디렉토리를 Python path에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from collectors.browser_collector import BrowserCollector
from analyzers.search_analyzer import SearchAnalyzer
from analyzers.category_analyzer import CategoryAnalyzer


def save_to_json(data: dict, filename: str):
    """데이터를 JSON 파일로 저장"""
    output_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(output_dir, exist_ok=True)
    
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 데이터 저장됨: {filepath}")


def main():
    """메인 실행 함수"""
    print("🌐 Personal Logging Platform - Browser Collector (Enhanced)")
    print("=" * 60)
    
    # 수집기 및 분석기 초기화
    browser_collector = BrowserCollector()
    search_analyzer = SearchAnalyzer()
    category_analyzer = CategoryAnalyzer()
    
    available_browsers = browser_collector.get_available_browsers()
    if not available_browsers:
        print("❌ 사용 가능한 브라우저를 찾을 수 없습니다.")
        print("Chrome 또는 Safari가 설치되어 있는지 확인해주세요.")
        return
    
    print(f"📚 사용 가능한 브라우저: {', '.join(available_browsers)}")
    
    try:
        # 오늘 날짜
        today = datetime.now()
        print(f"📅 수집 날짜: {today.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # === 1단계: 데이터 수집 ===
        print(f"\n" + "=" * 30)
        print("📥 1단계: 브라우저 데이터 수집")
        print("=" * 30)
        
        # 모든 브라우저에서 히스토리 수집
        print(f"🔍 브라우저 히스토리 수집 중...")
        all_history = browser_collector.collect_all_history()
        
        # 히스토리 병합
        print(f"🔄 히스토리 병합 중...")
        merged_history = browser_collector.merge_histories(all_history)
        print(f"✅ 총 {len(merged_history)}개의 통합 기록 생성")
        
        if not merged_history:
            print("📭 오늘 브라우징 기록이 없습니다.")
            return
        
        # === 2단계: 검색어 분석 ===
        print(f"\n" + "=" * 30)
        print("🔍 2단계: 검색어 분석")
        print("=" * 30)
        
        # 검색어 추출 및 분석
        search_queries = browser_collector.extract_all_search_queries(all_history)
        print(f"✅ {len(search_queries)}개의 검색어 추출")
        
        if search_queries:
            search_analysis = search_analyzer.analyze_search_patterns(search_queries)
            search_insights = search_analyzer.get_search_insights(search_queries)
            
            print(f"\n🔎 검색 분석 결과:")
            print(f"  • 총 검색: {search_analysis.get('total_searches', 0)}회")
            print(f"  • 고유 검색어: {search_analysis.get('unique_queries', 0)}개")
            print(f"  • 평균 검색어 길이: {search_analysis.get('average_query_length', 0)}자")
            
            engine_dist = search_analysis.get('engine_distribution', {})
            if engine_dist:
                main_engine = max(engine_dist.items(), key=lambda x: x[1])
                print(f"  • 주요 검색 엔진: {main_engine[0]} ({main_engine[1]}회)")
            
            print(f"\n💡 검색 인사이트:")
            for insight in search_insights[:3]:
                print(f"  • {insight}")
        else:
            search_analysis = {}
            search_insights = []
            print("📭 검색 기록이 없습니다.")
        
        # === 3단계: 카테고리 분석 ===
        print(f"\n" + "=" * 30)
        print("📂 3단계: 카테고리 분석")
        print("=" * 30)
        
        # 카테고리 분류 및 분석
        categories = category_analyzer.categorize_websites(merged_history)
        category_analysis = category_analyzer.analyze_category_patterns(categories)
        category_insights = category_analyzer.get_category_insights(categories)
        
        print(f"✅ 카테고리 분류 완료")
        print(f"  • 활성 카테고리: {category_analysis.get('active_categories', 0)}개")
        
        top_categories = category_analysis.get('top_categories', [])
        if top_categories:
            print(f"  • 상위 카테고리:")
            for i, (category, count) in enumerate(top_categories[:3], 1):
                stats = category_analysis['category_stats'][category]
                print(f"    {i}. {category}: {count}회 ({stats['percentage']}%)")
        
        print(f"\n💡 카테고리 인사이트:")
        for insight in category_insights[:3]:
            print(f"  • {insight}")
        
        # === 4단계: 통합 통계 ===
        print(f"\n" + "=" * 30)
        print("📊 4단계: 통합 통계 분석")
        print("=" * 30)
        
        # 포괄적인 통계 생성
        comprehensive_stats = browser_collector.get_comprehensive_stats(all_history, merged_history)
        
        print(f"📈 전체 활동 요약:")
        print(f"  • 총 방문: {comprehensive_stats.get('total_visits', 0)}회")
        print(f"  • 고유 도메인: {comprehensive_stats.get('unique_domains', 0)}개")
        print(f"  • 활성 브라우저: {len(comprehensive_stats.get('available_browsers', []))}개")
        
        # 브라우저별 통계
        browser_stats = comprehensive_stats.get('browser_stats', {})
        if browser_stats:
            print(f"\n🌐 브라우저별 활동:")
            for browser, stats in browser_stats.items():
                print(f"  • {browser.title()}: {stats['visits']}회, {stats['unique_domains']}개 도메인")
        
        # 상위 도메인
        top_domains = comprehensive_stats.get('top_domains', [])
        if top_domains:
            print(f"\n🏆 상위 방문 도메인:")
            for i, (domain, count) in enumerate(top_domains[:5], 1):
                print(f"  {i}. {domain}: {count}회")
        
        # 시간대별 활동
        hourly_dist = comprehensive_stats.get('hourly_distribution', {})
        if hourly_dist:
            print(f"\n⏰ 시간대별 활동 패턴:")
            sorted_hours = sorted(hourly_dist.items())
            max_count = max(hourly_dist.values()) if hourly_dist.values() else 1
            
            # 피크 시간 찾기
            peak_hour = max(hourly_dist.items(), key=lambda x: x[1])
            print(f"  • 피크 시간: {peak_hour[0]}시 ({peak_hour[1]}회)")
            
            # 활동 분포 (간단한 막대그래프)
            print(f"  • 시간대별 분포:")
            for hour, count in sorted_hours:
                if count > 0:
                    bar = "█" * (count * 15 // max_count)
                    print(f"    {hour:02d}시: {count:3d}회 {bar}")
        
        # === 5단계: 데이터 저장 ===
        print(f"\n" + "=" * 30)
        print("💾 5단계: 데이터 저장")
        print("=" * 30)
        
        date_str = today.strftime('%Y%m%d_%H%M%S')
        
        # 완전한 데이터 세트 저장
        complete_data = {
            'metadata': {
                'collection_date': today.strftime('%Y-%m-%d'),
                'collection_timestamp': today.isoformat(),
                'available_browsers': available_browsers,
                'total_records': len(merged_history),
                'version': '1.0'
            },
            'raw_data': {
                'history_by_browser': all_history,
                'merged_history': merged_history
            },
            'search_analysis': {
                'queries': search_queries,
                'analysis': search_analysis,
                'insights': search_insights
            },
            'category_analysis': {
                'categories': categories,
                'analysis': category_analysis,
                'insights': category_insights
            },
            'comprehensive_stats': comprehensive_stats
        }
        
        save_to_json(complete_data, f"browser_complete_{date_str}.json")
        
        # 요약 리포트 저장
        summary_report = {
            'date': today.strftime('%Y-%m-%d'),
            'summary': {
                'total_visits': comprehensive_stats.get('total_visits', 0),
                'unique_domains': comprehensive_stats.get('unique_domains', 0),
                'browsers_used': list(browser_stats.keys()) if browser_stats else [],
                'search_count': len(search_queries),
                'category_count': category_analysis.get('active_categories', 0)
            },
            'highlights': {
                'top_domains': top_domains[:5] if top_domains else [],
                'top_searches': [q['query'] for q in search_queries[:5]] if search_queries else [],
                'top_categories': [(cat, count) for cat, count in top_categories[:5]] if top_categories else [],
                'peak_hour': peak_hour[0] if hourly_dist else None
            },
            'insights': {
                'search': search_insights[:3] if search_insights else [],
                'category': category_insights[:3] if category_insights else [],
                'general': [
                    f"총 {comprehensive_stats.get('total_visits', 0)}회 웹사이트 방문",
                    f"{comprehensive_stats.get('unique_domains', 0)}개의 고유 도메인 접속",
                    f"{len(search_queries)}개의 검색어 사용" if search_queries else "검색 활동 없음"
                ]
            }
        }
        
        save_to_json(summary_report, f"browser_summary_{today.strftime('%Y%m%d')}.json")
        
        # 카테고리 리포트 텍스트 파일로 저장
        category_report_text = category_analyzer.generate_category_report(categories)
        report_filepath = os.path.join(os.path.dirname(__file__), "..", "output", f"category_report_{today.strftime('%Y%m%d')}.txt")
        with open(report_filepath, 'w', encoding='utf-8') as f:
            f.write(category_report_text)
        print(f"📄 카테고리 리포트 저장됨: {report_filepath}")
        
        # === 최종 요약 ===
        print(f"\n" + "=" * 60)
        print("🎉 브라우저 데이터 수집 및 분석 완료!")
        print("=" * 60)
        
        print(f"📊 최종 요약:")
        print(f"  • 수집된 기록: {len(merged_history)}개")
        print(f"  • 브라우저: {', '.join(available_browsers)}")
        print(f"  • 검색어: {len(search_queries)}개")
        print(f"  • 카테고리: {category_analysis.get('active_categories', 0)}개")
        print(f"  • 저장된 파일: 3개 (완전 데이터, 요약, 리포트)")
        
        if top_categories:
            main_category = top_categories[0]
            print(f"  • 주요 활동: {main_category[0]} ({main_category[1]}회)")
        
        if hourly_dist:
            print(f"  • 피크 시간: {peak_hour[0]}시")
        
        print(f"\n💡 다음 단계:")
        print(f"  1. output/ 폴더의 JSON 파일들을 확인해보세요")
        print(f"  2. 앱 추적기 개발을 시작할 수 있습니다")
        print(f"  3. 수집된 데이터를 Obsidian Daily Notes로 변환할 준비가 되었습니다")
        
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        import traceback
        traceback.print_exc()
        print(f"\n🔧 문제 해결:")
        print(f"  • Chrome/Safari 브라우저가 실행 중이면 종료해보세요")
        print(f"  • 디스크 접근 권한을 확인해보세요")
        print(f"  • 터미널에서 'python3 main.py' 명령어로 실행해보세요")


if __name__ == "__main__":
    main()
