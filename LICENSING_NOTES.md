# LICENSING_NOTES

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Target release | v0.1 |
| Phase / work unit | Phase 0 / Work Unit 9 |
| Revision | 0.2 |
| Date | 2026-09-17 |
| Status | WU9-C03 APPROVED; Apache-2.0 selected for original engineering repository materials; license file not yet applied |
| Decision owner | Xiangyu Guo, subject to authority over each included work |
| Approval evidence | User instruction: `那就apache2.0吧` |
| Supersedes | Revision 0.1 split Apache-2.0 / CC BY 4.0 proposal |
| Existing source basis | `SPEC_AUDIT.md` source register; six supplied theory notices |
| Implementation / final Phase 0 approval | Neither is authorized by this decision |

## 1. Approved policy

WU9-C03 is resolved in favor of a single Apache License 2.0 policy for the project's newly authored engineering repository materials.

When the later scaffold phase applies the license, Apache-2.0 is intended to cover original project material whose rights are controlled by the licensor, including:

- software implementation, CLI and library code;
- build and maintenance tools;
- executable tests and fixture generators;
- machine-readable schemas and configuration;
- original reusable specifications and architecture documents;
- original explanatory engineering documentation;
- original prose test/oracle descriptions;
- original fictional evidence bundles, examples and synthetic fixture data.

The unified policy reduces license-boundary complexity inside the engineering repository. File type alone does not determine ownership or permission. Material that the project does not have authority to license remains outside the Apache-2.0 grant even when stored beside covered project files.

This Phase 0 decision records the selected policy. It does not yet create a root `LICENSE`, `NOTICE`, package metadata, SPDX headers or a released software distribution. Those repository artifacts belong to the separately approved scaffold phase after the Phase 0 baseline is completed and approved.

## 2. Materials excluded from the repository Apache-2.0 grant

| Material class | Treatment | Boundary |
|---|---|---|
| Six theory papers by Xiangyu Guo | Retain their displayed CC BY-NC-ND 4.0 notices | They are reference assets and are excluded from the normal engineering distribution unless separately authorized |
| Extracts, page images, translations or adaptations of the theory papers | Source-specific rights or separate permission | Inclusion in an Apache-licensed repository does not relicense them |
| Third-party code, documents, data, standards extracts, media or benchmark material | Preserve the applicable third-party license or permission | Review origin, version and distribution conditions before incorporation |
| User-supplied evidence dossiers | No toolkit license is applied | Auditing does not transfer ownership or authorize redistribution |
| Confidential identity mappings or protected-source material | No toolkit license is applied | Privacy and disclosure rules remain controlling |
| Input-derived portions of audit reports | Preserve the rights and disclosure limits of the supplied material | Tool-authored template text can be project material; embedded source expression is not automatically Apache-licensed |

The repository license must therefore be accompanied by clear exclusion language in later public-facing documentation. A root Apache-2.0 license cannot be described as relicensing every byte that may ever be processed by, linked from, or referenced by the toolkit.

## 3. Apache-2.0 reference and intended effect

Apache License 2.0 provides copyright permissions and a defined contributor patent grant subject to its conditions. Redistribution requires preservation of the license and applicable notices, and modified files must carry appropriate change notices. The patent grant and termination terms apply according to the standard license text.

Official reference:

- Apache Software Foundation, Apache License, Version 2.0: `https://www.apache.org/licenses/LICENSE-2.0.html`

The standard legal text controls. This specification records project policy and does not replace that text or provide a legal opinion about ownership, patent scope, fair use or a particular third-party asset.

The selected policy permits commercial adoption, modification and redistribution of the newly licensed engineering material under Apache-2.0. It does not modify the NC or ND conditions attached to the theory papers and does not grant commercial rights to evidence that the project does not own.

## 4. Theory-source register remains separate

The source identities recorded in `SPEC_AUDIT.md` remain controlling for theory provenance.

| Source ID | Reviewed work | Existing notice |
|---|---|---|
| SIL | The Source Integrity Layer: Presence × Integrity and the Governance of AI-Native Information Distribution | CC BY-NC-ND 4.0 |
| UIL | The Universal Inbreeding Law: Closure, Diversity Loss, Correlated Error, and Integrity Decay in Self-Organizing Systems | CC BY-NC-ND 4.0 |
| EC | Evaluation Closure: Benchmark Inbreeding and the Design of Open AI Evaluation | CC BY-NC-ND 4.0 |
| HDL | The Heat Death of Language: Reality-Coupled Information, Semantic Gradient Collapse, and the Source Integrity of AI | CC BY-NC-ND 4.0 |
| EBC | Entropy as a Structural Boundary Condition, Not a Causal Force | CC BY-NC-ND 4.0 |
| BVL | The Boundary Vacuum Law: Gradient, Boundary Failure, Topological Flow, and Pressure Capture in Social Systems | CC BY-NC-ND 4.0 |

