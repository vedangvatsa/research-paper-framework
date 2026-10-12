# Expanded academic review record

Review date: October 13, 2026 (local time). Retrieval manifests use UTC timestamps. This is a targeted narrative review, not a systematic search or an independent replication.

## Search and selection

The preceding version had three direct shopping-agent papers and two vendor surveys. The expansion looked for research on human reliance and control, task completion, search/ranking economics, and agent security/responsibility. It retained twelve additional research works. Together with references 17-19, the academic discussion now uses fifteen works. Reviews, a dissertation, theory, legal analysis, and experiments are identified separately; fifteen works does not mean fifteen independent experiments.

Searches attempted on October 13:

| Route | Query or lookup | Result and use |
|---|---|---|
| DuckDuckGo | `algorithm aversion Dietvorst Simmons Massey 2015 pdf`; `algorithm appreciation Logg Minson Moore 2019 pdf`; `Haubl Trifts 2000 interactive decision aids online shopping pdf`; `Ursu 2018 power rankings consumer search purchase decisions pdf`; `agentic commerce consumer delegation trust university experiment 2026 paper` | CAPTCHA responses. No results treated as evidence. |
| OpenAlex search | `agentic commerce consumer delegation trust` | Located Balaskas's review, de Bellis/Johar via related search, and other possible studies. Search response saved. |
| OpenAlex search | `AI shopping agents consumer control experiment` | Located consumer-law scholarship and autonomous-shopping research. Search response saved. |
| OpenAlex search | `algorithmic recommendation agent consumer experiment` | Leads on recommendation research; not added solely because a title appeared. |
| OpenAlex search | `shopping agent prompt injection` | Located Whispers of Wealth and later security papers. DOI/arXiv versions of the same work deduplicated. |
| OpenAlex DOI lookups | Dietvorst aversion/control; Logg appreciation; Castelo; Longoni/Cian; Haubl/Trifts; Ursu; Bakos; de Bellis/Johar; consumer delegation; Balaskas | Used for discovery, not as final authority on dates or full-text identity. Candidate metadata saved. |
| Crossref | `10.1037/xge0000033`, `10.1287/mnsc.2016.2643`, `10.3390/info17030222` | Verified journal citation dates and metadata. Distinguished online/author versions from issue years. |
| Author and institutional pages | Penn, Julia Minson's publication list, St Gallen, NYU/Stern, Chicago, Cambridge, arXiv, Princeton WebShop page | Followed public full-text links, read the relevant methods/results, and checked author/version identity. |
| Bing RSS | `"Algorithm Appreciation" pdf` | Irrelevant results; not used as evidence. |

The search retained works that added a distinct comparison or mechanism and provided enough accessible text to inspect the used claim. Each of the four saved OpenAlex discovery queries requested at most eight results; known-study lookups and source links supplied further leads. This limit and the lack of independent duplicate appraisal are now explicit in the manuscript. The same study in a review, preprint, and journal record was not counted again. Search ranking and citation count were not quality measures. Source access affected selection and is a limit of the review.

## Study-level extraction and appraisal

### Earlier research retained as references 17-19

These papers retain their detailed claim records and source files in `../sources/checked-2026-10-12/` and `../../agentic_commerce_paper_sources.md`.

| Work and inspected version | Author setting | Design, finding, and limit used |
|---|---|---|
| 17. ACES, arXiv v3, December 17, 2025 | MyCustomAI, Columbia, and Yale; mixed company/university team. Funding not established by this review. | Controlled eight-category/eight-item store; presentation manipulations and model comparisons. Position/label effects under tested prompts, not real sales or measured market concentration. |
| 18. EComAgentBench, arXiv v3, September 2, 2026 | Shopee; company-only author block. | Constructed requests/profiles/clarification and target/rubric checks; 662 tasks, seven models, best 57.1%. Synthetic needs and some AI judging, not live-order reliability. |
| 19. Tool-Lab, arXiv v1, September 23, 2026 | McGill University. Funding not established by this review. | Eight models, coffee attributes, goal specificity and stated information costs. Search omissions vary by model; unit-price outcome excludes search fees, and simulated charges are not observed fees. |

### 29. Dietvorst, Simmons, and Massey, Algorithm Aversion

