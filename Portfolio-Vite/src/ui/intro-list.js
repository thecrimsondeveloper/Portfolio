export function renderIntroList(page) {
  const points = Array.isArray(page.introPoints) ? page.introPoints.filter(Boolean) : [];
  if (!points.length) return "";

  return `
    <section class="intro-list">
      ${points
        .map(
          (point) => `
            <div class="intro-list-item">
              <h2 class="intro-list-heading">${point.pair}</h2>
              <p class="content-section-copy">${point.text}</p>
            </div>
          `
        )
        .join("")}
    </section>
  `;
}
