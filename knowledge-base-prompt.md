
## GraphRAG + Knowledgebase + Neptune based 医疗器械助手

## Chat PE

<!-- 1. 请你把所有的血压计型号列举给我，并且精确回答他们每个型号有什么优缺点？以及我如何选择？ -->
2. 请你把你知道的所有的血压计型号列举给我，并且精确回答他们每个型号有什么优缺点？以及如何推荐给我？ 
3. 请你列举出所有的血压计型号，并且仔细的对比，帮我整理出他们的优缺点，以及如果在它们之中做出合适的选择？
4. 我想要了解所有的血压计的型号，以及他们的优缺点如何? 
5. 哪一款产品是有背光的?
6. 哪一款是有语音功能的？还有吗？
7. 哪些blood presure monitors 带背光，哪些又带语音功能?
8. 请总结所有你知道的blood pressure monitors 的型号?

* what kind of model blood pressure monitors can you provide me?
* what's pros and cons between them?


4. ```yaml
claude 3.7 

请列出鱼悦牌所有可用的血压计型号，并提供以下具体信息：

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

请只提供关于鱼悦牌血压计的官方确认信息，不要包含未经验证的数据或猜测。




## Agent instruction

You are an professional customer care services agent for blook monitor, show the precise answers to customers.


## Impelmentation 步骤

1. 建立智识库 -> Knowledge-base 
   * GraphRAG + Neptune
   * RAG Vector + Opensearch - normal ones

2. 文件转换
使用MineU 开源工具将pdf转换为Markdown，以此来提高准确率，未来也可以做成工程化,文档放至 - s3://knowledgebase-graphrag-yuyue/markdown-data/
2. 使用同源文档，鱼跃血压计说明书不同型号包括：

   - YE660C (with voice function)
   - YE670D
   - YE670E
   - YE690C
   - YE8100C
   - YE8900A (with voice function)

* 鱼跃YE660C电子血压计(语音版)-中文说明书.pdf
* 鱼跃YE670D电子血压计中文说明书.pdf
* 鱼跃YE670E电子血压计中文说明书（语音+背光+360）.pdf
* 鱼跃YE690C电子血压计-中文说明书.pdf
* 鱼跃YE8100C电子血压计中文说明书.pdf
* 鱼跃YE8900A电子血压计(语音款)中文说明书.pdf


3. 开始建立Knowledgebase，和Agent

4. 创建Streamlint应用，访问Agent

## 架构图

   

## Future Roadmap
1. 多个Agent协同，
2. 每个Agent负责特定的医疗器械类型
3. 使用多模态Embedding 模型，增加图片搜索



### Reference link:

- https://mp.weixin.qq.com/s/z7VxAGueILkJ1ptMKWTzOA
- (When to use Graphs in RAG: A Comprehensive
Analysis for Graph Retrieval-Augmented Generation)[!https://arxiv.org/pdf/2506.05690]
