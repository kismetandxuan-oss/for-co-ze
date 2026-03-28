"""
飞书 Webhook 代理服务 - Railway 部署版
"""

import os
import json
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 从环境变量读取配置
COZE_API_TOKEN = os.getenv("COZE_API_TOKEN", "")
COZE_WEBHOOK_URL = os.getenv("COZE_WEBHOOK_URL", "https://kp2dz8j3vw.coze.site/feishu/webhook")

# 创建 FastAPI 应用
app = FastAPI(title="飞书 Webhook 代理服务")


@app.get("/")
async def root():
    """根路径"""
    return {"status": "ok", "service": "feishu-webhook-proxy"}


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "ok",
        "message": "Proxy service is running",
        "target_url": COZE_WEBHOOK_URL
    }


@app.get("/feishu/webhook")
async def feishu_webhook_get(challenge: str = None):
    """处理飞书 URL 验证（GET 请求）"""
    logger.info(f"收到飞书GET请求, challenge={challenge}")
    if challenge:
        return {"challenge": challenge}
    return {"status": "ok", "message": "Feishu webhook endpoint is ready"}


@app.post("/feishu/webhook")
async def feishu_webhook_post(request: Request):
    """处理飞书 Webhook 请求"""
    try:
        # 读取请求体
        body_bytes = await request.body()
        body_text = body_bytes.decode('utf-8')
        
        logger.info(f"收到飞书POST请求: {body_text[:200]}")
        
        # 解析JSON
        try:
            body = json.loads(body_text)
        except json.JSONDecodeError:
            logger.error("JSON解析失败")
            return JSONResponse(
                content={"error": "Invalid JSON"},
                status_code=400
            )
        
        # 处理飞书 URL 验证
        if body.get("type") == "url_verification":
            challenge = body.get("challenge", "")
            logger.info(f"飞书URL验证, 返回challenge: {challenge}")
            return {"challenge": challenge}
        
        # 转发到 Coze 服务
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {COZE_API_TOKEN}"
        }
        
        logger.info(f"转发到Coze: {COZE_WEBHOOK_URL}")
        
        response = requests.post(
            COZE_WEBHOOK_URL,
            json=body,
            headers=headers,
            timeout=30
        )
        
        logger.info(f"Coze响应: {response.status_code}")
        
        # 返回 Coze 的响应
        return JSONResponse(
            content=response.json() if response.text else {},
            status_code=response.status_code
        )
        
    except requests.exceptions.RequestException as e:
        logger.error(f"请求Coze失败: {e}")
        return JSONResponse(
            content={"error": f"Failed to connect to Coze: {str(e)}"},
            status_code=502
        )
    except Exception as e:
        logger.error(f"处理请求失败: {e}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )
