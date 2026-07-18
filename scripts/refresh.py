#!/usr/bin/env python3
"""
compendium — refresh / repackaging engine.

Single source of truth for building the marketplace's vendored plugins from their
upstream GitHub sources AND for keeping them up to date. Run with no arguments:

    python3 scripts/refresh.py

It clones each tracked upstream, vendors it into ./plugins/<name>/ as a Cowork plugin,
and rewrites ./.claude-plugin/marketplace.json. In CI, the workflow commits whatever
changed. If nothing upstream changed, the rebuild is byte-identical and git shows no diff.

WHY THIS EXISTS (Cowork repackaging):
    The upstream projects here mostly target *Claude Code*. Cowork wants the SKILLS, not
    the Claude-Code-only machinery. So for every plugin we vendor the skills and STRIP the
    Claude-Code-only component keys (hooks, mcpServers, lspServers, commands, agents, ...)
    from the plugin manifest. This stripping is re-applied on every refresh, so automatic
    updates stay Cowork-clean.

kinds (see registry.json):
    plugin      upstream is itself a Claude plugin  -> copy its .claude-plugin/plugin.json
                (stripped) + the named skills + LICENSE
    skill-wrap  upstream is a bare skills repo       -> keep our wrapper plugin.json, vendor
                the named skills + upstream LICENSE
    local       authored in-house, no upstream       -> never rebuilt; included in the
                catalog from its existing vendored copy
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = json.loads((ROOT / "registry.json").read_text())
PLUGINS_DIR = ROOT / "plugins"
MP_PATH = ROOT / ".claude-plugin" / "marketplace.json"

# Claude-Code-only manifest keys removed when repackaging for Cowork.
CC_ONLY_KEYS = ["hooks", "mcpServers", "lspServers", "commands", "agents",
                "statusLine", "statusline", "outputStyles"]
# Repo-meta files that should not be copied inside a skill directory.
SKILL_DENYLIST = {"LICENSE", "LICENSE.md", "LICENSE.txt", "README.md", "CHANGELOG.md",
                  "CONTRIBUTING.md", ".git", ".gitignore", ".DS_Store"}


def run(args, **kw):
    return subprocess.run(args, check=True, capture_output=True, text=True, **kw).stdout.strip()


def clone(owner, repo, ref):
    d = tempfile.mkdtemp(prefix=f"cmp-{repo}-")
    url = f"https://github.com/{owner}/{repo}.git"
    args = ["git", "clone", "--depth", "1"]
    if ref:
        args += ["--branch", ref]
    args += [url, d]
    subprocess.run(args, check=True, capture_output=True, text=True)
    sha = run(["git", "-C", d, "rev-parse", "--short", "HEAD"])
    return pathlib.Path(d), sha


def frontmatter_version(path):
    txt = pathlib.Path(path).read_text()
    m = re.search(r"^---\s*\n(.*?)\n---", txt, re.S)
    if not m:
        return None
    v = re.search(r"^version:\s*[\"']?([^\"'\n]+)", m.group(1), re.M)
    return v.group(1).strip() if v else None


def copy_skill(src_dir, dest_dir):
    src_dir = pathlib.Path(src_dir)
    dest_dir = pathlib.Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    for item in src_dir.iterdir():
        if item.name in SKILL_DENYLIST:
            continue
        target = dest_dir / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)


def ensure_credit(manifest, credit):
    """Fill in provenance fields on a vendored manifest without clobbering upstream values."""
    for key in ("homepage", "repository", "license"):
        if credit.get(key) and not manifest.get(key):
            manifest[key] = credit[key]
    if credit.get("author") and not manifest.get("author"):
        manifest["author"] = credit["author"]
    return manifest


def write_source_md(pdir, spec, sha):
    up = spec.get("upstream", {})
    url = f"https://github.com/{up.get('owner')}/{up.get('repo')}" if up else \
        spec.get("credit", {}).get("repository", "")
    author = (spec.get("wrapper_plugin_json") or {}).get("author") or spec.get("credit", {}).get("author", {})
    author_name = author.get("name", "unknown") if isinstance(author, dict) else str(author)
    kind = spec["kind"]
    if kind == "local":
        body = (
            f"# Source & credits\n\n"
            f"- **Plugin:** {spec['name']}\n"
            f"- **Author:** {author_name}\n"
            f"- **Repository:** {url}\n"
            f"- **License:** {spec.get('credit', {}).get('license', 'MIT')}\n\n"
            f"Authored in-house — no external upstream. This compendium marketplace is its "
            f"canonical home; it is not auto-refreshed.\n"
        )
    else:
        strip = "hooks, MCP servers, commands, LSP" if kind == "plugin" else "n/a (upstream is skills-only)"
        body = (
            f"# Source & credits\n\n"
            f"- **Plugin:** {spec['name']}\n"
            f"- **Author:** {author_name}\n"
            f"- **Upstream repository:** {url}\n"
            f"- **Vendored from commit:** {sha}\n"
            f"- **License:** {(spec.get('wrapper_plugin_json') or spec.get('credit') or {}).get('license', 'MIT')}\n\n"
            f"**Repackaged for Claude Cowork.** The upstream project primarily targets Claude "
            f"Code; this plugin vendors its skills as a Cowork-installable package. "
            f"Claude-Code-only components ({strip}) are intentionally not included. Skill content "
            f"is copied verbatim from upstream. Only the plugin wrapper, this SOURCE.md, and the "
            f"bundled upstream LICENSE were added. Kept current automatically by "
            f"`scripts/refresh.py` (see the compendium README).\n"
        )
    (pdir / "SOURCE.md").write_text(body)


def build_plugin(spec):
    name = spec["name"]
    pdir = PLUGINS_DIR / name
    up = spec["upstream"]
    clone_dir, sha = clone(up["owner"], up["repo"], up.get("ref"))

    # fresh vendored dir
    if pdir.exists():
        shutil.rmtree(pdir)
    (pdir / ".claude-plugin").mkdir(parents=True, exist_ok=True)

    # ---- manifest ----
    if spec["kind"] == "plugin":
        manifest = json.loads((clone_dir / spec["plugin_src"] / "plugin.json").read_text())
        for k in CC_ONLY_KEYS + spec.get("strip_keys", []):
            manifest.pop(k, None)
        manifest = ensure_credit(manifest, spec.get("credit", {}))
    else:  # skill-wrap
        manifest = dict(spec["wrapper_plugin_json"])

    # ---- version ----
    vspec = spec["version"]
    if vspec["type"] == "plugin_json":
        version = json.loads((clone_dir / spec["plugin_src"] / "plugin.json").read_text()).get("version", "0.0.0")
    elif vspec["type"] == "skillmd":
        version = frontmatter_version(clone_dir / vspec["path"]) or vspec.get("base", "0.0.0")
    elif vspec["type"] == "sha":
        version = f"{vspec.get('base', '0.0.0')}+g{sha}"
    else:
        version = "0.0.0"
    manifest["version"] = version
    (pdir / ".claude-plugin" / "plugin.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")

    # ---- skills ----
    skills_root = clone_dir / spec.get("skills_src", "") if spec.get("skills_src") else clone_dir
    for s in spec["skills"]:
        copy_skill(skills_root / s["src"], pdir / "skills" / s["dest"])

    # ---- license + source ----
    lic = spec.get("license_src")
    if lic and (clone_dir / lic).exists():
        shutil.copy2(clone_dir / lic, pdir / "LICENSE")
    write_source_md(pdir, spec, sha)

    shutil.rmtree(clone_dir, ignore_errors=True)
    return version


def marketplace_entry(spec, version):
    """Build one marketplace.json plugin entry from the vendored manifest + registry credit."""
    manifest = json.loads((PLUGINS_DIR / spec["name"] / ".claude-plugin" / "plugin.json").read_text())
    credit = spec.get("credit") or spec.get("wrapper_plugin_json") or {}
    entry = {
        "name": spec["name"],
        "source": spec["name"],  # resolved under metadata.pluginRoot = ./plugins
        "description": manifest.get("description", ""),
        "version": version or manifest.get("version", "0.0.0"),
    }
    for key in ("author", "homepage", "repository", "license", "keywords"):
        val = manifest.get(key) or credit.get(key)
        if val:
            entry[key] = val
    return entry


def main():
    entries = []
    for spec in REG["plugins"]:
        if spec.get("track") and spec["kind"] != "local":
            version = build_plugin(spec)
            print(f"  vendored {spec['name']:22s} v{version}  <- {spec['upstream']['owner']}/{spec['upstream']['repo']}")
        else:
            # local / untracked: keep existing vendored copy, read its version
            pj = PLUGINS_DIR / spec["name"] / ".claude-plugin" / "plugin.json"
            version = json.loads(pj.read_text()).get("version", "0.0.0") if pj.exists() else "0.0.0"
            print(f"  kept     {spec['name']:22s} v{version}  (local / not auto-refreshed)")
        entries.append(marketplace_entry(spec, version))

    marketplace = {
        "$schema": "https://json.schemastore.org/claude-code-marketplace.json",
        "name": REG["marketplace"]["name"],
        "owner": {"name": "samhv-dev"},
        "description": "A curated toolbox of hand-picked Claude-Code skills repackaged as Cowork plugins, each credited to its upstream author and kept current automatically.",
        "metadata": {"pluginRoot": "./plugins"},
        "plugins": entries,
    }
    MP_PATH.parent.mkdir(parents=True, exist_ok=True)
    MP_PATH.write_text(json.dumps(marketplace, indent=2, ensure_ascii=False) + "\n")
    print(f"\nwrote {MP_PATH.relative_to(ROOT)} with {len(entries)} plugins")


if __name__ == "__main__":
    main()