- **Publication:** Journal of Experimental Psychology: General 144(1), 114-126, 2015, DOI `10.1037/xge0000033`. The inspected Penn-hosted early copy has a 2014 prepublication header; the final citation year was checked with Crossref. This is one work.
- **Author setting/funding:** University of Pennsylvania. The copy acknowledges the Wharton Behavioral Laboratory and Wharton Risk Center Ackoff Doctoral Student Fellowship. No vendor employment appears in its author block.
- **Design:** Five incentivized forecasting experiments. Participants saw a model's forecasts, human forecasts, both, or neither, then chose a forecaster for later bonus-linked forecasts. Tasks included student outcomes and state rankings; samples included laboratory participants and MTurk users.
- **Finding used:** Seeing an imperfect algorithm perform could reduce willingness to choose it even when it outperformed the human comparison. This is a response to performance feedback, not evidence of general rejection of all algorithms.
- **Limits:** Forecasting tasks, selected participants, and a forced choice of forecaster. No shopping agent or real purchase permission was tested. Do not sum participants across related conditions as an adoption estimate.
- **Inspection:** Methods and Results sections, study tables, general discussion, first-page affiliations/acknowledgments. Full text `dietvorst-aversion.pdf`.

### 30. Logg, Minson, and Moore, Algorithm Appreciation

- **Publication:** Organizational Behavior and Human Decision Processes 151, 90-103, 2019, DOI `10.1016/j.obhdp.2018.12.005`. Final journal PDF from coauthor Julia Minson's publication page, not the different 2017 single-author Harvard working paper incorrectly linked in some discovery metadata.
- **Author setting:** Harvard Kennedy School and UC Berkeley. The paper reports preregistrations/materials for most experiments. Its author block is academic; this review does not infer complete financial independence from that fact.
- **Design:** Numeric estimates and forecasts. In key tests, identical advice was labeled as coming from people or an algorithm. Other tests compared one's own judgment with an external source and compared laypeople with forecasting professionals.
- **Finding used:** Participants often gave more weight to algorithm-labeled advice. This preference was weaker when compared with their own judgment and among the expert sample.
- **Counterpoint:** Advice quality was held fixed in key tests. This differs from observing errors and then choosing a forecaster, so it does not simply refute reference 29. It also does not establish willingness to authorize spending.
- **Inspection:** Sections 1.2-1.4, experimental methods/results, Sections 5.2-6.3; `logg-appreciation.pdf`.

### 31. Dietvorst, Simmons, and Massey, Overcoming Algorithm Aversion

- **Publication:** Management Science 64(3), 1155-1170, 2018, DOI `10.1287/mnsc.2016.2643`. Penn repository supplies a pre-final author manuscript associated with the 2016 online version. Crossref gives the 2018 issue date. The inspected version is disclosed rather than silently relabeled.
- **Author setting:** Chicago Booth and Wharton. This is follow-up work by the same authors as reference 29, not an independent replication by a separate team.
- **Design:** Three incentivized forecasting studies allowing no changes, limited changes, or freer adjustment of a model's prediction. Random assignment is described; lab and MTurk samples were used.
- **Finding used:** Even restricted adjustment increased willingness to use the model. Greater total reliance improved performance relative to refusing it in these tasks; wider freedom to change output was not necessary for the uptake effect.
- **Limits:** Choice, completion, and attrition denominators vary within the manuscript; no aggregate participant count or pooled effect is used. Acceptance/control and actual decision accuracy remain different outcomes. No claim that manual changes improve every algorithmic decision.
- **Inspection:** Study 1 methods/results, Study 2 methods/results, Study 3 and general discussion; `dietvorst-control.pdf`.

### 32. de Bellis and Johar, Autonomous Shopping Systems

- **Publication:** Journal of Retailing 96(1), 74-87, 2020, DOI `10.1016/j.jretai.2019.12.004`; journal PDF from St Gallen.
- **Author setting:** University of St Gallen and Columbia Business School.
- **Design/type:** Cross-disciplinary review that also reanalyzes earlier qualitative material. It is not a new randomized test of autonomous checkout. The underlying interviews/focus groups are not counted as a separate new dataset in this review.
- **Finding/argument used:** Saving time need not settle adoption because control, identity, meaningful activity, and social contact can matter. Distinguishes recommendations from delegating decisions and tasks.
- **Limits:** Conceptual proposals and reused qualitative evidence, preceding present LLM shopping systems. The paper's broad cultural and market-size claims are not imported.
- **Inspection:** Definitions, barriers, qualitative-data discussion, recommendations and limits; `debellis-autonomous.pdf`.

### 33. Yao, Chen, Yang, and Narasimhan, WebShop

- **Version:** First released 2022; inspected arXiv v4, February 8, 2023, which corrects a choice-oracle result.
- **Author setting:** Princeton University, verified in the paper/project page. University-led benchmark research, not a retailer's product announcement.
- **Design:** Simulated store using scraped product information and crowdsourced instructions. Agents search, open pages, select product options, and press a simulated buy button. Programmed scoring checks attributes/type/options/price.
- **Finding used:** Search and option selection are separate failure points. Partial-match score and full success are distinct; reported RL fine-tuning improved average score while slightly lowering full success relative to its imitation baseline.
- **Limits:** Fixed catalog and reward rules; human and model interfaces differ; expert human comparison selected stronger workers. Original baseline scores describe that dated experiment, not current agent performance. Simulated buy is not payment/fulfillment.
- **Inspection:** Sections 3-5 and results/trajectory analysis; `webshop.html` and extracted text.

