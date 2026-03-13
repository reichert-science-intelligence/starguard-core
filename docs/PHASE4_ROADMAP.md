# Phase 4 Roadmap — SDK Distribution + Public Docs

**Repository:** reichert-science-intelligence/starguard-core  
**Prerequisite:** Phase 3 Engineering Hardening (v4.5.0, 132 tests, 99.02% coverage)  
**Goal:** Transform starguard-core from a GitHub library into a published, documented Python package that can be installed from PyPI and explored via public documentation.

---

## Scope Decision

PyPI publish and public docs are treated as a **single compound deliverable** — not two phases, but one shippable finish line. Both artifacts reinforce each other: the package gives installers something to run, and the docs give evaluators something to read. Splitting them would defer credibility without reducing scope.

---

## Deliverables

### D1 — PyPI Publish Pipeline

| Component | Description |
|-----------|-------------|
| **Release workflow** | GitHub Actions workflow triggered on tag push → publish to PyPI |
| **Version enforcement** | Semantic versioning: only `v4.x.x`-style tags accepted |
| **Changelog automation** | Automated changelog generation via towncrier or keep-a-changelog |
| **Safety gate** | TestPyPI dry-run gate before live publish to catch packaging/config issues |

The pipeline must be fully automated: tagging a release should not require manual uploads or token juggling.

### D2 — Public Docs Site

| Component | Description |
|-----------|-------------|
| **Framework** | MkDocs Material (not Sphinx — faster build, more modern UX) |
| **API reference** | mkdocstrings auto-generated from existing docstrings |
| **Migration guide** | Documented path from 3.x → 4.x for existing consumers |
| **Hosting** | GitHub Pages or Read the Docs |
| **URL target** | `starguard-core.readthedocs.io` (or equivalent public URL) |

Docs must be publicly accessible without authentication. The migration guide is essential for anyone upgrading from v3.

---

## Deferred (Phase 5+)

| Phase | Scope |
|-------|-------|
| **Phase 5** | Consumer integration (AuditShield, Desktop, Mobile E2E tests) |
| **Phase 6** | Observability / OpenTelemetry |
| **Phase 6** | Performance benchmarks |

These items remain in the backlog; Phase 4 success does not depend on them.

---

## Success Gate

- [ ] `pip install starguard-core` resolves from PyPI
- [ ] Docs URL is live and publicly accessible
- [ ] Release workflow triggers on tag push (e.g. `v4.6.0`)
- [ ] Changelog entry exists for v4.5.0 → v4.6.0

---

## Rationale (for Cursor context)

| Priority | Rationale |
|----------|-----------|
| **PyPI publish** | Highest portfolio credibility signal remaining. Anyone can install without cloning; `pip install` is the industry-standard entry point. |
| **Docs site** | Technical decision-makers click documentation during due diligence. No docs = no confidence. |
| **May 2026 deadline** | Visible artifacts matter more than internal engineering depth for portfolio and stakeholder visibility. |
| **Observability / perf** | Valuable as engagement accelerators in later phases, but not portfolio signals for Phase 4. |
