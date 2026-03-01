# 管理台和工作台完整实现方案

## 概述

本文档描述了管理台文件上传系统和工作台其他功能的完整实现方案。

## 一、管理台文件上传系统

### 1.1 后端 API 实现

在 `backend/app.py` 中添加文件上传接口：

```python
@app.route('/api/projects/<int:project_id>/files/upload', methods=['POST'])
def upload_file(project_id):
    """上传文件到项目"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': '没有文件'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': '文件名为空'}), 400

        # 获取表单数据
        name = request.form.get('name', file.filename)
        file_type = request.form.get('type', '')
        category = request.form.get('category', 'original')
        remark = request.form.get('remark', '')

        # 获取存储配置
        storage_config = project_mgr.get_storage_config(project_id)

        # 生成文件路径
        import os
        from datetime import datetime
        from werkzeug.utils import secure_filename

        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"

        # 根据存储类型保存文件
        if storage_config['type'] == 'local':
            save_path = os.path.join(storage_config['path'], category, unique_filename)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            file.save(save_path)
            storage_path = save_path
        elif storage_config['type'] == 'nas':
            save_path = os.path.join(storage_config['path'], category, unique_filename)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            file.save(save_path)
            storage_path = save_path
        else:  # url
            # 对于 URL 类型，需要上传到对象存储
            # 这里简化处理，保存到临时目录
            temp_dir = os.path.join(BASE_DIR, 'temp', str(project_id), category)
            os.makedirs(temp_dir, exist_ok=True)
            save_path = os.path.join(temp_dir, unique_filename)
            file.save(save_path)
            storage_path = f"{storage_config['url']}/{category}/{unique_filename}"

        # 添加文件记录到数据库
        file_data = {
            'name': name,
            'type': file_type,
            'category': category,
            'path': category,
            'storage_path': storage_path,
            'size': os.path.getsize(save_path) if os.path.exists(save_path) else 0,
            'remark': remark
        }

        result = project_mgr.add_file(project_id, file_data)
        return jsonify({'success': True, 'data': result})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
```

### 1.2 前端完整代码

由于 management.vue 文件太大，我已经创建了补丁文件 `MANAGEMENT_UPLOAD_PATCH.md`，请按照该文件中的说明手动添加代码。

关键点：
1. 添加 `showUploadModal`, `uploading`, `uploadForm`, `fileTypes`, `currentCategory` 到 data()
2. 添加 `computed.filteredFiles` 计算属性
3. 添加文件上传相关的 methods
4. 修改 `selectPrimaryDir` 和 `selectSecondaryDir` 更新 `currentCategory`
5. 在 `onShow()` 中调用 `this.loadFiles()`
6. 添加 CSS 样式

## 二、工作台功能实现

### 2.1 尺寸计算工具

创建 `uniapp-frontend/pages/size-calc/size-calc.vue`：

