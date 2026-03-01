<template>
	<view class="page-container">
		<view class="workspace-card">
			<view class="top-bar">
				<view class="user-avatar-header"><text>👤</text></view>
				<view class="window-controls">
					<view class="control-btn">−</view>
					<view class="control-btn">□</view>
					<view class="control-btn">×</view>
				</view>
			</view>

			<view class="main-body">
				<view class="sidebar">
					<view class="nav-items">
						<view class="nav-item" @click="switchTab('index')">项目</view>
						<view class="nav-item" @click="switchTab('resource')">资源</view>
						<view class="nav-item" @click="switchTab('workbench')">工作台</view>
						<view class="nav-item" @click="switchTab('entertainment')">娱乐室</view>
						<view class="nav-item" @click="switchTab('management')">管理台</view>
						<view class="nav-item active">设置</view>
					</view>
					<view class="sidebar-footer">v1.0</view>
				</view>

				<view class="main-content">
					<scroll-view class="settings-container" scroll-y>
						<view class="settings-section" v-for="(section, index) in settings" :key="index">
							<view class="section-title">{{ section.title }}</view>
							<view class="setting-item" v-for="(item, idx) in section.items" :key="idx" @click="handleSettingClick(section.title, item)" :class="item.clickable ? 'clickable' : ''">
								<view class="setting-label">{{ item.label }}</view>
								<view class="setting-value">{{ item.value }}</view>
							</view>
						</view>
					</scroll-view>

					<view class="bottom-fixed-area">
						<view class="divider"></view>
						<view class="search-container">
							<view :class="['search-box', searchFocused ? 'focused' : '']">
								<input class="search-input" placeholder="搜索设置..." v-model="searchText" @focus="searchFocused = true" @blur="searchFocused = false" />
								<view v-if="searchFocused" class="submit-btn"><text>→</text></view>
							</view>
						</view>
					</view>
				</view>
			</view>
		</view>

		<!-- API配置弹窗 -->
		<view v-if="showApiModal" class="modal-overlay">
			<view class="modal-content">
				<view class="modal-header">
					<text class="modal-title">配置 {{ currentApiProvider }}</text>
					<text class="modal-close" @click="closeApiModal">×</text>
				</view>
				<scroll-view class="modal-body" scroll-y>
					<view class="form-group">
						<text class="form-label">API 提供商</text>
						<picker mode="selector" :range="apiProviders" @change="onProviderChange" :value="selectedProviderIndex">
							<view class="picker-input">{{ apiProviders[selectedProviderIndex] }}</view>
						</picker>
					</view>

					<view class="form-group" v-if="currentProvider !== 'ollama'">
						<text class="form-label">API Key</text>
						<input
							class="form-input"
							type="text"
							v-model="apiConfig.apiKey"
							placeholder="请输入 API Key"
							confirm-type="done"
							:focus="false"
							@focus="handleInputFocus"
							@input="handleApiKeyInput"
						/>
					</view>

					<view class="form-group" v-if="currentProvider === 'ollama'">
						<text class="form-label">Base URL</text>
						<input
							class="form-input"
							type="text"
							v-model="apiConfig.baseUrl"
							placeholder="http://localhost:11434"
							confirm-type="done"
							:focus="false"
							@focus="handleInputFocus"
						/>
					</view>

					<view class="form-group">
						<text class="form-label">模型</text>
						<view class="model-selector">
							<picker mode="selector" :range="getModelOptions()" @change="onModelChange" :value="selectedModelIndex" class="model-picker">
								<view class="picker-input">
									<text>{{ apiConfig.model || getModelOptions()[0] }}</text>
									<text class="picker-arrow">▼</text>
								</view>
							</picker>
						</view>
						<input
							class="form-input model-input"
							type="text"
							v-model="apiConfig.model"
							placeholder="或手动输入模型名称"
							confirm-type="done"
							:focus="false"
							@focus="handleInputFocus"
						/>
					</view>

					<view class="form-actions">
						<button class="btn-test" @click="testConnection">测试连接</button>
						<button class="btn-save" @click="saveApiConfig">保存配置</button>
					</view>

					<view v-if="testResult" class="test-result" :class="testResult.success ? 'success' : 'error'">
						{{ testResult.message }}
					</view>
				</scroll-view>
			</view>
		</view>

		<!-- 图像生成API配置弹窗 -->
		<view v-if="showImageModal" class="modal-overlay">
			<view class="modal-content">
				<view class="modal-header">
					<text class="modal-title">配置图像生成 API</text>
					<text class="modal-close" @click="closeImageModal">×</text>
				</view>
				<scroll-view class="modal-body" scroll-y>
					<!-- 模式切换 -->
					<view class="mode-tabs">
						<view :class="['mode-tab', imageApiMode === 'official' ? 'active' : '']" @click="imageApiMode = 'official'">
							官方 API
						</view>
						<view :class="['mode-tab', imageApiMode === 'wild' ? 'active' : '']" @click="imageApiMode = 'wild'">
							野路子
						</view>
					</view>

					<!-- 官方 API 配置 -->
					<view v-if="imageApiMode === 'official'">
						<view class="form-group">
							<text class="form-label">API Key</text>
							<input
								class="form-input"
								type="text"
								v-model="imageConfig.apiKey"
								placeholder="请输入 Google AI Studio API Key"
								confirm-type="done"
								:focus="false"
								@focus="handleInputFocus"
							/>
						</view>

						<view class="form-group">
							<text class="form-label">模型</text>
							<picker mode="selector" :range="officialModels" @change="onOfficialModelChange" :value="selectedOfficialModelIndex">
								<view class="picker-input">
									<text>{{ officialModels[selectedOfficialModelIndex] }}</text>
									<text class="picker-arrow">▼</text>
								</view>
							</picker>
						</view>
					</view>

					<!-- 野路子配置 -->
					<view v-if="imageApiMode === 'wild'">
						<view class="wild-hint">
							<text>⚠️ 野路子使用第三方代理服务，请确保服务可用</text>
						</view>

						<view class="form-group">
							<text class="form-label">Base URL</text>
							<input
								class="form-input"
								type="text"
								v-model="imageConfig.baseUrl"
								placeholder="http://zx2.52youxi.cc:3000"
								confirm-type="done"
								:focus="false"
								@focus="handleInputFocus"
							/>
						</view>

						<view class="form-group">
							<text class="form-label">API Key</text>
							<input
								class="form-input"
								type="text"
								v-model="imageConfig.wildApiKey"
								placeholder="请输入 API Key"
								confirm-type="done"
								:focus="false"
								@focus="handleInputFocus"
							/>
						</view>

						<view class="form-group">
							<text class="form-label">模型名称</text>
							<input
								class="form-input"
								type="text"
								v-model="imageConfig.wildModel"
								placeholder="gemini-3-pro-image-preview"
								confirm-type="done"
								:focus="false"
								@focus="handleInputFocus"
							/>
						</view>

						<view class="form-group">
							<text class="form-label">图片比例</text>
							<picker mode="selector" :range="aspectRatios" @change="onAspectRatioChange" :value="selectedAspectRatioIndex">
								<view class="picker-input">
									<text>{{ aspectRatios[selectedAspectRatioIndex] }}</text>
									<text class="picker-arrow">▼</text>
								</view>
							</picker>
						</view>
					</view>

					<view class="form-actions">
						<button class="btn-test" @click="testImageConnection">测试连接</button>
						<button class="btn-save" @click="saveImageConfig">保存配置</button>
					</view>

					<view v-if="testResult" class="test-result" :class="testResult.success ? 'success' : 'error'">
						{{ testResult.message }}
					</view>
				</scroll-view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				searchText: '',
				searchFocused: false,
				showApiModal: false,
				currentApiProvider: '',
				currentProvider: '',
				selectedProviderIndex: 0,
				selectedModelIndex: 0,
				apiProviders: ['DeepSeek', 'OpenAI', 'Claude', 'Gemini', 'Moonshot', 'Zhipu', 'Ollama'],
				modelOptions: {
					deepseek: ['deepseek-chat', 'deepseek-coder'],
					openai: ['gpt-4o', 'gpt-4-turbo', 'gpt-3.5-turbo'],
					claude: ['claude-3-5-sonnet-20241022', 'claude-3-sonnet-20240229', 'claude-3-opus-20240229'],
					gemini: ['gemini-pro', 'gemini-1.5-pro', 'gemini-1.5-flash'],
					moonshot: ['moonshot-v1-8k', 'moonshot-v1-32k', 'moonshot-v1-128k'],
					zhipu: ['glm-4', 'glm-4v', 'glm-3-turbo'],
					ollama: ['llama3', 'llama2', 'mistral', 'codellama']
				},
				apiConfig: {
					apiKey: '',
					baseUrl: '',
					model: ''
				},
				testResult: null,
				showImageModal: false,
				imageApiMode: 'official',
				selectedOfficialModelIndex: 0,
				selectedAspectRatioIndex: 0,
				officialModels: ['gemini-2.5-flash', 'gemini-2.5-flash-image', 'gemini-2.0-flash-exp-image-generation'],
				aspectRatios: ['1:1', '16:9', '9:16', '4:3', '3:4'],
				imageConfig: {
					apiKey: '',
					model: '',
					baseUrl: '',
					wildApiKey: '',
					wildModel: '',
					aspectRatio: '1:1'
				},
				settings: [
					{
						title: '基本设置',
						items: [
							{ label: '用户名', value: '管理员', clickable: false },
							{ label: '邮箱', value: 'admin@example.com', clickable: false }
						]
					},
					{
						title: '文档分析 API',
						items: [
							{ label: 'DeepSeek', value: '未配置', clickable: true, provider: 'deepseek' },
							{ label: 'OpenAI', value: '未配置', clickable: true, provider: 'openai' },
							{ label: 'Claude', value: '未配置', clickable: true, provider: 'claude' },
							{ label: 'Gemini', value: '未配置', clickable: true, provider: 'gemini' },
							{ label: 'Moonshot', value: '未配置', clickable: true, provider: 'moonshot' },
							{ label: 'Zhipu', value: '未配置', clickable: true, provider: 'zhipu' },
							{ label: 'Ollama', value: '未配置', clickable: true, provider: 'ollama' }
						]
					},
					{
						title: '图像生成 API',
						items: [
							{ label: 'Gemini 官方', value: '未配置', clickable: true, type: 'image', mode: 'official' },
							{ label: 'Gemini 野路子', value: '未配置', clickable: true, type: 'image', mode: 'wild' }
						]
					}
				]
			}
		},
		mounted() {
			// 在组件挂载后更新 API 状态
			this.updateApiStatus()
		},
		methods: {
			switchTab(page) {
				uni.switchTab({ url: '/pages/' + page + '/' + page })
			},
			handleInputFocus(e) {
				console.log('输入框获得焦点', e)
			},
			handleApiKeyInput(e) {
				console.log('API Key 输入:', e.detail.value)
				this.apiConfig.apiKey = e.detail.value
			},
			getModelOptions() {
				const options = this.modelOptions[this.currentProvider] || ['自定义']
				console.log('当前提供商:', this.currentProvider, '模型选项:', options)
				return options
			},
			onModelChange(e) {
				console.log('模型选择改变:', e.detail.value)
				this.selectedModelIndex = e.detail.value
				const options = this.getModelOptions()
				this.apiConfig.model = options[this.selectedModelIndex]
				console.log('选中的模型:', this.apiConfig.model)

				// 强制更新视图
				this.$forceUpdate()
			},
			updateApiStatus() {
				// 更新文档分析 API 状态
				const docApiSection = this.settings.find(s => s.title === '文档分析 API')
				if (docApiSection) {
					docApiSection.items.forEach(item => {
						item.value = this.getApiStatus(item.provider)
					})
				}

				// 更新图像生成 API 状态
				const imageApiSection = this.settings.find(s => s.title === '图像生成 API')
				if (imageApiSection) {
					imageApiSection.items.forEach(item => {
						item.value = this.getImageApiStatus(item.mode)
					})
				}
			},
			getApiStatus(provider) {
				const config = uni.getStorageSync('api_config_' + provider)
				return config ? '已配置' : '未配置'
			},
			getImageApiStatus(mode) {
				const config = uni.getStorageSync('image_api_config')
				if (!config) return '未配置'
				const parsed = JSON.parse(config)
				if (mode === 'official') {
					return parsed.apiKey ? '已配置' : '未配置'
				} else {
					return parsed.baseUrl && parsed.wildApiKey ? '已配置' : '未配置'
				}
			},
			handleSettingClick(sectionTitle, item) {
				console.log('点击了设置项:', sectionTitle, item)

				if (!item.clickable) {
					console.log('该项不可点击')
					return
				}

				if (sectionTitle === '文档分析 API') {
					console.log('打开文档分析 API 配置')
					this.openApiModal(item.label, item.provider)
				} else if (sectionTitle === '图像生成 API') {
					console.log('打开图像生成 API 配置')
					this.openImageModal(item.mode)
				}
			},
			openApiModal(providerName, provider) {
				console.log('openApiModal 被调用:', providerName, provider)
				this.currentApiProvider = providerName
				this.currentProvider = provider
				this.selectedProviderIndex = this.apiProviders.indexOf(providerName)

				// 加载已保存的配置
				const savedConfig = uni.getStorageSync('api_config_' + provider)
				if (savedConfig) {
					this.apiConfig = JSON.parse(savedConfig)
					// 设置模型选择器的索引
					const options = this.getModelOptions()
					this.selectedModelIndex = options.indexOf(this.apiConfig.model)
					if (this.selectedModelIndex === -1) this.selectedModelIndex = 0
				} else {
					// 根据不同提供商设置默认值
					const options = this.modelOptions[provider] || ['自定义']
					this.apiConfig = {
						apiKey: '',
						baseUrl: provider === 'ollama' ? 'http://localhost:11434' : '',
						model: options[0]
					}
					this.selectedModelIndex = 0
				}

				this.testResult = null
				this.showApiModal = true
				console.log('showApiModal 设置为 true')

				// 强制更新视图
				this.$forceUpdate()

				// 测试：显示提示
				uni.showToast({
					title: '弹窗已打开',
					icon: 'none',
					duration: 1000
				})
			},
			closeApiModal() {
				this.showApiModal = false
			},
			onProviderChange(e) {
				this.selectedProviderIndex = e.detail.value
				const providerName = this.apiProviders[this.selectedProviderIndex]
				this.currentApiProvider = providerName
				this.currentProvider = providerName.toLowerCase()

				// 加载新提供商的配置
				const savedConfig = uni.getStorageSync('api_config_' + this.currentProvider)
				if (savedConfig) {
					this.apiConfig = JSON.parse(savedConfig)
					// 设置模型选择器的索引
					const options = this.getModelOptions()
					this.selectedModelIndex = options.indexOf(this.apiConfig.model)
					if (this.selectedModelIndex === -1) this.selectedModelIndex = 0
				} else {
					// 使用默认值
					const options = this.modelOptions[this.currentProvider] || ['自定义']
					this.apiConfig = {
						apiKey: '',
						baseUrl: this.currentProvider === 'ollama' ? 'http://localhost:11434' : '',
						model: options[0]
					}
					this.selectedModelIndex = 0
				}
			},
			getModelPlaceholder() {
				const placeholders = {
					deepseek: 'deepseek-chat 或 deepseek-coder',
					openai: 'gpt-4o 或 gpt-4-turbo',
					claude: 'claude-3-sonnet-20240229',
					gemini: 'gemini-pro',
					moonshot: 'moonshot-v1-8k-vision-preview',
					zhipu: 'glm-4 或 glm-4v',
					ollama: 'llama3 或 llava'
				}
				return placeholders[this.currentProvider] || '请输入模型名称'
			},
			async testConnection() {
				if (!this.apiConfig.apiKey && this.currentProvider !== 'ollama') {
					this.testResult = { success: false, message: '请输入 API Key' }
					return
				}

				this.testResult = { success: false, message: '测试中...' }

				try {
					const response = await uni.request({
						url: 'http://localhost:5002/api/test-connection',
						method: 'POST',
						data: {
							provider: this.currentProvider,
							apiKey: this.apiConfig.apiKey,
							baseUrl: this.apiConfig.baseUrl,
							model: this.apiConfig.model
						}
					})

					if (response.data.success) {
						this.testResult = { success: true, message: '连接成功！' }
					} else {
						this.testResult = { success: false, message: '连接失败：' + response.data.error }
					}
				} catch (error) {
					this.testResult = { success: false, message: '连接失败：' + error.message }
				}
			},
			saveApiConfig() {
				if (!this.apiConfig.apiKey && this.currentProvider !== 'ollama') {
					uni.showToast({ title: '请输入 API Key', icon: 'none' })
					return
				}

				uni.setStorageSync('api_config_' + this.currentProvider, JSON.stringify(this.apiConfig))

				// 更新设置列表中的状态
				const apiSection = this.settings.find(s => s.title === '文档分析 API')
				const item = apiSection.items.find(i => i.provider === this.currentProvider)
				if (item) {
					item.value = '已配置'
				}

				uni.showToast({ title: '保存成功', icon: 'success' })
				this.closeApiModal()
			},
			// 图像生成 API 相关方法
			openImageModal(mode) {
				console.log('openImageModal 被调用:', mode)
				this.imageApiMode = mode

				// 加载已保存的配置
				const savedConfig = uni.getStorageSync('image_api_config')
				if (savedConfig) {
					this.imageConfig = JSON.parse(savedConfig)
				} else {
					this.imageConfig = {
						apiKey: '',
						model: 'gemini-2.5-flash',
						baseUrl: '',
						wildApiKey: '',
						wildModel: 'gemini-3-pro-image-preview',
						aspectRatio: '1:1'
					}
				}

				this.testResult = null
				this.showImageModal = true
				console.log('showImageModal 设置为 true')
			},
			closeImageModal() {
				this.showImageModal = false
			},
			onOfficialModelChange(e) {
				console.log('官方模型选择改变:', e.detail.value)
				this.selectedOfficialModelIndex = e.detail.value
				this.imageConfig.model = this.officialModels[this.selectedOfficialModelIndex]
				console.log('选中的官方模型:', this.imageConfig.model)
			},
			onAspectRatioChange(e) {
				console.log('图片比例选择改变:', e.detail.value)
				this.selectedAspectRatioIndex = e.detail.value
				this.imageConfig.aspectRatio = this.aspectRatios[this.selectedAspectRatioIndex]
				console.log('选中的比例:', this.imageConfig.aspectRatio)
			},
			async testImageConnection() {
				this.testResult = { success: false, message: '测试中...' }

				try {
					let url, key, body

					if (this.imageApiMode === 'official') {
						if (!this.imageConfig.apiKey) {
							this.testResult = { success: false, message: '请输入 API Key' }
							return
						}
						key = this.imageConfig.apiKey
						const model = this.imageConfig.model || 'gemini-2.5-flash'
						url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${key}`
						body = { contents: [{ parts: [{ text: 'test' }] }] }
					} else {
						if (!this.imageConfig.baseUrl || !this.imageConfig.wildApiKey) {
							this.testResult = { success: false, message: '请输入 Base URL 和 API Key' }
							return
						}
						key = this.imageConfig.wildApiKey
						url = `${this.imageConfig.baseUrl}/v1beta/models/${this.imageConfig.wildModel}:generateContent`
						body = {
							contents: [{ parts: [{ text: 'test' }] }],
							generationConfig: { responseModalities: ['Image'] }
						}
					}

					const response = await uni.request({
						url: url,
						method: 'POST',
						header: {
							'Content-Type': 'application/json',
							'Authorization': `Bearer ${key}`
						},
						data: body
					})

					if (response.statusCode === 200 || response.statusCode === 400) {
						this.testResult = { success: true, message: '连接成功！' }
					} else {
						this.testResult = { success: false, message: '连接失败：' + response.statusCode }
					}
				} catch (error) {
					this.testResult = { success: false, message: '连接失败：' + error.message }
				}
			},
			saveImageConfig() {
				if (this.imageApiMode === 'official' && !this.imageConfig.apiKey) {
					uni.showToast({ title: '请输入 API Key', icon: 'none' })
					return
				}

				if (this.imageApiMode === 'wild' && (!this.imageConfig.baseUrl || !this.imageConfig.wildApiKey)) {
					uni.showToast({ title: '请输入 Base URL 和 API Key', icon: 'none' })
					return
				}

				uni.setStorageSync('image_api_config', JSON.stringify(this.imageConfig))

				// 更新设置列表中的状态
				this.updateApiStatus()

				uni.showToast({ title: '保存成功', icon: 'success' })
				this.closeImageModal()
			}
		}
	}
</script>

<style>
	@import "../../static/css/common.css";
	.settings-container { flex: 1; padding: 40rpx; overflow-y: auto; }
	.settings-section { margin-bottom: 40rpx; }
	.section-title { font-size: 28rpx; font-weight: 600; color: #333; margin-bottom: 24rpx; }
	.setting-item { display: flex; justify-content: space-between; padding: 24rpx; background: #fafafa; border-radius: 12rpx; margin-bottom: 16rpx; }
	.setting-item.clickable { cursor: pointer; transition: background 0.2s; }
	.setting-item.clickable:hover { background: #f0f0f0; }
	.setting-label { font-size: 24rpx; color: #666; }
	.setting-value { font-size: 24rpx; color: #333; }

	/* 弹窗样式 */
	.modal-overlay {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		z-index: 999999;
		display: flex;
		align-items: center;
		justify-content: center;
		background: rgba(0, 0, 0, 0.7);
	}
	.modal-content {
		width: 600rpx;
		max-height: 80vh;
		background: white;
		border-radius: 16rpx;
		z-index: 1000000;
		position: relative;
		box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.5);
		display: flex;
		flex-direction: column;
	}
	.modal-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 32rpx;
		border-bottom: 1px solid #eee;
		background: white;
		flex-shrink: 0;
	}
	.modal-title {
		font-size: 32rpx;
		font-weight: 600;
		color: #333;
		flex: 1;
	}
	.modal-close {
		font-size: 56rpx;
		color: #999;
		cursor: pointer;
		line-height: 1;
		width: 56rpx;
		height: 56rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
	}
	.modal-close:hover {
		color: #333;
	}
	.modal-body {
		padding: 32rpx;
		max-height: 60vh;
		background: white;
		overflow-y: auto;
		flex: 1;
	}

	/* 表单样式 */
	.form-group {
		margin-bottom: 32rpx;
		position: relative;
		z-index: 10;
	}
	.form-label {
		display: block;
		font-size: 24rpx;
		color: #666;
		margin-bottom: 12rpx;
	}
	.form-input {
		width: 100%;
		height: 80rpx;
		padding: 0 20rpx;
		border: 2px solid #ddd;
		border-radius: 8rpx;
		font-size: 24rpx;
		line-height: 80rpx;
		box-sizing: border-box;
		background-color: #ffffff;
		color: #333333;
	}
	.form-input:focus {
		border-color: #7cb342;
	}
	.model-selector {
		margin-bottom: 16rpx;
	}
	.model-picker {
		width: 100%;
	}
	.model-input {
		margin-top: 0;
	}
	.picker-input {
		padding: 20rpx;
		border: 2px solid #ddd;
		border-radius: 8rpx;
		font-size: 24rpx;
		background: white;
		color: #333;
		position: relative;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.picker-arrow {
		font-size: 20rpx;
		color: #999;
	}

	/* 按钮样式 */
	.form-actions { display: flex; gap: 16rpx; margin-top: 32rpx; }
	.btn-test, .btn-save { flex: 1; padding: 20rpx; border-radius: 8rpx; font-size: 24rpx; text-align: center; border: none; }
	.btn-test { background: #f0f0f0; color: #333; }
	.btn-save { background: #7cb342; color: white; }

	/* 测试结果 */
	.test-result { margin-top: 24rpx; padding: 20rpx; border-radius: 8rpx; font-size: 24rpx; text-align: center; }
	.test-result.success { background: #e8f5e9; color: #2e7d32; }
	.test-result.error { background: #ffebee; color: #c62828; }

	/* 模式切换标签 */
	.mode-tabs { display: flex; gap: 16rpx; margin-bottom: 32rpx; }
	.mode-tab { flex: 1; padding: 20rpx; border-radius: 8rpx; font-size: 24rpx; text-align: center; background: #f5f5f5; color: #666; cursor: pointer; }
	.mode-tab.active { background: #6366f1; color: white; }

	/* 野路子提示 */
	.wild-hint { background: #fff3cd; color: #856404; padding: 20rpx; border-radius: 8rpx; font-size: 22rpx; margin-bottom: 24rpx; }
</style>
