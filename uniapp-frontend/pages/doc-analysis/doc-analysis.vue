<template>
	<view class="page-container">
		<view class="workspace-card">
			<view class="top-bar">
				<view class="user-avatar-header"><text>👤</text></view>
				<view class="page-title">文档分析</view>
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
						<view class="nav-item" @click="switchTab('settings')">设置</view>
					</view>
					<view class="sidebar-footer">v1.0</view>
				</view>

				<view class="main-content">
					<view class="doc-analysis-container">
						<!-- 步骤指示器 -->
						<view class="steps">
							<view :class="['step', currentStep >= 1 ? 'active' : '']">1. 输入文档</view>
							<view :class="['step', currentStep >= 2 ? 'active' : '']">2. 分析结构</view>
							<view :class="['step', currentStep >= 3 ? 'active' : '']">3. 生成新文档</view>
						</view>

						<!-- 步骤1: 输入文档 -->
						<view v-if="currentStep === 1" class="step-content">
							<view class="section-title">输入原始文档</view>
							<textarea class="text-input" v-model="originalText" placeholder="请输入需要分析的文档内容..." />

							<view class="api-selector">
								<text class="label">选择 API:</text>
								<picker mode="selector" :range="availableApis" @change="onApiChange" :value="selectedApiIndex">
									<view class="picker-input">{{ availableApis[selectedApiIndex] }}</view>
								</picker>
							</view>

							<button class="btn-primary" @click="analyzeDocument" :disabled="!originalText || analyzing">
								{{ analyzing ? '分析中...' : '分析文档' }}
							</button>
						</view>

						<!-- 步骤2: 显示分析结果 -->
						<view v-if="currentStep === 2" class="step-content">
							<view class="section-title">文档结构分析</view>
							<view class="analysis-result">
								<view class="result-item" v-for="(value, key) in template" :key="key">
									<text class="result-label">{{ key }}:</text>
									<text class="result-value">{{ value }}</text>
								</view>
							</view>

							<view class="button-group">
								<button class="btn-secondary" @click="currentStep = 1">返回修改</button>
								<button class="btn-primary" @click="currentStep = 3">继续生成</button>
							</view>
						</view>

						<!-- 步骤3: 生成新文档 -->
						<view v-if="currentStep === 3" class="step-content">
							<view class="section-title">输入新内容要点</view>
							<textarea class="text-input" v-model="newContent" placeholder="请输入新文档的内容要点..." />

							<button class="btn-primary" @click="generateDocument" :disabled="!newContent || generating">
								{{ generating ? '生成中...' : '生成新文档' }}
							</button>

							<view v-if="generatedText" class="generated-result">
								<view class="result-header">
									<text class="result-title">生成的文档</text>
									<button class="btn-copy" @click="copyResult">复制</button>
								</view>
								<view class="result-text">{{ generatedText }}</view>
							</view>

							<view class="button-group" v-if="generatedText">
								<button class="btn-secondary" @click="resetAll">重新开始</button>
							</view>
						</view>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				currentStep: 1,
				originalText: '',
				newContent: '',
				generatedText: '',
				template: null,
				analyzing: false,
				generating: false,
				selectedApiIndex: 0,
				availableApis: []
			}
		},
		onLoad() {
			this.loadAvailableApis()
		},
		methods: {
			switchTab(page) {
				uni.switchTab({ url: '/pages/' + page + '/' + page })
			},
			loadAvailableApis() {
				// 从本地存储加载已配置的 API
				const providers = ['deepseek', 'openai', 'claude', 'gemini', 'moonshot', 'zhipu', 'ollama']
				const configured = []

				providers.forEach(provider => {
					const config = uni.getStorageSync('api_config_' + provider)
					if (config) {
						const providerNames = {
							deepseek: 'DeepSeek',
							openai: 'OpenAI',
							claude: 'Claude',
							gemini: 'Gemini',
							moonshot: 'Moonshot',
							zhipu: 'Zhipu',
							ollama: 'Ollama'
						}
						configured.push(providerNames[provider])
					}
				})

				if (configured.length === 0) {
					this.availableApis = ['请先在设置中配置 API']
				} else {
					this.availableApis = configured
				}
			},
			onApiChange(e) {
				this.selectedApiIndex = e.detail.value
			},
			async analyzeDocument() {
				if (!this.originalText) {
					uni.showToast({ title: '请输入文档内容', icon: 'none' })
					return
				}

				if (this.availableApis[0] === '请先在设置中配置 API') {
					uni.showToast({ title: '请先在设置中配置 API', icon: 'none' })
					return
				}

				this.analyzing = true

				try {
					const selectedApi = this.availableApis[this.selectedApiIndex].toLowerCase()
					const response = await uni.request({
						url: 'http://localhost:5002/api/document/analyze',
						method: 'POST',
						data: {
							text: this.originalText,
							api_type: selectedApi
						}
					})

					if (response.data.success) {
						this.template = response.data.data
						this.currentStep = 2
					} else {
						uni.showToast({ title: '分析失败: ' + response.data.error, icon: 'none' })
					}
				} catch (error) {
					uni.showToast({ title: '请求失败: ' + error.message, icon: 'none' })
				} finally {
					this.analyzing = false
				}
			},
			async generateDocument() {
				if (!this.newContent) {
					uni.showToast({ title: '请输入新内容要点', icon: 'none' })
					return
				}

				this.generating = true

				try {
					const selectedApi = this.availableApis[this.selectedApiIndex].toLowerCase()
					const response = await uni.request({
						url: 'http://localhost:5002/api/document/generate',
						method: 'POST',
						data: {
							template: this.template,
							new_content: this.newContent,
							api_type: selectedApi
						}
					})

					if (response.data.success) {
						this.generatedText = response.data.data.text
					} else {
						uni.showToast({ title: '生成失败: ' + response.data.error, icon: 'none' })
					}
				} catch (error) {
					uni.showToast({ title: '请求失败: ' + error.message, icon: 'none' })
				} finally {
					this.generating = false
				}
			},
			copyResult() {
				uni.setClipboardData({
					data: this.generatedText,
					success: () => {
						uni.showToast({ title: '已复制到剪贴板', icon: 'success' })
					}
				})
			},
			resetAll() {
				this.currentStep = 1
				this.originalText = ''
				this.newContent = ''
				this.generatedText = ''
				this.template = null
			}
		}
	}
