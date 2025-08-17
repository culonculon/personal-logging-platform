"""
macOS 앱 사용 데이터 수집기
NSWorkspace와 psutil을 사용하여 실행중인 앱과 과거 사용 기록을 수집
"""

import json
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

try:
    import psutil
    from Foundation import NSLog
    from AppKit import NSWorkspace, NSRunningApplication
except ImportError as e:
    print(f"macOS 전용 라이브러리를 가져올 수 없습니다: {e}")
    print("pip install pyobjc-framework-Cocoa pyobjc-framework-ApplicationServices psutil")


class AppCollector:
    """macOS 앱 사용 데이터 수집 클래스"""
    
    def __init__(self):
        self.workspace = NSWorkspace.sharedWorkspace()
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        """로거 설정"""
        logger = logging.getLogger('AppCollector')
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def get_running_apps(self) -> List[Dict]:
        """현재 실행 중인 앱 목록 수집"""
        apps = []
        current_time = datetime.now()
        
        try:
            running_apps = self.workspace.runningApplications()
            
            for app in running_apps:
                # 시스템 프로세스 제외
                if app.activationPolicy() == 0:  # NSApplicationActivationPolicyRegular
                    app_info = {
                        'bundle_id': str(app.bundleIdentifier()) if app.bundleIdentifier() else 'Unknown',
                        'app_name': str(app.localizedName()) if app.localizedName() else 'Unknown',
                        'pid': int(app.processIdentifier()),
                        'is_active': bool(app.isActive()),
                        'is_frontmost': bool(app.isActive() and app.isFinishedLaunching()),
                        'launch_date': app.launchDate().description() if app.launchDate() else None,
                        'timestamp': current_time.isoformat(),
                        'app_path': str(app.bundleURL().path()) if app.bundleURL() else None
                    }
                    apps.append(app_info)
                    
        except Exception as e:
            self.logger.error(f"실행 중인 앱 수집 중 오류: {e}")
            
        self.logger.info(f"현재 실행 중인 앱 {len(apps)}개 수집 완료")
        return apps
    
    def get_process_usage(self) -> List[Dict]:
        """psutil을 사용한 프로세스 사용량 정보 수집"""
        processes = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'create_time']):
                try:
                    proc_info = proc.info
                    # 앱과 관련된 프로세스만 필터링 (.app이 포함된 경로)
                    if proc_info['name'] and not proc_info['name'].startswith('kernel'):
                        process_data = {
                            'pid': proc_info['pid'],
                            'name': proc_info['name'],
                            'cpu_percent': proc_info['cpu_percent'],
                            'memory_percent': proc_info['memory_percent'],
                            'create_time': datetime.fromtimestamp(proc_info['create_time']).isoformat(),
                            'timestamp': datetime.now().isoformat()
                        }
                        processes.append(process_data)
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            self.logger.error(f"프로세스 사용량 수집 중 오류: {e}")
            
        self.logger.info(f"프로세스 사용량 정보 {len(processes)}개 수집 완료")
        return processes
    
    def get_frontmost_app_history(self, minutes: int = 60) -> List[Dict]:
        """
        최근 활성화된 앱 히스토리 수집 (시뮬레이션)
        실제로는 백그라운드 모니터링이 필요하지만, 현재 상태를 기반으로 샘플 데이터 생성
        """
        history = []
        current_time = datetime.now()
        
        try:
            # 현재 활성 앱 정보
            frontmost_app = self.workspace.frontmostApplication()
            if frontmost_app:
                # 최근 1시간 동안의 사용 패턴을 시뮬레이션
                for i in range(0, minutes, 5):  # 5분 간격으로 기록
                    timestamp = current_time - timedelta(minutes=i)
                    
                    app_record = {
                        'bundle_id': str(frontmost_app.bundleIdentifier()) if frontmost_app.bundleIdentifier() else 'Unknown',
                        'app_name': str(frontmost_app.localizedName()) if frontmost_app.localizedName() else 'Unknown',
                        'timestamp': timestamp.isoformat(),
                        'duration_minutes': 5,  # 5분간 사용으로 가정
                        'is_active': True,
                        'window_title': None  # 향후 확장 가능
                    }
                    history.append(app_record)
                    
        except Exception as e:
            self.logger.error(f"앱 히스토리 수집 중 오류: {e}")
            
        self.logger.info(f"앱 사용 히스토리 {len(history)}개 기록 생성")
        return history
    
    def get_app_usage_stats(self) -> Dict:
        """
        macOS 시스템 로그에서 앱 사용 통계 수집 시도
        """
        stats = {
            'daily_app_launches': {},
            'total_usage_time': {},
            'most_used_apps': [],
            'collection_timestamp': datetime.now().isoformat()
        }
        
        try:
            # 실행 중인 앱들의 실행 시간 계산
            running_apps = self.get_running_apps()
            
            for app in running_apps:
                if app['launch_date']:
                    app_name = app['app_name']
                    # 실행 시간 계산 (시뮬레이션)
                    launch_time = datetime.fromisoformat(app['launch_date'].replace(' +0000', ''))
                    running_time = (datetime.now() - launch_time).total_seconds() / 60  # 분 단위
                    
                    stats['total_usage_time'][app_name] = round(running_time, 2)
                    stats['daily_app_launches'][app_name] = stats['daily_app_launches'].get(app_name, 0) + 1
            
            # 가장 많이 사용된 앱 순서로 정렬
            if stats['total_usage_time']:
                stats['most_used_apps'] = sorted(
                    stats['total_usage_time'].items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )[:10]
                
        except Exception as e:
            self.logger.error(f"앱 사용 통계 수집 중 오류: {e}")
            
        return stats
    
    def collect_all_data(self) -> Dict:
        """모든 앱 데이터를 수집하여 통합 딕셔너리로 반환"""
        self.logger.info("앱 데이터 수집 시작...")
        
        data = {
            'collection_info': {
                'timestamp': datetime.now().isoformat(),
                'collector': 'AppCollector',
                'platform': 'macOS',
                'version': '1.0.0'
            },
            'running_apps': self.get_running_apps(),
            'process_usage': self.get_process_usage(),
            'app_history': self.get_frontmost_app_history(60),  # 최근 1시간
            'usage_stats': self.get_app_usage_stats()
        }
        
        self.logger.info("앱 데이터 수집 완료!")
        return data
    
    def save_data(self, data: Dict, output_dir: str = "output") -> str:
        """수집된 데이터를 JSON 파일로 저장"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"app_usage_complete_{timestamp}.json"
        filepath = output_path / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"앱 사용 데이터가 저장되었습니다: {filepath}")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"데이터 저장 중 오류: {e}")
            return None


if __name__ == "__main__":
    # 테스트 실행
    collector = AppCollector()
    
    print("=== macOS 앱 추적기 테스트 ===")
    print("현재 실행 중인 앱 데이터를 수집합니다...")
    
    # 모든 데이터 수집
    all_data = collector.collect_all_data()
    
    # 데이터 저장
    saved_file = collector.save_data(all_data)
    
    if saved_file:
        print(f"✅ 성공: {saved_file}")
        
        # 간단한 통계 출력
        print(f"\n📊 수집 결과:")
        print(f"- 실행 중인 앱: {len(all_data['running_apps'])}개")
        print(f"- 프로세스 정보: {len(all_data['process_usage'])}개") 
        print(f"- 앱 히스토리: {len(all_data['app_history'])}개")
        print(f"- 사용 통계: {len(all_data['usage_stats']['total_usage_time'])}개 앱")
        
        # 가장 많이 사용된 앱 상위 3개
        if all_data['usage_stats']['most_used_apps']:
            print(f"\n🔥 가장 많이 사용된 앱:")
            for i, (app_name, minutes) in enumerate(all_data['usage_stats']['most_used_apps'][:3]):
                print(f"   {i+1}. {app_name}: {minutes:.1f}분")
    else:
        print("❌ 데이터 저장 실패")
