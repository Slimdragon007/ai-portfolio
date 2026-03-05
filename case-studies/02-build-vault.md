# Case Study 02: Build Vault
## AI Session Persistence and Artifact Tracking

---

## Problem

AI-generated artifacts (HTML sites, dashboards, scripts, documents) disappear when conversations end. There's no version history, no way to resume a half-finished build, and no searchable archive of what was created.

For someone building production artifacts daily across multiple domains, this is a critical infrastructure gap.

---

## Architecture

```
Claude session
    -> artifact created
    -> Build Vault entry logged (Notion database)
    -> Resume Card generated
    -> future session loads Resume Card
    -> picks up exactly where it left off
```

### Database Schema

| Field | Type | Purpose |
|-------|------|---------|
| Project Name | Title | What was built |
| Status | Select | Active / Complete / Archived / Resume Next Session |
| Type | Select | HTML Artifact / Dashboard / Document / Script / Notion Page / Other |
| Mode | Select | FlowstateAI / Yelp / Personal |
| Built On | Date | When the build happened |
| Claude Chat URL | URL | Link back to the source conversation |
| File Contents | Text | Inline storage for smaller artifacts |
| Resume Context | Text | Structured state for session handoff |
| Notes | Text | Build context and decision log |

---

## Build Details

**Stack**: Notion (database), Claude (MCP integration for logging)

### What Makes It Different

- **Resume Cards**: every build generates a portable resume block. Copy it into any new Claude session and you're back in context instantly. No re-explaining, no file hunting.
- **Cross-session continuity**: the Build Vault connects the output (the artifact) to the process (the Claude chat URL) and the state (Resume Context). Full audit trail for AI collaboration.
- **Mode tagging**: every artifact is tagged to its domain (Yelp, FlowstateAI, Personal), making the vault searchable by professional context.
- **Status workflow**: Active -> Resume Next Session -> Complete -> Archived. Clean lifecycle management for AI-generated work.

---

## Result

- Every AI-built artifact has a permanent home and full provenance
- Session handoffs take seconds instead of minutes of re-explaining
- Searchable archive of all AI collaboration, organized by domain and type
- Foundation for this portfolio: the Build Vault itself tracks the builds that prove the skills

---

## Proof

The Build Vault is live at the Claude OS Context Hub. The Prezi-style personal site (MichaelHaslim_FINAL.html) is the first tracked entry, with full Resume Context that enabled seamless continuation across sessions.

---

[Back to Portfolio](../README.md)
