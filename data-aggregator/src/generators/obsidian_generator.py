"""
옵시디언 노트 생성기 - 통합된 데이터를 예쁜 마크다운 Daily Notes로 변환

Personal Logging Platform
Author: Personal Data Engineer
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from string import Template
import re


class ObsidianNoteGenerator:
    """통합 데이터를 옵시디언 Daily Notes로 변환하는 클래스"""
    
    def __init__(self, template_dir: str, output_dir: str):
        """
        Args:
            template_dir: 템플릿 디렉토리 경로
            output_dir: 출력 디렉토리 경로
        """
        self.template_dir = Path(template_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 기본 템플릿 생성
        self._ensure_templates_exist()
    
    def _ensure_templates_exist(self):
        """기본 템플릿이 없으면 생성"""
        self.template_dir.mkdir(parents=True, exist_ok=True)
        
        # 메인 Daily Note 템플릿
        main_template_path = self.template_dir / "daily_note_template.md"
        if not main_template_path.exists():
            self._create_default_template()
    
    def _create_default_template(self):
        """기본 Daily Note 템플릿 생성"""
        template_content = """# ${date} Daily Log

## 📊 활동 요약
${activity_summary}

## 💻 디지털 활동 패턴
${digital_activity}

## 🌐 웹 브라우징 분석
${browser_analysis}

## 📱 앱 사용 패턴
${app_analysis}

## 🕒 시간대별 활동
${time_patterns}

## 📈 생산성 분석
${productivity_analysis}

## 💡 인사이트 & 추천
${insights_recommendations}

## 🏷️ 태그
${tags}

