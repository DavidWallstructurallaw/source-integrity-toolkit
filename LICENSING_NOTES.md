# LICENSING_NOTES

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Target release | v0.1 |
| Phase / work unit | Phase 0 / Work Unit 9 |
| Revision | 0.1 |
| Date | 2026-09-17 |
| Status | PROPOSED LICENSE POLICY; no license is applied by this proposal |
| Decision owner | Xiangyu Guo, subject to authority over each included work |
| Repository baseline | `bfebc1095ff000f816e21fecf34df32debe6727b` |
| Review item | WU9-C03 |
| Current authority | Draft and publish this specification; no blanket relicensing or runtime release |
| Existing source basis | SPEC_AUDIT source register; six supplied theory notices |
| External reference scope | Official Apache and Creative Commons license text only |

## 1. Purpose and current status

PLAN Work Unit 9 requires separate treatment of software, reusable specifications, example data, theory papers and third-party source material. SIT-D015 explicitly reserved this decision. Recursive Integrity Toolkit's license and earlier assistant suggestions do not select the license of this independent project.

This document proposes a file-class policy for later adoption. It does not grant a new license, retroactively relicense historical snapshots, declare the public repository to be a released open-source package, or change any paper's existing notice. No `LICENSE`, `NOTICE`, package metadata or license header is created in this work unit. Their implementation belongs to a separately approved scaffold phase after the relevant owner decisions.

The source papers support provenance, accountability and source return. They do not establish a software licensing scheme. The explanations of standard license terms in §3 are limited external reference checks; the material classification, approval procedure and release checklist below are proposed project policy. This is not a legal opinion about ownership, fair use, privacy compliance or any particular third-party asset.

## 2. Recommended separation of materials

| Material class | Proposed later license treatment | Boundaries |
|---|---|---|
| Original software implementation, CLI/library glue, build tools and executable tests | Apache-2.0 | Applies only to included contributions whose rights are controlled or properly licensed |
| Original machine-readable schemas and software configuration | Apache-2.0 | Classify explicitly; do not label a whole mixed repository with one ambiguous expression |
| Original reusable specifications, explanatory documentation and prose test/oracle descriptions | CC-BY-4.0 | Embedded third-party passages, images and existing papers remain separately identified |
| Original fictional evidence bundles and standalone synthetic fixture data | CC-BY-4.0 | A synthetic label does not authorize copied real records; executable fixture generators follow the software class |
| Theory papers and their full-text extracts, page images or translations | Retain their source-specific rights; exclude from the normal toolkit distribution | No transfer to the code/specification license by association |
| Third-party code, documentation, data, standards extracts or media | Preserve their own licenses/permissions and distribution conditions | Approval and a provenance/rights record precede incorporation |
| User input dossiers and confidential identity mappings | No toolkit license is applied | Auditing or storing a record does not claim its ownership or authorize redistribution |
| User-generated audit reports | No blanket license over embedded user/source material | Tool-authored template text and input-derived content remain distinguishable |

This is a file-class policy, not dual licensing of every file. A schema with code-like configuration and a fictional JSON evidence bundle may share an extension while belonging to different classes. A future manifest must identify actual paths after WU10 fixes the architecture.

The recommendation permits commercial adoption and modification of the project's newly licensed software, specifications and fictional examples, subject to their actual license terms. That product-policy choice does not loosen the theory papers' notices or promise commercial rights to third-party evidence. WU9-C03 must be explicitly accepted before it is implemented.

## 3. Limited external license-reference check

The following official texts were consulted on 2026-09-17. Their legal text controls; these brief notes explain the proposed choices and do not replace it.

### 3.1 Apache-2.0

Apache License 2.0 §§2-4 provides copyright permissions and a defined contributor patent grant, subject to its conditions. Redistribution requires the license, change notices and relevant retained notices; an included NOTICE has its own carry-forward treatment. Sections 6-8 address trademarks, warranty and liability. The patent grant is limited to covered contributor claims and has a litigation-termination condition. It supplies no general clearance of third-party patents. [EXT-L01]

### 3.2 CC-BY-4.0

CC BY 4.0 permits sharing and adaptation, including commercial uses, with attribution, license identification and modification notices as applicable. It does not authorize additional restrictions that defeat the licensed rights. The legal code distinguishes the licensor's controlled copyright/database rights from privacy, publicity, patent and trademark rights. Compliance with a copyright license therefore does not establish that publishing a personal-data dossier is permissible. [EXT-L02]

