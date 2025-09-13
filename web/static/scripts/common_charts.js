/* common_charts.js */

// ====== Dark Theme Defaults for Chart.js ======

Chart.defaults.color = "#e0e0e0"; // default font color
Chart.defaults.font.family = "'Segoe UI', Roboto, Helvetica, Arial, sans-serif";

function getDarkChartOptions(titleText = "") {
    return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            title: {
                display: !!titleText,
                text: titleText,
                color: "#ffffff",
                font: {
                    size: 16,
                    weight: "bold"
                }
            },
            legend: {
                labels: {
                    color: "#e0e0e0"
                }
            },
            tooltip: {
                backgroundColor: "rgba(50,50,50,0.9)",
                titleColor: "#ffffff",
                bodyColor: "#e0e0e0",
                borderColor: "rgba(255,255,255,0.1)",
                borderWidth: 1
            }
        },
        scales: {
            x: {
                ticks: { color: "#cfcfcf" },
                grid: { color: "rgba(255,255,255,0.05)" }
            },
            y: {
                ticks: { color: "#cfcfcf" },
                grid: { color: "rgba(255,255,255,0.05)" }
            }
        }
    };
}

