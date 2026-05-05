# Agent Knowledge: Deployment

## CI/CD Pipeline

- **Platform**: GitHub Actions (primary), Azure DevOps (legacy services)
- **Registry**: Azure Container Registry (acr-prod.azurecr.io)
- **Strategy**: Blue-green for App Service, rolling update for AKS

## Deployment Flow

1. PR merged to `main` → GitHub Actions triggered
2. Build container image → Push to ACR with `main-{sha}` tag
3. Deploy to **staging** → Run integration tests
4. Manual approval gate → Deploy to **production**
5. Canary: 10% traffic → 50% → 100% over 30 minutes
6. Post-deploy health check runs automatically

## Rollback Procedures

### AKS (Primary Method)
```bash
kubectl rollout undo deployment/<name> -n production
kubectl rollout status deployment/<name> -n production
```

### App Service (Slot Swap)
```bash
az webapp deployment slot swap -g rg-prod-web -n app-web --slot staging --target-slot production
```

### Container Apps
```bash
az containerapp revision activate -g <rg> -n <app> --revision <previous>
az containerapp ingress traffic set -g <rg> -n <app> --revision-weight <previous>=100
```

## Version Lookup

- **Current production version**: Check AKS deployment image tag or App Service configuration
- **Deployment history**: GitHub Actions run history or `kubectl rollout history`
- **Last deploy time**: Check deployment annotations on AKS resources

## Deployment Windows

- **Production**: Weekdays 10:00-16:00 UTC (avoid Fridays)
- **Emergency hotfix**: Anytime with on-call engineer approval
- **Database migrations**: Scheduled maintenance windows only
