const sections = document.querySelectorAll("section[id]");
const navLinks = document.querySelectorAll("nav a");
const collapseBtns = document.querySelectorAll(".collapse-btn");
const hamburger = document.getElementById("hamburger");
const navLinksContainer = document.getElementById("nav-links");
const navItems = document.querySelectorAll(".nav-links a");
const navbar = document.getElementById("navbar");
const logo = document.querySelector(".logo");

function updateActiveLink() {
  let current = "";
  const scrollPos = window.scrollY + 180;

  sections.forEach(section => {
    const sectionTop = section.offsetTop - 120;
    const sectionBottom = sectionTop + section.offsetHeight;

    if (scrollPos >= sectionTop && scrollPos < sectionBottom) {
      current = section.getAttribute("id");
    }
  });

  if (!current && sections.length) {
    current = sections[0].getAttribute("id");
  }

  navLinks.forEach(link => {
    link.classList.remove("active");
    if (link.getAttribute("href") === "#" + current) {
      link.classList.add("active");
    }
  });
}

collapseBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    const content = btn.nextElementSibling;
    if (content) {
      content.style.display = content.style.display === "block" ? "none" : "block";
    }
  });
});

if (hamburger && navLinksContainer) {
  hamburger.addEventListener("click", () => {
    navLinksContainer.classList.toggle("active");
  });
}

navItems.forEach(item => {
  item.addEventListener("click", () => {
    if (navLinksContainer) {
      navLinksContainer.classList.remove("active");
    }
  });
});

function updateNavbarState() {
  if (!navbar) return;

  const scrolled = window.scrollY > 30;
  navbar.classList.toggle("scrolled", scrolled);
}

if (typeof Typed !== "undefined") {
  new Typed("#typed", {
    strings: [
      "Electronics Engineer",
      "Communication Engineer",
      "IoT System Developer",
      "Embedded System Developer",
      "AI & ML Enthusiast"
    ],
    typeSpeed: 50,
    backSpeed: 30,
    loop: true
  });
}

window.addEventListener("scroll", () => {
  updateActiveLink();
  updateNavbarState();
}, { passive: true });

updateActiveLink();
updateNavbarState();