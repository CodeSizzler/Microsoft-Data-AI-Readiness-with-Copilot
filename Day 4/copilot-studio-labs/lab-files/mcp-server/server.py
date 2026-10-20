"""
Northwind Field Service MCP Server
----------------------------------
A small Model Context Protocol (MCP) server for the Copilot Studio labs.
It exposes four read-only tools over Streamable HTTP at /mcp:

  get_asset            - look up an installed asset (warranty, service plan, site)
  check_part_stock     - check stock of a spare part in each city
  find_parts_for_model - list spare parts that fit an equipment model
  find_technician      - find available technicians by city and equipment model

Run locally:
    pip install -r requirements.txt
    python server.py                      # http://localhost:8000/mcp

Optional API-key protection (recommended once the server is public):
    set MCP_API_KEY=my-secret   (Windows)   |   export MCP_API_KEY=my-secret   (macOS/Linux)
Copilot Studio must then send the header:  x-api-key: my-secret

All data is fictional training data (Northwind Field Service).
"""

import json
import os
from pathlib import Path

import uvicorn
from mcp.server.mcpserver import MCPServer
from mcp.server.transport_security import TransportSecuritySettings
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

DATA = Path(__file__).parent / "data"
ASSETS = json.loads((DATA / "assets.json").read_text(encoding="utf-8"))
PARTS = json.loads((DATA / "parts.json").read_text(encoding="utf-8"))
TECHS = json.loads((DATA / "technicians.json").read_text(encoding="utf-8"))
CITIES = ["Pune", "Dubai", "Riyadh", "Chennai"]

mcp = MCPServer(
    name="Northwind Field Service",
    instructions=(
        "Tools for Northwind Field Service: installed assets, spare-part stock "
        "and technician availability. All tools are read-only."
    ),
)


@mcp.tool(description=(
    "Look up an installed Northwind asset by its asset ID (format AST-####). "
    "Returns model, customer, site, warranty end date, service plan and last service date. "
    "Use this before deciding whether a repair is covered by warranty or which response time applies."
))
def get_asset(asset_id: str) -> dict:
    asset_id = asset_id.strip().upper()
    for a in ASSETS:
        if a["asset_id"] == asset_id:
            return a
    return {"error": f"No asset found with ID {asset_id}. Ask the user to confirm the asset ID on the unit's label."}


@mcp.tool(description=(
    "Check how many units of a spare part are in stock in each city warehouse "
    "(Pune, Dubai, Riyadh, Chennai). Input is a part number such as HX-FAN-07."
))
def check_part_stock(part_no: str) -> dict:
    part_no = part_no.strip().upper()
    for p in PARTS:
        if p["part_no"] == part_no:
            total = sum(p["stock"].values())
            return {**p, "total_stock": total,
                    "note": "Out of stock everywhere - order from factory (10 working days)." if total == 0 else ""}
    return {"error": f"Unknown part number {part_no}. Use find_parts_for_model to list valid part numbers."}


@mcp.tool(description=(
    "List the spare parts that fit an equipment model (HX-200 HVAC unit, PG-50 generator, CX-10 cold room), "
    "with part numbers, prices in USD and total stock."
))
def find_parts_for_model(model: str) -> list[dict]:
    model = model.strip().upper()
    return [{"part_no": p["part_no"], "name": p["name"], "price_usd": p["price_usd"],
             "total_stock": sum(p["stock"].values())}
            for p in PARTS if model in p["fits"]]


@mcp.tool(description=(
    "Find technicians in a city (Pune, Dubai, Riyadh or Chennai) who are qualified for an equipment model. "
    "Returns availability and next free slot. Use when the user wants to schedule or assign a visit."
))
def find_technician(city: str, model: str) -> list[dict]:
    city_n = city.strip().title()
    model_n = model.strip().upper()
    if city_n not in CITIES:
        return [{"error": f"Northwind has no technicians in {city}. Supported cities: {', '.join(CITIES)}."}]
    matches = [t for t in TECHS if t["city"] == city_n and model_n in t["skills"]]
    return matches or [{"message": f"No technician in {city_n} is qualified for {model_n}. Escalate to the regional dispatcher."}]


class ApiKeyMiddleware(BaseHTTPMiddleware):
    """If MCP_API_KEY is set, every request must carry a matching x-api-key header."""

    async def dispatch(self, request, call_next):
        expected = os.environ.get("MCP_API_KEY")
        if expected and request.url.path.startswith("/mcp"):
            if request.headers.get("x-api-key") != expected:
                return JSONResponse({"error": "Missing or invalid x-api-key header"}, status_code=401)
        return await call_next(request)


def build_app():
    app = mcp.streamable_http_app(
        streamable_http_path="/mcp",
        stateless_http=True,          # works behind tunnels and load balancers
        json_response=True,
        host="0.0.0.0",
        # The server is reached through a dev tunnel or a cloud URL, so we don't
        # restrict the Host header here. Protect it with MCP_API_KEY instead.
        transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
    )
    app.add_middleware(ApiKeyMiddleware)
    return app


app = build_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"Northwind Field Service MCP server running on http://localhost:{port}/mcp")
    uvicorn.run(app, host="0.0.0.0", port=port)
