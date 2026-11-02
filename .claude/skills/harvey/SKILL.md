---
name: harvey
description: Sales outreach playbooks from Harvey (github.com/ethanplusai/harvey). Use when writing cold emails or follow-up sequences, handling objections, qualifying leads, finding prospects without a paid database, planning offers, or LinkedIn outreach for Excellent Tiling Services (trade accounts, builders, renovators, designers).
license: MIT, see LICENSE.txt
---

# Harvey sales playbooks

Harvey is an autonomous cold-email agent. The app itself (Python daemon, mailbox sending, dashboard) runs on a local machine, not here. This skill carries its sales knowledge library: plain Markdown playbooks, concatenated into a prompt before an agent writes.

Read the playbook that matches the job, then write. Rules in `email_frameworks.md` override style anywhere else.

| Job | Read |
| --- | --- |
| Cold email, follow-ups, any outbound copy | `playbooks/email_frameworks.md` (banned AI patterns, compliance, AIDA / PAS / BAB / QVC / 3Ps) |
| Opening line from something observed about the prospect | `playbooks/signal_playbook.md` |
| Reply handling, "too expensive", "not now", "send me info" | `playbooks/objection_handling.md` (LAARC) |
| Who to contact, is it worth it | `playbooks/lead_qualification.md` (BANT, ICP score, MEDDIC), `playbooks/account_navigation.md` |
| Finding builders, renovators, designers without Apollo etc. | `playbooks/prospecting_tactics.md` |
| What to offer and when | `playbooks/offer_strategy.md` |
| Overall approach and ethical lines | `playbooks/sales_methodology.md` |
| LinkedIn connection requests and messages | `playbooks/linkedin_outreach.md` |
| Early-stage startups (rare for ETS) | `playbooks/selling_to_startups.md` |

ETS rules still apply: every public line goes through `ets-copy-review` before it is sent, facts come from the live store, no invented claims about a prospect. Harvey's compliance section mentions US CAN-SPAM; for Australia the Spam Act 2003 applies (consent or inferred consent, clear sender identity, working unsubscribe).

Not installed: the Harvey app. To run it, clone the repo on your own computer, `python3.13 -m venv .venv && pip install -e .`, then `claude` and say "set up Harvey for me".
