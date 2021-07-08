(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["subscriptions-pages-pricing-pricing-module"],{

/***/ "6M2z":
/*!****************************************************************************!*\
  !*** ./src/app/modules/subscriptions/pages/pricing/pricing.component.scss ***!
  \****************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (".header {\n  background-color: var(--background-base);\n  background-image: url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400' viewBox='0 0 800 800'%3E%3Cg fill='none' stroke='%23e6e6e6' stroke-width='1'%3E%3Cpath d='M769 229L1037 260.9M927 880L731 737 520 660 309 538 40 599 295 764 126.5 879.5 40 599-197 493 102 382-31 229 126.5 79.5-69-63'/%3E%3Cpath d='M-31 229L237 261 390 382 603 493 308.5 537.5 101.5 381.5M370 905L295 764'/%3E%3Cpath d='M520 660L578 842 731 737 840 599 603 493 520 660 295 764 309 538 390 382 539 269 769 229 577.5 41.5 370 105 295 -36 126.5 79.5 237 261 102 382 40 599 -69 737 127 880'/%3E%3Cpath d='M520-140L578.5 42.5 731-63M603 493L539 269 237 261 370 105M902 382L539 269M390 382L102 382'/%3E%3Cpath d='M-222 42L126.5 79.5 370 105 539 269 577.5 41.5 927 80 769 229 902 382 603 493 731 737M295-36L577.5 41.5M578 842L295 764M40-201L127 80M102 382L-261 269'/%3E%3C/g%3E%3Cg fill='%23e6e6e6'%3E%3Ccircle cx='769' cy='229' r='5'/%3E%3Ccircle cx='539' cy='269' r='5'/%3E%3Ccircle cx='603' cy='493' r='5'/%3E%3Ccircle cx='731' cy='737' r='5'/%3E%3Ccircle cx='520' cy='660' r='5'/%3E%3Ccircle cx='309' cy='538' r='5'/%3E%3Ccircle cx='295' cy='764' r='5'/%3E%3Ccircle cx='40' cy='599' r='5'/%3E%3Ccircle cx='102' cy='382' r='5'/%3E%3Ccircle cx='127' cy='80' r='5'/%3E%3Ccircle cx='370' cy='105' r='5'/%3E%3Ccircle cx='578' cy='42' r='5'/%3E%3Ccircle cx='237' cy='261' r='5'/%3E%3Ccircle cx='390' cy='382' r='5'/%3E%3C/g%3E%3C/svg%3E\");\n}\n\n.footer {\n  background-image: url(\"/assets/img/illustrations/it_support.svg\");\n  background-position: bottom right;\n  background-repeat: no-repeat;\n  background-size: 250px;\n  padding-bottom: 250px;\n}\n\n@media (min-width: 960px) {\n  .footer {\n    padding-bottom: 1rem;\n  }\n}\n\n.text-white {\n  color: white !important;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uLy4uL3ByaWNpbmcuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSx3Q0FBQTtFQUNBLDY1Q0FBQTtBQUNGOztBQUVBO0VBQ0UsaUVBQUE7RUFDQSxpQ0FBQTtFQUNBLDRCQUFBO0VBQ0Esc0JBQUE7RUFDQSxxQkFBQTtBQUNGOztBQUVBO0VBQ0U7SUFDRSxvQkFBQTtFQUNGO0FBQ0Y7O0FBRUE7RUFDRSx1QkFBQTtBQUFGIiwiZmlsZSI6InByaWNpbmcuY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyIuaGVhZGVyIHtcbiAgYmFja2dyb3VuZC1jb2xvcjogdmFyKC0tYmFja2dyb3VuZC1iYXNlKTtcbiAgYmFja2dyb3VuZC1pbWFnZTogdXJsKFwiZGF0YTppbWFnZS9zdmcreG1sLCUzQ3N2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPSc0MDAnIGhlaWdodD0nNDAwJyB2aWV3Qm94PScwIDAgODAwIDgwMCclM0UlM0NnIGZpbGw9J25vbmUnIHN0cm9rZT0nJTIzZTZlNmU2JyBzdHJva2Utd2lkdGg9JzEnJTNFJTNDcGF0aCBkPSdNNzY5IDIyOUwxMDM3IDI2MC45TTkyNyA4ODBMNzMxIDczNyA1MjAgNjYwIDMwOSA1MzggNDAgNTk5IDI5NSA3NjQgMTI2LjUgODc5LjUgNDAgNTk5LTE5NyA0OTMgMTAyIDM4Mi0zMSAyMjkgMTI2LjUgNzkuNS02OS02MycvJTNFJTNDcGF0aCBkPSdNLTMxIDIyOUwyMzcgMjYxIDM5MCAzODIgNjAzIDQ5MyAzMDguNSA1MzcuNSAxMDEuNSAzODEuNU0zNzAgOTA1TDI5NSA3NjQnLyUzRSUzQ3BhdGggZD0nTTUyMCA2NjBMNTc4IDg0MiA3MzEgNzM3IDg0MCA1OTkgNjAzIDQ5MyA1MjAgNjYwIDI5NSA3NjQgMzA5IDUzOCAzOTAgMzgyIDUzOSAyNjkgNzY5IDIyOSA1NzcuNSA0MS41IDM3MCAxMDUgMjk1IC0zNiAxMjYuNSA3OS41IDIzNyAyNjEgMTAyIDM4MiA0MCA1OTkgLTY5IDczNyAxMjcgODgwJy8lM0UlM0NwYXRoIGQ9J001MjAtMTQwTDU3OC41IDQyLjUgNzMxLTYzTTYwMyA0OTNMNTM5IDI2OSAyMzcgMjYxIDM3MCAxMDVNOTAyIDM4Mkw1MzkgMjY5TTM5MCAzODJMMTAyIDM4MicvJTNFJTNDcGF0aCBkPSdNLTIyMiA0MkwxMjYuNSA3OS41IDM3MCAxMDUgNTM5IDI2OSA1NzcuNSA0MS41IDkyNyA4MCA3NjkgMjI5IDkwMiAzODIgNjAzIDQ5MyA3MzEgNzM3TTI5NS0zNkw1NzcuNSA0MS41TTU3OCA4NDJMMjk1IDc2NE00MC0yMDFMMTI3IDgwTTEwMiAzODJMLTI2MSAyNjknLyUzRSUzQy9nJTNFJTNDZyBmaWxsPSclMjNlNmU2ZTYnJTNFJTNDY2lyY2xlIGN4PSc3NjknIGN5PScyMjknIHI9JzUnLyUzRSUzQ2NpcmNsZSBjeD0nNTM5JyBjeT0nMjY5JyByPSc1Jy8lM0UlM0NjaXJjbGUgY3g9JzYwMycgY3k9JzQ5Mycgcj0nNScvJTNFJTNDY2lyY2xlIGN4PSc3MzEnIGN5PSc3MzcnIHI9JzUnLyUzRSUzQ2NpcmNsZSBjeD0nNTIwJyBjeT0nNjYwJyByPSc1Jy8lM0UlM0NjaXJjbGUgY3g9JzMwOScgY3k9JzUzOCcgcj0nNScvJTNFJTNDY2lyY2xlIGN4PScyOTUnIGN5PSc3NjQnIHI9JzUnLyUzRSUzQ2NpcmNsZSBjeD0nNDAnIGN5PSc1OTknIHI9JzUnLyUzRSUzQ2NpcmNsZSBjeD0nMTAyJyBjeT0nMzgyJyByPSc1Jy8lM0UlM0NjaXJjbGUgY3g9JzEyNycgY3k9JzgwJyByPSc1Jy8lM0UlM0NjaXJjbGUgY3g9JzM3MCcgY3k9JzEwNScgcj0nNScvJTNFJTNDY2lyY2xlIGN4PSc1NzgnIGN5PSc0Micgcj0nNScvJTNFJTNDY2lyY2xlIGN4PScyMzcnIGN5PScyNjEnIHI9JzUnLyUzRSUzQ2NpcmNsZSBjeD0nMzkwJyBjeT0nMzgyJyByPSc1Jy8lM0UlM0MvZyUzRSUzQy9zdmclM0VcIik7XG59XG5cbi5mb290ZXIge1xuICBiYWNrZ3JvdW5kLWltYWdlOiB1cmwoXCIvYXNzZXRzL2ltZy9pbGx1c3RyYXRpb25zL2l0X3N1cHBvcnQuc3ZnXCIpO1xuICBiYWNrZ3JvdW5kLXBvc2l0aW9uOiBib3R0b20gcmlnaHQ7XG4gIGJhY2tncm91bmQtcmVwZWF0OiBuby1yZXBlYXQ7XG4gIGJhY2tncm91bmQtc2l6ZTogMjUwcHg7XG4gIHBhZGRpbmctYm90dG9tOiAyNTBweDtcbn1cblxuQG1lZGlhIChtaW4td2lkdGg6IDk2MHB4KSB7XG4gIC5mb290ZXIge1xuICAgIHBhZGRpbmctYm90dG9tOiAxcmVtO1xuICB9XG59XG5cbi50ZXh0LXdoaXRlIHtcbiAgY29sb3I6IHdoaXRlICFpbXBvcnRhbnQ7XG59Il19 */");

/***/ }),

/***/ "6qw8":
/*!********************************************************!*\
  !*** ./node_modules/@iconify/icons-ic/twotone-mail.js ***!
  \********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

var data = {
	"body": "<path opacity=\".3\" d=\"M20 6H4l8 4.99zM4 8v10h16V8l-8 5z\" fill=\"currentColor\"/><path d=\"M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 2l-8 4.99L4 6h16zm0 12H4V8l8 5l8-5v10z\" fill=\"currentColor\"/>",
	"width": 24,
	"height": 24
};
exports.__esModule = true;
exports.default = data;


/***/ }),

/***/ "7dR5":
/*!*******************************************************!*\
  !*** ./src/@vex/animations/scale-in-out.animation.ts ***!
  \*******************************************************/
/*! exports provided: scaleInOutAnimation */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "scaleInOutAnimation", function() { return scaleInOutAnimation; });
/* harmony import */ var _angular_animations__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/animations */ "GS7A");

const scaleInOutAnimation = Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["trigger"])('scaleInOut', [
    Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["transition"])(':enter', [
        Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["style"])({
            transform: 'scale(0)',
            opacity: 0
        }),
        Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["animate"])('0.2s cubic-bezier(0.35, 0, 0.25, 1)', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["style"])({
            transform: 'scale(1)',
            opacity: 1
        }))
    ]),
    Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["transition"])(':leave', [
        Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["style"])({
            transform: 'scale(1)',
            opacity: 1
        }),
        Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["animate"])('0.2s cubic-bezier(0.35, 0, 0.25, 1)', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["style"])({
            transform: 'scale(0)',
            opacity: 0
        }))
    ])
]);


/***/ }),

/***/ "DkW8":
/*!************************************************************!*\
  !*** ./node_modules/@iconify/icons-ic/twotone-beenhere.js ***!
  \************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

var data = {
	"body": "<path opacity=\".3\" d=\"M19 3H5v12.93l7 4.66l7-4.67V3zm-9 13l-4-4l1.41-1.41l2.58 2.58l6.59-6.59L18 8l-8 8z\" fill=\"currentColor\"/><path d=\"M19 1H5c-1.1 0-1.99.9-1.99 2L3 15.93c0 .69.35 1.3.88 1.66L12 23l8.11-5.41c.53-.36.88-.97.88-1.66L21 3c0-1.1-.9-2-2-2zm-7 19.6l-7-4.66V3h14v12.93l-7 4.67zm-2.01-7.42l-2.58-2.59L6 12l4 4l8-8l-1.42-1.42z\" fill=\"currentColor\"/>",
	"width": 24,
	"height": 24
};
exports.__esModule = true;
exports.default = data;


/***/ }),

/***/ "Nz9i":
/*!******************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/subscriptions/pages/pricing/pricing.component.html ***!
  \******************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div @stagger>\n  <div class=\"bg-card py-16 px-gutter\">\n    <h1 @fadeInUp class=\"display-2 mt-0 mb-4 text-center\">Pricing & Plans</h1>\n    <h2 @fadeInUp class=\"subheading-2 text-hint text-center max-w-lg mx-auto m-0\">Simple, transparent pricing.</h2>\n  </div>\n\n  <div class=\"my-12 container\"\n       fxLayout=\"row\"\n       fxLayout.xs=\"column\"\n       fxLayoutAlign=\"start start\"\n       fxLayoutAlign.xs=\"start stretch\"\n       fxLayoutGap=\"24px\">\n\n    <div @fadeInUp class=\"card p-6\" fxFlex fxLayout=\"column\" fxLayoutAlign=\"start center\" *ngFor=\"let plan of plans\">\n      <div [style.background-color]=\"theme.colors.primary['500'] | colorFade:0.9\"\n           class=\"inline-block p-6 rounded-full text-primary-500 mx-auto\"\n           fxLayout=\"row\"\n           fxLayoutAlign=\"center center\">\n        <ic-icon [icon]=\"icBeenhere\" size=\"48px\"></ic-icon>\n      </div>\n\n      <h2 class=\"headline mt-5\">{{ plan.name }}</h2>\n      <h4 class=\"mb-5 text-center text-secondary\">{{ plan.description }}</h4>\n\n      <div class=\"body-1\"><span class=\"body-2\">{{ plan.max_seats }}</span> Users</div>\n      <div class=\"body-1\"><span class=\"body-2\">{{ plan.max_projects }}</span> Projects</div>\n      <div class=\"body-1\"><span class=\"body-2\">10GB</span> Storage</div>\n      <div class=\"body-1\"><span class=\"body-2\">Basic</span> Support</div>\n\n      <div [ngClass]=\"{'text-white': plan.charge_amount === null}\">\n        <h3 class=\"display-2 font-bold mt-6\">\n          {{ plan.charge_amount }}<span ngClass=\"{'text-secondary': plan.charge_amount}\" class=\"headline align-top\">$</span>\n        </h3>\n\n        <span>per user/month</span>\n      </div>\n\n      <button\n        class=\"mt-5 max-w-full w-200\"\n        color=\"primary\"\n        (click)=\"buy(plan)\"\n        [disabled]=\"isSubscribed(plan)\"\n        mat-raised-button type=\"button\">\n        <span *ngIf=\"!isSubscribed(plan)\">\n          {{ plan.charge_amount === 0 ? 'CONTINUE FREE' : (plan.charge_amount ? 'GET STARTED' : 'CONTACT SALES') }}\n        </span>\n        <span *ngIf=\"isSubscribed(plan)\">\n          SUBSCRIBED\n        </span>\n      </button>\n    </div>\n  </div>\n\n  <div @fadeInUp class=\"bg-card py-16 px-gutter footer\">\n    <h2 class=\"display-1 mt-0 mb-4 text-center\">Still have questions?</h2>\n    <h3 class=\"subheading-2 text-hint text-center max-w-lg mx-auto m-0\">A wonderful serenity has taken possession of my\n      entire\n      soul, like these sweet\n      mornings of spring which I enjoy with my whole heart.</h3>\n\n    <div class=\"mt-16 max-w-3xl mx-auto flex flex-col md:flex-row\">\n      <a class=\"text-center p-6 border rounded md:w-1/2 md:mx-2\"\n         routerLinkActive>\n        <ic-icon [icon]=\"icPhoneInTalk\" class=\"text-hint\" size=\"42px\"></ic-icon>\n        <h3 class=\"title mb-0 mt-4\">+1 (840) 423-3404</h3>\n        <h4 class=\"subheading-2 m-0 text-hint\">Call us anytime for a quick solution</h4>\n      </a>\n\n      <a class=\"text-center p-6 border rounded md:w-1/2 md:mx-2\"\n         routerLinkActive>\n        <ic-icon [icon]=\"icMail\" class=\"text-hint\" size=\"42px\"></ic-icon>\n        <h3 class=\"title mb-0 mt-4\">support@example.com</h3>\n        <h4 class=\"subheading-2 m-0 text-hint\">Send us a mail to resolve your issue</h4>\n      </a>\n    </div>\n  </div>\n</div>\n");

/***/ }),

