// games_per_month.js 

/*
const line_chart_context = document.getElementById("gamesChart").getContext("2d");
new Chart(line_chart_context, {
    type: "line",
    data: {
        labels: labels,
        datasets: [{
            label: "Games Played",
            data: data,
            borderColor: "#2196f3",
            backgroundColor: "rgba(33, 150, 243, 0.3)",
            fill: true,
            tension: 0.2,
            pointRadius: 4
        }]
    },
    options: {
        ...getDarkChartOptions("Monthly Games Played"),
        responsive: true,
        maintainAspectRatio: false,
        scales: { 
            x: { title: {display: true, text: "Month"} },
            y: { title: {display: true, text: "Games"}, beginAtZero: true } 
        }
    }
});
*/

new Chart(document.getElementById("gamesChart"), {
    type: "line",
    data: { labels: labels, datasets: [{ label: "Games", data: data }] },
    options: {
        responsive: false,
        maintainAspectRatio: false,
    }
});

