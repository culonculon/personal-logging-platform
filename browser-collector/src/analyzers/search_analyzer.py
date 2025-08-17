"""
검색어 분석기
브라우징 데이터에서 검색어를 추출하고 분석하는 모듈
"""

import re
from urllib.parse import urlparse, parse_qs
from typing import List, Dict, Optional
from datetime import datetime
from collections import Counter


class SearchAnalyzer:
    """검색어 추출 및 분석 클래스"""
    
    def __init__(self):
        # 검색 엔진 패턴 (확장 가능)
        self.search_patterns = {
            'google': {
                'domains': ['www.google.com', 'google.com', 'google.co.kr'],
                'param': 'q'
            },
            'naver': {
                'domains': ['search.naver.com'],
                'param': 'query'
            },
            'youtube': {
                'domains': ['www.youtube.com', 'youtube.com'],
                'param': 'search_query'
            },
            'bing': {
                'domains': ['www.bing.com', 'bing.com'],
                'param': 'q'
            },
            'duckduckgo': {
                'domains': ['duckduckgo.com'],
                'param': 'q'
            },
            'yahoo': {
                'domains': ['search.yahoo.com'],
                'param': 'p'
            },
            'baidu': {
                'domains': ['www.baidu.com'],
                'param': 'wd'
            }
        }
    
    def extract_search_queries(self, history_data: List[Dict]) -> List[Dict]:
        """브라우징 데이터에서 검색어 추출"""
        search_queries = []
        
        for entry in history_data:
            url = entry['url']
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            
            # 검색 엔진 매칭
            for engine, config in self.search_patterns.items():
                if domain in config['domains']:
                    # URL에서 검색어 파라미터 추출
                    query_params = parse_qs(parsed_url.query)
                    search_param = config['param']
                    
                    if search_param in query_params:
                        query = query_params[search_param][0]
                        if query.strip():  # 빈 검색어 제외
                            search_data = {
                                'engine': engine,
                                'query': query.strip(),
                                'url': url,
                                'visit_time': entry['visit_time'],
                                'title': entry['title'],
                                'domain': domain
                            }
                            
                            # 브라우저 정보가 있으면 추가
                            if 'browser' in entry:
                                search_data['browser'] = entry['browser']
                            
                            search_queries.append(search_data)
                        break
        
        return search_queries
    
    def analyze_search_patterns(self, search_queries: List[Dict]) -> Dict:
        """검색 패턴 분석"""
        if not search_queries:
            return {}
        
        # 검색 엔진별 통계
        engine_counts = Counter(q['engine'] for q in search_queries)
        
        # 검색어 빈도
        query_counts = Counter(q['query'].lower() for q in search_queries)
        
        # 시간대별 검색 분포
        hourly_search = {}
        for query in search_queries:
            visit_time = datetime.fromisoformat(query['visit_time'])
            hour = visit_time.hour
            hourly_search[hour] = hourly_search.get(hour, 0) + 1
        
        # 브라우저별 검색 (브라우저 정보가 있는 경우)
        browser_search = {}
        for query in search_queries:
            if 'browser' in query:
                browser = query['browser']
                browser_search[browser] = browser_search.get(browser, 0) + 1
        
        # 검색어 길이 분석
        query_lengths = [len(q['query']) for q in search_queries]
        avg_query_length = sum(query_lengths) / len(query_lengths) if query_lengths else 0
        
        # 검색어 카테고리 분류
        search_categories = self.categorize_search_queries(search_queries)
        
        return {
            'total_searches': len(search_queries),
            'unique_queries': len(set(q['query'].lower() for q in search_queries)),
            'engine_distribution': dict(engine_counts),
            'top_queries': query_counts.most_common(10),
            'hourly_distribution': hourly_search,
            'browser_distribution': browser_search,
            'average_query_length': round(avg_query_length, 1),
            'search_categories': search_categories,
            'first_search': search_queries[-1]['visit_time'] if search_queries else None,
            'last_search': search_queries[0]['visit_time'] if search_queries else None
        }
    
    def categorize_search_queries(self, search_queries: List[Dict]) -> Dict[str, List[str]]:
        """검색어를 카테고리별로 분류"""
        categories = {
            'programming': [],
            'news': [],
            'shopping': [],
            'entertainment': [],
            'education': [],
            'travel': [],
            'health': [],
            'work': [],
            'other': []
        }
        
        # 카테고리 키워드 패턴
        category_keywords = {
            'programming': [
                'python', 'javascript', 'react', 'vue', 'angular', 'node', 'django',
                'flask', 'git', 'github', 'docker', 'kubernetes', 'aws', 'api',
                'database', 'sql', 'mongodb', 'error', 'bug', 'code', 'programming',
                'development', 'framework', 'library', 'tutorial'
            ],
            'news': [
                '뉴스', '속보', '정치', '경제', '사회', '국제', '스포츠', '연예',
                'news', 'breaking', 'politics', 'economy', 'society'
            ],
            'shopping': [
                '쇼핑', '구매', '가격', '할인', '세일', '리뷰', '배송',
                'shopping', 'buy', 'price', 'discount', 'sale', 'review',
                'amazon', 'coupang', '쿠팡', '11번가', 'gmarket'
            ],
            'entertainment': [
                '영화', '드라마', '음악', '게임', '유튜브', '넷플릭스',
                'movie', 'drama', 'music', 'game', 'youtube', 'netflix',
                'entertainment', 'fun', 'video', 'streaming'
            ],
            'education': [
                '공부', '학습', '강의', '교육', '시험', '자격증', '코스',
                'study', 'learn', 'course', 'education', 'tutorial',
                'exam', 'certification', 'university', 'school'
            ],
            'travel': [
                '여행', '호텔', '항공', '맛집', '관광', '휴가',
                'travel', 'hotel', 'flight', 'restaurant', 'tourism',
                'vacation', 'trip', 'booking'
            ],
            'health': [
                '건강', '병원', '의료', '운동', '다이어트', '약',
                'health', 'hospital', 'medical', 'exercise', 'diet',
                'medicine', 'fitness', 'wellness'
            ],
            'work': [
                '일', '업무', '회사', '취업', '이력서', '면접', '급여',
                'work', 'job', 'company', 'career', 'resume', 'interview',
                'salary', 'business', 'office'
            ]
        }
        
        for query_data in search_queries:
            query = query_data['query'].lower()
            categorized = False
            
            for category, keywords in category_keywords.items():
                if any(keyword.lower() in query for keyword in keywords):
                    categories[category].append(query_data['query'])
                    categorized = True
                    break
            
            if not categorized:
                categories['other'].append(query_data['query'])
        
        # 빈 카테고리 제거
        return {k: v for k, v in categories.items() if v}
    
    def get_search_insights(self, search_queries: List[Dict]) -> List[str]:
        """검색 패턴에서 인사이트 추출"""
        if not search_queries:
            return ["검색 기록이 없습니다."]
        
        insights = []
        analysis = self.analyze_search_patterns(search_queries)
        
        # 검색 활동 수준
        total_searches = analysis['total_searches']
        if total_searches > 20:
            insights.append(f"활발한 검색 활동: 총 {total_searches}회 검색")
        elif total_searches > 10:
            insights.append(f"보통 수준의 검색 활동: 총 {total_searches}회 검색")
        else:
            insights.append(f"가벼운 검색 활동: 총 {total_searches}회 검색")
        
        # 주요 검색 엔진
        engine_dist = analysis['engine_distribution']
        if engine_dist:
            main_engine = max(engine_dist.items(), key=lambda x: x[1])
            insights.append(f"주요 검색 엔진: {main_engine[0]} ({main_engine[1]}회)")
        
        # 검색 패턴
        hourly_dist = analysis['hourly_distribution']
        if hourly_dist:
            peak_hour = max(hourly_dist.items(), key=lambda x: x[1])
            insights.append(f"검색 피크 시간: {peak_hour[0]}시 ({peak_hour[1]}회)")
        
        # 주요 관심사
        categories = analysis['search_categories']
        if categories:
            top_category = max(categories.items(), key=lambda x: len(x[1]))
            insights.append(f"주요 관심 분야: {top_category[0]} ({len(top_category[1])}개 검색어)")
        
        # 검색어 다양성
        unique_ratio = analysis['unique_queries'] / total_searches
        if unique_ratio > 0.8:
            insights.append("매우 다양한 주제의 검색")
        elif unique_ratio > 0.6:
            insights.append("다양한 주제의 검색")
        else:
            insights.append("특정 주제에 집중된 검색")
        
        return insights


