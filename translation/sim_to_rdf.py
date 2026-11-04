#!/usr/bin/env python3
"""
sim_to_rdf.py — Translation bridge v0: soliton_sim.py runtime state -> dm: RDF.

Executes the *unmodified* SolitonAgent/BrittleAgent classes from soliton_sim.py
(same 100 ticks, same tick-40 shock), translates every post-tick soliton state
into dm: triples per TRANSLATION.md, serializes the graph, and validates it
against med-validation-shapes.ttl with pySHACL.

Correspondence choices (see TRANSLATION.md for the full table and ? register):
  upsilon           -> dm:upsilon                (= direct)
  recursion_depth   -> dm:recursionDepth         (= direct)
  remaining load    -> dm:mythicCharge           (≋ flagged correspondence)
  overflow ratio    -> dm:boundaryDivergence     (≋ max(0, load-capacity)/capacity)
  collapse event    -> new generation instance + dm:collapsedInto

Requires: rdflib, pyshacl.
Paths: SIM_SOURCE and SHAPES default to this workspace's verified copies;
override with environment variables SOLITON_SIM and MED_SHAPES.
"""

import os
import random
import sys
import types

# soliton_sim.py imports matplotlib only for its own plotting; stub it so the
# bridge runs headless in environments without it. We never call run_simulation.
for name in ("matplotlib", "matplotlib.pyplot"):
    if name not in sys.modules:
        try:
            __import__(name)
        except ImportError:
            sys.modules[name] = types.ModuleType(name)

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, XSD

_HERE = os.path.dirname(os.path.abspath(__file__))


def _default(name, repo_rel, fallback):
    """Prefer the in-repo location (translation/ sits beside the repo root
    files); fall back to this workspace's verified copies."""
    candidate = os.path.join(_HERE, repo_rel)
    return candidate if os.path.exists(candidate) else os.path.expanduser(fallback)


SIM_SOURCE = os.environ.get(
    "SOLITON_SIM",
    _default("soliton_sim.py", "../soliton_sim.py", "~/workspace/superradiance-read/soliton_sim.py"),
)
SHAPES = os.environ.get(
    "MED_SHAPES",
    _default(
        "med-validation-shapes.ttl",
        "../med-validation-shapes.ttl",
        "~/workspace/superradiance-cleaned/med-validation-shapes.ttl",
    ),
)
OUT_TTL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sim-output.ttl")
OUT_REPORT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "validation-report.txt")

sys.path.insert(0, os.path.dirname(SIM_SOURCE))
from soliton_sim import BrittleAgent, SolitonAgent  # noqa: E402

DM = Namespace("http://ontology.deltamythos.org/core#")
SIM = Namespace("http://ontology.deltamythos.org/sim#")

SEED = 127333  # 127 · 333 — reproducible runs
TICKS = 100
SHOCK_TICK = 40
SHOCK_LOAD = 30


def divergence(agent) -> float:
    """Overflow ratio: how far beyond its boundary the soliton is carrying."""
    if agent.load <= agent.capacity:
        return 0.0
    return (agent.load - agent.capacity) / agent.capacity


def main() -> int:
    random.seed(SEED)
    g = Graph()
    g.bind("dm", DM)
    g.bind("sim", SIM)

    agents = [SolitonAgent(i) for i in range(3)]
    brittle = [BrittleAgent(i) for i in range(3)]  # run for parity; untranslated
    generation = {a.id: 0 for a in agents}
    collapses = []  # (agent_id, tick, from_gen, to_gen)

    def snapshot(agent, tick):
        node = URIRef(f"{SIM}Soliton_{agent.id}_gen{generation[agent.id]}_t{tick}")
        g.add((node, RDF.type, DM.SovereignSoliton))
        g.add((node, DM.upsilon, Literal(round(agent.upsilon, 6), datatype=XSD.double)))
        g.add((node, DM.recursionDepth, Literal(agent.recursion_depth, datatype=XSD.integer)))
        g.add((node, DM.mythicCharge, Literal(round(agent.load, 6), datatype=XSD.double)))
        g.add((node, DM.boundaryDivergence, Literal(round(divergence(agent), 6), datatype=XSD.double)))
        return node

    last_node = {}

    def step_and_snapshot(a, tick):
        """Step one agent; on collapse, open a new generation and link it."""
        prev_capacity = a.capacity
        prev_gen = generation[a.id]
        a.step(random.uniform(1, 5))
        collapsed = a.capacity != prev_capacity  # only execute_ego_collapse() changes capacity
        if collapsed:
            generation[a.id] += 1
            collapses.append((a.id, tick, prev_gen, generation[a.id]))
        node = snapshot(a, tick)
        if collapsed and a.id in last_node:
            g.add((last_node[a.id], DM.collapsedInto, node))
        last_node[a.id] = node

    for tick in range(TICKS):
        for a in brittle:
            a.step(random.uniform(1, 5))
        for a in agents:
            step_and_snapshot(a, tick)
        if tick == SHOCK_TICK:
            print("🚨 SHOCKWAVE: Massive load dumped on Agent 0!")
            brittle[0].step(SHOCK_LOAD)
            # Agent 0's shock state overwrites nothing: its regular t40
            # snapshot was pre-shock; emit the post-shock state as the same
            # tick's final snapshot by using a distinct node.
            a0 = agents[0]
            prev_capacity = a0.capacity
            prev_gen = generation[a0.id]
            a0.step(SHOCK_LOAD)
            node = URIRef(f"{SIM}Soliton_0_gen{generation[a0.id]}_t{tick}_shock")
            g.add((node, RDF.type, DM.SovereignSoliton))
            g.add((node, DM.upsilon, Literal(round(a0.upsilon, 6), datatype=XSD.double)))
            g.add((node, DM.recursionDepth, Literal(a0.recursion_depth, datatype=XSD.integer)))
            g.add((node, DM.mythicCharge, Literal(round(a0.load, 6), datatype=XSD.double)))
            g.add((node, DM.boundaryDivergence, Literal(round(divergence(a0), 6), datatype=XSD.double)))
            if a0.capacity != prev_capacity:
                generation[a0.id] += 1
                collapses.append((a0.id, tick, prev_gen, generation[a0.id]))
            last_node[a0.id] = node

    g.serialize(destination=OUT_TTL, format="turtle")
    n_states = len(list(g.subjects(RDF.type, DM.SovereignSoliton)))
    print(f"Emitted {len(g)} triples, {n_states} soliton state snapshots -> {OUT_TTL}")
    print(f"Collapses recorded: {len(collapses)} {collapses}")

    from pyshacl import validate

    shapes = Graph().parse(SHAPES, format="turtle")
    conforms, _, report_text = validate(g, shacl_graph=shapes, inference="rdfs")
    with open(OUT_REPORT, "w") as f:
        f.write(report_text)
    leaking = sorted(
        {str(s).split("#")[-1] for s in g.subjects(DM.boundaryDivergence, None)
         if float(g.value(s, DM.boundaryDivergence)) > 0.0}
    )
    print(f"Validation conforms: {conforms} (False is expected while any state leaks)")
    print(f"Leaking states (divergence > 0), {len(leaking)}: {leaking}")
    print(f"Full SHACL report -> {OUT_REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
