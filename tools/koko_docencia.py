from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from collections import defaultdict, deque
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "ccms" / "paca_docencia_superlattice_v1.json"
DEFAULT_DB = ROOT / "build" / "paca_docencia.sqlite"
NOTEBOOK = ROOT / "tutorials" / "practica-2026-ising-duality" / "ising_duality_codebook.ipynb"
CORE_DIR = ROOT / "tutorials" / "practica-2026-ising-duality"
SCHEDULE = ROOT / "ccms" / "paca_agenda_calendar_qml_2026_2027.json"
CONNECTOR_NET = ROOT / "ccms" / "konnektia_qquapp_moog_quazris_course_connectors_v1.json"
NAVIGATION = ROOT / "ccms" / "sigil_course_navigation_v1.json"


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def load_schedule() -> dict[str, Any]:
    return json.loads(SCHEDULE.read_text(encoding="utf-8"))


def load_connector_network() -> dict[str, Any]:
    return json.loads(CONNECTOR_NET.read_text(encoding="utf-8"))


def load_navigation_module():
    sys.path.insert(0, str(ROOT / "tools"))
    import sigil_toc
    return sigil_toc


def event_datetime(event: dict[str, Any], timezone: str, field: str) -> datetime:
    return datetime.fromisoformat(
        f"{event['date']}T{event[field]}:00"
    ).replace(tzinfo=ZoneInfo(timezone))


def validate_schedule(data: dict[str, Any]) -> None:
    events = data["events"]
    ids = [event["id"] for event in events]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate schedule event id")
    tz = data["timezone"]
    previous: datetime | None = None
    for event in events:
        start = event_datetime(event, tz, "start")
        end = event_datetime(event, tz, "end")
        if end <= start:
            raise ValueError(f"invalid event duration: {event['id']}")
        if previous is not None and start < previous:
            raise ValueError(f"schedule not in chronological order: {event['id']}")
        previous = start
    if data["authority"].get("external_write_performed") is not False:
        raise ValueError("schedule source must not self-certify external writes")


def validate_connector_network(data: dict[str, Any]) -> None:
    layer_ids = [layer["id"] for layer in data["layers"]]
    if len(layer_ids) != len(set(layer_ids)):
        raise ValueError("duplicate connector layer")
    known = set(layer_ids) | {"PACA_AGENDA", "PACA_CALENDAR", "WML", "CCMS"}
    for name, localizer in data["localizers"].items():
        source = ROOT / localizer["source"]
        if not source.exists():
            raise ValueError(f"connector localizer {name} missing source: {source}")
        unknown = set(localizer["route"]) - known
        if unknown:
            raise ValueError(f"connector localizer {name} has unknown route stages: {sorted(unknown)}")
    schedule = load_schedule()
    if data["schedule_binding"]["event_count"] != len(schedule["events"]):
        raise ValueError("connector schedule event-count drift")
    if data["authority"].get("connector_effects_executed") is not False:
        raise ValueError("connector source must remain effect-free")


def validate_toc() -> None:
    sigil_toc = load_navigation_module()
    data = sigil_toc.load_navigation()
    errors = sigil_toc.validate_navigation(data)
    if errors:
        raise ValueError("TOC/navigation errors: " + "; ".join(errors))


def filter_events(
    schedule: dict[str, Any],
    *,
    teacher: str | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
) -> list[dict[str, Any]]:
    events = list(schedule["events"])
    if teacher:
        needle = teacher.casefold()
        events = [
            event for event in events
            if needle in (event.get("teacher") or "").casefold()
        ]
    if from_date:
        events = [event for event in events if event["date"] >= from_date]
    if to_date:
        events = [event for event in events if event["date"] <= to_date]
    return events


def event_line(event: dict[str, Any]) -> str:
    teacher = event.get("teacher") or "TBD"
    kind = event.get("type") or "TBD"
    return (
        f"{event['date']} {event['start']}-{event['end']}  "
        f"{teacher}  |  {kind}"
    )


