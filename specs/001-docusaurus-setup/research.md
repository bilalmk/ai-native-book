# Research: Docusaurus Documentation Site Setup

**Date:** 2025-11-29
**Feature:** 001-docusaurus-setup

## Overview

This research document consolidates findings for implementing a Docusaurus documentation site within the book/ folder with automated GitHub Pages deployment.

## 1. Docusaurus Setup Methods

### Decision: Use npx create-docusaurus@latest

**Rationale:**
- Official Docusaurus CLI tool maintained by Facebook/Meta
- Ensures correct dependency versions and configurations
- Automatically scaffolds proper project structure
- Reduces setup errors compared to manual configuration
- Well-documented and widely adopted

**Command:**
```bash
npx create-docusaurus@latest book classic --typescript
```

**Options:**
- `book`: Target directory name
- `classic`: Template choice (recommended starter)
- `--typescript`: Enable TypeScript support (optional but recommended)

**Alternatives Considered:**
- Manual setup: Rejected - error-prone, requires deep knowledge of all dependencies
- Forking existing project: Rejected - may include unwanted customizations
- Using older npx @docusaurus/init: Rejected - deprecated approach

**References:**
- Official docs: https://docusaurus.io/docs/installation
- Best practices: Use latest stable version

## 2. Docusaurus Version Selection

### Decision: Docusaurus v3.x (Latest Stable)

**Rationale:**
- Current production-ready version as of 2025
- Active development and security updates
- Improved performance over v2.x
- Modern React 18 support
- Better TypeScript integration
- Latest documentation and community support

**Version Specification:**
- Use @latest tag for automatic latest stable
- Lock version in package.json after installation
- Monitor for security updates

**Alternatives Considered:**
- Docusaurus v2.x: Rejected - approaching end-of-life, missing performance improvements
- Beta/canary versions: Rejected - not production-ready, may have breaking changes
- Version pinning to specific minor: Accepted for production stability

**Migration Path (if needed):**
- v2 to v3 migration guide available
- Breaking changes documented
- Automated migration tools provided

## 3. GitHub Pages Deployment Strategy

### Decision: GitHub Actions with Official Docusaurus Action

**Rationale:**
- Fully automated CI/CD pipeline
- No manual intervention required (meets SC-006)
- Official support from Docusaurus team
- Handles build artifacts and deployment automatically
- Integrated error reporting and notifications
- Free for public repositories

**Workflow Approach:**
1. Trigger on push to main branch
2. Checkout repository code
3. Setup Node.js environment (v18 or v20 LTS)
4. Install dependencies (npm ci)
5. Build Docusaurus site (npm run build)
6. Deploy to GitHub Pages (gh-pages branch)

**GitHub Pages Configuration:**
- Source: gh-pages branch (auto-created by workflow)
- Base URL: /repository-name/ (for project pages)
- CNAME: Not required for *.github.io domain

**Alternatives Considered:**
- Manual deployment via npm run deploy: Rejected - violates SC-006 (no manual intervention)
- Netlify/Vercel: Rejected - adds external dependency, GitHub Pages specified in constitution
- GitHub Pages from docs/ folder: Rejected - doesn't support build process

**Security Considerations:**
- Use GITHUB_TOKEN for authentication (auto-provided)
- No secrets required for public repos
- Workflow permissions: contents: write for deployment

## 4. Package Manager Choice

### Decision: npm (Default Node.js Package Manager)

**Rationale:**
- Bundled with Node.js (no additional installation)
- Widely supported across all platforms
- package-lock.json provides dependency locking
- Standard for JavaScript ecosystem
- Docusaurus officially supports npm

**Best Practices:**
- Use `npm ci` in CI/CD for reproducible builds
- Use `npm install` for local development
- Commit package-lock.json to repository
- Specify Node.js version in package.json engines field

**Alternatives Considered:**
- yarn: Accepted as alternative - faster, better workspace support
- pnpm: Accepted as alternative - disk space efficient
- Decision: Use npm as default, document yarn/pnpm as acceptable alternatives

**Dependency Management:**
- Lock file (package-lock.json) ensures reproducible builds
- Regular security audits: npm audit
- Update strategy: Minor/patch updates regularly, major updates with testing

## 5. Error Handling Strategy

### Decision: Fail-Fast with Diagnostic Messages

**Rationale:**
- Aligns with clarified requirements (FR-011, FR-012, FR-013)
- Prevents data loss (e.g., existing book/ folder)
- Provides actionable error messages
- Enables quick issue resolution
- Transparent failure modes

**Implementation Approach:**

