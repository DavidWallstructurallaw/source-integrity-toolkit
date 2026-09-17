# DEPENDENCY_STRATEGY

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Target release | v0.1 |
| Phase / work unit | Phase 0 / Work Unit 10 |
| Revision | 0.1 |
| Date | 2026-09-17 |
| Status | PROPOSED FOR REVIEW; no dependency is installed by this document |
| Theory Owner | Xiangyu Guo |
| Technical Owner | Unassigned |
| License policy | Original engineering repository materials: Apache-2.0 |
| Runtime dependency target | Python standard library only |
| Cross-project dependency | None |
| Network/model dependency | None |
| Implementation / Phase 1 authorization | Not granted |

## 1. Purpose

This document selects a deliberately small dependency posture for v0.1. The product's first responsibility is reproducible structural analysis of a caller-supplied local bundle. Its core operations do not require a graph framework, dataframe system, web client, model SDK or database.

Dependency decisions must preserve the approved evidence semantics, offline boundary, bounded processing and Apache-2.0 repository policy. Convenience alone is insufficient reason to add a runtime package.

## 2. v0.1 runtime dependency decision

The reference runtime will target **CPython 3.11 or later and Python standard library only**.

No mandatory third-party runtime dependency is planned for v0.1.

Standard-library capabilities cover the required first-release work:

- JSON parsing and encoding;
- immutable/value-model implementation primitives;
- exact integers, `Fraction`/decimal presentation support where appropriate;
- graph adjacency structures and deterministic traversal;
- hashing;
- path/file/stat handling;
- monotonic clocks and cooperative cancellation checks;
- argument parsing;
- datetimes and time-zone-aware timestamps;
- safe text escaping primitives;
- unit-test support where necessary.

This decision is architectural rather than a claim that every implementation detail is already solved. If later implementation proves that a third-party runtime library is required to satisfy an approved contract safely, development must return to dependency review before adding it.

## 3. Explicitly excluded runtime dependency classes

v0.1 has no runtime dependency on:

- `requests`, HTTP clients or browser automation;
- OpenAI, Anthropic or other model SDKs;
- embedding/vector databases;
- NetworkX or another graph engine;
- pandas or dataframe frameworks;
- Pydantic or a generic validation framework;
- JSON Schema validation engines;
- databases, ORM layers or caches;
- template engines for Markdown;
- plugin/entry-point discovery frameworks;
- Recursive Integrity Toolkit or an `integrity-core` package;
- telemetry/crash-reporting SDKs.

These exclusions reduce hidden I/O, initialization side effects, semantic delegation and supply-chain surface. They do not prohibit a later separately approved optional integration.

## 4. Build and development dependencies

Runtime and development dependencies are treated separately.

### 4.1 Build backend

Phase 1 may select a conventional PEP 517 build backend. The recommended default is **setuptools** because the package has no compiled extension or unusual build pipeline requirement.

The Phase 1 plan must pin a minimum compatible build-tool version appropriate to its CI environment and verify its actual license/version before release. Build isolation must not create a runtime dependency.

### 4.2 Test runner

The recommended test-only dependency is **pytest**. The Work Unit 8 obligation set is large and benefits from parametrization, fixtures and failure localization.

Use of pytest is a development choice. The installed library must remain usable without pytest. Phase 1 must verify the actual selected version/license and keep it out of runtime requirements.

### 4.3 Linting and formatting

No external formatter, linter or static type checker is mandatory for the v0.1 architecture. Phase 1 may propose one developer tool if it materially improves CI and its license/version is reviewed. Such a tool cannot rewrite specification files or become a release-time dependency without an explicit plan change.

### 4.4 Coverage tooling

Coverage reporting is desirable but not a Phase 0 dependency commitment. Phase 1 may add coverage tooling after the test structure exists. Coverage percentage cannot substitute for satisfying the named SIT-VF/SIT-VG obligations.

## 5. Why no graph dependency

The graph operations required by the current specification are bounded and typed:

- construct view-specific adjacency from admitted assertions;
- deterministic traversal from finite seeds;
- find finite witnesses;
- detect typed cycles;
- retain unresolved terminals and coverage limitations.

A general graph library would not supply the product's epistemic rules. The risky parts are relation eligibility, scope, polarity, lifecycle, dimension and witness interpretation. Those rules remain project-owned even if a library were added.

