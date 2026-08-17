# Archive Gate Checklist

Date: 2026-08-16

Gate status: NOT READY — archive/freeze requires a later explicit approval

This checklist prepares a non-destructive archive decision. Completing it does
not authorize deletion, remote archival, force push, history rewrite, provider
execution, build execution, or sensitive-file inspection by an unauthorized
reviewer.

## Identity and preservation

- [x] Canonical name recorded: `forge-os-endgame-edition`
- [x] Lifecycle classified: superseded predecessor
- [x] Canonical replacements mapped by responsibility
- [x] Pre-documentation branch and commit recorded: `main` at
  `aaa948ce1ae1704238d9962144d130a5d38d2c0d`
- [x] GitHub and Codeberg remotes recorded
- [x] Harvest ledger created
- [x] Unsupported claims quarantined in current transition documentation
- [ ] Final post-harvest branch and commit approved
- [ ] Final remote refs verified and preservation receipt stored externally

## Selective harvest

- [ ] Endgame OS/Core/Harness owner reviews each operator/tooling candidate
- [ ] Project Monolith owner reviews each Experience/workstation UX candidate
- [ ] Project Forge owner reviews each registry/control-plane candidate against
  its charter
- [ ] Cerberus or lawful-OSINT owner reviews each investigation/case candidate
- [ ] Every accepted item records source path, destination, license/provenance,
  transformation, tests, and reviewer
- [ ] Every rejected item records the reason it was intentionally not migrated
- [ ] No broad claim or repository subtree is imported wholesale

## Legal, privacy, and security

- [ ] Qualified reviewer resolves the restricted-use license, ownership,
  branding, contact, and redistribution questions
- [ ] Lawful authority, privacy impact, source terms, data minimization,
  retention, human review, and misuse controls are defined for any OSINT concept
- [ ] Evidence-handling/court-admissibility claims receive qualified legal and
  forensic review
- [ ] Security and encryption claims receive a current threat model and
  implementation review
- [ ] An authorized security reviewer handles the excluded sensitive-looking
  file without exposing its contents in migration reports
- [ ] Raw evidence, case data, credentials, secrets, logs, and sensitive scan
  outputs are excluded from ordinary migration and publication
- [ ] Generated scan-report provenance, scope, freshness, and safe retention are
  established

## Technical state

- [x] Existing code review identifies material build/runtime blockers
- [ ] A safe, unprivileged reviewer independently confirms the retained source
  inventory without running build/ISO/USB targets
- [ ] Current build/test state is recorded honestly as unavailable, failed, or
  verified; no result is inferred
- [ ] External dependency and SDK versions are inventoried without credential
  access
- [ ] GitHub automation is reviewed for safe frozen-repository behavior
- [ ] Open issues, pull requests, releases, packages, and downstream references
  are inventoried read-only

## Archive/freeze execution prerequisites

- [ ] Cash approves the completed harvest ledger and every unresolved item
- [ ] The Todoist lifecycle gate links to this checklist and records approval
- [ ] A prominent root-level supersession notice is approved if needed
- [ ] Project Forge registry state points active alerts to canonical successors
- [ ] GitHub and Codeberg archive/freeze actions are separately authorized
- [ ] Final review confirms no deletion, history rewrite, or force push is
  required
- [ ] Recovery instructions name the final branch, commit, remotes, and clone
  procedure

## Explicitly deferred from this pass

- GitHub or Codeberg archival/freeze;
- repository deletion or file cleanup;
- building or testing the distro, ISO, container, USB, or agent runtime;
- resolving or inspecting sensitive material;
- importing predecessor code or claims; and
- changing successor repositories based on this ledger alone.

## Archive decision template

```text
Decision: APPROVE ARCHIVE | DEFER | REJECT
Approved by:
Date:
Final branch:
Final commit:
GitHub disposition:
Codeberg disposition:
Harvest ledger approved:
Sensitive-material review receipt:
Legal/privacy/security review receipts:
Remaining non-migrated material:
Recovery location and clone procedure:
```
