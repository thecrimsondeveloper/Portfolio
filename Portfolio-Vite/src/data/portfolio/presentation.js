const MEDIA_BASE_URL = import.meta.env?.VITE_PORTFOLIO_MEDIA_BASE_URL?.trim().replace(/\/+$/, "") || "";

const gameplayPresentation = {
  "sky-drifter-dragon-edition": ["Sky Drifter: Dragon Edition", "sky-drifter-dragon-edition", "Flight between glowing lanes while dodging incoming sky hazards."],
  "signal-runner": ["Signal Runner", "signal-runner", "Lane changes avoid a stream of red signal hazards as the pace rises."],
  "orbit-pop": ["Orbit Pop", "orbit-pop", "The cursor tracks moving orbital targets and chains successful pops."],
  "grid-pulse": ["Grid Pulse", "grid-pulse", "Timed inputs energize a reactive neon grid and build score."],
  "lab-rift": ["Lab Rift", "lab-rift", "The player navigates a rift chamber, gathers shards, and opens the exit."],
  "phase-drop": ["Phase Drop", "phase-drop", "Lane swaps and phase timing avoid falling neon blocks."],
  "drift-harbor": ["Drift Harbor", "drift-harbor", "Pointer steering guides a skiff through currents toward harbor markers."],
  "pulse-drift": ["Pulse Drift", "pulse-drift", "Beat-matched inputs trigger visible pulses and increase the score."],
  "echo-loop": ["Echo Loop", "echo-loop", "A revealed four-pad pattern is repeated successfully from memory."],
  "playtest-studio": ["Playtest Studio", "playtest-studio", "Timed studio inputs light grid cells and produce score feedback."],
  "playtest-studio-with-presets-and-replay": ["Playtest Studio Plus", "playtest-studio-plus", "Moving orbital targets are selected to build a visible combo."],
  "physics-draw-replay": ["Physics Draw Replay", "physics-draw-replay", "A displayed input pattern is repeated with A, S, D, and F."],
  "neon-lane-runner": ["Neon Lane Runner", "neon-lane-runner", "Fast lane changes thread between falling neon hazards."],
  "drift-beat-harbor": ["Harbor Beat", "harbor-beat", "Beat-timed inputs keep a glowing harbor rhythm active."],
  "sandstorm-memory-harbor": ["Sandstorm Harbor", "sandstorm-harbor", "A skiff follows pointer movement through sand toward harbor markers."],
  "crystal-orbit-salvage": ["Orbit Salvage", "orbit-salvage", "Precision clicks recover moving salvage cores in orbit."],
  "help-panel-harbor": ["Harbor Help Run", "harbor-help-run", "Pointer steering collects harbor markers and advances the run."],
  "salvage-orbit-ruins-neon-pressure-with-salvage-pickups": ["Salvage Orbit", "salvage-orbit", "Targeted salvage pickups build score amid orbital pressure."],
  "neural-network-pulse-dodger": ["Neural Pulse", "neural-pulse", "Timed inputs stabilize a pulsing neural grid."],
  "crystal-comet-run-prismatic-neon-crystals-with-celestial-ste-momentum-racing-maze-reconfiguration-temporal-phasing-high-speed-comet-runs-through-shifting-crystal-mazes-whe-tense-neon": ["Comet Drift", "comet-drift", "A comet shifts lanes through a fast neon crystal corridor."],
  "beacon-run-relay-courier-neon-plasma-city-inertial-courier-with-beam-routi-high-speed-courier-races-deliver-urgent": ["Neon Relay", "neon-relay", "A courier changes lanes while crossing a neon relay route."],
  "aurora-vaultrun-bioluminescent-aurora-meets-beat-matching-tumblers-phase-sh-endless-rhythm-run-through-shift-neo-noir": ["Aurora Run", "aurora-run", "Lane movement carries a runner through a glowing aurora course."],
  "ember-harbor-rescue-drift-charred-industrial-docks-wit-grapple-tether-physics-with-time-fast-side-scroll-rescue-runs-tha-urgent-heroic": ["Ember Rescue", "ember-rescue", "A rescue craft steers between ember-harbor markers."],
  "harbor-sprint-retro-seaport-reflex-lane-runner-with-pulse-gr-short-rhythmic-lane-runs-dodge-energetic": ["Seaport Sprint", "seaport-sprint", "Quick lane shifts dodge traffic during a seaport sprint."],
  "neon-orbital-courier-neon-cyberpunk-astro-minimal-timed-dash-windows-with-orbit-at-short-high-score-courier-runs-wi-urgent": ["Orbital Courier", "orbital-courier", "A neon courier changes lanes through timed orbital windows."],
  "neon-phase-courier-auto-ru-neon-cyberpunk-pixel-with-bi-auto-run-lane-switching-with-tim-compact-scope-short-lane-strips-urgent-neon-pulse": ["Phase Courier", "phase-courier", "Precision lane switching keeps an auto-running courier moving."],
  "campfire-cozy-dodge-lanterns": ["Lantern Drift", "lantern-drift", "A cozy runner changes lanes between drifting lantern hazards."],
};

function buildMedia(mediaSlug, caption) {
  if (!MEDIA_BASE_URL) return null;
  const root = `${MEDIA_BASE_URL}/${mediaSlug}`;
  return {
    poster: `${root}/poster.webp`,
    webm: `${root}/gameplay-15s.webm`,
    mp4: `${root}/gameplay-15s.mp4`,
    caption,
    duration: 15,
  };
}

export function applyProjectPresentation(projects) {
  return Object.fromEntries(
    Object.entries(projects).map(([key, project]) => {
      const presentation = gameplayPresentation[key];
      if (!presentation) return [key, project];
      const [title, mediaSlug, caption] = presentation;
      const media = buildMedia(mediaSlug, caption);
      return [
        key,
        {
          ...project,
          title,
          image: media?.poster || project.image,
          media,
          links: project.links.filter((link) => !String(link.href).startsWith("Pages/")),
        },
      ];
    })
  );
}

