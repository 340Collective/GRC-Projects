# UAR Simulation Templates (reference copy)
These templates are a contractor-facing reference copy. The source of truth is the private 340collective-website repo, and the ISSM deploys from there. Nothing is deployed from the GRC repo.

| Template | Contents |
| --- | --- |
| grc-uar-sim-base.yaml | The `uar-sim-deny-all-boundary` permissions boundary, the synthetic customer managed policies, and 14 groups, each with an inline deny-all guard |
| grc-uar-sim-users-1.yaml to grc-uar-sim-users-5.yaml | The 222 synthetic IAM users, split so each template stays under the 51,200 byte inline limit |

The files are generated. Do not hand-edit them. Deploy order is base, then users-1 to users-5. Teardown order is users-5 to users-1, then base. See [../README.md](../README.md).
