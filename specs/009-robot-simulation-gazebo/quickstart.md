# Quickstart: Adding New Chapters

**Date**: 2025-11-30
**Status**: Completed

This guide provides a quick overview of how to add a new chapter to the textbook.

## Steps

1.  **Generate Content**:
    *   Use the `robotics-course-writer` agent to generate the content for the new chapter. Provide a clear and concise prompt describing the chapter's topic and learning objectives.
    *   Save the generated content to a markdown file (e.g., `new-chapter.md`).

2.  **Integrate into Docusaurus**:
    *   Use the `docusaurus-architect` agent to integrate the new chapter. This agent will:
        *   Create the new page in the Docusaurus site.
        *   Add a link to the new chapter in the sidebar navigation in the appropriate section.
        *   Ensure the site builds correctly with the new content.

3.  **Deploy**:
    *   Once the new chapter is integrated and verified locally, use the `docusaurus-deployment` skill to deploy the updated site to GitHub Pages.
