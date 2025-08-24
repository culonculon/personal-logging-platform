#!/usr/bin/env python3
"""
Personal Logging Platform - 데이터 통합 및 옵시디언 노트 생성 메인 실행기

기능:
- 브라우저 및 앱 데이터 통합
- 옵시디언 Daily Notes 자동 생성
- 원클릭 전체 파이프라인 실행

Usage:
    python main.py [--date YYYY-MM-DD] [--vault-path PATH] [--template TEMPLATE]

Author: Personal Data Engineer
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict

# 프로젝트 루트 추가
PROJECT_ROOT = Path(__file__).parent.parent
DATA_AGGREGATOR_ROOT = Path(__file__).parent
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(DATA_AGGREGATOR_ROOT))

from src.integrators.data_integrator import DataIntegrator
from src.generators.obsidian_generator import ObsidianNoteGenerator


class PersonalLoggingPlatform:
    """Personal Logging Platform 메인 클래스"""
    
    def __init__(self, project_root: str = None):
        """
        Args:
            project_root: 프로젝트 루트 디렉토리. None이면 자동 감지
        """
        if project_root is None:
            project_root = str(PROJECT_ROOT)
        
        self.project_root = Path(project_root)
        
        # 컴포넌트 초기화
        self.data_integrator = DataIntegrator(str(self.project_root))
        
        template_dir = self.project_root / "data-aggregator" / "templates"
        output_dir = self.project_root / "data-aggregator" / "output"
        self.note_generator = ObsidianNoteGenerator(str(template_dir), str(output_dir))
        
        print(f"🚀 Personal Logging Platform 초기화 완료")
        print(f"📁 프로젝트 루트: {self.project_root}")
    
    def run_full_pipeline(self, target_date: str = None, vault_path: str = None, template: str = "daily_note_template.md") -> Dict:
        """전체 파이프라인 실행
        
        Args:
            target_date: YYYY-MM-DD 형식 날짜. None이면 최신 데이터
            vault_path: 옵시디언 Vault 경로. None이면 일반 출력만
            template: 사용할 템플릿 파일명
            
        Returns:
            실행 결과 딕셔너리
        """
        print(f"\n🎯 Personal Logging Platform 파이프라인 시작")
        print(f"📅 대상 날짜: {target_date or '최신 데이터'}")
        print(f"📓 Vault 경로: {vault_path or '일반 출력만'}")
        print("=" * 60)
        
        results = {
            'success': False,
            'target_date': target_date,
            'timestamp': datetime.now().isoformat(),
            'steps': {},
            'outputs': {},
            'errors': []
        }
        
        try:
            # Step 1: 데이터 통합
            print("\n🔄 Step 1: 데이터 통합")
            print("-" * 30)
            integrated_data = self.data_integrator.integrate_daily_data(target_date)
            
            if not integrated_data:
                raise Exception("데이터 통합 실패")
            
            results['steps']['data_integration'] = '✅ 완료'
            results['outputs']['integrated_data'] = integrated_data
            
            # 통합 데이터 저장
            integration_output_path = self.data_integrator.save_integrated_data(integrated_data)
            results['outputs']['integration_file'] = integration_output_path
            
            # Step 2: Daily Note 생성
            print(f"\n📝 Step 2: Daily Note 생성")
            print("-" * 30)
            note_path = self.note_generator.generate_daily_note(integrated_data, template)
            
            results['steps']['note_generation'] = '✅ 완료'
            results['outputs']['daily_note'] = note_path
            
            # Step 3: 옵시디언 Vault 연동 (선택사항)
            if vault_path:
                print(f"\n📓 Step 3: 옵시디언 Vault 연동")
                print("-" * 30)
                vault_note_path = self.note_generator.create_obsidian_vault_note(
                    integrated_data, vault_path, template
                )
                results['steps']['vault_integration'] = '✅ 완료'
                results['outputs']['vault_note'] = vault_note_path
            else:
                results['steps']['vault_integration'] = '⏭️ 건너뜀'
            
            results['success'] = True
            
            # 결과 요약 출력
            self._print_pipeline_summary(results, integrated_data)
            
        except Exception as e:
            error_msg = f"파이프라인 실행 실패: {str(e)}"
            print(f"❌ {error_msg}")
            results['errors'].append(error_msg)
            results['success'] = False
        
        return results
    
    def _print_pipeline_summary(self, results: Dict, integrated_data: Dict):
        """파이프라인 실행 결과 요약 출력"""
        print("\n" + "=" * 60)
        print("🎉 Personal Logging Platform 파이프라인 완료!")
        print("=" * 60)
        
        # 기본 정보
        date = integrated_data.get('date', 'Unknown')
        print(f"📅 처리 날짜: {date}")
        print(f"⏰ 실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 데이터 소스 정보
        data_sources = integrated_data.get('data_sources', {})
        print(f"\n📊 데이터 소스:")
        print(f"   🌐 브라우저: {'✅' if data_sources.get('browser') else '❌'}")
        print(f"   📱 앱: {'✅' if data_sources.get('app') else '❌'}")
        
        # 활동 요약
        analysis = integrated_data.get('analysis', {})
        overview = analysis.get('activity_overview', {})
        if overview:
            print(f"\n📈 활동 요약:")
            browser_visits = overview.get('total_browser_visits', 0)
            app_sessions = overview.get('total_app_sessions', 0)
            if browser_visits > 0:
                print(f"   🌐 브라우저 방문: {browser_visits}회")
            if app_sessions > 0:
                print(f"   📱 앱 세션: {app_sessions}회")
        
        # 생산성 정보
        productivity = analysis.get('productivity_insights', {})
        if productivity:
            score = productivity.get('productivity_score', 0)
            if score > 0:
                print(f"\n💪 생산성 점수: {score}/100")
                focus_areas = productivity.get('main_focus_areas', [])
                if focus_areas:
                    print(f"   🎯 주요 집중 영역: {', '.join(focus_areas)}")
        
        # 출력 파일 정보
        print(f"\n📁 생성된 파일:")
        for key, path in results['outputs'].items():
            if path and key != 'integrated_data':
                print(f"   📄 {key}: {path}")
        
        # 권장사항
        recommendations = analysis.get('recommendations', [])
        if recommendations:
            print(f"\n💡 오늘의 인사이트:")
            for i, rec in enumerate(recommendations[:3], 1):  # 최대 3개만 표시
                print(f"   {i}. {rec}")
        
        print("\n✨ 수고하셨습니다! 내일도 좋은 하루 되세요! 🌟")
    
    def run_data_integration_only(self, target_date: str = None) -> Dict:
        """데이터 통합만 실행"""
        print(f"🔄 데이터 통합만 실행 (날짜: {target_date or '최신'})")
        
        try:
            integrated_data = self.data_integrator.integrate_daily_data(target_date)
            output_path = self.data_integrator.save_integrated_data(integrated_data)
            
            return {
                'success': True,
                'integrated_data': integrated_data,
                'output_path': output_path
            }
        except Exception as e:
            print(f"❌ 데이터 통합 실패: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def run_note_generation_only(self, integration_file: str, vault_path: str = None) -> Dict:
        """노트 생성만 실행 (기존 통합 데이터 사용)"""
        print(f"📝 노트 생성만 실행 (통합 데이터: {integration_file})")
        
        try:
            # 통합 데이터 로드
            with open(integration_file, 'r', encoding='utf-8') as f:
                integrated_data = json.load(f)
            
            # 노트 생성
            note_path = self.note_generator.generate_daily_note(integrated_data)
            
            result = {
                'success': True,
                'note_path': note_path
            }
            
            # Vault 연동
            if vault_path:
                vault_note_path = self.note_generator.create_obsidian_vault_note(
                    integrated_data, vault_path
                )
                result['vault_note_path'] = vault_note_path
            
            return result
            
        except Exception as e:
            print(f"❌ 노트 생성 실패: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def list_available_data(self) -> Dict:
        """사용 가능한 데이터 목록 표시"""
        print("📊 사용 가능한 데이터 스캔...")
        
        available_data = {
            'browser_data': [],
            'app_data': [],
            'integrated_data': []
        }
        
        # 브라우저 데이터 스캔
        browser_path = self.project_root / "browser-collector" / "output"
        if browser_path.exists():
            browser_files = list(browser_path.glob("browser_summary_*.json"))
            for file in browser_files:
                date_match = file.stem.split('_')[-1]  # 20250817
                if len(date_match) == 8:
                    formatted_date = f"{date_match[:4]}-{date_match[4:6]}-{date_match[6:]}"
                    available_data['browser_data'].append({
                        'date': formatted_date,
                        'file': str(file)
                    })
        
        # 앱 데이터 스캔
        app_path = self.project_root / "app-tracker" / "output"
        if app_path.exists():
            app_files = list(app_path.glob("app_summary_*.json"))
            for file in app_files:
                date_match = file.stem.split('_')[-1]
                if len(date_match) == 8:
                    formatted_date = f"{date_match[:4]}-{date_match[4:6]}-{date_match[6:]}"
                    available_data['app_data'].append({
                        'date': formatted_date,
                        'file': str(file)
                    })
        
        # 통합 데이터 스캔
        integration_path = self.project_root / "data-aggregator" / "output"
        if integration_path.exists():
            integration_files = list(integration_path.glob("integrated_data_*.json"))
            for file in integration_files:
                available_data['integrated_data'].append({
                    'file': str(file),
                    'modified': datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
                })
        
        # 결과 출력
        print("\n📋 사용 가능한 데이터:")
        print("-" * 40)
        
        if available_data['browser_data']:
            print("🌐 브라우저 데이터:")
            for data in sorted(available_data['browser_data'], key=lambda x: x['date'], reverse=True)[:5]:
                print(f"   📅 {data['date']}")
        else:
            print("🌐 브라우저 데이터: 없음")
        
        if available_data['app_data']:
            print("\n📱 앱 데이터:")
            for data in sorted(available_data['app_data'], key=lambda x: x['date'], reverse=True)[:5]:
                print(f"   📅 {data['date']}")
        else:
            print("\n📱 앱 데이터: 없음")
        
        if available_data['integrated_data']:
            print("\n🔗 통합 데이터:")
            for data in sorted(available_data['integrated_data'], key=lambda x: x['modified'], reverse=True)[:3]:
                filename = Path(data['file']).name
                print(f"   📄 {filename} (수정: {data['modified']})")
        else:
            print("\n🔗 통합 데이터: 없음")
        
        return available_data


def create_argument_parser():
    """명령행 인수 파서 생성"""
    parser = argparse.ArgumentParser(
        description="Personal Logging Platform - 디지털 활동 데이터 통합 및 옵시디언 노트 생성",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
    python main.py                                    # 최신 데이터로 전체 파이프라인 실행
    python main.py --date 2025-08-24                 # 특정 날짜 데이터 처리
    python main.py --vault-path ~/Obsidian/MyVault   # 옵시디언 Vault에 직접 저장
    python main.py --list                            # 사용 가능한 데이터 목록 보기
    python main.py --integration-only                # 데이터 통합만 실행
        """
    )
    
    parser.add_argument(
        '--date', 
        type=str, 
        help='처리할 날짜 (YYYY-MM-DD 형식). 지정하지 않으면 최신 데이터 사용'
    )
    
    parser.add_argument(
        '--vault-path', 
        type=str, 
        help='옵시디언 Vault 경로. 지정하면 Vault에 직접 노트 생성'
    )
    
    parser.add_argument(
        '--template', 
        type=str, 
        default='daily_note_template.md',
        help='사용할 템플릿 파일명 (기본값: daily_note_template.md)'
    )
    
    parser.add_argument(
        '--list', 
        action='store_true',
        help='사용 가능한 데이터 목록만 표시'
    )
    
    parser.add_argument(
        '--integration-only', 
        action='store_true',
        help='데이터 통합만 실행 (노트 생성 제외)'
    )
    
    parser.add_argument(
        '--note-from-file', 
        type=str,
        help='기존 통합 데이터 파일에서 노트 생성'
    )
    
    parser.add_argument(
        '--project-root', 
        type=str,
        help='프로젝트 루트 디렉토리 경로 (기본값: 자동 감지)'
    )
    
    return parser


def main():
    """메인 함수"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Personal Logging Platform 초기화
    try:
        platform = PersonalLoggingPlatform(args.project_root)
    except Exception as e:
        print(f"❌ 플랫폼 초기화 실패: {str(e)}")
        sys.exit(1)
    
    # 명령 실행
    if args.list:
        platform.list_available_data()
        return
    
    if args.integration_only:
        result = platform.run_data_integration_only(args.date)
        if not result['success']:
            sys.exit(1)
        return
    
    if args.note_from_file:
        if not Path(args.note_from_file).exists():
            print(f"❌ 통합 데이터 파일을 찾을 수 없습니다: {args.note_from_file}")
            sys.exit(1)
        
        result = platform.run_note_generation_only(args.note_from_file, args.vault_path)
        if not result['success']:
            sys.exit(1)
        return
    
    # 기본 동작: 전체 파이프라인 실행
    result = platform.run_full_pipeline(args.date, args.vault_path, args.template)
    
    if not result['success']:
        print(f"\n❌ 파이프라인 실행 실패")
        if result['errors']:
            for error in result['errors']:
                print(f"   💥 {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
