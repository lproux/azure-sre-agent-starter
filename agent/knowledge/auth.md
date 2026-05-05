# Agent Knowledge: Authentication & Identity

## Identity Providers

| Component | Auth Method | Provider |
|-----------|------------|----------|
| User login | OIDC | Microsoft Entra ID (Azure AD) |
| Service-to-service | Managed Identity | User-Assigned MI per service |
| External APIs | API Key + OAuth2 | Key Vault stored secrets |
| Database | Managed Identity | Entra ID authentication |

## Managed Identities

| Service | Identity Name | Roles |
|---------|--------------|-------|
| AKS | id-aks-prod | AcrPull, Key Vault Secrets User, Storage Blob Reader |
| App Service | id-web-prod | Key Vault Secrets User |
| Functions | id-func-prod | Storage Queue Contributor, Key Vault Secrets User |

## Key Vault

- **Production**: kv-prod-[region]
- **Staging**: kv-staging-[region]
- **Access**: RBAC model (not access policies)
- **Secret rotation**: Automated for database passwords (90-day cycle)
- **Certificate management**: Auto-renewal enabled for App Service certs

## Common Auth Issues

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| 401 from API | Token expired or wrong audience | Check token audience, refresh |
| 403 from storage | Missing RBAC role | Add role assignment for MI |
| Key Vault 403 | Network restriction or missing role | Check firewall rules + RBAC |
| Database auth fail | MI not configured on server | Enable Entra admin on DB server |