/***/ "ORuP":
/*!**************************************!*\
  !*** ./src/@vex/animations/index.ts ***!
  \**************************************/
/*! exports provided: dropdownAnimation, fadeInRightAnimation, fadeInRight400ms, fadeInUpAnimation, fadeInUp400ms, popoverAnimation, scaleFadeInAnimation, scaleFadeIn400ms, scaleInOutAnimation, scaleInAnimation, scaleIn400ms, staggerAnimation, stagger80ms, stagger60ms, stagger40ms, stagger20ms */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _dropdown_animation__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./dropdown.animation */ "T/nk");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "dropdownAnimation", function() { return _dropdown_animation__WEBPACK_IMPORTED_MODULE_0__["dropdownAnimation"]; });

/* harmony import */ var _fade_in_right_animation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./fade-in-right.animation */ "yriF");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "fadeInRightAnimation", function() { return _fade_in_right_animation__WEBPACK_IMPORTED_MODULE_1__["fadeInRightAnimation"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "fadeInRight400ms", function() { return _fade_in_right_animation__WEBPACK_IMPORTED_MODULE_1__["fadeInRight400ms"]; });

/* harmony import */ var _fade_in_up_animation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./fade-in-up.animation */ "y3Ys");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "fadeInUpAnimation", function() { return _fade_in_up_animation__WEBPACK_IMPORTED_MODULE_2__["fadeInUpAnimation"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "fadeInUp400ms", function() { return _fade_in_up_animation__WEBPACK_IMPORTED_MODULE_2__["fadeInUp400ms"]; });

/* harmony import */ var _popover_animation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./popover.animation */ "2e3Z");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "popoverAnimation", function() { return _popover_animation__WEBPACK_IMPORTED_MODULE_3__["popoverAnimation"]; });

