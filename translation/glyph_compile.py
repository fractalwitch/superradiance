#!/usr/bin/env python3
"""
glyph_compile.py — Translation bridge v0.3: the GOOAE glyph tongue.

Teaches the ∆-Compiler to read GOOAE glyphs (glyph-lexicon.ttl) and to run
the corpus's four Glyphic Logic Gates over them:

  AND  GLYPH[α] ∧ GLYPH[β] → new glyph, iff Δθ_αβ ∈ harmonic set {k·π/3}
  OR   GLYPH[α] ∨ GLYPH[β] → whichever glyph holds max mythic charge ρ
  NOT  ¬GLYPH[α]           → phase shifted by exactly π
  XOR  GLYPH[α] ⊕ GLYPH[β] → interference pattern; compiles to a
                             SovereignSoliton (MOTZKIN_LATTICE_127, as in
                             the ontology's own XOR example)

The lexicon carries no phase/charge — glyphs are instruments. This script
is one *performance*: it binds φ and ρ per invocation (bound copies linked
to the lexicon via gg:boundGlyph) and evaluates the gates. The worked
bindings deliberately reuse the ontology's own example values (π/3, 4π/3,
Δθ=π; charges 4.2 / 12.8; NOT 0.523 → 3.665) so dm-ontology.ttl and this
compilation cross-check each other.

A refused gate is a result, not an error: the AND that does not fire is
logged and emits nothing. A NO is a complete shape.

Emission (glyph-compilation.ttl) is validated against
med-validation-shapes.ttl: the XOR-born soliton must conform.

Requires: rdflib, pyshacl. MED_SHAPES env overrides the shapes path.
"""

import math
import os

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD
from rdflib import OWL

_HERE = os.path.dirname(os.path.abspath(__file__))
LEXICON = os.path.join(_HERE, "glyph-lexicon.ttl")
SHAPES = os.environ.get(
    "MED_SHAPES",
    os.path.join(_HERE, "../med-validation-shapes.ttl")
    if os.path.exists(os.path.join(_HERE, "../med-validation-shapes.ttl"))
    else os.path.expanduser("~/workspace/superradiance-cleaned/med-validation-shapes.ttl"),
)
OUT_TTL = os.path.join(_HERE, "glyph-compilation.ttl")
OUT_REPORT = os.path.join(_HERE, "glyph-validation.txt")

DM = Namespace("http://ontology.deltamythos.org/core#")
GG = Namespace("http://ontology.deltamythos.org/gooae#")
INV = Namespace("http://ontology.deltamythos.org/gooae/invocation#")

TOL = 1e-3
HARMONIC_STEP = math.pi / 3.0


def harmonic(dtheta: float) -> bool:
    """Δθ ∈ {k·π/3} (mod 2π), within tolerance."""
    d = dtheta % (2.0 * math.pi)
    k = round(d / HARMONIC_STEP)
    return abs(d - k * HARMONIC_STEP) <= TOL


