# Quickstart: Creating the Introduction to Physical AI Page

This guide outlines the high-level steps to implement, integrate, and deploy the new introduction page using the specified AI agents and skills.

## 1. Content Generation

- **Tool**: `robotics-course-writer` agent
- **Action**: Use the agent to generate the full content for the introduction page based on the topics defined in the specification.
- **Example Prompt**:
  ```
  Generate the content for the 'Introduction to Physical AI' page. The page should cover:
  1. Foundations of Physical AI and embodied intelligence.
  2. The transition from digital AI to robots that understand physical laws.
  3. An overview of the humanoid robotics landscape.
  4. An overview of sensor systems, including LiDAR, cameras, IMUs, and force/torque sensors.
  ```

## 2. Integration

- **Tool**: `docusaurus-architect` agent
- **Action**: After the content is generated and saved to a file (e.g., `book/docs/physical-ai/introduction.mdx`), use this agent to update the Docusaurus sidebar to include a link to the new page.
- **Example Prompt**:
  ```
  Integrate the new 'Introduction to Physical AI' page into the Docusaurus site structure. The file is located at 'book/docs/physical-ai/introduction.mdx'. Please add it to the main sidebar.
  ```

## 3. Deployment

- **Tool**: `docusaurus-deployment` skill
- **Action**: Once the content is integrated and you have verified that the site builds correctly locally, use this skill to deploy the changes to GitHub Pages.
- **Example Invocation**:
  ```
  /skill docusaurus-deployment
  ```
