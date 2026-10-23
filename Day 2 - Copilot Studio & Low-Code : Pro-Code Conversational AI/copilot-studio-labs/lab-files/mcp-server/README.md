# Northwind Field Service MCP Server

Read-only MCP server for the Copilot Studio labs (Streamable HTTP at `/mcp`).

| Tool | Purpose |
| --- | --- |
| `get_asset(asset_id)` | Asset model, customer, site, warranty end, service plan |
| `check_part_stock(part_no)` | Stock per city + total |
| `find_parts_for_model(model)` | Parts that fit HX-200 / PG-50 / CX-10 |
| `find_technician(city, model)` | Qualified technicians and next free slot |

## Run locally
```bash
pip install -r requirements.txt
export MCP_API_KEY="choose-a-secret"     # PowerShell: $env:MCP_API_KEY="choose-a-secret"
python server.py                         # http://localhost:8000/mcp
```

## Make it reachable by Copilot Studio
- **Dev tunnel:** `devtunnel host -p 8000 --allow-anonymous` → use `https://<tunnel>/mcp`
- **Azure Container Apps:** `az containerapp up --name northwind-mcp --resource-group rg-copilot-labs --location centralindia --source . --ingress external --target-port 8000 --env-vars MCP_API_KEY=<key>`

In Copilot Studio use **API key** authentication, sent as header **`x-api-key`**.

Edit the JSON files in `data/` to change assets, parts or technicians. Restart the server afterwards.
