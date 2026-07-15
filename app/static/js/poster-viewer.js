// =====================================
// Poster Viewer
// Focus / Zoom / Pan / Download
// =====================================

import { appState } from "./app-state.js";

// Elements
const posterPreview = document.getElementById("poster-preview");
const posterContent = document.getElementById("poster-content");

const editorLayout = document.getElementById("editor-layout");

// Buttons
const maximizeButton = document.getElementById("maximize-button");
const closeButton = document.getElementById("close-button");
const zoomInButton = document.getElementById("zoom-in-button");
const zoomOutButton = document.getElementById("zoom-out-button");
const resetZoomButton = document.getElementById("reset-zoom-button" );

// Download
const downloadButton = document.getElementById("download-button");
const downloadModal = document.getElementById("download-modal");
const downloadClose = document.getElementById("download-close");
const confirmDownload = document.getElementById( "confirm-download");
const downloadName = document.getElementById("download-name");


let zoomLevel = 1;

let offsetX = 0;
let offsetY = 0;

let isDragging = false;

let startX = 0;
let startY = 0;



// =====================================
// Transform
// =====================================

function updatePosterTransform() {

    posterContent.style.transform =
        `
        translate(${offsetX}px, ${offsetY}px)
        scale(${zoomLevel})
        `;
}

function resetPosterZoom() {

    zoomLevel = 1;

    offsetX = 0;
    offsetY = 0;

    posterContent.style.transform = "";
}


window.resetPosterZoom = resetPosterZoom;

function limitPan() {

    const maxMove = 450 * zoomLevel;

    offsetX = Math.max( Math.min(offsetX,maxMove), -maxMove );
    offsetY = Math.max( Math.min(offsetY,maxMove), -maxMove );
}



// =====================================
// Focus mode
// =====================================

function openFocusMode(){

    resetPosterZoom();

    posterPreview.classList.add("focus-mode");
}

function closeFocusMode(){

    posterPreview.classList.remove(
        "focus-mode",
        "editor-open"
    );

    editorLayout.classList.remove("active");

    resetPosterZoom();
}

window.openFocusMode = openFocusMode;

window.closeFocusMode =  closeFocusMode;

maximizeButton.addEventListener( "click", openFocusMode);

closeButton.addEventListener( "click", () => {
        closeFocusMode();
        if(window.closeEditor){
            window.closeEditor();
        }
    }
);

document.addEventListener("keydown", event => {
        if(
            event.key === "Escape" &&
            posterPreview.classList.contains(
                "focus-mode"
            )
        ){
            closeFocusMode();
            if(window.closeEditor){
                window.closeEditor();
            }
        }
    }
);



// =====================================
// Zoom buttons
// =====================================

zoomInButton.addEventListener("click", ()=>{
        zoomLevel = Math.min( zoomLevel + .25, 3 );
        updatePosterTransform();
    }
);

zoomOutButton.addEventListener("click", ()=>{
        zoomLevel = Math.max( zoomLevel - .25, 1 );
        if(zoomLevel === 1){
            offsetX = 0;
            offsetY = 0;
        }

        updatePosterTransform();
    }
);

resetZoomButton.addEventListener("click",  resetPosterZoom);



// =====================================
// Wheel zoom
// =====================================

posterPreview.addEventListener("wheel", event =>{
        if(
            !posterPreview.classList.contains(
                "focus-mode"
            )
        ){
            return;
        }

        event.preventDefault();

        if(event.deltaY < 0){
            zoomLevel = Math.min( zoomLevel + .25, 3 );
        }
        else{
            zoomLevel = Math.max( zoomLevel - .25, 1 );

            if(zoomLevel === 1){
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



// =====================================
// Drag
// =====================================

posterPreview.addEventListener("mousedown", event =>{
        if(
            event.button !== 0 ||
            !posterPreview.classList.contains(
                "focus-mode"
            ) ||
            zoomLevel <= 1
        ){
            return;
        }

        event.preventDefault();

        isDragging = true;

        posterPreview.classList.add("dragging");

        startX = event.clientX - offsetX;
        startY = event.clientY - offsetY;
    }
);


document.addEventListener( "mousemove", event=>{
        if(!isDragging){
            return;
        }

        offsetX = event.clientX - startX;
        offsetY = event.clientY - startY;

        limitPan();

        updatePosterTransform();
    }
);


document.addEventListener( "mouseup", ()=>{
        isDragging = false;

        posterPreview.classList.remove("dragging");
    }
);



// =====================================
// Download
// =====================================

downloadButton.addEventListener("click", ()=>{
        if(!appState.posterUrl){
            alert(
                "No activity loaded."
            );
            return;
        }

        downloadName.value = appState.activityName;

        downloadModal.classList.add("active");
    }
);


downloadClose.addEventListener("click", ()=>{
        downloadModal.classList.remove("active");
    }
);


confirmDownload.addEventListener("click", ()=>{       

        const link = document.createElement("a");

        link.href = appState.posterUrl;
        link.download = `${downloadName.value}.svg`;

        link.click();

        downloadModal.classList.remove("active");
    }
);