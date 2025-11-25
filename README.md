# AI News Radar 🤖📡

一个自动化的AI新闻监控系统，帮助你第一时间了解AI领域的最新动态。系统会自动抓取多个权威AI资讯源，并通过企业微信机器人推送到你的手机。

## ✨ 特性

- 🌐 **多源抓取**: 支持多个AI资讯网站（机器之心、InfoQ、TechCrunch、OpenAI等）
- 🎯 **智能过滤**: 基于关键词智能过滤，只推送你关心的内容
- 🔄 **自动去重**: 智能记录已推送新闻，避免重复推送
- ⏰ **定时监控**: 通过GitHub Actions实现定时检查，无需自己部署服务器
- 📱 **企业微信推送**: 直接推送到企业微信，随时随地接收消息
- 🎨 **美观排版**: Markdown格式，阅读体验优秀

## 📦 快速开始

### 1. Fork本仓库

点击右上角的 Fork 按钮，将本仓库复制到你的GitHub账号下。

### 2. 配置企业微信机器人

1. 在企业微信群中添加一个机器人
2. 获取机器人的 Webhook 地址（格式类似：`https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxx`）
3. 在你的GitHub仓库中配置 Secret：
   - 进入仓库的 `Settings` > `Secrets and variables` > `Actions`
   - 点击 `New repository secret`
   - Name: `WECOM_WEBHOOK`
   - Value: 粘贴你的webhook地址

### 3. 自定义配置（可选）

如果需要自定义新闻源和关键词：

1. 复制 `config.yaml.example` 为 `config.yaml`
2. 根据需要修改配置：
   - 添加/删除新闻源
   - 修改关键词列表
   - 调整检查间隔和推送数量
3. 提交到仓库

### 4. 启用GitHub Actions

1. 进入仓库的 `Actions` 标签
2. 点击 "I understand my workflows, go ahead and enable them"
3. 等待定时任务自动运行，或手动触发测试

## 📋 配置说明

### 新闻源配置

系统预置了 **30+** 个优质AI新闻源，分为以下几类：

#### 📰 中文AI媒体
- 机器之心、AI前线（InfoQ）、量子位

#### 🌍 国际科技媒体AI频道
- TechCrunch AI、The Verge AI、VentureBeat AI
- MIT Technology Review AI、Ars Technica AI、Wired AI

#### 🏢 AI公司官方博客
- **OpenAI Blog** - GPT系列最新动态
- **Anthropic News** - Claude模型更新
- **Google AI / DeepMind** - Gemini和研究进展
- **Meta AI Blog** - Llama系列发布
- **Microsoft AI Blog** - Copilot和Azure AI
- **Hugging Face Blog** - 开源模型和工具
- **Cohere、Mistral AI** - 新兴AI公司动态

#### 🎓 学术研究资源
- Papers with Code - 最新论文和代码
- arXiv cs.AI / cs.LG - 论文预印本（可选）

#### 👥 专业社区
- AI Alignment Forum - AI安全和对齐
- Product Hunt AI - 最新AI产品

📝 **所有RSS源都可以在 `config.yaml` 中自由启用/禁用**

### 关键词过滤

系统会根据配置的关键词过滤新闻，预置关键词包括：
- GPT, Claude, Gemini
- 大模型, LLM, AI
- 机器学习, 深度学习
- 升级, 发布
- 等等...

### 定时任务

默认每6小时检查一次（北京时间 8:00, 14:00, 20:00, 2:00）。

可以在 `.github/workflows/news-monitor.yml` 中修改 cron 表达式：

```yaml
schedule:
  - cron: '0 */6 * * *'  # 每6小时
  # - cron: '0 */3 * * *'  # 每3小时
  # - cron: '0 9,18 * * *'  # 每天9点和18点
```

## 🏗️ 项目结构

```
ai-news-radar/
├── main.py                 # 主程序入口
├── news_fetcher.py         # 新闻获取模块
├── wecom_notifier.py       # 企业微信推送模块
├── news_storage.py         # 新闻存储和去重模块
├── requirements.txt        # Python依赖
├── config.yaml.example     # 配置文件模板
├── .github/
│   └── workflows/
│       └── news-monitor.yml # GitHub Actions工作流
├── data/
│   └── news_history.json   # 新闻历史记录（自动生成）
└── README.md               # 项目文档
```

## 🔧 本地开发

如果你想在本地测试：

```bash
# 克隆仓库
git clone https://github.com/your-username/ai-news-radar.git
cd ai-news-radar

# 安装依赖
pip install -r requirements.txt

# 复制配置文件
cp config.yaml.example config.yaml

# 编辑配置文件，填入你的webhook地址
vim config.yaml

# 运行
python main.py
```

## 📱 推送效果预览

推送到企业微信的消息格式如下：

```
## 🤖 AI新闻速报
> 共发现 3 条AI领域新动态

### 1. OpenAI发布GPT-5
**来源:** OpenAI Blog | **时间:** 2025-11-25 10:30
> OpenAI今天发布了最新的GPT-5模型，性能提升显著...
[查看详情](https://...)

### 2. Claude 4震撼发布
**来源:** Anthropic News | **时间:** 2025-11-25 09:15
> Anthropic推出了Claude 4，在多项基准测试中...
[查看详情](https://...)

---
*由 AI News Radar 自动推送*
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

如果你发现了好的AI新闻源，欢迎分享。

## 📝 常见问题

### Q: 信息源有多少？都是什么语言的？

A: 系统预置了 **30+** 个RSS源：
- **英文源 25+** 个：国际主流科技媒体 + AI公司官博 + 学术社区
- **中文源 3个**：机器之心、InfoQ AI前线、量子位

默认全部启用，你可以在 `config.yaml` 中自由选择。建议：
- 想要全面资讯：全部启用 + 设置关键词过滤
- 只想要重大事件：只启用官方博客（OpenAI、Anthropic等）
- 关注学术：启用 Papers with Code 和 arXiv

### Q: 如何调整推送频率？

A: 修改 `.github/workflows/news-monitor.yml` 中的 `cron` 表达式。

### Q: 消息太多怎么办？

A: 可以在 `config.yaml` 中：
- 精简新闻源（禁用某些源，比如关闭学术论文源）
- 优化关键词列表（更精确的关键词）
- 减少 `max_items_per_push` 的值
- 增加 `check_interval_hours` 的值（比如改为12小时）

### Q: 如何添加钉钉/飞书推送？

A: 可以参考 `wecom_notifier.py`，添加对应的推送类。钉钉和飞书的webhook格式类似。

### Q: GitHub Actions为什么没有运行？

A: 检查：
1. Actions是否已启用
2. Secret `WECOM_WEBHOOK` 是否已配置
3. 查看Actions日志排查错误

### Q: 能否部署到自己的服务器？

A: 当然可以！使用crontab定时运行 `main.py` 即可。

## 📄 许可证

MIT License

## 🌟 Star History

如果这个项目对你有帮助，请给个⭐️吧！

---

**Made with ❤️ for AI enthusiasts**