### 3.3 Existing CC-BY-NC-ND-4.0 theory notices

The six reviewed PDFs display CC BY-NC-ND 4.0 notices. Under that license, permitted sharing is limited to noncommercial use, and the license does not authorize sharing adapted material. Its exceptions-and-limitations provision and permitted technical modifications must be considered separately. A rights holder may grant additional permissions; this work unit records none. Do not automatically treat a translation, edited paper, diagram adaptation or extracted collection as newly licensed toolkit material. [EXT-L03; SPEC_AUDIT §2]

### Official references

- EXT-L01: Apache Software Foundation, Apache License, Version 2.0, §§2-9 and application guidance. `https://www.apache.org/licenses/LICENSE-2.0.html`
- EXT-L02: Creative Commons, Attribution 4.0 International, legal code, §§1-6. `https://creativecommons.org/licenses/by/4.0/legalcode`
- EXT-L03: Creative Commons, Attribution-NonCommercial-NoDerivatives 4.0 International, legal code, §§1-6. `https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode`

No current national-law analysis, standards-compliance review or dependency compatibility audit was performed. No exact third-party dependency has been selected in this unit.

## 4. Theory-source register and attribution

The existing SPEC_AUDIT §2 supplies complete filenames, version observations, page counts and SHA-256 values. Retain those identities rather than inferring a new canonical version from filename suffixes or current publication metadata.

| Source ID | Reviewed work | Displayed notice / version observation |
|---|---|---|
| SIL | The Source Integrity Layer: Presence × Integrity and the Governance of AI-Native Information Distribution | CC BY-NC-ND 4.0; copyright 2026; no numbered cover revision |
| UIL | The Universal Inbreeding Law: Closure, Diversity Loss, Correlated Error, and Integrity Decay in Self-Organizing Systems | CC BY-NC-ND 4.0; copyright 2026; v2 in supplied filename |
| EC | Evaluation Closure Benchmark Inbreeding and the Design of Open AI Evaluation | CC BY-NC-ND 4.0; cover 2026; no numbered cover revision |
| HDL | The Heat Death of Language: Reality-Coupled Information, Semantic Gradient Collapse, and the Source Integrity of AI | CC BY-NC-ND 4.0; cover August 2026, Version 2.0 |
| EBC | Entropy as a Structural Boundary Condition, Not a Causal Force | CC BY-NC-ND 4.0; preserve cover copyright 2025 and the separate 2026 original-publication revision note |
| BVL | The Boundary Vacuum Law: Gradient, Boundary Failure, Topological Flow, and Pressure Capture in Social Systems | CC BY-NC-ND 4.0; copyright 2026; v2 in supplied filename |

The author named in these sources is Xiangyu Guo. Project attribution may identify that theory provenance without declaring that every software or documentation contribution has the same author. Attribution must not imply endorsement by a cited standards body, journal, software foundation or unrelated contributor.

Normal public releases should contain original engineering descriptions, source references and the traceability map, not bundled theory PDFs, screenshots, extracted full texts, fonts or previous conversation archives. Any later inclusion of source expression requires an item-specific rights decision. Citation alone is not treated as redistribution permission, and using a theoretical idea is not automatically classified as copying a whole paper. The proposed policy requires distinguishing those cases rather than making a blanket legal determination.

## 5. Third-party material and input-derived reports

Before including a third-party asset in the repository, a maintainer must record its origin, exact version or digest, rights holder where known, license/permission basis, intended use, permitted modifications/distribution, required notices and decision owner. A relevant source license must be reviewed for the actual use. A link, downloadable file or source-verified label cannot fill an absent permission record.

These rights-review records belong to future release governance. They do not add a mandatory runtime license field or expand `sit-bundle/0.1`. An audit may represent an unknown or restricted source through an authorized locator or protected attestation while exposing its evidentiary limits. The runtime does not adjudicate whether every source's license was correctly supplied.

Do not place licensed or confidential real-world material in a fictional fixture by changing its names. Third-party JSON data, excerpts, photos, benchmark questions, expected answers and screenshots need the same review as other assets. Tests of protected-data handling must use independently constructed fictional canaries.

