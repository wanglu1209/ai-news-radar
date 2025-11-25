# 📡 AI新闻源列表

本文档列出了所有预置的AI新闻RSS源，你可以根据需要在 `config.yaml` 中启用或禁用。

## 🇨🇳 中文AI媒体（3个）

| 名称 | RSS地址 | 说明 |
|------|---------|------|
| 机器之心 | https://www.jiqizhixin.com/rss | 国内领先的AI专业媒体，深度报道AI技术和产业 |
| AI前线（InfoQ） | https://www.infoq.cn/topic/ai/feed | InfoQ中文站的AI专栏，偏向技术实践 |
| 量子位 | https://www.qbitai.com/feed | 关注AI科技新闻和产业动态 |

## 🌍 国际科技媒体AI频道（7个）

| 名称 | RSS地址 | 说明 |
|------|---------|------|
| TechCrunch AI | https://techcrunch.com/category/artificial-intelligence/feed/ | 硅谷科技媒体，关注AI创业和产品 |
| The Verge AI | https://www.theverge.com/ai-artificial-intelligence/rss/index.xml | 科技新闻网站，报道AI产品和行业动态 |
| VentureBeat AI | https://venturebeat.com/category/ai/feed/ | 关注AI商业应用和企业技术 |
| MIT Technology Review AI | https://www.technologyreview.com/topic/artificial-intelligence/feed | MIT旗下，深度分析AI技术影响 |
| Ars Technica AI | https://feeds.arstechnica.com/arstechnica/technology-lab | 技术深度报道，包含AI相关内容 |
| Wired AI | https://www.wired.com/feed/tag/ai/latest/rss | 知名科技杂志，关注AI文化和社会影响 |
| AI News | https://www.artificialintelligence-news.com/feed/ | AI专门新闻聚合站 |

## 🏢 AI公司官方博客（10个）

| 名称 | RSS地址 | 说明 |
|------|---------|------|
| OpenAI Blog | https://openai.com/blog/rss/ | GPT系列模型更新，官方最新动态 ⭐ |
| Anthropic News | https://www.anthropic.com/news/rss.xml | Claude模型发布和研究成果 ⭐ |
| Google AI Blog | https://blog.google/technology/ai/rss/ | Gemini和Google AI产品更新 ⭐ |
| DeepMind Blog | https://deepmind.google/blog/rss.xml | 前沿AI研究，AlphaFold等项目 |
| Meta AI Blog | https://ai.meta.com/blog/rss/ | Llama系列开源模型发布 ⭐ |
| Microsoft AI Blog | https://blogs.microsoft.com/ai/feed/ | Copilot、Azure AI服务更新 |
| Hugging Face Blog | https://huggingface.co/blog/feed.xml | 开源模型、工具和社区动态 ⭐ |
| Cohere Blog | https://cohere.com/blog/rss.xml | 企业级AI模型和应用 |
| Mistral AI News | https://mistral.ai/news/rss/ | 欧洲AI新星，Mistral系列模型 |

⭐ = 强烈推荐，模型发布第一手信息

## 🎓 学术研究资源（3个）

| 名称 | RSS地址 | 说明 | 默认状态 |
|------|---------|------|----------|
| Papers with Code | https://paperswithcode.com/latest/rss | 最新AI论文+代码实现 | ✅ 启用 |
| arXiv AI (cs.AI) | http://export.arxiv.org/rss/cs.AI | AI领域论文预印本 | ⏸️ 禁用（量大）|
| arXiv ML (cs.LG) | http://export.arxiv.org/rss/cs.LG | 机器学习论文预印本 | ⏸️ 禁用（量大）|

💡 **提示**: arXiv源每天产出大量论文，建议只在需要时启用，并配合严格的关键词过滤。

## 👥 专业社区（2个）

| 名称 | RSS地址 | 说明 | 默认状态 |
|------|---------|------|----------|
| AI Alignment Forum | https://www.alignmentforum.org/feed.xml | AI安全和对齐讨论 | ✅ 启用 |
| LessWrong AI | https://www.lesswrong.com/feed.xml?view=community-rss&karmaThreshold=30 | 理性主义社区的AI讨论 | ⏸️ 禁用（内容较杂）|

## 🚀 AI产品资讯（1个）

| 名称 | RSS地址 | 说明 |
|------|---------|------|
| Product Hunt AI | https://www.producthunt.com/topics/artificial-intelligence.rss | 最新AI产品发布 |

---

## 📊 信息源统计

- **总计**: 26个RSS源
- **默认启用**: 22个
- **默认禁用**: 4个（学术论文源，可按需启用）
- **语言分布**: 英文 23个 | 中文 3个
- **更新频率**: 
  - 高频（每天多次）: 科技媒体、学术源
  - 中频（每周数次）: AI公司博客
  - 低频（不定期）: 专业社区

## 🎯 推荐配置方案

### 方案一：全面监控（适合深度关注AI的用户）
```yaml
# 启用所有源 + 关键词过滤
# 建议检查间隔: 6小时
# 每次推送上限: 10-15条
```

### 方案二：重点关注（适合想了解重大事件的用户）
只启用官方博客源：
- OpenAI、Anthropic、Google AI、Meta AI、Hugging Face
- 建议检查间隔: 12小时
- 不需要关键词过滤（官博更新本身就不频繁）

### 方案三：技术研究（适合研究人员）
- 官方博客 + Papers with Code + AI Alignment Forum
- 建议检查间隔: 6小时
- 关键词：具体技术方向（transformer、diffusion等）

### 方案四：产品导向（适合产品经理）
- TechCrunch + The Verge + Product Hunt AI + 官方博客
- 建议检查间隔: 12小时
- 关键词：launch、release、product

## 🔧 如何添加自定义RSS源

在 `config.yaml` 中添加：

```yaml
news_sources:
  - name: "你的RSS源名称"
    url: "https://example.com/feed.xml"
    type: "rss"
    enabled: true
```

### 如何找到RSS源？

1. **寻找RSS图标**: 很多网站在页面底部或侧边栏有RSS图标
2. **URL规律**: 常见RSS地址格式
   - `/rss`
   - `/feed`
   - `/feed.xml`
   - `/rss.xml`
   - `/atom.xml`
3. **使用RSS发现工具**: 浏览器插件如"RSS Feed Reader"可以自动检测
4. **查看网页源代码**: 搜索 `application/rss+xml` 或 `application/atom+xml`

### 推荐的其他AI信息源

- Reddit r/MachineLearning (需要通过第三方RSS服务)
- Hacker News AI标签 (可以用 hnrss.org)
- Twitter Lists (需要通过nitter等服务转RSS)
- Discord/Slack频道 (需要webhook桥接)

---

**💡 提示**: 启用源越多，信息越全面，但也更容易信息过载。建议先从推荐配置开始，逐步调整。

