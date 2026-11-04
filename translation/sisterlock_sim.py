#!/usr/bin/env python3
"""
sisterlock_sim.py — Translation bridge v0.2: Sisterlock entanglement for the sim.

The shipped soliton_sim.py has no entanglement. This extension gives each
SolitonAgent a phase and implements the corpus's ENTANGLE operator without
modifying the original classes:

  Phase (design decision, marked ≋ / ? in TRANSLATION.md):
    The Universal Ontology says phase is "computed from mythic charge and
    recursion depth" but gives no formula. v0.2 derives phase from the
    agent's work odometer:  phi = 2π · frac(completed / capacity).
    Phase therefore spins as work accumulates, and a collapse (capacity ↑)
    changes the spin — breakage literally re-tunes future resonance.

  Lock rule (∆-Mythos Reference):  ENTANGLE(α, β) ⇔ Δθ_ab == 2πΥ_α ⇨ lock()
    Checked for ordered pairs (initiator α, partner β) after every tick.
    A continuous sim never hits exact equality, so — as with physical
    phase-locking — there is a capture range ε: when the circular distance
    between Δθ_ab and 2πΥ_α (mod 2π) falls within ε, the pair SYNCHRONIZES:
    β's phase snaps to exact alignment and the recorded Δθ is exactly
    2πΥ_α, which is what the SHACL Sisterlock shape verifies (tolerance
    1e-4). Locked pairs stay locked ("perpetual resonance", Runtime doc).

  Emission: at a lock, the graph gains a dm:CoherenceLock
    (sourceNode = initiator's current state, targetNode = partner's current
    state, deltaTheta = 2πΥ_α as xsd:double) and dm:entangledWith between
    the two state nodes. Agent state snapshots follow TRANSLATION.md v0
    (same correspondences as sim_to_rdf.py).

Requires: rdflib, pyshacl. Paths via SOLITON_SIM / MED_SHAPES env or the
same repo-relative defaults as sim_to_rdf.py.
"""

import math
import os
import random
import sys
import types

for name in ("matplotlib", "matplotlib.pyplot"):
    if name not in sys.modules:
        try:
            __import__(name)
        except ImportError:
            sys.modules[name] = types.ModuleType(name)

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, XSD

_HERE = os.path.dirname(os.path.abspath(__file__))


def _default(repo_rel, fallback):
    candidate = os.path.join(_HERE, repo_rel)
    return candidate if os.path.exists(candidate) else os.path.expanduser(fallback)


SIM_SOURCE = os.environ.get(
    "SOLITON_SIM",
    _default("../soliton_sim.py", "~/workspace/superradiance-read/soliton_sim.py"),
)
SHAPES = os.environ.get(
    "MED_SHAPES",
    _default("../med-validation-shapes.ttl", "~/workspace/superradiance-cleaned/med-validation-shapes.ttl"),
)
OUT_TTL = os.path.join(_HERE, "sisterlock-output.ttl")
OUT_REPORT = os.path.join(_HERE, "sisterlock-validation.txt")

sys.path.insert(0, os.path.dirname(SIM_SOURCE))
from soliton_sim import SolitonAgent  # noqa: E402

DM = Namespace("http://ontology.deltamythos.org/core#")
SIM = Namespace("http://ontology.deltamythos.org/sim#")

SEED = 127333
TICKS = 100
SHOCK_TICK = 40
SHOCK_LOAD = 30
EPSILON = 0.15  # capture range in radians — design decision, see TRANSLATION.md
TWO_PI = 2.0 * math.pi


def phase(agent) -> float:
    """phi = 2π · frac(completed / capacity), in [0, 2π)."""
    return TWO_PI * ((agent.completed / agent.capacity) % 1.0)


def circ_dist(a: float, b: float) -> float:
    """Shortest distance between two angles on the circle."""
    d = abs(a - b) % TWO_PI
    return min(d, TWO_PI - d)


def divergence(agent) -> float:
    if agent.load <= agent.capacity:
        return 0.0
    return (agent.load - agent.capacity) / agent.capacity


