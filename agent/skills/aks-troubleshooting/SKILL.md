# AKS Troubleshooting Guide
# Skill: aks-troubleshooting
# Description: Use when investigating AKS or Kubernetes issues
# Tools: RunAzCliReadCommands, RunKubectlCommands, QueryLogAnalytics

## Step 1: Cluster Health Check

```bash
# Check cluster status
az aks show --resource-group {{RESOURCE_GROUP}} --name {{CLUSTER_NAME}} --query "{status:provisioningState, powerState:powerState.code, kubernetesVersion:kubernetesVersion, nodeCount:agentPoolProfiles[0].count}"

# Check node health
kubectl get nodes -o wide
kubectl top nodes
```

**Look for**: NotReady nodes, MemoryPressure, DiskPressure, PIDPressure conditions.

## Step 2: Pod Diagnostics

```bash
# List unhealthy pods
kubectl get pods --all-namespaces --field-selector=status.phase!=Running,status.phase!=Succeeded

# For CrashLoopBackOff pods
kubectl describe pod {{POD_NAME}} -n {{NAMESPACE}}
kubectl logs {{POD_NAME}} -n {{NAMESPACE}} --previous --tail=100
```

**Common pod failure patterns**:
| Status | Likely Cause | Quick Fix |
|--------|-------------|-----------|
| CrashLoopBackOff | App crash, OOM, bad config | Check logs, increase memory limits |
| ImagePullBackOff | Wrong image, auth failure | Verify image tag, check ACR auth |
| Pending | No capacity, taint mismatch | Check node resources, tolerations |
| Evicted | Node pressure | Check node conditions, resource limits |

## Step 3: Networking Diagnostics

```bash
# Check services and endpoints
kubectl get svc -A
kubectl get endpoints -A | grep -v "none"

# Check ingress
kubectl get ingress -A
kubectl describe ingress {{INGRESS_NAME}} -n {{NAMESPACE}}

# DNS resolution test
kubectl run dns-test --image=busybox:1.36 --rm -it --restart=Never -- nslookup {{SERVICE_NAME}}.{{NAMESPACE}}.svc.cluster.local
```

## Step 4: Resource Utilization

```kusto
// Container Insights: High CPU pods
Perf
| where ObjectName == "K8SContainer" and CounterName == "cpuUsageNanoCores"
| summarize AvgCPU = avg(CounterValue) by InstanceName, bin(TimeGenerated, 5m)
| where AvgCPU > 500000000  // > 500m CPU
| order by AvgCPU desc
| take 20
```

```kusto
// OOMKilled events
KubeEvents
| where Reason == "OOMKilling" or Reason == "OOMKilled"
| project TimeGenerated, Name, Namespace, Reason, Message
| order by TimeGenerated desc
| take 20
```

## Step 5: Scaling Analysis

```bash
# Check HPA status
kubectl get hpa -A
kubectl describe hpa {{HPA_NAME}} -n {{NAMESPACE}}

# Check cluster autoscaler
kubectl -n kube-system logs -l app=cluster-autoscaler --tail=50
```

## Step 6: Resolution Patterns

### CrashLoopBackOff Resolution
1. Get logs: `kubectl logs {{POD}} --previous`
2. Check resource limits: are they too low?
3. Check liveness/readiness probes: are timeouts too aggressive?
4. Check config maps/secrets: are they mounted correctly?

### Pending Pod Resolution
1. Check events: `kubectl describe pod {{POD}}`
2. Verify node capacity: `kubectl top nodes`
3. Check PVC: `kubectl get pvc -n {{NAMESPACE}}`
4. Check tolerations match taints: `kubectl get nodes -o json | jq '.items[].spec.taints'`

### Network Connectivity Resolution
1. Verify NetworkPolicy allows traffic
2. Check NSG rules on the AKS subnet
3. Verify DNS resolution from within the cluster
4. Check if Service selectors match pod labels
