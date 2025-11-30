import type { SidebarsConfig } from "@docusaurus/plugin-content-docs";

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: "category",
      label: "Physical AI",
      link: {
        type: "doc",
        id: "physical-ai/index",
      },
      items: [
        "physical-ai/physical-ai-introduction",
        "physical-ai/foundations-of-physical-ai",
        "physical-ai/from-digital-ai-to-robots",
        "physical-ai/humanoid-robotics-landscape",
        "physical-ai/sensor-systems",
      ],
    },
    {
      type: "category",
      label: "ROS 2 Fundamentals",
      link: {
        type: "doc",
        id: "ros2-fundamentals/index",
      },
      items: [
        "ros2-fundamentals/ros2-architecture-core-concepts",
        "ros2-fundamentals/nodes-topics-services-actions",
        "ros2-fundamentals/building-ros2-packages-with-python",
        "ros2-fundamentals/launch-files-parameter-management",
      ],
    },
    {
      type: "category",
      label: "Robot Simulation with Gazebo",
      link: {
        type: "doc",
        id: "robot-simulation-gazebo/index",
      },
      items: [
        "robot-simulation-gazebo/gazebo-setup",
        "robot-simulation-gazebo/urdf-sdf",
        "robot-simulation-gazebo/physics-sensors",
        "robot-simulation-gazebo/unity-visualization",
      ],
    },
  ],
};

export default sidebars;
