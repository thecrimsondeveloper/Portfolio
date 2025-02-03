// Handle hover and click animations for project links
const projectLinks = document.querySelectorAll(".project-link");

if (projectLinks && projectLinks.length > 0) {
  projectLinks.forEach((link) => {
    let hoverTimeout;

    link.addEventListener("mouseenter", () => {
      link.classList.add("progressing");
      const progressDuration =
        parseFloat(getComputedStyle(link).getPropertyValue("--progress-duration")) * 1000;
      hoverTimeout = setTimeout(() => {
        window.location.href = link.href;
      }, progressDuration); // Trigger navigation after animation
    });

    link.addEventListener("mouseleave", () => {
      link.classList.remove("progressing");
      clearTimeout(hoverTimeout); // Clear timeout to avoid unintended navigation
    });

    link.addEventListener("click", (event) => {
      event.preventDefault(); // Prevent immediate navigation
      link.classList.add("clicked");
      setTimeout(() => {
        window.location.href = link.href;
      }, 300); // Small delay for visual feedback
    });
  });
} else {
  console.warn("No project links found on the page.");
}
