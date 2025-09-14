// adoption_data.js

// Prepare datasets from Flask
const adoptedScatter = fullAdopted.map(p => ({
    x: p.highest_elo,
    y: p.num_win_streaks,
    name: p.name
}));
const beenAdoptedScatter = fullBeenAdopted.map(p => ({
    x: p.highest_elo,
    y: p.num_lose_streaks,
    name: p.name
}));

// Generic chart factory
function makeScatterChart(canvasId, label, color, tableId, yLabel) {
    return new Chart(document.getElementById(canvasId), {
        type: "scatter",
        data: { datasets: [{ label, data: [], backgroundColor: color, pointRadius: 6 }] },
        options: {
            responsive: true,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: ctx => {
                            const p = ctx.raw;
                            return `${p.name} (${p.x}) : ${p.y}`;
                        }
                    }
                }
            },
            onClick: (evt, elements) => chartClickHandler(tableId, evt, charts[canvasId]),
            scales: {
                x: { title: { display: true, text: "Elo" } },
                y: { title: { display: true, text: yLabel }, beginAtZero: true }
            }
        }
    });
}

// Charts collection
const charts = {
    scatterAdopted: makeScatterChart("scatterAdopted", "Adoptions", "#4caf50", "tableAdopted", "Number of Adoptions"),
    scatterBeenAdopted: makeScatterChart("scatterBeenAdopted", "Been Adopted", "#f44336", "tableBeenAdopted", "Number of Adoptions")
};

// Unified click handler for both charts
function chartClickHandler(tableId, evt, chart) {
    const points = chart.getElementsAtEventForMode(evt, "nearest", { intersect: true }, true);
    if (points.length === 0) return;

    const { index } = points[0];
    const dp = chart.data.datasets[0].data[index];
    const table = document.getElementById(tableId);
    const rows = Array.from(table.tBodies[0].rows);

    for (let row of rows) {
        if (row.cells[1].innerText === dp.name) {
            row.scrollIntoView({ behavior: "smooth", block: "center" });
            row.style.backgroundColor = "#0000ff";
            setTimeout(() => (row.style.backgroundColor = ""), 2000);
            break;
        }
    }
}

// Sorting
function sortTable(tableId, colIndex, type, dir) {
    const table = document.getElementById(tableId);
    const tbody = table.tBodies[0];
    const rows = Array.from(tbody.rows);

    rows.sort((a, b) => {
        let valA = a.cells[colIndex].innerText;
        let valB = b.cells[colIndex].innerText;

        if (type === "num") {
            valA = parseInt(valA);
            valB = parseInt(valB);
        } else if (type === "name") {
            valA = valA.toLowerCase();
            valB = valB.toLowerCase();
        }

        return dir === "asc" ? (valA > valB ? 1 : -1) : (valA < valB ? 1 : -1);
    });

    rows.forEach(r => tbody.appendChild(r));
}

function sortIntTable(tableId, colIndex, type, dir) {
    const table = document.getElementById(tableId);
    const tbody = table.tBodies[0];
    const rows = Array.from(tbody.rows);

    rows.sort((a, b) => {
        let valA = parseInt(a.cells[colIndex].innerText);
        let valB = parseInt(b.cells[colIndex].innerText);

        if (type === "num") {
            valA = parseInt(valA);
            valB = parseInt(valB);
        } else if (type === "name") {
            valA = valA.toLowerCase();
            valB = valB.toLowerCase();
        }

        return dir === "asc" ? (valA > valB ? 1 : -1) : (valA < valB ? 1 : -1);
    });

    rows.forEach(r => tbody.appendChild(r));
}

// Attach sorting behavior
document.querySelectorAll("th[data-sort]").forEach(th => {
    th.addEventListener("click", () => {
        const table = th.closest("table");
        const colIndex = Array.from(th.parentNode.children).indexOf(th);
        const type = th.dataset.sort;
        const dir = th.dataset.dir;
        
        if (th.id == "th3") {
            sortIntTable(table.id, colIndex, type, dir);
        }
        else {
            sortTable(table.id, colIndex, type, dir);
        }

        th.dataset.dir = dir === "asc" ? "desc" : "asc";
        th.innerText = th.innerText.replace(/▲|▼/, "") + (th.dataset.dir === "asc" ? " ▲" : " ▼");
    });
});

// Update charts (with dropdown limits)
function updateCharts(limitAdopted, limitBeen) {
    const la = limitAdopted === "all" ? adoptedScatter.length : parseInt(limitAdopted);
    const lb = limitBeen === "all" ? beenAdoptedScatter.length : parseInt(limitBeen);

    charts.scatterAdopted.data.datasets[0].data = adoptedScatter.slice(0, la);
    charts.scatterBeenAdopted.data.datasets[0].data = beenAdoptedScatter.slice(0, lb);

    charts.scatterAdopted.update();
    charts.scatterBeenAdopted.update();
}

// Table handlers
function setupTableToggle(checkboxId, tableId) {
    const checkbox = document.getElementById(checkboxId);
    const table = document.getElementById(tableId);

    function updateVisibility() {
        table.style.display = checkbox.checked ? "block" : "none";
    }

    checkbox.addEventListener("change", updateVisibility);
    updateVisibility(); // initialize state
}

// Initialize toggles
setupTableToggle("toggleTableAdopted", "scroll_1");
setupTableToggle("toggleTableBeenAdopted", "scroll_2");

// Attach dropdown events
document.getElementById("topFilterAdopted").addEventListener("change", () =>
    updateCharts(
        document.getElementById("topFilterAdopted").value,
        document.getElementById("topFilterBeenAdopted").value
    )
);

document.getElementById("topFilterBeenAdopted").addEventListener("change", () =>
    updateCharts(
        document.getElementById("topFilterAdopted").value,
        document.getElementById("topFilterBeenAdopted").value
    )
);

// Initial render
updateCharts(
    document.getElementById("topFilterAdopted").value,
    document.getElementById("topFilterBeenAdopted").value
);

