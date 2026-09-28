# Repository Standards

This document is the authoritative list of standards every repository in this
workspace is expected to follow. New repositories created from
`theprawntemplate` inherit the baseline automatically; this file records what
that baseline is, what is required vs. optional, and the packaging pattern for
container repositories.

It exists so that humans and automation agents working across the fleet have a
single source of truth to conform to, rather than relying on implicit
per-repository conventions.

Last reviewed: 2026-09-27.

## Scope

Applies to all owned repositories (currently 79: 71 non-container, 7 container,
plus one history-managed repository). "Container repository" means a repository
that builds and publishes one or more container images to GitHub Container
Registry (GHCR, `ghcr.io`).

## 1. Security scanning (REQUIRED for every repo)

Every repository must carry these GitHub Actions workflows. They are present in
`theprawntemplate` and propagate to new repositories:

| Workflow | File | Purpose |
| --- | --- | --- |
| CodeQL | `.github/workflows/codeql.yml` | Static analysis / code scanning |
| Semgrep | `.github/workflows/semgrep.yml` | Pattern-based SAST |
| TruffleHog | `.github/workflows/trufflehog.yml` | Secret scanning |
| Dependency Review | `.github/workflows/dependency-review.yml` | Blocks vulnerable dependency changes in PRs |
| Scorecard | `.github/workflows/scorecard.yml` | OpenSSF supply-chain posture |
| LFS Guard | `.github/workflows/lfs-guard.yml` | Blocks accidental large/binary commits |

A repository is **security-compliant** when all six are present and enabled.

## 2. Automation and CI (REQUIRED)

- `.github/workflows/ci.yml` — project checks; adapt commands to the stack.
- `.github/dependabot.yml` + `.github/workflows/dependabot-auto-merge.yml` and
  `.github/workflows/auto-merge-bots.yml` — dependency updates with guarded
  auto-merge.
- `.github/workflows/labeler.yml`, `greetings.yml`, `heartbeat.yml`,
  `summary.yml` — repository hygiene and activity signals.
- `.github/workflows/deploy.yml` — deployment (or a clear statement that the
  repo is not deployed).

## 3. Governance and hygiene files (REQUIRED unless noted)

| File | Requirement |
| --- | --- |
| `LICENSE` | Required — Apache-2.0. |
| `NOTICE` | Required — accompanies Apache-2.0. |
| `SECURITY.md` | Required. Use GitHub private "Report a vulnerability"; never a personal email. |
| `CONTRIBUTING.md` | Required. |
| `AGENTS.md` | Required — instructions for automation agents. |
| `.github/dependabot.yml` | Required. |
| `.env.example` | Required **only when the project reads environment variables**. Repos with no env config legitimately omit it. |
| `.github/ISSUE_TEMPLATE/*`, `.github/pull_request_template.md` | Required. |
| `.gitignore`, `.gitattributes` | Required. |

## 4. Privacy and portability rules (REQUIRED)

These reflect the fleet-wide remediation sweep and must hold for every repo:

- **No secrets in git.** Use environment variables and `.env.example`. TruffleHog
  enforces this in CI; do not defeat it.
- **No personal contact details or private operator references** in tracked
  files (READMEs, SECURITY.md, configs, `.agents/`). Vulnerability reporting goes
  through GitHub's private channel, not a personal email.
- **Windows/Linux portability.** Launchers and paths must work on both; avoid
  hardcoded absolute paths and OS-specific-only launch scripts where a portable
  equivalent exists.
- **`.agents/` hygiene.** Never write secrets or personal details into
  `.agents/STATE.md` or `.agents/JOURNAL.md`.
- **PRs over direct commits to `main`.** Changes land through reviewed pull
  requests.

## 5. Container / GHCR packaging (REQUIRED for container repos; OPT-IN for others)

Container repositories publish images to `ghcr.io/<owner>/<repo>/<component>`.
The standard packaging pattern — verified present in all seven current container
repositories (musicstream, facetracker, FORGE, unifiedcollector, unifiedanalyzer,
ticketremaster-b, ctfsolver) — is:

| File | Purpose |
| --- | --- |
| `.github/workflows/docker-publish.yml` | Builds and pushes image(s) to GHCR on the release trigger. |
| `.github/scripts/ghcr-retention.cjs` | Prunes old GHCR package versions to control storage. |
| `Dockerfile` (and variants) | Image build definition(s). |

Opt-in scaffolding for these files lives under
[`.github/optional/`](.github/optional/) so a new repository can adopt the
packaging pattern by copying them into place rather than hand-rolling each time.
See [`.github/optional/README.md`](.github/optional/README.md) for enable steps.

**Package visibility:** package visibility (private vs public) is governed by the
organization's package-creation policy (Org Settings → Packages). Individual
container package visibility is a deliberate, per-package decision — especially
for privacy-sensitive images (photo/OSINT/security tooling) whose layers become
world-pullable when public.

## 6. Compliance status

A live compliance matrix across all owned repositories is maintained out-of-band
(see `repo-standards-compliance-matrix.md` in the workspace release artifacts).
As of the last review, 76/79 repositories carry the full security-workflow set;
the known exceptions are actively-developed repositories that have not yet
adopted the baseline. All seven container repositories carry the complete GHCR
pipeline.

## How to use this document

- **Creating a new repo:** start from `theprawntemplate`; you inherit sections
  1–4 automatically. If it will publish containers, adopt section 5 from
  `.github/optional/`.
- **Auditing an existing repo:** check it against sections 1–4 (all repos) and
  section 5 (container repos). Missing required items are compliance gaps to fix
  via a reviewed PR.
- **Agents:** treat this file as the conformance target for any repository work.
