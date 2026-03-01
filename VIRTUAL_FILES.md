# 虚拟文件分类说明

## 文件分类结构

我已经在后端添加了 28 个虚拟文件，展示完整的文件分类结构。

### 1. 原始资料 (original)

#### 1.1 红线图 (original/redline) - 3个文件
- 红线图 v1.dwg (2.4 MB) - 初版红线图
- 红线图 v2.dwg (2.5 MB) - 修改后的红线图
- 红线图.pdf (8.1 MB) - PDF版本

#### 1.2 测绘图 (original/survey) - 2个文件
- 地形测绘图.dwg (5.0 MB) - 1:500地形图
- 现状建筑测绘.dwg (3.0 MB) - 现状建筑平面

#### 1.3 地质报告 (original/geology) - 1个文件
- 岩土工程勘察报告.pdf (15.0 MB) - 详细勘察报告

### 2. 项目管理 (management)

#### 2.1 合同 (management/contract) - 2个文件
- 设计合同.pdf (2.0 MB) - 设计服务合同
- 补充协议.pdf (1.0 MB) - 合同补充协议

#### 2.2 会议纪要 (management/meeting) - 2个文件
- 启动会议纪要.doc (512 KB) - 项目启动会
- 方案评审会议纪要.doc (600 KB) - 方案评审会

#### 2.3 进度计划 (management/schedule) - 1个文件
- 总体进度计划.xls (400 KB) - 项目总进度

### 3. 阶段文件 (stage)

#### 3.1 方案设计 (stage/concept) - 5个文件
- 总平面图.dwg (3.2 MB) - 方案总平面
- 总平面图.pdf (12.5 MB) - PDF版总平面
- 1号楼平面图.dwg (2.5 MB) - 1号楼各层平面
- 1号楼立面图.dwg (1.8 MB) - 1号楼四个立面
- 1号楼剖面图.dwg (1.5 MB) - 1号楼剖面

#### 3.2 初步设计 (stage/preliminary) - 1个文件
- 初步设计说明.doc (1.0 MB) - 初设说明书

#### 3.3 施工图 (stage/construction) - 0个文件
- （暂无文件，等待上传）

### 4. 专项设计 (special) - 2个文件
- 结构方案.pdf (5.0 MB) - 结构专业方案
- 景观方案.pdf (10.0 MB) - 景观设计方案

### 5. 工作文件 (work) - 3个文件
- 草图方案A.skp (15.0 MB) - 初步草图
- 草图方案B.skp (16.0 MB) - 修改方案
- 分析图.skp (12.0 MB) - 场地分析模型

### 6. 效果图 (rendering) - 6个文件
- 鸟瞰图 01.jpg (5.8 MB) - 整体鸟瞰
- 鸟瞰图 02.jpg (6.2 MB) - 另一角度鸟瞰
- 沿街透视图.jpg (5.5 MB) - 沿街效果
- 入口透视图.jpg (5.0 MB) - 主入口效果
- 庭院透视图.jpg (4.5 MB) - 内庭院效果
- AI生成效果图_01.png (3.8 MB) - AI生成的效果图

## 文件分类逻辑

### 分类字段说明

每个文件包含以下字段：
```json
{
  "id": 1,
  "name": "红线图 v1",
  "type": "DWG",
  "category": "original/redline",  // 分类路径
  "path": "original/redline",      // 存储路径（与category相同）
  "size": 2457600,                 // 文件大小（字节）
  "date": "2026-02-20",            // 文件日期
  "uploaded_at": "2026-02-20",     // 上传日期
  "remark": "初版红线图"            // 备注
}
```

### 前端过滤逻辑

```javascript
computed: {
    filteredFiles() {
        let list = this.files
        // 按当前分类过滤
        if (this.currentCategory) {
            list = list.filter(f => {
                const cat = f.category || f.path || ''
                // 精确匹配或前缀匹配
                return cat === this.currentCategory ||
                       cat.startsWith(this.currentCategory + '/')
            })
        }
        return list
    }
}
```

### 分类切换示例

1. **点击"原始资料"**：
   - `currentCategory = 'original'`
   - 显示所有 `category` 以 `original` 开头的文件
   - 包括：original/redline、original/survey、original/geology
   - 共 6 个文件

2. **点击"原始资料" → "红线图"**：
   - `currentCategory = 'original/redline'`
   - 只显示 `category = 'original/redline'` 的文件
   - 共 3 个文件

3. **点击"效果图"**：
   - `currentCategory = 'rendering'`
   - 显示所有 `category = 'rendering'` 的文件
   - 共 6 个文件（包括AI生成的效果图）

## 使用方法

### 1. 查看虚拟文件

启动后端服务：
```bash
cd backend
python app.py
```

启动前端（UniApp开发工具）：
- 打开 HBuilderX
- 运行到浏览器
- 进入管理台页面

### 2. 切换文件分类

- 点击左侧文件夹导航
- 一级分类：原始资料、项目管理、阶段文件、专项设计、工作文件、效果图
- 二级分类：点击一级分类后，右侧会显示二级分类（如果有）

### 3. 上传新文件

1. 选择分类（点击左侧文件夹）
2. 点击"📤 上传"按钮
3. 填写文件信息
4. 选择文件
5. 确认上传

新上传的文件会自动归类到当前选中的分类下。

## 文件类型统计

- **DWG**: 9个（CAD图纸）
- **PDF**: 8个（文档、图纸）
- **JPG**: 5个（效果图）
- **PNG**: 1个（AI生成图）
- **SKP**: 3个（SketchUp模型）
- **DOC**: 3个（Word文档）
- **XLS**: 1个（Excel表格）

**总计**: 30个文件

## 文件大小分布

- 小文件（< 1 MB）: 3个
- 中文件（1-5 MB）: 12个
- 大文件（5-10 MB）: 8个
- 超大文件（> 10 MB）: 7个

## 注意事项

1. 这些是虚拟文件，实际文件不存在于磁盘
2. 文件大小是模拟的，用于展示
3. 上传新文件时，需要实现后端文件上传API
4. 删除文件只会删除数据库记录，不会删除实际文件
5. 下载功能需要根据存储配置实现

## 扩展分类

如果需要添加新的分类，在 `management.vue` 的 `selectPrimaryDir` 方法中添加：

```javascript
selectPrimaryDir(id) {
    this.selectedPrimaryDir = id
    this.currentCategory = id
    const secondaryMap = {
        original: [
            { id: 'redline', name: '红线图' },
            { id: 'survey', name: '测绘图' },
            { id: 'geology', name: '地质报告' }
        ],
        // 添加新的二级分类
        special: [
            { id: 'structure', name: '结构设计' },
            { id: 'mep', name: '机电设计' },
            { id: 'landscape', name: '景观设计' }
        ]
    }
    this.secondaryDirs = secondaryMap[id] || []
    this.selectedSecondaryDir = ''
}
```

然后在 `getCurrentCategoryName` 方法中添加对应的名称映射。
