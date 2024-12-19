const mobileNavToggle = document.querySelector(".mobile-nav-toggle");
const primaryNav = document.querySelector(".primary-navigation");
const primaryHeader = document.querySelector(".secondary-header");
console.log(11);
mobileNavToggle.addEventListener("click", () => {
  primaryNav.hasAttribute("data-visible")
    ? mobileNavToggle.setAttribute("aria-expanded", false)
    : mobileNavToggle.setAttribute("aria-expanded", true);
  primaryNav.toggleAttribute("data-visible");
});

// Mobile Navingatio Dropdown
var dropdown = document.getElementsByClassName("dropdown-btn");
var i;
const mediaQuery = window.matchMedia("(max-width: 1120px)");
if (mediaQuery.matches) {
  for (i = 0; i < dropdown.length; i++) {
    dropdown[i].addEventListener("click", function () {
      this.classList.toggle("active");
      var dropdownContent = this.nextElementSibling;
      if (dropdownContent.style.display === "block") {
        dropdownContent.style.display = "none";
      } else {
        dropdownContent.style.display = "block";
      }
    });
  }
}




// // Define the logout button globally
// const logout_btn = document.getElementById('logout-btn');

// // Function to check if the user is authenticated
// function isAuthenticated() {
//     console.log('isAuthenticated method is running....');
    
//     const token = localStorage.getItem('access');
//     if (!token) return false;

//     const payload = JSON.parse(atob(token.split('.')[1]));
//     const now = Math.floor(Date.now() / 1000);
//     return payload.exp > now; // Check if the token is expired
// }


// // Function to show/hide the logout button based on authentication status
// function showLogoutButton() {
//     if (isAuthenticated()) {
//         logout_btn.style.display = ''; // Show the button if authenticated
//     } else {
//         logout_btn.style.display = 'none'; // Hide the button if not authenticated
//     }
// }

// // Initial call to set the button visibility on page load
// document.addEventListener('DOMContentLoaded', () => {
//     showLogoutButton(); // Run the check on page load
// });

// // Handle login (you need to call this when a login event happens)
// function loginUser(accessToken, refreshToken) {
//     localStorage.setItem('access', accessToken);
//     localStorage.setItem('refresh', refreshToken);
//     showLogoutButton(); // Dynamically update the button visibility after login
// }

// // Handle logout
// logout_btn.addEventListener('click', () => {
//     localStorage.removeItem('access');
//     localStorage.removeItem('refresh');
//     showLogoutButton(); // Update the button visibility after logout
//     // Optionally, redirect to login or show a message
// });