/* harmony import */ var _scale_fade_in_animation__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./scale-fade-in.animation */ "U0RW");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "scaleFadeInAnimation", function() { return _scale_fade_in_animation__WEBPACK_IMPORTED_MODULE_4__["scaleFadeInAnimation"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "scaleFadeIn400ms", function() { return _scale_fade_in_animation__WEBPACK_IMPORTED_MODULE_4__["scaleFadeIn400ms"]; });

/* harmony import */ var _scale_in_out_animation__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./scale-in-out.animation */ "7dR5");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "scaleInOutAnimation", function() { return _scale_in_out_animation__WEBPACK_IMPORTED_MODULE_5__["scaleInOutAnimation"]; });

/* harmony import */ var _scale_in_animation__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./scale-in.animation */ "mu09");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "scaleInAnimation", function() { return _scale_in_animation__WEBPACK_IMPORTED_MODULE_6__["scaleInAnimation"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "scaleIn400ms", function() { return _scale_in_animation__WEBPACK_IMPORTED_MODULE_6__["scaleIn400ms"]; });

/* harmony import */ var _stagger_animation__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./stagger.animation */ "UOrl");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "staggerAnimation", function() { return _stagger_animation__WEBPACK_IMPORTED_MODULE_7__["staggerAnimation"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "stagger80ms", function() { return _stagger_animation__WEBPACK_IMPORTED_MODULE_7__["stagger80ms"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "stagger60ms", function() { return _stagger_animation__WEBPACK_IMPORTED_MODULE_7__["stagger60ms"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "stagger40ms", function() { return _stagger_animation__WEBPACK_IMPORTED_MODULE_7__["stagger40ms"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "stagger20ms", function() { return _stagger_animation__WEBPACK_IMPORTED_MODULE_7__["stagger20ms"]; });











/***/ }),

/***/ "PGLt":
/*!*******************************************************************!*\
  !*** ./node_modules/@iconify/icons-ic/twotone-business-center.js ***!
  \*******************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

var data = {
	"body": "<path opacity=\".3\" d=\"M15 17H9v-1H5v3h14v-3h-4zM4 14h5v-3h6v3h5V9H4z\" fill=\"currentColor\"/><path d=\"M20 7h-4V5l-2-2h-4L8 5v2H4c-1.1 0-2 .9-2 2v5c0 .75.4 1.38 1 1.73V19c0 1.11.89 2 2 2h14c1.11 0 2-.89 2-2v-3.28c.59-.35 1-.99 1-1.72V9c0-1.1-.9-2-2-2zM10 5h4v2h-4V5zm9 14H5v-3h4v1h6v-1h4v3zm-8-4v-2h2v2h-2zm9-1h-5v-3H9v3H4V9h16v5z\" fill=\"currentColor\"/>",
	"width": 24,
	"height": 24
};
exports.__esModule = true;
exports.default = data;


/***/ }),

/***/ "QKIt":
/*!*********************************************************!*\
  !*** ./node_modules/@iconify/icons-ic/twotone-stars.js ***!
  \*********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

var data = {
	"body": "<path opacity=\".3\" d=\"M19.47 9.16a8.027 8.027 0 0 0-7.01-5.14l2 4.71l5.01.43zm-7.93-5.14c-3.22.18-5.92 2.27-7.02 5.15l5.02-.43l2-4.72zm-7.31 6.12C4.08 10.74 4 11.36 4 12c0 2.48 1.14 4.7 2.91 6.17l1.11-4.75l-3.79-3.28zm15.54-.01l-3.79 3.28l1.1 4.76A7.99 7.99 0 0 0 20 12c0-.64-.09-1.27-.23-1.87zM7.84 18.82c1.21.74 2.63 1.18 4.15 1.18c1.53 0 2.95-.44 4.17-1.18L12 16.31l-4.16 2.51z\" fill=\"currentColor\"/><path d=\"M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zm7.48 7.16l-5.01-.43l-2-4.71c3.21.19 5.91 2.27 7.01 5.14zM12 8.06l1.09 2.56l2.78.24l-2.11 1.83l.63 2.73L12 13.98l-2.39 1.44l.63-2.72l-2.11-1.83l2.78-.24L12 8.06zm-.46-4.04l-2 4.72l-5.02.43c1.1-2.88 3.8-4.97 7.02-5.15zM4 12c0-.64.08-1.26.23-1.86l3.79 3.28l-1.11 4.75A8.014 8.014 0 0 1 4 12zm7.99 8c-1.52 0-2.94-.44-4.15-1.18L12 16.31l4.16 2.51A8.008 8.008 0 0 1 11.99 20zm5.1-1.83l-1.1-4.76l3.79-3.28c.13.6.22 1.23.22 1.87c0 2.48-1.14 4.7-2.91 6.17z\" fill=\"currentColor\"/>",
	"width": 24,
	"height": 24
};
exports.__esModule = true;
exports.default = data;


/***/ }),

/***/ "U0RW":
/*!********************************************************!*\
  !*** ./src/@vex/animations/scale-fade-in.animation.ts ***!
  \********************************************************/
/*! exports provided: scaleFadeInAnimation, scaleFadeIn400ms */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "scaleFadeInAnimation", function() { return scaleFadeInAnimation; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "scaleFadeIn400ms", function() { return scaleFadeIn400ms; });
/* harmony import */ var _angular_animations__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/animations */ "GS7A");

