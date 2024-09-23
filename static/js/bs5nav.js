var bs5menu_btn = document.querySelector("#menu-btn");
var bs5sidebar = document.querySelector("#sidebar");
var bs5container = document.querySelector(".my-container");

bs5menu_btn.addEventListener("click", () => {
     bs5sidebar.classList.toggle("active-nav");
     bs5container.classList.toggle("active-cont");
  }
);