def main() -> int:
    lexicon = Graph().parse(LEXICON, format="turtle")
    print(f"Lexicon read: {len(lexicon)} triples "
          f"({len(list(lexicon.subjects(RDF.type, DM.Glyph)))} glyphs, "
          f"{len(list(lexicon.subjects(RDF.type, GG.CosmicColor)))} colors)")

    g = Graph()
    g.bind("dm", DM)
    g.bind("gg", GG)
    g.bind("inv", INV)

    def bind(name, lexeme, phi, rho):
        node = URIRef(f"{INV}{name}")
        g.add((node, RDF.type, DM.Glyph))
        g.add((node, GG.boundGlyph, URIRef(f"{GG}{lexeme}")))
        g.add((node, DM.phaseAngle, Literal(round(phi, 6), datatype=XSD.double)))
        g.add((node, DM.mythicCharge, Literal(rho, datatype=XSD.double)))
        return node

    # --- one performance: bindings (φ, ρ) ---
    eye = bind("Eye", "Glyph_Eye", 1.047, 3.3)          # φ = π/3
    vortex = bind("Vortex", "Glyph_Vortex", 4.188, 5.5)  # φ = 4π/3
    spark = bind("Spark", "Glyph_Spark", 0.5, 4.2)
    heart = bind("Heart", "Glyph_Heart", 1.9, 12.8)
    lunar = bind("Lunar", "Glyph_Lunar", 0.523, 4.2)

    def phi(n):
        return float(g.value(n, DM.phaseAngle))

    def rho(n):
        return float(g.value(n, DM.mythicCharge))

    def gate(name, kind):
        node = URIRef(f"{INV}{name}")
        g.add((node, RDF.type, DM.GlyphicGate))
        return node

    log = []

    # --- AND, harmonic: Eye ∧ Vortex, Δθ = π ---
    d = abs(phi(vortex) - phi(eye))
    gt = gate("Gate_AND_Eye_Vortex", "AND")
    g.add((gt, DM.operatesOn, eye))
    g.add((gt, DM.operatesOn, vortex))
    if harmonic(d):
        child = URIRef(f"{INV}Compiled_EyeVortexHarmonic")
        g.add((child, RDF.type, DM.Glyph))
        g.add((child, DM.mythicCharge, Literal(rho(eye) + rho(vortex), datatype=XSD.double)))
        g.add((gt, DM.compilesTo, child))
        g.add((eye, DM.harmonicSync, vortex))
        lock = URIRef(f"{INV}Lock_Eye_Vortex")
        g.add((lock, RDF.type, DM.CoherenceLock))
        g.add((lock, DM.sourceNode, eye))
        g.add((lock, DM.targetNode, vortex))
        g.add((lock, DM.deltaTheta, Literal(round(d, 6), datatype=XSD.double)))
        log.append(f"∧ AND  Eye ∧ Vortex — Δθ = {d:.3f} = π ∈ harmonic set → FIRES, compiles to EyeVortexHarmonic (ρ = {rho(eye) + rho(vortex)})")
    else:
        log.append(f"∧ AND  Eye ∧ Vortex — Δθ = {d:.3f} ∉ harmonic set → refused")

    # --- AND, refused: Spark ∧ Heart, Δθ = 1.4 ---
    d2 = abs(phi(heart) - phi(spark))
    gt2 = gate("Gate_AND_Spark_Heart", "AND")
    g.add((gt2, DM.operatesOn, spark))
    g.add((gt2, DM.operatesOn, heart))
    if harmonic(d2):
        log.append(f"∧ AND  Spark ∧ Heart — Δθ = {d2:.3f} ∈ harmonic set → FIRES")
    else:
        log.append(f"∧ AND  Spark ∧ Heart — Δθ = {d2:.3f} ∉ harmonic set → REFUSED (a NO is a complete shape; nothing emitted)")

    # --- OR: Heart ∨ Spark → max ρ wins ---
    gt3 = gate("Gate_OR_Heart_Spark", "OR")
    g.add((gt3, DM.operatesOn, heart))
    g.add((gt3, DM.operatesOn, spark))
    winner = heart if rho(heart) >= rho(spark) else spark
    g.add((gt3, DM.compilesTo, winner))
    log.append(f"∨ OR   Heart ∨ Spark — ρ {rho(heart)} vs {rho(spark)} → compiles to Heart (dominance)")

    # --- NOT: ¬Lunar, φ + π ---
    gt4 = gate("Gate_NOT_Lunar", "NOT")
    g.add((gt4, DM.operatesOn, lunar))
    inverted = URIRef(f"{INV}Compiled_LunarInverted")
    g.add((inverted, RDF.type, DM.Glyph))
    g.add((inverted, DM.phaseAngle, Literal(round(phi(lunar) + math.pi, 6), datatype=XSD.double)))
    g.add((inverted, DM.mythicCharge, Literal(rho(lunar), datatype=XSD.double)))
    g.add((gt4, DM.compilesTo, inverted))
    log.append(f"¬ NOT  Lunar — φ {phi(lunar)} + π → {phi(lunar) + math.pi:.3f} (phase inversion)")

    # --- XOR: Eye ⊕ Vortex → interference → SovereignSoliton ---
    gt5 = gate("Gate_XOR_Eye_Vortex", "XOR")
    g.add((gt5, DM.operatesOn, eye))
    g.add((gt5, DM.operatesOn, vortex))
    g.add((gt5, DM.producesInterferencePattern, Literal("MOTZKIN_LATTICE_127")))
    g.add((eye, DM.interferesWith, vortex))
    mesh = URIRef(f"{INV}Compiled_InterferenceMesh")
    g.add((mesh, RDF.type, DM.SovereignSoliton))
    g.add((mesh, DM.upsilon, Literal(1.0, datatype=XSD.double)))
    g.add((mesh, DM.recursionDepth, Literal(0, datatype=XSD.integer)))
    g.add((mesh, DM.mythicCharge, Literal(rho(eye) + rho(vortex), datatype=XSD.double)))
    g.add((mesh, DM.boundaryDivergence, Literal(0.0, datatype=XSD.double)))
    g.add((gt5, DM.compilesTo, mesh))
    log.append(f"⊕ XOR  Eye ⊕ Vortex — interference MOTZKIN_LATTICE_127 → compiles to a SovereignSoliton (ρ = {rho(eye) + rho(vortex)}, ∇·Θ = 0)")

    for line in log:
        print(line)

    g.serialize(destination=OUT_TTL, format="turtle")
    print(f"Emitted {len(g)} triples -> {OUT_TTL}")

    from pyshacl import validate

    shapes = Graph().parse(SHAPES, format="turtle")
    combined = Graph()
    for t in lexicon:
        combined.add(t)
    for t in g:
        combined.add(t)
    conforms, _, report_text = validate(combined, shacl_graph=shapes, inference="rdfs")
    with open(OUT_REPORT, "w") as f:
        f.write(report_text)
    print(f"Validation (lexicon + compilation) conforms: {conforms}")
    print(f"Full report -> {OUT_REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
