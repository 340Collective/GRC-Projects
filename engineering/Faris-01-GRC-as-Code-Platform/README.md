# GRC-as-Code Platform

An AWS-native GRC engineering environment that uses AWS security services as the audit engine. It continuously evaluates the cloud and identity environment against SOC 2, NIST 800-53, ISO 27001, PCI DSS, and HIPAA. All findings are centralized in one format (ASFF), routed through EventBridge, and turned into one Jira ticket per event, with a human approval gate before any change is deployed.

Status: target design, not yet deployed.

![GRC Engineering AWS architecture](diagram/grc-engineering-aws-architecture.png)

## Files

| File | What it is |
| --- | --- |
| [diagram/grc-engineering-aws-architecture.png](diagram/grc-engineering-aws-architecture.png) | Architecture diagram (PNG, 2x) |
| [diagram/grc-engineering-aws-architecture.svg](diagram/grc-engineering-aws-architecture.svg) | Same diagram as a scalable SVG |
| [diagram/build_diagram.py](diagram/build_diagram.py) | Script that regenerates the diagram and runs its layout and sensitive-text checks |
| [GRC-Platform-Architecture.md](GRC-Platform-Architecture.md) | Layer-by-layer breakdown: pipeline, producers, Security Hub, EventBridge routing, Lambdas, consumers, DynamoDB state, crosswalk, services, cost, repo structure, build order |
| [ASFF-Control-Matrix-Indexed.xlsx](../../non-engineering/Jason-01-GRC-as-Code-Platform/ASFF-Control-Matrix-Indexed.xlsx) | Control matrix mapping controls to framework requirements carried in ASFF `Compliance.RelatedRequirements` |
| [LAB-STEPS.md](../../non-engineering/Jason-01-GRC-as-Code-Platform/LAB-STEPS.md) | Build playbook: manual lab steps for the collaboration team |

## Regenerate the diagram

```bash
python3 diagram/build_diagram.py --setup          # once: venv + diagrams==0.25.1 (needs rsvg-convert from librsvg)
python3 diagram/build_diagram.py diagram/grc-engineering-aws-architecture
```

The script must print `crossings: 0`, `layout problems: none`, and `sensitive text: none`.

## Notes

- The diagram icon package has no Audit Manager icon, so the generic AWS security and compliance icon stands in for it.
