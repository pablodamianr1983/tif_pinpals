document.addEventListener("DOMContentLoaded", function() {
    // Mostrar la imagen de carga
    document.getElementById("loadingDiv").style.display = "block";

    // Ocultar la imagen de carga después de 2 segundos
    setTimeout(function() {
        document.getElementById("loadingDiv").style.display = "none";
    }, 2000);
});
