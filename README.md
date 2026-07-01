# Career Weaver

[English](#english) | [中文](#中文)

## English

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
- Tectonic preferred, or `pdflatex` from TeX Live/MacTeX/BasicTeX/MiKTeX

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

Validate a profile before generating outputs:

```bash
python skill/scripts/setup_workflow.py validate-profile --file data/alex_chen/profile.yaml
```

Render an existing generated resume:

```bash
python skill/scripts/render_resume.py --output output/alex_chen/jobs/senior_backend_engineer
```

Render with the LuxSleek two-column template:

```bash
python skill/scripts/render_resume.py --output output/alex_chen/jobs/senior_backend_engineer --template luxsleek
```

List available resume templates:

```bash
python skill/scripts/setup_workflow.py list-templates
```

Add a custom resume template:

```bash
python skill/scripts/setup_workflow.py add-template --name sidebar_modern --file sidebar_modern.tex.jinja2
```

## Resume Template Library

Browse more LaTeX CV designs here:

**[Overleaf CV Templates](https://cn.overleaf.com/latex/templates/tagged/cv)**

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

## Multilingual Behavior

User interaction can stay in Chinese while the resume output is localized to the JD or requested language. For example, a Chinese user can provide a Chinese profile and a German JD, then ask for a German resume. Career Weaver keeps facts grounded in `profile.yaml`, translates resume-facing text, and localizes section labels through `labels` in `debug/resume_data.json`.

Current PDF templates use Noto Sans through the LaTeX `noto` package and work best for English, German, French, and other Latin-script targets. Chinese can be used as the interaction/source-profile language; direct Chinese PDF output needs a future CJK-capable template or renderer.

## 中文

Career Weaver 是一个可安装到 Codex 等 coding agent 中的求职材料 skill。它可以把用户的原始简历、岗位 JD、照片等材料，整理成面向具体岗位的多语言求职产物。

它可以帮助 agent 完成：

- 将用户简历导入为 `profile.yaml`
- 保存用户粘贴或提供的 JD
- 复制和管理简历照片
- 分析简历与 JD 的匹配度
- 生成针对岗位定制的 PDF 简历
- 将简历本地化为英文、德文、法文、中文或其它目标语言
- 生成面试准备问题

## Skill 包内容

真正可安装的 skill 位于 `skill/`：

- `skill/SKILL.md`
- `skill/agents/openai.yaml`
- `skill/references/`
- `skill/scripts/`
- `skill/assets/`

示例数据和生成结果不属于 skill 本体。

安装时，将 `skill/` 复制或软链接为 skill 目录：

```text
~/.codex/skills/career-weaver/
```

## 仓库结构

```text
skill/
  SKILL.md
  agents/
  references/
  scripts/
  assets/
examples/data/        # 示例数据
output/               # 本地生成结果，新文件默认忽略
```

## 环境要求

- Python 3.12+
- `jinja2` 和 `pyyaml`
- 推荐使用 Tectonic，也可以使用 TeX Live、MacTeX、BasicTeX 或 MiKTeX 中的 `pdflatex`

安装 Python 依赖：

```bash
python -m pip install -e .
```

## 基本命令

在当前工作区保存一份新的 JD：

```bash
python skill/scripts/setup_workflow.py save-jd --person "Alex Chen" --job "Senior Backend Engineer" --file jd.txt
```

添加简历照片：

```bash
python skill/scripts/setup_workflow.py add-photo --person "Alex Chen" --file headshot.jpg
```

生成产物前检查 profile：

```bash
python skill/scripts/setup_workflow.py validate-profile --file data/alex_chen/profile.yaml
```

渲染已有的简历数据：

```bash
python skill/scripts/render_resume.py --output output/alex_chen/jobs/senior_backend_engineer
```

使用 LuxSleek 双栏模板渲染：

```bash
python skill/scripts/render_resume.py --output output/alex_chen/jobs/senior_backend_engineer --template luxsleek
```

列出可用简历模板：

```bash
python skill/scripts/setup_workflow.py list-templates
```

添加自定义简历模板：

```bash
python skill/scripts/setup_workflow.py add-template --name sidebar_modern --file sidebar_modern.tex.jinja2
```

## 简历模板库

可以在这里浏览更多 LaTeX 简历设计：

**[Overleaf CV 简历模板库](https://cn.overleaf.com/latex/templates/tagged/cv)**

复制示例数据到运行时 `data/`：

```bash
python -c "import shutil, pathlib; shutil.copytree('examples/data', 'data', dirs_exist_ok=True)"
```

## 输出目录

每个岗位输出目录会区分用户交付物和调试文件：

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

## 多语言能力

用户可以用中文与 agent 交互，同时让最终简历输出为 JD 或用户指定的语言。例如，中文用户可以提供中文 profile 和德语 JD，然后要求生成德语简历。Career Weaver 会基于 `profile.yaml` 中的事实生成内容，翻译简历文本，并通过 `debug/resume_data.json` 中的 `labels` 本地化章节标题。

当前 PDF 模板通过 LaTeX `noto` 包使用 Noto Sans，最适合英文、德文、法文等拉丁字母语言。中文可以作为交互语言和源 profile 语言；如果要直接生成中文 PDF，还需要后续增加支持 CJK 的模板或渲染器。
