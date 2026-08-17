# Forge OS Endgame Edition Harvest Ledger

Date: 2026-08-16

Lifecycle: superseded — preserved pending selective harvest and archive approval

Harvest status: classification only; no material migrated

## Review boundary

This ledger uses the approved Endgame repository identity packet, tracked path
names, current-facing documentation, and the repository's existing code-review
summary. It does not validate the predecessor's feature claims and does not
authorize its build or operational paths.

The following were deliberately not inspected in this pass:

- any file named `potential-secrets`;
- raw evidence, credentials, vaults, case data, or provider artifacts;
- generated security-scan payload contents; and
- the contents or runtime behavior of ISO/build/USB scripts and Make targets.

No provider, agent, build, ISO, USB, system activation, or privileged command
was executed.

## Replacement map

| Predecessor lineage | Canonical destination or successor |
|---|---|
| Operator command language, interface doctrine, and orchestration boundaries | Endgame OS, Endgame Core, and Endgame Harness |
| Workstation presentation and Experience concepts | Project Monolith |
| Registry, fleet, discovery, and control-plane concepts | Project Forge (`project-forge-registry`) |
| Investigation, case, lawful OSINT, identity/geolocation/social-analysis concepts | Cerberus Case Workspace or a future explicitly lawful-OSINT successor |

These destinations are ownership mappings, not proof that the predecessor
material is suitable for migration.

## Classification

### Migrate candidate

Candidates are concepts to re-specify under the destination repository's
contracts. They are not approved code transfers.

| Candidate | Destination | Required gate before migration |
|---|---|---|
| A stable operator vocabulary and bounded command categories | Endgame OS | Compare with the versioned `eg` contract; import no unverified capability claim |
| Capability/provider separation and explicit failure handling | Endgame Core | Re-express as current descriptors/preflight evidence; no predecessor runtime reuse by default |
| Review, refusal, recovery, and audit discipline | Endgame Harness | Define a fixture-only authorization/review contract before any executor |
| Workstation/field presentation concepts | Project Monolith | Human UX review, asset provenance, and host-safe implementation ownership |
| Registry/agent inventory and technical status concepts | Project Forge | Fit the existing charter; do not add personal-planning or investigation authority |
| Agent role taxonomy useful to lawful investigations | Cerberus or future lawful-OSINT successor | Legal basis, privacy impact, data minimization, source terms, human review, and measurable non-harm requirements |

### Reference only

Retain these as predecessor archaeology unless a later review produces a
specific migration decision:

- `README.md`, `SECURITY.md`, and `docs/OBSIDIAN-COUNCIL.md` as records of the
  proposed product vision, not current capability evidence;
- `docs/CODE_REVIEW.md` as a dated technical critique;
- the Makefile, container/build scaffold, and ISO builder as evidence of the
  investigation-distro direction, never as a command to run from this ledger;
- the partial Obsidian Council Python tree as an early orchestration prototype;
- security workflow and report filenames as provenance leads whose contents
  require a separately authorized security review; and
- GitHub/Codeberg setup instructions as historical publication evidence.

### Reject / intentionally not migrated

- Claims of a complete, hardened, encrypted, court-ready, real-time, or
  production investigation platform without reproducible evidence.
- Performance and accuracy percentages without a documented dataset,
  methodology, evaluation, or provenance.
- Claims that stub agents, absent agents, missing packages, or broken imports
  are implemented capabilities.
- Root-only ISO construction and USB deployment as an Endgame OS operator path.
- Hard-coded integrations with obsolete or unpinned third-party SDK behavior.
- Automated surveillance, identity resolution, evidence handling, or law
  enforcement claims that bypass lawful authority and human review.
- Any secret, credential, raw evidence, case data, log, or scan payload as
  ordinary repository migration material.

### Requires legal/privacy/security review

| Material | Why review is required |
|---|---|
| `LICENSE` | Restricted-use, ownership, contact, redistribution, and authorized-user terms require legal confirmation before reuse |
| Social-media, face/identity, geolocation, surveillance, and vehicle-analysis concepts/code | High-risk privacy, consent, source-terms, discrimination, misuse, and jurisdiction questions |
| Evidence/chain-of-custody and court-admissibility claims | Must be designed and validated with qualified legal/evidence-handling authority |
| Security/encryption/authentication claims | Need a current threat model and independent implementation evidence |
| Security reports and generated scan outputs | Provenance, freshness, scope, and sensitive-content review are unknown |
| The excluded `potential-secrets` file | Must be handled only by an authorized security reviewer; never opened or migrated by this pass |
| Names, branding, contacts, and organizational claims | Ownership and present authority are unverified |

## Claim quarantine

All claims in the predecessor README, security policy, Obsidian Council guide,
and generated reports are quarantined as historical assertions unless a named
canonical successor independently verifies them. In particular, the documents
do not establish that thirteen functional agents, hardened OS controls,
encryption, automated chain of custody, court-ready output, continuous
monitoring, or stated response/accuracy levels exist.

The repository's own `docs/CODE_REVIEW.md` reports broken imports, missing build
paths, root-only assumptions, SDK misuse, non-functional stubs, missing
dependencies, and documentation drift. A future harvest must verify current
bytes independently; it must not treat that review as a complete security or
legal assessment either.

## Harvest decision record

No source, claim, asset, generated report, or configuration was copied to a
successor during this transaction. Every candidate remains pending a bounded,
destination-owned review. Rejection here means intentionally excluded from the
canonical lineage by default, not deletion from this preserved repository.
