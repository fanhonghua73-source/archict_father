"""
图像生成模块
使用 Gemini API 生成图像
"""

import os
import base64
import requests
from typing import List, Dict, Any

class ImageGenerator:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY', '')
        self.model = 'gemini-2.0-flash-exp'
        self.base_url = 'https://generativelanguage.googleapis.com/v1beta/models'

    def generate(self, prompt: str, base_image: str = '', reference_images: List[str] = []) -> Dict[str, Any]:
        """
        生成图像

        Args:
            prompt: 文本提示
            base_image: 底图 (base64)
            reference_images: 参考图列表 (base64)

        Returns:
            生成的图像数据
        """
        if not self.api_key:
            raise ValueError("未设置 GEMINI_API_KEY")

        # 构建请求内容
        contents = []
        parts = []

        # 添加底图
        if base_image:
            parts.append({
                'inline_data': {
                    'mime_type': 'image/jpeg',
                    'data': base_image
                }
            })

        # 添加参考图
        for ref_img in reference_images:
            if ref_img:
                parts.append({
                    'inline_data': {
                        'mime_type': 'image/jpeg',
                        'data': ref_img
                    }
                })

        # 添加提示词
        parts.append({'text': prompt})

        contents.append({'parts': parts})

        # 调用 API
        url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"

        data = {
            'contents': contents,
            'generationConfig': {
                'temperature': 0.7,
                'topK': 40,
                'topP': 0.95,
                'maxOutputTokens': 2048
            }
        }

        response = requests.post(url, json=data)
        response.raise_for_status()

        result = response.json()

        # 提取生成的内容
        if 'candidates' in result and len(result['candidates']) > 0:
            candidate = result['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                parts = candidate['content']['parts']

                # 查找图像数据
                for part in parts:
                    if 'inline_data' in part:
                        return {
                            'image': part['inline_data']['data'],
                            'mime_type': part['inline_data']['mime_type']
                        }
                    elif 'text' in part:
                        return {
                            'text': part['text']
                        }

        return {
            'error': '未能生成图像',
            'raw_response': result
        }

    def edit_image(self, base_image: str, mask: str, prompt: str) -> Dict[str, Any]:
        """
        编辑图像（局部修改）

        Args:
            base_image: 原图 (base64)
            mask: 遮罩 (base64)
            prompt: 编辑提示
        """
        if not self.api_key:
            raise ValueError("未设置 GEMINI_API_KEY")

        url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"

        contents = [{
            'parts': [
                {
                    'inline_data': {
                        'mime_type': 'image/jpeg',
                        'data': base_image
                    }
                },
                {
                    'inline_data': {
                        'mime_type': 'image/jpeg',
                        'data': mask
                    }
                },
                {'text': f"请根据遮罩区域编辑图像：{prompt}"}
            ]
        }]

        data = {
            'contents': contents,
            'generationConfig': {
                'temperature': 0.7,
                'maxOutputTokens': 2048
            }
        }

        response = requests.post(url, json=data)
        response.raise_for_status()

        result = response.json()

        if 'candidates' in result and len(result['candidates']) > 0:
            candidate = result['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                parts = candidate['content']['parts']
                for part in parts:
                    if 'inline_data' in part:
                        return {
                            'image': part['inline_data']['data'],
                            'mime_type': part['inline_data']['mime_type']
                        }

        return {
            'error': '未能编辑图像',
            'raw_response': result
        }
