# Runbook: AKS Cluster Scaling

## Trigger
- Node CPU/memory utilization consistently > 80%
- Pods in Pending state due to insufficient resources
- Anticipated traffic increase (event, campaign, etc.)

## Pre-Checks
1. Current node count and utilization:
   ```bash
   kubectl top nodes
   kubectl get nodes -o wide
   ```
2. Pending pods:
   ```bash
   kubectl get pods --all-namespaces --field-selector=status.phase=Pending
   ```
3. Cluster autoscaler status:
   ```bash
   kubectl -n kube-system logs -l app=cluster-autoscaler --tail=20
   ```

## Scaling Procedures

### Horizontal Pod Autoscaler (Preferred)
```bash
# Check current HPA status
kubectl get hpa -A

# Manually scale deployment if HPA isn't responding
kubectl scale deployment/<name> -n <namespace> --replicas=<count>
```

### Node Pool Scaling (Manual)
```bash
# Scale user node pool
az aks nodepool scale \
  --resource-group <rg> \
  --cluster-name <cluster> \
  --name <nodepool> \
  --node-count <count>

# Monitor scaling
watch -n 10 'kubectl get nodes'
```

### Add New Node Pool (For different VM sizes)
```bash
az aks nodepool add \
  --resource-group <rg> \
  --cluster-name <cluster> \
  --name <pool-name> \
  --node-count 3 \
  --node-vm-size Standard_D4s_v5 \
  --mode User
```

### Cluster Autoscaler Configuration
```bash
# Update autoscaler limits
az aks nodepool update \
  --resource-group <rg> \
  --cluster-name <cluster> \
  --name <nodepool> \
  --enable-cluster-autoscaler \
  --min-count 3 \
  --max-count 20
```

## Post-Scaling Verification
1. All nodes in Ready state: `kubectl get nodes`
2. Pending pods now scheduled: `kubectl get pods -A | grep Pending`
3. Resource utilization normalized: `kubectl top nodes`
4. No eviction events: `kubectl get events --sort-by=.metadata.creationTimestamp | grep Evict`

## Scale-Down Considerations
- Wait for traffic to normalize before scaling down
- Ensure PodDisruptionBudgets are configured
- Cluster autoscaler scale-down delay: 10 minutes by default
- Drain nodes gracefully: `kubectl drain <node> --ignore-daemonsets --delete-emptydir-data`

## Cost Impact
- Each additional Standard_D4s_v5 node: ~$140/month
- Monitor actual usage vs. provisioned capacity weekly
- Consider spot instances for non-critical workloads
