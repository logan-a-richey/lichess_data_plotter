// casual_rating_simulation.js 

new Chart(document.getElementById("casual_game_simulation_line_graph"), {
    type: "line",
    data: { 
        labels: times, 
        datasets: [
            { 
                label: "Casual Games", 
                data: ratings
            }] 
    },
    options: {
        responsive: false,
        maintainAspectRatio: false,
    }
});