Normal toolkit releases should use original engineering descriptions, citations and the traceability map rather than bundling theory PDFs, page screenshots or long extracts. The Apache-2.0 selection for the engineering repository does not alter those papers' existing notices.

## 5. Third-party material and user evidence

Before a third-party asset is incorporated into a distributable repository artifact, future release governance must record its origin, exact version or digest where practical, rights holder where known, license or permission basis, intended use, required notices and any modification or redistribution conditions.

A URL, source citation, public availability or successful audit does not itself establish a right to redistribute the underlying work. Real-world material must not be turned into an Apache-licensed fixture merely by changing names or formatting.

Tests of protected-data behavior should use independently constructed fictional canaries. User evidence may be represented through an authorized locator or protected attestation without being copied into a public example set.

Applying an Apache-licensed report template does not relicense the user's evidence. Any later report license statement must identify the portion actually covered by the project license and preserve source/input rights and disclosure restrictions.

## 6. Contributions and rights uncertainty

Future contributions should record that the contributor has authority to submit the covered material under Apache-2.0. Employer-controlled material, copied passages, third-party examples or assets with uncertain rights require review before inclusion.

AI-assisted drafting does not by itself establish originality or ownership. Project maintainers must continue to distinguish original engineering expression from copied theory or third-party expression before applying the repository license.

Project privacy, security and evidentiary rules are implementation and governance requirements. They are not added as extra downstream restrictions to the standard Apache-2.0 license.

## 7. Later scaffold requirements

After final Phase 0 approval and under the separately approved scaffold plan, the repository should implement this decision by creating and checking the appropriate release artifacts. At minimum, the scaffold plan should address:

| Release artifact / check | Required treatment |
|---|---|
| `LICENSE` | Standard Apache License 2.0 text |
| `NOTICE` | Project attribution and any notices that are actually required; no fabricated third-party notices |
| README license statement | State that original engineering repository materials are Apache-2.0, subject to clearly named exclusions |
| Package metadata | Use `Apache-2.0` consistently where package metadata applies |
| Specifications and fictional examples | Include them in the engineering Apache-2.0 scope unless an individual file carries an explicit separate notice |
| Theory sources | Exclude PDFs/full-text/page images from ordinary toolkit packages; preserve their CC BY-NC-ND 4.0 notices when referenced |
| Third-party materials | Preserve their own terms and list included items in the appropriate notice/rights record |
| User/runtime data | Never package it as project-licensed fixture material by default |
| Distribution inspection | Verify source archives, wheels, docs and examples rather than checking only the repository root |

No `LICENSE` file is created in Work Unit 9 because Phase 0 remains a specification phase.

## 8. Written licensing acceptance cases

| Case | Required result |
|---|---|
| W9-LIC01: Original executable test plus original fictional JSON dossier | Both fall under the later repository Apache-2.0 policy |
| W9-LIC02: Full HDL PDF is placed in an examples directory | Exclude it from the ordinary engineering distribution or handle it under its existing CC BY-NC-ND 4.0 terms and a separate rights decision |
| W9-LIC03: A private supplied dossier is audited successfully | No Apache-2.0 license, publication permission or ownership transfer attaches to the dossier |
| W9-LIC04: A diagram adapted from a theory paper is labeled Apache-2.0 | Do not accept that relicensing without an independent rights basis or specific permission |
| W9-LIC05: WU10 proposes a dependency | Review the actual dependency version, license and distribution role before adoption |
| W9-LIC06: This Apache-2.0 policy is approved while Phase 1 remains unauthorized | Record the policy now; wait for the authorized scaffold phase before creating `LICENSE`, `NOTICE` or package metadata |

These are documentation-level obligations. No runtime test, dependency review or legal clearance of a new asset is claimed here.

## 9. Decision record and remaining Work Unit 9 gates

**WU9-C03: APPROVED.** The owner selected Apache-2.0 for the project's original engineering repository materials through the instruction `那就apache2.0吧`. This supersedes revision 0.1's split Apache-2.0 / CC BY 4.0 recommendation.

WU9-C01 and WU9-C02 concern privacy/disclosure and bounded-processing controls. This license decision does not approve, reject or modify those separate proposals.

The next planned unit remains Work Unit 10 after the remaining Work Unit 9 package is accepted. Full Phase 0 approval and implementation authorization remain separate later actions.
