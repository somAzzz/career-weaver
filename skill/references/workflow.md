# Workflow

This skill should feel conversational to the user. Translate simple user requests into files and deliverables without exposing internal formats unless the user asks.

## Happy Path

1. User provides a resume.
2. Create `data/{person}/profile.yaml` from the resume. Ask only for essential missing facts.
3. User provides a JD, or explicitly asks for a generic/template-preview resume.
4. Save the JD to `data/{person}/jds/{job}.txt` with `scripts/setup_workflow.py save-jd`.
5. Analyze fit and write `output/{person}/jobs/{job}/deliverables/match_report.md`.
6. Use the match report strategy to create tailored `output/{person}/jobs/{job}/debug/resume_data.json`.
7. Render the PDF with `scripts/render_resume.py`.
8. Optionally create `deliverables/interview_prep.md` from the profile, JD, match report, and final resume JSON.

## Deterministic Conversation Funnel

Use this funnel whenever the user gives an open-ended request such as "help me make a resume" or "use this JD".

### Step 1: Candidate

Goal: select or create `data/{person}/profile.yaml`.

- If the user names a person, use that name to create the slug.
- If exactly one `data/*/profile.yaml` exists, use it without asking.
- If multiple profiles exist, ask: "Which profile should I use?"
- If no profile exists, ask: "Please paste your resume text or provide a resume file path."
- If a profile already exists and the request suggests importing or refreshing career facts, ask: "I found an existing profile. Do you want to update it with new resume/profile material?"

### Step 2: Resume Import

Goal: produce a usable master profile.

- If the user pasted resume text or provided a resume file, follow `references/importing.md`.
- If a usable profile already exists and the user has not provided new resume/profile material, ask whether they want to update it instead of asking them to upload it again.
- If extraction leaves important uncertainty, ask one concise clarification question.
- If the uncertainty is not blocking, write it to `review_notes` and continue.
- Before continuing, run `python scripts/setup_workflow.py validate-profile --file data/{person}/profile.yaml`.
- If validation fails because `profile.target_roles` is missing, ask the user for the position they are applying for.
- If validation fails because `contact.location` contains a full address, postal code, or overly specific location, ask for a short city/state/country-level location only.

### Step 3: JD

Goal: save the full JD exactly once.

- If the user pasted a JD, infer a concise job slug and save it.
- If the user provided a file path, save/copy it with `scripts/setup_workflow.py save-jd`.
- If no JD is available, do not silently create `general_resume`.
- Ask: "Please paste the job description or provide a JD file path. If you want a generic resume instead, say so explicitly."
- Continue without a JD only when the user explicitly asks for a generic resume, sample render, or template preview. In that case use the job slug `general_resume`, skip `match_report.md`, and state that the resume is not tailored to a job.
- Even for generic resumes, the user's target position is required in `profile.target_roles` and the resume `role`.

### Step 4: Output Choice

Ask only if the desired output is unclear:

```text
What should I generate?
1. Match analysis only
2. Tailored resume PDF only
3. Match analysis + tailored resume PDF
4. Full package: match analysis + resume PDF + interview prep
```

Default to option 4 when the user says "full pipeline", "apply to this job", or "analyze and generate".

### Step 5: Run Scope And Reuse Choice

Ask before generating when prior job outputs, JDs, match reports, resume JSON files, or helper scripts exist and the user's intended scope is not explicit:

```text
How should I use existing materials?
1. New JD / new tailored resume
2. Reuse an existing JD and regenerate from profile + JD
3. Reuse existing match strategy / resume data
4. Generic resume without JD tailoring
```

Do not silently copy old `match_report.md`, old `debug/resume_data.json`, or run historical helper scripts such as `work/build_*.py`. Existing artifacts are inputs only when the user explicitly chooses reuse.

For a new JD, always create or refresh `match_report.md` and `debug/resume_data.json` from `profile.yaml` + the selected JD. For a generic resume, skip `match_report.md`, use `general_resume`, and state that no JD tailoring was performed.

### Step 6: Photo Choice

Ask before rendering any resume PDF unless the user already made an explicit photo/no-photo choice in the current request. This happens before final template selection so the agent cannot silently choose a no-photo template to avoid the question.

```text
Photo option?
1. No photo version
2. Use existing photo
3. Add a new photo
4. Generate both photo and no-photo versions
```

If the user chooses a photo option, use a photo-capable template such as `luxsleek`, `engineer_with_photo`, or a custom template that renders `photo.filename`.
Default to no-photo for US roles only after the user answers or explicitly asks Codex to choose defaults.

### Step 7: Language Choice

Ask only if the target resume language is unclear:

```text
目标简历语言用哪一种？
1. English
2. Deutsch
3. Français
4. 中文
```

Default to the JD language when it is obvious. Keep interacting with the user in Chinese when the user uses Chinese, even if the resume output is German, French, or English. See `references/localization.md`.

### Step 8: Template Choice

Ask before rendering any resume PDF unless the user already specified a template or explicitly asked Codex to choose defaults. List available templates first:

```bash
python scripts/setup_workflow.py list-templates
```

Then ask:

```text
Which resume template should I use?
1. engineer
2. engineer_with_photo
3. luxsleek
```

If `list-templates` shows different templates, use that list instead. Do not silently use the default `engineer` template.

### Step 9: Version Matrix

Ask before generating multiple PDFs unless the requested matrix is explicit:

```text
Which versions should I generate?
1. One template, no photo
2. One template, with photo
3. Both photo and no-photo for one template
4. Custom matrix, e.g. engineer no-photo + luxsleek with-photo
```

Do not infer a multi-version matrix from prior outputs. If separate output directories are needed, create them only after the user confirms the exact versions.

