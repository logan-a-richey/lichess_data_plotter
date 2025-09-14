// top_wins.js

function renderTable(category) {
    const data = winsData[category] || [];
    let html = `
    <table>
        <thead>
            <tr>
                <th>Rank</th>
                <th>Opponent</th>
                <th>Title</th>
                <th>Rating</th>
                <th>Site</th>
            </tr>
        </thead>
        <tbody>
    `;
    data.forEach((g, idx) => {
        html += `
        <tr>
            <td>${idx+1}</td>
            <td>${g.opp_name}</td>
            <td>${g.opp_title || ""}</td>
            <td>${g.opp_elo}</td>
            <td><a href="${g.site}" target="_blank">${g.site}</a></td>
        </tr>
        `;
    });
    html += `</tbody></table>`;
    document.getElementById("tableContainer").innerHTML = html;
}

document.getElementById("winCategory").addEventListener("change", (e) => {
    renderTable(e.target.value);
});

// Initial render
renderTable("rated");
