"""
통합 브라우저 수집기
Chrome과 Safari 브라우저 히스토리를 통합하여 수집하는 모듈
"""

from datetime import datetime
from typing import List, Dict, Optional
from .chrome_collector import ChromeCollector
from .safari_collector import SafariCollector


class BrowserCollector:
    """Chrome과 Safari 브라우저 히스토리를 통합 수집하는 클래스"""
    
    def __init__(self):
        self.chrome_collector = ChromeCollector()
        self.safari_collector = SafariCollector()
        
    def get_available_browsers(self) -> List[str]:
        """사용 가능한 브라우저 목록 반환"""
        browsers = []
        if self.chrome_collector.is_chrome_available():
            browsers.append('chrome')
        if self.safari_collector.is_safari_available():
            browsers.append('safari')
        return browsers
    
    def collect_all_history(self, date: Optional[datetime] = None) -> Dict[str, List[Dict]]:
        """모든 사용 가능한 브라우저에서 히스토리 수집"""
        all_history = {}
        
        # Chrome 히스토리 수집
        if self.chrome_collector.is_chrome_available():
            try:
                chrome_history = self.chrome_collector.get_today_history(date)
                all_history['chrome'] = chrome_history
                print(f"✅ Chrome: {len(chrome_history)}개 기록 수집")
            except Exception as e:
                print(f"❌ Chrome 수집 실패: {e}")
                all_history['chrome'] = []
        
        # Safari 히스토리 수집
        if self.safari_collector.is_safari_available():
            try:
                safari_history = self.safari_collector.get_today_history(date)
                all_history['safari'] = safari_history
                print(f"✅ Safari: {len(safari_history)}개 기록 수집")
            except Exception as e:
                print(f"❌ Safari 수집 실패: {e}")
                all_history['safari'] = []
        
        return all_history
    
    def merge_histories(self, all_history: Dict[str, List[Dict]]) -> List[Dict]:
        """여러 브라우저의 히스토리를 시간순으로 병합"""
        merged = []
        
        for browser, history in all_history.items():
            for entry in history:
                # 브라우저 정보 추가
                entry_with_browser = entry.copy()
                entry_with_browser['browser'] = browser
                merged.append(entry_with_browser)
        
        # 시간순으로 정렬 (최신순)
        merged.sort(key=lambda x: x['visit_time'], reverse=True)
        return merged
    
    def extract_all_search_queries(self, all_history: Dict[str, List[Dict]]) -> List[Dict]:
        """모든 브라우저에서 검색어 추출"""
        all_searches = []
        
        # Chrome 검색어
        if 'chrome' in all_history:
            chrome_searches = self.chrome_collector.extract_search_queries(all_history['chrome'])
            for search in chrome_searches:
                search['browser'] = 'chrome'
                all_searches.append(search)
        
        # Safari 검색어
        if 'safari' in all_history:
            safari_searches = self.safari_collector.extract_search_queries(all_history['safari'])
            for search in safari_searches:
                search['browser'] = 'safari'
                all_searches.append(search)
        
        # 시간순으로 정렬
        all_searches.sort(key=lambda x: x['visit_time'], reverse=True)
        return all_searches
    
    def categorize_all_websites(self, merged_history: List[Dict]) -> Dict[str, List[Dict]]:
        """통합된 히스토리를 카테고리별로 분류"""
        categories = {
            'social': [],
            'work': [],
            'news': [],
            'entertainment': [],
            'shopping': [],
            'education': [],
            'developer': [],
            'other': []
        }
        
        # 카테고리 분류 규칙 (확장된 버전)
        category_patterns = {
            'social': [
                'facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com',
                'discord.com', 'reddit.com', 'youtube.com', 'tiktok.com',
                'snapchat.com', 'pinterest.com', 'tumblr.com'
            ],
            'work': [
                'slack.com', 'notion.so', 'trello.com', 'asana.com', 'teams.microsoft.com',
                'zoom.us', 'meet.google.com', 'confluence.atlassian.com', 'jira.atlassian.com',
                'monday.com', 'clickup.com', 'basecamp.com'
            ],
            'news': [
                'naver.com', 'daum.net', 'hani.co.kr', 'chosun.com', 'joins.com',
                'cnn.com', 'bbc.com', 'reuters.com', 'news.google.com',
                'yna.co.kr', 'sbs.co.kr', 'kbs.co.kr', 'mbc.co.kr'
            ],
            'entertainment': [
                'netflix.com', 'youtube.com', 'twitch.tv', 'spotify.com',
                'disney.com', 'hulu.com', 'prime.amazon.com', 'apple.com/tv'
            ],
            'shopping': [
                'amazon.com', 'coupang.com', 'gmarket.co.kr', 'auction.co.kr',
                'ebay.com', '11st.co.kr', 'interpark.com', 'yes24.com'
            ],
            'education': [
                'coursera.org', 'udemy.com', 'khan.org', 'edx.org',
                'stackoverflow.com', 'wikipedia.org', 'w3schools.com',
                'codecademy.com', 'pluralsight.com'
            ],
            'developer': [
                'github.com', 'stackoverflow.com', 'medium.com', 'dev.to',
                'docs.python.org', 'developer.mozilla.org', 'aws.amazon.com',
                'docker.com', 'kubernetes.io', 'golang.org'
            ]
        }
        
        for entry in merged_history:
            domain = entry['domain']
            categorized = False
            
            # 도메인 매칭으로 카테고리 결정
            for category, patterns in category_patterns.items():
                if any(pattern in domain for pattern in patterns):
                    categories[category].append(entry)
                    categorized = True
                    break
            
            # 매칭되지 않으면 'other'로 분류
            if not categorized:
                categories['other'].append(entry)
        
        return categories
    
    def get_comprehensive_stats(self, all_history: Dict[str, List[Dict]], merged_history: List[Dict]) -> Dict:
        """포괄적인 브라우징 통계 생성"""
        if not merged_history:
            return {}
        
        # 기본 통계
        total_visits = len(merged_history)
        unique_domains = len(set(entry['domain'] for entry in merged_history))
        
        # 브라우저별 통계
        browser_stats = {}
        for browser, history in all_history.items():
            if history:
                browser_stats[browser] = {
                    'visits': len(history),
                    'unique_domains': len(set(entry['domain'] for entry in history))
                }
        
        # 도메인 방문 횟수
        domain_counts = {}
        for entry in merged_history:
            domain = entry['domain']
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
        
        top_domains = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # 시간별 분포
        hourly_distribution = {}
        for entry in merged_history:
            visit_time = datetime.fromisoformat(entry['visit_time'])
            hour = visit_time.hour
            hourly_distribution[hour] = hourly_distribution.get(hour, 0) + 1
        
        # 브라우저별 시간 분포
        browser_hourly = {}
        for entry in merged_history:
            browser = entry['browser']
            visit_time = datetime.fromisoformat(entry['visit_time'])
            hour = visit_time.hour
            
            if browser not in browser_hourly:
                browser_hourly[browser] = {}
            browser_hourly[browser][hour] = browser_hourly[browser].get(hour, 0) + 1
        
        return {
            'total_visits': total_visits,
            'unique_domains': unique_domains,
            'browser_stats': browser_stats,
            'top_domains': top_domains,
            'hourly_distribution': hourly_distribution,
            'browser_hourly_distribution': browser_hourly,
            'first_visit': merged_history[-1]['visit_time'] if merged_history else None,
            'last_visit': merged_history[0]['visit_time'] if merged_history else None,
            'available_browsers': list(all_history.keys())
        }