function scaleFadeInAnimation(duration) {
    return Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["trigger"])('scaleFadeIn', [
        Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["transition"])(':enter', [
            Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["style"])({
                transform: 'scale(0.8)',
                opacity: 0
            }),
            Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["animate"])(`${duration}ms cubic-bezier(0.35, 0, 0.25, 1)`, Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["style"])({
                transform: 'scale(1)',
                opacity: 1
            }))
        ])
    ]);
}
const scaleFadeIn400ms = scaleFadeInAnimation(400);


/***/ }),

/***/ "UOrl":
/*!**************************************************!*\
  !*** ./src/@vex/animations/stagger.animation.ts ***!
  \**************************************************/
/*! exports provided: staggerAnimation, stagger80ms, stagger60ms, stagger40ms, stagger20ms */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "staggerAnimation", function() { return staggerAnimation; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "stagger80ms", function() { return stagger80ms; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "stagger60ms", function() { return stagger60ms; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "stagger40ms", function() { return stagger40ms; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "stagger20ms", function() { return stagger20ms; });
/* harmony import */ var _angular_animations__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/animations */ "GS7A");

function staggerAnimation(timing) {
    return Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["trigger"])('stagger', [
        Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["transition"])('* => *', [
            Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["query"])('@fadeInUp, @fadeInRight, @scaleIn', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["stagger"])(timing, Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["animateChild"])()), { optional: true })
        ])
    ]);
}
const stagger80ms = staggerAnimation(80);
const stagger60ms = staggerAnimation(60);
const stagger40ms = staggerAnimation(40);
const stagger20ms = staggerAnimation(20);


/***/ }),

/***/ "Uqjg":
/*!***********************************************************************!*\
  !*** ./src/app/modules/subscriptions/pages/pricing/pricing.module.ts ***!
  \***********************************************************************/
/*! exports provided: PricingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PricingModule", function() { return PricingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _angular_material_menu__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/menu */ "rJgo");
/* harmony import */ var _vex_pipes_color_color_fade_module__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @vex/pipes/color/color-fade.module */ "Chvm");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _pricing_routing_module__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./pricing-routing.module */ "bqDx");
/* harmony import */ var _pricing_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./pricing.component */ "iYu/");











let PricingModule = class PricingModule {
};
PricingModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_pricing_component__WEBPACK_IMPORTED_MODULE_10__["PricingComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _pricing_routing_module__WEBPACK_IMPORTED_MODULE_9__["PricingRoutingModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_8__["IconModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_4__["MatButtonModule"],
            _angular_material_menu__WEBPACK_IMPORTED_MODULE_6__["MatMenuModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_5__["MatIconModule"],
            _vex_pipes_color_color_fade_module__WEBPACK_IMPORTED_MODULE_7__["ColorFadeModule"],
        ],
    })
], PricingModule);



/***/ }),

/***/ "bqDx":
/*!*******************************************************************************!*\
  !*** ./src/app/modules/subscriptions/pages/pricing/pricing-routing.module.ts ***!
  \*******************************************************************************/
/*! exports provided: PricingRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PricingRoutingModule", function() { return PricingRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _pricing_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./pricing.component */ "iYu/");




const routes = [
    {
        path: '',
        component: _pricing_component__WEBPACK_IMPORTED_MODULE_3__["PricingComponent"],
    },
];
let PricingRoutingModule = class PricingRoutingModule {
};
PricingRoutingModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
    })
], PricingRoutingModule);



/***/ }),

/***/ "iYu/":
/*!**************************************************************************!*\
  !*** ./src/app/modules/subscriptions/pages/pricing/pricing.component.ts ***!
  \**************************************************************************/
