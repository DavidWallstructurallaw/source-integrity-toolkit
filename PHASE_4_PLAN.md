# Source Integrity Toolkit 下一阶段实施计划

## 文档控制

| 项目 | 内容 |
| --- | --- |
| 建议仓库文件名 | PHASE_4_PLAN.md |
| 阶段建议编号 | Phase 4 / P4 |
| 阶段名称 | 公共内存审计与正式报告 |
| 修订 | 0.1 |
| 日期 | 2026-10-11，America/Los_Angeles |
| 状态 | 待项目所有者批准；计划草案，未开始实施 |
| 当前授权 | 起草下一阶段计划，列清工作单元、可修改文件及验收标准 |
| 实施基线 | PR #35 已验收并合并后的 main：fdad8c3449d2d223420c5d52bb9b4c1e863a9e3c |
| 当前交付 | 本计划一份；不修改仓库，不创建远程分支或 PR |
| 审批对象 | 本文件最终交付的准确字节及以下范围、接口选择、工作单元和验收门槛 |

本计划用 Phase 4 作为新阶段的建议编号。冻结的 Phase 0 规范没有预先规定所有后续阶段编号。编号、阶段拆分和下列 Python 接口实现选择均属于本次提交审阅的工程方案。

## 1. 决策摘要与阶段成果

建议按 **10 个顺序工作单元、1 条实施分支、1 个实施 PR、最终候选的一轮四环境完整验收** 执行。工作单元是可检查的内部检查点，不默认各建一个 PR、各增加一层历史验证框架。失败修复或影响可执行行为的后续变更，仍须针对实际最终候选重新取得相应证据。

本阶段使调用者可以在 Python 内存中提交一个 dossier，通过 audit_bundle 得到符合 sit-report/0.1 的不可变报告，并取得内容一致、字节规则确定的 JSON 与 Markdown。分析、披露选择、正式报告组装和两种编码均在同一次调用的既有预算内完成。

完成后必须具备：

1. 所有 15 个分析家族、57 个字段及所需非结果、原因、前提、范围、人口集合和见证，都能通过正式公共报告表达。
2. 公共报告与已验收分析语义一致；报告模块不能重算、增强或删减分析结论。
3. JSON 和 Markdown 使用同一份冻结逻辑文档，保留相同的实质信息及披露范围。
4. 公开的 audit_bundle、类型、异常和只读编码访问方法具有明确行为。
5. 原始私有准备/分析接口继续满足已验收行为；文件 API 与 CLI 实际审计仍保持拒绝。
6. 当前验证体系沿用 VC 已实现的直接行为控制，不恢复旧测试加载器、逆向补丁或全历史阶段重演。

**本阶段完成的含义：公共内存审计与报告通过验收。v0.1 的文件工作流和正式发布仍有后续工作。**

后续路线仅作依赖说明，不在本计划实施授权内：

| 顺序 | 交付内容 | 启动条件 |
| --- | --- | --- |
| 已完成 | Phase 3 私有分析核心、VC 验证整合及 PR #35 合并 | 已有接受记录 |
| 本次建议 | 公共内存审计、报告契约、披露、JSON/Markdown、公共边界验证 | 本计划获准后启动 P4-W01 |
| 后续实现阶段 | 安全文件捕获、Linux/Windows native adapter、私有目录和完整报告对发布、audit_file、CLI | 单独制定范围与平台验收计划 |
| 后续发布阶段 | 用户全流程、支持平台证据、安装与发布材料、最终验收及 v0.1 发布 | 所有拟发布功能及相应义务实际完成 |

后续阶段编号、工作单元数量及发布渠道留给对应计划确定。

## 2. 已接受基线与证据边界

