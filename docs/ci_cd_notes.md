# CI/CD Notes — GitHub Actions vs Jenkins

## Overview

Both GitHub Actions and Jenkins are CI/CD tools that automate the
build → test → report pipeline. The right choice depends on team
size, infrastructure ownership, and project complexity.

---

## GitHub Actions

**Type:** Cloud-hosted, SaaS  
**Config format:** YAML (`.github/workflows/*.yml`)  
**Runs on:** GitHub-managed runners (or self-hosted)

### Strengths
- Zero infrastructure to manage — GitHub handles the runners
- Native integration with GitHub PRs, branches, and secrets
- Marketplace has thousands of pre-built actions
- Free tier is generous for public repos
- YAML config is simple and readable for small pipelines

### Weaknesses
- Tightly coupled to GitHub — migrating away is painful
- Less flexible for complex enterprise pipelines
- Self-hosted runners require extra setup if needed
- Limited build history and audit controls out of the box

### When to choose GitHub Actions
- Open-source or startup projects already on GitHub
- Small-to-medium teams who want CI without infrastructure burden
- Projects where GitHub is the single source of truth

---

## Jenkins

**Type:** Self-hosted, open-source  
**Config format:** Groovy (`Jenkinsfile` — declarative or scripted)  
**Runs on:** Your own servers or VMs

### Strengths
- Fully customizable — plugins for almost everything
- Runs behind a corporate firewall (critical for regulated industries)
- Rich plugin ecosystem: Allure, SonarQube, Slack, Docker, etc.
- Fine-grained access control and audit logging
- Supports complex multi-branch and multi-repo pipelines

### Weaknesses
- Requires dedicated infrastructure and maintenance
- Steeper learning curve (Groovy DSL, plugin management)
- UI is dated; plugin version conflicts are a known pain point
- Higher operational overhead for small teams

### When to choose Jenkins
- Enterprise environments with strict security/compliance needs
- Teams running tests on on-premise hardware or private networks
- Complex pipelines with many integrations (JIRA, Artifactory, etc.)
- Organisations already invested in Jenkins infrastructure

---

## Quick Comparison Table

| Dimension             | GitHub Actions          | Jenkins                     |
|-----------------------|-------------------------|-----------------------------|
| Hosting               | Cloud (GitHub)          | Self-hosted                 |
| Config language       | YAML                    | Groovy (Jenkinsfile)        |
| Setup effort          | Low                     | High                        |
| Customisability       | Moderate                | Very high                   |
| Plugin ecosystem      | GitHub Marketplace      | Jenkins Plugin Index        |
| Cost                  | Free tier + usage-based | Free (infra cost only)      |
| Best for              | OSS / small teams       | Enterprise / regulated envs |
| GitHub integration    | Native                  | Via plugin                  |
| Firewall / on-prem    | Requires self-hosted    | Native                      |

---

## How This Project Uses CI

This framework targets Jenkins as the primary CI pipeline definition
(`Jenkinsfile` at repo root) with five stages:

1. **Checkout** — pulls the latest code from SCM
2. **Install Dependencies** — creates a venv and installs from `pyproject.toml`
   via `pip install -e ".[dev]"`, then installs the Playwright browser binary
3. **Run API Tests** — executes `tests/api/` with Allure result generation
4. **Run UI Tests** — executes `tests/ui/` in headless Chromium with Allure result generation
5. **Publish Report** — renders the combined Allure HTML report via the
   Allure Jenkins Plugin and archives per-test artifacts (screenshots, traces, logs).
   Raw results are written to `allure-results/` at the repo root.

GitHub Actions would be the natural choice for this project if it were
open-source, since the repo already lives on GitHub. Jenkins is used here
to demonstrate enterprise-grade CI knowledge relevant to SDET roles.