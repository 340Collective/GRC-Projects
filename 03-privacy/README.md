# Privacy Operations

An AWS-native privacy operations design for GDPR, CCPA, and CPRA. Amazon Macie discovers personal data, an inventory Lambda keeps a record of processing activities (RoPA) current in DynamoDB, a consent and opt-out API records choices, and a Step Functions workflow fulfills data subject access requests (DSARs) inside the legal deadline. Discovery, inventory updates, request intake, data location, and deadline tracking are automated; the privacy owner approves every release.

Status: target design, not yet deployed.

![Privacy Operations AWS architecture](diagram/privacy-aws-architecture.png)

## Automation moving parts

1. A scheduled Lambda exports DynamoDB tables to a private staging prefix in S3.
2. Macie discovery jobs classify PII in S3 (client files, form uploads, and the staging prefix).
3. Macie findings go through EventBridge to an inventory updater Lambda.
4. The DynamoDB data inventory (RoPA) holds data category, purpose, lawful basis, retention, and location.
5. The consent and opt-out API (API Gateway and Lambda) writes a consent ledger.
6. A DSAR starts a Step Functions workflow: verify identity, locate data from the inventory, assemble the package, wait for privacy owner approval, deliver.
7. SES sends the response, and a CloudWatch deadline alarm watches the GDPR (one month) and CCPA (45 days) clocks.

## 340 Collective testbed

340 Collective's real AWS infrastructure is the environment this design is validated against. The data in scope is the 340collective.com contact form submissions, newsletter subscribers, invoice records, and client files in the 340 Collective account, and every DSAR test uses synthetic test subjects only. No client data, account identifiers, or resource names are published in this repo.

## Files

| File | What it is |
| --- | --- |
| [diagram/privacy-aws-architecture.png](diagram/privacy-aws-architecture.png) | Architecture diagram (PNG, 2x) |
| [diagram/privacy-aws-architecture.svg](diagram/privacy-aws-architecture.svg) | Same diagram as a scalable SVG |
| [diagram/build_diagram.py](diagram/build_diagram.py) | Script that regenerates the diagram and runs its layout and sensitive-text checks |
| [Privacy-Architecture.md](Privacy-Architecture.md) | Stage-by-stage breakdown: data sources, PII discovery, RoPA inventory, consent, DSAR workflow, data model, security, cost note, build order |

## Regenerate the diagram

```bash
python3 diagram/build_diagram.py --setup          # once: venv + diagrams==0.25.1 (needs rsvg-convert from librsvg)
python3 diagram/build_diagram.py diagram/privacy-aws-architecture
```

The script must print `crossings: 0`, `layout problems: none`, and `sensitive text: none`.

## Notes

- Macie scans S3 only. It cannot scan RDS or DynamoDB directly, so a scheduled export Lambda writes DynamoDB items (and RDS snapshot exports, if RDS is ever added) to a private staging prefix that Macie scans. 340 Collective runs on S3 and DynamoDB today, not RDS.
- Connections show design intent. Nothing is deployed yet, so no line is verified from IaC.
- Pairs with [06 Evidence Automation](../06-evidence-automation/README.md) (DSAR records become privacy evidence) and [02 TPRM/VRM](../02-tprm-vrm/README.md) (vendors that process personal data).
