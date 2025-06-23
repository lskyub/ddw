#!/usr/bin/env python3
"""
Markdown to HTML Converter for DDW Services
개인정보처리방침과 지원 페이지를 위한 Markdown -> HTML 변환기

사용법:
python scripts/md-to-html.py <markdown_file> [--type privacy|support] [--lang en|ko] [--service service_name]

예시:
python scripts/md-to-html.py privacy.md --type privacy --lang ko --service gokitty
python scripts/md-to-html.py support.md --type support --lang en --service travelee
"""

import argparse
import os
import re
from datetime import datetime
from pathlib import Path

try:
    import markdown
    from markdown.extensions import codehilite, tables, toc
except ImportError:
    print("❌ markdown 패키지가 필요합니다. 다음 명령어로 설치해주세요:")
    print("pip install markdown")
    exit(1)

# HTML 템플릿들
PRIVACY_TEMPLATE = '''<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Pretendard', sans-serif;
        }}

        body {{
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
        }}

        .nav {{
            background: white;
            padding: 1rem 2rem;
            border-bottom: 1px solid #e9ecef;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .nav-container {{
            max-width: 1000px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .nav-brand {{
            font-size: 1.3rem;
            font-weight: bold;
            color: {brand_color};
            text-decoration: none;
        }}

        .nav-links {{
            display: flex;
            gap: 2rem;
            align-items: center;
        }}

        .nav-link {{
            text-decoration: none;
            color: #666;
            transition: color 0.3s;
        }}

        .nav-link:hover {{
            color: {brand_color};
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem;
        }}

        .header {{
            background: white;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }}

        .header h1 {{
            color: {brand_color};
            margin-bottom: 1rem;
            font-size: 2.5rem;
        }}

        .service-icon {{
            font-size: 3rem;
            margin-bottom: 1rem;
        }}

        .policy-content {{
            background: white;
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }}

        .policy-content h1, .policy-content h2 {{
            color: #2c3e50;
            margin-bottom: 1rem;
            border-bottom: 2px solid {brand_color};
            padding-bottom: 0.5rem;
        }}

        .policy-content h3 {{
            color: #2c3e50;
            margin: 1.5rem 0 1rem;
            font-size: 1.2rem;
        }}

        .policy-content p {{
            margin-bottom: 1rem;
            color: #666;
        }}

        .policy-content ul, .policy-content ol {{
            margin-left: 2rem;
            margin-bottom: 1rem;
        }}

        .policy-content li {{
            margin-bottom: 0.5rem;
            color: #666;
        }}

        .policy-content blockquote {{
            background-color: #e3f2fd;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid {brand_color};
            margin: 1rem 0;
        }}

        .policy-content code {{
            background-color: #f8f9fa;
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        }}

        .policy-content pre {{
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            overflow-x: auto;
            margin: 1rem 0;
        }}

        .last-updated {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
            margin-bottom: 2rem;
            border: 1px solid #e9ecef;
        }}

        .actions {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-top: 2rem;
        }}

        .btn {{
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            text-decoration: none;
            transition: all 0.3s;
            font-weight: 500;
        }}

        .btn-primary {{
            background-color: {brand_color};
            color: white;
        }}

        .btn-primary:hover {{
            background-color: {brand_color_hover};
        }}

        .btn-secondary {{
            background-color: #f8f9fa;
            color: #666;
            border: 1px solid #e9ecef;
        }}

        .btn-secondary:hover {{
            background-color: #e9ecef;
        }}

        @media (max-width: 768px) {{
            .nav-links {{
                display: none;
            }}

            .container {{
                padding: 1rem;
            }}

            .header h1 {{
                font-size: 2rem;
            }}

            .actions {{
                flex-direction: column;
                align-items: center;
            }}

            .btn {{
                width: 100%;
                max-width: 300px;
                text-align: center;
            }}
        }}
    </style>
</head>
<body>
    <nav class="nav">
        <div class="nav-container">
            <a href="../" class="nav-brand">{service_icon} {service_name}</a>
            <div class="nav-links">
                {nav_links}
            </div>
        </div>
    </nav>

    <div class="container">
        <div class="header">
            <div class="service-icon">{service_icon}</div>
            <h1>{page_title}</h1>
            <p>{page_description}</p>
        </div>

        <div class="last-updated">
            <strong>{last_updated_label}:</strong> {last_updated_date}
        </div>

        <div class="policy-content">
            {content}
        </div>

        <div class="actions">
            {action_buttons}
        </div>
    </div>
</body>
</html>'''

