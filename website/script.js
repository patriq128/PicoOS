const hamburger = document.getElementById("hamburger");
const navLinks = document.getElementById("nav_links");


hamburger.onclick = () => {
    navLinks.classList.toggle("active");
};