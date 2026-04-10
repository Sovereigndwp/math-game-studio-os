# Taskade Exports — Raw Source Staging

This directory holds **raw, unprocessed exports** from the Taskade space that drives the live operating layer of the studio. Durable content from these exports is normalized into permanent repo locations (see the mapping table below); this directory is the provenance backup so that normalized content can always be traced back to its source.

Do **not** use files in this directory as operational sources of truth. Use the normalized locations.

## Provenance

| Field | Value |
|---|---|
| **Source repo** | `github.com/Sovereigndwp/math-games` |
| **Source branch** | `main` |
| **Source description** | "Exported from Taskade" |
| **Taskade space ID** | `63ifx7l9wtgfvsop` |
| **Taskade space name** | `Concept Journey Dashboard` |
| **Taskade space emoji** | 🔥 |
| **Taskade space visibility** | `collaborator` |
| **Taskade space URL** | `https://www.taskade.com/spaces/63ifx7l9wtgfvsop/app/default/preview` |
| **Export format version** | `1.0` |
| **Source environment** | `production` |
| **Exported from Taskade** | `2026-04-10T14:51:53.528Z` |
| **Cloned into this repo** | `2026-04-10` |
| **Snapshot matches** | `manifest.json` in this directory |

## Layout

```
taskade_exports/
├── README.md                     ← this file
├── manifest.json                 ← Taskade space metadata (authoritative)
├── projects/                     ← 24 project JSONs (Quill delta tree format)
├── agents/                       ← 17 agent definition JSONs
├── automations/                  ← 15 workflow/automation JSONs
├── apps/default.json             ← Taskade runtime app state (UI config, transient)
├── media/                        ← media directory placeholders from the Taskade export (all empty in this snapshot)
└── markdown_renderings/          ← 23 markdown + 1 jpeg flattened from Taskade (lossy)
```

### `projects/`

Each file is named by Taskade project ID (e.g. `pBj7H2VZq1WPfZBs.json`). The root object is a Quill-style delta tree: `{root: {type: "root", children: [...]}}`. Text nodes carry their content under `text.ops[]` with formatting attributes. These are authoritative — the `markdown_renderings/` files are lossy flattenings of the same trees.

Project ID → human title mapping (as of this snapshot):

| ID | Title | Size |
|---|---|---|
| `1A7jTuKq9Zqa1sMF` | Echo Heist — Question Audit Results | 217 KB |
| `5SRug2XHWm5ky39N` | *external scrape: GMTK / "How to find game ideas"* | 159 KB |
| `6ra74LfBTu38GdVF` | Genesis Build Progress — Math Game Studio OS | 661 KB |
| `72ZxzsrS1yu4cUnR` | Bakery Rush — Question Audit Results | 45 KB |
| `9a1qJTArrd2EgdUh` | Meaningful Fix / Playtest / Audit / Reference Extraction / Pass Closure | 20 KB |
| `9bfNR2acXuAHiWyC` | Prototype Specifications | 732 KB |
| `AhQEf6x9M4aL3vKS` | Pass Rules | 230 KB |
| `L3WGWvXe4GsP2Eep` | *external scrape: Mathigon* | 80 KB |
| `LnpYq2qGt5DrXpda` | Game Concepts Pipeline | 1.2 MB |
| `Mvouna45U9uP6Vk4` | Snack Line Shuffle — Question Audit Results (v2) | 67 KB |
| `N9S2kjQdv3s7tyya` | Game Family Registry | 130 KB |
| `RoSBoqumnZCn8PSi` | *external scrape: awesome-game-design repo README* | 120 KB |
| `WnpdzZdJdDu3GUtH` | *external scrape: Prodigy marketing page* | 60 KB |
| `YP3v6uyRFV38x3mR` | Execution Handoff | 32 KB |
| `ZpbMJ7Dvpt9NVxmN` | Fire Dispatch — Question Audit Results | 59 KB |
| `c1De995aCmGDJhy3` | PORTFOLIO | 34 KB |
| `cyt3zvpjf32D1Ddt` | Misconception Library | 82 KB |
| `estDxAUXWBeMtJet` | Snack Line Shuffle — Question Audit Results (v3) | 55 KB |
| `fQKsxPJWgG2kPRoQ` | K-12 Curriculum Map | 96 KB |
| `gHvckrSZso2Mpp4q` | Math Game Studio OS | 151 KB |
| `hdmGqCEhxF8TS6Ei` | Snack Line Shuffle — Question Audit Results (v1) | 80 KB |
| `kVuJPKGWsBcgeGcH` | K-12 Subject & Skill Registry | 26 KB |
| `m4UNd8SUQQ4A45zf` | Trig Tower — HS Trigonometry Game | 41 KB |
| `pBj7H2VZq1WPfZBs` | Build Standards Checklist — Prototype Engineer → Software Developer Gate | 59 KB |

