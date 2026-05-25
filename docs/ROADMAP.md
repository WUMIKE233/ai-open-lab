# Roadmap / 路线图

AI Open Lab is growing into a bilingual teaching lab for practical AI engineering. The roadmap favors small, inspectable labs over a large framework.

AI Open Lab 正在成长为一个面向实用 AI 工程的双语教学实验室。路线图优先选择小而可读的实验，而不是大型框架。

## Phase 1: Teaching Foundation / 第一阶段：教学基础

Status: in progress.

状态：进行中。

- Bilingual README, contribution guide, and project notes. / 双语 README、贡献指南和项目说明。
- A hands-on learning path for prompt evaluation, mini RAG, and agent safety. / 面向提示词评测、迷你 RAG 和 Agent 安全的动手学习路径。
- Deterministic examples that run without API keys. / 无需 API key 即可运行的确定性示例。
- Clear first contribution ideas. / 清晰的首次贡献方向。

## Phase 2: Open Source Readiness / 第二阶段：开源成熟度

Status: in progress.

状态：进行中。

- GitHub Actions CI for tests and CLI smoke checks. / 用于测试和 CLI 冒烟检查的 GitHub Actions CI。
- Issue templates for bugs, feature requests, and good first issues. / 面向 bug、功能请求和首次贡献任务的 issue 模板。
- Pull request template with bilingual documentation and test reminders. / 带有双语文档和测试提醒的 PR 模板。
- Package metadata that points contributors to the repository, documentation, and issues. / 指向仓库、文档和 issue 的包元数据。

## Phase 3: Better Learning Artifacts / 第三阶段：更好的学习材料

Status: planned.

状态：计划中。

- Markdown or HTML reports for prompt evaluation. / 提示词评测的 Markdown 或 HTML 报告。
- Markdown reports for prompt evaluation are available with `eval-prompts --format markdown`. / 提示词评测已可通过 `eval-prompts --format markdown` 生成 Markdown 报告。
- More bilingual fixtures and knowledge-base examples. / 更多双语固件和知识库示例。
- Guided exercises for changing one module and one test at a time. / 引导式练习，每次修改一个模块和一个测试。
- Small benchmark fixtures for scanner precision. / 用于扫描器精度的小型基准固件。

## Phase 4: Optional Integrations / 第四阶段：可选集成

Status: planned.

状态：计划中。

- Optional model provider adapters while keeping the default path zero-dependency. / 可选模型服务适配器，同时保持默认路径零依赖。
- Optional embedding adapters for RAG experiments. / 面向 RAG 实验的可选嵌入适配器。
- SARIF output for safety scanning in CI. / 用于 CI 安全扫描的 SARIF 输出。
- Interactive examples or a lightweight demo site. / 交互式示例或轻量演示站点。

## Project Principles / 项目原则

- Teach the concept before adding abstraction. / 先讲清概念，再添加抽象。
- Keep the default path local, deterministic, and easy to test. / 保持默认路径本地、确定且易测试。
- Keep public docs bilingual. / 保持公开文档中英双语。
- Prefer small, reviewable pull requests. / 优先选择小而易审查的 pull request。
- Request maintainer review before deleting files or examples. / 删除文件或示例前请求维护者审核。
