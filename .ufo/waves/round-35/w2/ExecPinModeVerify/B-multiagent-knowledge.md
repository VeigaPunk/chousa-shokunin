Skip to content
ChatGPT
New chat
Scheduled
Library
Plugins
Explore
Pinned
PC Build Components
Open Bug Bounties Compilation
Clean Omarchy Install Guide
Explain DSH Integration
L1 T3
Clip Big Hero 6
Projects
Recents
Research agent knowledge bases
Generate Skills and Memory
Propose Skills and Memory
Review recurring errors
Review recurring errors
Review agent learnings
Propose Skills Memory Delta
Propose Skills Memory
Review recurring errors
Propose Skills and Memory
Loading chats
jpveiga
Pro
Research agent knowledge bases
·
Work
Share
You said:
Deep research: multi-agent LLM systems where agents are persistent domain specialists that maintain and iteratively rewrite their own long-term knowledge bases (voyager skill libraries, generative agents memory streams, self-improving agents, expert-LLM rosters, mixture-of-experts lifelong learning). I'm building a 'shokunin' fleet: each agent owns one domain, writes its own SKILL/corpus files each round, promotes apprentice->artisan->self-iterating. What does the literature say about (1) knowledge-base self-rewrite failure modes (drift, forgetting, hallucinated citations), (2) when to split a domain into a new specialist vs expand an existing one, (3) credit assignment for 'which agent gets better'. Cite papers.
Worked for 1m 36s
Working for 2m 8s
ChatGPT said:

I’ll trace the literature across persistent memory, self-improving agents, specialist routing, and multi-agent credit assignment, then map the findings to your shokunin fleet.

Searched the web

ChatGPT said:
Response started

The closest match is newer work on evolving external skills and playbooks. A key finding is that rewriting the entire knowledge base can erase useful detail; another is that team success does not establish which specialist actually improved. I’m checking the evidence for domain splitting and counterfactual evaluation separately.

Analyzing AI Citation Errors and Persistent Memory

arxiv.org

ChatGPT said:

The literature supports the core of your shokunin fleet: persistent specialists whose capabilities improve through external memory, reusable procedures, and evaluated revisions. It offers much weaker support for unrestricted whole-corpus rewriting or automatic creation of specialists based on topic novelty alone.

The strongest design implication is to make knowledge changes—not agent self-assessments—the unit of evaluation. Track five axes separately: task competence, retention, evidence fidelity, cross-domain transfer, and operating cost.

Below, I distinguish published findings from my proposed engineering rules. Some of the closest architectural matches are recent preprints; their benchmark results do not establish indefinite, reliable self-improvement.

Your architecture sits at the intersection of several distinct research lines.

Work	What persists or improves	Relevance to shokunin
Voyager, Wang et al., 2023	An expanding library of executable skills, developed using environment feedback	Strong precedent for accumulating reusable procedures. Its verified code library differs substantially from freely rewritten factual prose.
Generative Agents, Park et al., 2023	Experience streams and higher-level reflections retrieved for planning	Precedent for persistent identity and memory. Its central evaluation concerns believable behavior, rather than increasing domain expertise.
Reflexion, Shinn et al., 2023	Verbal reflections stored across trials	Precedent for learning from task feedback without changing model weights.
Dynamic Cheatsheet, Suzgun et al., 2025; ACE, Zhang et al., 2025	Evolving strategies and domain playbooks	Closest lineage for agents maintaining their own instructions and knowledge files.
Memento-Skills, Zhou et al., 2026	Structured Markdown skills, a trainable skill router, and read–write improvement	An especially close match to your SKILL idea: persistent external skills are revised and expanded through experience.
LEGOMem, Han et al., 2025	Procedural memories allocated to orchestrator and worker agents	Directly relevant to deciding which specialist should own which learned procedure.

Sources: Voyager and Generative Agents; Reflexion; Dynamic Cheatsheet and ACE; Memento-Skills; LEGOMem. 
arxiv.org
+6

A useful distinction: weight-space mixture-of-experts, ensembles of LLM calls, and persistent memory-owning agents are different systems. Results about neural expert expansion can inspire your fleet’s design, but they do not directly validate rules for splitting Markdown corpora.

(1) Self-rewriting knowledge bases: the most important failure is losing the distinction between observation, interpretation, and established knowledge.

Destructive compression has direct experimental evidence. ACE identifies “brevity bias” and “context collapse” in iterative context rewriting. In one AppWorld case, a rewrite reduced accumulated context from 18,282 tokens to 122; accuracy fell from 66.7 to 57.1, below the 63.7 no-adaptation baseline. This is a case study, not a universal failure rate. ACE addresses the problem through localized delta updates and structured curation rather than repeatedly regenerating the entire playbook.

ChatGPT can make mistakes. Check important info.
Latest response




GPT-6 Astra
Light
None
Minimal
Light
Medium
High
Extra High
Max
Ultra
Persistent
Outputs
Create file or site
Sources
Web search