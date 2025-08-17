#!/usr/bin/env python3
"""
Chrome 수집기 간단 테스트
"""

import sys
import os

# 현재 디렉토리를 Python path에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from collectors.chrome_collector import ChromeCollector

def test_chrome_collector():
    """Chrome 수집기 기본 테스트"""
    print("🧪 Chrome 수집기 테스트 시작")
    
    # 수집기 초기화
    collector = ChromeCollector()
    
    # Chrome 가용성 확인
    print(f"Chrome 가용성: {collector.is_chrome_available()}")
    print(f"Chrome 경로: {collector.chrome_history_path}")
    
    if not collector.is_chrome_available():
        print("❌ Chrome 히스토리 파일을 찾을 수 없습니다.")
        return
    
    try:
        # 히스토리 수집 테스트
        print("\n📖 히스토리 수집 테스트...")
        history = collector.get_today_history()
        print(f"✅ 수집된 기록: {len(history)}개")
        
        if history:
            # 첫 번째 기록 출력
            print(f"\n📄 첫 번째 기록 예시:")
            first = history[0]
            print(f"  URL: {first['url'][:80]}...")
            print(f"  제목: {first['title'][:50]}...")
            print(f"  방문시간: {first['visit_time']}")
            print(f"  도메인: {first['domain']}")
            
            # 검색어 추출 테스트
            print(f"\n🔍 검색어 추출 테스트...")
            searches = collector.extract_search_queries(history)
            print(f"✅ 추출된 검색어: {len(searches)}개")
            
            if searches:
                print(f"검색어 예시:")
                for i, search in enumerate(searches[:3]):
                    print(f"  {i+1}. [{search['engine']}] {search['query']}")
            
            # 카테고리 분류 테스트
            print(f"\n📂 카테고리 분류 테스트...")
            categories = collector.categorize_websites(history)
            print(f"✅ 카테고리 분류 완료")
            
            for cat, items in categories.items():
                if items:
                    print(f"  {cat}: {len(items)}개")
            
            # 통계 테스트
            print(f"\n📊 통계 생성 테스트...")
            stats = collector.get_summary_stats(history)
            print(f"✅ 통계 생성 완료")
            print(f"  총 방문: {stats['total_visits']}회")
            print(f"  고유 도메인: {stats['unique_domains']}개")
            print(f"  상위 도메인: {len(stats['top_domains'])}개")
        
        else:
            print("📭 오늘 브라우징 기록이 없습니다.")
        
        print(f"\n🎉 모든 테스트 완료!")
        
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chrome_collector()