Three separate Taskade projects share the title "Snack Line Shuffle — Question Audit Results" (`hdmGqCEhxF8TS6Ei`, `Mvouna45U9uP6Vk4`, `estDxAUXWBeMtJet`). These are separate project records in Taskade and are preserved as-is; the normalized version in `concepts/snack-line-shuffle/question_audit.md` is the superset.

### `markdown_renderings/`

Pre-existing markdown flattenings that were originally dropped into `docs/` and moved here during normalization. These are lossy (they lose Quill formatting metadata, custom field values, and board-view state). Use `projects/*.json` if you need the authoritative version.

### `agents/` and `automations/`

Each file is a Taskade agent or workflow definition. These drive the live operating layer documented in `docs/taskade_app_reference.md`. They are not normalized into the repo because the repo is not the source of truth for the live Taskade operational state — it is the source of truth for durable artifacts.

### `apps/default.json` and `media/`

Runtime app state and media-placeholder directories. Transient. Preserved for completeness of the snapshot only.

## Normalization mapping

| Taskade source | Normalized location |
|---|---|
| `projects/pBj7H2VZq1WPfZBs.json` | `docs/build_standards_gate.md` |
| `projects/hdmGqCEhxF8TS6Ei.json` + `Mvouna45U9uP6Vk4.json` + `estDxAUXWBeMtJet.json` | `concepts/snack-line-shuffle/question_audit.md` |
| `projects/9bfNR2acXuAHiWyC.json` (SLS section) | `concepts/snack-line-shuffle/p1_engineer_handoff.md` |
| `projects/fQKsxPJWgG2kPRoQ.json` (SLS entry) | `concepts/snack-line-shuffle/curriculum_map.md` |
| `projects/6ra74LfBTu38GdVF.json` (Fire Dispatch lessons section only) | `artifacts/learning_captures/2026-04-09-fire-dispatch-audit-lessons.md` |
| `projects/1A7jTuKq9Zqa1sMF.json` | `artifacts/qa_audits/echo-heist-audit-2026-04-07.md` |
| `projects/ZpbMJ7Dvpt9NVxmN.json` | `artifacts/qa_audits/fire-dispatch-audit.md` |
| `projects/72ZxzsrS1yu4cUnR.json` | `artifacts/qa_audits/bakery-rush-audit.md` |
| `projects/N9S2kjQdv3s7tyya.json` + `LnpYq2qGt5DrXpda.json` + `c1De995aCmGDJhy3.json` + `m4UNd8SUQQ4A45zf.json` (non-packetized games only) | `docs/taskade_concept_inbox.md` |
| `projects/RoSBoqumnZCn8PSi.json` (scrape) | `references/external/awesome-game-design.md` |
| `projects/L3WGWvXe4GsP2Eep.json` (scrape) | `references/external/mathigon.md` |
| `projects/WnpdzZdJdDu3GUtH.json` (scrape) | `references/external/prodigy.md` |
| `projects/5SRug2XHWm5ky39N.json` (scrape) | `references/external/gmtk-how-to-find-game-ideas.md` |
| `agents/*` + `automations/*` (summary only) | updates to `docs/taskade_app_reference.md` |

## Rules for this directory

1. **Do not edit** any file under `projects/`, `agents/`, `automations/`, `apps/`, `media/`, or `manifest.json`. These are an immutable snapshot.
2. **Do not use** files here as operational sources of truth. Use the normalized repo locations.
3. **Refresh policy** — when a new Taskade export is pulled from `github.com/Sovereigndwp/math-games`, replace the contents of this directory wholesale and re-run normalization, rather than patching files in place.
4. **Markdown renderings** under `markdown_renderings/` may drift from the JSON source. If there is ever a discrepancy, trust the JSON.
5. **PII** — no Taskade-side PII (real student data, playtest participant identities) should be in this directory. If such data appears, escalate before committing.
