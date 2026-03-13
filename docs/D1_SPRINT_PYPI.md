# D1 Sprint — PyPI Publish Pipeline

**Phase:** 4 | **Repo:** reichert-science-intelligence/starguard-core  
**Prerequisite:** PHASE4_ROADMAP.md committed, local synced with remote main

---

## Overview

This sprint delivers the automated PyPI publish pipeline for starguard-core. A basic `publish.yml` workflow already exists; this sprint adds the TestPyPI dry-run gate, tightens tag semantics to `v4.*.*`, and validates end-to-end from tag push to `pip install`.

---

## Tasks

### T1 — PyPI account + API token

**Status:** Manual — cannot be automated in Cursor.

| Step | Action |
|------|--------|
| 1 | Confirm PyPI account exists at [pypi.org](https://pypi.org) |
| 2 | Generate API token scoped to `starguard-core` (Account Settings → API tokens) |
| 3 | Add token to GitHub repo: Settings → Secrets and variables → Actions → `PYPI_API_TOKEN` |

Run T1 in parallel while implementing T2–T3.

---

### T2 — pyproject.toml publish config

**Current state:** `[project]`, `[project.urls]`, and `[build-system]` (hatchling) are already present.

| Check | Verdict |
|-------|---------|
| `[project]` metadata (name, version, description, license, classifiers) | ✅ Present |
| `[build-system]` uses hatchling | ✅ Present |
| `[project.urls]` (Homepage, Documentation, Repository) | ✅ Present |

**Action:** Spot-check that `Documentation` URL matches the chosen hosting target (GitHub Pages or Read the Docs) once D2 is live. No code change required for this sprint.

---

### T3 — GitHub Actions release workflow

**Current state:** `.github/workflows/publish.yml` exists. It builds and publishes on any `v*` tag, but lacks a TestPyPI gate and `v4.*.*` enforcement.

| Requirement | Current | Target |
|-------------|---------|--------|
| Trigger | `v*` (all version tags) | `v4.*.*` only |
| TestPyPI dry-run | None | Run before live publish |
| Live publish | Direct | Only after TestPyPI succeeds |

**Steps to implement:**

1. Restrict trigger: `tags: ["v4.*.*"]` (or regex equivalent)
2. Add TestPyPI step: `twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
3. Gate: run TestPyPI step first; only proceed to PyPI publish if it succeeds
4. Ensure `PYPI_API_TOKEN` is used for both TestPyPI and PyPI (same token works for both when scoped)

---

### T4 — TestPyPI dry-run validation

**Decision:** Use `v4.5.0` as the first real release. No separate test tag — cleaner history, one less thing to delete.

**Purpose:** Prove the pipeline works. The workflow will run TestPyPI first (gate), then PyPI. `v4.5.0` serves as both validation and first production release.

| Step | Action |
|------|--------|
| 1 | Confirm pyproject.toml version is `4.5.0` |
| 2 | Add changelog entry for v4.5.0 (first PyPI release) |
| 3 | Commit, push, then: `git tag v4.5.0 && git push origin v4.5.0` |
| 4 | Confirm workflow runs TestPyPI step, then PyPI step, both green |
| 5 | Confirm package appears on [test.pypi.org](https://test.pypi.org) and [pypi.org](https://pypi.org/project/starguard-core) |
| 6 | Confirm `pip install starguard-core` resolves from production PyPI |

---

### T5 — Subsequent release (e.g. v4.6.0)

**Purpose:** Validate the pipeline for future releases.

| Step | Action |
|------|--------|
| 1 | Bump version to `4.6.0` in pyproject.toml |
| 2 | Add changelog entry for 4.5.0 → 4.6.0 |
| 3 | Commit, push, then: `git tag v4.6.0 && git push origin v4.6.0` |
| 4 | Confirm workflow completes green |
| 5 | Confirm `pip install starguard-core` resolves with updated version |

---

## Success Gate

- [ ] `PYPI_API_TOKEN` set in repo secrets
- [ ] `publish.yml` workflow updated (TestPyPI gate, `v4.*.*` trigger)
- [ ] TestPyPI dry-run passes
- [ ] `pip install starguard-core` resolves from production PyPI
- [ ] PyPI project page is public and metadata is correct

---

## Notes

| Item | Detail |
|------|--------|
| **T1** | Manual only; do in parallel with T2–T3 |
| **T4 / T5** | v4.5.0 is first real release; no separate test tag |
| **Changelog** | Version bump 4.5.0 → 4.6.0 is the first changelog entry; use towncrier or keep-a-changelog format per PHASE4_ROADMAP |
| **Existing workflow** | `publish.yml` is present; this sprint augments it rather than creating from scratch |
