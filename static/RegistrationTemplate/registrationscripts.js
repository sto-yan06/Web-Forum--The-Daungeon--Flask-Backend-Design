document.addEventListener("DOMContentLoaded", function () {
    const passwordInput = document.getElementById("password");
    const passwordPattern = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$/;
  
    passwordInput.addEventListener("input", function () {
      const password = passwordInput.value;
  
      if (passwordPattern.test(password)) {
        // Password meets the criteria, show a success message or change input style
        passwordInput.setCustomValidity(""); // Clear any previous validation message
      } else {
        // Password does not meet the criteria, show an error message
        passwordInput.setCustomValidity("Password must be at least 8 characters long and include one uppercase letter, one number, and one special character.");
      }
    });
  
    const confirmPasswordInput = document.getElementById("confirm_password");
    confirmPasswordInput.addEventListener("input", function () {
      const password = passwordInput.value;
      const confirmPassword = confirmPasswordInput.value;
  
      if (password === confirmPassword) {
        confirmPasswordInput.setCustomValidity("");
      } else {
        confirmPasswordInput.setCustomValidity("Passwords do not match.");
      }
    });
  });

  document.getElementById("login-button").onclick = function(){
    location.href = "/login";
}; 

const ageInput = document.getElementById("age")
ageInput.addEventListener("input", function(){
  const age = parseInt(ageInput.value, 10);

  if(age < 0){
    ageInput.value = 0;
  }
});