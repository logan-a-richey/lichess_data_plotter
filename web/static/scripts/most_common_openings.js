// most_common_openings.js

new Chart(document.getElementById("whiteChart"), {
type: "pie",
data: {
    labels: whiteLabels,
    datasets: [{
        data: whiteCounts,
        backgroundColor: [
            "#e6194b","#3cb44b","#ffe119","#4363d8","#f58231",
            "#911eb4","#46f0f0","#f032e6","#bcf60c","#fabebe"
        ]
    }]
},
options: {
    plugins: { title: { display: true, text: "Top White Openings" } }
}
});

new Chart(document.getElementById("blackChart"), {
type: "pie",
data: {
    labels: blackLabels,
    datasets: [{
        data: blackCounts,
        backgroundColor: [
            "#e6194b","#3cb44b","#ffe119","#4363d8","#f58231",
            "#911eb4","#46f0f0","#f032e6","#bcf60c","#fabebe"
        ]
    }]
},
options: {
    plugins: { title: { display: true, text: "Top Black Openings" } }
}
});