def main():
    """테스트용 메인 함수"""
    collector = BrowserCollector()
    
    available_browsers = collector.get_available_browsers()
    print(f"사용 가능한 브라우저: {available_browsers}")
    
    if not available_browsers:
        print("사용 가능한 브라우저가 없습니다.")
        return
    
    try:
        # 모든 브라우저에서 히스토리 수집
        print("\n모든 브라우저 히스토리 수집 중...")
        all_history = collector.collect_all_history()
        
        # 히스토리 병합
        merged_history = collector.merge_histories(all_history)
        print(f"총 {len(merged_history)}개 기록 병합됨")
        
        # 검색어 추출
        all_searches = collector.extract_all_search_queries(all_history)
        print(f"총 {len(all_searches)}개 검색어 추출됨")
        
        # 카테고리 분류
        categories = collector.categorize_all_websites(merged_history)
        
        # 포괄적인 통계 생성
        stats = collector.get_comprehensive_stats(all_history, merged_history)
        
        # 결과 출력
        print("\n=== 통합 브라우징 요약 ===")
        print(f"총 방문: {stats.get('total_visits', 0)}회")
        print(f"고유 도메인: {stats.get('unique_domains', 0)}개")
        
        print("\n=== 브라우저별 통계 ===")
        for browser, browser_stat in stats.get('browser_stats', {}).items():
            print(f"  {browser}: {browser_stat['visits']}회 방문, {browser_stat['unique_domains']}개 도메인")
        
        print("\n=== 상위 도메인 ===")
        for domain, count in stats.get('top_domains', [])[:5]:
            print(f"  {domain}: {count}회")
        
        print("\n=== 주요 검색어 ===")
        for query in all_searches[:5]:
            print(f"  [{query['browser']}-{query['engine']}] {query['query']}")
        
        print("\n=== 카테고리별 방문 ===")
        for category, entries in categories.items():
            if entries:
                print(f"  {category}: {len(entries)}개")
    
    except Exception as e:
        print(f"에러 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