```vue
<template>
	<view class="page-container">
		<view class="workspace-card">
			<view class="top-bar">
				<view class="user-avatar-header"><text>👤</text></view>
				<view class="top-bar-title">尺寸计算</view>
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
					<view class="calc-container">
						<!-- 左侧：输入表单 -->
						<view class="input-section">
							<view class="section-title">基础参数</view>

							<view class="form-group">
								<text class="form-label">用地面积（㎡）</text>
								<input class="form-input" type="digit" v-model.number="params.landArea" placeholder="如：36000" />
							</view>

							<view class="form-group">
								<text class="form-label">容积率</text>
								<input class="form-input" type="digit" v-model.number="params.far" placeholder="如：2.4" />
							</view>

							<view class="form-group">
								<text class="form-label">建筑类型</text>
								<picker mode="selector" :range="buildingTypes" :value="params.buildingTypeIndex" @change="onBuildingTypeChange">
									<view class="picker-input">
										<text>{{ buildingTypes[params.buildingTypeIndex] }}</text>
										<text class="picker-arrow">▼</text>
									</view>
								</picker>
							</view>

							<view class="form-group">
								<text class="form-label">最大高度（m）</text>
								<input class="form-input" type="digit" v-model.number="params.maxHeight" placeholder="如：100" />
							</view>

							<view class="form-group">
								<text class="form-label">绿地率</text>
								<input class="form-input" type="digit" v-model.number="params.greenRatio" placeholder="如：0.3" />
							</view>

							<button class="btn-primary" @click="calculate" :disabled="calculating">
								{{ calculating ? '计算中...' : '开始计算' }}
							</button>
						</view>

						<!-- 右侧：计算结果 -->
						<view class="result-section">
							<view class="section-title">计算结果</view>

							<view v-if="!result" class="empty-result">
								<text>请输入参数并点击"开始计算"</text>
							</view>

							<view v-else class="result-content">
								<view class="result-item">
									<text class="result-label">总建筑面积</text>
									<text class="result-value">{{ result.totalArea }} ㎡</text>
								</view>

								<view class="result-item">
									<text class="result-label">住宅面积</text>
									<text class="result-value">{{ result.breakdown.residential }} ㎡</text>
								</view>

								<view class="result-item">
									<text class="result-label">商业面积</text>
									<text class="result-value">{{ result.breakdown.commercial }} ㎡</text>
								</view>

								<view class="result-item">
									<text class="result-label">地下停车面积</text>
									<text class="result-value">{{ result.breakdown.parking }} ㎡</text>
								</view>

								<view class="recommendations">
									<text class="recommendations-title">建议</text>
									<view v-for="(rec, index) in result.recommendations" :key="index" class="recommendation-item">
										<text>• {{ rec }}</text>
									</view>
								</view>

								<button class="btn-secondary" @click="exportToManagement">
									导入到管理台
								</button>
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
			params: {
				landArea: null,
				far: null,
				buildingTypeIndex: 0,
				buildingType: 'residential',
				maxHeight: null,
				greenRatio: null
			},
			buildingTypes: ['住宅', '商业', '办公', '综合'],
			calculating: false,
			result: null
		}
	},
	methods: {
		switchTab(page) {
			uni.switchTab({ url: '/pages/' + page + '/' + page })
		},

		onBuildingTypeChange(e) {
			this.params.buildingTypeIndex = e.detail.value
			const typeMap = ['residential', 'commercial', 'office', 'mixed']
			this.params.buildingType = typeMap[e.detail.value]
		},

		async calculate() {
			if (!this.params.landArea || !this.params.far) {
				uni.showToast({ title: '请输入用地面积和容积率', icon: 'none' })
				return
			}

			this.calculating = true

			try {
				const res = await uni.request({
					url: 'http://localhost:5002/api/calculation/size',
					method: 'POST',
					data: this.params
				})

				if (res.data.success) {
					this.result = res.data.data
				}
			} catch (error) {
				console.error('计算失败:', error)
				uni.showToast({ title: '计算失败', icon: 'none' })
			} finally {
				this.calculating = false
			}
		},

		async exportToManagement() {
			const selected = uni.getStorageSync('selectedProject')
			if (!selected || !selected.id) {
				uni.showToast({ title: '请先选择项目', icon: 'none' })
				return
			}

			try {
				// 将计算结果转换为经济指标格式
				const indexes = [
					{ name: '用地面积', value: this.params.landArea, unit: '㎡', calculated: false },
					{ name: '容积率', value: this.params.far, unit: '/', calculated: true },
					{ name: '建筑面积', value: this.result.totalArea, unit: '㎡', calculated: true },
					{ name: '住宅面积', value: this.result.breakdown.residential, unit: '㎡', calculated: false },
					{ name: '商业面积', value: this.result.breakdown.commercial, unit: '㎡', calculated: false },
					{ name: '停车面积', value: this.result.breakdown.parking, unit: '㎡', calculated: false }
				]

				await uni.request({
					url: `http://localhost:5002/api/projects/${selected.id}/indexes`,
					method: 'PUT',
					data: indexes
				})

				uni.showToast({ title: '已导入到管理台', icon: 'success' })
			} catch (error) {
				console.error('导入失败:', error)
				uni.showToast({ title: '导入失败', icon: 'none' })
			}
		}
	}
}
</script>

<style>
@import "../../static/css/common.css";

