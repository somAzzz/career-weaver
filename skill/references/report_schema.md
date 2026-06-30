# Match Report

Write match reports to `output/{person}/jobs/{job}/deliverables/match_report.md`.

The match report is the strategy source for the tailored resume and interview prep. It must be evidence-first, reproducible, and honest about gaps.

## Required Structure

```markdown
# Resume-JD Match Report

## Overall Score: XX/100

## Executive Summary
Short assessment of fit, strongest angle, and biggest risk.

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
| Requirement | Type | Importance | Evidence From Profile | Strength | Gap | Resume Action |
|---|---|---|---|---|---|---|

## Evidence-Based Fit Analysis
| JD Requirement | Profile Evidence | Evidence Source | Strength | Resume Action |
|---|---|---|---|---|

## Keyword Coverage
| Keyword | JD Importance | In Profile | In Resume Draft | Action |
|---|---|---|---|---|

## Strongest Selling Points
- Evidence-backed selling point.

## Gaps And Risks
| Gap | Severity | Mitigation |
|---|---|---|

## Do Not Claim
- Claim that must not appear in the resume unless the user provides evidence.

## Resume Strategy
### Summary Angle
Recommended positioning for the resume summary.

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
- Mark unclear but potentially true claims as gaps or review items; do not treat them as evidence.
- If `constraints`, `do_not_claim`, or `review_notes` conflict with the JD, reflect that in `Gaps And Risks` and `Do Not Claim`.

## Requirement Types

Use these values in `JD Requirement Map`:

- `Must-have`: required skill, language, location, authorization, experience, or credential.
- `Nice-to-have`: preferred or bonus requirement.
- `Responsibility`: work the candidate will perform.
- `Hidden signal`: implicit expectation such as ownership, regulated domain, on-call maturity, writing, or stakeholder communication.
- `Red flag`: requirement or context that may expose a serious gap.

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
- Do not recommend adding unsupported skills or claims.
- If the target resume language differs from the profile language, include localization guidance for role titles, section labels, and JD keywords.
