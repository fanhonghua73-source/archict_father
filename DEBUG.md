# 设置页面调试指南

## 问题排查步骤

### 1. 检查控制台输出
在浏览器中打开开发者工具（F12），查看 Console 标签页，点击设置项时应该看到：
```
点击了设置项: 文档分析 API {label: "DeepSeek", value: "未配置", ...}
打开文档分析 API 配置
openApiModal 被调用: DeepSeek deepseek
showApiModal 设置为 true
```

### 2. 检查弹窗是否显示
- 打开浏览器开发者工具的 Elements 标签
- 点击任意 API 配置项
- 在 DOM 树中搜索 `modal-overlay`
- 检查该元素是否存在，以及 `v-if="showApiModal"` 是否为 true

### 3. 检查 CSS 层级
在开发者工具中检查 `.modal-overlay` 的样式：
- `z-index` 应该是 9999
- `position` 应该是 fixed
- `display` 应该是 flex

### 4. 检查输入框
如果弹窗显示但输入框无法点击：
- 检查 `.form-input` 的 `z-index` 是否为 10
- 检查是否有其他元素覆盖在输入框上方
- 尝试在输入框上右键 -> 检查元素，查看实际的层级关系

### 5. 常见问题

#### 问题1：点击设置项没有反应
- 检查 `handleSettingClick` 方法是否被调用（看控制台）
- 检查 `item.clickable` 是否为 true
- 检查 `sectionTitle` 是否匹配

#### 问题2：弹窗不显示
- 检查 `showApiModal` 或 `showImageModal` 是否变为 true
- 检查 `v-if` 条件是否正确
- 检查是否有 CSS 将弹窗隐藏了

#### 问题3：弹窗显示但被遮挡
- 检查 `.modal-overlay` 的 z-index 是否足够高（应该是 9999）
- 检查父元素是否有 `overflow: hidden`
- 检查弹窗是否在正确的 DOM 位置（应该在 `.page-container` 下，而不是 `.workspace-card` 内）

#### 问题4：输入框无法点击
- 检查 `.form-input` 的 z-index
- 检查是否有透明遮罩覆盖
- 尝试移除 `.modal-mask` 看是否能点击

## 临时测试方法

在 `<script>` 的 `mounted()` 中添加：
```javascript
mounted() {
    this.updateApiStatus()

    // 测试：3秒后自动打开弹窗
    setTimeout(() => {
        console.log('自动打开测试弹窗')
        this.showApiModal = true
    }, 3000)
}
```

这样可以验证弹窗本身是否能正常显示。
