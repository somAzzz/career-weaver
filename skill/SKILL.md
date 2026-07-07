---
name: career-weaver
description: End-to-end multilingual resume workflow for importing a user's resume into profile.yaml, saving job descriptions, adding profile photos, analyzing JD fit, translating/localizing resume content into a target language, generating tailored technical resumes/CVs, rendering LaTeX PDFs, and preparing interview questions. Use when the user wants to import a resume, paste a JD, generate a resume, make a photo/no-photo version, analyze fit, translate a resume into German/French/English/another language, or prepare for interviews in Codex or another coding-agent environment across Windows, macOS, and Linux.
---

# Career Weaver

Turn raw user materials into job-specific resume deliverables. The user should not need to know YAML, JSON, LaTeX, or the folder structure.

## User-First Commands

When the user says one of these, perform the matching workflow:

- "Here is my resume" / "Import my resume": create or update `data/{person}/profile.yaml`.
- "Here is a JD" / "Analyze this job": save the JD to `data/{person}/jds/{job}.txt`, create the job folder, and write `deliverables/match_report.md`.
- "Generate my resume": create `debug/resume_data.json`, render the PDF, and put the final PDF in `deliverables/`.
- "Use this photo": copy the image into `data/{person}/` and generate a photo resume when requested.
- "Add this resume template" / "Use this template": add, list, or select templates using `references/templates.md`.
- "Prepare me for the interview": write question-only interview prep to `deliverables/interview_prep.md`.
- "Generate a German/French/English resume": translate and localize the generated resume into the target language while preserving verified facts.

Read `references/workflow.md` for the full flow. Read `references/importing.md` when importing raw resumes, JDs, or photos. Read `references/localization.md` when the profile language and target resume language differ.
Read `references/templates.md` when adding, listing, choosing, or previewing resume templates.

## Conversation Flow

Use a deterministic question funnel when the user's request is underspecified. Ask at most one short question at a time. Skip any step already answered by the user's message or existing files.

1. **Candidate**: Identify the person/profile.
   - If exactly one profile exists, use it.
   - If no profile exists, ask the user to paste a resume or provide a file path.
   - If multiple profiles exist, ask which one to use.
2. **Resume Import**: If profile data is missing or stale, import/update `profile.yaml`.
   - If a profile already exists, do not ask the user to upload a profile again. Ask whether they want to update the existing profile.
   - Do not ask the user about YAML.
   - Ask only about facts that affect truthfulness, such as missing dates, unclear employers, or ambiguous metrics.
   - Validate the result with `python scripts/setup_workflow.py validate-profile --file data/{person}/profile.yaml`.
   - `profile.target_roles` must include at least one target position the user is applying for.
   - `contact.location` must stay short and non-specific, such as city/state/country-level text; do not store full street addresses or postal details.
3. **Job Description**: Save the JD.
   - If the user pasted a JD, infer a job slug and save it.
   - If no JD is available, ask the user to paste the JD or provide a file path.
   - Do not create `general_resume` unless the user explicitly asks for a generic resume, sample render, or template preview.
4. **Run Scope**: Ask before generating when prior job outputs, JDs, match reports, or resume JSON files exist and the user's intended scope is not explicit.
   1. New JD / new tailored resume
   2. Reuse an existing JD and regenerate from profile + JD
   3. Reuse existing match strategy / resume data
   4. Generic resume without JD tailoring
   - Do not silently copy old `match_report.md`, old `resume_data.json`, or run ad hoc historical build scripts.
5. **Output Choice**: If the user did not specify the task, ask with numbered options:
   1. Match analysis only
   2. Tailored resume PDF only
   3. Match analysis + tailored resume PDF
   4. Full package: match analysis + resume PDF + interview prep
6. **Photo Choice**: Ask before rendering any resume PDF unless the user already made an explicit photo/no-photo choice:
   1. No photo version
   2. Use existing photo
   3. Add a new photo
   4. Generate both photo and no-photo versions
   - Do not choose a no-photo template just to avoid this question.
   - If the user chooses a photo option, use a photo-capable template such as `luxsleek`, `engineer_with_photo`, or a custom template that renders `photo.filename`.
7. **Language Choice**: Ask only if the target resume language is unclear.
   - Default to the JD language when obvious.
   - If the user speaks Chinese but the JD is German, interact in Chinese and generate the resume in German.
8. **Template Choice**: Ask before rendering any resume PDF unless the user already specified a template or explicitly asked Codex to choose defaults.
   - List templates with `python scripts/setup_workflow.py list-templates` immediately before asking.
   - Build the template candidates from that command output every time; do not use a hard-coded candidate list.
   - Newly added templates under `assets/templates/{template_name}/{template_name}.txt` must appear in the next template-choice candidates.
   - Render with a template name such as `--template luxsleek`.
   - Do not silently use the default `engineer` template.
