# Sample Data

This directory contains fictional sample content for testing the Career Weaver skill.

## Profiles

- `alex_chen/profile.yaml`: Rich senior backend/platform engineer profile with enough evidence for tailoring, gap analysis, interview prep, and no-fabrication checks.

## Job Description Test Cases

- `alex_chen/jds/senior_backend_engineer.txt`: Strong match for backend, APIs, AWS, PostgreSQL, Kafka, CI/CD, and mentoring.
- `alex_chen/jds/tech_lead.txt`: Strong match for hands-on technical leadership and developer platform work.
- `alex_chen/jds/platform_engineer_observability.txt`: Strong match for Kubernetes, SLOs, incident response, Prometheus, Grafana, and developer tools.
- `alex_chen/jds/ml_platform_engineer.txt`: Partial match that should emphasize inference infrastructure and data pipelines while avoiding model-research claims.
- `alex_chen/jds/engineering_manager_platform.txt`: Intentional mismatch for testing gap reporting; Alex has technical leadership but not formal people management.

Use these cases to test whether agents can select evidence, avoid fabrication, identify gaps, and produce different resumes from the same master profile.
