
const binForm = document.getElementById("binForm");

// Load and display all bins
async function loadBins() {
    const response = await fetch("/api/bins");
    const bins = await response.json();

    const table = document.getElementById("binTable");
    table.innerHTML = "";

    let normal = 0;
    let fillingUp = 0;
    let almostFull = 0;
    let full = 0;
    let warning = 0;
    let urgent = 0;

    bins.forEach(bin => {
        if (bin.status === "Normal") normal++;
        else if (bin.status === "Filling Up") fillingUp++;
        else if (bin.status === "Almost Full") almostFull++;
        else if (bin.status === "Full") full++;

        if (bin.fill_level >= 95) {
            urgent++;
        } else if (bin.fill_level >= 80) {
            warning++;
        }

    const fillColor = bin.fill_level >= 95
        ? "#d32f2f"
        : bin.fill_level >= 80
        ? "#e6a23c"
        : "#176b52";

    const statusClass = bin.status.toLowerCase().replace(/\s+/g, "-");

    table.innerHTML += `
        <tr>
            <td>${bin.bin_id}</td>
            <td>${bin.location}</td>
            <td>
                <div class="fill-container">
                    <div class="fill-bar">
                        <div class="fill-progress"
                            style="width: ${bin.fill_level}%; background: ${fillColor};">
                        </div>
                    </div>
                    <span>${bin.fill_level}%</span>
                </div>
            </td>
            <td>
                <span class="status-label ${statusClass}">
                    ${bin.status}
                </span>
            </td>
        </tr>
    `;
    });

    document.getElementById("totalBins").textContent = bins.length;
    document.getElementById("normalBins").textContent = normal;
    document.getElementById("almostFullBins").textContent =
        fillingUp + almostFull;
    document.getElementById("fullBins").textContent = full;
    document.getElementById("warningBins").textContent = warning;
    document.getElementById("urgentBins").textContent = urgent;

    displayAlerts(bins);
}

// Display collection alerts
function displayAlerts(bins) {
    const alertContainer = document.getElementById("alertContainer");

    const alertBins = bins.filter(bin => bin.fill_level >= 80);

    if (alertBins.length === 0) {
        alertContainer.innerHTML = "<p>No pending collection alerts.</p>";
        return;
    }

    alertContainer.innerHTML = "";

    alertBins.forEach(bin => {
        const isUrgent = bin.fill_level >= 95;
        const alertClass = isUrgent ? "urgent" : "warning";

        alertContainer.innerHTML += `
            <div class="alert-card">
                <div>
                    <strong>${bin.bin_id}</strong>
                    <p>${bin.location}</p>
                    <p>Fill Level: ${bin.fill_level}%</p>
                    <span class="${alertClass}">
                        ${isUrgent
                            ? 'Urgent Collection Required'
                            : 'Collection Should Be Planned'}
                    </span>
                </div>
            </div>
        `;
    });
}

// Load collection history
async function loadCollectionHistory() {
    const response = await fetch("/api/collection-history");
    const history = await response.json();

    const table = document.getElementById("historyTable");
    table.innerHTML = "";

    if (history.length === 0) {
        table.innerHTML = `
            <tr>
                <td colspan="4">No collection records yet.</td>
            </tr>
        `;
        return;
    }

    history.forEach((record, index) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${record.bin_id}</td>
            <td>${record.location}</td>
            <td>${record.collected_at}</td>
        `;

        table.appendChild(row);
    });
}

// Add a new bin
binForm.addEventListener("submit", async function(event) {
    event.preventDefault();

    const bin_id = document.getElementById("binId").value;
    const location = document.getElementById("location").value;

    const response = await fetch("/api/bins", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ bin_id, location })
    });

    const result = await response.json();
    alert(result.message);

    if (response.ok) {
        binForm.reset();
        await loadBins();
    }
});

// Generate automatic simulated sensor readings
async function updateSensorReadings() {
    const response = await fetch("/api/simulate", {
        method: "POST"
    });

    if (response.ok) {
        await loadBins();
    }
}

// Simulate automatic waste collection
async function simulateCollection() {
    const response = await fetch("/api/simulate-collection", {
        method: "POST"
    });

    const result = await response.json();

    console.log("Collection response:", result);

    if (result.bin_id) {
        await loadBins();
        await loadCollectionHistory();
    }
}

// Initial dashboard load
loadBins();
loadCollectionHistory();

// Update simulated sensor readings every 5 seconds
setInterval(updateSensorReadings, 5000);

// Simulate collection vehicle visit every 30 seconds
setInterval(simulateCollection, 30000);
