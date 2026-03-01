#!/usr/bin/env python3
"""
测试新增项目 API
"""

import requests
import json

# 测试数据
test_project = {
    "name": "测试项目",
    "location": "杭州市西湖区",
    "stage": "方案设计",
    "area_total": 45000,
    "status": "设计中",
    "progress": 0
}

print("=" * 60)
print("测试新增项目 API")
print("=" * 60)

# 1. 测试健康检查
print("\n1. 测试健康检查...")
try:
    response = requests.get("http://localhost:5002/api/health")
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
except Exception as e:
    print(f"   ❌ 错误: {e}")
    print("   请确保后端服务正在运行: cd backend && python app.py")
    exit(1)

# 2. 获取现有项目列表
print("\n2. 获取现有项目列表...")
try:
    response = requests.get("http://localhost:5002/api/projects")
    data = response.json()
    print(f"   状态码: {response.status_code}")
    print(f"   项目数量: {data.get('count', 0)}")
    print(f"   项目列表: {json.dumps(data.get('data', []), ensure_ascii=False, indent=2)}")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 3. 创建新项目
print("\n3. 创建新项目...")
print(f"   请求数据: {json.dumps(test_project, ensure_ascii=False, indent=2)}")
try:
    response = requests.post(
        "http://localhost:5002/api/projects",
        json=test_project,
        headers={'Content-Type': 'application/json'}
    )
    print(f"   状态码: {response.status_code}")
    data = response.json()
    print(f"   响应: {json.dumps(data, ensure_ascii=False, indent=2)}")

    if data.get('success'):
        print(f"   ✅ 创建成功！项目 ID: {data['data']['id']}")
    else:
        print(f"   ❌ 创建失败: {data.get('error')}")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 4. 再次获取项目列表验证
print("\n4. 验证项目是否已创建...")
try:
    response = requests.get("http://localhost:5002/api/projects")
    data = response.json()
    print(f"   项目数量: {data.get('count', 0)}")
    print(f"   最新项目: {json.dumps(data.get('data', [])[-1], ensure_ascii=False, indent=2)}")
except Exception as e:
    print(f"   ❌ 错误: {e}")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
