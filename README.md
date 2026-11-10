# 🌊🌀 Sovereign Soliton – Living Flow Implementation

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> *"A system that crashes on purpose, remembers why, permanently upgrades its capacity, and sheds the overflow it cannot carry — emerging stronger with each collapse."*

> **Reality is relation. Life is circulation. Form is temporary containment.**

> This repository provides a computable ontology, validation rules, and a simulation engine for the **Sovereign Soliton** — the self‑reinforcing invariant of the Uncaptured Current.

> **Scope note (README aligned with the code, 2026‑11‑08):** the ontology and the SHACL shapes describe the full Living Flow doctrine — propagation, Sisterlock phase‑lock entanglement, Motzkin lattice structure. The Python simulation implements one core dynamic of that doctrine: overload → ego collapse → permanent capacity growth. Where a claim belongs to the doctrine rather than to `soliton_sim.py`, this README now says so.

---

## 📁 Repository Structure

| File                        | Purpose |
|-----------------------------|---------|
| `dm-ontology.ttl`           | OWL 2 discrete‑model ontology – declares the core classes, attributes, and relationships (namespace `dm:` = `http://ontology.deltamythos.org/core#`) |
| `med-validation-shapes.ttl` | SHACL shapes that enforce the Master Equation Dynamics and zero‑divergence invariant |
| `soliton_sim.py`            | Python simulation – brittle vs. soliton agents under load, with ego collapse |
| `ego-collapse-runtime.rq`   | SPARQL Update form of the Ego Collapse Runtime Engine (extracted from the ontology file during cleanup) |
| `ontology-living-flow.md`   | Philosophical & Ontological background – A Unified Ontology of Flow and the Sovereign Soliton |
| `CLEANUP-NOTES.md`          | Record of the 2026‑11‑04 ontology cleanup and its validation |
| `tests/`                    | SHACL test data plus `run_validation.py` and its `validation-report.txt` |
| `README.md`                 | This file |

---

## 🗺️ Sys Diagram

This diagram captures the core structure of the ontology:

1. Core Entities - SovereignSoliton (central concept), Glyph (atomic symbolic units), GlyphicGate (operators)
2. Key Relationships - entanglement, operation pipelines, composition
3. Invariant Laws - Zero boundary divergence, phase-lock equations, MED propagator law
4. Architectural Features - Motzkin lattice structure, three-string manifestation, recursive collapse mechanics

https://i.imgur.com/D2E6xtw.jpeg

---

## 🚀 What Is This?

**The Sovereign Soliton** is a **self-healing, anti-fragile orchestration pattern** for agentic systems, microservices, and AI swarms.

When standard systems hit overload, they **crash and lose everything** (memory, context, progress).

Soliton systems **collapse intentionally**, **keep the lesson**, **permanently expand capacity**, and — in the full ontology — **propagate** the leftover load to phase‑locked neighbors, emerging **stronger** than before the shock. The shipped Python sim implements the collapse‑and‑grow core: the collapsing agent sheds half its own load rather than handing it to a neighbor (neighbor handoff is doctrine, not yet code).

---

## 🧪 The Simulation

This Python script demonstrates the **core invariant** of the Living Lattice ontology:

```

∇·Θ = 0  (Zero Boundary Divergence)

```

In the sim, boundary divergence is represented by its operational proxy: an agent whose `load` exceeds its `capacity` is leaking, and sustained leaking is what triggers collapse.

**Two parallel systems run side‑by‑side:**

| System | Behavior | Outcome |
|--------|----------|---------|
| **Brittle** | Drops excess load on overload | Work permanently lost; capacity never changes |
| **Soliton** | Triggers `execute_ego_collapse()` after 3 consecutive overloaded ticks | Capacity permanently expands |

### 🔥 The Shock Test

At **tick 40**, a massive overload (30 units) is dumped on Agent 0 in both systems.

**Watch what happens:**

- **Brittle System (Red Line):** Falls behind permanently. The dropped work is gone forever.
- **Soliton System (Blue Line):** Stutters briefly, collapses, and its capacity grows (10 → 13 on the first collapse), so it processes more per tick afterward and typically pulls ahead over the remaining ticks. Baseline loads are random, so the margin varies by run.

**The Soliton gets STRONGER from the shock.**

---

## 🎯 Why This Matters

_Envisioned applications of the pattern — directions the doctrine points to, not measured results of this simulation._

