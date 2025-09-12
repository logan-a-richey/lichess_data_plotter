// adoption_data.js

// Extract data from Flask-passed objects
const fullAdoptedNames = fullAdopted.map(p=>p.name);
const fullAdoptedCounts = fullAdopted.map(p=>p.num_win_streaks);
const fullAdoptedScatter = fullAdopted.map(p=>({x:p.highest_elo, y:p.num_win_streaks, name:p.name}));

const fullBeenAdoptedNames = fullBeenAdopted.map(p=>p.name);
const fullBeenAdoptedCounts = fullBeenAdopted.map(p=>p.num_lose_streaks);
const fullBeenAdoptedScatter = fullBeenAdopted.map(p=>({x:p.highest_elo, y:p.num_lose_streaks, name:p.name}));

// ====== Initialize Charts ======
let barAdoptedChart = new Chart(document.getElementById("barAdopted"), {
    type: "bar",
    data: { labels: [], datasets: [{ label:"Num Adoptions", data: [], backgroundColor:"#4caf50" }] },
    options: { responsive:true, plugins:{ legend:{display:false}, title:{display:true,text:"Top Adopted Players"}} }
});

let barBeenAdoptedChart = new Chart(document.getElementById("barBeenAdopted"), {
    type: "bar",
    data: { labels: [], datasets: [{ label:"Num Times Adopted", data: [], backgroundColor:"#f44336" }] },
    options: { responsive:true, plugins:{ legend:{display:false}, title:{display:true,text:"Top Players Who Adopted Me"}} }
});

let scatterAdoptedChart = new Chart(document.getElementById("scatterAdopted"), {
    type: "scatter",
    data: { datasets:[{ label:"Adoptions", data:[], backgroundColor:"#4caf50", pointRadius:6 }] },
    options: { responsive:true,
        plugins:{ tooltip:{ callbacks:{ label: function(ctx){ const p=ctx.raw; return `${p.name} (${p.x}) : ${p.y}`; }}}},
        onClick: scatterClickHandler.bind(null,'tableAdopted'),
        scales:{ x:{ title:{display:true,text:"Elo"} }, y:{ title:{display:true,text:"Number of Adoptions"}, beginAtZero:true } }
    }
});

let scatterBeenAdoptedChart = new Chart(document.getElementById("scatterBeenAdopted"), {
    type: "scatter",
    data: { datasets:[{ label:"Been Adopted", data:[], backgroundColor:"#f44336", pointRadius:6 }] },
    options: { responsive:true,
        plugins:{ tooltip:{ callbacks:{ label: function(ctx){ const p=ctx.raw; return `${p.name} (${p.x}) : ${p.y}`; }}}},
        onClick: scatterClickHandler.bind(null,'tableBeenAdopted'),
        scales:{ x:{ title:{display:true,text:"Elo"} }, y:{ title:{display:true,text:"Number of Adoptions"}, beginAtZero:true } }
    }
});

// ====== Scatter click handler ======
function scatterClickHandler(tableId, evt, elements){
    if(elements.length>0){
        const index = elements[0].index;
        const chart = elements[0].chart;
        const dp = chart.data.datasets[0].data[index];
        const table = document.getElementById(tableId);
        const rows = Array.from(table.tBodies[0].rows);
        for(let row of rows){
            if(row.cells[1].innerText === dp.name){
                row.scrollIntoView({behavior:"smooth",block:"center"});
                row.style.backgroundColor="#ffff99";
                setTimeout(()=>row.style.backgroundColor="",2000);
                break;
            }
        }
    }
}

// ====== Table Sorting ======
function sortTable(tableId, colIndex, type, dir) {
    const table = document.getElementById(tableId);
    const tbody = table.tBodies[0];
    const rows = Array.from(tbody.rows);
    rows.sort((a,b)=>{
        let valA = a.cells[colIndex].innerText;
        let valB = b.cells[colIndex].innerText;
        if(type==="num"){ valA=parseInt(valA); valB=parseInt(valB); }
        if(type==="name"){ valA=valA.toLowerCase(); valB=valB.toLowerCase(); }
        return dir==="asc" ? (valA>valB?1:-1) : (valA<valB?1:-1);
    });
    rows.forEach(r=>tbody.appendChild(r));
}

// Attach click handlers for headers
document.querySelectorAll("th[data-sort]").forEach(th=>{
    th.addEventListener("click", ()=>{
        const table = th.closest("table");
        const colIndex = Array.from(th.parentNode.children).indexOf(th);
        const type = th.dataset.sort;
        const dir = th.dataset.dir;
        sortTable(table.id, colIndex, type, dir);
        th.dataset.dir = dir==="asc"?"desc":"asc";
        th.innerText = th.innerText.replace(/▲|▼/,"") + (th.dataset.dir==="asc"?" ▲":" ▼");
    });
});

// ====== Update charts based on dropdown ======
function updateCharts(limitAdopted, limitBeen){
    const la = limitAdopted==="all"?fullAdopted.length:parseInt(limitAdopted);
    const lb = limitBeen==="all"?fullBeenAdopted.length:parseInt(limitBeen);

    // Bar charts
    barAdoptedChart.data.labels = fullAdoptedNames.slice(0,la);
    barAdoptedChart.data.datasets[0].data = fullAdoptedCounts.slice(0,la);
    barAdoptedChart.update();

    barBeenAdoptedChart.data.labels = fullBeenAdoptedNames.slice(0,lb);
    barBeenAdoptedChart.data.datasets[0].data = fullBeenAdoptedCounts.slice(0,lb);
    barBeenAdoptedChart.update();

    // Scatter charts
    scatterAdoptedChart.data.datasets[0].data = fullAdoptedScatter.slice(0,la);
    scatterAdoptedChart.update();

    scatterBeenAdoptedChart.data.datasets[0].data = fullBeenAdoptedScatter.slice(0,lb);
    scatterBeenAdoptedChart.update();
}

// Attach dropdown events
document.getElementById("topFilterAdopted").addEventListener("change",()=>updateCharts(
    document.getElementById("topFilterAdopted").value,
    document.getElementById("topFilterBeenAdopted").value
));
document.getElementById("topFilterBeenAdopted").addEventListener("change",()=>updateCharts(
    document.getElementById("topFilterAdopted").value,
    document.getElementById("topFilterBeenAdopted").value
));

// Initial update
updateCharts(document.getElementById("topFilterAdopted").value,
             document.getElementById("topFilterBeenAdopted").value);