A report should reproduce only material permitted by the disclosure contract. Applying a toolkit template does not convert user evidence to Apache-2.0 or CC-BY-4.0. Any report licensing statement must describe the covered portion and exclude source/input content whose rights the issuer does not control. No mandatory ownership assignment from users, source-return charge or data-sharing permission is introduced.

The full Source Integrity Layer's licensing markets and source-return infrastructure remain outside v0.1. Representing a source-return event, where otherwise expressible, cannot execute payment or grant a reuse license.

## 6. Contributions and rights uncertainty

For future contributions, record the intended material class and confirmation that the contributor has authority to submit it under that class's adopted terms. An employer-controlled contribution, an imported passage or material with uncertain rights requires review before inclusion. No copyright assignment or contributor agreement is presumed signed by this conversation.

AI-assisted drafting must not be used as evidence that all output is original or that all necessary rights are owned. Preserve material provenance and review copied source expression. License only rights the licensor controls; do not manufacture legal ownership, an earlier approval date or a contributor signature.

Project safety, privacy and evidentiary rules govern what the project accepts and how its reference implementation behaves. They must not be silently inserted as extra downstream restrictions into an unmodified standard license. Required attribution and change notices remain distinct from demands for permission, ideological agreement or endorsement of the theory.

## 7. Adoption and later scaffold requirements

Before any license is applied, the owner must accept WU9-C03's chosen policy and confirm the authority to license the covered project material. The complete Phase 0 audit must also reconcile source-expression exclusions and unresolved rights issues. The future scaffold plan must then list the exact license/notice files and covered paths it may create.

Later implementation of the recommended policy must include:

| Release obligation | Required evidence |
|---|---|
| Clear license application | Correct standard text and material/path-specific scope; no ambiguous single-license assertion over excluded assets |
| Attribution and modification records | Project contributors, source references and changes identified without false endorsement |
| Third-party notices | Only actually included dependencies/assets; their actual versions and licenses reviewed |
| Software/package scope | Code, schemas and executable tests classified consistently; no runtime dossier automatically included |
| Specification/data scope | Original reusable prose and fictional data identified; embedded source material excluded or separately authorized |
| Distribution inspection | Wheel/source archive/docs/example bundle contents checked, not merely the root directory |
| Theory exclusion | No automatic packaging of the six PDFs, extracted full texts or page images |
| No fabricated legal completion | Actual adoption event recorded; unresolved assets excluded until cleared |

The absence of an implemented licensing file in the present Phase 0 repository is intentional. This proposal does not retrospectively apply terms simply because a document was publicly uploaded.

## 8. Written licensing acceptance cases

| Case | Required result |
|---|---|
| W9-LIC01: Original executable test plus separate fictional JSON dossier | Classify test software and standalone fixture data separately under the adopted policy |
| W9-LIC02: Full HDL PDF is copied into an examples folder | Do not include it in the standard toolkit release; require separate source-rights review |
| W9-LIC03: A private supplied dossier is audited successfully | No automatic license, publication or ownership transfer attaches to the dossier or its evidence |
| W9-LIC04: A diagram is adapted from a theory paper and labeled CC-BY-4.0 | Block the proposed inclusion until specific permission/basis is established; do not silently relicense it |
| W9-LIC05: A dependency is proposed in WU10 | Inspect its actual version/license and distribution role; this document has approved no dependency by name |
| W9-LIC06: The owner approves the policy but Phase 1 is not authorized | Record the decision in an allowed document; create no implementation, package metadata or scaffold license files yet |

These are documentation-level acceptance obligations. No runtime test or legal clearance of an actual new asset is claimed.

## 9. Review item and stop point

WU9-C03 offers three alternatives: A, one uniform license for all newly authored project materials; B, the separated Apache-2.0 / CC-BY-4.0 policy in §2 with source/input exclusions; C, defer a licensing decision and prohibit representing the project as a licensed release until that gate is resolved. **Option B is recommended.** It separates reusable engineering material from separately licensed papers and caller evidence while keeping software adoption straightforward.

This choice requires owner acceptance. It leaves source-paper rights unchanged and does not authorize Phase 1, a source-return service, a third-party rights assumption or final Phase 0 approval. The next work unit remains architecture and handoff, subject to its own authorization.
