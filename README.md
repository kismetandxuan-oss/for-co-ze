# 🔗 链接自动归档助手

一个智能的链接归档 Agent，支持自动解析小红书和微信公众号链接，并将内容归档到飞书多维表格。

## ✨ 功能特性

- 🎯 **自动识别链接**：支持小红书和微信公众号链接
- 📝 **内容提取**：自动提取标题、正文、图片等信息
- 🏷️ **智能标签**：基于内容自动生成场景标签
- 📊 **飞书归档**：一键写入飞书多维表格
- 💬 **用户备注**：支持保存用户的主观评价
- ⏰ **时间记录**：自动记录收藏时间

## 🛠️ 技术栈

- **框架**: LangGraph + LangChain
- **模型**: Doubao Seed (豆包)
- **服务**: FastAPI + Uvicorn
- **集成**: 飞书多维表格 API
- **部署**: Railway

## 📦 项目结构

```
.
├── config/
│   └── agent_llm_config.json    # Agent 配置文件
├── src/
│   ├── agents/
│   │   └── agent.py              # Agent 主逻辑
│   ├── tools/
│   │   ├── link_parser.py        # 链接解析工具
│   │   └── feishu_bitable.py     # 飞书多维表格工具
│   ├── storage/                  # 存储模块
│   ├── utils/                    # 工具函数
│   └── main.py                   # 服务入口
├── requirements.txt              # 依赖包
├── runtime.txt                   # Python 版本
├── Procfile                      # Railway 启动命令
└── README.md                     # 项目文档
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/link-archive-agent.git
cd link-archive-agent
```

### 2. 安装依赖

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入必要的配置
```

### 4. 本地运行

```bash
python src/main.py -m http -p 5000
```

访问 `http://localhost:5000/health` 检查服务状态。

## 📤 部署到 Railway

### 步骤 1: 上传代码到 GitHub

1. 在 GitHub 创建新仓库
2. 推送代码：

```bash
git init
git add .
git commit -m "Initial commit: 链接自动归档助手"
git branch -M main
git remote add origin https://github.com/yourusername/link-archive-agent.git
git push -u origin main
```

### 步骤 2: 在 Railway 创建项目

1. 访问 [Railway.app](https://railway.app/)
2. 使用 GitHub 账号登录
3. 点击 **"New Project"**
4. 选择 **"Deploy from GitHub repo"**
5. 选择你的仓库

### 步骤 3: 配置环境变量

在 Railway 项目设置中添加环境变量：

**必要的环境变量：**
- `FEISHU_APP_TOKEN`: 飞书多维表格的 app token
- `FEISHU_TABLE_ID`: 飞书多维表格的 table id

**自动配置的环境变量：**
- `PORT`: Railway 自动分配（无需手动设置）
- `COZE_WORKLOAD_IDENTITY_API_KEY`: Coze 平台自动注入
- `COZE_INTEGRATION_MODEL_BASE_URL`: Coze 平台自动注入

### 步骤 4: 部署

1. Railway 会自动检测 Python 项目
2. 自动安装依赖（`requirements.txt`）
3. 自动运行启动命令（`Procfile`）
4. 部署成功后获取域名，如：`https://your-app.railway.app`

### 步骤 5: 验证部署

访问健康检查接口：
```
https://your-app.railway.app/health
```

预期返回：
```json
{
  "status": "ok",
  "message": "Service is running"
}
```

## 🔗 接入飞书

### 1. 获取飞书多维表格信息

从飞书多维表格 URL 中提取：
- **App Token**: URL 中 `/wiki/` 后的部分
- **Table ID**: URL 中 `?table=` 后的部分

示例 URL：
```
https://example.feishu.cn/wiki/Wg4zwGaOKiJJ6OkI6SJc2avenxd?table=tblHoEKeUuiz2zet
```

- App Token: `Wg4zwGaOKiJJ6OkI6SJc2avenxd`
- Table ID: `tblHoEKeUuiz2zet`

### 2. 配置飞书机器人

1. 在飞书开放平台创建机器人应用
2. 配置事件订阅地址：
   ```
   https://your-app.railway.app/run
   ```
3. 启用消息接收权限
4. 发布应用并添加到群组

### 3. 测试集成

在飞书中发送消息：
```
帮我归档这个链接：https://mp.weixin.qq.com/s/xxx 这是一篇很有用的文章
```

Agent 会自动：
1. 解析链接和备注
2. 提取内容
3. 生成标签
4. 写入飞书多维表格

## 📊 API 接口

### 健康检查
```
GET /health
```

### 运行 Agent
```
POST /run
Content-Type: application/json

{
  "text": "帮我归档这个链接：https://...",
  "app_token": "your_app_token",
  "table_id": "your_table_id"
}
```

### 流式运行
```
POST /stream_run
Content-Type: application/json

{
  "text": "帮我归档这个链接：https://...",
  "app_token": "your_app_token",
  "table_id": "your_table_id"
}
```

### OpenAI 兼容接口
```
POST /v1/chat/completions
Content-Type: application/json

{
  "model": "agent",
  "messages": [
    {
      "role": "user",
      "content": "帮我归档这个链接：https://..."
    }
  ]
}
```

## 🎯 使用示例

### 示例 1: 小红书链接
```
帮我归档这个链接：http://xhslink.com/abc123 这是一个关于 AI 绘画的教程
```

### 示例 2: 微信公众号文章
```
https://mp.weixin.qq.com/s/xyz789 这篇文章介绍了 Python 编程技巧
```

## 📝 飞书多维表格字段要求

确保表格包含以下字段：

| 字段名称 | 字段类型 | 说明 |
|---------|---------|------|
| 标题 | 文本 | 文章标题 |
| 链接 | 网址 | 原始链接 |
| 正文摘要 | 文本 | 内容摘要 |
| 备注 | 文本 | 用户备注 |
| 场景标签 | 多选 | 自动生成的标签 |
| 来源平台 | 文本 | 小红书/微信公众号 |
| 收藏时间 | 日期时间 | 归档时间 |
| 图片 OCR 文字 | 文本 | 图片识别文字（可选） |

## 🔧 故障排查

### 1. 服务无法启动
- 检查 `requirements.txt` 是否完整
- 检查 Python 版本（需要 3.12+）
- 查看 Railway 日志

### 2. 链接解析失败
- 确认链接格式正确
- 检查网络连接
- 查看服务日志

### 3. 飞书写入失败
- 确认 App Token 和 Table ID 正确
- 检查表格字段是否完整
- 确认应用有编辑权限

## 📄 License

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📮 联系方式

如有问题，请提交 Issue 或联系维护者。
