"""
앱 추적기 메인 실행 파일
macOS 앱 사용 데이터 수집 및 분석을 통합 실행
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# 프로젝트 루트를 파이썬 경로에 추가
sys.path.append(str(Path(__file__).parent))

from collectors.app_collector import AppCollector
from analyzers.app_category_analyzer import AppCategoryAnalyzer


def main():
    """앱 추적기 메인 실행 함수"""
    print("🚀 Personal Logging Platform - App Tracker")
    print("=" * 50)
    print("macOS 앱 사용 패턴을 수집하고 분석합니다.\n")
    
    try:
        # 1. 앱 데이터 수집
        print("📱 1단계: 앱 사용 데이터 수집 중...")
        collector = AppCollector()
        app_data = collector.collect_all_data()
        
        print(f"   ✅ 실행 중인 앱: {len(app_data['running_apps'])}개")
        print(f"   ✅ 프로세스 정보: {len(app_data['process_usage'])}개")
        print(f"   ✅ 앱 히스토리: {len(app_data['app_history'])}개")
        
        # 2. 완전한 데이터 저장
        print("\n💾 2단계: 완전한 데이터 저장 중...")
        complete_file = collector.save_data(app_data, "output")
        if complete_file:
            print(f"   ✅ 완전 데이터: {complete_file}")
        
        # 3. 카테고리 분석
        print("\n📊 3단계: 앱 카테고리 분석 중...")
        analyzer = AppCategoryAnalyzer()
        
        # 실행 중인 앱 분석
        running_analysis = analyzer.analyze_running_apps(app_data['running_apps'])
        usage_analysis = analyzer.analyze_usage_patterns(app_data['app_history'])
        productivity = analyzer.analyze_productivity_score(
            app_data['running_apps'], 
            app_data['app_history']
        )
        
        # 4. 요약 데이터 생성 및 저장
        print("\n📝 4단계: 요약 데이터 생성 중...")
        summary_data = {
            'collection_info': app_data['collection_info'],
            'summary': {
                'total_running_apps': len(app_data['running_apps']),
                'total_processes': len(app_data['process_usage']),
                'total_history_records': len(app_data['app_history']),
                'analysis_timestamp': datetime.now().isoformat()
            },
            'category_analysis': {
                'running_apps': running_analysis,
                'usage_patterns': usage_analysis,
                'productivity_score': productivity
            },
            'top_apps': {
                'most_used': app_data['usage_stats']['most_used_apps'][:5],
                'currently_running': [
                    {'name': app['app_name'], 'category': analyzer.categorize_app(app['bundle_id'], app['app_name'])}
                    for app in app_data['running_apps'][:10]
                ]
            }
        }
        
        # 요약 파일 저장
        timestamp = datetime.now().strftime("%Y%m%d")
        summary_filename = f"app_summary_{timestamp}.json"
        summary_path = Path("output") / summary_filename
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
        print(f"   ✅ 요약 데이터: {summary_path}")
        
        # 5. 카테고리 리포트 생성
        print("\n📋 5단계: 카테고리 리포트 생성 중...")
        report_content = analyzer.generate_category_report(app_data)
        
        report_filename = f"app_category_report_{timestamp}.txt"
        report_path = Path("output") / report_filename
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"   ✅ 카테고리 리포트: {report_path}")
        
        # 6. 최종 결과 요약 출력
        print("\n" + "=" * 50)
        print("🎉 앱 추적기 실행 완료!")
        print("=" * 50)
        
        print(f"\n📊 수집 결과:")
        print(f"   • 실행 중인 앱: {len(app_data['running_apps'])}개")
        print(f"   • 활성 카테고리: {running_analysis['active_categories']}개")
        print(f"   • 총 사용 시간: {productivity['total_usage_minutes']:.1f}분")
        print(f"   • 생산성 점수: {productivity['overall_score']}/100")
        
        # 카테고리별 앱 수 출력
        if running_analysis['category_counts']:
            print(f"\n🏷️ 카테고리별 현재 실행 중인 앱:")
            for category, count in sorted(running_analysis['category_counts'].items(), 
                                        key=lambda x: x[1], reverse=True):
                percentage = (count / len(app_data['running_apps'])) * 100
                print(f"   • {category}: {count}개 ({percentage:.1f}%)")
        
        # 가장 많이 사용된 앱
        if app_data['usage_stats']['most_used_apps']:
            print(f"\n🔥 가장 많이 사용된 앱 (상위 3개):")
            for i, (app_name, minutes) in enumerate(app_data['usage_stats']['most_used_apps'][:3]):
                print(f"   {i+1}. {app_name}: {minutes:.1f}분")
        
        print(f"\n📁 생성된 파일:")
        print(f"   • 완전 데이터: {complete_file}")
        print(f"   • 요약 데이터: {summary_path}")
        print(f"   • 카테고리 리포트: {report_path}")
        
        print(f"\n💡 다음 단계: 브라우저 데이터와 통합하여 종합 분석 가능")
        
        return True
        
    except ImportError as e:
        print(f"❌ 필수 라이브러리 누락: {e}")
        print("다음 명령어로 설치해주세요:")
        print("pip install pyobjc-framework-Cocoa pyobjc-framework-ApplicationServices psutil")
        return False
        
    except Exception as e:
        print(f"❌ 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
