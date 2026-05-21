const uploadBtn = document.getElementById("uploadBtn");

uploadBtn.addEventListener("click", uploadPDF);

async function uploadPDF() {
    const file = document.getElementById("pdfInput").files[0];

    if (!file) {
        alert("Please select a PDF");
        return;
    }

    const status = document.getElementById("status");
    status.textContent = "Analyzing pitch deck...";

    try {
        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch("http://localhost:9000/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        console.log(data);

        status.textContent = "Analysis Complete";
        renderDashboard(data.report);

    } catch (error) {
        console.error(error);
        status.textContent = "Failed to connect to backend";
    }
}

function renderDashboard(report) {
    const output = document.getElementById("output");

    output.innerHTML = `
        <div class="score-card">
            <h2>Overall Score</h2>
            <div class="score">${report.overall_score}</div>
            <p><strong>Investment Readiness:</strong> ${report.investment_readiness}</p>
            <p><strong>Confidence:</strong> ${report.confidence_level}</p>
        </div>

        <div class="grid">
            <div class="section">
                <h2>Dimension Scores</h2>
                ${Object.entries(report.dimension_scores)
                    .map(([key, value]) => `
                        <div class="metric">
                            <span>${key}</span>
                            <span>${value}</span>
                        </div>
                    `)
                    .join("")}
            </div>

            <div class="section">
                <h2>Reviewer Consensus</h2>
                <p><strong>Agreement:</strong> ${report.reviewer_consensus?.agreement_level || "-"}</p>
            </div>
        </div>

        <div class="grid">
            <div class="section">
                <h2>Top Strengths</h2>
                <ul>
                    ${report.top_strengths.map(item => `<li>${item}</li>`).join("")}
                </ul>
            </div>

            <div class="section">
                <h2>Top Weaknesses</h2>
                <ul>
                    ${report.top_weaknesses.map(item => `<li>${item}</li>`).join("")}
                </ul>
            </div>
        </div>

        <div class="grid">
            <div class="section">
                <h2>Missing Sections</h2>
                <ul>
                    ${report.missing_sections.map(item => `<li>${item}</li>`).join("")}
                </ul>
            </div>

            <div class="section">
                <h2>Red Flags</h2>
                <ul>
                    ${report.red_flags.map(item => `<li>${item}</li>`).join("")}
                </ul>
            </div>
        </div>

        <div class="section full-width">
            <h2>Improvement Suggestions</h2>
            ${Object.entries(report.improvement_suggestions)
                .map(([key, value]) => `
                    <div class="suggestion">
                        <h3>${key}</h3>
                        <p>${value}</p>
                    </div>
                `)
                .join("")}
        </div>

        <div class="section full-width">
            <h2>Overall Recommendation</h2>
            <p class="recommendation">${report.overall_recommendation}</p>
        </div>
    `;
}