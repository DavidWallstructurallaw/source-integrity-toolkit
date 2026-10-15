# Phase 4 W01 current CI migration review

Reviewed 2026-10-14 UTC. Owner approved the exact PHASE_4_PLAN.md bytes and started P4-W01. This record is evidence only and grants no authority.

The accepted anchor is fdad8c3449d2d223420c5d52bb9b4c1e863a9e3c, tree f6fbb8965520f33a09ca38cf413e11ca561110dd, with ordered parents 2413a29b839b7e1de8f76a449762f031de19d52b and ce05c5dda9368182dbee074253d3a7c829af7719. Approved plan SHA-256: 5fac7a2a796338faae9b98af6e0cc4519396e378ba10b8c5afeb4d029d97cd48.

## Migration

The existing guard now uses same-repository phase4/public-report to main, actual hash-verified commit footers, all-parent scope checks, exact ten owner scopes, and monotonic ancestor activation. Earlier-unit repairs keep the current activation state. Inherited merge bytes must come from separately validated parent histories; novel bytes require the merge owner's scope. Main-push merge trees must equal their candidate parent tree; owner acceptance and exact tested-candidate identity remain separate requirements. No pre-anchor source loading, inverse patching or historical stage execution is introduced.

The workflow bytes, seven steps, runner/minor matrix, action pins, read-only permissions, suite 2,400 seconds/job 50 minutes and 14-day artifacts remain unchanged. Existing phase3 artifact labels and sit-p3 paths are retained. Only PHASE_4_COMPLETION.md and phase4/implementation_evidence.json qualify for the documentation route, determined from every parent edge of the actual interval after verified activation reaches W10. Earlier record-only updates remain full risk. README affects packaging and remains full risk.

Installed receipts bind actual head, owner unit and activation stage. At W01 both public APIs still refuse and all private preparation/analytical/effect/installed-package witnesses remain. P4-W08 must atomically add real public success and both encodings with the retained audit_file refusal. No receipt count edit alone can establish that future behavior.

Current implementation validation is in progress. No local run is claimed to be hosted four-profile evidence, and W01 does not claim public reports or phase completion.

## Bounded toolchain review

P4-W01 bounded toolchain applicability review
Reviewed 2026-10-14 UTC. Working notes for phase4/ci_review.md.
Author: collaborating instance of the same assistant, using shared repository and freshly retrieved official sources. No independent external security review. No repository edits, package installation, dependency upgrade or workflow mutation performed by this reviewer.

Outcome
No mandatory dependency/action replacement was identified for the inspected current verification path. This conclusion has the specific limits below. It does not establish that these pins, their transitive components, runner images, or arbitrary uses are vulnerability-free. The next hosted run must supply actual resolution, non-yanked status, hashes, installed versions, pip check and Python/image versions. Existing preinstalled packages are not that evidence.

Current reviewed workflow
.github/workflows/phase1-ci.yml retains ubuntu-24.04 and windows-2025 x CPython 3.11/3.13, read-only contents permission, exact-candidate checkout, persist-credentials false, no dependency cache, no supplied secrets or publishing, 50-minute job timeout and 14-day JSON/XML/log retention. The cumulative suite has its separate finite timeout. The current source driver downloads binary wheels only from explicit PyPI, verifies selected names/versions and PyPI hashes/non-yanked status, then installs offline. Package tests build this repository with direct setuptools.build_meta, inspect exact regular members and reconstruct its own sdist using tarfile.extractfile. This review does not extend that use to untrusted third-party source archives.

Exact release availability/declared compatibility
Each listed release page was opened on 2026-10-14; each exposes a platform-independent wheel. Declared Python requirements admit both chosen minors. Presence of a wheel listing is not a performed network download or installation gate.
- setuptools 84.0.0, Python >=3.10: https://pypi.org/project/setuptools/84.0.0/
- pytest 9.1.1, Python >=3.10: https://pypi.org/project/pytest/9.1.1/
- iniconfig 2.3.0, Python >=3.10: https://pypi.org/project/iniconfig/2.3.0/
- packaging 25.0, Python >=3.8: https://pypi.org/project/packaging/25.0/
- pluggy 1.6.0, Python >=3.9: https://pypi.org/project/pluggy/1.6.0/
- Pygments 2.20.0, Python >=3.9: https://pypi.org/project/Pygments/2.20.0/
- Windows-only colorama 0.4.6, Python >=2.7 excluding 3.0 through 3.6: https://pypi.org/project/colorama/0.4.6/
Newer releases appear for some packages, including Pygments 2.21.0 and packaging 26.3. Existence of a newer version does not authorize replacing the retained pins.

Exact action definitions
All three action.yml files were freshly retrieved successfully via the GitHub connector on 2026-10-14 after the web renderer returned DisabledError. Each specifies Node 24. No audit of their entire bundled JavaScript/transitive component tree was performed.
- https://github.com/actions/checkout/blob/3d3c42e5aac5ba805825da76410c181273ba90b1/action.yml
- https://github.com/actions/setup-python/blob/5fda3b95a4ea91299a34e894583c3862153e4b97/action.yml
- https://github.com/actions/upload-artifact/blob/043fb46d1a93c77aae656e7c1c64a875d1fc6a0a/action.yml
Their official security overview pages were retrieved and displayed no published repository advisories:
https://github.com/actions/checkout/security
https://github.com/actions/setup-python/security
https://github.com/actions/upload-artifact/security
This observation is restricted to those overview pages and is not a claim that no vulnerability exists elsewhere or in bundled dependencies.

