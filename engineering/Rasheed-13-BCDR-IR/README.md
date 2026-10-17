# BC/DR and Incident Response Compliance

An AWS-native way to prove that backups restore and that incident response is practiced, written from the compliance evidence angle. AWS Backup protects the data, a quarterly Step Functions DR test restores a recovery point into an isolated test target, validates it, and records the achieved RTO and RPO against targets. IR runbooks and tabletop exercise records are kept as evidence, and any failed or late test becomes a finding in the risk register and the evidence lake. It supports SOC 2 A1.2, A1.3, CC7.4, and CC7.5; ISO 27001:2022 A.5.24 to A.5.30; and NIST CSF 2.0 RS and RC. Backups, restore tests, validation, RTO and RPO evidence, and finding routing are automated; the IR lead runs tabletop exercises and signs off each DR test result.

Status: target design, not yet deployed.

![BC/DR and Incident Response Compliance AWS architecture](diagram/bcdr-ir-aws-architecture.png)

## Automation moving parts

1. AWS Backup plans protect the DynamoDB tables and S3 data.
2. A quarterly EventBridge Scheduler run starts a Step Functions DR test.
3. The test restores a recovery point to an isolated test target, runs a validation Lambda (row counts, checksums), and times the restore.
4. Results (achieved RTO and RPO compared with targets) are written to DynamoDB, and the test report goes to S3.
5. IR runbooks (Systems Manager Automation documents) and tabletop exercise records are stored in S3.
6. Failed or late tests become findings sent through EventBridge to the 07 risk register and the 06 evidence lake.

## 340 Collective testbed

340 Collective's real AWS infrastructure is the environment this design is validated against. The DR test exercises 340 Collective's own backup plans for its DynamoDB tables and S3 data, and the IR lead runs tabletop exercises against 340 Collective's incident response process. No client data, account identifiers, or resource names are published in this repo.

## Files

| File | What it is |
| --- | --- |
| [diagram/bcdr-ir-aws-architecture.png](diagram/bcdr-ir-aws-architecture.png) | Architecture diagram (PNG, 2x) |
| [diagram/bcdr-ir-aws-architecture.svg](diagram/bcdr-ir-aws-architecture.svg) | Same diagram as a scalable SVG |
| [diagram/build_diagram.py](diagram/build_diagram.py) | Script that regenerates the diagram and runs its layout and sensitive-text checks |
| [BCDR-IR-Architecture.md](BCDR-IR-Architecture.md) | Stage-by-stage breakdown: backup, DR test, results, incident response, findings routing, downstream, data model, security, cost note, build order |
| [LAB-STEPS.md](../../non-engineering/Jason-13-BCDR-IR/LAB-STEPS.md) | Build playbook: manual lab steps for the collaboration team |

## Regenerate the diagram

```bash
python3 diagram/build_diagram.py --setup          # once: venv + diagrams==0.25.1 (needs rsvg-convert from librsvg)
python3 diagram/build_diagram.py diagram/bcdr-ir-aws-architecture
```

The script must print `crossings: 0`, `layout problems: none`, and `sensitive text: none`.

## Notes

- Approvers: the IR lead signs off each DR test result and each tabletop record; the 340 Collective owner approves the RTO and RPO targets and accepts any finding a failed test raises.
- Restore tests always run into an isolated test target (a restored copy, never the live resource), and the test target is deleted after the check. A DR test never touches production data.
- Connections show design intent. Nothing is deployed yet, so no line is verified from IaC.
- Pairs with [07 Risk Register](../Rasheed-07-Risk-Register/README.md) (failed tests become risks), [06 Evidence Automation](../Maria-06-Evidence-Automation/README.md) (test results are BC/DR evidence), and [10 Audit Engagement Manager](../Maria-10-Audit-Engagement-Manager/README.md) (auditors request these records as PBC items).
