// =====================================
// Duration Formatter
// =====================================


/**
 * Format duration from seconds.
 *
 * @param {number} seconds
 * @param {string} format
 * @returns {string}
 */

/**
 * Helper to parse raw total seconds into hours, minutes, and seconds.
 */
export function parseSeconds(totalSeconds) {
    const sec = parseInt(totalSeconds, 10) || 0;
    const hours = Math.floor(sec / 3600);
    const minutes = Math.floor((sec % 3600) / 60);
    const seconds = sec % 60;
    return { hours, minutes, seconds };
}

/**
 * Formats duration into string matching backend formatting.py logic.
 */

export function formatDuration(durationObj, style = "clock") {
    const hours = parseInt(durationObj.hours, 10) || 0;
    const minutes = parseInt(durationObj.minutes, 10) || 0;
    const secs = parseInt(durationObj.seconds, 10) || 0;

    const pad2 = (num) => String(num).padStart(2, "0");

    if (style === "clock") {
        return `${pad2(hours)}:${pad2(minutes)}:${pad2(secs)}`;
    }

    if (style === "hms") {
        return `${hours}h${pad2(minutes)}m${pad2(secs)}s`;
    }

    if (style === "prime") {
        return `${hours}h${pad2(minutes)}'${pad2(secs)}"`;
    }

    if (style === "short") {
        return `${hours}h${pad2(minutes)}`;
    }

    return `${pad2(hours)}:${pad2(minutes)}:${pad2(secs)}`;
}