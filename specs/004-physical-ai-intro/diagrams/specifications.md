# Visual Diagram Specifications: Physical AI Introduction

**Purpose**: Define visual assets required by FR-012 (minimum 2 diagrams) for the introduction chapter

**Accessibility Requirement**: All diagrams MUST have detailed alt-text for WCAG 2.1 AA compliance

**File Format**: SVG (scalable, text-editable, web-optimized)

**Color Palette**: Colorblind-friendly (use tools like ColorBrewer or sufficient contrast ratios)

**Location**: `docs/physical-ai/assets/`

---

## Diagram 1: Physical AI vs Traditional AI Comparison

**File Name**: `physical-ai-comparison.svg`

**Placement in Content**: Section 3A (Problem - The Digital-Physical Gap)

**Purpose**: Visually contrast Traditional AI (digital, screen-bound) with Physical AI (embodied, interacting with reality)

**Functional Requirements Addressed**: FR-001, FR-012

### Visual Composition

**Layout**: Side-by-side comparison (Traditional AI on left, Physical AI on right)

**Dimensions**: 1200px wide × 600px tall (16:10 aspect ratio for readability)

### Left Side: Traditional AI

**Visual Elements**:
- Icon: Computer monitor/laptop displaying neural network graph or game screen
- Background: Digital grid pattern or abstract data visualization
- Example icons (small, subtle):
  - Chess piece (AlphaGo)
  - Text document (GPT/LLMs)
  - Image with bounding box (Computer Vision classification)

**Labels**:
- **Title**: "Traditional AI"
- **Environment**: "Digital Spaces"
- **Characteristics** (bullet points):
  - ✓ Perfect information
  - ✓ Instant actions
  - ✓ Infinite retries
  - ✓ No physics constraints

**Color Scheme**: Cool blues and grays (digital aesthetic)

### Right Side: Physical AI

**Visual Elements**:
- Icon: Simplified humanoid robot silhouette in action pose (walking or reaching)
- Background: Physical environment sketch (warehouse floor, stairs, objects)
- Example icons (small, subtle):
  - Robot hand grasping object
  - Bipedal legs on uneven terrain
  - Sensors (camera, LIDAR rays)

**Labels**:
- **Title**: "Physical AI"
- **Environment**: "Physical Reality"
- **Characteristics** (bullet points):
  - ⚠ Noisy sensors
  - ⚠ Real-time constraints
  - ⚠ Safety-critical
  - ⚠ Physics laws apply

**Color Scheme**: Warm oranges and earth tones (physical world aesthetic)

### Central Divider

**Visual**: Dashed vertical line separating the two sides

**Label (center, top)**: "The Digital-Physical Gap"

**Arrow (optional)**: Small arrow from left to right with text "This Quarter's Journey →"

### Typography

- **Titles**: Bold, 24px, Sans-serif (e.g., Inter, Roboto)
- **Labels**: Regular, 16px, Sans-serif
- **Bullet points**: 14px, easy-to-read font

### Accessibility

**Alt-Text** (minimum 200 characters):
```
Comparison diagram showing Traditional AI on the left (represented by a computer monitor with digital elements, operating in digital spaces with perfect information, instant actions, and no physics constraints) versus Physical AI on the right (represented by a humanoid robot in a physical environment, dealing with noisy sensors, real-time constraints, safety requirements, and physics laws). A dashed line separates the two domains, labeled "The Digital-Physical Gap."
```

### Design Notes

- Keep visual style clean and minimalist (avoid clutter)
- Use icons/symbols rather than detailed illustrations
- Ensure sufficient contrast for readability (WCAG AA: 4.5:1 for text, 3:1 for graphics)
- Colorblind-safe: Don't rely solely on color to convey meaning (use icons, text, patterns)

---

## Diagram 2: Learning Progression Through the Quarter

**File Name**: `learning-progression.svg`

**Placement in Content**: Section 5A (Journey - Learning Progression Overview)

**Purpose**: Visualize the three-phase learning journey (Design → Simulate → Deploy) and show which tools are used at each stage

**Functional Requirements Addressed**: FR-004, FR-005, FR-012

### Visual Composition

**Layout**: Horizontal flow diagram with three connected stages

**Dimensions**: 1400px wide × 500px tall (widescreen for horizontal flow)

### Stage 1: Design

**Position**: Left third of diagram

**Visual Elements**:
- Icon: Blueprint/schematic icon or pencil & paper
- Tool logo/icon: ROS 2 logo (or "ROS 2" text with robot icon)
- Small sub-icons:
  - Robot architecture diagram (simplified)
  - Sensor/actuator symbols
  - Data flow arrows

**Labels**:
- **Stage Title**: "Phase 1: Design"
- **Tool**: "ROS 2"
- **Activities**:
  - Define architecture
  - Plan control interfaces
  - Design AI integration
- **Output**: "Robot Software Architecture"

**Color**: Blue tones (planning/thinking)

### Stage 2: Simulate

**Position**: Center third of diagram

**Visual Elements**:
- Icon: Computer screen showing 3D simulation viewport
- Tool logos/icons:
  - "Gazebo" with robot in virtual environment
  - "NVIDIA Isaac Sim" with GPU/parallel symbol
- Small sub-icons:
  - Physics symbols (gravity arrow, friction)
  - Camera/sensor beams
  - Multiple robot copies (parallel training)

**Labels**:
- **Stage Title**: "Phase 2: Simulate"
- **Tools**: "Gazebo → Isaac Sim"
- **Activities**:
  - Test in safe environment
  - Train AI models
  - Iterate rapidly
- **Output**: "Validated Behaviors"

**Color**: Green tones (testing/iteration)

