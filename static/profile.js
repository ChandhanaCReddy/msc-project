document.getElementById("profileForm")
.addEventListener("submit", function(event){

    event.preventDefault();

    let name =
    document.getElementById("name").value;

    let age =
    document.getElementById("age").value;

    let phone =
    document.getElementById("phone").value;

    let email =
    document.getElementById("email").value;

    if(name === ""){
        alert("Enter your name");
        return;
    }

    if(age < 18){
        alert("Age must be 18 or above");
        return;
    }

    if(phone.length !== 10){
        alert("Enter valid phone number");
        return;
    }

    if(email === ""){
        alert("Enter email");
        return;
    }

    alert("Profile Saved Successfully!");

    window.location.href = "home.html";

});
