const boton = document.getElementById("calcular");
const input = document.getElementById("valor");
const mensajeerror = document.getElementById("error");

// Escuchamos el evento 'submit' del formulario en lugar del 'click' del botón
// (Es una mejor práctica porque atrapa también cuando el usuario da Enter)
const formulario = document.querySelector(".Tarjeta");

formulario.addEventListener("submit", function (evento) {
    const saldo = Number(input.value);

    // Validación local en el navegador
    if (isNaN(saldo) || saldo <= 0) {
        // 1. Detenemos por completo el envío del formulario a Django
        evento.preventDefault(); 
        
        // 2. Mostramos el mensaje de error en la pantalla
        mensajeerror.textContent = "Por favor, ingrese un número válido mayor que cero.";
        mensajeerror.style.display = "block"; 
    } else {
        // Si el número está perfecto, limpiamos el error y dejamos que el formulario viaje normal
        mensajeerror.textContent = "";
        mensajeerror.style.display = "none";
    }
});