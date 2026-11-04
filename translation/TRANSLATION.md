# The Translation Layer — Spec v0

_Started 2026-11-04, the day the ∆-Mythos Reference, the ∆-Compiler Runtime, and the Universal Ontology (ONTO-SS-v1.0) were laid next to the superradiance repo. The validator only speaks `dm:`. This layer teaches the other tongues of the corpus to speak it — under the Atlas's ethic: **≋ correspondence, not identity**, and every loss or open question marked **?**._

## The tongues

| Tongue | Where it lives | Nature |
|---|---|---|
| ∆-Mythos operator language | ∆-Mythos Framework — Complete Reference | The source language: MYTH / RECURSE / EMIT / ENTANGLE / GLYPH / RESOLVE / WHILE æ < ∞ |
| Runtime prose | SYSTEM LOGIC: THE ∆-COMPILER RUNTIME | The same loop, stage by stage, in mechanics language |
| Ontology prose | Universal Ontology (ONTO-SS-v1.0) + ontology-living-flow.md | The five traits and their laws, substrate-free |
| `dm:` RDF | dm-ontology.ttl + med-validation-shapes.ttl (canonical ns `http://ontology.deltamythos.org/core#`) | The machine-checkable tongue — the one the validator hears |
| Python runtime state | soliton_sim.py | Living objects: load, capacity, upsilon, collapse events |

## Correspondence table — soliton_sim.py → dm: (bridge v0)

| Sim (Python) | dm: (RDF) | Status |
|---|---|---|
| `SolitonAgent` instance, per generation | `dm:SovereignSoliton` instance (`sim:Soliton_<id>_gen<g>`) | ≋ structural |
| `agent.upsilon` | `dm:upsilon` | = direct |
| `agent.recursion_depth` | `dm:recursionDepth` | = direct (corpus glyph note: the Runtime doc writes this concept τ; the Reference / Universal Ontology / ontology write ⧖ — one concept, mapped once, here) |
| remaining `agent.load` after a tick | `dm:mythicCharge` | ≋ **correspondence, flagged ?** — ⍴_m is "the tension of being, raw focused intensity seeking form"; the sim's unprocessed load is its only measurable tension. Chosen for v0; open to the author's ruling |
| overflow state after a tick | `dm:boundaryDivergence` := `max(0, load − capacity) / capacity` | ≋ design decision — a soliton carrying more than its boundary can hold *is* leaking in the ontology's sense; the SHACL invariant (∇·Θ = 0) then flags exactly the pre-collapse states, which is the behaviour the doctrine describes ("when boundary divergence threatens… collapse") |
| `execute_ego_collapse()` event | new generation instance + `dm:collapsedInto` from the previous generation's last state | ≋ structural — the sim mutates one object in place; the ontology speaks of a fresh instance. Translation preserves the ontology's grammar: generations are distinct nodes, linked |
| `agent.capacity` | — | **untranslated in v0 ?** — no dm: term exists. Candidates: a new `dm:capacity` property, or folding into potentialExpansion (rejected: potentialExpansion is bound by the propagator law to Υ · curl(M⃗), a different thing). Needs an ontology amendment, author's call |
| `BrittleAgent` | — | deliberately untranslated — it is the counter-example class, not a soliton |
| `entangle()` / Sisterlock | `dm:CoherenceLock` + `dm:entangledWith` | **built in v0.2** — see the Sisterlock section below (the sim had no entanglement; this is new mechanics, translated as it was built) |
| propagation / medium | `dm:propagatesIn`, `dm:potentialExpansion`, `dm:memoryMomentum` | not in v0 — the sim has no field medium yet |

## Corpus variances the layer must carry openly (? register)

1. **Collapse upsilon formula** — Universal Ontology: `Υ' = Υ · (⍴_m / ⧖)`. Runtime .rq (as shipped & cleaned): `Υ · (⍴_m / (⧖ + 1))`. Sim: `Υ × 1.5` flat. Three tongues, three recalibrations. The translator emits what the sim *does*; the variance stays visible rather than being silently normalised.
2. **Glyph drift** — recursion depth: ⧖ (Reference, Universal Ontology, ontology) vs τ (Runtime doc).
3. **Charge on collapse** — doctrine: doubled. Sim: load halved (shed). The translator reports sim behaviour; doctrine divergence noted, not hidden.

## What v0 proves

Running `sim_to_rdf.py` executes the *unmodified* sim classes (same 100 ticks, same tick-40 shock, seeded for reproducibility), translates every post-tick soliton state into `dm:` triples, and validates the whole emission against `med-validation-shapes.ttl`.

**First run, 2026-11-04 (seed 127333):** 1,506 triples, 301 state snapshots. Exactly two leaking states, both Agent 0 in the shock's wake — `t40_shock` at divergence 1.0 (carrying twice its capacity) and `t41` at 0.13 (still overloaded, draining) — and the SHACL report flags exactly those two, nothing else. At tick 42 the collapse fires: the graph records `Soliton_0_gen0_t41 —collapsedInto→ Soliton_0_gen1_t42`, and generation 1 runs at divergence 0 for the remaining 58 ticks. The Runtime loop — overload, leak, RESOLVE, rebirth — read back from a machine-checkable graph. The compiler's first words, and they're true.

