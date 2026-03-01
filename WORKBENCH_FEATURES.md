# 工作台功能规划

## 已实现功能

### 1. 文档分析 (Document Analysis)
- 上传文档（PDF、Word、TXT）
- AI 分析文档结构
- 生成模板
- 基于模板生成新文档

### 2. 图片生成 (Image Generation)
- 上传基础图片 + 3张参考图
- 输入提示词
- 调用 Gemini API 生成图片
- 图片编辑工具（画笔、橡皮擦、填充）
- 保存生成的图片
- **新增**：可以将生成的图片导入到管理台的"效果图"分类

## 待实现功能

### 3. PPT 生成 (PPT Generation)
**功能描述**：
- 输入项目信息（项目名称、地点、面积等）
- 选择 PPT 模板（方案汇报、设计说明、进度汇报）
- 从管理台选择图片（效果图、平面图等）
- AI 生成 PPT 内容大纲
- 自动排版生成 PPT 文件

**技术方案**：
- 前端：上传区 + 模板选择 + 图片选择器 + 预览区
- 后端：使用 python-pptx 库生成 PPT
- API：`POST /api/ppt/generate`

**数据结构**：
```json
{
  "project_id": 1,
  "template": "design_presentation",
  "title": "温州中心项目方案汇报",
  "content": {
    "project_info": {...},
    "images": [
      {"type": "rendering", "file_id": 1},
      {"type": "plan", "file_id": 2}
    ]
  }
}
```

### 4. 图片搜索 (Image Search)
**功能描述**：
- 上传一张参考图片
- 在项目文件库中搜索相似图片
- 支持按类型筛选（效果图、平面图、立面图）
- 显示相似度评分

**技术方案**：
- 前端：上传区 + 搜索结果网格
- 后端：使用 CLIP 或其他图像嵌入模型
- API：`POST /api/images/search`

**数据结构**：
```json
{
  "query_image": "base64...",
  "project_id": 1,
  "file_types": ["JPG", "PNG"],
  "categories": ["rendering", "plan"],
  "limit": 20
}
```

**响应**：
```json
{
  "results": [
    {
      "file_id": 1,
      "name": "效果图 01",
      "similarity": 0.92,
      "thumbnail": "base64..."
    }
  ]
}
```

### 5. 尺寸计算 (Size Calculation)
**功能描述**：
- 输入用地面积、容积率等基础参数
- 选择建筑类型（住宅、商业、办公）
- AI 计算建议的各项指标
- 生成面积分配方案
- 可以直接导入到管理台的"经济技术指标"

**技术方案**：
- 前端：表单输入 + 计算结果展示 + 图表可视化
- 后端：建筑规范计算逻辑
- API：`POST /api/calculation/size`

**数据结构**：
```json
{
  "land_area": 36000,
  "far": 2.4,
  "building_type": "residential",
  "constraints": {
    "max_height": 100,
    "green_ratio": 0.3
  }
}
```

**响应**：
```json
{
  "total_area": 86400,
  "breakdown": {
    "residential": 70000,
    "commercial": 10000,
    "parking": 6400
  },
  "recommendations": [
    "建议高层住宅面积 70000㎡",
    "地下停车位约 200 个"
  ]
}
```

### 6. 造价估算 (Cost Estimation)
**功能描述**：
- 输入建筑面积、类型、地区
- 选择装修标准（毛坯、精装、豪装）
- AI 估算总造价和单方造价
- 分项造价明细（结构、装修、机电等）
- 生成造价报告

**技术方案**：
- 前端：表单输入 + 造价明细表 + 图表
- 后端：造价数据库 + 计算逻辑
- API：`POST /api/calculation/cost`

**数据结构**：
```json
{
  "project_id": 1,
  "area": 121400,
  "building_type": "residential",
  "location": "温州市",
  "standard": "fine_decoration"
}
```

**响应**：
```json
{
  "total_cost": 486000000,
  "unit_cost": 4000,
  "breakdown": {
    "structure": 180000000,
    "decoration": 150000000,
    "mep": 100000000,
    "other": 56000000
  },
  "currency": "CNY"
}
```

## 工具间的数据流

### 图片生成 → 管理台
```
用户在图片生成工具中生成图片
  ↓
点击"保存到项目"按钮
  ↓
选择保存到哪个分类（效果图/平面图/立面图）
  ↓
调用 POST /api/projects/{id}/files
  ↓
文件保存到管理台对应分类
```

### 尺寸计算 → 管理台
```
用户在尺寸计算工具中完成计算
  ↓
点击"导入到管理台"按钮
  ↓
调用 PUT /api/projects/{id}/indexes
  ↓
经济技术指标自动更新
```

### 管理台 → PPT 生成
```
用户在 PPT 生成工具中选择图片
  ↓
调用 GET /api/projects/{id}/files?category=rendering
  ↓
显示项目中的效果图列表
  ↓
用户选择图片，生成 PPT
```

## UI 设计原则

### 统一风格
- 所有工具页面使用相同的布局结构
- 顶栏：用户头像 + 工具名称 + 窗口控制
- 左侧：导航栏（80px）
- 主区域：工具内容
- 底部：搜索框（可选）

### 交互模式
- 上传区：拖拽上传 + 点击上传
- 结果展示：卡片式 + 列表式
- 操作按钮：主按钮（绿色）+ 次按钮（灰色）
- 加载状态：显示进度条或加载动画

### 响应式
- 适配不同屏幕尺寸
- 移动端优化（如果需要）

## 开发优先级

1. **高优先级**：
   - 管理台文件上传系统
   - 图片生成 → 管理台的导入功能
   - 尺寸计算工具

2. **中优先级**：
   - PPT 生成工具
   - 造价估算工具

3. **低优先级**：
   - 图片搜索工具（需要 AI 模型）

## 技术栈

### 前端
- UniApp (Vue 2)
- uni-file-picker（文件上传组件）
- echarts-for-weixin（图表可视化）

### 后端
- Flask (Python)
- python-pptx（PPT 生成）
- Pillow（图像处理）
- OpenAI/Claude API（AI 功能）

### 存储
- 本地文件系统 / NAS
- JSON 文件（元数据）
- 对象存储（可选，用于大文件）
