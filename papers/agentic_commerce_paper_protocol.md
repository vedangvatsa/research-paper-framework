# Research protocol: Agentic commerce revision

## 1. Status and scope

- Responsible author: Vedang Ratan Vatsa. Research and editing assisted by an AI coding assistant.
- Current author list supplied by the user: Vedang Ratan Vatsa, Author2, and Author3. Displayed contact: [veda.ng](https://veda.ng), under Vedang's name.
- Protocol started October 12, 2026. Version 4 adds the requested full reviewer pass after the academic expansion; earlier planning and audit entries remain below as history.
- Manuscript: `agentic_commerce_paper.md`.
- Study type: Focused narrative review of published evidence and official product and legal documents. This design fits a question about what current evidence supports. It does not estimate a market share or test an intervention.
- Stage: First two revisions completed October 12; expanded research inspection and manuscript revision completed October 13. Production checks are recorded separately in the review report. The original planning sections below precede the first review; the second-pass plan is in Section 10 and the expansion plan/outcome in Sections 11-12.
- Prior exposure: The existing manuscript has been read. It contains adoption curves, survey comparisons, simulator effect estimates, regulatory scores, and risk probabilities. Their provenance has not yet been established. This plan is retrospective with respect to that manuscript and prospective with respect to the new source review.
- Registration: Unregistered. This is not a preregistration.
- Primary question: What do current public sources establish about AI agents' ability to help people buy goods, and what remains uncertain about buyer control, seller competition, and responsibility for errors?
- Setting: Consumer-facing online commerce, with payment and protocol examples relevant to that setting. English-language sources available at the review date.
- Contribution: Distinguish product claims from observed evidence; compare the jobs performed by payment and shopping protocols; compare conditional research findings on acceptance, choice, seller access, and security; explain consumer and seller risks in plain language.
- Exclusions: No original shopping experiment, market forecast, country ranking, investment advice, or legal opinion. Machine payments for APIs are included only to explain how they differ from consumer checkout.

## 2. Literature and gap record

The source search and claim-level evidence will be recorded in `agentic_commerce_paper_sources.md`, including the actual search queries, dates, URLs, passage summaries, evidence types, and access limitations.

Selection follows the original paper's citation trail, official documentation for shopping and payment systems, research papers on shopping-agent behavior, and official legal texts. Prefer original studies and first-party documents. Use news coverage for discovery and context, not as a substitute for an accessible original study. A company announcement establishes what a company says it launched, not adoption or reliability. Include critical and negative findings. Deduplicate articles about the same underlying study. Do not pool unlike surveys or laboratory results.

The closest work and its methods will be recorded after reading. The intended gap is an accessible account that connects technical capabilities with evidence quality and buyer protections, not a claim that this topic has never been reviewed.

## 3. Proposed claim-to-evidence map

| ID | Proposition and scope | Evidence needed | Rival explanation or disconfirming evidence |
|---|---|---|---|
| C1 | Some systems can carry out parts of checkout under stated conditions | Dated product documents specifying markets, availability, and user approval | Announced feature is a pilot, planned, withdrawn, or narrower than the claim |
| C2 | Protocols solve different parts of shopping and payment | Current specifications and first-party descriptions | Similar names hide different functions; advertised compatibility is not tested interoperability |
| C3 | Confidence in advice and willingness to delegate payment are different outcomes | Survey wording, sample, field dates, and method | Different wording or samples can explain apparently changing attitudes |
| C4 | Shopping agents can respond to seller-controlled cues | Methods and results of controlled research | Results vary by model and task or fail to transfer to real purchasing |
| C5 | Product data and platform choices may affect seller access | Supported mechanism and competing explanations | Brand and platform reputation can remain relevant; no market-level causal estimate |
| C6 | Existing rules govern parts of AI-assisted buying but do not provide one universal liability answer | Official legal text and scope, with legal status checked | Rules differ by jurisdiction, contract, use case, and later amendments |

## 4. Definitions and assumptions

AI shopping advice, user-confirmed checkout, and delegated purchase are separate activities. A recommendation is not a completed purchase. A payment protocol is not a promise that an agent chose a suitable product. An announcement is not an independent evaluation. No mathematical proof or formal model is proposed.

Assumption A1: Official documents accurately describe their advertised features at the stated date. Cross-check dates and scope; narrow to a company-reported claim if independent confirmation is absent.

Assumption A2: Published simulator findings are informative about tested systems, not representative of all live shopping. Preserve model, task, and design limits; exclude unsupported generalizations.

## 5. Decision log

| ID | Decision and rationale | Alternative and trade-off | Sensitivity or revision trigger |
|---|---|---|---|
| D1 | Use a narrative review and plain language, as requested | A new experiment could support causal estimates but requires new data and a separate design | Do not call this a systematic review or original quantitative study |
| D2 | Remove old numerical claims unless their original data and method can be traced | Retaining them as scenarios could confuse assumptions with findings | Restore a number only with a source passage, denominator, and valid interpretation |
| D3 | Avoid complex mathematics; use small comparison tables | Equations could represent an illustrative model but do not fill the evidence gap | Include arithmetic only when it clarifies a sourced comparison |
| D4 | State a source-check date and preserve original publication dates | Calling all retrieved documents new could misstate chronology | Flag mutable documents and distinguish announcement dates from access dates |
| D5 | Replace numerical country rankings with selected US and EU legal examples | A global legal comparison requires more languages and a separate legal search | Restrict conclusions to the inspected provisions; no claim about China's relative readiness |

## 6. Review design

- Unit: A source-supported claim, with multiple reports of the same source treated as dependent.
- Sampling: Purposeful coverage of shopping capability, protocols, trust, agent behavior, seller effects, and legal responsibility. English-language and accessibility limits apply.
- Stopping: Each central claim has an inspected supporting source or is narrowed/withdrawn; unresolved points remain explicit. This does not establish exhaustive coverage.
- Experimental allocation, power, held-out tasks, and cost-per-success: Not applicable to a document review. No new performance estimate is calculated.
- Source appraisal: Identify author or publisher, publication/update date, study design or document type, population or product scope, passage supporting the claim, commercial interests, and uncertainty.

## 7. Recording and analysis

Record source IDs, titles, verified URLs, dates, supporting passages in paraphrase, access problems, and manuscript claims. Keep reported outcomes separate from the author's proposed controls. Do not invent missing standard errors or treat a press release as a full methods report. Do not combine incompatible denominators. Legal comparison is descriptive, without readiness scores.

## 8. Reproducibility and validity

Artifact paths: manuscript, this protocol, source ledger, review report, build script, and generated HTML/PDF files. Retain the pre-revision manuscript and PDF outputs in a dated archive before rebuilding. Record actual build and verification commands in the final review report. Documents on the web can change; source summaries and retrieval dates support auditing but are not a full web archive.

## 9. Initial open questions

| ID | Question | Consequence and planned action |
|---|---|---|
| Q1 | Is there support for the original ACES effect sizes and standard errors? | Inspect the full paper; omit any unsupported numeric table |
| Q2 | Were the Riskified figures measured with matching questions and samples? | Inspect the survey releases and method; avoid a longitudinal claim without evidence |
| Q3 | Which announced checkout features remain available? | Check current official documentation and distinguish historical launches from current scope |
| Q4 | Have legal deadlines or provisions changed? | Check current official sources and avoid treating proposed changes as enacted law |

## 10. Final evidence audit

### Second audit and framework revision plan

The user requested another full fact check, a stricter plain-language edit, and the format in the public framework repository. This second pass starts with exposure to all results recorded above. It is a retrospective audit, not preregistered research.

- Framework snapshot: `vedangvatsa/research-paper-framework`, commit `4681f29ae80006ca659e9f706c7148e98f537122`, checked October 12, 2026.
- Format decision: follow the formal-paper pipeline in `PAPER_FRAMEWORK.md` and its example, using the ICLR style, LaTeX, and Tectonic. Keep numbered citations, left-aligned references, author name/email, and keywords. The local methodological rules take priority over any older suggestion to infer a cause without a valid design or treat HTTP status as source verification.
- Fact-check plan: re-read source passages for every numerical, dated, product, protocol, study-design, and legal claim. Check research PDFs as well as the HTML/abstract where practical. Map paragraphs and table rows to sources, definitions, illustrations, or explicitly proposed checks. Narrow or remove claims that the available material cannot establish.
- Language plan: remove repeated disclaimers, vague summaries, stock transitions, and unnecessary technical terms. Preserve precise legal and study limits in plain wording. This is a style edit, not an attempt to conceal AI assistance.
- Preservation: save the preceding revision and update only the paper's managed files in the publication folder. Check the package manifest before replacing files.
- Initial correction: Section 7001(h) makes legal attribution a condition. It does not compel attribution of every electronic agent action to the user. Correct this distinction in the manuscript.

| Claim | Finding and evidence | Status and allowed interpretation |
|---|---|---|
| C1 | References 1-4 describe user-confirmed, merchant-site, and target-price purchase paths | Supported as provider-documented features. No independent live checkout or usage-rate claim |
| C2 | References 5-14 describe distinct commerce, authorization, record, and digital-service payment functions | Supported at specification/announcement level. Interoperability and adoption not independently tested |
| C3 | References 15-16 use different country samples and do not establish a panel | Interest and delegation are distinct reported outcomes. A measured 25-point decline is withdrawn |
| C4 | ACES v3, EComAgentBench v3, and Tool-Lab methods/results were inspected | Supported for the tested tasks and models. No common or live purchase error rate |
| C5 | ACES and current shopping documentation support mechanisms involving presentation and access | Market-wide concentration and a universal data-completeness sales gain remain unestablished |
| C6 | References 22-28 distinguish contract attribution, state error rules, AI disclosure, return rights, and data rights | Supported within selected legal scope. No universal liability rule or readiness ranking |

Open questions Q1-Q4 were resolved or narrowed. Q1: the old fixed ACES effects and error bars were unsupported and removed. Q2: survey populations differ; longitudinal wording was removed. Q3: historical launches were separated from current help guidance and planned releases. Q4: the current Commission timeline and consolidated Article 50 page were checked; the manuscript does not treat all AI rules as having the same deadline.

The old adoption confidence band, risk probabilities, and country scores were also withdrawn after inspecting the hard-coded chart script. Originals remain in the dated archive. The review uses no complex mathematics or unsupported replacement figures.

In that revision, the strongest remaining objection was transfer from published tests and commercial documentation to actual shopping. The paper limited its conclusions and proposed whole-purchase evaluation. The abstract benchmark numbers matched the then Section 5.3 (Section 5.5 after expansion).

Actual checks, corrections, unavailable tools, and the ten-perspective review are recorded in `agentic_commerce_paper_review.md`. Source details are in `agentic_commerce_paper_sources.md`. Artifact results and hashes are in `../reports/agentic_commerce_validation_2026-10-12.json`. The work involved AI-assisted source review and editing; no independent human peer review or original replication was performed.

The completed second-pass fact check, now preserved in `agentic-commerce-archive/before-academic-expansion/agentic_commerce_fact_check.md`, covered 69 substantive units and all 28 references. The current `agentic_commerce_fact_check.md` covers the expanded paper. Dated source copies and the pinned framework files are under `agentic-commerce/`. The formal build uses the repository's ICLR style with LaTeX and Tectonic.

## 11. Expanded academic review plan, October 13, 2026

The user requested a wider review of independent academic research after the narrow academic base of the previous version was explained. Prior exposure includes the three already reviewed shopping-agent papers, two Riskified survey releases, and product/legal sources. The names of several older trust and search studies are known as search leads, but their findings will not be added without source inspection. This remains an unregistered narrative review.

### Questions and selection

| Stream | Question | Sources sought | Important boundary |
|---|---|---|---|
| Consumer behavior | When do people accept, reject, or want control over algorithmic advice and decisions? | University-led experiments, including evidence of both aversion and appreciation; studies of shopping decision aids | Advice acceptance is not permission for autonomous spending |
| Agent performance | What do tests establish about search, choice, interaction, and task completion? | Published academic shopping/web-agent benchmarks and current follow-up work | Older benchmark results are not current product success rates; different scores cannot be pooled |
| Markets and sellers | How can search costs and rankings affect buyers and sellers? | Economic models and independent field studies | Human-market or theoretical findings are mechanisms to examine, not observed effects of AI shopping |
| Security and responsibility | How can outside information redirect an agent, and what do existing controls cover? | Academic prompt-injection experiments and relevant legal scholarship, alongside enacted law already checked | General agent attacks do not measure the frequency of shopping fraud |

Eligible additions need a relevant method or argument, identifiable authors and source, and enough accessible text to check the used claim. Search publisher records, institutional repositories, conference proceedings, and arXiv. Follow citations from central studies. Prioritize peer-reviewed work where available, but distinguish peer review from correctness and record the inspected version. Earlier work is eligible when it tests a mechanism still relevant to delegation, recommendation, search, or ranking. Exclude promotional statistics compilations, unsupported opinion pieces, duplicate versions counted as separate studies, and studies whose relevant methods/results cannot be inspected.

Independence is not inferred from the word 'academic'. Record author affiliations and declared funding/conflicts when available. Distinguish university-led work, mixed university/company work, company-only research, and vendor releases. Unknown funding remains unknown. Sources with overlapping authors, data, or designs are not treated as independent replications.

### Extraction and synthesis

For each selected study record publication/version, question, design, sample/task, comparison, outcome, key finding, counterevidence, access route, and limit of transfer to agentic commerce. Compare contradictory findings explicitly. Keep human experiments, simulations, field observations, theory, product documents, and law distinct. Do not calculate a combined trust or reliability score.

Stopping rule: obtain relevant, inspected evidence for each stream, including opposing or conditional findings where the search finds them; follow up unresolved central contradictions or narrow the paper's claim. Stop when the planned streams have coverage and additional inspected leads duplicate already represented mechanisms. This is a coverage rule, not a claim of exhaustive or systematic retrieval and not a citation quota.

Keep the approved title, simple language, absence of complex mathematics, blue reference links, and native ICLR-style build. Save the preceding manuscript and records before editing. Update the evidence log, study comparison tables, claim audit, quality report, and Downloads bundle after the new review.

## 12. Expanded evidence audit, October 13, 2026

### Work performed and decisions

The search retained twelve additions, references 29-40, after inspecting relevant full-text methods/results or arguments. The full research set is fifteen works, including the earlier references 17-19. Search queries, routes, unsuccessful retrievals, and version identities appear in `agentic-commerce/literature-expansion/review-matrix.md`; `selection.json` lists the retained source keys. Sources with distinct versions were counted once. The two reviews are contextual evidence, not fifteen plus their underlying studies. This AI-assisted search and appraisal was not independently double-screened.

| Decision | Rationale and alternative | Assumption, check, and consequence |
|---|---|---|
| Include older forecasting experiments | Tests of feedback, advice labeling, and control can clarify conflicting trust claims. Restricting to papers called agentic commerce would omit these contrasts. | Shopping transfer is untested. Separate reliance from spending permission; no pooled trust estimate. |
| Include both reviews and original studies | Reviews explain scope while primary studies support detailed comparisons. A review-only account would hide design differences. | Do not count review citations as independently inspected studies. Mark single-researcher coding and reused qualitative evidence. |
| Cite Ursu's 2016 dissertation | Its complete methods/results are accessible; the 2018 final article is not. Exclusion is the alternative. | Cite the actual inspected version and restrict use to ranking/click/booking findings, not uninspected journal differences or modeled welfare dollars. |
| Include Whispers of Wealth with narrow wording | Direct shopping prototype complements broader AgentDojo tasks. Excluding a small study would remove this concrete failure example. | Preserve one-task repetition, attacker capabilities, synthetic data, six clear versus four ambiguous product outcomes, and version differences. General security conclusion also has evidence without this source. |
| Keep company involvement visible | Company-only, mixed, and industry-supported research can contain useful methods. Blanket exclusion would discard EComAgentBench and AgentDojo. | Appraise methods as well as affiliations; no claim that all fifteen works are independent academic experiments. |
| Retain stable DOI links plus saved alternate full texts | DOI links identify publications; accessible source copies support passage inspection. Replacing them all with transient file URLs could reduce reference stability. | Four added DOI destinations block curl. Record actual full-text access and hashes, never interpret 403 as evidence of content. |

### Claim status after expansion

| Claim | Evidence and counterpoint | Status and scope |
|---|---|---|
| C1-C2, service scope and protocol roles | Existing product/specification evidence retained; research distinguishes choice, tool access, and permission | Supported as documented capabilities/designs, not independently tested deployment or interoperability |
| C3, reliance versus delegated spending | References 29-31 contrast performance feedback, identical advice labels, and limited control. References 32/39 add review context; surveys 15/16 remain unlike samples | Conditional human-task findings supported. Population trust trend and willingness to delegate real spending remain unestablished |
| C4, choice and completion | ACES, WebShop, WebArena, EComAgentBench, Tool-Lab test different decisions/scoring. WebShop's partial score and full success can differ in direction | Supported under source test conditions. No pooled reliability score or universal claim that newer models choose better products |
| C5, seller access and prices | Bakos distinguishes price versus feature information costs; Ursu's random-order data distinguish clicks/overall bookings from conditional conversion | Theory and human-field mechanisms supported. Net AI-market price/concentration effect remains open |
| C6, legal scope | Existing statutory guidance plus Busch's argument about earlier goal/permission setting and provider influence | Enacted text separated from legal reform; no new universal liability conclusion |
| C7, tool safety versus payment permission | AgentDojo measures useful completion and attacker success separately; Whispers illustrates prototype ranking/credential failures without signature breaks | Controlled failure mechanisms supported. No real-world fraud rate, universal AP2 flaw, or validated effectiveness for the proposed checks |

### Sensitivity and open questions

- Removing the vendor surveys preserves the distinction between advice reliance and payment permission, but this review then has no direct survey basis for describing the sampled shopping attitudes. Neither version estimates population adoption.
- Removing the small AP2 prototype retains the general tool-security concern through AgentDojo and AP2's threat model, but removes its shopping-specific repeated-run outcomes.
- Omitting older human forecasting studies leaves review arguments and shopping surveys, but weakens the experimental basis for explaining why feedback, comparator, and control matter. Their transfer remains a research question, not an assumed shopping effect.
- Excluding the inaccessible final Ursu article does not justify pretending the dissertation is that article. No claims depend on uninspected differences between versions.
- Unresolved questions concern real orders, repeated use, useful versus burdensome control, market-wide prices/exposure, implementation security, and liability across settings. Complete purchase attempts with failures and correction outcomes are proposed next evidence, not results already obtained.

The expanded manuscript retains eight numbered sections and has seven tables and 40 references. Its full audit covers 96 prose blocks/table rows. The benchmark's 662 tasks, seven models, and 57.1% remain in Section 5.5; the later reviewer pass replaces the abstract's single-score example with a comparison of outcome measures. Research counts exclude reviews' underlying studies. The preceding revision is archived in `agentic-commerce-archive/before-academic-expansion/`. Current artifact checks and hashes belong to `../reports/agentic_commerce_validation_2026-10-13.json`.

### Conclusion wording revision

The author subsequently called the conclusion vague and flagged its last sentence as stock AI wording. The replacement names the ACES, EComAgentBench, and Tool-Lab findings, distinguishes buying permission from a suitable product, and specifies the comparison needed for real orders. Wrong items, duplicate orders, charges, refunds, and correction time already appear in Sections 6-7. No evidence or numerical result was added. The possible extra work after a fast order is stated as a possibility, not a measured effect. Audit units U95-U96 and the manuscript hash were updated. The preceding passage is retained in `agentic-commerce-archive/conclusion-before-2026-10-13-edit.md`.

## 13. Requested full reviewer pass

The author requested a full review and revision after the abstract's completion-date sentence had been removed. This pass is retrospective and uses the existing evidence set. It is performed by the same AI assistant, not an independent peer reviewer. The working draft and earlier artifacts were saved under `agentic-commerce-archive/before-reviewer-pass/` before the broader edit. The review findings and response are in `agentic-commerce/reviewer-response.md`.

The pass re-inspected EComAgentBench Sections 3/5/6 and Limitations, AgentDojo Sections 3.4/4.3, Ursu Section 4.3/Chapter 5, WebShop Section 5.2, Logg Sections 1.2-1.3, Bakos Section 5, Whispers Section V, and the checkout idempotency requirement. This is additional appraisal of retained sources, not a new literature search, experiment, or independent replication.

| Decision | Reason and alternative | Effect on conclusions |
|---|---|---|
| Disclose the eight-result cap on four discovery queries | The saved requests show this limit. Calling the search saturated or broad would overstate it. | Review conclusions concern selected sources, with access and investigator selection limits. |
| Retain separate approval and task-automation concepts | Advice, per-order approval and advance permission are not a single maturity ladder. | A service can automate search while leaving order approval with the person. |
| Add benchmark counterevidence and scoring checks | Reporting only Opus's accuracy or only the presence of an AI judge omits other outcome rankings and author validation. | EComAgentBench and WebShop both motivate distinguishing partial from full success; no pooled score or universal training effect. |
| Add Ursu sample restrictions | No-click searches are missing and bookings are oversampled. A general hotel-market rate is not justified. | Limit position effects to the sampled setting and separate conditional conversion. |
| Balance security results and study scale | AgentDojo includes useful defenses as well as false-positive failures; the prototype repeats one task. | Retain failure mechanisms without implying every defense harms utility or every AP2 implementation fails. |
| Strengthen proposed control/accounting language | A check-then-retry instruction is weaker than a stable retry identifier; spending limits alone do not check item suitability. | Propose retry-safe identifiers and both choice/permission checks, without claiming their effectiveness was measured here. |
| Remove chronological and defensive repetition | Product milestones and earlier correction history belong mainly in the source record. | Keep meaningful availability, source limits, legal scope and version dates while shortening the main argument. |

The qualitative source-removal checks in Section 12 remain part of the protocol but are no longer repeated in the manuscript. No new references were added. The abstract now separates economic theory from restricted hotel-field evidence; the conclusion includes choice, permission, security/usefulness and correction work. The same 96-unit audit was revised and rebound to the new source hash.

### Subsequent presentation edits

The user requested deletion of the repeated review-type/date sentence at the start of Section 1.1, replacement of the email with a `veda.ng` link to `https://veda.ng`, and addition of the literal supplied author names `Author2` and `Author3`. The author block and PDF/HTML metadata now follow that list. The methods section starts directly with the search procedure. Source dates and language scope remain recorded here and in the evidence ledger; no research result or reference was changed.
