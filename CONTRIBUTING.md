# Contributing / 参与贡献

Thanks for helping improve AI Open Lab.

感谢你帮助改进 AI Open Lab。

AI Open Lab is a bilingual teaching project for practical AI engineering. Contributions should make the labs easier to learn, run, test, or extend.

AI Open Lab 是一个面向实用 AI 工程的双语教学项目。贡献应帮助学习者更容易理解、运行、测试或扩展这些实验。

## Development / 开发环境

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
python -m unittest discover -s tests
```

The project currently uses only the Python standard library. Please keep new dependencies out of the core package unless there is a clear teaching benefit.

项目目前只使用 Python 标准库。除非有明确的教学价值，请不要向核心包添加新依赖。

## Pull Request Checklist / Pull Request 检查清单

- Keep changes focused on one feature, lesson, or bug fix. / 让改动聚焦于一个功能、一个课程点或一个 bug 修复。
- Add or update tests for behavior changes. / 行为变化需要新增或更新测试。
- Update examples or docs when CLI behavior changes. / CLI 行为变化时，请同步更新示例或文档。
- Keep public docs bilingual. / 保持公开文档中英双语。
- Do not commit secrets, API keys, private prompts, or production logs. / 不要提交密钥、API key、私有提示词或生产日志。
- If a change deletes files or examples, request maintainer review first. / 如果改动涉及删除文件或示例，请先请求维护者审核。

## Code Style / 代码风格

Prefer small modules, typed functions, readable errors, and deterministic examples.

优先使用小模块、类型标注函数、可读错误信息和确定性示例。

Good contributions should help readers answer:

好的贡献应帮助读者回答：

- What AI engineering concept does this teach? / 这在教授哪个 AI 工程概念？
- Which command shows the behavior? / 哪条命令可以展示这个行为？
- Which test protects it? / 哪个测试可以保护这个行为？
- How can another contributor extend it? / 其他贡献者如何继续扩展？

## Good First Contributions / 适合首次贡献的方向

- Add prompt-eval cases for summarization, refusal, or citation behavior. / 为摘要、拒答或引用行为添加提示词评测用例。
- Add safety scanner rules with focused tests. / 添加带有针对性测试的安全扫描规则。
- Improve RAG snippets or add small knowledge-base examples. / 改进 RAG 片段或添加小型知识库示例。
- Add bilingual lesson notes, exercises, or expected outputs. / 添加双语课程笔记、练习或预期输出。

## GitHub Remote Note / GitHub Remote 提醒

This local checkout has a remote named `ai-open-lab` for the Python teaching lab. Use that remote for publishing this project.

当前本地仓库中，名为 `ai-open-lab` 的 remote 对应该 Python 教学实验室。发布本项目时请使用该 remote。
