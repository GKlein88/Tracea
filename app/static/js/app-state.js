// =====================================
// Application State
// Shared data between modules
// =====================================

export const appState = {

    // Current activity
    activityName: "",

    // Generated poster
    posterUrl: "",

    // Active loaded template configuration (JSON)
    currentTemplate: null,

    // GPX statistics
    statistics: {
        distance: 0,
        elevation: 0,
        duration: 0
    },

    // Current editor configuration
    editorConfig: {
        template: "minimal",
        title: "",
        stats: {
            distance: {
                enabled: true,
                value: 0
            },
            elevation: {
                enabled: true,
                value: 0
            },
            duration: {
                enabled: true,
                value: "",
                format: "clock"
            }
        }
    }
};