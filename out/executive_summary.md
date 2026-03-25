# Executive Summary

- Total cryptographic assets normalized: **11**
- Wave 1 assets (to 2028): **10**
- Wave 2 assets (to 2031): **1**
- Wave 3 assets (to 2035): **0**
- Monitor/aligned assets: **0**

## Recommended program shape

1. Finish discovery and owner mapping for all Wave 1 assets.
2. Start design decisions for ML-KEM, ML-DSA, SLH-DSA, or hybrid adoption paths where appropriate.
3. Track vendor readiness and interoperability constraints for externally managed systems.
4. Use the inventory as a living artifact inside broader cyber risk and architecture governance.

## Highest-priority items

- **api.novabank.example:443** — ECDHE — score 100 — Plan migration to ML-KEM or hybrid key establishment
- **api.novabank.example:443 certificate** — RSA — score 100 — Plan migration to ML-KEM or hybrid key establishment
- **Legacy RSA verification key detected** — RSA — score 78 — Plan migration to ML-KEM or hybrid key establishment
- **ECDH key exchange in TLS helper** — ECDH — score 78 — Plan migration to ML-KEM or hybrid key establishment
- **RSA-PKCS1-2048-Signing** — RSASSA-PKCS1 — score 70 — Plan migration to ML-DSA or SLH-DSA, potentially via hybrid deployments
- **Public TLS Gateway** — ECDHE — score 70 — Plan migration to ML-KEM or hybrid key establishment
- **api.novabank.example certificate** — RSA — score 70 — Plan migration to ML-KEM or hybrid key establishment
- **RSA-2048 Active Server Key** — RSA — score 70 — Plan migration to ML-KEM or hybrid key establishment
- **admin.novabank.example:22** — RSA — score 70 — Plan migration to ML-KEM or hybrid key establishment
- **admin.novabank.example:22 certificate** — RSA — score 70 — Plan migration to ML-KEM or hybrid key establishment