9. **Version Choice**: If the user asks for multiple versions, confirm the exact version matrix before generating.
   - Example: `engineer` no-photo + `luxsleek` with-photo.
   - Use separate output directories only after the user confirms the matrix.
10. **Generate**: Run the selected workflow and show only the key `deliverables/` paths.

Do not expose internal paths, debug files, schema details, or LaTeX details unless the user asks or there is a blocker.

## Default Folder Contract

```text
data/{person}/
  profile.yaml
  profile_photo.jpg
  jds/{job}.txt

output/{person}/jobs/{job}/
  deliverables/       # files users should open or send
    {person}_{job}_resume.pdf
    match_report.md
    interview_prep.md
  debug/              # reproducibility and troubleshooting
    resume_data.json
    tailored_resume.tex
    tailored_resume.log
```

Use `scripts/setup_workflow.py` for deterministic setup:

```bash
python scripts/setup_workflow.py save-jd --person "Alex Chen" --job "Senior Backend Engineer" --file jd.txt
python scripts/setup_workflow.py add-photo --person "Alex Chen" --file headshot.jpg
python scripts/setup_workflow.py init-job --person "Alex Chen" --job "Senior Backend Engineer"
python scripts/setup_workflow.py validate-profile --file data/alex_chen/profile.yaml
```

Render with:

```bash
python scripts/render_resume.py --output output/{person}/jobs/{job}
```

Use a specific template when requested:

```bash
python scripts/render_resume.py --output output/{person}/jobs/{job} --template luxsleek
```

Use `python` on every platform. If Python 3 is exposed only as `python3`, use `python3`.

## Non-Negotiables

- Do not fabricate skills, employers, degrees, dates, certifications, metrics, management scope, or tools.
- Treat `do_not_claim`, `constraints`, and `review_notes` in profile data as hard boundaries.
- Translate and localize wording, section labels, and role summaries into the target language, but never translate into new claims.
- If source material is ambiguous, preserve uncertainty in `review_notes` or ask a short clarification question.
- Treat `match_report.md` as the strategy source for resume generation and interview prep; interview gap defense must inherit match report gaps.
- Do not skip JD collection for a tailored resume. Generate a generic resume only when the user explicitly requests it, and say that no JD tailoring was performed.
- Do not reuse old match reports, resume JSON, generated scripts, or prior output directories unless the user explicitly chooses to reuse them for the current run.
- Require the target position before saving a JD, initializing a job, or generating a resume. Do not proceed with an empty, TODO, unknown, or placeholder job title.
- Ask whether the user has/wants a photo before rendering any resume PDF; do not silently default to a no-photo template.
- Ask the user to choose a resume template before rendering any resume PDF; do not silently default to `engineer`.
- Store and render the main contact location as short city/state/country-level text. Do not put full street addresses, postal codes, or apartment/neighborhood details in profile data or compact headers unless the user explicitly asks.
- Keep generated resume JSON as plain text. The renderer applies LaTeX escaping.
- Save artifacts to files; do not only answer in chat.
- Put user-facing files in `deliverables/` and build/debug files in `debug/`.
- Keep paths relative and use forward slashes in docs so instructions stay portable across Windows, macOS, and Linux.
- Choose `assets/templates/luxsleek/luxsleek.txt` when the user wants a polished sidebar CV with compact experience entries. Keep long summary content in the main paginating flow and keep sidebar skills concise.

## Bundled Resources

- `scripts/setup_workflow.py`: Saves JDs, copies photos, and initializes job folders.
- `scripts/render_resume.py`: Validates resume JSON, resolves template names, renders LaTeX, copies template resources/photos, and runs a LaTeX engine.
- `references/workflow.md`: End-to-end user flows.
- `references/importing.md`: Resume/JD/photo import rules.
- `references/localization.md`: Target-language and multilingual resume rules.
- `references/resume_schema.md`: JSON contract for rendered resumes.
- `references/report_schema.md`: Match report format.
- `references/interview_prep.md`: Interview question generation rules.
- `references/templates.md`: Adding, listing, choosing, and previewing resume templates.
- `assets/templates/engineer/`: Default LaTeX templates.
- `assets/templates/luxsleek/`: Two-column sidebar LaTeX template based on LuxSleek-CV.

## Dependencies

Python packages:

```bash
python -m pip install jinja2 pyyaml
```

PDF engine:

- Tectonic is preferred because it is lighter and can fetch the bundled Noto font package automatically.
- Windows: install Tectonic, MiKTeX, or TeX Live and ensure the engine is on `PATH`.
- macOS: install Tectonic, MacTeX, or BasicTeX and ensure the engine is on `PATH`.
- Linux: install Tectonic, or TeX Live packages that include `pdflatex`.
- Built-in templates use the LaTeX `noto` package for consistent Latin-script multilingual output, including English, German, and French.

If no LaTeX engine is available, still generate and inspect `debug/tailored_resume.tex`; PDF compilation can happen later.
