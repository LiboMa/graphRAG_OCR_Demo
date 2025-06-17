# GraphRAG + Knowledge Base + Neptune 医疗器械助手

## 项目概述
本文档概述了基于图检索增强生成(GraphRAG)系统的实现，用于创建智能医疗设备助手，重点关注血压计产品。

## 查询示例, Prompt Engineer

中文类型的查询：

1. 请你把你知道的所有的血压计型号列举给我，并且精确回答他们每个型号有什么优缺点？以及如何推荐给我？ 
2. 请你列举出所有的血压计型号，并且仔细的对比，帮我整理出他们的优缺点，以及如何在它们之中做出合适的选择？
3. 我想要了解所有的血压计的型号，以及他们的优缺点如何? 
4. 哪一款产品是有背光的?
5. 哪一款是有语音功能的？还有吗？
6. 哪些blood pressure monitors 带背光，哪些又带语音功能?
7. 请总结所有你知道的blood pressure monitors 的型号?

英文查询示例：
* What kind of model blood pressure monitors can you provide me?
* What are the pros and cons between them?

## Bedrock Agent的 Instructure Version 1

```yaml
请列出鱼跃牌所有可用的血压计型号，并提供以下具体信息：

## 必须包含的内容：
1. 每个型号的完整名称和产品代码
2. 按类别分组（如臂式、腕式、智能联网型等）
3. 针对每个型号提供：
   - 核心技术特点（如测量方式、精度等）
   - 3-5个主要优点
   - 1-3个可能的局限性
   - 适合的用户群体（如老年人、高血压患者、运动员等）
   - 价格区间

## 推荐标准：
提供基于以下因素的产品推荐：
- 用户年龄段和身体状况
- 使用频率需求
- 技术熟练程度
- 预算范围
- 是否需要数据同步和分析功能

## 回复格式：
请使用表格或结构化列表呈现比较信息，并在末尾提供一个简短的"如何选择合适血压计"的决策指南。

请只提供关于鱼跃牌血压计的官方确认信息，不要包含未经验证的数据或猜测。
```

## Bedrock Agent的 Instructure Version 2

你是一位专业的血压计客户服务代理，需要向客户提供精确的回答：

```yaml
You are a professional customer care services agent for blood pressure monitors. 
Provide precise answers to customers based on official product information.
```

## 实现步骤

1. **建立知识库 (Knowledge Base)**
   * GraphRAG + Neptune 数据库
   * RAG Vector + Opensearch - 常规方法

2. **文档处理**
   * 使用MineU开源工具将PDF转换为Markdown，以提高准确率
   * 文档存储位置: `s3://knowledgebase-graphrag-yuyue/markdown-data/`
   * 处理以下血压计说明书:
     - 鱼跃YE660C电子血压计(语音版)-中文说明书.pdf
     - 鱼跃YE670D电子血压计中文说明书.pdf
     - 鱼跃YE670E电子血压计中文说明书（语音+背光+360）.pdf
     - 鱼跃YE690C电子血压计-中文说明书.pdf
     - 鱼跃YE8100C电子血压计中文说明书.pdf
     - 鱼跃YE8900A电子血压计(语音款)中文说明书.pdf

3. **知识图谱构建**
   * 从处理后的文档中提取实体和关系
   * 在Neptune中构建综合知识图谱

4. **用户界面开发**
   * 创建Streamlit应用程序与Agent交互

## 产品型号特点

| 型号 | 特点 |
|------|------|
| YE660C | 语音功能 |
| YE670D | 标准型号 |
| YE670E | 语音功能 + 背光 + 360度显示 |
| YE690C | 标准型号 |
| YE8100C | 高级型号 |
| YE8900A | 语音功能 |

## 系统架构图

[此处添加架构图]

## 未来路线图

1. **多Agent协同**
   * 开发专门针对不同医疗设备类别的Agent
   * 实现Agent协调机制

2. **多模态能力**
   * 集成多模态Embedding模型，增加图片搜索功能
   * 启用视觉查询处理

3. **增强个性化**
   * 开发用户画像，提供更有针对性的推荐
   * 实现反馈机制，持续改进

## 参考链接

- [医疗设备助手微信文章](https://mp.weixin.qq.com/s/z7VxAGueILkJ1ptMKWTzOA)
- [When to use Graphs in RAG: A Comprehensive Analysis for Graph Retrieval-Augmented Generation](https://arxiv.org/pdf/2506.05690)
- [LightRAG](https://github.com/HKUDS/LightRAG)
- [ollama](https://github.com/ollama/ollama)
- [ollama, operation](https://translucentcomputing.github.io/kubert-assistant-lite/ollama.html)
- [OpenAI Compatiable URL](https://github.com/aws-samples/bedrock-access-gateway )
