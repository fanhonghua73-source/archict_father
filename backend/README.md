# 建筑学爸 AI 助手 - 后端服务

## 功能模块

### 1. 文档分析 (Document Analyzer)
- 支持多种 LLM API (OpenAI, Claude, Gemini)
- 文档结构分析
- 模板生成
- 基于模板生成新文档

### 2. 图像生成 (Image Generator)
- 使用 Gemini API 生成图像
- 支持底图 + 参考图
- 图像编辑功能

### 3. 项目管理 (Project Manager)
- 项目 CRUD 操作
- 项目数据持久化

## 安装

```bash
cd backend
pip install -r requirements.txt
```

## 配置

创建 `.env` 文件：

```env
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_claude_key
GEMINI_API_KEY=your_gemini_key
```

## 运行

```bash
python app.py
```

服务将在 `http://localhost:5000` 启动

## API 接口

### 健康检查
```
GET /api/health
```

### 文档分析
```
POST /api/document/analyze
{
  "text": "文档内容",
  "api_type": "openai"  // openai, claude, gemini
}
```

### 文档生成
```
POST /api/document/generate
{
  "template": {...},
  "new_content": "新内容",
  "api_type": "openai"
}
```

### 图像生成
```
POST /api/image/generate
{
  "prompt": "生成提示",
  "base_image": "base64编码",
  "reference_images": ["base64编码1", "base64编码2"]
}
```

### 项目管理
```
GET /api/projects              // 获取所有项目
GET /api/projects/:id          // 获取单个项目
POST /api/projects             // 创建项目
PUT /api/projects/:id          // 更新项目
DELETE /api/projects/:id       // 删除项目
```
