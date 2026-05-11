document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("formCalculadora");
    const numero1 = document.getElementById("numero1");
    const numero2 = document.getElementById("numero2");

    form.addEventListener("submit", function (event) {
        if (numero1.value.trim() === "" || numero2.value.trim() === "") {
            event.preventDefault();
            alert("Preencha os dois números antes de calcular.");
        }
    });
});