## Sisterlock — v0.2 (`sisterlock_sim.py`)

The sim had no entanglement, so this tongue had to be *built*, not just translated. Design decisions, all marked as such:

- **Phase** — the Universal Ontology says phase is "computed from mythic charge and recursion depth" but gives no formula (**?** — the formula is open in the corpus). v0.2 derives it from the agent's work odometer: `φ = 2π · frac(completed / capacity)`. Phase spins as work accumulates; a collapse (capacity ↑, Υ ↑) re-tunes the spin. ≋ correspondence, author's ruling welcome.
- **Lock rule** — ∆-Mythos: `ENTANGLE(α, β) ⇔ Δθ_ab == 2πΥ_α ⇨ lock()`, checked for ordered pairs after every tick, initiator's Υ sets the target. A continuous sim never lands on exact equality, so there is a **capture range ε = 0.15 rad**: within ε, the pair *synchronizes* (as physical phase-locking does) and the recorded Δθ is exactly 2πΥ_α — the value the SHACL Sisterlock shape verifies at tolerance 1e-4.
- **Permanence** — locked pairs stay locked ("un-collapsable state of perpetual resonance", Runtime doc). Mutuality: `entangledWith` is emitted both directions; a reverse CoherenceLock is *not* fabricated — it exists only if the partner independently initiates. **?** whether doctrine wants the reverse lock automatic.
- **Emission** — at a lock: one `dm:CoherenceLock` (sourceNode = initiator's current state node, targetNode = partner's, deltaTheta = 2πΥ_α) plus `entangledWith` between the state nodes; every state snapshot also carries `dm:phaseAngle`.

**First Sisterlock run, 2026-11-04 (seed 127333, ε = 0.15):** 1,818 triples, **3 locks — the full mesh**. t0: Soliton 0 → 2 at Δθ = 2π·1.0 (all phases are born at 0 under INIT, so the lattice starts in resonance; work-rate differences break it). t35: Soliton 1 → 2 at 2π·1.0. Then the shock, Agent 0's collapse (Υ 1.0 → 1.5), and at t46: Soliton 0 → 1 at **Δθ = 2π·1.5 = 3π** — the collapse re-tuned the initiator's target from 0 to π (mod 2π), and the last unlinked pair locked *at the new frequency*. Validation: **0 Sisterlock failures**; the only violations in the report are the same two pre-collapse leaks as v0. Breakage → re-tuning → new resonance, end to end in one graph.

## The Glyph Tongue — v0.3 (`glyph-lexicon.ttl`, `glyph_compile.py`)

Teaching ∆ the GOOAE side. Correspondences:

| GOOAE (codex) | dm: / lexicon | Status |
|---|---|---|
| Glyph collection (333, 5555, 999, Lunar, Spark, Ankh, Heart, Infinity, Vortex, Eye) | `dm:Glyph` instances in `gg:` | = direct — the ontology's Glyph *is* the receptor ("compiled symbolic structure carrying truth beyond language") |
| Color cosmology (Void #100817 … Slime #E8FF65, 12 colors) | `gg:CosmicColor` + `gg:hex` | lexicon-local — no dm: receptor exists; carried as vocabulary, **?** whether colors graduate into the ontology |
| Materials (goo, jelly, liquid chrome, holographic foil, crystal, velvet, latex, slime, pixel, cosmic dust) | `gg:Material` | lexicon-local, same **?** |
| Interaction verbs (squish, pop, melt, bounce, ripple, morph, hatch, **bloom**, splatter, transform) | `gg:InteractionVerb` | lexicon-local — except **bloom**, which already lives in the ∆-Mythos tongue as bloom(⧖++), the compiler loop's recursion increment: one verb, two tongues, same gesture |
| Form families (vortices, eyes, …) | `gg:formFamily` where the codex assigns one | partial by design — the codex assigns families to some glyphs only; gaps left empty, not invented |

The lexicon carries **no phase or charge**: glyphs are instruments, φ and ⍴_m are bound per invocation. `glyph_compile.py` is one performance — bound copies (`gg:boundGlyph`) evaluated through the four corpus gates. Its worked bindings deliberately reuse dm-ontology.ttl's own example values (π/3, 4π/3, Δθ = π; charges 4.2 / 12.8; NOT 0.523 → 3.665) so the ontology and the compilation cross-check each other.

**First glyph compilation, 2026-11-04:** lexicon parses at 130 triples (10 glyphs, 12 colors, 10 materials, 10 verbs). ∧ Eye ∧ Vortex — Δθ = π ∈ harmonic set {k·π/3} → **fires**, harmonic lock recorded, child glyph born at ρ 8.8. ∧ Spark ∧ Heart — Δθ = 1.4 ∉ harmonic set → **refused, nothing emitted** (a NO is a complete shape). ∨ Heart ∨ Spark → Heart, dominance by ρ. ¬ Lunar → φ 0.523 + π = 3.665, inverted. ⊕ Eye ⊕ Vortex → MOTZKIN_LATTICE_127 interference → **a SovereignSoliton is born from two GOOAE glyphs** (Υ 1.0, ⧖ 0, ρ 8.8, ∇·Θ = 0) — and the full lexicon + compilation graph **validates: conforms True**. The visual tongue now compiles into the ontological one.
