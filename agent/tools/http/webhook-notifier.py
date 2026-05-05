# ============================================================================
# Python Tool: Webhook Notifier (HTTP Client Tool)
# Purpose: Send investigation summaries to external webhooks (Slack, custom APIs)
# Setup: Builder > Agent Canvas > Create > Tool > Python Tool
# ============================================================================
#
# Tool Name: webhook-notifier
# Description: Sends a structured notification payload to an HTTP webhook endpoint.
#              Supports Slack-compatible formatting, Microsoft Teams Adaptive Cards,
#              and generic JSON payloads. Use for alerting external systems.
#
# Parameters:
#   webhook_url (str): The webhook endpoint URL
#   title (str): Notification title/summary
#   message (str): The notification body text
#   severity (str, optional): "critical", "warning", "info" — default "info"
#   format (str, optional): "slack", "teams", "generic" — default "generic"

def main(webhook_url: str, title: str, message: str, severity: str = "info", format: str = "generic") -> dict:
    """Send a notification to an HTTP webhook endpoint."""
    import requests
    import json
    from datetime import datetime, timezone

    severity_colors = {
        "critical": "#FF0000",
        "warning": "#FFA500",
        "info": "#0078D4",
    }
    color = severity_colors.get(severity.lower(), "#0078D4")

    timestamp = datetime.now(timezone.utc).isoformat()

    if format.lower() == "slack":
        payload = {
            "attachments": [{
                "color": color,
                "title": title,
                "text": message,
                "footer": "Azure SRE Agent",
                "ts": int(datetime.now(timezone.utc).timestamp()),
                "fields": [
                    {"title": "Severity", "value": severity.upper(), "short": True},
                    {"title": "Time (UTC)", "value": timestamp, "short": True},
                ],
            }]
        }
    elif format.lower() == "teams":
        payload = {
            "type": "message",
            "attachments": [{
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.4",
                    "body": [
                        {"type": "TextBlock", "text": title, "weight": "Bolder", "size": "Large", "color": "Attention" if severity == "critical" else "Default"},
                        {"type": "TextBlock", "text": message, "wrap": True},
                        {"type": "FactSet", "facts": [
                            {"title": "Severity", "value": severity.upper()},
                            {"title": "Time (UTC)", "value": timestamp},
                            {"title": "Source", "value": "Azure SRE Agent"},
                        ]},
                    ],
                },
            }],
        }
    else:
        payload = {
            "title": title,
            "message": message,
            "severity": severity.upper(),
            "timestamp": timestamp,
            "source": "Azure SRE Agent",
        }

    try:
        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30,
        )
        return {
            "status": "sent",
            "status_code": response.status_code,
            "format": format,
            "webhook_url": webhook_url[:50] + "..." if len(webhook_url) > 50 else webhook_url,
        }
    except Exception as e:
        return {"status": "failed", "error": str(e)}
