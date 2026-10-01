---
name: newsletter-playbook
description: >-
  Plan, write and grow a recurring B2B email newsletter: positioning, format, issue
  structure, cadence, subject lines, deliverability hygiene, growth loops and the metrics
  that matter. Use when the user says "start a newsletter", "newsletter ideas", "write this
  week's issue", "our newsletter open rates are falling", "grow our subscriber list",
  "monthly customer update", "digest email", or "newsletter vs blog". Not for automated
  drip flows (use email-lifecycle-sequences) or one-to-one outreach (use cold-outbound-email).
metadata:
  department: "marketing"
  domain: "lifecycle-email"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Newsletter Playbook

A newsletter is a promise: "every <cadence>, you get <specific value> in <N minutes>."
Most fail because the promise is vague, so issues drift into company news nobody asked for.

## 1. Before writing anything

Answer in one line each; if you cannot, stop and fix that first.
1. **Reader**: one role, one problem (e.g. "finance leads at multi-channel e-commerce firms reconciling marketplace payouts").
2. **Promise**: the one thing they get each issue that they cannot get from your blog feed.
3. **Job for the business**: pipeline nurture, retention, authority, or recruiting. Pick one primary; it decides the CTA.
4. **Owner and capacity**: who writes, who approves, what is the real hours-per-issue? Pick a cadence you can hold for 6 months, not 6 weeks. Consistency beats frequency; fortnightly or monthly is right for most B2B teams.
5. **Source of substance**: a recurring input (customer questions, support tickets, product changelog, benchmarks, curated links with your opinion). No input pipeline = no newsletter.

## 2. Pick the format (one, not a mix)

| Format | Best when | Risk |
|---|---|---|
| Single deep-dive | You have genuine expertise on one topic per issue | Heavy to produce |
| Curated digest with commentary | Fast-moving field (tax rules, platform API changes) | Commentary becomes thin; becomes a link dump |
| Q&A / customer-question | Support inbox is rich | Needs permission to use questions; anonymise |
| Product and release notes | Existing customers, retention goal | Reads as self-promotion if nothing else is in it |

## 3. Issue structure (works for any format)

1. **Subject line**: specific, 4-9 words, one idea. Promise the payoff, not the topic. Test two options (see below).
2. **Preview text**: complements the subject, never repeats it; never leave it to default to "View in browser".
3. **Opening (2-3 lines)**: the point of the issue or the problem it solves. No "Hope you are well".
4. **Body**: one main idea, scannable: short paragraphs, 1-2 subheads, one concrete example or number. Plain text-leaning layout; heavy templates reduce replies and can hit Promotions tabs.
5. **One primary CTA**, placed after the value. A secondary soft CTA ("reply with your question") is allowed. Do not run three equal buttons.
6. **Sign-off from a named human** with a monitored reply-to. Replies are your best engagement and deliverability signal.
7. **Footer**: unsubscribe link that works in one click, postal address and sender identity (CAN-SPAM, GDPR/ePrivacy where relevant).

## 4. Subject-line rules

- Specific beats clever: "Why marketplace payouts never match your bank feed" beats "Reconciliation, rethought".
- Avoid spam triggers in volume (all caps, "free!!!", excessive punctuation), but do not over-index on them; engagement history matters more.
- Do not mislead (no fake "Re:"). It lifts opens once and costs trust and complaints.
- Test one variable at a time on a split of at least 1,000 per arm; judge by clicks and replies, not opens (see Metrics).

## 5. Growth loops (ranked by effort for a B2B team)

1. **Capture on high-intent pages**: inline signup on top blog posts and resources, not a generic footer form.
2. **Content upgrade / archive**: offer the best 10 past issues as a bundle for signup.
3. **Customer and partner inclusion**: invite a customer to contribute a quote or a Q&A; they share it.
4. **Sales and CS hand-off**: reps add "subscribe" to follow-ups; only with consent and a clear opt-in.
5. **Referral**: "forward to one colleague" CTA with a subscribe link. Formal reward programs are a later stage.
- Never import purchased lists or scrape addresses. It destroys deliverability and breaks GDPR/CASL rules.

## 6. Deliverability hygiene

- Authenticate the sending domain: SPF, DKIM, DMARC aligned; send from a subdomain separate from transactional mail.
- Confirm new signups (double opt-in) when the list source is open web forms.
- Sunset policy: after 90-120 days with no opens or clicks, send a re-permission email, then suppress non-responders.
- Keep spam-complaint rate below 0.1% and hard bounces below 2%; investigate any spike before the next send.
- Machine opens (Apple Mail Privacy Protection, security scanners) inflate opens; do not use open rate as the success metric.

## 7. Metrics that matter

| Metric | Use | Healthy signal |
|---|---|---|
| Click-to-open and unique click rate | Content relevance | Trend up or flat issue over issue |
| Reply rate | Relationship strength | Any non-zero; track by issue |
| Net subscriber growth | Health | Growth after unsubscribes and suppressions |
| Unsubscribe rate per send | Promise mismatch | Under ~0.3-0.5%; a spike names the issue to study |
| Newsletter-sourced pipeline | Business value | Tag links with UTMs; attribute by account, not by click alone |

Review monthly: top 3 and bottom 3 issues by clicks and replies, then write one rule from each.

## 8. Workflow when asked to "write this week's issue"

1. Confirm reader, promise and the one idea for this issue. If the user gave a topic only, propose the angle first.
2. Draft: subject (3 options), preview text, body, CTA, sign-off.
3. Self-check against section 3, cut any paragraph that does not serve the one idea, read aloud for tone.
4. Output the issue in plain text/markdown plus a short send checklist: UTM on links, plain-text version, test send to two inbox providers, unsubscribe works, send time.

## Do not
- Do not turn the newsletter into a press-release feed.
- Do not change format, voice and cadence every month.
- Do not add tracking pixels or personal data beyond what the privacy notice covers.
- Do not invent statistics or customer quotes; mark placeholders `[VERIFY: source]`.
