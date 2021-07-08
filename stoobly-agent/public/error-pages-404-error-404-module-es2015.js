(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["error-pages-404-error-404-module"],{

/***/ "50/R":
/*!****************************************************************!*\
  !*** ./src/app/modules/error/pages/404/error-404.component.ts ***!
  \****************************************************************/
/*! exports provided: Error404Component */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Error404Component", function() { return Error404Component; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_error_404_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./error-404.component.html */ "N0ro");
/* harmony import */ var _error_404_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./error-404.component.scss */ "h+t2");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _vex_services_config_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @vex/services/config.service */ "lC2v");
/* harmony import */ var _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @iconify/icons-ic/twotone-search */ "sF+I");
/* harmony import */ var _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_5__);






let Error404Component = class Error404Component {
    constructor(configService) {
        this.configService = configService;
        this.icSearch = _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_5___default.a;
        this.configService.setConfig('vex-layout-ikaros');
    }
    ngOnInit() {
    }
    ngOnDestroy() {
        this.configService.setConfig('vex-layout-zeus');
    }
};
Error404Component.ctorParameters = () => [
    { type: _vex_services_config_service__WEBPACK_IMPORTED_MODULE_4__["ConfigService"] }
];
Error404Component = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'vex-error404',
        template: _raw_loader_error_404_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_error_404_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], Error404Component);



/***/ }),

/***/ "C7IK":
/*!*********************************************************************!*\
  !*** ./src/app/modules/error/pages/404/error-404-routing.module.ts ***!
  \*********************************************************************/
/*! exports provided: Error404RoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Error404RoutingModule", function() { return Error404RoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _error_404_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./error-404.component */ "50/R");




const routes = [
    {
        path: '',
        component: _error_404_component__WEBPACK_IMPORTED_MODULE_3__["Error404Component"],
        data: {
            containerEnabled: true,
            toolbarShadowEnabled: true,
        },
    },
];
let Error404RoutingModule = class Error404RoutingModule {
};
Error404RoutingModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
    })
], Error404RoutingModule);



/***/ }),

/***/ "N0ro":
/*!********************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/error/pages/404/error-404.component.html ***!
  \********************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div class=\"w-full p-gutter text-center\">\n  <img class=\"w-full max-w-lg mx-auto mb-6\" src=\"assets/img/illustrations/data_center.svg\">\n\n  <h1 class=\"display-3 font-medium m-0\">404</h1>\n  <h2 class=\"headline m-0\">Page not found.</h2>\n\n  <div class=\"bg-card rounded-full overflow-hidden relative ltr:pl-5 rtl:pr-5 h-12 max-w-md w-full shadow-8 mx-auto mt-6\"\n       fxLayout=\"row\"\n       fxLayoutAlign=\"start center\">\n    <ic-icon [icon]=\"icSearch\" class=\"text-secondary\" fxFlex=\"none\" height=\"24px\" width=\"24px\"></ic-icon>\n    <input class=\"border-0 h-12 outline-none ltr:pl-4 rtl:pr-4 placeholder:text-secondary bg-card\"\n           fxFlex=\"auto\"\n           placeholder=\"Search for other pages ...\"\n           type=\"text\">\n  </div>\n</div>\n");

/***/ }),

/***/ "h+t2":
/*!******************************************************************!*\
  !*** ./src/app/modules/error/pages/404/error-404.component.scss ***!
  \******************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJlcnJvci00MDQuY29tcG9uZW50LnNjc3MifQ== */");

/***/ }),

/***/ "y9RA":
/*!*************************************************************!*\
  !*** ./src/app/modules/error/pages/404/error-404.module.ts ***!
  \*************************************************************/
/*! exports provided: Error404Module */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Error404Module", function() { return Error404Module; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _error_404_routing_module__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./error-404-routing.module */ "C7IK");
/* harmony import */ var _error_404_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./error-404.component */ "50/R");







let Error404Module = class Error404Module {
};
Error404Module = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_error_404_component__WEBPACK_IMPORTED_MODULE_6__["Error404Component"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _error_404_routing_module__WEBPACK_IMPORTED_MODULE_5__["Error404RoutingModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_4__["IconModule"],
        ],
    })
], Error404Module);



/***/ })

}]);
//# sourceMappingURL=error-pages-404-error-404-module-es2015.js.map