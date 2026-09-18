# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Finite H7 transcription checks only; no source-integrity analysis is implemented.

Authority: PHASE_1_PLAN.md section 8. JSON loading reads only fixed test assets.
No traversal, qualification, scoring, report rendering or native I/O is provided.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
CASES = ('H7-01', 'H7-V01', 'H7-V02', 'H7-V03')
SEEDS = ['H7-E' + letter for letter in 'ABCDEF']
ARTIFACTS = ['H7-' + letter for letter in 'ABCDEF']
TARGETS = ['H7-R1-V1', 'H7-A', 'H7-D', 'H7-E']
LINEAGE = 'CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md'
VALIDATION = 'VALIDATION_PLAN.md'
REPORTING = 'OBSERVABILITY_AND_REPORTING.md'
SOURCE_HASHES = {
    'DEFINITIONS_AND_UNITS.md': '913697e733d4430a64696b36a7893fe2113da7e2cfbcadbb54247a36c1792e9d',
    LINEAGE: '32272903b45a8749115ed6b4ec9904dd864a2190f9e1a2ba43ced4c8256c0374',
    VALIDATION: 'f958a12bda396cd12bfec096353ec17ec786e8c7fe30e07ee987f7d52874b707',
    REPORTING: '44daa3c86fc7d12e7be16a3aedfe10d16b99f55aa69141f90319ce2b5e63ff6a',
}


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate key in a fixed test asset')
        result[key] = value
    return result


def _load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'), object_pairs_hook=_pairs)


def _objects(bundle, collection):
    result = {}
    for obj in bundle[collection]:
        if obj['id'] in result:
            raise AssertionError('Duplicate fixture identifier')
        result[obj['id']] = obj
    return result


def _check_direct_references(bundle):
    """Check finite declared references, without following any graph edge."""
    ids = []
    for name in ('inquiries', 'records', 'assertions', 'evidence_references'):
        ids.extend(item['id'] for item in bundle[name])
    if len(ids) != len(set(ids)):
        raise AssertionError('Duplicate identifier across fixture collections')
    valid = set(ids)
    stack = [bundle]
    while stack:
        value = stack.pop()
        if isinstance(value, dict):
            for name, item in value.items():
                if name.endswith('_ref') and item is not None:
                    if not isinstance(item, str) or item not in valid:
                        raise AssertionError('Unknown direct fixture reference')
                elif name.endswith(('_refs', '_ref_ids')):
                    if not isinstance(item, list) or len(item) != len(set(item)):
                        raise AssertionError('Nonunique fixture reference list')
                    if any(ref not in valid for ref in item):
                        raise AssertionError('Unknown member in fixture reference list')
                stack.append(item)
        elif isinstance(value, list):
            stack.extend(value)


def _check_v01(main, candidate):
    expected = deepcopy(main)
    expected['snapshot_id'] = 'H7-S-FIVE'
    expected['inquiries'][0]['seed_artifact_refs'] = ARTIFACTS[:5]
    expected['inquiries'][0]['seed_evidence_refs'] = SEEDS[:5]
    if candidate != expected:
        raise AssertionError('V01 changed more than its prescribed snapshot/seed lists')


def _check_unchanged(main, candidate, changed_assertions):
    """Compare old entries directly; no dependency discovery or inference."""
    for coll in ('records', 'assertions', 'evidence_references'):
        before, after = _objects(main, coll), _objects(candidate, coll)
        for ident, original in before.items():
            if coll == 'assertions' and ident in changed_assertions:
                continue
            if after.get(ident) != original:
                raise AssertionError('Unapproved change to an original fixture object')
    for key in ('contract_version', 'bundle_id', 'recorded_at', 'predecessor'):
        if candidate[key] != main[key]:
            raise AssertionError('Unapproved envelope change')
    for key, original in main['inquiries'][0].items():
        if key not in ('seed_artifact_refs', 'seed_evidence_refs', 'coverage_assertion_refs'):
            if candidate['inquiries'][0][key] != original:
                raise AssertionError('Unapproved inquiry change')


def _check_hhi(oracle, expected_value, reasons):
    field = oracle['selected_field_expectations']['SIT-M005.single_origin_contribution_hhi']
    if field['execution_state'] != 'completed':
        raise AssertionError('Logical expected operation must state its completion premise')
    if field['value'] != expected_value or field['required_reason_codes'] != reasons:
        raise AssertionError('HHI oracle changed')
    expected_state = 'unavailable' if expected_value is None else 'available'
    if field['result_state'] != expected_state:
        raise AssertionError('HHI availability changed')


class FixtureIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundles = {case: _load(f'tests/fixtures/hero/{case}.bundle.json') for case in CASES}
        cls.oracles = {case: _load(f'tests/golden/{case}.logical.json') for case in CASES}
        cls.lineage = (ROOT / LINEAGE).read_text(encoding='utf-8')
        cls.validation = (ROOT / VALIDATION).read_text(encoding='utf-8')
        cls.reporting = (ROOT / REPORTING).read_text(encoding='utf-8')

    def test_frozen_case_sources_match_full_bytes(self):
        for path, expected in SOURCE_HASHES.items():
            with self.subTest(path=path):
                self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), expected)

    def test_exact_asset_inventory_and_manifest_hashes(self):
        manifest = _load('tests/fixtures/hero/fixture_manifest.json')
        expected = {f'tests/fixtures/hero/{c}.bundle.json' for c in CASES}
        expected |= {f'tests/golden/{c}.logical.json' for c in CASES}
        self.assertEqual({row['path'] for row in manifest['files']}, expected)
        self.assertEqual(len(manifest['files']), 8)
        for entry in manifest['files']:
            data = (ROOT / entry['path']).read_bytes()
            self.assertEqual(len(data), entry['bytes'])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry['sha256'])
            self.assertTrue(data.endswith(b'\n'))
            self.assertNotIn(b'\r', data)
        self.assertEqual({p.name for p in (ROOT / 'tests/fixtures/hero').glob('*.bundle.json')}, {c+'.bundle.json' for c in CASES})

    def test_distinct_complete_snapshot_envelopes(self):
        expected = dict(zip(CASES, ('H7-S1', 'H7-S-FIVE', 'H7-S-UNKNOWN', 'H7-S-MULTI')))
        for case, bundle in self.bundles.items():
            self.assertEqual(set(bundle), {'contract_version','bundle_id','snapshot_id','recorded_at','predecessor','inquiries','records','assertions','evidence_references'})
            self.assertEqual(bundle['contract_version'], 'sit-bundle/0.1')
            self.assertEqual(bundle['bundle_id'], 'H7-BUNDLE')
            self.assertEqual(bundle['snapshot_id'], expected[case])
            self.assertIsNone(bundle['predecessor'])
            self.assertEqual(len(bundle['inquiries']), 1)

    def test_ids_and_direct_references(self):
        for case, bundle in self.bundles.items():
            with self.subTest(case=case):
                _check_direct_references(bundle)
                for coll in ('records', 'assertions', 'inquiries', 'evidence_references'):
                    for item in bundle[coll]:
                        self.assertRegex(item['id'], r'^[A-Za-z0-9][A-Za-z0-9._:-]*$')

    def test_main_record_and_assertion_inventory(self):
        main = self.bundles['H7-01']
        expected = {'claim':1,'actor':5,'model':3,'artifact':27,'evidence_item':7,'origin_event':2,
                    'evaluation':2,'correction_channel':1,'correction_event':5,'pipeline_record':24,'anomaly':1}
        self.assertEqual({kind: sum(r['kind']==kind for r in main['records']) for kind in expected}, expected)
        self.assertEqual(len(main['records']),78)
        self.assertEqual(len(main['assertions']),50)
        self.assertEqual(len(main['evidence_references']),8)
        self.assertEqual({a['data']['assessment_kind'] for a in main['assertions'] if a['assertion_kind']=='assessment'}, {'coverage','origin_boundary','independence','externality','authority'})

    def test_expanded_fixture_field_sets_are_closed(self):
        # Exact prescribed H7 shapes, not a general executable dossier schema.
        fields = {
            'claim': {'claim_key','version_label','text','context'},
            'artifact': {'artifact_kind','work_key','version_label','locators','published_at','retrieved_at','content_evidence_refs'},
            'actor': {'actor_kind','identity_disclosure','display_name'},
            'model': {'model_key','version_label','family_label','provider_ref'},
            'evidence_item': {'claim_ref','artifact_ref','locator','epistemic_type','description'},
            'origin_event': {'event_kind','event_key','performed_by_refs','method_ref','occurred_at','description'},
            'evaluation': {'evaluation_kind','target_refs','role_bindings','result_refs','occurred_at','review_contribution'},
            'correction_channel': {'owner_refs','target_refs','contact_locator','declared_action_types','valid_window'},
            'correction_event': {'event_kind','case_ref','channel_ref','target_refs','occurred_at','details'},
            'pipeline_record': {'subject_ref','run_key','stage_key','stage','state','output_refs','observed_at','linkage_kind','detail'},
            'anomaly': {'inquiry_refs','claim_ref','original_context','context_evidence_ref','classification_state','caller_label','comparison_note'},
            'unresolved_reference': {'expected_kinds','reason','description'},
        }
        for case,bundle in self.bundles.items():
            for rec in bundle['records']:
                with self.subTest(case=case,record=rec['id']):
                    self.assertEqual(set(rec['data']), fields[rec['kind']])
                    self.assertTrue(any('Fictional' in q for q in rec['provenance']['qualifications']))
                    self.assertEqual(rec['label'], rec['id'])

    def test_original_support_excerpts_exactly_match_source(self):
        source = {}
        for line in self.lineage.splitlines():
            m = re.match(r'^\| `(CHAIN|ACQ|COMPARE|MODEL|PIPE|GRANT|CORR|CONTEXT)` \| “(.*?)” (.*?) \|$', line)
            if m:
                name, text, use = m.groups(); source['H7-SUP-'+name] = (text,use)
        self.assertEqual(len(source),8)
        for bundle in self.bundles.values():
            references = _objects(bundle,'evidence_references')
            for ident,(text,use) in source.items():
                self.assertEqual(references[ident]['excerpt'], text)
                self.assertEqual(references[ident]['scope_note'], use)
                self.assertEqual(references[ident]['reference_kind'], 'supplied_excerpt')
                self.assertEqual(references[ident]['availability'], 'supplied')

    def test_seven_acquisition_rows_match_authoritative_table(self):
        source = {}
        for line in self.lineage.splitlines():
            m=re.match(r'^\| `(H7-L0[1-7])` \| (\w+) \| (H7-[A-Z0-9-]+) \| (H7-[A-Z0-9-]+) \|$',line)
            if m: source[m[1]]=(m[2],m[3],m[4])
        self.assertEqual(len(source),7)
        for bundle in self.bundles.values():
            assertions = _objects(bundle,'assertions')
            for ident, expected in source.items():
                a=assertions[ident];d=a['data']
                self.assertEqual((d['predicate'],d['from_ref'],d['to_ref']),expected)
                self.assertEqual(d['dimension'],'acquisition')
                self.assertEqual(d['polarity'],'affirmed')
                self.assertEqual(a['scope']['claim_refs'],['H7-C1'])
                self.assertEqual(a['provenance']['evidence_ref_ids'],['H7-SUP-CHAIN'])

    def test_no_metadata_edge_becomes_acquisition(self):
        for bundle in self.bundles.values():
            for a in bundle['assertions']:
                if a['assertion_kind'] != 'relation': continue
                d=a['data']
                if a['id'].startswith(('H7-MAT-', 'H7-CITE-', 'H7-PUB-', 'H7-GEN-', 'H7-REV-')):
                    self.assertIsNone(d['dimension'])
                if a['id'].startswith(('H7-ML', 'H7-GEN-')):
                    self.assertEqual(a['scope']['claim_refs'],[])
                if a['id'].startswith('H7-PUB-'):
                    self.assertEqual(a['provenance']['basis_kind'],'declaration')

    def test_seed_sets_and_independent_populations(self):
        for case,bundle in self.bundles.items():
            i=bundle['inquiries'][0];o=self.oracles[case]
            expected=SEEDS[:5] if case=='H7-V01' else SEEDS+(['H7-EU'] if case=='H7-V02' else ['H7-EG'] if case=='H7-V03' else [])
            self.assertEqual(i['seed_evidence_refs'],expected)
            self.assertEqual(i['seed_evidence_refs'],o['populations']['source_contributions'])
            self.assertEqual(i['seed_artifact_refs'],o['populations']['source_artifacts'])
            self.assertEqual(o['populations']['pipeline_cohort'],SEEDS)
            self.assertEqual(o['populations']['correction_targets'],TARGETS)
            self.assertEqual(o['populations']['comparison_members'],['H7-O1','H7-O2'])

    def test_v01_is_only_seed_selection(self):
        _check_v01(self.bundles['H7-01'],self.bundles['H7-V01'])

    def test_v02_precise_delta_and_old_coverage(self):
        main, v=self.bundles['H7-01'],self.bundles['H7-V02']
        _check_unchanged(main,v,{'H7-COV-ACQ','H7-OB1','H7-OB2'})
        self.assertEqual(set(_objects(v,'records'))-set(_objects(main,'records')),{'H7-U','H7-EU','H7-UX','H7-DOC-V02'})
        self.assertEqual(set(_objects(v,'assertions'))-set(_objects(main,'assertions')),{'H7-LU','H7-COV-ACQ-OLD'})
        a=_objects(v,'assertions');r=_objects(v,'records');before=_objects(main,'assertions')['H7-COV-ACQ']
        self.assertEqual(r['H7-UX']['data']['expected_kinds'],['evidence_item'])
        self.assertEqual(r['H7-UX']['data']['reason'],'not_recorded')
        self.assertIn('H7-C1',r['H7-UX']['data']['description'])
        self.assertEqual(a['H7-LU']['data']['to_ref'],'H7-UX')
        self.assertEqual(a['H7-COV-ACQ']['data']['details']['state'],'partial')
        old=a['H7-COV-ACQ-OLD']
        for key,value in before['data']['details'].items():
            if key!='scope_note': self.assertEqual(old['data']['details'][key],value)
        self.assertEqual(old['provenance'],before['provenance'])
        for name in ('H7-OB1','H7-OB2'):
            expected=deepcopy(_objects(main,'assertions')[name]);expected['data']['details']['coverage_ref']='H7-COV-ACQ-OLD'
            self.assertEqual(a[name],expected)
        self.assertEqual(a['H7-COV-ACQ']['data']['details']['member_refs'],before['data']['details']['member_refs']+['H7-EU','H7-UX'])

    def test_v03_precise_delta_without_weights(self):
        main,v=self.bundles['H7-01'],self.bundles['H7-V03']
        _check_unchanged(main,v,{'H7-COV-ACQ'})
        self.assertEqual(set(_objects(v,'records'))-set(_objects(main,'records')),{'H7-G','H7-EG','H7-DOC-V03'})
        self.assertEqual(set(_objects(v,'assertions'))-set(_objects(main,'assertions')),{'H7-LG1','H7-LG2'})
        a=_objects(v,'assertions')
        self.assertEqual([a[name]['data']['to_ref'] for name in ('H7-LG1','H7-LG2')],['H7-EA','H7-EF'])
        for name in ('H7-LG1','H7-LG2'):
            self.assertEqual(a[name]['data']['from_ref'],'H7-EG')
            self.assertEqual(a[name]['data']['dimension'],'acquisition')
            self.assertEqual(set(a[name]['data']['details']),{'portion_note'})
        self.assertEqual(a['H7-COV-ACQ']['data']['details']['state'],'complete_for_scope')
        self.assertEqual(a['H7-COV-ACQ']['data']['details']['member_refs'],_objects(main,'assertions')['H7-COV-ACQ']['data']['details']['member_refs']+['H7-EG'])

    def test_pipeline_matrix_unchanged_with_unknown_use(self):
        expected={'PA':['occurred']*6,'PP':['occurred']*6,'PS':['occurred']*5+['did_not_occur'],
                  'PU':['occurred','occurred','did_not_occur','occurred','unknown','did_not_occur']}
        for bundle in self.bundles.values():
            r=_objects(bundle,'records');a=_objects(bundle,'assertions')
            for prefix,states in expected.items():
                self.assertEqual([r['H7-'+prefix+'-'+x]['data']['state'] for x in 'ABCDEF'],states)
            self.assertEqual(r['H7-PU-E']['data']['linkage_kind'],'unspecified')
            self.assertEqual(r['H7-PU-E']['data']['output_refs'],[])
            for suffix in ('ADM','PRES','SEL','USE'):
                self.assertEqual(a['H7-COV-'+suffix]['data']['details']['member_refs'],SEEDS)

    def test_correction_submission_handling_and_changes(self):
        for bundle in self.bundles.values():
            r=_objects(bundle,'records')
            events={i:x for i,x in r.items() if x['kind']=='correction_event'}
            self.assertEqual(set(events),{'H7-CASE1','H7-HAND1','H7-CHANGE-R1','H7-CHANGE-A','H7-CHANGE-D'})
            self.assertEqual(r['H7-CASE1']['data']['target_refs'],TARGETS)
            self.assertEqual(r['H7-HAND1']['data']['details']['outcome'],'accepted')
            for suffix,old,new in [('R1','H7-R1-V1','H7-R1-V2'),('A','H7-A','H7-A-V2'),('D','H7-D','H7-D-V2')]:
                event=r['H7-CHANGE-'+suffix]['data']
                self.assertEqual(event['case_ref'],'H7-CASE1')
                self.assertEqual((event['details']['before_ref'],event['details']['after_ref']),(old,new))
                self.assertIsNone(event['details']['after_absence_reason'])
            self.assertIsNone(r['H7-CHANNEL']['data']['contact_locator'])
            self.assertEqual(r['H7-CHANNEL']['gaps'][0]['reason'],'withheld')

    def test_native_roles_anomaly_and_unknown_metadata(self):
        for bundle in self.bundles.values():
            r=_objects(bundle,'records')
            self.assertEqual(r['H7-EF']['data']['epistemic_type'],'measurement')
            self.assertEqual(r['H7-ED']['data']['epistemic_type'],'analytical_inference')
            self.assertEqual(r['H7-O1']['data']['event_key'],r['H7-O2']['data']['event_key'])
            self.assertNotEqual(r['H7-O1']['data']['performed_by_refs'],r['H7-O2']['data']['performed_by_refs'])
            self.assertEqual(r['H7-AN1']['data']['classification_state'],'unclassified')
            self.assertIsNone(r['H7-AN1']['data']['claim_ref'])
            self.assertIsNone(r['H7-EVAL']['data']['review_contribution'])
            self.assertTrue(r['H7-HREVIEW']['data']['review_contribution'])
            for item in r.values():
                if item['kind']=='artifact':
                    for key in ('published_at','retrieved_at'):
                        self.assertEqual(item['data'][key]['state'],'unknown')
                        self.assertIsNone(item['data'][key]['value'])

    def test_logical_assets_do_not_claim_execution(self):
        for case,o in self.oracles.items():
            self.assertEqual(o['artifact_type'],'test_only_logical_oracle')
            self.assertEqual(o['status']['runtime_execution'],'not_performed')
            self.assertEqual(o['status']['domain_tests'],'pending')
            self.assertNotIn('report_id',o)
            self.assertNotIn('tool_version',o)
            self.assertNotIn('raw_file_digest',o)
            self.assertEqual(o['case_id'],case)
            self.assertEqual(o['scope']['snapshot_id'],self.bundles[case]['snapshot_id'])

    def test_hhi_oracles_preserve_source_fractions_and_blockers(self):
        _check_hhi(self.oracles['H7-01'],{'numerator':26,'denominator':36},[])
        _check_hhi(self.oracles['H7-V01'],{'numerator':25,'denominator':25},[])
        _check_hhi(self.oracles['H7-V02'],None,['unknown_endpoint','upstream_coverage_incomplete'])
        _check_hhi(self.oracles['H7-V03'],None,['multi_origin_unallocated'])
        self.assertIn('26/36',self.validation)
        self.assertIn('25/25',self.validation)
        self.assertIn('M005 is completed/unavailable, null, with unknown_endpoint and upstream_coverage_incomplete.',self.validation)
        self.assertIn('M005 is completed/unavailable with multi_origin_unallocated.',self.validation)

    def test_origin_and_immediate_partitions_are_static_oracles(self):
        expected={'H7-01':([0,0,0,0,6],[5,1,0,0]),'H7-V01':([0,0,0,0,5],[5,0,0,0]),
                  'H7-V02':([1,0,0,0,6],[5,1,0,1]),'H7-V03':([0,0,0,1,6],[6,1,0,0])}
        for case,(orig,imm) in expected.items():
            self.assertEqual(self.oracles[case]['origin_partition_counts'],orig)
            self.assertEqual(self.oracles[case]['immediate_partition_counts'],imm)
        multi=self.oracles['H7-V03']['origin_incidences']
        self.assertEqual([(row['count'],row['fraction']) for row in multi],[(6,{'numerator':6,'denominator':7}),(2,{'numerator':2,'denominator':7})])

    def test_completion_intervals_keep_units(self):
        for o in self.oracles.values():
            use=o['pipeline'][3]
            self.assertEqual(use['stage_occurrence_fraction']['result_state'],'unavailable')
            self.assertEqual(use['stage_occurrence_fraction']['required_reason_codes'],['stage_classification_unresolved'])
            self.assertEqual(use['stage_occurrence_completion_interval']['value'],{'interval_kind':'finite_cohort_completion','lower':{'numerator':3,'denominator':6},'upper':{'numerator':4,'denominator':6}})
            self.assertEqual([t['to_stage_key'] for t in o['eligible_transition_expectations']],['store-1','select-1'])
        self.assertEqual(self.oracles['H7-V02']['selected_field_expectations']['SIT-M006.inherited_only_completion_interval']['value'],{'interval_kind':'finite_record_completion','lower':{'numerator':5,'denominator':7},'upper':{'numerator':6,'denominator':7}})

    def test_qualified_comparison_and_human_independence_stay_separate(self):
        for case,o in self.oracles.items():
            for name in ('submitted_comparison_member_count','qualified_process_set_member_count','qualified_origin_set_member_count'):
                self.assertEqual(o['selected_field_expectations']['SIT-M003.'+name]['value'],2)
            self.assertEqual(o['human_review']['corrective_independence']['required_reason_codes'],['missing_comparison_assessment'])
            self.assertEqual(o['correction']['undocumented_target_effect']['expectation']['required_reason_codes'],['change_evidence_missing'])
            self.assertEqual(o['evaluator_pair']['shared_ancestor_refs'],['H7-MBASE','H7-TRAINING'])
            self.assertEqual(o['evaluator_pair']['matching_family_labels'],['H7-family'])

    def test_field_and_reason_names_exist_in_adopted_catalogs(self):
        leaf_section=self.reporting.split('## 17. Output leaf catalog',1)[1].split('\n## 18.',1)[0]
        names=set(re.findall(r'`([a-z][a-z0-9_]*)`',leaf_section))
        reason_section=self.reporting.split('### 13.2 Reason objects',1)[1].split('\n## 14.',1)[0]
        reasons=set(re.findall(r'`([a-z][a-z0-9_]*)`',reason_section))
        for o in self.oracles.values():
            for name,expected in o['selected_field_expectations'].items():
                self.assertIn(name.split('.',1)[1],names)
                self.assertTrue(set(expected['required_reason_codes'])<=reasons)

    def test_whole_source_sections_are_bound(self):
        for o in self.oracles.values():
            for ref in o['authoritative_sections']:
                data=(ROOT/ref['path']).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(),ref['source_sha256'])
                lines=data.decode('utf-8').splitlines(keepends=True)
                part=''.join(lines[ref['start_line']-1:ref['end_line']])
                self.assertEqual(part.splitlines()[0],ref['heading'])
                self.assertEqual(hashlib.sha256(part.encode()).hexdigest(),ref['section_sha256'])
        self.assertIn('## 1. Purpose and source discipline',[x['heading'] for x in self.oracles['H7-01']['authoritative_sections']])

    def test_micro_index_matches_all_source_sections(self):
        index=_load('tests/fixtures/micro/case_index.json')
        source=dict(re.findall(r'^### (W7-\d\d): (.+)$',self.validation,re.M))
        self.assertEqual({c['case_id']:c['title'] for c in index['cases']},source)
        self.assertEqual(len(index['cases']),28)
        for case in index['cases']:
            self.assertEqual(case['runtime_test_status'],'pending')
            ref=case['source']; lines=self.validation.splitlines(keepends=True)
            self.assertEqual(hashlib.sha256(''.join(lines[ref['start_line']-1:ref['end_line']]).encode()).hexdigest(),ref['section_sha256'])

    def test_control_index_preserves_adopted_w03_bindings(self):
        index=_load('tests/fixtures/adversarial/case_index.json')
        self.assertEqual(index['source_bound_index']['git_blob_sha1'],'62ec0c934aee408c5bd9e9e32d0c03bac3c806e4')
        ids=[c['case_id'] for c in index['cases']]
        expected=[f'W9-{n:02d}' for n in range(1,25)]+[f'W9-LIC{n:02d}' for n in range(1,7)]+[f'W11-R{n:02d}' for n in range(1,33)]
        self.assertEqual(ids,expected)
        for row in index['cases']:
            self.assertEqual(row['runtime_test_status'],'pending')
            self.assertEqual(row['materialization_status'],'indexed_only')
            if row['case_id'].startswith('W11-R'):
                n=int(row['case_id'][5:])
                expected_path=('tests/contract/test_normalization_profile.py' if n<=10 else 'tests/contract/test_realization_profile.py' if n<=17 or n>=31 else 'tests/security/test_resource_profile.py' if n<=22 else 'tests/security/test_filesystem_profiles.py')
                self.assertEqual(row['future_test_paths'],[expected_path])
            else: self.assertNotIn('future_test_paths',row)
        self.assertIn('GOVERNANCE_AND_HANDOFF.md section 22',index['binding_refinements'])

    def test_exact_disposition_vocabulary(self):
        definitions = (ROOT / 'DEFINITIONS_AND_UNITS.md').read_text(encoding='utf-8')
        expected_origin = ['unresolved_or_conflicted','contains_baseline_or_scope_cut','contains_declared_origin','multiple_documented_origins','single_documented_origin']
        expected_immediate = ['inherited_only_at_evidence_layer','direct_origin_link_only','mixed_direct_and_inherited','unresolved_at_evidence_layer']
        for name in expected_origin + expected_immediate:
            self.assertIn('`'+name+'`', definitions)
        for oracle in self.oracles.values():
            self.assertEqual(oracle['origin_partition_order'], expected_origin)
            self.assertEqual(oracle['immediate_partition_order'], expected_immediate)
            for row in oracle['origin_rows']:
                self.assertIn(row['origin_disposition'], expected_origin)
                self.assertIn(row['immediate_disposition'], expected_immediate)

    def test_finite_witnesses_are_transcribed_from_source_table(self):
        source = {}
        for line in self.validation.splitlines():
            if not re.match(r'^\| H7-E[A-F] \| ', line):
                continue
            cells = [x.strip() for x in line.strip('|').split('|')]
            if len(cells) == 5 and ', L0' in cells[1]:
                source[cells[0]] = ['H7-'+x.strip() for x in cells[1].split(',')]
        self.assertEqual(set(source), set(SEEDS))
        for oracle in self.oracles.values():
            for row in oracle['origin_rows']:
                if row['seed_ref'] in source:
                    self.assertEqual(row['finite_witness'], source[row['seed_ref']])

    def test_negative_probes_detect_transcription_damage(self):
        main=self.bundles['H7-01']
        bad=deepcopy(main);bad['records'].append(deepcopy(bad['records'][0]))
        with self.assertRaises(AssertionError):_check_direct_references(bad)
        bad=deepcopy(main);bad['records'][0]['provenance']['attributed_to_ref']='H7-MISSING'
        with self.assertRaises(AssertionError):_check_direct_references(bad)
        for ident,key,new in [('H7-PU-E','state','did_not_occur'),('H7-HAND1','details',{'outcome':'failed','reason':'changed'})]:
            bad=deepcopy(self.bundles['H7-V01']);_objects(bad,'records')[ident]['data'][key]=new
            with self.assertRaises(AssertionError):_check_v01(main,bad)
        bad=deepcopy(self.bundles['H7-V02']);_objects(bad,'assertions')['H7-COV-USE']['data']['details']['member_refs'].append('H7-EU')
        with self.assertRaises(AssertionError):_check_unchanged(main,bad,{'H7-COV-ACQ','H7-OB1','H7-OB2'})
        bad=deepcopy(self.oracles['H7-01']);bad['selected_field_expectations']['SIT-M005.single_origin_contribution_hhi']['value']={'numerator':13,'denominator':18}
        with self.assertRaises(AssertionError):_check_hhi(bad,{'numerator':26,'denominator':36},[])
        bad=deepcopy(self.oracles['H7-V02']);bad['selected_field_expectations']['SIT-M005.single_origin_contribution_hhi']['value']={'numerator':26,'denominator':36}
        with self.assertRaises(AssertionError):_check_hhi(bad,None,['unknown_endpoint','upstream_coverage_incomplete'])
        bad=deepcopy(self.oracles['H7-V03']);bad['selected_field_expectations']['SIT-M005.single_origin_contribution_hhi']['required_reason_codes']=[]
        with self.assertRaises(AssertionError):_check_hhi(bad,None,['multi_origin_unallocated'])

    def test_duplicate_json_keys_are_not_hidden(self):
        with self.assertRaises(ValueError):json.loads('{"fixture":1,"fixture":2}',object_pairs_hook=_pairs)


if __name__ == '__main__':
    unittest.main()
