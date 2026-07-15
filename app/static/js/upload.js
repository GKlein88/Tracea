// =====================================
// GPX Upload & Poster Generation
// =====================================

// File input elements
const fileInput = document.getElementById("gpx-upload");
const fileName = document.getElementById("file-name");

// Upload button
const uploadButton = document.getElementById("upload-button");

// Activity information section
const activityInfo = document.getElementById("activity-info");


// Open file explorer when clicking upload button
uploadButton.addEventListener("click", () => {
    fileInput.click();
});


// Handle selected file
fileInput.addEventListener("change", () => {

    const file = fileInput.files[0];

    if (!file) {
        return;
    }

    // Only accept GPX files
    if (!file.name.toLowerCase().endsWith(".gpx")) {
        fileName.textContent = "Please select a GPX file.";
        fileInput.value = "";
        return;
    }

    fileName.textContent = file.name;

    generatePoster(file);

});


// Send GPX file to backend and generate poster
async function generatePoster(file) {

    const formData = new FormData();

    formData.append(
        "file",
        file
    );

    uploadButton.textContent = "Generating Preview...";

    const response = await fetch(
        "/generate",
        {
            method: "POST",
            body: formData
        }
    );

    const data = await response.json();

    if (!data.success) {
        uploadButton.textContent = "Upload activity";
        return;
    }

    displayPoster(data);

    uploadButton.textContent = "Upload activity";
}


// Display generated SVG and activity data
function displayPoster(data) {

    currentActivityName = data.activity_name;
    currentPosterUrl = data.svg_url;

    // Insert generated SVG into poster container
    posterContent.innerHTML = `
        <img
            src="${data.svg_url}"
            alt="Generated route poster"
        >
    `;

    // Insert activity information
    activityInfo.innerHTML = `

        <h3>
            ${data.activity_name}
        </h3>


        <div class="activity-stats">
            <span>
                ↗ ${data.statistics.distance_km.toFixed(1)} km
            </span>


            <span>
                ▲ ${data.statistics.elevation_gain_m} m
            </span>
        </div>


        <p class="activity-note">
            * Distance and elevation gain are calculated from your GPX file
        </p>

    `;
}