"""Link repository-owned OpenCode adapters without editing JSON configuration."""

import argparse
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def default_config_dir():
    base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / "opencode"


def install(config_dir, *, replace=False, dry_run=False, root=ROOT):
    config_dir = Path(config_dir).expanduser().absolute()
    root = Path(root).resolve()
    links = [(config_dir / "frameworks/my-ai-framework", root)]
    for kind in ("agents", "commands"):
        links.extend(
            (config_dir / kind / source.name, source)
            for source in sorted((root / "adapters/opencode" / kind).glob("*.md"))
        )
    pending = []
    for destination, source in links:
        if not source.exists():
            raise FileNotFoundError(f"Missing source: {source}")
        for parent in destination.parents:
            if (parent.exists() or parent.is_symlink()) and not parent.is_dir():
                raise FileExistsError(f"Parent is not a directory: {parent}")
        if destination.is_symlink() and destination.resolve() == source:
            continue
        exists = destination.exists() or destination.is_symlink()
        if exists and not replace:
            raise FileExistsError(f"Conflict: {destination}; use --replace to back up existing entries")
        pending.append((destination, source, exists))

    desired = {destination for destination, _ in links}
    stale = []
    for kind in ("agents", "commands", "skills"):
        directory = config_dir / kind
        if not directory.is_dir():
            continue
        namespace = root / ("skills" if kind == "skills" else f"adapters/opencode/{kind}")
        for entry in directory.iterdir():
            owned = entry.is_symlink() and (
                entry.resolve().is_relative_to(namespace)
                or (kind == "skills" and entry.name == "my-ai-framework" and entry.resolve() == root)
            )
            if owned and entry not in desired:
                stale.append(entry)

    # Check all conflicts before writing anything. Keep backups outside discovery directories.
    backup_root = config_dir / "framework-backups" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    for destination, source, exists in pending:
        if exists:
            backup = backup_root / destination.relative_to(config_dir)
            print(f"Back up {destination} -> {backup}")
            if not dry_run:
                backup.parent.mkdir(parents=True, exist_ok=True)
                destination.rename(backup)
        print(f"Link {destination} -> {source}")
        if not dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.symlink_to(source, target_is_directory=source.is_dir())
    for entry in stale:
        print(f"Remove obsolete framework link {entry}")
        if not dry_run:
            entry.unlink()
    return links


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-dir", type=Path, default=default_config_dir())
    parser.add_argument("--replace", action="store_true", help="Back up conflicting entries before linking")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    args = parser.parse_args()
    try:
        install(args.config_dir, replace=args.replace, dry_run=args.dry_run)
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
