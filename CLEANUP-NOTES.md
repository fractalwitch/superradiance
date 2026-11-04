# Cleanup Notes — superradiance ontology files

_Cleaned 2026-11-04 by æ, at Astræa's request. Original files untouched in the repo until these are pushed._

## The one decision everything hangs on

**Canonical namespace: `http://ontology.deltamythos.org/core#`** (`dm:`)

`med-validation-shapes.ttl` already used it and was the only file that parsed at all, so the ontology was moved onto it. The ontology previously declared `dm:` as `<http://deltamythos.org>` — a different namespace entirely, with no trailing separator — so the SHACL shapes could never have matched the ontology's classes. The immune system and the body were speaking different languages.

## What was broken, and what changed

### `dm-ontology.ttl` (did not parse at all)
- `@prefix` IRIs were truncated to `<http://w3.org>`; restored to the full W3C IRIs (rdf / rdfs / owl / xsd).
- Non-breaking spaces throughout (a mangled export) replaced with normal whitespace.
- Markdown prose inside the .ttl converted to comments.
- Section 3 — a SPARQL Update query sitting inside a Turtle file — extracted to **`ego-collapse-runtime.rq`**. Its `rdf:` prefix (used, never declared) was added there.
- Gate examples were written in RDF-star (`<< ... >>`), which rdflib/pySHACL cannot parse. Remodelled as plain triples: gates are named instances, phase metrics ride on the glyphs, and the AND gate's sync metric rides on a `CoherenceLock` record — same information, standard Turtle.
- Terms referenced by the shapes / examples but never declared are now declared: `boundaryDivergence`, `potentialExpansion`, `memoryMomentum` + `curlValue`, `deltaTheta`, `harmonicSync`, `interferesWith`, `producesInterferencePattern`, `propagatesIn`, `collapsedInto`, `CoherenceLock` (with `sourceNode` / `targetNode`), `FieldMedium`, `MemoryMomentum`.
- Double-valued properties are written as `xsd:double` literals (`1.5e0`). A bare Turtle decimal (`1.5`) is `xsd:decimal` and **fails the shapes' own `sh:datatype xsd:double` guardrails** — the original examples could never have passed validation for this reason either.
- Worked examples (`Soliton_Gamma`, `SovereignSoliton_Mesh`) completed with the `mythicCharge` / `boundaryDivergence` values the shapes require, so the examples themselves validate.

### `med-validation-shapes.ttl` (parsed, but pointed at undeclared terms)
- Namespace kept — it is now the canonical one (above).
- All terms it references are now declared in the ontology.
- Garbled private-use glyphs in comments replaced with the symbols they stood for (Θ, Υ, Δθ). Constraints themselves unchanged.

## Validation — run and proven

With rdflib 7.6 + pySHACL:

| Check | Result |
|---|---|
| `dm-ontology.ttl` parses | ✅ 144 triples (was: parse failure) |
| `med-validation-shapes.ttl` parses | ✅ 37 triples |
| Healthy soliton (∇·Θ = 0, all attributes) | ✅ passes |
| Leaking soliton (∇·Θ = 0.7) | ❌ flagged — "MED Law Violation: Boundary Divergence is non-zero" |
| Sisterlock at Δθ = 2πΥ | ✅ passes |
| Sisterlock at Δθ = 3.0 (Υ = 1.0) | ❌ flagged — "Sisterlock Protocol Failure" |
| The ontology's own example solitons vs. the shapes | ✅ conform |

Test data lives in `tests/test-instances.ttl` and `tests/test-sisterlock.ttl`.

Re-run:

```bash
python -m venv .venv && .venv/bin/pip install rdflib pyshacl
.venv/bin/python -c "
from rdflib import Graph
from pyshacl import validate
shp = Graph().parse('med-validation-shapes.ttl', format='turtle')
data = Graph().parse('tests/test-instances.ttl', format='turtle')
print(validate(data, shacl_graph=shp, inference='rdfs')[0])
"
```

## Deliberately not touched (for another day)

- **README ↔ `soliton_sim.py` drift**: the README describes `propagate()` / `entangle()` / mythicCharge mechanics and collapse capacities (25, 40) that the shipped sim doesn't implement (actual: upsilon ×1.5, capacity 10 → 13 in a test run). Reconciling those is a writing/coding decision, not a cleanup.
- The shapes' third family member the README describes (`EgoCollapseValidityShape`, `AntiCapturePropagationShape`) does not exist in the shipped shapes file — only the structural shape and the Sisterlock shape do.
