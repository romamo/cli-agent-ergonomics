# REQ-F-042: Log Rotation in Framework Logger

**Tier:** Framework-Automatic | **Priority:** P3

**Source:** [§30 Undeclared Filesystem Side Effects](../challenges/05-high-environment-and-state/30-medium-filesystem-side-effects.md)

**Addresses:** Severity: Medium / Token Spend: Low / Time: Low / Context: Low

---

## Description

The framework's internal logger MUST automatically rotate log files when they exceed a configurable maximum size (default: 100 MB) and MUST retain a configurable maximum number of rotated files (default: 5). The framework MUST prune log files older than a configurable maximum age (default: 30 days). These defaults MUST be configurable via framework-level configuration, not requiring per-command implementation.

## Acceptance Criteria

- A log file that exceeds the size limit is rotated and a new file is started.
- Rotated files beyond the retention count are deleted automatically.
- Log files older than the maximum age are deleted on framework startup.
- Disk usage from framework logs is bounded even across unlimited invocations.
