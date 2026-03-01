"""
文档分析模块
支持多种 LLM API 接入，分析文档结构并生成模板
"""

import os
import json
import requests
from typing import Dict, List, Any

class DocumentAnalyzer:
    def __init__(self):
        self.api_configs = {
            'openai': {
                'url': 'https://api.openai.com/v1/chat/completions',
                'key_env': 'OPENAI_API_KEY',
                'model': 'gpt-4'
            },
            'claude': {
                'url': 'https://api.anthropic.com/v1/messages',
                'key_env': 'ANTHROPIC_API_KEY',
                'model': 'claude-3-sonnet-20240229'
            },
            'gemini': {
                'url': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',
                'key_env': 'GEMINI_API_KEY',
                'model': 'gemini-pro'
            }
        }

    def analyze(self, text: str, api_type: str = 'openai') -> Dict[str, Any]:
        """
        分析文档结构，提取关键信息并生成模板
        """
        prompt = f"""请分析以下文档的结构，提取关键信息并生成一个可复用的模板。

文档内容：
{text}

请按以下格式返回JSON：
{{
    "structure": {{
        "sections": ["章节1", "章节2", ...],
        "key_fields": ["字段1", "字段2", ...]
    }},
    "template": {{
        "title": "模板标题",
        "sections": [
            {{
                "name": "章节名称",
                "content": "章节内容模板",
                "variables": ["变量1", "变量2"]
            }}
        ]
    }},
    "summary": "文档摘要"
}}
"""

        response = self._call_api(prompt, api_type)

        try:
            result = json.loads(response)
            return result
        except:
            return {
                'structure': {'sections': [], 'key_fields': []},
                'template': {'title': '', 'sections': []},
                'summary': response
            }

    def generate(self, template: Dict, new_content: str, api_type: str = 'openai') -> Dict[str, Any]:
        """
        基于模板和新内容生成新文档
        """
        prompt = f"""请基于以下模板和新内容，生成一份新文档。

模板：
{json.dumps(template, ensure_ascii=False, indent=2)}

新内容：
{new_content}

请将新内容填充到模板中，生成完整的文档。
"""

        response = self._call_api(prompt, api_type)

        return {
            'generated_text': response,
            'template_used': template
        }

    def _call_api(self, prompt: str, api_type: str) -> str:
        """
        调用指定的 LLM API
        """
        config = self.api_configs.get(api_type)
        if not config:
            raise ValueError(f"不支持的 API 类型: {api_type}")

        api_key = os.getenv(config['key_env'])
        if not api_key:
            raise ValueError(f"未设置 API Key: {config['key_env']}")

        if api_type == 'openai':
            return self._call_openai(prompt, config, api_key)
        elif api_type == 'claude':
            return self._call_claude(prompt, config, api_key)
        elif api_type == 'gemini':
            return self._call_gemini(prompt, config, api_key)

    def _call_openai(self, prompt: str, config: Dict, api_key: str) -> str:
        """调用 OpenAI API"""
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        data = {
            'model': config['model'],
            'messages': [
                {'role': 'user', 'content': prompt}
            ]
        }

        response = requests.post(config['url'], headers=headers, json=data)
        response.raise_for_status()

        return response.json()['choices'][0]['message']['content']

    def _call_claude(self, prompt: str, config: Dict, api_key: str) -> str:
        """调用 Claude API"""
        headers = {
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01',
            'Content-Type': 'application/json'
        }

        data = {
            'model': config['model'],
            'max_tokens': 4096,
            'messages': [
                {'role': 'user', 'content': prompt}
            ]
        }

        response = requests.post(config['url'], headers=headers, json=data)
        response.raise_for_status()

        return response.json()['content'][0]['text']

    def _call_gemini(self, prompt: str, config: Dict, api_key: str) -> str:
        """调用 Gemini API"""
        url = f"{config['url']}?key={api_key}"

        data = {
            'contents': [
                {
                    'parts': [
                        {'text': prompt}
                    ]
                }
            ]
        }

        response = requests.post(url, json=data)
        response.raise_for_status()

        return response.json()['candidates'][0]['content']['parts'][0]['text']
