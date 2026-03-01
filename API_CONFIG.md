# API 配置说明

## 文档分析 API 配置

根据 Text_Censorship 的标准，各个 API 提供商的配置如下：

### 1. DeepSeek
- **Endpoint**: `https://api.deepseek.com/v1/chat/completions`
- **默认模型**: `deepseek-chat`
- **可选模型**: `deepseek-coder`
- **需要**: API Key

### 2. OpenAI
- **Endpoint**: `https://api.openai.com/v1/chat/completions`
- **默认模型**: `gpt-4o`
- **可选模型**: `gpt-4-turbo`
- **需要**: API Key

### 3. Claude
- **Endpoint**: Anthropic API
- **默认模型**: `claude-3-sonnet-20240229`
- **需要**: API Key

### 4. Gemini
- **Endpoint**: Google Generative AI
- **默认模型**: `gemini-pro`
- **需要**: API Key

### 5. Moonshot
- **Endpoint**: `https://api.moonshot.cn/v1/chat/completions`
- **默认模型**: `moonshot-v1-8k-vision-preview`
- **需要**: API Key

### 6. Zhipu (智谱AI)
- **Endpoint**: `https://open.bigmodel.cn/api/paas/v4/chat/completions`
- **默认模型**: `glm-4`
- **可选模型**: `glm-4v`
- **需要**: API Key

### 7. Ollama
- **Endpoint**: `http://localhost:11434/api/generate`
- **默认模型**: `llama3`
- **可选模型**: `llava`
- **需要**: Base URL（本地地址）

## 图像生成 API 配置

### Gemini 官方
- **默认模型**: `gemini-2.5-flash`
- **可选模型**:
  - `gemini-2.5-flash-image`
  - `gemini-2.0-flash-exp-image-generation`
- **需要**: Google AI Studio API Key

### Gemini 野路子
- **默认模型**: `gemini-3-pro-image-preview`
- **需要**:
  - Base URL（如 `http://zx2.52youxi.cc:3000`）
  - API Key
  - 模型名称
  - 图片比例（1:1, 16:9, 9:16, 4:3, 3:4）

## 配置存储

所有配置保存在 UniApp 的本地存储中：
- 文档分析 API: `api_config_{provider}`
- 图像生成 API: `image_api_config`

## 使用方式

1. 在设置页面点击对应的 API 配置项
2. 填写 API Key 和选择模型
3. 点击"测试连接"验证配置
4. 点击"保存配置"保存设置
5. 配置成功后，状态会显示为"已配置"
