let productosGlobal = [];

async function cargarDatos() {
    try {
        const res = await fetch("/api/precios");
        const data = await res.json();

        // METADATOS
        const scraper = data.metadata?.ultima_ejecucion_scraper;
        const git = data.metadata?.ultima_actualizacion_git;

        document.getElementById("scraper").textContent =
            scraper
                ? "🕒 Última ejecución del scraper: " + scraper
                : "🕒 Sin datos del scraper";

        document.getElementById("git").textContent =
            git
                ? "🔄 Última actualización en Git: " + git
                : "🔄 Git: sin cambios recientes";

        productosGlobal = data.productos;

        renderTabla(productosGlobal);

    } catch (error) {
        document.getElementById("scraper").textContent =
            "❌ Error cargando datos";
        console.error(error);
    }
}

function renderTabla(lista) {
    const tbody = document.querySelector("#tabla tbody");
    tbody.innerHTML = "";

    if (lista.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="8">No se encontraron resultados</td>
            </tr>
        `;
        return;
    }

    lista.forEach(p => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${p.producto}</td>
            <td>${p.unidad}</td>
            <td>${p.mayorista}</td>
            <td>${formato(p.minimo)}</td>
            <td>${formato(p.maximo)}</td>
            <td>${formato(p.moda)}</td>
            <td>${formato(p.promedio)}</td>
            <td>${p.fecha}</td>
        `;

        tbody.appendChild(tr);
    });
}

// BUSCADOR
document.addEventListener("input", e => {
    if (e.target.id !== "buscador") return;

    const texto = e.target.value.toLowerCase();

    const filtrados = productosGlobal.filter(p =>
        p.producto.toLowerCase().includes(texto)
    );

    renderTabla(filtrados);
});

function formato(valor) {
    if (valor === null || valor === undefined || valor === "") {
        return "-";
    }

    return Number(valor).toLocaleString("es-CR", {
        style: "currency",
        currency: "CRC",
        minimumFractionDigits: 0
    });
}

cargarDatos();
