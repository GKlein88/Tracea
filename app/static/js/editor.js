// =====================================
// Poster Editor
// =====================================

import { appState } from "./app-state.js";
import { formatDuration, parseSeconds } from "./formatter.js";
import { displayPoster } from "./upload.js";

const posterPreview = document.getElementById("poster-preview");

const editButton = document.getElementById("edit-button");
const editorLayout = document.getElementById("editor-layout");
const applyEditorButton = document.getElementById("apply-editor");
const closeEditorButton = document.getElementById("close-editor");
const resetEditorButton = document.getElementById("reset-editor");

const editorTitle = document.getElementById("editor-title");

const editorDistance = document.getElementById("editor-distance");
const showDistance = document.getElementById("show-distance");

const editorElevation = document.getElementById("editor-elevation");
const showElevation = document.getElementById("show-elevation");

const showDuration = document.getElementById("show-duration");

const titleFontSize = document.getElementById("title-font-size");
const titleAlign = document.getElementById("title-align");

// DOM References for Duration Controls (IDs HTML mis à jour)
const durationHoursInput = document.getElementById("editor-duration-hours");
const durationMinutesInput = document.getElementById("editor-duration-minutes");
const durationSecondsInput = document.getElementById("editor-duration-seconds");
const durationFormatSelect = document.getElementById("duration-format");


// =====================================
// EDITOR FUNCTIONS
// =====================================


/**
 * Loads current state values into the editor input fields.
 * Fallbacks to initial template configuration or raw GPX data if user state is empty.
 */
export function loadEditorValues() {
    // 1. Populate activity title input
    if (editorTitle) {
        editorTitle.value = appState.editorConfig.title || appState.activityName || "";
    }

    // 2. Retrieve default title settings from the current template JSON
    const titleConfig = appState.currentTemplate?.title || {};
    const defaultFontSize = titleConfig.font_size || 125;
    const defaultAnchor = titleConfig.text_anchor || "middle";
    
    let defaultAlign = "center";
    if (defaultAnchor === "start") defaultAlign = "start";
    else if (defaultAnchor === "end") defaultAlign = "end";

    // 3. Set title font size and alignment
    if (titleFontSize) {
        titleFontSize.value = appState.editorConfig.fontSize || defaultFontSize;
    }

    if (titleAlign) {
        titleAlign.value = appState.editorConfig.align || defaultAlign;
    }

    // 4. Restore statistics visibility checkboxes
    if (showDistance) {
        showDistance.checked = appState.editorConfig.stats.distance.enabled ?? true;
    }
    if (showElevation) {
        showElevation.checked = appState.editorConfig.stats.elevation.enabled ?? true;
    }
    if (showDuration) {
        showDuration.checked = appState.editorConfig.stats.duration.enabled ?? true;
    }

    // 5. Populate Distance and Elevation inputs
    const defaultDistance = String(appState.statistics.distance || "").replace(/[^0-9.,]/g, "").trim();
    if (editorDistance) {
        editorDistance.value = appState.editorConfig.stats.distance.value !== "" && appState.editorConfig.stats.distance.value !== undefined
            ? appState.editorConfig.stats.distance.value
            : defaultDistance;
    }

    const defaultElevation = String(appState.statistics.elevation || "").replace(/[^0-9]/g, "").trim();
    if (editorElevation) {
        editorElevation.value = appState.editorConfig.stats.elevation.value !== "" && appState.editorConfig.stats.elevation.value !== undefined
            ? appState.editorConfig.stats.elevation.value
            : defaultElevation;
    }

    // 6. Populate Duration inputs (Hours, Minutes, Seconds, Format)
    const rawDuration = parseSeconds(appState.statistics.duration);

    if (durationHoursInput) {
        durationHoursInput.value = appState.editorConfig.stats.duration.hours !== undefined
            ? appState.editorConfig.stats.duration.hours
            : rawDuration.hours;
    }

    if (durationMinutesInput) {
        durationMinutesInput.value = appState.editorConfig.stats.duration.minutes !== undefined
            ? appState.editorConfig.stats.duration.minutes
            : rawDuration.minutes;
    }

    if (durationSecondsInput) {
        durationSecondsInput.value = appState.editorConfig.stats.duration.seconds !== undefined
            ? appState.editorConfig.stats.duration.seconds
            : rawDuration.seconds;
    }

    if (durationFormatSelect) {
        durationFormatSelect.value = appState.editorConfig.stats.duration.format 
            || appState.currentTemplate?.stats?.duration_format 
            || "prime";
    }
}

