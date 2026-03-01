# 下拉选择器调试指南

## 当前实现

### 文档分析 API - 模型选择
现在提供两种方式：
1. **下拉选择器**：从预设模型中选择
2. **手动输入框**：可以手动输入自定义模型名称

### 图像生成 API
1. **官方模型选择器**：3个预设模型
2. **图片比例选择器**：5个比例选项

## 测试步骤

### 1. 打开开发者工具
按 F12，切换到 Console 标签

### 2. 测试文档分析 API 模型选择
1. 点击任意文档分析 API 配置项（如 DeepSeek）
2. 查看控制台输出：
   ```
   当前提供商: deepseek 模型选项: ["deepseek-chat", "deepseek-coder"]
   ```
3. 点击"模型"下拉框
4. 选择一个模型
5. 查看控制台输出：
   ```
   模型选择改变: 1
   选中的模型: deepseek-coder
   ```
6. 或者在下方的输入框中手动输入模型名称

### 3. 测试图像生成 API
1. 点击"Gemini 官方"配置项
2. 点击"模型"下拉框
3. 选择一个模型
4. 查看控制台输出：
   ```
   官方模型选择改变: 1
   选中的官方模型: gemini-2.5-flash-image
   ```

### 4. 测试图片比例选择
1. 点击"Gemini 野路子"配置项
2. 点击"图片比例"下拉框
3. 选择一个比例
4. 查看控制台输出：
   ```
   图片比例选择改变: 2
   选中的比例: 9:16
   ```

## 可能的问题

### 问题1：点击下拉框没有反应
**原因**：picker 组件可能被遮罩层阻挡

**解决方案**：
- 已添加 `.picker-arrow` 视觉指示器（▼）
- 已为文档分析 API 添加了备用输入框
- 检查 CSS 的 z-index 设置

### 问题2：选择后没有更新
**原因**：事件没有正确触发或数据没有绑定

**检查**：
- 查看控制台是否有 "模型选择改变" 的日志
- 如果有日志但界面没更新，可能是视图更新问题
- 已添加 `$forceUpdate()` 强制更新

### 问题3：下拉选项为空
**原因**：`getModelOptions()` 返回空数组

**检查**：
- 查看控制台 "当前提供商" 和 "模型选项" 的日志
- 确认 `currentProvider` 的值是否正确（应该是小写）

## 当前配置

### 文档分析 API 模型选项
```javascript
modelOptions: {
    deepseek: ['deepseek-chat', 'deepseek-coder'],
    openai: ['gpt-4o', 'gpt-4-turbo', 'gpt-3.5-turbo'],
    claude: ['claude-3-5-sonnet-20241022', 'claude-3-sonnet-20240229', 'claude-3-opus-20240229'],
    gemini: ['gemini-pro', 'gemini-1.5-pro', 'gemini-1.5-flash'],
    moonshot: ['moonshot-v1-8k', 'moonshot-v1-32k', 'moonshot-v1-128k'],
    zhipu: ['glm-4', 'glm-4v', 'glm-3-turbo'],
    ollama: ['llama3', 'llama2', 'mistral', 'codellama']
}
```

### 图像生成 API 模型选项
```javascript
officialModels: ['gemini-2.5-flash', 'gemini-2.5-flash-image', 'gemini-2.0-flash-exp-image-generation']
aspectRatios: ['1:1', '16:9', '9:16', '4:3', '3:4']
```

## 备用方案

如果下拉选择器始终无法工作，可以：
1. 使用手动输入框（文档分析 API 已添加）
2. 在输入框的 placeholder 中显示可选模型
3. 使用按钮组代替下拉选择器
