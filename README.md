# ClaudeCode-for-eval

Run Claude Code CLI as an autonomous agent on [SWE-bench-Live](https://github.com/microsoft/SWE-bench-Live) tasks. The agent is given a bug description, explores the codebase inside a Docker sandbox, and produces a patch. The patch is then scored by the SWE-bench-Live evaluation harness.

## How it works

```
SWE-bench task (problem_statement)
        ↓
Docker container (pre-built repo snapshot)
        ↓
Claude Code CLI (explores code, writes fix, validates)
        ↓
git diff → preds.json
        ↓
evaluation.py → resolved / unresolved
```

## Setup

```bash
git clone https://github.com/lieexxli/ClaudeCode-for-eval --recursive
cd ClaudeCode-for-eval
pip install -r requirements.txt
pip install -r server/requirements.txt
```

Docker must be running and your user must have access to it.

## Configure

### Option 1 — Claude OAuth token (simplest)

Edit `config/claude-oauth.yaml` and fill in your token. Get it with:

```bash
cat ~/.claude/.credentials.json \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['claudeAiOauth']['accessToken'])"
```

### Option 2 — Any OpenAI-compatible API

Create `config/myconfig.yaml` (reference `config/default.yaml`). Set `model`, `api_key`, and `base_url`. Requests are routed through a local litellm proxy so Claude Code CLI doesn't need to know the actual provider.

## Run

```bash
python main.py \
    --config config/claude-oauth.yaml \
    --run-id my-run \
    --dataset lieeli/swetry1 \
    --split python
```

Or pass a local `.jsonl` file instead of a HuggingFace dataset name.

Predictions are saved to `logs/{model}/{run-id}/preds.json`.

## Evaluate

```bash
# inside the SWE-bench-Live repo
python -m evaluation.evaluation \
    --dataset lieeli/swetry1 \
    --patch_dir /path/to/preds.json \
    --output_dir logs/eval \
    --platform linux \
    --workers 1 \
    --overwrite 1
```

Results are saved to `logs/eval/results.json`.
