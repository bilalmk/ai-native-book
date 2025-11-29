# Quickstart Guide: Docusaurus Documentation Site

Date: 2025-11-28
Feature: 001-docusaurus-setup

## Overview

This guide provides step-by-step instructions for setting up the Docusaurus documentation site locally, building it, and deploying it to GitHub Pages.

## Prerequisites

Before starting, ensure you have:

### Required Software
- **Node.js**: v18.0.0 or higher (LTS recommended: v18.x or v20.x)
  - Download: https://nodejs.org/
  - Verify: `node --version`
- **npm**: v8.0.0 or higher (bundled with Node.js)
  - Verify: `npm --version`
- **Git**: Latest version
  - Verify: `git --version`

### Repository Access
- GitHub repository with write access
- GitHub Actions enabled on the repository
- GitHub Pages enabled in repository settings

### Environment Check
Run these commands to verify your environment:
```bash
node --version    # Should show v18.x or v20.x
npm --version     # Should show v8.x or higher
git --version     # Should show git version 2.x or higher
```

## Initial Setup

### Step 1: Clone Repository (If Not Already)
```bash
git clone https://github.com/[username]/ai-native-book.git
cd ai-native-book
```

### Step 2: Verify `book/` Folder Does Not Exist
```bash
# On Windows (PowerShell)
Test-Path book

# On macOS/Linux
ls book
```

**Expected result**: Folder should not exist or should be empty
**If folder exists with content**: See "Troubleshooting" section below

### Step 3: Initialize Docusaurus Project
```bash
npx create-docusaurus@latest book classic --typescript
```

**What this does**:
- Creates `book/` directory
- Installs Docusaurus v3.x and dependencies
- Scaffolds classic template with TypeScript support
- Sets up package.json and configuration files

**Expected output**:
```
Creating new Docusaurus project...
✔ Created book/package.json
✔ Created book/docusaurus.config.js
✔ Installing dependencies with npm...
✔ Success! Created book at /path/to/ai-native-book/book
```

**Duration**: 2-5 minutes depending on internet speed

### Step 4: Navigate to Book Directory
```bash
cd book
```

### Step 5: Configure Site Metadata
Edit `docusaurus.config.js`:

```javascript
module.exports = {
  title: 'AI Native Development',
  tagline: 'Comprehensive guide to Physical AI & Humanoid Robotics',
  favicon: 'img/favicon.ico',

  // GitHub Pages deployment config
  url: 'https://[your-username].github.io',
  baseUrl: '/ai-native-book/',
  organizationName: '[your-username]',
  projectName: 'ai-native-book',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Deployment configuration
  deploymentBranch: 'gh-pages',
  trailingSlash: false,

  // ... rest of configuration
};
```

**Important**: Replace `[your-username]` with your actual GitHub username

## Local Development

### Start Development Server
```bash
npm run start
```

**What this does**:
- Starts local development server
- Opens browser to http://localhost:3000
- Enables hot reload for content changes

**Expected output**:
```
[INFO] Starting the development server...
[SUCCESS] Docusaurus website is running at http://localhost:3000/
```

**Success criteria** (SC-001): Server starts in under 2 minutes

### Make Content Changes
1. Edit files in `docs/` directory
2. Save changes
3. Browser automatically reloads
4. Verify changes appear correctly

### Stop Development Server
Press `Ctrl+C` in the terminal

## Production Build

### Build Static Site
```bash
npm run build
```

**What this does**:
- Compiles all content to static HTML/CSS/JS
- Creates `build/` directory with optimized files
- Validates all links and references

**Expected output**:
```
[INFO] Creating an optimized production build...
[SUCCESS] Generated static files in build/
[INFO] Use `npm run serve` to test your build locally.
```

**Success criteria** (SC-002): Build completes without errors

**Duration**: 1-2 minutes

### Test Production Build Locally
```bash
npm run serve
```

**What this does**:
- Serves production build from `build/` directory
- Opens browser to http://localhost:3000
- Simulates production environment

**Use this to**: Verify production build before deploying

## GitHub Pages Deployment

### Automated Deployment (Recommended)

#### Step 1: Create GitHub Actions Workflow
Create file `.github/workflows/deploy-docusaurus.yml`:

```yaml
name: Deploy Docusaurus to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: write
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: book/package-lock.json

      - name: Install dependencies
        working-directory: ./book
        run: npm ci

      - name: Build Docusaurus site
        working-directory: ./book
        run: npm run build

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./book/build
          publish_branch: gh-pages
          user_name: 'github-actions[bot]'
          user_email: 'github-actions[bot]@users.noreply.github.com'
```

#### Step 2: Commit and Push
```bash
git add .github/workflows/deploy-docusaurus.yml
git add book/
git commit -m "feat: Add Docusaurus setup with GitHub Pages deployment"
git push origin main
```

#### Step 3: Monitor Deployment
1. Go to repository on GitHub
2. Click "Actions" tab
3. Watch workflow run progress
4. Verify deployment succeeds