### Stage 3: Deploy

**Position**: Right third of diagram

**Visual Elements**:
- Icon: Physical robot (more realistic/detailed than Stage 2)
- Tool reference: "ROS 2" (same code as design)
- Small sub-icons:
  - Real-world environment (factory floor, warehouse)
  - Safety symbols (caution signs)
  - Monitoring dashboard

**Labels**:
- **Stage Title**: "Phase 3: Deploy"
- **Tool**: "ROS 2 (Hardware)"
- **Activities**:
  - Transfer to real robot
  - Adapt & fine-tune
  - Monitor performance
- **Output**: "Working Physical AI System"

**Color**: Orange tones (real-world/action)

### Connecting Elements

**Forward Arrows**:
- Large arrows connecting Stage 1 → Stage 2 → Stage 3
- Label on arrows: "Same Code, Different Environments"

**Backward Iteration Arrows** (optional but recommended):
- Dashed curved arrows from Stage 3 back to Stage 2 and Stage 2 back to Stage 1
- Label: "Iterate When Issues Arise"
- Purpose: Show non-linear professional workflow

### Top Banner (Optional but Helpful)

**Label**: "Your Learning Journey: From Concept to Reality"

**Timeline indicators**: "Week 1-3" (Design), "Week 4-8" (Simulate), "Week 9-10" (Deploy)

### Typography

- **Stage Titles**: Bold, 22px, Sans-serif
- **Tool Names**: Bold, 18px, highlight color
- **Activities**: Regular, 14px, bulleted list
- **Output**: Italic, 14px, distinct color (e.g., dark green)

### Accessibility

**Alt-Text** (minimum 300 characters):
```
Learning progression diagram showing three connected phases: Phase 1 Design (using ROS 2 to define robot architecture and plan control interfaces, outputting robot software architecture), Phase 2 Simulate (using Gazebo and NVIDIA Isaac Sim to test in safe environments and train AI models, outputting validated behaviors), and Phase 3 Deploy (using ROS 2 on hardware to transfer code to real robots and monitor performance, outputting working Physical AI systems). Large arrows connect the stages forward, with dashed arrows showing iteration loops back to earlier stages when issues arise. All stages emphasize using the same code across different environments.
```

### Design Notes

- Use consistent iconography across all three stages (same style/weight)
- Make arrows prominent (visual flow is key)
- Tool logos should be recognizable but not overwhelming
- Ensure ROS 2 appears in both Stage 1 and Stage 3 to emphasize "same code" concept
- Iteration arrows should be visually distinct from forward progress arrows (dashed vs solid)

---

## Implementation Guidelines

### Technical Specifications

**SVG Best Practices**:
- Use vector shapes (paths, circles, rects) rather than embedded raster images
- Optimize with SVGO or similar tool before deployment
- Embed fonts or use web-safe fonts to ensure consistency
- Target file size: < 100KB per diagram

**Responsive Design**:
- Diagrams should scale gracefully on mobile devices
- Minimum readable width: 320px (mobile)
- Test readability at various viewport sizes

**Docusaurus Integration**:
- Use Markdown image syntax: `![Alt text](./assets/filename.svg "Caption")`
- Diagrams will auto-scale within content width
- Add captions using Markdown (e.g., italicized text below image)

### Creation Tools (Suggestions)

**Recommended**:
- **Figma**: Free, web-based, export to SVG
- **Inkscape**: Free, open-source SVG editor
- **Draw.io (diagrams.net)**: Free, diagram-focused, exports clean SVG

**AI-Assisted (if available)**:
- Use AI tools (DALL-E, Midjourney, Claude Artifacts) to generate initial concepts
- Refine in vector editor for precision and accessibility

### Validation Checklist

Before finalizing diagrams, verify:

- [ ] Alt-text is comprehensive (200+ characters, describes all visual elements)
- [ ] Color contrast meets WCAG AA standards (check with WebAIM Contrast Checker)
- [ ] Colorblind-safe palette (test with Coblis simulator or similar)
- [ ] Text is readable at minimum mobile width (320px)
- [ ] File size is optimized (< 100KB)
- [ ] SVG validates (use W3C SVG validator)
- [ ] Labels match terminology used in text (consistency check)
- [ ] Diagrams render correctly in Docusaurus dev server

---

## Diagram Captions (For Reference)

### Diagram 1 Caption
*Traditional AI excels in digital domains with perfect information and instant actions, while Physical AI must navigate the uncertainties and constraints of the real world, including noisy sensors, physics laws, and safety requirements.*

### Diagram 2 Caption
*The learning journey from design to deployment: use ROS 2 to architect your robot, test and refine behaviors in Gazebo and Isaac Sim simulations, then deploy the same code to physical hardware. Iteration loops back to simulation when real-world issues arise, mirroring professional robotics workflows.*

---

## Success Criteria Mapping

- **SC-005**: Both diagrams specified (Physical AI comparison + Learning progression) ✓
- **FR-012**: Minimum 2 diagrams requirement met ✓
- **Accessibility (Non-Functional)**: Alt-text, contrast, colorblind-safe palette specified ✓
- **SC-010** (Consistency): Diagram labels match text terminology (validate during writing) ✓

---

## Next Steps (Phase 6: Visual Assets - Tasks T029-T032)

1. **T029**: Create Diagram 1 SVG based on these specifications
2. **T030**: Create Diagram 2 SVG based on these specifications
3. **T031**: Add comprehensive alt-text to both diagrams
4. **T032**: Embed diagrams into `docs/physical-ai/index.md` with captions

**Note**: These tasks can run in parallel with Content Section writing (Phase 3-5) since specifications are now complete.