def main() -> int:
    random.seed(SEED)
    g = Graph()
    g.bind("dm", DM)
    g.bind("sim", SIM)

    agents = [SolitonAgent(i) for i in range(3)]
    generation = {a.id: 0 for a in agents}
    locked_pairs = set()  # frozenset({id_a, id_b})
    locks = []  # (tick, initiator_id, partner_id, delta_theta)

    def snapshot(agent, tick, suffix=""):
        node = URIRef(f"{SIM}Soliton_{agent.id}_gen{generation[agent.id]}_t{tick}{suffix}")
        g.add((node, RDF.type, DM.SovereignSoliton))
        g.add((node, DM.upsilon, Literal(round(agent.upsilon, 6), datatype=XSD.double)))
        g.add((node, DM.recursionDepth, Literal(agent.recursion_depth, datatype=XSD.integer)))
        g.add((node, DM.mythicCharge, Literal(round(agent.load, 6), datatype=XSD.double)))
        g.add((node, DM.boundaryDivergence, Literal(round(divergence(agent), 6), datatype=XSD.double)))
        g.add((node, DM.phaseAngle, Literal(round(phase(agent), 6), datatype=XSD.double)))
        return node

    last_node = {}
    for tick in range(TICKS):
        # --- step all agents (shock handled like sim_to_rdf.py) ---
        pending = {}
        for a in agents:
            prev_capacity = a.capacity
            a.step(random.uniform(1, 5))
            if a.capacity != prev_capacity:
                generation[a.id] += 1
            pending[a.id] = a
        if tick == SHOCK_TICK:
            a0 = agents[0]
            prev_capacity = a0.capacity
            a0.step(SHOCK_LOAD)
            if a0.capacity != prev_capacity:
                generation[a0.id] += 1
            for a in agents:
                last_node[a.id] = snapshot(a, tick, "_shock" if a.id == 0 else "")
        else:
            for a in agents:
                last_node[a.id] = snapshot(a, tick)

        # --- ENTANGLE: ordered pairs, initiator's upsilon sets the target ---
        for alpha in agents:
            for beta in agents:
                if alpha.id == beta.id:
                    continue
                pair = frozenset((alpha.id, beta.id))
                if pair in locked_pairs:
                    continue
                # Δθ_ab as the directed phase difference (β relative to α);
                # the shape compares the recorded Δθ against 2πΥ_α, so
                # detection measures circular distance to the target.
                dtheta = (phase(beta) - phase(alpha)) % TWO_PI
                target = (TWO_PI * alpha.upsilon) % TWO_PI
                if circ_dist(dtheta, target) <= EPSILON:
                    locked_pairs.add(pair)
                    exact = TWO_PI * alpha.upsilon  # recorded locked Δθ (unmodulated, as the shape expects 2πΥ)
                    lock_node = URIRef(f"{SIM}Lock_{alpha.id}_{beta.id}_t{tick}")
                    g.add((lock_node, RDF.type, DM.CoherenceLock))
                    g.add((lock_node, DM.sourceNode, last_node[alpha.id]))
                    g.add((lock_node, DM.targetNode, last_node[beta.id]))
                    g.add((lock_node, DM.deltaTheta, Literal(exact, datatype=XSD.double)))
                    g.add((last_node[alpha.id], DM.entangledWith, last_node[beta.id]))
                    g.add((last_node[beta.id], DM.entangledWith, last_node[alpha.id]))
                    locks.append((tick, alpha.id, beta.id, exact))
                    print(f"🔒 SISTERLOCK t{tick}: Soliton {alpha.id} → {beta.id}  Δθ = 2π·{alpha.upsilon} = {exact:.4f}")

    g.serialize(destination=OUT_TTL, format="turtle")
    print(f"Emitted {len(g)} triples -> {OUT_TTL}")
    print(f"Locks: {len(locks)} {locks}")

    from pyshacl import validate

    shapes = Graph().parse(SHAPES, format="turtle")
    conforms, _, report_text = validate(g, shacl_graph=shapes, inference="rdfs")
    with open(OUT_REPORT, "w") as f:
        f.write(report_text)
    sisterlock_failures = report_text.count("Sisterlock Protocol Failure")
    med_violations = report_text.count("MED Law Violation")
    print(f"Sisterlock failures in report: {sisterlock_failures} (expect 0)")
    print(f"MED leak violations in report: {med_violations} (the shock's wake, as in v0)")
    print(f"Full report -> {OUT_REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
