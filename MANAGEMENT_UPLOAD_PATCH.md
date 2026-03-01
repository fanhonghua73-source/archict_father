# 管理台文件上传功能补丁

## 需要在 management.vue 的 data() 中添加的字段

在 `showStorageModal: false,` 后面添加：

```javascript
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
currentCategory: 'original',
```

## 需要添加的 computed 属性

在 `methods: {` 之前添加：

```javascript
computed: {
    filteredFiles() {
        // 根据当前选中的文件夹过滤文件
        if (!this.currentCategory) {
            return this.files
        }
        return this.files.filter(file => {
            return file.category === this.currentCategory ||
                   file.path === this.currentCategory ||
                   file.path?.startsWith(this.currentCategory + '/')
        })
    }
},
```

## 需要添加的 methods

在 `methods: {` 内部添加：

```javascript
// ==================== 文件分类和过滤 ====================

getCurrentCategoryName() {
    const categoryMap = {
        'original': '原始资料',
        'original/redline': '红线图',
        'original/survey': '测绘图',
        'original/geology': '地质报告',
        'management': '项目管理',
        'management/contract': '合同',
        'management/meeting': '会议纪要',
        'management/schedule': '进度计划',
        'stage': '阶段文件',
        'stage/concept': '方案设计',
        'stage/preliminary': '初步设计',
        'stage/construction': '施工图',
        'special': '专项设计',
        'work': '工作文件',
        'rendering': '效果图'
    }
    return categoryMap[this.currentCategory] || '全部文件'
},

// ==================== 文件上传 ====================

openUploadModal() {
    this.uploadForm = {
        name: '',
        typeIndex: 0,
        type: 'DWG',
        filePath: '',
        fileName: '',
        fileSize: '',
        remark: ''
    }
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
        extension: ['.dwg', '.pdf', '.skp', '.jpg', '.png', '.doc', '.docx', '.xls', '.xlsx'],
        success: (res) => {
            const file = res.tempFiles[0]
            this.uploadForm.filePath = file.path
            this.uploadForm.fileName = file.name
            this.uploadForm.fileSize = this.formatFileSize(file.size)

            // 自动填充文件名（如果用户没有输入）
            if (!this.uploadForm.name) {
                this.uploadForm.name = file.name.replace(/\.[^/.]+$/, '')
            }

            // 自动识别文件类型
            const ext = file.name.split('.').pop().toUpperCase()
            const typeIndex = this.fileTypes.indexOf(ext)
            if (typeIndex !== -1) {
                this.uploadForm.typeIndex = typeIndex
                this.uploadForm.type = ext
            }
        },
        fail: (err) => {
            console.error('选择文件失败:', err)
            uni.showToast({ title: '选择文件失败', icon: 'none' })
        }
    })
},

formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
},

async submitUpload() {
    if (!this.uploadForm.name) {
        uni.showToast({ title: '请输入文件名称', icon: 'none' })
        return
    }
    if (!this.uploadForm.filePath) {
        uni.showToast({ title: '请选择文件', icon: 'none' })
        return
    }

    this.uploading = true

    try {
        // 上传文件到后端
        const uploadRes = await uni.uploadFile({
            url: `http://localhost:5002/api/projects/${this.projectId}/files/upload`,
            filePath: this.uploadForm.filePath,
            name: 'file',
            formData: {
                'name': this.uploadForm.name,
                'type': this.uploadForm.type,
                'category': this.currentCategory,
                'remark': this.uploadForm.remark
            }
        })

        const result = JSON.parse(uploadRes[1].data)
        if (result.success) {
            uni.showToast({ title: '上传成功', icon: 'success' })
            this.closeUploadModal()
            // 重新加载文件列表
            await this.loadFiles()
        } else {
            throw new Error(result.error || '上传失败')
        }
    } catch (error) {
        console.error('上传文件失败:', error)
        uni.showToast({ title: '上传失败: ' + error.message, icon: 'none' })
    } finally {
        this.uploading = false
    }
},

async loadFiles() {
    try {
        const res = await uni.request({
            url: `http://localhost:5002/api/projects/${this.projectId}/files`,
            method: 'GET'
        })
        if (res.data.success) {
            this.files = res.data.data
        }
    } catch (error) {
        console.error('加载文件列表失败:', error)
    }
},