</script>

<style>
	@import "../../static/css/common.css";

	.page-title {
		position: absolute;
		left: 50%;
		transform: translateX(-50%);
		font-size: 28rpx;
		font-weight: 500;
		color: #333;
	}

	.doc-analysis-container {
		flex: 1;
		padding: 40rpx;
		overflow-y: auto;
	}

	/* 步骤指示器 */
	.steps {
		display: flex;
		justify-content: space-between;
		margin-bottom: 40rpx;
		padding: 0 40rpx;
	}

	.step {
		flex: 1;
		text-align: center;
		padding: 20rpx;
		background: #f5f5f5;
		border-radius: 8rpx;
		font-size: 24rpx;
		color: #999;
		margin: 0 8rpx;
	}

	.step.active {
		background: #7cb342;
		color: white;
		font-weight: 500;
	}

	/* 步骤内容 */
	.step-content {
		background: white;
		border-radius: 16rpx;
		padding: 40rpx;
	}

	.section-title {
		font-size: 32rpx;
		font-weight: 600;
		color: #333;
		margin-bottom: 32rpx;
	}

	.text-input {
		width: 100%;
		min-height: 400rpx;
		padding: 24rpx;
		border: 1px solid #ddd;
		border-radius: 12rpx;
		font-size: 24rpx;
		line-height: 1.6;
		box-sizing: border-box;
		margin-bottom: 32rpx;
	}

	.api-selector {
		display: flex;
		align-items: center;
		margin-bottom: 32rpx;
	}

	.api-selector .label {
		font-size: 24rpx;
		color: #666;
		margin-right: 16rpx;
	}

	.picker-input {
		flex: 1;
		padding: 20rpx;
		border: 1px solid #ddd;
		border-radius: 8rpx;
		font-size: 24rpx;
		background: white;
	}

	/* 按钮 */
	.btn-primary, .btn-secondary, .btn-copy {
		padding: 24rpx 48rpx;
		border-radius: 8rpx;
		font-size: 28rpx;
		text-align: center;
		border: none;
	}

	.btn-primary {
		width: 100%;
		background: #7cb342;
		color: white;
	}

	.btn-primary:disabled {
		background: #ccc;
		color: #999;
	}

	.btn-secondary {
		background: #f5f5f5;
		color: #333;
	}

	.btn-copy {
		padding: 16rpx 32rpx;
		background: #2196f3;
		color: white;
		font-size: 24rpx;
	}

	.button-group {
		display: flex;
		gap: 16rpx;
		margin-top: 32rpx;
	}

	.button-group button {
		flex: 1;
	}

	/* 分析结果 */
	.analysis-result {
		background: #fafafa;
		border-radius: 12rpx;
		padding: 32rpx;
		margin-bottom: 32rpx;
	}

	.result-item {
		margin-bottom: 24rpx;
		padding-bottom: 24rpx;
		border-bottom: 1px solid #eee;
	}

	.result-item:last-child {
		margin-bottom: 0;
		padding-bottom: 0;
		border-bottom: none;
	}

	.result-label {
		display: block;
		font-size: 24rpx;
		color: #666;
		margin-bottom: 8rpx;
	}

	.result-value {
		display: block;
		font-size: 26rpx;
		color: #333;
		line-height: 1.6;
	}

	/* 生成结果 */
	.generated-result {
		margin-top: 32rpx;
		background: #fafafa;
		border-radius: 12rpx;
		padding: 32rpx;
	}

	.result-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 24rpx;
	}

	.result-title {
		font-size: 28rpx;
		font-weight: 600;
		color: #333;
	}

	.result-text {
		font-size: 26rpx;
		color: #333;
		line-height: 1.8;
		white-space: pre-wrap;
	}
</style>

