<template>
	<view class="page-container">
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
				<!-- 左侧导航 -->
				<view class="sidebar">
					<view class="nav-items">
						<view class="nav-item" @click="switchTab('index')">项目</view>
						<view class="nav-item" @click="switchTab('resource')">资源</view>
						<view class="nav-item active">工作台</view>
						<view class="nav-item" @click="switchTab('entertainment')">娱乐室</view>
						<view class="nav-item" @click="switchTab('management')">管理台</view>
						<view class="nav-item" @click="switchTab('settings')">设置</view>
					</view>
					<view class="sidebar-footer">v1.0</view>
				</view>

				<!-- 内容区 -->
				<view class="main-content">
					<view class="workbench-container">
						<view
							v-for="(tool, index) in tools"
							:key="index"
							:class="['tool-card', tool.active ? 'active' : 'placeholder']"
							@click="tool.active && openTool(tool)"
						>
							<view v-if="tool.active" class="tool-icon">
								<text>{{ tool.icon }}</text>
							</view>
							<view v-if="tool.active" class="tool-name">{{ tool.name }}</view>
							<view v-if="!tool.active" class="placeholder-text">预留</view>
						</view>
					</view>

					<!-- 底部搜索框 -->
					<view class="bottom-fixed-area">
						<view class="divider"></view>
						<view class="search-container">
							<view :class="['search-box', searchFocused ? 'focused' : '']">
								<input
									class="search-input"
									placeholder="搜索工具..."
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
	</view>
</template>

<script>
	export default {
		data() {
			return {
				searchText: '',
				searchFocused: false,
				tools: [
					{ icon: '📝', name: '文档分析', active: true },
					{ icon: '🖼️', name: '图片生成', active: true },
					{ icon: '📊', name: 'PPT生成', active: true },
					{ icon: '🔍', name: '图片搜索', active: true },
					{ icon: '📐', name: '尺寸计算', active: true },
					{ icon: '💰', name: '成本估算', active: true },
					{ active: false },
					{ active: false }
				]
			}
		},
		methods: {
			switchTab(page) {
				uni.switchTab({
					url: '/pages/' + page + '/' + page
				})
			},
			openTool(tool) {
				if (tool.name === '图片生成') {
					uni.navigateTo({
						url: '/pages/image-gen/image-gen'
					})
				} else if (tool.name === '文档分析') {
					uni.navigateTo({
						url: '/pages/doc-analysis/doc-analysis'
					})
				} else {
					uni.showToast({
						title: tool.name,
						icon: 'none'
					})
				}
			}
		}
	}
</script>

<style>
	@import "../../static/css/common.css";

	/* 工作台容器 */
	.workbench-container {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		grid-template-rows: repeat(2, 1fr);
		gap: 40rpx;
		padding: 40rpx;
		height: 1070rpx;
		flex-shrink: 0;
		overflow: hidden;
	}

	/* 工具卡片 */
	.tool-card {
		background: #fafafa;
		border: 1px solid #e0e0e0;
		border-radius: 16rpx;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		transition: all 0.3s;
	}

	.tool-card.active:hover {
		border-color: #333;
		background: #f5f5f5;
		transform: translateY(-8rpx);
		box-shadow: 0 16rpx 48rpx rgba(0, 0, 0, 0.12);
	}

	.tool-card.placeholder {
		border-style: dashed;
	}

	.tool-icon {
		font-size: 96rpx;
		margin-bottom: 32rpx;
	}

	.tool-name {
		font-size: 28rpx;
		font-weight: 500;
		color: #333;
	}

	.placeholder-text {
		font-size: 24rpx;
		color: #ccc;
	}
</style>
