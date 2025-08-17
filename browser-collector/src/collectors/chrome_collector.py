"""
Chrome 브라우저 히스토리 수집기
Chrome SQLite DB에서 브라우징 데이터를 추출하는 모듈
"""

import sqlite3
import os
import shutil
import tempfile
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
from typing import List, Dict, Optional
import json
import re


class ChromeCollector:
    """Chrome 브라우저 히스토리를 수집하고 분석하는 클래스"""
    
    def __init__(self):
        self.chrome_history_path = os.path.expanduser(
            "~/Library/Application Support/Google/Chrome/Default/History"
        )
        # Chrome은 WebKit epoch (1601-01-01)를 사용
        self.webkit_epoch = datetime(1601, 1, 1)
        
    def is_chrome_available(self) -> bool:
        """Chrome 히스토리 DB가 존재하는지 확인"""
        return os.path.exists(self.chrome_history_path)
    
    def _webkit_timestamp_to_datetime(self, webkit_timestamp: int) -> datetime:
        """Chrome WebKit timestamp를 datetime으로 변환"""
        return self.webkit_epoch + timedelta(microseconds=webkit_timestamp)
    
    def _copy_history_db(self) -> str:
        """
        Chrome 히스토리 DB를 임시 위치로 복사
        (Chrome이 실행 중일 때 락 문제 해결)
        """
        temp_dir = tempfile.gettempdir()
        temp_db_path = os.path.join(temp_dir, "chrome_history_temp.db")
        
        try:
            shutil.copy2(self.chrome_history_path, temp_db_path)
            return temp_db_path
        except Exception as e:
            raise Exception(f"Chrome 히스토리 DB 복사 실패: {e}")
    
    def get_today_history(self, date: Optional[datetime] = None) -> List[Dict]:
        """오늘의 브라우징 히스토리를 가져오기"""
        if not self.is_chrome_available():
            raise Exception("Chrome 히스토리 DB를 찾을 수 없습니다.")
        
        if date is None:
            date = datetime.now().date()
        else:
            date = date.date()
        
        # 오늘 시작/끝 시간을 WebKit timestamp로 변환
        start_of_day = datetime.combine(date, datetime.min.time())
        end_of_day = datetime.combine(date, datetime.max.time())
        
        start_webkit = int((start_of_day - self.webkit_epoch).total_seconds() * 1_000_000)
        end_webkit = int((end_of_day - self.webkit_epoch).total_seconds() * 1_000_000)
        
        # 임시 DB 복사
        temp_db_path = self._copy_history_db()
        
        try:
            conn = sqlite3.connect(temp_db_path)
            cursor = conn.cursor()
            
            # 오늘의 방문 기록 쿼리
            query = """
            SELECT 
                urls.url,
                urls.title,
                visits.visit_time,
                visits.visit_duration,
                visits.transition
            FROM visits
            JOIN urls ON visits.url = urls.id
            WHERE visits.visit_time >= ? AND visits.visit_time <= ?
            ORDER BY visits.visit_time DESC
            """
            
            cursor.execute(query, (start_webkit, end_webkit))
            results = cursor.fetchall()
            
            # 결과를 딕셔너리 리스트로 변환
            history_data = []
            for row in results:
                url, title, visit_time, duration, transition = row
                
                # WebKit timestamp를 datetime으로 변환
                visit_datetime = self._webkit_timestamp_to_datetime(visit_time)
                
                history_data.append({
                    'url': url,
                    'title': title or 'No Title',
                    'visit_time': visit_datetime.isoformat(),
                    'duration': duration or 0,
                    'transition': transition,
                    'domain': urlparse(url).netloc
                })
            
            conn.close()
            return history_data
            
        except Exception as e:
            raise Exception(f"Chrome 히스토리 읽기 실패: {e}")
        finally:
            # 임시 파일 정리
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)
    
    def extract_search_queries(self, history_data: List[Dict]) -> List[Dict]:
        """브라우징 데이터에서 검색어 추출"""
        search_queries = []
        
        # 주요 검색 엔진 패턴
        search_patterns = {
            'google': {
                'domains': ['www.google.com', 'google.com'],
                'param': 'q'
            },
            'naver': {
                'domains': ['search.naver.com'],
                'param': 'query'
            },
            'youtube': {
                'domains': ['www.youtube.com'],
                'param': 'search_query'
            },
            'bing': {
                'domains': ['www.bing.com'],
                'param': 'q'
            }
        }
        
        for entry in history_data:
            url = entry['url']
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            
            # 검색 엔진 매칭
            for engine, config in search_patterns.items():
                if domain in config['domains']:
                    # URL에서 검색어 파라미터 추출
                    query_params = parse_qs(parsed_url.query)
                    search_param = config['param']
                    
                    if search_param in query_params:
                        query = query_params[search_param][0]
                        if query.strip():  # 빈 검색어 제외
                            search_queries.append({
                                'engine': engine,
                                'query': query,
                                'url': url,
                                'visit_time': entry['visit_time'],
                                'title': entry['title']
                            })
                        break
        
        return search_queries
    
    def categorize_websites(self, history_data: List[Dict]) -> Dict[str, List[Dict]]:
        """웹사이트를 카테고리별로 분류"""
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
        
        # 카테고리 분류 규칙
        category_patterns = {
            'social': [
                'facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com',
                'discord.com', 'reddit.com', 'youtube.com', 'tiktok.com'
            ],
            'work': [
                'slack.com', 'notion.so', 'trello.com', 'asana.com', 'teams.microsoft.com',
                'zoom.us', 'meet.google.com', 'confluence.atlassian.com'
            ],
            'news': [
                'naver.com', 'daum.net', 'hani.co.kr', 'chosun.com', 'joins.com',
                'cnn.com', 'bbc.com', 'reuters.com'
            ],
            'entertainment': [
                'netflix.com', 'youtube.com', 'twitch.tv', 'spotify.com',
                'disney.com', 'hulu.com'
            ],
            'shopping': [
                'amazon.com', 'coupang.com', 'gmarket.co.kr', 'auction.co.kr',
                'ebay.com', '11st.co.kr'
            ],
            'education': [
                'coursera.org', 'udemy.com', 'khan.org', 'edx.org',
                'stackoverflow.com', 'wikipedia.org'
            ],
            'developer': [
                'github.com', 'stackoverflow.com', 'medium.com', 'dev.to',
                'docs.python.org', 'developer.mozilla.org', 'aws.amazon.com'
            ]
        }
        
        for entry in history_data:
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
    
    def get_summary_stats(self, history_data: List[Dict]) -> Dict:
        """브라우징 데이터 요약 통계"""
        if not history_data:
            return {}
        
        total_visits = len(history_data)
        unique_domains = len(set(entry['domain'] for entry in history_data))
        
        # 가장 많이 방문한 도메인 Top 5
        domain_counts = {}
        for entry in history_data:
            domain = entry['domain']
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
        
        top_domains = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # 시간별 방문 분포 (시간대별)
        hourly_distribution = {}
        for entry in history_data:
            visit_time = datetime.fromisoformat(entry['visit_time'])
            hour = visit_time.hour
            hourly_distribution[hour] = hourly_distribution.get(hour, 0) + 1
        
        return {
            'total_visits': total_visits,
            'unique_domains': unique_domains,
            'top_domains': top_domains,
            'hourly_distribution': hourly_distribution,
            'first_visit': history_data[-1]['visit_time'] if history_data else None,
            'last_visit': history_data[0]['visit_time'] if history_data else None
        }


