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
						<view class="nav-item active">资源</view>
						<view class="nav-item" @click="switchTab('workbench')">工作台</view>
						<view class="nav-item" @click="switchTab('entertainment')">娱乐室</view>
						<view class="nav-item" @click="switchTab('management')">管理台</view>
						<view class="nav-item" @click="switchTab('settings')">设置</view>
					</view>
					<view class="sidebar-footer">v1.0</view>
				</view>

				<!-- 内容区 -->
				<view class="main-content">
					<view class="resource-container">
						<view
							v-for="(item, index) in resources"
							:key="index"
							class="resource-card"
							@click="openResource(item)"
						>
							<view class="resource-icon">
								<text>{{ item.icon }}</text>
							</view>
							<view class="resource-name">{{ item.name }}</view>
							<view class="resource-count">{{ item.count }} 项</view>
						</view>
					</view>

					<!-- 底部搜索框 -->
					<view class="bottom-fixed-area">
						<view class="divider"></view>
						<view class="search-container">
							<view :class="['search-box', searchFocused ? 'focused' : '']">
								<input
									class="search-input"
									placeholder="搜索资源..."
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
				resources: [
					{ icon: '📐', name: '规范标准', count: 156 },
					{ icon: '📚', name: '技术文档', count: 89 },
					{ icon: '🖼️', name: '图片素材', count: 2340 },
					{ icon: '📊', name: '数据报表', count: 45 },
					{ icon: '🎨', name: '设计模板', count: 78 },
					{ icon: '📝', name: '合同模板', count: 23 },
					{ icon: '🔧', name: '工具软件', count: 34 },
					{ icon: '📦', name: '材料库', count: 567 }
				]
			}
		},
		methods: {
			switchTab(page) {
				uni.switchTab({
					url: '/pages/' + page + '/' + page
				})
			},
			openResource(item) {
				uni.showToast({
					title: item.name,
					icon: 'none'
				})
			}
		}
	}
</script>

<style>
	@import "../../static/css/common.css";

	/* 资源容器 */
	.resource-container {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		grid-template-rows: repeat(2, 1fr);
		gap: 40rpx;
		padding: 40rpx;
		height: 1070rpx;
		flex-shrink: 0;
		overflow: hidden;
	}

	/* 资源卡片 */
	.resource-card {
		background: #fafafa;
		border: 1px solid #e0e0e0;
		border-radius: 16rpx;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		transition: all 0.3s;
	}

	.resource-card:hover {
		border-color: #333;
		background: #f5f5f5;
		transform: translateY(-8rpx);
		box-shadow: 0 16rpx 48rpx rgba(0, 0, 0, 0.12);
	}

	.resource-icon {
		font-size: 96rpx;
		margin-bottom: 32rpx;
	}

	.resource-name {
		font-size: 28rpx;
		font-weight: 500;
		color: #333;
		margin-bottom: 12rpx;
	}

	.resource-count {
		font-size: 22rpx;
		color: #999;
	}
</style>
