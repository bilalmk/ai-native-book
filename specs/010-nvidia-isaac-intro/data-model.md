# Data Model: NVIDIA Isaac Platform Introduction

This document outlines the key data entities for the NVIDIA Isaac Platform documentation feature.

## Entity: Page

Represents a single documentation page within the Docusaurus site.

**Attributes**:

-   **title** (string): The main title of the page, displayed at the top.
-   **content** (string - Markdown): The body content of the page.
-   **slug** (string): The URL-friendly identifier for the page.

## Entity: Chapter

A specialized type of `Page` that represents a chapter within the "NVIDIA Isaac Platform" section. It inherits all attributes from `Page`.

**Relationships**:

-   A `Chapter` belongs to the "NVIDIA Isaac Platform" section.
-   The "NVIDIA Isaac Platform" introduction `Page` has links to multiple `Chapter` pages.