def main():
    """테스트용 메인 함수"""
    collector = ChromeCollector()
    
    if not collector.is_chrome_available():
        print("Chrome 히스토리를 찾을 수 없습니다.")
        return
    
    try:
        # 오늘 히스토리 수집
        print("Chrome 히스토리 수집 중...")
        history = collector.get_today_history()
        print(f"총 {len(history)}개 기록 수집됨")
        
        # 검색어 추출
        search_queries = collector.extract_search_queries(history)
        print(f"검색어 {len(search_queries)}개 추출됨")
        
        # 카테고리 분류
        categories = collector.categorize_websites(history)
        
        # 요약 통계
        stats = collector.get_summary_stats(history)
        
        # 결과 출력
        print("\n=== 브라우징 요약 ===")
        print(f"총 방문: {stats.get('total_visits', 0)}회")
        print(f"고유 도메인: {stats.get('unique_domains', 0)}개")
        
        print("\n=== 상위 도메인 ===")
        for domain, count in stats.get('top_domains', []):
            print(f"  {domain}: {count}회")
        
        print("\n=== 검색어 ===")
        for query in search_queries[:5]:  # 상위 5개만
            print(f"  [{query['engine']}] {query['query']}")
        
        print("\n=== 카테고리별 방문 ===")
        for category, entries in categories.items():
            if entries:
                print(f"  {category}: {len(entries)}개")
    
    except Exception as e:
        print(f"에러 발생: {e}")


if __name__ == "__main__":
    main()
