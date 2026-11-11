# Graph Report - .  (2026-11-09)

## Corpus Check
- 118 files · ~107,352 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 369 nodes · 682 edges · 18 communities (17 shown, 1 thin omitted)
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 145 edges (avg confidence: 0.83)
- Token cost: 115,308 input · 11,200 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Quiz Matching Logic|Quiz Matching Logic]]
- [[_COMMUNITY_Wiki Maintenance Scripts|Wiki Maintenance Scripts]]
- [[_COMMUNITY_Wiki Memory Tests|Wiki Memory Tests]]
- [[_COMMUNITY_Questionnaire Screens and Decisions|Questionnaire Screens and Decisions]]
- [[_COMMUNITY_Quiz Research and Decisions|Quiz Research and Decisions]]
- [[_COMMUNITY_Local Quiz Frontend|Local Quiz Frontend]]
- [[_COMMUNITY_Wiki Curation and Search|Wiki Curation and Search]]
- [[_COMMUNITY_Local Quiz API Tests|Local Quiz API Tests]]
- [[_COMMUNITY_Wiki Bootstrap and Migration|Wiki Bootstrap and Migration]]
- [[_COMMUNITY_Quiz Scope and Requirements|Quiz Scope and Requirements]]
- [[_COMMUNITY_Catalog Builder and Tests|Catalog Builder and Tests]]
- [[_COMMUNITY_Production Quiz Backend|Production Quiz Backend]]
- [[_COMMUNITY_Sandbox Documentation|Sandbox Documentation]]
- [[_COMMUNITY_Content Index Validation|Content Index Validation]]
- [[_COMMUNITY_Content Taxonomy Design|Content Taxonomy Design]]
- [[_COMMUNITY_Wiki Session Memory Guidance|Wiki Session Memory Guidance]]
- [[_COMMUNITY_Prompt Installer|Prompt Installer]]
- [[_COMMUNITY_Wiki Rules and Templates|Wiki Rules and Templates]]

## God Nodes (most connected - your core abstractions)
1. `MemoryCliTests` - 35 edges
2. `run()` - 34 edges
3. `recommend()` - 29 edges
4. `MatcherTests` - 21 edges
5. `Quiz Product Set Generator` - 19 edges
6. `migrate()` - 14 edges
7. `byId()` - 13 edges
8. `save()` - 12 edges
9. `_tags()` - 12 edges
10. `ApiTests` - 12 edges

## Surprising Connections (you probably didn't know these)
- `Owner questionnaire: budget and selection limits` --semantically_similar_to--> `Buyer-Selected Budget Input`  [INFERRED] [semantically similar]
  .playwright-cli/page-2026-11-04T12-49-47-887Z.yml → raw/sources/2026-11-04-budget-is-buyer-input.md
- `Owner questionnaire: scenario and recommendation scope` --semantically_similar_to--> `Owner Requirements Questionnaire`  [INFERRED] [semantically similar]
  .playwright-cli/page-2026-11-04T12-47-21-032Z.yml → raw/sources/2026-11-04-quiz-owner-questionnaire-request.md
- `Athlete Product Selection Research Request` --semantically_similar_to--> `Quiz Matching Rules Technical Brief`  [INFERRED] [semantically similar]
  raw/sources/2026-11-09-athlete-product-selection-research-request.md → wiki/projects/quiz-matching-rules-technical-brief.md
- `V1 Ready Sets Only Scope and Portable Catalog` --semantically_similar_to--> `Quiz Product Set Generator`  [INFERRED] [semantically similar]
  raw/sources/2026-11-09-v1-ready-sets-only-scope-and-portable-catalog.md → wiki/projects/project-5-quiz-product-set-generator.md
- `Test-only Recommendation Heuristics` --semantically_similar_to--> `Owner Approval of Matching Rules`  [INFERRED] [semantically similar]
  wiki/projects/quiz-test-sandbox.md → spec.md

## Import Cycles
- 1-file cycle: `.agents/skills/llm-wiki-session-memory/scripts/wiki_memory.py -> .agents/skills/llm-wiki-session-memory/scripts/wiki_memory.py`

