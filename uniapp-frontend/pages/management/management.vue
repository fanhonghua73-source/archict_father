<template>
	<view class="page-container">
		<view class="workspace-card">
			<view class="top-bar">
				<view class="user-avatar-header"><text>👤</text></view>
				<view class="top-bar-title">{{ projectName }}</view>
				<view class="top-bar-right">
					<view class="storage-btn" @click="openStorageModal">
						<text>📁 存储配置</text>
					</view>
					<view class="window-controls">
						<view class="control-btn">−</view>
						<view class="control-btn">□</view>
						<view class="control-btn">×</view>
					</view>
				</view>
			</view>

			<view class="main-body">
				<view class="sidebar">
					<view class="nav-items">
						<view class="nav-item" @click="switchTab('index')">项目</view>
						<view class="nav-item" @click="switchTab('resource')">资源</view>
						<view class="nav-item" @click="switchTab('workbench')">工作台</view>
						<view class="nav-item" @click="switchTab('entertainment')">娱乐室</view>
						<view class="nav-item active">管理台</view>
						<view class="nav-item" @click="switchTab('settings')">设置</view>
					</view>
					<view class="sidebar-footer">v1.0</view>
				</view>

				<view class="main-content">
					<view class="content-three-columns">
						<!-- 左列：文件夹层级 -->
						<view class="folder-hierarchy">
							<view class="project-name-header">{{ projectName }}</view>
							<view class="folder-dirs">
								<view class="dir-column">
									<view
										v-for="(dir, index) in primaryDirs"
										:key="index"
										:class="['dir-item', selectedPrimaryDir === dir.id ? 'active' : '']"
										@click="selectPrimaryDir(dir.id)"
									>
										{{ dir.name }}
									</view>
								</view>
								<view class="dir-column" v-if="secondaryDirs.length > 0">
									<view
										v-for="(dir, index) in secondaryDirs"
										:key="index"
										:class="['dir-item', selectedSecondaryDir === dir.id ? 'active' : '']"
										@click="selectSecondaryDir(dir.id)"
									>
										{{ dir.name }}
									</view>
								</view>
							</view>
						</view>

						<!-- 中列：文件表格 + 人员表格 -->
						<view class="middle-column">
							<!-- 文件表格 -->
							<scroll-view class="file-text-area" scroll-y>
								<view class="file-header">
									<view class="file-summary">
										<text class="bold">{{ getCurrentCategoryName() }}</text>
										（{{ filteredFiles.length }} 个文件）
									</view>
									<view class="upload-btn" @click="openUploadModal">
										<text>📤 上传</text>
									</view>
								</view>
								<view class="file-table">
									<view class="file-table-header">
										<text class="col-name">文件名</text>
										<text class="col-type">类型</text>
										<text class="col-date">日期</text>
										<text class="col-size">大小</text>
										<text class="col-action">操作</text>
									</view>
									<view class="file-table-body">
										<view v-for="(file, idx) in filteredFiles" :key="idx" class="file-row">
											<text class="col-name">{{ file.name }}</text>
											<text class="col-type">{{ file.type }}</text>
											<text class="col-date">{{ file.date || file.uploaded_at }}</text>
											<text class="col-size">{{ formatSize(file.size) }}</text>
											<view class="col-action">
												<text class="action-btn" @click="downloadFile(file)">下载</text>
												<text class="action-btn delete" @click="deleteFile(file)">删除</text>
											</view>
										</view>
										<view v-if="filteredFiles.length === 0" class="empty-state">
											<text>暂无文件，点击上传按钮添加</text>
										</view>
									</view>
								</view>
							</scroll-view>

							<!-- 人员表格 -->
							<view class="staff-table-section">
								<view class="staff-grid-container">
									<view
										v-for="(staff, index) in staffList"
										:key="index"
										:class="['staff-cell', staff.active ? 'active' : '']"
										@click="toggleStaff(index)"
									>
										<view class="staff-cell-top">
											<text class="staff-name">{{ staff.name }}</text>
											<text class="staff-edit-btn" @click.stop="editStaff(index)">✎</text>
										</view>
										<view class="busy-bar">
											<view class="busy-fill" :style="{ width: staff.busy + '%' }"></view>
										</view>
									</view>
								</view>
							</view>
						</view>

						<!-- 右列：人员时间规划 + 经济技术指标 -->
						<view class="right-column">
							<!-- 人员时间规划 -->
							<view class="time-planning-section">
								<view class="section-title">人员时间规划</view>
								<scroll-view class="planning-list" scroll-y>
									<view v-for="(staff, index) in activeStaffList" :key="index" class="planning-item">
										<view class="planning-header">
											<text class="planning-name">{{ staff.name }}</text>
											<text class="planning-role">{{ staff.role || '未设置角色' }}</text>
										</view>
										<view v-if="staff.schedule" class="planning-schedule">
											<text>{{ staff.schedule }}</text>
										</view>
										<view v-else class="planning-empty">
											<text>暂无时间安排</text>
										</view>
									</view>
									<view v-if="activeStaffList.length === 0" class="empty-state-small">
										<text>暂无激活人员</text>
									</view>
								</scroll-view>
							</view>

							<!-- 经济技术指标 -->
							<scroll-view class="economic-index" scroll-y>
								<view class="section-title">经济技术指标</view>
								<view class="index-list">
									<view
										v-for="(item, index) in economicIndexes"
										:key="index"
										:class="['index-item', item.calculated ? 'calculated' : '']"
										@click="editIndex(index)"
									>
										<text class="index-name">{{ item.name }}{{ item.calculated ? ' *' : '' }}</text>
										<view class="index-value-group">
											<text class="index-value">{{ item.value }}</text>
											<text class="index-unit">{{ item.unit }}</text>
										</view>
									</view>
								</view>
							</scroll-view>
						</view>
					</view>

					<!-- 底部搜索框 -->
					<view class="bottom-fixed-area">
						<view class="divider"></view>
						<view class="search-container">
							<view :class="['search-box', searchFocused ? 'focused' : '']">
								<input class="search-input" placeholder="搜索文件..." v-model="searchText" @focus="searchFocused = true" @blur="searchFocused = false" />
								<view v-if="searchFocused" class="submit-btn"><text>→</text></view>
							</view>
						</view>
					</view>
				</view>
			</view>
		</view>

		<!-- 文件上传弹窗 -->
		<view v-if="showUploadModal" class="modal-overlay">
			<view class="modal-content">
				<view class="modal-header">
					<text class="modal-title">上传文件 — {{ getCurrentCategoryName() }}</text>
					<text class="modal-close" @click="closeUploadModal">×</text>
				</view>
				<view class="modal-body">
					<view class="form-group">
						<text class="form-label">文件名称</text>
						<input class="form-input" v-model="uploadForm.name" placeholder="如：红线图 v2" />
					</view>
					<view class="form-group">
						<text class="form-label">文件类型</text>
						<picker mode="selector" :range="fileTypes" :value="uploadForm.typeIndex" @change="onFileTypeChange">
							<view class="picker-input">
								<text>{{ fileTypes[uploadForm.typeIndex] }}</text>
								<text class="picker-arrow">▼</text>
							</view>
						</picker>
						<view class="picker-hint">或手动输入：</view>
						<input class="form-input" v-model="uploadForm.type" placeholder="如：DWG、PDF、JPG" />
					</view>
					<view class="form-group">
						<text class="form-label">选择文件</text>
						<view class="upload-area" @click="chooseFile">
							<view v-if="!uploadForm.filePath" class="upload-placeholder">
								<text class="upload-icon">📂</text>
								<text class="upload-hint">点击选择文件</text>
								<text class="upload-hint-sub">支持 DWG、PDF、SKP、JPG、PNG 等格式</text>
							</view>
							<view v-else class="upload-selected">
								<text class="upload-icon">✅</text>
								<text class="upload-filename">{{ uploadForm.fileName }}</text>
								<text class="upload-filesize">{{ uploadForm.fileSize }}</text>
							</view>
						</view>
					</view>
					<view class="form-group">
						<text class="form-label">备注（可选）</text>
						<input class="form-input" v-model="uploadForm.remark" placeholder="备注信息" />
					</view>
					<view class="form-actions">
						<button class="btn-secondary" @click="closeUploadModal">取消</button>
						<button class="btn-primary" @click="submitUpload" :disabled="uploading">
							{{ uploading ? '上传中...' : '确认上传' }}
						</button>
					</view>
				</view>
			</view>
		</view>

		<!-- 人员编辑弹窗 -->
		<view v-if="showStaffModal" class="modal-overlay">
			<view class="modal-content">
				<view class="modal-header">
					<text class="modal-title">编辑人员信息</text>
					<text class="modal-close" @click="closeStaffModal">×</text>
				</view>
				<view class="modal-body">
					<view class="form-group">
						<text class="form-label">姓名</text>
						<input class="form-input" v-model="editingStaff.name" placeholder="请输入姓名" />
					</view>
					<view class="form-group">
						<text class="form-label">忙碌度：{{ editingStaff.busy }}%</text>
						<slider class="busy-slider" :value="editingStaff.busy" @change="onBusyChange" min="0" max="100" step="5" activeColor="#7cb342" />
					</view>
					<view class="form-group">
						<text class="form-label">角色</text>
						<input class="form-input" v-model="editingStaff.role" placeholder="如：主创建筑师" />
					</view>
					<view class="form-group">
						<text class="form-label">时间安排</text>
						<textarea class="form-textarea" v-model="editingStaff.schedule" placeholder="如：&#10;2026-03-01 至 2026-03-15: 方案设计&#10;2026-03-16 至 2026-03-31: 施工图绘制" />
					</view>
					<view class="form-actions">
						<button class="btn-secondary" @click="closeStaffModal">取消</button>
						<button class="btn-primary" @click="saveStaff">保存</button>
					</view>
				</view>
			</view>
		</view>

		<!-- 存储配置弹窗 -->
		<view v-if="showStorageModal" class="modal-overlay">
			<view class="modal-content">
				<view class="modal-header">
					<text class="modal-title">文件存储配置</text>
					<text class="modal-close" @click="closeStorageModal">×</text>
				</view>
				<view class="modal-body">
					<view class="form-group">
						<text class="form-label">存储类型</text>
						<picker mode="selector" :range="storageTypes" :value="storageTypeIndex" @change="onStorageTypeChange">
							<view class="picker-input">
								<text>{{ storageTypes[storageTypeIndex] }}</text>
								<text class="picker-arrow">▼</text>
							</view>
						</picker>
					</view>
					<view class="form-group" v-if="storageConfig.type === 'local'">
						<text class="form-label">本地路径</text>
						<input class="form-input" v-model="storageConfig.path" placeholder="/Users/xxx/projects/wenzhou" />
					</view>
					<view class="form-group" v-if="storageConfig.type === 'nas'">
						<text class="form-label">NAS 路径</text>
						<input class="form-input" v-model="storageConfig.path" placeholder="/mnt/nas/projects/wenzhou" />
					</view>
					<view class="form-group" v-if="storageConfig.type === 'url'">
						<text class="form-label">网络地址</text>
						<input class="form-input" v-model="storageConfig.url" placeholder="https://files.example.com/projects/wenzhou" />
					</view>
					<view class="storage-hint">
						<text>💡 提示：</text>
						<text v-if="storageConfig.type === 'local'">本地存储：文件保存在本机硬盘</text>
						<text v-if="storageConfig.type === 'nas'">NAS存储：文件保存在网络存储设备</text>
						<text v-if="storageConfig.type === 'url'">网络地址：文件通过URL访问</text>
					</view>
					<view class="form-actions">
						<button class="btn-secondary" @click="closeStorageModal">取消</button>
						<button class="btn-primary" @click="saveStorageConfig">保存</button>
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
				projectId: 1,
				projectName: '温州中心项目',
				selectedPrimaryDir: 'original',
				selectedSecondaryDir: '',
				currentCategory: 'original',

				// 弹窗控制
				showStaffModal: false,
				showStorageModal: false,
				showUploadModal: false,
				uploading: false,

				// 文件上传表单
				uploadForm: {
					name: '',
					typeIndex: 0,
					type: 'DWG',
					filePath: '',
					fileName: '',
					fileSize: '',
					remark: ''
				},
				fileTypes: ['DWG', 'PDF', 'SKP', 'JPG', 'PNG', 'DOC', 'XLS'],

				// 编辑中的人员
				editingStaff: { id: null, name: '', busy: 50, active: false, role: '', schedule: '' },
				editingStaffIndex: -1,

				// 存储配置
				storageConfig: { type: 'local', path: '', url: '' },
				storageTypes: ['本地存储', 'NAS存储', '网络地址'],
				storageTypeIndex: 0,

				primaryDirs: [
					{ id: 'original', name: '原始资料' },
					{ id: 'management', name: '项目管理' },
					{ id: 'stage', name: '阶段文件' },
					{ id: 'special', name: '专项设计' },
					{ id: 'work', name: '工作文件' },
					{ id: 'rendering', name: '效果图' }
				],
				secondaryDirs: [],

				files: [
				// 原始资料 - 红线图
				{ id: 1, name: '红线图 v1', type: 'DWG', category: 'original/redline', path: 'original/redline', size: 2457600, date: '2026-02-20' },
				{ id: 2, name: '红线图 v2', type: 'DWG', category: 'original/redline', path: 'original/redline', size: 2512000, date: '2026-02-25' },
				{ id: 3, name: '红线图', type: 'PDF', category: 'original/redline', path: 'original/redline', size: 8495104, date: '2026-02-25' },
				// 原始资料 - 测绘图
				{ id: 4, name: '地形测绘图', type: 'DWG', category: 'original/survey', path: 'original/survey', size: 5242880, date: '2026-02-18' },
				{ id: 5, name: '现状建筑测绘', type: 'DWG', category: 'original/survey', path: 'original/survey', size: 3145728, date: '2026-02-18' },
				// 原始资料 - 地质报告
				{ id: 6, name: '岩土工程勘察报告', type: 'PDF', category: 'original/geology', path: 'original/geology', size: 15728640, date: '2026-02-10' },
				// 项目管理 - 合同
				{ id: 7, name: '设计合同', type: 'PDF', category: 'management/contract', path: 'management/contract', size: 2097152, date: '2026-01-15' },
				{ id: 8, name: '补充协议', type: 'PDF', category: 'management/contract', path: 'management/contract', size: 1048576, date: '2026-02-01' },
				// 项目管理 - 会议纪要
				{ id: 9, name: '启动会议纪要', type: 'DOC', category: 'management/meeting', path: 'management/meeting', size: 524288, date: '2026-01-20' },
				{ id: 10, name: '方案评审会议纪要', type: 'DOC', category: 'management/meeting', path: 'management/meeting', size: 614400, date: '2026-02-28' },
				// 项目管理 - 进度计划
				{ id: 11, name: '总体进度计划', type: 'XLS', category: 'management/schedule', path: 'management/schedule', size: 409600, date: '2026-01-25' },
				// 阶段文件 - 方案设计
				{ id: 12, name: '总平面图', type: 'DWG', category: 'stage/concept', path: 'stage/concept', size: 3355443, date: '2026-02-28' },
				{ id: 13, name: '总平面图', type: 'PDF', category: 'stage/concept', path: 'stage/concept', size: 13107200, date: '2026-02-28' },
				{ id: 14, name: '1号楼平面图', type: 'DWG', category: 'stage/concept', path: 'stage/concept', size: 2621440, date: '2026-02-28' },
				{ id: 15, name: '1号楼立面图', type: 'DWG', category: 'stage/concept', path: 'stage/concept', size: 1887436, date: '2026-02-28' },
				{ id: 16, name: '1号楼剖面图', type: 'DWG', category: 'stage/concept', path: 'stage/concept', size: 1572864, date: '2026-02-28' },
				// 阶段文件 - 初步设计
				{ id: 17, name: '初步设计说明', type: 'DOC', category: 'stage/preliminary', path: 'stage/preliminary', size: 1048576, date: '2026-03-01' },
				// 效果图
				{ id: 18, name: '鸟瞰图 01', type: 'JPG', category: 'rendering', path: 'rendering', size: 6082560, date: '2026-02-26' },
				{ id: 19, name: '鸟瞰图 02', type: 'JPG', category: 'rendering', path: 'rendering', size: 6502400, date: '2026-02-26' },
				{ id: 20, name: '沿街透视图', type: 'JPG', category: 'rendering', path: 'rendering', size: 5767168, date: '2026-02-27' },
				{ id: 21, name: '入口透视图', type: 'JPG', category: 'rendering', path: 'rendering', size: 5242880, date: '2026-02-27' },
				{ id: 22, name: '庭院透视图', type: 'JPG', category: 'rendering', path: 'rendering', size: 4718592, date: '2026-02-27' },
				{ id: 23, name: 'AI生成效果图_01', type: 'PNG', category: 'rendering', path: 'rendering', size: 3932160, date: '2026-03-01' },
				// 工作文件
				{ id: 24, name: '草图方案A', type: 'SKP', category: 'work', path: 'work', size: 15728640, date: '2026-02-15' },
				{ id: 25, name: '草图方案B', type: 'SKP', category: 'work', path: 'work', size: 16777216, date: '2026-02-16' },
				{ id: 26, name: '分析图', type: 'SKP', category: 'work', path: 'work', size: 12582912, date: '2026-02-20' },
				// 专项设计
				{ id: 27, name: '结构方案', type: 'PDF', category: 'special', path: 'special', size: 5242880, date: '2026-02-25' },
				{ id: 28, name: '景观方案', type: 'PDF', category: 'special', path: 'special', size: 10485760, date: '2026-02-26' }
			],
				staffList: [
				{ id: 1, name: '张三', busy: 75, active: true, role: '主创建筑师', schedule: '2026-03-01 至 2026-03-15: 方案设计\n2026-03-16 至 2026-03-31: 施工图绘制' },
				{ id: 2, name: '李四', busy: 50, active: false, role: '结构工程师', schedule: '' },
				{ id: 3, name: '王五', busy: 80, active: true, role: '项目经理', schedule: '2026-03-01 至 2026-04-30: 项目管理' },
				{ id: 4, name: '赵六', busy: 20, active: false, role: '', schedule: '' },
				{ id: 5, name: '钱七', busy: 60, active: true, role: '建筑师', schedule: '2026-03-10 至 2026-03-25: 立面设计' },
				{ id: 6, name: '孙八', busy: 40, active: false, role: '', schedule: '' },
				{ id: 7, name: '周九', busy: 90, active: false, role: '', schedule: '' },
				{ id: 8, name: '吴十', busy: 30, active: true, role: '助理建筑师', schedule: '2026-03-01 至 2026-03-31: 图纸绘制' },
				{ id: 9, name: '郑一', busy: 55, active: false, role: '', schedule: '' },
				{ id: 10, name: '冯二', busy: 65, active: true, role: '机电工程师', schedule: '2026-03-15 至 2026-04-15: 机电设计' },
				{ id: 11, name: '陈三', busy: 45, active: false, role: '', schedule: '' },
				{ id: 12, name: '褚四', busy: 35, active: false, role: '', schedule: '' },
				{ id: 13, name: '卫五', busy: 70, active: true, role: '景观设计师', schedule: '2026-03-20 至 2026-04-10: 景观方案' },
				{ id: 14, name: '蒋六', busy: 25, active: false, role: '', schedule: '' },
				{ id: 15, name: '沈七', busy: 85, active: false, role: '', schedule: '' },
				{ id: 16, name: '韩八', busy: 95, active: true, role: '总建筑师', schedule: '2026-03-01 至 2026-05-31: 全程把控' },
				{ id: 17, name: '杨九', busy: 15, active: false, role: '', schedule: '' },
				{ id: 18, name: '朱十', busy: 42, active: false, role: '', schedule: '' },
				{ id: 19, name: '秦十一', busy: 58, active: true, role: '室内设计师', schedule: '2026-04-01 至 2026-04-30: 室内方案' },
				{ id: 20, name: '尤十二', busy: 33, active: false, role: '', schedule: '' },
				{ id: 21, name: '许十三', busy: 67, active: false, role: '', schedule: '' },
				{ id: 22, name: '何十四', busy: 72, active: true, role: '造价工程师', schedule: '2026-03-01 至 2026-03-20: 造价估算' },
				{ id: 23, name: '吕十五', busy: 28, active: false, role: '', schedule: '' },
				{ id: 24, name: '施十六', busy: 52, active: false, role: '', schedule: '' }
			],
				economicIndexes: []
			}
		},
		computed: {
			filteredFiles() {
				let list = this.files
				// 按当前分类过滤
				if (this.currentCategory) {
					list = list.filter(f => {
						const cat = f.category || f.path || ''
						return cat === this.currentCategory || cat.startsWith(this.currentCategory + '/')
					})
				}
				// 按搜索词过滤
				if (this.searchText) {
					const q = this.searchText.toLowerCase()
					list = list.filter(f => f.name.toLowerCase().includes(q))
				}
				return list
			},
			activeStaffList() {
				return this.staffList.filter(s => s.active)
			}
		},
		mounted() {
			const selected = uni.getStorageSync('selectedProject')
			if (selected && selected.id) {
				this.projectId = selected.id
				this.projectName = selected.name
			}
		},
		onShow() {
			const selected = uni.getStorageSync('selectedProject')
			if (selected && selected.id) {
				this.projectId = selected.id
				this.projectName = selected.name
			}
			this.loadStorageConfig()
			this.loadFiles()
			this.loadStaff()
			this.loadIndexes()
		},
		methods: {
			switchTab(page) {
				uni.switchTab({ url: '/pages/' + page + '/' + page })
			},

			// ==================== 数据加载 ====================

			async loadStorageConfig() {
				try {
					const res = await uni.request({ url: `http://localhost:5002/api/projects/${this.projectId}/storage`, method: 'GET' })
					if (res.data.success) {
						this.storageConfig = res.data.data
						const typeMap = { 'local': 0, 'nas': 1, 'url': 2 }
						this.storageTypeIndex = typeMap[this.storageConfig.type] || 0
					}
				} catch (e) { console.error('加载存储配置失败:', e) }
			},

			async loadFiles() {
				try {
					const res = await uni.request({ url: `http://localhost:5002/api/projects/${this.projectId}/files`, method: 'GET' })
					if (res.data.success) this.files = res.data.data
				} catch (e) { console.error('加载文件失败:', e) }
			},

			async loadStaff() {
				try {
					const res = await uni.request({ url: `http://localhost:5002/api/projects/${this.projectId}/staff`, method: 'GET' })
					if (res.data.success) this.staffList = res.data.data
				} catch (e) { console.error('加载人员失败:', e) }
			},

			async loadIndexes() {
				try {
					const res = await uni.request({ url: `http://localhost:5002/api/projects/${this.projectId}/indexes`, method: 'GET' })
					if (res.data.success) this.economicIndexes = res.data.data
				} catch (e) { console.error('加载指标失败:', e) }
			},

			// ==================== 文件夹导航 ====================

			getCurrentCategoryName() {
				const map = {
					'original': '原始资料', 'original/redline': '红线图', 'original/survey': '测绘图',
					'original/geology': '地质报告', 'management': '项目管理', 'management/contract': '合同',
					'management/meeting': '会议纪要', 'management/schedule': '进度计划',
					'stage': '阶段文件', 'stage/concept': '方案设计', 'stage/preliminary': '初步设计',
					'stage/construction': '施工图', 'special': '专项设计', 'work': '工作文件', 'rendering': '效果图'
				}
				return map[this.currentCategory] || '全部文件'
			},

			selectPrimaryDir(id) {
				this.selectedPrimaryDir = id
				this.currentCategory = id
				const secondaryMap = {
					original: [{ id: 'redline', name: '红线图' }, { id: 'survey', name: '测绘图' }, { id: 'geology', name: '地质报告' }],
					management: [{ id: 'contract', name: '合同' }, { id: 'meeting', name: '会议纪要' }, { id: 'schedule', name: '进度计划' }],
					stage: [{ id: 'concept', name: '方案设计' }, { id: 'preliminary', name: '初步设计' }, { id: 'construction', name: '施工图' }]
				}
				this.secondaryDirs = secondaryMap[id] || []
				this.selectedSecondaryDir = ''
			},

			selectSecondaryDir(id) {
				this.selectedSecondaryDir = id
				this.currentCategory = this.selectedPrimaryDir + '/' + id
			},

			// ==================== 文件上传 ====================

			openUploadModal() {
				this.uploadForm = { name: '', typeIndex: 0, type: 'DWG', filePath: '', fileName: '', fileSize: '', remark: '' }
				this.showUploadModal = true
			},

			closeUploadModal() {
				this.showUploadModal = false
			},

			onFileTypeChange(e) {
				this.uploadForm.typeIndex = e.detail.value
				this.uploadForm.type = this.fileTypes[e.detail.value]
			},

			chooseFile() {
				uni.chooseFile({
					count: 1,
					success: (res) => {
						const file = res.tempFiles[0]
						this.uploadForm.filePath = file.path
						this.uploadForm.fileName = file.name
						this.uploadForm.fileSize = this.formatSize(file.size)
						if (!this.uploadForm.name) {
							this.uploadForm.name = file.name.replace(/\.[^/.]+$/, '')
						}
						const ext = file.name.split('.').pop().toUpperCase()
						const idx = this.fileTypes.indexOf(ext)
						if (idx !== -1) { this.uploadForm.typeIndex = idx; this.uploadForm.type = ext }
					},
					fail: () => uni.showToast({ title: '选择文件失败', icon: 'none' })
				})
			},

			formatSize(bytes) {
				if (!bytes) return '-'
				if (typeof bytes === 'string') return bytes
				if (bytes < 1024) return bytes + ' B'
				if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
				return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
			},

			async submitUpload() {
				if (!this.uploadForm.name) { uni.showToast({ title: '请输入文件名称', icon: 'none' }); return }
				if (!this.uploadForm.filePath) { uni.showToast({ title: '请选择文件', icon: 'none' }); return }
				this.uploading = true
				try {
					const uploadRes = await uni.uploadFile({
						url: `http://localhost:5002/api/projects/${this.projectId}/files/upload`,
						filePath: this.uploadForm.filePath,
						name: 'file',
						formData: {
							name: this.uploadForm.name,
							type: this.uploadForm.type,
							category: this.currentCategory,
							remark: this.uploadForm.remark
						}
					})
					const result = JSON.parse(uploadRes[1] ? uploadRes[1].data : uploadRes.data)
					if (result.success) {
						uni.showToast({ title: '上传成功', icon: 'success' })
						this.closeUploadModal()
						await this.loadFiles()
					} else {
						throw new Error(result.error || '上传失败')
					}
				} catch (e) {
					console.error('上传失败:', e)
					uni.showToast({ title: '上传失败', icon: 'none' })
				} finally {
					this.uploading = false
				}
			},

			downloadFile(file) {
				uni.showToast({ title: '开始下载...', icon: 'loading' })
			},

			async deleteFile(file) {
				uni.showModal({
					title: '确认删除',
					content: `确定要删除"${file.name}"吗？`,
					success: async (res) => {
						if (res.confirm) {
							try {
								await uni.request({ url: `http://localhost:5002/api/projects/${this.projectId}/files/${file.id}`, method: 'DELETE' })
								uni.showToast({ title: '删除成功', icon: 'success' })
								await this.loadFiles()
							} catch (e) {
								uni.showToast({ title: '删除失败', icon: 'none' })
							}
						}
					}
				})
			},

			// ==================== 人员管理 ====================

			toggleStaff(index) {
				this.staffList[index].active = !this.staffList[index].active
				this.saveStaffToBackend()
			},

			editStaff(index) {
				this.editingStaffIndex = index
				const s = this.staffList[index]
				this.editingStaff = { id: s.id, name: s.name, busy: s.busy, active: s.active, role: s.role || '', schedule: s.schedule || '' }
				this.showStaffModal = true
			},

			onBusyChange(e) { this.editingStaff.busy = e.detail.value },

			closeStaffModal() { this.showStaffModal = false },

			async saveStaff() {
				if (!this.editingStaff.name) { uni.showToast({ title: '请输入姓名', icon: 'none' }); return }
				this.staffList[this.editingStaffIndex] = { ...this.staffList[this.editingStaffIndex], ...this.editingStaff }
				await this.saveStaffToBackend()
				uni.showToast({ title: '保存成功', icon: 'success' })
				this.closeStaffModal()
			},

			async saveStaffToBackend() {
				try {
					await uni.request({ url: `http://localhost:5002/api/projects/${this.projectId}/staff`, method: 'PUT', data: this.staffList })
				} catch (e) {
					console.error('保存人员失败:', e)
				}
			},

			// ==================== 存储配置 ====================

			openStorageModal() { this.showStorageModal = true },
			closeStorageModal() { this.showStorageModal = false },

			onStorageTypeChange(e) {
				this.storageTypeIndex = e.detail.value
				this.storageConfig.type = ['local', 'nas', 'url'][this.storageTypeIndex]
			},

			async saveStorageConfig() {
				try {
					const res = await uni.request({ url: `http://localhost:5002/api/projects/${this.projectId}/storage`, method: 'PUT', data: this.storageConfig })
					if (res.data.success) { uni.showToast({ title: '保存成功', icon: 'success' }); this.closeStorageModal() }
				} catch (e) {
					uni.showToast({ title: '保存失败', icon: 'none' })
				}
			},

			// ==================== 经济指标 ====================

			editIndex(index) {
				const item = this.economicIndexes[index]
				if (item.calculated) { uni.showToast({ title: '此项为计算值，不可编辑', icon: 'none' }); return }
				uni.showModal({
					title: '编辑 ' + item.name,
					editable: true,
					placeholderText: item.value.toString(),
					success: async (res) => {
						if (res.confirm && res.content) {
							const v = parseFloat(res.content)
							if (!isNaN(v)) {
								this.economicIndexes[index].value = v
								this.calculateIndexes()
								await this.saveIndexes()
							}
						}
					}
				})
			},

			calculateIndexes() {
				const landArea = this.economicIndexes[0]?.value || 0
				const highRise = this.economicIndexes[5]?.value || 0
				const lowRise = this.economicIndexes[6]?.value || 0
				const commercial = this.economicIndexes[7]?.value || 0
				if (this.economicIndexes[4]) this.economicIndexes[4].value = highRise + lowRise + commercial
				if (this.economicIndexes[1] && landArea > 0) {
					this.economicIndexes[1].value = parseFloat(((highRise + lowRise + commercial) / landArea).toFixed(2))
				}
			},

			async saveIndexes() {
				try {
					await uni.request({ url: `http://localhost:5002/api/projects/${this.projectId}/indexes`, method: 'PUT', data: this.economicIndexes })
					uni.showToast({ title: '保存成功', icon: 'success' })
				} catch (e) {
					uni.showToast({ title: '保存失败', icon: 'none' })
				}
			}
		}
	}
