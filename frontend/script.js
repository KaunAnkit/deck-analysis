console.log("SCRIPT LOADED");

const uploadBtn = document.getElementById("uploadBtn");

uploadBtn.addEventListener("click", uploadPDF);

async function uploadPDF() {

    const file =
        document.getElementById("pdfInput").files[0];

    if (!file) {
        alert("Please select a PDF");
        return;
    }

    const deckGoal =
        document.getElementById("deckGoal").value;

    const deckType =
        document.getElementById("deckType").value;

    const fundSize =
        document.getElementById("fundSize").value;

    const growthFocus =
        document.getElementById("growthFocus").value;

    const deckTimeline =
        document.getElementById("deckTimeline").value;

    const status =
        document.getElementById("status");

    status.textContent =
        "Analyzing pitch deck...";

    try {

        const formData =
            new FormData();

        formData.append(
            "file",
            file
        );

        formData.append(
            "deck_goal",
            deckGoal
        );

        formData.append(
            "deck_type",
            deckType
        );

        formData.append(
            "fund_size",
            fundSize
        );

        formData.append(
            "growth_focus",
            growthFocus
        );

        formData.append(
            "deck_timeline",
            deckTimeline
        );

        console.log("Sending:");

        console.log({
            deckGoal,
            deckType,
            fundSize,
            growthFocus,
            deckTimeline
        });

        const response =
            await fetch(
                "http://localhost:9000/upload",
                {
                    method: "POST",
                    body: formData
                }
            );

        if (!response.ok) {

            throw new Error(
                `Server error: ${response.status}`
            );

        }

        const data =
            await response.json();

        let report =
            data.report;

        if (typeof report === "string") {

            report =
                JSON.parse(report);

        }

        status.textContent =
            "Analysis Complete";

        renderDashboard(report);

    }
    catch (error) {

        console.error(error);

        status.textContent =
            "Failed to analyze PDF";

        document.getElementById("output")
            .innerHTML =
            `
            <div class="section">
                <h2>Error</h2>
                <p>${error.message}</p>
            </div>
            `;
    }
}

function renderDashboard(report) {

    console.log("Rendering dashboard...");
    console.log(report);

    const output =
        document.getElementById("output");

    const dimensionScores =
        report.dimension_scores || {};

    const strengths =
        report.top_strengths || [];

    const weaknesses =
        report.top_weaknesses || [];

    const missingSections =
        report.missing_sections || [];

    const redFlags =
        report.red_flags || [];

    const suggestions =
        report.improvement_suggestions || {};

    output.innerHTML = `

        <div class="score-card">
            <h2>Overall Score</h2>

            <div class="score">
                ${report.overall_score ?? "N/A"}
            </div>

            <p>
                <strong>
                    Investment Readiness:
                </strong>
                ${report.investment_readiness ?? "N/A"}
            </p>

            <p>
                <strong>
                    Confidence:
                </strong>
                ${report.confidence_level ?? "N/A"}
            </p>
        </div>

        <div class="grid">

            <div class="section">

                <h2>Dimension Scores</h2>

                ${Object.entries(dimensionScores)
                    .map(([key, value]) => `
                        <div class="metric">
                            <b><span>${key}</span></b>
                            <span>${value}</span>
                        </div>
                    `)
                    .join("")}

            </div>

            <div class="section">

                <h2>Reviewer Consensus</h2>

                <p>
                    <strong>Agreement:</strong>
                    ${report.reviewer_consensus?.agreement_level || "N/A"}
                </p>

            </div>

        </div>

        <div class="grid">

            <div class="section">

                <h2>Top Strengths</h2>

                <ul>
                    ${strengths
                        .map(item =>
                            `<li>${item}</li>`
                        )
                        .join("")}
                </ul>

            </div>

            <div class="section">

                <h2>Top Weaknesses</h2>

                <ul>
                    ${weaknesses
                        .map(item =>
                            `<li>${item}</li>`
                        )
                        .join("")}
                </ul>

            </div>

        </div>

        <div class="grid">

            <div class="section">

                <h2>Missing Sections</h2>

                <ul>
                    ${missingSections
                        .map(item =>
                            `<li>${item}</li>`
                        )
                        .join("")}
                </ul>

            </div>

            <div class="section">

                <h2>Red Flags</h2>

                <ul>
                    ${redFlags
                        .map(item =>
                            `<li>${item}</li>`
                        )
                        .join("")}
                </ul>

            </div>

        </div>

        <div class="section full-width">

            <h2>
                Improvement Suggestions
            </h2>

            ${Object.entries(suggestions)
                .map(([key, value]) => `
                    <div class="suggestion">
                        <h3>${key}</h3>
                        <p>${value}</p>
                    </div>
                `)
                .join("")}

        </div>

        <div class="section full-width">

            <h2>
                Overall Recommendation
            </h2>

            <p class="recommendation">
                ${report.overall_recommendation || "N/A"}
            </p>

        </div>

    `;
}