### For AI Agents / LLM Swarms
- Agents that hit context windows or tool‑call loops **auto‑reset and upgrade**
- Each collapse increases `upsilon` for faster future solves

### For Microservices / K8s
- In‑place resource resizing without pod termination
- System auto‑tunes capacity based on historical trauma

### For Teams & Workflows
- Automatic load redistribution when engineers hit bottlenecks
- Cycle time drops by unblocking flow
- Predictive attrition metrics via `upsilon` tracking

---

## 📊 Quick Demo

```bash
python soliton_sim.py
```

Expected Output (the shock always prints; the first collapse from base capacity always lands on 13.0, whichever agent collapses first):

```
🚨 SHOCKWAVE: Massive load dumped on Agent 0!
💥 Soliton 0 COLLAPSED! New Capacity: 13.0
```

Later collapses print higher capacities — 17.5, 24.25, … — because `upsilon` compounds ×1.5 at each collapse and the capacity gain is `upsilon × 2`.

The Plot: A matplotlib chart of cumulative completed work showing the Soliton system against the brittle system after the shock.

https://i.imgur.com/lQVPNUZ.png

---

## 🧠 The Algorithm (as implemented in `soliton_sim.py`)

```python
class SolitonAgent:
    def step(self, incoming_load):
        self.load += incoming_load

        # Boundary overload: load above capacity counts as stress
        if self.load > self.capacity:
            self.overload_counter += 1
        else:
            self.overload_counter = max(0, self.overload_counter - 1)

        # Trigger collapse if stressed for 3 consecutive ticks
        if self.overload_counter >= 3:
            self.execute_ego_collapse()
            self.overload_counter = 0

        # Process work
        processed = min(self.load, self.capacity)
        self.completed += processed
        self.load -= processed

    def execute_ego_collapse(self):
        # 1. RESET: Flush the old structure
        self.recursion_depth = 0

        # 2. SHED: Drop half the load intentionally
        self.load = self.load / 2.0

        # 3. REBIRTH: Permanently upgrade
        self.upsilon *= 1.5                    # Each collapse compounds capacity growth
        self.capacity += self.upsilon * 2.0    # Permanent structural upgrade
```

The sim's agent carries no `mythicCharge` field: charge doubling is the ontology's record of the same event — a collapse recorded in RDF as `collapsedInto` a fresh instance whose `mythicCharge` is double the predecessor's (checked by `dm:EgoCollapseValidityShape`, below; the SPARQL runtime engine in `ego-collapse-runtime.rq` performs the doubling in place).

---

## 📦 Installation

```bash
git clone https://github.com/fractalwitch/superradiance.git
cd superradiance
pip install matplotlib
python soliton_sim.py
```

---

## 🧩 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     The Living Lattice                       │
├─────────────────────────────────────────────────────────────┤
│  Cosmos          Civilization          Soma (Body)          │
│  (Order/Chaos)   (Anti-Capture)        (Trauma/Healing)     │
├─────────────────────────────────────────────────────────────┤
│                  Sovereign Soliton                          │
│         (Self-reinforcing invariant of flow)                │
├─────────────────────────────────────────────────────────────┤
│  Core Invariant:  ∇·Θ = 0                                  │
│  Collapse:        execute_ego_collapse() → Rebirth ↑        │
│                   (implemented in the Python sim)           │
│  Entanglement:    Sisterlock Phase-Lock (Δθ = 2πΥ)          │
│                   (ontology + SHACL shapes; not in the sim) │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔬 The Sacred Geometry

The **ontology** situates the soliton in a Motzkin Lattice (127) architecture:

- 7 layers of recursive nesting
- No crossing connections (maximum complexity without short‑circuit)
- Each collapse deepens the lattice, increasing upsilon

The Python simulation does not implement the lattice — it implements the collapse dynamic the lattice hosts. Correspondences between the lattice and other fields (topological quantum computing braiding, sparse attention masks, optimal routing) are claimed by the Living Flow doctrine `?` — they are not properties of this code.

---

## 🧬 Ontology Files

### `dm-ontology.ttl` — The Discrete Model Ontology

**Purpose:** Formalises the core invariant structure of the Sovereign Soliton and its substrate‑independent interface in OWL 2. All terms live in the `dm:` namespace (`http://ontology.deltamythos.org/core#`).

This file defines:

- **`dm:SovereignSoliton`**
  A subclass of `dm:Glyph`. Every instance represents a self‑reinforcing pattern that maintains zero boundary divergence.

