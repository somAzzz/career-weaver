#!/usr/bin/env python3
"""
Set up Career Weaver inputs in a cross-platform way.

The script intentionally handles deterministic file operations only:
- create person/job directories
- save pasted JD text or copy an existing JD file
- copy a profile photo
- create a profile draft placeholder

Agents still perform semantic extraction, matching, and resume writing.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_ROOT = ROOT / "assets" / "templates"
DEFAULT_WORKSPACE = Path.cwd()
PLACEHOLDER_VALUES = {"", "todo", "tbd", "unknown", "n/a", "na", "none", "untitled"}


def workspace_path(args: argparse.Namespace) -> Path:
    return Path(args.workspace).resolve()


def data_dir(args: argparse.Namespace) -> Path:
    return workspace_path(args) / "data"


def output_dir(args: argparse.Namespace) -> Path:
    return workspace_path(args) / "output"


def slugify(value: str) -> str:
    text = value.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_") or "untitled"


class ProfileValidationError(ValueError):
    """Raised when profile.yaml is missing required master-profile fields."""


def is_placeholder(value: Any) -> bool:
    return str(value or "").strip().lower() in PLACEHOLDER_VALUES


def require_profile_text(data: dict[str, Any], key: str, path: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or is_placeholder(value):
        raise ProfileValidationError(f"{path}.{key} must be a non-empty, non-placeholder string")
    return value.strip()


def validate_job_title(job: str) -> str:
    if is_placeholder(job):
        raise ValueError("job must be the target position being applied for, not TODO/unknown/empty")
    return slugify(job)


def validate_resume_safe_location(location: str, path: str) -> None:
    text = location.strip()
    if re.search(r"\d", text):
        raise ProfileValidationError(f"{path} must be city/state/country level only; remove street/postal details")
    if len(text) > 60:
        raise ProfileValidationError(f"{path} is too long for resume display; keep it to city/state/country level")
    if any(is_placeholder(part) for part in re.split(r"[,/|-]", text)):
        raise ProfileValidationError(f"{path} must not contain placeholder location parts")


def validate_profile_data(data: dict[str, Any]) -> None:
    if not isinstance(data, dict):
        raise ProfileValidationError("profile.yaml root must be an object")

    profile = data.get("profile")
    if not isinstance(profile, dict):
        raise ProfileValidationError("$.profile must be an object")
    require_profile_text(profile, "name", "$.profile")

    target_roles = profile.get("target_roles")
    if not isinstance(target_roles, list) or not target_roles:
        raise ProfileValidationError("$.profile.target_roles must include at least one target position")
    for index, role in enumerate(target_roles):
        if not isinstance(role, str) or is_placeholder(role):
            raise ProfileValidationError(
                f"$.profile.target_roles[{index}] must be the target position being applied for"
            )

    contact = data.get("contact")
    if not isinstance(contact, dict):
        raise ProfileValidationError("$.contact must be an object")
    require_profile_text(contact, "email", "$.contact")
    location = require_profile_text(contact, "location", "$.contact")
    validate_resume_safe_location(location, "$.contact.location")


def load_profile(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"profile not found: {path}")

    try:
        import yaml
    except ImportError as error:
        raise ProfileValidationError("PyYAML is required for validate-profile; install with: python -m pip install pyyaml") from error

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        raise ProfileValidationError(f"invalid YAML: {error}") from error

    if not isinstance(data, dict):
        raise ProfileValidationError("profile.yaml root must be an object")
    return data


def discover_templates() -> dict[str, Path]:
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


def template_supports_photo(template_path: Path) -> bool:
    return "photo.filename" in template_path.read_text(encoding="utf-8", errors="ignore")


def person_slug(name: str) -> str:
    return slugify(name)


def ensure_person_dirs(person: str, args: argparse.Namespace) -> Path:
    person_dir = data_dir(args) / person
    (person_dir / "jds").mkdir(parents=True, exist_ok=True)
    return person_dir


def ensure_job_dirs(person: str, job: str, args: argparse.Namespace) -> Path:
    job_dir = output_dir(args) / person / "jobs" / job
    (job_dir / "deliverables").mkdir(parents=True, exist_ok=True)
    (job_dir / "debug").mkdir(parents=True, exist_ok=True)
    return job_dir


def read_stdin_text() -> str:
    if sys.stdin.isatty():
        return ""
    return sys.stdin.read()


def command_init_profile(args: argparse.Namespace) -> int:
    person = person_slug(args.name)
    person_dir = ensure_person_dirs(person, args)
    profile_path = person_dir / "profile.yaml"
    if profile_path.exists() and not args.force:
        print(f"EXISTS: {profile_path}")
        return 0

    profile_path.write_text(
        "\n".join(
            [
                "# Draft profile generated by setup_workflow.py.",
                "# Replace TODO values with facts extracted from the user's resume.",
                "",
                "profile:",
                f'  name: "{args.name}"',
                '  summary: "TODO"',
                "",
                "contact:",
                '  email: "TODO"',
                '  phone: ""',
                '  location: "TODO"',
                '  linkedin: ""',
                '  github: ""',
                "",
                "experience: []",
                "projects: []",
                "skills: []",
                "education: []",
                "certifications: []",
                "languages: []",
                "",
                "review_notes:",
                '  - "Profile is a draft. Confirm all TODO fields before generating resumes."',
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"CREATED: {profile_path}")
    return 0


def command_save_jd(args: argparse.Namespace) -> int:
    person = person_slug(args.person)
    try:
        job = validate_job_title(args.job)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    person_dir = ensure_person_dirs(person, args)
    job_dir = ensure_job_dirs(person, job, args)

    jd_path = person_dir / "jds" / f"{job}.txt"
    if args.file:
        source = Path(args.file)
        if not source.exists():
            print(f"ERROR: JD file not found: {source}", file=sys.stderr)
            return 1
        text = source.read_text(encoding=args.encoding)
    else:
        text = args.text or read_stdin_text()

    if not text.strip():
        print("ERROR: provide JD text with --text, --file, or stdin", file=sys.stderr)
        return 1

    jd_path.write_text(text.strip() + "\n", encoding="utf-8")
    print(f"JD: {jd_path}")
    print(f"JOB_DIR: {job_dir}")
    return 0


def command_add_photo(args: argparse.Namespace) -> int:
    person = person_slug(args.person)
    person_dir = ensure_person_dirs(person, args)
    source = Path(args.file)
    if not source.exists():
        print(f"ERROR: photo file not found: {source}", file=sys.stderr)
        return 1

    suffix = source.suffix.lower() or ".jpg"
    destination = person_dir / f"profile_photo{suffix}"
    shutil.copy2(source, destination)
    print(f"PHOTO: {destination}")
    print('Use in resume_data.json as: "photo": {"filename": "' + destination.name + '"}')
    return 0


def command_init_job(args: argparse.Namespace) -> int:
    person = person_slug(args.person)
    try:
        job = validate_job_title(args.job)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    ensure_person_dirs(person, args)
    job_dir = ensure_job_dirs(person, job, args)
    print(f"JOB_DIR: {job_dir}")
    print(f"DEBUG_JSON: {job_dir / 'debug' / 'resume_data.json'}")
    print(f"DELIVERABLES: {job_dir / 'deliverables'}")
    return 0


def command_validate_profile(args: argparse.Namespace) -> int:
    path = Path(args.file)
    try:
        validate_profile_data(load_profile(path))
    except (FileNotFoundError, ProfileValidationError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: {path}")
    return 0


def command_list_templates(args: argparse.Namespace) -> int:
    templates = discover_templates()
    if not templates:
        print("No templates found.")
        return 0

    seen: set[Path] = set()
    for name in sorted(templates):
        template_path = templates[name]
        if template_path in seen and name != template_path.parent.name:
            continue
        seen.add(template_path)
        marker = " [photo]" if template_supports_photo(template_path) else ""
        print(f"{name}{marker}: {template_path.relative_to(ROOT)}")
    return 0


def command_add_template(args: argparse.Namespace) -> int:
    source = Path(args.file)
    if not source.exists():
        print(f"ERROR: template file not found: {source}", file=sys.stderr)
        return 1
    if source.suffixes[-2:] != [".tex", ".jinja2"]:
        print("ERROR: template file must end with .tex.jinja2", file=sys.stderr)
        return 1

    name = slugify(args.name or source.name.removesuffix(".tex.jinja2"))
    template_dir = TEMPLATES_ROOT / name
    template_dir.mkdir(parents=True, exist_ok=True)
    destination = template_dir / f"{name}.tex.jinja2"

    if destination.exists() and not args.force:
        print(f"EXISTS: {destination}")
        print("Use --force to replace it.")
        return 1

    shutil.copy2(source, destination)
    print(f"TEMPLATE: {destination}")
    print(f"Use with: --template {name}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Set up Career Weaver input and output files.")
    parser.add_argument(
        "--workspace",
        default=str(DEFAULT_WORKSPACE),
        help="Workspace where data/ and output/ should be created. Defaults to the current directory.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_profile = subparsers.add_parser("init-profile", help="Create a draft profile.yaml for a person.")
    init_profile.add_argument("--name", required=True, help="Person name, e.g. 'Alex Chen'.")
    init_profile.add_argument("--force", action="store_true", help="Overwrite an existing profile.yaml.")
    init_profile.set_defaults(func=command_init_profile)

    validate_profile = subparsers.add_parser(
        "validate-profile",
        help="Validate profile.yaml required fields and resume-safe contact location.",
    )
    validate_profile.add_argument("--file", required=True, help="Path to profile.yaml.")
    validate_profile.set_defaults(func=command_validate_profile)

    save_jd = subparsers.add_parser("save-jd", help="Save a JD from text, stdin, or an existing file.")
    save_jd.add_argument("--person", required=True, help="Person name or slug.")
    save_jd.add_argument("--job", required=True, help="Job title or slug.")
    save_jd.add_argument("--text", help="JD text. For long text, prefer stdin or --file.")
    save_jd.add_argument("--file", help="Path to an existing JD text file.")
    save_jd.add_argument("--encoding", default="utf-8", help="Encoding for --file input.")
    save_jd.set_defaults(func=command_save_jd)

    add_photo = subparsers.add_parser("add-photo", help="Copy a photo into data/{person}/.")
    add_photo.add_argument("--person", required=True, help="Person name or slug.")
    add_photo.add_argument("--file", required=True, help="Path to a photo file.")
    add_photo.set_defaults(func=command_add_photo)

    init_job = subparsers.add_parser("init-job", help="Create deliverables/ and debug/ for a job.")
    init_job.add_argument("--person", required=True, help="Person name or slug.")
    init_job.add_argument("--job", required=True, help="Job title or slug.")
    init_job.set_defaults(func=command_init_job)

    list_templates = subparsers.add_parser("list-templates", help="List available resume templates.")
    list_templates.set_defaults(func=command_list_templates)

    add_template = subparsers.add_parser("add-template", help="Copy a .tex.jinja2 resume template into the skill.")
    add_template.add_argument("--name", help="Template name. Defaults to the source filename.")
    add_template.add_argument("--file", required=True, help="Path to a .tex.jinja2 template file.")
    add_template.add_argument("--force", action="store_true", help="Overwrite an existing template with the same name.")
    add_template.set_defaults(func=command_add_template)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args) or 0)


if __name__ == "__main__":
    raise SystemExit(main())
