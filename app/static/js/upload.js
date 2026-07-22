// =====================================
// GPX Upload & Poster Generation
// =====================================

import { appState } from "./app-state.js";
import { formatDuration, parseSeconds } from "./formatter.js";
import { loadEditorValues } from "./editor.js"; 

// File input
const fileInput = document.getElementById("gpx-upload");
const fileName = document.getElementById("file-name");

// Upload button
const uploadButton = document.getElementById("upload-button");

// Poster elements
const posterContent = document.getElementById("poster-content");


// Open explorer
uploadButton.addEventListener("click", () => {
    fileInput.click();
});

// File selected
fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];

    if (!file) {
        return;
    }

    if (!file.name.toLowerCase().endsWith(".gpx")) {
        fileName.textContent = "Please select a GPX file.";
        fileInput.value = "";
        return;
    }

    fileName.textContent = file.name;

    generatePoster(file);
});


// Generate poster
async function generatePoster(file) {
    const formData = new FormData();
    formData.append("file", file);

    uploadButton.textContent = "Generating ...";

    showGeneratingState();

    try {
        const response = await fetch("/generate", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        // console.log(data);

        if (!data.success) {
            uploadButton.textContent = "Upload activity";
            return;
        }

        await displayPoster(data);
    } catch (error) {
        console.error("Error generating poster:", error);
    } finally {
        uploadButton.textContent = "Upload activity";
    }
}

// Display poster
export async function displayPoster(data) {

    // Set appState Values
    appState.activityName = data.activity_name;
    appState.posterUrl = data.svg_url;

    appState.statistics = {
        distance: data.statistics.distance_km ?? 0,
        elevation: data.statistics.elevation_gain_m ?? 0,
        duration: data.statistics.duration_seconds ?? 0
    };

    appState.editorConfig.title = data.activity_name;

    appState.editorConfig.stats.distance.value = data.statistics.distance_km ?? 0
    appState.editorConfig.stats.elevation.value = data.statistics.elevation_gain_m ?? 0
    appState.editorConfig.stats.duration.value = formatDuration(parseSeconds(data.statistics.duration_seconds ?? 0))

    // 1. Load active template JSON config into appState
    const templateName = data.template || appState.editorConfig.template || "minimal";
    if (data.template_config) {
        // If backend sends the JSON config directly in response
        appState.currentTemplate = data.template_config;
    } else {
        // Otherwise fetch the template JSON file directly
        try {
            const templateResponse = await fetch(`/static/poster-templates/${templateName}.json`);
            if (templateResponse.ok) {
                appState.currentTemplate = await templateResponse.json();
            }
        } catch (err) {
            console.warn("Could not load template JSON configuration:", err);
        }
    }

    // 2. Fetch and inject raw SVG into DOM
    try {
        const svgResponse = await fetch(data.svg_url);
        const svgContent = await svgResponse.text();
        posterContent.innerHTML = svgContent;
    } catch (error) {
        console.error("Error loading interactive SVG:", error);
        posterContent.innerHTML = `<img src="${data.svg_url}" alt="Generated route poster">`;
    }

    // 3. Update editor sidebar input values from appState & currentTemplate
    if (typeof loadEditorValues === "function") {
        loadEditorValues();
    }

}

// Loading state
function showGeneratingState() {
    appState.posterUrl = "";
    appState.activityName = "";
    appState.currentTemplate = null;

    posterContent.innerHTML = `
        <div class="poster-empty-state loading">
            <span>.</span>
            <span>.</span>
            <span>.</span>
        </div>
    `;

    // Reset viewer if available
    if (window.resetPosterZoom) {
        window.resetPosterZoom();
    }
}