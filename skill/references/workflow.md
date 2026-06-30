# Workflow

This skill should feel conversational to the user. Translate simple user requests into files and deliverables without exposing internal formats unless the user asks.

## Happy Path

1. User provides a resume.
2. Create `data/{person}/profile.yaml` from the resume. Ask only for essential missing facts.
3. User provides a JD.
4. Save the JD to `data/{person}/jds/{job}.txt` with `scripts/setup_workflow.py save-jd`.
5. Analyze fit and write `output/{person}/jobs/{job}/deliverables/match_report.md`.
6. Create tailored `output/{person}/jobs/{job}/debug/resume_data.json`.
7. Render the PDF with `scripts/render_resume.py`.
8. Optionally create `deliverables/interview_prep.md`.

## Deterministic Conversation Funnel

Use this funnel whenever the user gives an open-ended request such as "help me make a resume" or "use this JD".

### Step 1: Candidate

Goal: select or create `data/{person}/profile.yaml`.

- If the user names a person, use that name to create the slug.
- If exactly one `data/*/profile.yaml` exists, use it without asking.
- If multiple profiles exist, ask: "Which profile should I use?"
- If no profile exists, ask: "Please paste your resume text or provide a resume file path."

### Step 2: Resume Import

Goal: produce a usable master profile.

- If the user pasted resume text or provided a resume file, follow `references/importing.md`.
- If extraction leaves important uncertainty, ask one concise clarification question.
- If the uncertainty is not blocking, write it to `review_notes` and continue.

### Step 3: JD

Goal: save the full JD exactly once.

- If the user pasted a JD, infer a concise job slug and save it.
- If the user provided a file path, save/copy it with `scripts/setup_workflow.py save-jd`.
- If no JD is available, ask: "Please paste the job description or provide a JD file path."

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

### Step 5: Photo Choice

Ask only if the user mentions a photo, a photo file exists, or the target market commonly expects photo variants:

```text
Photo option?
1. No photo version
2. Use existing photo
3. Add a new photo
4. Generate both photo and no-photo versions
```

Default to no-photo for US roles unless the user asks otherwise.

### Step 6: Language Choice

Ask only if the target resume language is unclear:

```text
目标简历语言用哪一种？
1. English
2. Deutsch
3. Français
4. 中文
```

Default to the JD language when it is obvious. Keep interacting with the user in Chinese when the user uses Chinese, even if the resume output is German, French, or English. See `references/localization.md`.

### Step 7: Finish

Generate the selected artifacts. In the final reply, list only files in `deliverables/` plus any blockers or review notes that matter.

## User Request Routing

### "Import my resume"

Read `references/importing.md`. Extract facts from the supplied text or file and create `data/{person}/profile.yaml`. Include `review_notes` for uncertain or missing facts.

### "Here is a JD"

Save the JD with:

```bash
python scripts/setup_workflow.py save-jd --person "{person}" --job "{job}" --file path/to/jd.txt
```

For pasted JD text, write the text to stdin or a temporary text file, then run the script. Create the job output directory at the same time.

### "Analyze this job"

1. Read `data/{person}/profile.yaml`.
2. Read `data/{person}/jds/{job}.txt`.
3. Compare JD requirements against verified profile facts and constraints.
4. Save `output/{person}/jobs/{job}/deliverables/match_report.md` using `references/report_schema.md`.

### "Generate my resume"

1. Read the profile, JD, and match report if present.
2. Select the strongest relevant facts from the profile.
3. Generate a tailored factual summary.
4. Create `output/{person}/jobs/{job}/debug/resume_data.json` using `references/resume_schema.md`.
5. If the target resume language is not English, apply `references/localization.md`.
6. Render:

```bash
python scripts/render_resume.py --output output/{person}/jobs/{job}
```

Use `--template assets/templates/engineer/engineer_with_photo.tex.jinja2` when `photo.filename` is present and the user wants a photo version.

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

Read the JD and generated `resume_data.json`, then save `output/{person}/jobs/{job}/deliverables/interview_prep.md`. Generate questions only, not answers. See `references/interview_prep.md`.

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
- If `pdflatex` is missing, report the missing dependency and preserve `debug/tailored_resume.tex`.
