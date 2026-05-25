# Project Notes / 项目说明

AI Open Lab contains three related teaching labs. Each lab is intentionally small, local-first, and easy to inspect.

AI Open Lab 包含三个互相关联的教学实验。每个实验都刻意保持小巧、本地优先，并且便于阅读源码。

## Prompt Evaluation Kit / 提示词评测工具

Goal: make prompt behavior testable with small JSONL fixtures.

目标：用小型 JSONL 固件让提示词行为可测试。

Learners practice:

学习者将练习：

- turning expected behavior into deterministic checks / 将预期行为转化为确定性检查
- separating test data from evaluation logic / 将测试数据与评测逻辑分离
- reading machine-friendly JSON reports / 阅读机器友好的 JSON 报告

Future ideas:

未来方向：

- weighted assertions / 加权断言
- semantic similarity hooks / 语义相似度扩展点
- provider adapters for OpenAI-compatible APIs / OpenAI 兼容 API 的服务适配器
- HTML or Markdown reports / HTML 或 Markdown 报告

## Mini RAG Search / 迷你 RAG 检索

Goal: explain retrieval-augmented generation concepts without hiding the retrieval logic behind a large framework.

目标：解释检索增强生成的核心概念，而不是把检索逻辑隐藏在大型框架后面。

Learners practice:

学习者将练习：

- loading local Markdown and text files / 加载本地 Markdown 和文本文件
- tokenizing documents and queries / 对文档和查询分词
- ranking documents with TF-IDF and cosine similarity / 使用 TF-IDF 和余弦相似度排序文档
- returning snippets that are useful for downstream prompts / 返回可用于下游提示词的片段

Future ideas:

未来方向：

- persistent indexes / 持久化索引
- chunking strategies / 分块策略
- metadata filters / 元数据过滤
- optional embedding-model adapters / 可选嵌入模型适配器

## Agent Safety Scanner / Agent 安全扫描器

Goal: provide a local, auditable rule engine for common prompt and tool-use risks.

目标：为常见提示词风险和工具使用风险提供本地、可审计的规则引擎。

Learners practice:

学习者将练习：

- writing focused regular-expression rules / 编写聚焦的正则表达式规则
- mapping findings to categories and severities / 将发现映射到类别和严重级别
- using exit codes for CI-style guardrails / 使用退出码构建 CI 风格的防护栏
- balancing useful warnings against false positives / 平衡有效警告与误报

Future ideas:

未来方向：

- configurable rule files / 可配置规则文件
- allowlists for trusted internal prompts / 可信内部提示词白名单
- SARIF export for CI / 面向 CI 的 SARIF 导出
- benchmark fixtures for scanner precision / 用于扫描精度的基准固件

## Open Source Readiness / 开源成熟度

The first milestone is bilingual teaching content. Later milestones should improve project trust and contributor experience.

第一个里程碑是双语教学内容。后续里程碑应提升项目可信度和贡献者体验。

Planned improvements:

计划改进：

- GitHub issue and pull request templates / GitHub issue 与 pull request 模板
- continuous integration for tests and CLI smoke checks / 针对测试和 CLI 冒烟检查的持续集成
- more guided good first issues / 更多有引导性的首次贡献 issue
- richer reports and optional integrations / 更丰富的报告与可选集成