.calc-container {
	display: grid;
	grid-template-columns: 1fr 1fr;
	gap: 40rpx;
	padding: 40rpx;
	height: 100%;
}

.input-section, .result-section {
	background: #fafafa;
	border-radius: 16rpx;
	padding: 32rpx;
	display: flex;
	flex-direction: column;
	gap: 24rpx;
}

.section-title {
	font-size: 28rpx;
	font-weight: 600;
	color: #333;
	margin-bottom: 8rpx;
}

.form-group {
	display: flex;
	flex-direction: column;
	gap: 12rpx;
}

.form-label {
	font-size: 24rpx;
	color: #666;
}

.form-input {
	border: 1px solid #e0e0e0;
	border-radius: 12rpx;
	padding: 20rpx 24rpx;
	font-size: 24rpx;
	background: white;
}

.picker-input {
	border: 1px solid #e0e0e0;
	border-radius: 12rpx;
	padding: 20rpx 24rpx;
	font-size: 24rpx;
	background: white;
	display: flex;
	justify-content: space-between;
}

.picker-arrow {
	color: #999;
}

.btn-primary {
	margin-top: 16rpx;
	padding: 24rpx;
	background: #7cb342;
	color: white;
	border-radius: 12rpx;
	font-size: 26rpx;
	font-weight: 500;
	border: none;
}

.btn-secondary {
	padding: 20rpx;
	background: #f5f5f5;
	color: #666;
	border-radius: 12rpx;
	font-size: 24rpx;
	border: none;
	margin-top: 16rpx;
}

.empty-result {
	flex: 1;
	display: flex;
	align-items: center;
	justify-content: center;
	color: #999;
	font-size: 24rpx;
}

.result-content {
	display: flex;
	flex-direction: column;
	gap: 20rpx;
}

.result-item {
	display: flex;
	justify-content: space-between;
	padding: 20rpx;
	background: white;
	border-radius: 12rpx;
}

.result-label {
	font-size: 24rpx;
	color: #666;
}

.result-value {
	font-size: 26rpx;
	font-weight: 600;
	color: #333;
}

.recommendations {
	background: #e8f5e9;
	border-radius: 12rpx;
	padding: 20rpx;
	margin-top: 16rpx;
}

.recommendations-title {
	font-size: 24rpx;
	font-weight: 600;
	color: #2e7d32;
	margin-bottom: 12rpx;
	display: block;
}

.recommendation-item {
	font-size: 22rpx;
	color: #558b2f;
	line-height: 1.6;
	margin-bottom: 8rpx;
}
</style>
```

### 2.2 后端尺寸计算 API

在 `backend/app.py` 中添加：

```python
@app.route('/api/calculation/size', methods=['POST'])
def calculate_size():
    """计算建筑面积分配"""
    try:
        data = request.json
        land_area = data.get('landArea', 0)
        far = data.get('far', 0)
        building_type = data.get('buildingType', 'residential')
        max_height = data.get('maxHeight', 100)
        green_ratio = data.get('greenRatio', 0.3)

        # 计算总建筑面积
        total_area = land_area * far

        # 根据建筑类型分配面积
        if building_type == 'residential':
            residential = total_area * 0.8
            commercial = total_area * 0.15
            parking = total_area * 0.05
        elif building_type == 'commercial':
            residential = 0
            commercial = total_area * 0.9
            parking = total_area * 0.1
        elif building_type == 'office':
            residential = 0
            commercial = total_area * 0.85
            parking = total_area * 0.15
        else:  # mixed
            residential = total_area * 0.6
            commercial = total_area * 0.3
            parking = total_area * 0.1

        # 生成建议
        recommendations = []
        if residential > 0:
            recommendations.append(f"建议住宅面积 {int(residential)}㎡")
        if commercial > 0:
            recommendations.append(f"建议商业面积 {int(commercial)}㎡")
        if parking > 0:
            parking_spaces = int(parking / 32)  # 假设每个车位32㎡
            recommendations.append(f"地下停车位约 {parking_spaces} 个")

        result = {
            'totalArea': int(total_area),
            'breakdown': {
                'residential': int(residential),
                'commercial': int(commercial),
                'parking': int(parking)
            },
            'recommendations': recommendations
        }

        return jsonify({'success': True, 'data': result})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
