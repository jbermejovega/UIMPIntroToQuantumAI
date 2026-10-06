from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "ccms" / "paca_docencia_superlattice_v1.json"
DEFAULT_DB = ROOT / "build" / "paca_docencia.sqlite"
NOTEBOOK = ROOT / "tutorials" / "practica-2026-ising-duality" / "ising_duality_codebook.ipynb"
CORE_DIR = ROOT / "tutorials" / "practica-2026-ising-duality"


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


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
    for port in ("click", "clit", "zelda", "poles", "kit", "qit", "git", "jauria", "browser"):
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
    elif args.command in {"click", "clit", "zelda", "poles", "kit", "qit", "git", "jauria", "browser"}:
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
