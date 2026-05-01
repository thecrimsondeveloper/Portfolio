export const projects = {
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
        "/images/projects/screenshots-2026-05-01/signal-runner.png",
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
        "/images/projects/screenshots-2026-05-01/orbit-pop.png",
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
        "/images/projects/screenshots-2026-05-01/grid-pulse.png",
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
        "/images/projects/screenshots-2026-05-01/lab-rift.png",
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
        "/images/projects/screenshots-2026-05-01/phase-drop.png",
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
        "/images/projects/screenshots-2026-05-01/drift-harbor.png",
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
        "/images/projects/screenshots-2026-05-01/pulse-drift.png",
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
        "/images/projects/screenshots-2026-05-01/echo-loop.png",
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
        "/images/projects/screenshots-2026-05-01/playtest-studio.png",
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
        "/images/projects/screenshots-2026-05-01/playtest-studio-with-presets-and-replay.png",
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
        "/images/projects/screenshots-2026-05-01/physics-draw-replay.png",
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
        "/images/projects/screenshots-2026-05-01/neon-lane-runner.png",
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
        "/images/projects/screenshots-2026-05-01/drift-beat-harbor.png",
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
        "/images/projects/screenshots-2026-05-01/sandstorm-memory-harbor.png",
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
        "/images/projects/screenshots-2026-05-01/crystal-orbit-salvage.png",
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
        "/images/projects/screenshots-2026-05-01/help-panel-harbor.png",
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
        "/images/projects/screenshots-2026-05-01/salvage-orbit-ruins-neon-pressure-with-salvage-pickups.png",
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
        "/images/projects/screenshots-2026-05-01/neural-network-pulse-dodger.png",
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
        "/images/projects/screenshots-2026-05-01/beacon-run-relay-courier-neon-plasma-city-inertial-courier-with-beam-routi-high-speed-courier-races-deliver-urgent.png",
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
        "/images/projects/screenshots-2026-05-01/aurora-vaultrun-bioluminescent-aurora-meets-beat-matching-tumblers-phase-sh-endless-rhythm-run-through-shift-neo-noir.png",
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
        "/images/projects/screenshots-2026-05-01/ember-harbor-rescue-drift-charred-industrial-docks-wit-grapple-tether-physics-with-time-fast-side-scroll-rescue-runs-tha-urgent-heroic.png",
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
        "/images/projects/screenshots-2026-05-01/harbor-sprint-retro-seaport-reflex-lane-runner-with-pulse-gr-short-rhythmic-lane-runs-dodge-energetic.png",
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
        "/images/projects/screenshots-2026-05-01/neon-orbital-courier-neon-cyberpunk-astro-minimal-timed-dash-windows-with-orbit-at-short-high-score-courier-runs-wi-urgent.png",
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
        "/images/projects/screenshots-2026-05-01/neon-phase-courier-auto-ru-neon-cyberpunk-pixel-with-bi-auto-run-lane-switching-with-tim-compact-scope-short-lane-strips-urgent-neon-pulse.png",
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
        "/images/projects/screenshots-2026-05-01/campfire-cozy-dodge-lanterns.png",
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
  };
