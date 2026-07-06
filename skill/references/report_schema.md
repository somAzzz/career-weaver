# Match Report

Write match reports to `output/{person}/jobs/{job}/deliverables/match_report.md`.

The match report is the strategy source for the tailored resume and interview prep. It must be evidence-first, reproducible, and honest about gaps.

## Required Structure

```markdown
# Resume-JD Match Report

## Overall Score: XX/100

## Executive Summary
Short assessment of fit, strongest angle, and biggest risk.

## JD Intent Analysis
### Likely Hiring Need
- Business, product, team, or operational problem this role appears designed to solve.

### Why This JD Is Structured This Way
- Why the must-have requirements, responsibilities, and seniority signals are emphasized.

### Hidden Priorities
- Unstated priorities implied by the JD language, ordering, tools, domain, stakeholders, or delivery context.

### Candidate Positioning Implication
- How the candidate should position verified experience in response to the likely hiring need.

## Role Archetype
| Archetype | Confidence | JD Signals | Resume Implication |
|---|---|---|---|
| Builder / Maintainer / Scale / Migration / Leadership / Rescue / Hybrid | High/Medium/Low | Explicit or inferred JD signals. | What verified evidence should move forward or recede. |

## Layered Requirements
| Requirement | Layer | Gate Severity | Evidence Needed | Candidate Status | Scoring Impact |
|---|---|---|---|---|---|

## Candidate Positioning
### Primary Positioning Label
- Concise recruiter-facing label grounded in verified profile evidence.

### Alternative Positioning
- Backup positioning if the primary angle is weakened by a gap.

### Positioning To Avoid
- Framing that would overclaim, mismatch the role archetype, or trigger avoidable screening risk.

## Application Recommendation
| Decision | Confidence | Why | Required Changes Before Applying | Best Channel |
|---|---|---|---|---|
| Strong apply / Apply with tailoring / Referral first / Low priority / Do not apply | High/Medium/Low | Evidence-based rationale. | Top 3 changes or blockers. | Direct / Referral / Recruiter outreach / Do not apply yet |

## Recruiter First-Screen Optimization
### 10-Second Impression
- What a recruiter should understand almost immediately.

### Above-The-Fold Must Show
1. Verified fact, keyword, metric, or role signal that should appear early in the resume.

### Keywords To Surface Early
- Supported JD keyword or seniority signal.

### Content To De-Emphasize
- Lower-relevance content that could dilute the first screen.

## Scoring Rubric
| Dimension | Max | Score | Evidence |
|---|---:|---:|---|
| Must-have skills | 30 |  |  |
| Relevant experience | 25 |  |  |
| Domain/context fit | 15 |  |  |
| Seniority/ownership | 15 |  |  |
| Language/location/work authorization | 10 |  |  |
| Bonus/nice-to-have signals | 5 |  |  |

## JD Requirement Map
| Requirement | Type | Layer | Importance | Evidence From Profile | Strength | Gap | Resume Action |
|---|---|---|---|---|---|---|---|

## Evidence-Based Fit Analysis
| JD Requirement | Profile Evidence | Evidence Source | Strength | Resume Action |
|---|---|---|---|---|

## Keyword Coverage
| Keyword | JD Importance | In Profile | In Resume Draft | Action |
|---|---|---|---|---|

## Strongest Selling Points
- Evidence-backed selling point.

## Graded Gaps And Risks
| Gap | Risk Grade | Severity | Likely Screening Impact | Mitigation |
|---|---|---|---|---|

## Do Not Claim
- Claim that must not appear in the resume unless the user provides evidence.

## Resume Strategy
### Summary Angle
Recommended positioning for the resume summary.

### First-Screen Plan
- How to make the primary positioning label, strongest evidence, and critical keywords visible in the first resume scan.

### Experience Priority
1. Experience to emphasize and why.

### Project Priority
1. Project to include/exclude and why.

### Skills Priority
- Skills to promote, group, translate, or omit.

### Bullet Rewrite Guidance
- How to rewrite bullets using verified evidence and JD language.

## Recommended Next Action
1. Specific action before generating or revising the resume.
```

## Scoring Rules

- Total score must equal the sum of the scoring rubric rows.
- Do not award full points for a requirement unless there is explicit profile evidence.
- Penalize missing must-have requirements more heavily than missing nice-to-have items.
- Treat missing `Legal gate` and critical `Core technical gate` requirements as high-impact risks even when the rest of the profile is strong.
- Do not let missing `Cosmetic keyword` items materially lower the score when stronger adjacent evidence exists.
- Mark unclear but potentially true claims as gaps or review items; do not treat them as evidence.
- If `constraints`, `do_not_claim`, or `review_notes` conflict with the JD, reflect that in `Graded Gaps And Risks` and `Do Not Claim`.

## Requirement Types

Use these values in `JD Requirement Map`:

