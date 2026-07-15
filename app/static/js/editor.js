// =====================================
// Poster Editor
// =====================================

import { appState } from "./app-state.js";
import { formatDuration } from "./formatter.js";

const posterPreview = document.getElementById("poster-preview");

const editButton = document.getElementById("edit-button");
const editorLayout = document.getElementById("editor-layout");
const applyEditorButton = document.getElementById("apply-editor");

const editorTitle = document.getElementById("editor-title" );
const editorDistance = document.getElementById("editor-distance");
const editorElevation = document.getElementById("editor-elevation");
const editorDuration = document.getElementById("editor-duration");

const showDistance = document.getElementById("show-distance");
const showElevation = document.getElementById("show-elevation");
const showDuration = document.getElementById("show-duration");

const durationFormat = document.getElementById("duration-format");


function loadEditorValues(){

    editorTitle.value = appState.activityName;
    editorDistance.value = appState.statistics.distance;
    editorElevation.value = appState.statistics.elevation;
    editorDuration.value =
        formatDuration(
            appState.statistics.duration,
            durationFormat.value
        );
}


function openEditor(){

    if(!appState.posterUrl){
        alert(
            "No activity loaded."
        );
        return;
    }

    editorLayout.classList.add("active");

    if(window.openFocusMode){
        window.openFocusMode();
    }

    posterPreview.classList.add("editor-open");

    loadEditorValues();
}


function closeEditor(){

    editorLayout.classList.remove("active");
    posterPreview.classList.remove("editor-open");
}

window.closeEditor = closeEditor;

editButton.addEventListener("click", openEditor);

applyEditorButton.addEventListener("click", async ()=>{

        appState.editorConfig.title =editorTitle.value;

        appState.editorConfig.stats.distance = {
            enabled:
                showDistance.checked,
            value:
                editorDistance.value
        };

        appState.editorConfig.stats.elevation = {
            enabled:
                showElevation.checked,
            value:
                editorElevation.value
        };

        appState.editorConfig.stats.duration = {
            enabled:
                showDuration.checked,
            value:
                editorDuration.value,
            format:
                durationFormat.value
        };

        await updatePoster();

        closeEditor();

    }
);


async function updatePoster(){

    const formData = new FormData();

    formData.append( "config", JSON.stringify(appState.editorConfig) );

    const response =
        await fetch(
            "/update-poster",
            {
                method:"POST",
                body:formData
            }
        );

    const data = await response.json();

    if(data.success){
        // sera remplacé ensuite
        // par une fonction commune
        appState.posterUrl =
            data.svg_url;
    }
}