def main():
    """테스트용 메인 함수"""
    # 테스트 데이터
    test_data = [
        {
            'url': 'https://www.google.com/search?q=python+tutorial',
            'title': 'python tutorial - Google 검색',
            'visit_time': '2025-08-17T10:30:00',
            'domain': 'www.google.com'
        },
        {
            'url': 'https://search.naver.com/search.naver?query=맛집+추천',
            'title': '맛집 추천 : 네이버 통합검색',
            'visit_time': '2025-08-17T12:15:00',
            'domain': 'search.naver.com'
        }
    ]
    
    analyzer = SearchAnalyzer()
    
    # 검색어 추출
    queries = analyzer.extract_search_queries(test_data)
    print("추출된 검색어:")
    for q in queries:
        print(f"  [{q['engine']}] {q['query']}")
    
    # 검색 패턴 분석
    analysis = analyzer.analyze_search_patterns(queries)
    print(f"\n검색 분석 결과:")
    print(f"  총 검색: {analysis.get('total_searches', 0)}회")
    print(f"  고유 검색어: {analysis.get('unique_queries', 0)}개")
    
    # 인사이트
    insights = analyzer.get_search_insights(queries)
    print(f"\n검색 인사이트:")
    for insight in insights:
        print(f"  • {insight}")


if __name__ == "__main__":
    main()