downloadFile(file) {
    uni.showToast({ title: '开始下载...', icon: 'loading' })
    // TODO: 实现文件下载
    console.log('下载文件:', file)
},

async deleteFile(file) {
    uni.showModal({
        title: '确认删除',
        content: `确定要删除文件"${file.name}"吗？`,
        success: async (res) => {
            if (res.confirm) {
                try {
                    await uni.request({
                        url: `http://localhost:5002/api/projects/${this.projectId}/files/${file.id}`,
                        method: 'DELETE'
                    })
                    uni.showToast({ title: '删除成功', icon: 'success' })
                    await this.loadFiles()
                } catch (error) {
                    console.error('删除文件失败:', error)
                    uni.showToast({ title: '删除失败', icon: 'none' })
                }
            }
        }
    })
},
```

## 修改 selectPrimaryDir 和 selectSecondaryDir 方法

```javascript
selectPrimaryDir(id) {
    this.selectedPrimaryDir = id
    this.currentCategory = id  // 更新当前分类
    const secondaryMap = {
        original: [
            { id: 'redline', name: '红线图' },
            { id: 'survey', name: '测绘图' },
            { id: 'geology', name: '地质报告' }
        ],
        management: [
            { id: 'contract', name: '合同' },
            { id: 'meeting', name: '会议纪要' },
            { id: 'schedule', name: '进度计划' }
        ],
        stage: [
            { id: 'concept', name: '方案设计' },
            { id: 'preliminary', name: '初步设计' },
            { id: 'construction', name: '施工图' }
        ]
    }
    this.secondaryDirs = secondaryMap[id] || []
    this.selectedSecondaryDir = ''
},

selectSecondaryDir(id) {
    this.selectedSecondaryDir = id
    this.currentCategory = this.selectedPrimaryDir + '/' + id  // 更新为二级分类
},
```

## 在 onShow() 中添加文件加载

```javascript
onShow() {
    // 每次显示页面时重新读取项目并加载数据
    const selected = uni.getStorageSync('selectedProject')
    console.log('onShow - 读取到的项目:', selected)
    if (selected && selected.id) {
        this.projectId = selected.id
        this.projectName = selected.name
        console.log('onShow - 设置项目ID:', this.projectId, '名称:', this.projectName)
    }
    console.log('开始加载项目数据，项目ID:', this.projectId)
    this.loadStorageConfig()
    this.loadFiles()  // 添加这一行
    this.loadStaff()
    this.loadIndexes()
},
```

## 需要添加的 CSS 样式

在 `<style>` 部分添加：

```css
/* 文件头部 */
.file-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16rpx;
}

.upload-btn {
    padding: 12rpx 24rpx;
    background: #7cb342;
    color: white;
    border-radius: 12rpx;
    font-size: 22rpx;
    cursor: pointer;
    transition: background 0.2s;
}

.upload-btn:hover {
    background: #6fa035;
}

/* 文件表格操作列 */
.col-action {
    display: flex;
    gap: 12rpx;
    justify-content: flex-end;
}

.action-btn {
    font-size: 20rpx;
    color: #7cb342;
    cursor: pointer;
    padding: 4rpx 8rpx;
}

.action-btn:hover {
    text-decoration: underline;
}

.action-btn.delete {
    color: #f44336;
}

.empty-state {
    padding: 60rpx 0;
    text-align: center;
    color: #999;
    font-size: 22rpx;
}

/* 上传区域 */
.upload-area {
    border: 2px dashed #e0e0e0;
    border-radius: 12rpx;
    padding: 40rpx;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
}

.upload-area:hover {
    border-color: #7cb342;
    background: #f1f8e9;
}

.upload-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12rpx;
}

.upload-icon {
    font-size: 60rpx;
}

.upload-hint {
    font-size: 24rpx;
    color: #666;
}

.upload-hint-sub {
    font-size: 20rpx;
    color: #999;
}

.upload-selected {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8rpx;
}

.upload-filename {
    font-size: 22rpx;
    color: #333;
    font-weight: 500;
}

.upload-filesize {
    font-size: 20rpx;
    color: #999;
}
```
