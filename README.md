# 飞书 Webhook 代理服务

## 📖 项目说明

这个代理服务用于解决 **Coze 平台需要鉴权，但飞书事件订阅不支持自定义 Header** 的问题。

### 工作原理

```
飞书 → 代理服务（自动添加 Authorization 头） → Coze 服务 → Agent 处理
```

### 功能特性

- ✅ 自动添加 Coze API Token 鉴权头
- ✅ 支持飞书 URL 验证
- ✅ 转发飞书消息事件到 Coze 服务
- ✅ 详细的日志记录
- ✅ 健康检查接口

## 🚀 快速部署

### 前置要求

1. **Coze API Token**：从 Coze 项目页面获取
2. **Coze 服务地址**：你的 Coze Agent 服务地址

### 方法 1：部署到 Railway（推荐）

#### 步骤 1：创建 GitHub 仓库

1. 访问 [GitHub](https://github.com/)
2. 创建新仓库（例如：`feishu-proxy`）
3. 将此目录的所有文件上传到仓库

```bash
# 在 feishu-proxy 目录下执行
git init
git add .
git commit -m "Initial commit: Feishu proxy service"
git branch -M main
git remote add origin https://github.com/你的用户名/feishu-proxy.git
git push -u origin main
```

#### 步骤 2：部署到 Railway

1. 访问 [Railway](https://railway.app/)
2. 使用 GitHub 登录
3. 点击 "New Project" → "Deploy from GitHub repo"
4. 选择你创建的 `feishu-proxy` 仓库
5. 添加环境变量：
   - `COZE_API_TOKEN`: 你的 Coze API Token
   - `COZE_WEBHOOK_URL`: 你的 Coze 服务地址（例如：`https://kp2dz8j3vw.coze.site/feishu/webhook`）
6. 点击 "Deploy"
7. 等待部署完成，获取 Railway 提供的域名

#### 步骤 3：验证部署

```bash
# 测试健康检查
curl https://your-railway-app.railway.app/health

# 测试飞书 URL 验证
curl -X POST https://your-railway-app.railway.app/feishu/webhook \
  -H "Content-Type: application/json" \
  -d '{"type":"url_verification","challenge":"test123"}'
```

### 方法 2：部署到 Render

1. 访问 [Render](https://render.com/)
2. 使用 GitHub 登录
3. 点击 "New" → "Web Service"
4. 连接你的 GitHub 仓库
5. 配置服务：
   - Name: `feishu-proxy`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn proxy_server:app --host 0.0.0.0 --port $PORT`
6. 添加环境变量：
   - `COZE_API_TOKEN`: 你的 Coze API Token
   - `COZE_WEBHOOK_URL`: 你的 Coze 服务地址
7. 点击 "Create Web Service"

### 方法 3：本地测试（使用 ngrok）

```bash
# 设置环境变量
export COZE_API_TOKEN="your_token_here"
export COZE_WEBHOOK_URL="https://kp2dz8j3vw.coze.site/feishu/webhook"

# 启动服务
python proxy_server.py

# 在另一个终端启动 ngrok
ngrok http 8000
```

## 🔧 配置飞书

### 步骤 1：创建飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 应用名称：`智能归档助手`

### 步骤 2：配置权限

在「权限管理」中开通：
- `im:message` - 获取与发送单聊、群组消息
- `im:message:send_as_bot` - 以应用身份发消息
- `im:message:receive_as_bot` - 接收群聊中@机器人消息

### 步骤 3：配置事件订阅

1. 在「事件订阅」中添加事件订阅
2. 配置请求地址：
   ```
   https://your-proxy-domain.com/feishu/webhook
   ```
3. 添加事件：`im.message.receive_v1`
4. 点击保存

### 步骤 4：发布应用

1. 在「版本管理与发布」中创建版本
2. 提交审核
3. 审核通过后发布应用

### 步骤 5：添加机器人到群聊

1. 打开飞书群聊
2. 点击「设置」→「群机器人」→「添加机器人」
3. 选择你创建的机器人

## 📝 环境变量说明

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `COZE_API_TOKEN` | Coze API Token | `ylh_xxxxxxxxxx` |
| `COZE_WEBHOOK_URL` | Coze 服务的飞书 Webhook 地址 | `https://kp2dz8j3vw.coze.site/feishu/webhook` |

## 🧪 测试验证

### 测试 1：健康检查

```bash
curl https://your-domain.com/health
```

预期返回：
```json
{
  "status": "ok",
  "message": "Proxy service is running",
  "target_url": "https://kp2dz8j3vw.coze.site/feishu/webhook"
}
```

### 测试 2：飞书 URL 验证

```bash
curl -X POST https://your-domain.com/feishu/webhook \
  -H "Content-Type: application/json" \
  -d '{"type":"url_verification","challenge":"test_challenge"}'
```

预期返回：
```json
{
  "challenge": "test_challenge"
}
```

### 测试 3：消息接收

在飞书群聊中发送：
```
http://xhslink.com/o/test 这是一个测试链接
```

预期：
- 机器人回复确认消息
- 飞书多维表格新增记录

## 📂 文件结构

```
feishu-proxy/
├── proxy_server.py      # 主程序文件
├── requirements.txt     # Python 依赖
├── Procfile            # Railway 部署配置
├── .gitignore          # Git 忽略文件
└── README.md           # 说明文档
```

## 🔍 问题排查

### 问题 1：Challenge code 没有返回

**原因**：代理服务未正确启动或环境变量未配置

**解决方案**：
1. 检查 Railway 服务是否正常运行
2. 确认环境变量已配置
3. 查看 Railway 日志

### 问题 2：返回 502 Bad Gateway

**原因**：无法连接到 Coze 服务

**解决方案**：
1. 检查 `COZE_WEBHOOK_URL` 是否正确
2. 检查 `COZE_API_TOKEN` 是否有效
3. 使用 curl 直接测试 Coze 服务

### 问题 3：机器人没有响应

**原因**：
- 飞书应用权限未开通
- 事件订阅未配置
- 应用未发布

**解决方案**：
1. 确认飞书应用权限已开通
2. 确认事件订阅已保存
3. 确认应用已发布

## 📞 技术支持

如遇到问题，请：
1. 查看代理服务日志
2. 使用 curl 逐层测试
3. 检查飞书应用配置
4. 查看项目文档

## 📄 License

MIT License
