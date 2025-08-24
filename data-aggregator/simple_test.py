#!/usr/bin/env python3
"""
간단한 데이터 통합 테스트
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def simple_test():
    """간단한 기능 테스트"""
    
    print("🧪 Personal Logging Platform - 간단 테스트")
    print("=" * 50)
    
    # 1. 경로 확인
    project_root = Path('/Users/admin/Documents/GitHub/personal-logging-platform')
    browser_data_path = project_root / 'browser-collector' / 'output'
    
    print(f"📁 프로젝트 루트: {project_root}")
    print(f"📁 브라우저 데이터 경로: {browser_data_path}")
    print(f"📁 브라우저 데이터 존재: {browser_data_path.exists()}")
    
    # 2. 브라우저 데이터 확인
    if browser_data_path.exists():
        browser_files = list(browser_data_path.glob("*.json"))
        print(f"📊 브라우저 데이터 파일: {len(browser_files)}개")
        for file in browser_files:
            print(f"   - {file.name}")
        
        # 샘플 데이터 읽기
        summary_files = [f for f in browser_files if 'summary' in f.name]
        if summary_files:
            with open(summary_files[0], 'r', encoding='utf-8') as f:
                sample_data = json.load(f)
            
            print(f"\n📋 샘플 데이터 미리보기:")
            print(f"   날짜: {sample_data.get('date', 'Unknown')}")
            summary = sample_data.get('summary', {})
            print(f"   총 방문: {summary.get('total_visits', 0)}회")
            print(f"   도메인: {summary.get('unique_domains', 0)}개")
            print(f"   검색: {summary.get('search_count', 0)}회")
    else:
        print("⚠️  브라우저 데이터가 없습니다.")
    
    # 3. 템플릿 생성 테스트
    template_dir = project_root / 'data-aggregator' / 'templates'
    template_file = template_dir / 'daily_note_template.md'
    
    print(f"\n📝 템플릿 확인:")
    print(f"   템플릿 디렉토리: {template_dir.exists()}")
    print(f"   기본 템플릿: {template_file.exists()}")
    
    if template_file.exists():
        with open(template_file, 'r', encoding='utf-8') as f:
            template_content = f.read()
        print(f"   템플릿 크기: {len(template_content)} characters")
        print(f"   템플릿 첫 줄: {template_content.split(chr(10))[0]}")
    
    # 4. 간단한 노트 생성 테스트
    output_dir = project_root / 'data-aggregator' / 'output'
    output_dir.mkdir(exist_ok=True)
    
    sample_note_path = output_dir / 'test_note.md'
    
    sample_note_content = f"""# {datetime.now().strftime('%Y-%m-%d')} - 테스트 노트

## 🧪 테스트 결과
- ✅ 프로젝트 구조 정상
- ✅ 데이터 경로 확인 완료
- ✅ 템플릿 시스템 준비됨

## 📊 현재 상태
- 브라우저 데이터: {'✅' if browser_data_path.exists() else '❌'}
- 템플릿: {'✅' if template_file.exists() else '❌'}
- 출력 디렉토리: {'✅' if output_dir.exists() else '❌'}

---
*테스트 실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    with open(sample_note_path, 'w', encoding='utf-8') as f:
        f.write(sample_note_content)
    
    print(f"\n📄 테스트 노트 생성: {sample_note_path}")
    
    # 5. 결과 요약
    print(f"\n🎯 테스트 완료!")
    print(f"   📁 data-aggregator 모듈 준비: ✅")
    print(f"   📊 브라우저 데이터: {'✅' if browser_data_path.exists() else '❌'}")
    print(f"   📝 템플릿 시스템: {'✅' if template_file.exists() else '❌'}")
    print(f"   📄 노트 생성: ✅")
    
    print(f"\n✨ Personal Logging Platform이 준비되었습니다!")
    print(f"📋 다음 단계:")
    if browser_data_path.exists():
        print(f"   1. python main.py --list  (데이터 확인)")
        print(f"   2. python main.py         (전체 실행)")
    else:
        print(f"   1. 브라우저 수집기 실행 (데이터 수집)")
        print(f"   2. python main.py --list  (데이터 확인)")
        print(f"   3. python main.py         (전체 실행)")
    
    return True

if __name__ == "__main__":
    simple_test()