/**
 * Reads user modifications from editor inputs, updates internal appState,
 * and renders changes dynamically onto the inline SVG elements.
 */
export async function updatePoster() {
    // 1. Sync title state
    let rawTitle = editorTitle ? editorTitle.value : "";
    appState.editorConfig.title = rawTitle;

    let upperTitle = rawTitle.toUpperCase();

    if (titleFontSize) {
        appState.editorConfig.fontSize = titleFontSize.value;
    }
    if (titleAlign) {
        appState.editorConfig.align = titleAlign.value;
    }

    // 2. Sync Distance & Elevation state
    if (editorDistance) {
        appState.editorConfig.stats.distance.value = editorDistance.value;
    }
    if (showDistance) {
        appState.editorConfig.stats.distance.enabled = showDistance.checked;
    }

    if (editorElevation) {
        appState.editorConfig.stats.elevation.value = editorElevation.value;
    }
    if (showElevation) {
        appState.editorConfig.stats.elevation.enabled = showElevation.checked;
    }

    // 3. Sync Duration inputs state (Hours, Minutes, Seconds, Format)
    const hours = durationHoursInput ? parseInt(durationHoursInput.value, 10) || 0 : 0;
    const minutes = durationMinutesInput ? parseInt(durationMinutesInput.value, 10) || 0 : 0;
    const seconds = durationSecondsInput ? parseInt(durationSecondsInput.value, 10) || 0 : 0;
    const style = durationFormatSelect ? durationFormatSelect.value : "prime";

    // Persist values in AppState so they stay retained after closing/opening
    appState.editorConfig.stats.duration.hours = hours;
    appState.editorConfig.stats.duration.minutes = minutes;
    appState.editorConfig.stats.duration.seconds = seconds;
    appState.editorConfig.stats.duration.format = style;

    if (showDuration) {
        appState.editorConfig.stats.duration.enabled = showDuration.checked;
    }

    // Compute formatted duration string dynamically
    const formattedDurationString = formatDuration({ hours, minutes, seconds }, style);

    // 4. Update SVG Title element
    const titleElement = document.getElementById("poster-title");
    if (titleElement) {
        const templateConfig = appState.currentTemplate?.title || {};
        const maxWidth = templateConfig.max_width || 1500;
        
        const canvasWidth = 1800;
        const sideMargin = 150;

        const templateFontSize = templateConfig.font_size || 125;
        const templateLineHeight = templateConfig.line_height || 125;

        const fontSizeVal = (titleFontSize && titleFontSize.value && parseFloat(titleFontSize.value) > 0)
            ? parseFloat(titleFontSize.value)
            : templateFontSize;

        const lineHeightRatio = templateLineHeight / templateFontSize;
        const computedLineHeight = fontSizeVal * lineHeightRatio;

        titleElement.setAttribute("font-size", `${fontSizeVal}px`);

        const alignVal = titleAlign ? titleAlign.value : "center";
        let targetX = canvasWidth / 2;

        if (alignVal === "start" || alignVal === "left") {
            targetX = sideMargin;
            titleElement.setAttribute("text-anchor", "start");
        } else if (alignVal === "end" || alignVal === "right") {
            targetX = canvasWidth - sideMargin;
            titleElement.setAttribute("text-anchor", "end");
        } else {
            targetX = canvasWidth / 2;
            titleElement.setAttribute("text-anchor", "middle");
        }

        const words = upperTitle.split(" ");
        const lines = [];
        let current = "";

        for (const word of words) {
            const test = current ? `${current} ${word}` : word;

            if (measureTextWidth(test, titleElement) <= maxWidth) {
                current = test;
            } else {
                if (current) lines.push(current);
                current = word;
            }
        }
        if (current) lines.push(current);

        const finalLines = lines.slice(0, 2);

        titleElement.innerHTML = ""; 

        finalLines.forEach((line, index) => {
            const tspan = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
            tspan.textContent = line;
            tspan.setAttribute("x", `${targetX}`);
            tspan.setAttribute("dy", index === 0 ? "0" : `${computedLineHeight}`);
            titleElement.appendChild(tspan);
        });
    }

    // 5. Update SVG Statistics elements
    const statsConfig = [
        { 
            id: "stat-distance", 
            enabled: appState.editorConfig.stats.distance.enabled, 
            value: appState.editorConfig.stats.distance.value 
        },
        { 
            id: "stat-elevation", 
            enabled: appState.editorConfig.stats.elevation.enabled, 
            value: appState.editorConfig.stats.elevation.value 
        },
        { 
            id: "stat-duration", 
            enabled: appState.editorConfig.stats.duration.enabled, 
            value: formattedDurationString 
        }
    ];

    statsConfig.forEach(stat => {
        const groupElement = document.getElementById(stat.id);
        if (groupElement) {
            groupElement.setAttribute("display", stat.enabled ? "inline" : "none");
            
            const valueElement = groupElement.querySelector("text .stat-value");
            if (valueElement) {
                valueElement.textContent = stat.value;
            } else {
                const textElement = groupElement.querySelector("text");
                if (textElement) {
                    textElement.textContent = stat.value;
                }
            }
        }
    });
}

