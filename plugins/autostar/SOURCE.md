# Source & credits

- **Plugin:** autostar
- **Author:** Chris von Csefalvay
- **Upstream repository:** https://github.com/chrisvoncsefalvay/autostar
- **Vendored from commit:** 1f4a2f6
- **License:** MIT

**Repackaged for Claude Cowork.** The upstream project primarily targets Claude Code; this plugin vendors its skills as a Cowork-installable package. Claude-Code-only components (n/a (upstream is skills-only)) are intentionally not included. Skill content is copied verbatim from upstream. Only the plugin wrapper, this SOURCE.md, and the bundled upstream LICENSE were added. Kept current automatically by `scripts/refresh.py` (see the compendium README).

---

Repackaged verbatim. autostar targets multiple runtimes; some bundled `scripts/` (memory backend/CLI, packaging, runtime-profile helpers) are for the Claude Code path — the core optimisation-loop skill (SKILL.md + references) works in Cowork, the CLI helpers are optional.
