<template>
	<view class="page-container">
		<!-- 主卡片 -->
		<view class="workspace-card">
			<!-- 顶栏 -->
			<view class="top-bar">
				<view class="user-avatar-header">
					<text>👤</text>
				</view>
				<view class="window-controls">
					<view class="control-btn">−</view>
					<view class="control-btn">□</view>
					<view class="control-btn">×</view>
				</view>
			</view>

			<!-- 主体 -->
			<view class="main-body">
				<!-- 左侧导航 80px -->
				<view class="sidebar">
					<view class="nav-items">
						<view class="nav-item active">项目</view>
						<view class="nav-item" @click="switchTab('resource')">资源</view>
						<view class="nav-item" @click="switchTab('workbench')">工作台</view>
						<view class="nav-item" @click="switchTab('entertainment')">娱乐室</view>
						<view class="nav-item" @click="switchTab('management')">管理台</view>
						<view class="nav-item" @click="switchTab('settings')">设置</view>
					</view>
					<view class="sidebar-footer">v1.0</view>
				</view>

				<!-- 内容区 -->
				<view class="main-content">
					<!-- 项目网格 -->
					<scroll-view class="p1-container" scroll-y>
						<view class="project-grid">
							<!-- 新增项目卡片 -->
							<view class="project-card new-project-card" @click="openNewProjectModal">
								<view class="new-project-icon">
									<text>+</text>
								</view>
								<view class="new-project-text">新增项目</view>
							</view>

							<!-- 现有项目卡片 -->
							<view
								v-for="(project, index) in projects"
								:key="index"
								:class="['project-card', selectedIndex === index ? 'active' : '']"
								@click="selectProject(index)"
							>
								<!-- 项目图标 -->
								<view class="project-icon">
									<text>🏢</text>
								</view>

								<!-- 项目名称 -->
								<view class="project-name">{{ project.name }}</view>

								<!-- 项目信息 -->
								<view class="project-info">{{ project.location }}</view>

								<!-- 展开后的详细信息 -->
								<view v-if="selectedIndex === index" class="project-details">
									<view class="project-meta">
										<view class="meta-row">
											<text>类型</text>
											<text>{{ project.stage }}</text>
										</view>
										<view class="meta-row">
											<text>地点</text>
											<text>{{ project.location }}</text>
										</view>
										<view class="meta-row">
											<text>面积</text>
											<text>{{ project.area_total }}㎡</text>
										</view>
									</view>

									<!-- 进度条 -->
									<view class="progress-section">
										<view class="progress-label">进度 {{ project.progress }}%</view>
										<view class="progress-bar">
											<view class="progress-fill" :style="{width: project.progress + '%'}"></view>
										</view>
									</view>

									<!-- 进入管理台 -->
									<view class="enter-management-btn" @click.stop="enterManagement(index)">
										<text>进入管理台 →</text>
									</view>
								</view>

								<!-- 状态标签 -->
								<view class="project-meta">
									<view :class="['status-tag', getStatusClass(project.status)]">
										{{ project.status }}
									</view>
								</view>
							</view>
						</view>

						<!-- 分隔线 -->
						<view class="divider"></view>
					</scroll-view>

					<!-- 底部搜索框 -->
					<view class="bottom-fixed-area">
						<view class="divider"></view>
						<view class="search-container">
							<view :class="['search-box', searchFocused ? 'focused' : '']">
								<input
									class="search-input"
									placeholder="搜索项目..."
									v-model="searchText"
									@focus="searchFocused = true"
									@blur="searchFocused = false"
								/>
								<view v-if="searchFocused" class="submit-btn">
									<text>→</text>
								</view>
							</view>
						</view>
					</view>
				</view>
			</view>
		</view>

		<!-- 新增项目弹窗 -->
		<view v-if="showNewProjectModal" class="modal-overlay">
			<view class="modal-content">
				<view class="modal-header">
					<text class="modal-title">新增项目</text>
					<text class="modal-close" @click="closeNewProjectModal">×</text>
				</view>
				<view class="modal-body">
					<view class="form-group">
						<text class="form-label">项目名称</text>
						<input class="form-input" v-model="newProject.name" placeholder="如：滨江住宅项目" />
					</view>
					<view class="form-group">
						<text class="form-label">项目地点</text>
						<input class="form-input" v-model="newProject.location" placeholder="如：杭州市滨江区" />
					</view>
					<view class="form-group">
						<text class="form-label">项目阶段</text>
						<picker mode="selector" :range="stageOptions" :value="newProject.stageIndex" @change="onStageChange">
							<view class="picker-input">
								<text>{{ stageOptions[newProject.stageIndex] }}</text>
								<text class="picker-arrow">▼</text>
							</view>
						</picker>
					</view>
					<view class="form-group">
						<text class="form-label">总面积（㎡）</text>
						<input class="form-input" type="digit" v-model.number="newProject.area_total" placeholder="如：50000" />
					</view>
					<view class="form-group">
						<text class="form-label">项目状态</text>
						<picker mode="selector" :range="statusOptions" :value="newProject.statusIndex" @change="onStatusChange">
							<view class="picker-input">
								<text>{{ statusOptions[newProject.statusIndex] }}</text>
								<text class="picker-arrow">▼</text>
							</view>
						</picker>
					</view>
					<view class="form-actions">
						<button class="btn-secondary" @click="closeNewProjectModal">取消</button>
						<button class="btn-primary" @click="createProject">创建项目</button>
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
				projects: [],
				selectedIndex: -1,
				searchText: '',
				searchFocused: false,
				showNewProjectModal: false,
				newProject: {
					name: '',
					location: '',
					stage: '方案设计',
					stageIndex: 0,
					area_total: null,
					status: '设计中',
					statusIndex: 0,
					progress: 0
				},
				stageOptions: ['方案设计', '初步设计', '施工图设计', '概念设计'],
				statusOptions: ['设计中', '施工中', '规划中', '已完成']
			}
		},
		onLoad() {
			this.loadProjects()
		},
		methods: {
			async loadProjects() {
				try {
					const res = await uni.request({
						url: 'http://localhost:5002/api/projects',
						method: 'GET'
					})

					console.log('加载项目列表响应:', res)
					if (res.data && res.data.success) {
						this.projects = res.data.data
						console.log('加载到的项目:', this.projects)
					} else if (res[1] && res[1].data && res[1].data.success) {
						// 兼容不同的 UniApp 返回格式
						this.projects = res[1].data.data
						console.log('加载到的项目 (格式2):', this.projects)
					}
				} catch (e) {
					console.log('加载项目失败，使用模拟数据:', e)
					this.projects = this.getMockData()
				}
			},

			getMockData() {
				return [
					{
						id: 1,
						name: '滨江住宅项目',
						location: '杭州市滨江区',
						stage: '方案设计',
						area_total: 50000,
						progress: 45,
						status: '设计中'
					},
					{
						id: 2,
						name: '科技园办公楼',
						location: '杭州市余杭区',
						stage: '施工图设计',
						area_total: 80000,
						progress: 75,
						status: '施工中'
					},
					{
						id: 3,
						name: '文化艺术中心',
						location: '杭州市西湖区',
						stage: '概念设计',
						area_total: 35000,
						progress: 20,
						status: '规划中'
					}
				]
			},

			selectProject(index) {
				this.selectedIndex = this.selectedIndex === index ? -1 : index
				// 每次选择都保存到 storage，即使是取消选择
				if (this.selectedIndex !== -1) {
					const project = this.projects[index]
					console.log('选择项目:', project.name, 'ID:', project.id)
					uni.setStorageSync('selectedProject', {
						id: project.id || (index + 1),
						name: project.name
					})
				}
			},

			enterManagement(index) {
				// 确保使用正确的项目
				const project = this.projects[index]
				console.log('进入管理台 - 项目:', project.name, 'ID:', project.id)

				// 强制保存到 storage
				uni.setStorageSync('selectedProject', {
					id: project.id || (index + 1),
					name: project.name
				})

				// 验证保存是否成功
				const saved = uni.getStorageSync('selectedProject')
				console.log('已保存到 storage:', saved)

				// 延迟一下再跳转，确保 storage 已更新
				setTimeout(() => {
					uni.switchTab({ url: '/pages/management/management' })
				}, 100)
			},

			getStatusClass(status) {
				if (status === '设计中' || status === '施工中') return 'status-active'
				if (status === '规划中') return 'status-pending'
				return 'status-done'
			},

			switchTab(page) {
				uni.switchTab({
					url: '/pages/' + page + '/' + page
				})
			},

			openNewProjectModal() {
				this.newProject = { name: "", location: "", stage: "方案设计", stageIndex: 0, area_total: null, status: "设计中", statusIndex: 0, progress: 0 }
				this.showNewProjectModal = true
			},

			closeNewProjectModal() {
				this.showNewProjectModal = false
			},

			onStageChange(e) {
				this.newProject.stageIndex = e.detail.value
				this.newProject.stage = this.stageOptions[e.detail.value]
			},

			onStatusChange(e) {
				this.newProject.statusIndex = e.detail.value
				this.newProject.status = this.statusOptions[e.detail.value]
			},

		async createProject() {
			if (!this.newProject.name) {
				uni.showToast({ title: "请输入项目名称", icon: "none" })
				return
			}
			if (!this.newProject.location) {
				uni.showToast({ title: "请输入项目地点", icon: "none" })
				return
			}

			console.log('准备创建项目:', this.newProject)

			try {
				const res = await uni.request({
					url: "http://localhost:5002/api/projects",
					method: "POST",
					data: this.newProject,
					header: {
						'Content-Type': 'application/json'
					}
				})

				console.log('创建项目响应:', res)

				// UniApp 的 uni.request 返回格式可能是 [err, res]
				const response = res.data ? res : (res[1] || {})
				const data = response.data || {}

				if (data.success) {
					uni.showToast({ title: "创建成功", icon: "success" })
					this.closeNewProjectModal()
					await this.loadProjects()
				} else {
					console.error('创建失败:', data.error)
					uni.showToast({ title: data.error || "创建失败", icon: "none" })
				}
			} catch (e) {
				console.error("创建项目异常:", e)
				uni.showToast({ title: "创建失败: " + e.message, icon: "none", duration: 3000 })
			}
		}
	}
}
</script>

