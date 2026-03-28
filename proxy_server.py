"""
飞书 Webhook 代理服务
用于解决 Coze 平台需要鉴权但飞书不支持自定义 Header 的问题

部署说明：
1. 将此文件部署到不需要鉴权的平台（如 Railway, Render, Vercel 等）
2. 配置环境变量：
   - COZE_API_TOKEN: 你的 Coze API Token
   - COZE_WEBHOOK_URL: Coze 服务的飞书 Webhook 地址
3. 将此服务的地址配置到飞书事件订阅中

使用方法：
- 本地测试：python proxy_server.py
- 部署到云平台：参考平台文档
"""

import os
import json
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import requests
import uvicorn

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 从环境变量读取配置
COZE_API_TOKEN = os.getenv("COZE_API_TOKEN", "")
COZE_WEBHOOK_URL = os.getenv("COZE_WEBHOOK_URL", "https://kp2dz8j3vw.coze.site/feishu/webhook")

app = FastAPI(title="飞书 Webhook 代理服务")
@app.get("/feishu/webhook")
async def feishu_url_verification(challenge: str = None):
    """
    处理飞书 URL 验证（GET 请求方式）
    飞书有时会通过 GET 请求进行 URL 验证
    """
    if challenge:
        logger.info(f"飞书 GET 验证，返回 challenge: {challenge}")
        return {"challenge": challenge}
    return {"status": "ok", "message": "Feishu webhook endpoint is ready"}

@app.post("/feishu/webhook")
async def proxy_feishu_webhook(request: Request):
    """
    代理飞书 Webhook 请求到 Coze 服务
    
    自动添加 Authorization 头，解决飞书不支持自定义 Header 的问题
    """
    try:
        # 获取原始请求体
        body = await request.json()
        
        logger.info(f"收到飞书请求: {json.dumps(body, ensure_ascii=False)[:200]}")
        
        # 处理飞书 URL 验证
        if body.get("type") == "url_verification":
            challenge = body.get("challenge", "")
            logger.info(f"飞书 URL 验证，返回 challenge: {challenge}")
            return {"challenge": challenge}
        
        # 转发到 Coze 服务
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {COZE_API_TOKEN}"
        }
        
        logger.info(f"转发请求到 Coze: {COZE_WEBHOOK_URL}")
        
        response = requests.post(
            COZE_WEBHOOK_URL,
            json=body,
            headers=headers,
            timeout=30
        )
        
        # 返回 Coze 的响应
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Coze 响应: {json.dumps(result, ensure_ascii=False)[:200]}")
            return result
        else:
            logger.error(f"Coze 返回错误: {response.status_code} - {response.text}")
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Coze service error: {response.text}"
            )
            
    except json.JSONDecodeError as e:
        logger.error(f"JSON 解析错误: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    
    except requests.exceptions.RequestException as e:
        logger.error(f"请求 Coze 服务失败: {e}")
        raise HTTPException(status_code=502, detail=f"Failed to connect to Coze service: {str(e)}")
    
    except Exception as e:
        logger.error(f"未知错误: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "ok",
        "message": "Proxy service is running",
        "target_url": COZE_WEBHOOK_URL
    }


if __name__ == "__main__":
    # 检查配置
    if not COZE_API_TOKEN:
        logger.warning("⚠️  COZE_API_TOKEN 未配置，请设置环境变量或在代码中填写")
        logger.warning("   示例: export COZE_API_TOKEN=ylh_your_token_here")
    
    # 使用动态端口（Railway/Render等平台需要）
    port = int(os.getenv("PORT", 8000))
    
    logger.info(f"🚀 启动代理服务")
    logger.info(f"   目标地址: {COZE_WEBHOOK_URL}")
    logger.info(f"   监听端口: {port}")
    
    # 启动服务（生产环境关闭reload）
    uvicorn.run(
        "proxy_server:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )
