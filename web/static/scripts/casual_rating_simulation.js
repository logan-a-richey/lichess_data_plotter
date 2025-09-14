// casual_rating_simulation.js 

new Chart(document.getElementById("ratingChart"), {
    type: "line",
    data: {
        labels: labels,
        datasets: [
            { label: "High", data: highs, borderColor: "green", fill: false },
            { label: "Average", data: avgs, borderColor: "gold", fill: false },
            { label: "Low", data: lows, borderColor: "red", fill: false }
        ]
    },
    options: {
        responsive: true,
        scales: {
            x: { title: { display: true, text: "Month" } },
            y: { title: { display: true, text: "Elo" } }
        }
    }
});
