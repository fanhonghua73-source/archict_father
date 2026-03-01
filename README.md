# 建筑学爸 App

基于 Python + UniApp 的 AI 助手应用

## 项目结构

```
建筑学爸app/
├── backend/              # Python Flask 后端
│   ├── app.py           # 主应用入口
│   ├── api/             # API 模块
│   │   ├── document_analyzer.py   # 文档分析
│   │   ├── image_generator.py     # 图像生成
│   │   └── project_manager.py     # 项目管理
│   └── requirements.txt # Python 依赖
│
└── uniapp-frontend/     # UniApp 前端
    ├── pages/           # 页面
    │   ├── index/       # 项目页面
    │   ├── resource/    # 资源页面
    │   ├── workbench/   # 工作台
    │   ├── entertainment/ # 娱乐室
    │   ├── management/  # 管理台
    │   ├── settings/    # 设置页面
    │   ├── image-gen/   # 图像生成
    │   └── doc-analysis/ # 文档分析
    ├── static/          # 静态资源
    ├── pages.json       # 页面配置
    └── manifest.json    # 应用配置
```

## 启动方式

### 1. 启动后端

```bash
cd backend
pip install -r requirements.txt
python app.py
```

后端将运行在 http://localhost:5002

### 2. 启动前端

使用 HBuilderX 打开 `uniapp-frontend` 目录，然后：
- 点击"运行" -> "运行到浏览器" -> "Chrome"
- 或者运行到手机/模拟器

## 功能说明

### 文档分析
- 支持多个 LLM API（DeepSeek、OpenAI、Claude、Gemini、Moonshot、Zhipu、Ollama）
- 分析文档结构，生成模板
- 基于模板生成新文档

### 图像生成
- 支持 Gemini 官方 API
- 支持野路子（第三方代理）
- 主图 + 最多 3 张参考图
- 自定义提示词生成

### API 配置
在设置页面配置各个 API 的密钥和参数：
- 文档分析 API：7 个提供商可选
- 图像生成 API：官方/野路子两种模式

## 技术栈

- 后端：Python 3.x + Flask
- 前端：UniApp (Vue 2)
- API：OpenAI、Claude、Gemini 等多个 LLM 服务
