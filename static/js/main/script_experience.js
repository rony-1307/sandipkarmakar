document.addEventListener("DOMContentLoaded", function () {
  const slider = document.getElementById("trainingSlider");
  const cards = document.querySelectorAll(".training-card");
  const prevButton = document.getElementById("trainingPrev");
  const nextButton = document.getElementById("trainingNext");
  const dotsContainer = document.getElementById("trainingDots");
  let currentSlide = 0;
  let autoScrollTimer = null;

  function getVisibleCards() {
    if (window.innerWidth <= 600) return 1;
    if (window.innerWidth <= 992) return 2;
    return 3;
  }

  function getTotalSlides() {
    const visibleCards = getVisibleCards();
    return Math.max(1, Math.ceil(cards.length / visibleCards));
  }

  function createDots() {
    dotsContainer.innerHTML = "";
    const totalSlides = getTotalSlides();
    for (let i = 0; i < totalSlides; i++) {
      const dot = document.createElement("button");
      dot.classList.add("training-dot");
      dot.setAttribute("aria-label", "Go to training slide " + (i + 1));
      dot.addEventListener("click", function () {
        currentSlide = i;
        scrollToSlide();
        restartAutoScroll();
      });
      dotsContainer.appendChild(dot);
    }
    updateDots();
  }

  function updateDots() {
    const dots = document.querySelectorAll(".training-dot");
    dots.forEach(function (dot, index) {
      dot.classList.toggle("active", index === currentSlide);
    });
  }

  function updateButtons() {
    const totalSlides = getTotalSlides();
    prevButton.disabled = currentSlide === 0;
    nextButton.disabled = currentSlide >= totalSlides - 1;
  }

  function scrollToSlide() {
    if (!cards.length) return;
    const visibleCards = getVisibleCards();
    const cardWidth = cards[0].getBoundingClientRect().width;
    const gap = 20;
    const scrollPosition = currentSlide * visibleCards * (cardWidth + gap);
    slider.scrollTo({ left: scrollPosition, behavior: "smooth" });
    updateDots();
    updateButtons();
  }

  function goToNextSlide() {
    const totalSlides = getTotalSlides();
    currentSlide = (currentSlide + 1) % totalSlides;
    scrollToSlide();
  }

  function restartAutoScroll() {
    clearInterval(autoScrollTimer);
    autoScrollTimer = setInterval(function () {
      goToNextSlide();
    }, 2600);
  }

  nextButton.addEventListener("click", function () {
    currentSlide = Math.min(currentSlide + 1, getTotalSlides() - 1);
    scrollToSlide();
    restartAutoScroll();
  });

  prevButton.addEventListener("click", function () {
    currentSlide = Math.max(currentSlide - 1, 0);
    scrollToSlide();
    restartAutoScroll();
  });

  let scrollTimer;
  slider.addEventListener("scroll", function () {
    clearTimeout(scrollTimer);
    scrollTimer = setTimeout(function () {
      const visibleCards = getVisibleCards();
      const cardWidth = cards[0].getBoundingClientRect().width;
      const gap = 20;
      const slideWidth = visibleCards * (cardWidth + gap);
      const detectedSlide = Math.round(slider.scrollLeft / slideWidth);
      if (detectedSlide !== currentSlide) {
        currentSlide = Math.max(0, Math.min(detectedSlide, getTotalSlides() - 1));
        updateDots();
        updateButtons();
      }
    }, 100);
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "ArrowLeft") {
      currentSlide = Math.max(currentSlide - 1, 0);
      scrollToSlide();
      restartAutoScroll();
    }
    if (event.key === "ArrowRight") {
      currentSlide = Math.min(currentSlide + 1, getTotalSlides() - 1);
      scrollToSlide();
      restartAutoScroll();
    }
  });

  window.addEventListener("resize", function () {
    currentSlide = 0;
    slider.scrollTo({ left: 0, behavior: "auto" });
    createDots();
    updateButtons();
    restartAutoScroll();
  });

  createDots();
  updateButtons();
  restartAutoScroll();
});
