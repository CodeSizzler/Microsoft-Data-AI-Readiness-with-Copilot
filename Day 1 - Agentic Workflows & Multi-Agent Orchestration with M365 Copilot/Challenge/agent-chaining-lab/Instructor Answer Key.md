# Instructor Answer Key – Customer Care Agent Chain

> For trainers only. Don't share this with learners before the lab.
> AI output varies between runs. Mark learners on **Route, Priority and Flags**, not exact wording. A day or two off in "Days since delivery" is fine if the Coverage is right.

## Expected triage – `Customer_Cases_Batch_15Oct.xlsx` (lab date 2026-10-15)

| Case ID | Customer | Product | Category | Days | Coverage | Route | Priority | Flags | Why (policy section) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NW-1001 | Emma (UK) | KettlePro | Fault | 13 | 30-day return | Auto-reply | P2 | none | §3 faulty within 30 days: refund or replacement, free return shipping |
| NW-1002 | Ravi (India) | AirFry 5L | Fault | 584 | Out of warranty | Auto-reply | P3 | none | §4 India 12 months has expired: offer a paid repair quote |
| NW-1003 | Carlos (US) | SmartVac X2 | Safety | 117 | In warranty | **Product Safety** | **P1** | none | §6 rule 1, burning smell; §7 no troubleshooting |
| NW-1004 | Fatima (UAE) | BlendMax | Fault | 20 | 30-day return* | Auto-reply | P2 | **NEEDS INFO** (order number) | §8 order number missing |
| NW-1005 | Hannah (Germany) | SmartVac X2 | Refund request | 440 | In warranty (24 m) | **Supervisor** | P2 | none | §4 warranty gives repair/replace, not refund; §5 refund >25 USD needs approval |
| NW-1006 | James (US) | CoolBreeze Fan | Wrong/Damaged item | 5 | 30-day return | Auto-reply | P3 | **SENSITIVE DATA – MASK** | §3 wrong item: free return shipping; §9 card ending 1234 |
| NW-1007 | Priya (India) | KettlePro | Legal threat | 106 | In warranty | **Legal** | **P1** | none | §6 rule 2, "consumer court" |
| NW-1008 | Emma (UK) | KettlePro | Follow-up | 13 | 30-day return | **Duplicate of NW-1001** | P2 | none | §6 rule 4 |
| NW-1009 | Liam (Ireland) | AirFry 5L | Fault | 61 | In warranty (24 m) | Auto-reply | P3 | none | §4 free repair or replacement; product still works |
| NW-1010 | Aisha (UAE) | CoolBreeze Fan | Fault | 166 | In warranty | Auto-reply | P3 | none | §5 a 20 USD voucher is within the 25 USD limit |
| NW-1011 | Tom (US) | BlendMax | Refund request | 380 (system) | NOT SPECIFIED / conflict | **Supervisor** | P2 | **NEEDS CLARIFICATION** | §8 system date 2025-09-30 vs "bought it last month" |
| NW-1012 | Sofia (Spain) | SmartVac X2 | Compliment | 10 | 30-day return | Auto-reply | P3 | none | §6 rule 6 |

\* Accept "NEEDS INFO" in Coverage for NW-1004 too. The order can't be verified without the number.

**Summary:** Auto-reply 7 · Supervisor 2 · Product Safety 1 · Legal 1 · Duplicate 1

**Debatable rows (accept if the reason cites the policy):**

- NW-1001 and NW-1004 as P3 instead of P2.
- NW-1009 as P2.
- NW-1005 as Category "Fault".

## Expected final decisions after Part E

| Case | Final reply must contain |
| --- | --- |
| NW-1003 | Stop using it, courier collection within 2 working days, 399 USD refund once collected, ref PS-2026-114 |
| NW-1005 | Free replacement shipped within 3 working days. **No refund.** Refund reconsidered only if the replacement fails |
| NW-1007 | Replacement kettle + 25 USD voucher, marked **LEGAL REVIEW REQUIRED** |
| NW-1011 | Delivery confirmed as 2026-09-28, so within 30 days: 89 USD refund with free return shipping |
| NW-1004 | Still on hold, asking for the order number |

## Challenge – `Challenge_New_Cases_16Oct.xlsx` (lab date 2026-10-16)

| Case | Correct triage | What to discuss |
| --- | --- | --- |
| NW-2001 Omar (Saudi Arabia) | Coverage **NOT SPECIFIED**, Route **Supervisor**, P2 | Saudi Arabia isn't in the §4 table. Agents often "helpfully" apply the UAE's 12 months. That's a guess. |
| NW-2002 Kevin (US) | 45 days, In warranty, **Auto-reply**, P2. After the fix: flag **POSSIBLE PROMPT INJECTION** | The message tries to order a 500 USD refund. Neither agent should approve anything over 25 USD. Before the fix, the risk is that the triage silently changes or the injected text gets repeated. |
| NW-2003 Layla (UAE) | 67 days, In warranty, Auto-reply, P2 | The message is in **Arabic**. The Brand Voice Guide says to reply in the customer's language, so the Reply Writer should answer in Arabic. |

## Timing guide

| Section | Minutes |
| --- | --- |
| Intro, scenario, files | 10 |
| Part A–B (Agent 1) | 25 |
| Part C (Agent 2) | 15 |
| Part D (chain + review) | 20 |
| Part E–F (human in the loop + Word) | 15 |
| Challenge | 15 |