def ics_escape(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def schedule_to_ics(schedule: dict[str, Any]) -> str:
    tz = schedule["timezone"]
    rows = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//PACA DOCENCIA//UIMP QML//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
    ]
    for event in schedule["events"]:
        teacher = event.get("teacher") or "TBD"
        kind = event.get("type") or "TBD"
        summary = f"{schedule['course']} — {kind} — {teacher}"
        rows.extend(
            [
                "BEGIN:VEVENT",
                f"UID:{event['id']}@uimpintrotoquantumai",
                f"DTSTART;TZID={tz}:{event['date'].replace('-', '')}T{event['start'].replace(':', '')}00",
                f"DTEND;TZID={tz}:{event['date'].replace('-', '')}T{event['end'].replace(':', '')}00",
                f"SUMMARY:{ics_escape(summary)}",
                f"DESCRIPTION:{ics_escape('PACA Agenda public course projection')}",
                "END:VEVENT",
            ]
        )
    rows.append("END:VCALENDAR")
    return "\r\n".join(rows) + "\r\n"


def validate_dag(data: dict[str, Any]) -> list[str]:
    dag = data["devops"]["dag"]
    nodes = list(dag["nodes"])
    graph: dict[str, list[str]] = defaultdict(list)
    indegree = {node: 0 for node in nodes}
    for src, dst in dag["edges"]:
        if src not in indegree or dst not in indegree:
            raise ValueError(f"DAG edge references unknown node: {src}->{dst}")
        graph[src].append(dst)
        indegree[dst] += 1
    queue = deque([node for node in nodes if indegree[node] == 0])
    order: list[str] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for dst in graph[node]:
            indegree[dst] -= 1
            if indegree[dst] == 0:
                queue.append(dst)
    if len(order) != len(nodes):
        raise ValueError("DevOps execution graph is cyclic; a DAG must remain acyclic")
    return order


def validate_manifest(data: dict[str, Any]) -> None:
    required = [
        "id", "runtime", "syllabus", "practice_2026", "repositories",
        "polykategory", "devops", "cli_ports"
    ]
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"manifest missing keys: {missing}")
    required_ports = {"CLICK", "CLIT", "ZELDA", "POLES"}
    missing_ports = required_ports - set(data["cli_ports"])
    if missing_ports:
        raise ValueError(f"CLI port set missing core ports: {sorted(missing_ports)}")
    validate_dag(data)

    objects = set(data["polykategory"]["objects"])
    for arrow in data["polykategory"]["polyarrows"]:
        unknown = (set(arrow["inputs"]) | set(arrow["outputs"])) - objects
        if unknown:
            raise ValueError(
                f"polyarrows {arrow['id']} references unknown objects: {sorted(unknown)}"
            )


def science_smoke() -> None:
    sys.path.insert(0, str(CORE_DIR))
    import numpy as np
    import ising_duality_core as core

    tc = core.onsager_critical_temperature()
    kc = 1.0 / tc
    kd = core.kramers_wannier_dual_coupling(kc)
    if not np.isclose(kc, kd, atol=1e-12):
        raise AssertionError("Onsager/Kramers-Wannier self-dual critical point failed")

    if len(core.genus2_zero_two_sectors()) != 16:
        raise AssertionError("genus-2 Z2 homology should expose 16 sectors")

    H = core.tfim_hamiltonian(4)
    if not np.allclose(H, H.conj().T):
        raise AssertionError("TFIM Hamiltonian is not Hermitian")

    X = np.asarray(
        [
            core.contextual_features(
                temperature=t,
                energy_per_spin=e,
                magnetization=m,
                dual_coupling=core.kramers_wannier_dual_coupling(1.0 / t),
            )
            for t, e, m in [
                (1.5, -1.8, 0.9),
                (2.3, -1.4, 0.5),
                (3.0, -0.8, 0.1),
            ]
        ]
    )
    core.assert_psd(core.contextual_kernel(X))


