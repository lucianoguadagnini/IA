Module 8 Practice: The Full Engagement Simulation — Result

Scenario: Meridian Health Services, provider credentialing Sponsor: Diane Okafor, COO Author: Luciano Guadagnini Date: September 2026 Mode: solo (answers written out; defense answered in writing, not aloud)

Sections marked [PLACEHOLDER] reference artifacts from earlier modules (Module 1 doubt, Module 6 ninety-day plan) and need to be replaced with the actual text from those labs.

Exercise 1: The diagnosis
1a. Flow analysis

Working time per step (from Meridian's table)

Step	Working time	Wait before (days)
Application received, logged	20 min	0
Completeness check	45 min	1.5
Primary source verification	210 min	5
Malpractice history review	90 min	2
Reference outreach and follow-up	120 min	11
Committee review preparation	120 min	3
Committee decision	15 min	7
Contract generation and countersign	60 min	2
System enablement across 4 systems	90 min	1
Total	770 min = 12.8 h ≈ 1.6 working days	32.5 days

The waits (32.5 days) plus the working time (~1.6 days) reconcile to the reported 34-day average, so the table is internally consistent. That matters: it means the 34 days is not an estimate, it is the sum of measured queue times, and the queue times are where the time is.

Flow efficiency

On a working-day basis (8-hour days): 1.6 / 34 = 4.7%
On a calendar-hour basis: 12.8 h / 816 h = 1.6%

I use the 4.7% figure with the client because it is the more generous one and it is still damning. Either way the shape is the same: roughly 95% of a credentialing file's life is spent waiting for someone, not being worked on.

Three longest waits, in order

Reference outreach and follow-up: 11 days (34% of all wait time)
Committee decision: 7 days (22%) — a calendar artifact of a twice-monthly meeting
Primary source verification: 5 days (15%)

Together these three are 23 of the 32.5 wait days (71%).

The true constraint

The verification team. Not because they are slow (their 7 hours of active work per file is reasonable) but because 18 of the 32.5 wait days (PSV 5 + malpractice 2 + references 11) sit in queues in front of the same 11 people, who work from a shared spreadsheet, hold the process in their heads, and have no capacity buffer. The committee's 7 days is a policy constraint (a batching cadence), not a capacity constraint; it is the second constraint and it is the cheaper one to break, but if you break it first, files simply arrive at the verification queue faster and wait there instead.

What the number means, for Diane to say to her CEO

"A credentialing file takes 34 days to get through us, and during those 34 days someone is actually working on it for about a day and a half. Ninety-five percent of the time it is sitting in a queue. We have been paying for tools that make the day and a half faster. The 30-day contract is lost in the other 32 days, and nothing we have bought touches those."

1b. Where the previous attempts went wrong

The chatbot at 4% usage. Mechanism: capability with no workflow attachment. The chatbot answers policy questions, but nobody's job has a step called "ask the policy question" that the chatbot replaces. It was deployed as a destination, not inserted into a flow, so using it is an extra action on top of the existing way of finding out (ask the person who knows). Against the three conditions: shared context fails because the chatbot sits over the same untaxonomied 400,000 SharePoint files, so its answers are as fragmented as the source, and users learned within a couple of tries that the person next to them is more reliable. Accountable execution fails because usage was the only metric; no one defined which decisions it was supposed to speed up, so 4% is not even known to be bad, it is just low.

Copilot with unchanged release cadence. Mechanism: local optimization of a non-constraint. Engineers report being faster at writing code. Release cadence is fixed at two weeks by something that is not code-writing speed: test and integration time, change approval, the mainframe integration, whatever the actual bottleneck of their delivery system is. Speeding up a step upstream of the constraint produces inventory (more finished code waiting to ship), not throughput. The bottleneck argument applied precisely: if coding is 30% of lead time and Copilot makes it 30% faster, the best possible system improvement is 9%, and only if nothing else is queued, which it is. And the VP of Engineering's technical debt point is exactly this: the constraint on release cadence is the debt (fragile integrations, slow tests, manual regression on 27-year-old systems). Copilot made the non-constraint faster and the constraint, the debt, untouched. He is not wrong; paying down the debt would move the constraint and is the precondition for Copilot ever showing up in cadence. Against the three conditions: accountable execution fails because "engineers feel faster" was the measure and nothing attributable to a business outcome was tracked.

The classification pilot blocked by compliance. Mechanism: an accuracy metric was substituted for a decision design. 91% accuracy means 9% of documents go somewhere wrong, and the pilot never specified where, who owns them, how they are found, or what the consequence is. Compliance asked the only question that matters in a regulated process, "what happens to the errors," and the project had no answer because it was designed as a model, not as a workflow with an exception path. Against the three conditions: accountable execution fails outright (no traceability for the 9%); identity fails because there was no defined actor with defined authority to move a document, so there was no one to hold accountable for a misfiled one. This was the closest of the four to working and it failed for the most fixable reason.

Three independent retrieval systems. Mechanism: shared context failure at the organizational level, reproduced at the technical level. The reason three teams built the same thing is the same reason the policy documents are hard to retrieve: there is no place where "what exists and who owns it" is written down. Each team paid the full reconstruction cost of understanding the document corpus, and each will pay it again at maintenance time. Against the three conditions: shared context is the obvious failure, but accountable execution is the underlying one: nobody owns "retrieval over policy documentation" as a capability, so three people could each spend budget on it without anyone noticing. It is also the clearest evidence for the diagnosis in 1d.

The common pattern across all four: every initiative measured its own output (usage, developer sentiment, model accuracy, "we built it") and none measured a number in Diane's operations reporting. That is why she cannot point to one.

1c. The three conditions

Shared context. What is fragmented: the credentialing file itself. Its pieces live in ServiceNow (sometimes), the verification team's shared spreadsheet (mostly), SharePoint (400,000 files, no taxonomy), Oracle (provider data), the mainframe (eligibility), email threads (reference outreach), and the heads of 11 people with 9-year tenure. Where the reconstruction cost lands: on every handoff. Committee review preparation is 2 hours of work whose entire content is reassembling a file that already exists in five places. System enablement across 4 systems is 1.5 hours of re-keying a decision that was made 3 days earlier. Reference follow-up takes 11 days partly because nobody can see, without opening the spreadsheet, which references have been chased. Evidence: three retrieval systems built independently, the spreadsheet-vs-ServiceNow split, the 2-hour prep step.

Identity. What exists for automated actors today: effectively nothing that the security team would accept. Meridian has a moderately well governed Azure tenancy and an identity provider (assume Entra ID), so the primitives exist: service principals, managed identities, RBAC, Conditional Access. But no AI initiative has defined an agent as a principal with scoped permissions, which is why security refused one over data residency: the project could not say what the actor was, what it could touch, or where the data went. What would be needed: one named workload identity per agent role, least-privilege access to specific ServiceNow tables, a read-only Oracle view, a scoped SharePoint site, an audit trail security can query, and a residency answer (region-pinned processing inside the tenancy). Evidence: the refused project; the classification pilot with no actor accountable for the 9%.

Accountable execution. What is measured: elapsed time, percentile, penalty rate (the operations data in the scenario is good; Diane's team can produce a flow table). What is attributed: nothing. $3.4M of spend has no outcome attached; Copilot has a sentiment; the chatbot has a usage number. What is invisible: which step caused a 30-day miss on a given file, what happened to a misclassified document, which of three retrieval systems anyone uses, and what the verification team decided and why on any given file (it is in the spreadsheet, or it is not). Evidence: "I cannot point to a single number"; ServiceNow used inconsistently.

Ranking by severity for this client:

Accountable execution. Most severe because it is the reason the other two were never fixed. Without a number attached to each initiative, nobody could see that the chatbot and Copilot were not moving anything, and $3.4M went by. It is also the condition the sponsor's own survival depends on in November. Fixing it first (a measured baseline, an outcome number, a decision log) is cheap and makes every other decision in the engagement legible.
Shared context. Second because it is what the 32.5 days of wait are made of. But it cannot be fixed globally (400,000 files) and attempting to is how this client has failed three times already. It has to be fixed for one workflow, scoped.
Identity. Third not because it is unimportant but because it is the best-understood of the three here. Security is strict and competent, the Azure tenancy is governed, and the primitives exist. This is a design and negotiation problem with a known solution, and the security team's earlier refusal is actually an asset: they have already told us what the bar is.
1d. The uncomfortable finding

Nobody owns credentialing end to end. Five groups each own a step, the committee that contributes the second-largest wait does not report to the COO, the people who actually know the process work outside the system of record, and the sponsor approved $3.4M without a single outcome number attached to any of it. That is not a technology gap; it is an accountability gap that starts at Diane's level, and every previous vendor was hired into it.

What I would say, to Diane, in the first week and privately: "The reason none of the spend moved a number is that no spend was ever tied to a number, and that decision was yours to make. I am not saying it to assign blame; I am saying it because if we do not fix that first, we will be vendor number four. The first thing we ship is the number, and you will own it, and I need you to be willing to say to the CEO in November that the previous $3.4M was not measured and this is." The secondary version of the same finding goes to her as well: eleven people with an average tenure of nine years are the process, and the redesign will ask them to write it down. Some of them will read that as being replaced. That is a management conversation, hers to have, not ours to automate around.

Exercise 2: The engagement design
2a. The outcome

Primary outcome measure: on-time credentialing rate.

The number: percentage of credentialing files completed (system enablement done in all 4 systems) within 30 calendar days of application receipt.
Current baseline: approximately 60% (Meridian reports missing the 30-day commitment "roughly 40% of the time"; average 34 days, p90 41 days). Verified how: in week 1, reconstruct the last six months of files from two timestamps that exist regardless of ServiceNow discipline: the intake log date and the provider activation date in Oracle (the last of the 4 enablement systems). That gives a per-file elapsed time independent of the spreadsheet and of anyone's memory. If the reconstruction disagrees with the "roughly 40%" figure, the reconstruction wins and the baseline is restated before anything else is built.
Target and date: ≥ 85% on-time, and p90 ≤ 30 days, for files received from day 46 onward, measured at day 90 (files received days 46–60, all closed by day 90). Interim readout at day 60 on the first partial cohort, in time for Diane's November conversation.
Measurement method, reproducible by someone else: a single ServiceNow report over the credentialing record type, with two mandatory timestamps (received, enabled) that are set by the intake step and the enablement step and cannot be edited afterwards. Anyone with report access runs it; the query is checked into the engagement repo. Files withdrawn by the provider are counted separately and disclosed, not excluded silently.
What would falsify it: the day-90 cohort is below 85% on-time or p90 is above 30 days; or the improvement is explained by a drop in intake volume of more than 20% versus the baseline period (less work, not a faster process); or the secondary measure degrades beyond its threshold; or the on-time rate is achieved by files being marked "enabled" before the provider can actually bill (checked by sampling against the mainframe eligibility record).

Secondary measure (anti-gaming): verification defect rate.

If you only optimize elapsed time, the dimension that degrades silently is verification quality: a faster PSV that misses a lapsed licence, a reference step closed on two responses instead of three, a malpractice history skimmed. Nobody notices until an insurer audit or a patient.

The number: percentage of completed files in which a blind re-review finds a material verification error (missing or incorrect primary-source finding, unresolved malpractice flag, reference requirement not met per the client's own policy).
Method: 10% random sample of completed files each month, re-reviewed by a senior verifier who did not work the file, using a fixed checklist. Baseline established on files from the last three months before any change.
Threshold: the defect rate must not rise above baseline by more than 1 percentage point. If it does, the primary result does not count and the engagement reports a failure.
Tertiary signal, tracked not targeted: rework rate (files returned from committee for missing information). If the committee redesign hides errors by removing the committee's second look, this is where it shows.
2b. Scope

In scope (first ninety days)

One workflow: initial provider credentialing, from application receipt to system enablement. Nothing else.
ServiceNow becomes the system of record for that workflow, with the two mandatory timestamps and a per-file state that the spreadsheet cannot represent. The verification team's spreadsheet is retired for new files by day 30; it stays read-only for history.
Measurement: baseline reconstruction, primary and secondary measures, a report in Diane's operations pack.
Reference outreach redesign: start at day 0 in parallel, structured follow-up cadence, tracked state, phone escalation.
Committee decision redesign: consent agenda with delegated approval for clean files between meetings.
Two agents in production by day 60: intake completeness pre-screen and PSV evidence collection (read-only). One more by day 90 if the first two hold: committee packet assembly.
A verification playbook, written by the verification team, scoped to what the agents and the new hires need. Not a knowledge management programme.
The decision log and cost attribution from day 1.

Explicitly out, and why

The chatbot, Copilot, and the classification pilot. Not because they are wrong but because touching them spends the first ninety days on the previous ninety days. Copilot stays; it costs nothing to leave. The classification pilot gets a one-page note on what an exception path would look like, offered to compliance, no work.
The three retrieval systems. We inventory them (one page: what each indexes, who built it, who uses it) and we reuse one if it helps the playbook. We do not consolidate them. Consolidation is a governance decision Diane can make after she has a number.
The mainframe. We read from it (eligibility) and never write to it.
Re-credentialing, claims correspondence, provider network management. Same shape, later, see 3d.
Any new platform licence. No budget; also no need.
Any new taxonomy for the 400,000 files. See 2d.

The first thing that ships: week 2. The measured baseline in Diane's operations report, produced from the intake log and Oracle activation dates, with the on-time rate, average and p90 by month for the last six months. Alongside it, the intake completeness pre-screen: an agent that reads a new application against the completeness checklist and returns a missing-items list to the intake team within minutes of logging, so the completeness check happens on day 0 instead of after a 1.5-day wait. It is small (one step, 1.5 days out of 34), it is read-only, it puts nothing in front of security they have not seen before, and it demonstrates the method: a number first, an agent inserted into an existing step, a human still doing the step, the effect visible in the same report the following week.

2c. The workflow redesign

The driveshaft version: AI applied to the current shape

Apply assistance to the working time of each step and leave every wait where it is.

Step	Current working	With AI assist	Rationale
Logging	20	20	Already trivial
Completeness check	45	15	Pre-screen agent
PSV	210	120	Evidence collection automated, judgment human
Malpractice review	90	60	Summarization, human reads
Reference outreach	120	45	Drafting and tracking
Committee prep	120	45	Packet assembly
Committee decision	15	15	Unchanged
Contract	60	30	Template generation
Enablement	90	60	Partial
Total	770	410	

Working time drops 47%, which is a good headline. Elapsed time drops from 34 days to about 33.3 days, a 2% improvement, because 360 minutes saved is three quarters of a working day against 32.5 days of queue. The 30-day miss rate barely moves. This is precisely what Copilot did to the engineering organization, and it would produce exactly the same conversation with Diane in another eighteen months. I would show her this table and this number so she can see why the previous approach was structurally unable to work.

The redesign version: change the shape

The committee. 7 days of wait for 15 minutes of decision is a batch-size problem. Options, in ascending order of change: (1) move to weekly meetings, halves the wait, costs physician time; (2) asynchronous electronic vote with a 48-hour window, standard in credentialing, requires bylaws change; (3) a consent agenda: files that meet every criterion with no flags are approved by the committee chair or medical director under delegated authority between meetings, and the committee ratifies the list at its next meeting; only flagged files go to discussion. Option 3 is what accreditation bodies already allow for "clean" files and is what I propose: clean files wait 1–2 days for the chair's signature; flagged files keep the 7 days. What fraction is clean is a number we measure in week 1 (I expect a majority, based on nothing but the shape of most credentialing populations, so it is stated as an assumption to verify, not a fact).

The 11-day reference wait. What is actually happening: three emails go out, references are busy physicians and practice managers, nobody follows up until someone remembers to open the spreadsheet, the third reference is often a different person than named, and the step cannot close until the last one replies. Nothing is happening for most of those 11 days; the step is not slow, it is unattended. The redesign: outreach starts at day 0, the moment the file passes completeness, in parallel with PSV and malpractice, instead of after them (sequential dependency that exists only because one team does all three and works them in order). Follow-ups are on a fixed cadence (day 2, day 4, day 6) with state visible in ServiceNow, phone escalation by a human at day 5, and a "reference substitution" path so a non-responsive reference can be replaced without restarting. Target: 11 days to 6, and running concurrently with the 7 days of PSV and malpractice rather than after them.

Steps that exist because context could not carry forward. Committee review preparation (2 hours, 3-day wait) is entirely a reassembly step: everything in the packet was produced by the verification team and exists in the spreadsheet, SharePoint, and email. If the verification outputs land in a structured ServiceNow record as they are produced, the packet is a rendering of that record and the step collapses to a review of a generated document. System enablement across 4 systems (1.5 hours, 1-day wait) exists because the contract decision is a signed PDF and not a machine-readable event; it does not fully collapse in ninety days (the mainframe is out of scope) but it becomes a checklist driven from the record. The completeness check as a separate step exists because intake does not know the requirements; with the pre-screen it merges into logging.

What could be verified continuously. Licence status, board certification, sanctions and exclusion lists (OIG, state boards) are queryable primary sources. Today they are checked once, at a gate, 5 days after the file reaches the verification queue. They can be pulled automatically the moment a file passes completeness, so that when a verifier opens the file the evidence is already attached and dated, and the human work is reviewing evidence rather than gathering it. The same mechanism monitors already-credentialed providers between cycles, which is out of scope now and is the obvious next engagement.

Load-bearing knowledge. Of the 11 verifiers, the knowledge that is load-bearing is: which primary source is authoritative for which state, specialty, and licence type; how to read a malpractice history and decide what is a flag versus noise; which reference types actually respond and how to reach them; and what the committee (each physician on it) will and will not accept. In the redesign, two of the eleven become playbook owners and exception handlers for the first ninety days, paid in time not headcount, and their job becomes writing down what they know as the agents and the new state model force the questions. The other nine keep working files, with the evidence already collected and the follow-ups already tracked. Nobody's role disappears in ninety days; the team's work moves from gathering to judging. What happens after ninety days is Diane's decision and she should make it with the numbers in front of her, not have it made for her by the design.

Redesigned flow (target state at day 90)

Step	Owner	Working	Wait before
Logging + completeness pre-screen	Intake + agent	30 min	0
PSV evidence collection (automated) → human verification	Agent → Verifier	90 min	2 days
Malpractice review (parallel)	Verifier	60 min	parallel
Reference outreach (parallel, starts day 0)	Agent + Verifier	60 min	6 days, parallel
Packet generation → analyst review	Agent → Analyst	30 min	0.5 day
Consent-agenda approval (clean) / committee (flagged)	Chair / Committee	15 min	1.5 days / 7 days
Contract generation	Contracting	30 min	1 day
Enablement (checklist, 3 of 4 systems from record)	Operations	45 min	0.5 day

Critical path for a clean file: completeness (0) → references 6 days (PSV and malpractice finish inside them) → packet 0.5 → chair 1.5 → contract 1 → enablement 0.5 → about 10–12 days average. Flagged files add the committee cadence: 17–19 days. Blended, with the clean/flagged split still to be measured, an average in the mid-teens and a p90 under 30 days, against 34 and 41 today. I would not put a more precise number in front of Diane until the week-1 baseline is done; the point is that the shape change is worth roughly ten times the driveshaft version.

The honest paragraph. The driveshaft version asks nobody to change how they work; it makes the same day feel faster and it will be adopted immediately and change nothing. The redesign asks the verification team to move out of a spreadsheet they have controlled for nine years into a system they distrust, and to write down knowledge whose scarcity is the source of their standing in the company. It asks physicians who do not report to Diane to give up a meeting-based approval they may see as their professional safeguard. It asks the intake team to accept an agent reading applications before they do. It makes the process visible, which means it makes individual slowness visible, and some of the 11 days of reference wait is a person's habit, not a system's. The human cost is real: at least a couple of the eleven will experience this as the end of the version of the job they were good at, and one or two may leave, taking the knowledge before it is written down. That is the largest single risk in the engagement and it is not a technical one. The mitigation is that the two playbook owners are chosen by the team, paid attention to, and named in the proposal as the people the engagement depends on. The failure mode is that Diane treats the redesign as a systems project and the team as its users.

2d. The three conditions, built with what exists

Constraints: SharePoint, Oracle, ServiceNow, Azure (existing tenancy), the identity provider (Entra ID, which a moderately governed Azure tenancy implies). No new platform licences. Model access via Azure OpenAI in their own tenancy, which is consumption-billed on the existing subscription rather than a licence, but I flag it as the one item that needs security sign-off before anything else: it is deployed in-region, data is not used for training, and access is through a private endpoint. If security declines it, the fallback is a smaller open-weight model on Azure compute in-region, and the timeline slips two weeks.

Shared context

What gets externalized: the credentialing file as a structured record, and the verification playbook.
The record lives in ServiceNow: one custom table (or an extension of the existing workflow record) with a fixed state model (received, complete, evidence collected, verified, references complete, packet ready, approved, contracted, enabled), per-step timestamps, and attachments for evidence. This is the object humans and agents both read. The spreadsheet's columns become fields on it; the spreadsheet's history is imported once.
The playbook lives in a single dedicated SharePoint site, not the 400,000-file corpus. Scoped first version: the documents the verification team actually opens. Discovery method: for two weeks, the two playbook owners log every document they consult; combine with the indexing logs of whichever of the three retrieval systems is closest; expect the result to be a few hundred documents out of 400,000. Those get a minimal taxonomy (state, licence type, source, policy version) and are indexed with Azure AI Search inside the tenancy. Nothing else in SharePoint is touched.
What updates it: humans update the playbook (owned by the two playbook owners, reviewed monthly, version-controlled through SharePoint versioning). Agents update the record (evidence attachments, outreach state, timestamps) and never the playbook. When an agent hits a case the playbook does not cover, it raises an exception on the record, and the exception is the prompt for a playbook entry.
How humans and agents find it: humans through the ServiceNow record and the playbook site; agents through the ServiceNow API for the record and Azure AI Search over the playbook site. One place each, and the same place for both.
Oracle and the mainframe: read-only views exposed for provider identity and eligibility. Nothing writes to either.

Identity

Four agents. Each is a separate workload identity so the blast radius of any one is bounded and the audit trail is per-role.

Agent	Role	Permissions	Enforcement mechanism	Memory and history	Boundaries
Intake Completeness	Read new application, return missing-items list	Read: ServiceNow credentialing record (new state only), application attachments; Read: playbook completeness checklist. Write: one field (completeness result) and a work note on the same record. No other tables.	Entra ID app registration with its own service principal; ServiceNow OAuth client credentials bound to a dedicated integration user with a custom role whose ACLs allow read on the credentialing table and write on two fields only; Graph API Sites.Selected permission granted to the playbook site alone; secret in Azure Key Vault with RBAC to the agent's managed identity only.	No memory across files. Every run logged with run id, input hashes, output, model version.	Cannot create or delete records, cannot see provider PII beyond the application it is asked about, cannot send email.
PSV Evidence Collector	Query licence boards, board certification, sanctions/exclusion lists; attach dated evidence	Read: record identity fields (name, NPI, licences claimed); Write: evidence attachments and "evidence collected" state only; Outbound HTTPS to an allowlist of primary-source domains.	Same Entra/ServiceNow pattern with a distinct integration user and role; outbound traffic through Azure Firewall / NSG with an explicit FQDN allowlist maintained by security; managed identity for any storage; no Oracle access at all.	No memory. Evidence stored as immutable attachments with source URL, timestamp, and response hash.	Never renders a verification judgment; the "verified" state can only be set by a human in the verifier role. Cannot query sources not on the allowlist.
Reference Outreach	Send and track reference requests, schedule follow-ups, flag non-response	Read: reference contact fields; Write: outreach state, follow-up timestamps, received responses as attachments; Send mail from a dedicated shared mailbox.	Entra app with Exchange Online application access policy scoping Mail.Send to one mailbox only; ServiceNow role limited to the reference sub-table; DLP policy on the mailbox preventing attachments containing provider PII outbound.	Memory limited to per-file outreach state, held in ServiceNow, not in the agent.	Cannot substitute a reference (human decision), cannot close the step, cannot email anyone not listed on the record.
Packet Assembler	Render the committee packet from the record	Read: the full record for files in "references complete" state; Write: packet document as an attachment and the "packet ready" state.	Distinct Entra app and ServiceNow role; read scoped by state via ACL condition; writes to a single SharePoint library via Sites.Selected.	No memory. Packet is a deterministic rendering plus a summarized narrative that is labelled as generated.	Cannot modify evidence, cannot set approval state.

Cross-cutting enforcement: Conditional Access for workload identities restricts every agent principal to Azure-hosted compute in the tenancy's region (data residency answer for security); Privileged Identity Management is not used for agents because nothing they do is privileged; every secret rotates through Key Vault; Entra sign-in logs and ServiceNow audit tables are forwarded to Log Analytics / Sentinel, which security already runs. The security team gets the table above as the first document, before any code, and they veto any row.

Accountability

Link	What it holds	System
Outcome measurement	On-time rate, p90, volume, defect rate	ServiceNow report over the credentialing table; published into Diane's operations pack monthly
Decision log	Engagement design decisions (why consent agenda, why these four agents, why not the mainframe), each with date, decider, alternatives	Markdown ADRs in the engagement repository (Azure DevOps or GitHub, whichever engineering uses); operational decisions on a file (reference substituted, flag cleared) as ServiceNow work notes on the record, mandatory on state transition
Cost attribution	Model tokens per agent per file, Azure compute, human hours per step	Azure cost tags per agent identity; Azure OpenAI usage logs joined to run ids; ServiceNow time tracking on the record
Traceability chain	For any file: which agent ran, when, with what input, what it wrote, which human approved what	Run id on every ServiceNow work note → Application Insights trace → Entra sign-in log for the principal → immutable evidence attachment with hash. Six months later security follows the run id and reconstructs the whole thing without asking anyone.
2e. The hybrid split
Step	Human / Agent / Both	Justification (verification cost, consequence of error)	Context in → out
Logging	Human	Trivial; entry point of accountability	In: application. Out: record created with received timestamp
Completeness pre-screen	Both (agent screens, human confirms)	Verification is cheap (a checklist); error consequence is a delay, not a wrong decision	In: application + checklist. Out: missing-items list, flagged for human, who sends the request to the provider
PSV evidence collection	Agent	Gathering from named sources is mechanical and the evidence is self-verifying (dated, hashed, source-attributed)	In: identity fields, claimed credentials. Out: evidence attachments with source and timestamp
PSV judgment	Human, always	Regulated. The decision that a licence is valid and matches the applicant is what an accreditor audits and what a malpractice suit examines. The agent's role is to make the human's review faster and better evidenced, never to make the call. Verification cost of a wrong call is discovered at the worst possible time	In: evidence set. Out: verified state, verifier name, timestamp, any exception raised
Malpractice review	Both (agent summarizes and extracts events, human decides)	Interpretation is judgment; the consequence of a missed pattern is a credentialed provider with a history	In: NPDB/malpractice reports. Out: structured event list + human's flag/no-flag decision with reasoning as a work note
Reference outreach	Both (agent sends and tracks, human escalates and substitutes)	Sending is mechanical; deciding a reference is acceptable is a policy judgment	In: reference contacts, template. Out: outreach state, responses, non-response flags for the human
Packet assembly	Agent, human reviews	Rendering is deterministic; the review is the safeguard	In: full record. Out: packet, labelled as generated, with the analyst's sign-off
Approval	Human (chair or committee)	Regulated, and a professional judgment by physicians; no agent role beyond presentation	In: packet, flag status. Out: decision, decider, date, conditions
Contract generation	Both	Template rendering is mechanical; countersign is human	In: decision, terms. Out: signed contract, contract event on the record
Enablement	Human with agent-generated checklist	Writes to production systems including the mainframe; not automated in ninety days	In: contract event. Out: enabled timestamps per system, the last one closing the file

Context crossing back upstream: every human decision (exception, flag, substitution, rejection) is written to the record as a structured work note, which is what the playbook owners mine weekly for playbook updates, which is what the agents read next time. That loop is the whole point; without it the agents are frozen at the playbook's first version.

Exercise 3: The client communication
3a. The proposal (two pages, for Diane)

Meridian Health Services — Provider Credentialing: Proposal Prepared for Diane Okafor, COO. For onward use with the CEO.

What we found

A provider credentialing file takes 34 days on average to get through Meridian, and 41 days for the slowest one in ten. The contract with your insurer clients says 30. You miss it about 40% of the time, pay a penalty each time, and lose some of those providers to competing networks.

During those 34 days, the file is actively being worked on for about a day and a half. The rest, roughly 95% of the time, it is waiting in a queue for the next person. Three queues account for most of it: waiting for provider references to reply (11 days), waiting for the credentialing committee to meet (7 days, because it meets twice a month), and waiting for the verification team to start primary-source checks (5 days).

The verification team of eleven people, most of them here nine years or more, are the only people who know how the process really works, and they run it from a shared spreadsheet rather than from ServiceNow. That means nobody, including you, can see where a file is or why it is stuck without asking them.

Why the previous initiatives did not produce results

The tools bought over the last two years all made the day and a half of active work faster. None of them touched the 32 days of waiting, because none of them were aimed at a specific queue in a specific workflow. The chatbot answered questions nobody was routing through it. Copilot made engineers faster at writing code, but releases are paced by testing and integration on 27-year-old systems, so the cadence did not move; your VP of Engineering's point about technical debt is the accurate description of why. The document classification pilot worked well and stopped because nobody had defined what happens to the documents it gets wrong, which is the first question compliance will always ask. Three teams built the same retrieval system because there was no place to see that it already existed.

The common thread is that each initiative was measured by its own activity rather than by a number in your operations reporting. That is fixable, and fixing it is where we start.

What we propose

Ninety days on one workflow, provider credentialing, from application to the provider being able to bill.

In the first two weeks we put a measured baseline in your operations report: the on-time rate, average and 90th-percentile days, month by month for the last six months, built from timestamps that already exist. Alongside it we ship one small assistant that checks new applications for completeness the day they arrive, instead of a day and a half later.

Over the ninety days we change the shape of the process: reference outreach starts on day one and runs in parallel with verification instead of after it, with tracked follow-ups; clean files are approved by the committee chair between meetings under delegated authority and ratified at the next meeting, so only files with issues wait for the meeting; primary-source evidence is collected automatically the moment a file is complete, so your verifiers spend their time judging evidence rather than hunting for it; ServiceNow becomes the one place a file lives, and the spreadsheet is retired for new files. Your verification team writes down what they know, with two of them leading that, and their work shifts from gathering to deciding.

What it will take

Most of the work is not AI. About eighty percent of it is: reconstructing the baseline, agreeing the state model with the verification team, getting the ServiceNow record right, getting security's approval of exactly what each automated assistant may read and write, writing the playbook, and changing how the committee approves clean files. The assistants themselves are the smaller part and they are built with what you already own: ServiceNow, SharePoint, Oracle, and your Azure environment. No new platform licences.

The hard part is human. The verification team will be asked to leave a spreadsheet they have controlled for years and to write down knowledge that is currently theirs alone. Some will find that threatening. The committee's physicians will be asked to change how they approve. Both need you, not us.

How we will know it worked

The number is the percentage of credentialing files completed within 30 days. Baseline: about 60%, verified from intake and activation dates in week one. Target: 85% or better, with the slowest one in ten under 30 days, for files received from day 46 onward, reported at day 90. A first partial reading at day 60, in time for November.

A second number guards the first: a monthly blind re-check of one in ten completed files for verification errors. If that gets worse, the speed does not count and we will say so.

If at day 90 the on-time rate is below 85%, or volume dropped, or quality slipped, the engagement did not work and you will have a report saying exactly which step did not move and why.

What we need from you

Access, by day 5: read access to ServiceNow, the intake log, Oracle provider activation dates, and the verification team's spreadsheet.
People: two members of the verification team, chosen by the team, at roughly half their time for ninety days; one credentialing analyst, one contracting lead and one operations lead at a few hours a week; one named person from security as our reviewer from day 1, not day 60.
Decisions: by day 10, that ServiceNow is the system of record for credentialing and the spreadsheet is retired for new files; by day 30, your sponsorship of the consent-agenda proposal to the committee chair, since the committee does not report to you and this will be your ask, not ours.
A conversation, this week, with your VP of Engineering, with me in the room.
Thirty minutes every two weeks. The first fifteen are the number; the second fifteen are what is not working.
3b. The engineering conversation

Me: Before I show you anything, I want to say the thing you are probably expecting me not to say. You are right about the technical debt. The reason Copilot made your engineers faster and your release cadence did not move is that the cadence is set by the debt: the integration work, the regression on the mainframe path, the things that make a release a two-week event. Making coding faster in front of that just builds a bigger pile waiting to ship. I am not here to tell you AI fixes that. I am here because I think what I have been asked to do can be pointed at it, and I want to know if you agree before I put it in front of Diane.

VP: I appreciate the honesty, but I have heard "we will help with the debt" from every vendor who wanted my team's time. What actually lands on my people is integration tickets for someone else's pilot. What are you asking for?

Me: Less than you expect, and something specific in return. The scope is credentialing, which is an operations process, not an engineering one; the verification team and ServiceNow carry most of it. What I need from engineering is a read-only view over the Oracle provider tables, a review of four service accounts with security, and a place to store decision records. Maybe fifteen days of one engineer across ninety. What you get is this: the enablement step at the end of the process writes to four systems by hand, including the mainframe, because there is no machine-readable event for "provider approved." That is a piece of your debt with a business number attached to it, 1.5 hours per file and a day of delay, and by day 90 I will have that number in Diane's operations pack next to the on-time rate. That gives you something you have not had, which is a debt item the COO can see the cost of.

VP: So your pitch is that you will instrument a piece of my debt so I can get budget for it. That is not nothing. But you are also going to want my team to write decision records and keep them current, and I will tell you now: they will not. Not because they are lazy, because every previous process like that died in three months.

Me: Agreed, and I would not ask them to. Anything that depends on people voluntarily writing things down decays. What I would propose is that the record is a by-product: the pull request template requires a link to a decision record, the pipeline refuses to merge without it, and the assistant drafts the record from the diff so the engineer edits three sentences instead of writing a page. If the gate is off, the process does not exist, and I would rather you tell me now that you will not turn the gate on than find out at week six. If you will not, I will tell Diane that the engineering side of the accountability chain is a commitment rather than a mechanism, and that she should weight it accordingly.

VP: Put the gate in the proposal so it is her decision and not mine, and I will turn it on. And I want to see the fifteen days written down before anyone talks to my engineers.

If there had been no version that served his interest: I would tell Diane that the engagement can be run without engineering beyond read access and security review, that the VP's objection is correct and is about a different problem, and that she should not spend her political capital making him support something that does not help him. The credentialing outcome does not depend on his enthusiasm. His debt does depend on someone putting a number on it, and I would offer to do that as a side-product whether or not he wants it.

3c. The bad news memo

To: Diane Okafor Subject: Reference outreach automation is underperforming — status and plan

Diane,

The automated reference outreach we turned on in week four is not working. Response rates from provider references are about 20% lower than the manual process. References appear to be treating the automated emails as noise; several have told our verifiers they never saw them.

What it means for the number: the reference step is the longest wait in the process, so this puts the 85% on-time target at day 90 at risk. The measurement itself is unaffected, and the other changes (parallel start, committee consent agenda, evidence collection) are performing as expected.

What we are trying this week: sending from the assigned verifier's own mailbox with the agent drafting and tracking behind them rather than sending; a phone-first escalation at day three instead of day five; and a short test of whether the message content or the sender is the cause.

What we need: nothing from you today beyond awareness. If the sender change works, the team keeps the tracking benefit without the response loss.

I will update you by Friday with data from the test, and we will re-forecast the day-90 number then. If it needs to move, I will tell you rather than hope.

Luciano

3d. The next gain

"While we were mapping enablement, we found that every credentialed provider has their record re-keyed by hand into four systems, and the same happens again at every re-credentialing cycle and every change of address, licence, or group affiliation. On the volumes we measured in weeks eight to ten, that is roughly 180 hours a month of operations time and, more importantly, the source of most of the provider data mismatches your insurer clients complain about. A provider record event, published once from ServiceNow and consumed by the other three systems, would recover most of those hours and remove the mismatches at the source. It is a bigger engineering piece than anything we did in these ninety days, it is a piece of the technical debt your VP of Engineering has been describing, and it now has a number."

Exercise 4: The defense

Legend: [F] answered from the framework; [I] improvised or partly improvised.

Diane: "The last three vendors told me they would fix this. Why is this different?" [F] Because I will tell you in week two whether it is working. The previous initiatives were measured by their own activity; this one is measured by a number that is already in your operations report and that I did not choose: the on-time rate against your 30-day contract. You will see the baseline before we build anything, you will see the number every two weeks, and the proposal says in writing what would make us say it failed. If by day 60 the number is not moving, you will know, and so will I, and you can stop. The other difference is scope: one workflow, not "AI at Meridian." The last three vendors were probably not wrong about the technology; they were aimed at nothing in particular.

Diane: "You are proposing to change how the credentialing committee works. That committee has physicians on it who do not report to me. How do you expect me to make that happen?" [I] I do not expect you to make it happen; I expect you to ask for it, with two things in hand that you do not have today. First, the number: the committee's cadence costs seven days of the thirty, and the chair will see that in the same report you see. Second, the fact that consent agendas for clean files are already standard practice under the accreditation frameworks the committee itself works under, so this is not an operations person telling physicians how to do medicine; it is the committee adopting a mechanism its peers use. Frame it to the chair as "you approve the clean ones between meetings and the committee ratifies," which increases the chair's authority rather than reducing the committee's. If the chair refuses, the redesign still works for the other 25 days and the proposal is honest that the committee piece is yours to win. — Improvised: the framework says the sponsor owns decisions outside the engagement's authority, but the specific move (accreditation practice as the lever) came from my own experience with governance bodies, not from the modules.

Diane: "What happens if this does not work? What do I tell my CEO in November?" [F] By November you will have three things regardless of the outcome: a verified baseline showing how credentialing actually performs, which you do not have today; a measured reading at day 60 showing whether the on-time rate is moving and, step by step, which part of the process moved and which did not; and a written account of why. If it worked, you tell him the number. If it did not, you tell him that for the first time in two years a piece of AI spend was measured against an operations outcome, that it did not clear the bar, and exactly what did not move and why, and that the same measurement now applies to everything else. That is a much better November than the one you were going to have, and it is the honest one.

Diane: "Can I do a smaller version first?" [F] Yes, and it is already in the plan: the first two weeks are the smaller version. The baseline and the completeness pre-screen are real, shipped, measured, and they touch nothing that security or the committee cares about. If after two weeks you do not want to continue, you keep the baseline report and the pre-screen and you have spent two weeks. What I would push back on is a smaller version that leaves out the measurement or the ServiceNow record, because that is the version that cannot tell you whether it worked, which is the version you have already bought three times.

VP of Engineering: "We already have Copilot. What are you adding?" [F] Nothing to your engineers' editors. Copilot makes writing code faster; your release cadence is set by integration and regression on the older systems, so it cannot show up in a business number, and it has not. What I am adding is on the operations side: four narrowly scoped assistants inside the credentialing workflow, each one attached to a queue that is measured, and the measurement itself. The only thing that touches engineering is a read-only Oracle view, a security review, and, if you want it, a number on the enablement debt that you can take to Diane.

VP of Engineering: "You want my team to write decision records. They will not do it. What is your plan for when they do not?" [F] My plan is that they do not have to. Any process that depends on sustained voluntary diligence decays, and I would design as if it will. So the record is a by-product, not a task: the merge is gated on a linked decision record, the assistant drafts it from the change, and the engineer edits rather than authors. If the gate is off, the process does not exist, and the accountability chain on the engineering side is a promise, and I will report it to Diane as a promise. On the operations side it is the same shape: a file cannot change state in ServiceNow without a work note on the transition, so the operational decision log writes itself as a condition of the work happening at all. — This is the question the module flags, and it was the one I answered most directly from the framework: mechanism, not commitment.

VP of Engineering: "Who maintains all this after you leave?" [I] Two named people and a small surface area. The playbook and the exception queue are owned by the two verification-team members who built them, and their time for it is in the proposal. The four assistants are each a few hundred lines with one identity, one set of permissions, and one job; the engineer who spent fifteen days on the Oracle view and the security review is the same person who reviews changes to them, and the decision records are how that person knows why anything is the way it is. What I will not leave behind is a platform. If the answer had been "a new platform with its own team," you would be right to say no. — Partly improvised: the framework covers the handover principle, but sizing the maintenance to "one engineer who already touched it" was my judgment.

Head of Security: "You want service accounts for AI agents with access to provider data. Walk me through the blast radius if one is compromised." [F] Four separate identities, so the question is per agent. The worst case is the PSV evidence collector: it can read identity fields and claimed credentials for files in one state, write attachments to those files, and reach an allowlist of licence-board domains through your firewall. Compromised, it can exfiltrate identity fields for files currently in evidence collection (tens, not thousands, at any time, and bounded by the ServiceNow ACL to that state), and it can write junk attachments, which a human verifier would see before any decision. It cannot reach Oracle, cannot send email, cannot see files in other states, cannot change a verification result, and cannot reach any domain not on your list. Its secret lives in Key Vault, rotates, and its sign-ins are in your Sentinel with Conditional Access pinning it to in-region compute. The reference outreach agent is the one I would scrutinize hardest because it sends mail; its Mail.Send is scoped by application access policy to one mailbox, DLP blocks PII attachments outbound, and it can only address contacts on the record. I would like you to review the permission table before anything is built and strike anything you are not comfortable with.

Head of Security: "Where does the data go? We refused a project over data residency." [F] Nowhere it does not go today. All four assistants run on compute in your Azure tenancy in your region, the models are Azure OpenAI deployed in that region with no training on your data and reached through a private endpoint, and no provider data leaves the tenancy boundary at all. Outbound traffic is only to the primary-source domains on your allowlist and only carries what a verifier would type into those sites by hand today. If you decline Azure OpenAI, the fallback is an open-weight model on your own compute in-region and a two-week slip, and I would rather have that conversation now than at week six.

Head of Security: "How do I audit what an agent did six months from now?" [F] Take any credentialing file. Every agent action on it is a ServiceNow work note with a run id. The run id resolves in Application Insights to the full trace: which agent identity, what input, what model version, what it wrote. The identity's sign-in for that run is in Entra logs forwarded to Sentinel. The evidence it attached is immutable with a source URL, timestamp and hash. You can follow that chain without talking to me, to the verification team, or to anyone who built it, and the same applies to the human decisions on the file, which are the mandatory work notes on each state transition. If any link in that chain is missing, the design is wrong and I want to know.

Tally: eight from the framework, two improvised (the committee question and the maintenance question). Both improvised answers are about organizational authority and continuity rather than about the design itself, which tells me where my understanding is thin: I know how to build and measure the thing better than I know how to secure and sustain sponsorship for it inside a client's politics.

Exercise 5: The self-assessment
Readiness evidence item	Demonstrated today?	Artifact
1. Can explain Taller, the productivity gap and the role architecture without a script	Partly	The proposal (3a) explains the productivity gap in Diane's terms without naming the framework; the role architecture is implicit in the hybrid split (2e) but never explained as such. Not demonstrated as a standalone explanation.
2. Can diagnose a client scenario through shared context, identity and accountability	Yes	1b, 1c, with evidence cited and the three conditions ranked
3. Can propose a practical implementation without Chiron and Echo	Yes	2d: ServiceNow record, scoped SharePoint site, four agents with Entra/ServiceNow/Graph enforcement, accountability table naming systems
4. Can scope and lead a bounded piece of work end to end	Yes	2b (in/out/first ship), the ninety-day shape in 3a, the ask list with dates
5. Can communicate plan, risks, decisions, progress and outcome to a client	Yes	3a (plan), 3c (bad news, sent before the fix), 3d (outcome and next), 4 (defense)
6. Can show disciplined AI and agent usage, including quality controls and cost awareness	Partly	Quality controls are strong (secondary measure, human-only verification judgment, evidence hashing). Cost awareness is a row in a table (cost tags, token logs) with no estimate of what the agents will actually cost per file. Weak.
7. Can identify a business-process opportunity beyond the immediate engineering task	Yes	3d (provider record event across four systems), and the continuous-monitoring note in 2c
8. Has simulation or field evidence supporting client readiness	Partly	This simulation, run solo and in writing. No live pushback, no senior scoring. Counts as one data point, not as evidence.

Weakest item: 6, cost awareness. I designed the attribution mechanism and never used it to produce a number. A Frontier Engineer should be able to tell Diane what a credentialing file will cost in model and compute terms before building, and put it next to the penalty and the lost-provider cost. Added to the ninety-day plan: [PLACEHOLDER: add to the Module 6 ninety-day plan — "Produce a per-unit cost model (tokens, compute, human review minutes) for every agent I design, before it ships, and report actual against estimate at day 30." Insert under the relevant milestone of the existing plan.]

Worst-answered defense question: the committee question (Diane's second). The answer was reasonable but it was improvised from my own governance experience, not from the framework, and I could not point to anything in the modules that tells a Frontier Engineer how to help a sponsor win a decision outside her authority. I think this is mostly a gap in the framework as I understand it (it treats sponsor decisions as inputs rather than as work to be supported), and partly a gap in my experience (I have had this conversation with steering committees, not with clinical governance bodies). The remedy for the framework gap is to raise it; the remedy for the experience gap is field exposure with a client that has a regulated governance body.

What I would do differently tomorrow: run it with someone playing the VP and the head of security, aloud. In writing I gave myself time to construct the security answers; in the room I would have had to know the Entra and ServiceNow enforcement mechanisms cold, and I am not certain I do. I would also size the four agents' cost per file before writing the proposal, and I would measure the clean/flagged committee split as part of the diagnosis instead of leaving it as an assumption to verify, because the whole committee estimate hangs on it.

Exercise 6: Return to your doubt

[PLACEHOLDER: paste the Module 1 doubt here verbatim, as written at the end of Module 1.]

Has anything in the last seven modules changed my view? [PLACEHOLDER: answer against the actual Module 1 doubt. Guide for writing it: name the specific module or exercise that moved the view, and what evidence in it did the moving. If the doubt was about whether the productivity gap is real at the business level, this scenario is direct evidence: 770 minutes of work inside 34 days, and $3.4M spent entirely on the 770 minutes. If the doubt was about whether the three conditions are sufficient rather than merely necessary, note that this scenario needed a fourth thing, sponsor authority over the committee, that the conditions do not cover.]

If still unconvinced, the strongest version of the objection now: [PLACEHOLDER. Suggested shape, to be replaced with your own: "The framework's three conditions are diagnostic, not predictive. They explain every failure after the fact and they predicted none of Meridian's four in advance, because any failed initiative can be described as a shared-context, identity or accountability failure. A framework that cannot be wrong is not doing work. The sharper version: what would a failed initiative that satisfied all three conditions look like, and does the framework admit that one can exist?"]

What evidence would settle it, observable in the field: [PLACEHOLDER. Suggested shape: "Two engagements at comparable clients, one where the three conditions were established in the first thirty days and one where they were not, with the same outcome measure, and a difference in the outcome number that survives the secondary quality measure. Or the reverse: an engagement where all three were demonstrably in place and the outcome number did not move, which would show the conditions are not sufficient and would tell us what the missing condition is."]

This doubt, once written, goes to [PLACEHOLDER: name the senior person or cohort lead] rather than into the repo, because the framework's own position is that it evolves from people who noticed something that did not hold up and said so.

Against "what good looks like"
Criterion	Status
Flow efficiency correct and explainable in one sentence	4.7% (working days) / 1.6% (calendar hours); sentence in 1a
All four failed initiatives diagnosed with a specific mechanism	1b: workflow attachment, non-constraint optimization, decision design substituted by accuracy, organizational shared-context failure
Non-technology problem found	1d: no end-to-end owner; $3.4M spent without a number; sponsor-level
Outcome measure includes falsification and anti-gaming guard	2a: four falsifiers, defect-rate secondary with a threshold
Redesign changes the shape; honest about human cost	2c: parallel start, consent agenda, continuous evidence collection; honest paragraph
Every permission names an enforcement mechanism in the client's environment	2d: Entra app registrations, ServiceNow roles/ACLs, Graph Sites.Selected, Exchange application access policies, Key Vault, Conditional Access, firewall allowlist
Bad news memo under 200 words, sent before the fix	3c: under 200 words, hypothesis stated, no fix
Actual dialogue for the VP conversation	3b: three exchanges written out
All ten defense questions answered, improvised ones identified	4: eight framework, two improvised
Module 1 doubt revisited honestly	6: placeholders pending the original text
