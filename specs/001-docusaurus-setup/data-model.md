# Data Model: Docusaurus Configuration

Date: 2025-11-28
Feature: 001-docusaurus-setup

## Overview
This document defines the data structures, configuration schemas, and build artifacts for the Docusaurus documentation site.

## 1. Docusaurus Configuration Schema (docusaurus.config.js)

### Site Metadata
```javascript
{
  title: string,              // "AI Native Development"
  tagline: string,            // Brief project description
  favicon: string,            // Path to favicon (default: img/favicon.ico)
  url: string,                // https://[username].github.io
  baseUrl: string,            // /ai-native-book/
  organizationName: string,   // GitHub username/organization
  projectName: string,        // Repository name
  onBrokenLinks: 'throw',     // Fail build on broken links
  onBrokenMarkdownLinks: 'warn'
}
```

### Deployment Configuration
```javascript
{
  deploymentBranch: 'gh-pages',
  trailingSlash: false
}
```

### Theme Configuration
```javascript
{
  navbar: {
    title: string,
    logo: {
      alt: string,
      src: string              // Path to logo image
    },
    items: Array<NavbarItem>
  },
  footer: {
    style: 'dark' | 'light',
    links: Array<FooterLinkColumn>,
    copyright: string
  },
  prism: {
    theme: PrismTheme,
    darkTheme: PrismTheme
  }
}
```

## 2. Package Configuration (package.json)

### Essential Fields
```json
{
  "name": "ai-native-development-docs",
  "version": "0.0.0",
  "private": true,
  "engines": {
    "node": ">=18.0.0"
  },
  "scripts": {
    "docusaurus": "docusaurus",
    "start": "docusaurus start",
    "build": "docusaurus build",
    "swizzle": "docusaurus swizzle",
    "deploy": "docusaurus deploy",
    "clear": "docusaurus clear",
    "serve": "docusaurus serve",
    "write-translations": "docusaurus write-translations",
    "write-heading-ids": "docusaurus write-heading-ids"
  },
  "dependencies": {
    "@docusaurus/core": "^3.0.0",
    "@docusaurus/preset-classic": "^3.0.0",
    "@mdx-js/react": "^3.0.0",
    "clsx": "^2.0.0",
    "prism-react-renderer": "^2.1.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  },
  "devDependencies": {
    "@docusaurus/module-type-aliases": "^3.0.0",
    "@docusaurus/types": "^3.0.0"
  },
  "browserslist": {
    "production": [">0.5%", "not dead", "not op_mini all"],
    "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
  }
}
```

## 3. Sidebar Configuration (sidebars.js)

### Structure
```javascript
{
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Getting Started',
      items: ['intro', 'tutorial-basics/create-a-page']
    }
  ]
}
```

## 4. Build Artifacts

### Build Directory Structure
```
build/
├── index.html               # Homepage
├── docs/                    # Documentation pages
├── blog/                    # Blog pages (if enabled)
├── assets/
│   ├── css/                 # Compiled CSS
│   ├── js/                  # Compiled JavaScript bundles
│   └── images/              # Optimized images
├── img/                     # Static images
└── sitemap.xml              # Auto-generated sitemap
```

### Artifact Characteristics
- Static HTML files (server-side rendered)
- Minified CSS and JavaScript
- Code-split bundles for performance
- Pre-rendered React components
- SEO-optimized meta tags

## 5. Content Structure

### Documentation Files (docs/)
```
docs/
├── intro.md                 # Introduction page
└── tutorial-basics/
    ├── create-a-page.md
    ├── create-a-document.md
    ├── markdown-features.md
    └── deploy-your-site.md
```

### Front Matter Schema
```yaml
---
id: string                   # Unique identifier
title: string                # Page title
sidebar_label: string        # Label in sidebar
sidebar_position: number     # Order in sidebar
description: string          # Meta description
keywords: [string]           # SEO keywords
---
```

## 6. GitHub Actions Workflow Data

### Workflow Triggers
```yaml
on:
  push:
    branches: [main]
  workflow_dispatch:          # Manual trigger
```

### Build Environment
```yaml
runs-on: ubuntu-latest
node-version: '20'           # LTS version
```

### Deployment Output
```yaml
github_pages_deployment:
  branch: gh-pages
  url: https://[username].github.io/[repo-name]
  commit_sha: string
  deployment_status: success | failure
```

## 7. Error Data Structures

### Pre-Setup Validation Error (FR-011)
```javascript
{
  error_code: 'FOLDER_EXISTS',
  message: 'The \'book\' folder already contains files.',
  resolution: 'Please move or remove existing content before running setup.',
  folder_path: string,
  file_count: number
}
```

### Dependency Conflict Error (FR-013)
```javascript
{
  error_code: 'DEPENDENCY_CONFLICT',
  message: 'npm dependency installation failed due to version conflicts',
  conflicting_packages: [
    {
      name: string,
      required_version: string,
      installed_version: string,
      conflicted_by: string
    }
  ],
  resolution_suggestions: [string]
}
```

### Deployment Failure Data (FR-012)
```javascript
{
  error_code: 'DEPLOYMENT_FAILED',
  workflow_run_id: string,
  step_failed: string,
  error_logs: string,
  timestamp: ISO8601,
  notification_sent: boolean
}
```

## 8. State Transitions

### Setup States
```
PENDING → VALIDATING → INSTALLING → CONFIGURING → BUILDING → COMPLETED
                ↓           ↓            ↓            ↓
              ERROR       ERROR        ERROR        ERROR
```

### Deployment States
```
IDLE → TRIGGERED → BUILDING → DEPLOYING → DEPLOYED
         ↓            ↓           ↓
       FAILED       FAILED      FAILED
```

## Summary

This data model defines all configuration schemas, build artifacts, error structures, and state transitions for the Docusaurus documentation site setup. All structures align with official Docusaurus conventions and the feature requirements (FR-001 through FR-013).
