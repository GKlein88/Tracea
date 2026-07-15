// =====================================
// Poster Viewer Interactions
// =====================================

// Poster elements
const posterPreview = document.getElementById("poster-preview");
const posterContent = document.getElementById("poster-content");

// Viewer buttons
const maximizeButton = document.getElementById("maximize-button");
const closeButton = document.getElementById("close-button");
const zoomInButton = document.getElementById("zoom-in-button");
const zoomOutButton = document.getElementById("zoom-out-button");
const resetZoomButton = document.getElementById("reset-zoom-button");


// Viewer state
let zoomLevel = 1;

let offsetX = 0;
let offsetY = 0;

let isDragging = false;

let startX = 0;
let startY = 0;


// Apply zoom and pan transform
function updatePosterTransform() {
    posterContent.style.transform =
        `
        translate(${offsetX}px, ${offsetY}px)
        scale(${zoomLevel})
        `;
}

// Reset poster zoom
function resetPosterZoom() {
    zoomLevel = 1;
    offsetX = 0;
    offsetY = 0;
    posterContent.style.transform = "";
}

// Reset zoom in focus mode
function resetZoom() {
    zoomLevel = 1;
    offsetX = 0;
    offsetY = 0;
    updatePosterTransform();
}

// Limit poster drag in focus mode
function limitPan() {
    const maxMove =
        250 * zoomLevel;
        
    offsetX = Math.max(
        Math.min(offsetX, maxMove),
        -maxMove
    );

    offsetY = Math.max(
        Math.min(offsetY, maxMove),
        -maxMove
    );
}


// Enter focus mode
maximizeButton.addEventListener("click", () => {
    resetPosterZoom();
    posterPreview.classList.add("focus-mode");
});


// Exit focus mode
closeButton.addEventListener("click", () => {
    posterPreview.classList.remove("focus-mode");
    resetPosterZoom();
});


// Exit focus mode with Escape key
document.addEventListener("keydown", (event) => {
    if (
        event.key === "Escape" &&
        posterPreview.classList.contains("focus-mode")
    ) {
        posterPreview.classList.remove("focus-mode");
        resetPosterZoom();
    }
});


// Zoom in
zoomInButton.addEventListener("click", () => {
    zoomLevel = Math.min(zoomLevel + 0.25, 3);

    updatePosterTransform();
});


// Zoom out
zoomOutButton.addEventListener("click", () => {
    zoomLevel = Math.max(zoomLevel - 0.25, 1);

    if (zoomLevel === 1) {
        offsetX = 0;
        offsetY = 0;
    }

    updatePosterTransform();
});


// Zoom poster with mouse wheel in focus mode
posterPreview.addEventListener("wheel", (event) => {

        // Disable zoom outside focus mode
        if (!posterPreview.classList.contains("focus-mode")) {
            return;
        }

        event.preventDefault();

        // Scroll up = zoom in
        if (event.deltaY < 0) {
            zoomLevel = Math.min(
                zoomLevel + 0.25,
                3
            );
        } 
        // Scroll down = zoom out
        else {
            zoomLevel = Math.max(
                zoomLevel - 0.25,
                1
            );

            // Reset position when returning to original scale
            if (zoomLevel === 1) {
                offsetX = 0;
                offsetY = 0;
            }
        }
        updatePosterTransform();
    },
    {
        passive:false
    }
);


// Reset zoom on click
if (resetZoomButton) {
    resetZoomButton.addEventListener("click", () => {
            resetZoom();
        }
    );
}


// Start moving poster when clicking and dragging
posterPreview.addEventListener("mousedown", (event) => {
        // Pan only works in focus mode and when zoomed
        if (
            event.button !== 0
            ||
            !posterPreview.classList.contains("focus-mode")
            ||
            zoomLevel <= 1
        ) {
            return;
        }

        event.preventDefault();
        isDragging = true;

        posterPreview.classList.add(
            "dragging"
        );

        startX = event.clientX - offsetX;
        startY = event.clientY - offsetY;
    }
);


// Move poster while dragging
document.addEventListener("mousemove", (event) => {

        if (!isDragging) {
            return;
        }

        offsetX = event.clientX - startX;
        offsetY = event.clientY - startY;

        limitPan();

        updatePosterTransform();
    }
);



// Stop moving poster after releasing mouse button
document.addEventListener("mouseup", () => {

        if (!isDragging) {
            return;
        }

        isDragging = false;

        posterPreview.classList.remove(
            "dragging"
        );
    }
);