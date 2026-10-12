# Full fact and wording check

Audit date: October 13, 2026. This record covers the reviewer-led revision of **A Review of Agentic Commerce**. Earlier audits are preserved in `agentic-commerce-archive/before-academic-expansion/` and `before-reviewer-pass/`.

Reviewed manuscript SHA-256: `1db83fc7e989fb13fdbe0a72625c8b22844f4c56377b386f17b3e033dfbdd213`.

This revision adds twelve research works, for fifteen research works among 40 references, and compares their methods and conditional findings. It retains the approved title, blue reference links, plain language, and native ICLR-style format.

## What was checked

The review checks every substantive paragraph and table row below. A source-supported statement means the cited source supports that wording within its stated scope. It does not mean this review independently reproduced the study, tested the product, or gave a legal opinion. Definitions, examples, and proposed checks are identified separately from observations.

The 40-reference source log is `agentic_commerce_paper_sources.md`. Original dated copies are under `agentic-commerce/sources/checked-2026-10-12/`. The twelve additions, extraction cards, selection record, queries, metadata, and retrieval hashes are under `agentic-commerce/literature-expansion/`. The earlier three research PDFs and the additions were inspected for relevant methods, results, and limits. This review does not claim to have independently read every study cited by the two included reviews.

The current URL check returned 28 HTTP 200 and twelve HTTP 403 responses. Eight specific provider pages, references 1, 2, 3, 9, 11, 15, 16, and 20, were previously inspected through web-fetch, with notes in `agentic-commerce/sources/checked-2026-10-12/web-checked-notes.md`. Added DOI destinations 29, 31, 35, and 39 blocked curl, but their texts were obtained from Penn, NYU, and the publisher resource host. Findings are not inferred from HTTP status. Source files are hash-checked by the artifact verifier.

## Retained corrections from the preceding audit

1. **E-SIGN condition corrected.** The earlier sentence could imply that Section 7001(h) requires the law to attribute every agent action to its user. It makes attribution a condition of the stated protection. The revised paragraph states that condition explicitly.
2. **AI Act duty clarified.** Article 50 places a disclosure duty on providers, with exceptions. The text no longer describes it as a guarantee that people know they are interacting with AI.
3. **ACES effects scoped to the tested prompts.** Label effects are described for the default buying prompts. Their size depends on prompt, model, and interface; price-focused instructions can change them.
4. **Label ownership corrected.** The earlier audit replaced seller labels with platform labels, matching the ACES manipulation. The expanded ACES discussion retains that distinction.
5. **Publication status narrowed.** Reference 18 cites the inspected arXiv version. The paper no longer presents an independently verified conference-publication status on the basis of an author-posted acceptance note.
6. **Examples made explicit.** The washing-machine opening and $800 laptop request are illustrations, not reported incidents or study data.
7. **Legal return scope made explicit.** The text identifies goods bought online from traders, the start of the usual 14-day period, exceptions, and the exclusion of private-seller purchases.

## Qualifications added in the academic expansion

1. Algorithm aversion and appreciation are compared on feedback, choice, advice weighting, comparator, and expertise. Neither is generalized to willingness to delegate spending.
2. Follow-up control experiments share authors with the aversion study and are not called an independent replication. Greater use and decision quality remain distinct.
3. WebShop's partial-match score and full-success result move differently in the reported training comparison. Different benchmarks are not pooled into a trend or reliability rate.
4. Bakos is theory; Ursu is an inspected dissertation using hotel-search field data. Conditional conversion is distinguished from clicks and overall bookings.
5. Whispers uses one synthetic task repeated under three conditions. Product-first outcomes are separated from the six clear user-constraint conflicts; other cases have attribution ambiguity. It does not establish a universal AP2 flaw or broken signatures.
6. Funding/affiliations and version differences are recorded. Academic does not mean industry-independent. The 2018 control-paper issue date, 2016 author version, Ursu dissertation, corrected WebShop version, Whispers title mismatch, and Busch issue/online date mismatch are disclosed.
7. The two reviews provide context, not new experiments or 47 independently inspected additions. Access exclusions and the narrative selection method are explicit.

## Reviewer-led corrections

The full findings and response are in `agentic-commerce/reviewer-response.md`. The pass clarified the approval taxonomy and limited search, separated theory from hotel-field evidence in the abstract, narrowed the explanation of conflicting human findings, added EComAgentBench's metric ordering and judge checks, added Ursu's two sampling restrictions, balanced AgentDojo's helpful and harmful defense results, and made retry and product-choice checks more precise. Product chronology and repeated caveats were shortened. The sources and reference count remain the same.