SUPPORT_TEMPLATE = '''<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Pretendard', sans-serif;
        }}

        body {{
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
        }}

        .nav {{
            background: white;
            padding: 1rem 2rem;
            border-bottom: 1px solid #e9ecef;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .nav-container {{
            max-width: 1000px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .nav-brand {{
            font-size: 1.3rem;
            font-weight: bold;
            color: {brand_color};
            text-decoration: none;
        }}

        .nav-links {{
            display: flex;
            gap: 2rem;
            align-items: center;
        }}

        .nav-link {{
            text-decoration: none;
            color: #666;
            transition: color 0.3s;
        }}

        .nav-link:hover {{
            color: {brand_color};
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem;
        }}

        .header {{
            background: white;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }}

        .header h1 {{
            color: {brand_color};
            margin-bottom: 1rem;
            font-size: 2.5rem;
        }}

        .service-icon {{
            font-size: 3rem;
            margin-bottom: 1rem;
        }}

        .support-content {{
            background: white;
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }}

        .support-content h1, .support-content h2 {{
            color: #2c3e50;
            margin-bottom: 1.5rem;
        }}

        .support-content h3 {{
            color: #2c3e50;
            margin: 1.5rem 0 1rem;
        }}

        .support-content p {{
            margin-bottom: 1rem;
            color: #666;
        }}

        .support-content ul, .support-content ol {{
            margin-left: 2rem;
            margin-bottom: 1rem;
        }}

        .support-content li {{
            margin-bottom: 0.5rem;
            color: #666;
        }}

        .support-content blockquote {{
            background-color: #e3f2fd;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid {brand_color};
            margin: 1rem 0;
        }}

        .support-content code {{
            background-color: #f8f9fa;
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        }}

        .support-content pre {{
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            overflow-x: auto;
            margin: 1rem 0;
        }}

        .faq-item {{
            border-bottom: 1px solid #e9ecef;
            padding: 1.5rem 0;
        }}

        .faq-item:last-child {{
            border-bottom: none;
        }}

        .faq-question {{
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 0.5rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .faq-answer {{
            color: #666;
            margin-top: 0.5rem;
            padding-left: 1.5rem;
        }}

        .contact-section {{
            background: linear-gradient(135deg, {brand_color} 0%, {brand_color_light} 100%);
            border-radius: 12px;
            padding: 2rem;
            text-align: center;
            color: white;
            margin-top: 2rem;
        }}

        .contact-methods {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
        }}

        .contact-method {{
            background: rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            padding: 1.5rem;
            text-decoration: none;
            color: white;
            transition: background 0.3s;
        }}

        .contact-method:hover {{
            background: rgba(255, 255, 255, 0.3);
        }}

        @media (max-width: 768px) {{
            .nav-links {{
                display: none;
            }}

            .container {{
                padding: 1rem;
            }}

            .header h1 {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <nav class="nav">
        <div class="nav-container">
            <a href="../" class="nav-brand">{service_icon} {service_name}</a>
            <div class="nav-links">
                {nav_links}
            </div>
        </div>
    </nav>

    <div class="container">
        <div class="header">
            <div class="service-icon">{service_icon}</div>
            <h1>{page_title}</h1>
            <p>{page_description}</p>
        </div>

        <div class="support-content">
            {content}
        </div>

        <div class="contact-section">
            <h2>{contact_title}</h2>
            <p>{contact_description}</p>
            
            <div class="contact-methods">
                <a href="mailto:support@ddwservices.com" class="contact-method">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">📧</div>
                    <div>{email_label}</div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">support@ddwservices.com</div>
                </a>
                <div class="contact-method">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">💬</div>
                    <div>{community_label}</div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">{coming_soon_label}</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>'''

