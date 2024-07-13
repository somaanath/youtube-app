document.addEventListener("DOMContentLoaded", () => {
  const toggleButton = document.querySelector(
    '[data-collapse-toggle="mobile-menu"]'
  );
  const menu = document.querySelector("#mobile-menu");
  // Ensure the mobile menu is hidden initially
  menu.style.display = "none";
  toggleButton.addEventListener("click", () => {
    if (menu.style.display === "none") {
      menu.style.display = "block";
    } else {
      menu.style.display = "none";
    }
  });
});
