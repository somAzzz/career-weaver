# Career Weaver

Career Weaver is a portable coding-agent skill for turning raw career materials into targeted, multilingual job-application deliverables.

It helps an agent:

- import a user's resume into `profile.yaml`
- save pasted job descriptions
- copy profile photos
- analyze JD fit
- generate tailored resume PDFs
- localize resumes into English, German, French, Chinese, or another requested language
- prepare interview questions

## Skill Package

The installable skill lives in `skill/`:

- `skill/SKILL.md`
- `skill/agents/openai.yaml`
- `skill/references/`
- `skill/scripts/`
- `skill/assets/`

Example data and generated outputs are not part of the skill package.

To install the skill, copy or symlink `skill/` as the skill directory:

```text
~/.codex/skills/career-weaver/
```

## Repository Layout

```text
skill/
  SKILL.md
  agents/
  references/
  scripts/
  assets/
examples/data/        # sample data only
output/               # local generated files, ignored for new files
```

## Requirements

- Python 3.12+
- `jinja2` and `pyyaml`
- `pdflatex` from TeX Live, MacTeX, BasicTeX, or MiKTeX

Install Python dependencies:

```bash
python -m pip install -e .
```

## Basic Commands

Save a new JD in the current workspace:

```bash
python skill/scripts/setup_workflow.py save-jd --person "Alex Chen" --job "Senior Backend Engineer" --file jd.txt
```

Add a profile photo:

```bash
python skill/scripts/setup_workflow.py add-photo --person "Alex Chen" --file headshot.jpg
```

Render an existing generated resume:

```bash
python skill/scripts/render_resume.py --output output/alex_chen/jobs/senior_backend_engineer
```

Use example data by copying it into runtime `data/`:

```bash
python -c "import shutil, pathlib; shutil.copytree('examples/data', 'data', dirs_exist_ok=True)"
```

## Output Layout

Each job output directory separates user-facing files from build artifacts:

```text
output/{person}/jobs/{job}/
  deliverables/
    {person}_{job}_resume.pdf
    match_report.md
    interview_prep.md
  debug/
    resume_data.json
    tailored_resume.tex
    tailored_resume.log
    tailored_resume.aux
    tailored_resume.out
    developercv.cls
```

For compatibility, the renderer still reads legacy `logs/resume_data.json` when `debug/resume_data.json` does not exist.

## Multilingual Behavior

User interaction can stay in Chinese while the resume output is localized to the JD or requested language. For example, a Chinese user can provide a Chinese profile and a German JD, then ask for a German resume. Career Weaver keeps facts grounded in `profile.yaml`, translates resume-facing text, and localizes section labels through `labels` in `debug/resume_data.json`.

Current PDF templates work best for English, German, French, and other Latin-script targets. Chinese can be used as the interaction/source-profile language; direct Chinese PDF output needs a future CJK-capable template or renderer.