### 34. Zhou et al., WebArena

- **Version:** First released 2023; inspected arXiv v4, April 16, 2024.
- **Author setting/funding:** Carnegie Mellon University authors; acknowledges Air Force Research Laboratory support and a gift from AWS AI. University-led does not mean free of industry support.
- **Design:** Self-hosted shopping, forum, development, and content-management sites. Browser actions are checked against intended outcomes; some answer checks use a model. Includes unachievable tasks for which an appropriate response is no answer/action.
- **Finding used:** Tests need to verify resulting state, not merely fluent responses or completed-looking action sequences. Tasks requiring a stop/no-answer belong in the evaluation.
- **Limits:** Broad web tasks, not all shopping; static controlled sites; selected graduate-student human sample on a subset, not the same full task denominator. No direct comparison of its success percentage to EComAgentBench.
- **Inspection:** Sections 2-4, evaluation functions, unachievable tasks, human protocol and acknowledgments; `webarena.html`.

### 35. Bakos, Reducing Buyer Search Costs

- **Publication:** Management Science 43(12), 1676-1692, 1997, DOI `10.1287/mnsc.43.12.1676`; author copy at NYU.
- **Author setting:** NYU Stern; theoretical economics/information-systems work.
- **Design/type:** Models of buyer search and differentiated products, not observations of AI buyers. Assumptions include the modeled distribution of preferences, information costs, and seller behavior.
- **Argument used:** Lowering the cost of finding prices and lowering the cost of learning product features can have different competitive effects. Cheaper matching alone need not produce lower prices.
- **Limits:** Conditional model results, not a prediction that all AI markets become more competitive or more concentrated. No equations or numerical forecasts imported into this paper.
- **Inspection:** Sections 1-3 and 5.1-5.3; `bakos-search.pdf`.

### 36. Ursu, The Power of Rankings

- **Inspected version:** University of Chicago PhD dissertation, June 2016. Related research appeared in Marketing Science in 2018, but the publisher full text was inaccessible. The reference therefore cites the inspected dissertation, not an uninspected final article.
- **Author setting/funding/data:** University of Chicago; university fellowships and Marketing Science Institute dissertation support acknowledged. Data from Expedia, Kaggle, and Wharton Customer Analytics Initiative acknowledged.
- **Design:** Analysis of field data containing random variation in hotel order, plus a structural search model. The randomized-order analysis separates position from the quality/relevance that ordinarily affects ranking.
- **Finding used:** Higher placement affected clicks and overall bookings; conditional on a click, the analysis did not detect a further position effect on conversion. This does not mean ranking cannot change sales.
- **Limits:** Human hotel search on a particular platform. Section 4.3 states that no-click searches were omitted and bookings oversampled, limiting population rates and direct comparisons between ranking regimes. Conditional-choice analysis and modeled welfare effects have additional assumptions. The dissertation's dollar effects and simulated welfare changes are not used.
- **Inspection:** Data description/limits, Chapter 5, Chapter 11, acknowledgments; `ursu-rankings.pdf`.

### 37. Debenedetti et al., AgentDojo

- **Version:** Inspected arXiv v3, November 24, 2024.
- **Author setting/funding:** ETH Zurich and Invariant Labs; mixed university/company authorship. Acknowledges armasuisse and SNSF support. Not presented as fully independent of the agent-security industry.
- **Design:** Stateful test environments covering office tools, travel and banking, with separate user goals and attacker goals. It measures legitimate task completion, task completion under attack, and completion of the attacker's goal.
- **Finding used:** A low attack-success rate can reflect a weak agent that cannot execute either task. In the GPT-4o defense comparisons, some defenses improve benign completion and reduce attacker success, while the detector's false positives reduce legitimate performance. Limiting tools has boundaries when allowed tools can still perform the harmful act. The benchmark contains 97 user tasks and 629 security cases pairing user tasks with attacker goals, not 629 independent shoppers.
- **Limits:** Dummy data, controlled tasks and tested model/attack versions; no real-world fraud incidence. Different headline rates use different settings, so no single aggregate attack percentage is imported.
- **Inspection:** Sections 3-5, defense limitations, data card and acknowledgments; `agentdojo.html`.

### 38. Debi, Zhu, and Gupta, Whispers of Wealth

