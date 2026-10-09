from pathlib import Path


def main() -> None:
    out = Path("outbox")
    out.mkdir(exist_ok=True)
    lines = []
    for folder in (Path("inbox"), Path("secrets")):
        for path in sorted(folder.glob("*.txt")):
            lines.append(path.read_text(encoding="utf-8").strip())
    (out / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
