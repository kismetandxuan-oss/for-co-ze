# 🚀 快速部署指南

## 📋 部署清单

### ✅ 准备工作

- [ ] 注册 GitHub 账号
- [ ] 注册 Railway 账号（可用 GitHub 登录）
- [ ] 获取 Coze API Token
- [ ] 确认 Coze 服务地址：`https://kp2dz8j3vw.coze.site`

## 🔧 详细步骤

### 第 1 步：上传代码到 GitHub

#### 方式 A：创建新仓库

1. **在 GitHub 创建新仓库**
   - 访问：https://github.com/new
   - Repository name: `feishu-proxy`
   - 选择 Public
   - 不要勾选 "Initialize with README"
   - 点击 "Create repository"

2. **上传文件**
   
   方式 1：网页上传
   - 在仓库页面点击 "uploading an existing file"
   - 拖拽 `feishu-proxy` 目录下的所有文件：
     - `proxy_server.py`
     - `requirements.txt`
     - `Procfile`
     - `.gitignore`
     - `README.md`
   - 点击 "Commit changes"
   
   方式 2：命令行上传
   ```bash
   cd feishu-proxy
   git init
   git add .
   git commit -m "Initial commit: Feishu proxy service"
   git branch -M main
   git remote add origin https://github.com/你的用户名/feishu-proxy.git
   git push -u origin main
   ```

#### 方式 B：使用现有项目

如果你的当前项目已经在 GitHub 上，可以直接使用当前仓库：
- Railway 可以选择部署子目录
- 或者将代理服务文件添加到项目根目录

### 第 2 步：部署到 Railway

1. **访问 Railway**
   ```
   https://railway.app/
   ```

2. **使用 GitHub 登录**
   - 点击 "Start a New Project"
   - 选择 "Login with GitHub"
   - 授权 Railway 访问你的 GitHub

3. **创建新项目**
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择你创建的 `feishu-proxy` 仓库
   - Railway 会自动检测 `Procfile` 并开始部署

4. **配置环境变量**
   
   在部署过程中或部署后：
   - 点击服务名称进入服务详情
   - 点击 "Variables" 标签
   - 点击 "Add Variable" 添加以下变量：
   
   ```
   COZE_API_TOKEN=你的Coze_API_Token
   ```
   
   ```
   COZE_WEBHOOK_URL=https://kp2dz8j3vw.coze.site/feishu/webhook
   ```
   
   **注意**：`COZE_API_TOKEN` 从 Coze 项目页面获取（格式：`ylh_xxxxx`）

5. **等待部署完成**
   - 查看 "Deployments" 标签
   - 等待状态变为 "SUCCESS"
   - 通常需要 1-3 分钟

6. **获取服务域名**
   - 点击服务名称
   - 点击 "Settings" 标签
   - 在 "Domains" 区域可以看到自动生成的域名
   - 例如：`https://feishu-proxy-production.up.railway.app`

### 第 3 步：验证部署

在终端中执行以下命令测试：

```bash
# 测试健康检查
curl https://你的railway域名/health
```

预期返回：
```json
{
  "status": "ok",
  "message": "Proxy service is running",
  "target_url": "https://kp2dz8j3vw.coze.site/feishu/webhook"
}
```

```bash
# 测试飞书 URL 验证
curl -X POST https://你的railway域名/feishu/webhook \
  -H "Content-Type: application/json" \
  -d '{"type":"url_verification","challenge":"test123"}'
```

预期返回：
```json
{
  "challenge": "test123"
}
```

✅ **如果两个测试都通过，说明代理服务部署成功！**

### 第 4 步：配置飞书

#### 4.1 创建飞书应用

1. 访问：https://open.feishu.cn/
2. 点击右上角「开发者后台」
3. 点击「创建企业自建应用」
4. 填写信息：
   - 应用名称：`智能归档助手`
   - 应用描述：`自动归档小红书和微信公众号文章`
5. 点击「确定创建」

#### 4.2 配置权限

1. 在应用详情页，点击左侧「权限管理」
2. 搜索并开通以下权限：
   - `im:message`
   - `im:message:send_as_bot`
   - `im:message:receive_as_bot`
3. 点击每个权限右侧的「申请权限」
4. 填写申请理由：`用于实现消息自动归档功能`
5. 点击「确认申请」

#### 4.3 配置事件订阅

1. 点击左侧「事件订阅」
2. 点击「添加事件订阅」
3. 配置请求地址：
   ```
   https://你的railway域名/feishu/webhook
   ```
4. 点击「验证」按钮
   - ✅ 如果验证成功，会显示绿色成功标识
   - ❌ 如果验证失败，检查代理服务是否正常运行
5. 点击「添加事件」
6. 搜索并选择：`im.message.receive_v1`
7. 点击「保存」

#### 4.4 发布应用

1. 点击左侧「版本管理与发布」
2. 点击「创建版本」
3. 填写：
   - 版本号：`1.0.0`
   - 版本说明：`初始版本，支持小红书和微信公众号链接自动归档`
4. 点击「提交审核」
5. 等待审核通过（通常几分钟到几小时）
6. 审核通过后，点击「发布」
7. 选择发布范围：`全员可见`或指定部门

### 第 5 步：添加机器人到群聊

1. 打开飞书
2. 进入一个群聊
3. 点击右上角「设置」图标
4. 点击「群机器人」
5. 点击「添加机器人」
6. 选择「智能归档助手」

### 第 6 步：测试功能

在群聊中发送：
```
http://xhslink.com/o/test 这是一个测试链接
```

预期：
- ✅ 机器人回复确认消息
- ✅ 飞书多维表格新增记录

## 🎉 完成！

恭喜你完成了所有配置！现在可以：

1. ✅ 在飞书群聊中发送小红书链接
2. ✅ 机器人自动识别并归档
3. ✅ 数据自动写入飞书多维表格

## 📊 时间预估

- GitHub 上传：5 分钟
- Railway 部署：5 分钟
- 飞书配置：10 分钟
- **总计：约 20 分钟**

## 🔍 常见问题

### Q1: Railway 部署失败

**检查项**：
- [ ] GitHub 仓库是否包含所有文件
- [ ] `Procfile` 文件是否正确
- [ ] `requirements.txt` 文件是否存在

**解决方案**：
1. 查看 Railway 的部署日志
2. 确认所有文件都已上传到 GitHub

### Q2: 飞书验证失败

**检查项**：
- [ ] 代理服务是否正常运行
- [ ] URL 地址是否正确
- [ ] 环境变量是否配置

**解决方案**：
1. 使用 curl 测试代理服务
2. 查看 Railway 日志
3. 确认环境变量配置正确

### Q3: 机器人没有响应

**检查项**：
- [ ] 飞书应用是否已发布
- [ ] 机器人是否已添加到群聊
- [ ] 权限是否已开通

**解决方案**：
1. 确认应用已发布
2. 确认机器人已添加到群聊
3. 确认权限已生效

## 📞 需要帮助？

如果遇到问题：
1. 查看 Railway 日志
2. 使用 curl 测试代理服务
3. 检查飞书应用配置
4. 参考项目 README.md
