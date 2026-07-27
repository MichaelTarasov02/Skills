---
name: Vanta
description: Use when automating compliance workflows, building integrations to push data into Vanta, managing controls and tests, querying compliance status, handling vendor assessments, or connecting AI agents to compliance data via the Vanta API or MCP server.
metadata:
    mintlify-proj: vanta
    version: "1.0"
---

# Vanta API Skill

## Product summary

Vanta is a compliance automation platform with a RESTful API that lets you automate compliance workflows, build integrations that push data into Vanta, manage controls and tests, query compliance status, and connect AI agents to compliance data. The API exposes three distinct surfaces: **Manage Vanta** (automate your own tenant), **Build Integrations** (push data into customer tenants), and **Conduct an Audit** (for audit partners). All requests use OAuth 2.0 bearer tokens and go to `https://api.vanta.com` (or `https://api.vanta-gov.com` for Vanta Gov). The Vanta MCP server at `https://mcp.vanta.com/mcp` lets AI agents query and remediate compliance issues directly. See the [Vanta Developer Hub](https://developer.vanta.com) for full documentation.

## When to use

Reach for this skill when:

- **Automating your own Vanta tenant** — assigning control owners, querying test results, managing vendors, uploading documents, offboarding people, creating custom controls.
- **Building an integration** — pushing user accounts, devices, vulnerabilities, background checks, training records, or custom resources into Vanta on a recurring schedule.
- **Querying compliance status** — listing frameworks, controls, tests, failing resources, vendors, or audit information.
- **Connecting AI agents** — using the Vanta MCP server to let Claude, Cursor, or other AI tools remediate failing tests and manage compliance data.
- **Handling webhooks** — receiving real-time events when questionnaires, vendors, information requests, or controls change.
- **Managing audit workflows** — for audit partners, pulling audit data, managing information requests, and sampling evidence.

## Quick reference

### API endpoints and base URLs

| Use case | Base URL | Endpoint examples |
|----------|----------|-------------------|
| Manage your tenant | `https://api.vanta.com` | `GET /v1/frameworks`, `GET /v1/controls`, `PUT /v1/resources/<type>` |
| Build integrations | `https://api.vanta.com` | `PUT /v1/resources/<type>`, `GET /v1/resources/<type>` |
| Conduct audits | `https://api.vanta.com` | `GET /audits/{auditId}/controls`, `GET /audits/{auditId}/information-requests` |
| Vanta Gov | `https://api.vanta-gov.com` | Same endpoints as above |

### OAuth token exchange

All three APIs use the same token endpoint: `POST https://api.vanta.com/oauth/token`

| App type | Grant type | Scopes example | Token lifetime |
|----------|-----------|-----------------|-----------------|
| Manage Vanta | `client_credentials` | `vanta-api.all:read` or `vanta-api.all:write` | 1 hour |
| Build Integrations (Private) | `client_credentials` | `connectors.self:write-resource` | 1 hour |
| Build Integrations (Public) | `authorization_code` | `connectors.self:write-resource` | 1 hour (+ refresh token) |
| Auditor API | `client_credentials` | `auditor-api.audit:read` | 1 hour |

### Essential commands

**Get an access token (client_credentials flow):**
```bash
curl -X POST https://api.vanta.com/oauth/token \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "vci_...",
    "client_secret": "vcs_...",
    "scope": "vanta-api.all:read",
    "grant_type": "client_credentials"
  }'
```

**List frameworks:**
```bash
curl https://api.vanta.com/v1/frameworks \
  -H "Authorization: Bearer $TOKEN"
```

**List controls for a framework:**
```bash
curl "https://api.vanta.com/v1/controls?frameworkMatchesAny=soc2" \
  -H "Authorization: Bearer $TOKEN"
```

**Sync resources (integration):**
```bash
curl -X PUT https://api.vanta.com/v1/resources/user_account \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"resources": [{"uniqueId": "user1", "displayName": "Alice", ...}]}'
```

**Query failing tests:**
```bash
curl "https://api.vanta.com/v1/tests?statusesMatchesAny=NEEDS_ATTENTION" \
  -H "Authorization: Bearer $TOKEN"
```

### MCP server setup

Connect AI agents to Vanta via Model Context Protocol:

| AI tool | Setup |
|---------|-------|
| Claude Code | `claude mcp add --transport http vanta https://mcp.vanta.com/mcp` then `/mcp` → authorize |
| Cursor | Settings → Tools & MCP → Add custom MCP → paste `{"mcpServers": {"vanta": {"url": "https://mcp.vanta.com/mcp"}}}` |
| Perplexity | Set up remote custom connector with URL `https://mcp.vanta.com/mcp` and OAuth auth |

Regional MCP URLs: US `https://mcp.vanta.com/mcp`, EU `https://mcp.eu.vanta.com/mcp`, AU `https://mcp.aus.vanta.com/mcp`

### Webhook setup

Register an endpoint in **Settings → Webhooks** to receive real-time events. Verify signatures using the Svix library with your endpoint's signing secret (starts with `whsec_`). Respond with `2xx` within 15 seconds, then process asynchronously. Deduplicate on the `svix-id` header.

## Decision guidance

### When to use Manage Vanta vs Build Integrations API

| Task | Use Manage Vanta | Use Build Integrations |
|------|------------------|----------------------|
| Automate your own tenant (controls, vendors, documents) | ✓ | ✗ |
| Push data from external system into Vanta | ✗ | ✓ |
| Query test results and failing resources | ✓ | ✗ |
| Assign control owners | ✓ | ✗ |
| Sync user accounts, devices, vulnerabilities | ✗ | ✓ |
| Build a public marketplace integration | ✗ | ✓ |
| Build a private single-tenant integration | ✗ | ✓ |

### When to use built-in tests vs custom tests

| Scenario | Built-in test | Custom test |
|----------|---------------|------------|
| Syncing supported resource type (UserAccount, Computer, etc.) | ✓ | ✗ |
| Testing custom resource | ✗ | ✓ |
| Stricter rule than Vanta's default | ✗ | ✓ |
| Testing custom properties on built-in resource | ✗ | ✓ |
| Modeling internal servers, on-prem appliances | ✗ | ✓ |

### When to use base resources vs custom resources

| Data | Base resource | Custom resource |
|------|---------------|-----------------|
| User accounts from IdP | ✓ UserAccount | ✗ |
| Devices from MDM | ✓ Computer | ✗ |
| Vulnerabilities from scanner | ✓ Vulnerability | ✗ |
| Internal servers | ✗ | ✓ CustomResource |
| Change-management records | ✗ | ✓ CustomResource |
| Vendor review artifacts | ✗ | ✓ CustomResource |

## Workflow

### Typical task: Query failing compliance tests and remediate

1. **Authenticate** — Exchange `client_id` and `client_secret` for an `access_token` using the `client_credentials` flow. Store the token securely; it expires in 1 hour.

2. **List frameworks** — Call `GET /v1/frameworks` to see which compliance frameworks (SOC 2, ISO 27001, etc.) are active in your tenant.

3. **Query failing tests** — Call `GET /v1/tests?statusesMatchesAny=NEEDS_ATTENTION` to find tests that are not passing. Filter by framework if needed.

4. **Get test details** — Call `GET /v1/tests/{testId}` to see which resources are failing and why.

5. **Identify the issue** — Call `GET /v1/resources/<type>?testIdMatchesAny={testId}` to list the specific resources failing the test.

6. **Remediate** — Either fix the resource in the source system (if it's synced data) or update the resource metadata in Vanta using `PATCH /v1/resources/<type>/{resourceId}`.

7. **Verify** — Re-run the test or wait for the next automated evaluation to confirm the fix.

### Typical task: Build a private integration

1. **Create an application** — In Vanta Dashboard → Settings → Developer Console, create a "Build Integrations" app (private). Copy the `client_id` and `client_secret`.

2. **Define your resource schema** — In Vanta Dashboard → Resources → + Create Resource, choose a base type (UserAccount, Computer, etc.) or CustomResource. Define custom properties if needed. Copy the Resource ID.

3. **Authenticate** — Exchange credentials for an `access_token` using `client_credentials` flow.

4. **Compute full state** — In your integration, fetch the complete current state of resources from the source system.

5. **Sync to Vanta** — Call `PUT /v1/resources/<resourceId>` with the full resource list. This is a full-state sync; omitted resources are marked deleted.

6. **Schedule recurring syncs** — Run the integration on a schedule (typically hourly) to keep Vanta's data fresh.

7. **Pair with tests** — If using custom resources, create Custom Tests in the Vanta Dashboard to define what "compliant" means. Built-in resources get tests automatically.

### Typical task: Connect an AI agent via MCP

1. **Verify admin access** — Confirm you're a Vanta Admin; MCP is not available to non-Admin users.

2. **Choose your AI tool** — Claude Code, Cursor, Perplexity, or another MCP-compatible client.

3. **Add the MCP server** — Use the tool-specific setup (see Quick Reference). For Claude Code: `claude mcp add --transport http vanta https://mcp.vanta.com/mcp`.

4. **Authorize** — Run `/mcp` in your AI tool, select Vanta, and complete the OAuth flow in your browser.

5. **Use MCP tools** — The agent can now list failing tests, inspect controls, assess vendor risk, and generate remediation plans.

## Common gotchas

- **Token revocation on new mint** — Vanta allows only one active token per Application. Requesting a new token immediately revokes the previous one. Don't run two processes that both mint tokens for the same app; centralize token issuance.

- **Content-Type must be JSON** — The `/oauth/token` endpoint requires `Content-Type: application/json`, not `application/x-www-form-urlencoded`. Many OAuth libraries default to form-encoded; override this.

- **Don't call regional API hostnames** — `api.eu.vanta.com` and `api.aus.vanta.com` exist but only redirect to `https://api.vanta.com`. Many HTTP libraries don't replay POST bodies through redirects, causing token requests to fail. Always call `https://api.vanta.com` directly.

- **Full-state sync, not incremental** — When syncing resources via Build Integrations API, every `PUT` replaces the entire set. Omitted resources are marked deleted. Compute and send the full current state on every run.

- **Custom resources need custom tests** — A custom resource without a Custom Test contributes zero evidence to controls. Pair every custom resource with a Custom Test that defines pass/fail logic.

- **Custom tests are immutable** — Once created, a Custom Test cannot be edited. Copy and edit the copy if you need changes.

- **Webhook signatures must be verified** — Always verify Svix signatures in production using the endpoint's signing secret. Use the raw request body (not parsed JSON) for verification.

- **Webhook responses must be fast** — Return `2xx` within 15 seconds, then process asynchronously. Slow processing causes retries.

- **Scope mismatch returns invalid_scope** — Requesting a scope that doesn't match your app type (e.g., Manage Vanta scope on a Build Integrations app) returns `invalid_scope`. Check the scope table for your app type.

- **MCP requires admin role** — The Vanta MCP server is only accessible to Vanta Admins. Non-Admin users cannot connect.

- **Refresh token rotation** — For public integrations using `authorization_code` flow, every refresh returns a new `refresh_token`. Persist it immediately; the old token expires 3 hours after first reuse.

## Verification checklist

Before submitting work with the Vanta API:

- [ ] **Token is fresh** — Verify the access token was minted within the last hour (tokens expire after 3600 seconds).
- [ ] **Correct API surface** — Confirm you're calling the right API (Manage Vanta, Build Integrations, or Auditor) for your task.
- [ ] **Scopes are minimal** — Request only the scopes your app actually needs; over-scoped tokens are a security risk.
- [ ] **Base URL is correct** — Use `https://api.vanta.com` (not regional hostnames) unless you're on Vanta Gov.
- [ ] **Authorization header is present** — Every request includes `Authorization: Bearer <access_token>`.
- [ ] **Content-Type is JSON** — Token requests and API calls use `Content-Type: application/json`.
- [ ] **Full state is synced** — For integrations, every `PUT /v1/resources/<type>` includes the complete current state.
- [ ] **Webhook signatures are verified** — If handling webhooks, verify Svix signatures using the endpoint's signing secret.
- [ ] **Webhook responses are fast** — Webhook handlers return `2xx` within 15 seconds, then process asynchronously.
- [ ] **Custom resources have tests** — Every custom resource is paired with a Custom Test that defines pass/fail logic.
- [ ] **Error handling is in place** — Code handles `401` (expired token), `429` (rate limit), and `5xx` (server errors) gracefully.

## Resources

- **[Vanta Developer Hub llms.txt](https://developer.vanta.com/llms.txt)** — Comprehensive page-by-page navigation for all Vanta API documentation.
- **[API Overview](https://developer.vanta.com/reference/overview)** — The three APIs, base URLs, authentication, scopes, and error codes.
- **[Manage Vanta API Reference](https://developer.vanta.com/reference/manage-vanta/overview)** — Full endpoint reference for automating your own tenant.
- **[Build Integrations API Reference](https://developer.vanta.com/reference/build-integrations/overview)** — Full endpoint reference for pushing data into Vanta.

---

> For additional documentation and navigation, see: https://developer.vanta.com/llms.txt