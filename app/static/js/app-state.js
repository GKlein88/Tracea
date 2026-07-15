// =====================================
// Application State
// Shared data between modules
// =====================================

export const appState = {

    // Current activity
    activityName: "",

    // Generated poster
    posterUrl: "",

    // GPX statistics
    statistics: {
        distance: "",
        elevation: "",
        duration: 0
    },


    // Current editor configuration
    editorConfig: {
        template: "minimal",
        title: "",
        stats: {
            distance: {
                enabled: true,
                value: ""
            },
            elevation: {
                enabled: true,
                value: ""
            },
            duration: {
                enabled: true,
                value: "",
                format: "clock"
            }
        }
    }
};