- `Must-have`: required skill, language, location, authorization, experience, or credential.
- `Nice-to-have`: preferred or bonus requirement.
- `Responsibility`: work the candidate will perform.
- `Hidden signal`: implicit expectation such as ownership, regulated domain, on-call maturity, writing, or stakeholder communication.
- `Red flag`: requirement or context that may expose a serious gap.

## Requirement Layers

Use these values in `Layered Requirements` and the `Layer` column of `JD Requirement Map`:

- `Legal gate`: work authorization, location, language, license, credential, or compliance requirement that can block the application regardless of technical fit.
- `Core technical gate`: skill, domain, or experience requirement central to doing the job.
- `Experience gate`: seniority, ownership, people leadership, project scale, or years-of-experience expectation.
- `Strong filter`: important preference that materially improves screening odds but may be compensated by adjacent evidence.
- `Tie-breaker`: nice-to-have signal that differentiates otherwise similar candidates.
- `Cosmetic keyword`: low-signal wording, buzzword, or tool mention that should not dominate scoring.

## JD Intent Analysis Rules

- Infer hiring need only from the JD text, role title, company/team context provided by the user, and common role-design logic.
- Clearly distinguish inference from explicit JD statements.
- Explain why requirements are likely included, not only whether the candidate matches them.
- Do not overfit to one keyword; use requirement clusters, repeated themes, responsibility order, and seniority signals.
- Connect intent analysis to resume strategy: what angle to emphasize, what evidence to foreground, and which risks to avoid.
- If the JD is too generic to infer intent confidently, say so and list the strongest weak signals.

## Role Archetype Rules

- Choose the dominant archetype from the JD's responsibility mix, seniority signals, repeated verbs, system context, and success metrics.
- Use `Hybrid` when two archetypes are genuinely central; do not force a single archetype when the JD combines, for example, scale and migration.
- Explain the resume implication in terms of verified facts to emphasize, not unsupported claims to add.

## Candidate Positioning Rules

- The primary positioning label should read like a recruiter shorthand, for example `Senior backend engineer with platform reliability depth`.
- Ground every positioning label in profile evidence and the role archetype.
- The `Positioning To Avoid` section must protect against overclaiming, irrelevant seniority framing, or a misleading transition story.

## Application Recommendation Rules

- Use one decision value: `Strong apply`, `Apply with tailoring`, `Referral first`, `Low priority`, or `Do not apply`.
- `Strong apply` requires strong evidence for legal gates, core technical gates, and the dominant role archetype.
- Use `Apply with tailoring` when the candidate is viable but the resume must be reshaped before applying.
- Use `Referral first` when the candidate has explainable gaps that a human introduction or context could help overcome.
- Use `Low priority` when gaps are meaningful but not necessarily disqualifying.
- Use `Do not apply` when a legal gate, non-negotiable credential, location/work authorization requirement, or core role expectation is unsupported and unlikely to be resolved.
- Required changes before applying must be specific and limited to the top 3 actions.

## Recruiter First-Screen Rules

- Optimize for a 10-30 second scan by a recruiter who may not read every bullet.
- The primary positioning label, strongest verified evidence, and critical supported JD keywords should appear early in the resume.
- Above-the-fold recommendations must not require unsupported claims or keyword stuffing.
- De-emphasize content that is truthful but weakly related to the role archetype or screening gates.

## Risk Grade Rules

Use these values in `Graded Gaps And Risks`:

- `Fatal gap`: likely to block the application or fail screening unless resolved before applying.
- `Explainable gap`: real gap that can be mitigated with adjacent verified evidence, positioning, referral context, or interview preparation.
- `Resume-only gap`: evidence may exist in the profile but is not visible enough in the tailored resume.
- `Interview gap`: resume may pass screening, but the topic is likely to be probed in interviews.

Do not soften legal or credential gaps into explainable gaps unless the JD clearly allows alternatives.

## Evidence Rules

- Every positive fit claim must cite evidence from `profile.yaml`.
- `Evidence Source` should name the company/project/education/certification section, not just a generic skill.
- Example: `TechCorp Inc. - Kafka ingestion platform handling 1.4M events/day`.
- JD text alone is never evidence that the candidate has a skill.

## Keyword Rules

- Include must-have keywords, seniority signals, domain terms, tools, frameworks, languages, and location/language requirements.
- `In Resume Draft` can be `Yes`, `No`, or `Not generated yet`.
- If a keyword is not supported by profile evidence, the action should be `Do not add unless user confirms evidence`.

## Resume Strategy Rules

- Strategy must be executable: what to emphasize, what to remove, what to rewrite, and what to avoid.
- Resume strategy must reflect the role archetype, layered requirements, and primary candidate positioning label.
- Resume strategy must implement recruiter first-screen optimization before lower-priority content.
- Explainable and interview gaps should feed into interview preparation; fatal gaps should feed into application recommendation.
- Do not recommend adding unsupported skills or claims.
- If the target resume language differs from the profile language, include localization guidance for role titles, section labels, and JD keywords.
