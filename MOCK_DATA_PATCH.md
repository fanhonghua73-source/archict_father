# 管理台模拟数据补丁

## 问题
管理台的文件和人员数据是空的，需要添加模拟数据来查看效果。

## 解决方案

在 `management.vue` 的 `data()` 中，将 `files: []` 和 `staffList: []` 替换为以下模拟数据：

### 文件数据（28个）

```javascript
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
```

### 人员数据（24人，部分有角色和时间安排）

```javascript
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
```

## 如何应用

1. 打开 `uniapp-frontend/pages/management/management.vue`
2. 找到 `data()` 函数中的 `files: []`
3. 替换为上面的文件数据
4. 找到 `staffList: []`
5. 替换为上面的人员数据
6. 保存文件
7. 刷新浏览器

## 预期效果

### 文件显示
- 点击"原始资料" → 显示 6 个文件
- 点击"原始资料" → "红线图" → 显示 3 个红线图文件
- 点击"效果图" → 显示 6 个效果图文件
- 点击"阶段文件" → "方案设计" → 显示 5 个方案设计文件

### 人员显示
- 中列显示 24 个人员格子
- 激活的人员（绿色）：张三、王五、钱七、吴十、冯二、卫五、韩八、秦十一、何十四（共9人）
- 右侧"人员时间规划"显示这 9 个激活人员的详细信息
- 其中 8 人有角色和时间安排，可以看到具体的工作安排

### 交互测试
1. 点击人员格子 → 切换激活/停用状态
2. 点击 ✎ 按钮 → 编辑人员信息
3. 修改角色和时间安排 → 保存
4. 右侧时间规划区域会更新显示

## 注意
这些是前端模拟数据，不会保存到后端。如果需要持久化，需要调用后端 API。
