"""
데이터 통합기 - 브라우저 및 앱 데이터를 통합하여 하나의 일일 활동 로그 생성

Personal Logging Platform
Author: Personal Data Engineer
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import glob
from collections import defaultdict


class DataIntegrator:
    """브라우저 데이터와 앱 데이터를 통합하는 클래스"""
    
    def __init__(self, project_root: str):
        """
        Args:
            project_root: personal-logging-platform 프로젝트 루트 경로
        """
        self.project_root = Path(project_root)
        self.browser_data_path = self.project_root / "browser-collector" / "output"
        self.app_data_path = self.project_root / "app-tracker" / "src" / "output"
        
    def load_browser_data(self, target_date: str = None) -> Optional[Dict]:
        """브라우저 데이터 로드
        
        Args:
            target_date: YYYY-MM-DD 형식. None이면 가장 최신 데이터
            
        Returns:
            통합된 브라우저 데이터 딕셔너리
        """
        try:
            if target_date:
                # 특정 날짜 데이터 찾기
                summary_pattern = f"browser_summary_{target_date.replace('-', '')}.json"
                complete_pattern = f"browser_complete_{target_date.replace('-', '')}_*.json"
            else:
                # 최신 데이터 찾기
                summary_files = list(self.browser_data_path.glob("browser_summary_*.json"))
                if not summary_files:
                    print("⚠️  브라우저 데이터가 없습니다.")
                    return None
                
                latest_summary = max(summary_files, key=os.path.getctime)
                date_str = latest_summary.stem.split('_')[-1]  # 20250817
                summary_pattern = f"browser_summary_{date_str}.json"
                complete_pattern = f"browser_complete_{date_str}_*.json"
            
            # Summary 데이터 로드
            summary_files = list(self.browser_data_path.glob(summary_pattern))
            complete_files = list(self.browser_data_path.glob(complete_pattern))
            
            if not summary_files:
                print(f"⚠️  {target_date or '최신'} 날짜의 브라우저 요약 데이터를 찾을 수 없습니다.")
                return None
                
            with open(summary_files[0], 'r', encoding='utf-8') as f:
                summary_data = json.load(f)
                
            # Complete 데이터 로드 (있으면)
            complete_data = None
            if complete_files:
                with open(complete_files[0], 'r', encoding='utf-8') as f:
                    complete_data = json.load(f)
            
            return {
                'type': 'browser',
                'date': summary_data.get('date'),
                'summary': summary_data,
                'complete': complete_data,
                'source_files': {
                    'summary': str(summary_files[0]),
                    'complete': str(complete_files[0]) if complete_files else None
                }
            }
            
        except Exception as e:
            print(f"❌ 브라우저 데이터 로드 실패: {str(e)}")
            return None
    
    def load_app_data(self, target_date: str = None) -> Optional[Dict]:
        """앱 데이터 로드
        
        Args:
            target_date: YYYY-MM-DD 형식. None이면 가장 최신 데이터
            
        Returns:
            통합된 앱 데이터 딕셔너리
        """
        try:
            if not self.app_data_path.exists():
                print("⚠️  앱 추적 데이터 디렉토리가 없습니다. 앱 추적기를 먼저 실행해주세요.")
                return None
                
            if target_date:
                # 특정 날짜 데이터 찾기
                summary_pattern = f"app_summary_{target_date.replace('-', '')}.json"
                complete_pattern = f"app_complete_{target_date.replace('-', '')}_*.json"
            else:
                # 최신 데이터 찾기
                summary_files = list(self.app_data_path.glob("app_summary_*.json"))
                if not summary_files:
                    print("⚠️  앱 데이터가 없습니다. 앱 추적기를 먼저 실행해주세요.")
                    return None
                
                latest_summary = max(summary_files, key=os.path.getctime)
                date_str = latest_summary.stem.split('_')[-1]
                summary_pattern = f"app_summary_{date_str}.json"
                complete_pattern = f"app_complete_{date_str}_*.json"
            
            # Summary 데이터 로드
            summary_files = list(self.app_data_path.glob(summary_pattern))
            complete_files = list(self.app_data_path.glob(complete_pattern))
            
            if not summary_files:
                print(f"⚠️  {target_date or '최신'} 날짜의 앱 요약 데이터를 찾을 수 없습니다.")
                return None
                
            with open(summary_files[0], 'r', encoding='utf-8') as f:
                summary_data = json.load(f)
                
            # Complete 데이터 로드 (있으면)
            complete_data = None
            if complete_files:
                with open(complete_files[0], 'r', encoding='utf-8') as f:
                    complete_data = json.load(f)
            
            return {
                'type': 'app',
                'date': summary_data.get('date'),
                'summary': summary_data,
                'complete': complete_data,
                'source_files': {
                    'summary': str(summary_files[0]),
                    'complete': str(complete_files[0]) if complete_files else None
                }
            }
            
        except Exception as e:
            print(f"❌ 앱 데이터 로드 실패: {str(e)}")
            return None
    
    def integrate_daily_data(self, target_date: str = None) -> Dict:
        """일일 데이터 통합
        
        Args:
            target_date: YYYY-MM-DD 형식. None이면 가장 최신 데이터
            
        Returns:
            통합된 일일 활동 데이터
        """
        print(f"🔄 일일 데이터 통합 시작...")
        
        # 데이터 로드
        browser_data = self.load_browser_data(target_date)
        app_data = self.load_app_data(target_date)
        
        # 날짜 결정
        if browser_data and app_data:
            integration_date = browser_data['date'] or app_data['date']
        elif browser_data:
            integration_date = browser_data['date']
        elif app_data:
            integration_date = app_data['date']
        else:
            integration_date = target_date or datetime.now().strftime('%Y-%m-%d')
        
        integrated_data = {
            'date': integration_date,
            'timestamp': datetime.now().isoformat(),
            'data_sources': {
                'browser': browser_data is not None,
                'app': app_data is not None
            },
            'browser_data': browser_data,
            'app_data': app_data
        }
        
        # 통합 분석 수행
        integrated_data['analysis'] = self._perform_integration_analysis(browser_data, app_data)
        
        print(f"✅ 데이터 통합 완료: {integration_date}")
        print(f"   - 브라우저 데이터: {'✓' if browser_data else '✗'}")
        print(f"   - 앱 데이터: {'✓' if app_data else '✗'}")
        
        return integrated_data
    
    def _perform_integration_analysis(self, browser_data: Optional[Dict], app_data: Optional[Dict]) -> Dict:
        """브라우저와 앱 데이터의 교차 분석"""
        analysis = {
            'activity_overview': {},
            'productivity_insights': {},
            'time_patterns': {},
            'focus_analysis': {},
            'category_breakdown': {},
            'recommendations': []
        }
        
        try:
            # 활동 개요 생성
            total_browser_visits = browser_data['summary']['summary']['total_visits'] if browser_data else 0
            total_app_sessions = len(app_data['complete']['sessions']) if app_data and app_data['complete'] else 0
            
            analysis['activity_overview'] = {
                'total_browser_visits': total_browser_visits,
                'total_app_sessions': total_app_sessions,
                'data_richness': 'high' if browser_data and app_data else 'medium'
            }
            
            # 생산성 분석
            if browser_data and app_data:
                browser_dev_ratio = 0
                if browser_data['summary']['highlights']['top_categories']:
                    for cat, count in browser_data['summary']['highlights']['top_categories']:
                        if cat in ['developer', 'work', 'education']:
                            browser_dev_ratio += count / total_browser_visits
                
                analysis['productivity_insights'] = {
                    'browser_productivity_ratio': round(browser_dev_ratio, 3),
                    'main_focus_areas': self._extract_focus_areas(browser_data, app_data),
                    'productivity_score': self._calculate_productivity_score(browser_data, app_data)
                }
            
            # 카테고리 분석
            if browser_data:
                analysis['category_breakdown'] = {
                    'browser_categories': browser_data['summary']['highlights']['top_categories'][:5],
                    'top_domains': browser_data['summary']['highlights']['top_domains'][:5]
                }
                
            # 시간 패턴 분석
            if browser_data:
                peak_hour = browser_data['summary']['highlights']['peak_hour']
                analysis['time_patterns'] = {
                    'browser_peak_hour': peak_hour,
                    'activity_distribution': f"브라우저 활동 피크: {peak_hour}시"
                }
            
            # 추천사항 생성
            analysis['recommendations'] = self._generate_recommendations(browser_data, app_data)
            
        except Exception as e:
            print(f"⚠️  통합 분석 중 오류: {str(e)}")
            analysis['error'] = str(e)
        
        return analysis
    
    def _extract_focus_areas(self, browser_data: Dict, app_data: Dict) -> List[str]:
        """주요 집중 영역 추출"""
        focus_areas = []
        
        if browser_data:
            top_categories = browser_data['summary']['highlights']['top_categories']
            for cat, _ in top_categories[:3]:
                if cat == 'developer':
                    focus_areas.append('개발')
                elif cat == 'education':
                    focus_areas.append('학습')
                elif cat == 'work':
                    focus_areas.append('업무')
                else:
                    focus_areas.append(cat)
        
        return focus_areas
    
    def _calculate_productivity_score(self, browser_data: Dict, app_data: Dict) -> int:
        """생산성 점수 계산 (0-100)"""
        score = 50  # 기본 점수
        
        if browser_data:
            # 개발/업무/교육 카테고리 비율로 점수 조정
            total_visits = browser_data['summary']['summary']['total_visits']
            productive_visits = 0
            
            for cat, count in browser_data['summary']['highlights']['top_categories']:
                if cat in ['developer', 'work', 'education']:
                    productive_visits += count
            
            productivity_ratio = productive_visits / total_visits if total_visits > 0 else 0
            score += int(productivity_ratio * 40)  # 최대 40점 추가
        
        return min(100, max(0, score))
    
    def _generate_recommendations(self, browser_data: Dict, app_data: Dict) -> List[str]:
        """개인화된 추천사항 생성"""
        recommendations = []
        
        if browser_data:
            # 브라우저 패턴 기반 추천
            peak_hour = browser_data['summary']['highlights']['peak_hour']
            
            if peak_hour < 6:  # 새벽 시간 활동
                recommendations.append("새벽 시간대 활동이 많습니다. 충분한 수면을 위해 취침 시간을 앞당기는 것을 고려해보세요.")
            
            # 카테고리 다양성 체크
            categories = len(browser_data['summary']['highlights']['top_categories'])
            if categories < 3:
                recommendations.append("웹 활동이 특정 영역에 집중되어 있습니다. 다양한 분야의 컨텐츠도 탐색해보세요.")
            
            # 검색 활동 분석
            search_count = browser_data['summary']['summary']['search_count']
            if search_count > 20:
                recommendations.append("검색 활동이 활발합니다. 찾은 정보를 정리해서 나중에 참고할 수 있도록 문서화해보세요.")
        
        if not browser_data and not app_data:
            recommendations.append("데이터 수집을 시작해보세요. 더 정확한 분석과 추천을 위해서는 더 많은 데이터가 필요합니다.")
        
        return recommendations
    
    def save_integrated_data(self, integrated_data: Dict, output_path: str = None) -> str:
        """통합 데이터를 JSON 파일로 저장"""
        if output_path is None:
            date_str = integrated_data['date'].replace('-', '')
            timestamp = datetime.now().strftime('%H%M%S')
            filename = f"integrated_data_{date_str}_{timestamp}.json"
            output_path = self.project_root / "data-aggregator" / "output" / filename
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(integrated_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 통합 데이터 저장됨: {output_path}")
        return str(output_path)


if __name__ == "__main__":
    # 테스트 실행
    import sys
    sys.path.append(str(Path(__file__).parent.parent.parent))
    
    project_root = "/Users/admin/Documents/GitHub/personal-logging-platform"
    integrator = DataIntegrator(project_root)
    
    # 데이터 통합 실행
    integrated_data = integrator.integrate_daily_data()
    
    # 결과 저장
    output_file = integrator.save_integrated_data(integrated_data)
    
    print(f"\n🎯 데이터 통합 완료!")
    print(f"📁 저장 위치: {output_file}")
    print(f"📊 분석 결과: {integrated_data['analysis']['activity_overview']}")
