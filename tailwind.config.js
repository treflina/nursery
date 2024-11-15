/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./apps/templates/**/*.{html,js}",
        "./apps/**/*.py",
        "./node_modules/flowbite/**/*.js",
        "./assets/js/*.js"
    ],
    theme: {
        extend: {},
    },
    plugins: [require('flowbite/plugin')],

};
