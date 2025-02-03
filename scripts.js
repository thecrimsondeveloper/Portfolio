// Create Starfield in the Background
const starContainer = document.getElementById("threejs-scene");

// Set up canvas
const canvas = document.createElement("canvas");
const ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
starContainer.appendChild(canvas);

// Create stars
const stars = [];
const starCount = 500; // Number of stars
for (let i = 0; i < starCount; i++) {
  stars.push({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    radius: Math.random() * 2,
    speed: Math.random() * 0.5,
  });
}

// Animate stars
function drawStars() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "white";

  stars.forEach((star) => {
    star.y += star.speed;
    if (star.y > canvas.height) {
      star.y = 0;
      star.x = Math.random() * canvas.width;
    }
    ctx.beginPath();
    ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
    ctx.fill();
  });

  requestAnimationFrame(drawStars);
}
drawStars();

// Add hover animations to project links
const projectLinks = document.querySelectorAll(".project-link");

projectLinks.forEach((link) => {
  link.style.position = "relative";
  link.style.display = "inline-block";
  link.style.padding = "10px 20px";
  link.style.margin = "10px";
  link.style.border = "2px solid white";
  link.style.borderRadius = "5px";
  link.style.color = "white";
  link.style.textDecoration = "none";
  link.style.transition = "all 0.3s ease-in-out";

  const progressBar = document.createElement("div");
  progressBar.style.position = "absolute";
  progressBar.style.top = "0";
  progressBar.style.left = "0";
  progressBar.style.width = "0%";
  progressBar.style.height = "100%";
  progressBar.style.backgroundColor = "rgba(255, 102, 0, 0.5)";
  progressBar.style.transition = "width 5s linear"; // Matches the 5-second delay
  progressBar.style.borderRadius = "5px";
  link.appendChild(progressBar);

  let hoverTimeout = null; // Ensure the timeout reference is accessible

  link.addEventListener("mouseenter", () => {
    // Prevent multiple triggers
    if (!hoverTimeout) {
      progressBar.style.width = "100%"; // Start progress bar animation
      hoverTimeout = setTimeout(() => {
        window.location.href = link.href; // Navigate after 5 seconds
      }, 5000); // 5 seconds
    }
  });

  link.addEventListener("mouseleave", () => {
    // Reset progress bar and clear timeout
    progressBar.style.width = "0%";
    clearTimeout(hoverTimeout);
    hoverTimeout = null; // Reset timeout reference
  });

  link.addEventListener("click", (event) => {
    event.preventDefault(); // Prevent immediate navigation
    window.location.href = link.href; // Navigate on click
  });
});


// Handle window resize
window.addEventListener("resize", () => {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
});
