# P2-W01 CI transition review

Revision 0.1. Scope: PHASE_2_PLAN.md section 7. Status: candidate; hosted evidence pending at initial submission.

## Retained toolchain and permissions

No package version, Python minor, runner family or action revision is changed. The selected action definitions were re-read from the official repositories at their exact commits during this unit:

| Action | Retained commit | Re-read action.yml blob |
|---|---|---|
| actions/checkout | 3d3c42e5aac5ba805825da76410c181273ba90b1 | 5b0524f730db83f9513c18ab31a6c086c7239076 |
| actions/setup-python | 5fda3b95a4ea91299a34e894583c3862153e4b97 | df6c8235b476652b6402d31d92a2a89cdea74bb9 |
| actions/upload-artifact | 043fb46d1a93c77aae656e7c1c64a875d1fc6a0a | 7cb4d1e81db55320b41217e1a78a1a46e3d2baef |

The inherited dependency-review/install function executes unchanged from its exact hash-pinned prior source. It checks selected versions, actual downloaded wheel bytes and PyPI metadata, non-yanked status, notices, vendored metadata, installation and dependency consistency. Direct choices remain setuptools 84.0.0 and pytest 9.1.1; the prior resolved support set remains iniconfig 2.3.0, packaging 25.0, pluggy 1.6.0, pygments 2.20.0, with colorama 0.4.6 on Windows. No transitive or direct version is silently substituted.

Repository permissions stay `contents: read`; persist-credentials stays false. No secrets, elevated trigger, cache, subprocess shell expression from source/PR text, reusable third-party workflow, networked auditor or auto-publish/merge action is added. The four existing OS/minor combinations, 25-minute timeout, fail-fast false and fourteen-day verification-artifact retention remain.

## Enumerated migration

The existing workflow path stays `.github/workflows/phase1-ci.yml`. Display labels, concurrency group and artifact names now identify Phase 2. Checkout fetch-depth changes from 1 to 0 so the driver can inspect exact prior commit archives and the migrated tests can execute only their immutable historical assertions. This adds developer Git-history availability; it grants no product access and uploads no source archive.

The six migrated test files use a closed, hash-verified historical test loader. The loader accepts only fixed test paths, verifies source bytes against the independently pinned composed entry manifest, suppresses the old direct-main dispatcher and supplies no network/mutable-ref fallback. Its execution authority is developer test code, never a dossier, source locator, arbitrary callback or product import. All 194 collected historical test identities remain required.

The original twenty workflow-policy/JUnit tests are inherited unchanged. The new policy validates each enumerated migration delta, then checks the original closed policy. New transition tests exercise the added invariants. Exact result/collection matching, failures/skips and subtest accounting remain inherited and controlling.

## Stage and file authority

The runner event provides a separately validated work-unit context: exact `phase2/p2-wNN` for PRs, or one explicit `SIT-Phase-Unit: P2-WNN` footer for a main push. The actual head and base SHA are checked. Candidate policy must match the context and cannot advance it. The context does not authenticate conversational approval; work-unit execution and merge still require the owner.

The pinned plan supplies closed per-unit path lists. CI compares the actual base-to-head delta against the current list and rejects deletions/renames. It verifies every resolved intake hash against actual local Git archives, then protects current files outside the cumulative authorized lists. Product guards separately protect 48 paths and all unpromoted modules; W01 permits no product promotion.

Collection includes all present scaffold/security/contract/unit/integration directories. Every present test file must collect, all 194 original node IDs must remain, and raw JUnit must cover exactly the collected IDs. No skip, xfail, ignore-failure or count-only success is accepted. New test totals are determined by real collection, not set in advance.

## Primary reference and limits

GitHub's official secure-use guidance was checked for minimum token permissions and immutable full-commit pins: `https://docs.github.com/en/actions/reference/security/secure-use`. Pytest's official node-ID and collect-only documentation was checked for collection identity semantics: `https://docs.pytest.org/en/9.0.x/example/markers.html`.

These sources support narrow tooling choices. No complete fresh audit of all vendor source, new supply-chain certification or vulnerability-database clearance is claimed. The selected actions must resolve and every required step must pass on the actual W01 head. Actual runner images, patch versions, packages, run/job/artifact IDs and failures are recorded after execution. Phase 2 input/schema/analysis/native functionality remains unimplemented in W01.
