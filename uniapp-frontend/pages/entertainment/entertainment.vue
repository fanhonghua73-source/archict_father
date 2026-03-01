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
						<view class="nav-item active">娱乐室</view>
						<view class="nav-item" @click="switchTab('management')">管理台</view>
						<view class="nav-item" @click="switchTab('settings')">设置</view>
					</view>
					<view class="sidebar-footer">v1.0</view>
				</view>

				<view class="main-content">
					<view class="content-container">
						<view class="empty-state">
							<text class="empty-icon">🎮</text>
							<text class="empty-text">娱乐功能开发中</text>
						</view>
					</view>

					<view class="bottom-fixed-area">
						<view class="divider"></view>
						<view class="search-container">
							<view :class="['search-box', searchFocused ? 'focused' : '']">
								<input class="search-input" placeholder="搜索..." v-model="searchText" @focus="searchFocused = true" @blur="searchFocused = false" />
								<view v-if="searchFocused" class="submit-btn"><text>→</text></view>
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
			return { searchText: '', searchFocused: false }
		},
		methods: {
			switchTab(page) {
				uni.switchTab({ url: '/pages/' + page + '/' + page })
			}
		}
	}
</script>

<style>
	@import "../../static/css/common.css";
	.content-container { flex: 1; display: flex; align-items: center; justify-content: center; }
	.empty-state { text-align: center; }
	.empty-icon { font-size: 128rpx; display: block; margin-bottom: 40rpx; }
	.empty-text { font-size: 28rpx; color: #999; }
</style>
