# Author Quickstart Guide

This guide provides a quick overview for authors on how to update and maintain the book content.

## Making Content Changes

1.  **Edit Content**: All book content is located in the `book/docs/` directory. Edit the Markdown files in this directory to make changes to the book.
2.  **Run Locally**: To preview your changes, navigate to the `book/` directory and run `npm start`. This will start a local development server.
3.  **Commit and Push**: Once you are happy with your changes, commit them to a new branch and create a pull request.
4.  **Deployment**: Merging a pull request to the `main` branch will automatically trigger a deployment to GitHub Pages.

## Project Structure

*   `book/`: Contains the Docusaurus project.
    *   `docs/`: The book content.
    *   `docusaurus.config.ts`: Docusaurus configuration.
    *   `sidebars.ts`: Sidebar navigation.
*   `specs/`: Contains the specification and planning documents for each chapter.
