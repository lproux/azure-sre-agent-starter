# ============================================================================
# Python Tool: SLA Calculator
# Purpose: Calculate SLA compliance from uptime/downtime metrics
# Setup: Builder > Agent Canvas > Create > Tool > Python Tool
# ============================================================================
#
# Tool Name: sla-calculator
# Description: Calculate SLA compliance percentage from uptime and downtime minutes.
#              Returns whether the target SLA (default 99.9%) is met,
#              remaining error budget, and allowed downtime per month.
#
# Parameters:
#   uptime_minutes (int): Total minutes of service availability
#   downtime_minutes (int): Total minutes of service unavailability
#   target_sla (float, optional): Target SLA percentage, default 99.9

def main(uptime_minutes: int, downtime_minutes: int, target_sla: float = 99.9) -> dict:
    """Calculate SLA compliance and error budget from uptime/downtime."""

    total_minutes = uptime_minutes + downtime_minutes
    if total_minutes == 0:
        return {"error": "Total minutes cannot be zero"}

    # Calculate actual SLA
    actual_sla = (uptime_minutes / total_minutes) * 100

    # Monthly error budget (assuming 30-day month = 43,200 minutes)
    monthly_minutes = 43200
    allowed_downtime_monthly = monthly_minutes * (1 - target_sla / 100)
    error_budget_remaining = allowed_downtime_monthly - downtime_minutes

    # SLA tiers for context
    sla_tiers = {
        99.0: {"downtime_monthly": "7h 18m", "name": "Two Nines"},
        99.9: {"downtime_monthly": "43m 50s", "name": "Three Nines"},
        99.95: {"downtime_monthly": "21m 55s", "name": "Three and a Half Nines"},
        99.99: {"downtime_monthly": "4m 23s", "name": "Four Nines"},
        99.999: {"downtime_monthly": "26s", "name": "Five Nines"},
    }

    return {
        "actual_sla_percent": round(actual_sla, 4),
        "target_sla_percent": target_sla,
        "meets_target": actual_sla >= target_sla,
        "uptime_minutes": uptime_minutes,
        "downtime_minutes": downtime_minutes,
        "total_minutes": total_minutes,
        "error_budget_remaining_minutes": round(error_budget_remaining, 1),
        "error_budget_consumed_percent": round(
            (downtime_minutes / allowed_downtime_monthly) * 100, 1
        ) if allowed_downtime_monthly > 0 else 100,
        "allowed_downtime_monthly_minutes": round(allowed_downtime_monthly, 1),
        "status": "✅ COMPLIANT" if actual_sla >= target_sla else "🔴 BREACH",
        "sla_tiers_reference": sla_tiers,
    }