**Pre-Setup Validation (FR-011):**
- Check if book/ folder exists
- If exists and not empty: Abort with error message
- Error message format: "Error: The 'book' folder already contains files. Please move or remove existing content before running setup."

**Dependency Installation (FR-013):**
- Capture npm install stderr
- Detect version conflict patterns
- Parse conflicting package names
- Display diagnostic information
- Suggest resolutions (update Node.js, clear cache, check package versions)

**Deployment Failures (FR-012):**
- GitHub Actions workflow failure
- Detailed logs in Actions tab
- Email notifications to repository maintainers
- Status badges show deployment state

**Error Message Guidelines:**
1. Clear description of what went wrong
2. Context about where error occurred
3. Specific action user should take
4. Link to troubleshooting documentation

**Alternatives Considered:**
- Auto-recovery (backup and proceed): Rejected - could hide issues, data loss risk
- Silent failures with logging: Rejected - violates transparency requirement
- Interactive prompts: Rejected - doesn't work in CI/CD

## 6. Site Configuration Approach

### Decision: Minimal Initial Setup, Extensible Later

**Rationale:**
- Custom theme development out of scope (spec line 143)
- Extensive styling out of scope (spec line 143)
- Focus on functional deployment first
- Default theme provides professional appearance
- Easy to customize incrementally

**Initial Configuration Items:**

1. **Site metadata (docusaurus.config.js):**
   - title: "AI Native Development"
   - tagline: Brief project description
   - url: https://[username].github.io
   - baseUrl: /ai-native-book/
   - organizationName: GitHub username
   - projectName: Repository name

2. **Deployment settings:**
   - deploymentBranch: gh-pages
   - trailingSlash: false

3. **Theme config:**
   - navbar: Title and basic navigation
   - footer: Copyright and links
   - Default color mode: light/dark toggle

4. **Plugins:**
   - Default plugins only (docs, blog, pages, sitemap)

**Out of Scope for Initial Setup:**
- Custom theme development
- Analytics integration
- Search functionality customization
- Multi-language support
- API documentation generation
- SEO optimization beyond defaults

**Future Customization Path:**
- Theme customization via src/css/custom.css
- Plugin additions as needed
- Navigation structure refinement
- Content organization improvements

## 7. Testing Strategy

### Decision: Multi-Layer Verification

**Rationale:**
- Ensures quality at each stage
- Catches issues early
- Validates both build and deployment
- Aligns with success criteria

**Testing Layers:**

**1. Local Development Testing:**
- `npm run start` - Verify dev server works
- Check http://localhost:3000 loads
- Validate navigation works
- Test hot reload functionality

**2. Production Build Testing:**
- `npm run build` - Ensure build completes
- Check build/ directory created
- Verify no errors or warnings
- Test built files serve correctly

**3. Deployment Testing:**
- Push to trigger GitHub Actions
- Monitor workflow execution
- Check deployment success
- Verify site accessible at GitHub Pages URL
- Test deployed site functionality

**4. Browser Compatibility Testing:**
- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest 2 versions)

**Success Criteria Validation:**
- SC-001: Dev server starts <2min (measure with time command)
- SC-002: Build completes without errors (exit code 0)
- SC-003: Site loads <3sec (use browser DevTools Network tab)
- SC-004: Deployment completes <5min (GitHub Actions duration)
- SC-005: Cross-browser functionality (manual testing)
- SC-006: First-attempt success (no manual fixes required)

## 8. Documentation Requirements

### Decision: Comprehensive README with Quick start Guide

**Rationale:**
- FR-010: Must include setup and deployment instructions
- Enables team members to work independently
- Reduces support overhead
- Standard practice for documentation projects

**Documentation Deliverables:**

**1. book/README.md:**
- Project overview
- Prerequisites (Node.js version, tools)
- Installation steps
- Local development commands
- Build and deployment commands
- Troubleshooting section
- Configuration customization guide

**2. quickstart.md (in specs/):**
- Step-by-step setup guide
- Common issues and solutions
- Links to official Docusaurus docs

**3. Inline Comments:**
- docusaurus.config.js: Explain key settings
- GitHub Actions workflow: Document each step

**Command Documentation:**
```bash
# Install dependencies
npm install

# Start local development server
npm run start

# Build for production
npm run build

# Serve production build locally (testing)
npm run serve

# Deploy to GitHub Pages (manual, if needed)
npm run deploy
```

**Troubleshooting Sections:**
- Node.js version issues
- Dependency conflicts
- Build failures
- Deployment errors
- GitHub Pages not updating

## 9. Repository Integration

