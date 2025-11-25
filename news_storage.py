"""
新闻存储模块
用于去重和记录已推送的新闻
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Set
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsStorage:
    """新闻存储器"""
    
    def __init__(self, storage_file: str = "data/news_history.json"):
        """
        初始化存储器
        
        Args:
            storage_file: 存储文件路径
        """
        self.storage_file = storage_file
        self.history = self._load_history()
    
    def _ensure_data_dir(self):
        """确保数据目录存在"""
        data_dir = os.path.dirname(self.storage_file)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def _load_history(self) -> Dict:
        """
        加载历史记录
        
        Returns:
            历史记录字典
        """
        if not os.path.exists(self.storage_file):
            return {
                'pushed_news': {},  # {news_id: timestamp}
                'last_check': None
            }
        
        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载历史记录失败: {e}")
            return {
                'pushed_news': {},
                'last_check': None
            }
    
    def _save_history(self):
        """保存历史记录"""
        try:
            self._ensure_data_dir()
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
            logger.info("历史记录已保存")
        except Exception as e:
            logger.error(f"保存历史记录失败: {e}")
    
    def is_news_pushed(self, news_id: str) -> bool:
        """
        检查新闻是否已推送
        
        Args:
            news_id: 新闻ID
            
        Returns:
            是否已推送
        """
        return news_id in self.history['pushed_news']
    
    def mark_as_pushed(self, news_id: str):
        """
        标记新闻为已推送
        
        Args:
            news_id: 新闻ID
        """
        self.history['pushed_news'][news_id] = datetime.now().isoformat()
    
    def mark_batch_as_pushed(self, news_list: List[Dict]):
        """
        批量标记新闻为已推送
        
        Args:
            news_list: 新闻列表
        """
        for news in news_list:
            self.mark_as_pushed(news['id'])
        self._save_history()
    
    def filter_new_news(self, news_list: List[Dict]) -> List[Dict]:
        """
        过滤出未推送的新闻
        
        Args:
            news_list: 新闻列表
            
        Returns:
            未推送的新闻列表
        """
        new_news = [
            news for news in news_list
            if not self.is_news_pushed(news['id'])
        ]
        logger.info(f"过滤后剩余 {len(new_news)} 条新新闻")
        return new_news
    
    def cleanup_old_history(self, days: int = 30):
        """
        清理旧的历史记录
        
        Args:
            days: 保留最近多少天的记录
        """
        cutoff = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff.isoformat()
        
        old_count = len(self.history['pushed_news'])
        self.history['pushed_news'] = {
            k: v for k, v in self.history['pushed_news'].items()
            if v >= cutoff_str
        }
        new_count = len(self.history['pushed_news'])
        
        logger.info(f"清理历史记录: {old_count} -> {new_count}")
        self._save_history()
    
    def update_last_check(self):
        """更新最后检查时间"""
        self.history['last_check'] = datetime.now().isoformat()
        self._save_history()
    
    def get_last_check(self) -> str:
        """获取最后检查时间"""
        return self.history.get('last_check', '从未检查')
    
    def get_stats(self) -> Dict:
        """
        获取统计信息
        
        Returns:
            统计信息
        """
        return {
            'total_pushed': len(self.history['pushed_news']),
            'last_check': self.get_last_check()
        }

