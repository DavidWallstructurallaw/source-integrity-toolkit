# Source Integrity Toolkit 验证体系整合计划

Revision: 0.1  
Date: 2026-10-02  
Status: 待项目所有者批准；仅为计划，尚未实施。  
Identifier: VC（Verification Consolidation）

## 1. 决策摘要

在已验收的 Phase 3 私有分析核心之上，进行一次独立的验证体系整合，然后再启动下一个主要实现阶段。

建议采用 **1 个整合任务、6 个连续步骤、1 个实施 PR、最终候选提交的 1 轮四环境验收**。失败修复或后续实质性可执行变更需要重新验证，不能把“一轮”理解为失败后免测。六个步骤是同一任务的内部检查点，不是六个新 phase，也不默认要求六次 PR 或六轮完整矩阵。

遵循已批准的《Verification Governance and Evidence-Semantics Protection》：

> Preserve semantic rigor. Compress administrative rigor when it no longer protects a distinct failure mode.

本次要达成的结果：

- 分析语义、安全边界、私有端到端组合和安装包验证继续保持严格。
- 历史测试加载、逆向补丁还原、旧方法逐轮 AST 比较和完整阶段链重演，退出日常验收路径。
- 当前边界由直接、独立、有正反例的测试保护；旧代码、失败尝试和执行凭据保留在 Git 历史及既有证据包中。
- 后续工作不再要求复演所有早期开发步骤，也不以测试数量持续增长作为质量目标。

本次不实现公开 audit API、报告输出、CLI 实际审计、文件输入/native adapter 或正式发布；不修改产品语义、冻结规范和依赖。

## 2. 已确认基线