## Hyperedges (group relationships)
- **Owner questionnaire design and refinement** — sources_2026_11_04_quiz_owner_questionnaire_request_owner_questionnaire, sources_2026_11_04_questionnaire_addressed_to_single_client_single_client_audience, sources_2026_11_04_questionnaire_buyer_inputs_not_full_quiz_buyer_input_scope, sources_2026_11_04_questionnaire_feedback_result_type_gating_result_type_gating, sources_2026_11_04_questionnaire_rule_basis_and_coverage_matching_rule_basis, sources_2026_11_04_questionnaire_ukrainian_simple_list_simple_ukrainian_questionnaire, sources_2026_11_04_questionnaire_question_3_clarification_consultation_metric [INFERRED 0.85]
- **Catalog evidence, access, and matching requirements** — sources_2026_11_04_quiz_questionnaire_catalog_and_matching_catalog_matching_requirements, sources_2026_11_04_race_expert_public_catalog_review_public_catalog_review, sources_2026_11_04_quiz_logic_question_audit_on_site_catalog_constraint, sources_2026_11_06_206_set_follow_up_verifications_set_verification, sources_2026_11_06_approved_tags_for_206_sets_analysis_tagging_policy [INFERRED 0.75]
- **Quiz v1 work centered on the 206 ready need sets** — sources_2026_11_06_scope_206_needs_sets_need_sets_206_scope, sources_2026_11_09_quiz_matching_rules_spec_request_matching_rules_specification_request, sources_2026_11_09_standalone_test_quiz_request_standalone_test_quiz_request, sources_2026_11_09_v1_ready_sets_only_scope_and_portable_catalog_v1_ready_sets_only_scope, projects_project_5_quiz_product_set_generator_quiz_product_set_generator [INFERRED 0.85]
- **225-set Catalog Snapshot Composition** — projects_race_expert_set_catalog_2026_11_06_document, projects_race_expert_set_catalog_2026_11_06_need_based_sets, projects_race_expert_set_catalog_2026_11_06_distance_sets [EXTRACTED 1.00]
- **Content Quality and Review-first Curation** — specs_2026_07_23_card_taxonomy_quality_design, specs_2026_07_23_card_taxonomy_quality_design_controlled_vocabulary, specs_2026_07_23_card_taxonomy_quality_design_content_quality_audit, specs_2026_07_23_card_taxonomy_quality_design_review_first_curation [EXTRACTED 1.00]
- **Validated Session Save Workflow** — templates_commands_save_memory_command, templates_prompts_save_memory_prompt, references_session_schema_document, references_tagging_document [EXTRACTED 1.00]
- **Owner questionnaire wizard states from scenario through final submission** — playwright_cli_page_2026_11_04t12_47_21_032z_scenario_scope, playwright_cli_page_2026_11_04t12_49_47_887z_budget_and_selection_limits, playwright_cli_page_2026_11_04t12_50_38_808z_conditional_rules_overview, playwright_cli_page_2026_11_04t12_51_11_360z_conditional_branch_module, playwright_cli_page_2026_11_04t12_52_39_863z_conditional_rules_answers, playwright_cli_page_2026_11_04t12_53_12_413z_conditional_modules_answers, playwright_cli_page_2026_11_04t12_55_50_316z_review_before_send, playwright_cli_page_2026_11_04t12_57_20_346z_submission_complete, playwright_cli_page_2026_11_04t14_45_41_329z_ukrainian_scenario [INFERRED 0.85]
- **Test-only quiz sandbox plans, catalog, matching, restrictions, and interface** — test_quiz_sandbox_implementation_plan_architecture, test_quiz_sandbox_readme_local_quiz, test_quiz_sandbox_test_plan_matching_rules, tickets_test_01_catalog_snapshot_extraction, tickets_test_02_local_recommendation_flow, tickets_test_03_safe_filter_behavior, tickets_test_04_bilingual_local_api, web_index_bilingual_quiz_ui, wiki_log_quiz_project_history [INFERRED 0.85]

## Communities (18 total, 1 thin omitted)

### Community 0 - "Quiz Matching Logic"
Cohesion: 0.11
Nodes (20): _availability(), _caffeine_status(), _candidate_reasons(), _data_notes(), goal_group_for_purpose(), goal_group_options(), _has_unverified_audience(), MatchError (+12 more)

### Community 1 - "Wiki Maintenance Scripts"
Cohesion: 0.12
Nodes (34): Path, Path, Path, Path, apply(), main(), apply(), main() (+26 more)

### Community 3 - "Questionnaire Screens and Decisions"
Cohesion: 0.08
Nodes (32): Owner questionnaire: scenario and recommendation scope, Owner questionnaire: budget and selection limits, Owner questionnaire: conditional rules overview, Owner questionnaire: conditional branch module, Owner questionnaire: conditional rules answers, Owner questionnaire: conditional modules answers, Owner questionnaire: review before sending, Owner questionnaire: submission complete (+24 more)

### Community 4 - "Quiz Research and Decisions"
Cohesion: 0.11
Nodes (31): Quiz Product Set Generator, Athlete Product Selection Research, Quiz Matching Rules Technical Brief, Owner Discovery Questionnaire, Owner Discovery Questionnaire V2, Owner Discovery Questionnaire V3, Address Questionnaire to One Client, Connect Telegram and Test Questionnaire Delivery (+23 more)

