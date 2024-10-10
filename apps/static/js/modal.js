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

/***/ "./assets/js/modal.js":
/*!****************************!*\
  !*** ./assets/js/modal.js ***!
  \****************************/
/***/ (() => {

eval("(() => {\r\n    let modal, targetModal;\r\n    const wrapper = document.querySelector(\".modal-wrapper\")\r\n    const openModalBtns = document.querySelectorAll(\".openModal\");\r\n    const cancelBtns = document.querySelectorAll(\".cancelBtn\");\r\n    const modalBackground = document.querySelector(\".modalBackground\");\r\n\r\n\r\n    const openModal = (e) => {\r\n        e.preventDefault();\r\n        targetModal = e.currentTarget.getAttribute(\"data-target\");\r\n        modal = document.querySelector(`${targetModal}`);\r\n        modal.classList.remove(\"hidden\");\r\n        modalBackground.classList.remove(\"hidden\");\r\n        modal.focus();\r\n        !modal.classList.contains(\"no-inert\") && wrapper.setAttribute(\"inert\", \"\");\r\n    }\r\n\r\n    const closeModal = () => {\r\n        modal.classList.add(\"hidden\");\r\n        modalBackground.classList.add(\"hidden\");\r\n        wrapper.removeAttribute(\"inert\")\r\n        const openModalBtn = document.querySelector(`[data-target=\"${targetModal}\"]`)\r\n        openModalBtn.focus()\r\n    }\r\n\r\n    openModalBtns.forEach((btn) =>\r\n        btn.addEventListener(\"click\", openModal)\r\n    )\r\n\r\n    cancelBtns.forEach((btn) =>\r\n        btn.addEventListener(\"click\", closeModal)\r\n    )\r\n\r\n    modalBackground.addEventListener(\"click\", closeModal)\r\n    window.addEventListener(\"keyup\", (e) => {\r\n        if (e.key === \"Escape\" && !modal.classList.contains(\"hidden\")) {\r\n            closeModal()\r\n        }\r\n        })\r\n\r\n}) ();\n\n//# sourceURL=webpack://nursery/./assets/js/modal.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = {};
/******/ 	__webpack_modules__["./assets/js/modal.js"]();
/******/ 	
/******/ })()
;