### Decision: Isolated book/ Folder with Minimal External Changes

**Rationale:**
- FR-008: Preserve existing repository structure
- Minimizes risk of conflicts
- Clear separation of concerns
- Easy to understand and maintain

**Integration Points:**

**1. New Directories:**
- `book/`: Complete Docusaurus project
- `book/.gitignore`: Docusaurus-specific ignores

**2. Modified Files:**
- `.github/workflows/deploy-docusaurus.yml`: New workflow file
- `.gitignore`: Add book/node_modules, book/build, book/.docusaurus (if not in book/.gitignore)

**3. Preserved Files:**
- All existing project files unchanged
- `.specify/` framework untouched
- `specs/` directory continues to function
- `history/` records preserved

**Git Workflow:**
- Commit book/ folder initialization
- Commit GitHub Actions workflow separately
- Clear commit messages referencing FR numbers
- Verify no unintended file changes

## 10. Best Practices Summary

### Docusaurus Official Recommendations

**1. Project Structure:**
- Use standard folder layout (docs/, blog/, src/)
- Keep configuration in docusaurus.config.js
- Use sidebars.js for navigation structure

**2. Content Organization:**
- Use Markdown for documentation
- Front matter for metadata
- Consistent file naming (kebab-case)

**3. Performance:**
- Lazy load images
- Optimize static assets
- Use production build for deployment

**4. Accessibility:**
- Semantic HTML from default theme
- Keyboard navigation support
- ARIA labels on interactive elements

**5. SEO:**
- Meta descriptions in front matter
- Proper heading hierarchy
- Sitemap auto-generation

**6. Deployment:**
- Always use production build (npm run build)
- Test locally before deploying
- Monitor deployment logs

## 11. Risk Mitigation Strategies

### Key Risks and Mitigations

**1. Node.js Version Incompatibility:**
- Risk: Docusaurus requires Node.js v18+
- Mitigation: Document version requirement, use engines field in package.json
- Validation: Add Node.js version check to setup script

**2. Dependency Conflicts:**
- Risk: npm install may fail with version conflicts
- Mitigation: FR-013 error handling, use package-lock.json
- Resolution: Clear instructions for updating Node.js or clearing npm cache

**3. GitHub Pages Deployment Failure:**
- Risk: Workflow may fail due to permissions or configuration
- Mitigation: FR-012 detailed error logs and notifications
- Prevention: Test workflow in development branch first

**4. Existing book/ Folder:**
- Risk: User may have existing book/ folder with content
- Mitigation: FR-011 pre-validation check, fail-safe abort
- Communication: Clear error message with resolution steps

**5. Build Errors:**
- Risk: Production build may fail with errors/warnings
- Mitigation: Local build testing before deployment
- Monitoring: GitHub Actions logs capture all build output

## 12. Implementation Timeline

### Recommended Phased Approach

**Phase 1: Core Setup (P1 - Highest Priority)**
- Validate environment (check Node.js, book/ folder)
- Run Docusaurus initialization
- Configure basic site metadata
- Test local development server
- Success: Dev server runs successfully

**Phase 2: Deployment Configuration (P2)**
- Create GitHub Actions workflow
- Configure GitHub Pages settings
- Test deployment to gh-pages branch
- Verify deployed site accessibility
- Success: Automated deployment working

**Phase 3: Documentation & Verification (P3)**
- Write book/README.md
- Update quickstart.md
- Create troubleshooting guide
- Verify all success criteria
- Success: Complete documentation, all tests pass

## Summary of Key Decisions

| Decision Area | Choice | Primary Rationale |
|---------------|--------|-------------------|
| Setup Method | npx create-docusaurus@latest | Official, maintained, correct dependencies |
| Version | Docusaurus v3.x | Latest stable, active support |
| Deployment | GitHub Actions | Automated, no manual intervention |
| Package Manager | npm | Default, widely supported |
| Error Handling | Fail-fast with diagnostics | Prevents data loss, clear feedback |
| Configuration | Minimal initial setup | Out of scope for extensive customization |
| Testing | Multi-layer verification | Quality at each stage |
| Documentation | Comprehensive README | Enables team independence |
| Integration | Isolated book/ folder | Preserves existing structure |

## References

- **Docusaurus Official Documentation:** https://docusaurus.io/docs
- **GitHub Pages Documentation:** https://docs.github.com/en/pages
- **GitHub Actions for Docusaurus:** https://docusaurus.io/docs/deployment#deploying-to-github-pages
- **Node.js LTS Releases:** https://nodejs.org/en/about/releases/
- **npm Documentation:** https://docs.npmjs.com/
