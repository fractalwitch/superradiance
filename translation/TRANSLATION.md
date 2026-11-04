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
