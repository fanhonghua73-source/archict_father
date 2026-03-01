"""
项目管理模块 - 管理建筑项目数据
包含：项目基本信息、文件列表、人员安排、经济技术指标、存储配置
"""

import json
from pathlib import Path
from datetime import datetime

class ProjectManager:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent / 'data'
        self.projects_file = self.base_dir / 'projects.json'
        self.management_dir = self.base_dir / 'management'
        self.base_dir.mkdir(exist_ok=True)
        self.management_dir.mkdir(exist_ok=True)

        if not self.projects_file.exists():
            self._init_projects()

    # ==================== 项目列表 ====================

    def _init_projects(self):
        sample = [
            {
                'id': 1, 'name': '温州中心项目', 'code': 'WZ-2026-001',
                'location': '温州市鹿城区', 'status': '设计中', 'stage': '方案设计',
                'progress': 45, 'created_at': '2026-01-15', 'updated_at': '2026-03-01'
            },
            {
                'id': 2, 'name': '滨江住宅', 'code': 'BJ-2026-002',
                'location': '杭州市滨江区', 'status': '施工中', 'stage': '施工图',
                'progress': 75, 'created_at': '2025-10-20', 'updated_at': '2026-03-01'
            }
        ]
        with open(self.projects_file, 'w', encoding='utf-8') as f:
            json.dump(sample, f, ensure_ascii=False, indent=2)

    def _load_projects(self):
        with open(self.projects_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_projects(self, data):
        with open(self.projects_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_all(self):
        return self._load_projects()

    def get_by_id(self, project_id):
        for p in self._load_projects():
            if p['id'] == project_id:
                return p
        return None

    def create(self, data):
        projects = self._load_projects()
        data['id'] = max([p['id'] for p in projects], default=0) + 1
        now = datetime.now().strftime('%Y-%m-%d')
        data['created_at'] = now
        data['updated_at'] = now
        projects.append(data)
        self._save_projects(projects)
        return data

    def update(self, project_id, updates):
        projects = self._load_projects()
        for i, p in enumerate(projects):
            if p['id'] == project_id:
                p.update(updates)
                p['updated_at'] = datetime.now().strftime('%Y-%m-%d')
                projects[i] = p
                self._save_projects(projects)
                return p
        return None

    # ==================== 项目管理台数据 ====================

    def _mgmt_file(self, project_id):
        return self.management_dir / f'project_{project_id}.json'

    def _load_mgmt(self, project_id):
        f = self._mgmt_file(project_id)
        if f.exists():
            with open(f, 'r', encoding='utf-8') as fp:
                return json.load(fp)
        # 返回默认结构
        return {
            'project_id': project_id,
            'storage_config': {'type': 'local', 'path': '', 'url': ''},
            'files': self._default_files(),
            'staff': self._default_staff(),
            'economic_indexes': self._default_indexes()
        }

    def _save_mgmt(self, project_id, data):
        data['updated_at'] = datetime.now().isoformat()
        with open(self._mgmt_file(project_id), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return data

    def _default_staff(self):
        names = ['张三','李四','王五','赵六','钱七','孙八',
                 '周九','吴十','郑一','冯二','陈三','褚四',
                 '卫五','蒋六','沈七','韩八','杨九','朱十',
                 '秦十一','尤十二','许十三','何十四','吕十五','施十六']
        import random
        return [{'id': i+1, 'name': n, 'busy': random.randint(10, 95),
                 'active': random.choice([True, False]),
                 'schedule': '', 'role': ''}
                for i, n in enumerate(names)]

    def _default_files(self):
        """默认虚拟文件数据，展示文件分类结构"""
        return [
            # 原始资料 - 红线图
            {'id': 1, 'name': '红线图 v1', 'type': 'DWG', 'category': 'original/redline', 'path': 'original/redline',
             'size': 2457600, 'date': '2026-02-20', 'uploaded_at': '2026-02-20', 'remark': '初版红线图'},
            {'id': 2, 'name': '红线图 v2', 'type': 'DWG', 'category': 'original/redline', 'path': 'original/redline',
             'size': 2512000, 'date': '2026-02-25', 'uploaded_at': '2026-02-25', 'remark': '修改后的红线图'},
            {'id': 3, 'name': '红线图', 'type': 'PDF', 'category': 'original/redline', 'path': 'original/redline',
             'size': 8495104, 'date': '2026-02-25', 'uploaded_at': '2026-02-25', 'remark': 'PDF版本'},

            # 原始资料 - 测绘图
            {'id': 4, 'name': '地形测绘图', 'type': 'DWG', 'category': 'original/survey', 'path': 'original/survey',
             'size': 5242880, 'date': '2026-02-18', 'uploaded_at': '2026-02-18', 'remark': '1:500地形图'},
            {'id': 5, 'name': '现状建筑测绘', 'type': 'DWG', 'category': 'original/survey', 'path': 'original/survey',
             'size': 3145728, 'date': '2026-02-18', 'uploaded_at': '2026-02-18', 'remark': '现状建筑平面'},

            # 原始资料 - 地质报告
            {'id': 6, 'name': '岩土工程勘察报告', 'type': 'PDF', 'category': 'original/geology', 'path': 'original/geology',
             'size': 15728640, 'date': '2026-02-10', 'uploaded_at': '2026-02-10', 'remark': '详细勘察报告'},

            # 项目管理 - 合同
            {'id': 7, 'name': '设计合同', 'type': 'PDF', 'category': 'management/contract', 'path': 'management/contract',
             'size': 2097152, 'date': '2026-01-15', 'uploaded_at': '2026-01-15', 'remark': '设计服务合同'},
            {'id': 8, 'name': '补充协议', 'type': 'PDF', 'category': 'management/contract', 'path': 'management/contract',
             'size': 1048576, 'date': '2026-02-01', 'uploaded_at': '2026-02-01', 'remark': '合同补充协议'},

            # 项目管理 - 会议纪要
            {'id': 9, 'name': '启动会议纪要', 'type': 'DOC', 'category': 'management/meeting', 'path': 'management/meeting',
             'size': 524288, 'date': '2026-01-20', 'uploaded_at': '2026-01-20', 'remark': '项目启动会'},
            {'id': 10, 'name': '方案评审会议纪要', 'type': 'DOC', 'category': 'management/meeting', 'path': 'management/meeting',
             'size': 614400, 'date': '2026-02-28', 'uploaded_at': '2026-02-28', 'remark': '方案评审会'},

            # 项目管理 - 进度计划
            {'id': 11, 'name': '总体进度计划', 'type': 'XLS', 'category': 'management/schedule', 'path': 'management/schedule',
             'size': 409600, 'date': '2026-01-25', 'uploaded_at': '2026-01-25', 'remark': '项目总进度'},

            # 阶段文件 - 方案设计
            {'id': 12, 'name': '总平面图', 'type': 'DWG', 'category': 'stage/concept', 'path': 'stage/concept',
             'size': 3355443, 'date': '2026-02-28', 'uploaded_at': '2026-02-28', 'remark': '方案总平面'},
            {'id': 13, 'name': '总平面图', 'type': 'PDF', 'category': 'stage/concept', 'path': 'stage/concept',
             'size': 13107200, 'date': '2026-02-28', 'uploaded_at': '2026-02-28', 'remark': 'PDF版总平面'},
            {'id': 14, 'name': '1号楼平面图', 'type': 'DWG', 'category': 'stage/concept', 'path': 'stage/concept',
             'size': 2621440, 'date': '2026-02-28', 'uploaded_at': '2026-02-28', 'remark': '1号楼各层平面'},
            {'id': 15, 'name': '1号楼立面图', 'type': 'DWG', 'category': 'stage/concept', 'path': 'stage/concept',
             'size': 1887436, 'date': '2026-02-28', 'uploaded_at': '2026-02-28', 'remark': '1号楼四个立面'},
            {'id': 16, 'name': '1号楼剖面图', 'type': 'DWG', 'category': 'stage/concept', 'path': 'stage/concept',
             'size': 1572864, 'date': '2026-02-28', 'uploaded_at': '2026-02-28', 'remark': '1号楼剖面'},

            # 阶段文件 - 初步设计
            {'id': 17, 'name': '初步设计说明', 'type': 'DOC', 'category': 'stage/preliminary', 'path': 'stage/preliminary',
             'size': 1048576, 'date': '2026-03-01', 'uploaded_at': '2026-03-01', 'remark': '初设说明书'},

            # 效果图
            {'id': 18, 'name': '鸟瞰图 01', 'type': 'JPG', 'category': 'rendering', 'path': 'rendering',
             'size': 6082560, 'date': '2026-02-26', 'uploaded_at': '2026-02-26', 'remark': '整体鸟瞰'},
            {'id': 19, 'name': '鸟瞰图 02', 'type': 'JPG', 'category': 'rendering', 'path': 'rendering',
             'size': 6502400, 'date': '2026-02-26', 'uploaded_at': '2026-02-26', 'remark': '另一角度鸟瞰'},
            {'id': 20, 'name': '沿街透视图', 'type': 'JPG', 'category': 'rendering', 'path': 'rendering',
             'size': 5767168, 'date': '2026-02-27', 'uploaded_at': '2026-02-27', 'remark': '沿街效果'},
            {'id': 21, 'name': '入口透视图', 'type': 'JPG', 'category': 'rendering', 'path': 'rendering',
             'size': 5242880, 'date': '2026-02-27', 'uploaded_at': '2026-02-27', 'remark': '主入口效果'},
            {'id': 22, 'name': '庭院透视图', 'type': 'JPG', 'category': 'rendering', 'path': 'rendering',
             'size': 4718592, 'date': '2026-02-27', 'uploaded_at': '2026-02-27', 'remark': '内庭院效果'},
            {'id': 23, 'name': 'AI生成效果图_01', 'type': 'PNG', 'category': 'rendering', 'path': 'rendering',
             'size': 3932160, 'date': '2026-03-01', 'uploaded_at': '2026-03-01', 'remark': 'AI生成的效果图'},

            # 工作文件
            {'id': 24, 'name': '草图方案A', 'type': 'SKP', 'category': 'work', 'path': 'work',
             'size': 15728640, 'date': '2026-02-15', 'uploaded_at': '2026-02-15', 'remark': '初步草图'},
            {'id': 25, 'name': '草图方案B', 'type': 'SKP', 'category': 'work', 'path': 'work',
             'size': 16777216, 'date': '2026-02-16', 'uploaded_at': '2026-02-16', 'remark': '修改方案'},
            {'id': 26, 'name': '分析图', 'type': 'SKP', 'category': 'work', 'path': 'work',
             'size': 12582912, 'date': '2026-02-20', 'uploaded_at': '2026-02-20', 'remark': '场地分析模型'},

            # 专项设计
            {'id': 27, 'name': '结构方案', 'type': 'PDF', 'category': 'special', 'path': 'special',
             'size': 5242880, 'date': '2026-02-25', 'uploaded_at': '2026-02-25', 'remark': '结构专业方案'},
            {'id': 28, 'name': '景观方案', 'type': 'PDF', 'category': 'special', 'path': 'special',
             'size': 10485760, 'date': '2026-02-26', 'uploaded_at': '2026-02-26', 'remark': '景观设计方案'},
        ]

    def _default_indexes(self):
        return [
            {'id': 1, 'name': '用地面积',     'value': 36000, 'unit': '㎡', 'calculated': False},
            {'id': 2, 'name': '容积率',       'value': 2.4,   'unit': '/', 'calculated': True},
            {'id': 3, 'name': '地下室面积',   'value': 40000, 'unit': '㎡', 'calculated': True},
            {'id': 4, 'name': '配套面积',     'value': 5000,  'unit': '㎡', 'calculated': False},
            {'id': 5, 'name': '建筑面积',     'value': 121400,'unit': '㎡', 'calculated': True},
            {'id': 6, 'name': '高层住宅面积', 'value': 80000, 'unit': '㎡', 'calculated': False},
            {'id': 7, 'name': '低层住宅面积', 'value': 20000, 'unit': '㎡', 'calculated': False},
            {'id': 8, 'name': '商业面积',     'value': 15000, 'unit': '㎡', 'calculated': False},
        ]

    # ==================== 存储配置 ====================

    def get_storage_config(self, project_id):
        return self._load_mgmt(project_id).get('storage_config', {})

    def update_storage_config(self, project_id, config):
        data = self._load_mgmt(project_id)
        data['storage_config'] = config
        return self._save_mgmt(project_id, data)

    # ==================== 文件管理 ====================

    def get_files(self, project_id, dir_path=''):
        data = self._load_mgmt(project_id)
        files = data.get('files', [])
        if dir_path:
            files = [f for f in files if f.get('path', '').startswith(dir_path)]
        return files

    def add_file(self, project_id, file_data):
        data = self._load_mgmt(project_id)
        files = data.get('files', [])
        file_data['id'] = max([f.get('id', 0) for f in files], default=0) + 1
        file_data['uploaded_at'] = datetime.now().strftime('%Y-%m-%d')
        files.append(file_data)
        data['files'] = files
        self._save_mgmt(project_id, data)
        return file_data

    def delete_file(self, project_id, file_id):
        data = self._load_mgmt(project_id)
        data['files'] = [f for f in data.get('files', []) if f.get('id') != file_id]
        return self._save_mgmt(project_id, data)

    # ==================== 人员管理 ====================

    def get_staff(self, project_id):
        return self._load_mgmt(project_id).get('staff', [])

    def update_staff(self, project_id, staff_list):
        data = self._load_mgmt(project_id)
        data['staff'] = staff_list
        return self._save_mgmt(project_id, data)

    def update_staff_member(self, project_id, staff_id, updates):
        data = self._load_mgmt(project_id)
        for s in data.get('staff', []):
            if s.get('id') == staff_id:
                s.update(updates)
                break
        return self._save_mgmt(project_id, data)

    # ==================== 经济技术指标 ====================

    def get_indexes(self, project_id):
        return self._load_mgmt(project_id).get('economic_indexes', [])

    def update_indexes(self, project_id, indexes):
        data = self._load_mgmt(project_id)
        data['economic_indexes'] = indexes
        return self._save_mgmt(project_id, data)
