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
  projects: `
    <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path d="M4 4h7v7H4V4Zm9 0h7v7h-7V4ZM4 13h7v7H4v-7Zm9 0h7v7h-7v-7Z"></path>
    </svg>
  `,
};

export const nav = [
    { id: "full-stack", label: "Work", icon: navIcons["full-stack"] },
    { id: "projects", label: "Projects", icon: navIcons.projects },
    { id: "connect", label: "About", icon: navIcons.connect },
    { id: "prototypes", label: "Arcade", icon: navIcons.prototypes },
    { id: "settings", label: "Settings", icon: navIcons.settings },
  ];
