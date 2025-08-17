"""
앱 추적기 테스트 파일
기본 기능들이 제대로 작동하는지 확인
"""

import sys
from pathlib import Path

# 프로젝트 루트를 파이썬 경로에 추가
sys.path.append(str(Path(__file__).parent))

from collectors.app_collector import AppCollector
from analyzers.app_category_analyzer import AppCategoryAnalyzer


def test_app_collector():
    """앱 수집기 테스트"""
    print("🧪 앱 수집기 테스트 시작...")
    
    try:
        collector = AppCollector()
        
        # 실행 중인 앱 수집 테스트
        running_apps = collector.get_running_apps()
        print(f"   ✅ 실행 중인 앱 수집: {len(running_apps)}개")
        
        # 프로세스 사용량 테스트
        processes = collector.get_process_usage()
        print(f"   ✅ 프로세스 사용량 수집: {len(processes)}개")
        
        # 몇 개 샘플 출력
        if running_apps:
            print(f"   📱 샘플 앱: {running_apps[0]['app_name']}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 앱 수집기 테스트 실패: {e}")
        return False


def test_category_analyzer():
    """카테고리 분석기 테스트"""
    print("\n🧪 카테고리 분석기 테스트 시작...")
    
    try:
        analyzer = AppCategoryAnalyzer()
        
        # 샘플 앱들로 카테고리 분류 테스트
        test_apps = [
            ('com.microsoft.VSCode', 'Visual Studio Code'),
            ('com.google.Chrome', 'Google Chrome'),
            ('com.spotify.client', 'Spotify'),
            ('unknown.bundle', 'Unknown App')
        ]
        
        print("   📊 카테고리 분류 테스트:")
        for bundle_id, app_name in test_apps:
            category = analyzer.categorize_app(bundle_id, app_name)
            print(f"     • {app_name} -> {category}")
        
        # 실제 실행 중인 앱으로 분석 테스트
        collector = AppCollector()
        running_apps = collector.get_running_apps()
        
        if running_apps:
            analysis = analyzer.analyze_running_apps(running_apps)
            print(f"   ✅ 실행 중인 앱 분석: {analysis['active_categories']}개 카테고리")
            
            if analysis['category_counts']:
                print("   📈 카테고리별 앱 수:")
                for category, count in analysis['category_counts'].items():
                    print(f"     • {category}: {count}개")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 카테고리 분석기 테스트 실패: {e}")
        return False


def test_integration():
    """통합 테스트"""
    print("\n🧪 통합 테스트 시작...")
    
    try:
        # 전체 데이터 수집
        collector = AppCollector()
        app_data = collector.collect_all_data()
        
        # 분석
        analyzer = AppCategoryAnalyzer()
        running_analysis = analyzer.analyze_running_apps(app_data['running_apps'])
        productivity = analyzer.analyze_productivity_score(
            app_data['running_apps'], 
            app_data['app_history']
        )
        
        print(f"   ✅ 통합 데이터 수집 완료")
        print(f"   📊 통계:")
        print(f"     • 실행 중인 앱: {len(app_data['running_apps'])}개")
        print(f"     • 활성 카테고리: {running_analysis['active_categories']}개")
        print(f"     • 생산성 점수: {productivity['overall_score']}/100")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 통합 테스트 실패: {e}")
        return False


def main():
    """메인 테스트 실행"""
    print("🚀 App Tracker 테스트 시작")
    print("=" * 40)
    
    tests = [
        ("앱 수집기", test_app_collector),
        ("카테고리 분석기", test_category_analyzer),
        ("통합 기능", test_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} 테스트 실패")
        except Exception as e:
            print(f"❌ {test_name} 테스트 중 예외 발생: {e}")
    
    print("\n" + "=" * 40)
    print(f"🏁 테스트 결과: {passed}/{total} 통과")
    
    if passed == total:
        print("✅ 모든 테스트 통과! 앱 추적기가 정상적으로 작동합니다.")
        print("💡 이제 main.py를 실행하여 전체 데이터를 수집해보세요.")
    else:
        print("⚠️ 일부 테스트 실패. 환경 설정을 확인해주세요.")
        print("필요한 라이브러리: pyobjc-framework-Cocoa, psutil")
    
    return passed == total


if __name__ == "__main__":
    main()
