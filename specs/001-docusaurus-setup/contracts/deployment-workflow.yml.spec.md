# GitHub Actions Deployment Workflow Specification

Date: 2025-11-28
Feature: 001-docusaurus-setup
Contract: deployment-workflow.yml

## Overview

This document specifies the contract for the GitHub Actions workflow that automates building and deploying the Docusaurus documentation site to GitHub Pages.

## Workflow File Location

`.github/workflows/deploy-docusaurus.yml`

## Trigger Conditions

### Primary Trigger
- **Event**: `push`
- **Branch**: `main`
- **Condition**: Any file changes in `book/` directory trigger deployment

### Manual Trigger
- **Event**: `workflow_dispatch`
- **Purpose**: Allow manual deployment initiation

## Inputs

None required (workflow uses repository context)

## Environment Requirements

### Runner
- **OS**: `ubuntu-latest`
- **Reason**: Consistent Linux environment, supports all Node.js operations

### Node.js Version
- **Version**: `20.x` (LTS)
- **Fallback**: `18.x` (also LTS)
- **Validation**: Specified in package.json engines field

### Permissions
- **contents**: `write` (required for pushing to gh-pages branch)
- **pages**: `write` (required for GitHub Pages deployment)
- **id-token**: `write` (required for deployment authentication)

## Workflow Steps

### Step 1: Checkout Repository
```yaml
- name: Checkout repository
  uses: actions/checkout@v4
  with:
    fetch-depth: 0                    # Full history for git info plugin
```

**Purpose**: Get repository code for building
**Success Criteria**: Repository code available in runner workspace
**Failure Handling**: Workflow stops, no notification (GitHub infrastructure issue)

### Step 2: Setup Node.js
```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'
    cache-dependency-path: book/package-lock.json
```

**Purpose**: Install Node.js environment for Docusaurus
**Success Criteria**: Node.js v20 installed, npm cache restored
**Failure Handling**: Workflow fails with error log

### Step 3: Install Dependencies
```yaml
- name: Install dependencies
  working-directory: ./book
  run: npm ci
```

**Purpose**: Install exact dependencies from package-lock.json
**Success Criteria**: All dependencies installed, exit code 0
**Failure Handling**:
- Capture stderr output
- Log dependency conflict errors (FR-013 compliance)
- Workflow fails with diagnostic information

### Step 4: Build Docusaurus Site
```yaml
- name: Build Docusaurus site
  working-directory: ./book
  run: npm run build
```

**Purpose**: Generate production-ready static files
**Success Criteria**:
- Build completes without errors
- `build/` directory created with static files
- Exit code 0

**Failure Handling** (FR-012 compliance):
- Capture full build logs
- Display error stack traces
- Workflow fails with detailed error output
- GitHub notifications sent to repository maintainers

### Step 5: Deploy to GitHub Pages
```yaml
- name: Deploy to GitHub Pages
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./book/build
    publish_branch: gh-pages
    user_name: 'github-actions[bot]'
    user_email: 'github-actions[bot]@users.noreply.github.com'
```

**Purpose**: Deploy built site to gh-pages branch
**Success Criteria**:
- Static files pushed to gh-pages branch
- GitHub Pages updated
- Deployment URL accessible

**Failure Handling** (FR-012 compliance):
- Log deployment errors
- Provide commit SHA and error details
- Workflow fails visibly in Actions tab
- Email notifications sent to repository watchers

## Outputs

### Deployment URL
- **Value**: `https://[username].github.io/[repo-name]/`
- **Availability**: Displayed in workflow summary after successful deployment

### Deployment Status
- **Values**: `success | failure | cancelled`
- **Visibility**: GitHub Actions tab, status badges, commit status

### Build Artifacts
- **Location**: gh-pages branch
- **Contents**: Complete static site in branch root
- **Retention**: Permanent until overwritten by next deployment

## Error Handling Contract (FR-012)

### On Build Failure
1. Workflow status: **Failed**
2. Error logs: Visible in "Build Docusaurus site" step
3. Notifications: GitHub sends email to repository maintainers
4. Deployment: Does NOT proceed (fail-fast)

