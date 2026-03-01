# 数据闭环说明

## 项目选择流程

### 1. 项目页面 (index.vue)
用户在项目页面选择项目时：

```javascript
selectProject(index) {
    this.selectedIndex = this.selectedIndex === index ? -1 : index
    if (this.selectedIndex !== -1) {
        const project = this.projects[index]
        // 保存到本地存储
        uni.setStorageSync('selectedProject', {
            id: project.id || (index + 1),
            name: project.name
        })
    }
}
```

点击"进入管理台"按钮：
```javascript
enterManagement(index) {
    const project = this.projects[index]
    uni.setStorageSync('selectedProject', {
        id: project.id || (index + 1),
        name: project.name
    })
    uni.switchTab({ url: '/pages/management/management' })
}
```

### 2. 管理台页面 (management.vue)
管理台页面在显示时自动读取选中的项目：

```javascript
onShow() {
    // 每次显示页面时重新读取项目并加载数据
    const selected = uni.getStorageSync('selectedProject')
    if (selected && selected.id) {
        this.projectId = selected.id
        this.projectName = selected.name
    }
    this.loadStorageConfig()
    this.loadStaff()
    this.loadIndexes()
}
```

## 数据存储结构

### 本地存储 (uni.setStorageSync)
```javascript
{
    selectedProject: {
        id: 1,              // 项目ID
        name: '温州中心项目'  // 项目名称
    }
}
```

### 后端存储

#### 项目列表
`backend/data/projects.json`
```json
[
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
]
```

#### 项目管理台数据
`backend/data/management/project_{id}.json`
```json
{
    "project_id": 1,
    "storage_config": {
        "type": "local",
        "path": "/Users/xxx/projects/wenzhou",
        "url": ""
    },
    "files": [
        {
            "id": 1,
            "name": "红线图",
            "type": "DWG",
            "date": "2026-02-20",
            "size": "2.4 MB",
            "path": "original/redline",
            "storage_path": "/mnt/nas/projects/wenzhou/original/redline.dwg",
            "uploaded_at": "2026-02-20"
        }
    ],
    "staff": [
        {
            "id": 1,
            "name": "张三",
            "busy": 75,
            "active": true,
            "schedule": "2026-03-01 至 2026-03-15: 方案设计",
            "role": "主创建筑师"
        }
    ],
    "economic_indexes": [
        {
            "id": 1,
            "name": "用地面积",
            "value": 36000,
            "unit": "㎡",
            "calculated": false
        }
    ]
}
```

## API 接口

### 项目接口
- `GET /api/projects` - 获取所有项目
- `GET /api/projects/{id}` - 获取单个项目
- `POST /api/projects` - 创建项目

### 管理台接口
- `GET /api/projects/{id}/storage` - 获取存储配置
- `PUT /api/projects/{id}/storage` - 更新存储配置
- `GET /api/projects/{id}/files?dir=original` - 获取文件列表
- `POST /api/projects/{id}/files` - 添加文件
- `DELETE /api/projects/{id}/files/{file_id}` - 删除文件
- `GET /api/projects/{id}/staff` - 获取人员列表
- `PUT /api/projects/{id}/staff` - 批量更新人员
- `PUT /api/projects/{id}/staff/{staff_id}` - 更新单个人员
- `GET /api/projects/{id}/indexes` - 获取经济指标
- `PUT /api/projects/{id}/indexes` - 更新经济指标

## 数据流向

```
用户操作 → 前端页面 → 本地存储 → 后端API → JSON文件
   ↑                                              ↓
   └──────────────── 数据回显 ←──────────────────┘
```

### 完整流程示例

1. **用户在项目页面选择项目**
   - 点击项目卡片 → `selectProject(index)` → `uni.setStorageSync('selectedProject', {...})`

2. **用户点击"进入管理台"**
   - `enterManagement(index)` → `uni.switchTab('/pages/management/management')`

3. **管理台页面加载**
   - `onShow()` → `uni.getStorageSync('selectedProject')` → 设置 `projectId` 和 `projectName`
   - 调用 `loadStorageConfig()`, `loadStaff()`, `loadIndexes()`

4. **加载数据**
   - `GET /api/projects/{projectId}/staff` → 后端读取 `project_{id}.json` → 返回人员列表
   - 前端更新 `staffList`

5. **用户编辑人员**
   - 点击编辑按钮 → 打开弹窗 → 修改数据 → 点击保存
   - `saveStaff()` → `PUT /api/projects/{projectId}/staff` → 后端保存到 `project_{id}.json`

6. **数据持久化**
   - 所有修改自动保存到后端
   - 下次打开管理台时，从后端重新加载最新数据

## 关键特性

### 1. 项目切换
- 在项目页面选择不同项目，管理台会自动切换到对应项目
- 使用 `uni.setStorageSync` 和 `uni.getStorageSync` 实现跨页面状态共享

### 2. 数据同步
- 所有数据修改立即保存到后端
- 页面切换时自动重新加载最新数据

### 3. 离线支持
- 本地存储保存选中的项目
- 即使刷新页面，也能记住用户的选择

### 4. 数据隔离
- 每个项目的数据独立存储在 `project_{id}.json`
- 不同项目之间数据互不干扰
