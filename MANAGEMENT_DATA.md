# 管理台数据存储说明

## 数据结构

### 1. 项目基本信息
存储位置：`backend/data/projects.json`

```json
{
  "id": 1,
  "name": "温州中心项目",
  "code": "WZ-2026-001",
  "location": "温州市鹿城区",
  "status": "设计中",
  "stage": "方案设计",
  "progress": 45,
  "created_at": "2026-01-15",
  "updated_at": "2026-03-01"
}
```

### 2. 项目管理台数据
存储位置：`backend/data/management/project_{id}.json`

#### 2.1 存储配置
```json
{
  "storage_config": {
    "type": "local",  // local, nas, url
    "path": "/mnt/nas/projects/wenzhou",  // NAS路径
    "url": "https://files.example.com/projects/wenzhou"  // 网络地址
  }
}
```

#### 2.2 文件列表
```json
{
  "files": [
    {
      "id": 1,
      "name": "红线图",
      "type": "DWG",
      "date": "2026-02-20",
      "size": "2.4 MB",
      "path": "original/redline",  // 文件夹路径
      "storage_path": "/mnt/nas/projects/wenzhou/original/redline.dwg",  // 实际存储路径
      "uploaded_at": "2026-02-20"
    }
  ]
}
```

#### 2.3 人员列表（24人）
```json
{
  "staff": [
    {
      "id": 1,
      "name": "张三",
      "busy": 75,  // 忙碌度 0-100
      "active": true,  // 是否激活
      "schedule": "2026-03-01 至 2026-03-15: 方案设计\n2026-03-16 至 2026-03-31: 施工图绘制",  // 时间安排
      "role": "主创建筑师"  // 角色
    }
  ]
}
```

#### 2.4 经济技术指标
```json
{
  "economic_indexes": [
    {
      "id": 1,
      "name": "用地面积",
      "value": 36000,
      "unit": "㎡",
      "calculated": false  // false=可编辑, true=自动计算
    },
    {
      "id": 5,
      "name": "建筑面积",
      "value": 121400,
      "unit": "㎡",
      "calculated": true  // 自动计算：高层+低层+商业
    }
  ]
}
```

## API 接口

### 存储配置
- `GET /api/projects/{id}/storage` - 获取存储配置
- `PUT /api/projects/{id}/storage` - 更新存储配置

### 文件管理
- `GET /api/projects/{id}/files?dir=original` - 获取文件列表
- `POST /api/projects/{id}/files` - 添加文件记录
- `DELETE /api/projects/{id}/files/{file_id}` - 删除文件记录

### 人员管理
- `GET /api/projects/{id}/staff` - 获取人员列表
- `PUT /api/projects/{id}/staff` - 批量更新人员
- `PUT /api/projects/{id}/staff/{staff_id}` - 更新单个人员

### 经济指标
- `GET /api/projects/{id}/indexes` - 获取指标
- `PUT /api/projects/{id}/indexes` - 更新指标

## 前端使用

### 1. 页面加载时
```javascript
mounted() {
  this.loadProjectData()
  this.loadFiles()
  this.loadStaff()
  this.loadIndexes()
}
```

### 2. 人员编辑
- 点击人员格子：切换激活状态
- 长按人员格子：弹出编辑弹窗，可编辑：
  - 姓名
  - 忙碌度（滑块 0-100）
  - 时间安排（多行文本）
  - 角色

### 3. 存储配置
点击顶栏"存储配置"按钮，弹出配置弹窗：
- 存储类型：本地/NAS/网络地址
- NAS路径：如 `/mnt/nas/projects/wenzhou`
- 网络地址：如 `https://files.example.com/projects/wenzhou`

### 4. 文件管理
- 文件记录存储在数据库
- 实际文件存储在配置的位置（NAS或网络地址）
- 点击文件夹时，根据 `dir_path` 过滤文件列表

### 5. 经济指标
- 可编辑项：点击弹出输入框
- 计算项：自动计算，显示 * 标记
- 关联计算：
  - 建筑面积 = 高层住宅 + 低层住宅 + 商业
  - 容积率 = 建筑面积 / 用地面积

## 数据持久化

所有数据自动保存到后端：
- 人员激活状态：点击即保存
- 人员信息编辑：点击保存按钮后保存
- 经济指标：输入后自动保存并触发关联计算
- 存储配置：点击保存按钮后保存

## 文件存储方案

### 方案1：本地存储
```
type: "local"
path: "/Users/xxx/projects/wenzhou"
```

### 方案2：NAS存储
```
type: "nas"
path: "/mnt/nas/projects/wenzhou"
```

### 方案3：网络地址
```
type: "url"
url: "https://files.example.com/projects/wenzhou"
```

文件上传时，根据配置的存储类型和路径，将文件保存到对应位置，并在数据库中记录文件信息。
