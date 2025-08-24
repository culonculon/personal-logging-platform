#!/usr/bin/env python3
"""
Personal Logging Platform - 테스트 실행기

데이터 통합 모듈의 기능을 테스트합니다.
"""

import os
import sys
from pathlib import Path

# 현재 디렉토리를 data-aggregator로 설정
os.chdir('/Users/admin/Documents/GitHub/personal-logging-platform/data-aggregator')

# Python 경로 설정
PROJECT_ROOT = Path('/Users/admin/Documents/GitHub/personal-logging-platform')
DATA_AGGREGATOR_ROOT = Path('/Users/admin/Documents/GitHub/personal-logging-platform/data-aggregator')

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DATA_AGGREGATOR_ROOT))

def test_platform():
    """플랫폼 기능 테스트"""
    print("🧪 Personal Logging Platform 테스트 시작!")
    print("=" * 60)
    
    try:
        # 메인 모듈 임포트 테스트
        print("📦 모듈 임포트 테스트...")
        from main import PersonalLoggingPlatform
        print("✅ 메인 모듈 임포트 성공!")
        
        # 플랫폼 초기화
        print("\n🚀 플랫폼 초기화...")
        platform = PersonalLoggingPlatform(str(PROJECT_ROOT))
        print("✅ 플랫폼 초기화 성공!")
        
        # 사용 가능한 데이터 스캔
        print("\n📊 데이터 스캔 테스트...")
        available_data = platform.list_available_data()
        print("✅ 데이터 스캔 완료!")
        
        # 데이터 통합 테스트 (브라우저 데이터만)
        print("\n🔄 데이터 통합 테스트...")
        if available_data['browser_data']:
            print("브라우저 데이터 발견! 통합 테스트 진행...")
            result = platform.run_data_integration_only()
            if result['success']:
                print("✅ 데이터 통합 성공!")
                
                # Daily Note 생성 테스트
                print("\n📝 Daily Note 생성 테스트...")
                integration_data = result['integrated_data']
                note_result = platform.note_generator.generate_daily_note(integration_data)
                print(f"✅ Daily Note 생성 성공: {note_result}")
                
                # 생성된 노트 내용 미리보기
                print("\n👀 생성된 노트 미리보기:")
                print("-" * 40)
                with open(note_result, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines[:20]):  # 처음 20줄만 표시
                        print(f"{i+1:2d}: {line.rstrip()}")
                    if len(lines) > 20:
                        print(f"... (총 {len(lines)}줄 중 20줄 표시)")
                
            else:
                print(f"❌ 데이터 통합 실패: {result.get('error', 'Unknown error')}")
        else:
            print("⚠️ 브라우저 데이터가 없습니다. 기본 테스트만 실행합니다.")
            
            # 샘플 데이터로 노트 생성 테스트
            print("\n📝 샘플 데이터로 노트 생성 테스트...")
            sample_data = create_sample_data()
            note_result = platform.note_generator.generate_daily_note(sample_data)
            print(f"✅ 샘플 노트 생성 성공: {note_result}")
        
        print("\n🎉 모든 테스트 완료!")
        return True
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {str(e)}")
        import traceback
        print("상세 에러:")
        traceback.print_exc()
        return False


def create_sample_data():
    """테스트용 샘플 데이터 생성"""
    from datetime import datetime
    
    return {
        'date': '2025-08-24',
        'timestamp': datetime.now().isoformat(),
        'data_sources': {'browser': True, 'app': False},
        'browser_data': {
            'summary': {
                'summary': {
                    'total_visits': 121,
                    'unique_domains': 16,
                    'search_count': 14
                },
                'highlights': {
                    'top_domains': [
                        ['github.com', 58],
                        ['www.google.com', 14],
                        ['stackoverflow.com', 12]
                    ],
                    'top_searches': [
                        'python data integration',
                        'obsidian markdown',
                        'personal logging'
                    ],
                    'top_categories': [
                        ['developer', 68],
                        ['other', 44],
                        ['education', 9]
                    ],
                    'peak_hour': 15
                },
                'insights': {
                    'general': [
                        'Today was a productive day with focused development work'
                    ],
                    'search': [
                        'Active learning through targeted searches'
                    ]
                }
            }
        },
        'app_data': None,
        'analysis': {
            'activity_overview': {
                'total_browser_visits': 121,
                'total_app_sessions': 0,
                'data_richness': 'medium'
            },
            'productivity_insights': {
                'productivity_score': 87,
                'main_focus_areas': ['개발', '학습'],
                'browser_productivity_ratio': 0.72
            },
            'recommendations': [
                '오늘은 개발과 학습에 집중한 생산적인 하루였습니다.',
                '일관된 작업 패턴을 유지하고 있습니다.',
                '계속해서 좋은 습관을 유지하세요!'
            ]
        }
    }


if __name__ == "__main__":
    success = test_platform()
    sys.exit(0 if success else 1)
