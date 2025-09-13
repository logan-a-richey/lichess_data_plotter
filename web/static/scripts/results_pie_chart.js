// results_pie_chart.js

// const whiteData = {{ white_results | tojson }};
// const blackData = {{ black_results | tojson }};

const white_chart_context = document.getElementById("WhiteChart").getContext("2d");
new Chart(white_chart_context, {
    type: "pie",
    data: {
        labels: ["Wins", "Draws", "Losses"],
        datasets: [{
            data: [
                whiteData["wins"], 
                whiteData["draws"],
                whiteData["losses"] 
            ],
            backgroundColor: [
                "rgba(79,163,255,0.6)", // blue : wins
                "rgba(200,200,200,0.6)", // gray : draws
                "rgba(255,99,132,0.6)" // red : losses
            ],
            borderColor: "#2b2b2b"
        }]
    },
    options: {
        ...getDarkChartOptions("Performance as White"),
        maintainAspectRatio: false,
        scales: {
            x: { display: false},
            y: { display: false}
        }
    }
});

const black_chart_context = document.getElementById("BlackChart").getContext("2d");
new Chart(black_chart_context, {
    type: "pie",
    data: {
        labels: ["Wins", "Draws", "Losses"],
        datasets: [{
            data: [
                blackData["wins"], 
                blackData["draws"],
                blackData["losses"]
            ],
            backgroundColor: [
                "rgba(79,163,255,0.6)", // blue : wins
                "rgba(200,200,200,0.6)", // gray : draws
                "rgba(255,99,132,0.6)" // red : losses
            ],
            borderColor: "#2b2b2b"
        }]
    },
    options: {
        ...getDarkChartOptions("Performance as Black"),
        maintainAspectRatio: false,
        scales: {
            x: { display: false},
            y: { display: false}
        }
    }
});