# 서비스별 설정
SERVICE_CONFIG = {
    'travelee': {
        'icon': '✈️',
        'name': 'Travelee',
        'brand_color': '#FF6B6B',
        'brand_color_hover': '#FF5252',
        'brand_color_light': '#FFB3B3'
    },
    'gokitty': {
        'icon': '🐱',
        'name': 'Go Kitty', 
        'brand_color': '#87CEEB',
        'brand_color_hover': '#5DADE2',
        'brand_color_light': '#B8E6FF'
    }
}

# 언어별 텍스트
TEXTS = {
    'en': {
        'privacy_title': 'Privacy Policy',
        'privacy_description': 'How {service} protects your personal information',
        'support_title': 'Support Center', 
        'support_description': 'Get help with {service} - we\'re here to assist you!',
        'last_updated_label': 'Last Updated',
        'back_to_service': '← Back to {service}',
        'policy_history': 'View Policy History',
        'contact_support': 'Contact Support',
        'service_info': 'Service Info',
        'privacy_policy': 'Privacy Policy',
        'all_services': 'All Services',
        'contact_title': 'Still Need Help?',
        'contact_description': 'Can\'t find what you\'re looking for? Contact our support team!',
        'email_label': 'Email Support',
        'community_label': 'Community',
        'coming_soon_label': 'Coming Soon'
    },
    'ko': {
        'privacy_title': '개인정보처리방침',
        'privacy_description': '{service}가 개인정보를 보호하는 방법',
        'support_title': '지원 센터',
        'support_description': '{service} 도움말 - 언제든지 도와드리겠습니다!',
        'last_updated_label': '최종 수정',
        'back_to_service': '← {service}로 돌아가기',
        'policy_history': '방침 히스토리 보기',
        'contact_support': '지원 센터 문의',
        'service_info': '서비스 정보',
        'privacy_policy': '개인정보처리방침',
        'all_services': '전체 서비스',
        'contact_title': '아직도 도움이 필요하신가요?',
        'contact_description': '찾고 있는 정보를 찾을 수 없나요? 지원팀에 문의해 주세요!',
        'email_label': '이메일 지원',
        'community_label': '커뮤니티',
        'coming_soon_label': '곧 출시 예정'
    }
}