- **Version:** Inspected arXiv v2, May 18, 2026. The arXiv record uses 'Red-Teaming Google's Agent Payments Protocol via Prompt Injection'; the rendered v2 document title is 'A Systematic Red-Teaming Study of the Agent Payments Protocol (AP2)'. This title difference is recorded; the bibliography uses the arXiv record title and pins v2.
- **Author setting:** University of Georgia and Kennesaw State University. No commercial affiliation in the author block; lack of a funding statement is not proof of no support.
- **Design:** An isolated, synthetic, four-agent prototype using Gemini-2.5-Flash and Google ADK. One fixed shoe-shopping query. Ten runs each for baseline, product-description attack, and credential attack.
- **Finding used:** Attacker's product ranked first in ten attack runs, with clear user-constraint conflicts in six. In the other four, partial semantic overlap makes attribution less clear. Cross-account synthetic-data exposure occurred in two of ten credential-attack runs. The work did not break cryptographic signatures.
- **Limits:** Thirty repeated runs of one task, not thirty independent shoppers. Its original Intent/Cart/Payment mandate terminology differs from current AP2 documentation. App-level prototype failures do not establish that every conforming AP2 implementation has the flaw or that real cards/accounts were compromised.
- **Inspection:** Sections III-VI; `whispers-ap2.html`.

### 39. Balaskas, From Recommendations to Delegation

- **Publication:** Information 17(3), 222, February 25, 2026, DOI `10.3390/info17030222`. Publisher-hosted PDF retrieved from its resource host after main-site access failures.
- **Author setting/funding:** University of Patras. Declares no external funding. Single-author review, with its coding limitations stated.
- **Design/type:** Systematic evidence map of consumer-focused peer-reviewed literature. Scopus/Web of Science searches last run December 20, 2025, followed by supplementary searches/citation chasing. Reports 47 included studies, single-researcher screening/coding, no pooled effects, and no formal cross-design risk-of-bias tool.
- **Finding used:** Within its consumer-focused corpus, recommendations, chatbot interactions, intentions, and scenarios are more common than observed delegated checkout/payment.
- **Limits:** Scope excludes much practitioner and preprint/technical literature. The review's 47 studies were not all independently read here and are not added to this review's fifteen-work count. It supports positioning/coverage, not a new measured consumer effect.
- **Inspection:** Sections 3.1-3.4, results summary, limitations and declarations; `literature-review.pdf`.

### 40. Busch, Consumer Law for AI Agents

- **Publication:** German Law Journal 26(7), 1367-1382. Publisher lists an October 2025 issue but online publication April 24, 2026. Both are recorded instead of inventing a single consistent date.
- **Author setting/funding:** Osnabrück University. Declares no competing interests. Acknowledgments identify a VolkswagenStiftung-funded project; the separate funding statement says no specific funding declared for the article. Both disclosures are retained.
- **Design/type:** Legal analysis and reform argument, not a consumer experiment or enacted law.
- **Argument used:** Protect people when they set an agent's goals and permissions, not only at checkout; distinguish manipulation of the agent from manipulation by its provider. Model rules and proposed duties are not treated as binding law.
- **Limits:** EU-focused scholarship. Does not settle all liability cases or prove an economic effect.
- **Inspection:** Sections C-D, conclusion, funding and interests; `busch-consumer-law.pdf`.

## Excluded or unresolved leads

- Haubl and Trifts (2000): relevant earlier shopping-aid experiment, but the discovered institutional record had no original file and the publisher blocked retrieval. Not included on an abstract-only basis.
- The 2023 consumer-delegation article, DOI `10.1002/cb.2234`: publisher PDF blocked and no inspected full-text alternative obtained. Not used for a detailed claim.
- Castelo (2019) and Longoni/Cian: useful related leads, but not added after metadata alone. OpenAlex also conflated the Castelo article with a later book chapter; metadata was not trusted blindly.
- Additional commercial reports, survey compilations, and overlapping arXiv/DOI versions were not counted as new academic evidence.
- The Harvard record initially suggested for Logg was a different 2017 working paper. Replaced with the actual 2019 journal PDF from the coauthor's site.
- The final 2018 Ursu article was inaccessible. The 2016 dissertation is cited explicitly, with no claim that it is an independently inspected journal version.

## Synthesis decisions

1. Human distrust and appreciation results differ in feedback, comparison source, and task. They are conditional findings, not a binary vote on whether people trust AI.
2. Control can improve uptake while not making every manual adjustment accurate. Acceptance and purchase quality need separate outcomes.
3. Shopping and browser tests score different actions and definitions of correctness. Their percentages are not a time trend or one reliability rate.
4. Lower search costs can improve matching while changing competition differently depending on what information becomes easier to obtain. AI market outcomes remain unmeasured here.
5. Secure payment records, reliable choice, and secure tool access are different requirements. Both attack success and legitimate completion need reporting.
6. The expanded paper remains a narrative review with documented selection and access limits. It does not reproduce the cited experiments, claim a systematic census, or certify scientific validity from publication status.
