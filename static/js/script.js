const form = document.querySelector("form");
const loader = document.getElementById("loader");

const uploadBox = document.getElementById("uploadBox");
const fileInput = document.getElementById("image");
const uploadLabel = document.getElementById("uploadLabel");

// Loader
form.addEventListener("submit", function () {

    loader.style.display = "block";

});

// Drag Over
uploadBox.addEventListener("dragover", function (e) {

    e.preventDefault();

    uploadBox.classList.add("dragover");

});

// Drag Leave
uploadBox.addEventListener("dragleave", function () {

    uploadBox.classList.remove("dragover");

});

// Drop
uploadBox.addEventListener("drop", function (e) {

    e.preventDefault();

    uploadBox.classList.remove("dragover");

    fileInput.files = e.dataTransfer.files;

    uploadLabel.innerHTML =
        "<h2>✅ " + e.dataTransfer.files[0].name + "</h2>";

});

// File Selected
fileInput.addEventListener("change", function () {

    if (fileInput.files.length > 0) {

        uploadLabel.innerHTML =
            "<h2>✅ " + fileInput.files[0].name + "</h2>";

    }

});