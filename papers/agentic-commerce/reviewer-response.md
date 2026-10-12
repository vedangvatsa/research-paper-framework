# Reviewer assessment and response

Review date: October 13, 2026. This is a critical review by the same AI assistant that helped prepare the manuscript, not independent human peer review. The author requested a full reviewer pass after identifying vague wording and an unnecessary completion-date sentence.

## Assessment before revision

The paper has a useful distinction between permission to pay and a satisfactory purchase. Its sources cover consumer behavior, agent tests, protocols, markets, security, and law. The draft needs substantive revision because some comparisons omit relevant source qualifications or counterevidence, the search description is too loose, and repeated summaries obscure the main argument.

The working draft had already lost the completion-date sentence in its abstract, but its PDFs and hash-bound audit had not yet been rebuilt for that small deletion. The archive `../agentic-commerce-archive/before-reviewer-pass/` preserves this working state. The current revision will be checked as one complete manuscript.

## Findings and required changes

| ID | Finding | Required revision and evidence |
|---|---|---|
| R1 | The question and definition do not cleanly separate buying authority from the amount of work the agent performs. Advice is included without explaining its role as a comparison case. | State the question in terms of suitable purchases, buyer permission, and errors. Explain that unsupervised search can still end in per-order approval; Table 1 classifies purchase permission, not a single scale of autonomy. |
| R2 | The method sounds broader than the recorded search. The saved OpenAlex discovery requests cap results at eight per query; known-study lookups supply additional sources. There was no independent duplicate screening or formal cross-design bias score. | Describe this as a purposive, accessible-source narrative review. Disclose the query cap and AI-assisted, non-independent appraisal. Keep the search date as methodological scope, not an abstract completion announcement. Avoid claiming saturation or exhaustive coverage. |
| R3 | The abstract combines economic theory and hotel-field findings in a way that can suggest that cheaper search was itself tested as a cause of persistent ranking effects. | Attribute the price-versus-feature distinction to Bakos's model, and the ranking/click/booking finding to Ursu's field data. Do not combine these into a measured effect of AI search. |
| R4 | The forecasting comparison gives a plausible explanation for conflicting findings more causal force than this review can establish. | Compare feedback, advice labels, and choice tasks explicitly, without treating a cross-paper comparison as a matched test of why findings differ. Logg Sections 1.2-1.3 and experimental designs support the distinction. |
| R5 | Benchmark appraisal is incomplete. EComAgentBench's target/rubric metrics can favor different models, and the draft mentions its AI judge without the authors' checks. WebShop's small full-success difference must not become a general claim about reward training. | Add the metric-dependent ordering from EComAgentBench Table 3, its exact-match and manual-judge checks in Sections 5-6, and the absence of headline uncertainty intervals. Keep the WebShop direction scoped to the reported comparison. |
| R6 | The Ursu paragraph omits consequential sample restrictions and uses 'overall bookings' too broadly. | State that the released sample excludes searches with no click and oversamples bookings. Confine position/click/booking results to sampled searches; distinguish this from conditional conversion. Source: dissertation Section 4.3 and Chapter 5. |
| R7 | Security coverage overweights a one-task AP2 prototype and reports AgentDojo's detector failure without its favorable defense results. A payment-limit check alone cannot validate product choice. | Compare AgentDojo's 97 user tasks/629 security cases with the prototype's repeated single query. Report both helpful defenses and detector false positives, and keep distinct attacker capabilities. Check product choice as well as payment/tool limits. Source: AgentDojo Sections 3.4/4.3; Whispers Section V. |
| R8 | The retry recommendation can be read as a check-then-repeat operation, which is weaker than a retry-safe request. | Recommend a stable request identifier for retries and checking the resulting order count, consistent with the checkout specification's idempotency requirement. |
| R9 | Product chronology, corrective history from earlier drafts, and repeated statements of what the review does not establish consume space without developing the argument. | Condense product descriptions to approval, availability, and responsibility. Remove the unnecessary 25-point straw comparison and first-review disclaimer. Keep access, scope, and source-removal details in the protocol/source record where possible. |
| R10 | The research recommendations need a defined comparison and outcome accounting; the conclusion needs to answer the paper's question using the revised evidence. | Specify comparable tasks, permission modes, failed attempts, tool/verification charges, buyer time, justified stopping, delivery and returns. Label these as a proposed evaluation, not one already run. Retain a concrete conclusion about suitable items, permitted actions, and correction work. |

