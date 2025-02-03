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

  // Add a border animation container
  const borderAnimation = document.createElement("div");
  borderAnimation.style.position = "absolute";
  borderAnimation.style.top = "0";
  borderAnimation.style.left = "0";
  borderAnimation.style.width = "100%";
  borderAnimation.style.height = "100%";
  borderAnimation.style.border = "2px solid orange";
  borderAnimation.style.borderRadius = "5px";
  borderAnimation.style.boxSizing = "border-box";
  borderAnimation.style.clipPath = "polygon(0% 0%, 0% 0%, 0% 100%, 0% 100%)"; // Start at 0%
  borderAnimation.style.transition = "clip-path 5s linear"; // 5 seconds for full animation
  link.appendChild(borderAnimation);

  let hoverTimeout = null;

  link.addEventListener("mouseenter", () => {
    // Trigger the border animation
    borderAnimation.style.clipPath = "polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)"; // Full outline
    if (!hoverTimeout) {
      hoverTimeout = setTimeout(() => {
        window.location.href = link.href; // Navigate after animation
      }, 5000); // 5 seconds
    }
  });

  link.addEventListener("mouseleave", () => {
    // Reset the border animation
    borderAnimation.style.clipPath = "polygon(0% 0%, 0% 0%, 0% 100%, 0% 100%)";
    if (hoverTimeout) {
      clearTimeout(hoverTimeout);
      hoverTimeout = null;
    }
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
