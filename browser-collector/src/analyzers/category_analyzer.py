"""
카테고리 분석기
웹사이트를 카테고리별로 분류하고 분석하는 모듈
"""

from typing import List, Dict, Optional
from urllib.parse import urlparse
from datetime import datetime
from collections import Counter


class CategoryAnalyzer:
    """웹사이트 카테고리 분석 클래스"""
    
    def __init__(self):
        # 카테고리 분류 규칙 (확장 가능)
        self.category_patterns = {
            'social': {
                'domains': [
                    'facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com',
                    'discord.com', 'reddit.com', 'youtube.com', 'tiktok.com',
                    'snapchat.com', 'pinterest.com', 'tumblr.com', 'kakao.com',
                    'band.us', 'naver.com/cafe', 'cafe.naver.com'
                ],
                'keywords': ['social', 'community', 'chat', 'message']
            },
            'work': {
                'domains': [
                    'slack.com', 'notion.so', 'trello.com', 'asana.com', 'teams.microsoft.com',
                    'zoom.us', 'meet.google.com', 'confluence.atlassian.com', 'jira.atlassian.com',
                    'monday.com', 'clickup.com', 'basecamp.com', 'office.com', 'sharepoint.com',
                    'dropbox.com', 'drive.google.com', 'onedrive.com'
                ],
                'keywords': ['work', 'office', 'team', 'project', 'meeting']
            },
            'news': {
                'domains': [
                    'naver.com', 'daum.net', 'hani.co.kr', 'chosun.com', 'joins.com',
                    'cnn.com', 'bbc.com', 'reuters.com', 'news.google.com', 'news.yahoo.com',
                    'yna.co.kr', 'sbs.co.kr', 'kbs.co.kr', 'mbc.co.kr', 'jtbc.co.kr',
                    'newspim.com', 'mt.co.kr', 'mk.co.kr'
                ],
                'keywords': ['news', 'breaking', 'report', 'article']
            },
            'entertainment': {
                'domains': [
                    'netflix.com', 'youtube.com', 'twitch.tv', 'spotify.com',
                    'disney.com', 'hulu.com', 'prime.amazon.com', 'apple.com/tv',
                    'wavve.com', 'watcha.com', 'tving.com', 'melon.com', 'genie.co.kr'
                ],
                'keywords': ['streaming', 'video', 'music', 'entertainment', 'movie']
            },
            'shopping': {
                'domains': [
                    'amazon.com', 'coupang.com', 'gmarket.co.kr', 'auction.co.kr',
                    'ebay.com', '11st.co.kr', 'interpark.com', 'yes24.com',
                    'aladin.co.kr', 'kyobobook.co.kr', 'lotte.com', 'shinsegae.com'
                ],
                'keywords': ['shop', 'buy', 'cart', 'order', 'product']
            },
            'education': {
                'domains': [
                    'coursera.org', 'udemy.com', 'khan.org', 'edx.org',
                    'stackoverflow.com', 'wikipedia.org', 'w3schools.com',
                    'codecademy.com', 'pluralsight.com', 'hackerrank.com',
                    'leetcode.com', 'programmers.co.kr', 'acmicpc.net'
                ],
                'keywords': ['learn', 'course', 'tutorial', 'education', 'study']
            },
            'developer': {
                'domains': [
                    'github.com', 'stackoverflow.com', 'medium.com', 'dev.to',
                    'docs.python.org', 'developer.mozilla.org', 'aws.amazon.com',
                    'docker.com', 'kubernetes.io', 'golang.org', 'nodejs.org',
                    'reactjs.org', 'vuejs.org', 'angular.io', 'tensorflow.org'
                ],
                'keywords': ['code', 'api', 'documentation', 'developer', 'programming']
            },
            'finance': {
                'domains': [
                    'investing.com', 'finance.yahoo.com', 'bloomberg.com',
                    'kb.co.kr', 'shinhan.com', 'wooribank.com', 'hanabank.com',
                    'nhbank.com', 'kisbank.com', 'krx.co.kr', 'naver.com/finance'
                ],
                'keywords': ['finance', 'bank', 'investment', 'stock', 'money']
            },
            'travel': {
                'domains': [
                    'booking.com', 'expedia.com', 'airbnb.com', 'agoda.com',
                    'yanolja.com', 'goodchoice.kr', 'interpark.com', 'hanatour.com',
                    'modetour.com', 'koreatravelpost.com'
                ],
                'keywords': ['travel', 'hotel', 'flight', 'booking', 'trip']
            },
            'health': {
                'domains': [
                    'webmd.com', 'mayoclinic.org', 'healthline.com',
                    'amc.seoul.kr', 'severance.or.kr', 'snuh.org', 'samsung.com/sec/medical'
                ],
                'keywords': ['health', 'medical', 'hospital', 'doctor', 'medicine']
            }
        }
        
        self.default_category = 'other'
    
    def categorize_website(self, url: str, title: str = "") -> str:
        """단일 웹사이트 카테고리 분류"""
        domain = urlparse(url).netloc.lower()
        title_lower = title.lower()
        url_lower = url.lower()
        
        for category, config in self.category_patterns.items():
            # 도메인 매칭
            if any(pattern in domain for pattern in config['domains']):
                return category
            
            # 키워드 매칭 (URL과 제목에서)
            if any(keyword in url_lower or keyword in title_lower 
                   for keyword in config['keywords']):
                return category
        
        return self.default_category
    
    def categorize_websites(self, history_data: List[Dict]) -> Dict[str, List[Dict]]:
        """웹사이트 목록을 카테고리별로 분류"""
        categories = {category: [] for category in self.category_patterns.keys()}
        categories[self.default_category] = []
        
        for entry in history_data:
            url = entry['url']
            title = entry.get('title', '')
            
            category = self.categorize_website(url, title)
            categories[category].append(entry)
        
        return categories
    
    def analyze_category_patterns(self, categories: Dict[str, List[Dict]]) -> Dict:
        """카테고리별 패턴 분석"""
        analysis = {}
        
        # 카테고리별 기본 통계
        category_stats = {}
        total_visits = sum(len(entries) for entries in categories.values())
        
        for category, entries in categories.items():
            if entries:
                visit_count = len(entries)
                unique_domains = len(set(entry['domain'] for entry in entries))
                
                # 시간대별 분포
                hourly_dist = {}
                for entry in entries:
                    visit_time = datetime.fromisoformat(entry['visit_time'])
                    hour = visit_time.hour
                    hourly_dist[hour] = hourly_dist.get(hour, 0) + 1
                
                # 상위 도메인
                domain_counts = Counter(entry['domain'] for entry in entries)
                top_domains = domain_counts.most_common(5)
                
                category_stats[category] = {
                    'visit_count': visit_count,
                    'percentage': round(visit_count / total_visits * 100, 1) if total_visits > 0 else 0,
                    'unique_domains': unique_domains,
                    'top_domains': top_domains,
                    'hourly_distribution': hourly_dist,
                    'peak_hour': max(hourly_dist.items(), key=lambda x: x[1])[0] if hourly_dist else None,
                    'avg_visits_per_hour': round(visit_count / len(hourly_dist), 1) if hourly_dist else 0
                }
        
        # 전체 분석
        analysis['category_stats'] = category_stats
        analysis['total_visits'] = total_visits
        analysis['active_categories'] = len([cat for cat, entries in categories.items() if entries])
        
        # 주요 카테고리 (방문 횟수 기준)
        sorted_categories = sorted(
            [(cat, stats['visit_count']) for cat, stats in category_stats.items()],
            key=lambda x: x[1], reverse=True
        )
        analysis['top_categories'] = sorted_categories[:5]
        
        # 카테고리별 시간 패턴
        time_patterns = {}
        for category, stats in category_stats.items():
            hourly_dist = stats['hourly_distribution']
            if hourly_dist:
                # 활동 시간대 분류
                morning_visits = sum(hourly_dist.get(h, 0) for h in range(6, 12))
                afternoon_visits = sum(hourly_dist.get(h, 0) for h in range(12, 18))
                evening_visits = sum(hourly_dist.get(h, 0) for h in range(18, 24))
                night_visits = sum(hourly_dist.get(h, 0) for h in range(0, 6))
                
                time_patterns[category] = {
                    'morning': morning_visits,
                    'afternoon': afternoon_visits,
                    'evening': evening_visits,
                    'night': night_visits,
                    'peak_period': max([
                        ('morning', morning_visits),
                        ('afternoon', afternoon_visits),
                        ('evening', evening_visits),
                        ('night', night_visits)
                    ], key=lambda x: x[1])[0]
                }
        
        analysis['time_patterns'] = time_patterns
        
        return analysis
    
    def get_category_insights(self, categories: Dict[str, List[Dict]]) -> List[str]:
        """카테고리 분석에서 인사이트 추출"""
        analysis = self.analyze_category_patterns(categories)
        insights = []
        
        if not analysis['category_stats']:
            return ["웹사이트 방문 기록이 없습니다."]
        
        # 전체 활동 수준
        total_visits = analysis['total_visits']
        active_categories = analysis['active_categories']
        
        insights.append(f"총 {total_visits}회 방문, {active_categories}개 카테고리 활동")
        
        # 주요 카테고리
        top_categories = analysis['top_categories']
        if top_categories:
            main_category, main_count = top_categories[0]
            percentage = round(main_count / total_visits * 100, 1)
            insights.append(f"주요 활동 영역: {main_category} ({percentage}%, {main_count}회)")
        
        # 다양성 분석
        if len(top_categories) >= 3:
            top3_total = sum(count for _, count in top_categories[:3])
            diversity_ratio = top3_total / total_visits
            
            if diversity_ratio < 0.7:
                insights.append("매우 다양한 카테고리의 웹사이트 방문")
            elif diversity_ratio < 0.85:
                insights.append("적당히 다양한 웹사이트 사용 패턴")
            else:
                insights.append("특정 카테고리에 집중된 웹사이트 사용")
        
        # 시간 패턴 인사이트
        time_patterns = analysis['time_patterns']
        category_stats = analysis['category_stats']
        
        # 각 시간대별 주요 활동
        period_activities = {
            'morning': [],
            'afternoon': [],
            'evening': [],
            'night': []
        }
        
        for category, pattern in time_patterns.items():
            peak_period = pattern['peak_period']
            visits = pattern[peak_period]
            if visits > 0:
                period_activities[peak_period].append((category, visits))
        
        for period, activities in period_activities.items():
            if activities:
                activities.sort(key=lambda x: x[1], reverse=True)
                main_activity = activities[0]
                period_name = {
                    'morning': '오전',
                    'afternoon': '오후', 
                    'evening': '저녁',
                    'night': '밤'
                }[period]
                insights.append(f"{period_name} 주요 활동: {main_activity[0]} ({main_activity[1]}회)")
        
        # 특별한 패턴 감지
        for category, stats in category_stats.items():
            if stats['visit_count'] > total_visits * 0.3:  # 30% 이상
                insights.append(f"{category} 카테고리 집중 사용 (전체의 {stats['percentage']}%)")
        
        return insights
    
    def generate_category_report(self, categories: Dict[str, List[Dict]]) -> str:
        """카테고리 분석 리포트 생성"""
        analysis = self.analyze_category_patterns(categories)
        insights = self.get_category_insights(categories)
        
        report = []
        report.append("📂 웹사이트 카테고리 분석 리포트")
        report.append("=" * 40)
        
        # 전체 요약
        report.append(f"\n📊 전체 요약:")
        report.append(f"  • 총 방문: {analysis['total_visits']}회")
        report.append(f"  • 활성 카테고리: {analysis['active_categories']}개")
        
        # 상위 카테고리
        report.append(f"\n🏆 상위 카테고리:")
        for i, (category, count) in enumerate(analysis['top_categories'], 1):
            stats = analysis['category_stats'][category]
            report.append(f"  {i}. {category}: {count}회 ({stats['percentage']}%)")
        
        # 카테고리별 상세
        report.append(f"\n📋 카테고리별 상세:")
        for category, stats in analysis['category_stats'].items():
            if stats['visit_count'] > 0:
                report.append(f"\n  🔹 {category}:")
                report.append(f"    • 방문: {stats['visit_count']}회 ({stats['percentage']}%)")
                report.append(f"    • 고유 도메인: {stats['unique_domains']}개")
                if stats['peak_hour'] is not None:
                    report.append(f"    • 피크 시간: {stats['peak_hour']}시")
                
                # 상위 도메인
                if stats['top_domains']:
                    top_domain = stats['top_domains'][0]
                    report.append(f"    • 주요 사이트: {top_domain[0]} ({top_domain[1]}회)")
        
        # 인사이트
        report.append(f"\n💡 주요 인사이트:")
        for insight in insights:
            report.append(f"  • {insight}")
        
        return "\n".join(report)