```

### 2.3 图片生成导入到管理台

在 `image-gen.vue` 中添加"保存到项目"按钮：

在生成结果区域添加：

```vue
<button class="btn-save-to-project" @click="saveToProject">
	保存到项目效果图
</button>
```

添加方法：

```javascript
async saveToProject() {
	const selected = uni.getStorageSync('selectedProject')
	if (!selected || !selected.id) {
		uni.showToast({ title: '请先选择项目', icon: 'none' })
		return
	}

	if (!this.generatedImage) {
		uni.showToast({ title: '没有可保存的图片', icon: 'none' })
		return
	}

	try {
		// 将 base64 图片上传到项目
		const res = await uni.request({
			url: `http://localhost:5002/api/projects/${selected.id}/files/upload-base64`,
			method: 'POST',
			data: {
				name: `AI生成效果图_${Date.now()}`,
				type: 'JPG',
				category: 'rendering',
				base64: this.generatedImage,
				remark: '由AI图片生成工具生成'
			}
		})

		if (res.data.success) {
			uni.showToast({ title: '已保存到项目', icon: 'success' })
		}
	} catch (error) {
		console.error('保存失败:', error)
		uni.showToast({ title: '保存失败', icon: 'none' })
	}
}
```

后端添加 base64 上传接口：

```python
@app.route('/api/projects/<int:project_id>/files/upload-base64', methods=['POST'])
def upload_base64_file(project_id):
    """上传 base64 编码的文件"""
    try:
        data = request.json
        name = data.get('name', '')
        file_type = data.get('type', 'JPG')
        category = data.get('category', 'rendering')
        base64_data = data.get('base64', '')
        remark = data.get('remark', '')

        # 解码 base64
        import base64
        from datetime import datetime

        # 移除 data:image/xxx;base64, 前缀
        if ',' in base64_data:
            base64_data = base64_data.split(',')[1]

        file_data = base64.b64decode(base64_data)

        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{name}.{file_type.lower()}"

        # 获取存储配置
        storage_config = project_mgr.get_storage_config(project_id)

        # 保存文件
        if storage_config['type'] in ['local', 'nas']:
            save_path = os.path.join(storage_config['path'], category, filename)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(file_data)
            storage_path = save_path
        else:  # url
            temp_dir = os.path.join(BASE_DIR, 'temp', str(project_id), category)
            os.makedirs(temp_dir, exist_ok=True)
            save_path = os.path.join(temp_dir, filename)
            with open(save_path, 'wb') as f:
                f.write(file_data)
            storage_path = f"{storage_config['url']}/{category}/{filename}"

        # 添加文件记录
        file_record = {
            'name': name,
            'type': file_type,
            'category': category,
            'path': category,
            'storage_path': storage_path,
            'size': len(file_data),
            'remark': remark
        }

        result = project_mgr.add_file(project_id, file_record)
        return jsonify({'success': True, 'data': result})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
```

## 三、实施步骤

1. **后端 API**：
   - 在 `backend/app.py` 中添加文件上传、尺寸计算、base64上传接口
   - 测试 API 是否正常工作

2. **管理台文件上传**：
   - 按照 `MANAGEMENT_UPLOAD_PATCH.md` 修改 `management.vue`
   - 测试文件上传、分类过滤、删除功能

3. **尺寸计算工具**：
   - 创建 `size-calc.vue` 页面
   - 在 `pages.json` 中注册路由
   - 从工作台添加跳转链接

4. **图片生成导入**：
   - 修改 `image-gen.vue` 添加保存到项目功能
   - 测试生成图片后保存到管理台

5. **其他工具**：
   - PPT 生成、造价估算、图片搜索可以按照类似模式实现

## 四、注意事项

1. 文件上传需要配置存储路径，确保目录有写权限
2. 大文件上传可能需要调整 Flask 的 `MAX_CONTENT_LENGTH` 配置
3. 生产环境建议使用对象存储（如阿里云 OSS、腾讯云 COS）
4. 文件下载功能需要根据存储类型实现不同的逻辑
5. 建议添加文件类型和大小限制
