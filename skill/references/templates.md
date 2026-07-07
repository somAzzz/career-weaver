# Resume Templates

Use this reference when the user wants to add, list, choose, preview, or render a resume template.

## Template Contract

Templates are `.txt` files whose contents are rendered by Jinja2 into LaTeX:

```text
assets/templates/{template_name}/{template_name}.txt
```

Template names should be lowercase slugs, for example:

- `engineer`
- `luxsleek`
- `academic`
- `sidebar_modern`

Templates should use the resume JSON fields described in `references/resume_schema.md`. Keep templates data-driven; do not hard-code a candidate's name, contact details, companies, dates, or skills.

## Add A Template

When the user provides a `.txt` template and asks to add it:

```bash
python scripts/setup_workflow.py add-template --name "{template_name}" --file path/to/template.txt
```

Use `--force` only when the user explicitly wants to replace an existing template.

If the user provides a raw `.tex` file instead of a `.txt` Jinja2 template:

1. Analyze the static resume structure.
2. Replace candidate-specific content with `resume_data.json` variables.
3. Save the converted file as `.txt`.
4. Add it with `setup_workflow.py add-template`.
5. Render a small preview before treating it as ready.

## List Templates

When the user asks what templates are available:

```bash
python scripts/setup_workflow.py list-templates
```

Show the template names to the user and ask which one they prefer before rendering a resume PDF unless the user already specified a template or explicitly asked Codex to choose defaults. Templates marked `[photo]` support `photo.filename`; if the user selects one, ask the mandatory photo question before rendering.

When generating a resume, always rerun `list-templates` immediately before asking the template-choice question. Build the candidate list from that output, not from a static list in docs or memory. A newly added template must be included in the next template-choice candidates.

## Choose A Template

The renderer accepts either a template name or a path:

```bash
python scripts/render_resume.py --output output/{person}/jobs/{job} --template luxsleek
python scripts/render_resume.py --output output/{person}/jobs/{job} --template assets/templates/luxsleek/luxsleek.txt
```

Prefer template names in user-facing instructions. Paths are useful for debugging or one-off templates.

Before rendering any resume PDF, ask which template to use unless the user already specified one. Do not silently default to `engineer`.

When generating multiple PDFs, ask for the exact version matrix before rendering. Do not infer versions from old output directories. Examples:

- `engineer` no-photo only
- `luxsleek` with-photo only
- both photo and no-photo for `luxsleek`
- `engineer` no-photo + `luxsleek` with-photo

## Selection Guidance

- `engineer`: default compact technical resume.
- `engineer_with_photo`: technical resume with a photo block.
- `luxsleek`: polished sidebar CV with compact experience entries. The sidebar is for identity/contact/language details and concise skills; summary renders in the main flow so long profile text can paginate.
- `businessinsider`: two-column AltaCV template adapted from the Business Insider / Marissa Mayer Overleaf example. It supports an optional right-side photo and works well for concise executive, product, and leadership resumes with strong skills tags.
- `resume_cv`: two-column minimalist template adapted from Stefan Radu's Overleaf "Resume / CV" example. It is a no-photo layout for concise Computer Science and Engineering resumes.

## Photo-Capable Templates

Treat a template as photo-capable when it renders `photo.filename`.

Bundled photo-capable templates:

- `engineer_with_photo`
- `luxsleek`
- `businessinsider`

Before rendering any resume PDF, ask whether the user has a photo or wants a no-photo version. Ask before final template selection so the agent cannot silently choose a no-photo template to avoid the question. Do not silently default unless the user explicitly asks Codex to choose defaults.

For markets or roles where photos are uncommon, recommend a no-photo version after asking.

Do not put long summaries or dense project content in a fixed sidebar. LuxSleek keeps skills in the sidebar, so keep sidebar skills concise; overflow-prone content belongs in the main paginating flow.
