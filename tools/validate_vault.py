"""Read-only validation of LandGrand links, configuration, and retained sources."""
from pathlib import Path
import argparse
import hashlib
import json
import re


def validate(vault, manifest_path):
    vault = vault.resolve()
    files = [p for p in vault.rglob('*') if p.is_file()]
    notes = [p for p in files if p.suffix.lower() == '.md']
    errors = []
    links = 0
    checked = 0
    config_count = 0
    if not vault.is_dir():
        errors.append(f'Vault directory does not exist: {vault}')
    elif not notes:
        errors.append(f'No Markdown notes found in vault: {vault}')
    by_name = {}
    for path in files:
        for key in {path.name, path.stem}:
            by_name.setdefault(key, []).append(path)
    headings = {}
    blocks = {}
    for path in notes:
        text = path.read_text(encoding='utf-8-sig')
        headings[path] = set(re.findall(r'^#{1,6}\s+(.+?)\s*#*\s*$', text, re.M))
        blocks[path] = set(re.findall(r'\^([\w-]+)\s*$', text, re.M))
    for path in notes:
        text = path.read_text(encoding='utf-8-sig')
        for raw in re.findall(r'\[\[([^\]]+)\]\]', text):
            links += 1
            target = raw.split('|', 1)[0]
            dest, _, anchor = target.partition('#')
            candidates = [vault / dest, vault / (dest + '.md')] if dest else [path]
            resolved = next((p.resolve() for p in candidates if p.is_file()), None)
            if resolved is None:
                matches = by_name.get(dest, [])
                if len(matches) == 1:
                    resolved = matches[0]
                elif len(matches) > 1:
                    errors.append(f'{path.relative_to(vault)}: ambiguous link {target}')
                    continue
            if resolved is None:
                errors.append(f'{path.relative_to(vault)}: missing link {target}')
            elif anchor and resolved.suffix.lower() == '.md':
                valid = anchor[1:] in blocks.get(resolved, set()) if anchor.startswith('^') else anchor in headings.get(resolved, set())
                if not valid:
                    errors.append(f'{path.relative_to(vault)}: missing anchor {target}')
    for path in (vault / '.obsidian').glob('*.json'):
        config_count += 1
        try:
            json.loads(path.read_text(encoding='utf-8-sig'))
        except (ValueError, OSError) as exc:
            errors.append(f'{path.name}: invalid JSON: {exc}')
    try:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
        for entry in manifest['files']:
            relative = Path(entry['path'])
            path = (vault / relative).resolve()
            if not path.is_relative_to(vault):
                errors.append(f'Integrity manifest path leaves vault: {entry["path"]}')
                continue
            checked += 1
            if not path.is_file():
                errors.append(f'Missing retained file: {entry["path"]}')
            elif hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256'].lower():
                errors.append(f'Retained file changed: {entry["path"]}')
    except (ValueError, OSError, KeyError, TypeError) as exc:
        errors.append(f'Invalid integrity manifest: {exc}')
    return {'notes': len(notes), 'internal_links_checked': links, 'configurations_checked': config_count,
            'retained_files_checked': checked, 'errors': errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vault', type=Path, default=Path(__file__).resolve().parent.parent / 'LandGrand')
    parser.add_argument('--manifest', type=Path, default=Path(__file__).resolve().with_name('source-integrity.json'))
    args = parser.parse_args()
    result = validate(args.vault, args.manifest)
    print(json.dumps(result, indent=2))
    return bool(result['errors'])


if __name__ == '__main__':
    raise SystemExit(main())