## Response to the findings

| ID | Change made |
|---|---|
| R1 | Introduction now asks about suitable items, permitted actions and mistakes. Table 1's introduction separates approval from search automation and identifies advice as the comparison case. |
| R2 | Section 1.1 discloses the four short discovery queries, eight-result cap, purposive selection, access effects, AI assistance and absence of independently repeated appraisal or a common bias score. It no longer claims the search stopped at adequate topic coverage. |
| R3 | Abstract gives the economic-model and restricted hotel-field findings separate clauses and replaces a standalone benchmark score with the comparison of outcome measures. |
| R4 | Section 5.1 compares the designs without asserting that this cross-paper comparison identifies why the findings differ. |
| R5 | Section 5.5 reports the different best models under full-task accuracy and requirements satisfaction, author scoring checks and headline uncertainty limits. Section 5.3 keeps WebShop's small difference scoped to its reported comparison. |
| R6 | Section 6.1 states the omitted no-click searches and oversampled bookings and confines the ranking finding to the sampled setting. |
| R7 | Section 6.2 and Table 6 now compare study settings, state the GPT-4o defense-test scope and include both helpful defenses and detector false alarms. Table 7 checks item choice as well as externally enforced limits. |
| R8 | Table 7 now calls for the same unique request identifier on retries and inspection of the resulting order count. |
| R9 | Removed the abstract completion announcement, long introduction roadmap, first-review disclaimer, irrelevant product-launch detail, earlier draft's 25-point straw comparison, and repeated source-removal discussion. The source record retains historical/access details. |
| R10 | Section 7 now proposes comparable task/permission settings, all-attempt accounting, buyer-paid charges, separate buyer time, justified stopping and post-order outcomes. The conclusion names concrete choice failures, separates permission from safe tool use and retains correction work as a possible cost. |

## Remaining limitations

The changes improve the argument supported by the selected sources. They do not turn the review into a systematic search, remove inaccessible-source bias, independently reproduce the studies, validate the proposed controls, or supply live-order evidence. An independent human review has not occurred. The query cap is disclosed rather than retroactively described as a broader search.

## Verification status

All 96 prose blocks/table rows have been remapped in the fact-check record. The current manuscript SHA-256 is `1db83fc7e989fb13fdbe0a72625c8b22844f4c56377b386f17b3e033dfbdd213`, including the later author-list/contact changes and removal of the redundant methods opener. These presentation edits do not change the research findings; source dates remain in the protocol and ledger. The wording check returned 31 previously explained flags: thirty permitted bibliography colons and one negated proof claim. Initial PDF inspection found an isolated final conclusion paragraph; removing repeated legal/limitation summaries resolved it without changing margins or type size.

Completed checks:

- Native LaTeX/Tectonic PDF: 11 pages, no overfull boxes or undefined references.
- Alternate PDF: nine pages, with balanced final reference columns.
- All 40 references cited and linked; all 40 reference links blue and underlined in each HTML layout, with blue PDF links visually checked.
- All source prose/table/reference words recovered; no text outside the intended margins. One expected native word was rejoined across a line-end hyphen, with that restoration recorded in validation.
- Twelve added research-source files match their retrieval hashes. Fifteen research reference IDs are unique.
- First, table, conclusion and final reference pages rendered/inspected; conclusion is intact on native page 9.
- Manuscript whitespace and package-script syntax checks pass.

The dated validation JSON contains exact hashes. The checked package update preserves previous delivered files under a PDF-hash-named snapshot and records the new copies in its manifest. API-based external research aids remain unavailable as documented in the quality report; none is represented as a completed independent review.
