import { themes } from "../themes.js";

const navIcons = {
  "full-stack": `
    <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path d="M4 7.5A2.5 2.5 0 0 1 6.5 5h11A2.5 2.5 0 0 1 20 7.5v9a2.5 2.5 0 0 1-2.5 2.5h-11A2.5 2.5 0 0 1 4 16.5v-9ZM7 8v2h3V8H7Zm5 0v2h5V8h-5Zm0 4v2h5v-2h-5Zm-5 0v2h3v-2H7Zm0 4v2h5v-2H7Z"></path>
    </svg>
  `,
  automation: `
    <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path d="M12 2a2 2 0 0 1 2 2v1.1c.7.2 1.4.5 2 .9l.8-.8a2 2 0 1 1 2.8 2.8l-.8.8c.4.6.7 1.3.9 2H20a2 2 0 1 1 0 4h-1.1c-.2.7-.5 1.4-.9 2l.8.8a2 2 0 1 1-2.8 2.8l-.8-.8c-.6.4-1.3.7-2 .9V20a2 2 0 1 1-4 0v-1.1c-.7-.2-1.4-.5-2-.9l-.8.8a2 2 0 1 1-2.8-2.8l.8-.8c-.4-.6-.7-1.3-.9-2H4a2 2 0 1 1 0-4h1.1c.2-.7.5-1.4.9-2l-.8-.8a2 2 0 1 1 2.8-2.8l.8.8c.6-.4 1.3-.7 2-.9V4a2 2 0 0 1 2-2Zm0 6a4 4 0 1 0 0 8 4 4 0 0 0 0-8Z"></path>
    </svg>
  `,
  research: `
    <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path d="M12 2 13.8 5.2 17.4 5.6 18.5 9.2 15.7 11.8 16.2 15.5 12.9 17.3 10.2 15.7 6.9 17.3 5.6 13.9 2.9 11.9 4 8.4 7.6 7.9 9.5 4.7 12 2Zm0 6.1a3.9 3.9 0 1 0 0 7.8 3.9 3.9 0 0 0 0-7.8Z"></path>
    </svg>
  `,
  "game-dev": `
    <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path d="M7 8h10a4 4 0 0 1 4 4v3a3 3 0 0 1-3 3h-2l-2-2H10l-2 2H6a3 3 0 0 1-3-3v-3a4 4 0 0 1 4-4Zm2 2a1 1 0 1 0 0 2H8v1a1 1 0 1 0 2 0v-1h1a1 1 0 1 0 0-2h-1V9a1 1 0 1 0-2 0v1Zm7.5 1.5a1 1 0 1 0 0 2 1 1 0 0 0 0-2Zm2 2a1 1 0 1 0 0 2 1 1 0 0 0 0-2Z"></path>
    </svg>
  `,
  prototypes: `
    <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path d="M6 4h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2Zm1.5 3A1.5 1.5 0 1 0 7.5 10a1.5 1.5 0 0 0 0-3ZM9 14.5h7v-1.5H9v1.5Zm0-3h6v-1.5H9v1.5Z"></path>
    </svg>
  `,
  xr: `
    <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path d="M7 6h10a4 4 0 0 1 4 4v2.5A3.5 3.5 0 0 1 17.5 16H16l-1.7 2.3a2 2 0 0 1-1.6.7h-1.2a2 2 0 0 1-1.6-.7L8.2 16H6.5A3.5 3.5 0 0 1 3 12.5V10a4 4 0 0 1 4-4Zm-.5 5a2.5 2.5 0 0 0 0 5H8l1.9 2.5h4.2L16 16h1.5a2.5 2.5 0 0 0 0-5h-11Z"></path>
    </svg>
  `,
  "agentic-engineering": `
    <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path d="M12 3a3 3 0 0 1 3 3v1h2a2 2 0 0 1 2 2v2h-1.5a1.5 1.5 0 0 0 0 3H19v2a2 2 0 0 1-2 2h-2v1a3 3 0 0 1-6 0v-1H7a2 2 0 0 1-2-2v-2h1.5a1.5 1.5 0 0 0 0-3H5V9a2 2 0 0 1 2-2h2V6a3 3 0 0 1 3-3Zm0 5a4 4 0 1 0 0 8 4 4 0 0 0 0-8Z"></path>
    </svg>
  `,
  settings: `
    <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path d="M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8Zm9 4a7.9 7.9 0 0 0-.2-1.8l2.1-1.6-2-3.5-2.5 1a8.2 8.2 0 0 0-3.1-1.8L14.8 2h-4l-.5 2.3A8.2 8.2 0 0 0 7.2 6.1l-2.5-1-2 3.5 2.1 1.6a7.9 7.9 0 0 0 0 3.6l-2.1 1.6 2 3.5 2.5-1a8.2 8.2 0 0 0 3.1 1.8L10.2 22h4l.5-2.3a8.2 8.2 0 0 0 3.1-1.8l2.5 1 2-3.5-2.1-1.6c.1-.6.2-1.2.2-1.8Z"></path>
    </svg>
  `,
  connect: `
    <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path d="M7 12a4 4 0 0 1 4-4h2v2h-2a2 2 0 1 0 0 4h2v2h-2a4 4 0 0 1-4-4Zm6-1h2v2h-2v-2Zm3-5a4 4 0 0 1 4 4 4 4 0 0 1-4 4h-1v-2h1a2 2 0 1 0 0-4h-2V6h2Z"></path>
    </svg>
  `,
};

