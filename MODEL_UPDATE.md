# API 配置更新说明

## 已完成的修改

### 1. 为所有 API 提供商添加了模型下拉选择

每个提供商现在都有预设的模型选项：

#### DeepSeek
- deepseek-chat
- deepseek-coder

#### OpenAI
- gpt-4o
- gpt-4-turbo
- gpt-3.5-turbo

#### Claude
- claude-3-5-sonnet-20241022
- claude-3-sonnet-20240229
- claude-3-opus-20240229

#### Gemini
- gemini-pro
- gemini-1.5-pro
- gemini-1.5-flash

#### Moonshot
- moonshot-v1-8k
- moonshot-v1-32k
- moonshot-v1-128k

#### Zhipu
- glm-4
- glm-4v
- glm-3-turbo

#### Ollama
- llama3
- llama2
- mistral
- codellama

### 2. 修复了关闭按钮位置

- 将 `<view>` 改为 `<text>` 标签
- 设置固定宽高 56rpx × 56rpx
- 使用 flex 布局居中
- 添加 hover 效果
- 确保按钮在右上角正确位置

### 3. 图片比例选择器

图片比例下拉菜单已经存在，使用 picker 组件：
```vue
<picker mode="selector" :range="aspectRatios" @change="onAspectRatioChange" :value="selectedAspectRatioIndex">
    <view class="picker-input">{{ aspectRatios[selectedAspectRatioIndex] }}</view>
</picker>
```

可选比例：
- 1:1
- 16:9
- 9:16
- 4:3
- 3:4

### 4. 模型选择逻辑

- 打开弹窗时，如果有保存的配置，会自动选中对应的模型
- 切换提供商时，会重置为该提供商的第一个模型
- 选择模型后，会自动更新 `apiConfig.model`

## 使用方式

1. 点击任意 API 配置项
2. 在"模型"下拉框中选择预设模型
3. 或者保持默认的第一个模型
4. 填写 API Key
5. 点击"测试连接"验证
6. 点击"保存配置"

## 注意事项

- 所有模型选项都是可调用的真实模型
- 默认选中每个提供商的第一个模型
- 配置会保存到本地存储
- 切换提供商会自动加载对应的模型列表