function openEditor() {
    // Prevent opening if no active poster file or data is loaded
    if (!appState.posterUrl) {
        alert("No activity loaded.");
        return;
    }

    // Toggle active classes to slide in the side panel and adjust workspace layout
    editorLayout.classList.add("active");

    if (window.openFocusMode) {
        window.openFocusMode();
    }

    posterPreview.classList.add("editor-open");

    // Hydrate the form input elements with current state values
    loadEditorValues();
}


function closeEditor() {
    // Remove active layout classes to hide the panel and restore viewport
    editorLayout.classList.remove("active");
    posterPreview.classList.remove("editor-open");
}


// --- INPUT RESTRICTIONS (NUMERIC ONLY) ---
if (editorDistance) {
    editorDistance.addEventListener("input", (e) => {
        e.target.value = e.target.value.replace(/[^0-9.,]/g, "");
    });
}

if (editorElevation) {
    editorElevation.addEventListener("input", (e) => {
        e.target.value = e.target.value.replace(/[^0-9]/g, "");
    });
}

if (titleFontSize) {
    titleFontSize.addEventListener("input", (e) => {
        e.target.value = e.target.value.replace(/[^0-9]/g, "");
    });
}


// --- ALIGNMENT SELECT LISTENER ---
if (titleAlign) {
    titleAlign.addEventListener("change", () => {
        updatePoster();
    });
}


// --- MEASURE TEXT WIDTH UTILITY ---
function measureTextWidth(text, templateElement) {
    const svg = templateElement.ownerSVGElement;
    if (!svg) return 0;

    const testText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    testText.textContent = text;
    testText.style.fontFamily = templateElement.getAttribute("font-family");
    testText.style.fontSize = templateElement.getAttribute("font-size");
    testText.style.fontWeight = templateElement.getAttribute("font-weight");
    testText.style.visibility = "hidden";

    svg.appendChild(testText);
    const width = testText.getBBox().width;
    svg.removeChild(testText);

    return width;
}


// --- DURATION FORMAT SELECT LISTENER ---
if (durationFormatSelect) {
    durationFormatSelect.addEventListener("change", () => {
        updatePoster();
    });
}


// --- ENTER KEY TRIGGER FOR INPUTS ---
const editorInputs = [
    editorTitle, 
    titleFontSize, 
    editorDistance, 
    editorElevation, 
    durationHoursInput, 
    durationMinutesInput, 
    durationSecondsInput
];

editorInputs.forEach(inputElement => {
    if (inputElement) {
        inputElement.addEventListener("keydown", (event) => {
            if (event.key === "Enter") {
                event.preventDefault();
                updatePoster();
            }
        });
    }
});


// =====================================
// SCRIPT
// =====================================

window.closeEditor = closeEditor;

editButton.addEventListener("click", openEditor);

// APPLY BUTTON ACTION
applyEditorButton.addEventListener("click", async () => {
    await updatePoster();
});

// CLOSE BUTTON ACTION
if (closeEditorButton) {
    closeEditorButton.addEventListener("click", () => {
        closeEditor();
    });
}

let initState = {}
// RESET BUTTON ACTION
if (resetEditorButton) {
    resetEditorButton.addEventListener('click', () => {
        // console.log(appState)

        initState = {
            activity_name: appState.activityName,
            statistics: {
                distance_km: appState.statistics.distance,
                elevation_gain_m: appState.statistics.elevation,
                duration_seconds: appState.statistics.duration
            },
            template: "minimal",
            svg_url: appState.posterUrl
        };
        appState.editorConfig.fontSize = appState.currentTemplate.title.font_size || 125;

        const rawDuration = parseSeconds(appState.statistics.duration)

        appState.editorConfig.stats.duration.hours = rawDuration.hours
        appState.editorConfig.stats.duration.minutes = rawDuration.minutes
        appState.editorConfig.stats.duration.seconds = rawDuration.seconds
        appState.editorConfig.stats.duration.format = appState.currentTemplate.stats.duration_format

        // console.log(initState);
        displayPoster(initState);
    });
}