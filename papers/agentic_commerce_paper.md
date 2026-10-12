# A Review of Agentic Commerce

<div class="author-info">

<div class="author-entry">

**Vedang Ratan Vatsa**<br>
[veda.ng](https://veda.ng)

</div>

<div class="author-entry">

**Author2**

</div>

<div class="author-entry">

**Author3**

</div>

</div>

## Abstract

Artificial intelligence (AI) shopping agents can choose products and submit orders, but permission to pay does not establish that a purchase meets the buyer's needs. This narrative review compares 15 research works with two consumer survey releases, product and payment documents, and selected US and EU legal sources. Human experiments test reliance on advice and choice after seeing errors; neither measures willingness to delegate spending. Agent evaluations find failures involving product position, missing requirements, and the cost of checking details. They also show that partial-match scores and complete-task success can favor different models. Economic theory distinguishes cheaper price comparison from better product matching, while hotel-search evidence links ranking to clicks and bookings in a restricted sample. Security tests find both useful defenses and false alarms that block legitimate tasks. A comparison with ordinary shopping needs to count failed attempts, full charges, buyer time, delivery, and returns. The selected evidence does not supply a rate of successful real purchases or a population estimate of adoption.

_**Keywords**_: agentic commerce, AI shopping agents, online shopping, buying permission, payment standards, consumer protection

---

## 1. Introduction

Suppose a shopper asks an AI assistant to find a washing machine for a small kitchen. A low price is only one condition. The machine also needs to fit the space, arrive on time, and come with acceptable delivery and return terms. Payment can succeed even when the purchase fails to meet those needs.

This paper uses *agentic commerce* to mean shopping in which AI software uses tools to find products, prepare an order, or submit a purchase on a buyer's behalf. It compares advice, approval for each order, and permission given in advance. OpenAI's Instant Checkout launch and Amazon's Alexa for Shopping announcement describe different approval arrangements [1, 4].

The review asks what evidence supports an agent's ability to choose a suitable product, act within the buyer's permission, and deal with mistakes. Consumer studies, agent evaluations, and payment specifications each address part of that question. Comparing them exposes cases where an accepted recommendation, a high task score, or a valid payment leaves another part of the purchase unchecked.

### 1.1 Sources and method

The search used four OpenAlex queries, each limited to eight results, alongside known-study lookups, citations, arXiv, and author and institutional repositories. Queries included "agentic commerce consumer delegation trust" and "shopping agent prompt injection". The accompanying source log records all four queries, retrieved leads, versions, access failures, and passages used. This search does not support an exhaustive account of the field.

Selection sought distinct comparisons concerning consumer control, agent performance, search and ranking, or security and responsibility. A work needed enough accessible full text to inspect the claim used. Earlier studies were included when they tested a relevant mechanism; abstract-only leads and duplicate versions were excluded. Access affected selection, including the use of Ursu's dissertation rather than the unavailable final journal article [36]. The retained set contains 15 works, including experiments, benchmarks, field-data analysis, theory, two reviews, and legal scholarship.

Appraisal checked the task, comparison, outcome measure, source of variation, commercial ties, and limits of each claim. The records distinguish human behavior, simulated agent actions, field observations, model predictions, and legal arguments. Source selection and appraisal were AI-assisted and were not independently repeated. No common risk-of-bias score or pooled effect was calculated. The two reviews supply context; their underlying studies are not all independently inspected additions.

Commercial involvement varies across the research. ACES and AgentDojo have mixed university/company authorship, EComAgentBench's authors are affiliated with Shopee, and WebArena acknowledges an AWS AI gift as well as government support [17, 18, 34, 37]. Affiliations and declared support are recorded in the study matrix rather than treating every academic paper as industry-independent.

Company documents establish reported features or plans, not independently measured use or benefit. Legal claims are confined to the inspected provisions and jurisdictions. This review reports no new purchase experiment. Its proposed checks have not been tested here.

## 2. Related Work

De Bellis and Johar's review of autonomous shopping systems argues that saving time may not settle acceptance. Control, identity, meaningful activity, and social contact can matter; its evidence includes reanalyzed qualitative material [32]. Balaskas's later map reports 47 consumer-focused studies, with more coverage of advice, chatbots, and intentions than observed delegated checkout. It relies on single-researcher screening and a consumer-focused search [39]. The former explains reasons people may retain parts of shopping; the latter identifies how little its corpus directly observes payment delegation.

Technical evaluations answer a different question from studies of willingness to use advice. WebShop tests search and option selection in a simulated store; WebArena checks outcomes on controlled websites, including tasks beyond shopping [33, 34]. The Agentic e-Commerce Simulator, known as ACES, isolates product presentation. EComAgentBench tests needs spread across requests, profiles, and follow-up replies. Tool-Lab tests whether agents inspect product details when information has a stated cost [17, 18, 19]. Their different tasks can reveal different failures even when each paper calls its outcome success or accuracy.

Security research tests whether outside content or another user can redirect an agent [37, 38]. Legal scholarship asks how protections apply when people set an agent's goals before checkout [40]. These questions extend beyond whether a recommended product looks suitable. They concern who can cause an action, whose interests it serves, and how an error can be challenged.

## 3. Buying Permission and Current Services

Table 1 separates purchase approval from the amount of searching an agent performs. Advice is a comparison case in which the person still places the order. An agent may search without supervision yet require approval for each purchase; the categories are not successive stages of autonomy.

**Table 1. Forms of buying permission**

| Form | What the agent does | What the person decides |
|---|---|---|
| Advice | Finds and compares products | Chooses the item and places the order |
| Approval for each order | Prepares and helps submit an order | Approves that particular purchase |
| Advance permission | Acts later within agreed limits | Sets what it may buy, when, and at what cost |

OpenAI's September 2025 Instant Checkout launch allowed US users to make single-item purchases from US Etsy sellers after confirming the order, shipping, and payment details. The seller handled delivery, returns, and support [1]. The inspected help pages describe in-chat checkout for some eligible products and links to seller websites for others. Shopify guidance directs customers to the seller's store [2, 3]. Listing a product in ChatGPT does not by itself establish in-chat checkout support.

Amazon's May 2026 US rollout announcement for Alexa for Shopping describes both Auto Buy at a chosen price and actions that only send a notice or add items to a cart. It also describes Buy for Me purchases from other stores for eligible products [4]. These flows assign different decisions to the customer. A scheduled cart update is not a completed purchase.

Advance permission leaves decisions that a spending limit alone cannot settle. In an illustrative request to buy a laptop under $800, the person has not said whether a used model is acceptable. Size, condition, delivery date, seller, and return terms may all matter. Asking about a missing need is part of the buying task, even when the software already has permission to pay.

## 4. Commerce and Payment Standards

A protocol is an agreed way to exchange information. An application programming interface (API) lets one program request data or an action from another. Table 2 compares the main jobs of the reviewed protocols and related systems. The entries describe published designs and plans. They are not results from a test of every connection between them [6, 8, 9, 10, 12, 14].

**Table 2. Roles of the reviewed systems**

| System | Main role | Limit of that role |
|---|---|---|
| Agentic Commerce Protocol (ACP) | Connects assistants to seller checkout and order updates | Does not judge whether an item suits the buyer |
| Universal Commerce Protocol (UCP) | Describes catalog, cart, checkout, and order functions | Both parties still need matching functions and versions |
| Agent Payments Protocol (AP2) | Records and checks buying and payment permission | Valid permission does not prove product quality |
| Verifiable Intent | Records who gave permission and what action followed | The record does not decide legal responsibility |
| x402 | Lets software pay for an API or digital resource | Does not itself handle delivery or returns of physical goods |
| Personal Agent Protocol | Proposes shared access to business websites, APIs, and service agents | First specification was still planned in its October announcement |

ACP's checkout specification describes how to create, update, complete, and cancel a checkout session. The seller supplies the current items, shipping options, taxes, fees, and total. It also sends order updates. The specification calls for request checks and safe retries, including protection against carrying out the same request twice [12]. These requirements matter when a connection fails after payment but before the assistant receives a reply.

UCP describes how a business and a platform find the functions and versions they both support [6]. Compatibility depends on that match, not just the use of the UCP name. Its release history also includes a hotel-booking extension marked as a draft [5], so that entry does not establish hotel deployment.

AP2 calls its signed permission records *mandates*. Its current documentation distinguishes checkout records from payment records. An open mandate sets limits before the final order is known. A closed mandate records permission for a particular checkout or payment [8]. The UCP integration guide describes linking the payment to the agreed cart [13]. This link helps prevent permission for one order from being used for another.

AP2's version 0.2 announcement includes payments without the person present [7]. Mastercard's Verifiable Intent design links identity, permission, and action while limiting the transaction details shared [9]. These records can help reconstruct who approved an order and which limits applied, even when the person was absent at checkout.

x402 covers payment for digital resources such as API access [14]. If a shopping agent incurs an information fee on the buyer's behalf, that fee belongs in the buyer's costs even when no order follows. It is separate from the price of a physical item and its delivery or return charges.

The Personal Agent Protocol proposal covers customer-approved access across websites, APIs, and business agents. Its October announcement planned the first specification for later that month [10]. Riskified's Agent Identity Risk Intelligence announcement planned a limited beta for December 2026 [11]. Both belong among proposed or planned functions, not evidence of generally available services.

## 5. Consumer and Agent Evidence

### 5.1 Acceptance and control

The human experiments in Table 3 do not support a simple claim that people either trust or reject algorithms. Dietvorst and colleagues let participants observe forecasting performance before choosing a forecaster. Seeing errors reduced algorithm choice even when the model performed better than the human comparison [29]. Logg and colleagues held advice constant in key tests and changed whether it was described as human or algorithmic. Participants often gave algorithm-labeled advice more weight, although this preference weakened against their own judgment and among forecasting experts [30].

**Table 3. Human reliance studies and their different comparisons**

| Work | Comparison | Finding and boundary |
|---|---|---|
| Dietvorst et al., aversion [29] | Choose a forecaster after different exposure to performance | Seeing errors can reduce algorithm choice; forecasting rather than spending |
| Logg et al., appreciation [30] | Weight identical advice labeled human or algorithmic | Algorithm label can increase reliance; own judgment and expertise matter |
| Dietvorst et al., control [31] | Use a model with no, limited, or freer adjustment | Even limited adjustment can increase use; changes need not improve every decision |

The studies are not a like-for-like test of trust. Choosing a forecaster after observing mistakes differs from weighting identical advice attributed to another person or an algorithm. This comparison does not isolate which design difference explains the findings. It does show why neither result supplies a measure of willingness to delegate spending. Advice use, approval of one order, and permission for later purchases need separate outcomes [29, 30].

Follow-up experiments by Dietvorst and colleagues find greater model use when participants can change its forecast, even within a narrow range [31]. This is work by the same team, not an independent replication. More reliance on the model improved performance in the tested tasks, but that does not mean each manual adjustment was useful. For shopping, the result motivates testing editable limits and meaningful approval alongside purchase quality. It does not establish that adding a confirmation button produces better orders.

### 5.2 Consumer surveys

Table 4 reports two Riskified surveys separately. Both sampled people aged 18 to 64 who had bought online in the previous three months. The 2025 survey covered nine markets. The 2026 release covered only the US and UK [15, 16].

**Table 4. Survey results with sample details**

| Survey | Sample | Selected answers reported by Riskified |
|---|---|---|
| September-October 2025 | 5,400 people across nine markets | 73% used AI during shopping; 13% bought after an AI referral; 70% were at least somewhat comfortable with an agent buying for them |
| Q1 2026 edition, released April 27 | 2,000 people, with 1,000 each in the US and UK | 61.5% used AI for discovery or recommendations; 55.0% were uncomfortable with AI buying for them; 73.9% expected strong identity checks for transactions |

The first survey covered the US, UK, Brazil, Mexico, Singapore, Australia, China, the Netherlands, and UAE. The different country mix prevents a direct comparison over time. Full questions and response options are also unavailable for checking whether the measures match. The share reporting discomfort does not establish that every remaining respondent was comfortable [15, 16].

Within the 2026 survey, people reported both use of shopping advice and reluctance to hand over purchases. The published totals do not show exactly how those groups overlap. When asked who ought to be responsible for unauthorized or mistaken purchases, 50.8% chose the AI platform [16]. This measures respondents' views about responsibility, not their legal rights.

Riskified sells fraud-prevention services. Its releases provide sample summaries, but not the full questionnaires, weighting details, or individual responses needed for a deeper check. The results describe answers from those samples. They do not measure the share of purchases that agents completed. A repeat survey with the same country mix and questions could provide a firmer basis for studying changes over time.

### 5.3 Search and task completion

Table 5 compares five evaluations by what they test and how they judge a result. These distinctions matter more for this review than a ranking of their headline scores. Models, tasks, available actions, and scoring rules differ across the papers [17, 18, 19, 33, 34].

**Table 5. What shopping and browser evaluations measure**

| Evaluation | Task and comparison | Outcome and limit |
|---|---|---|
| WebShop [33] | Search products and select options; compare trained agents and baselines | Partial-match score and full success; simulated buy button |
| WebArena [34] | Complete tasks on controlled websites, including shopping | Resulting state or answer; not all tasks concern purchases |
| ACES [17] | Select from a store while presentation and product details change | Product choice and simple-task correctness; no paid sale |
| EComAgentBench [18] | Recover needs from a request, profile, and scripted replies | Target match or all requirements met; constructed buyers |
| Tool-Lab [19] | Inspect hidden coffee details under different goals and information costs | Search behavior and unit price; search fees are a separate cost |

WebShop checks product attributes, options, and price against crowdsourced requests. In its reported comparison, further training with task rewards improved the average partial-match score but slightly reduced full success relative to training on demonstrations alone [33]. This is a difference between getting more requirements right on average and satisfying a request completely. The small reported decrease does not establish that reward-based training generally harms full success. Neither measure includes delivery or returns, and the inspected 2023 results do not describe current models.

WebArena checks whether actions produce the intended website state or answer. Some answer checks use a model. It also includes tasks that cannot be completed, for which an appropriate response is to stop without claiming success [34]. This supports evaluating justified refusal as well as completion. Its sites are controlled, and its human comparison uses a selected sample on a subset of tasks. Comparing its success percentage directly with EComAgentBench could confuse different task difficulty, evaluation rules, and human involvement with model progress.

### 5.4 Product presentation and model changes

ACES uses eight product categories, with eight items in each. The main store display presents the products on one page. The authors change position, labels, prices, ratings, and review counts. They also test a text-only list of product data [17].

With the default buying prompts, agents responded to where an item appeared and to labels supplied by the platform. A sponsored label reduced selection when position and other features were held fixed. An "Overall Pick" label increased it. The effects varied by model, prompt, and interface. Product-order effects remained in the text-only list, so removing the visual page did not remove every ordering effect [17].

The December 2025 revision also reports better performance by newer models on simple tasks with one clear answer. At the same time, model updates changed which products and positions the agents favored. The results support checking choices again after an update rather than assuming earlier behavior continues [17].

ACES records intended choices in a test store, not sales. Its generic requests also omit much of the variation in real buyers' tastes. The sponsored-label finding has another limit. An advertisement may gain a product a position it could not otherwise obtain. A penalty for the label at a fixed position does not measure the total effect of paid placement [17].

### 5.5 Missing needs and information costs

EComAgentBench contains 662 valid tasks with needs spread across a request, a buyer profile, and scripted answers to questions. Each run permits up to 100 tool calls and 10 question-and-answer turns. Of seven models, Claude Opus 4.6 had the highest reported accuracy at 57.1%, where a correct answer matched the target product or met all requirements. A separate score for satisfaction of individual requirements ranked GPT-5.4 first [18]. The headline table gives point estimates without uncertainty intervals.

The study finds agents reading profile information without using it, or choosing before obtaining enough review evidence. It uses constructed buyer profiles, fixed replies, and an English-language catalog concentrated in electronics-related goods. Each task ends in one recommendation rather than a paid order [18]. These choices make it a test of finding and using requirements, not a measure of customer purchase reliability.

Scoring also needs qualification. An exact target match counts as correct without an AI judge. Non-target recommendations can pass if the judge finds that all requirements are met. The authors report cross-checks against exact matches and a manual audit of accepted non-target answers for one model. Those checks address some grading errors without establishing perfect judging for every model [18]. The metric-dependent ranking also appears in WebShop, giving a second reason to report partial and complete success separately [33].

Tool-Lab tests eight models on coffee choices. Product details sit behind tool calls, which are requests to another program for information. The researchers vary the stated cost of those calls and compare requests for the "best deal" with requests for the lowest price per ounce. Under costly access and vague goals, models often inspected fewer relevant details. Clearer goals generally preserved more of that search, with differences among models [19].

The main cost contrasts assign $10 or $50 to each information request; these are simulated charges, not observed shopper fees. The choice score uses product price per ounce and excludes those search charges. Less searching can be reasonable when another lookup is expensive. The study supports a claim about what agents inspect under stated costs and goals, not a general claim that shorter searches waste buyers' money [19].

## 6. Discussion

### 6.1 Product data, seller access, and advertising

Current prices, quantities, sizes, stock, and return terms give agents facts to compare. OpenAI's shopping guidance says it uses structured product data and other sources, while warning that prices may lag behind seller updates and that it does not show every available product [2]. A seller can therefore have a listed product without having complete or current details shown to a buyer.

ACES shows that product position and labels can affect choice [17]. If many buyers use an assistant with similar defaults, exposure could concentrate on a few products. Broader search could instead help smaller sellers appear. Distinguishing these possibilities requires exposure and sales records that account for prices, stock, and the products the assistant could access.

Bakos's economic model explains why cheaper search need not always lower prices. Reducing the cost of finding prices and reducing the cost of learning product features can affect competition differently. Better information about features can help buyers find a closer match without creating the same pressure on prices [35]. These are results under a model's assumptions about buyers, information, and sellers. They do not predict the net effect of today's assistants. Tool-Lab also changes the agent's stated information cost rather than observing prices set by competing sellers [19].

Ursu's dissertation uses hotel-search data with random variation in result order. Higher placement increased a hotel's chances of being clicked or booked within the sampled searches. Conditional on a click, the analysis did not detect a further position effect on conversion [36]. The released data exclude searches with no click and oversample bookings, so their rates do not describe all Expedia visitors. Random order helps separate position from relevance within this setting; it does not remove those sampling limits. Alongside ACES, the result supports checking both exposure and choice, without assuming that AI buyers respond like hotel shoppers [17, 36].

OpenAI's shopping and advertising documents state that product results and answers are separate from ads [2, 20]. Those policies do not establish how fees, endorsement labels, paid placement, or access rules affect what buyers see. Each can be tested separately while holding product details and position fixed where the comparison requires it.

Open standards may reduce the work needed to connect sellers to assistants. They do not decide which products an assistant searches or ranks first. For sellers, a connection that accepts orders and a fair chance to appear in recommendations are different concerns. The reviewed evidence supports testing both rather than treating protocol support as a measure of market access.

### 6.2 Preventing and correcting errors

A signed permission record helps check whether a payment matches an approved order or limit. It does not establish that the product suits the buyer. AP2's security document includes agents in its threat model and considers prompt injection, where outside content tries to redirect an agent's actions [21]. Riskified's October announcement makes a related distinction between an authorized agent and the trustworthiness of the account behind it [11].

AgentDojo reports completion without attack, completion under attack, and attacker success across 97 user tasks and 629 security cases. A security case pairs a user task with an attacker goal [37]. A low attacker-success rate can reflect an agent that cannot carry out either goal, so it is not enough to judge a defense by that rate alone.

In AgentDojo's GPT-4o defense tests, some defenses reduced attacker success while improving ordinary task completion. The attack detector was a counterexample, with false alarms that blocked valid tasks. Restricting available tools also helped in tested cases, but could fail when an allowed tool was enough to perform the attack [37]. These results call for testing useful completion and prevented harm together, under stated attacks and tool permissions.

Table 6 compares that broader benchmark with Whispers of Wealth, an AP2-style prototype using four Gemini-2.5-Flash agents and synthetic data. The prototype repeats one basketball-shoe request ten times under each of three conditions, including a baseline with no attack. Product attacks enter through merchant descriptions; credential attacks enter through a malicious user's request [38]. The study therefore tests different attacker capabilities as well as different outcomes.

**Table 6. Security evaluations and their limits**

| Evaluation | Setting | Result and limit |
|---|---|---|
| AgentDojo [37] | 97 user tasks and 629 task/attack cases | Some defenses reduce attacks and improve ordinary completion; false alarms can block valid tasks |
| Whispers, product attack [38] | One shoe request, 10 repeated attack runs | Attacker's product first in 10; six clear conflicts with user constraints |
| Whispers, credential attack [38] | Same request, 10 repeated attack runs | Synthetic cross-account exposure in two; not a customer fraud rate |

The 30 runs are repetitions of one task, not 30 independent shoppers. In some product-attack runs, overlap between the product and the request made harmful influence less clear, even though the product ranked first. The study did not break signatures or compromise real customer accounts. Its older mandate terms also differ from the current AP2 documents [8, 38]. The results show failure paths in that prototype. They do not establish that every AP2 implementation has the same flaws. The broader AgentDojo tasks and this small shopping test support separate checks of tool access and payment permission, without supplying a real-world fraud rate [37, 38].

Table 7 proposes checks based on these risks and the reviewed checkout specifications. These checks cover product choice, payment, and support after purchase. This review has not tested their effectiveness [12, 21, 37, 38].

**Table 7. Proposed checks for a complete purchase**

| Possible error | Check to test | Record to keep |
|---|---|---|
| Wrong item, size, or quantity | Compare the final order with the buyer's needs | Requested and selected details |
| Price or terms change | Refresh the order before payment | Approved total and terms, with a time |
| Permission is too broad | Limit amount, seller, time, and actions | Permission and later changes |
| A retry creates two orders | Reuse the same unique request identifier for retries | Request identifier and resulting order count |
| Outside text redirects the agent | Check product choice as well as limits enforced outside the model | Choice changes, rejected actions, and limit breaches |
| An agent requests another user's data | Check identity and access at the tool or service | Requesting account and access decision |
| A defense blocks a valid order | Test ordinary tasks as well as attacks | Legitimate completion and false rejections |
| A delivery or return fails | Provide status and a clear support route | Receipt, refund, and resolution records |

The buyer also needs a readable account of what happened. A useful receipt names the seller, item, total, and delivery and return terms. When the agent acts on advance permission, the record can link the order to the limits the buyer set. A long chat history alone may leave the buyer unable to tell which terms were approved.

### 6.3 Contracts, returns, and personal data

The US Electronic Signatures in Global and National Commerce Act, known as E-SIGN, protects certain contracts from being denied effect solely because electronic agents were involved. Section 7001(h) applies that protection only if the law treats the agent's action as an act of the person being bound. It does not itself make every agent action the user's action. Section 7001(b) preserves other rights and duties [22].

Washington's version of the Uniform Electronic Transactions Act gives a state-law example. It recognizes contracts formed through electronic agents, with terms governed by other applicable law [23]. Another section offers relief for some errors made by a person dealing with another party's electronic agent. Conditions include lack of an opportunity to prevent or correct the error, prompt notice, and rules about returning and not using what was received [24]. That is narrower than a right to reverse any unwanted AI purchase.

In the EU, the AI Act's transparency rules apply from August 2, 2026. Article 50 generally requires providers to tell people when they are interacting directly with AI, unless this is obvious in context, with stated exceptions. Some rules for specified high-risk uses have later dates [25, 26]. Disclosure that a service uses AI does not settle who pays for a mistaken order.

For covered online purchases of goods from a trader, EU consumers generally have 14 days after delivery to withdraw. Exceptions include perishable or customized goods, and separate rules apply to dated travel bookings and some digital content. Purchases from private individuals are not covered by this general withdrawal right [27].

The General Data Protection Regulation, or GDPR, gives rights to information, access, correction, and deletion of personal data, subject to conditions [28]. Records kept to resolve an order dispute still need limits on access and retention.

Busch argues for protection when a person sets an agent's goals and permissions. The article distinguishes manipulation of the agent by outside parties from manipulation by its provider [40]. These are legal reform arguments, not enacted duties. They motivate tests of whether people understand and can revise buying permissions before an order.

## 7. Open Questions and Limits

The missing comparison is a complete purchase under different forms of assistance. A study could assign comparable buying tasks to ordinary shopping, AI advice, per-order approval, and advance permission, while keeping needs, spending limits, and seller access comparable. It needs to record whether the item meets the request, whether every action stays within permission, what the buyer pays, how much time the buyer spends, and what happens through delivery and any return.

The accounting needs all attempts, including abandoned searches, duplicate orders, failed payments, and unresolved returns. Buyer-paid tool, verification, delivery, and return charges belong alongside the item price; time spent checking and correcting orders is a separate outcome. Tasks also need cases where asking a question or declining to buy is correct, as the information-gathering and unachievable-task designs in EComAgentBench and WebArena suggest [18, 34]. Repeated runs, changed model versions, and attacks can then test how stable those outcomes are.

The limited search covers accessible English-language sources. The human experiments concern forecasts, the field evidence concerns hotel search, and agent studies often use constructed tasks. Both shopping surveys come from one vendor; product and legal coverage favors large platforms and selected US and EU provisions. No studies were replicated, orders placed, or independent second appraisal performed. Real purchase reliability, repeat use, and market-wide price or seller effects remain unresolved.

## 8. Conclusion

An agent can stay within a spending limit and still choose the wrong product. ACES finds effects of product position and labels; EComAgentBench finds missed buyer requirements; Tool-Lab finds less checking under costly access and vague requests. Security tests add the need to measure both blocked attacks and completed user tasks. Payment records address permission, but do not establish that the item is suitable or that every tool action is safe.

The reviewed evidence does not yet show how reliably agents complete real purchases or how much time and money they save buyers. Advice experiments and shopping surveys also do not establish demand for delegated spending across the population. A comparison with ordinary shopping needs the full order record, including wrong items, duplicate orders, charges, refunds, and time spent correcting mistakes. An agent that places an order quickly may still leave the buyer with more work.

---

## References

1. OpenAI. "Buy it in ChatGPT: Instant Checkout and the Agentic Commerce Protocol." September 29, 2025. [openai.com/index/buy-it-in-chatgpt](https://openai.com/index/buy-it-in-chatgpt/) (accessed October 12, 2026).

2. OpenAI. "Shopping with ChatGPT Search." Help Center, current guidance. [help.openai.com: Shopping with ChatGPT Search](https://help.openai.com/en/articles/11128490-shopping-with-chatgpt-search) (accessed October 12, 2026).

3. OpenAI. "Shopping from Shopify merchants in ChatGPT." Help Center, current guidance. [help.openai.com: Shopify merchants](https://help.openai.com/en/articles/20001241-shopping-from-shopify-merchants-in-chatgpt) (accessed October 12, 2026).

4. Amazon. "Meet Alexa for Shopping, your personalized, agentic AI assistant on Amazon." May 13, 2026. [aboutamazon.com: Alexa for Shopping](https://www.aboutamazon.com/news/retail/alexa-for-shopping-ai-assistant) (accessed October 12, 2026).

5. UCP Authors. "Announcements." Releases from January to September 2026. [ucp.dev/documentation/announcements](https://ucp.dev/documentation/announcements/) (accessed October 12, 2026).

6. UCP Authors. "Universal Commerce Protocol (UCP) Official Specification." Version 2026-08-25. [ucp.dev: versioned specification](https://ucp.dev/2026-08-25/specification/overview/) (accessed October 12, 2026).

7. S. Parikh. "We're donating Agent Payments Protocol to the FIDO Alliance to support the future of secure, agentic payments." Google, April 28, 2026. [blog.google: AP2 and FIDO](https://blog.google/products-and-platforms/platforms/google-pay/agent-payments-protocol-fido-alliance/) (accessed October 12, 2026).

8. AP2 Authors. "Agent Payments Protocol (AP2)." Current documentation. [ap2-protocol.org](https://ap2-protocol.org/) (accessed October 12, 2026).

9. P. Fourez. "When AI starts buying for you, trust becomes the product." Mastercard, March 5, 2026. [mastercard.com: Verifiable Intent](https://www.mastercard.com/global/en/news-and-trends/stories/2026/verifiable-intent.html) (accessed October 12, 2026).

10. B. Taylor and C. Bavor. "Introducing Personal Agent Protocol." Sierra, October 6, 2026. [sierra.ai/blog/introducing-personal-agent-protocol](https://sierra.ai/blog/introducing-personal-agent-protocol) (accessed October 12, 2026).

11. Riskified. "Riskified Launches Agent Identity Risk Intelligence: Know Who Is Behind AI Personal Assistants like Muse at Checkout and in Customer Service." October 8, 2026. [riskified.com: Agent Identity Risk Intelligence](https://www.riskified.com/press/agent-identity-risk-intelligence/) (accessed October 12, 2026).

12. OpenAI. "Agentic Checkout Spec." Current developer documentation. [developers.openai.com/commerce/specs/checkout.md](https://developers.openai.com/commerce/specs/checkout.md) (accessed October 12, 2026).

13. UCP Authors. "UCP and AP2." Current integration guide. [ucp.dev/documentation/ucp-and-ap2](https://ucp.dev/documentation/ucp-and-ap2/) (accessed October 12, 2026).

14. Coinbase Developer Platform. "x402 Overview." Current documentation. [docs.cdp.coinbase.com/x402/welcome](https://docs.cdp.coinbase.com/x402/welcome) (accessed October 12, 2026).

15. Riskified. "Global Study: 73% of Shoppers Using AI in Shopping Journey - But Merchants Face New Agentic Commerce Risks." October 20, 2025. [riskified.com: 2025 shopper survey](https://www.riskified.com/press/global-study-73-of-shoppers-using-ai-in-shopping-journey-but-merchants-face-new-agentic-commerce-risks/) (accessed October 12, 2026).

16. Riskified. "Riskified Study Finds Consumers Aren't Ready to Hand Over Control as AI Transforms Shopping, with Over Half Afraid of Online Fraud." April 27, 2026. [riskified.com: Agentic Commerce Pulse](https://www.riskified.com/press/riskified-agentic-commerce-pulse/) (accessed October 12, 2026).

17. A. Allouah, O. Besbes, J. D. Figueroa, Y. Kanoria, and A. Kumar. "What Is Your AI Agent Buying? Evaluation, Biases, Model Dependence, & Emerging Implications for Agentic E-Commerce." arXiv preprint, version 3, December 17, 2025. [arxiv.org/abs/2508.02630v3](https://arxiv.org/abs/2508.02630v3).

18. Z. Du, T. Li, and H. Zhang. "EComAgentBench: Benchmarking Shopping Agents on Long-Horizon Tasks with Distributed Hidden Intent." arXiv, version 3, September 2, 2026. [arxiv.org/abs/2606.17698v3](https://arxiv.org/abs/2606.17698v3).

19. D. Wadi and Y. Ma. "Shopping by algorithm: How agentic AI deploys human heuristics as a surrogate consumer." arXiv preprint, September 23, 2026. [arxiv.org/abs/2609.28372v1](https://arxiv.org/abs/2609.28372v1).

20. OpenAI. "Building advertising for the way people use AI." October 5, 2026. [openai.com: advertising update](https://openai.com/index/new-chatgpt-ads-format-and-measurement/) (accessed October 12, 2026).

21. AP2 Authors. "Security and Privacy Considerations." Current documentation. [ap2-protocol.org: security and privacy](https://ap2-protocol.org/ap2/security_and_privacy_considerations/) (accessed October 12, 2026).

22. United States. "Electronic Signatures in Global and National Commerce Act." 15 USC 7001, especially subsections (b) and (h), enacted 2000. Statutory text reproduced by Cornell Legal Information Institute. [law.cornell.edu/uscode/text/15/7001](https://www.law.cornell.edu/uscode/text/15/7001) (accessed October 12, 2026).

23. Washington State Legislature. "Automated transaction." RCW 1.80.130, enacted 2020. [app.leg.wa.gov: RCW 1.80.130](https://app.leg.wa.gov/RCW/default.aspx?cite=1.80.130) (accessed October 12, 2026).

24. Washington State Legislature. "Effect of change or error." RCW 1.80.090, enacted 2020. [app.leg.wa.gov: RCW 1.80.090](https://app.leg.wa.gov/RCW/default.aspx?cite=1.80.090) (accessed October 12, 2026).

25. European Commission. "AI Act." Application timeline and amendments, updated August 3, 2026. [digital-strategy.ec.europa.eu: AI Act](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) (accessed October 12, 2026).

26. European Commission, AI Act Service Desk. "Article 50: Transparency obligations for providers and deployers of certain AI systems." Consolidated-text basis July 27, 2026. [ai-act-service-desk.ec.europa.eu: Article 50](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50) (accessed October 12, 2026).

27. European Union, Your Europe. "Returns." Current consumer guidance. [europa.eu: Returns](https://europa.eu/youreurope/citizens/consumers/shopping/returns/index_en.htm) (accessed October 12, 2026).

28. European Data Protection Board. "Respect individuals' rights." Data protection guide for small business, current guidance. [edpb.europa.eu: individual rights](https://www.edpb.europa.eu/sme/be-compliant/respect-individuals-rights_en) (accessed October 12, 2026).

29. B. J. Dietvorst, J. P. Simmons, and C. Massey. "Algorithm Aversion: People Erroneously Avoid Algorithms After Seeing Them Err." Journal of Experimental Psychology: General, 144(1), 114-126, 2015. Penn-hosted early author copy inspected. [doi.org/10.1037/xge0000033](https://doi.org/10.1037/xge0000033).

30. J. M. Logg, J. A. Minson, and D. A. Moore. "Algorithm Appreciation: People Prefer Algorithmic to Human Judgment." Organizational Behavior and Human Decision Processes, 151, 90-103, 2019. [doi.org/10.1016/j.obhdp.2018.12.005](https://doi.org/10.1016/j.obhdp.2018.12.005).

31. B. J. Dietvorst, J. P. Simmons, and C. Massey. "Overcoming Algorithm Aversion: People Will Use Imperfect Algorithms If They Can (Even Slightly) Modify Them." Management Science, 64(3), 1155-1170, 2018; first online 2016. Pre-final author manuscript inspected. [doi.org/10.1287/mnsc.2016.2643](https://doi.org/10.1287/mnsc.2016.2643).

32. E. de Bellis and G. V. Johar. "Autonomous Shopping Systems: Identifying and Overcoming Barriers to Consumer Adoption." Journal of Retailing, 96(1), 74-87, 2020. [doi.org/10.1016/j.jretai.2019.12.004](https://doi.org/10.1016/j.jretai.2019.12.004).

33. S. Yao, H. Chen, J. Yang, and K. Narasimhan. "WebShop: Towards Scalable Real-World Web Interaction with Grounded Language Agents." First released 2022; inspected arXiv version 4, February 8, 2023. [arxiv.org/abs/2207.01206v4](https://arxiv.org/abs/2207.01206v4).

34. S. Zhou et al. "WebArena: A Realistic Web Environment for Building Autonomous Agents." First released 2023; inspected arXiv version 4, April 16, 2024. [arxiv.org/abs/2307.13854v4](https://arxiv.org/abs/2307.13854v4).

35. J. Y. Bakos. "Reducing Buyer Search Costs: Implications for Electronic Marketplaces." Management Science, 43(12), 1676-1692, 1997. [doi.org/10.1287/mnsc.43.12.1676](https://doi.org/10.1287/mnsc.43.12.1676).

36. R. M. Ursu. "The Power of Rankings: Quantifying the Effect of Rankings on Online Consumer Search and Purchase Decisions." PhD dissertation, University of Chicago, June 2016. [knowledge.uchicago.edu: dissertation](https://knowledge.uchicago.edu/records/w2hvk-p7722/files/Ursu_uchicago_0330D_13283.pdf?download=1).

37. E. Debenedetti, J. Zhang, M. Balunovic, L. Beurer-Kellner, M. Fischer, and F. Tramer. "AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents." arXiv version 3, November 24, 2024. [arxiv.org/abs/2406.13352v3](https://arxiv.org/abs/2406.13352v3).

38. T. Debi, W. Zhu, and P. S. Gupta. "Whispers of Wealth: Red-Teaming Google's Agent Payments Protocol via Prompt Injection." arXiv version 2, May 18, 2026; rendered document title uses "A Systematic Red-Teaming Study of the Agent Payments Protocol (AP2)." [arxiv.org/abs/2601.22569v2](https://arxiv.org/abs/2601.22569v2).

39. S. Balaskas. "From Recommendations to Delegation: A Systematic Review Mapping Agentic AI in E-Commerce and Its Consumer Effects." Information, 17(3), 222, February 25, 2026. [doi.org/10.3390/info17030222](https://doi.org/10.3390/info17030222).

40. C. Busch. "Consumer Law for AI Agents." German Law Journal, 26(7), 1367-1382; issue dated October 2025, published online April 24, 2026. [doi.org/10.1017/glj.2026.10188](https://doi.org/10.1017/glj.2026.10188).
