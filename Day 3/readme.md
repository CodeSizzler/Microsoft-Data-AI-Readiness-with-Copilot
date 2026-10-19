
# Fendt SmartGuide Launch — Hands-on Agent Labs for Microsoft 365 Copilot

Hands-on labs where you build, chain and govern AI agents in **Microsoft 365 Copilot Agent Builder**. Every lab follows one realistic business storyline, so each new skill builds on the last.

No prior experience with Copilot, Agent Builder or AI agents is needed. Every click is spelled out.

## The scenario

AGCO is preparing the pilot launch of **Fendt SmartGuide**, a new autonomous steering-assist feature for the Fendt 900 Vario series. It rolls out first to Brazil, India, Germany and the United States.

Across the labs you follow the launch through one working day. First the engineering spec arrives, then the dealer material goes through compliance review. Later a field issue appears, and the day ends with a leadership decision on how to respond.

## Labs

| # | Lab | What you solve | What you'll practise | Duration |
| --- | --- | --- | --- | --- |
| 1 | [Launch Coordination](labs/lab-1-launch-coordination.md) | Turn messy, partly unresolved engineering notes into an approved, region-ready dealer brief | Structured outputs, ReAct-style tool calling (Human-as-API), multi-agent chaining with @mention, turning agent output into Word and Excel files | ~105 min |
| 2 | [Governance Layer](labs/lab-2-governance-layer.md) | Put a Brazil dealer email through brand and compliance review before it goes out | Separation of concerns, agents that recommend instead of approve, cross-border data risk (LGPD / GDPR), a two-step human sign-off | — |
| 3 | Field Issue Investigation | Investigate a field issue reported by pilot customers | *Coming soon* | — |
| 4 | Incident Response | Run the full incident response and make the final leadership call | *Coming soon* | — |

Do the labs in order: Lab 2 reuses the @mention chaining pattern from Lab 1.

## Key ideas you'll take away

- **Agents that refuse to guess.** Instructions that flag missing or conflicting data instead of making up a value.
- **Structured outputs.** Agents return fixed fields and tables that people and other agents can act on.
- **Simulated tool calling.** An agent asks for data it doesn't have in a set format, and a human answers it (the Human-as-API pattern).
- **Multi-agent chaining.** Specialist agents work in one thread, each improving on the previous agent's output.
- **Human in the loop.** Agents give advice; people make the decisions and record them.

## Prerequisites

- A Microsoft 365 account with **Copilot** access
- Chrome or Edge
- Access to your organisation's **OneDrive**
- The lab input files (Word and Excel), handed out by your session lead. Each lab lists the files it needs.

> **Note:** The links to lab input files point to Google Drive and only open for people who have been given access. The regional compliance notes in Lab 2 are simplified for training and are **not legal advice**.

## Repository structure

```
README.md
labs/
├── lab-1-launch-coordination.md
├── lab-2-governance-layer.md
└── images/
    ├── lab-1/media/   # Lab 1 screenshots
    └── lab-2/media/   # Lab 2 screenshots
```

## Tools used

Microsoft 365 Copilot Chat · Agent Builder · OneDrive · Word · Excel
