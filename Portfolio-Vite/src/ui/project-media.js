let cleanupActiveVideos = () => {};

export function renderProjectMedia(project, className) {
  if (!project.media) return null;
  return `
    <figure class="${className} project-video-media" data-project-video>
      <img
        class="project-video-poster"
        src="${project.media.poster}"
        alt="${project.title} gameplay still"
        loading="lazy"
      />
      <video
        class="project-video-element"
        muted
        loop
        playsinline
        preload="none"
        poster="${project.media.poster}"
        aria-label="${project.media.caption}"
      >
        <source src="${project.media.webm}" type="video/webm" />
        <source src="${project.media.mp4}" type="video/mp4" />
      </video>
      <figcaption class="visually-hidden">${project.media.caption}</figcaption>
    </figure>
  `;
}

export function hydrateProjectVideos(root) {
  cleanupActiveVideos();
  const wrappers = Array.from(root.querySelectorAll("[data-project-video]"));
  if (!wrappers.length) {
    cleanupActiveVideos = () => {};
    return;
  }

  const controller = new AbortController();
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const intersections = new Map();
  let observer;

  const refreshPlayback = () => {
    const ranked = wrappers
      .filter((wrapper) => intersections.get(wrapper) > 0.2)
      .sort((a, b) => (intersections.get(b) || 0) - (intersections.get(a) || 0))
      .slice(0, 2);
    wrappers.forEach((wrapper) => {
      const video = wrapper.querySelector("video");
      if (!video) return;
      const shouldPlay = !reducedMotion.matches && !document.hidden && ranked.includes(wrapper) && wrapper.classList.contains("video-ready");
      if (shouldPlay) {
        video.play().catch(() => wrapper.classList.remove("video-ready"));
      } else {
        video.pause();
      }
    });
  };

  wrappers.forEach((wrapper) => {
    const video = wrapper.querySelector("video");
    if (!video) return;
    video.addEventListener("loadeddata", () => {
      wrapper.classList.add("video-ready");
      refreshPlayback();
    }, { signal: controller.signal });
    video.addEventListener("error", () => {
      wrapper.classList.remove("video-ready");
      wrapper.classList.add("video-unavailable");
    }, { signal: controller.signal });
  });

  observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      intersections.set(entry.target, entry.intersectionRatio);
      const video = entry.target.querySelector("video");
      if (video && entry.intersectionRatio > 0.2 && video.preload === "none") {
        video.preload = "metadata";
        video.load();
      }
    });
    refreshPlayback();
  }, { rootMargin: "120px 0px", threshold: [0, 0.2, 0.55, 0.8] });
  wrappers.forEach((wrapper) => observer.observe(wrapper));
  document.addEventListener("visibilitychange", refreshPlayback, { signal: controller.signal });
  reducedMotion.addEventListener("change", refreshPlayback, { signal: controller.signal });

  cleanupActiveVideos = () => {
    observer?.disconnect();
    controller.abort();
    wrappers.forEach((wrapper) => wrapper.querySelector("video")?.pause());
  };
}
