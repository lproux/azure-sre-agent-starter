# ============================================================================
# Python Tool: Cost Anomaly Detector
# Purpose: Detect spend anomalies by comparing current vs. baseline periods
# Setup: Builder > Agent Canvas > Create > Tool > Python Tool
# ============================================================================
#
# Tool Name: cost-anomaly-detector
# Description: Analyzes Azure cost data to detect spend anomalies.
#              Compares current period costs against a historical baseline
#              using standard deviation to identify outliers.
#
# Parameters:
#   current_costs (list[dict]): List of {service: str, cost: float} for current period
#   baseline_costs (list[dict]): List of {service: str, cost: float} for baseline period
#   threshold_percent (float, optional): Anomaly threshold %, default 20

def main(current_costs: list, baseline_costs: list, threshold_percent: float = 20.0) -> dict:
    """Detect cost anomalies by comparing current vs baseline spending."""
    import statistics

    # Aggregate by service
    current_by_svc = {}
    for item in current_costs:
        svc = item.get("service", "Unknown")
        current_by_svc[svc] = current_by_svc.get(svc, 0) + float(item.get("cost", 0))

    baseline_by_svc = {}
    for item in baseline_costs:
        svc = item.get("service", "Unknown")
        baseline_by_svc[svc] = baseline_by_svc.get(svc, 0) + float(item.get("cost", 0))

    # Detect anomalies
    anomalies = []
    all_services = set(list(current_by_svc.keys()) + list(baseline_by_svc.keys()))

    for svc in sorted(all_services):
        current = current_by_svc.get(svc, 0)
        baseline = baseline_by_svc.get(svc, 0)

        if baseline > 0:
            change_pct = ((current - baseline) / baseline) * 100
        elif current > 0:
            change_pct = 100.0  # New cost
        else:
            change_pct = 0.0

        entry = {
            "service": svc,
            "current_cost": round(current, 2),
            "baseline_cost": round(baseline, 2),
            "change_percent": round(change_pct, 1),
            "change_amount": round(current - baseline, 2),
        }

        if abs(change_pct) > threshold_percent:
            entry["status"] = "🔴 ANOMALY" if change_pct > 0 else "🟢 SAVINGS"
            anomalies.append(entry)
        else:
            entry["status"] = "✅ NORMAL"

    total_current = sum(current_by_svc.values())
    total_baseline = sum(baseline_by_svc.values())
    total_change = total_current - total_baseline

    return {
        "total_current_cost": round(total_current, 2),
        "total_baseline_cost": round(total_baseline, 2),
        "total_change": round(total_change, 2),
        "total_change_percent": round(
            (total_change / total_baseline * 100) if total_baseline > 0 else 0, 1
        ),
        "anomaly_count": len(anomalies),
        "anomalies": sorted(anomalies, key=lambda x: abs(x["change_percent"]), reverse=True),
        "threshold_percent": threshold_percent,
        "services_analyzed": len(all_services),
    }
