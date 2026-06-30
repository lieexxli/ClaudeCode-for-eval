import json

from utils.docker_runtime import (
    CMD_OUTPUT_PS1_BEGIN,
    CMD_OUTPUT_PS1_END,
    CmdOutputMetadata,
    Runtime,
)


def _ps1_block() -> str:
    payload = {
        "exit_code": 0,
        "username": "root",
        "hostname": "container",
        "working_dir": "/repo",
        "py_interpreter_path": "/usr/bin/python",
    }
    return CMD_OUTPUT_PS1_BEGIN + json.dumps(payload) + CMD_OUTPUT_PS1_END + "\n"


def test_ps1_matching_preserves_trailing_blank_diff_context_line():
    diff_output = (
        "diff --git a/f.py b/f.py\n"
        "@@ -1,3 +1,4 @@\n"
        " ctx1\n"
        "+added\n"
        " ctx2\n"
        " \n"
    )
    pane_content = _ps1_block() + diff_output + _ps1_block()

    matches = CmdOutputMetadata.matches_ps1_metadata(pane_content)
    output = Runtime._combine_outputs_between_matches(None, pane_content, matches)

    assert len(matches) == 2
    assert CmdOutputMetadata.from_ps1_match(matches[-1]).exit_code == 0
    assert " ctx2\n \n" in output
