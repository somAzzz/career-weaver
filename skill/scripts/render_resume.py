#!/usr/bin/env python3
"""
Cross-platform resume renderer for Career Weaver.

Input JSON -> Jinja2 LaTeX template -> PDF via pdflatex or Tectonic.
The script validates the resume data contract and keeps generated files in:
  <job-output>/deliverables/  # user-facing files
  <job-output>/debug/         # rendered TeX and LaTeX build artifacts
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_ROOT = ROOT / "assets" / "templates"
DEFAULT_OUTPUT = Path("output")
DEFAULT_DATA = Path("debug") / "resume_data.json"
LATEX_TIMEOUT_SECONDS = 120

LATEX_SPECIALS = {
    "%": r"\%",
    "&": r"\&",
    "_": r"\_",
    "#": r"\#",
    "$": r"\$",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


class ResumeValidationError(ValueError):
    """Raised when resume JSON does not match the template contract."""


def slugify(value: Any) -> str:
    """Create a portable lowercase filename segment."""
    text = str(value or "").strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_") or "resume"


def latex_escape(value: Any) -> str:
    """Escape user-controlled text for LaTeX while preserving common existing escapes."""
    if value is None:
        return ""

    text = str(value)
    escaped: list[str] = []
    for index, char in enumerate(text):
        if char in LATEX_SPECIALS:
            previous = text[index - 1] if index > 0 else ""
            escaped.append(char if previous == "\\" else LATEX_SPECIALS[char])
        else:
            escaped.append(char)
    return "".join(escaped)


def display_url(url: str) -> str:
    """Convert a profile URL to compact display text."""
    return re.sub(r"^https?://(www\.)?", "", url).rstrip("/")


def compact_location(location: Any) -> str:
    """Prefer a resume-safe location over a full street address."""
    text = str(location or "").strip()
    if not text:
        return ""

    parts = [part.strip() for part in text.split(",") if part.strip()]
    if len(parts) >= 3 and re.match(r"^\d+\b", parts[0]):
        locality = re.sub(
            r"\b[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}\b$",
            "",
            parts[-2],
            flags=re.IGNORECASE,
        ).strip()
        locality = re.sub(r"\b\d{4,6}\b$", "", locality).strip()
        return f"{locality}, {parts[-1]}" if locality else parts[-1]

    return text


def discover_templates() -> dict[str, Path]:
    """Return bundled/custom templates by stable name."""
    templates: dict[str, Path] = {}
    if not TEMPLATES_ROOT.exists():
        return templates

    for template_path in sorted(TEMPLATES_ROOT.glob("*/*.tex.jinja2")):
        if template_path.parent.name == "common":
            continue
        name = template_path.stem.removesuffix(".tex")
        templates.setdefault(name, template_path)
        templates.setdefault(template_path.parent.name, template_path)
    return templates


def resolve_template_path(template_arg: str) -> Path:
    """Resolve a template name, relative path, or absolute path."""
    templates = discover_templates()
    if template_arg in templates:
        return templates[template_arg]

    template_path = Path(template_arg)
    candidates = [
        template_path,
        ROOT / template_path,
        TEMPLATES_ROOT / template_path,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    available = ", ".join(sorted(templates)) or "none"
    raise FileNotFoundError(f"Template not found: {template_arg}. Available templates: {available}")


def template_supports_photo(template_path: Path) -> bool:
    return "photo.filename" in template_path.read_text(encoding="utf-8", errors="ignore")


def require_mapping(data: dict[str, Any], key: str, path: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise ResumeValidationError(f"{path}.{key} must be an object")
    return value


def require_list(data: dict[str, Any], key: str, path: str) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list):
        raise ResumeValidationError(f"{path}.{key} must be an array")
    return value


def require_text(data: dict[str, Any], key: str, path: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ResumeValidationError(f"{path}.{key} must be a non-empty string")
    return value


def validate_bulleted_entries(entries: list[Any], path: str, title_key: str) -> None:
    for index, entry in enumerate(entries):
        item_path = f"{path}[{index}]"
        if not isinstance(entry, dict):
            raise ResumeValidationError(f"{item_path} must be an object")
        for key in (title_key, "company", "date", "bullets"):
            if key == "bullets":
                bullets = require_list(entry, key, item_path)
                if not bullets:
                    raise ResumeValidationError(f"{item_path}.bullets must not be empty")
                for bullet_index, bullet in enumerate(bullets):
                    if not isinstance(bullet, str) or not bullet.strip():
                        raise ResumeValidationError(
                            f"{item_path}.bullets[{bullet_index}] must be a non-empty string"
                        )
            else:
                require_text(entry, key, item_path)


def validate_resume_data(data: dict[str, Any]) -> None:
    """Validate the stable JSON contract expected by bundled templates."""
    for key in ("name", "role", "summary"):
        require_text(data, key, "$")

    contact = require_mapping(data, "contact", "$")
    for key in ("email", "location"):
        require_text(contact, key, "$.contact")

    skills = require_mapping(data, "skills", "$")
    if not skills:
        raise ResumeValidationError("$.skills must not be empty")
    for category, items in skills.items():
        if not isinstance(category, str) or not category.strip():
            raise ResumeValidationError("$.skills keys must be non-empty strings")
        if not isinstance(items, list) or not items:
            raise ResumeValidationError(f"$.skills.{category} must be a non-empty array")
        for index, item in enumerate(items):
            if not isinstance(item, str) or not item.strip():
                raise ResumeValidationError(f"$.skills.{category}[{index}] must be a non-empty string")

    validate_bulleted_entries(require_list(data, "experience", "$"), "$.experience", "role")

    for section, title_key in (("projects", "title"), ("research", "title")):
        if section in data and data[section] is not None:
            validate_bulleted_entries(require_list(data, section, "$"), f"$.{section}", title_key)

    education = require_list(data, "education", "$")
    for index, entry in enumerate(education):
        item_path = f"$.education[{index}]"
        if not isinstance(entry, dict):
            raise ResumeValidationError(f"{item_path} must be an object")
        for key in ("school", "degree", "date"):
            require_text(entry, key, item_path)

    labels = data.get("labels")
    if labels is not None:
        if not isinstance(labels, dict):
            raise ResumeValidationError("$.labels must be an object when provided")
        for key, value in labels.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise ResumeValidationError("$.labels must map strings to strings")


def load_resume_data(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ResumeValidationError("Resume data root must be an object")
    validate_resume_data(data)
    contact = data.get("contact")
    if isinstance(contact, dict):
        contact.setdefault("display_location", compact_location(contact.get("location")))
    return data


def build_jinja_env(template_dir: Path) -> Environment:
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        block_start_string=r"\BLOCK{",
        block_end_string="}",
        variable_start_string=r"\VAR{",
        variable_end_string="}",
        comment_start_string=r"\#{",
        comment_end_string="}",
        line_statement_prefix="%%",
        line_comment_prefix="%#",
        trim_blocks=True,
        autoescape=False,
    )
    env.filters["latex_escape"] = latex_escape
    env.filters["display_url"] = display_url
    env.filters["compact_location"] = compact_location
    return env


def copy_template_resources(template_path: Path, build_path: Path) -> None:
    candidates = [
        template_path.parent / "common",
        template_path.parent.parent / "common",
        ROOT / "assets" / "templates" / "common",
    ]
    for common_dir in candidates:
        if common_dir.exists():
            for cls_file in common_dir.glob("*.cls"):
                shutil.copy2(cls_file, build_path / cls_file.name)


def copy_photo(data: dict[str, Any], data_path: Path, build_path: Path) -> None:
    photo = data.get("photo")
    if not isinstance(photo, dict) or not photo.get("filename"):
        return

    photo_name = str(photo["filename"])
    profile_slug = str(data.get("name", "")).lower().replace(" ", "_")
    candidates = [
        data_path.parent / photo_name,
        ROOT / photo_name,
        ROOT / "data" / profile_slug / photo_name,
        Path(photo_name),
    ]
    for candidate in candidates:
        if candidate.exists():
            destination = build_path / candidate.name
            if candidate.resolve() != destination.resolve():
                shutil.copy2(candidate, destination)
            return
    print(f"Warning: photo file not found: {photo_name}", file=sys.stderr)


def resume_pdf_name(data: dict[str, Any], output_dir: Path) -> str:
    person = slugify(data.get("name"))
    job = slugify(output_dir.name)
    return f"{person}_{job}_resume.pdf"


def compile_pdf(tex_file: Path, debug_path: Path, engine: str) -> None:
    selected_engine = engine
    if selected_engine == "auto":
        selected_engine = "pdflatex" if shutil.which("pdflatex") else "tectonic"

    if selected_engine == "pdflatex":
        pdflatex = shutil.which("pdflatex")
        if not pdflatex:
            raise RuntimeError("pdflatex not found. Install TeX Live, MacTeX, or MiKTeX.")
        result = subprocess.run(
            [
                pdflatex,
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-output-directory",
                str(debug_path.resolve()),
                str(tex_file.resolve()),
            ],
            capture_output=True,
            text=True,
            timeout=LATEX_TIMEOUT_SECONDS,
        )
    elif selected_engine == "tectonic":
        tectonic = shutil.which("tectonic")
        if not tectonic:
            raise RuntimeError("tectonic not found. Install Tectonic or use --engine pdflatex.")
        result = subprocess.run(
            [tectonic, tex_file.name],
            cwd=debug_path,
            capture_output=True,
            text=True,
            timeout=LATEX_TIMEOUT_SECONDS,
        )
    else:
        raise RuntimeError(f"Unsupported LaTeX engine: {engine}")

    build_pdf = debug_path / "tailored_resume.pdf"
    if result.returncode != 0 or not build_pdf.exists():
        log_file = debug_path / "tailored_resume.log"
        details = result.stderr or result.stdout[-2000:]
        if log_file.exists():
            details = log_file.read_text(encoding="utf-8", errors="replace")[-2000:]
        raise RuntimeError(f"PDF compilation failed with {selected_engine}. Check {log_file}\n\n{details}")


def render(data_file: Path, template_file: Path, output_dir: Path, engine: str = "auto") -> Path:
    base_path = output_dir
    deliverables_path = base_path / "deliverables"
    debug_path = base_path / "debug"
    deliverables_path.mkdir(parents=True, exist_ok=True)
    debug_path.mkdir(parents=True, exist_ok=True)

    data = load_resume_data(data_file)
    data.setdefault("labels", {})
    template_file = template_file.resolve()
    if template_supports_photo(template_file) and not data.get("photo"):
        print(
            "Warning: selected template supports photos, but resume_data.json has no photo. "
            "Confirm the user chose a no-photo render.",
            file=sys.stderr,
        )
    env = build_jinja_env(template_file.parent)
    template = env.get_template(template_file.name)

    tex_file = debug_path / "tailored_resume.tex"
    tex_file.write_text(template.render(**data), encoding="utf-8")

    copy_template_resources(template_file, debug_path)
    copy_photo(data, data_file, debug_path)

    build_pdf = debug_path / "tailored_resume.pdf"
    build_pdf.unlink(missing_ok=True)
    compile_pdf(tex_file, debug_path, engine)

    final_pdf = deliverables_path / resume_pdf_name(data, output_dir)
    shutil.copy2(build_pdf, final_pdf)
    return final_pdf


def resolve_data_path(output_dir: Path, data_arg: str) -> Path:
    data_path = Path(data_arg)
    if data_path.is_absolute():
        return data_path
    return output_dir / data_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a tailored resume PDF from JSON data.")
    parser.add_argument(
        "--data",
        "-d",
        default=str(DEFAULT_DATA),
        help="Resume JSON file. Relative paths are resolved against --output. Defaults to debug/resume_data.json.",
    )
    parser.add_argument(
        "--template",
        "-t",
        default="engineer",
        help="Template name or Jinja2 LaTeX template path. Use setup_workflow.py list-templates to inspect options.",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=str(DEFAULT_OUTPUT),
        help="Job directory containing deliverables/ and debug/ folders.",
    )
    parser.add_argument(
        "--engine",
        choices=("auto", "pdflatex", "tectonic"),
        default="auto",
        help="LaTeX engine. Defaults to auto, preferring pdflatex and falling back to tectonic.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output)
    data_path = resolve_data_path(output_dir, args.data)

    try:
        pdf_path = render(data_path, resolve_template_path(args.template), output_dir, args.engine)
    except (FileNotFoundError, ResumeValidationError, RuntimeError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"SUCCESS: {pdf_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
