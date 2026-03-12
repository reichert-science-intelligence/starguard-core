# starguard-core Architecture

**Version:** 4.x (frozen API — additions permitted, removals require v5.0.0)
**Python:** 3.11+
**Test count:** 279 | **Coverage:** 90%+
**Install:** `pip install starguard-core>=4.0.0,<5.0.0`

---

## Repository Layout
starguard-core/
├── src/
│   └── starguard_core/
│       ├── init.py          ← top-level exports + StarGuardClient
│       ├── client.py            ← StarGuardClient (async, all 11 domain modules)
│       ├── auth/
│       │   ├── validator.py     ← validate_api_key(), validate_api_key_sync()
│       │   ├── features.py      ← is_feature_enabled(), Tier enum
│       │   └── leads.py         ← capture_lead()
│       ├── radv/
│       │   ├── calculator.py    ← score_exposure()
│       │   ├── scenarios.py     ← default_scenario()
│       │   ├── models.py        ← RadvScenario, RadvResult
│       │   └── gaps.py          ← HCC severity thresholds
│       ├── hcc/
│       │   ├── raf.py           ← compute_raf_batch()
│       │   ├── gaps.py          ← identify_chronic_gaps()
│       │   └── revenue.py       ← compute_revenue_opportunity()
│       ├── hedis/
│       │   ├── predictor.py     ← predict_closure_batch()
│       │   ├── interventions.py ← build_intervention_plan()
│       │   └── measures.py      ← measure registry (update annually post-CMS specs)
│       ├── stars/
│       │   ├── trajectory.py    ← project_trajectory_batch()
│       │   ├── impact.py        ← compute_bonus_threshold_impact(), QBP thresholds
│       │   ├── cutpoints.py     ← CMS cut-point registry (update annually)
│       │   ├── models.py        ← StarMeasure, PlanStarProfile, TrajectoryResult
│       │   └── scenarios.py     ← default_stars_scenario()
│       ├── ingest/
│       │   ├── ingest.py        ← ingest(), IngestDomain, get_template_csv()
│       │   └── models.py        ← IngestionResult, IngestResult
│       ├── phi/
│       │   ├── deidentify.py    ← deidentify_rows()
│       │   └── detector.py      ← is_phi_column()
│       ├── compound/
│       │   └── view.py          ← run_compound_view()
│       ├── multiplan/           ← Enterprise tier only
│       │   ├── analysis.py      ← run_multiplan_analysis()
│       │   └── benchmark.py     ← peer_benchmark()
│       ├── billing/
│       │   ├── checkout.py      ← create_checkout_session()
│       │   └── webhook.py       ← handle_stripe_webhook()
│       └── audit/
│           ├── logger.py        ← log_event()
│           └── controls.py      ← get_controls_summary()
├── tests/
│   ├── test_auth.py
│   ├── test_radv.py
│   ├── test_hcc.py
│   ├── test_hedis.py
│   ├── test_stars.py
│   ├── test_ingest.py
│   ├── test_phi.py
│   ├── test_compound.py
│   ├── test_multiplan.py
│   ├── test_billing.py
│   ├── test_audit.py
│   ├── test_client.py
│   └── test_v400.py            ← 4.x shim removal + async gate
├── docs/
│   ├── api.md
│   ├── v4-migration.md
│   └── changelog.md
├── pyproject.toml
├── ARCHITECTURE.md             ← this file
└── .github/
└── workflows/
└── ci.yml

---

## Public API Surface (Frozen 4.x)

### Auth
```python
from starguard_core.auth.validator import validate_api_key, validate_api_key_sync
from starguard_core.auth.features  import is_feature_enabled
from starguard_core.auth.leads     import capture_lead
```

### RADV
```python
from starguard_core.radv import score_exposure, default_scenario
```

### HCC
```python
from starguard_core.hcc import compute_raf_batch, identify_chronic_gaps, compute_revenue_opportunity
```

### HEDIS
```python
from starguard_core.hedis import predict_closure_batch, build_intervention_plan
```

### Stars
```python
from starguard_core.stars import project_trajectory_batch, compute_bonus_threshold_impact
```

### Ingest
```python
from starguard_core.ingest import ingest, IngestDomain, get_template_csv
```

### PHI
```python
from starguard_core.phi import deidentify_rows, is_phi_column
```

### Compound
```python
from starguard_core.compound import run_compound_view
```

### Multiplan (Enterprise)
```python
from starguard_core.multiplan import run_multiplan_analysis, peer_benchmark
```

### Billing
```python
from starguard_core.billing import create_checkout_session, handle_stripe_webhook
```

### Audit
```python
from starguard_core.audit import log_event, get_controls_summary
```

### StarGuardClient (async high-level)
```python
from starguard_core import StarGuardClient

client = StarGuardClient("pro-MYKEY")
auth   = await client.authenticate(feature="radv_calculator")
```

---

## Tier Map

| Module | Free | Pro | Enterprise |
|---|---|---|---|
| auth | ✅ | ✅ | ✅ |
| ingest | ✅ | ✅ | ✅ |
| phi | ✅ | ✅ | ✅ |
| radv | summary only | ✅ | ✅ |
| hcc | summary only | ✅ | ✅ |
| hedis | gap counts only | predictions + interventions | ✅ |
| stars | current ratings only | trajectory + cut-points | ✅ |
| compound | — | ✅ | ✅ |
| multiplan | — | — | ✅ |
| billing | ✅ | ✅ | ✅ |
| audit | — | — | ✅ |

---

## Key Design Constraints

- **OPA binary:** Pinned v0.70.0 — do not upgrade without Sprint gate review
- **Async-first:** `validate_api_key()` is async; use `validate_api_key_sync()` for sync contexts
- **Annual update files:** `hedis/measures.py`, `stars/cutpoints.py` — update after CMS spec release each year
- **Single-source truth:** CMS demographic weights ONLY in `radv/calculator.py`; HCC severity thresholds ONLY in `radv/gaps.py`; recapture rate ONLY in `hcc/revenue.py`; closure probability weights ONLY in `hedis/predictor.py`; revenue per Star point ONLY in `stars/interventions.py` and `stars/impact.py`; QBP bonus thresholds ONLY in `stars/impact.py`
- **4.x API freeze:** Removals require v5.0.0 and DeprecationWarning cycle in 4.x first

---

## Downstream Consumers

| App | Import pattern | Port | HuggingFace Space |
|---|---|---|---|
| AuditShield Live | `from starguard_core import ...` | 8000 | rreichert-auditshield-live.hf.space |
| StarGuard Desktop | `from starguard_core import ...` | 8080 | rreichert-starguard-desktop.hf.space |
| StarGuard Mobile | `from starguard_core import ...` | 8090 | rreichert-starguardai.hf.space |

StarGuard Mobile must be launched with `shiny run app.app:app` from the `Artifacts/` directory.

---

## Version History (highlights)

| Version | Notes |
|---|---|
| 4.5.0 | Current stable. 12 modules, 279 tests, 90%+ coverage, frozen 4.x API |
| 4.0.0 | async-first, StarGuardClient, 3.x shims removed |
| 1.5.0 | Public API freeze declaration, CycloneDX SBOM, OpenAPI spec |

---
