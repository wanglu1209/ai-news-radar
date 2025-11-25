"""
AI新闻雷达主程序
"""

import yaml
import os
import sys
import logging
from datetime import datetime
from news_fetcher import NewsFetcher
from wecom_notifier import WeComNotifier
from news_storage import NewsStorage

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config(config_path: str = 'config.yaml') -> dict:
    """加载配置文件"""
    if not os.path.exists(config_path):
        logger.error(f"配置文件不存在: {config_path}")
        logger.info("请复制 config.yaml.example 为 config.yaml 并填写配置")
        sys.exit(1)
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"加载配置文件失败: {e}")
        sys.exit(1)


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("AI News Radar 启动")
    logger.info(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    # 加载配置
    config = load_config()
    
    # 从环境变量或配置文件获取webhook
    webhook_url = os.getenv('WECOM_WEBHOOK') or config.get('wecom_webhook')
    if not webhook_url or webhook_url == 'YOUR_KEY_HERE':
        logger.error("未配置企业微信Webhook地址")
        logger.info("请在config.yaml中配置或设置WECOM_WEBHOOK环境变量")
        sys.exit(1)
    
    # 初始化各模块
    storage = NewsStorage()
    fetcher = NewsFetcher(
        sources=config.get('news_sources', []),
        keywords=config.get('keywords', [])
    )
    notifier = WeComNotifier(webhook_url)
    
    try:
        # 获取配置的检查间隔
        check_hours = config.get('push_settings', {}).get('check_interval_hours', 6)
        max_items = config.get('push_settings', {}).get('max_items_per_push', 10)
        
        logger.info(f"开始获取最近 {check_hours} 小时的AI新闻...")
        
        # 获取新闻
        all_news = fetcher.fetch_all_news(hours=check_hours)
        
        if not all_news:
            logger.info("未获取到任何新闻")
            storage.update_last_check()
            return
        
        # 过滤已推送的新闻
        new_news = storage.filter_new_news(all_news)
        
        if not new_news:
            logger.info("没有新的未推送新闻")
            storage.update_last_check()
            return
        
        # 限制推送数量
        if len(new_news) > max_items:
            logger.info(f"新闻数量 ({len(new_news)}) 超过限制，仅推送最新的 {max_items} 条")
            new_news = new_news[:max_items]
        
        # 格式化新闻
        formatted_news = fetcher.format_news_for_display(new_news)
        
        # 推送到企业微信
        logger.info(f"准备推送 {len(formatted_news)} 条新闻...")
        success = notifier.send_news_digest(formatted_news)
        
        if success:
            # 标记为已推送
            storage.mark_batch_as_pushed(new_news)
            logger.info("✅ 新闻推送成功！")
        else:
            logger.error("❌ 新闻推送失败")
        
        # 更新检查时间
        storage.update_last_check()
        
        # 清理旧记录
        storage.cleanup_old_history(days=30)
        
        # 输出统计信息
        stats = storage.get_stats()
        logger.info(f"统计信息: 累计推送 {stats['total_pushed']} 条新闻")
        
    except Exception as e:
        logger.error(f"运行出错: {e}", exc_info=True)
        try:
            notifier.send_error_notification(f"运行异常: {str(e)}")
        except:
            pass
        sys.exit(1)
    
    logger.info("=" * 60)
    logger.info("AI News Radar 运行完成")
    logger.info("=" * 60)


if __name__ == '__main__':
    main()