export const portfolioSchema = {
  profile: {
    name: "Crimson Wheeler",
    eyebrow: "Portfolio",
    title:
      "Systems architect, gameplay engineer, XR developer, and agentic engineering builder.",
    email: "crimson@crimsonwheeler.dev",
    github: "https://github.com/crimsonwheeler",
    linkedin: "https://www.linkedin.com/in/crimson-wheeler/",
  },
  design: {
    shell: {
      headerHeight: "4.9rem",
      railCollapsedWidth: "4rem",
      railItemHeight: "4rem",
      railExpandedWidth: "192px",
      mobileRailWidth: "min(88vw, 340px)",
      contentPaddingDesktop: "0",
      contentPaddingMobile: "0",
    },
    grid: {
      defaultColumns: 2,
      supportedColumns: [1, 2, 3],
    },
  },
  themes,
  nav: [
    { id: "full-stack", label: "Full Stack", icon: navIcons["full-stack"] },
    { id: "automation", label: "Automation", icon: navIcons.automation },
    { id: "research", label: "Research", icon: navIcons.research },
    { id: "game-dev", label: "Game Dev / XR", icon: navIcons["game-dev"] },
    { id: "arcade-library", label: "Arcade Library", icon: navIcons.prototypes },
    { id: "prototypes", label: "Arcade", icon: navIcons.prototypes },
    {
      id: "agentic-engineering",
      label: "Agentic Engineering",
      icon: navIcons["agentic-engineering"],
    },
    { id: "connect", label: "Connect", icon: navIcons.connect },
    { id: "settings", label: "Settings", icon: navIcons.settings },
  ],
  pages: {
    landing: {
      id: "landing",
      title: "Star Harbor",
      route: "landing",
      type: "landing",
      description:
        "Landing page for Crimson Wheeler with a quiet catching-stars scene, persistent star counter, and entry point into the portfolio.",
      subtitle:
        "A floating portfolio in a quiet harbor of systems work, playable experiments, and human-centered tools.",
      introPoints: [],
      meta: ["Cinematic entry", "Persistent stars", "Portfolio gateway"],
      featuredProjectSlugs: [],
      tools: ["Three.js", "Vite", "Local Storage"],
    },
    "full-stack": {
      id: "full-stack",
      title: "Full Stack",
      route: "full-stack",
      type: "section",
      description:
        "Full Stack portfolio for Crimson Wheeler covering end-to-end product delivery, interface work, tooling, and deployment paths.",
      subtitle:
        "End-to-end product systems spanning interface work, tooling, automation, and delivery.",
      introPoints: [
        {
          pair: "Web Apps + UI Systems",
          text: "Product-facing interfaces shaped for clarity, structure, and maintainable interaction patterns.",
        },
        {
          pair: "Automation + Delivery",
          text: "Operational workflows designed to keep build, release, and deployment work dependable.",
        },
        {
          pair: "Integration + Architecture",
          text: "End-to-end systems thinking across interface layers, tooling, and infrastructure decisions.",
        },
      ],
      meta: ["End-to-end delivery", "Interface to infrastructure", "Default entry"],
      featuredProjectSlugs: [
        "powershell-toolkit",
        "deployment-automation-at-scale",
        "delivery-systems-architecture",
        "a-tiny-rhythm-meter-prototype",
        "playtest-studio",
        "playtest-studio-with-presets-and-replay",
        "physics-draw-replay",
      ],
      tools: [
        "Web Apps",
        "UI Systems",
        "Automation",
        "CI/CD",
        "GitHub",
        "API Integration",
        "Delivery Flow",
      ],
    },
    automation: {
      id: "automation",
      title: "Automation",
      route: "automation",
      type: "section",
      description:
        "Automation portfolio for Crimson Wheeler covering repeatable workflows, release systems, and operational tooling.",
      subtitle:
        "Repeatable workflows and operator-facing systems designed to reduce manual work safely.",
      introPoints: [
        {
          pair: "Release + Reliability",
          text: "Automation patterns aimed at repeatable delivery with fewer fragile manual steps.",
        },
        {
          pair: "Operators + Tooling",
          text: "Interfaces and scripts built so technical teams can act quickly without losing control.",
        },
        {
          pair: "CI/CD + Operations",
          text: "Workflow design that connects deployment surfaces, verification, and support readiness.",
        },
      ],
      meta: ["Operations tooling", "Repeatable workflows", "System support"],
      featuredProjectSlugs: [
        "powershell-toolkit",
        "deployment-automation-at-scale",
        "delivery-systems-architecture",
      ],
      tools: [
        "PowerShell",
        "CI/CD",
        "Release Automation",
        "GitHub",
        "N-central",
        "Workflow Reliability",
      ],
    },
    research: {
      id: "research",
      title: "Research",
      route: "research",
      type: "section",
      description:
        "Research portfolio for Crimson Wheeler covering technical exploration, validation, and architecture framing.",
      subtitle:
        "Technical exploration and validation work focused on reducing risk before implementation.",
      introPoints: [
        {
          pair: "Exploration + Validation",
          text: "Early investigation used to test assumptions before a larger implementation path is chosen.",
        },
        {
          pair: "Architecture + Framing",
          text: "Technical options compared with attention to delivery risk, complexity, and fit.",
        },
        {
          pair: "Experiments + Decisions",
          text: "Prototype-driven discovery translated into concrete direction for buildable systems.",
        },
      ],
      meta: ["Problem framing", "Technical exploration", "Validation"],
      featuredProjectSlugs: [
        "delivery-systems-architecture",
        "onnx-runtime-tooling",
        "agent-workflow-orchestration",
      ],
      tools: [
        "Prototyping",
        "Evaluation",
        "Architecture",
        "Tool Selection",
        "Experimentation",
        "Workflow Design",
      ],
    },
    "game-dev": {
      id: "game-dev",
      title: "Game Dev / XR",
      route: "game-dev",
      type: "section",
      description:
        "Game development and XR portfolio for Crimson Wheeler covering gameplay prototypes, technical slices, immersive demos, and spatial experiences.",
      subtitle:
        "Gameplay loops, technical slices, immersive demos, and spatial experiences built to prove feel and readability early.",
      introPoints: [
        {
          pair: "Gameplay + Readability",
          text: "Mechanics and interaction loops tuned to communicate intent quickly and feel responsive.",
        },
        {
          pair: "XR + Presence",
          text: "Immersive work built around comfort, clarity, and stable player-facing experience design.",
        },
        {
          pair: "Prototypes + Production",
          text: "Fast experiments and polished slices used together to validate mechanics and delivery quality.",
        },
      ],
      meta: ["Playable demos", "Mechanics-first", "XR production"],
      featuredProjectSlugs: [
        "cyber-slingers",
        "sky-drifter-dragon-edition",
        "multiplayer-escape-room-island",
        "pillow",
        "watson",
        "dancing-with-the-ancestors",
        "oticon-audio-experience",
      ],
      tools: [
        "Unity",
        "Gameplay Prototyping",
        "Rendering",
        "XR Interaction Toolkit",
        "Meta Presence Platform",
        "Hand Tracking",
        "Mixed Reality",
        "Depthkit",
        "Player Feedback",
        "Rapid Iteration",
      ],
    },
    prototypes: {
      id: "prototypes",
      title: "Arcade",
      route: "prototypes",
      type: "section",
      description:
        "Arcade space for Crimson Wheeler, featuring small single-file JavaScript games and interactive browser experiments.",
      subtitle:
        "Short, self-contained browser games built to test motion, feedback, and interaction ideas quickly.",
      introPoints: [
        {
          pair: "Motion + Feedback",
          text: "Short-form prototypes used to test response, rhythm, and visual clarity without heavy scaffolding.",
        },
        {
          pair: "Canvas + Input",
          text: "Interaction experiments focused on how controls and movement feel in a minimal browser surface.",
        },
        {
          pair: "Speed + Iteration",
          text: "Small standalone pages built to validate one idea at a time and keep experimentation fast.",
        },
      ],
      meta: ["Single-file demos", "Fast iteration", "Browser-first"],
      featuredProjectSlugs: [
        "signal-runner",
        "orbit-pop",
        "grid-pulse",
        "lab-rift",
        "phase-drop",
        "drift-harbor",
        "pulse-drift",
        "echo-loop",
      ],
      tools: [
        "JavaScript",
        "Canvas",
        "Animation Loops",
        "Input Handling",
        "Rapid Prototyping",
      ],
    },
    "arcade-library": {
      id: "arcade-library",
      title: "Arcade Library",
      route: "arcade-library",
      type: "section",
      description:
        "Arcade Library for Crimson Wheeler, featuring the full gallery of one-file browser games and experiments.",
      subtitle:
        "Browse the full gallery, then open a game in Arcade to play it.",
      introPoints: [
        {
          pair: "Gallery + Shelf",
          text: "Every arcade game lives here as a browsable visual library.",
        },
        {
          pair: "Pick + Launch",
          text: "Choose a game from the gallery, then open it in the dedicated Arcade player.",
        },
        {
          pair: "Fast + Small",
          text: "Short browser games built as compact one-file demos for rapid iteration.",
        },
      ],
      meta: ["Game gallery", "Arcade shelf", "Browser-first"],
      featuredProjectSlugs: [
        "signal-runner",
        "orbit-pop",
        "grid-pulse",
        "lab-rift",
        "phase-drop",
        "drift-harbor",
        "pulse-drift",
        "echo-loop",
      ],
      tools: [
        "JavaScript",
        "Canvas",
        "Animation Loops",
        "Input Handling",
        "Rapid Prototyping",
      ],
    },
    "agentic-engineering": {
      id: "agentic-engineering",
      title: "Agentic Engineering",
      route: "agentic-engineering",
      type: "section",
      description:
        "Agentic engineering portfolio for Crimson Wheeler covering AI tooling, local inference, bots, and workflow orchestration.",
      subtitle:
        "AI systems work focused on orchestration, inference tooling, and operator-facing automation.",
      introPoints: [
        {
          pair: "Agents + Workflows",
          text: "Multi-step systems designed to connect prompts, tools, and human checkpoints into usable operations.",
        },
        {
          pair: "Inference + Tooling",
          text: "Runtime-minded implementation work that turns model capability into dependable local tools.",
        },
        {
          pair: "Operators + Interfaces",
          text: "Automation surfaces shaped around trust, visibility, and clear execution boundaries.",
        },
      ],
      meta: ["Applied AI systems", "Inference + tooling", "Operator-facing workflows"],
      featuredProjectSlugs: [
        "onnx-runtime-tooling",
        "agent-workflow-orchestration",
        "bot-operations-tooling",
      ],
      tools: [
        "ONNX",
        "Bot Systems",
        "Workflow Orchestration",
        "Automation",
        "Inference Tooling",
        "Prompt Design",
        "Operator UX",
      ],
    },
    settings: {
      id: "settings",
      title: "Settings",
      route: "settings",
      type: "settings",
      description:
        "Portfolio system notes for Crimson Wheeler, covering the fixed visual baseline and presentation principles.",
      subtitle:
        "A single shared interface baseline keeps every section visually consistent.",
      introPoints: [
        {
          pair: "Consistency + Rhythm",
          text: "Spacing, scale, and structure stay aligned so the portfolio reads as one system instead of a configurable dashboard.",
        },
        {
          pair: "Layout + Restraint",
          text: "The shell stays intentionally fixed so the work, writing, and project imagery carry the presentation.",
        },
        {
          pair: "Design + Focus",
          text: "Settings now describe the visual system rather than mutating it, which keeps every tab on the same baseline.",
        },
      ],
      meta: ["Fixed baseline", "Shared styling", "Portfolio system"],
      featuredProjectSlugs: [],
      tools: ["Slate", "Avenir Next", "Tight Structure"],
    },
    connect: {
      id: "connect",
      title: "Connect",
      route: "connect",
      type: "connect",
      description:
        "Connect with Crimson Wheeler across email, GitHub, and LinkedIn.",
      subtitle:
        "Reach out for portfolio work, collaboration, or technical conversations.",
      introPoints: [
        {
          pair: "Email + Projects",
          text: "Best path for direct outreach, scoped work discussions, and follow-up questions.",
        },
        {
          pair: "GitHub + Source",
          text: "Public code and technical experiments that show implementation style and ongoing exploration.",
        },
        {
          pair: "LinkedIn + Network",
          text: "Professional context, background, and a straightforward connection point for collaboration.",
        },
      ],
      meta: ["Contact links", "Professional networks", "Open to connect"],
      featuredProjectSlugs: [],
      tools: ["Email", "GitHub", "LinkedIn"],
    },
  },
  projects: {
    "powershell-toolkit": {
      slug: "powershell-toolkit",
      title: "PowerShell Toolkit",
      section: "full-stack",
      kind: "Engineering",
      shortDescription:
        "Command-line automation toolkit built to standardize software deployment and fleet operations.",
      description:
        "A modular PowerShell toolkit built to streamline large-scale IT operations. It packaged repeatable deployment, troubleshooting, and maintenance workflows into a system operators could use quickly without sacrificing control.",
      image:
        "https://crimsonwheeler.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fb0930ce5-2382-4810-8e92-3ece8545d32c%2F80c67ee6-7c52-4aee-90b9-f40013b46d13%2Fazure-powershell-bg.jpg?table=block&id=195caa1b-d33a-812c-9710-f8c8d6e86ceb&spaceId=b0930ce5-2382-4810-8e92-3ece8545d32c&width=2000&userId=&cache=v2",
      features: [
        "100+ modular scripts covering common operational tasks",
        "Automated deployment flows through GitHub and N-central",
        "Dependency-aware setup for 800 preconfigured machines",
        "Remote management patterns designed for everyday IT use",
      ],
      technologies: [
        "PowerShell",
        "GitHub",
        "N-central",
        "CI/CD",
        "Office 365",
        "Active Directory",
      ],
      links: [],
    },
    "deployment-automation-at-scale": {
      slug: "deployment-automation-at-scale",
      title: "Deployment Automation at Scale",
      section: "full-stack",
      kind: "Engineering",
      shortDescription:
        "Release automation patterns for keeping large device fleets consistent and supportable.",
      description:
        "A delivery initiative centered on repeatable rollout workflows, dependency control, and operator trust. The work focused on making deployments predictable, auditable, and fast to troubleshoot across a large managed environment.",
      image:
        "/images/projects/deployment-automation-at-scale.svg",
      features: [
        "Repeatable deployment sequencing across managed endpoints",
        "Operational guardrails to reduce misconfigured rollouts",
        "Troubleshooting paths designed for support speed",
        "Clear separation between tooling logic and operator actions",
      ],
      technologies: [
        "Automation",
        "Systems Administration",
        "Release Design",
        "Workflow Reliability",
      ],
      links: [],
    },
    "delivery-systems-architecture": {
      slug: "delivery-systems-architecture",
      title: "Delivery Systems Architecture",
      section: "full-stack",
      kind: "Engineering",
      shortDescription:
        "Technical leadership work around delivery systems, build hygiene, and project execution.",
      description:
        "A cross-project architecture effort around the systems that let product teams ship reliably: environment setup, workflow design, technical handoff, and implementation patterns that keep delivery moving as scope expands.",
      image:
        "/images/projects/delivery-systems-architecture.svg",
      features: [
        "Technical decision-making focused on delivery risk reduction",
        "Workflow patterns built for cross-discipline teams",
        "Clear handoff paths for implementation and support",
        "Infrastructure-minded planning for growing project scope",
      ],
      technologies: [
        "Architecture",
        "Technical Leadership",
        "Delivery Planning",
        "Process Design",
      ],
      links: [],
    },
    "cyber-slingers": {
      slug: "cyber-slingers",
      title: "Cyber Slingers",
      section: "game-dev",
      kind: "Game Dev",
      shortDescription:
        "Fast-paced VR game built around short sessions and adaptive difficulty.",
      description:
        "A solo-developed VR game designed for immediate readability and replayability. The core loop is tuned for one-and-a-half-minute sessions, with difficulty adapting to player performance as the run escalates.",
      image:
        "https://crimsonwheeler.notion.site/image/attachment%3Ab64bdc56-bfe6-49da-abca-1ef19745c94e%3AScreenshot_2025-02-09_174548.png?table=block&id=195caa1b-d33a-80ae-b2c3-ea4f8b551a3d&spaceId=b0930ce5-2382-4810-8e92-3ece8545d32c&width=2000&userId=&cache=v2",
      features: [
        "Adaptive difficulty driven by player performance",
        "Custom rendering and lighting decisions for VR readability",
        "Integrated leaderboard support",
        "Short-form replay loop built for rapid re-entry",
      ],
      technologies: [
        "Unity",
        "VR",
        "XR Interaction Toolkit",
        "Post-Processing",
        "Game Design",
      ],
      links: [],
    },
    "sky-drifter-dragon-edition": {
      slug: "sky-drifter-dragon-edition",
      title: "Sky Drifter: Dragon Edition",
      section: "game-dev",
      kind: "Game Dev Demo",
      shortDescription:
        "Three.js flying demo that turns a simple web page into a playable dragon prototype.",
      description:
        "A lightweight browser demo built around flight feel, terrain generation, and immediate input response. It works as a fast proof point for mechanics, motion language, and interactive polish outside a heavy engine pipeline.",
      image:
        "/images/projects/sky-drifter-dragon-edition.svg",
      features: [
        "Browser-playable dragon flight loop",
        "Procedural terrain generation with ring collection",
        "Mouse steering and flap-based movement controls",
        "Standalone demo page for quick access and review",
      ],
      technologies: [
        "Three.js",
        "JavaScript",
        "Procedural Generation",
        "Browser Gameplay",
      ],
      links: [
        {
          label: "Launch Demo",
          href: "Pages/dragon/",
          style: "secondary",
        },
      ],
    },
    "multiplayer-escape-room-island": {
      slug: "multiplayer-escape-room-island",
      title: "Multiplayer Escape Room Island",
      section: "game-dev",
      kind: "Game Dev",
      shortDescription:
        "Networked VR escape room prototype built around synchronized puzzle progression.",
      description:
        "A multiplayer gameplay slice focused on coordinated puzzle logic, intuitive onboarding, and network-aware progression. The project emphasizes state flow and cooperative interactions across players.",
      image:
        "https://crimsonwheeler.notion.site/image/attachment%3Ae05e3479-9cb8-4f1f-b5a1-c929da0a47e8%3AScreenshot_2025-02-09_173857.png?table=block&id=195caa1b-d33a-8030-8c10-e2d41e0bc5e6&spaceId=b0930ce5-2382-4810-8e92-3ece8545d32c&width=2000&userId=&cache=v2",
      features: [
        "Integrated state machine for networked progression",
        "Tutorial puzzle structure for faster player comprehension",
        "Hand tracking integration",
        "Physics-aware interactions in cooperative play",
      ],
      technologies: [
        "Unity",
        "PUN2 Networking",
        "Meta Presence Platform",
        "Gameplay Systems",
      ],
      links: [],
    },
    "signal-runner": {
      slug: "signal-runner",
      title: "Signal Runner",
      section: "prototypes",
      kind: "Demo Game",
      shortDescription:
        "An infinite lane runner where speed ramps up and hazard timing keeps tightening.",
      description:
        "Signal Runner is a browser endless runner built around fast lane swaps, readable hazard timing, and escalating pressure as the track speeds up.",
      image:
        "/images/projects/signal-runner.svg",
      features: [
        "Infinite lane runner loop with restart flow",
        "Escalating speed and denser obstacle pressure",
        "Readable neon track with fast keyboard response",
        "Single-file HTML and JavaScript implementation",
      ],
      technologies: ["JavaScript", "Canvas", "Game Loop", "Input Response"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/signal-runner/",
          style: "secondary",
        },
      ],
    },
    "orbit-pop": {
      slug: "orbit-pop",
      title: "Orbit Pop",
      section: "prototypes",
      kind: "Prototype",
      shortDescription:
        "A mouse-driven orbit prototype for checking spatial feedback and click timing.",
      description:
        "Orbit Pop explores simple pointer control and target acquisition with a clean circular motion language. The goal is to keep the interaction obvious while still feeling responsive and a little playful.",
      image:
        "/images/projects/orbit-pop.svg",
      features: [
        "Pointer-following orbit motion",
        "Click targets that award quick feedback",
        "Small scoring loop for repeat testing",
        "Single-file HTML and JavaScript implementation",
      ],
      technologies: ["JavaScript", "Pointer Input", "Canvas", "Feedback"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/orbit-pop/",
          style: "secondary",
        },
      ],
    },
    "grid-pulse": {
      slug: "grid-pulse",
      section: "prototypes",
      title: "Grid Pulse",
      kind: "Prototype",
      shortDescription:
        "A keyboard-toggled grid pulse test for motion rhythm and state clarity.",
      description:
        "Grid Pulse is a small state-driven prototype used to evaluate whether a reactive grid, beat timing, and mode changes remain legible under quick user input.",
      image:
        "/images/projects/grid-pulse.svg",
      features: [
        "Toggleable pulse states for visual rhythm testing",
        "Keyboard interaction with immediate feedback",
        "Clean tiled layout for readability checks",
        "Single-file HTML and JavaScript implementation",
      ],
      technologies: ["JavaScript", "Animation", "State Changes", "Canvas"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/grid-pulse/",
          style: "secondary",
        },
      ],
    },
    "lab-rift": {
      slug: "lab-rift",
      title: "Lab Rift",
      section: "prototypes",
      kind: "Demo Game",
      shortDescription: "A compact arena test for movement timing and hazard spacing.",
      description:
        "Lab Rift is a small browser demo about crossing a shifting arena while reading hazard timing and keeping the player path clear.",
      image:
        "/images/projects/lab-rift.svg",
      features: [
        "Single-screen arena loop",
        "Timing-based hazard checks",
        "Fast restart flow",
        "Single-file HTML and JavaScript implementation",
      ],
      technologies: ["JavaScript", "Canvas", "Game Loop", "Input Response"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/lab-rift/",
          style: "secondary",
        },
      ],
    },
    "phase-drop": {
      slug: "phase-drop",
      title: "Phase Drop",
      section: "prototypes",
      kind: "Demo Game",
      shortDescription: "A falling-block reaction demo with lane swaps and pressure ramping.",
      description:
        "Phase Drop tests quick lane changes against a rising fall speed and simple collision states.",
      image:
        "/images/projects/phase-drop.svg",
      features: [
        "Lane swap controls",
        "Increasing drop speed",
        "Clear fail and retry state",
        "Single-file HTML and JavaScript implementation",
      ],
      technologies: ["JavaScript", "Canvas", "Reaction", "State Changes"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/phase-drop/",
          style: "secondary",
        },
      ],
    },
    "drift-harbor": {
      slug: "drift-harbor",
      title: "Drift Harbor",
      section: "prototypes",
      kind: "Demo Game",
      shortDescription: "A calm steering demo that checks glide feel and path control.",
      description:
        "Drift Harbor uses a soft steering loop to evaluate how movement inertia and waypoint timing feel in a browser prototype.",
      image:
        "/images/projects/drift-harbor.svg",
      features: [
        "Smooth steering loop",
        "Waypoint collection",
        "Motion-readability focus",
        "Single-file HTML and JavaScript implementation",
      ],
      technologies: ["JavaScript", "Canvas", "Motion", "Feedback"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/drift-harbor/",
          style: "secondary",
        },
      ],
    },
    "pulse-drift": {
      slug: "pulse-drift",
      title: "Pulse Drift",
      section: "prototypes",
      kind: "Demo Game",
      shortDescription: "A rhythm-state prototype built around toggled pulses and drift.",
      description:
        "Pulse Drift uses changing beat states and simple drift behavior to test how rhythm and feedback read together.",
      image:
        "/images/projects/pulse-drift.svg",
      features: [
        "Rhythm-state toggles",
        "Visible pulse feedback",
        "Quick repeat loop",
        "Single-file HTML and JavaScript implementation",
      ],
      technologies: ["JavaScript", "Animation", "State Changes", "Canvas"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/pulse-drift/",
          style: "secondary",
        },
      ],
    },
    "echo-loop": {
      slug: "echo-loop",
      title: "Echo Loop",
      section: "prototypes",
      kind: "Demo Game",
      shortDescription: "A repeat-run prototype that checks memory, feedback, and pacing.",
      description:
        "Echo Loop is a replay-focused demo where each run echoes the last so pacing and memory cues stay obvious.",
      image:
        "/images/projects/echo-loop.svg",
      features: [
        "Repeat-run structure",
        "Simple recall-driven scoring",
        "Short session pacing",
        "Single-file HTML and JavaScript implementation",
      ],
      technologies: ["JavaScript", "Canvas", "Replay", "Feedback"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/echo-loop/",
          style: "secondary",
        },
      ],
    },
    "playtest-studio": {
      slug: "playtest-studio",
      title: "Playtest Studio",
      section: "prototypes",
      kind: "Prototype",
      shortDescription:
        "Single-file browser prototype for playtest studio.",
      description:
        "playtest studio",
      image:
        "/images/projects/playtest-studio.svg",
      features: [
        "Single-file browser prototype",
        "Generated from Portfolio-CLI",
      ],
      technologies: ["JavaScript", "HTML", "Prototype"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/playtest-studio/",
          style: "secondary",
        },
      ],
    },
    "playtest-studio-with-presets-and-replay": {
      slug: "playtest-studio-with-presets-and-replay",
      title: "Playtest Studio With Presets And Replay",
      section: "prototypes",
      kind: "Prototype",
      shortDescription:
        "Single-file browser prototype for playtest studio with presets and replay.",
      description:
        "playtest studio with presets and replay",
      image:
        "/images/projects/playtest-studio-with-presets-and-replay.svg",
      features: [
        "Single-file browser prototype",
        "Generated from Portfolio-CLI",
      ],
      technologies: ["JavaScript", "HTML", "Prototype"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/playtest-studio-with-presets-and-replay/",
          style: "secondary",
        },
      ],
    },
    "physics-draw-replay": {
      slug: "physics-draw-replay",
      title: "Physics Draw Replay",
      section: "prototypes",
      kind: "Prototype",
      shortDescription:
        "Single-file browser prototype for physics draw replay.",
      description:
        "physics draw replay",
      image:
        "/images/projects/physics-draw-replay.svg",
      features: [
        "Single-file browser prototype",
        "Generated from Portfolio-CLI",
      ],
      technologies: ["JavaScript", "HTML", "Prototype"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/physics-draw-replay/",
          style: "secondary",
        },
      ],
    },
    "neon-lane-runner": {
      slug: "neon-lane-runner",
      title: "Neon Lane Runner",
      section: "prototypes",
      kind: "Prototype",
      shortDescription:
        "Greyboxed arcade game generated for neon lane runner.",
      description:
        "neon lane runner",
      image:
        "/images/projects/neon-lane-runner.svg",
      features: [
        "JSON-driven content",
        "Shared runtime mode",
        "Greyboxed visual treatment",
      ],
      technologies: ["JSON", "Shared Runtime", "Prototype"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/neon-lane-runner/",
          style: "secondary",
        },
      ],
    },
    "drift-beat-harbor": {
      slug: "drift-beat-harbor",
      title: "Drift Beat Harbor",
      section: "prototypes",
      kind: "Prototype",
      shortDescription:
        "Greyboxed arcade game generated for drift beat harbor.",
      description:
        "drift beat harbor",
      image:
        "/images/projects/drift-beat-harbor.svg",
      features: [
        "JSON-driven content",
        "Shared runtime mode",
        "Greyboxed visual treatment",
      ],
      technologies: ["JSON", "Shared Runtime", "Prototype"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/drift-beat-harbor/",
          style: "secondary",
        },
      ],
    },
    "sandstorm-memory-harbor": {
      slug: "sandstorm-memory-harbor",
      title: "Sandstorm Memory Harbor",
      section: "prototypes",
      kind: "Prototype",
      shortDescription:
        "Greyboxed arcade game generated for sandstorm memory harbor.",
      description:
        "sandstorm memory harbor",
      image:
        "/images/projects/sandstorm-memory-harbor.svg",
      features: [
        "JSON-driven content",
        "Dodge And Route",
        "Timed Swap",
        "Pickup Pressure",
      ],
      technologies: ["JSON", "Shared Runtime", "Prototype"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/sandstorm-memory-harbor/",
          style: "secondary",
        },
      ],
    },
    "crystal-orbit-salvage": {
      slug: "crystal-orbit-salvage",
      title: "Crystal Orbit Salvage",
      section: "prototypes",
      kind: "Prototype",
      shortDescription:
        "Greyboxed arcade game generated for crystal orbit salvage.",
      description:
        "crystal orbit salvage",
      image:
        "/images/projects/crystal-orbit-salvage.svg",
      features: [
        "JSON-driven content",
        "Dodge And Route",
        "Timed Swap",
        "Pickup Pressure",
      ],
      technologies: ["JSON", "Shared Runtime", "Prototype"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/crystal-orbit-salvage/",
          style: "secondary",
        },
      ],
    },
    "help-panel-harbor": {
      slug: "help-panel-harbor",
      title: "Help Panel Harbor",
      section: "prototypes",
      kind: "Prototype",
      shortDescription:
        "Greyboxed arcade game generated for help panel harbor.",
      description:
        "help panel harbor",
      image:
        "/images/projects/help-panel-harbor.svg",
      features: [
        "JSON-driven content",
        "Dodge And Route",
        "Timed Swap",
        "Pickup Pressure",
      ],
      technologies: ["JSON", "Shared Runtime", "Prototype"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/help-panel-harbor/",
          style: "secondary",
        },
      ],
    },
    "salvage-orbit-ruins-neon-pressure-with-salvage-pickups": {
      slug: "salvage-orbit-ruins-neon-pressure-with-salvage-pickups",
      title: "Salvage Orbit Ruins Neon Pressure With Salvage Pickups",
      section: "prototypes",
      kind: "Prototype",
      shortDescription:
        "Greyboxed arcade game generated for salvage orbit ruins neon pressure with salvage pickups.",
      description:
        "salvage orbit ruins neon pressure with salvage pickups",
      image:
        "/images/projects/salvage-orbit-ruins-neon-pressure-with-salvage-pickups.svg",
      features: [
        "JSON-driven content",
        "Dodge And Route",
        "Timed Swap",
        "Pickup Pressure",
      ],
      technologies: ["JSON", "Shared Runtime", "Prototype"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/salvage-orbit-ruins-neon-pressure-with-salvage-pickups/",
          style: "secondary",
        },
      ],
    },
    "neural-network-pulse-dodger": {
      slug: "neural-network-pulse-dodger",
      title: "Neural Network Pulse Dodger",
      section: "prototypes",
      kind: "Prototype",
      shortDescription:
        "Greyboxed arcade game generated for Neural Network Pulse Dodger.",
      description:
        "Neural Network Pulse Dodger",
      image:
        "/images/projects/neural-network-pulse-dodger.svg",
      features: [
        "JSON-driven content",
        "Dodge And Route",
        "Timed Swap",
        "Pickup Pressure",
      ],
      technologies: ["JSON", "Shared Runtime", "Prototype"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/neural-network-pulse-dodger/",
          style: "secondary",
        },
      ],
    },
    "crystal-comet-run-prismatic-neon-crystals-with-celestial-ste-momentum-racing-maze-reconfiguration-temporal-phasing-high-speed-comet-runs-through-shifting-crystal-mazes-whe-tense-neon": {
      slug: "crystal-comet-run-prismatic-neon-crystals-with-celestial-ste-momentum-racing-maze-reconfiguration-temporal-phasing-high-speed-comet-runs-through-shifting-crystal-mazes-whe-tense-neon",
      title: "Crystal Comet Run Prismatic Neon Crystals With Celestial Ste Momentum Racing; Maze Reconfiguration; Temporal Phasing High-Speed Comet Runs Through Shifting Crystal Mazes Whe Tense Neon",
      section: "prototypes",
      kind: "Prototype",
      shortDescription:
        "Greyboxed arcade game generated for Crystal Comet Run Prismatic neon crystals with celestial ste Momentum racing; maze reconfiguration; temporal phasing High-speed comet runs through shifting crystal mazes whe tense neon.",
      description:
        "Crystal Comet Run Prismatic neon crystals with celestial ste Momentum racing; maze reconfiguration; temporal phasing High-speed comet runs through shifting crystal mazes whe tense neon",
      image:
        "/images/projects/crystal-comet-run-prismatic-neon-crystals-with-celestial-ste-momentum-racing-maze-reconfiguration-temporal-phasing-high-speed-comet-runs-through-shifting-crystal-mazes-whe-tense-neon.svg",
      features: [
        "JSON-driven content",
        "Momentum Racing; Maze Reconfiguration; Temporal Phasing",
        "Prismatic Neon Crystals With Celestial Ste",
        "High-Speed Comet Runs Through Shifting Crystal Mazes Whe",
      ],
      technologies: ["JSON", "Shared Runtime", "Prototype"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/crystal-comet-run-prismatic-neon-crystals-with-celestial-ste-momentum-racing-maze-reconfiguration-temporal-phasing-high-speed-comet-runs-through-shifting-crystal-mazes-whe-tense-neon/",
          style: "secondary",
        },
      ],
    },
    "beacon-run-relay-courier-neon-plasma-city-inertial-courier-with-beam-routi-high-speed-courier-races-deliver-urgent": {
      slug: "beacon-run-relay-courier-neon-plasma-city-inertial-courier-with-beam-routi-high-speed-courier-races-deliver-urgent",
      title: "Beacon Run — Relay Courier Neon Plasma City Inertial Courier With Beam-Routi High-Speed Courier Races Deliver Urgent",
      section: "prototypes",
      kind: "Prototype",
      shortDescription:
        "Greyboxed arcade game generated for Beacon Run — Relay Courier neon plasma city inertial courier with beam-routi High-speed courier races deliver urgent.",
      description:
        "Beacon Run — Relay Courier neon plasma city inertial courier with beam-routi High-speed courier races deliver urgent",
      image:
        "/images/projects/beacon-run-relay-courier-neon-plasma-city-inertial-courier-with-beam-routi-high-speed-courier-races-deliver-urgent.svg",
      features: [
        "JSON-driven content",
        "Inertial Courier With Beam-Routi",
        "Neon Plasma City",
        "High-Speed Courier Races Deliver",
      ],
      technologies: ["JSON", "Shared Runtime", "Prototype"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/beacon-run-relay-courier-neon-plasma-city-inertial-courier-with-beam-routi-high-speed-courier-races-deliver-urgent/",
          style: "secondary",
        },
      ],
    },
    "aurora-vaultrun-bioluminescent-aurora-meets-beat-matching-tumblers-phase-sh-endless-rhythm-run-through-shift-neo-noir": {
      slug: "aurora-vaultrun-bioluminescent-aurora-meets-beat-matching-tumblers-phase-sh-endless-rhythm-run-through-shift-neo-noir",
      title: "Aurora Vaultrun Bioluminescent Aurora Meets Beat-Matching Tumblers, Phase-Sh Endless Rhythm-Run Through Shift Neo-Noir",
      section: "prototypes",
      kind: "Prototype",
      shortDescription:
        "Greyboxed arcade game generated for Aurora Vaultrun bioluminescent aurora meets beat-matching tumblers, phase-sh endless rhythm-run through shift neo-noir.",
      description:
        "Aurora Vaultrun bioluminescent aurora meets beat-matching tumblers, phase-sh endless rhythm-run through shift neo-noir",
      image:
        "/images/projects/aurora-vaultrun-bioluminescent-aurora-meets-beat-matching-tumblers-phase-sh-endless-rhythm-run-through-shift-neo-noir.svg",
      features: [
        "JSON-driven content",
        "Beat-Matching Tumblers, Phase-Sh",
        "Bioluminescent Aurora Meets",
        "Endless Rhythm-Run Through Shift",
      ],
      technologies: ["JSON", "Shared Runtime", "Prototype"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/aurora-vaultrun-bioluminescent-aurora-meets-beat-matching-tumblers-phase-sh-endless-rhythm-run-through-shift-neo-noir/",
          style: "secondary",
        },
      ],
    },
    "ember-harbor-rescue-drift-charred-industrial-docks-wit-grapple-tether-physics-with-time-fast-side-scroll-rescue-runs-tha-urgent-heroic": {
      slug: "ember-harbor-rescue-drift-charred-industrial-docks-wit-grapple-tether-physics-with-time-fast-side-scroll-rescue-runs-tha-urgent-heroic",
      title: "Ember Harbor Rescue-Drift Charred Industrial Docks Wit Grapple-Tether Physics With Time Fast Side-Scroll Rescue Runs Tha Urgent Heroic",
      section: "prototypes",
      kind: "Prototype",
      shortDescription:
        "Greyboxed arcade game generated for Ember Harbor Rescue-Drift Charred industrial docks wit Grapple-tether physics with time Fast side-scroll rescue runs tha urgent heroic.",
      description:
        "Ember Harbor Rescue-Drift Charred industrial docks wit Grapple-tether physics with time Fast side-scroll rescue runs tha urgent heroic",
      image:
        "/images/projects/ember-harbor-rescue-drift-charred-industrial-docks-wit-grapple-tether-physics-with-time-fast-side-scroll-rescue-runs-tha-urgent-heroic.svg",
      features: [
        "JSON-driven content",
        "Grapple-Tether Physics With Time",
        "Charred Industrial Docks Wit",
        "Fast Side-Scroll Rescue Runs Tha",
      ],
      technologies: ["JSON", "Shared Runtime", "Prototype"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/ember-harbor-rescue-drift-charred-industrial-docks-wit-grapple-tether-physics-with-time-fast-side-scroll-rescue-runs-tha-urgent-heroic/",
          style: "secondary",
        },
      ],
    },
    "harbor-sprint-retro-seaport-reflex-lane-runner-with-pulse-gr-short-rhythmic-lane-runs-dodge-energetic": {
      slug: "harbor-sprint-retro-seaport-reflex-lane-runner-with-pulse-gr-short-rhythmic-lane-runs-dodge-energetic",
      title: "Harbor Sprint Retro Seaport Reflex Lane-Runner With Pulse-Gr Short Rhythmic Lane Runs: Dodge Energetic",
      section: "prototypes",
      kind: "Prototype",
      shortDescription:
        "Greyboxed arcade game generated for Harbor Sprint Retro seaport Reflex lane-runner with pulse-gr Short rhythmic lane runs: dodge energetic.",
      description:
        "Harbor Sprint Retro seaport Reflex lane-runner with pulse-gr Short rhythmic lane runs: dodge energetic",
      image:
        "/images/projects/harbor-sprint-retro-seaport-reflex-lane-runner-with-pulse-gr-short-rhythmic-lane-runs-dodge-energetic.svg",
      features: [
        "JSON-driven content",
        "Reflex Lane-Runner With Pulse-Gr",
        "Retro Seaport",
        "Short Rhythmic Lane Runs: Dodge",
      ],
      technologies: ["JSON", "Shared Runtime", "Prototype"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/harbor-sprint-retro-seaport-reflex-lane-runner-with-pulse-gr-short-rhythmic-lane-runs-dodge-energetic/",
          style: "secondary",
        },
      ],
    },
    "neon-orbital-courier-neon-cyberpunk-astro-minimal-timed-dash-windows-with-orbit-at-short-high-score-courier-runs-wi-urgent": {
      slug: "neon-orbital-courier-neon-cyberpunk-astro-minimal-timed-dash-windows-with-orbit-at-short-high-score-courier-runs-wi-urgent",
      title: "Neon Orbital Courier Neon Cyberpunk Astro-Minimal Timed Dash Windows With Orbit At Short High-Score Courier Runs Wi Urgent",
      section: "prototypes",
      kind: "Prototype",
      shortDescription:
        "Greyboxed arcade game generated for Neon Orbital Courier neon cyberpunk astro-minimal timed dash windows with orbit at short high-score courier runs wi urgent.",
      description:
        "Neon Orbital Courier neon cyberpunk astro-minimal timed dash windows with orbit at short high-score courier runs wi urgent",
      image:
        "/images/projects/neon-orbital-courier-neon-cyberpunk-astro-minimal-timed-dash-windows-with-orbit-at-short-high-score-courier-runs-wi-urgent.svg",
      features: [
        "JSON-driven content",
        "Timed Dash Windows With Orbit At",
        "Neon Cyberpunk Astro-Minimal",
        "Short High-Score Courier Runs Wi",
      ],
      technologies: ["JSON", "Shared Runtime", "Prototype"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/neon-orbital-courier-neon-cyberpunk-astro-minimal-timed-dash-windows-with-orbit-at-short-high-score-courier-runs-wi-urgent/",
          style: "secondary",
        },
      ],
    },
    "neon-phase-courier-auto-ru-neon-cyberpunk-pixel-with-bi-auto-run-lane-switching-with-tim-compact-scope-short-lane-strips-urgent-neon-pulse": {
      slug: "neon-phase-courier-auto-ru-neon-cyberpunk-pixel-with-bi-auto-run-lane-switching-with-tim-compact-scope-short-lane-strips-urgent-neon-pulse",
      title: "Neon Phase Courier — Auto-Ru Neon Cyberpunk Pixel With Bi Auto-Run Lane-Switching With Tim Compact Scope: Short Lane Strips Urgent Neon Pulse",
      section: "prototypes",
      kind: "Prototype",
      shortDescription:
        "Greyboxed arcade game generated for Neon Phase Courier — auto-ru Neon cyberpunk pixel with bi Auto-run lane-switching with tim Compact scope: short lane strips urgent neon pulse.",
      description:
        "Neon Phase Courier — auto-ru Neon cyberpunk pixel with bi Auto-run lane-switching with tim Compact scope: short lane strips urgent neon pulse",
      image:
        "/images/projects/neon-phase-courier-auto-ru-neon-cyberpunk-pixel-with-bi-auto-run-lane-switching-with-tim-compact-scope-short-lane-strips-urgent-neon-pulse.svg",
      features: [
        "JSON-driven content",
        "Auto-Run Lane-Switching With Tim",
        "Neon Cyberpunk Pixel With Bi",
        "Compact Scope: Short Lane Strips",
      ],
      technologies: ["JSON", "Shared Runtime", "Prototype"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/neon-phase-courier-auto-ru-neon-cyberpunk-pixel-with-bi-auto-run-lane-switching-with-tim-compact-scope-short-lane-strips-urgent-neon-pulse/",
          style: "secondary",
        },
      ],
    },
    "campfire-cozy-dodge-lanterns": {
      slug: "campfire-cozy-dodge-lanterns",
      title: "Campfire Cozy Dodge Lanterns",
      section: "prototypes",
      kind: "Prototype",
      shortDescription:
        "Greyboxed arcade game generated for campfire cozy dodge lanterns.",
      description:
        "campfire cozy dodge lanterns",
      image:
        "/images/projects/campfire-cozy-dodge-lanterns.svg",
      features: [
        "JSON-driven content",
        "Dodge",
        "Cozy",
        "Lanterns",
      ],
      technologies: ["JSON", "Shared Runtime", "Prototype"],
      links: [
        {
          label: "Open Prototype",
          href: "Pages/campfire-cozy-dodge-lanterns/",
          style: "secondary",
        },
      ],
    },
    pillow: {
      slug: "pillow",
      title: "Pillow",
      section: "game-dev",
      kind: "XR",
      shortDescription:
        "Mixed reality app designed specifically for comfortable headset use while lying down.",
      description:
        "Pillow rethinks posture and presence for mixed reality by designing around in-bed use. The experience combines interactive dreams, social play, and comfort-first interaction patterns tailored for a different physical context.",
      image:
        "https://crimsonwheeler.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fb0930ce5-2382-4810-8e92-3ece8545d32c%2Ffa86501f-431e-40ab-b203-7253a4555bb5%2FScreenshot_2024-03-05_164431.png?table=block&id=195caa1b-d33a-8127-8276-ded6d2d557bd&spaceId=b0930ce5-2382-4810-8e92-3ece8545d32c&width=2000&userId=&cache=v2",
      features: [
        "Four distinct dream-like interactive experiences",
        "Single-player and 2-player co-op support",
        "Ceiling-first interactions for reclined play",
        "Comfort-oriented MR design choices",
      ],
      technologies: [
        "Unity",
        "Meta Quest",
        "Mixed Reality",
        "Meta Presence Platform",
        "Multiplayer",
      ],
      links: [
        {
          label: "Visit Project",
          href: "https://pillow.social",
          style: "secondary",
          external: true,
        },
      ],
    },
    watson: {
      slug: "watson",
      title: "Watson",
      section: "game-dev",
      kind: "XR",
      shortDescription:
        "Mixed reality investigation tool with persistent scene data and hand-tracked interaction.",
      description:
        "Built during the Meta Presence Platform Hackathon, Watson explores how passthrough MR and persistent data can support investigative workflows. The concept centers on virtual tools, evidence review, and continuity across sessions.",
      image:
        "https://crimsonwheeler.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fb0930ce5-2382-4810-8e92-3ece8545d32c%2F5edf6f79-5eef-4b66-b459-ac6b7b9bd838%2Fimage_(4).png?table=block&id=195caa1b-d33a-816f-b866-dcc06333e792&spaceId=b0930ce5-2382-4810-8e92-3ece8545d32c&width=2000&userId=&cache=v2",
      features: [
        "Hand-tracked investigation workflow",
        "Persistent scene data for later review",
        "Virtual toolset for evidence analysis",
        "Passthrough MR designed for practical context",
      ],
      technologies: [
        "Unity",
        "Meta Presence Platform",
        "Hand Tracking",
        "Meta Quest",
        "Mixed Reality",
      ],
      links: [],
    },
    "dancing-with-the-ancestors": {
      slug: "dancing-with-the-ancestors",
      title: "Dancing with the Ancestors",
      section: "game-dev",
      kind: "XR",
      shortDescription:
        "Interactive AR performance experience produced for a live cultural event.",
      description:
        "An interactive mobile AR performance experience built for the Aryzon headset and prepared for the LA Music Center's Black Bar Social. The work covered technical leadership, content workflow, and production execution across the app lifecycle.",
      image:
        "https://crimsonwheeler.notion.site/image/attachment%3A51ed88a5-e66d-43b1-a986-93e2ed09b262%3Aimage.png?table=block&id=195caa1b-d33a-81bc-9992-df110be656a2&spaceId=b0930ce5-2382-4810-8e92-3ece8545d32c&width=2000&userId=&cache=v2",
      features: [
        "Co-located interactive mobile experience",
        "Custom shader and VFX work for volumetric media",
        "Content insertion workflow for the development team",
        "Optimized environments per performer and scene",
      ],
      technologies: [
        "Unity",
        "Aryzon SDK",
        "Depthkit",
        "Mobile AR",
        "Volumetric Capture",
      ],
      links: [],
    },
    "oticon-audio-experience": {
      slug: "oticon-audio-experience",
      title: "Oticon Audio Experience",
      section: "game-dev",
      kind: "XR",
      shortDescription:
        "Audio-first VR demonstration built to communicate hearing aid value through immersion.",
      description:
        "A VR experience designed to compare Oticon hearing aid features against competitors through embodied audio demonstrations. The project combined story progression, device optimization, and branding goals in one tightly scoped immersive product.",
      image:
        "https://crimsonwheeler.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fb0930ce5-2382-4810-8e92-3ece8545d32c%2Ff790d028-41d5-4f53-9896-7c3832b99196%2Fimage_(1).png?table=block&id=195caa1b-d33a-81e1-8f04-d1cb3d9b7842&spaceId=b0930ce5-2382-4810-8e92-3ece8545d32c&width=2000&userId=&cache=v2",
      features: [
        "Audio-focused story progression system",
        "Quest-ready immersive comparison experience",
        "Real-time demonstration of product differences",
        "Delivery shaped around brand and stakeholder goals",
      ],
      technologies: [
        "Unity",
        "VR Interaction Framework",
        "Meta Quest",
        "3D Audio",
        "CI/CD",
      ],
      links: [],
    },
    "onnx-runtime-tooling": {
      slug: "onnx-runtime-tooling",
      title: "ONNX Runtime Tooling",
      section: "agentic-engineering",
      kind: "Agentic Engineering",
      shortDescription:
        "Inference tooling focused on packaging models into dependable local execution flows.",
      description:
        "A tooling track centered on getting models out of notebooks and into reliable runtime environments. The work emphasizes predictable execution, manageable model packaging, and practical interfaces for using local inference in production-minded workflows.",
      image:
        "/images/projects/onnx-runtime-tooling.svg",
      features: [
        "Runtime-aware packaging for local model execution",
        "Operator-facing tooling rather than notebook-only demos",
        "Clear handoff between model assets and application code",
        "Performance-conscious implementation patterns",
      ],
      technologies: [
        "ONNX",
        "Runtime Integration",
        "Local Inference",
        "Tooling",
      ],
      links: [],
    },
    "agent-workflow-orchestration": {
      slug: "agent-workflow-orchestration",
      title: "Agent Workflow Orchestration",
      section: "agentic-engineering",
      kind: "Agentic Engineering",
      shortDescription:
        "Multi-step agent workflows that connect tools, prompts, and system actions into usable operations.",
      description:
        "An applied agent systems track focused on orchestration rather than isolated prompts. The emphasis is on bounded workflows, tool calling, and operational clarity so human users can trust what the system is doing and where intervention belongs.",
      image:
        "/images/projects/agent-workflow-orchestration.svg",
      features: [
        "Tool-connected multi-step workflows",
        "Clear separation between decision logic and execution",
        "Human-visible checkpoints for operator trust",
        "Structured outputs suited for downstream systems",
      ],
      technologies: [
        "Agents",
        "Workflow Design",
        "Prompt Systems",
        "Automation",
      ],
      links: [],
    },
    "bot-operations-tooling": {
      slug: "bot-operations-tooling",
      title: "Bot Operations Tooling",
      section: "agentic-engineering",
      kind: "Agentic Engineering",
      shortDescription:
        "Bot and automation infrastructure designed around repeatable operations rather than novelty.",
      description:
        "A systems-oriented approach to bots and operator tooling, built to reduce manual work while keeping workflows legible. The focus is on automation surfaces, action safety, and interfaces that fit day-to-day use by technical teams.",
      image:
        "/images/projects/bot-operations-tooling.svg",
      features: [
        "Operator-first automation flows",
        "Bot actions shaped around repeatable task patterns",
        "Safety-minded execution boundaries",
        "Interfaces intended for daily technical operations",
      ],
      technologies: [
        "Bots",
        "Automation",
        "Operations Tooling",
        "System Design",
      ],
      links: [],
    },
  },
};
