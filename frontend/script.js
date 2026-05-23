console.log("SCRIPT LOADED");

const API_URL =
    "https://deck-analysis.onrender.com";

let startupProfile = null;

const uploadBtn = document.getElementById("uploadBtn");

uploadBtn.addEventListener("click", uploadPDF);

async function uploadPDF() {

    const file = document.getElementById("pdfInput").files[0];

    if (!file) {
        alert("Please select a PDF");
        return;
    }

    const deckGoal = document.getElementById("deckGoal").value;
    const deckType = document.getElementById("deckType").value;
    const fundSize = document.getElementById("fundSize").value;
    const growthFocus = document.getElementById("growthFocus").value;
    const deckTimeline = document.getElementById("deckTimeline").value;

    const status = document.getElementById("status");

    status.textContent = "Analyzing pitch deck...";

    try {

        const formData = new FormData();

        formData.append("file", file);
        formData.append("deck_goal", deckGoal);
        formData.append("deck_type", deckType);
        formData.append("fund_size", fundSize);
        formData.append("growth_focus", growthFocus);
        formData.append("deck_timeline", deckTimeline);

        console.log("Sending:");

        console.log({
            deckGoal,
            deckType,
            fundSize,
            growthFocus,
            deckTimeline
        });

        const response = await fetch(
            `${API_URL}/upload`,
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

        const data = await response.json();

        let report =
            data.report;

        startupProfile =
            data.startup_profile;

        if (typeof report === "string") {
            report = JSON.parse(report);
        }

        status.textContent = "Analysis Complete";

        renderDashboard(report);

    } catch (error) {

        console.error(error);

        status.textContent = "Failed to analyze PDF";

        document.getElementById("output").innerHTML = `
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

    const output = document.getElementById("output");

    const dimensionScores = report.dimension_scores || {};
    const strengths = report.top_strengths || [];
    const weaknesses = report.top_weaknesses || [];
    const missingSections = report.missing_sections || [];
    const redFlags = report.red_flags || [];
    const suggestions = report.improvement_suggestions || {};

    output.innerHTML = `

        

        <div class="score-card">

            <h2>Overall Score</h2>

            <div class="score">
                ${report.overall_score ?? "N/A"}
            </div>

            <p>
                <strong>Investment Readiness:</strong>
                ${report.investment_readiness ?? "N/A"}
            </p>

            <p>
                <strong>Confidence:</strong>
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
                        .map(item => `<li>${item}</li>`)
                        .join("")}
                </ul>

            </div>

            <div class="section">

                <h2>Top Weaknesses</h2>

                <ul>
                    ${weaknesses
                        .map(item => `<li>${item}</li>`)
                        .join("")}
                </ul>

            </div>

        </div>

        <div class="grid">

            <div class="section">

                <h2>Missing Sections</h2>

                <ul>
                    ${missingSections
                        .map(item => `<li>${item}</li>`)
                        .join("")}
                </ul>

            </div>

            <div class="section">

                <h2>Red Flags</h2>

                <ul>
                    ${redFlags
                        .map(item => `<li>${item}</li>`)
                        .join("")}
                </ul>

            </div>

        </div>

        <div class="section full-width">

            <h2>Improvement Suggestions</h2>

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

            <h2>Overall Recommendation</h2>

            <p class="recommendation">
                ${report.overall_recommendation || "N/A"}
            </p>

        </div>

        <div class="section full-width">

            <h2>
                Investor Outreach
            </h2>

            <p>
                Generate a personalized investor outreach email
                using this deck analysis.
            </p>

            <input
                type="text"
                id="linkedinUrl"
                placeholder="Paste LinkedIn profile URL"
            >

            <button id="generateEmailBtn">
                Generate Email
            </button>

            <div
                id="emailOutput"
                style="margin-top:20px;"
        ></div>

    </div>

    `;
    document.getElementById(
    "generateEmailBtn")
    .addEventListener(
    "click",
    generateInvestorEmail);
}

async function generateInvestorEmail() {

    const linkedinUrl =
        document.getElementById(
            "linkedinUrl"
        ).value;

    if (!linkedinUrl) {

        alert(
            "Please paste a LinkedIn URL"
        );

        return;
    }

    const emailOutput =
        document.getElementById(
            "emailOutput"
        );

    emailOutput.innerHTML =
        "<p>Generating email...</p>";

    try {

        const formData =
            new FormData();

        formData.append(
            "linkedin_url",
            linkedinUrl
        );

        formData.append(
            "startup_profile",
            JSON.stringify(
                startupProfile
            )
        );

        const response =
            await fetch(
                `${API_URL}/generate-email`,
                {
                    method: "POST",
                    body: formData
                }
            );

        if (!response.ok) {

            throw new Error(
                "Failed to generate email"
            );

        }

        const data =
            await response.json();

        emailOutput.innerHTML = `
            <div class="email-card">

                <h3>
                    Generated Email
                </h3>

                <div class="email-content">
        ${data.email}
                </div>

                <button
                    class="copy-btn"
                    id="copyEmailBtn"
                >
                    Copy Email
                </button>

            </div>
        `;

        document
        .getElementById("copyEmailBtn")
        .addEventListener("click", () => {

            navigator.clipboard.writeText(
                data.email
            );

            alert("Email copied");

});

    }
    catch(error){

        console.error(error);

        emailOutput.innerHTML =
            "<p>Failed to generate email</p>";

    }
}