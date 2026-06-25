# ClaudeCode-for-eval

Benchmark ClaudeCode against SWE-bench tasks. Runs Claude Code CLI inside each task's Docker container and collects the resulting patch for evaluation.

## Setup

```bash
git clone https://github.com/lieexxli/ClaudeCode-for-eval --recursive
cd ClaudeCode-for-eval
pip install -r requirements.txt
pip install -r server/requirements.txt
```

Make sure Docker is running and accessible.

## Configuration

Create a config file (do NOT commit it — it contains credentials):

### Option 1: Claude Code OAuth Token (Recommended)

Get your token from `~/.claude/.credentials.json` after logging in with `claude login`.

```yaml
# config/myrun.yaml
model:
  model: 'claude-sonnet-4-6'
  oauth_token: 'sk-ant-oat01-...'

agent:
  max_step: 50
  timeout: 300
  workers: 1
  tools:
    - Glob
    - Grep
    - Bash
    - Read
    - Edit
    - Write
    - TodoWrite
  user_prompt: |-
    You are given a code repository in the current directory (pwd && ls ./).
    The bug description is:
    {description}
    =================================================
    You task is to fix the bug with the following steps:
    (1) explore the source codes to find relevant files.
    (2) write test cases to reproduce the bug.
    (3) edit the source codes to fix the bug.
    (4) rerun your written test cases to validate that the bug is fixed. If not, go back to explore the source codes and fix the codes again.
    (5) remember to delete the test cases you write at last; if you modified the regression tests folder, git restore it.
    =================================================
    Notes:
    (1) Please do not commit your edits. We will do it later.
    (2) In our setting, each of your response must contain exactly one text content and one tool call. If you want to submit your result, just output one reponse with only text content and without tool call -- a response without tool call means stop and submission. If you have not finished, each of your response must have one tool call to make the session continue.
```

### Option 2: Any LLM via OpenAI-compatible API (litellm proxy)

Routes Claude Code CLI through a local litellm proxy, so any model works.

```yaml
# config/myrun.yaml
model:
  model: 'openai/gpt-4o'      # any litellm model name
  api_key: 'sk-...'
  base_url: 'https://api.openai.com/v1'  # or any compatible endpoint

agent:
  max_step: 50
  timeout: 300
  workers: 1
  tools: [Glob, Grep, Bash, Read, Edit, Write, TodoWrite]
  user_prompt: |-
    ...same as above...
```

### Option 3: Azure OpenAI

```yaml
model:
  model: 'azure/gpt-4o'
  # configure azure credentials in server/server.py::start_from_azure_openai
```

## Run

```bash
python main.py \
    --config config/myrun.yaml \
    --run-id my-experiment \
    --dataset lieeli/swetry1 \     # HuggingFace dataset name
    --split python
```

Or with a local jsonl file:

```bash
python main.py \
    --config config/myrun.yaml \
    --run-id my-experiment \
    --dataset path/to/instances.jsonl
```

Results are saved to `logs/{model}/{run-id}/preds.json`.

## Evaluate

Use [SWE-bench-Live](https://github.com/microsoft/SWE-bench-Live) to score the predictions:

```bash
python -m evaluation.evaluation \
    --dataset lieeli/swetry1 \
    --patch_dir logs/claude-sonnet-4-6/my-experiment/preds.json \
    --output_dir logs/eval \
    --platform linux \
    --workers 1 \
    --overwrite 1
```

Results are saved to `logs/eval/results.json`.
