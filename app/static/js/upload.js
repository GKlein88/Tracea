const fileInput = document.getElementById("gpx-upload");
const fileName = document.getElementById("file-name");

const uploadButton = document.getElementById("upload-button");
const expandButton = document.getElementById("expand-button");

const posterPreview = document.getElementById("poster-preview");
const posterContent = document.getElementById("poster-content");
const placeholderText = document.getElementById("placeholder-text");

const activityInfo = document.getElementById("activity-info");


uploadButton.addEventListener("click", () => {

    fileInput.click();

});



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



async function generatePoster(file) {


    const formData = new FormData();


    formData.append(
        "file",
        file
    );


    uploadButton.textContent = "Generating...";



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



function displayPoster(data) {

    // Display SVG

    posterContent.innerHTML = `
        <img
            src="${data.svg_url}"
            alt="Generated route poster"
        >
    `;


    // Display statistics

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