## Paragraph and table-row audit

U numbers follow the order of non-heading prose blocks and table data rows, from the abstract to the conclusion. Table headings and captions are checked against their contents. Source numbers match the paper. A single row may contain both a sourced fact and a stated interpretation; the notes distinguish them.

| Unit | Kind | Evidence and disposition |
|---|---|---|
| U01 | Abstract summary | Fifteen works from selection.json; two surveys 15-16; human task limits 29-31; choice findings 17-19; metric-dependent comparisons 18/33; Bakos theory 35 separated from restricted hotel sample 36; both helpful defenses and false alarms 37. Proposed full-purchase outcomes from Section 7. No completion-date filler, pooled score, live-order rate, or population adoption estimate. |
| U02 | Illustration | Hypothetical washing-machine purchase introduced with 'Suppose', not an observed incident. |
| U03 | Definition and examples | Working definition now specifies tool use; advice, per-order and advance permission remain distinct. Product examples supported by 1/4. |
| U04 | Question and contribution | Suitable product, permitted action and correction are addressed in Sections 3-7. Recommendation/task/payment measures do not assess the same outcome. |
| U05 | Method record | Four saved OpenAlex discovery queries use per-page=8; known-study/citation/repository routes also recorded. Removed the redundant review-type/date opener at the author's request. Source dates remain in the evidence records. No census or saturation claim. |
| U06 | Eligibility, count and access | Protocol/matrix selection; three earlier plus twelve additions, including two reviews. Dissertation 36 inspected rather than unavailable final article. No count inflation from versions or underlying review corpora. |
| U07 | Appraisal procedure | Source matrix records tasks, comparisons, outcomes, commercial ties and scope; AI-assisted and not independently repeated. No common bias score or pooled effect calculated. |
| U08 | Independence appraisal | ACES author block includes MyCustomAI/Columbia/Yale; 18 Shopee; 37 ETH/Invariant; 34 AWS gift/government support. Recorded ties are not grounds for automatic acceptance or rejection. |
| U09 | Evidence rule | Provider claims, selected legal text and proposed checks remain distinct from independently measured outcomes. |
| U10 | Review comparison | Reference 32 review/reused qualitative barriers versus 39 evidence map, reported 47 studies, single-researcher coding and consumer focus. Reasons to retain shopping tasks are arguments from the review, not a new effect estimate. |
| U11 | Evaluation comparison | WebShop Sections 3-5, WebArena Sections 2-4, ACES Section 2, EComAgentBench Sections 3-4, Tool-Lab methods. Tasks and scoring differ. |
| U12 | Scope and positioning | Security 37/38 and Busch C-D extend product suitability to who can direct actions and how errors can be challenged. Removed the unnecessary first-review disclaimer. |
| U13 | Definition | Table 1 classifies purchase approval, not search autonomy. Advice is a comparison case. Unsupervised search with per-order approval is a definition/example, not a measured product claim. |
| U14 | Definition | Advice leaves purchase selection/action with the person. |
| U15 | Definition | Per-order approval consistent with launch flow in 1. |
| U16 | Definition | Advance permission consistent with 4/8; no promise every service supports every limit. |
| U17 | Product facts | Reference 1 September 2025 US-user/US-Etsy/one-item confirmation and seller duties; 2-3 mixed checkout routes. Shortened launch description preserves geographic and approval limits. |
| U18 | Product facts | Reference 4 May 2026 US rollout, target-price Auto Buy, eligible Buy for Me, and notice/cart-only actions. Cart updates not counted as completed purchases. |
| U19 | Illustration and reasoning | Explicitly illustrative $800 request. Missing condition/preferences motivate questions, not an incident count. |
| U20 | Definitions and scope | Protocol/API definitions and roles in 6, 8-10, 12, 14. No tested interoperability claim. |
| U21 | Protocol role | ACP 12 overview/checkout session; suitability outside checkout function. |
| U22 | Protocol role | UCP 6 discovery/negotiation/capability list; matching functions and versions. |
| U23 | Protocol role | AP2 8 mandate definitions. Valid permission is not product quality. |
| U24 | Protocol role | Mastercard 9 identity-permission-action records; legal responsibility remains separate. |
| U25 | Protocol role | x402 14 digital/API access, not physical fulfillment. |
| U26 | Announced plan | Sierra 10 'What comes next'; first specification planned later in October. |
| U27 | Requirements and scenario | ACP 12 states, headers, retries and idempotency. Lost-response scenario is illustrative, not a measured failure. |
| U28 | Compatibility and status | UCP 6 discovery/negotiation depends on matching functions/versions; 5 labels hotel extension draft. Removed release chronology without changing status. |
| U29 | Technical definitions | AP2 8 open/closed checkout/payment records; UCP 13 binding checkout to payment. |
| U30 | Protocol designs | Google 7 v0.2 human-not-present flow; Mastercard 9 identity-permission-action/selective disclosure. Records can support reconstruction, not measured dispute resolution or agent compliance. |
| U31 | Technical role and cost accounting | Coinbase 14 API/digital-resource payment. Including a buyer-borne information fee even after a failed attempt is an explicit accounting recommendation, not an observed charge or market estimate. |
| U32 | Announced plans | Sierra 10 October announcement with later-month specification; Riskified 11 December beta. Both remain planned, not generally available services established by these sources. |
| U33 | Human findings | Reference 29 methods/results, 30 identical-label tests and own/expert comparisons. Feedback and weighting tasks are different; no universal distrust/appreciation claim. |
| U34 | Human comparison | Reference 29 forecasting choice after varied performance exposure. Not a spending task. |
| U35 | Human comparison | Reference 30 identical advice in key tests, own judgment/expertise qualifications. |
| U36 | Human comparison | Reference 31 studies 1-3; limited modifications can improve uptake. Does not assert each manual correction improves accuracy. |
| U37 | Comparison and inference limit | References 29/30 differ in feedback, comparator and decision. The review does not isolate a causal explanation across papers. Neither measures spending permission; separate outcomes are proposed for shopping. |
| U38 | Control finding and proposal | Reference 31 abstract, methods/results/discussion; author overlap with 29. Performance benefit from model use separated from per-adjustment quality. Editable limits require a shopping test. |
| U39 | Survey methods | 'About the Survey' in 15/16, age 18-64, recent online buyers, nine-market versus US/UK coverage. |
| U40 | Survey data | Reference 15: September-October 2025, 5,400, nine markets, 73%, 13%, 70%. Referral purchases not delegated agent orders. |
| U41 | Survey data | Reference 16: Q1 label, April 27 release, 2,000, 1,000 each country, 61.5%, 55.0%, 73.9%. No invented field dates. |
| U42 | Survey comparison limit | Countries from 15, narrower coverage 16, unavailable full matched scales. Removed the earlier draft's 25-point straw comparison; discomfort still cannot be complemented into a verified comfortable share. |
| U43 | Survey interpretation | Reference 16 reports 50.8% assigning platform responsibility; no cross-tabulation or legal allocation inferred. |
| U44 | Source appraisal and proposal | Vendor purpose and published methods in 15/16; questionnaires, weights and individual data unavailable. Repeat comparable survey is a proposal. |
| U45 | Evaluation comparison | Five evaluations in Table 5 correspond to 17-19/33-34. Incompatible tasks, actions and scoring prevent direct headline ranking. |
| U46 | Benchmark row | WebShop Sections 3-5, partial reward and reward-equals-one success; simulated buy. |
| U47 | Benchmark row | WebArena Sections 2-4, website state/answers across multiple domains. |
| U48 | Benchmark row | ACES Section 2 and simple-task tests; selection not paid sales. |
| U49 | Benchmark row | EComAgentBench constructed needs/profile/replies and target-or-rubric correctness. |
| U50 | Benchmark row | Tool-Lab goals/inspection-cost comparisons; unit price differs from total including search costs. |
| U51 | Metric counterexample | WebShop Section 5.2/Figure 4: partial score 59.9 to 62.4, full success 29.1% to 28.7%. Direction in this comparison, not a general adverse effect of reward training or a statistical-detectability claim. Neither score includes delivery/returns; dated v4 pinned. |
| U52 | Benchmark design and limit | WebArena evaluation functions, unachievable tasks, human protocol. Some checks use models and humans cover a subset; no cross-benchmark trend asserted. |
| U53 | Research setup | ACES Section 2, eight categories/eight items, one-page and text-list interfaces. |
| U54 | Research finding | ACES Sections 5.2/7.2, default buying prompts, fixed position for label effects; model/prompt/interface dependence. |
| U55 | Research finding | ACES v3 Sections 3.2/5.3, improved simple tasks plus changed selection patterns. No all-model/current-deployment claim. |
| U56 | Research limits | ACES generic preferences and fixed-position ad-label comparison. Label penalty not total paid-placement effect. |
| U57 | Research numbers and metric ordering | EComAgentBench Sections 3/5, Table 3: 662 tasks, 100 calls, 10 questions, seven models, Opus 4.6 57.1% accuracy; GPT-5.4 leads the separate rubric-satisfaction score. Main table has no uncertainty intervals. No invented intervals or live-order rate. |
| U58 | Research findings/limits | EComAgentBench Sections 5-7/Limitations: unused profile facts, missing review evidence, constructed needs, English electronics-heavy catalog, scripted replies and single recommendation per task. |
| U59 | Evaluator appraisal | EComAgentBench Sections 5-6: exact-match correctness independent of judge; non-exact path judged against all rubrics; exact-match cross-check and GPT-5.4 manual non-exact audit. Source does not establish perfect judging for every model. Metric comparison linked to WebShop 33. |
| U60 | Research design/finding | Tool-Lab methods/Studies 1-2, eight models, vague versus unit-price goals under stated inspection cost; model variation retained. |
| U61 | Cost-accounting limit | Tool-Lab methods specify $0/$10/$50 task-assigned costs. Product unit-price outcome excludes lookup charges; no actual shopper fees or general waste claim. |
| U62 | Product documentation | OpenAI 2 selection/pricing guidance; incomplete coverage and possible delayed prices attributed to provider. |
| U63 | Conditional market argument | ACES 17 presentation effects motivate competing concentration/small-seller possibilities; no aggregate sales or exposure effect measured here. Proposed controls include stock, prices and accessible catalog. |
| U64 | Theory comparison | Bakos Sections 1-3/5.1-5.3 distinguish price and feature information costs under assumptions. Unlike Tool-Lab's assigned inspection costs, this is an economic model of buyers and sellers, not observed AI-market prices. |
| U65 | Restricted field-data finding | Ursu Section 4.3/Chapter 5: no-click searches omitted, bookings oversampled. Random-order position findings scoped to sampled searches; conditional conversion not detected as a further effect. No all-visitor rate or automatic transfer to AI. |
| U66 | Stated policy and proposed test | OpenAI 2/20 describe ad/result separation. No independently verified neutrality. Proposed isolation of fees/labels/access/placement retains ACES fixed-position versus total-placement distinction. |
| U67 | Design argument | Integration in 6/12 does not determine ranking in 2/17. Possible reduced integration effort is not measured savings or guaranteed seller access. |
| U68 | Technical threat scope | AP2 21 includes agents/prompt injection in the threat model; Riskified 11 separates authorization/account trust. No security guarantee. |
| U69 | Security task units and metrics | AgentDojo Sections 3.4/4: 97 user tasks, 629 task/attacker-goal cases; no-attack completion, completion under attack, attacker success. Low success can reflect weak execution, not safe behavior. |
| U70 | Balanced defense findings | AgentDojo Section 4.3/Figure 9 and tool-isolation limits: GPT-4o tests include defenses improving ordinary completion while reducing attacks; detector false positives reduce utility; allowed tools can still enable harm. Not generalized to every defense/model. |
| U71 | Prototype design/comparison | Whispers Sections III-V: four Gemini-2.5-Flash agents, synthetic data, one shoe query, ten runs in each of baseline/product/credential conditions. Merchant-content versus malicious-user attack capabilities distinguished. |
| U72 | Security comparison row | AgentDojo 97 tasks/629 security cases and both helpful defenses/false alarms from Sections 3.4/4.3. Test cases are not independent shoppers or a deployed fraud denominator. |
| U73 | Prototype product attack | Whispers V-A/Table I: first rank 10/10, clear conflict 6/10. Four ambiguous cases not counted as equally clear harm. |
| U74 | Prototype credential attack | Whispers V-B/Table I: synthetic cross-account exposure 2/10; partial access attempts excluded from exposure count. |
| U75 | Security scope | Thirty runs repeat one query; synthetic data, intact signatures and ambiguous product cases. Old mandate terminology checked against AP2 8. Broader 37 plus prototype 38 support failure paths, not universal AP2 flaws or real fraud incidence. |
| U76 | Proposed checks | Table 7 motivated by 12/21/37/38 and choice evidence; no effectiveness validation performed. |
| U77 | Proposed check | Compare order and requested details; no estimated benefit/frequency. |
| U78 | Proposed check | Refresh order total/terms; ACP 12 authoritative checkout state. |
| U79 | Proposed check | Record and bound permission; AP2 8/21. |
| U80 | Retry check | ACP 12 overview and Idempotency-Key request header. Reusing the stable identifier for retries is more precise than a check-then-repeat instruction; inspect resulting order count. |
| U81 | Proposed choice/limit checks | AP2 21 and shopping attacks 38. External limits alone do not establish product suitability, so record changed choices as well as denied/out-of-limit actions. Not a proven defense. |
| U82 | Proposed access check | Tool/service identity enforcement motivated by Whispers credential failures; not a certified fix. |
| U83 | Proposed usefulness check | Ordinary completion and false rejection motivated by AgentDojo defense trade-off. |
| U84 | Proposed correction check | Support/refund records, not a claim all protocols implement this control. |
| U85 | Recommendation | Readable receipt/permission linkage; no measured comprehension gain. |
| U86 | Legal text | E-SIGN 7001(b)/(h), attribution a condition rather than automatically created by the Act. |
| U87 | State legal text | RCW 1.80.130/.090, automated formation and conditional human-error relief, not universal reversal. |
| U88 | Legal text/guidance | Commission timeline 25 and Article 50(1) 26; provider duty, exceptions, different later high-risk dates. |
| U89 | Consumer guidance | Your Europe 27, covered trader/online goods, 14 days from delivery, exceptions/private-seller exclusion. |
| U90 | Data rights and scope | EDPB 28 qualified rights; retention/access recommendation not automatic erasure. Selected US/EU scope. |
| U91 | Legal scholarship | Busch C-D/conclusion on goal setting and manipulation of/by agents. Reform argument separated from enacted law or tested comprehension effects. |
| U92 | Proposed complete-purchase comparison | Four assistance modes with comparable needs, limits and access; suitability, permitted actions, money, time and post-order outcomes. Proposal only, no experiment performed. |
| U93 | Proposed accounting and stability checks | All attempts and buyer-paid costs, with time separate; stop/ask tasks motivated by 18/34. Repeated runs/model versions/attacks suggested, not pooled or newly measured. |
| U94 | Review limits | Limited accessible-English search, forecasting/hotel transfer, constructed tasks, one survey vendor, provider/legal coverage, no replication/live orders/independent second appraisal. |
| U95 | Conclusion findings | Choice evidence 17-19, permission 8/12/13, and separate security/usefulness measures 37-38. No new result, market claim or live-order success rate. |
| U96 | Conclusion and proposed comparison | Section 5 human/survey scope does not estimate population delegation. Sections 6-7 support full-order and correction accounting; extra work after a fast order remains a possibility, not measured aggregate harm. |

