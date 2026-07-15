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
export function formatDuration(
    seconds,
    format = "hms"
) {

    if (
        seconds === undefined ||
        seconds === null ||
        seconds < 0
    ) {
        return "00:00:00";
    }

    const hours = Math.floor(
        seconds / 3600
    );

    const minutes = Math.floor(
        (seconds % 3600) / 60
    );

    const secs = Math.floor(
        seconds % 60
    );

    const hh = String(hours).padStart(2, "0");
    const mm = String(minutes).padStart(2, "0");
    const ss = String(secs).padStart(2, "0");

    switch(format) {

        // 01h02m36s
        case "hms":
            return `${hh}h${mm}m${ss}s`;

        // 01h02'36"
        case "prime":
            return `${hh}h${mm}'${ss}"`;

        // 01h02
        case "short":
            return `${hh}h${mm}`;

        // 01:02:36
        case "clock":
        default:
            return `${hh}:${mm}:${ss}`;
    }
}