### Step 10: Finish

Generate the selected artifacts. In the final reply, list only files in `deliverables/` plus any blockers or review notes that matter.

## User Request Routing

### "Import my resume"

Read `references/importing.md`. Extract facts from the supplied text or file and create `data/{person}/profile.yaml`. Include `review_notes` for uncertain or missing facts.
Validate the result with `python scripts/setup_workflow.py validate-profile --file data/{person}/profile.yaml`.

### "Here is a JD"

Save the JD with:

```bash
python scripts/setup_workflow.py save-jd --person "{person}" --job "{job}" --file path/to/jd.txt
```

For pasted JD text, write the text to stdin or a temporary text file, then run the script. Create the job output directory at the same time.

### "Analyze this job"

1. Read `data/{person}/profile.yaml`.
2. Read `data/{person}/jds/{job}.txt`.
3. Parse JD requirements into must-have, nice-to-have, responsibilities, hidden signals, and red flags.
4. Compare JD requirements against verified profile facts and constraints.
5. Build evidence-backed scoring, keyword coverage, gaps, do-not-claim boundaries, and resume strategy.
6. Save `output/{person}/jobs/{job}/deliverables/match_report.md` using `references/report_schema.md`.

### "Generate my resume"

1. Read the profile.
2. Validate the profile with `python scripts/setup_workflow.py validate-profile --file data/{person}/profile.yaml`; if the target position or resume-safe short location is missing, ask for it before continuing.
3. If no JD is available, ask for a JD unless the user explicitly requested a generic resume, sample render, or template preview.
4. If prior job outputs or helper scripts exist and the user has not chosen reuse, ask the Run Scope And Reuse Choice question. Do not copy old `match_report.md` or `resume_data.json` by default.
5. For JD-targeted resumes, read the selected JD. Generate or refresh `match_report.md` from the current `profile.yaml` + JD unless the user explicitly chose to reuse an existing strategy.
6. Treat `match_report.md` as the strategy source for summary angle, experience priority, project priority, skills priority, gaps, and do-not-claim boundaries.
7. For generic resumes, use the strongest broad profile facts, skip fit scoring, use the job slug `general_resume`, and state that no JD tailoring was performed.
8. Select the strongest relevant facts from the profile.
9. Generate a factual summary.
10. Create a fresh `output/{person}/jobs/{job}/debug/resume_data.json` using `references/resume_schema.md` unless the user explicitly chose to reuse existing resume data.
11. If the target resume language is not English, apply `references/localization.md`.
12. Ask the photo choice before rendering if the user has not already made an explicit photo/no-photo decision. Do this before final template selection.
13. Ask the template choice before rendering if the user has not already selected a template. Do not silently default to `engineer`.
14. If multiple PDFs are requested, ask for the exact version matrix unless already explicit.
15. Use short city/state/country-level `contact.location` or `contact.display_location` for the rendered resume; do not put full street addresses in compact template headers unless the user explicitly asks.
16. Render:

```bash
python scripts/render_resume.py --output output/{person}/jobs/{job}
```

Use `--template engineer_with_photo` or `--template luxsleek` when `photo.filename` is present and the user wants a photo version.

### "Use this photo"

Copy the photo with:

```bash
python scripts/setup_workflow.py add-photo --person "{person}" --file path/to/photo.jpg
```

When generating a photo resume, include:

```json
"photo": {"filename": "profile_photo.jpg"}
```

### "Prepare me for the interview"

1. Read `data/{person}/profile.yaml`.
2. Read `data/{person}/jds/{job}.txt`.
3. Read `output/{person}/jobs/{job}/deliverables/match_report.md`.
4. Read `output/{person}/jobs/{job}/debug/resume_data.json`.
5. Generate `output/{person}/jobs/{job}/deliverables/interview_prep.md` using `references/interview_prep.md`.

Generate questions, what-they-test notes, best evidence to prepare, and avoid-saying guidance. Do not generate full answers unless the user asks for coaching.

## Information Dependency

Career Weaver should preserve this strategy chain:

```text
profile.yaml + JD
      ↓
match_report.md
      ↓
debug/resume_data.json
      ↓
deliverables/{person}_{job}_resume.pdf
      ↓
deliverables/interview_prep.md
```

- `match_report.md` determines resume strategy.
- `debug/resume_data.json` should implement that strategy without inventing facts.
- `interview_prep.md` should inherit final resume claims and match report gaps.
- Prior outputs are not the source of truth for a new run. Treat them as reusable only after explicit user confirmation.

## Output Layout

Use this layout for every generated job:

```text
output/{person}/jobs/{job}/
  deliverables/       # files users should open or send
    {person}_{job}_resume.pdf
    match_report.md
    interview_prep.md
  debug/              # reproducibility and troubleshooting
    resume_data.json
    tailored_resume.tex
    tailored_resume.log
    tailored_resume.aux
    tailored_resume.out
    developercv.cls
```

## Response Style

Keep user-facing replies simple:

- Say what was created.
- List the 1-3 files the user should open.
- Mention only important uncertainties or blockers.

Example:

```text
Done. I saved the JD, generated the match report, and rendered the resume.

Open:
- output/alex_chen/jobs/senior_backend_engineer/deliverables/alex_chen_senior_backend_engineer_resume.pdf
- output/alex_chen/jobs/senior_backend_engineer/deliverables/match_report.md
```

## Cross-Platform Notes

- Use Python scripts for setup and rendering instead of shell-specific loops.
- Avoid POSIX-only commands in reusable instructions.
- Use `scripts/render_resume.py --engine auto` by default so the renderer can choose `pdflatex` or Tectonic.
- If no LaTeX engine is available, report the missing dependency and preserve `debug/tailored_resume.tex`.
