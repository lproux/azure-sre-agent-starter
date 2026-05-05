# Certificate Renewal Guide
# Skill: certificate-renewal
# Description: Use when checking or renewing TLS/SSL certificates
# Tools: RunAzCliReadCommands, RunAzCliWriteCommands

## Step 1: Scan for Expiring Certificates

```bash
# Key Vault: List certificates with expiration
az keyvault certificate list --vault-name {{VAULT_NAME}} --query "[].{name:name, expires:attributes.expires, enabled:attributes.enabled}" -o table

# App Service: Check custom domain SSL bindings
az webapp config ssl list --resource-group {{RESOURCE_GROUP}} --query "[].{thumbprint:thumbprint, subjectName:subjectName, expirationDate:expirationDate, hostNames:hostNames}" -o table

# Application Gateway: Check SSL certificates
az network application-gateway ssl-cert list --resource-group {{RESOURCE_GROUP}} --gateway-name {{GATEWAY_NAME}}
```

**Urgency classification**:
| Days to Expiry | Action |
|---|---|
| < 7 days | **CRITICAL** — Renew immediately |
| 7-30 days | **HIGH** — Schedule renewal this week |
| 30-90 days | **MEDIUM** — Plan renewal |
| > 90 days | **LOW** — Monitor |

## Step 2: Renew Certificate

### Key Vault Managed Certificate (Auto-Renewal)
```bash
# Check if auto-renewal is enabled
az keyvault certificate show --vault-name {{VAULT_NAME}} --name {{CERT_NAME}} --query "policy.lifetimeActions"

# Enable auto-renewal (renew at 80% of lifetime)
az keyvault certificate set-attributes --vault-name {{VAULT_NAME}} --name {{CERT_NAME}} --policy @policy.json
```

### App Service Managed Certificate
```bash
# Create free managed certificate for custom domain
az webapp config ssl create --resource-group {{RESOURCE_GROUP}} --name {{APP_NAME}} --hostname {{DOMAIN_NAME}}

# Bind certificate to the domain
az webapp config ssl bind --resource-group {{RESOURCE_GROUP}} --name {{APP_NAME}} --certificate-thumbprint {{THUMBPRINT}} --ssl-type SNI
```

### Manual Certificate Upload
```bash
# Upload PFX to Key Vault
az keyvault certificate import --vault-name {{VAULT_NAME}} --name {{CERT_NAME}} --file {{PFX_FILE}} --password {{PFX_PASSWORD}}

# Upload to App Service
az webapp config ssl upload --resource-group {{RESOURCE_GROUP}} --name {{APP_NAME}} --certificate-file {{PFX_FILE}} --certificate-password {{PFX_PASSWORD}}
```

## Step 3: Verify Renewal

```bash
# Check the new certificate details
az keyvault certificate show --vault-name {{VAULT_NAME}} --name {{CERT_NAME}} --query "{subject:x509CertificateProperties.subject, expires:attributes.expires, enabled:attributes.enabled}"

# Test TLS externally
openssl s_client -connect {{DOMAIN}}:443 -servername {{DOMAIN}} < /dev/null 2>/dev/null | openssl x509 -noout -dates
```

## Step 4: Proactive Monitoring Setup

Create an Azure Monitor alert for certificates expiring within 30 days:
```bash
az monitor metrics alert create \
  --name "cert-expiry-warning" \
  --resource-group {{RESOURCE_GROUP}} \
  --scopes "/subscriptions/{{SUB_ID}}/resourceGroups/{{RESOURCE_GROUP}}/providers/Microsoft.KeyVault/vaults/{{VAULT_NAME}}" \
  --condition "avg CertificateNearExpiry > 0" \
  --description "Certificate in Key Vault is expiring within 30 days"
```
