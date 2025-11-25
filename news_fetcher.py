"""
AI新闻获取模块
从各种RSS源获取AI相关新闻
"""

import feedparser
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
from bs4 import BeautifulSoup
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsFetcher:
    """新闻获取器"""
    
    def __init__(self, sources: List[Dict], keywords: Optional[List[str]] = None):
        """
        初始化新闻获取器
        
        Args:
            sources: 新闻源配置列表
            keywords: 关键词列表，用于过滤
        """
        self.sources = [s for s in sources if s.get('enabled', True)]
        self.keywords = keywords or []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def fetch_rss_news(self, source: Dict) -> List[Dict]:
        """
        获取RSS源新闻
        
        Args:
            source: 新闻源配置
            
        Returns:
            新闻列表
        """
        news_list = []
        try:
            logger.info(f"正在获取 {source['name']} 的新闻...")
            feed = feedparser.parse(source['url'])
            
            for entry in feed.entries[:20]:  # 限制每个源最多20条
                try:
                    # 提取发布时间
                    published = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        published = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        published = datetime(*entry.updated_parsed[:6])
                    else:
                        published = datetime.now()
                    
                    # 提取摘要
                    summary = ""
                    if hasattr(entry, 'summary'):
                        # 清理HTML标签
                        soup = BeautifulSoup(entry.summary, 'html.parser')
                        summary = soup.get_text().strip()[:200]  # 限制长度
                    
                    news_item = {
                        'title': entry.title,
                        'link': entry.link,
                        'summary': summary,
                        'published': published,
                        'source': source['name'],
                        'id': entry.get('id', entry.link)
                    }
                    
                    # 关键词过滤
                    if self._match_keywords(news_item):
                        news_list.append(news_item)
                
                except Exception as e:
                    logger.warning(f"处理条目时出错: {e}")
                    continue
            
            logger.info(f"从 {source['name']} 获取到 {len(news_list)} 条新闻")
            
        except Exception as e:
            logger.error(f"获取 {source['name']} 失败: {e}")
        
        return news_list
    
    def _match_keywords(self, news_item: Dict) -> bool:
        """
        检查新闻是否匹配关键词
        
        Args:
            news_item: 新闻条目
            
        Returns:
            是否匹配
        """
        if not self.keywords:
            return True
        
        text = f"{news_item['title']} {news_item['summary']}".lower()
        
        for keyword in self.keywords:
            if keyword.lower() in text:
                return True
        
        return False
    
    def fetch_all_news(self, hours: int = 24) -> List[Dict]:
        """
        获取所有源的新闻
        
        Args:
            hours: 获取最近多少小时的新闻
            
        Returns:
            新闻列表
        """
        all_news = []
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        for source in self.sources:
            if source['type'] == 'rss':
                news = self.fetch_rss_news(source)
                # 过滤时间
                news = [n for n in news if n['published'] >= cutoff_time]
                all_news.extend(news)
        
        # 按时间排序，最新的在前
        all_news.sort(key=lambda x: x['published'], reverse=True)
        
        logger.info(f"共获取到 {len(all_news)} 条符合条件的新闻")
        return all_news
    
    def format_news_for_display(self, news_list: List[Dict]) -> List[Dict]:
        """
        格式化新闻用于显示
        
        Args:
            news_list: 新闻列表
            
        Returns:
            格式化后的新闻列表
        """
        formatted = []
        for news in news_list:
            formatted.append({
                'title': news['title'],
                'link': news['link'],
                'summary': news['summary'][:150] + '...' if len(news['summary']) > 150 else news['summary'],
                'source': news['source'],
                'time': news['published'].strftime('%Y-%m-%d %H:%M')
            })
        return formatted