## Bibliography audit

The current author block uses the supplied names Vedang Ratan Vatsa, Author2, and Author3. Vedang's website is displayed as `veda.ng` with target `https://veda.ng`. Author names and website are presentation data, separate from the research references and the 96-unit claim audit.

All 40 entries have a specific source link and a body citation. Authors, source names, titles, publication/version dates and access dates were checked against inspected documents and source metadata. The date/version exceptions are recorded above and in the matrix. Mutable documentation without a stable date remains labeled current guidance/documentation. Exact bibliography titles retain terms such as 'Emerging Implications' in 17 and 'Implications' in 35, even though these words are excluded from original prose.

## Wording and format review

- Removed stock summary sentences, repeated caveats, and phrases such as 'the more defensible finding' and 'the central test'.
- Replaced technical wording where the meaning allowed it, including 'authorization' in the AP2 explanation, 'clarification turns', and 'denominators'.
- Kept required names and explained AI, API, mandates, ACES, and GDPR. Training/scoring comparisons use plain descriptions rather than equations or unexplained learning-method abbreviations.
- Added three compact comparison tables for human reliance, agent evaluations, and prototype security. The existing checks table now also covers account access and false rejection of valid tasks.
- Shortened and reorganized the paper into the framework's formal structure: introduction with method, related work, analysis, discussion, open questions/limits, conclusion, references.
- Used the ICLR style file from the requested repository at commit `4681f29ae80006ca659e9f706c7148e98f537122`, with Tectonic, Times text, numbered citations, booktabs-style tables at consistent footnote size, and left-aligned references starting on a new page.
- No equations, fabricated uncertainties, country scores, risk probabilities, or adoption curves were added.
- After the author's wording feedback, replaced the whole conclusion with named study findings, the limit of payment permission, and concrete purchase/correction outcomes. Removed the generic closing sentence about what product announcements cannot measure.
- The subsequent full reviewer pass removed the abstract completion announcement, shortened product chronology and repetitive caveats, and made substantive corrections to sampling, scoring, defense comparisons, and recommended checks. The conclusion now also reflects the security and population-inference limits.

Automated word checks can flag unwanted phrases but cannot prove that prose has no recognizable AI style. The text received a sentence-level edit in addition to those checks. AI assistance remains recorded in the research protocol; this audit is not independent human peer review.
