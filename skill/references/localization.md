# Localization

Use this reference when the user's source profile, conversation language, JD language, and target resume language differ.

## Interaction Language

Prefer Chinese for user interaction when the user writes in Chinese. This does not force the resume language.

Examples:

- User writes Chinese + JD is German: reply in Chinese, generate German resume unless the user asks otherwise.
- User writes Chinese + JD is English: reply in Chinese, generate English resume unless the user asks otherwise.
- User writes English + asks for French CV: reply in English, generate French resume.

## Target Language Selection

Choose the target resume language in this order:

1. Explicit user request, such as "生成德语简历" or "make it French".
2. JD language, if the JD is clearly in one language.
3. Locale expectation, if the role/country strongly implies a language.
4. English, if unclear.

Ask one short question only if the choice materially affects the output:

```text
目标简历语言用哪一种？
1. English
2. Deutsch
3. Français
4. 中文
```

## Translation Rules

- Translate resume-facing text into the target language: `role`, `summary`, `skills` category names, bullets, descriptions, project text, education labels, and language levels.
- Preserve proper nouns, product names, company names, technology names, certification names, URLs, and metrics unless the target language has a standard localized form.
- Do not translate facts into stronger claims. Translation is wording, not invention.
- Keep dates in a format appropriate to the target market when possible.
- Use natural professional language, not literal word-by-word translation.
- Adapt section labels with `labels` in `debug/resume_data.json`.

## Current PDF Support Matrix

- Strong: English and most Latin-script European languages, including German and French.
- Strong: Chinese or other-language source profiles translated into English/German/French target resumes.
- Limited: Chinese/Japanese/Korean target PDF output with the default LaTeX templates. The renderer enforces the LaTeX `noto` package for Latin-script multilingual output, but does not include a CJK-capable template, font setup, or XeLaTeX/LuaLaTeX workflow.
- Workaround for CJK target output: generate `debug/resume_data.json` and a translated text/Markdown draft, then use a future CJK template or a DOCX/HTML renderer.

## Suggested Labels

English:

```json
"labels": {
  "summary": "Summary",
  "skills": "Skills",
  "experience": "Experience",
  "projects": "Projects",
  "research": "Research Projects",
  "education": "Education",
  "languages": "Languages"
}
```

German:

```json
"target_language": "de",
"labels": {
  "summary": "Profil",
  "skills": "Kenntnisse",
  "experience": "Berufserfahrung",
  "projects": "Projekte",
  "research": "Forschungsprojekte",
  "education": "Ausbildung",
  "languages": "Sprachen"
}
```

French:

```json
"target_language": "fr",
"labels": {
  "summary": "Profil",
  "skills": "Compétences",
  "experience": "Expérience professionnelle",
  "projects": "Projets",
  "research": "Projets de recherche",
  "education": "Formation",
  "languages": "Langues"
}
```

Chinese:

```json
"target_language": "zh",
"labels": {
  "summary": "个人简介",
  "skills": "技能",
  "experience": "工作经历",
  "projects": "项目经历",
  "research": "研究项目",
  "education": "教育背景",
  "languages": "语言"
}
```

## Quality Checklist

- The final resume language matches the target language.
- User-facing reply language matches the user's preferred language, usually Chinese in this project.
- Every translated claim traces back to `profile.yaml`.
- JD keywords are localized naturally without inventing missing skills.
- Section labels are localized through `labels`.
