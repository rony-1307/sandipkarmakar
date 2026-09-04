document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".project-flip-card").forEach(function (card) {
    card.querySelectorAll(".flip-btn").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        card.classList.toggle("is-flipped");
      });
    });

    // Also allow clicking anywhere on the card
    card.addEventListener("click", function () {
      card.classList.toggle("is-flipped");
    });
  });
});