# Phase 2 test transition ledger

## Authority and identity

The owner approved the exact Phase 2 plan and authorized P2-W01. PR #9 was merged as `eb730dda31d189c8487b5247a45bae47b678821b`. This ledger changes no historical result. Phase 1 review head was `f7a0ecad3ff1c472c55698748d0d4fd33633610d`, accepted main merge `d7d73a790a2a627d19307c9dd48281eff3017023`. The 194 original collected identities below come from the inspected run 35385818222 artifacts; all four rows agree. Its 420 successful subtest events per row are distinct from 194 top-level tests.

No test is deleted, renamed, skipped, xfailed or deselected here. The replacement identity is unchanged. 'Adapted' identifies files in which a phase-specific assertion or test context changes; every other assertion in those files remains binding. Existing source/record/oracle/packaging/API/isolation protections continue to execute. New tests are additional and never replace a missing historical identity.

Canonical identity digest is SHA-256 of sorted original node IDs joined by LF plus a final LF:
`3262e08ba9825a41ab78ba55845a9f45ccf3195d3f33dc030cc28ce772eedc83`

## Exact assertion migrations

| File | Retained obligation and bounded adaptation |
|---|---|
| `tests/scaffold/test_imports.py` | Adapt only the live-slot form check; retain 48 import instances, exact paths and fresh-process effects guard. |
| `tests/scaffold/test_module_manifest.py` | Keep historical catalog states and pins; compare promoted code to independent live checks; keep owners, mutation probes and no catalog runtime import. |
| `tests/scaffold/test_no_runtime_implementation.py` | Keep all destructive controls; copy the explicit Phase 2 policy context into temporary workspaces; protected bodies and API refusal remain exact. |
| `tests/scaffold/test_layer_boundaries.py` | Allow reviewed standard-library imports only in promoted modules; retain forbidden directions, cycles and cross-project/native/network probes. |
| `tests/scaffold/test_contract_catalogs.py` | Keep all frozen source/Trace/field/228 obligations and mutation probes; adapt only the schema reservation assertion at its authorized later unit. |
| `tests/scaffold/test_ci_contract.py` | Retain all 20 CI/JUnit controls; adapt phase labels, complete history, trusted unit context and cumulative collection. Add entry/path/transition checks. |

### Stage authority and no self-approval

The current W01 product promotion list is empty. All 48 product modules keep their accepted bytes. The thirteen future candidates and earliest units are independently enumerated in the checker and corroborated against the SHA-256-pinned plan. The other 35 never acquire behavior under this plan.

The unit argument belongs to the developer invocation, outside product data and candidate policy. CI supplies it from the exact `phase2/p2-wNN` review branch; the main push uses a required `SIT-Phase-Unit: P2-WNN` merge-message footer. A local invocation may use `--unit`, with W01 as the conservative default. A policy must match that separately supplied unit and cannot advance it. These mechanical checks do not authenticate conversational owner approval; review/merge authorization remains a separate human gate. No privileged workflow or secret is used.

Changing policy plus code to promote W02 while the trusted work unit is W01 fails. Changing the plan or entry manifest and their adjacent metadata fails the independent digests. Promoted files retain syntax/import/effect checks and later behavioral conformance tests. Static checks are deliberately bounded and are not a general Python sandbox or proof of semantic correctness.

A new input schema is absent in W01. From W02 only the exact bundle schema path is admitted; the report schema remains absent. The broader structure/runtime distinction is tested by W02, never counted as exercised by W01.

## Original-to-current collected identities

