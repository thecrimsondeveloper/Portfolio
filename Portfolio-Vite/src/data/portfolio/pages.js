export const pages = {
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
  };
