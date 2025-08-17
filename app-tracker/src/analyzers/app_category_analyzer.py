"""
앱 카테고리 분석기
앱 번들 ID와 이름을 기반으로 카테고리 분류 및 분석
"""

import json
from typing import Dict, List, Tuple
from collections import defaultdict, Counter
from datetime import datetime


class AppCategoryAnalyzer:
    """앱을 카테고리별로 분류하고 사용 패턴을 분석하는 클래스"""
    
    def __init__(self):
        # 앱 카테고리 매핑 (번들 ID 기반)
        self.category_mapping = {
            # 개발 도구
            'developer': [
                'com.microsoft.VSCode', 'com.apple.dt.Xcode', 'com.jetbrains.pycharm',
                'com.sublimetext.3', 'com.github.atom', 'com.apple.Terminal',
                'com.iterm2', 'com.docker.docker', 'com.postmanlabs.mac',
                'com.jetbrains.intellij', 'com.jetbrains.webstorm', 'com.vim',
                'com.sourcetreeapp.mac', 'com.git-tower.mac', 'com.panic.nova',
                'com.github.GitHubClient', 'org.tabby'  # GitHub Desktop, Tabby Terminal
            ],
            
            # 브라우저
            'browser': [
                'com.google.Chrome', 'com.apple.Safari', 'org.mozilla.firefox',
                'com.microsoft.edgemac', 'com.operasoftware.Opera', 'com.brave.Browser'
            ],
            
            # 업무/생산성
            'productivity': [
                'com.microsoft.Word', 'com.microsoft.Excel', 'com.microsoft.PowerPoint',
                'com.apple.Pages', 'com.apple.Numbers', 'com.apple.Keynote',
                'com.notion.id', 'com.evernote.Evernote', 'com.bear-writer.BearMarkdown',
                'com.culturedcode.ThingsMac', 'com.omnigroup.OmniFocus3',
                'com.readdle.smartemail-Mac', 'com.microsoft.Outlook',
                'md.obsidian', 'com.anthropic.claudefordesktop'  # Obsidian, Claude
            ],
            
            # 커뮤니케이션
            'communication': [
                'com.apple.MobileSMS', 'com.discord', 'com.slack.desktop',
                'us.zoom.xos', 'com.microsoft.teams', 'com.skype.skype',
                'com.telegram.desktop', 'org.whispersystems.signal-desktop',
                'com.apple.FaceTime', 'com.apple.Mail',
                'com.jandi.osx.JANDI', 'com.kakao.KakaoTalkMac'  # JANDI, 카카오톡
            ],
            
            # 미디어/엔터테인먼트
            'entertainment': [
                'com.spotify.client', 'com.apple.Music', 'com.apple.TV',
                'com.netflix.Netflix', 'com.youtube.desktop', 'com.apple.QuickTimePlayerX',
                'com.vlc.vlc', 'com.adobe.Photoshop', 'com.adobe.Illustrator',
                'com.apple.Photos', 'com.figma.Desktop'
            ],
            
            # 시스템/유틸리티
            'system': [
                'com.apple.finder', 'com.apple.ActivityMonitor', 'com.apple.Console',
                'com.apple.systempreferences', 'com.apple.calculator', 'com.apple.TextEdit',
                'com.apple.Preview', 'com.apple.Automator', 'com.apple.ScriptEditor'
            ],
            
            # 게임
            'gaming': [
                'com.valvesoftware.steam', 'com.epicgames.launcher', 'com.blizzard.app',
                'com.riotgames.Riot Client', 'com.apple.gamecenter'
            ]
        }
        
        # 앱 이름 기반 키워드 매핑 (번들 ID가 없는 경우 대비)
        self.name_keywords = {
            'developer': ['code', 'terminal', 'git', 'docker', 'vim', 'emacs', 'studio', 'xcode', 'tabby', 'github'],
            'browser': ['chrome', 'safari', 'firefox', 'edge', 'opera', 'brave'],
            'productivity': ['word', 'excel', 'powerpoint', 'pages', 'numbers', 'keynote', 'notion', 'bear', 'obsidian', 'claude'],
            'communication': ['slack', 'discord', 'zoom', 'teams', 'skype', 'telegram', 'signal', 'facetime', 'jandi', '카카오톡', 'kakaotalk'],
            'entertainment': ['spotify', 'music', 'netflix', 'youtube', 'vlc', 'photoshop', 'figma'],
            'system': ['finder', 'activity', 'console', 'preferences', 'calculator', 'textedit'],
            'gaming': ['steam', 'epic', 'blizzard', 'riot', 'game']
        }
    
    def categorize_app(self, bundle_id: str, app_name: str) -> str:
        """앱을 카테고리로 분류"""
        # 번들 ID 기반 분류 (우선순위)
        for category, bundle_ids in self.category_mapping.items():
            if bundle_id in bundle_ids:
                return category
        
        # 앱 이름 기반 분류 (번들 ID 매칭 실패 시)
        app_name_lower = app_name.lower()
        for category, keywords in self.name_keywords.items():
            for keyword in keywords:
                if keyword in app_name_lower:
                    return category
        
        return 'other'  # 분류되지 않은 앱
    
    def analyze_running_apps(self, running_apps: List[Dict]) -> Dict:
        """실행 중인 앱들을 카테고리별로 분석"""
        category_stats = defaultdict(list)
        category_counts = Counter()
        
        for app in running_apps:
            bundle_id = app.get('bundle_id', 'Unknown')
            app_name = app.get('app_name', 'Unknown')
            category = self.categorize_app(bundle_id, app_name)
            
            category_stats[category].append({
                'app_name': app_name,
                'bundle_id': bundle_id,
                'is_active': app.get('is_active', False),
                'is_frontmost': app.get('is_frontmost', False),
                'pid': app.get('pid')
            })
            category_counts[category] += 1
        
        return {
            'category_breakdown': dict(category_stats),
            'category_counts': dict(category_counts),
            'total_apps': len(running_apps),
            'active_categories': len(category_stats)
        }
    
    def analyze_usage_patterns(self, app_history: List[Dict]) -> Dict:
        """앱 사용 히스토리에서 패턴 분석"""
        category_usage = defaultdict(float)  # 카테고리별 총 사용 시간
        category_frequency = defaultdict(int)  # 카테고리별 사용 빈도
        hourly_patterns = defaultdict(lambda: defaultdict(float))  # 시간대별 카테고리 사용
        
        for record in app_history:
            bundle_id = record.get('bundle_id', 'Unknown')
            app_name = record.get('app_name', 'Unknown')
            duration = record.get('duration_minutes', 0)
            timestamp = record.get('timestamp', '')
            
            category = self.categorize_app(bundle_id, app_name)
            
            # 사용 시간 및 빈도 누적
            category_usage[category] += duration
            category_frequency[category] += 1
            
            # 시간대별 패턴 (시간 추출)
            try:
                hour = datetime.fromisoformat(timestamp).hour
                hourly_patterns[hour][category] += duration
            except:
                pass
        
        return {
            'category_usage_minutes': dict(category_usage),
            'category_frequency': dict(category_frequency),
            'hourly_patterns': {hour: dict(categories) for hour, categories in hourly_patterns.items()},
            'top_categories': sorted(category_usage.items(), key=lambda x: x[1], reverse=True)[:5]
        }
    
    def analyze_productivity_score(self, running_apps: List[Dict], app_history: List[Dict]) -> Dict:
        """생산성 점수 계산"""
        # 생산성 카테고리 가중치
        productivity_weights = {
            'developer': 1.0,
            'productivity': 0.9,
            'communication': 0.7,
            'browser': 0.5,  # 브라우저는 작업용일 수도 있지만 오락용일 수도 있음
            'entertainment': 0.1,
            'gaming': 0.0,
            'system': 0.3,
            'other': 0.5
        }
        
        # 현재 실행 중인 앱 기반 점수
        running_score = 0
        total_running = len(running_apps)
        
        if total_running > 0:
            for app in running_apps:
                category = self.categorize_app(app.get('bundle_id', ''), app.get('app_name', ''))
                weight = productivity_weights.get(category, 0.5)
                running_score += weight
            running_score = (running_score / total_running) * 100
        
        # 히스토리 기반 점수
        history_score = 0
        total_usage_time = 0
        
        for record in app_history:
            category = self.categorize_app(record.get('bundle_id', ''), record.get('app_name', ''))
            duration = record.get('duration_minutes', 0)
            weight = productivity_weights.get(category, 0.5)
            
            history_score += duration * weight
            total_usage_time += duration
        
        if total_usage_time > 0:
            history_score = (history_score / total_usage_time) * 100
        
        return {
            'current_productivity_score': round(running_score, 1),
            'historical_productivity_score': round(history_score, 1),
            'overall_score': round((running_score + history_score) / 2, 1),
            'total_usage_minutes': total_usage_time,
            'productivity_weights': productivity_weights
        }
    
    def generate_category_report(self, app_data: Dict) -> str:
        """카테고리 분석 리포트 생성"""
        running_analysis = self.analyze_running_apps(app_data.get('running_apps', []))
        usage_analysis = self.analyze_usage_patterns(app_data.get('app_history', []))
        productivity = self.analyze_productivity_score(
            app_data.get('running_apps', []), 
            app_data.get('app_history', [])
        )
        
        report_lines = [
            "=" * 60,
            "📱 APP CATEGORY ANALYSIS REPORT",
            "=" * 60,
            f"분석 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "🏃 현재 실행 중인 앱 분석:",
            f"총 앱 개수: {running_analysis['total_apps']}개",
            f"활성 카테고리: {running_analysis['active_categories']}개",
            ""
        ]
        
        # 카테고리별 실행 중인 앱 수
        if running_analysis['category_counts']:
            report_lines.append("📊 카테고리별 실행 중인 앱:")
            for category, count in sorted(running_analysis['category_counts'].items(), 
                                        key=lambda x: x[1], reverse=True):
                percentage = (count / running_analysis['total_apps']) * 100
                report_lines.append(f"  {category}: {count}개 ({percentage:.1f}%)")
            report_lines.append("")
        
        # 사용 패턴 분석
        if usage_analysis['category_usage_minutes']:
            report_lines.extend([
                "⏱️ 카테고리별 사용 시간:",
                ""
            ])
            for category, minutes in usage_analysis['top_categories']:
                hours = minutes / 60
                report_lines.append(f"  {category}: {minutes:.1f}분 ({hours:.1f}시간)")
            report_lines.append("")
        
        # 생산성 점수
        report_lines.extend([
            "🎯 생산성 분석:",
            f"현재 생산성 점수: {productivity['current_productivity_score']}/100",
            f"히스토리 생산성 점수: {productivity['historical_productivity_score']}/100",
            f"종합 생산성 점수: {productivity['overall_score']}/100",
            "",
            "📈 해석:",
        ])
        
        # 생산성 점수 해석
        overall_score = productivity['overall_score']
        if overall_score >= 80:
            report_lines.append("  🟢 매우 높은 생산성 - 주로 업무/개발 도구 사용")
        elif overall_score >= 60:
            report_lines.append("  🟡 높은 생산성 - 업무와 기타 활동의 균형")
        elif overall_score >= 40:
            report_lines.append("  🟠 보통 생산성 - 업무와 오락의 혼재")
        else:
            report_lines.append("  🔴 낮은 생산성 - 주로 오락/기타 활동")
        
        report_lines.extend([
            "",
            "=" * 60,
            "리포트 끝"
        ])
        
        return "\n".join(report_lines)


if __name__ == "__main__":
    # 테스트용 샘플 데이터
    sample_running_apps = [
        {'bundle_id': 'com.microsoft.VSCode', 'app_name': 'Visual Studio Code', 'is_active': True},
        {'bundle_id': 'com.google.Chrome', 'app_name': 'Google Chrome', 'is_active': False},
        {'bundle_id': 'com.spotify.client', 'app_name': 'Spotify', 'is_active': False}
    ]
    
    analyzer = AppCategoryAnalyzer()
    
    print("=== 앱 카테고리 분석기 테스트 ===")
    
    # 개별 앱 분류 테스트
    for app in sample_running_apps:
        category = analyzer.categorize_app(app['bundle_id'], app['app_name'])
        print(f"{app['app_name']} -> {category}")
    
    # 실행 중인 앱 분석 테스트
    running_analysis = analyzer.analyze_running_apps(sample_running_apps)
    print(f"\n실행 중인 앱 분석: {running_analysis}")
