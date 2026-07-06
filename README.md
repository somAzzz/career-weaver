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
python skill/scripts/setup_workflow.py add-template --name sidebar_modern --file sidebar_modern.txt
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
    developercv.cls        # generated from skill/assets/templates/common/developercv.txt
```

## Multilingual Behavior

User interaction can stay in Chinese while the resume output is localized to the JD or requested language. For example, a Chinese user can provide a Chinese profile and a German JD, then ask for a German resume. Career Weaver keeps facts grounded in `profile.yaml`, translates resume-facing text, and localizes section labels through `labels` in `debug/resume_data.json`.

Current PDF templates use Noto Sans through the LaTeX `noto` package and work best for English, German, French, and other Latin-script targets. Chinese can be used as the interaction/source-profile language; direct Chinese PDF output needs a future CJK-capable template or renderer.

## TODO

The product direction is to move beyond keyword matching and model the recruiting logic behind a JD: why the role exists, what the real gates are, and how a truthful candidate story should be positioned.

### P0: Recruiting Mindset Foundation

- [x] Add `Role Archetype` to the match report so roles can be interpreted as builder, maintainer, scale, migration, leadership, rescue, or hybrid roles.
- [x] Add `Candidate Positioning` with a primary recruiter-facing label, alternative positioning, and positioning to avoid.
- [x] Add `Layered Requirements` to distinguish legal gates, core technical gates, experience gates, strong filters, tie-breakers, and cosmetic keywords.
- [x] Make P0 outputs part of the upstream strategy for tailored resume generation.

### P1: Actionable Delivery Layer

- [x] Add `Application Recommendation` with decisions such as strong apply, apply with tailoring, referral first, low priority, or do not apply.
- [x] Add recruiter first-screen optimization for the 10-30 second resume scan and above-the-fold content.
- [x] Add graded risk handling, such as fatal gap, explainable gap, resume-only gap, and interview gap.

### P2: Full Funnel Extension

- [ ] Add a hiring funnel assessment for ATS, recruiter screen, hiring manager review, interview, and offer/logistics risk.
- [ ] Add HR screen question generation for work authorization, location, salary, notice period, language, and motivation.
- [ ] Add outreach strategy for recruiter messages, referral requests, and cover letter angles.
- [ ] Add market competitiveness estimates only when enough external or user-provided market context is available.

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
python skill/scripts/setup_workflow.py add-template --name sidebar_modern --file sidebar_modern.txt
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
    developercv.cls        # 由 skill/assets/templates/common/developercv.txt 生成
```

## 多语言能力

用户可以用中文与 agent 交互，同时让最终简历输出为 JD 或用户指定的语言。例如，中文用户可以提供中文 profile 和德语 JD，然后要求生成德语简历。Career Weaver 会基于 `profile.yaml` 中的事实生成内容，翻译简历文本，并通过 `debug/resume_data.json` 中的 `labels` 本地化章节标题。

当前 PDF 模板通过 LaTeX `noto` 包使用 Noto Sans，最适合英文、德文、法文等拉丁字母语言。中文可以作为交互语言和源 profile 语言；如果要直接生成中文 PDF，还需要后续增加支持 CJK 的模板或渲染器。

## TODO

产品演进方向是从关键词匹配升级为招聘逻辑建模：理解岗位为什么存在、真正的筛选门槛是什么，以及候选人应该如何在不编造事实的前提下完成定位。

### P0：招聘心智地基

- [x] 在匹配报告中加入 `Role Archetype`，将岗位识别为 builder、maintainer、scale、migration、leadership、rescue 或 hybrid 类型。
- [x] 加入 `Candidate Positioning`，包含主定位标签、备选定位和应避免的定位。
- [x] 加入 `Layered Requirements`，区分 legal gate、core technical gate、experience gate、strong filter、tie-breaker 和 cosmetic keyword。
- [x] 让 P0 输出成为后续定制简历生成的上游策略约束。

### P1：行动交付层

- [x] 加入 `Application Recommendation`，给出 strong apply、apply with tailoring、referral first、low priority 或 do not apply 等决策。
- [x] 加入 recruiter 首屏优化，面向 10-30 秒简历扫视和首屏内容优先级。
- [x] 加入风险分级，例如 fatal gap、explainable gap、resume-only gap 和 interview gap。

### P2：完整招聘漏斗扩展

- [ ] 加入招聘漏斗评估，覆盖 ATS、HR 初筛、Hiring Manager review、面试和 offer/logistics 风险。
- [ ] 加入 HR 初筛问题生成，覆盖工作许可、地点、薪资、notice period、语言和求职动机。
- [ ] 加入触达策略，生成 recruiter message、内推请求和 cover letter 角度。
- [ ] 仅在有足够外部或用户提供的市场上下文时，加入市场竞争力判断。