**Success criteria** (SC-004): Deployment completes within 5 minutes

#### Step 4: Configure GitHub Pages
1. Go to repository Settings
2. Navigate to Pages section
3. Source: Select "gh-pages" branch, "/ (root)" folder
4. Click Save

#### Step 5: Access Deployed Site
Visit: `https://[your-username].github.io/ai-native-book/`

**Success criteria** (SC-003): Site loads within 3 seconds

### Manual Deployment (Not Recommended)

If you need to deploy manually:

```bash
GIT_USER=[your-username] npm run deploy
```

**Note**: This requires GIT_USER environment variable and direct git access

## Common Development Tasks

### Add New Documentation Page
1. Create file in `docs/`: `docs/new-page.md`
2. Add front matter:
   ```markdown
   ---
   id: new-page
   title: New Page Title
   sidebar_position: 3
   ---

   # New Page Content
   ```
3. Page automatically appears in sidebar
4. Test with `npm run start`

### Update Site Configuration
1. Edit `docusaurus.config.js`
2. Restart development server
3. Verify changes

### Clear Cache
```bash
npm run clear
```

Use when: Experiencing build issues or stale content

## Troubleshooting

### Problem: `book/` Folder Already Exists with Content

**Error message**:
```
Error: The 'book' folder already contains files.
Please move or remove existing content before running setup.
```

**Solution**:
1. Backup existing content: `mv book book.backup`
2. Run setup again: `npx create-docusaurus@latest book classic --typescript`
3. Restore needed content after setup

### Problem: Node.js Version Too Old

**Error message**:
```
Error: This package requires Node.js version >=18.0.0
```

**Solution**:
1. Install Node.js v18 or v20 LTS from https://nodejs.org/
2. Verify version: `node --version`
3. Retry setup

### Problem: Dependency Installation Fails

**Error message**:
```
npm ERR! code ERESOLVE
npm ERR! ERESOLVE unable to resolve dependency tree
```

**Solution**:
1. Clear npm cache: `npm cache clean --force`
2. Delete `node_modules` and `package-lock.json`: `rm -rf node_modules package-lock.json`
3. Reinstall: `npm install`

**Alternative**: Try with legacy peer deps: `npm install --legacy-peer-deps`

### Problem: Build Fails with Module Not Found

**Error message**:
```
Module not found: Error: Can't resolve './ComponentName'
```

**Solution**:
1. Check file path and import statement
2. Verify file exists: `ls docs/path/to/file.md`
3. Clear cache: `npm run clear`
4. Rebuild: `npm run build`

### Problem: GitHub Pages Not Updating

**Symptoms**: Deployment succeeds but site shows old content

**Solution**:
1. Check GitHub Actions workflow completed successfully
2. Verify gh-pages branch has latest commit
3. Clear browser cache (Ctrl+Shift+R)
4. Wait 2-3 minutes for CDN propagation
5. Check GitHub Pages settings (Settings > Pages)

### Problem: Deployment Workflow Fails

**Error**: Check specific step that failed in Actions tab

**Common causes and solutions**:
- **Checkout fails**: Repository access issue, check permissions
- **Node.js setup fails**: Infrastructure issue, retry workflow
- **Dependency install fails**: See "Dependency Installation Fails" above
- **Build fails**: Check build logs, fix content errors
- **Deploy fails**: Check repository permissions (Settings > Actions > General > Workflow permissions > Read and write permissions)

## Performance Validation

### Development Server Startup (SC-001)
```bash
time npm run start
```

**Target**: <2 minutes after dependencies installed

### Production Build Time
```bash
time npm run build
```

**Target**: <5 minutes

### Deployed Site Load Time
1. Open browser DevTools (F12)
2. Go to Network tab
3. Visit site URL
4. Check "Finish" time

**Target** (SC-003): <3 seconds

### Deployment Duration (SC-004)
1. Go to Actions tab
2. Click latest workflow run
3. Check total duration

**Target**: <5 minutes

## Next Steps

After successful setup:

1. **Customize Content**: Edit files in `docs/` directory
2. **Add Features**: Explore Docusaurus plugins (search, analytics, etc.)
3. **Customize Theme**: Modify `src/css/custom.css`
4. **Configure Navigation**: Update `sidebars.js`
5. **Add Blog**: Use `blog/` directory
6. **Review Documentation**: https://docusaurus.io/docs

## Additional Resources

- **Docusaurus Documentation**: https://docusaurus.io/docs
- **GitHub Pages Documentation**: https://docs.github.com/en/pages
- **Node.js LTS Releases**: https://nodejs.org/en/about/releases/
- **Troubleshooting Guide**: https://docusaurus.io/docs/troubleshooting

## Summary

You should now have:
- ✅ Docusaurus project in `book/` folder
- ✅ Local development server running
- ✅ Production build verified
- ✅ GitHub Actions workflow configured
- ✅ Site deployed to GitHub Pages

Congratulations! Your Docusaurus documentation site is now live.