/*! exports provided: PricingComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PricingComponent", function() { return PricingComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_pricing_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./pricing.component.html */ "Nz9i");
/* harmony import */ var _pricing_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./pricing.component.scss */ "6M2z");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _iconify_icons_ic_twotone_beenhere__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @iconify/icons-ic/twotone-beenhere */ "DkW8");
/* harmony import */ var _iconify_icons_ic_twotone_beenhere__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_beenhere__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _iconify_icons_ic_twotone_business_center__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @iconify/icons-ic/twotone-business-center */ "PGLt");
/* harmony import */ var _iconify_icons_ic_twotone_business_center__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_business_center__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @iconify/icons-ic/twotone-mail */ "6qw8");
/* harmony import */ var _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _iconify_icons_ic_twotone_phone_in_talk__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @iconify/icons-ic/twotone-phone-in-talk */ "reS8");
/* harmony import */ var _iconify_icons_ic_twotone_phone_in_talk__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_phone_in_talk__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _iconify_icons_ic_twotone_stars__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @iconify/icons-ic/twotone-stars */ "QKIt");
/* harmony import */ var _iconify_icons_ic_twotone_stars__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_stars__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _vex_animations__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @vex/animations */ "ORuP");
/* harmony import */ var _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @vex/utils/tailwindcss */ "XXSj");
/* harmony import */ var _core_http__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @core/http */ "vAmI");
/* harmony import */ var _layout_services_layout_config_service__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @layout/services/layout-config.service */ "U9Lm");
/* harmony import */ var _users_services_user_data_service__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @users/services/user-data.service */ "O7ya");















let PricingComponent = class PricingComponent {
    constructor(layoutConfigService, route, router, userResource, userDataService) {
        this.layoutConfigService = layoutConfigService;
        this.route = route;
        this.router = router;
        this.userResource = userResource;
        this.userDataService = userDataService;
        this.icBeenhere = _iconify_icons_ic_twotone_beenhere__WEBPACK_IMPORTED_MODULE_5___default.a;
        this.icStars = _iconify_icons_ic_twotone_stars__WEBPACK_IMPORTED_MODULE_9___default.a;
        this.icBusinessCenter = _iconify_icons_ic_twotone_business_center__WEBPACK_IMPORTED_MODULE_6___default.a;
        this.icPhoneInTalk = _iconify_icons_ic_twotone_phone_in_talk__WEBPACK_IMPORTED_MODULE_8___default.a;
        this.icMail = _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_7___default.a;
        this.theme = _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_11__["default"];
        this.layoutConfigService.setIkaros();
    }
    ngOnInit() {
        this.plans = this.route.snapshot.data.plans;
        this.subscription = this.route.snapshot.data.subscription;
    }
    buy(plan) {
        const snapshot = this.route.snapshot;
        const organizationId = snapshot.queryParams.organization_id;
        if (!organizationId) {
            const user = this.userDataService.user;
            if (!user) {
                // If the user is not logged in, route then to login page
                this.router.navigate(['/login']);
            }
            else {
                this.userResource.profile({ organization: true }).subscribe((res) => {
                    const { organization_id: organizationId } = res;
                    this.showBuy(plan, organizationId);
                });
            }
        }
        else {
            this.showBuy(plan, snapshot.queryParams.organization_id);
        }
    }
    showBuy(plan, organizationId) {
        const path = '/subscriptions/buy';
        this.router.navigate([path], {
            queryParams: {
                organization_id: organizationId,
                plan_id: plan.id,
            },
        });
    }
    isSubscribed(plan) {
        if (!this.subscription) {
            return false;
        }
        return plan.id == this.subscription.plan.id;
    }
    ngOnDestroy() {
        this.layoutConfigService.setZeus();
    }
};
PricingComponent.ctorParameters = () => [
    { type: _layout_services_layout_config_service__WEBPACK_IMPORTED_MODULE_13__["LayoutConfigService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["ActivatedRoute"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["Router"] },
    { type: _core_http__WEBPACK_IMPORTED_MODULE_12__["UserResource"] },
    { type: _users_services_user_data_service__WEBPACK_IMPORTED_MODULE_14__["UserDataService"] }
];
PricingComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'vex-pricing',
        template: _raw_loader_pricing_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        animations: [
            _vex_animations__WEBPACK_IMPORTED_MODULE_10__["stagger60ms"],
            _vex_animations__WEBPACK_IMPORTED_MODULE_10__["fadeInUp400ms"],
        ],
        styles: [_pricing_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], PricingComponent);



/***/ }),