def main():
    """테스트용 메인 함수"""
    # 테스트 데이터
    test_data = [
        {
            'url': 'https://github.com/user/repo',
            'title': 'GitHub Repository',
            'visit_time': '2025-08-17T10:30:00',
            'domain': 'github.com'
        },
        {
            'url': 'https://stackoverflow.com/questions/123',
            'title': 'Python question - Stack Overflow',
            'visit_time': '2025-08-17T11:15:00',
            'domain': 'stackoverflow.com'
        },
        {
            'url': 'https://youtube.com/watch?v=abc',
            'title': 'Some Video - YouTube',
            'visit_time': '2025-08-17T15:20:00',
            'domain': 'youtube.com'
        }
    ]
    
    analyzer = CategoryAnalyzer()
    
    # 카테고리 분류
    categories = analyzer.categorize_websites(test_data)
    print("카테고리 분류 결과:")
    for category, entries in categories.items():
        if entries:
            print(f"  {category}: {len(entries)}개")
    
    # 분석 결과
    analysis = analyzer.analyze_category_patterns(categories)
    print(f"\n분석 결과:")
    print(f"  활성 카테고리: {analysis['active_categories']}개")
    print(f"  상위 카테고리: {analysis['top_categories']}")
    
    # 인사이트
    insights = analyzer.get_category_insights(categories)
    print(f"\n인사이트:")
    for insight in insights:
        print(f"  • {insight}")
    
    # 리포트
    print(f"\n{analyzer.generate_category_report(categories)}")


if __name__ == "__main__":
    main()