def convert_markdown_to_html(md_file, page_type, lang, service):
    """Markdown 파일을 HTML로 변환"""
    
    # 파일 존재 확인
    if not os.path.exists(md_file):
        print(f"❌ 파일을 찾을 수 없습니다: {md_file}")
        return False
    
    # 서비스 설정 확인
    if service not in SERVICE_CONFIG:
        print(f"❌ 지원되지 않는 서비스입니다: {service}")
        print(f"지원되는 서비스: {', '.join(SERVICE_CONFIG.keys())}")
        return False
    
    # Markdown 파일 읽기
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Markdown을 HTML로 변환
    md = markdown.Markdown(extensions=['tables', 'toc', 'codehilite'])
    html_content = md.convert(md_content)
    
    # 설정 가져오기
    service_config = SERVICE_CONFIG[service]
    texts = TEXTS[lang]
    
    # 템플릿 변수 설정
    template_vars = {
        'lang': lang,
        'content': html_content,
        'service_icon': service_config['icon'],
        'service_name': service_config['name'],
        'brand_color': service_config['brand_color'],
        'brand_color_hover': service_config['brand_color_hover'],
        'brand_color_light': service_config['brand_color_light'],
        'last_updated_date': datetime.now().strftime('%Y년 %m월 %d일' if lang == 'ko' else '%B %d, %Y'),
        'last_updated_label': texts['last_updated_label']
    }
    
    if page_type == 'privacy':
        template_vars.update({
            'title': f"{texts['privacy_title']} - {service_config['name']}",
            'page_title': texts['privacy_title'],
            'page_description': texts['privacy_description'].format(service=service_config['name']),
            'nav_links': f'''
                <a href="../" class="nav-link">{texts['service_info']}</a>
                <a href="../support/" class="nav-link">{texts['support_title']}</a>
                <a href="./history/" class="nav-link">{texts['policy_history']}</a>
                <a href="../../" class="nav-link">{texts['all_services']}</a>
            ''',
            'action_buttons': f'''
                <a href="../" class="btn btn-primary">{texts['back_to_service'].format(service=service_config['name'])}</a>
                <a href="./history/" class="btn btn-secondary">{texts['policy_history']}</a>
                <a href="../support/" class="btn btn-secondary">{texts['contact_support']}</a>
            '''
        })
        template = PRIVACY_TEMPLATE
        
    elif page_type == 'support':
        template_vars.update({
            'title': f"{texts['support_title']} - {service_config['name']}",
            'page_title': texts['support_title'],
            'page_description': texts['support_description'].format(service=service_config['name']),
            'nav_links': f'''
                <a href="../" class="nav-link">{texts['service_info']}</a>
                <a href="../privacy/" class="nav-link">{texts['privacy_policy']}</a>
                <a href="../../" class="nav-link">{texts['all_services']}</a>
            ''',
            'contact_title': texts['contact_title'],
            'contact_description': texts['contact_description'],
            'email_label': texts['email_label'],
            'community_label': texts['community_label'],
            'coming_soon_label': texts['coming_soon_label']
        })
        template = SUPPORT_TEMPLATE
    
    else:
        print(f"❌ 지원되지 않는 페이지 타입입니다: {page_type}")
        print("지원되는 타입: privacy, support")
        return False
    
    # HTML 생성
    html_output = template.format(**template_vars)
    
    # 출력 파일 경로 생성
    output_dir = Path(f"{lang}/{service}")
    if page_type == 'privacy':
        output_dir = output_dir / "privacy"
    elif page_type == 'support':
        output_dir = output_dir / "support"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "index.html"
    
    # HTML 파일 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_output)
    
    print(f"✅ 변환 완료: {md_file} → {output_file}")
    return True

def main():
    parser = argparse.ArgumentParser(
        description='Markdown을 HTML로 변환 (DDW Services용)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
예시:
  python scripts/md-to-html.py privacy.md --type privacy --lang ko --service gokitty
  python scripts/md-to-html.py support.md --type support --lang en --service travelee
        '''
    )
    
    parser.add_argument('markdown_file', help='변환할 Markdown 파일 경로')
    parser.add_argument('--type', choices=['privacy', 'support'], required=True,
                       help='페이지 타입 (privacy: 개인정보처리방침, support: 지원센터)')
    parser.add_argument('--lang', choices=['en', 'ko'], required=True,
                       help='언어 (en: 영어, ko: 한국어)')
    parser.add_argument('--service', choices=list(SERVICE_CONFIG.keys()), required=True,
                       help=f'서비스 이름 ({", ".join(SERVICE_CONFIG.keys())})')
    
    args = parser.parse_args()
    
    print(f"🔄 Markdown → HTML 변환 중...")
    print(f"   파일: {args.markdown_file}")
    print(f"   타입: {args.type}")
    print(f"   언어: {args.lang}")
    print(f"   서비스: {args.service}")
    print()
    
    success = convert_markdown_to_html(
        args.markdown_file,
        args.type, 
        args.lang,
        args.service
    )
    
    if success:
        print()
        print("🎉 변환이 성공적으로 완료되었습니다!")
    else:
        print()
        print("❌ 변환에 실패했습니다.")
        exit(1)

if __name__ == '__main__':
    main() 