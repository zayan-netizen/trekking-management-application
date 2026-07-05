const role = document.getElementById("role");
const staffFields = document.getElementById("staff-fields");

role.addEventListener("change", function () {

    if (this.value === "Trek Staff") {
        staffFields.style.display = "block";
    } else {
        staffFields.style.display = "none";
    }

});