Using standard-library data structures keeps the relation registry visible and avoids accidentally applying a generic algorithm to an invalid mixed-edge graph.

If performance evidence later shows the implementation cannot meet an approved resource contract, optimization should first profile and improve the bounded representation. A dependency change requires its own evidence and review.

## 6. Why no generic validation/model framework

The logical dossier has a strict domain contract and several intentionally non-generic rules:

- duplicate JSON keys need raw-input handling;
- a valid unresolved reference differs from a dangling ID;
- claim/artifact versions and typed endpoint compatibility matter;
- structural invalidity differs from semantic conflict;
- extensions are inert and closed-core behavior must remain explicit;
- resource guards apply before and during object construction.

Delegating these semantics to a broad object-validation framework would still require custom code while adding another interpretation layer. v0.1 therefore keeps the validator project-owned.

This does not prohibit generating a machine-readable schema later under an approved phase. Such a schema is an external contract artifact, not the sole source of runtime truth.

## 7. Determinism and environment isolation

The same normalized input, configuration and contract version must produce the same substantive result independent of dependency discovery or machine network state.

Therefore:

- environment variables cannot silently enable networking, models or plugins;
- package entry points cannot register analytical predicates;
- locale cannot change ordering or numeric semantics;
- system time cannot affect analytical results except explicitly recorded run metadata and resource timing;
- optional developer packages cannot change runtime meaning;
- an unavailable external executable cannot change a completed analytical result.

Sort order, deterministic iteration and canonical result assembly are implementation obligations owned by the project.

## 8. Dependency review gate

Any proposed new runtime dependency must include, before adoption:

1. exact package and intended version range;
2. reason the standard library cannot safely satisfy the approved contract;
3. owned module and trace responsibilities affected;
4. transitive dependency inventory;
5. license and notice obligations;
6. network, subprocess, plugin, telemetry and import-side-effect review;
7. resource/failure behavior;
8. deterministic/offline behavior evidence;
9. tests proving semantics do not change when the package reports an error;
10. rollback or removal plan.

A dependency cannot define source trust, independence, threat severity or another product meaning by default.

## 9. Versioning and pinning policy

Runtime package metadata should declare the supported Python lower bound and avoid an artificial upper bound unless an incompatibility is known.

Build/test dependencies should be constrained in project configuration and resolved reproducibly in CI. Release governance must inspect the actual resolved versions, licenses and included artifacts.

Security or compatibility upgrades can change dependency versions without changing analytical semantics. If an upgrade changes parsing, ordering, numeric behavior, error classification or report rendering, treat it as a behavioral change requiring contract regression tests.

## 10. Supply-chain and offline controls

Package installation is a build/deployment concern. Normal audit execution must not contact package indexes, update servers or dependency metadata services.

The release should not auto-install optional integrations on first run. No dynamic downloading of schemas, models, rule packs or source registries is permitted.

Developer tools and GitHub Actions may access package registries during authorized CI setup. That network use is separate from the runtime no-network claim and must not be presented as audited-source access.

## 11. License compatibility

The repository's own original engineering material is planned for Apache-2.0 under the approved WU9-C03 decision.

Each third-party build or test dependency still keeps its own license. Before a release or distributable bundle includes third-party material, release governance must record the actual dependency version and applicable notices.

The six theory papers are not software dependencies and retain their existing CC BY-NC-ND 4.0 notices. They should not be packaged into a wheel/source distribution by default.

## 12. Phase 1 dependency boundary

A later approved Phase 1 may create package metadata and CI scaffolding consistent with this strategy.

Phase 1 may declare the selected build backend and test-only dependencies. It may not add analytical runtime libraries merely because an empty module path exists.

No runtime package dependency should appear in the initial scaffold without a separately approved amendment to this document or its successor.

## 13. Dependency acceptance criteria

The strategy passes when:

- normal v0.1 execution has zero required third-party runtime packages;
- no dependency can perform source retrieval, model inference or plugin registration;
- graph and domain-validation semantics remain project-owned;
- build/test dependencies remain outside runtime requirements;
- dependency changes have a documented review gate;
- cross-project integration cannot create a hidden required dependency;
- license review occurs on actual selected third-party versions before release.

## 14. Review item and stop point

**WU10-C02** asks the owner to approve the standard-library-only runtime strategy, with setuptools proposed as build backend and pytest proposed as a test-only dependency for the later scaffold.

Approval records the dependency architecture. It does not install packages or authorize Phase 1.
