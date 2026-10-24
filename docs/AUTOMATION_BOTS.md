# Automation Bots — Agent Cipher

**Source of truth (full guide):** [chichi-lyman/saphira-ai — docs/AUTOMATION_BOTS.md](https://github.com/chichi-lyman/saphira-ai/blob/main/docs/AUTOMATION_BOTS.md)

This repository is the identity / specialist mirror for **Agent Cipher** inside the Nova Umbrella ecosystem.

---

## Automation Box (Cipher-specific)

Agent Cipher sits on the security boundary between NovaReign dispatchers and any external LLM or third-party endpoint. When automation bots (GitHub Actions, webhooks, RPA, or multi-agent loops) call external models, Cipher is the gate that must run first.

### Responsibilities in automation flows

| Concern | Cipher action |
|---------|----------------|
| Prompt sanitization | Strip raw passwords, API keys, tokens, PII, and financial identifiers before the payload leaves the trust boundary |
| Zero-trust encryption | Ensure secrets never enter LLM context; use vault / env references only |
| Outbound policy | Enforce ALLOW / REQUIRE_APPROVAL / DENY decisions made upstream by Agent Two |
| Audit trail | Emit structured events to the Redis Pub/Sub bus and local audit log for every sanitized request |

### How bots should invoke Cipher

1. **GitHub Actions / scheduled bots**  
   Call the Saphira pipeline (or a thin FastAPI route) that always routes through Cipher before any external provider adapter.

2. **Webhook listeners**  
   External systems posting to a Nova Umbrella endpoint must pass through the same sanitization step; never forward raw webhook bodies to third-party LLMs.

3. **Multi-agent / autonomous loops (Manus, Muse, custom)**  
   Cipher is required before every outbound tool call that leaves the local trust zone.

### Recommended configuration checklist

- [ ] Repository secrets (PATs, provider keys) live only under **Settings → Secrets and variables → Actions**
- [ ] No secret values appear in workflow logs or commit history
- [ ] Any bot that generates or forwards prompts runs the Cipher sanitization step
- [ ] High-risk actions (payments, email send, production deploys) remain gated by Agent Two even after Cipher cleans the payload

### Related docs in the monorepo

- [docs/AUTOMATION_BOTS.md](https://github.com/chichi-lyman/saphira-ai/blob/main/docs/AUTOMATION_BOTS.md) — full bot taxonomy and setup paths
- [docs/NOVA_UMBRELLA_MASTER_CONTROL_PLANE.md](https://github.com/chichi-lyman/saphira-ai/blob/main/docs/NOVA_UMBRELLA_MASTER_CONTROL_PLANE.md) — pipeline order and domain-agent roles
- [docs/SOVEREIGN_COGNITIVE_OS_CAPABILITIES.md](https://github.com/chichi-lyman/saphira-ai/blob/main/docs/SOVEREIGN_COGNITIVE_OS_CAPABILITIES.md) — security & governance capability surface

Agent Cipher does not replace GitHub-native bots (Dependabot, Stale, CodeRabbit). It complements them by guaranteeing that any automation path that reaches an external model is scrubbed and policy-compliant first.