<style>
	page {
		background-color: #f0f2f5;
	}

	* {
		cursor: default;
	}

	.page-container {
		padding: 40rpx;
		min-height: 100vh;
	}

	/* 主卡片 1200px × 695px */
	.workspace-card {
		background: white;
		border-radius: 32rpx;
		box-shadow: 0 40rpx 120rpx rgba(0,0,0,0.3);
		width: 100%;
		max-width: 2400rpx;
		height: 1390rpx;
		margin: 0 auto;
		display: flex;
		flex-direction: column;
		overflow: hidden;
	}

	/* 顶栏 40px */
	.top-bar {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0 40rpx;
		height: 80rpx;
		border-bottom: 1px solid #f0f0f0;
	}

	.user-avatar-header {
		width: 56rpx;
		height: 56rpx;
		border-radius: 50%;
		background: #f5f5f5;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 32rpx;
	}

	.window-controls {
		display: flex;
		gap: 16rpx;
	}

	.control-btn {
		width: 48rpx;
		height: 48rpx;
		background: transparent;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 32rpx;
		color: #999;
		border: 1px solid #e0e0e0;
	}

	/* 主体 */
	.main-body {
		display: flex;
		flex: 1;
		min-height: 0;
	}

	/* 左侧导航 80px */
	.sidebar {
		width: 160rpx;
		padding: 40rpx 30rpx;
		border-right: 1px solid #f0f0f0;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}

	.nav-items {
		display: flex;
		flex-direction: column;
		gap: 16rpx;
	}

	.nav-item {
		font-size: 22rpx;
		color: #999;
		padding: 16rpx 0;
		width: 90rpx;
		margin: 0 auto;
		text-align: justify;
		text-align-last: justify;
	}

	.nav-item.active {
		color: #333;
		font-weight: 500;
	}

	.sidebar-footer {
		font-size: 20rpx;
		color: #ccc;
		text-align: center;
		padding-top: 20rpx;
	}

	/* 内容区 */
	.main-content {
		flex: 1;
		display: flex;
		flex-direction: column;
		height: 100%;
		min-height: 0;
	}

	.p1-container {
		flex: 1;
		padding: 40rpx;
		overflow-y: auto;
	}

	/* 项目网格 */
	.project-grid {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 24rpx;
	}

	.project-card {
		background: #fafafa;
		border: 1px solid #e8e8e8;
		border-radius: 16rpx;
		padding: 28rpx;
		transition: all 0.3s;
		min-height: 400rpx;
	}

	.project-card:hover {
		border-color: #ccc;
		background: #f5f5f5;
		transform: translateY(-4rpx);
	}

	.project-card.active {
		grid-column: span 2;
		grid-row: span 2;
		background: white;
		border-color: #ef4444;
		box-shadow: 0 16rpx 48rpx rgba(239, 68, 68, 0.2);
		padding: 40rpx;
		z-index: 10;
	}

	/* 项目图标 */
	.project-icon {
		width: 80rpx;
		height: 80rpx;
		background: #f5f5f5;
		border-radius: 16rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		margin-bottom: 24rpx;
		font-size: 40rpx;
		transition: all 0.3s;
	}

	.project-card.active .project-icon {
		width: 112rpx;
		height: 112rpx;
		margin-bottom: 32rpx;
		font-size: 56rpx;
	}

	/* 项目名称 */
	.project-name {
		font-size: 24rpx;
		font-weight: 500;
		color: #333;
		margin-bottom: 12rpx;
		transition: all 0.3s;
	}

	.project-card.active .project-name {
		font-size: 32rpx;
		margin-bottom: 16rpx;
	}

	/* 项目信息 */
	.project-info {
		font-size: 20rpx;
		color: #999;
		line-height: 1.6;
		transition: all 0.3s;
	}

	.project-card.active .project-info {
		font-size: 24rpx;
		line-height: 1.8;
	}

	/* 项目元数据 */
	.project-meta {
		margin-top: 20rpx;
		padding-top: 20rpx;
		border-top: 1px solid #f0f0f0;
		transition: all 0.3s;
	}

	.project-card.active .project-meta {
		margin-top: 32rpx;
		padding-top: 32rpx;
	}

	.meta-row {
		display: flex;
		justify-content: space-between;
		font-size: 20rpx;
		color: #999;
		margin-bottom: 8rpx;
		transition: all 0.3s;
	}

	.project-card.active .meta-row {
		font-size: 22rpx;
		margin-bottom: 12rpx;
	}

	/* 进度条 */
	.progress-section {
		margin-top: 24rpx;
	}

	.progress-label {
		font-size: 22rpx;
		color: #666;
		margin-bottom: 12rpx;
	}

	.progress-bar {
		height: 12rpx;
		background: #f0f0f0;
		border-radius: 6rpx;
		overflow: hidden;
	}

	.progress-fill {
		height: 100%;
		background: #7cb342;
		transition: width 0.3s;
	}

	/* 状态标签 */
	.status-tag {
		display: inline-block;
		padding: 6rpx 16rpx;
		border-radius: 8rpx;
		font-size: 18rpx;
		font-weight: 500;
		transition: all 0.3s;
	}

	.status-active {
		background: #e8f5e9;
		color: #2e7d32;
	}

	.status-pending {
		background: #fff3e0;
		color: #e65100;
	}

	.status-done {
		background: #f5f5f5;
		color: #999;
	}

	.project-card.active .status-tag {
		padding: 8rpx 20rpx;
		font-size: 20rpx;
	}

	/* 进入管理台按钮 */
	.enter-management-btn {
		margin-top: 24rpx;
		padding: 16rpx 24rpx;
		background: #7cb342;
		border-radius: 12rpx;
		text-align: center;
		color: white;
		font-size: 22rpx;
		font-weight: 500;
		cursor: pointer;
		transition: background 0.2s;
	}

	.enter-management-btn:hover {
		background: #6fa035;
	}

	/* 分隔线 */
	.divider {
		height: 1px;
		background: #f0f0f0;
		margin: 32rpx 0;
	}

	/* 底部固定区域 105px */
	.bottom-fixed-area {
		height: 210rpx;
		background: white;
		display: flex;
		flex-direction: column;
		justify-content: flex-end;
		flex-shrink: 0;
	}

	.search-container {
		padding: 24rpx 40rpx;
	}

	/* 搜索框 36px */
	.search-box {
		position: relative;
		background: #fafafa;
		border: 1px solid #e8e8e8;
		border-radius: 16rpx;
		padding: 24rpx 80rpx 24rpx 30rpx;
		transition: border-color 0.2s;
	}

	.search-box.focused {
		border-color: #ef4444;
	}

	.search-input {
		width: 100%;
		font-size: 24rpx;
		color: #333;
	}

	.submit-btn {
		position: absolute;
		bottom: 16rpx;
		right: 16rpx;
		width: 40rpx;
		height: 40rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #333;
		font-size: 28rpx;
	}

	.submit-btn:hover {
		color: #ef4444;
	}

	/* 新增项目卡片 */
	.new-project-card {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background: #f5f5f5;
		border: 2px dashed #ccc;
		cursor: pointer;
		transition: all 0.3s;
	}

	.new-project-card:hover {
		border-color: #7cb342;
		background: #f1f8e9;
		transform: translateY(-4rpx);
	}

	.new-project-icon {
		width: 80rpx;
		height: 80rpx;
		background: #e0e0e0;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 60rpx;
		color: #999;
		margin-bottom: 16rpx;
	}

	.new-project-text {
		font-size: 24rpx;
		color: #666;
	}

	/* 弹窗 */
	.modal-overlay {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(0, 0, 0, 0.5);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1000;
	}

	.modal-content {
		background: white;
		border-radius: 24rpx;
		width: 640rpx;
		max-height: 80vh;
		overflow-y: auto;
		box-shadow: 0 40rpx 120rpx rgba(0, 0, 0, 0.3);
	}

	.modal-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 32rpx 40rpx;
		border-bottom: 1px solid #f0f0f0;
	}

	.modal-title {
		font-size: 28rpx;
		font-weight: 600;
		color: #333;
	}

	.modal-close {
		font-size: 40rpx;
		color: #999;
		cursor: pointer;
		line-height: 1;
		padding: 0 8rpx;
	}

	.modal-body {
		padding: 32rpx 40rpx;
		display: flex;
		flex-direction: column;
		gap: 24rpx;
	}

	.form-group {
		display: flex;
		flex-direction: column;
		gap: 12rpx;
	}

	.form-label {
		font-size: 24rpx;
		color: #666;
		font-weight: 500;
	}

	.form-input {
		border: 1px solid #e0e0e0;
		border-radius: 12rpx;
		padding: 20rpx 24rpx;
		font-size: 24rpx;
		color: #333;
		background: #fafafa;
	}

	.picker-input {
		border: 1px solid #e0e0e0;
		border-radius: 12rpx;
		padding: 20rpx 24rpx;
		font-size: 24rpx;
		color: #333;
		background: #fafafa;
		display: flex;
		justify-content: space-between;
	}

	.picker-arrow {
		color: #999;
	}

	.form-actions {
		display: flex;
		gap: 16rpx;
		justify-content: flex-end;
		margin-top: 8rpx;
	}

	.btn-primary {
		padding: 20rpx 48rpx;
		background: #7cb342;
		color: white;
		border-radius: 12rpx;
		font-size: 24rpx;
		font-weight: 500;
		border: none;
	}

	.btn-secondary {
		padding: 20rpx 48rpx;
		background: #f5f5f5;
		color: #666;
		border-radius: 12rpx;
		font-size: 24rpx;
		border: none;
	}
</style>
