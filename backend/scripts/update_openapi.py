import json
from pathlib import Path

from app.main import app


def main() -> None:
    output = Path("docs/openapi/openapi.json")
    output.parent.mkdir(parents=True, exist_ok=True)

    schema = app.openapi()
    output.write_text(
        json.dumps(schema, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Successfully saved OpenAPI spec to {output}")


if __name__ == "__main__":
    main()