### Community 5 - "Local Quiz Frontend"
Cohesion: 0.24
Nodes (22): appendOption(), applyCopy(), buildRequest(), byId(), copy, element(), fillSelect(), goToStep() (+14 more)

### Community 6 - "Wiki Curation and Search"
Cohesion: 0.13
Nodes (17): Path, Namespace, Namespace, Path, datetime, main(), proposal_for(), is_youtube() (+9 more)

### Community 7 - "Local Quiz API Tests"
Cohesion: 0.16
Nodes (10): create_server(), _load_catalog(), main(), make_handler(), _options(), Local-only HTTP API and static page for the test quiz., Create an HTTP server bound only to a loopback IP address., Create the request handler used by the server and handler-level tests. (+2 more)

### Community 8 - "Wiki Bootstrap and Migration"
Cohesion: 0.21
Nodes (17): Path, Path, bootstrap(), copy_if_missing(), main(), body_after_frontmatter(), candidates(), card_id() (+9 more)

### Community 9 - "Quiz Scope and Requirements"
Cohesion: 0.13
Nodes (18): Conditional Multi-step Intake Form, Owner Requirements Questionnaire, Dynamic Buyer Quiz Direction, Race Expert Product Quiz Intent, Catalog Builder, Локальный тестовый квиз по 206 наборам, Loopback-only HTTP Server, Recommendation Matcher (+10 more)

### Community 10 - "Catalog Builder and Tests"
Cohesion: 0.15
Nodes (10): build_catalog(), _extract_after_label(), main(), parse_analysis(), _parse_record(), Build a test-only JSON catalog from the maintained 206-set Wiki analysis., _record_start(), _tag_map() (+2 more)

### Community 11 - "Production Quiz Backend"
Cohesion: 0.22
Nodes (9): BaseHTTPRequestHandler, active_question_ids(), build_document(), config_value(), Handler, main(), read_dotenv(), send_document() (+1 more)

### Community 12 - "Sandbox Documentation"
Cohesion: 0.32
Nodes (13): Test-only quiz sandbox implementation plan, Local test quiz README, Test plan for sandbox matching rules, TEST-01: Extract the 206-set catalog snapshot, TEST-02: Match answers to 1–3 alternative sets, TEST-03: Keep filters source-backed, TEST-04: Bilingual local API and quiz page, Bilingual local quiz interface (+5 more)

### Community 13 - "Content Index Validation"
Cohesion: 0.30
Nodes (10): Path, Path, audit(), finding(), main(), render_markdown(), graph_errors(), lint() (+2 more)

### Community 14 - "Content Taxonomy Design"
Cohesion: 0.22
Nodes (11): Card Taxonomy Quality Implementation Plan, Knowledge-card Schema, Session Tagging Rules, Card Taxonomy and Quality Design, Content Quality Audit, Controlled Content Vocabulary, Review-first Metadata Curation, Session Memory AGENTS Snippet (+3 more)

### Community 15 - "Wiki Session Memory Guidance"
Cohesion: 0.25
Nodes (9): OpenAI Skill Descriptor, Project Save Memory Command, LLM Wiki Session Memory README, Karpathy LLM Wiki Pattern, LLM Wiki Session Memory Skill, Local Memory and Content Index Tools, Session Record Schema, Save Memory Command Template (+1 more)

### Community 16 - "Prompt Installer"
Cohesion: 0.67
Nodes (3): Path, install(), main()

### Community 17 - "Wiki Rules and Templates"
Cohesion: 0.67
Nodes (3): Project Wiki Operating Rules, LLM Wiki AGENTS Template, Wiki Log Template

## Knowledge Gaps
- **39 isolated node(s):** `Path`, `Path`, `Path`, `Path`, `Namespace` (+34 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `datetime` connect `Wiki Curation and Search` to `Wiki Bootstrap and Migration`, `Wiki Maintenance Scripts`, `Wiki Memory Tests`, `Production Quiz Backend`?**
  _High betweenness centrality (0.184) - this node is a cross-community bridge._
- **Why does `MatchError` connect `Quiz Matching Logic` to `Wiki Maintenance Scripts`?**
  _High betweenness centrality (0.100) - this node is a cross-community bridge._
- **Why does `parse_time()` connect `Wiki Maintenance Scripts` to `Wiki Curation and Search`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `recommend()` (e.g. with `.test_applies_full_set_price_ceiling_inclusively()` and `.test_consumer_goal_group_maps_to_catalog_purpose_tags()`) actually correct?**
  _`recommend()` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `ValueError` (e.g. with `apply()` and `apply()`) actually correct?**
  _`ValueError` has 18 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Path`, `Path`, `Path` to the rest of the system?**
  _57 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Quiz Matching Logic` be split into smaller, more focused modules?**
  _Cohesion score 0.11282051282051282 - nodes in this community are weakly interconnected._