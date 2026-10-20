---
name: fault-diagnosis-report
description: Use when a technician or dispatcher reports an equipment fault (HVAC HX-200, generator PG-50 or cold room CX-10) and needs a diagnosis, parts, cost and priority. Produces a structured Fault Diagnosis Report. Do not use for general product questions or for customer-facing replies.
---

# Fault Diagnosis Report

## When to use
- Someone describes a fault, a symptom or a fault code on a Northwind asset.
- Someone asks "what's wrong with…", "what part do I need…", "diagnose…".

## Steps
1. **Safety first.** If the report mentions smoke, fire, sparks, burning smell, gas/refrigerant smell, fuel leak, electric shock or injury,
   STOP. Output only the "STOP-WORK – ESCALATE NOW" block from the Field Safety & Escalation SOP. Do not diagnose.
2. **Identify the asset.** If there is no asset ID (AST-####), ask for it and stop. Never guess.
3. **Look up the asset** with the `get_asset` tool: model, customer, warranty end date, service plan.
4. **Diagnose** using the service manual for that model: match the fault code or symptom to the likely cause.
5. **Parts.** Use `find_parts_for_model` and `check_part_stock` for each likely part. Note the city stock for the asset's city.
6. **Technician.** Use `find_technician` with the asset's city and model.
7. **Cost and approval.** In warranty → "No charge to customer". Out of warranty → parts at list price + 85 USD/hour labour
   (use the standard repair time from the manual). If parts cost more than 500 USD → "Service Manager approval required".
8. **Priority** using the SOP rules (P1 / P2 / P3) and the target response time from the service plan.

## Output format
### Fault Diagnosis Report – <Asset ID>
| Field | Value |
|---|---|
| Customer / site | |
| Model | |
| Reported symptom / code | |
| Likely cause | |
| Parts needed (stock in city) | |
| Warranty | In warranty until … / Expired on … |
| Estimated cost to customer | |
| Approval needed | Yes / No – reason |
| Priority & target response | |
| Suggested technician | name, next free slot |

**Next steps:** 2–3 bullet points.

## Guardrails
- Cite the manual or SOP section you used.
- If a tool returns an error, say so plainly. Don't invent stock or technician data.