| 项目 | 基线 |
| --- | --- |
| 已验收 PR | [PR #34](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/pull/34)，W15 / Phase 3 已验收并合并 |
| 整合起点 | `2413a29b839b7e1de8f76a449762f031de19d52b` |
| 原直接测试 head | `90684996eac568af6129973764fe40f3b666a15f` |
| 两者相同的 tree | `e2f230bdf6f838f3d12df233559732aa1d5c1699` |
| 原 CI | [run 36736103966](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/actions/runs/36736103966)，attempt 1，四环境全部成功 |
| 原测试集合 | 每环境 3,963 个 tests，另计 428 个 subtest events；72 个测试文件 |
| 原仓库范围 | 207 个 tracked files；48 个产品模块，其中 29 个已活动、19 个受保护未激活 |
| 原 CI 预算 | suite 2,400 秒；job 50 分钟 |
| 产品执行预算 | 60 秒协作式期限及既有资源配额，保持不变 |

实际最终收集按目录计数：contract 2,044、unit 1,021、security 393、integration 314、scaffold 191，共 3,963。这是原始集合的记账分类，不是删减配额。

两个 transition 文件目前合计 409 个 identities：Phase 2 为 57，Phase 3 为 352。W15 review 中的 374 是更早 W14 集合的历史数字，不能作为本次当前数字使用，更不能据此整文件退役。

冻结的完成文件仍可能保留“待验收”的成文时状态；实际所有者验收和合并记录已经完成。整合不得改写既有历史证据来制造事后状态一致。

既有 R03 执行证据包：`Source-Integrity-Toolkit-P3-W15-R03-Execution-Evidence.zip`；SHA-256 为 `81d7e9b02f71405ff0f3c13a7dd2fc198d9ae1e05762a94390582f49c6a63267`。保留原包，不覆盖。

## 3. 整合后的长期形态

| 部分 | 日常保留的保障 | 整合方向 |
| --- | --- | --- |
| Canonical analytical suite | 证据强度、来源独立性、未知祖先、图投影与遍历、Claim/member/dimension、分母、修正历史、未解决状态 | 保留现有直接行为和语义 mutation 测试；不因行政减负削弱它们 |
| Security / evidence boundary | 无隐式网络/native 效果、输入限额、恶意对象不执行、隐私、失败关闭、取消及中断 | 与当前输入和实际执行路径直接绑定 |
| Canonical integration suite | value / UTF-8 两种私有入口、跨组件一致性、原始 hero 结果、有限完整案例、已安装运行、公开接口拒绝 | 保留真实组合验证，不把资源中断包装为完整分析完成 |
| Release matrix | 四环境、构建/重建、成员清单、离线干净安装、产品模块字节一致、工具链与依赖边界 | 保留既有有效强度；不额外添加默认的“矩阵验证矩阵” |
| Lightweight current governance | 冻结基线、当前授权路径、受保护模块、实际 checkout、当前变更区间内的越权提交 | 用当前直接控制代替从 Phase 1 开始重演的迁移链 |
| Historical archive | 旧 transition 实现、逐轮修复、原始失败和成功凭据、接受记录 | 通过固定 Git 引用和既有证据包查阅；不放入默认 pytest 收集路径 |

这是逻辑分层，不要求为了目录整齐移动所有现有测试。当前源码 AST 效果检查和冻结规范字节检查继续有效；退出的是旧实现形状的逐轮保真链，不是所有 AST 或哈希检查。

## 4. 六步实施顺序

| 步骤 | 工作 | 完成条件 |
| --- | --- | --- |
| VC-01：锁定基线与保障映射 | 核对接受记录、原集合和现有依赖；把每个拟退役检查映射到故障类别及当前替代断言 | 没有未解释的待删断言；明确保留、替换、归档三种处置 |
| VC-02：建立当前直接控制 | 在现有工具和测试中建立当前授权、冻结范围、模块效果、实际 checkout、CI 入口和 collection 控制 | 正常基线通过；每项越权或遗漏反例由正确控制拒绝；测试预期不从被测 guard 自行生成 |
| VC-03：物化当前测试入口 | 将六个历史加载 wrapper 改成完整、直接的当前测试；解开混合文件对旧 transition helper 的依赖 | 默认测试不再从 Git blob 动态执行历史测试源码；原导入、效果、目录和接口保障得到覆盖 |
| VC-04：退役历史链 | 根据已验证映射，移除逆向补丁、旧方法保真链、逐阶段历史重演及固定历史 identity 配额 | 所有移除有去向；保留当前提交区间的越权检查；历史原件可定位 |
| VC-05：整合 CI 与开发入口 | 更新当前上下文解析、风险分流、集合/JUnit 对账、失败凭据、README 操作说明 | 无隐蔽跳过、空集合通过、可疑文档分流或丢失 package/installed 检查；操作说明可执行 |
| VC-06：最终验收与交接 | 固定完整候选 head，运行四环境矩阵，核对原始产物、范围和保障差异，提交所有者验收 | 第 9 节全部通过；得到明确验收后才具备进入下一主要实现阶段的条件 |

### 执行方式与启动边界

当前 guard 只识别既有 P2 / P3 单元；不能把整合冒充为 `P3-W15`，也不存在自动获得授权的 `P3-W16`。

批准后，从第 2 节的已接受 merge 建立单一整合分支，建议名为 `verification/consolidation`。`VC-01` 至 `VC-06` 只标识工作步骤，统一整合权限标识为 `VC`。分支名、候选元数据或提交 footer 本身不能替代所有者授权。

首次切换需要一次明确的 bootstrap 审核：

1. 以已接受 merge、已批准本计划和真实平台 event/base/head 为外部基准，核对整合路径表。
2. 独立检查当前差异和每个新增提交，确认所有产品字节、冻结规范及其他未授权路径不变。
3. 在默认路径中启用新控制之前，完成旧保障与新直接控制的对应证明。与 loader/CI 强耦合的改动作为同一原子切换处理。
4. 不要求混合中间状态通过不再适用的旧逐字迁移 oracle；也不把中间检查点报告为已完成验收。完整候选提交必须通过全部当前测试。

这是一项一次性过渡检查，不形成下一层永久迁移 oracle。不得停用必需检查、放宽分支保护，或用候选文件中自称“已批准”的字段扩大权限。

## 5. 拟批准的精确修改范围

本节是未来实施的路径上限；本轮制定计划不修改以下仓库文件。未列路径继续冻结；发现必要的额外调用方时，先说明保障和原因，再申请范围修订，不能自行扩到 `tests/**` 或 `tools/**`。

### 5.1 主控制和六个 wrapper

```text
tools/check_scaffold_boundary.py
tests/scaffold/test_imports.py
tests/scaffold/test_module_manifest.py
tests/scaffold/test_no_runtime_implementation.py
tests/scaffold/test_layer_boundaries.py
tests/scaffold/test_contract_catalogs.py
tests/scaffold/test_ci_contract.py
tests/contract/test_phase2_transition.py
tests/contract/test_phase3_transition.py
.github/workflows/phase1-ci.yml
```

允许为本计划改变历史加载、当前上下文、当前范围/效果控制、历史 source-binding、collection 和 evidence driver。两个 transition 文件按断言迁移，可最终删除空壳；不能先整文件删除再以总测试数掩盖保障缺口。

### 5.2 混合测试的限定部分

| 文件 | 允许处理的历史或上下文部分 | 必须保持的部分 |
| --- | --- | --- |
| `tests/contract/test_bundle_contract.py` | 六个 `test_repair_*` 函数及专用 `_repair_driver` | 所有私有表示、不可变性、恶意协议和数据区别断言 |
| `tests/contract/test_input_schema_mapping.py` | `test_r02_exact_extra_path_and_other_units_keep_their_immediate_scope`、`test_r02_preserves_every_old_schema_assertion_except_the_named_stage_check` 及专用失效 import | schema 映射、逐字段 obligation、实际 admission/rejection 和状态防夸大断言 |
| `tests/contract/test_observability_preparation.py` | `historical_segment`、`test_preserves_existing_report_declarations_and_w05_admission_body`、`test_only_ten_w06_paths_and_no_old_test_permissions_changed` 及专用失效 import | PC、family/leaf、准备层和完整检查之间的所有语义区分 |
| `tests/security/test_input_capture.py` | 四个 `test_r01_*` 历史修复测试，以及专用 `old_file` / `ci_driver` 和失效 import | 捕获安全、输入诊断、循环容器、信息泄漏等直接安全断言 |
| `tests/security/test_preparation_inertness.py` | `test_whole_package_guard_rejects_forbidden_implementation_in_temporary_copy` 的当前上下文和 fixture 接线 | 正例先通过、临时副本实际注入非法实现后拒绝、原仓库仍通过的完整负向证明 |

历史 helper 的删除以无剩余引用为前提。仅为历史控制服务的常量/import 可随其移除，不能顺带重写周边语义测试。

### 5.3 新直接控制及最少文档

```text
tests/contract/test_verification_boundary.py
verification/consolidation_map.json
VERIFICATION_CONSOLIDATION_PLAN.md
VERIFICATION_CONSOLIDATION_COMPLETION.md
README.md
```

以上为允许新增/更新的精确路径，不是要求每个路径必须发生修改。`test_verification_boundary.py` 只承接独立的当前行为反例；不复制另一个全套框架。映射文件仅供本次过渡审核，完成后归档冻结，不作为默认执行 authority，不要求未来阶段继续追加所有历史节点。

本计划批准版本不得在实施中悄悄改变授权。README 只更新当前状态、测试入口和必要开发说明；保留未完成公共功能和原 hero 限制的真实描述。

### 5.4 明确禁止

- 不修改 `src/**` 的任何产品字节，包括 48 个模块及已活动模块。
- 不激活 19 个受保护模块，不增加公开 audit、report、native 或外部 I/O 能力。
- 不修改冻结规范、schema、fixture、golden、Phase 0 基线、既有 Phase 1/2/3 接受与迁移记录。
- 不修改 `pyproject.toml`、依赖锁定、构建配置、Action pin、产品资源配额或现有 CI 时间上限。
- 不删除或改写本节未授权的语义、安全、集成及打包断言。
- 不增加永久登记册来证明旧登记册仍被保存；不建立跨执行、跨 ROOT 的可变 Git 信任缓存。

## 6. 历史机制如何替换

| 现有机制 | 要保留的实际保障 | 目标控制 |
| --- | --- | --- |
| 六个 `load_phase1_test` wrapper | 48 模块导入、目录/所有权、层间依赖、无运行时副作用、catalog、CI 隔离 | 当前源码中的显式测试和正反例；不再 `git show` 后 `exec` 测试源码 |
| Phase 2 逆向 patch / AST 还原 | 当前 checkout 真实受检、冻结字节、权限不从候选元数据产生、受保护行为不被激活 | 固定接受锚点及当前直接 scope/effect/byte 控制 |
| Phase 3 逐轮方法保真 | 当前有效语义和安全断言未消失；非法效果、超限、未激活模块受到约束 | 保留原直接断言或证明更强替代；退出逐个历史方法的源码重建 |
| 混合文件中的旧修复链 | 恶意对象、输入/schema/observability 的安全与意义不因修复遗失 | 语义部分保留原样；单独迁出历史权限例外和形状比较 |
| 194 / 1,650 个历史 identity 永久包含检查 | 不漏收集、不无声删除独特保障、不让空/重复测试通过 | 当前全量 collection/JUnit 对账，加本次一次性逐项退役映射 |
| 从旧 intake 起逐轮遍历所有阶段 | 不接受过去越权后又恢复的中间提交，不允许后来授权倒灌 | 接受锚点以前作为已验收历史；对锚点后的全部相关提交及 merge side branch 检查真实变更 |
| 将当前 workflow 反向改形后交给旧 Phase 1 policy | 真实 head、有限权限、固定工具链、四环境、隔离和完整证据 | 当前 workflow 的直接政策测试及破坏性反例 |

当前历史控制仍需拒绝：伪造/缺失接受锚点、错误 base/head、缺失必要 Git 对象、非祖先关系、重复或伪造上下文、路径别名/近似名、范围外 rename/delete、已提交后撤回的越权变更，以及实际 staged/unstaged/untracked 变更。

不再默认复演接受锚点之前的每个阶段，并不等于删 Git 历史或取消当前变更历史检查。常规测试中的只读 head 身份记录与当前 guard 的 Git 操作可以保留；本次不承诺整个仓库在没有 `.git` 的源码压缩包中运行全部开发检查。

### 一次性映射的最小字段

每个被替换或归档的旧 test identity / 参数用例记录：旧路径和节点、具体断言或故障类别、处置理由、替代节点、正例/破坏性反例证据、历史来源 commit、执行证据位置。多个重复旧节点可以对应一个更强当前测试，但必须说明为何没有丢失独特情况。

纯粹证明“旧函数体未变化”的历史断言可归档；其实际保护过的错误类别必须有当前覆盖。未能证明等价或更强覆盖时，先保留该检查，并将其列为整合未完成项。

## 7. 验证运行策略

| 变更类型 | 必需验证 |
| --- | --- |
| 本次完整整合候选 | 涉及 source loading、security boundary、CI 和跨平台行为，必须完整四环境矩阵 |
| 实施中的小检查点 | 受影响直接测试、相关负向反例和范围检查；不把局部成功称为完整验收 |
| README / 纯措辞 / 不参与可执行 authority 的接受记录 | 链接、内容、必要格式或受影响打包检查；不自动要求完整矩阵 |
| 参与 guard 或授权的行政记录 | 验证受影响控制；若同时改变安全、加载、平台、包装或发布行为，升级完整矩阵 |
| 分析语义、Python 版本敏感行为、Windows/POSIX、packaging、source loading、安全边界、public API、release candidate | 按既有治理政策要求完整四环境矩阵 |
| 文件类型不明、权限/依赖影响无法确定 | 不准按“文档”降级；默认提升到足够的验证范围 |

文档分流只使用明确许可的非可执行路径和真实完整差异，不以 `.md` 后缀单独决定；正文内容若参与授权或 package 行为，按实际影响处理。未知或混合变更不能走低风险捷径。

四环境保持 `ubuntu-24.04` / `windows-2025` × Python `3.11` / `3.13`。同一最终候选 head 的完整矩阵证据不能与旧 head 或不同尝试的缺失 profile 拼接为成功。

候选源码在矩阵前定稿。后续可执行改变需要重新产生适用证据；接受文字可记在外部 PR/所有者记录，避免为写“已通过”改变刚验证的代码。文档-only 后继提交仍须明确与已测 tree 的差异及影响，不能冒称是同一个直接受测 head。

保留 pytest 插件隔离、实际工具版本检查、有限执行预算、失败/超时原始输出和始终上传的证据。不得用新增 skip、xfail、`-k`、忽略目录、缩小 fixture 或只跑新增测试来获得通过。

## 8. 效率目标和证据边界

首先验收机制上的简化：

1. 默认路径中，历史 Git blob 测试源码动态执行为零。
2. 默认路径中，历史逆向补丁和逐轮旧方法保真重建为零。
3. 默认路径中，接受锚点以前的完整阶段 DAG 重演为零。
4. 永久日常检查不再强制 194 / 1,650 等历史 identity 下限。
5. 当前唯一保障、全量收集、安装包检查和严格边界仍有可执行证明。

VC-01 使用既有执行记录记录总体耗时，并对受影响历史机制做一次有界基线测量；最终以相同平台、Python、工具链和负载条件进行对照，报告 Git 子进程调用、重复历史遍历及对应测试耗时。构建产物中的成员与语义测试工作量不可被偷偷减小。

不承诺未经测量的加速百分比，也不把跨平台或不同 hosted runner 的时间差当成可靠的优化证据。可以报告全套 CI 的观察耗时，但不可把私有分析或原 hero 执行成本都归因于历史机制。

测试总数可以降低；变化必须满足 `最终集合 = 原集合 - 已映射退役集合 + 新直接控制集合`，同时说明参数展开、改名和 subtest 口径变化。428 是历史 subtest 观测值，不是可以牺牲真实检查来保持或永久增长的数字目标。

## 9. 最终验收门槛

以下全部满足才可称为“验证体系整合完成”：

1. 实际授权路径、每个相关提交、最终 tracked/工作区状态核对通过；没有范围外变更或隐藏的中间越权。
2. 相对接受 merge 的 48 个产品模块逐文件字节不变；冻结规范、schema、fixture、golden、依赖和产品预算不变。
3. 所有被移除或替换的旧断言有明确处置；所有独特语义/安全保障都有当前直接测试，不能仅凭总数或文件名证明。
4. 关键语义 mutation 保持有效：独立性、未知祖先、图边筛选、Claim/member/dimension、qualified/submitted、修正状态、未解决状态、分母和证据强度提升。
5. 当前边界反例确实触发对应拒绝；必须先有通过的正常基线，不能把 fixture 本来就坏了当成负例有效。
6. 六个 loader、逆向补丁、逐轮 AST 保真链和全历史阶段重演已退出默认路径；旧机制不存在被复制到新 helper 后继续执行的情况。
7. 当前 canonical 全量 collection 与 JUnit 身份/计数一致，无遗漏、重复、隐藏排除、失败、错误或未获授权的跳过；subtests 单独对账。
8. 同一最终候选 head 的四环境全部成功，原始 run/job/artifact、日志、collection 和 JUnit 可核验；不把失败尝试覆盖为成功。
9. 保留既有 wheel/sdist/重建成员检查、离线干净安装、48 模块源码一致、依赖/隐私排除、已安装私有组合及公开拒绝检查。成员字节重现不夸大为未经证明的整个 archive 字节完全可重现。
10. 历史映射、原件引用、失败记录和已知缺口明确。旧 W01-W07 原始 ZIP 及 W08 部分 profile 原件未包含在既有 handoff 的事实继续披露，不虚构已补齐。
11. README 给出唯一清楚的当前开发验证入口、何时运行矩阵、如何查旧证据；仍明确公共 audit/report/native/release 未完成。
12. 项目所有者明确验收。CI 通过不自动等于接受、合并或授权下一主要实现阶段。

## 10. 交付物与控制成本

仅保留这组必要交付：

- 本计划的批准版本。
- 一次性 `verification/consolidation_map.json`，包含基线、集合变化、保障映射和历史索引；不另外建立平行迁移登记册。
- 当前直接测试、精简后的 guard/CI 和 README。
- `VERIFICATION_CONSOLIDATION_COMPLETION.md`，汇总范围、通过情况、结构性减负、真实耗时及限制。
- 最终 head 的四环境原始证据，沿用既有留存方式，不复制新的多层证据框架。

历史源代码依靠不可变 Git 引用保存，不把旧测试整批复制进另一个默认收集目录。需要历史重演时，只对指定旧 commit 建立隔离 checkout，以当时工具链和原范围执行，并标注它是历史调查，不是当前验收。

## 11. 审批、停止条件和失败恢复

本轮只交付计划，没有启动 VC-01 的实施、改变仓库、创建 PR 或运行新 CI。

建议下一条执行指令：**“批准验证体系整合计划，启动 VC-01，按计划继续至 VC-06。”** 这将授权本计划精确范围内的整合工作和实施 PR，不自动授权最终合并、产品修复或下一个主要 phase。步骤内无需每一步重复请求批准。

遇到以下情况暂停并请求针对性决定：需要修改产品/冻结规范；出现未列路径或额外依赖；必须增加 CI/产品预算；无法证明旧保障有等价覆盖；需要改变权限边界、分支保护或已批准范围。

局部失败先保留失败证据，在原范围内修复。若需放弃候选，在独立分支上以可审阅的恢复提交回到接受基线；不 reset 主分支、不改写历史、不删除旧证据。若整合已合并后的问题需要 revert，另行取得明确恢复授权。

整合验收后的下一件事是制定下一主要实现阶段计划，依据冻结产品规范处理仍待完成的公共组合、报告、接口和发布工作；本计划不预先宣布其编号、范围或已经完成。

## 12. 依据

- 已批准的 `SOURCE_INTEGRITY_VERIFICATION_GOVERNANCE.md`，尤其第 2、3、5、6、7、8 节。
- [已接受 merge](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/commit/2413a29b839b7e1de8f76a449762f031de19d52b) 的所有者接受、测试 tree 和范围记录。
- 接受 tree 中的 [PHASE_3_COMPLETION.md](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/blob/2413a29b839b7e1de8f76a449762f031de19d52b/PHASE_3_COMPLETION.md)，Verification normalization review 及证据限制。
- 同一 tree 的 [phase3/delivery_manifest.json](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/blob/2413a29b839b7e1de8f76a449762f031de19d52b/phase3/delivery_manifest.json) 中 `verification_normalization_review`。
- 原最终 head 的 collection、原始四环境执行包、接受 merge 的字节一致核验，以及本次对当前 guard、workflow、wrapper 和混合测试依赖的只读检查。
