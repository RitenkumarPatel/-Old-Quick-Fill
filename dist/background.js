/******/ (() => { // webpackBootstrap
var __webpack_exports__ = {};
/*!**************************************!*\
  !*** ./src/background/background.ts ***!
  \**************************************/
chrome.commands.onCommand.addListener((command) => {
    if (command == 'Fill'){
        console.log("Ctrl+q pressed")
    }
})
/******/ })()
;
//# sourceMappingURL=background.js.map