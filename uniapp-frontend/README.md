# HBuilderX 打开 UniApp 项目指南

## ✅ 已创建标准 UniApp 项目

项目位置: `/Users/jiangyige/Documents/331建筑学爸/建筑学爸app/uniapp-frontend`

## 📝 在 HBuilderX 中打开步骤

### 1. 打开 HBuilderX
启动 HBuilderX 应用

### 2. 导入项目
- 点击菜单: **文件** → **导入** → **从本地目录导入**
- 或者: **文件** → **打开目录**

### 3. 选择项目目录
选择以下目录:
```
/Users/jiangyige/Documents/331建筑学爸/建筑学爸app/uniapp-frontend
```

### 4. 运行项目
- 点击顶部菜单: **运行** → **运行到浏览器** → **Chrome**
- 或者: **运行** → **运行到内置浏览器**

## 📁 项目结构

```
uniapp-frontend/
├── App.vue              ✅ 应用入口
├── main.js              ✅ 主入口文件
├── manifest.json        ✅ 应用配置
├── pages.json           ✅ 页面路由
├── index.html           ✅ HTML模板
├── package.json         ✅ 依赖配置
├── pages/               ✅ 页面目录
│   └── index/
│       └── index.vue    ✅ 首页
├── static/              ✅ 静态资源
└── unpackage/           ✅ 编译输出

```

## ✨ 项目特点

- ✅ 标准 uni-app 项目结构
- ✅ Vue 2 语法
- ✅ 包含完整的首页示例
- ✅ 连接后端 API
- ✅ 项目列表展示
- ✅ 统计数据显示

## 🔧 如果 HBuilderX 还是打不开

### 方法 1: 检查 HBuilderX 版本
确保使用 HBuilderX 3.0+ 版本
下载地址: https://www.dcloud.io/hbuilderx.html

### 方法 2: 重新安装 HBuilderX
1. 完全卸载当前 HBuilderX
2. 下载最新版本
3. 重新安装

### 方法 3: 使用命令行运行
```bash
cd "/Users/jiangyige/Documents/331建筑学爸/建筑学爸app/uniapp-frontend"

# 安装 HBuilderX CLI
npm install -g @dcloudio/uvm

# 使用最新版本
uvm use latest

# 运行项目
npx cross-env NODE_ENV=development uniapp-cli
```

## 🎯 验证项目是否正确

在 HBuilderX 中打开项目后，你应该看到:
- ✅ 左侧项目树显示完整结构
- ✅ 可以打开 `pages/index/index.vue` 文件
- ✅ 顶部有"运行"按钮
- ✅ 控制台没有错误提示

## 📞 常见问题

### Q: HBuilderX 提示"不是有效的项目"
**A**: 确保打开的是 `uniapp-frontend` 目录，不是 `frontend` 目录

### Q: 点击运行没反应
**A**:
1. 检查控制台是否有错误
2. 尝试: 运行 → 运行到内置浏览器
3. 重启 HBuilderX

### Q: 编译失败
**A**:
```bash
cd uniapp-frontend
rm -rf node_modules
rm -rf unpackage
```
然后在 HBuilderX 中重新运行

## 🚀 下一步

1. ✅ 在 HBuilderX 中打开 `uniapp-frontend` 目录
2. ✅ 点击"运行到浏览器"
3. ✅ 查看首页效果
4. ✅ 开始开发

---

**重要**: 请打开 `uniapp-frontend` 目录，不是之前的 `frontend` 目录！
