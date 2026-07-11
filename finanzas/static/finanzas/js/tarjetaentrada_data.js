const boton = document.getElementById("calcular");
const input = document.getElementById("valor");
const tablaDiv = document.getElementById("tabla");
const mensajeerror = document.getElementById("error");


boton.addEventListener("click", async () => {
    const saldo = Number(input.value);

    if (isNaN(saldo) || saldo <= 0) {
        mensajeerror.textContent = "Por favor, ingrese un número válido mayor que cero.";
        mensajeerror.style.display = "block";  // ✅ mostrar
        tablaDiv.innerHTML = "";        
        return;                                // ⚠️ detiene el resto de la función

    } else {
        mensajeerror.textContent = "";
        mensajeerror.style.display = "none";  
      }       

    const response = await fetch("/calcular", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ saldo })
    });

    const data = await response.json();

    construirTabla(data);
});

const ordenCategorias = [
    "Fecha",
    "Disfrute (15%)",
    "Esencial (40%)",
    "Estabilidad (15%)",
    "Inversión (30%)",
    "Saldo Total"
];

function construirTabla(data) {
   const objeto = data[0]; // diccionario real

    let html = `
        <table class="styling-tabla">
            <thead>
                <tr>
    `;

    // 1️⃣ Cabeceras (categorías como columnas)
    for (const categoria of ordenCategorias) {
        if (objeto[categoria] === undefined) continue;

        html += `<th>${categoria}</th>`;
    }

    html += `
                </tr>
            </thead>
            <tbody>
                <tr>
    `;

    // 2️⃣ Valores (una sola fila)
    for (const categoria of ordenCategorias) {
        const valor = objeto[categoria];
        if (valor === undefined) continue;

        html += `<td>${valor}</td>`;
    }

    html += `
                </tr>
            </tbody>
        </table>
    `;

    tablaDiv.innerHTML = html;
}
