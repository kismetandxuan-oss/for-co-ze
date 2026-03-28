# 🚀 Railway 部署指南

## 📋 准备工作

在开始之前，请确保：
1. 已有 GitHub 账号
2. 已有 Railway 账号（可使用 GitHub 登录）
3. 已有飞书多维表格，并获取了 App Token 和 Table ID

## 第一步：上传代码到 GitHub

### 1.1 初始化 Git 仓库

在项目根目录执行：

```bash
git init
git add .
git commit -m "feat: 链接自动归档助手 - 初始版本"
git branch -M main
```

### 1.2 创建 GitHub 仓库

1. 访问 https://github.com/new
2. 填写仓库名称：`link-archive-agent`
3. 选择 **Private**（推荐）或 **Public**
4. **不要**勾选 "Add a README file"（已有 README）
5. 点击 **"Create repository"**

### 1.3 推送代码

```bash
git remote add origin https://github.com/YOUR_USERNAME/link-archive-agent.git
git push -u origin main
```

## 第二步：部署到 Railway

### 2.1 登录 Railway

1. 访问 https://railway.app/
2. 点击 **"Start a New Project"**
3. 选择 **"Deploy from GitHub repo"**
4. 授权 Railway 访问你的 GitHub 仓库
5. 选择 `link-archive-agent` 仓库

### 2.2 配置环境变量

在 Railway 项目页面：

1. 点击项目名称进入详情页
2. 点击 **"Variables"** 标签
3. 点击 **"New Variable"**，添加以下变量：

**必须添加的环境变量：**

```
FEISHU_APP_TOKEN = Wg4zwGaOKiJJ6OkI6SJc2avenxd
FEISHU_TABLE_ID = tblHoEKeUuiz2zet
```

**注意：**
- `FEISHU_APP_TOKEN`: 从你的飞书多维表格 URL 中获取
- `FEISHU_TABLE_ID`: 从你的飞书多维表格 URL 中获取

**自动注入的环境变量（无需手动设置）：**
- `COZE_WORKLOAD_IDENTITY_API_KEY`: Coze 平台自动提供
- `COZE_INTEGRATION_MODEL_BASE_URL`: Coze 平台自动提供
- `PORT`: Railway 自动分配

### 2.3 触发部署

1. 添加环境变量后，Railway 会自动触发部署
2. 点击 **"Deployments"** 标签查看部署进度
3. 等待部署完成（通常需要 2-5 分钟）

### 2.4 获取服务域名

部署成功后：

1. 点击 **"Settings"** 标签
2. 找到 **"Domains"** 部分
3. 点击 **"Generate Domain"**
4. Railway 会生成一个域名，如：`https://link-archive-agent-production.up.railway.app`

### 2.5 验证部署

访问健康检查接口：

```
https://your-domain.railway.app/health
```

预期返回：

```json
{
  "status": "ok",
  "message": "Service is running"
}
```

## 第三步：配置飞书机器人

### 3.1 创建飞书应用

1. 访问 https://open.feishu.cn/app
2. 点击 **"创建企业自建应用"**
3. 填写应用名称和描述
4. 上传应用图标
5. 点击 **"创建"**

### 3.2 配置事件订阅

1. 在应用详情页，点击 **"事件订阅"**
2. 点击 **"配置"**
3. 填写请求地址：

```
https://your-domain.railway.app/run
```

4. 点击 **"发送测试请求"**，确认成功
5. 点击 **"保存"**

### 3.3 配置权限

在 **"权限管理"** 页面，添加以下权限：

**消息权限：**
- `im:message` - 获取与发送消息
- `im:message:receive_as_bot` - 接收群聊消息

**多维表格权限：**
- `bitable:app` - 查看、评论、编辑多维表格

### 3.4 发布应用

1. 点击 **"版本管理与发布"**
2. 创建新版本
3. 提交审核
4. 审核通过后，发布到企业

### 3.5 添加机器人到群组

1. 在飞书群组设置中
2. 点击 **"群机器人"**
3. 添加你创建的机器人

## 第四步：测试功能

### 4.1 在飞书群组中测试

发送消息：

```
帮我归档这个链接：http://xhslink.com/o/90tUxi9GZhW 这是阿里的文章
```

### 4.2 预期结果

Agent 会回复：

```
✅ 已归档：《阿里相关文章》

归档信息：
- 平台：小红书
- 链接：http://xhslink.com/o/90tUxi9GZhW
- 标签：企业资讯、互联网大厂、技术分享
- 备注：这是阿里的文章
```

### 4.3 检查飞书多维表格

打开你的飞书多维表格，应该能看到新增的一条记录，包含：
- 标题
- 链接（可点击）
- 正文摘要
- 备注
- 场景标签
- 来源平台
- 收藏时间

## 🔧 常见问题

### Q1: 部署失败，提示依赖安装错误

**解决方案：**
1. 检查 `requirements.txt` 是否完整
2. 查看 Railway 部署日志
3. 尝试清除 Railway 缓存并重新部署

### Q2: 服务启动成功，但健康检查失败

**解决方案：**
1. 检查 `Procfile` 文件格式是否正确
2. 确认端口号使用 `${PORT}` 环境变量
3. 查看 Railway 应用日志

### Q3: 飞书事件订阅配置失败

**解决方案：**
1. 确认 Railway 服务已成功部署
2. 检查域名是否可访问
3. 确认请求地址是 `https://` 开头

### Q4: 链接归档失败

**解决方案：**
1. 检查环境变量 `FEISHU_APP_TOKEN` 和 `FEISHU_TABLE_ID` 是否正确
2. 确认飞书应用有多维表格的编辑权限
3. 查看 Railway 应用日志

### Q5: 收藏时间显示错误

**解决方案：**
- 最新代码已修复时间戳问题
- 确保使用的是最新版本的代码

## 📊 监控和日志

### 查看 Railway 日志

1. 在 Railway 项目页面
2. 点击 **"Deployments"**
3. 点击具体的部署记录
4. 点击 **"Logs"** 查看实时日志

### 查看应用指标

在 Railway 项目页面：
- **"Metrics"** 标签：查看 CPU、内存使用情况
- **"Insights"** 标签：查看请求量和响应时间

## 💰 成本说明

Railway 提供免费额度：
- 每月 $5 免费额度
- 超出后按实际使用收费

预计成本：
- 小型应用：免费额度内
- 中型应用：约 $5-10/月
- 大型应用：约 $20+/月

## 🔄 更新和重新部署

### 更新代码

```bash
git add .
git commit -m "fix: 修复某个问题"
git push
```

Railway 会自动检测代码更新并重新部署。

### 手动触发部署

在 Railway 项目页面：
1. 点击 **"Deployments"**
2. 点击最新部署右侧的 **"..."**
3. 选择 **"Redeploy"**

## 🎉 完成！

恭喜！你的链接自动归档助手已经成功部署并接入飞书。

现在可以在飞书中发送链接，Agent 会自动解析并归档到多维表格中。

如有问题，请查看 Railway 日志或提交 Issue。
