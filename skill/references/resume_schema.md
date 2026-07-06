# Resume JSON Contract

Create `output/{person}/jobs/{job}/debug/resume_data.json` as plain JSON. Do not pre-escape LaTeX characters; `scripts/render_resume.py` escapes text fields.

## Required Root Fields

```json
{
  "name": "Full Name",
  "role": "Target Role",
  "contact": {
    "email": "email@example.com",
    "phone": "+1 555 123 4567",
    "location": "City, Country",
    "display_location": "City, Country",
    "github": "https://github.com/user",
    "linkedin": "https://linkedin.com/in/user"
  },
  "target_language": "en",
  "labels": {
    "summary": "Summary",
    "skills": "Skills",
    "experience": "Experience",
    "projects": "Projects",
    "research": "Research Projects",
    "education": "Education",
    "languages": "Languages"
  },
  "summary": "Tailored factual summary.",
  "skills": {
    "Languages": ["Python", "Go"],
    "Cloud & DevOps": ["AWS", "Docker", "Kubernetes"]
  },
  "experience": [
    {
      "company": "Company",
      "role": "Role",
      "date": "2021 - Present",
      "description": "Optional role focus.",
      "bullets": ["Achievement with metric."],
      "tags": ["Python", "AWS"]
    }
  ],
  "projects": [],
  "research": [],
  "education": [
    {
      "school": "University",
      "degree": "M.S.",
      "major": "Computer Science",
      "date": "2016 - 2018",
      "thesis": "Optional thesis"
    }
  ],
  "certifications": [
    {
      "name": "Certification",
      "issuer": "Issuer",
      "date": "2024",
      "description": "Optional focus"
    }
  ],
  "languages": [
    {"name": "English", "level": "Fluent"}
  ],
  "hobbies": "Optional short personal-interest line for templates that support it.",
  "photo": {
    "filename": "profile_photo.jpeg"
  }
}
```

## Rules

- Required: `name`, `role`, `contact.email`, `contact.location`, `summary`, non-empty `skills`, non-empty `experience`, and `education`.
- Optional: `contact.phone`, `contact.display_location`, `github`, `linkedin`, `projects`, `research`, `certifications`, `languages`, `hobbies`, `photo`.
- Optional but recommended for multilingual output: `target_language` and `labels`.
- Generate this JSON from verified `profile.yaml` facts and the target JD. Do not use JD-only claims as resume facts.
- `role` must be the target position the user is applying for. Do not use an empty, TODO, unknown, or placeholder role.
- Use a short, non-specific city/state/country-level location for resume display, for example `San Francisco, CA` or `Germany - Berlin`. Do not render full street addresses unless the user explicitly asks.
- When `match_report.md` is available, make the summary, first listed skills, first experience description, and earliest bullets implement its recruiter first-screen plan.
- The primary candidate positioning label should be visible through the `role`, `summary`, and highest-priority bullets without copying unsupported language.
- Resume-only gaps from the match report should be fixed by surfacing existing verified evidence; fatal or unsupported gaps must not be hidden with vague wording.
- If the target language is not English, translate resume-facing text and localize `labels`; preserve company names, product names, metrics, and technologies.
- Keep bullets concise and evidence-backed. Prefer 2-5 bullets per role.
- Use `date` consistently; templates render it exactly as provided.
- Use `photo.filename` only when the selected template includes a photo.
- The LuxSleek template (`assets/templates/luxsleek/luxsleek.txt`) uses a left sidebar for identity, photo, contact, languages, and a concise skills list. Summary renders in the main flow so long profile text can paginate. It can also render `certifications`, `hobbies`, and `photo.filename`.