| Original collected node | Disposition | Current collected node |
|---|---|---|
| `tests/scaffold/test_api_stubs.py::test_file_stub_neither_reads_nor_creates` | retained | same |
| `tests/scaffold/test_api_stubs.py::test_first_executable_statement_is_refusal[audit_bundle]` | retained | same |
| `tests/scaffold/test_api_stubs.py::test_first_executable_statement_is_refusal[audit_file]` | retained | same |
| `tests/scaffold/test_api_stubs.py::test_hostile_arguments_and_options_remain_untouched[audit_bundle]` | retained | same |
| `tests/scaffold/test_api_stubs.py::test_hostile_arguments_and_options_remain_untouched[audit_file]` | retained | same |
| `tests/scaffold/test_api_stubs.py::test_plain_bundle_remains_unchanged` | retained | same |
| `tests/scaffold/test_api_stubs.py::test_reserved_signatures` | retained | same |
| `tests/scaffold/test_baseline_integrity.py::BaselineGuardTests::test_actual_pinned_manifest_is_accepted_without_override` | retained | same |
| `tests/scaffold/test_baseline_integrity.py::BaselineGuardTests::test_actual_reference_document_exact_bytes` | retained | same |
| `tests/scaffold/test_baseline_integrity.py::BaselineGuardTests::test_changed_approval_and_plan_each_fail` | retained | same |
| `tests/scaffold/test_baseline_integrity.py::BaselineGuardTests::test_duplicate_key_parser_rejects` | retained | same |
| `tests/scaffold/test_baseline_integrity.py::BaselineGuardTests::test_editing_file_and_manifest_cannot_self_approve` | retained | same |
| `tests/scaffold/test_baseline_integrity.py::BaselineGuardTests::test_empty_checkout_cli_fails_even_under_optimization` | retained | same |
| `tests/scaffold/test_baseline_integrity.py::BaselineGuardTests::test_missing_file_is_not_a_pass` | retained | same |
| `tests/scaffold/test_baseline_integrity.py::BaselineGuardTests::test_newline_conversion_is_detected` | retained | same |
| `tests/scaffold/test_baseline_integrity.py::BaselineGuardTests::test_single_changed_byte_is_rejected` | retained | same |
| `tests/scaffold/test_baseline_integrity.py::BaselineGuardTests::test_synthetic_complete_twenty_file_positive` | retained | same |
| `tests/scaffold/test_baseline_integrity.py::BaselineGuardTests::test_unsafe_and_nonregular_inputs_fail` | retained | same |
| `tests/scaffold/test_ci_contract.py::CiContractTests::test_broad_artifact_upload_fails` | adapted | same |
| `tests/scaffold/test_ci_contract.py::CiContractTests::test_cache_or_secret_injection_fails` | adapted | same |
| `tests/scaffold/test_ci_contract.py::CiContractTests::test_duplicate_keys_fail` | adapted | same |
| `tests/scaffold/test_ci_contract.py::CiContractTests::test_ignored_failure_fails` | adapted | same |
| `tests/scaffold/test_ci_contract.py::CiContractTests::test_missing_guard_stage_fails` | adapted | same |
| `tests/scaffold/test_ci_contract.py::CiContractTests::test_missing_lower_bound_fails` | adapted | same |
| `tests/scaffold/test_ci_contract.py::CiContractTests::test_missing_platform_fails` | adapted | same |
| `tests/scaffold/test_ci_contract.py::CiContractTests::test_mutable_action_pin_fails` | adapted | same |
| `tests/scaffold/test_ci_contract.py::CiContractTests::test_privileged_trigger_fails` | adapted | same |
| `tests/scaffold/test_ci_contract.py::CiContractTests::test_saved_checkout_credentials_fail` | adapted | same |
| `tests/scaffold/test_ci_contract.py::CiContractTests::test_skipped_test_step_fails` | adapted | same |
| `tests/scaffold/test_ci_contract.py::CiContractTests::test_untrusted_shell_expression_fails` | adapted | same |
| `tests/scaffold/test_ci_contract.py::CiContractTests::test_workflow_is_closed_and_minimal` | adapted | same |
| `tests/scaffold/test_ci_contract.py::CiContractTests::test_write_permission_fails` | adapted | same |
| `tests/scaffold/test_ci_contract.py::JunitAccountingTests::test_failure_element_overrides_false_zero_header` | adapted | same |
| `tests/scaffold/test_ci_contract.py::JunitAccountingTests::test_invalid_aggregate_and_skipped_child_do_not_pass` | adapted | same |
| `tests/scaffold/test_ci_contract.py::JunitAccountingTests::test_missing_collected_result_is_rejected` | adapted | same |
| `tests/scaffold/test_ci_contract.py::JunitAccountingTests::test_subtest_aggregate_does_not_inflate_top_level_count` | adapted | same |
| `tests/scaffold/test_ci_contract.py::JunitAccountingTests::test_subtest_failure_in_suite_cannot_be_lost` | adapted | same |
| `tests/scaffold/test_ci_contract.py::JunitAccountingTests::test_unknown_or_duplicate_test_identity_is_rejected` | adapted | same |
| `tests/scaffold/test_cli_scaffold.py::test_audit_refuses_without_touching_paths[extra0]` | retained | same |
| `tests/scaffold/test_cli_scaffold.py::test_audit_refuses_without_touching_paths[extra1]` | retained | same |
| `tests/scaffold/test_cli_scaffold.py::test_audit_refuses_without_touching_paths[extra2]` | retained | same |
| `tests/scaffold/test_cli_scaffold.py::test_audit_refuses_without_touching_paths[extra3]` | retained | same |
| `tests/scaffold/test_cli_scaffold.py::test_audit_refuses_without_touching_paths[extra4]` | retained | same |
| `tests/scaffold/test_cli_scaffold.py::test_help[args0]` | retained | same |
| `tests/scaffold/test_cli_scaffold.py::test_help[args1]` | retained | same |
| `tests/scaffold/test_cli_scaffold.py::test_help[args2]` | retained | same |
| `tests/scaffold/test_cli_scaffold.py::test_help[args3]` | retained | same |
| `tests/scaffold/test_cli_scaffold.py::test_help[args4]` | retained | same |
| `tests/scaffold/test_cli_scaffold.py::test_other_requests_refuse_without_argument_echo[args0]` | retained | same |
| `tests/scaffold/test_cli_scaffold.py::test_other_requests_refuse_without_argument_echo[args1]` | retained | same |
| `tests/scaffold/test_cli_scaffold.py::test_other_requests_refuse_without_argument_echo[args2]` | retained | same |
| `tests/scaffold/test_cli_scaffold.py::test_other_requests_refuse_without_argument_echo[args3]` | retained | same |
| `tests/scaffold/test_cli_scaffold.py::test_version` | retained | same |
| `tests/scaffold/test_contract_catalogs.py::ContractCatalogTests::test_all_obligation_and_code_references` | adapted | same |
| `tests/scaffold/test_contract_catalogs.py::ContractCatalogTests::test_complete_primary_source_bytes` | adapted | same |
| `tests/scaffold/test_contract_catalogs.py::ContractCatalogTests::test_control_case_groups_and_exact_future_paths` | adapted | same |
| `tests/scaffold/test_contract_catalogs.py::ContractCatalogTests::test_cross_references_are_closed` | adapted | same |
| `tests/scaffold/test_contract_catalogs.py::ContractCatalogTests::test_data_handling_ids_and_reference_closure` | adapted | same |
| `tests/scaffold/test_contract_catalogs.py::ContractCatalogTests::test_duplicate_json_keys_are_rejected` | adapted | same |
| `tests/scaffold/test_contract_catalogs.py::ContractCatalogTests::test_mutations_cannot_drop_field_or_replace_primary_trace` | adapted | same |
| `tests/scaffold/test_contract_catalogs.py::ContractCatalogTests::test_mutations_cannot_relabel_test_cells_or_drop_codes` | adapted | same |
| `tests/scaffold/test_contract_catalogs.py::ContractCatalogTests::test_schemas_are_documentation_only` | adapted | same |
| `tests/scaffold/test_contract_catalogs.py::ContractCatalogTests::test_surrounding_qualifications_stay_binding` | adapted | same |
| `tests/scaffold/test_contract_catalogs.py::ContractCatalogTests::test_trace_owner_family_and_field_equality` | adapted | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_completion_intervals_keep_units` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_control_index_preserves_adopted_w03_bindings` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_correction_submission_handling_and_changes` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_distinct_complete_snapshot_envelopes` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_duplicate_json_keys_are_not_hidden` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_exact_asset_inventory_and_manifest_hashes` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_exact_disposition_vocabulary` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_expanded_fixture_field_sets_are_closed` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_field_and_reason_names_exist_in_adopted_catalogs` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_finite_witnesses_are_transcribed_from_source_table` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_frozen_case_sources_match_full_bytes` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_hhi_oracles_preserve_source_fractions_and_blockers` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_ids_and_direct_references` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_logical_assets_do_not_claim_execution` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_main_record_and_assertion_inventory` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_micro_index_matches_all_source_sections` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_native_roles_anomaly_and_unknown_metadata` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_negative_probes_detect_transcription_damage` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_no_metadata_edge_becomes_acquisition` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_origin_and_immediate_partitions_are_static_oracles` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_original_support_excerpts_exactly_match_source` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_pipeline_matrix_unchanged_with_unknown_use` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_qualified_comparison_and_human_independence_stay_separate` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_seed_sets_and_independent_populations` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_seven_acquisition_rows_match_authoritative_table` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_v01_is_only_seed_selection` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_v02_precise_delta_and_old_coverage` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_v03_precise_delta_without_weights` | retained | same |
| `tests/scaffold/test_fixture_integrity.py::FixtureIntegrityTests::test_whole_source_sections_are_bound` | retained | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[__init__.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[analysis/__init__.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[analysis/context.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[analysis/contribution_profile.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[analysis/correction_outcomes.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[analysis/correction_routes.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[analysis/evaluator_lineage.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[analysis/findings.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[analysis/human_review.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[analysis/inventory.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[analysis/origins.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[analysis/presence.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[analysis/process_comparison.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[api.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[cli.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[contracts/__init__.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[contracts/bundle.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[contracts/constants.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[contracts/evidence.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[contracts/execution.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[contracts/report.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[contracts/results.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[graph/__init__.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[graph/cycles.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[graph/projections.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[graph/traversal.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[graph/witnesses.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[io/__init__.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[io/input_file.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[io/output_directory.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[io/platform_linux.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[io/platform_windows.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[io/publication.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[reporting/__init__.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[reporting/assemble.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[reporting/escaping.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[reporting/json_report.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[reporting/markdown_report.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[runtime/__init__.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[runtime/boundary.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[runtime/diagnostics.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[runtime/disclosure.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[runtime/resources.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[validation/__init__.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[validation/limits.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[validation/references.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[validation/semantics.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_each_planned_module_imports[validation/structure.py]` | adapted | same |
| `tests/scaffold/test_imports.py::test_exact_package_file_set_and_inert_slots` | adapted | same |
| `tests/scaffold/test_imports.py::test_fresh_imports_have_no_application_io_or_native_activity` | adapted | same |
| `tests/scaffold/test_layer_boundaries.py::LayerBoundaryTests::test_accepted_imports_have_no_layer_errors` | adapted | same |
| `tests/scaffold/test_layer_boundaries.py::LayerBoundaryTests::test_allowed_architecture_direction_does_not_authorize_behavior` | adapted | same |
| `tests/scaffold/test_layer_boundaries.py::LayerBoundaryTests::test_cross_project_native_network_and_oracle_imports_fail` | adapted | same |
| `tests/scaffold/test_layer_boundaries.py::LayerBoundaryTests::test_import_cycle_detection_has_positive_and_negative_controls` | adapted | same |
| `tests/scaffold/test_layer_boundaries.py::LayerBoundaryTests::test_lower_layers_cannot_import_runtime_authority` | adapted | same |
| `tests/scaffold/test_layer_boundaries.py::LayerBoundaryTests::test_relative_escape_and_wildcard_fail` | adapted | same |
| `tests/scaffold/test_layer_boundaries.py::LayerBoundaryTests::test_reporting_cannot_recompute_analysis` | adapted | same |
| `tests/scaffold/test_module_manifest.py::ModuleManifestTests::test_all_trace_owners_have_a_recorded_home` | adapted | same |
| `tests/scaffold/test_module_manifest.py::ModuleManifestTests::test_exact_paths_owners_forms_and_accepted_bytes` | adapted | same |
| `tests/scaffold/test_module_manifest.py::ModuleManifestTests::test_layer_permissions_keep_their_qualifications` | adapted | same |
| `tests/scaffold/test_module_manifest.py::ModuleManifestTests::test_mutated_product_bytes_are_rejected` | adapted | same |
| `tests/scaffold/test_module_manifest.py::ModuleManifestTests::test_mutations_cannot_hide_missing_or_operational_slots` | adapted | same |
| `tests/scaffold/test_module_manifest.py::ModuleManifestTests::test_presentation_and_governance_keep_their_distinct_homes` | adapted | same |
| `tests/scaffold/test_module_manifest.py::ModuleManifestTests::test_product_has_no_catalog_dependency` | adapted | same |
| `tests/scaffold/test_module_manifest.py::ModuleManifestTests::test_shared_source_identities_agree` | adapted | same |
| `tests/scaffold/test_no_runtime_implementation.py::NoRuntimeImplementationTests::test_argument_inspection_before_refusal_fails_ast_and_tree` | adapted | same |
| `tests/scaffold/test_no_runtime_implementation.py::NoRuntimeImplementationTests::test_cached_directory_cannot_hide_python_source` | adapted | same |
| `tests/scaffold/test_no_runtime_implementation.py::NoRuntimeImplementationTests::test_changed_literal_or_fake_report_is_rejected` | adapted | same |
| `tests/scaffold/test_no_runtime_implementation.py::NoRuntimeImplementationTests::test_decorator_default_and_annotation_side_effects_fail` | adapted | same |
| `tests/scaffold/test_no_runtime_implementation.py::NoRuntimeImplementationTests::test_exact_package_path_set_is_independent` | adapted | same |
| `tests/scaffold/test_no_runtime_implementation.py::NoRuntimeImplementationTests::test_executable_body_is_detected_without_hash_check` | adapted | same |
| `tests/scaffold/test_no_runtime_implementation.py::NoRuntimeImplementationTests::test_extra_module_and_data_each_fail` | adapted | same |
| `tests/scaffold/test_no_runtime_implementation.py::NoRuntimeImplementationTests::test_extra_source_package_cannot_escape_inventory` | adapted | same |
| `tests/scaffold/test_no_runtime_implementation.py::NoRuntimeImplementationTests::test_missing_slot_fails` | adapted | same |
| `tests/scaffold/test_no_runtime_implementation.py::NoRuntimeImplementationTests::test_real_accepted_package_passes_all_guards` | adapted | same |
| `tests/scaffold/test_no_runtime_implementation.py::NoRuntimeImplementationTests::test_real_guard_cli_is_not_removed_by_python_optimization` | adapted | same |
| `tests/scaffold/test_no_runtime_implementation.py::NoRuntimeImplementationTests::test_syntax_error_and_oversize_do_not_crash_guard` | adapted | same |
| `tests/scaffold/test_packaging.py::test_declared_toolchain_is_actually_available` | retained | same |
| `tests/scaffold/test_packaging.py::test_generated_setup_cfg_exact_platform_bytes[nt-[egg_info]\r\ntag_build = \r\ntag_date = 0\r\n\r\n]` | retained | same |
| `tests/scaffold/test_packaging.py::test_generated_setup_cfg_exact_platform_bytes[posix-[egg_info]\ntag_build = \ntag_date = 0\n\n]` | retained | same |
| `tests/scaffold/test_packaging.py::test_generated_setup_cfg_rejects_extra_or_malformed_content[nt-\r\n]` | retained | same |
| `tests/scaffold/test_packaging.py::test_generated_setup_cfg_rejects_extra_or_malformed_content[posix-\n]` | retained | same |
| `tests/scaffold/test_packaging.py::test_generated_setup_cfg_rejects_unreviewed_platform` | retained | same |
| `tests/scaffold/test_packaging.py::test_project_metadata_and_runtime_dependency_boundary` | retained | same |
| `tests/scaffold/test_packaging.py::test_source_distribution_inventory` | retained | same |
| `tests/scaffold/test_packaging.py::test_source_distribution_rebuilds_same_package` | retained | same |
| `tests/scaffold/test_packaging.py::test_wheel_installs_without_developer_tools` | retained | same |
| `tests/scaffold/test_packaging.py::test_wheel_inventory_and_metadata` | retained | same |
| `tests/security/test_scaffold_inertness.py::ScaffoldInertnessTests::test_cache_helper_preloads_in_clean_interpreter` | retained | same |
| `tests/security/test_scaffold_inertness.py::ScaffoldInertnessTests::test_deliberate_evidence_read_is_detected_before_access` | retained | same |
| `tests/security/test_scaffold_inertness.py::ScaffoldInertnessTests::test_deliberate_path_inspection_is_detected` | retained | same |
| `tests/security/test_scaffold_inertness.py::ScaffoldInertnessTests::test_deliberate_write_is_detected_before_modification` | retained | same |
| `tests/security/test_scaffold_inertness.py::ScaffoldInertnessTests::test_imports_api_and_cli_are_inert` | retained | same |
| `tests/security/test_scaffold_inertness.py::ScaffoldInertnessTests::test_stub_that_inspects_argument_is_detected` | retained | same |
| `tests/security/test_scaffold_inertness.py::ScaffoldInertnessTests::test_swallowed_effect_violation_cannot_become_pass` | retained | same |
| `tests/security/test_scaffold_no_native_loading.py::ScaffoldNativeTests::test_all_slots_load_without_application_native_binding` | retained | same |
| `tests/security/test_scaffold_no_native_loading.py::ScaffoldNativeTests::test_deliberate_cdll_is_blocked_before_loading` | retained | same |
| `tests/security/test_scaffold_no_native_loading.py::ScaffoldNativeTests::test_deliberate_platform_loader_cannot_hide_in_other_slot` | retained | same |
| `tests/security/test_scaffold_no_network.py::ScaffoldNetworkTests::test_deliberate_dns_is_detected_without_resolution` | retained | same |
| `tests/security/test_scaffold_no_network.py::ScaffoldNetworkTests::test_deliberate_socket_creation_is_detected` | retained | same |
| `tests/security/test_scaffold_no_network.py::ScaffoldNetworkTests::test_real_scaffold_makes_no_application_network_attempt` | retained | same |

## Historical assertion loader

The six adapted test modules load their original source from the fixed intake Git commit, verify complete SHA-256 against the independently pinned entry manifest, and then replace only the named stage-sensitive assertions or driver functions. They retain the original collected test identities and assertions. This developer-only loader is in tools/check_scaffold_boundary.py; it accepts only those six fixed paths, does no network access, and has no mutable-ref or missing-history fallback. All original source remains inspectable in Git.

Full Git history is therefore an explicit test prerequisite. CI uses the same pinned checkout action with fetch-depth 0 and persist-credentials false. Source/wheel build and installed-runtime behavior do not load historical tests. The four historical test files included in the sdist remain repository-context developer tests, not standalone tests promised for an unpacked source archive. All 48 installed product slots are independent of this machinery.

No product object, source locator, input dossier, extension or user report can reach the historical loader. The fixed historical test sources are reviewed project code, not evidence being audited. The raw historical tests' original __main__ dispatcher is suppressed while loading; the current driver dispatches after the bounded adaptation.


## P2-W05-R01 authorized capture-test transition

Owner instruction: `批准 P2-W05-R01`. Accepted W04 merge is
`a1f102d82b7321f47df98f2672b91491cbd7fc9f`; W05 intake record is
`fb698272165303660092f02974a99ebbb2748a4c`.

This append preserves every historical row and result above. The migration is
an intermediate local candidate. Remote delivery, whole W05 implementation and
cumulative four-profile verification are still pending; it does not certify W05.

| Existing file / seam | Exact migration | Preserved obligations |
|---|---|---|
| tests/unit/test_input_decoding.py | Import `_capture_utf8` / `_capture_value` under the original local test aliases | All test names, parameter identities, payloads, byte/numeric oracles and failure classifications |
| tests/unit/test_value_capture.py | Import the two capture-only seams under original aliases | Exact types, hostile methods, ancestry cycles, alias occurrence counting, immutable copies, quotas and mutation faults |
| tests/security/test_input_capture.py | Retarget imports in the module and its isolated subprocess; extend only its named scope-accounting test for the five-path authorization | Audit-hook body, real negative-control events, safe diagnostic canaries, all test identities and constant-only R01 protection checks |
| tests/scaffold/test_ci_contract.py | Add the exact five P2-W05-R01 paths for W05 immediate scope and later cumulative accounting | All earlier scopes, guards, collection, workflow and failure rules |
| tests/contract/test_bundle_contract.py | Update its two named immediate/cumulative scope tests | All test identities and every other body; no additive W05 tests in this intermediate patch |

`runtime/boundary.py` adds only `_capture_value` and `_capture_utf8`, delegating
to the accepted `_capture` without options or public exports. Its existing
`_prepare_value` and `_prepare_utf8` are deliberately unchanged in this
intermediate migration. They still have W04-only behavior and must acquire the
full W05 pipeline before the work unit can pass. No test-only bypass or
successful full-dossier claim is introduced.

The later full-preparation cases belong to the already authorized W05 contract,
reference, temporal and hero integration test files. They must distinguish a
capturable empty/generic object from an admissible canonical dossier, require
all structural/identity/reference/type/time/index/scope work before acceptance,
and exercise all four unchanged H7 inputs. None of those future tests is marked
executed here. The 724 predecessor identities remain the required cumulative
baseline; local patch checks cannot replace their hosted execution.

## P2-W05-R02 and full preparation integration

The owner approved P2-W05-R02 and reiterated continuation of the already approved
W05. The verified R01 migration is now remotely present at
655f99e35052d56790f28d0c7971515c92b9ea6d, with run 35436261547 retaining all 724
predecessor test identities. The earlier local/pending wording above records its
historical preparation, not the current transport state.

R02 adds exactly tests/contract/test_input_schema_mapping.py to W05 immediate
scope. Its original test identity and source/schema/50-shape/242-field/30-rule
assertions remain intact. Only the unconditional pending/empty status assertion
is replaced by a strict check for the implemented private admission component,
PC01 alone completed, and PC02-PC24 still pending. New mutation tests reject both
stale pending metadata and inflated full-audit/analytical claims. A real sparse
input, capturable empty input and dangling-reference input witness the distinction
through the actual preparation functions. A pinned Git/AST regression protects
all other original assertions. The original historical test name stays unchanged.

The CI driver retains the old W02, W04 and W05-R01 exceptions and adds only the
one R02 path. Two named scope-accounting bodies in test_bundle_contract.py and
one in test_input_capture.py recognize that exact delta. Neither file loses a
test identity. The original capture observer and real negative controls, along
with the constant-only W04 diagnostic-repair checks, remain unchanged.

_capture_value and _capture_utf8 continue to run pure capture conformance.
_prepare_value and _prepare_utf8 now execute the complete W05 admission sequence
under one fixed budget: capture, closed-shape mapping, identity/reference/endpoint
and claim checks, time syntax, immutable normalization/indexing and finite
explicit inquiry/anchor planning. Only its final boundary records acceptance.
No component test is substituted for those full-preparation tests.

New W05 cases reside in test_typed_records.py, test_assertion_contract.py,
test_temporal_contract.py, test_reference_validation.py and
test_prepared_hero_inputs.py. They exercise every kind/predicate/assessment, exact
field presence and concrete type, valid sparse/protected/disputed/cyclic input,
late defects, source-native states, both input modes for every unchanged H7 case,
resource/cancellation/failure boundaries and real I/O/network/native controls.

All 724 predecessor identities remain required in the cumulative hosted suite.
Local component execution is separately recorded in PHASE_2_PROGRESS.md; it does
not replace full repository history, frozen-file, packaging or four-profile CI.
Acceptance and all new CI outcomes are recorded against the actual reviewed
commit in PR #14. W06, public auditing and analytical Trace closure remain absent.

## P2-W07-R01: authorized phase-context and permission transition

Owner instruction: `批准 P2-W07-R01 继续`. This approval implements the six-path
repair proposed in PR #16 at 067802f8df5b6958adde60bc7ced3ca8a06a7f33.
The accepted product remains W06 merge 4f55252d98f9b57975c2bc241c9079ac259a53cd.
The earlier W07 preflight failures, runs 35488938338 and 35489414729, remain
failures before test collection. Their evidence is not reused as a passing test.

Only active_unit changes from P2-W06 to P2-W07 in module_policy.json. The thirteen
promotions, earliest units, format and plan digest remain exact. Trusted review
context is still resolved independently. The CI driver adds exactly six W07-only
paths and retains them in cumulative accounting; it grants no other unit a new
immediate permission. The frozen plan and the module checker remain unchanged.

| File | Existing test entry point | Exact addition and retained requirement |
|---|---|---|
| tests/contract/test_bundle_contract.py | test_repair_does_not_expand_another_units_immediate_diff | Add W07's separate permission only at step 7; preserve every original assertion. |
| tests/contract/test_bundle_contract.py | test_repair_cumulative_accounting_retains_only_authorized_extras | Retain the six paths only from step 7 onward in cumulative history. |
| tests/security/test_input_capture.py | test_r01_exact_four_paths_and_no_other_unit_permission_expansion | Recognize W07 immediate/cumulative permissions; capture probes and effects assertions remain byte-identical. |
| tests/contract/test_input_schema_mapping.py | test_r02_exact_extra_path_and_other_units_keep_their_immediate_scope | Recognize step 7 only; schema, field, runtime-state and historical AST checks remain byte-identical. |

No original test identity or expected product outcome changes. Added tests in
W07R01Tests, within tests/contract/test_phase2_transition.py, verify exact old/new
bytes from the pinned pre-repair commit, one-field policy change, rejection of
mismatched trusted context and forbidden promotions, exact six-path scope,
unlisted-path denial, append-only history and unchanged product/checker bytes.

This append records authorization and intended assertions, not execution success.
Actual collection, failures and four-profile results are recorded on the exact
reviewed commit in PR #16 and phase2/implementation_evidence.json. All 1465 W06
test identities remain required. W07 acceptance, merge, W08 and release remain
separate gates; public auditing and analytical qualification remain unavailable.

## P2-W08-R01: authorized exact-head transition and installed-runtime check

Owner instruction: `批准 P2-W08-R01 继续已授权的 W08 工作`.
The authorized intake is a6847f90a32a4d478146f392acf83f49c84002c2, after accepted
W07 merge 22bd51454e425cf9eca87adbebecb09191fb925d. Historical entries above
remain byte-identical. R01 adds exactly seven immediate W08 paths; its scope
does not authorize W09. The module policy changes only active_unit to P2-W08.

| Existing file / entry point | Bounded migration |
|---|---|
| test_bundle_contract.py / test_repair_does_not_expand_another_units_immediate_diff | Recognize the distinct W08 exception only at step 8. |
| test_bundle_contract.py / test_repair_cumulative_accounting_retains_only_authorized_extras | Retain this exception from step 8 only in cumulative accounting. |
| test_input_capture.py / test_r01_exact_four_paths_and_no_other_unit_permission_expansion | Recognize the same immediate/cumulative delta, preserving all capture observers. |
| test_input_schema_mapping.py / test_r02_exact_extra_path_and_other_units_keep_their_immediate_scope | Recognize step 8 only, preserving every source/schema/runtime assertion. |
| W07R01Tests.test_exact_six_paths_are_w07_only_and_history_is_cumulative | Keep W07's six paths exact; add W08's separate authorization to the cross-unit comparison. |
| W07R01Tests.test_only_four_named_permission_test_bodies_change | Validate live W08 bytes against a pinned exact delta before checking the historical W07 transformation. |
| W07R01Tests.test_ci_context_collection_and_failure_controls_are_unchanged | Apply the same live-first exact validation to the CI driver; retain all context checks. |
| W07R01Tests.test_prior_phase2_transition_tests_keep_every_statement | Remove only the two explicitly added regression classes before comparing original W01 statements. |
| test_preparation_inertness.py / test_whole_package_guard_rejects_forbidden_implementation_in_temporary_copy | Resolve trusted developer context once and use it at four guard calls. All four target parameters, positive controls, mutations and rejection assertions remain. |

The CI driver already belongs to W08's original path list. Its only changes are
seven explicit repair paths, step-8 accounting and the repair evidence label.
The checker, workflow, pins, original collection/failure logic, product modules,
input schema, fixtures and oracles are unchanged. Eleven added W08R01Tests
methods protect exact source deltas, original statements, scope and installed
runtime independence. Their count and outcomes still require actual collection.

The installed-runtime witness uses the existing pinned packaging helpers to
build, inspect, install offline and rebuild outside the checkout. It verifies
all 48 installed module bytes, eight H7 preparation instances, empty-input
rejection, unchanged public refusals and real file/DNS/native negative controls.
It exports only a fixed JSON verification record, never source inputs or package
binaries. This is an additional engineering witness, not analytical closure.

Execution and final acceptance are recorded in the exact-head W08 review PR.
No test is removed, renamed or skipped; all 1629 predecessor identities remain
required. The 428 historical subtest events remain a separate count. Earlier
failed runs remain failures. W09, public auditing and releases remain separate
authorization gates.