GitHub guidance
https://docs.github.com/en/actions/reference/security/secure-use was retrieved 2026-10-14. It recommends least-privilege tokens and full SHA pins for repositories without workflow dependency lockfiles. Current guidance calls dependency lockfiles the strongest available protection for repositories adopting them; do not repeat older wording that SHA pinning is the strongest protection. The retained configuration uses full commit pins from the official repositories and least privilege. This review does not add a lockfile or expand the approved W01 scope.

Advisories rechecked
The following GitHub advisory-database records were retrieved through the connector on 2026-10-14, preserving the same recorded fixed boundaries as the earlier review:
1. pytest GHSA-6w46-j5rx-g56g / CVE-2025-71176: recorded affected before 9.0.3; pin 9.1.1 is outside that range.
https://github.com/github/advisory-database/blob/main/advisories/github-reviewed/2026/01/GHSA-6w46-j5rx-g56g/GHSA-6w46-j5rx-g56g.json
2. Pygments GHSA-5239-wwwm-4pmq / CVE-2026-4539: AdlLexer GUID regex, recorded affected before 2.20.0; pin is at fixed boundary.
https://github.com/github/advisory-database/blob/main/advisories/github-reviewed/2026/03/GHSA-5239-wwwm-4pmq/GHSA-5239-wwwm-4pmq.json
3. setuptools GHSA-h35f-9h28-mq5c / CVE-2026-59890: MANIFEST.in Unicode normalization exclusion issue, recorded affected before 83.0.0; pin 84.0.0 is outside that range.
https://github.com/github/advisory-database/blob/main/advisories/github-reviewed/2026/07/GHSA-h35f-9h28-mq5c/GHSA-h35f-9h28-mq5c.json
The following official pages were retrieved with the web tool:
4. jaraco.context GHSA-58pv-8j8x-9vj2 / CVE-2026-23949: affected >=5.2.0,<6.1.0, fixed 6.1.0.
https://github.com/advisories/GHSA-58pv-8j8x-9vj2
The local environment's setuptools 84.0.0 metadata contains vendored jaraco_context-6.1.0.dist-info/METADATA declaring jaraco.context 6.1.0. This is a local observation only; hosted installations must retain their own actual evidence.
5. setuptools GHSA-5rjg-fvgr-3xxf / CVE-2025-47273: PackageIndex.download traversal, affected <78.1.1; pin 84.0.0 is outside that recorded range.
https://github.com/pypa/setuptools/security/advisories/GHSA-5rjg-fvgr-3xxf

Explicit residual limitations
A. setuptools archive_util traversal repair
https://setuptools.pypa.io/en/latest/history.html still lists GHSA-grgh-hr87-3jpw under DRAFT, unreleased as on Sep 08, 2026. It concerns backslashes, drive letters, UNC prefixes and extraction-directory escape. Do not credit 84.0.0 with this fix. The direct advisory URL https://github.com/advisories/GHSA-grgh-hr87-3jpw did not produce an accessible advisory body in this review (web tool Internal Error), so the affected-version range remains unverified. Current binary-wheel installation/direct own-project builds/regular member inspections do not use archive_util to extract externally supplied archives. The source review found no applicable path requiring a pin change for this bounded use. That inference does not certify archive extraction generally.

B. Pygments looks_like_xml backtracking
The current official upstream changelog states that release 2.21.0 (2026-08-17) fixes catastrophic backtracking in looks_like_xml; 2.20.0 must not be credited with that fix.
https://github.com/pygments/pygments/blob/master/CHANGES
Upstream PR https://github.com/pygments/pygments/pull/3112 describes the issue; that individual PR is closed without a merge and should not itself be described as the merged implementation. The changelog is the release-level statement.
The retrieved pytest 9.1.1 terminalwriter source selects PythonLexer or DiffLexer explicitly, then calls pygments.highlight; it does not invoke lexer guessing:
https://github.com/pytest-dev/pytest/blob/9.1.1/src/_pytest/_io/terminalwriter.py
The retrieved pinned PythonLexer and DiffLexer source files contain neither looks_like_xml nor guess_lexer:
https://github.com/pygments/pygments/blob/2.20.0/pygments/lexers/python.py
https://github.com/pygments/pygments/blob/2.20.0/pygments/lexers/diff.py
Repository src/tests do not import Pygments directly. This bounded path inspection did not identify invocation of the affected XML guessing path in this workflow. It supplies no assurance for arbitrary highlighting services, other lexers, extensions or downstream use. Runtime dependencies remain a separate product boundary.

C. Search/retrieval limits
Official security overview pages for pytest, packaging, Pygments, colorama and the three actions exposed no published repository advisories at access time; existing advisories can still be in the global database or issue trackers, as the known pytest/Pygments records demonstrate. iniconfig and pluggy security overview retrieval failed. Targeted official-repository searches produced incomplete coverage. No search non-result is used as proof of absence. No comprehensive scanner, all-transitive dependency census or runner image security audit was performed.

Python maintenance status and execution limits
https://devguide.python.org/versions/ retrieved 2026-10-14 now lists BOTH Python 3.11 and 3.13 as security-maintenance branches. Earlier W14 wording calling 3.13 bugfix maintenance is historical and must not be carried into the current review.
https://www.python.org/downloads/release/python-3119/ still identifies 3.11.9 as the last 3.11 bugfix release, superseded by 3.11.17. Actual Windows/Ubuntu patches must come from the hosted run; minor labels do not establish latest security patches. No Windows 11 native or release security certification follows.

Local command disclosure
Only metadata reads were performed locally. The default runtime had setuptools 84.0.0 and packaging 26.3, with pytest/iniconfig/pluggy/Pygments/colorama absent. An optional local Pygments source-location probe stopped with PackageNotFoundError; exact upstream pinned source was inspected through the connector instead. This is not a passing installation check and was not used as a substitute for the approved tool venv.

