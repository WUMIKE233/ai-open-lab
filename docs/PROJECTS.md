# Project Notes

AI Open Lab contains three related but independent tools.

## Prompt Evaluation Kit

Goal: make prompt behavior testable with small JSONL fixtures.

Future ideas:

- weighted assertions
- semantic similarity hooks
- provider adapters for OpenAI-compatible APIs
- HTML or Markdown reports

## Mini RAG Search

Goal: explain retrieval-augmented generation concepts without hiding the retrieval logic behind a large framework.

Future ideas:

- persistent indexes
- chunking strategies
- metadata filters
- optional embedding-model adapters

## Agent Safety Scanner

Goal: provide a local, auditable rule engine for common prompt and tool-use risks.

Future ideas:

- configurable rule files
- allowlists for trusted internal prompts
- SARIF export for CI
- benchmark fixtures for scanner precision