---
*자동 생성됨 by Personal Logging Platform | ${timestamp}*
"""
        
        with open(self.template_dir / "daily_note_template.md", 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        print(f"📝 기본 템플릿 생성됨: {self.template_dir / 'daily_note_template.md'}")
    
    def generate_daily_note(self, integrated_data: Dict, template_name: str = "daily_note_template.md") -> str:
        """통합 데이터를 Daily Note로 변환
        
        Args:
            integrated_data: 데이터 통합기에서 생성된 통합 데이터
            template_name: 사용할 템플릿 파일명
            
        Returns:
            생성된 마크다운 파일의 경로
        """
        print(f"📝 Daily Note 생성 시작: {integrated_data['date']}")
        
        # 템플릿 로드
        template_path = self.template_dir / template_name
        if not template_path.exists():
            raise FileNotFoundError(f"템플릿을 찾을 수 없습니다: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # 템플릿 변수 생성
        template_vars = self._prepare_template_variables(integrated_data)
        
        # 템플릿 렌더링
        template = Template(template_content)
        rendered_note = template.safe_substitute(**template_vars)
        
        # 출력 파일 생성
        date_str = integrated_data['date']
        filename = f"{date_str} - Daily Log.md"
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered_note)
        
        print(f"✅ Daily Note 생성 완료: {output_path}")
        return str(output_path)
    
    def _prepare_template_variables(self, data: Dict) -> Dict[str, str]:
        """템플릿 변수 준비"""
        browser_data = data.get('browser_data')
        app_data = data.get('app_data')
        analysis = data.get('analysis', {})
        
        return {
            'date': data['date'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'activity_summary': self._generate_activity_summary(data, analysis),
            'digital_activity': self._generate_digital_activity_section(data, analysis),
            'browser_analysis': self._generate_browser_section(browser_data),
            'app_analysis': self._generate_app_section(app_data),
            'time_patterns': self._generate_time_patterns_section(browser_data, app_data),
            'productivity_analysis': self._generate_productivity_section(analysis),
            'insights_recommendations': self._generate_insights_section(analysis),
            'tags': self._generate_tags(browser_data, app_data, analysis)
        }
    
    def _generate_activity_summary(self, data: Dict, analysis: Dict) -> str:
        """활동 요약 섹션 생성"""
        summary_parts = []
        
        overview = analysis.get('activity_overview', {})
        productivity = analysis.get('productivity_insights', {})
        
        # 기본 활동 통계
        browser_visits = overview.get('total_browser_visits', 0)
        app_sessions = overview.get('total_app_sessions', 0)
        
        if browser_visits > 0 or app_sessions > 0:
            summary_parts.append(f"- **총 브라우저 방문**: {browser_visits}회")
            if app_sessions > 0:
                summary_parts.append(f"- **총 앱 세션**: {app_sessions}회")
            
            # 데이터 풍부도
            data_richness = overview.get('data_richness', 'low')
            richness_emoji = '🟢' if data_richness == 'high' else '🟡' if data_richness == 'medium' else '🔴'
            summary_parts.append(f"- **데이터 풍부도**: {richness_emoji} {data_richness.title()}")
            
            # 생산성 점수
            productivity_score = productivity.get('productivity_score', 0)
            if productivity_score > 0:
                score_emoji = '🟢' if productivity_score >= 80 else '🟡' if productivity_score >= 60 else '🔴'
                summary_parts.append(f"- **생산성 점수**: {score_emoji} {productivity_score}/100")
            
            # 주요 집중 영역
            focus_areas = productivity.get('main_focus_areas', [])
            if focus_areas:
                focus_text = ', '.join(focus_areas)
                summary_parts.append(f"- **주요 활동**: {focus_text}")
        else:
            summary_parts.append("- 오늘의 디지털 활동 데이터가 수집되지 않았습니다.")
            summary_parts.append("- 브라우저 수집기와 앱 추적기를 실행해서 데이터를 수집해보세요.")
        
        return '\n'.join(summary_parts)
    
    def _generate_digital_activity_section(self, data: Dict, analysis: Dict) -> str:
        """디지털 활동 패턴 섹션 생성"""
        sections = []
        
        browser_data = data.get('browser_data')
        app_data = data.get('app_data')
        
        if browser_data:
            browser_summary = browser_data['summary']['summary']
            sections.append("### 🌐 브라우저 활동")
            sections.append(f"- **방문 횟수**: {browser_summary['total_visits']}회")
            sections.append(f"- **고유 도메인**: {browser_summary['unique_domains']}개")
            sections.append(f"- **검색 횟수**: {browser_summary['search_count']}회")
            sections.append("")
        
        if app_data:
            sections.append("### 📱 앱 활동")
            if app_data['complete']:
                session_count = len(app_data['complete']['sessions'])
                sections.append(f"- **앱 세션**: {session_count}회")
            sections.append("- 상세한 앱 사용 패턴은 아래 '앱 사용 패턴' 섹션을 참고하세요.")
            sections.append("")
        
        if not browser_data and not app_data:
            sections.append("디지털 활동 데이터가 없습니다. 데이터 수집기를 실행해주세요.")
        
        return '\n'.join(sections)
    
    def _generate_browser_section(self, browser_data: Optional[Dict]) -> str:
        """브라우저 분석 섹션 생성"""
        if not browser_data:
            return "브라우저 데이터가 수집되지 않았습니다."
        
        sections = []
        highlights = browser_data['summary']['highlights']
        insights = browser_data['summary']['insights']
        
        # 주요 도메인
        if highlights.get('top_domains'):
            sections.append("### 🔗 주요 방문 사이트")
            sections.append("| 사이트 | 방문 횟수 |")
            sections.append("|-------|----------|")
            for domain, count in highlights['top_domains'][:5]:
                sections.append(f"| {domain} | {count}회 |")
            sections.append("")
        
        # 주요 검색어
        if highlights.get('top_searches'):
            sections.append("### 🔍 주요 검색어")
            unique_searches = list(dict.fromkeys(highlights['top_searches'][:10]))  # 중복 제거
            for i, search in enumerate(unique_searches, 1):
                if search.strip():  # 빈 검색어 제외
                    sections.append(f"{i}. `{search}`")
            sections.append("")
        
        # 카테고리 분석
        if highlights.get('top_categories'):
            sections.append("### 📊 활동 카테고리")
            sections.append("| 카테고리 | 횟수 | 비율 |")
            sections.append("|----------|------|------|")
            total_visits = browser_data['summary']['summary']['total_visits']
            for category, count in highlights['top_categories']:
                percentage = round((count / total_visits) * 100, 1) if total_visits > 0 else 0
                sections.append(f"| {category} | {count}회 | {percentage}% |")
            sections.append("")
        
        # 인사이트
        if insights:
            sections.append("### 💡 브라우징 인사이트")
            for category, insight_list in insights.items():
                if insight_list:
                    sections.append(f"**{category.title()}**")
                    for insight in insight_list:
                        sections.append(f"- {insight}")
                    sections.append("")
        
        return '\n'.join(sections)
    
    def _generate_app_section(self, app_data: Optional[Dict]) -> str:
        """앱 사용 패턴 섹션 생성"""
        if not app_data:
            return "앱 사용 데이터가 수집되지 않았습니다. 앱 추적기를 실행해주세요."
        
        return "앱 사용 데이터 분석 기능이 곧 추가될 예정입니다."
    
    def _generate_time_patterns_section(self, browser_data: Optional[Dict], app_data: Optional[Dict]) -> str:
        """시간대별 활동 섹션 생성"""
        sections = []
        
        if browser_data:
            peak_hour = browser_data['summary']['highlights']['peak_hour']
            sections.append(f"### ⏰ 브라우저 활동 패턴")
            sections.append(f"- **피크 시간**: {peak_hour}시")
            
            if peak_hour < 6:
                sections.append(f"- 🌙 새벽 시간대({peak_hour}시)에 가장 활발한 활동을 보였습니다.")
            elif peak_hour < 12:
                sections.append(f"- 🌅 오전 시간대({peak_hour}시)에 가장 활발한 활동을 보였습니다.")
            elif peak_hour < 18:
                sections.append(f"- ☀️ 오후 시간대({peak_hour}시)에 가장 활발한 활동을 보였습니다.")
            else:
                sections.append(f"- 🌆 저녁 시간대({peak_hour}시)에 가장 활발한 활동을 보였습니다.")
            
            sections.append("")
        
        if app_data:
            sections.append("### 📱 앱 사용 시간 패턴")
            sections.append("앱 시간 패턴 분석 기능이 곧 추가될 예정입니다.")
            sections.append("")
        
        if not browser_data and not app_data:
            sections.append("시간 패턴 분석을 위한 데이터가 부족합니다.")
        
        return '\n'.join(sections)
    
    def _generate_productivity_section(self, analysis: Dict) -> str:
        """생산성 분석 섹션 생성"""
        sections = []
        productivity = analysis.get('productivity_insights', {})
        
        if productivity:
            # 생산성 점수
            score = productivity.get('productivity_score', 0)
            if score > 0:
                sections.append(f"### 📊 생산성 측정")
                sections.append(f"- **생산성 점수**: {score}/100")
                
                if score >= 80:
                    sections.append(f"- 🎉 **매우 생산적인** 하루를 보내셨습니다!")
                elif score >= 60:
                    sections.append(f"- 👍 **생산적인** 하루였습니다.")
                else:
                    sections.append(f"- 💪 내일은 더 집중해서 생산성을 높여보세요.")
                
                sections.append("")
            
            # 브라우저 생산성 비율
            browser_ratio = productivity.get('browser_productivity_ratio', 0)
            if browser_ratio > 0:
                sections.append(f"### 🌐 브라우저 생산성")
                percentage = round(browser_ratio * 100, 1)
                sections.append(f"- **생산적인 웹 활동 비율**: {percentage}%")
                
                if percentage >= 70:
                    sections.append("- 🎯 웹 브라우징이 주로 업무/학습 목적으로 이루어졌습니다.")
                elif percentage >= 40:
                    sections.append("- ⚖️ 업무와 개인 브라우징이 적절히 균형을 이뤘습니다.")
                else:
                    sections.append("- 🎮 여가/오락 목적의 웹 활동이 많았습니다.")
                
                sections.append("")
        
        if not sections:
            sections.append("생산성 분석을 위한 충분한 데이터가 없습니다.")
        
        return '\n'.join(sections)
    
    def _generate_insights_section(self, analysis: Dict) -> str:
        """인사이트 및 추천 섹션 생성"""
        sections = []
        recommendations = analysis.get('recommendations', [])
        
        if recommendations:
            sections.append("### 💡 개인화된 인사이트")
            for i, rec in enumerate(recommendations, 1):
                sections.append(f"{i}. {rec}")
            sections.append("")
        
        # 추가 분석 결과가 있다면 포함
        focus_analysis = analysis.get('focus_analysis', {})
        if focus_analysis:
            sections.append("### 🎯 집중도 분석")
            sections.append("집중도 분석 기능이 곧 추가될 예정입니다.")
            sections.append("")
        
        if not sections:
            sections.append("### 💭 오늘의 한 줄 요약")
            sections.append("더 나은 분석을 위해 데이터를 꾸준히 수집해보세요!")
        
        return '\n'.join(sections)
    
    def _generate_tags(self, browser_data: Optional[Dict], app_data: Optional[Dict], analysis: Dict) -> str:
        """태그 생성"""
        tags = set()
        
        # 날짜 태그
        tags.add("#daily-log")
        
        # 브라우저 기반 태그
        if browser_data:
            tags.add("#browser-activity")
            highlights = browser_data['summary']['highlights']
            
            # 카테고리 기반 태그
            if highlights.get('top_categories'):
                for category, count in highlights['top_categories'][:3]:
                    if category == 'developer':
                        tags.add("#coding")
                        tags.add("#development")
                    elif category == 'education':
                        tags.add("#learning")
                    elif category == 'work':
                        tags.add("#work")
                    elif category == 'shopping':
                        tags.add("#shopping")
            
            # 검색 활동 기반 태그
            search_count = browser_data['summary']['summary']['search_count']
            if search_count > 15:
                tags.add("#research")
        
        # 앱 기반 태그
        if app_data:
            tags.add("#app-tracking")
        
        # 생산성 기반 태그
        productivity = analysis.get('productivity_insights', {})
        score = productivity.get('productivity_score', 0)
        if score >= 80:
            tags.add("#high-productivity")
        elif score >= 60:
            tags.add("#productive")
        
        # 데이터 소스 태그
        if browser_data and app_data:
            tags.add("#full-tracking")
        elif browser_data:
            tags.add("#browser-only")
        elif app_data:
            tags.add("#app-only")
        else:
            tags.add("#no-data")
        
        return ' '.join(sorted(tags))
    
    def create_obsidian_vault_note(self, integrated_data: Dict, vault_path: str, template_name: str = "daily_note_template.md") -> str:
        """옵시디언 Vault에 직접 Daily Note 생성
        
        Args:
            integrated_data: 통합 데이터
            vault_path: 옵시디언 Vault 경로
            template_name: 템플릿 파일명
            
        Returns:
            생성된 노트 파일의 경로
        """
        vault_path = Path(vault_path)
        if not vault_path.exists():
            raise FileNotFoundError(f"옵시디언 Vault를 찾을 수 없습니다: {vault_path}")
        
        print(f"📓 옵시디언 Vault에 노트 생성: {vault_path}")
        
        # Daily Notes 폴더 확인/생성
        daily_notes_dir = vault_path / "Daily Notes"
        daily_notes_dir.mkdir(exist_ok=True)
        
        # 임시로 일반 노트 생성 후 복사
        temp_note = self.generate_daily_note(integrated_data, template_name)
        
        # Vault에 복사
        date_str = integrated_data['date']
        vault_filename = f"{date_str}.md"  # 옵시디언 표준 형식
        vault_note_path = daily_notes_dir / vault_filename
        
        # 파일 복사
        with open(temp_note, 'r', encoding='utf-8') as src:
            with open(vault_note_path, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
        
        print(f"✅ 옵시디언 노트 생성 완료: {vault_note_path}")
        return str(vault_note_path)


if __name__ == "__main__":
    # 테스트 실행
    import sys
    from pathlib import Path
    
    # 예시 통합 데이터 생성
    sample_data = {
        'date': '2025-08-24',
        'timestamp': datetime.now().isoformat(),
        'data_sources': {'browser': True, 'app': False},
        'browser_data': {
            'summary': {
                'summary': {'total_visits': 121, 'unique_domains': 16, 'search_count': 14},
                'highlights': {
                    'top_domains': [['github.com', 58], ['www.google.com', 14]],
                    'top_searches': ['python', 'github', 'obsidian'],
                    'top_categories': [['developer', 68], ['other', 44]],
                    'peak_hour': 15
                }
            }
        },
        'analysis': {
            'activity_overview': {'total_browser_visits': 121, 'data_richness': 'medium'},
            'productivity_insights': {'productivity_score': 85, 'main_focus_areas': ['개발']},
            'recommendations': ['집중도가 높았습니다. 좋은 패턴을 유지하세요.']
        }
    }
    
    # 테스트 실행
    project_root = Path("/Users/admin/Documents/GitHub/personal-logging-platform")
    template_dir = project_root / "data-aggregator" / "templates"
    output_dir = project_root / "data-aggregator" / "output"
    
    generator = ObsidianNoteGenerator(str(template_dir), str(output_dir))
    note_path = generator.generate_daily_note(sample_data)
    
    print(f"\n🎯 테스트 노트 생성 완료!")
    print(f"📁 위치: {note_path}")
