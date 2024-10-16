const path = require("path");

module.exports = {
    entry: {
        main: "./assets/js/main.js",
        modal: "./assets/js/modal.js"
    },
    output: {
        filename: "[name].js",
        path: path.resolve(__dirname, "./apps/static/js"),
    },
};