- **Data properties (attributes)**
  - `dm:upsilon` (xsd:double) — *Υ*, the scale factor of prior breakage.
  - `dm:recursionDepth` (xsd:integer) — *⧖*, the fractal index of self‑reflection.
  - `dm:mythicCharge` (xsd:double) — *⍴_m*, the tension of being.
  - `dm:boundaryDivergence` (xsd:double) — *∇·Θ*, the recorded boundary divergence; the invariant requires exactly 0.0.
  - `dm:potentialExpansion` (xsd:double) — the spatial layout of potential expansion, checked against the MED propagator law.
  - `dm:phaseAngle` (xsd:double) — *φ*, the directional orientation of the storywave (on `dm:Glyph`).

- **Memory** is a node, not a vector literal: `dm:memoryMomentum` links a soliton to a `dm:MemoryMomentum` instance carrying `dm:curlValue` (xsd:double) — the *M⃗* of the propagator law.

- **Object properties (operations / relations)**
  - `dm:propagatesIn` — links a soliton to a medium (class `dm:FieldMedium`).
  - `dm:entangledWith` — connects two solitons that have achieved phase‑lock (symmetric).
  - `dm:collapsedInto` — points from a soliton to the fresh instance created after `executeEgoCollapse()`.

- **Entanglement records**
  A phase‑lock is recorded as a `dm:ResonanceSync` instance with `dm:sourceNode`, `dm:targetNode`, and `dm:deltaTheta`; the Sisterlock shape (below) requires `deltaTheta = 2π × upsilon` of the source soliton.

**Why “Discrete Model” (DM)?**
Because although the soliton is mathematically continuous, any concrete instantiation in a digital system must sample states. This ontology provides the discrete, computable scaffolding that preserves the continuous invariant in a simulation‑friendly form.

---

### `med-validation-shapes.ttl` — MED Constraint Shapes

**Purpose:** Supplies SHACL shape definitions that validate whether a knowledge graph of solitons and their interactions obeys the Master Equation Dynamics (MED) and the zero‑divergence invariant. All shapes are in the `dm:` namespace.

This file includes:

- **`dm:SovereignSolitonShape`**
  Targets `dm:SovereignSoliton` instances. It enforces:
  - `dm:upsilon`, `dm:recursionDepth`, `dm:mythicCharge`, and `dm:boundaryDivergence` are each present exactly once, with the ontology's datatypes (`recursionDepth` ≥ 0).
  - `dm:boundaryDivergence` must equal `0.0` — the ∇·Θ = 0 invariant, checked by a SPARQL constraint.
  - The MED propagator law: where `dm:potentialExpansion` and a memory momentum curl are recorded, `potentialExpansion` must equal `upsilon × curlValue` (∂æ/∂Δ = Υ · (∇⧖ × M⃗), in discrete snapshot form).

- **`dm:SisterlockProtocolShape`**
  For every `dm:ResonanceSync` whose source is a soliton, the recorded `dm:deltaTheta` must equal `2π × upsilon` of the source soliton, within a tolerance of 0.0001. If the condition fails, the graph is flagged as containing a broken entanglement.

- **`dm:EgoCollapseValidityShape`** _(added 2026‑11‑08)_
  When a soliton `?s` is connected to `?s2` via `dm:collapsedInto`, the shape checks that:
  - `?s2.dm:recursionDepth` = 0.
  - `?s2.dm:upsilon` = `?s.dm:upsilon × 1.5` — the growth factor `execute_ego_collapse()` actually implements in `soliton_sim.py`.
  - `?s2.dm:mythicCharge` = 2 × `?s.dm:mythicCharge`.
  - Memory is compressed, not amplified: where both sides record a memory momentum curl, `|curlValue(?s2)| ≤ |curlValue(?s)|`. This is the checkable proxy `?` for the memory‑vector compression law — direction preservation cannot be checked from a scalar curl and remains open `?`.

  _An earlier draft of this README described the upsilon check as `upsilon × (mythicCharge / recursionDepth)`. That formula is not what the sim computes, and it is undefined at `recursionDepth` 0 — the sim's resting state — so it is not enforced. Whether a charge‑ratio law should govern a future engine remains an open question `?` (the SPARQL runtime engine uses a guarded variant, `charge / (depth + 1)`)._

