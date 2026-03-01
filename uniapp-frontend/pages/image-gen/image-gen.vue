<template>
	<view class="page-container">
		<view class="workspace-card">
			<view class="top-bar">
				<view class="user-avatar-header"><text>👤</text></view>
				<view class="window-controls">
					<view class="control-btn" @click="goBack">←</view>
					<view class="control-btn">−</view>
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
					<view class="p9-container">
						<!-- 上半部分 -->
						<view class="upper-section">
							<!-- 左侧：2×2 上传框 -->
							<view class="upload-grid-left">
								<view class="upload-box main" @click="selectImage('base')">
									<image v-if="baseImage" :src="baseImage" mode="aspectFill" class="preview-img"></image>
									<view v-else>
										<view class="upload-icon">📷</view>
										<view class="upload-text">主图</view>
									</view>
								</view>
								<view v-for="(img, index) in referenceImages" :key="index" class="upload-box" @click="selectImage('ref', index)">
									<image v-if="img" :src="img" mode="aspectFill" class="preview-img"></image>
									<view v-else>
										<view class="upload-icon">🖼️</view>
										<view class="upload-text">参考{{ index + 1 }}</view>
									</view>
								</view>
							</view>

							<!-- 右侧：预览区 -->
							<view class="preview-area">
								<view class="preview-content">
									<image v-if="generatedImage" :src="generatedImage" mode="aspectFit" class="generated-img"></image>
									<view v-else class="preview-placeholder">
										<text class="preview-text">生成的图片将显示在这里</text>
									</view>
								</view>
								<!-- 工具栏 -->
								<view class="toolbar">
									<view class="tool-icon" @click="handleTool('brush')">🖌️</view>
									<view class="tool-icon" @click="handleTool('eraser')">🧹</view>
									<view class="tool-icon" @click="handleTool('fill')">🪣</view>
									<view class="tool-icon" @click="handleTool('save')">💾</view>
								</view>
							</view>
						</view>

						<!-- 下半部分：输入输出框 -->
						<view class="lower-section">
							<!-- 左侧输入 -->
							<view :class="['input-box', inputFocused ? 'focused' : '']">
								<textarea class="input-textarea" placeholder="输入生成提示..." v-model="prompt" @focus="inputFocused = true" @blur="inputFocused = false"></textarea>
								<view v-if="inputFocused" class="submit-btn" @click="generateImage"><text>→</text></view>
							</view>

							<!-- 右侧输出 -->
							<view :class="['input-box', outputFocused ? 'focused' : '']">
								<textarea class="input-textarea" placeholder="生成结果..." v-model="outputText" @focus="outputFocused = true" @blur="outputFocused = false"></textarea>
								<view v-if="outputFocused" class="submit-btn" @click="saveOutput"><text>→</text></view>
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
				baseImage: '',
				referenceImages: ['', '', ''],
				prompt: '',
				generatedImage: '',
				outputText: '',
				inputFocused: false,
				outputFocused: false
			}
		},
		methods: {
			switchTab(page) {
				uni.switchTab({ url: '/pages/' + page + '/' + page })
			},
			goBack() {
				uni.navigateBack()
			},
			selectImage(type, index) {
				uni.chooseImage({
					count: 1,
					success: (res) => {
						if (type === 'base') {
							this.baseImage = res.tempFilePaths[0]
						} else {
							this.referenceImages[index] = res.tempFilePaths[0]
						}
					}
				})
			},
			async generateImage() {
				if (!this.baseImage || !this.prompt) {
					uni.showToast({ title: '请上传主图并输入提示', icon: 'none' })
					return
				}

				// 检查是否配置了 API
				const config = uni.getStorageSync('image_api_config')
				if (!config) {
					uni.showToast({ title: '请先在设置中配置图像生成 API', icon: 'none' })
					return
				}

				const apiConfig = JSON.parse(config)

				uni.showLoading({ title: '生成中...' })

				try {
					// 将图片转换为 base64
					const baseImageBase64 = await this.imageToBase64(this.baseImage)
					const refImagesBase64 = []

					for (let i = 0; i < this.referenceImages.length; i++) {
						if (this.referenceImages[i]) {
							const refBase64 = await this.imageToBase64(this.referenceImages[i])
							refImagesBase64.push(refBase64)
						}
					}

					// 构建请求
					let url, key, body

					// 判断使用官方还是野路子
					const useOfficial = apiConfig.apiKey && apiConfig.apiKey.length > 0

					if (useOfficial) {
						// 官方 API
						key = apiConfig.apiKey
						const model = apiConfig.model || 'gemini-2.5-flash'
						url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${key}`

						const parts = [
							{ text: this.prompt },
							{ inline_data: { mime_type: 'image/png', data: baseImageBase64 } }
						]

						refImagesBase64.forEach(img => {
							parts.push({ inline_data: { mime_type: 'image/png', data: img } })
						})

						body = {
							contents: [{ parts: parts }],
							generationConfig: { responseModalities: ['image', 'text'] }
						}
					} else {
						// 野路子
						key = apiConfig.wildApiKey
						url = `${apiConfig.baseUrl}/v1beta/models/${apiConfig.wildModel}:generateContent`

						const parts = [
							{ text: this.prompt },
							{ inline_data: { mime_type: 'image/png', data: baseImageBase64 } }
						]

						refImagesBase64.forEach(img => {
							parts.push({ inline_data: { mime_type: 'image/png', data: img } })
						})

						body = {
							contents: [{ parts: parts }],
							generationConfig: {
								responseModalities: ['Image'],
								imageConfig: { aspectRatio: apiConfig.aspectRatio || '1:1' }
							}
						}
					}

					const response = await uni.request({
						url: url,
						method: 'POST',
						header: {
							'Content-Type': 'application/json',
							'Authorization': `Bearer ${key}`
						},
						data: body,
						timeout: 60000
					})

					uni.hideLoading()

					if (response.statusCode === 200 && response.data.candidates) {
						const candidate = response.data.candidates[0]
						if (candidate && candidate.content) {
							for (const part of candidate.content.parts) {
								if (part.inlineData && part.inlineData.data) {
									this.generatedImage = 'data:image/png;base64,' + part.inlineData.data
									this.outputText = '图片生成成功！'
									uni.showToast({ title: '生成成功', icon: 'success' })
									return
								}
							}
						}
					}

					this.outputText = '生成失败：' + JSON.stringify(response.data).substring(0, 100)
					uni.showToast({ title: '生成失败', icon: 'none' })

				} catch (error) {
					uni.hideLoading()
					this.outputText = '生成失败：' + error.message
					uni.showToast({ title: '生成失败：' + error.message, icon: 'none' })
				}
			},
			imageToBase64(imagePath) {
				return new Promise((resolve, reject) => {
					uni.getFileSystemManager().readFile({
						filePath: imagePath,
						encoding: 'base64',
						success: (res) => {
							resolve(res.data)
						},
						fail: (err) => {
							reject(err)
						}
					})
				})
			},
			handleTool(tool) {
				uni.showToast({ title: '工具: ' + tool, icon: 'none' })
			},
			saveOutput() {
				uni.showToast({ title: '保存成功', icon: 'success' })
			}
		}
	}
</script>

<style>
	@import "../../static/css/common.css";
	.p9-container { display: flex; flex-direction: column; padding: 40rpx; flex: 1; gap: 40rpx; }
	.upper-section { display: grid; grid-template-columns: 1fr 1fr; gap: 40rpx; flex: 1; }
	.upload-grid-left { display: grid; grid-template-columns: repeat(2, 1fr); grid-template-rows: repeat(2, 1fr); gap: 32rpx; }
	.upload-box { background: #fafafa; border: 1px dashed #d0d0d0; border-radius: 16rpx; display: flex; flex-direction: column; align-items: center; justify-content: center; transition: all 0.2s; padding: 32rpx; position: relative; }
	.upload-box:hover { background: #f5f5f5; border-color: #333; }
	.upload-box.main { background: #f5f5f5; border-color: #d0d0d0; }
	.upload-icon { font-size: 64rpx; color: #999; margin-bottom: 16rpx; }
	.upload-text { font-size: 22rpx; color: #999; text-align: center; }
	.preview-img { width: 100%; height: 100%; position: absolute; top: 0; left: 0; border-radius: 16rpx; }
	.preview-area { background: #fafafa; border: 1px solid #e8e8e8; border-radius: 16rpx; display: flex; flex-direction: column; overflow: hidden; position: relative; }
	.preview-content { flex: 1; display: flex; align-items: center; justify-content: center; padding: 32rpx; }
	.preview-placeholder { text-align: center; }
	.preview-text { font-size: 24rpx; color: #999; }
	.generated-img { max-width: 100%; max-height: 100%; }
	.toolbar { position: absolute; top: 20rpx; right: 20rpx; display: flex; gap: 16rpx; background: rgba(255, 255, 255, 0.9); padding: 16rpx; border-radius: 12rpx; }
	.tool-icon { width: 56rpx; height: 56rpx; display: flex; align-items: center; justify-content: center; background: #fff; border: 1px solid #e8e8e8; border-radius: 8rpx; font-size: 32rpx; }
	.lower-section { display: grid; grid-template-columns: 1fr 1fr; gap: 40rpx; height: 200rpx; }
	.input-box { background: #fafafa; border: 1px solid #e8e8e8; border-radius: 16rpx; padding: 20rpx 24rpx; position: relative; display: flex; flex-direction: column; transition: border-color 0.2s; }
	.input-box.focused { border-color: #ef4444; }
	.input-textarea { flex: 1; width: 100%; font-size: 24rpx; color: #333; padding-right: 64rpx; }
	.submit-btn { position: absolute; bottom: 16rpx; right: 16rpx; width: 40rpx; height: 40rpx; display: flex; align-items: center; justify-content: center; color: #333; font-size: 28rpx; }
	.submit-btn:hover { color: #ef4444; }
</style>