/***/ "mu09":
/*!***************************************************!*\
  !*** ./src/@vex/animations/scale-in.animation.ts ***!
  \***************************************************/
/*! exports provided: scaleInAnimation, scaleIn400ms */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "scaleInAnimation", function() { return scaleInAnimation; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "scaleIn400ms", function() { return scaleIn400ms; });
/* harmony import */ var _angular_animations__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/animations */ "GS7A");

function scaleInAnimation(duration) {
    return Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["trigger"])('scaleIn', [
        Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["transition"])(':enter', [
            Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["style"])({
                transform: 'scale(0)'
            }),
            Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["animate"])(`${duration}ms cubic-bezier(0.35, 0, 0.25, 1)`, Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["style"])({
                transform: 'scale(1)'
            }))
        ])
    ]);
}
const scaleIn400ms = scaleInAnimation(400);


/***/ }),

/***/ "reS8":
/*!*****************************************************************!*\
  !*** ./node_modules/@iconify/icons-ic/twotone-phone-in-talk.js ***!
  \*****************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

var data = {
	"body": "<path opacity=\".3\" d=\"M6.54 5h-1.5c.09 1.32.34 2.58.75 3.79l1.2-1.21c-.24-.83-.39-1.7-.45-2.58zm8.66 13.21c1.21.41 2.48.67 3.8.76v-1.5c-.88-.07-1.75-.22-2.6-.45l-1.2 1.19z\" fill=\"currentColor\"/><path d=\"M15 12h2c0-2.76-2.24-5-5-5v2c1.66 0 3 1.34 3 3zm4 0h2a9 9 0 0 0-9-9v2c3.87 0 7 3.13 7 7zm1 3.5c-1.25 0-2.45-.2-3.57-.57c-.1-.03-.21-.05-.31-.05c-.26 0-.51.1-.71.29l-2.2 2.2a15.045 15.045 0 0 1-6.59-6.59l2.2-2.21a.96.96 0 0 0 .25-1A11.36 11.36 0 0 1 8.5 4c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1c0 9.39 7.61 17 17 17c.55 0 1-.45 1-1v-3.5c0-.55-.45-1-1-1zM5.03 5h1.5c.07.88.22 1.75.45 2.58l-1.2 1.21c-.4-1.21-.66-2.47-.75-3.79zM19 18.97c-1.32-.09-2.6-.35-3.8-.76l1.2-1.2c.85.24 1.72.39 2.6.45v1.51z\" fill=\"currentColor\"/>",
	"width": 24,
	"height": 24
};
exports.__esModule = true;
exports.default = data;


/***/ }),

/***/ "y3Ys":
/*!*****************************************************!*\
  !*** ./src/@vex/animations/fade-in-up.animation.ts ***!
  \*****************************************************/
/*! exports provided: fadeInUpAnimation, fadeInUp400ms */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "fadeInUpAnimation", function() { return fadeInUpAnimation; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "fadeInUp400ms", function() { return fadeInUp400ms; });
/* harmony import */ var _angular_animations__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/animations */ "GS7A");

function fadeInUpAnimation(duration) {
    return Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["trigger"])('fadeInUp', [
        Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["transition"])(':enter', [
            Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["style"])({
                transform: 'translateY(20px)',
                opacity: 0
            }),
            Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["animate"])(`${duration}ms cubic-bezier(0.35, 0, 0.25, 1)`, Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["style"])({
                transform: 'translateY(0)',
                opacity: 1
            }))
        ])
    ]);
}
const fadeInUp400ms = fadeInUpAnimation(400);


/***/ }),

/***/ "yriF":
/*!********************************************************!*\
  !*** ./src/@vex/animations/fade-in-right.animation.ts ***!
  \********************************************************/
/*! exports provided: fadeInRightAnimation, fadeInRight400ms */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "fadeInRightAnimation", function() { return fadeInRightAnimation; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "fadeInRight400ms", function() { return fadeInRight400ms; });
/* harmony import */ var _angular_animations__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/animations */ "GS7A");

function fadeInRightAnimation(duration) {
    return Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["trigger"])('fadeInRight', [
        Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["transition"])(':enter', [
            Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["style"])({
                transform: 'translateX(-20px)',
                opacity: 0
            }),
            Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["animate"])(`${duration}ms cubic-bezier(0.35, 0, 0.25, 1)`, Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["style"])({
                transform: 'translateX(0)',
                opacity: 1
            }))
        ])
    ]);
}
const fadeInRight400ms = fadeInRightAnimation(400);


/***/ })

}]);
//# sourceMappingURL=subscriptions-pages-pricing-pricing-module-es2015.js.map