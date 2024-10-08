const path = require("path");

module.exports = {
    entry: {
        main: "./assets/js/main.js",
    },
    output: {
        filename: "[name].js",
        path: path.resolve(__dirname, "./apps/static/js"),
    },
};