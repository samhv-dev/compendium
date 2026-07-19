# compendium

**A curated toolbox marketplace — hand-picked Claude-Code skills, repackaged as Cowork plugins.**

Most of these tools were published for **Claude Code**. Cowork wants the *skills*, not the
Claude-Code-only machinery, so each one is vendored here as a clean Cowork plugin (skills only;
hooks / MCP servers / commands / LSP stripped out). Every plugin keeps a link back to its upstream
GitHub repo and credits its original developer, and the whole catalog is kept current automatically.

## Add it in Cowork

1. In the Claude desktop app: **Customize → Plugins → Add marketplace**
2. Enter the repo: `samhv-dev/compendium` (or the full `https://github.com/samhv-dev/compendium` URL)
3. Browse the catalog and **Install** the plugins you want
4. Open the marketplace's settings and **Enable auto-update** — third-party marketplaces have it
   off by default, so this one-time toggle is what turns on hands-free updates.

Skills are namespaced by plugin, e.g. `clarify-crit`, `ponytail`, `improve`.

## Catalog & credits

Every plugin is the work of its upstream author, redistributed here under its original licence.
Full provenance also lives in each plugin's `SOURCE.md` and bundled `LICENSE`.

| Plugin | What it is | Upstream author | Source | Licence |
|---|---|---|---|---|
| `clarify-crit` | Request refinement (CRIT: Context, Role, Interview, Task) | lanveric | [lanveric/clarify-crit](https://github.com/lanveric/clarify-crit) | MIT |
| `improve` | Read-only codebase advisor → implementation plans | shadcn | [shadcn/improve](https://github.com/shadcn/improve) | MIT |
| `ponytail` | Lazy-senior-dev / YAGNI over-engineering guard | Dietrich Gebert | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | MIT |
| `emilkowalski-design` | Design-engineering & animation skills | Emil Kowalski | [emilkowalski/skills](https://github.com/emilkowalski/skills) | MIT |
| `superpowers-extracts` | 5 general-discipline skills (verification, planning, skill-writing, debugging, brainstorming) | Jesse Vincent (obra) | [obra/superpowers](https://github.com/obra/superpowers) | MIT |
| `tastemaker` | Gives an AI real design taste so UIs don't look AI-made | codeswithroh | [codeswithroh/tastemaker](https://github.com/codeswithroh/tastemaker) | MIT |
| `onebreath` | Terse-answer constraints: `/1s` one sentence, `/1p` one paragraph | louixs | [louixs/onebreath](https://github.com/louixs/onebreath) | MIT |
| `scientific-agent-skills` | 149 scientific & research skills (bio/chem/clinical/ML/lit-review/DBs) | K-Dense Inc. | [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | MIT¹ |
| `claude-d3js` | d3.js playbook for custom interactive data visualisations | Chris von Csefalvay | [chrisvoncsefalvay/claude-d3js-skill](https://github.com/chrisvoncsefalvay/claude-d3js-skill) | ⚠️ none² |
| `autostar` | Autonomous optimisation loop ("soft RLVR") — measurable-goal → verifier-driven experiments | Chris von Csefalvay | [chrisvoncsefalvay/autostar](https://github.com/chrisvoncsefalvay/autostar) | MIT |
| `science-superpowers` | 15 computational-science methodology skills (pre-registration, reproducibility, red-team review, verification) | K-Dense Inc. | [K-Dense-AI/science-superpowers](https://github.com/K-Dense-AI/science-superpowers) | MIT |

¹ MIT for the collection; individual skills carry their own licence in each `SKILL.md`.
² The upstream repository ships **no LICENSE file** (technically all-rights-reserved). It is redistributed here in good faith with full attribution, and **will be removed immediately on the author's request**.

## How updates work

`scripts/refresh.py` is the single vendoring engine. Driven by [`registry.json`](registry.json),
it clones each upstream, re-vendors its skills into `plugins/<name>/`, re-applies the Cowork
stripping, and rewrites [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json). If
nothing upstream changed, the rebuild is byte-identical and produces no commit.

The GitHub Action in `.github/workflows/refresh.yml` runs it weekly (and on manual dispatch),
committing any changes. Because plugin versions track upstream (or, for versionless skill repos,
an upstream-commit suffix), a real upstream change bumps the version, and Cowork's marketplace
auto-update then pulls it to your machine — end to end, no manual repackaging.

Run it yourself any time:

```bash
python3 scripts/refresh.py
```

## Add a new plugin

1. Add an entry to `registry.json` (`kind`: `plugin` for a Claude-plugin repo, `skill-wrap` for a
   bare skills repo, `local` for in-house).
2. Run `python3 scripts/refresh.py`.
3. Commit. The Action keeps it current from then on.

## Repackaging principle

These are faithful redistributions: skill content is copied verbatim from upstream. Only a Cowork
plugin wrapper, a `SOURCE.md`, and the upstream `LICENSE` are added, and Claude-Code-only components
are removed. No skill logic is modified. If you're an upstream author and would prefer a different
arrangement, open an issue.

## Licence

The marketplace tooling (`scripts/`, `registry.json`, this README) is MIT © samhv-dev — see
[LICENSE](LICENSE). Each vendored plugin retains its own upstream licence in its folder.
