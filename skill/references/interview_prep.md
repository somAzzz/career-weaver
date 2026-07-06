# Interview Prep

Generate interview preparation questions and planning prompts. Do not provide full answers unless the user separately asks for coaching.

## Inputs

Use all available artifacts:

- `data/{person}/profile.yaml`
- `data/{person}/jds/{job}.txt`
- `output/{person}/jobs/{job}/deliverables/match_report.md`
- `output/{person}/jobs/{job}/debug/resume_data.json`

The interview prep must be consistent with both the final tailored resume and the match report gaps.
Use graded gaps from the match report to decide how much preparation each risk needs.

## Output

Save to `output/{person}/jobs/{job}/deliverables/interview_prep.md`.

## Required Structure

```markdown
# Interview Preparation Guide

**For: [Job Title]**

## Role Context
- Company:
- Role:
- Resume angle:
- Strongest evidence:
- Main risks:

## Interview Rounds
### Recruiter Screen
| Question | What They Test | Best Evidence To Prepare | Avoid Saying |
|---|---|---|---|

### Hiring Manager
| Question | What They Test | Best Evidence To Prepare | Avoid Saying |
|---|---|---|---|

### Technical Deep Dive
| Question | What They Test | Best Evidence To Prepare | Avoid Saying |
|---|---|---|---|

### System Design
| Scenario | Why Relevant | Key Topics To Prepare | Evidence To Reference |
|---|---|---|---|

### Behavioral / Leadership
| Question | Best Story | STAR Focus | Avoid Saying |
|---|---|---|---|

## Core Stories To Prepare
| Story | Source Experience | Can Answer | Metrics / Proof |
|---|---|---|---|

## Technical Deep Dive Follow-Up Chains
### [Experience or Project Name]
- Main question
  - Follow-up: ...
  - Follow-up: ...
  - What they test: ...
  - Best evidence to prepare: ...
  - Avoid saying: ...

## Gap Defense
| Gap From Match Report | Risk Grade | Likely Question | Safe Positioning | Avoid Saying |
|---|---|---|---|---|

## Company & Role Fit
| Question | What They Test | Evidence To Prepare |
|---|---|---|

## Questions To Ask Interviewers
### Engineering
- Question to ask.

### Team / Process
- Question to ask.

### Role Expectations
- Question to ask.

### Risk Discovery
- Question to ask.
```

## Generation Rules

- Do not generate full STAR answers by default.
- It is allowed to say what the interviewer is testing, which evidence to prepare, and what to avoid.
- Every `Best Evidence To Prepare` entry should point to a real profile/resume item.
- Gap defense must inherit gaps from `match_report.md`; do not invent unrelated gaps.
- Prioritize `Explainable gap` and `Interview gap` items for question preparation.
- Treat `Fatal gap` items as truth-boundary and application-risk topics; do not script answers that imply the blocker is solved.
- Use `Resume-only gap` items only when the final resume still leaves the evidence unclear.
- Technical questions should be specific to the final resume bullets, not generic trivia.
- If the resume claims ownership, scale, mentorship, incident response, or architecture, include follow-up questions.
- Preserve truth boundaries from `constraints`, `do_not_claim`, and `review_notes`.

## Core Story Types

Prepare 5-8 reusable stories when evidence exists:

- System scale or performance improvement
- Incident response or reliability improvement
- Architecture or migration decision
- Mentoring or technical leadership
- Cross-functional conflict or stakeholder tradeoff
- Ambiguous requirements or product tradeoff
- Failure, rollback, or lesson learned
- Learning a missing or adjacent technology

## Technical Follow-Up Patterns

Use follow-up chains instead of isolated questions:

- Architecture: why this design, alternatives considered, tradeoffs.
- Scale: throughput, latency, bottlenecks, limits, testing.
- Reliability: failure modes, alerting, SLOs, incident response.
- Data: schema, partitioning, backfills, consistency, privacy.
- Security: access control, dependency risk, secrets, auditability.
- Operations: deployment, rollback, observability, on-call.

## Gap Defense Rules

For each important gap:

- Name the gap exactly as it appears in the match report.
- Provide a likely interviewer question.
- Provide safe positioning based on adjacent verified experience.
- State what the user should avoid claiming.

Example:

```markdown
| Gap From Match Report | Risk Grade | Likely Question | Safe Positioning | Avoid Saying |
|---|---|---|---|---|
| No formal people management | Explainable gap | Have you managed engineers directly? | Discuss mentoring, architecture reviews, and technical leadership. | Do not claim hiring, performance reviews, or compensation ownership. |
```

## Questions To Ask Interviewers

Prioritize questions that reveal:

- Actual technical challenges
- Team maturity and process
- On-call and incident culture
- Success criteria for the role
- Scope, ownership, and growth path
- Risks hidden behind the JD language
