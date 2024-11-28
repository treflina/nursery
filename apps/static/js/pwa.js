/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./assets/js/pwa.js":
/*!**************************!*\
  !*** ./assets/js/pwa.js ***!
  \**************************/
/***/ (() => {

eval("let deferredPrompt;\r\nwindow.addEventListener(\"beforeinstallprompt\", (e) => {\r\n    e.preventDefault();\r\n    deferredPrompt = e;\r\n\r\n    const header = document.querySelector(\".profile-container\");\r\n    const installButton = document.createElement(\"button\");\r\n\r\n    const icon = '<svg xmlns=\"http://www.w3.org/2000/svg\" title=\"Zainstaluj aplikację\" class=\"w-6 h-6\" viewBox=\"0 0 512 512\"><path d=\"M 280 24 Q 278 2 256 0 Q 234 2 232 24 L 232 294 L 232 294 L 137 199 L 137 199 Q 120 185 103 199 Q 89 216 103 233 L 239 369 L 239 369 Q 256 383 273 369 L 409 233 L 409 233 Q 423 216 409 199 Q 392 185 375 199 L 280 294 L 280 294 L 280 24 L 280 24 Z M 129 304 L 64 304 L 129 304 L 64 304 Q 37 305 19 323 Q 1 341 0 368 L 0 448 L 0 448 Q 1 475 19 493 Q 37 511 64 512 L 448 512 L 448 512 Q 475 511 493 493 Q 511 475 512 448 L 512 368 L 512 368 Q 511 341 493 323 Q 475 305 448 304 L 383 304 L 383 304 L 335 352 L 335 352 L 448 352 L 448 352 Q 463 353 464 368 L 464 448 L 464 448 Q 463 463 448 464 L 64 464 L 64 464 Q 49 463 48 448 L 48 368 L 48 368 Q 49 353 64 352 L 177 352 L 177 352 L 129 304 L 129 304 Z M 432 408 Q 430 386 408 384 Q 386 386 384 408 Q 386 430 408 432 Q 430 430 432 408 L 432 408 Z\" /></svg>'\r\n\r\n    installButton.innerHTML = icon\r\n\r\n    installButton.classList.add(\"btn-profile\");\r\n\r\n    installButton.addEventListener(\"click\", async () => {\r\n        if (deferredPrompt !== null) {\r\n            deferredPrompt.prompt();\r\n            const { outcome } = await deferredPrompt.userChoice;\r\n            if (outcome === \"accepted\") {\r\n                deferredPrompt = null;\r\n            }\r\n        }\r\n        installButton.style.display = \"none\";\r\n    });\r\n\r\n        header?.appendChild(installButton);\r\n    });\r\n\n\n//# sourceURL=webpack://nursery/./assets/js/pwa.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = {};
/******/ 	__webpack_modules__["./assets/js/pwa.js"]();
/******/ 	
/******/ })()
;