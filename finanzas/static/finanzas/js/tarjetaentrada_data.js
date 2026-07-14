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

document.addEventListener("DOMContentLoaded", function () {
    // 1. Seleccionamos los elementos clave del DOM
    const modal = document.getElementById("modal-porcentajes");
    const btnAbrir = document.getElementById("btn-abrir-modal");
    const btnCerrar = document.getElementById("btn-cerrar-modal");
    const btnGuardar = document.getElementById("btn-guardar-modal");
    
    // Inputs del modal
    const inputEsencial = document.getElementById("p_esencial");
    const inputEstabilidad = document.getElementById("p_estabilidad");
    const inputDisfrute = document.getElementById("p_disfrute");
    const inputInversion = document.getElementById("p_inversion");
    
    // Párrafo de error dentro del modal
    const errorSumaModal = document.getElementById("error-suma-modal");

    // Guardamos una copia de respaldo por si el usuario cancela (Botón NO)
    let valoresRespaldados = {
        esencial: inputEsencial.value,
        estabilidad: inputEstabilidad.value,
        disfrute: inputDisfrute.value,
        inversion: inputInversion.value
    };

    // 2. Evento para ABRIR el modal
    btnAbrir.addEventListener("click", function () {
        // Respaldamos los valores actuales antes de que el usuario los edite
        valoresRespaldados = {
            esencial: inputEsencial.value,
            estabilidad: inputEstabilidad.value,
            disfrute: inputDisfrute.value,
            inversion: inputInversion.value
        };
        // Ocultamos cualquier error previo
        errorSumaModal.style.display = "none";
        // Mostramos el modal usando flex para centrarlo según tu CSS
        modal.style.display = "flex";
    });

    // 3. Evento para CERRAR (Botón NO - Cancela cambios)
    btnCerrar.addEventListener("click", function () {
        // Restauramos los valores originales que estaban antes de abrir el modal
        inputEsencial.value = valoresRespaldados.esencial;
        inputEstabilidad.value = valoresRespaldados.estabilidad;
        inputDisfrute.value = valoresRespaldados.disfrute;
        inputInversion.value = valoresRespaldados.inversion;
        
        // Escondemos el modal
        modal.style.display = "none";
    });

    // 4. Evento para GUARDAR (Botón SÍ - Valida la suma)
    btnGuardar.addEventListener("click", function () {
        // Obtenemos los valores ingresados (si están vacíos, por defecto tomamos 0)
        const valEsencial = parseFloat(inputEsencial.value) || 0;
        const valEstabilidad = parseFloat(inputEstabilidad.value) || 0;
        const valDisfrute = parseFloat(inputDisfrute.value) || 0;
        const valInversion = parseFloat(inputInversion.value) || 0;

        // Sumamos los porcentajes
        const sumaTotal = valEsencial + valEstabilidad + valDisfrute + valInversion;

        // Validamos tu regla de oro: la suma debe dar exactamente 100%
        if (sumaTotal === 100) {
            // ¡Todo en orden! Ocultamos errores y cerramos el modal guardando los cambios en los inputs
            errorSumaModal.style.display = "none";
            modal.style.display = "none";
            
            // Opcional: agregamos un efecto visual sutil para denotar que se guardaron cambios
            btnAbrir.style.boxShadow = "0 0 15px rgba(76, 175, 80, 0.8)";
            setTimeout(() => {
                btnAbrir.style.boxShadow = "0 8px 20px rgba(45, 104, 48, 0.35)";
            }, 1000);

        } else {
            // Si da más o menos de 100%, calculamos la diferencia para decírselo al usuario
            const diferencia = sumaTotal - 100;
            let mensaje = `La suma total debe ser exactamente 100%. Actualmente da: **${sumaTotal}%** `;
            
            if (diferencia > 0) {
                mensaje += `(Te pasaste por ${diferencia}%)`;
            } else {
                mensaje += `(Te faltan ${Math.abs(diferencia)}%)`;
            }
            
            // Pintamos el mensaje de error en el modal
            errorSumaModal.innerHTML = mensaje;
            errorSumaModal.style.display = "block";
        }
    });

    // 5. Cerrar al hacer clic fuera del recuadro del modal (Opcional, muy intuitivo)
    modal.addEventListener("click", function (e) {
        if (e.target === modal) {
            btnCerrar.click(); // Dispara la cancelación automática
        }
    });
});