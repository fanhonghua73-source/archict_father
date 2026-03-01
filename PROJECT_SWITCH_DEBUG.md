# 项目切换调试指南

## 问题描述
有时候从项目页面进入管理台，显示的不是选中的项目。

## 可能的原因

### 1. 存储时序问题
- `uni.setStorageSync` 可能在某些情况下没有立即完成
- 页面跳转太快，storage 还没写入完成

### 2. 数据加载时序问题
- `onShow` 触发时，`this.projectId` 可能还是旧值
- 异步请求使用了错误的 projectId

### 3. UniApp 返回格式不一致
- 不同版本的 UniApp，`uni.request` 返回格式可能不同
- 有的返回 `[error, response]`，有的直接返回 `response`

## 已实施的修复

### 1. 添加延迟跳转
```javascript
enterManagement(index) {
    const project = this.projects[index]
    uni.setStorageSync('selectedProject', {
        id: project.id || (index + 1),
        name: project.name
    })

    // 延迟 100ms 再跳转，确保 storage 已更新
    setTimeout(() => {
        uni.switchTab({ url: '/pages/management/management' })
    }, 100)
}
```

### 2. 添加调试日志
在以下位置添加了 console.log：
- index.vue `selectProject()` - 记录选择的项目
- index.vue `enterManagement()` - 记录进入管理台的项目和保存的数据
- management.vue `mounted()` - 记录读取到的项目
- management.vue `onShow()` - 记录读取到的项目和开始加载
- management.vue `loadStorageConfig()` - 记录请求的项目ID
- management.vue `loadStaff()` - 记录请求的项目ID和加载的数据
- management.vue `loadIndexes()` - 记录请求的项目ID

### 3. 兼容不同的 UniApp 返回格式
```javascript
async loadProjects() {
    try {
        const res = await uni.request({
            url: 'http://localhost:5002/api/projects',
            method: 'GET'
        })

        if (res.data && res.data.success) {
            this.projects = res.data.data
        } else if (res[1] && res[1].data && res[1].data.success) {
            // 兼容不同的 UniApp 返回格式
            this.projects = res[1].data.data
        }
    } catch (e) {
        this.projects = this.getMockData()
    }
}
```

## 调试步骤

### 1. 打开浏览器开发者工具
按 F12，切换到 Console 标签

### 2. 测试项目切换
1. 在项目页面点击一个项目（如"滨江住宅项目"）
2. 查看控制台输出：
   ```
   选择项目: 滨江住宅项目 ID: 1
   ```

3. 点击"进入管理台"按钮
4. 查看控制台输出：
   ```
   进入管理台 - 项目: 滨江住宅项目 ID: 1
   已保存到 storage: {id: 1, name: "滨江住宅项目"}
   ```

5. 管理台页面加载时，查看控制台输出：
   ```
   onShow - 读取到的项目: {id: 1, name: "滨江住宅项目"}
   onShow - 设置项目ID: 1 名称: 滨江住宅项目
   开始加载项目数据，项目ID: 1
   loadStorageConfig - 请求项目ID: 1
   loadStaff - 请求项目ID: 1
   loadIndexes - 请求项目ID: 1
   ```

### 3. 检查数据一致性
- 顶栏显示的项目名称应该与选中的项目一致
- 加载的人员、文件、经济指标应该属于该项目

### 4. 测试多次切换
1. 返回项目页面
2. 选择另一个项目（如"科技园办公楼"）
3. 点击"进入管理台"
4. 检查控制台日志，确认 ID 是 2
5. 检查管理台显示的是否为"科技园办公楼"的数据

## 如果问题仍然存在

### 检查点 1：Storage 是否正确保存
在浏览器开发者工具的 Application/Storage 标签中：
- 找到 Local Storage
- 查看 `selectedProject` 的值
- 确认 id 和 name 是否正确

### 检查点 2：后端数据是否存在
检查后端文件：
- `backend/data/projects.json` - 确认项目列表中有对应的 id
- `backend/data/management/project_1.json` - 确认项目 1 的数据文件存在
- `backend/data/management/project_2.json` - 确认项目 2 的数据文件存在

### 检查点 3：API 请求是否成功
在浏览器开发者工具的 Network 标签中：
- 查看 `/api/projects/{id}/staff` 请求
- 确认请求的 URL 中的 id 是否正确
- 查看响应数据是否正确

## 临时解决方案

如果问题持续，可以尝试：

### 方案 1：增加延迟时间
将 `enterManagement` 中的延迟从 100ms 增加到 300ms：
```javascript
setTimeout(() => {
    uni.switchTab({ url: '/pages/management/management' })
}, 300)
```

### 方案 2：使用 navigateTo 代替 switchTab
```javascript
uni.navigateTo({ url: '/pages/management/management' })
```
注意：这会改变导航行为，管理台将不再是 tab 页面

### 方案 3：在管理台添加刷新按钮
允许用户手动刷新数据，确保加载正确的项目

## 预期行为

正常情况下的完整流程：
1. 用户在项目页面点击项目卡片 → 卡片展开，显示详情
2. 用户点击"进入管理台"按钮 → 保存项目到 storage → 延迟 100ms → 跳转到管理台
3. 管理台 `onShow` 触发 → 读取 storage → 设置 projectId 和 projectName → 加载数据
4. 顶栏显示正确的项目名称
5. 人员、文件、经济指标显示该项目的数据

## 注意事项

- 确保后端服务正在运行（`python backend/app.py`）
- 确保后端监听在 `http://localhost:5002`
- 确保每个项目都有对应的管理台数据文件
- 如果是新项目，后端会自动创建默认数据
