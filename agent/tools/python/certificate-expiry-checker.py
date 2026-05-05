# ============================================================================
# Python Tool: Certificate Expiry Checker
# Purpose: Check SSL/TLS certificate expiration for a list of endpoints
# Setup: Builder > Agent Canvas > Create > Tool > Python Tool
# ============================================================================
#
# Tool Name: certificate-expiry-checker
# Description: Checks TLS certificate expiration for a list of hostnames.
#              Returns days until expiry and urgency classification.
#
# Parameters:
#   hostnames (list[str]): List of hostnames to check (e.g., ["api.contoso.com", "app.contoso.com"])
#   port (int, optional): Port to connect on, default 443
#   warning_days (int, optional): Days threshold for warning, default 30

def main(hostnames: list, port: int = 443, warning_days: int = 30) -> dict:
    """Check TLS certificate expiration for given hostnames."""
    import ssl
    import socket
    from datetime import datetime, timezone

    results = []
    critical = 0
    warning = 0
    healthy = 0

    for hostname in hostnames:
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    not_after = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
                    not_after = not_after.replace(tzinfo=timezone.utc)
                    days_left = (not_after - datetime.now(timezone.utc)).days

                    if days_left < 7:
                        status = "🔴 CRITICAL"
                        critical += 1
                    elif days_left < warning_days:
                        status = "🟡 WARNING"
                        warning += 1
                    else:
                        status = "✅ HEALTHY"
                        healthy += 1

                    results.append({
                        "hostname": hostname,
                        "status": status,
                        "days_until_expiry": days_left,
                        "expiry_date": not_after.isoformat(),
                        "issuer": dict(x[0] for x in cert.get("issuer", [])).get("organizationName", "Unknown"),
                        "subject": dict(x[0] for x in cert.get("subject", [])).get("commonName", "Unknown"),
                    })
        except Exception as e:
            results.append({
                "hostname": hostname,
                "status": "⚠️ CHECK FAILED",
                "error": str(e),
                "days_until_expiry": -1,
            })
            critical += 1

    return {
        "total_checked": len(hostnames),
        "critical": critical,
        "warning": warning,
        "healthy": healthy,
        "warning_threshold_days": warning_days,
        "results": sorted(results, key=lambda x: x.get("days_until_expiry", -1)),
    }
