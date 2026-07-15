// =====================================
// GPX Upload & Poster Generation
// =====================================


import { appState } from "./app-state.js";
import { formatDuration } from "./formatter.js";


// File input
const fileInput = document.getElementById("gpx-upload");
const fileName = document.getElementById("file-name");

// Upload button
const uploadButton = document.getElementById("upload-button");

// Poster elements
const posterContent = document.getElementById("poster-content");
const activityInfo = document.getElementById("activity-info");

// Open explorer
uploadButton.addEventListener("click", () => {
        fileInput.click();
    }
);


// File selected
fileInput.addEventListener("change", () => {

        const file =
            fileInput.files[0];

        if (!file) {
            return;
        }

        if (
            !file.name
                .toLowerCase()
                .endsWith(".gpx")
        ) {
            fileName.textContent = "Please select a GPX file.";
            fileInput.value = "";
            return;
        }

        fileName.textContent = file.name;

        generatePoster(file);
    }
);


// Generate poster

async function generatePoster(file) {

    const formData =
        new FormData();

    formData.append("file", file);

    uploadButton.textContent = "Generating ...";

    showGeneratingState();

    const response =
        await fetch(
            "/generate",
            {
                method:"POST",
                body:formData
            }
        );

    const data = await response.json();

    if (!data.success) {
        uploadButton.textContent =
            "Upload activity";
        return;
    }

    displayPoster(data);

    uploadButton.textContent = "Upload activity";
}


// Display poster
function displayPoster(data) {

    appState.activityName = data.activity_name;
    appState.posterUrl = data.svg_url;

    appState.statistics = {
        distance: `${data.statistics.distance_km.toFixed(1)} km`,
        elevation: `${data.statistics.elevation_gain_m} m`,
        duration:  data.statistics.duration_seconds ?? 0
    };

    posterContent.innerHTML = `
        <img
            src="${data.svg_url}"
            alt="Generated route poster"
        >
    `;

    activityInfo.innerHTML = `
        <h3> ${data.activity_name} </h3>

        <div class="activity-stats">
            <span>
                ↗ ${appState.statistics.distance}
            </span>

            <span>
                ▲ ${appState.statistics.elevation}
            </span>

            <span>
                ⏱ ${formatDuration(
                    appState.statistics.duration,
                    "clock"
                )}
</span>
        </div>

        <p class="activity-note">
            * Distance and elevation gain are calculated from your GPX file
        </p>
    `;
}

// Loading state

function showGeneratingState() {

    appState.posterUrl = "";
    appState.activityName = "";

    posterContent.innerHTML = `
        <div class="poster-empty-state loading">
            <span>.</span>
            <span>.</span>
            <span>.</span>
        </div>
    `;

    activityInfo.innerHTML = "";

    // Reset viewer if available
    if (
        window.resetPosterZoom
    ) {
        window.resetPosterZoom();
    }
}