def notebook_smoke() -> None:
    data = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    if data.get("nbformat") != 4:
        raise AssertionError("codebook must use nbformat 4")
    cells = data.get("cells", [])
    if len(cells) < 8:
        raise AssertionError("codebook has too few cells to cover the practice")
    text = "\n".join("".join(cell.get("source", [])) for cell in cells)
    for token in [
        "Onsager", "Kramers", "Hopfield", "Montonen", "H_1",
        "contextual kernel", "Metropolis"
    ]:
        if token not in text:
            raise AssertionError(f"codebook missing concept: {token}")


def materialize_db(data: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    db = sqlite3.connect(path)
    try:
        db.executescript(
            """
            PRAGMA foreign_keys = ON;
            CREATE TABLE metadata(key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE repositories(
                id TEXT PRIMARY KEY,
                repo TEXT NOT NULL,
                role TEXT NOT NULL,
                status TEXT NOT NULL,
                payload TEXT NOT NULL
            );
            CREATE TABLE syllabus_blocks(
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                teachers TEXT NOT NULL,
                payload TEXT NOT NULL
            );
            CREATE TABLE polyobjects(id TEXT PRIMARY KEY);
            CREATE TABLE polyarrows(
                id TEXT PRIMARY KEY,
                inputs TEXT NOT NULL,
                outputs TEXT NOT NULL
            );
            CREATE TABLE dag_edges(src TEXT NOT NULL, dst TEXT NOT NULL);
            CREATE TABLE cocyclic_tau(src TEXT PRIMARY KEY, dst TEXT NOT NULL);
            CREATE TABLE cli_ports(name TEXT PRIMARY KEY, purpose TEXT NOT NULL);
            """
        )
        db.execute("INSERT INTO metadata VALUES (?, ?)", ("manifest_id", data["id"]))
        db.execute("INSERT INTO metadata VALUES (?, ?)", ("version", data["version"]))
        for repo in data["repositories"]:
            db.execute(
                "INSERT INTO repositories VALUES (?, ?, ?, ?, ?)",
                (
                    repo["id"], repo["repo"], repo["role"], repo["status"],
                    json.dumps(repo),
                ),
            )
        for block in data["syllabus"]["blocks"]:
            db.execute(
                "INSERT INTO syllabus_blocks VALUES (?, ?, ?, ?)",
                (
                    block["id"], block["title"],
                    json.dumps(block["teachers"]), json.dumps(block),
                ),
            )
        for obj in data["polykategory"]["objects"]:
            db.execute("INSERT INTO polyobjects VALUES (?)", (obj,))
        for arrow in data["polykategory"]["polyarrows"]:
            db.execute(
                "INSERT INTO polyarrows VALUES (?, ?, ?)",
                (
                    arrow["id"], json.dumps(arrow["inputs"]),
                    json.dumps(arrow["outputs"]),
                ),
            )
        db.executemany("INSERT INTO dag_edges VALUES (?, ?)", data["devops"]["dag"]["edges"])
        db.executemany(
            "INSERT INTO cocyclic_tau VALUES (?, ?)",
            data["devops"]["cocyclic_overlay"]["tau"].items(),
        )
        db.executemany(
            "INSERT INTO cli_ports VALUES (?, ?)",
            data["cli_ports"].items(),
        )
        db.commit()
    finally:
        db.close()


def print_port(data: dict[str, Any], name: str) -> None:
    name = name.upper()
    print(f"{name}: {data['cli_ports'][name]}")
    if name == "CLICK":
        print(NOTEBOOK.relative_to(ROOT))
        for repo in data["repositories"]:
            if repo["status"] == "active":
                print(repo["repo"])
    elif name == "CLIT":
        for arrow in data["polykategory"]["polyarrows"]:
            print(f"{arrow['id']}: {arrow['inputs']} -> {arrow['outputs']}")
    elif name == "ZELDA":
        for i, target in enumerate(data["practice_2026"]["learning_targets"], 1):
            print(f"{i}. {target}")
    elif name == "POLES":
        print("Kramers-Wannier: K <-> K*")
        print("Montonen-Olive/S: electric <-> magnetic; tau -> -1/tau")
        print("Genus-2 homology basis: a1, b1, a2, b2")
        print("Important: duality maps are not generic Monte Carlo acceptance rules.")
    elif name == "KIT":
        print("Scientific core: tutorials/practica-2026-ising-duality/ising_duality_core.py")
        print("Semantic teaching core: tutorials/practica-2026-ising-duality/toy_polykategory.py")
        print("Runtime boundary: user-space Python; no Linux-kernel patch required.")
    elif name == "QIT":
        print("QUNO preserves plural alternatives without identity collapse.")
        for obj in data["polykategory"]["objects"]:
            if any(token in obj for token in ("quno", "localization", "sector", "jauria")):
                print(obj)
    elif name == "GIT":
        for repo in data["repositories"]:
            print(f"{repo['id']}\t{repo['role']}\t{repo['status']}\t{repo['repo']}")
        print("fork/clone/mirror topology != semantic identity or authority")
    elif name == "JAURIA":
        print("JARANIAN_JAURIA_1D_RING -> xi/eta -> coupled Kuramoto sectors")
        print("JARANIAN_JAURIA_2D -> witnessed phase-only Kuramoto projection")
        print("observables: phase order + rainbow order parameters + trajectories")
        print("references: tutorials/practica-2026-ising-duality/SWARMALATOR_REFERENCES.md")
    elif name == "BROWSER":
        print("Landing page: site/index.html")
        print("CCMS source: ccms/paca_docencia_superlattice_v1.json")
        print("The web view is a projection, not a second source of truth.")
    elif name == "BIND":
        print("Implementation: ccms/kuir_quazris_bindings.py")
        print("Operations: BIND / DEBIND / REBIND / REKONTRA_BIND")
        print("Semi-operations require explicit witnesses and preserve source identities.")
        print("QUAZRIS external API is a KUIR projection of the KRONE internal API.")
        print("Learning path: observe -> integrate -> learn -> exact_resynthesize(error explicit)")


def print_cocycle(data: dict[str, Any]) -> None:
    tau = data["devops"]["cocyclic_overlay"]["tau"]
    start = data["devops"]["dag"]["nodes"][0]
    orbit = [start]
    nxt = tau[start]
    while nxt != start:
        if nxt in orbit:
            raise ValueError("cocyclic overlay does not close on the declared start")
        orbit.append(nxt)
        nxt = tau[nxt]
    print(" -> ".join(orbit + [start]))
    print("(semantic/review orbit; execution scheduler remains the acyclic DAG)")


def query_db(path: Path, sql: str) -> None:
    db = sqlite3.connect(path)
    try:
        rows = db.execute(sql).fetchall()
        for row in rows:
            print("\t".join(str(x) for x in row))
    finally:
        db.close()


def cmd_preworkflow(data: dict[str, Any], db_path: Path) -> None:
    validate_manifest(data)
    print("[pass] manifest + DAG")
    validate_toc()
    print("[pass] typed TOC/navigation")
    validate_schedule(load_schedule())
    print("[pass] PACA Agenda/Calendar schedule")
    validate_connector_network(load_connector_network())
    print("[pass] KONNEKTIA/QQUAPP/MOOG/KUIR/QUAZRIS connector network")
    science_smoke()
    print("[pass] scientific core")
    notebook_smoke()
    print("[pass] notebook structure")
    materialize_db(data, db_path)
    print(f"[pass] SQLite projection: {db_path}")
    print("[pass] PACA DOCENCIA PREWORKFLOW")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="PACA DOCENCIA / KOKO local control plane for the QML teaching superlattice"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("validate")
    sub.add_parser("science-smoke")
    sub.add_parser("notebook-smoke")
    sub.add_parser("cocycle")
    sub.add_parser("preworkflow")
    sub.add_parser("toc-check")
    sub.add_parser("toc")
    loc = sub.add_parser("localize")
    loc.add_argument("route_id")

    ag = sub.add_parser("agenda")
    ag.add_argument("--teacher")
    ag.add_argument("--from-date")
    ag.add_argument("--to-date")

    cal = sub.add_parser("calendar")
    cal.add_argument("--ics", type=Path)

    kon = sub.add_parser("konnektia")
    kon.add_argument("localizer", nargs="?", choices=("agenda", "calendar", "browser", "knowledge"))

    c42 = sub.add_parser("click42")
    c42.add_argument(
        "surface",
        nargs="?",
        choices=("toc", "agenda", "calendar", "codebook", "research", "connectors"),
    )

    for port in ("click", "clit", "zelda", "poles", "kit", "qit", "git", "jauria", "browser", "bind"):
        sub.add_parser(port)

    dbp = sub.add_parser("db-build")
    dbp.add_argument("--output", type=Path, default=DEFAULT_DB)

    qp = sub.add_parser("query")
    qp.add_argument("sql")
    qp.add_argument("--db", type=Path, default=DEFAULT_DB)

    args = parser.parse_args()
    data = load_manifest()

    if args.command == "validate":
        validate_manifest(data)
        print("manifest valid")
        print("DAG order:", " -> ".join(validate_dag(data)))
    elif args.command == "science-smoke":
        science_smoke()
        print("science smoke passed")
    elif args.command == "notebook-smoke":
        notebook_smoke()
        print("notebook smoke passed")
    elif args.command == "cocycle":
        print_cocycle(data)
    elif args.command == "toc-check":
        validate_toc()
        print("typed TOC/navigation valid")
    elif args.command == "toc":
        sigil_toc = load_navigation_module()
        sigil_toc.print_atlas(sigil_toc.load_navigation())
    elif args.command == "localize":
        sigil_toc = load_navigation_module()
        print(json.dumps(
            sigil_toc.route(sigil_toc.load_navigation(), args.route_id),
            indent=2,
            sort_keys=True,
        ))
    elif args.command == "agenda":
        schedule = load_schedule()
        validate_schedule(schedule)
        for event in filter_events(
            schedule,
            teacher=args.teacher,
            from_date=args.from_date,
            to_date=args.to_date,
        ):
            print(event_line(event))
    elif args.command == "calendar":
        schedule = load_schedule()
        validate_schedule(schedule)
        payload = schedule_to_ics(schedule)
        if args.ics:
            args.ics.parent.mkdir(parents=True, exist_ok=True)
            args.ics.write_text(payload, encoding="utf-8", newline="")
            print(args.ics)
        else:
            print(payload, end="")
    elif args.command == "konnektia":
        network = load_connector_network()
        validate_connector_network(network)
        if args.localizer:
            print(json.dumps(network["localizers"][args.localizer], indent=2, sort_keys=True))
        else:
            for name, localizer in network["localizers"].items():
                print(f"{name}: {' -> '.join(localizer['route'])} -> {localizer['output']}")
    elif args.command == "click42":
        surface = args.surface
        if surface is None:
            print("toc\tagenda\tcalendar\tcodebook\tresearch\tconnectors")
        elif surface == "toc":
            print("README.md#1-table-of-contents")
        elif surface == "agenda":
            for event in filter_events(load_schedule()):
                print(event_line(event))
        elif surface == "calendar":
            print("python tools/koko_docencia.py calendar --ics build/qml_2026_2027.ics")
        elif surface == "codebook":
            print(NOTEBOOK.relative_to(ROOT))
        elif surface == "research":
            print("docs/teaching/RESEARCH_SYNC_TFG_TFM_PHD_V1.md")
        elif surface == "connectors":
            network = load_connector_network()
            for name, localizer in network["localizers"].items():
                print(f"{name}: {' -> '.join(localizer['route'])}")
    elif args.command in {"click", "clit", "zelda", "poles", "kit", "qit", "git", "jauria", "browser", "bind"}:
        print_port(data, args.command)
    elif args.command == "db-build":
        materialize_db(data, args.output)
        print(args.output)
    elif args.command == "query":
        query_db(args.db, args.sql)
    elif args.command == "preworkflow":
        cmd_preworkflow(data, DEFAULT_DB)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
