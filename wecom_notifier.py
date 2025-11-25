"""
企业微信通知模块
通过企业微信机器人推送消息
"""

import requests
import json
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WeComNotifier:
    """企业微信通知器"""
    
    def __init__(self, webhook_url: str):
        """
        初始化通知器
        
        Args:
            webhook_url: 企业微信机器人webhook地址
        """
        self.webhook_url = webhook_url
    
    def send_markdown_message(self, content: str) -> bool:
        """
        发送Markdown格式消息
        
        Args:
            content: Markdown内容
            
        Returns:
            是否发送成功
        """
        try:
            payload = {
                "msgtype": "markdown",
                "markdown": {
                    "content": content
                }
            }
            
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            result = response.json()
            
            if result.get('errcode') == 0:
                logger.info("消息发送成功")
                return True
            else:
                logger.error(f"消息发送失败: {result}")
                return False
                
        except Exception as e:
            logger.error(f"发送消息时出错: {e}")
            return False
    
    def send_news_digest(self, news_list: List[Dict], title: str = "AI新闻速报") -> bool:
        """
        发送新闻摘要
        
        Args:
            news_list: 新闻列表
            title: 标题
            
        Returns:
            是否发送成功
        """
        if not news_list:
            logger.info("没有新闻需要推送")
            return True
        
        # 构建Markdown内容
        content_parts = [f"## 🤖 {title}\n"]
        content_parts.append(f"> 共发现 **{len(news_list)}** 条AI领域新动态\n")
        
        for i, news in enumerate(news_list, 1):
            content_parts.append(f"### {i}. {news['title']}")
            content_parts.append(f"**来源:** {news['source']} | **时间:** {news['time']}")
            
            if news.get('summary'):
                content_parts.append(f"> {news['summary']}")
            
            content_parts.append(f"[查看详情]({news['link']})\n")
        
        content_parts.append("---")
        content_parts.append("*由 AI News Radar 自动推送*")
        
        content = "\n".join(content_parts)
        
        # 企业微信markdown消息有长度限制（4096字节），需要分段发送
        max_length = 4000
        if len(content.encode('utf-8')) > max_length:
            # 分段发送
            logger.info(f"内容过长，分段发送")
            return self._send_in_chunks(news_list, title)
        else:
            return self.send_markdown_message(content)
    
    def _send_in_chunks(self, news_list: List[Dict], title: str) -> bool:
        """
        分段发送新闻
        
        Args:
            news_list: 新闻列表
            title: 标题
            
        Returns:
            是否全部发送成功
        """
        chunk_size = 5
        total_chunks = (len(news_list) + chunk_size - 1) // chunk_size
        
        all_success = True
        for i in range(0, len(news_list), chunk_size):
            chunk = news_list[i:i + chunk_size]
            chunk_num = i // chunk_size + 1
            
            chunk_title = f"{title} (第{chunk_num}/{total_chunks}部分)"
            success = self.send_news_digest(chunk, chunk_title)
            all_success = all_success and success
            
            # 避免发送过快
            if i + chunk_size < len(news_list):
                import time
                time.sleep(1)
        
        return all_success
    
    def send_error_notification(self, error_msg: str) -> bool:
        """
        发送错误通知
        
        Args:
            error_msg: 错误信息
            
        Returns:
            是否发送成功
        """
        content = f"## ⚠️ AI News Radar 运行异常\n\n{error_msg}"
        return self.send_markdown_message(content)