### On Deployment Failure
1. Workflow status: **Failed**
2. Error logs: Visible in "Deploy to GitHub Pages" step
3. Notifications: GitHub sends email to repository maintainers
4. Site status: Previous deployment remains live (no downtime)

### Error Log Format
```
Error: [Error type]
Step: [Failed step name]
Command: [Exact command that failed]
Exit code: [Non-zero exit code]
Error output: [stderr content]
Stack trace: [If available]
```

## Performance Expectations

### Timing Constraints (from SC-004)
- **Total workflow duration**: <5 minutes
- **Breakdown**:
  - Checkout: <30 seconds
  - Node.js setup: <1 minute (with cache)
  - Dependency install: <2 minutes
  - Build: <1 minute
  - Deploy: <1 minute

### Resource Limits
- **Memory**: Default GitHub Actions runner (7 GB)
- **Disk**: Sufficient for node_modules and build artifacts
- **Network**: Unlimited (GitHub's infrastructure)

## Notification Contract

### Success Notifications
- **Recipient**: None (silent success)
- **Visibility**: Green checkmark in Actions tab and commit status

### Failure Notifications (FR-012)
- **Recipients**: Repository maintainers and watchers (GitHub email)
- **Content**: Workflow name, failed step, error snippet
- **Timing**: Immediate upon workflow failure
- **Format**: GitHub's standard notification email

## Security Considerations

### Token Usage
- **GITHUB_TOKEN**: Auto-provided by GitHub Actions
- **Scope**: Repository-scoped, expires after workflow
- **Permissions**: contents:write for deployment

### Branch Protection
- **gh-pages branch**: Auto-created, no direct commits
- **Source branch (main)**: Protected per repository settings

### Secrets
- **Required**: None (public repository deployment)
- **Optional**: Custom deployment tokens (if private repo)

## Validation Requirements

### Pre-Deployment Checks
1. ✅ Node.js version >= 18
2. ✅ package-lock.json exists
3. ✅ build/ directory created successfully
4. ✅ No build errors or warnings

### Post-Deployment Checks
1. ✅ gh-pages branch updated
2. ✅ Deployment commit includes all static files
3. ✅ GitHub Pages site accessible
4. ✅ Site content matches build output

## Integration Points

### GitHub Pages Settings
- **Source**: gh-pages branch, root directory
- **Custom domain**: Not configured (out of scope)
- **HTTPS**: Enforced (GitHub Pages default)

### Repository Settings
- **Actions**: Must be enabled
- **Pages**: Must be enabled
- **Permissions**: Actions must have write access to repository

## Workflow Maintenance

### Version Pinning
- **actions/checkout**: v4 (major version pinned)
- **actions/setup-node**: v4 (major version pinned)
- **peaceiris/actions-gh-pages**: v3 (major version pinned)

### Update Strategy
- Monitor for security advisories
- Update to latest minor/patch versions quarterly
- Test in development branch before merging to main

## Success Criteria Mapping

This workflow contract directly supports:
- **SC-004**: Changes deployed within 5 minutes
- **SC-006**: First-attempt success (automated, no manual intervention)
- **FR-005**: GitHub Pages deployment using GitHub Actions
- **FR-006**: Build to static HTML/CSS/JS files
- **FR-007**: Serve from gh-pages branch
- **FR-012**: Detailed error logs and notifications

## Example Workflow Run

### Successful Run
```
✓ Checkout repository (15s)
✓ Setup Node.js (45s)
✓ Install dependencies (90s)
✓ Build Docusaurus site (60s)
✓ Deploy to GitHub Pages (30s)
Total: 4 minutes

Deployment URL: https://username.github.io/ai-native-book/
```

### Failed Run (Build Error)
```
✓ Checkout repository (15s)
✓ Setup Node.js (45s)
✓ Install dependencies (90s)
✗ Build Docusaurus site (30s)
  Error: Module not found: Error: Can't resolve './missing-file'
  Exit code: 1

Workflow failed. Notifications sent to repository maintainers.
Previous deployment remains live.
```