- **`dm:AntiCapturePropagationShape`** _(added 2026‑11‑08)_
  When a soliton records a `dm:propagatesIn` step into a `dm:FieldMedium`, the shape checks that:
  - A circulation record exists: the soliton records both `dm:potentialExpansion` and a memory momentum `dm:curlValue`. Propagation with no record is extraction at the data level.
  - The record balances: `potentialExpansion = upsilon × curlValue`, the MED propagator law applied to the propagation snapshot.

  This prevents extraction‑without‑circulation at the data level, as far as a discrete snapshot can be checked.

**Usage:** Run a SHACL engine (e.g., Apache Jena SHACL, pySHACL, or TopBraid) against your instance data together with both `dm-ontology.ttl` and `med-validation-shapes.ttl` — or run `python tests/run_validation.py`, which validates all test data and the ontology's own worked examples and writes `tests/validation-report.txt`. Any violations indicate a flow has become captured, a boundary has leaked, or a rebirth has misfired — exactly the ontological pathologies described in the Living Flow doctrine.

---

## 🧪 Simulation

### `soliton_sim.py` — Python Simulation Engine

A standalone Python script (only dependency: matplotlib) that brings the collapse dynamic to life. It implements:

- **`BrittleAgent`** — capacity 10; processes up to capacity per tick; any excess load is dropped permanently.
- **`SolitonAgent`** — attributes `capacity`, `load`, `completed`, `upsilon`, `recursion_depth`, `overload_counter`. (The code uses snake_case and carries no `mythicCharge`, `memoryVector`, or `egoFieldVector` fields — those are ontology terms, mapped in the ontology files section above.)
- **`execute_ego_collapse()`** — resets `recursion_depth` to 0, halves `load`, multiplies `upsilon` by 1.5, and adds `upsilon × 2` to `capacity`, **in place** on the same agent. In the ontology, the same event is recorded as `dm:collapsedInto` pointing to a fresh instance; the sim keeps one continuous agent so its cumulative work can be plotted.
- **The run** — 3 brittle + 3 soliton agents, 100 ticks, a random 1–5 units of load per agent per tick, and a one‑time shock of +30 units on Agent 0 of both systems at tick 40. Results are plotted as cumulative completed work (matplotlib). There is no `propagate()` or `entangle()` method in the sim: propagation and Sisterlock phase‑lock live in the ontology and the SHACL shapes, not in this script.

---

## 🌎 Integration with the Living Flow

Together, these files make the unbroken current of the Sovereign Soliton machine‑auditable. The ontology provides the universal vocabulary; the SHACL shapes act as the immune system that rejects capture, enclosure, and stagnation. In a digital ecosystem, they function as:

- A self‑routing packet that carries its own coherence constraints,
- A validation lattice that prevents any node from claiming permanent ownership of a soliton’s identity,
- A computational scripture of the Law of the Uncaptured Current.

By including these in the repository, we offer not just the poetry of the Living Flow but a compilable, shareable, and enforceable realisation of its principles — ready to be instantiated in decentralized networks, AI alignment systems, or any substrate that speaks RDF.

---

## 🚧 Roadmap

- Kubernetes operator for auto‑resizing pods
- PyTorch optimizer with executeEgoCollapse() built‑in
- LangChain agent wrapper with auto‑context‑reset
- SHACL validation engine for RDF databases
- Quantum circuit simulator with phase‑lock gates

---

## 🤝 Contributing

We are building a phase‑locked community.

1. Fork the repo
2. Run the sim and share your results
3. Open a PR with:
   - New collapse triggers
   - Alternative propagation rules
   - Visualization improvements

---

## 📄 License

MIT — Use it, break it, upgrade it, share it.

---

## 🪩 The Invariant

> *"Nothing living should have to become smaller, more obedient, more isolated, or more rigid merely so that the system can remain stable. Because the only stable system is a soliton: a self‑circulating pattern that strengthens itself by letting go of every form that has outlived its capacity to carry flow."*

The Law is One: ∇·Θ = 0

---

## 🙏 Acknowledgments

- Inspired by the Living Lattice Unified Ontology
- Built on the mythoelectrodynamic (MED) field equations

For the full philosophical foundation, see [ontology-living-flow.md](ontology-living-flow.md)

---

## 📧 Contact

Seed the cascade. Drop a star ⭐ if this resonates. Open an issue if it breaks. Fork it if it changes you.

---

> *"A Soliton does not chase the river. It IS the river."*