| 项目 | 已核实状态 |
| --- | --- |
| PR | [PR #35](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/pull/35)，已验收并正常 merge |
| 当前 main / 新阶段锚点 | fdad8c3449d2d223420c5d52bb9b4c1e863a9e3c |
| tree | f6fbb8965520f33a09ca38cf413e11ca561110dd |
| 两个 merge parents | 2413a29b839b7e1de8f76a449762f031de19d52b；ce05c5dda9368182dbee074253d3a7c829af7719 |
| 直接验收的 VC 候选 | ce05c5dda9368182dbee074253d3a7c829af7719，与 merge 的 tree 完全一致 |
| VC 验收运行 | [38128491330，attempt 1](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/actions/runs/38128491330)，四环境成功，原始凭据已审阅 |
| merge 后 push 运行 | [38164028893，attempt 1](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/actions/runs/38164028893)，四环境全部成功 |
| VC 验收集合 | 每环境 3,724 个独立测试及另计 431 个成功 subtest events；73 个测试文件 |
| 仓库 | 211 个 tracked files，48 个产品模块；包版本 0.1.0.dev0 |
| 实际已完成 | 15 家族的私有核心及 228 项字段义务的核心层证据；公共报告、文件和发布条款仍分别待完成 |

3,724/431 是已接受候选的历史实测，不作为新阶段必须保持或增加的数量门槛。新的删除、替换或合并必须逐项说明保障去向。新阶段验收使用新候选的实际集合、实际 JUnit 和实际运行凭据。

README、PHASE_3_COMPLETION.md 和 VC 完成文件包含创建时的待验收措辞。后来的所有者接受、PR #35 和 merge 记录补充其状态；不通过改写旧文件消除历史痕迹。实施阶段可在 README 更新当前状态及功能说明。

沿用以下证据限制：

- 四个原始 H7 完整案例在既有预算下可能真实中断。有限完成案例及内部已提交观察不能被称为原始 H7 全字段公共报告完成。
- 既有 CI 上传 JSON/XML/log 凭据，未上传 wheel/sdist 原始文件或原始 GitHub event payload。成员清单和安装验证不等于完整压缩包逐字节可复现。
- W08 临时压缩包会被清理；其成员哈希交叉核对与 W14 精确归档记录的证明范围不同。
- VC 原始 event 摘要在 runner 组间不同的原因未知；已核实语义绑定，不补造换行或序列化解释。
- W01 至 W07 的历史原始 ZIP 和部分旧 W08 profile 凭据缺失；既有失败及未完成运行继续按原性质保留。
- 本次协作模型交叉检查属于工具辅助审阅，不代表外部人类审计。

## 3. 控制依据与本次工程选择

### 3.1 冻结依据

本计划从已接受规范落实行为，不重新解释六篇理论论文，也不修改理论文本。出现确切语义冲突时才回到相应源条款及其来源映射。

以下链接均固定到本阶段基线：

| 依据 | 使用范围 |
| --- | --- |
| [OBSERVABILITY_AND_REPORTING.md](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/blob/fdad8c3449d2d223420c5d52bb9b4c1e863a9e3c/OBSERVABILITY_AND_REPORTING.md) §§12–19 | 状态、16 个根成员、嵌套对象、57 字段、引用、见证及两种格式 |
| [REPOSITORY_ARCHITECTURE.md](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/blob/fdad8c3449d2d223420c5d52bb9b4c1e863a9e3c/REPOSITORY_ARCHITECTURE.md) §§17–19、21 | 内存输入、J 编码、局部 ID、输出字节、调用结果、统一预算 |
| [GOVERNANCE_AND_HANDOFF.md](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/blob/fdad8c3449d2d223420c5d52bb9b4c1e863a9e3c/GOVERNANCE_AND_HANDOFF.md) §22 | 精确 Markdown、取消、去重、数值及见证精化 |
| [PRIVACY_AND_DATA_HANDLING.md](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/blob/fdad8c3449d2d223420c5d52bb9b4c1e863a9e3c/PRIVACY_AND_DATA_HANDLING.md) §§4、6–10 | 字段最少披露、诊断、保留、渲染、资源配额 |
| [VALIDATION_PLAN.md](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/blob/fdad8c3449d2d223420c5d52bb9b4c1e863a9e3c/VALIDATION_PLAN.md) §§10–17 | 228 项 P/N/M/B 义务、26 个共享家族、嵌套成员及反例 |
| [THEORY_TO_CODE_TRACEABILITY.md](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/blob/fdad8c3449d2d223420c5d52bb9b4c1e863a9e3c/THEORY_TO_CODE_TRACEABILITY.md) | 35 条 Trace 及各字段的原有语义 owner |
| [V0.1_PRODUCT_SPEC.md](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/blob/fdad8c3449d2d223420c5d52bb9b4c1e863a9e3c/V0.1_PRODUCT_SPEC.md)、SUCCESS_CRITERIA.md | 产品边界、hero 意义与最终发布目标 |
| [VERIFICATION_CONSOLIDATION_PLAN.md](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/blob/fdad8c3449d2d223420c5d52bb9b4c1e863a9e3c/VERIFICATION_CONSOLIDATION_PLAN.md) §§3、7–9、11 | 当前直接验证、凭据强度和下阶段启动边界 |
| PHASE_3_COMPLETION.md、phase3/obligation_coverage.json、phase3/delivery_manifest.json | 已完成核心义务及尚待公共报告/文件/发布的逐项区分 |
| DEPENDENCY_STRATEGY.md、LICENSING_NOTES.md | 零第三方运行时依赖、冻结工具链及许可边界 |

VC 计划引用的 SOURCE_INTEGRITY_VERIFICATION_GOVERNANCE.md 不在本次仓库清单中。本次没有声称读取该缺失文件；直接采用可核实的已批准 VC 计划及既有接受记录所载规则。

治理 §22 已解决的后续精化继续有效。例如取消单独交付 AuditCancelled；精确代码围栏方案控制 Markdown；公开 options 不增加可调预算。无需为旧文档的历史待办表述重新打开这些已决选择。

### 3.2 本计划提交批准的具体工程选择

| 编号 | 本次选择 |
| --- | --- |
| P4-D01 | Phase 4 只开放内存审计与正式报告；文件、native adapter、CLI 实际审计及发布后置 |
| P4-D02 | 使用既有 48 模块布局；仅第 5.1 节 12 条产品路径可以修改，不新增产品模块或依赖 |
| P4-D03 | 公共返回类型为 AuditReport，代表既有 16 根成员的冻结逻辑文档；新增两个只读字节方法 |
| P4-D04 | 包根公开 AuditReport、AuditAbort、AuditCancelled、AuditUsageError；保留原有 audit_bundle、audit_file、__version__ |
| P4-D05 | 报告两种编码及一致性检查在调用返回前使用原有同一预算完成；返回后方法只读取私有不可变缓存 |
| P4-D06 | 一条 phase4/public-report 分支及一个实施 PR；10 个内部单元；按风险验证，最终 exact candidate 四环境验收 |

这些是本计划的实现安排。它们不新增报告字段、分析指标、Reason code、网络能力或自动匿名化行为。

## 4. 对外行为与必须保持的边界

### 4.1 公共 API

保留签名：

~~~python
audit_bundle(bundle, *, options=None) -> AuditReport
audit_file(input_path, output_directory, *, options=None)
~~~

audit_bundle 的根输入为精确 built-in dict，递归允许类型、并发修改前提、复制和大小规则沿用架构 §17。不接受自定义 mapping、子类、生成器、Decimal、回调或文件路径作为 dossier。

options 仅允许 None，或只含 raw_file_digest 的精确 built-in dict；值必须为精确 bool，默认 false。对象模式的 true、未知键、不合类型及任何回调/时钟/预算/输出 profile/子集选择均为安全 usage failure，必须先于 dossier 访问。检查选项不得调用恶意键或值的 repr、迭代、相等或其他自定义协议。

AuditReport：

- 是实际逻辑 envelope，不额外包一层文件 transport。
- 16 个根成员以只读命名属性访问，例如 report.results；嵌套 JSON 对象为项目持有且不暴露可变 backing 的不可变 Mapping[str, value]，数组为 tuple，标量为 str、bool、int、None。分数保留整数 numerator/denominator。当前正式字段不导出任意扩展里的非整数数值原子，不增加 opaque 公共数值类型或通用 serializer。
- 16 个根成员及所有嵌套内容只读；不持有调用者可变容器、完整准备快照、原始输入树、私有索引或执行预算。
- to_json_bytes()、to_markdown_bytes() 返回同次调用预先完成的 immutable bytes；不重新编码、不访问时钟、不做 I/O、不再启动分析。
- 私有缓存和 Python 方法不是 schema 成员，不能被通用对象序列化泄漏。
- 只有逻辑报告、两种完整编码及必要一致性验证全部完成后才交付对象。部分编码不能构成成功返回。
- 支持语法拒绝和处理诊断的合法 envelope；“有报告对象”不代表输入已接受或分析完成。

新增 Python 类型与方法的具体声明属于本计划批准范围。内部 report renderer 不再另行扩成接受任意对象的公共序列化服务。

AuditUsageError 建议继承 ValueError，使用固定消息 Invalid audit invocation. 和 transport code invalid_invocation。该 code 不进入报告的 40 个 Reason vocabulary。异常不携带输入值、未知键、路径或原生 exception repr。

AuditAbort、AuditCancelled 采用已批准架构和治理的字段及结果语义；本阶段 publication_state 始终为 not_published。包根的 __all__ 精确为上表七个名字，顺序由实现声明固定并测试；版本继续为 0.1.0.dev0。

audit_file 原有立即拒绝及参数不触碰保证继续保持；cli.py 原有审计拒绝、退出 1、无输入读取和无报告写出保持。其后续真实退出码映射不在本阶段启用。

### 4.2 正式报告投影

16 个根成员按冻结表保持：

~~~text
contract_version, report_kind, report_id, run, input_identity,
input_validation, scopes, populations, basis_index, capabilities,
checks, observability_domains, results, findings, reasons, release_limits
~~~

必须显式建立私有对象到公开契约的投影，不可对 _AnalyticalOutcome、dataclass 或私有记录执行通用递归 dump：

- 私有 prepared/raw source 不进入报告。
- 私有 Scope.operation_anchor 参与身份排序；公共 Scope 仍使用既有成员，实际 operation 语义通过契约要求的目标和 payload 保留。
- 私有 Finding.result_refs、native_records 不直接变成公开 Finding 成员。
- Result.witness_refs 必须解析为本报告 Finding IDs；见证内容进入其契约位置，不增加根级 witnesses 数组。
- 原私有 domain 按 inquiry 分组；公共普通 audit envelope 只有五个全局 domain 条目，跨 inquiry 正确归并引用。not_applicable 继续存在于 Result/Capability，不额外塞进不含此字段的 domain 契约。
- 每个 inquiry 的 15 家族 Capability 保持四类 Result 的精确分区。空 subject 不自动成为成功、独立或已完整覆盖。
- basis_index 从已接纳不可变记录中有界提取规定的 basis、asserter、method、support、availability、scope/time、lifecycle、qualification 和 checks；不重新作来源资格判断。
- 诊断 envelope 的各分析数组按规范为空，不用空数组暗示真实世界没有问题。原因、状态和安全诊断保留。

报告 schema 采用与既有 bundle schema 一致的声明风格，关闭固定对象键；规范定义的字典和多态 payload 逐类型约束。只用仓库内本地引用，不引入运行时 schema 文件读取、远程 $ref 或第三方 validator 依赖。schema 结构验证与跨引用、语义一致性验证分别有直接测试；不以 schema 通过代替分析正确。

### 4.3 身份、排序及精确编码

report_id 固定为 SIT-RPT-000001，只标识同次调用内的单一文档。其他对象使用既有八类前缀及至少六位序号，按语义键排序后编号；不使用随机数、输入哈希或发现顺序。

相同解释对象按完整无 ID 语义体及 anchor 去重。不同输入 ID 永不合并；相同 Result slot 的不同值为内部契约错误。Reason/Result 循环引用通过 anchor keys 排序，不递归展开完整链接对象。所有引用在交付前闭合。

JSON 为 J(冻结文档) 加一个 LF。保持 Unicode scalar key order、既有控制字符转义、源原生有序数组、可移植整数、精确数值原子及原始分数分子/分母；JSON 不输出可选 display_decimal。不能将 26/36 仅替换成 13/18 或浮点近似。

Markdown 精确采用治理 §22.2：固定标题、状态行、16 根节顺序、pretty-J 围栏；每个 Result 的完整对象和 Reason details；available fraction 的六位 half-up decimal 行；interval endpoints 不另加该行。围栏长度为 max(3, 正文最大连续 backtick 长度 + 1)。不可信数据只能进入已编码代码块，不能决定标题、链接、HTML 或图片。

run 时间按 SIT-RP-0.1 固定 unknown/null/not_recorded_by_SIT-RP-0.1；工具版本为实际安装版本。in_process 的 raw_file_digest 为 null，并给出规定的说明；不计算对象指纹来代替文件摘要。

同一规范化输入、真实工具版本/profile、source mode 和完成状态应生成相同字节。真实时限中断可能因机器而异；不要求把不同完成状态伪造成相同输出。

### 4.4 披露与资源

披露由 runtime/disclosure.py 统一选择，两个 renderer 只使用同一份已选择的文档。禁止自动复制整条输入记录、excerpt、contact locator、actor display_name、identity_key、任意 extensions、绝对路径或身份映射。

契约要求的 IDs、method、context、native outcomes、qualification、共同来源与未知限制仍须保留。字段可能具有识别性；不得声称输出已匿名或可直接公开。需要另一个可分享快照时，沿用调用者准备新快照并重新审计的规则。

全过程使用同一 ledger、同一开始时刻及同一应急储备：

| 控制 | 保持的上限 |
| --- | ---: |
| 每 capability/scope job | 1,000,000 work units |
| 全调用，含应急预留 | 10,000,000 work units |
| 一次应急预留 | 1,024 units，包含在上项内 |
| 应急诊断 | 4,096 bytes |
| 协作式时限 | 60 秒 |
| retained witnesses / member occurrences | 20,000 / 100,000 |
| 每种报告编码，分别计算 | 67,108,864 bytes |
| 其他 WU9-L01 至 L10 | 全部保持冻结数值及计数规则 |

在操作前计费，等于上限允许，下一单位触发停止。访问、复制、排序比较、数值转换、字符扫描、编码、引用检查和 parity 检查均按架构 §19 计费。不得通过第二次 budget、隐式重试、跨 job 语义缓存或未计费的收尾扩大范围。

当前 _run_analysis 把预算保留在内部并消耗 finalization 路径。本阶段必须调整运行时组合，使正式报告继续取得原有受限 finalization port；不能先调用 _analyze_value 再新建 report budget。旧私有入口保留原有返回和停止语义。

为 WU9-L14 增加明确的输出限额传播及固定受限 port 能力；报告模块不能取得时钟、文件、原生加载或任意 runtime 操作权限。两个格式分别测量编码后字节；不能为了适配长度截断、删原因、丢未知字段或保留单边成功编码。

私有见证预留与最终 Finding 必须对账。同一已保留见证的链接复用不重复增加 witness 数；正式投影实际新增的 witness/member occurrence 按 L13 计入，不能漏算，也不能把全部私有预留再完整扣一遍。遍历、复制和输出的工作量仍分别收费。中断后的 L14 或其他收尾失败不得覆盖首先确立的停止原因及真实接纳状态。

| 情况 | 必须交付的实际状态 |
| --- | --- |
| 完成，包括合法 unavailable | completed audit envelope |
| 结构拒绝 | 可交付时为 validation_diagnostics，rejected |
| 接纳前资源中断 | 可交付时为 processing_diagnostics/interrupted/not_completed |
| 接纳后局部 job 中断，尚能完整收尾 | interrupted audit；只保留已原子提交的完整结果，未做部分 not_evaluated |
| 全局/时限/输出边界使合规收尾不可能 | 安全 AuditAbort；保存真实接纳状态，不交付片段 AuditReport |
| 实际运行缺陷 | 安全 failed processing envelope 或 AuditAbort/execution_failed |
| 调用者取消 | 独立 AuditCancelled，保留真实 input/publication state，不制造报告原因 |
| 非法可信调用选项 | AuditUsageError，尚未访问 dossier |

首先安全确立的停止原因控制后续交付。源记录中的 failed/unknown 是证据数据，不得决定 toolkit 的处理成功或失败。

## 5. 精确路径上限

下列编号只是本计划的路径索引，不进入产品。实施中某单元可修改的文件为第 6 节列出的编号集合；“允许”不意味着必须改动。新增测试使用列明文件，不能自行扩成 tests/**、src/**、tools/**。

所有未列路径继续冻结。已有文件不移动、不删除；新增文件不替换旧义务记录。批准后的本计划按准确字节冻结，除非得到明确修订。

### 5.1 产品路径，共 12 条

| ID | 路径 | 唯一允许目的 |
| --- | --- | --- |
| P01 | src/source_integrity_toolkit/contracts/report.py | 正式不可变报告类型、契约验证、投影辅助；保存旧私有契约 |
| P02 | src/source_integrity_toolkit/contracts/execution.py | 公共安全 transport 异常及受限报告收尾 port；保存旧私有停止语义 |
| P03 | src/source_integrity_toolkit/reporting/assemble.py | 有界 envelope、ID、引用、去重、domain/capability 组合 |
| P04 | src/source_integrity_toolkit/runtime/disclosure.py | 同一规定字段披露选择 |
| P05 | src/source_integrity_toolkit/reporting/escaping.py | 固定 J 字符编码及 Markdown 围栏安全 |
| P06 | src/source_integrity_toolkit/reporting/json_report.py | 正式 JSON 字节及有界编码 |
| P07 | src/source_integrity_toolkit/reporting/markdown_report.py | 固定 Markdown 字节及与同一 envelope 的一致性 |
| P08 | src/source_integrity_toolkit/runtime/resources.py | 原预算的报告计费、L14 与收尾边界；不改数值 |
| P09 | src/source_integrity_toolkit/runtime/diagnostics.py | 安全公开停止映射；不泄漏原生异常或改变旧私有交付 |
| P10 | src/source_integrity_toolkit/runtime/boundary.py | 单一执行上下文贯通，公共内存组合及保留旧私有入口 |
| P11 | src/source_integrity_toolkit/api.py | 激活 audit_bundle；audit_file 函数保持原有字节和立即拒绝 |
| P12 | src/source_integrity_toolkit/__init__.py | 明确七项公开名字、正确当前说明；无导入时执行 |

其余 36 条产品路径与基线字节一致。包括全部 analysis、graph、validation 产品模块、io 下所有模块、cli.py、contracts/bundle.py/evidence.py/results.py/constants.py 和其余 package __init__.py。不修改算法、词汇常量、输入 schema、包版本或模块清单。

### 5.2 当前验证控制，共 8 条

| ID | 路径 |
| --- | --- |
| V01 | tools/check_scaffold_boundary.py |
| V02 | tests/contract/test_verification_boundary.py |
| V03 | tests/scaffold/test_ci_contract.py |
| V04 | tests/scaffold/test_imports.py |
| V05 | tests/scaffold/test_module_manifest.py |
| V06 | tests/scaffold/test_no_runtime_implementation.py |
| V07 | tests/scaffold/test_layer_boundaries.py |
| V08 | .github/workflows/phase1-ci.yml |

这些路径只执行第 7 节的当前阶段迁移和直接控制。V08 仅允许必要的阶段身份、名称、凭据接线或上下文协调；不得更改 pins、权限、平台、Python minor、步骤数、触发器种类、预算、凭据通配范围或留存天数。无必要时保持原字节，phase3 字样可以作为既有凭据路径保留。

### 5.3 既有混合测试的限定迁移，共 11 条

| ID | 路径 | 允许修改的部分与保留要求 |
| --- | --- | --- |
| T01 | tests/scaffold/test_api_stubs.py | W08 改 bundle refusal 参数化及 unchanged-input 断言；保留 audit_file 拒绝和两函数参数签名 |
| T02 | tests/scaffold/test_packaging.py | W08 更新 test_wheel_installs_without_developer_tools 内公共调用预期；保留构建、成员、重建、安装、CLI 拒绝 |
| T03 | tests/security/test_scaffold_inertness.py | PROBE 中 bundle outcomes、对应计数和 hostile bundle mutation；保留全部效果 observer、file/CLI 拒绝和负向证明 |
| T04 | tests/security/test_preparation_inertness.py | test_whole_package_guard_rejects_forbidden_implementation_in_temporary_copy 的上下文和仍受保护 mutation 目标 |
| T05 | tests/integration/test_preparation_capability_boundary.py | 保留准备层分界；只迁移末尾 bundle refusal 及公开名字预期 |
| T06 | tests/contract/test_analytical_observability.py | 保留私有 immutable/no-public-report/no-options 断言；只迁移 bundle refusal、__all__ 和当前公开边界 |
| T07 | tests/contract/test_phase2_transition.py | 保留 W08 安装准备见证；仅更新当前阶段绑定、public bundle 交付和 receipt 断言 |
| T08 | tests/integration/test_analytical_installed_runtime.py | PROBE 的公开名字、bundle 调用和 receipt；完整保留原 hero、有限完成、非法输入、effects 和包字节见证 |
| T09 | tests/contract/test_phase3_transition.py | 剩余 source-extension 测试的 VC 上下文及 api 未激活预期；数据不能授权阶段或伪造 PC 完成的断言保留 |
| T10 | tests/contract/test_input_schema_mapping.py | test_no_runtime_schema_or_source_reads 中 report-schema 不存在断言转为本地 schema 正确存在；保留产品无 schema/source 文件读取 |
| T11 | tests/scaffold/test_contract_catalogs.py | test_schemas_are_documentation_only 中 report schema 清单及 README 状态；冻结的源和历史 catalog 保持 |

T07/T08 在 W01 仅更新当前上下文绑定，保留两个 API 的立即拒绝。到 W08 时，不能仅把 public_refusals 从 2 改成 1；须同时加入真实 audit_bundle 有效公共交付及两个编码的独立预期，并与 V03 receipt 校验原子更新。

V04–V07、V02 中把 api/reporting 当作永久未激活槽位的 fixture，可以在 W01 迁移成阶段相关断言或仍受保护的文件/native 槽位。仍须有活动报告代码的直接效果反例，不能把该项保障整体删除。

### 5.4 新测试及新案例，共 20 条

| ID | 路径 | 内容 |
| --- | --- | --- |
| N01 | tests/contract/test_report_contract.py | 根/嵌套 schema、状态组合及安全类型 |
| N02 | tests/contract/test_report_assembly.py | 私有到公共的显式投影、引用、domain/capability |
| N03 | tests/contract/test_report_identity.py | 语义排序、ID、去重、同 slot 冲突 |
| N04 | tests/contract/test_json_report.py | 精确 J 与 JSON 字节 |
| N05 | tests/contract/test_report_parity.py | 全部实质字段一致、mutant 拒绝及精确 Markdown |
| N06 | tests/contract/test_public_api.py | 公开签名、类型、methods、options、结果 |
| N07 | tests/contract/test_public_report_obligations.py | 57 字段/228 义务的公共层逐项断言 |
| N08 | tests/security/test_report_disclosure.py | 必需披露与禁止自动导出字段的双向 canary |
| N09 | tests/security/test_rendering.py | 围栏、HTML/链接/图片、控制符、多语言 |
| N10 | tests/security/test_report_resource_limits.py | L14、单一 ledger、计费与各阶段停止 |
| N11 | tests/security/test_public_api_boundary.py | hostile options/inputs、无效果、安全异常 |
| N12 | tests/integration/test_public_audit.py | 真实 audit_bundle 全路径、原 hero 和有限案例 |
| N13 | tests/integration/test_report_determinism.py | 置换、重复调用、污染、字节稳定及合法差异 |
| N14 | tests/integration/test_public_installed_runtime.py | 各构建形态真实离线安装后的公共行为 |
| N15 | tests/fixtures/micro/phase4_public_cases.json | 独立命名有限 dossier 及冻结来源/差异说明 |
| N16 | tests/fixtures/adversarial/phase4_report_cases.json | 合成隐私与呈现 canary、异常和反例资料 |
| N17 | tests/golden/phase4_report_expectations.json | 独立人工推导的语义与投影 oracle |
| N18 | tests/golden/phase4_reference_report.json | 一个有界完整参考 envelope 的预期 JSON 字节 |
| N19 | tests/golden/phase4_reference_report.md | 同一独立 oracle 的预期 Markdown 字节 |
| N20 | tests/contract/test_report_test_oracles.py | oracle 正例可接受及单属性 mutant 可拒绝的自检 |

N15–N19 在产品实现被用来生成预期之前先完成独立预期和来源依据。修正 oracle 必须指明源条款及原错误，不得通过重录实际输出消除差异。不修改既有四个 hero、原 logical golden 或 Phase 3 案例。N20 验证测试 oracle 的判别能力，不另建一个会扩大生产能力的 public validator。

### 5.5 schema 与阶段记录，共 8 条

| ID | 路径 | 处理 |
| --- | --- | --- |
| D01 | PHASE_4_PLAN.md | W01 加入获准准确字节；此后冻结 |
| D02 | schemas/report/sit-report-0.1.schema.json | 新增正式报告结构 schema |
| D03 | schemas/report/README.md | 更新该 schema 的真实范围和限制 |
| D04 | phase4/report_contract_coverage.json | 新增公共投影、逐条 report 义务及来源/测试位置；不是 runtime authority |
| D05 | phase4/implementation_evidence.json | 各单元简明执行记录、测试替代去向及真实状态；不是权限授予源 |
| D06 | phase4/ci_review.md | 一次当前迁移、有限工具链评估与凭据限制 |
| D07 | PHASE_4_COMPLETION.md | 最终范围、测试事实、未完成项及所有者验收提交 |
| D08 | README.md | 真实阶段状态、公开调用示例、当前完整验证命令及未完成功能 |

共计 59 条路径上限：12 产品、8 当前控制、11 混合测试、20 新测试/案例、8 schema/记录。路径编号区间在后文仅代表此处逐条列出的封闭集合，不是目录通配权限。

D04/D05/D06 不导入产品、不通过设置 approved=true 获得权限。旧 phase2/phase3/scaffold catalogs、manifests、transition ledger、VC map/completion 及冻结规范全部保持。没有新的通用 manifest 框架或可无限追加的迁移链。

## 6. 十个顺序工作单元

每个单元开始前，核对已批准计划、实际前一检查点与该单元路径集合。完成时在 D05 记实际变更、直接检查、反例、失败及停止状态。D05 是各单元共同可写的唯一记录；禁止通过共同记录改变本计划权限。

审批整个阶段并授权连续执行后，在既定范围内无需逐项重新取得同一种授权。仅授权某一单元时，完成该单元后按用户指令继续。任何阶段合并与正式发布不由自动测试代为授权。

### P4-W01：当前基线与验证切换

- **前提：** 本计划获准，main 仍为第 2 节锚点；若已变化，先检查新变化，不能默默重新设锚点。
- **可修改：** V01–V08，T04、T07、T08、T09，D01、D04、D05、D06、D08。
- **工作：** 一次性切换到 P4 当前授权；建立所有十个单元的精确路径及产品激活表。迁移现有 context/receipt 身份，但保持两个 audit API 的当前拒绝。D04 只建立尚未完成的义务骨架及来源定位。D08 只更新接受事实和计划状态。
- **验收：** 基线正例先通过；错误 repo/base/head/footer、提前激活、越权路径、脏 index/worktree、隐藏中间改动及 merge side 均拒绝；旧历史加载与阶段重演仍为零；无产品字节变化。
- **停止点：** 当前 P4 验证能直接执行；不把 W01 称为公共功能已完成。

### P4-W02：正式报告契约、schema 与独立参考预期

- **可修改：** P01、P02，T10、T11，N01、N15、N17、N18、N19、N20，D02、D03、D04、D05。
- **工作：** 定义不可变 AuditReport 和安全 transport 声明、局部引用/嵌套对象；建立 closed schema；显式记录每个私有到公共映射和既有规范来源。N18/N19 为小型可完整运行案例的独立精确预期。
- **验收：** 正常契约各变体先通过，随后拒绝缺失/额外成员、非法状态组合、错误类型、错命名空间和错误值；16 根字段及嵌套成员逐项覆盖；没有虚构的新 metric/Reason/root 字段；旧私有类型仍通过原测试。
- **停止点：** 没有公共 audit 执行，API 仍拒绝；类型存在不代表可构造已完成审计。

### P4-W03：正式组装、稳定 ID 与引用闭合

- **可修改：** P01、P03，N01、N02、N03、N15、N17、N20，D04、D05。
- **工作：** 用有界内部结果建立 root/run/input 元数据；按语义 anchor 排序、去重、命名，组合 scopes/populations/checks/basis/capabilities/domains/results/findings/reasons；对披露输入使用显式内部契约。
- **验收：** 多 inquiry 仍只有五个普通报告 domain；15 家族和四态分区一致；所有输入/报告引用独立闭合；不同输入 ID 不合并；相同 slot 异值失败；Reason 循环不递归爆炸；发现顺序、输入数组置换不影响应当稳定的身份；原生有序数组不乱序。
- **停止点：** 对外入口仍拒绝。该单元的项目内可信构造 fixture 不能代替真实调用证据。

### P4-W04：统一披露与隐私边界

- **可修改：** P01、P03、P04，N02、N08、N15、N16、N17、N20，D04、D05。
- **工作：** 显式逐字段实现 basis/disclosure/witness 选择；接通组装的唯一披露来源。禁止通用 dataclass/source record 输出。
- **验收：** 整记录、excerpt、contact/display_name/identity_key/extensions/path canary 不自动输出；必需 IDs、method/context/native outcome/qualified limitations canary 正确保留；共同来源、未知祖先和受保护关系不被改成独立；当前输出无匿名化或可公开保证。
- **停止点：** 若某个必要解释与允许披露确实矛盾，停止受影响投影并提交具体条款问题，不能静默删信息。

### P4-W05：精确 JSON 与有界编码

- **可修改：** P01、P02、P05、P06、P08、P09，N04、N10、N16、N17、N18、N20，D04、D05。
- **工作：** 实现 J 字符、键序、精确数值和单 LF；通过受限 port 逐步计算编码字节、传播 L14。P02/P08/P09 只增加该输出边界的当前契约，不改预算数值或 private 停止语义。
- **验收：** 逐字节匹配独立参考；portable integer/bool、原始分数、极小 exact decimal、控制字符、合法多语言和 ordered arrays 正确；不调用自定义 default/repr；JSON 大小低于/等于/超过限额及中途停止有证据。
- **停止点：** 未完成 Markdown/运行时组合，不交付公共 AuditReport。

### P4-W06：精确 Markdown 与两种格式一致性

- **可修改：** P05、P07，N05、N09、N10、N16、N17、N19、N20，D04、D05。
- **工作：** 精确实现固定布局、pretty-J、变长围栏、Reason details 和 available fraction 的 decimal 行；两个 renderer 只消费同一冻结契约。
- **验收：** 独立预期逐字节匹配；测试独立解析 Markdown 规定区块，对照逻辑 oracle 与 JSON；删除未知字段/原因/反证/分母/qualification 的 mutant 被拒绝；反引号、HTML、图片、autolink、换行、ANSI/bidi 不能逃出数据位置；两种格式各自长度边界和 no-clipping 均覆盖。
- **停止点：** 无任意原文标题、无启用网络或浏览器的报告元素。

### P4-W07：单次预算贯通与真实停止交付

- **可修改：** P01、P02、P03、P04、P05、P06、P07、P08、P09、P10，N01、N02、N08、N10、N11、N12、N15、N16，D04、D05。
- **限制：** P03–P07 只用于组合和计费/停止接线，不借此修改已验收字段或编码规则。
- **工作：** 捕获、全结构/有限 job 计划、分析、披露、组装、ID、两编码、必要一致性检查共享同一 ledger/deadline/reserve；保留原有 private preparation/analysis 返回与行为。
- **验收：** 禁止 second-budget/restart；在每个阶段注入有限内部时钟/配额/故障，核对第一原因、accepted/not_completed、无私有输入泄漏和 partial-report 拒绝；取消独立；原私有同输入回归保持；无 native/file/network 权限穿透；成功返回前两份 bytes 完整且不持有原始源树/预算。
- **停止点：** 仅项目内部公共组合路径可测试；api.py 仍拒绝。

### P4-W08：激活公共 audit_bundle 并迁移旧拒绝断言

- **可修改：** P01、P02、P10、P11、P12，V03，T01、T02、T03、T05、T06、T07、T08，N06、N11、N12、N14、N15、N16，D04、D05、D08。
- **限制：** P01/P02/P10 只处理公开类型及 trusted invocation 接线；V03 只处理新公共成功见证与保留 file 拒绝的 receipt 对账，不扩大权限或改预算。
- **工作：** 激活精确签名、七项公开名字、只读缓存方法、使用错误；原拒绝测试迁移为直接有效/无效/恶意调用断言。三种已安装分发形态的当前 receipts 同步记录真实公共返回及 audit_file 拒绝。
- **验收：** 用户确实可 import、提交有限有效 dossier、读取 16 根逻辑 envelope 和两 bytes；None/{} / false 等价；true/未知键/恶意类型在 dossier 访问前安全拒绝；冻结输入及嵌套数据不变；所有已公开失败类型安全；反复读取 bytes 不触发新工作；audit_file 和 CLI 全部旧拒绝保障仍过。
- **停止点：** README 如实标明内存可用、文件/CLI 审计未完成，保持 dev 版本。

### P4-W09：公共语义义务与独立反例闭合

- **可修改：** N01–N13、N15–N20，D04、D05。
- **工作：** 对 57 字段的 228 项原义务逐项记录 core evidence、public-envelope evidence、rendering evidence 以及尚未适用的文件/发布条款；加入真实 public pipeline 和独立期望；执行原四个 hero 的公共路径。显式 sweep 24 PC、40 Reason codes、22 finding conditions 和 6 observation kinds，逐项记录公开保留、拒绝或尚不允许触发的条件，保留来源原生状态与 toolkit 状态的区别。
- **验收：** 所有本阶段字段/嵌套/共享义务都有来源到实际断言的映射；原 49 个 output-mutant negatives 从符合完整公共契约的报告开始，单改指定属性后拒绝；8 个 input-delta negatives 保留其不同性质；先验证 unchanged conforming baseline；不能以永远拒绝的 oracle 通过负向检查。
- **原 hero：** 使用原输入及不变预算，记录真实完成或停止，校验停止前后状态与无错误 salvage。用独立命名的有限真实 API 案例完成各字段的公共正/负/缺失/边界证明；不称其为原始 H7 全字段完成。
- **停止点：** 若发现产品缺陷，回到原 owner 单元的精确范围修复并重新验证受影响检查；W09 不直接取得产品路径权限。改变阶段编号或 footer 不能掩盖未经授权的修复。

### P4-W10：安装、四环境终验与交接

- **可修改：** N14，D04、D05、D06、D07、D08。
- **工作：** 固定完整候选；验证 clean offline installed 的实际公共报告、既有私有见证及 file/CLI 拒绝；完成四环境、范围、原始凭据、义务映射和停止限制审阅。
- **验收：** 第 8 节所有技术门槛通过，最终准确 head 有四 profile 成功和原始记录；新包源模块及实际运行一致；无依赖/算法/冻结规范偷改；报告真实剩余工作。
- **停止点：** 提交所有者验收。未获合并指令前保持实施 PR 可审阅；不打版本 tag、不上传 release、不启动后续 native/CLI 阶段。

若后期失败要求回到已完成单元，记录“回到 P4-Wxx 的哪项修复”及实际提交，按该单元原路径/目的限制执行。已实现功能状态不回退；不能用回退编号解除当前活跃功能的安全检查。需要原单元范围以外的文件或语义变化时，提交明确修订。

## 7. 验证启动、执行与减负规则

### 7.1 本次计划交付与实施启动

当前 VC guard 只承认 verification/consolidation、VC footer 及原 VC 精确路径。新 PHASE_4_PLAN.md 的 planning-only PR 会被该 guard 拒绝。

因此本次只交付外部计划稿。批准后由 W01 在 phase4/public-report 分支完成一个原子 bootstrap：加入获准计划的准确字节，同时切换当前 guard 和直接测试。不冒用 VC、不把计划 PR 伪装成旧单元、不先合并未经允许的红灯变更。

W01 外部审核基准是已接受 merge/tree/parents、所有者实际批准和准确计划字节。计划的 SHA-256 由批准后的文件计算并钉住；本文件不写自己的哈希，避免循环引用。新的策略源码、候选记录或 footer 自述不能单独证明授权。任何 branch protection 或必需检查保持有效。

### 7.2 当前授权与产品激活

- 使用真实平台事件、repo、base/head、branch、run/attempt 及 checkout；要求同仓库 phase4/public-report -> main。
- 单元标记读取已校验实际 head commit message 中唯一精确行 SIT-Phase-Unit: P4-Wnn，nn 仅限 01–10。PR 事件先核实 head SHA，再读取其真实 Git commit；不从候选 dossier、环境任意值或 PR 标题推断。push 还要求实际 event 的 head_commit.id/message 与该 commit 相符。拒绝重复、混合 VC/P2/P3、未知单元或实际 head 不一致。
- 每个实施提交记录修改所归属的单元；检查从 fdad8c3 起每个提交及每条 parent edge 的文件和许可目的，包含中间越权后恢复及 merge sides。每个单元第一次出现须按 W01 至 W10 的依赖顺序，不能跳过前置检查点。修改权限按该提交的 owner 单元，已激活功能状态按经过验证的祖先检查点单调保持；例如 W08 后的 W02 修复仍验证七项 exports 和公共成功行为。
- 已批准完整计划中的激活表是先决条件，单元标签本身不给予新权力。W02 之前不得加入产品行为；P03 从 W03、P04 从 W04、P05/P06 从 W05、P07 从 W06、P10 从 W07、P11/P12 从 W08 才取得相应行为。P01/P02 从 W02，P08/P09 从 W05 仅取得限定报告支持。
- 修复可回到已获准单元的路径目的，但当前验证必须继续覆盖已实现功能；不得把阶段上下文降级来重新接受旧拒绝或跳过公共行为。
- 接受锚点之前不重演历史开发步骤；保留 frozen baseline 和当前范围检查，拒绝不完整/替换/伪造 Git history、dirty index/worktree、未允许 untracked 代码及候选遗漏。
- 继续在现有工具与 test_verification_boundary.py 内维护直接正反例，不新增 test_phase4_transition.py、旧源码 loader 或自证 approval registry。
- 旧保障转成当前行为的去向记录在 D05，一次审查后保留；不成为未来每日历史 replay 的输入。

**合并的归属规则：** 正常最终 merge 的 tree 必须与已验收候选 tree 一致。先按各原 owner 单元验证候选及 side ancestry 的全部提交，再确认相对 main parent 的累计差异只继承这些已验证变化；不能把该累计差异全部当作 W10 新修改。分支内 merge 同样区分继承变化与新变化，不整体豁免 merge。任何冲突解决或 merge 新增字节仍须归属实际有权的单元并通过其范围及行为检查；这会形成新候选，需要重新验证，不能直接引用旧候选验收。W10 不因此扩大到任意产品文件。

### 7.3 local 与 hosted 验证

保留单一本地完整入口：

~~~sh
python -m pip install -r requirements-dev.txt
python -B tests/scaffold/test_ci_contract.py --local --evidence-dir ../sit-p4-local-evidence
~~~

每次使用新的证据目录。local 记录实际本地源码、工具、完整集合及结果，不伪造 GitHub event。它不能代替 hosted 的外部上下文和四 profile 门槛。裸 pytest 的默认 scaffold 范围仍不能宣称完整验证。

既有矩阵及限额不变：

| 配置 | 要求 |
| --- | --- |
| OS × Python | ubuntu-24.04 / windows-2025 × 3.11 / 3.13 |
| suite / job | 2,400 秒 / 50 分钟 |
| 依赖 | requirements-dev.txt 与 build pins 原字节；零第三方 runtime dependencies |
| Actions | 三个原 immutable pins；read-only token；不保留 checkout credentials |
| 检查目录 | scaffold、security、contract、unit、integration 五目录全部收集 |
| 对账 | 精确 collected identities 与 JUnit 对齐；successful subtests 单独记录 |
| 失败 | failure/error/skip/incomplete 不算成功；保持 timeout 与异常的原始 stdout/stderr/status |
| 凭据 | 真实 head、run/attempt、profile 和事件语义绑定；evidence/upload 保留 always() |
| 安装包 | 六份既有构建 inventory、三种分发形态的干净离线安装与模块哈希；原准备/分析见证保留，增加公共实际行为 |

新 report schema 是仓库开发契约资料，本阶段不改变 MANIFEST.in 或包数据规则，也不声称 wheel 内含该 JSON schema。已安装产品不读取仓库 schema 或测试文件。

可在不同单元只运行有明确影响范围的直接检查，报告其实际范围。完整候选终验必须运行全套；不人为加新一层每日完整矩阵，也不跳过 GitHub 已配置的必需工作流。阶段开发中若有 hosted 运行，同样按真实结果记录。

Documentation-only 仅允许最终单独改动 PHASE_4_COMPLETION.md 和 phase4/implementation_evidence.json 两个非执行记录，且当时变化区间每个 parent edge 都只含这两条路径。它仍检查权限、实际 checkout、冻结字节和当前范围，明确说明未运行完整测试。

README 是包 metadata；本计划、schema、coverage/test oracle、guard、test、workflow、产品代码均走 full。记录不得被产品、授权策略、收集选择或打包读取后还声称 documentation-only。空、未知、混合或中间 executable 后恢复的改动走 full。

### 7.4 工具链与执行凭据

W01 对既有 pins 的当前官方安全通告/可用性作一次有界评估，记录时间、适用性和无法确认部分。不因有新版本就升级。发现必要升级时提交明确依赖修订，不绕过安装版本 gate 或悄悄使用预装工具。

最终运行保存 collection、JUnit、原始日志、实际版本、before/after tracked-byte 对账、six inventories、准备/分析/公共 installed receipts 和失败状态。公共 receipt 必须绑定实际 module hashes、输入/独立预期及两种编码结果，不能仅记录 audit_bundle 被调用过。

尽量在现有 installed receipt 中整合公共见证，复用同一已构建分发形态，避免再加一套重复构建矩阵。N14 可提供调用和断言，不能把未执行的助手函数视作安装证据。

上传范围仍为现有 JSON/XML/log。任何 archive 或原始 event 未上传的事实在完成记录明示；不宣称完整 archive 重现或原事件字节已独立复核。真实失败保存后按原因修复，不用无说明重试覆盖原尝试。

## 8. 阶段验收门槛

必须全部满足以下技术门槛，再提交所有者验收：

| 门槛 | 必须提供的证据 |
| --- | --- |
| G01 范围与来源 | 精确锚点/获准计划、59 路径上限及各单元 purpose 审查；36 非授权产品路径和全部其他冻结文件字节不变 |
| G02 原核心保持 | 既有准备/分析语义、graph/lineage/来源独立性/缺失信息/修正结果直接测试继续有效 |
| G03 报告契约 | 三类 report kind、所有合法 run/input 与 Result 状态组合、16 根及所有嵌套成员、正确 schema 和引用闭合 |
| G04 每字段公共覆盖 | 57 字段/228 原 ID 保留逐项来源，明确完成公共 envelope/rendering 条款及仍延期条款；24 PC、40 Reasons、22 conditions、6 observation kinds 显式 sweep，含 dormant 禁用条件；非测试数总结 |
| G05 反例有效性 | 49 output-mutant 和 8 input-delta negatives 按原类别测试；oracle 先接受 conforming baseline，再拒绝指定单属性错误 |
| G06 ID 与确定性 | 全语义身份/去重、不同输入 ID 保留、跨 inquiry、引用循环、输入置换、合法有序数组及重复运行控制 |
| G07 精确双格式 | 独立 golden 的精确字节、Markdown 独立区块对账、所有原因/未知/反证/分母/限制保留 |
| G08 隐私与效果 | 双向 canary、惯常及恶意 Unicode/markup、无原始输入泄漏、无文件/网络/native/模型/日志行为 |
| G09 单预算与停止 | 一个 ledger/deadline/reserve，L14 两种编码分别边界，逐阶段取消/故障/中断，真实接纳状态及无 partial success |
| G10 真实 API | 七项 export、签名、options 优先校验、深不可变、两只读 bytes 方法、safe failures 和未触碰 audit_file/CLI |
| G11 实际案例 | 有限完整公共正例及各义务；四个原 hero 的真实公共执行状态和限制，不以组件/fixture 代替原 hero 完成 |
| G12 安装/平台 | 四 profile 的实际安装包源字节、准备/分析/公共见证及无开发目录依赖；不宣称 native 文件平台认证 |
| G13 最终 head | 一个固定最终 executable candidate 的完整四环境成功，准确集合/JUnit/subtests、无 fail/error/skip/incomplete；原始凭据核对 |
| G14 交接与接受 | D07 如实列出能力、未完成项和证据限制，提供用户接受对象；所有者明确验收单独记录 |

G04 不自动把所有 228 项完整 release obligation 宣告关闭。公共层已经验证的子条款、文件模式/发布尚未验证的子条款必须分栏。26 个共享验证家族及 35 条 Trace 也只按实际覆盖范围记账，特别保留 SIT-VG023 文件/内存等价和 SIT-VG026 发布条款的未完成部分。

若最后一次完整运行后只追加允许的非执行接受记录，可用外部 PR 记录和文档 successor 说明直接测试 head 与相同 executable bytes；不得把 successor 的有限检查叫作其全套运行。新增代码/schema/README/测试或改变实质行为后，最终 candidate 必须重新完成所需全矩阵。

## 9. 停止条件、修复与审批

以下情况停止受影响工作，提出具体、最小修订：

- 需要修改被冻结的分析语义、输入/图模块、原 hero 或逻辑 oracle，或新增指标/字段/Reason。
- 需要第 5 节以外文件、新产品模块、新依赖、Action/dependency pin、权限/平台/预算变化。
- 正式 report 形状无法保留已批准含义，或允许披露与必需依据存在具体冲突。
- 现有计费使本阶段必要的有限案例也无法合规完成，且修复超过许可范围。
- 无法取得实际基线/原始凭据、需要放宽 branch protection、无法证明旧安全保障的当前等价。
- 某环境不能满足必需能力；不得静默 xfail、skip、换平台或泛化其他环境成功。

正常范围内的实现缺陷、文档错误和测试接线可以按 owner 单元修复，不需要为同一已授权事项重复审批。保留失败证据和修复依据；不强推 main、不 reset 接受历史、不删除旧证据。

本轮起草任务到可审阅计划交付结束。建议批准指令：

**“批准 PHASE_4_PLAN.md，启动 P4-W01。”**

如希望按上述十个单元连续执行，可明确增加“按计划继续至 P4-W10”；期间仅在真实范围/语义/权限阻塞或需要所有者最终验收时暂停。接受整个阶段、合并实施 PR 和正式发布保持各自明确授权。

## 10. 本计划起草核验记录

- 从 GitHub 克隆并检查实际 fdad8c3 与 tree f6fbb89；211 tracked files，读取本计划所引冻结规范和相关当前产品/测试源码。
- 核实 PR #35 的所有者接受与 merge，核实 merge 后四环境 CI 已成功；新功能尚未执行测试。
- 将报告契约、运行时预算和验证迁移分成三项只读协作审查，合并其具体发现。
- 找到并列明既有 public refusal、schema absence、__all__、protected slot、runtime-to-report 依赖与 installed receipt 的实际迁移点。
- 明确私有源树、native_records、per-inquiry domains、witness references 和 full-body dedup 不能直接拷贝为公共报告。
- 交付前检查路径编号、单元范围、59 条路径的存在/新增归类、重复/未定义编号、链接/Markdown 结构、仓库未改动及文件 SHA-256。
- 本轮没有产品实现、仓库写入、新 CI、远程 PR、发布或原理论论文修改。基线成功只支持基线状态，不能作为 Phase 4 功能已完成的证据。

