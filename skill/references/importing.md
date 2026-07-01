# Importing User Inputs

Use this reference when the user provides a raw resume, a JD, or a photo.

## Resume Import

The user may paste resume text or point to a local `.txt`, `.md`, `.pdf`, `.docx`, or image/PDF export. Extract only facts present in the source.

Create or update:

```text
data/{person}/profile.yaml
```

Recommended profile sections:

- `profile`: name, headline, summary, target roles, availability, work authorization
- `contact`: email, phone, location, links
- `preferences`: locations, work style, industries
- `experience`: company, role, location, period, description, technologies, achievements, leadership examples
- `projects`: name, role, period, description, tech stack, links, highlights
- `skills`: category + items
- `education`
- `certifications`
- `publications_and_talks`
- `languages`
- `constraints`: `do_not_claim` and weak/transferable areas
- `review_notes`: uncertain or missing facts to confirm

Rules:

- Do not infer missing dates, metrics, team sizes, tools, degrees, or certifications.
- Preserve uncertainty in `review_notes`.
- If an existing profile exists, ask whether the user wants to update it instead of asking them to upload a profile again.
- When updating an existing profile, merge carefully and do not delete facts unless the user asks.
- If the user provides a PDF or DOCX and the local environment cannot extract it, ask for pasted text or a text export.

## JD Import

When the user pastes a JD, identify a concise job slug from role/company/context. Then save the JD:

```bash
python scripts/setup_workflow.py save-jd --person "{person}" --job "{job}" --file path/to/jd.txt
```

For direct pasted text, the agent may write it to a temporary text file or pass it through stdin. Preserve the full JD text; do not summarize it in the JD file.

Create the job output directory:

```text
output/{person}/jobs/{job}/deliverables/
output/{person}/jobs/{job}/debug/
```

## Photo Import

When the user provides a headshot:

```bash
python scripts/setup_workflow.py add-photo --person "{person}" --file path/to/photo.jpg
```

Then include the copied filename in `debug/resume_data.json` only when generating a photo resume:

```json
"photo": {"filename": "profile_photo.jpg"}
```

Generate both versions when the user is unsure:

- no-photo default template
- photo template: `assets/templates/engineer/engineer_with_photo.tex.jinja2`

## Minimal Clarifying Questions

Ask only when necessary:

- Which existing profile should I use?
- Is this a new JD or replacing an existing JD?
- Do you want a photo version, no-photo version, or both?
- I found missing/ambiguous facts that affect truthfulness. Can you confirm them?
