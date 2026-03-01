#!/usr/bin/env python3
"""
建筑学爸 AI 助手 - Flask API 后端
提供文档分析、图像生成、项目管理等接口
"""

import os
import json
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from pathlib import Path
import base64
from io import BytesIO

app = Flask(__name__)
CORS(app)

# 配置
BASE_DIR = Path(__file__).parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
TEMPLATE_FOLDER = BASE_DIR / "templates"
UPLOAD_FOLDER.mkdir(exist_ok=True)
TEMPLATE_FOLDER.mkdir(exist_ok=True)

# 导入功能模块
from api.document_analyzer import DocumentAnalyzer
from api.image_generator import ImageGenerator
from api.project_manager import ProjectManager

# 初始化模块
doc_analyzer = DocumentAnalyzer()
img_generator = ImageGenerator()
project_mgr = ProjectManager()

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'service': '建筑学爸 AI 助手',
        'version': '1.0.0'
    })

@app.route('/api/test-connection', methods=['POST'])
def test_connection():
    """测试 API 连接"""
    try:
        data = request.json
        provider = data.get('provider', '')
        api_key = data.get('apiKey', '')
        base_url = data.get('baseUrl', '')
        model = data.get('model', '')

        # 根据不同的提供商测试连接
        if provider == 'openai':
            import openai
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=model or 'gpt-3.5-turbo',
                messages=[{'role': 'user', 'content': 'test'}],
                max_tokens=5
            )
            return jsonify({'success': True, 'message': '连接成功'})

        elif provider == 'claude':
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            response = client.messages.create(
                model=model or 'claude-3-sonnet-20240229',
                max_tokens=5,
                messages=[{'role': 'user', 'content': 'test'}]
            )
            return jsonify({'success': True, 'message': '连接成功'})

        elif provider == 'gemini':
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model_obj = genai.GenerativeModel(model or 'gemini-pro')
            response = model_obj.generate_content('test')
            return jsonify({'success': True, 'message': '连接成功'})

        elif provider == 'ollama':
            import requests
            url = base_url or 'http://localhost:11434'
            response = requests.post(
                f'{url}/api/generate',
                json={'model': model or 'llama3', 'prompt': 'test', 'stream': False}
            )
            if response.status_code == 200:
                return jsonify({'success': True, 'message': '连接成功'})
            else:
                return jsonify({'success': False, 'error': '连接失败'})

        elif provider in ['deepseek', 'moonshot', 'zhipu']:
            # 这些提供商使用 OpenAI 兼容接口
            import openai
            base_urls = {
                'deepseek': 'https://api.deepseek.com/v1',
                'moonshot': 'https://api.moonshot.cn/v1',
                'zhipu': 'https://open.bigmodel.cn/api/paas/v4'
            }
            default_models = {
                'deepseek': 'deepseek-chat',
                'moonshot': 'moonshot-v1-8k-vision-preview',
                'zhipu': 'glm-4'
            }
            client = openai.OpenAI(
                api_key=api_key,
                base_url=base_urls.get(provider, '')
            )
            response = client.chat.completions.create(
                model=model or default_models.get(provider, 'deepseek-chat'),
                messages=[{'role': 'user', 'content': 'test'}],
                max_tokens=5
            )
            return jsonify({'success': True, 'message': '连接成功'})

        else:
            return jsonify({'success': False, 'error': '不支持的提供商'})

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== 文档分析接口 ====================

@app.route('/api/document/analyze', methods=['POST'])
def analyze_document():
    """
    分析文档结构，生成模板
    """
    try:
        data = request.json
        text = data.get('text', '')
        api_type = data.get('api_type', 'openai')  # openai, claude, gemini

        result = doc_analyzer.analyze(text, api_type)

        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/document/generate', methods=['POST'])
def generate_document():
    """
    基于模板和新内容生成文档
    """
    try:
        data = request.json
        template = data.get('template', {})
        new_content = data.get('new_content', '')
        api_type = data.get('api_type', 'openai')

        result = doc_analyzer.generate(template, new_content, api_type)

        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== 图像生成接口 ====================

@app.route('/api/image/generate', methods=['POST'])
def generate_image():
    """
    生成图像（Gemini API）
    """
    try:
        data = request.json
        prompt = data.get('prompt', '')
        base_image = data.get('base_image', '')  # base64
        reference_images = data.get('reference_images', [])  # list of base64

        result = img_generator.generate(prompt, base_image, reference_images)

        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== 项目管理接口 ====================

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """获取所有项目"""
    try:
        projects = project_mgr.get_all()
        return jsonify({
            'success': True,
            'count': len(projects),
            'data': projects
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """获取单个项目详情"""
    try:
        project = project_mgr.get_by_id(project_id)
        if project:
            return jsonify({
                'success': True,
                'data': project
            })
        else:
            return jsonify({
                'success': False,
                'error': '项目不存在'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/projects', methods=['POST'])
def create_project():
    """创建新项目"""
    try:
        data = request.json
        project = project_mgr.create(data)
        return jsonify({'success': True, 'data': project})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== 管理台接口 ====================

@app.route('/api/projects/<int:project_id>/storage', methods=['GET'])
def get_storage_config(project_id):
    """获取文件存储配置"""
    try:
        config = project_mgr.get_storage_config(project_id)
        return jsonify({'success': True, 'data': config})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects/<int:project_id>/storage', methods=['PUT'])
def update_storage_config(project_id):
    """更新文件存储配置（NAS路径或网络地址）"""
    try:
        config = request.json
        result = project_mgr.update_storage_config(project_id, config)
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects/<int:project_id>/files', methods=['GET'])
def get_project_files(project_id):
    """获取项目文件列表"""
    try:
        dir_path = request.args.get('dir', '')
        files = project_mgr.get_files(project_id, dir_path)
        return jsonify({'success': True, 'data': files})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects/<int:project_id>/files', methods=['POST'])
def add_project_file(project_id):
    """添加项目文件记录"""
    try:
        file_data = request.json
        result = project_mgr.add_file(project_id, file_data)
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects/<int:project_id>/files/<int:file_id>', methods=['DELETE'])
def delete_project_file(project_id, file_id):
    """删除项目文件记录"""
    try:
        project_mgr.delete_file(project_id, file_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects/<int:project_id>/staff', methods=['GET'])
def get_staff(project_id):
    """获取项目人员列表"""
    try:
        staff = project_mgr.get_staff(project_id)
        return jsonify({'success': True, 'data': staff})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects/<int:project_id>/staff', methods=['PUT'])
def update_staff(project_id):
    """批量更新人员列表"""
    try:
        staff_list = request.json
        result = project_mgr.update_staff(project_id, staff_list)
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects/<int:project_id>/staff/<int:staff_id>', methods=['PUT'])
def update_staff_member(project_id, staff_id):
    """更新单个人员信息（姓名、忙碌度、时间安排）"""
    try:
        updates = request.json
        result = project_mgr.update_staff_member(project_id, staff_id, updates)
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects/<int:project_id>/indexes', methods=['GET'])
def get_indexes(project_id):
    """获取经济技术指标"""
    try:
        indexes = project_mgr.get_indexes(project_id)
        return jsonify({'success': True, 'data': indexes})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects/<int:project_id>/indexes', methods=['PUT'])
def update_indexes(project_id):
    """更新经济技术指标"""
    try:
        indexes = request.json
        result = project_mgr.update_indexes(project_id, indexes)
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