</script>

<style>
@import "../../static/css/common.css";

.content-three-columns { display: grid; grid-template-columns: 200rpx 1fr 280rpx; gap: 32rpx; padding: 32rpx; flex: 1; min-height: 0; }
.folder-hierarchy { display: flex; flex-direction: column; border-right: 1px solid #f0f0f0; padding-right: 24rpx; }
.project-name-header { font-size: 28rpx; font-weight: 600; color: #333; margin-bottom: 24rpx; padding-bottom: 16rpx; border-bottom: 2px solid #7cb342; }
.folder-dirs { display: flex; gap: 16rpx; flex: 1; }
.dir-column { flex: 1; display: flex; flex-direction: column; gap: 8rpx; }
.dir-item { padding: 16rpx 12rpx; font-size: 22rpx; color: #666; background: #fafafa; border-radius: 8rpx; cursor: pointer; transition: all 0.2s; }
.dir-item.active { background: #7cb342; color: white; font-weight: 500; }
.dir-item:hover { background: #f0f0f0; }
.dir-item.active:hover { background: #6fa035; }
.middle-column { display: flex; flex-direction: column; gap: 24rpx; min-height: 0; }
.file-text-area { flex: 1; background: #fafafa; border-radius: 12rpx; padding: 24rpx; overflow-y: auto; }
.file-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16rpx; }
.file-summary { font-size: 22rpx; color: #666; }
.file-summary .bold { font-weight: 600; color: #333; }
.upload-btn { padding: 12rpx 24rpx; background: #7cb342; color: white; border-radius: 12rpx; font-size: 22rpx; cursor: pointer; transition: background 0.2s; }
.upload-btn:hover { background: #6fa035; }
.file-table { width: 100%; }
.file-table-header { display: grid; grid-template-columns: 2fr 1fr 1.5fr 1fr 1.2fr; padding: 12rpx 0; border-bottom: 2px solid #e0e0e0; font-size: 22rpx; font-weight: 600; color: #666; }
.file-table-body { display: flex; flex-direction: column; }
.file-row { display: grid; grid-template-columns: 2fr 1fr 1.5fr 1fr 1.2fr; padding: 16rpx 0; border-bottom: 1px solid #f0f0f0; font-size: 22rpx; color: #333; }
.col-name { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.col-type { color: #7cb342; font-weight: 500; }
.col-date { color: #999; }
.col-size { color: #666; }
.col-action { display: flex; gap: 12rpx; justify-content: flex-end; }
.action-btn { font-size: 20rpx; color: #7cb342; cursor: pointer; padding: 4rpx 8rpx; }
.action-btn:hover { text-decoration: underline; }
.action-btn.delete { color: #f44336; }
.empty-state { padding: 60rpx 0; text-align: center; color: #999; font-size: 22rpx; }
.staff-table-section { height: 280rpx; background: #fafafa; border-radius: 12rpx; padding: 24rpx; }
.staff-grid-container { display: grid; grid-template-columns: repeat(6, 1fr); grid-template-rows: repeat(4, 1fr); gap: 12rpx; height: 100%; }
.staff-cell { background: white; border: 1px solid #e0e0e0; border-radius: 8rpx; padding: 8rpx; display: flex; flex-direction: column; justify-content: space-between; cursor: pointer; transition: all 0.2s; }
.staff-cell.active { border-color: #7cb342; background: #f1f8e9; }
.staff-cell:hover { border-color: #7cb342; }
.staff-cell-top { display: flex; justify-content: space-between; align-items: center; }
.staff-name { font-size: 20rpx; color: #333; font-weight: 500; }
.staff-edit-btn { font-size: 18rpx; color: #bbb; padding: 2rpx 4rpx; cursor: pointer; transition: color 0.2s; }
.staff-edit-btn:hover { color: #7cb342; }
.busy-bar { height: 8rpx; background: #e0e0e0; border-radius: 4rpx; overflow: hidden; margin-top: 4rpx; }
.busy-fill { height: 100%; background: #7cb342; transition: width 0.3s; }
.economic-index { background: #fafafa; border-radius: 12rpx; padding: 24rpx; overflow-y: auto; }
.section-title { font-size: 26rpx; font-weight: 600; color: #333; margin-bottom: 20rpx; padding-bottom: 12rpx; border-bottom: 2px solid #7cb342; }
.index-list { display: flex; flex-direction: column; gap: 12rpx; }
.index-item { display: flex; justify-content: space-between; align-items: center; padding: 16rpx 12rpx; background: white; border-radius: 8rpx; border: 1px solid #e0e0e0; cursor: pointer; transition: all 0.2s; }
.index-item:hover { border-color: #7cb342; }
.index-item.calculated { background: #f1f8e9; }
.index-name { font-size: 22rpx; color: #666; }
.index-value-group { display: flex; align-items: baseline; gap: 4rpx; }
.index-value { font-size: 24rpx; font-weight: 600; color: #333; }
.index-unit { font-size: 20rpx; color: #999; }
.top-bar-title { font-size: 26rpx; font-weight: 600; color: #333; }
.top-bar-right { display: flex; align-items: center; gap: 24rpx; }
.storage-btn { padding: 12rpx 24rpx; background: #f5f5f5; border-radius: 12rpx; font-size: 22rpx; color: #666; cursor: pointer; transition: all 0.2s; }
.storage-btn:hover { background: #e8f5e9; color: #7cb342; }
.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0, 0, 0, 0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal-content { background: white; border-radius: 24rpx; width: 640rpx; max-height: 80vh; overflow-y: auto; box-shadow: 0 40rpx 120rpx rgba(0, 0, 0, 0.3); }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 32rpx 40rpx; border-bottom: 1px solid #f0f0f0; }
.modal-title { font-size: 28rpx; font-weight: 600; color: #333; }
.modal-close { font-size: 40rpx; color: #999; cursor: pointer; line-height: 1; padding: 0 8rpx; }
.modal-close:hover { color: #333; }
.modal-body { padding: 32rpx 40rpx; display: flex; flex-direction: column; gap: 24rpx; }
.form-group { display: flex; flex-direction: column; gap: 12rpx; }
.form-label { font-size: 24rpx; color: #666; font-weight: 500; }
.form-input { border: 1px solid #e0e0e0; border-radius: 12rpx; padding: 20rpx 24rpx; font-size: 24rpx; color: #333; background: #fafafa; transition: border-color 0.2s; }
.form-input:focus { border-color: #7cb342; background: white; }
.form-textarea { border: 1px solid #e0e0e0; border-radius: 12rpx; padding: 20rpx 24rpx; font-size: 24rpx; color: #333; background: #fafafa; height: 200rpx; width: 100%; box-sizing: border-box; }
.busy-slider { width: 100%; }
.form-actions { display: flex; gap: 16rpx; justify-content: flex-end; margin-top: 8rpx; }
.btn-primary { padding: 20rpx 48rpx; background: #7cb342; color: white; border-radius: 12rpx; font-size: 24rpx; font-weight: 500; border: none; cursor: pointer; }
.btn-primary:hover { background: #6fa035; }
.btn-secondary { padding: 20rpx 48rpx; background: #f5f5f5; color: #666; border-radius: 12rpx; font-size: 24rpx; border: none; cursor: pointer; }
.btn-secondary:hover { background: #e0e0e0; }
.storage-hint { background: #f1f8e9; border-radius: 12rpx; padding: 20rpx 24rpx; font-size: 22rpx; color: #558b2f; display: flex; flex-direction: column; gap: 8rpx; }
.picker-input { border: 1px solid #e0e0e0; border-radius: 12rpx; padding: 20rpx 24rpx; font-size: 24rpx; color: #333; background: #fafafa; display: flex; justify-content: space-between; align-items: center; }
.picker-arrow { font-size: 20rpx; color: #999; }
.upload-area { border: 2px dashed #e0e0e0; border-radius: 12rpx; padding: 40rpx; text-align: center; cursor: pointer; transition: all 0.2s; }
.upload-area:hover { border-color: #7cb342; background: #f1f8e9; }
.upload-placeholder { display: flex; flex-direction: column; align-items: center; gap: 12rpx; }
.upload-icon { font-size: 60rpx; }
.upload-hint { font-size: 24rpx; color: #666; }
.upload-hint-sub { font-size: 20rpx; color: #999; }
.upload-selected { display: flex; flex-direction: column; align-items: center; gap: 8rpx; }
.upload-filename { font-size: 22rpx; color: #333; font-weight: 500; }
.upload-filesize { font-size: 20rpx; color: #999; }

/* 右列布局 */
.right-column { display: flex; flex-direction: column; gap: 24rpx; min-height: 0; }

/* 人员时间规划 */
.time-planning-section { background: #fafafa; border-radius: 12rpx; padding: 24rpx; flex: 1; min-height: 0; display: flex; flex-direction: column; }
.planning-list { flex: 1; overflow-y: auto; }
.planning-item { background: white; border-radius: 8rpx; padding: 16rpx; margin-bottom: 12rpx; border: 1px solid #e0e0e0; }
.planning-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8rpx; }
.planning-name { font-size: 22rpx; font-weight: 600; color: #333; }
.planning-role { font-size: 20rpx; color: #7cb342; background: #f1f8e9; padding: 4rpx 12rpx; border-radius: 8rpx; }
.planning-schedule { font-size: 20rpx; color: #666; line-height: 1.6; white-space: pre-wrap; }
.planning-empty { font-size: 20rpx; color: #999; font-style: italic; }
.empty-state-small { padding: 40rpx 0; text-align: center; color: #999; font-size: 20rpx; }

/* Picker 提示 */
.picker-hint { font-size: 20rpx; color: #999; margin-top: 8rpx; margin-bottom: 8rpx; }
</style>
