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

Edit `config/claude-oauth.yaml` and fill in your token:

```bash
# get your token
cat ~/.claude/.credentials.json | python3 -c "import sys,json; print(json.load(sys.stdin)['claudeAiOauth']['accessToken'])"
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
