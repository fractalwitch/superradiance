#!/usr/bin/env python3
"""Validation runner for the superradiance SHACL shapes.

Validates every test dataset against the shapes in ../med-validation-shapes.ttl
and attributes each violation to the shape that raised it, so the two shapes
added 2026-11-08 (dm:EgoCollapseValidityShape, dm:AntiCapturePropagationShape)
can be checked individually, and the pre-existing cleanup checks
(dm:SovereignSolitonShape, dm:SisterlockProtocolShape) can be regression-checked.

Usage:  python tests/run_validation.py [path-to-shapes.ttl]
Writes: tests/validation-report.txt and prints the same report.
"""
import sys
from pathlib import Path

from rdflib import Graph, Namespace
from pyshacl import validate

ROOT = Path(__file__).resolve().parent.parent
SH = Namespace("http://www.w3.org/ns/shacl#")
DM = "http://ontology.deltamythos.org/core#"


def violations(data_path, shapes_graph):
    data = Graph().parse(str(data_path), format="turtle")
    conforms, report, _ = validate(data, shacl_graph=shapes_graph,
                                   inference="rdfs", advanced=True)
    out = []
    for result in report.subjects(None, SH.ValidationResult):
        focus = report.value(result, SH.focusNode)
        source = report.value(result, SH.sourceShape)
        message = report.value(result, SH.resultMessage)
        out.append((str(focus).replace(DM, "dm:"),
                    str(source).replace(DM, "dm:") if source else "?",
                    str(message)))
    return conforms, sorted(out)


def main():
    shapes_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "med-validation-shapes.ttl"
    shapes = Graph().parse(str(shapes_path), format="turtle")
    ontology = Graph().parse(str(ROOT / "dm-ontology.ttl"), format="turtle")

    lines = []
    lines.append(f"Shapes file: {shapes_path.name} — {len(shapes)} triples")
    lines.append(f"Ontology file: dm-ontology.ttl — {len(ontology)} triples")
    lines.append("")

    datasets = [
        ("tests/test-instances.ttl (cleanup regression)", ROOT / "tests/test-instances.ttl"),
        ("tests/test-sisterlock.ttl (cleanup regression)", ROOT / "tests/test-sisterlock.ttl"),
        ("tests/test-ego-collapse.ttl (new shape)", ROOT / "tests/test-ego-collapse.ttl"),
        ("tests/test-anti-capture.ttl (new shape)", ROOT / "tests/test-anti-capture.ttl"),
        ("dm-ontology.ttl as data (worked examples)", ROOT / "dm-ontology.ttl"),
    ]
    for label, path in datasets:
        conforms, viols = violations(path, shapes)
        lines.append(f"== {label}: conforms={conforms}, {len(viols)} violation(s)")
        for focus, source, message in viols:
            lines.append(f"   [{source}] focus={focus}")
            lines.append(f"       {message}")
        lines.append("")

    report = "\n".join(lines)
    (ROOT / "tests/validation-report.txt").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
