# REQ-F-065: Pipeline Exit Code Propagation

**Tier:** Framework-Automatic | **Priority:** P0

**Source:** [§56 Exit Code Masking in Shell Pipelines](../challenges/01-critical-ecosystem-runtime-agent-specific/56-high-pipeline-exit-masking.md)

**Addresses:** Severity: High / Token Spend: Medium / Time: Low / Context: Low

---

## Description

When the framework invokes multi-stage shell pipelines internally, it MUST use `set -o pipefail` (or language-level equivalent) so that a failure in any stage of the pipeline propagates as the pipeline's exit code. The framework MUST NOT use the pattern `cmd | other_cmd` without capturing intermediate exit codes. For language runtimes that do not support `pipefail` natively, the framework MUST use explicit pipe handling that checks each stage's exit code. The framework MUST document this behavior in its subprocess API and warn (at framework startup) if the calling shell does not have `pipefail` set.

## Acceptance Criteria

- A pipeline where the first stage fails exits with the first stage's non-zero code, not 0.
- The framework's subprocess API raises an error for any pipeline stage failure, not just the last.
- A pipeline `cmd1 | cmd2` where `cmd1` exits 1 and `cmd2` exits 0 results in overall exit 1.
- Framework startup emits a warning when `pipefail` is not set in the parent shell environment.
