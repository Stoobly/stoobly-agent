(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["main"],{

/***/ "+f9C":
/*!***********************************************!*\
  !*** ./src/@vex/layout/layout.component.scss ***!
  \***********************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (".page-container {\n  bottom: 0;\n  display: flex;\n  flex-direction: column;\n  left: 0;\n  position: absolute;\n  right: 0;\n  top: 0;\n}\n\n.sidenav {\n  background: var(--sidenav-background);\n}\n\n.sidenav ::ng-deep .mat-drawer-inner-container {\n  overflow: hidden;\n}\n\n.content {\n  background: var(--background-base);\n  min-height: calc(100% - var(--toolbar-height) - var(--navigation-height));\n  position: relative;\n  width: 100%;\n}\n\n.has-footer .content {\n  min-height: calc(100% - var(--toolbar-height) - var(--navigation-height) - var(--footer-height));\n}\n\n.scroll-disabled {\n  overflow: hidden;\n}\n\n.scroll-disabled .content {\n  height: calc(100% - var(--toolbar-height) - var(--navigation-height));\n  min-height: unset;\n  overflow: hidden;\n}\n\n.scroll-disabled.has-fixed-footer .content, .scroll-disabled.has-footer .content {\n  height: calc(100% - var(--toolbar-height) - var(--navigation-height) - var(--footer-height));\n  min-height: unset;\n}\n\n.is-mobile ::ng-deep .vex-toolbar {\n  position: fixed;\n  width: 100%;\n}\n\n.is-mobile .content {\n  margin-top: var(--toolbar-height);\n}\n\n.sidenav-container {\n  background: var(--background-base);\n  height: 100%;\n  transition: transform 0.5s cubic-bezier(0.2, 1, 0.3, 1);\n}\n\n.sidenav-content {\n  overflow-x: hidden;\n  overflow-y: auto;\n}\n\n.with-search {\n  overflow: hidden;\n  position: fixed;\n}\n\n.with-search .sidenav-container {\n  pointer-events: none;\n  transform: perspective(1000px) translate3d(0, 50vh, 0) rotate3d(1, 0, 0, 30deg);\n  transform-origin: 50vw 50vh;\n  transition: transform 0.5s cubic-bezier(0.2, 1, 0.3, 1);\n  border-radius: 0.25rem;\n  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);\n  overflow: visible;\n}\n\n.toolbar-fixed ::ng-deep .vex-toolbar {\n  position: fixed;\n  width: var(--toolbar-width);\n  z-index: 50;\n}\n\n.toolbar-fixed .content {\n  margin-top: calc(var(--toolbar-height) + var(--navigation-height));\n}\n\n.has-fixed-footer ::ng-deep .vex-footer {\n  box-shadow: var(--footer-elevation);\n  position: fixed;\n}\n\n.has-fixed-footer .content {\n  margin-bottom: var(--footer-height);\n  min-height: calc(100% - var(--toolbar-height) - var(--navigation-height) - var(--footer-height));\n}\n\n.has-fixed-footer.scroll-disabled .content {\n  height: calc(100% - var(--toolbar-height) - var(--navigation-height) - var(--footer-height));\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uL2xheW91dC5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLFNBQUE7RUFDQSxhQUFBO0VBQ0Esc0JBQUE7RUFDQSxPQUFBO0VBQ0Esa0JBQUE7RUFDQSxRQUFBO0VBQ0EsTUFBQTtBQUNGOztBQUVBO0VBQ0UscUNBQUE7QUFDRjs7QUFFQTtFQUNFLGdCQUFBO0FBQ0Y7O0FBRUE7RUFDRSxrQ0FBQTtFQUNBLHlFQUFBO0VBQ0Esa0JBQUE7RUFDQSxXQUFBO0FBQ0Y7O0FBRUE7RUFDRSxnR0FBQTtBQUNGOztBQUVBO0VBQ0UsZ0JBQUE7QUFDRjs7QUFFQTtFQUNFLHFFQUFBO0VBQ0EsaUJBQUE7RUFDQSxnQkFBQTtBQUNGOztBQUVBO0VBQ0UsNEZBQUE7RUFDQSxpQkFBQTtBQUNGOztBQUVBO0VBQ0UsZUFBQTtFQUNBLFdBQUE7QUFDRjs7QUFFQTtFQUNFLGlDQUFBO0FBQ0Y7O0FBRUE7RUFDRSxrQ0FBQTtFQUNBLFlBQUE7RUFDQSx1REFBQTtBQUNGOztBQUVBO0VBQ0Usa0JBQUE7RUFDQSxnQkFBQTtBQUNGOztBQUVBO0VBQ0UsZ0JBQUE7RUFDQSxlQUFBO0FBQ0Y7O0FBRUE7RUFDRSxvQkFBQTtFQUNBLCtFQUFBO0VBQ0EsMkJBQUE7RUFDQSx1REFBQTtFQUNBLHNCQUFBO0VBQ0EsaURBQUE7RUFDQSxpQkFBQTtBQUNGOztBQUVBO0VBQ0UsZUFBQTtFQUNBLDJCQUFBO0VBQ0EsV0FBQTtBQUNGOztBQUVBO0VBQ0Usa0VBQUE7QUFDRjs7QUFFQTtFQUNFLG1DQUFBO0VBQ0EsZUFBQTtBQUNGOztBQUVBO0VBQ0UsbUNBQUE7RUFDQSxnR0FBQTtBQUNGOztBQUVBO0VBQ0UsNEZBQUE7QUFDRiIsImZpbGUiOiJsYXlvdXQuY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyIucGFnZS1jb250YWluZXIge1xuICBib3R0b206IDA7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGZsZXgtZGlyZWN0aW9uOiBjb2x1bW47XG4gIGxlZnQ6IDA7XG4gIHBvc2l0aW9uOiBhYnNvbHV0ZTtcbiAgcmlnaHQ6IDA7XG4gIHRvcDogMDtcbn1cblxuLnNpZGVuYXYge1xuICBiYWNrZ3JvdW5kOiB2YXIoLS1zaWRlbmF2LWJhY2tncm91bmQpO1xufVxuXG4uc2lkZW5hdiA6Om5nLWRlZXAgLm1hdC1kcmF3ZXItaW5uZXItY29udGFpbmVyIHtcbiAgb3ZlcmZsb3c6IGhpZGRlbjtcbn1cblxuLmNvbnRlbnQge1xuICBiYWNrZ3JvdW5kOiB2YXIoLS1iYWNrZ3JvdW5kLWJhc2UpO1xuICBtaW4taGVpZ2h0OiBjYWxjKDEwMCUgLSB2YXIoLS10b29sYmFyLWhlaWdodCkgLSB2YXIoLS1uYXZpZ2F0aW9uLWhlaWdodCkpO1xuICBwb3NpdGlvbjogcmVsYXRpdmU7XG4gIHdpZHRoOiAxMDAlO1xufVxuXG4uaGFzLWZvb3RlciAuY29udGVudCB7XG4gIG1pbi1oZWlnaHQ6IGNhbGMoMTAwJSAtIHZhcigtLXRvb2xiYXItaGVpZ2h0KSAtIHZhcigtLW5hdmlnYXRpb24taGVpZ2h0KSAtIHZhcigtLWZvb3Rlci1oZWlnaHQpKTtcbn1cblxuLnNjcm9sbC1kaXNhYmxlZCB7XG4gIG92ZXJmbG93OiBoaWRkZW47XG59XG5cbi5zY3JvbGwtZGlzYWJsZWQgLmNvbnRlbnQge1xuICBoZWlnaHQ6IGNhbGMoMTAwJSAtIHZhcigtLXRvb2xiYXItaGVpZ2h0KSAtIHZhcigtLW5hdmlnYXRpb24taGVpZ2h0KSk7XG4gIG1pbi1oZWlnaHQ6IHVuc2V0O1xuICBvdmVyZmxvdzogaGlkZGVuO1xufVxuXG4uc2Nyb2xsLWRpc2FibGVkLmhhcy1maXhlZC1mb290ZXIgLmNvbnRlbnQsIC5zY3JvbGwtZGlzYWJsZWQuaGFzLWZvb3RlciAuY29udGVudCB7XG4gIGhlaWdodDogY2FsYygxMDAlIC0gdmFyKC0tdG9vbGJhci1oZWlnaHQpIC0gdmFyKC0tbmF2aWdhdGlvbi1oZWlnaHQpIC0gdmFyKC0tZm9vdGVyLWhlaWdodCkpO1xuICBtaW4taGVpZ2h0OiB1bnNldDtcbn1cblxuLmlzLW1vYmlsZSA6Om5nLWRlZXAgLnZleC10b29sYmFyIHtcbiAgcG9zaXRpb246IGZpeGVkO1xuICB3aWR0aDogMTAwJTtcbn1cblxuLmlzLW1vYmlsZSAuY29udGVudCB7XG4gIG1hcmdpbi10b3A6IHZhcigtLXRvb2xiYXItaGVpZ2h0KTtcbn1cblxuLnNpZGVuYXYtY29udGFpbmVyIHtcbiAgYmFja2dyb3VuZDogdmFyKC0tYmFja2dyb3VuZC1iYXNlKTtcbiAgaGVpZ2h0OiAxMDAlO1xuICB0cmFuc2l0aW9uOiB0cmFuc2Zvcm0gMC41cyBjdWJpYy1iZXppZXIoMC4yLCAxLCAwLjMsIDEpO1xufVxuXG4uc2lkZW5hdi1jb250ZW50IHtcbiAgb3ZlcmZsb3cteDogaGlkZGVuO1xuICBvdmVyZmxvdy15OiBhdXRvO1xufVxuXG4ud2l0aC1zZWFyY2gge1xuICBvdmVyZmxvdzogaGlkZGVuO1xuICBwb3NpdGlvbjogZml4ZWQ7XG59XG5cbi53aXRoLXNlYXJjaCAuc2lkZW5hdi1jb250YWluZXIge1xuICBwb2ludGVyLWV2ZW50czogbm9uZTtcbiAgdHJhbnNmb3JtOiBwZXJzcGVjdGl2ZSgxMDAwcHgpIHRyYW5zbGF0ZTNkKDAsIDUwdmgsIDApIHJvdGF0ZTNkKDEsIDAsIDAsIDMwZGVnKTtcbiAgdHJhbnNmb3JtLW9yaWdpbjogNTB2dyA1MHZoO1xuICB0cmFuc2l0aW9uOiB0cmFuc2Zvcm0gMC41cyBjdWJpYy1iZXppZXIoMC4yLCAxLCAwLjMsIDEpO1xuICBib3JkZXItcmFkaXVzOiAwLjI1cmVtO1xuICBib3gtc2hhZG93OiAwIDI1cHggNTBweCAtMTJweCByZ2JhKDAsIDAsIDAsIDAuMjUpO1xuICBvdmVyZmxvdzogdmlzaWJsZTtcbn1cblxuLnRvb2xiYXItZml4ZWQgOjpuZy1kZWVwIC52ZXgtdG9vbGJhciB7XG4gIHBvc2l0aW9uOiBmaXhlZDtcbiAgd2lkdGg6IHZhcigtLXRvb2xiYXItd2lkdGgpO1xuICB6LWluZGV4OiA1MDtcbn1cblxuLnRvb2xiYXItZml4ZWQgLmNvbnRlbnQge1xuICBtYXJnaW4tdG9wOiBjYWxjKHZhcigtLXRvb2xiYXItaGVpZ2h0KSArIHZhcigtLW5hdmlnYXRpb24taGVpZ2h0KSk7XG59XG5cbi5oYXMtZml4ZWQtZm9vdGVyIDo6bmctZGVlcCAudmV4LWZvb3RlciB7XG4gIGJveC1zaGFkb3c6IHZhcigtLWZvb3Rlci1lbGV2YXRpb24pO1xuICBwb3NpdGlvbjogZml4ZWQ7XG59XG5cbi5oYXMtZml4ZWQtZm9vdGVyIC5jb250ZW50IHtcbiAgbWFyZ2luLWJvdHRvbTogdmFyKC0tZm9vdGVyLWhlaWdodCk7XG4gIG1pbi1oZWlnaHQ6IGNhbGMoMTAwJSAtIHZhcigtLXRvb2xiYXItaGVpZ2h0KSAtIHZhcigtLW5hdmlnYXRpb24taGVpZ2h0KSAtIHZhcigtLWZvb3Rlci1oZWlnaHQpKTtcbn1cblxuLmhhcy1maXhlZC1mb290ZXIuc2Nyb2xsLWRpc2FibGVkIC5jb250ZW50IHtcbiAgaGVpZ2h0OiBjYWxjKDEwMCUgLSB2YXIoLS10b29sYmFyLWhlaWdodCkgLSB2YXIoLS1uYXZpZ2F0aW9uLWhlaWdodCkgLSB2YXIoLS1mb290ZXItaGVpZ2h0KSk7XG59Il19 */");

/***/ }),

/***/ "+fow":
/*!*********************************************!*\
  !*** ./src/app/data/schema/path-segment.ts ***!
  \*********************************************/
/*! exports provided: PathSegment */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PathSegment", function() { return PathSegment; });
/* harmony import */ var _request_component__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./request-component */ "2bXN");

class PathSegment extends _request_component__WEBPACK_IMPORTED_MODULE_0__["RequestComponent"] {
    constructor(pathSegment) {
        super(2, pathSegment.id, pathSegment.alias);
        this.position = pathSegment.position;
        this.name = pathSegment.name;
        this.aliasName = pathSegment.alias_name;
    }
}


/***/ }),

/***/ "+mfJ":
/*!*******************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/layout/custom-layout.component.html ***!
  \*******************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<ng-template #sidenavRef>\n  <vex-sidenav [collapsed]=\"(sidenavCollapsed$ | async) && !(sidenavCollapsedOpen$ | async)\"></vex-sidenav>\n</ng-template>\n\n<ng-template #toolbarRef>\n  <vex-toolbar [hasShadow]=\"toolbarShadowEnabled$ | async\"\n               [mobileQuery]=\"!(isDesktop$ | async)\"\n               class=\"vex-toolbar\"></vex-toolbar>\n</ng-template>\n\n<ng-template #footerRef>\n  <vex-footer *ngIf=\"isFooterVisible$ | async\" class=\"vex-footer\"></vex-footer>\n</ng-template>\n\n<ng-template #quickpanelRef>\n  <vex-quickpanel></vex-quickpanel>\n</ng-template>\n\n<vex-layout [footerRef]=\"footerRef\"\n            [quickpanelRef]=\"quickpanelRef\"\n            [sidenavRef]=\"sidenavRef\"\n            [toolbarRef]=\"toolbarRef\"></vex-layout>\n<!-- CONFIGPANEL -->\n<!-- <vex-config-panel-toggle (openConfig)=\"configpanel.open()\"></vex-config-panel-toggle>\n\n<vex-sidebar #configpanel [invisibleBackdrop]=\"true\" position=\"right\">\n  <vex-config-panel></vex-config-panel>\n</vex-sidebar> -->\n<!-- END CONFIGPANEL -->\n");

/***/ }),

/***/ "/7a8":
/*!**************************************************************!*\
  !*** ./src/@vex/components/scrollbar/scrollbar.directive.ts ***!
  \**************************************************************/
/*! exports provided: ScrollbarDirective */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ScrollbarDirective", function() { return ScrollbarDirective; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var simplebar__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! simplebar */ "pvl8");



let ScrollbarDirective = class ScrollbarDirective {
    constructor(_element, zone) {
        this._element = _element;
        this.zone = zone;
    }
    ngAfterContentInit() {
        this.zone.runOutsideAngular(() => {
            this.scrollbarRef = new simplebar__WEBPACK_IMPORTED_MODULE_2__["default"](this._element.nativeElement, this.options);
        });
    }
};
ScrollbarDirective.ctorParameters = () => [
    { type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["ElementRef"] },
    { type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["NgZone"] }
];
ScrollbarDirective.propDecorators = {
    options: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"], args: ['vexScrollbar',] }]
};
ScrollbarDirective = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Directive"])({
        selector: '[vexScrollbar],vex-scrollbar',
        host: {
            class: 'vex-scrollbar'
        }
    })
], ScrollbarDirective);



/***/ }),

/***/ "/8CK":
/*!*************************************!*\
  !*** ./src/app/data/schema/user.ts ***!
  \*************************************/
/*! exports provided: User */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "User", function() { return User; });
class User {
    constructor(user) {
        this.id = user.id;
        this.email = user.email;
        this.name = user.name;
        this.lastSignInAt = new Date(user.last_sign_in_at);
        this.createdAt = new Date(user.created_at);
        this.apiKey = user.api_key;
    }
}


/***/ }),

/***/ "/JUU":
/*!********************************************!*\
  !*** ./src/app/core/http/agent.service.ts ***!
  \********************************************/
/*! exports provided: AgentService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AgentService", function() { return AgentService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _core_utils_uri_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @core/utils/uri.service */ "BjwJ");
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @environments/environment */ "AytR");
/* harmony import */ var _http_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./http.service */ "gHic");





let AgentService = class AgentService {
    constructor(httpService, uri) {
        this.httpService = httpService;
        this.uri = uri;
        this.DO_PROXY_HEADER = 'X-Do-Proxy';
        this.SERVICE_URL_HEADER = 'X-Service-Url';
        this.RECORD_POLICY_HEADER = 'X-Record-Policy';
        this.MOCK_POLICY_HEADER = 'X-Mock-Policy';
        this.RECORD_NONE_POLICY = 'record_any';
        this.CONFIGS_ENDPOINT = '/api/v1/admin/configs';
        this.STATUSES_ENDPOINT = '/api/v1/admin/statuses';
    }
    showStatus(statusId) {
        return this.sendGetRequest(`${this.STATUSES_ENDPOINT}/${statusId}`);
    }
    showConfigsModes() {
        return this.sendGetRequest(`${this.CONFIGS_ENDPOINT}/modes`);
    }
    showConfigsPolicies() {
        return this.sendGetRequest(`${this.CONFIGS_ENDPOINT}/policies`);
    }
    showConfig(queryParams) {
        return this.sendGetRequest(this.CONFIGS_ENDPOINT, queryParams);
    }
    createConfig(body) {
        return this.sendPostRequest(this.CONFIGS_ENDPOINT, body);
    }
    updateConfig(body) {
        return this.sendPutRequest(`${this.CONFIGS_ENDPOINT}`, body);
    }
    sendRequest(request) {
        const uri = new this.uri.class(request.url);
        const headers = { SERVICE_URL_HEADER: uri.origin };
        if (request.headers) {
            request.headers.forEach(header => {
                headers[header.name] = header.value;
            });
        }
        const queryParams = {};
        if (request.queryParams) {
            request.queryParams.forEach(queryParam => {
                queryParams[queryParam.anme] = queryParam.value;
            });
        }
        let observable;
        switch (request.method) {
            case 'GET':
                observable = this.sendGetRequest(uri.pathname, queryParams, { headers });
        }
        return observable;
    }
    sendGetRequest(path, queryParams, options) {
        const url = `${_environments_environment__WEBPACK_IMPORTED_MODULE_3__["environment"].agentUrl}${path}`;
        return this.httpService.get(url, queryParams, options);
    }
    sendPostRequest(path, body, options) {
        const url = `${_environments_environment__WEBPACK_IMPORTED_MODULE_3__["environment"].agentUrl}${path}`;
        return this.httpService.post(url, body, options);
    }
    sendPutRequest(path, body, options) {
        const url = `${_environments_environment__WEBPACK_IMPORTED_MODULE_3__["environment"].agentUrl}${path}`;
        return this.httpService.put(url, body, options);
    }
};
AgentService.ctorParameters = () => [
    { type: _http_service__WEBPACK_IMPORTED_MODULE_4__["HttpService"] },
    { type: _core_utils_uri_service__WEBPACK_IMPORTED_MODULE_2__["UriService"] }
];
AgentService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], AgentService);



/***/ }),

/***/ 0:
/*!***************************!*\
  !*** multi ./src/main.ts ***!
  \***************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! /home/jvlarble/bitbucket/stoobly-dashboard/src/main.ts */"zUnb");


/***/ }),

/***/ "0mz7":
/*!****************************!*\
  !*** ./tailwind.config.js ***!
  \****************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = {
  prefix: '',
  important: ':root',
  separator: ':',
  theme: {
    screens: {
      sm: '600px',
      md: '960px',
      lg: '1280px'
    },
    colors: {
      transparent: 'transparent',

      black: 'var(--text-color)',
      white: 'var(--text-color-light)',
      'contrast-black': 'black',
      'contrast-white': 'white',

      gray: {
        50: '#fafafa',
        100: '#f5f5f5',
        200: '#eeeeee',
        300: '#e0e0e0',
        400: '#bdbdbd',
        500: '#9e9e9e',
        600: '#757575',
        700: '#616161',
        800: '#424242',
        900: '#212121',
      },
      red: {
        50: '#ffebee',
        100: '#ffcdd2',
        200: '#ef9a9a',
        300: '#e57373',
        400: '#ef5350',
        500: '#f44336',
        600: '#e53935',
        700: '#d32f2f',
        800: '#c62828',
        900: '#b71c1c',
      },
      orange: {
        50: '#fff3e0',
        100: '#ffe0b2',
        200: '#ffcc80',
        300: '#ffb74d',
        400: '#ffa726',
        500: '#ff9800',
        600: '#fb8c00',
        700: '#f57c00',
        800: '#ef6c00',
        900: '#e65100',
      },
      'deep-orange': {
        50: '#fbe9e7',
        100: '#ffccbc',
        200: '#ffab91',
        300: '#ff8a65',
        400: '#ff7043',
        500: '#ff5722',
        600: '#f4511e',
        700: '#e64a19',
        800: '#d84315',
        900: '#bf360c',
      },
      amber: {
        50: '#fff8e1',
        100: '#ffecb3',
        200: '#ffe082',
        300: '#ffd54f',
        400: '#ffca28',
        500: '#ffc107',
        600: '#ffb300',
        700: '#ffa000',
        800: '#ff8f00',
        900: '#ff6f00',
      },
      'light-green': {
        50: '#f1f8e9',
        100: '#dcedc8',
        200: '#c5e1a5',
        300: '#aed581',
        400: '#9ccc65',
        500: '#8bc34a',
        600: '#7cb342',
        700: '#689f38',
        800: '#558b2f',
        900: '#33691e',
      },
      green: {
        50: '#e8f5e9',
        100: '#c8e6c9',
        200: '#a5d6a7',
        300: '#81c784',
        400: '#66bb6a',
        500: '#4caf50',
        600: '#43a047',
        700: '#388e3c',
        800: '#2e7d32',
        900: '#1b5e20',
      },
      teal: {
        50: '#e0f2f1',
        100: '#b2dfdb',
        200: '#80cbc4',
        300: '#4db6ac',
        400: '#26a69a',
        500: '#009688',
        600: '#00897b',
        700: '#00796b',
        800: '#00695c',
        900: '#004d40',
      },
      cyan: {
        50: '#e0f7fa',
        100: '#b2ebf2',
        200: '#80deea',
        300: '#4dd0e1',
        400: '#26c6da',
        500: '#00bcd4',
        600: '#00acc1',
        700: '#0097a7',
        800: '#00838f',
        900: '#006064',
      },
      purple: {
        50: '#f3e5f5',
        100: '#e1bee7',
        200: '#ce93d8',
        300: '#ba68c8',
        400: '#ab47bc',
        500: '#9c27b0',
        600: '#8e24aa',
        700: '#7b1fa2',
        800: '#6a1b9a',
        900: '#4a148c',
      },
      'deep-purple': {
        50: '#ede7f6',
        100: '#d1c4e9',
        200: '#b39ddb',
        300: '#9575cd',
        400: '#7e57c2',
        500: '#673ab7',
        600: '#5e35b1',
        700: '#512da8',
        800: '#4527a0',
        900: '#311b92',
      },
      primary: {
        50: '#ecefff',
        100: '#ced7ff',
        200: '#aebcff',
        300: '#8ea1ff',
        400: '#758cff',
        500: '#5c77ff',
        600: '#5570ff',
        700: '#4b65ff',
        800: '#415bff',
        900: '#3048ff',
      }
    },
    spacing: {
      px: '1px',
      gutter: 'var(--padding-gutter)',
      '0': '0',
      '1': '0.25rem',
      '2': '0.5rem',
      '3': '0.75rem',
      '4': '1rem',
      '5': '1.25rem',
      '6': '1.5rem',
      '8': '2rem',
      '9': '2.25rem',
      '10': '2.5rem',
      '12': '3rem',
      '14': '3.5rem',
      '16': '4rem',
      '20': '5rem',
      '24': '6rem',
      '32': '8rem',
      '40': '10rem',
      '48': '12rem',
      '56': '14rem',
      '64': '16rem',
    },
    backgroundColor: theme => ({
      base: 'var(--background-base)',
      card: 'var(--background-card)',
      'app-bar': 'var(--background-app-bar)',
      hover: 'var(--background-hover)',
      ...theme('colors'),
    }),
    backgroundPosition: {
      bottom: 'bottom',
      center: 'center',
      left: 'left',
      'left-bottom': 'left bottom',
      'left-top': 'left top',
      right: 'right',
      'right-bottom': 'right bottom',
      'right-top': 'right top',
      top: 'top',
    },
    backgroundSize: {
      auto: 'auto',
      cover: 'cover',
      contain: 'contain',
    },
    borderColor: theme => ({
      ...theme('colors'),
      default: 'var(--foreground-divider)',
    }),
    borderRadius: {
      none: '0',
      sm: '0.125rem',
      default: '0.25rem',
      lg: '0.5rem',
      full: '9999px',
    },
    borderWidth: {
      default: '1px',
      '0': '0',
      '2': '2px',
      '4': '4px',
      '8': '8px',
    },
    boxShadow: {
      default: 'var(--elevation-z6)',
      md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      lg: '0px 7px 8px -4px rgba(82, 63, 104, 0.06),0px 12px 17px 2px rgba(82, 63, 104, 0.042),0px 5px 22px 4px rgba(82, 63, 104, 0.036)',
      xl: '0px 8px 10px -5px rgba(82, 63, 104, 0.06),0px 16px 24px 2px rgba(82, 63, 104, 0.042),0px 6px 30px 5px rgba(82, 63, 104, 0.036)',
      '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
      inner: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
      outline: '0 0 0 3px rgba(66, 153, 225, 0.5)',
      none: 'none',
      b: '0 10px 30px 0 rgba(82,63,104,.06)',
      1: 'var(--elevation-z1)',
      2: 'var(--elevation-z2)',
      3: 'var(--elevation-z3)',
      4: 'var(--elevation-z4)',
      5: 'var(--elevation-z5)',
      6: 'var(--elevation-z6)',
      7: 'var(--elevation-z7)',
      8: 'var(--elevation-z8)',
      9: 'var(--elevation-z9)',
      10: 'var(--elevation-z10)',
      11: 'var(--elevation-z11)',
      12: 'var(--elevation-z12)',
      13: 'var(--elevation-z13)',
      14: 'var(--elevation-z14)',
      15: 'var(--elevation-z15)',
      16: 'var(--elevation-z16)',
      17: 'var(--elevation-z17)',
      18: 'var(--elevation-z18)',
      19: 'var(--elevation-z19)',
      20: 'var(--elevation-z20)',
    },
    container: {
      center: true,
      padding: 'var(--padding-gutter)'
    },
    cursor: {
      auto: 'auto',
      default: 'default',
      pointer: 'pointer',
      wait: 'wait',
      text: 'text',
      move: 'move',
      'not-allowed': 'not-allowed',
    },
    fill: {
      current: 'currentColor',
    },
    flex: {
      '1': '1 1 0%',
      auto: '1 1 auto',
      initial: '0 1 auto',
      none: 'none',
    },
    flexGrow: {
      '0': '0',
      default: '1',
    },
    flexShrink: {
      '0': '0',
      default: '1',
    },
    fontFamily: {
      sans: [
        'Roboto',
        '-apple-system',
        'BlinkMacSystemFont',
        '"Segoe UI"',
        'Roboto',
        '"Helvetica Neue"',
        'Arial',
        '"Noto Sans"',
        'sans-serif',
        '"Apple ColorDef Emoji"',
        '"Segoe UI Emoji"',
        '"Segoe UI Symbol"',
        '"Noto ColorDef Emoji"',
      ],
      serif: [
        'Georgia',
        'Cambria',
        '"Times New Roman"',
        'Times',
        'serif',
      ],
      mono: [
        'Menlo',
        'Monaco',
        'Consolas',
        '"Liberation Mono"',
        '"Courier New"',
        'monospace',
      ],
    },
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      lg: '1.125rem',
      xl: '1.25rem',
      '2xl': '1.5rem',
      '3xl': '1.875rem',
      '4xl': '2.25rem',
      '5xl': '3rem',
      '6xl': '4rem',
    },
    fontWeight: {
      hairline: '100',
      thin: '200',
      light: '300',
      normal: '400',
      medium: '500',
      semibold: '600',
      bold: '700',
      extrabold: '800',
      black: '900',
    },
    height: theme => ({
      auto: 'auto',
      ...theme('spacing'),
      full: '100%',
      screen: '100vh',
    }),
    inset: {
      '0': '0',
      '1': '0.25rem',
      '2': '0.5rem',
      '3': '0.75rem',
      '4': '1rem',
      '5': '1.25rem',
      '6': '1.5rem',
      '8': '2rem',
      '10': '2.5rem',
      '12': '3rem',
      '-1': '-0.25rem',
      '-2': '-0.5rem',
      '-3': '-0.75rem',
      '-4': '-1rem',
      '-5': '-1.25rem',
      '-6': '-1.5rem',
      '-8': '-2rem',
      '-10': '-2.5rem',
      '-12': '-3rem',
      auto: 'auto',
    },
    letterSpacing: {
      tighter: '-0.05em',
      tight: '-0.025em',
      normal: '0',
      wide: '0.025em',
      wider: '0.05em',
      widest: '0.1em',
    },
    lineHeight: {
      none: '1',
      tight: '1.25',
      snug: '1.375',
      normal: '1.5',
      relaxed: '1.625',
      loose: '2',
    },
    listStyleType: {
      none: 'none',
      disc: 'disc',
      decimal: 'decimal',
    },
    margin: (theme, {negative}) => ({
      auto: 'auto',
      ...theme('spacing'),
      ...negative(theme('spacing')),
      ...negative({
        gutter: 'var(--padding-gutter)'
      })
    }),
    maxHeight: {
      full: '100%',
      screen: '100vh',
    },
    maxWidth: {
      xxxs: '16rem',
      xxs: '18rem',
      xs: '20rem',
      sm: '24rem',
      md: '28rem',
      lg: '32rem',
      xl: '36rem',
      '2xl': '42rem',
      '3xl': '48rem',
      '4xl': '56rem',
      '5xl': '64rem',
      '6xl': '72rem',
      full: '100%',
    },
    minHeight: {
      '0': '0',
      full: '100%',
      screen: '100vh',
    },
    minWidth: theme => ({
      '0': '0',
      full: '100%',
      ...theme('spacing')
    }),
    objectPosition: {
      bottom: 'bottom',
      center: 'center',
      left: 'left',
      'left-bottom': 'left bottom',
      'left-top': 'left top',
      right: 'right',
      'right-bottom': 'right bottom',
      'right-top': 'right top',
      top: 'top',
    },
    opacity: {
      '0': '0',
      '25': '0.25',
      '50': '0.5',
      '75': '0.75',
      '100': '1',
    },
    order: {
      first: '-9999',
      last: '9999',
      none: '0',
      '1': '1',
      '2': '2',
      '3': '3',
      '4': '4',
      '5': '5',
      '6': '6',
      '7': '7',
      '8': '8',
      '9': '9',
      '10': '10',
      '11': '11',
      '12': '12',
    },
    padding: theme => theme('spacing'),
    placeholderColor: theme => theme('colors'),
    stroke: {
      current: 'currentColor',
    },
    textColor: theme => ({
      'secondary': 'var(--text-secondary)',
      'hint': 'var(--text-hint)',
      ...theme('colors'),
      'primary-contrast': {
        50: '#000',
        100: '#000',
        200: '#000',
        300: '#000',
        400: '#000',
        500: '#FFF',
        600: '#FFF',
        700: '#FFF',
        800: '#FFF',
        900: '#FFF',
      },
      'red-contrast': {
        50: '#000',
        100: '#000',
        200: '#000',
        300: '#000',
        400: '#000',
        500: '#FFF',
        600: '#FFF',
        700: '#FFF',
        800: '#FFF',
        900: '#FFF',
      },
      'green-contrast': {
        50: '#000',
        100: '#000',
        200: '#000',
        300: '#000',
        400: '#000',
        500: '#FFF',
        600: '#FFF',
        700: '#FFF',
        800: '#FFF',
        900: '#FFF',
      },
      'amber-contrast': {
        50: '#000',
        100: '#000',
        200: '#000',
        300: '#000',
        400: '#000',
        500: '#000',
        600: '#000',
        700: '#000',
        800: '#000',
        900: '#000',
      },
      'orange-contrast': {
        50: '#000',
        100: '#000',
        200: '#000',
        300: '#000',
        400: '#000',
        500: '#000',
        600: '#000',
        700: '#000',
        800: '#FFF',
        900: '#FFF',
      },
      'deep-orange-contrast': {
        50: '#000',
        100: '#000',
        200: '#000',
        300: '#000',
        400: '#000',
        500: '#FFF',
        600: '#FFF',
        700: '#FFF',
        800: '#FFF',
        900: '#FFF',
      },
      'purple-contrast': {
        50: '#000',
        100: '#000',
        200: '#000',
        300: '#FFF',
        400: '#FFF',
        500: '#FFF',
        600: '#FFF',
        700: '#FFF',
        800: '#FFF',
        900: '#FFF',
      },
      'deep-purple-contrast': {
        50: '#000',
        100: '#000',
        200: '#000',
        300: '#FFF',
        400: '#FFF',
        500: '#FFF',
        600: '#FFF',
        700: '#FFF',
        800: '#FFF',
        900: '#FFF',
      },
      'cyan-contrast': {
        50: '#000',
        100: '#000',
        200: '#000',
        300: '#000',
        400: '#000',
        500: '#FFF',
        600: '#FFF',
        700: '#FFF',
        800: '#FFF',
        900: '#FFF',
      },
      'teal-contrast': {
        50: '#000',
        100: '#000',
        200: '#000',
        300: '#000',
        400: '#000',
        500: '#FFF',
        600: '#FFF',
        700: '#FFF',
        800: '#FFF',
        900: '#FFF',
      },
      'gray-contrast': {
        50: '#000',
        100: '#000',
        200: '#000',
        300: '#000',
        400: '#000',
        500: '#FFF',
        600: '#FFF',
        700: '#FFF',
        800: '#FFF',
        900: '#FFF',
      },
      'light-green-contrast': {
        50: '#000',
        100: '#000',
        200: '#000',
        300: '#000',
        400: '#000',
        500: '#000',
        600: '#000',
        700: '#FFF',
        800: '#FFF',
        900: '#FFF',
      },
    }),
    width: theme => ({
      auto: 'auto',
      ...theme('spacing'),
      '1/2': '50%',
      '1/3': '33.333333%',
      '2/3': '66.666667%',
      '1/4': '25%',
      '2/4': '50%',
      '3/4': '75%',
      '1/5': '20%',
      '2/5': '40%',
      '3/5': '60%',
      '4/5': '80%',
      '1/6': '16.666667%',
      '2/6': '33.333333%',
      '3/6': '50%',
      '4/6': '66.666667%',
      '5/6': '83.333333%',
      '1/12': '8.333333%',
      '2/12': '16.666667%',
      '3/12': '25%',
      '4/12': '33.333333%',
      '5/12': '41.666667%',
      '6/12': '50%',
      '7/12': '58.333333%',
      '8/12': '66.666667%',
      '9/12': '75%',
      '10/12': '83.333333%',
      '11/12': '91.666667%',
      full: '100%',
      screen: '100vw',
    }),
    zIndex: {
      auto: 'auto',
      '0': '0',
      '10': '10',
      '20': '20',
      '30': '30',
      '40': '40',
      '50': '50',
    },
  },
  variants: {
    accessibility: ['responsive', 'focus'],
    alignContent: ['responsive'],
    alignItems: ['responsive'],
    alignSelf: ['responsive'],
    appearance: ['responsive'],
    backgroundAttachment: ['responsive'],
    backgroundColor: ['responsive', 'hover', 'focus'],
    backgroundPosition: ['responsive'],
    backgroundRepeat: ['responsive'],
    backgroundSize: ['responsive'],
    borderCollapse: ['responsive'],
    borderColor: ['responsive', 'hover', 'focus'],
    borderRadius: ['responsive'],
    borderStyle: ['responsive'],
    borderWidth: ['responsive', 'ltr', 'rtl'],
    boxShadow: ['responsive', 'hover', 'focus'],
    cursor: ['responsive'],
    display: ['responsive'],
    fill: ['responsive'],
    flex: ['responsive'],
    flexDirection: ['responsive'],
    flexGrow: ['responsive'],
    flexShrink: ['responsive'],
    flexWrap: ['responsive'],
    float: ['responsive'],
    fontFamily: ['responsive'],
    fontSize: ['responsive'],
    fontSmoothing: ['responsive'],
    fontStyle: ['responsive'],
    fontWeight: ['responsive', 'hover', 'focus'],
    height: ['responsive'],
    inset: ['responsive', 'ltr', 'rtl'],
    justifyContent: ['responsive'],
    letterSpacing: ['responsive'],
    lineHeight: ['responsive'],
    listStylePosition: ['responsive'],
    listStyleType: ['responsive'],
    margin: ['responsive', 'ltr', 'rtl'],
    maxHeight: ['responsive'],
    maxWidth: ['responsive'],
    minHeight: ['responsive'],
    minWidth: ['responsive'],
    objectFit: ['responsive'],
    objectPosition: ['responsive'],
    opacity: ['responsive', 'hover', 'focus'],
    order: ['responsive'],
    outline: ['responsive', 'focus'],
    overflow: ['responsive'],
    padding: ['responsive', 'ltr', 'rtl'],
    placeholderColor: ['responsive', 'focus'],
    pointerEvents: ['responsive'],
    position: ['responsive'],
    resize: ['responsive'],
    stroke: ['responsive'],
    tableLayout: ['responsive'],
    textAlign: ['responsive'],
    textColor: ['responsive', 'hover', 'focus'],
    textDecoration: ['responsive', 'hover', 'focus'],
    textTransform: ['responsive'],
    userSelect: ['responsive'],
    verticalAlign: ['responsive'],
    visibility: ['responsive'],
    whitespace: ['responsive'],
    width: ['responsive'],
    wordBreak: ['responsive'],
    zIndex: ['responsive'],
  },
  corePlugins: {},
  plugins: [
    function ({addVariant, e}) {
      addVariant('ltr', ({separator, modifySelectors}) => {
        modifySelectors(({className}) => {
          return `[dir=ltr] .ltr${e(separator)}${className}`;
        })
      });

      addVariant('rtl', ({separator, modifySelectors}) => {
        modifySelectors(({className}) => {
          return `[dir=rtl] .rtl${e(separator)}${className}`;
        })
      });
    }
  ],
};


/***/ }),

/***/ "0tFB":
/*!**********************************************************!*\
  !*** ./src/@vex/components/search/search.component.scss ***!
  \**********************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (".search {\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  justify-content: center;\n  text-align: center;\n  position: fixed;\n  top: 0;\n  left: 0;\n  width: 100%;\n  opacity: 0;\n  height: 50vh;\n  pointer-events: none;\n  transform: scale(0.75);\n  transition: all 0.25s cubic-bezier(0.2, 1, 0.3, 1);\n  z-index: 1050;\n}\n\n.search.show {\n  opacity: 1;\n  pointer-events: auto;\n  transform: scale(1);\n  transition: all 0.5s cubic-bezier(0.2, 1, 0.3, 1);\n}\n\n.search-input {\n  border-bottom: 1px solid var(--foreground-divider);\n  font-size: 7vw;\n  line-height: 3rem;\n  width: 75%;\n  margin: 0;\n  border-radius: 0;\n  border-right-width: 0;\n  border-left-width: 0;\n  border-top-width: 0;\n  font-weight: 700;\n  background-color: transparent;\n}\n\n.search-input:focus {\n  outline: none;\n}\n\n.search-hint {\n  width: 75%;\n  font-size: 1rem;\n  text-align: right;\n  padding-top: 1rem;\n  padding-bottom: 1rem;\n  margin-left: auto;\n  margin-right: auto;\n  color: var(--text-hint);\n  font-weight: 700;\n}\n\n.search-overlay {\n  position: fixed;\n  width: 100%;\n  bottom: 0;\n  left: 0;\n  opacity: 0;\n  height: 50vh;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uL3NlYXJjaC5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLGFBQUE7RUFDQSxzQkFBQTtFQUNBLG1CQUFBO0VBQ0EsdUJBQUE7RUFDQSxrQkFBQTtFQUNBLGVBQUE7RUFDQSxNQUFBO0VBQ0EsT0FBQTtFQUNBLFdBQUE7RUFDQSxVQUFBO0VBQ0EsWUFBQTtFQUNBLG9CQUFBO0VBQ0Esc0JBQUE7RUFDQSxrREFBQTtFQUNBLGFBQUE7QUFDRjs7QUFFQTtFQUNFLFVBQUE7RUFDQSxvQkFBQTtFQUNBLG1CQUFBO0VBQ0EsaURBQUE7QUFDRjs7QUFFQTtFQUNFLGtEQUFBO0VBQ0EsY0FBQTtFQUNBLGlCQUFBO0VBQ0EsVUFBQTtFQUNBLFNBQUE7RUFDQSxnQkFBQTtFQUNBLHFCQUFBO0VBQ0Esb0JBQUE7RUFDQSxtQkFBQTtFQUNBLGdCQUFBO0VBQ0EsNkJBQUE7QUFDRjs7QUFFQTtFQUNFLGFBQUE7QUFDRjs7QUFFQTtFQUNFLFVBQUE7RUFDQSxlQUFBO0VBQ0EsaUJBQUE7RUFDQSxpQkFBQTtFQUNBLG9CQUFBO0VBQ0EsaUJBQUE7RUFDQSxrQkFBQTtFQUNBLHVCQUFBO0VBQ0EsZ0JBQUE7QUFDRjs7QUFFQTtFQUNFLGVBQUE7RUFDQSxXQUFBO0VBQ0EsU0FBQTtFQUNBLE9BQUE7RUFDQSxVQUFBO0VBQ0EsWUFBQTtBQUNGIiwiZmlsZSI6InNlYXJjaC5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbIi5zZWFyY2gge1xuICBkaXNwbGF5OiBmbGV4O1xuICBmbGV4LWRpcmVjdGlvbjogY29sdW1uO1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xuICBqdXN0aWZ5LWNvbnRlbnQ6IGNlbnRlcjtcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xuICBwb3NpdGlvbjogZml4ZWQ7XG4gIHRvcDogMDtcbiAgbGVmdDogMDtcbiAgd2lkdGg6IDEwMCU7XG4gIG9wYWNpdHk6IDA7XG4gIGhlaWdodDogNTB2aDtcbiAgcG9pbnRlci1ldmVudHM6IG5vbmU7XG4gIHRyYW5zZm9ybTogc2NhbGUoMC43NSk7XG4gIHRyYW5zaXRpb246IGFsbCAwLjI1cyBjdWJpYy1iZXppZXIoMC4yLCAxLCAwLjMsIDEpO1xuICB6LWluZGV4OiAxMDUwO1xufVxuXG4uc2VhcmNoLnNob3cge1xuICBvcGFjaXR5OiAxO1xuICBwb2ludGVyLWV2ZW50czogYXV0bztcbiAgdHJhbnNmb3JtOiBzY2FsZSgxKTtcbiAgdHJhbnNpdGlvbjogYWxsIDAuNXMgY3ViaWMtYmV6aWVyKDAuMiwgMSwgMC4zLCAxKTtcbn1cblxuLnNlYXJjaC1pbnB1dCB7XG4gIGJvcmRlci1ib3R0b206IDFweCBzb2xpZCB2YXIoLS1mb3JlZ3JvdW5kLWRpdmlkZXIpO1xuICBmb250LXNpemU6IDd2dztcbiAgbGluZS1oZWlnaHQ6IDNyZW07XG4gIHdpZHRoOiA3NSU7XG4gIG1hcmdpbjogMDtcbiAgYm9yZGVyLXJhZGl1czogMDtcbiAgYm9yZGVyLXJpZ2h0LXdpZHRoOiAwO1xuICBib3JkZXItbGVmdC13aWR0aDogMDtcbiAgYm9yZGVyLXRvcC13aWR0aDogMDtcbiAgZm9udC13ZWlnaHQ6IDcwMDtcbiAgYmFja2dyb3VuZC1jb2xvcjogdHJhbnNwYXJlbnQ7XG59XG5cbi5zZWFyY2gtaW5wdXQ6Zm9jdXMge1xuICBvdXRsaW5lOiBub25lO1xufVxuXG4uc2VhcmNoLWhpbnQge1xuICB3aWR0aDogNzUlO1xuICBmb250LXNpemU6IDFyZW07XG4gIHRleHQtYWxpZ246IHJpZ2h0O1xuICBwYWRkaW5nLXRvcDogMXJlbTtcbiAgcGFkZGluZy1ib3R0b206IDFyZW07XG4gIG1hcmdpbi1sZWZ0OiBhdXRvO1xuICBtYXJnaW4tcmlnaHQ6IGF1dG87XG4gIGNvbG9yOiB2YXIoLS10ZXh0LWhpbnQpO1xuICBmb250LXdlaWdodDogNzAwO1xufVxuXG4uc2VhcmNoLW92ZXJsYXkge1xuICBwb3NpdGlvbjogZml4ZWQ7XG4gIHdpZHRoOiAxMDAlO1xuICBib3R0b206IDA7XG4gIGxlZnQ6IDA7XG4gIG9wYWNpdHk6IDA7XG4gIGhlaWdodDogNTB2aDtcbn0iXX0= */");

/***/ }),

/***/ "0vMP":
/*!*************************************************!*\
  !*** ./src/@vex/services/navigation.service.ts ***!
  \*************************************************/
/*! exports provided: NavigationService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "NavigationService", function() { return NavigationService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "qCKp");



let NavigationService = class NavigationService {
    constructor() {
        this.subject = new rxjs__WEBPACK_IMPORTED_MODULE_2__["BehaviorSubject"](null);
        this.items$ = this.subject.asObservable();
        this.items = [];
        this._openChangeSubject = new rxjs__WEBPACK_IMPORTED_MODULE_2__["Subject"]();
        this.openChange$ = this._openChangeSubject.asObservable();
    }
    triggerOpenChange(item) {
        this._openChangeSubject.next(item);
    }
    isLink(item) {
        return item.type === 'link';
    }
    isDropdown(item) {
        return item.type === 'dropdown';
    }
    isSubheading(item) {
        return item.type === 'subheading';
    }
    setItems(items) {
        this.items = items;
        this.subject.next(items);
    }
};
NavigationService.ctorParameters = () => [];
NavigationService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], NavigationService);



/***/ }),

/***/ "1Fbs":
/*!******************************************************************!*\
  !*** ./src/app/layout/components/toolbar/toolbar.component.scss ***!
  \******************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (":host {\n  background: var(--toolbar-background);\n  box-sizing: border-box;\n  color: var(--toolbar-color);\n  display: block;\n  white-space: nowrap;\n  width: 100%;\n  z-index: var(--toolbar-z-index);\n}\n\n.toolbar {\n  height: var(--toolbar-height);\n}\n\n.mat-icon {\n  color: var(--toolbar-icon-color);\n}\n\na {\n  color: var(--toolbar-color);\n  text-decoration: none;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uL3Rvb2xiYXIuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSxxQ0FBQTtFQUNBLHNCQUFBO0VBQ0EsMkJBQUE7RUFDQSxjQUFBO0VBQ0EsbUJBQUE7RUFDQSxXQUFBO0VBQ0EsK0JBQUE7QUFDRjs7QUFFQTtFQUNFLDZCQUFBO0FBQ0Y7O0FBRUE7RUFDRSxnQ0FBQTtBQUNGOztBQUVBO0VBQ0UsMkJBQUE7RUFDQSxxQkFBQTtBQUNGIiwiZmlsZSI6InRvb2xiYXIuY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyI6aG9zdCB7XG4gIGJhY2tncm91bmQ6IHZhcigtLXRvb2xiYXItYmFja2dyb3VuZCk7XG4gIGJveC1zaXppbmc6IGJvcmRlci1ib3g7XG4gIGNvbG9yOiB2YXIoLS10b29sYmFyLWNvbG9yKTtcbiAgZGlzcGxheTogYmxvY2s7XG4gIHdoaXRlLXNwYWNlOiBub3dyYXA7XG4gIHdpZHRoOiAxMDAlO1xuICB6LWluZGV4OiB2YXIoLS10b29sYmFyLXotaW5kZXgpO1xufVxuXG4udG9vbGJhciB7XG4gIGhlaWdodDogdmFyKC0tdG9vbGJhci1oZWlnaHQpO1xufVxuXG4ubWF0LWljb24ge1xuICBjb2xvcjogdmFyKC0tdG9vbGJhci1pY29uLWNvbG9yKTtcbn1cblxuYSB7XG4gIGNvbG9yOiB2YXIoLS10b29sYmFyLWNvbG9yKTtcbiAgdGV4dC1kZWNvcmF0aW9uOiBub25lO1xufSJdfQ== */");

/***/ }),

/***/ "1vXY":
/*!********************************************************************!*\
  !*** ./src/@vex/components/config-panel/config-panel.component.ts ***!
  \********************************************************************/
/*! exports provided: ConfigPanelComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ConfigPanelComponent", function() { return ConfigPanelComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_config_panel_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./config-panel.component.html */ "fQJz");
/* harmony import */ var _config_panel_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./config-panel.component.scss */ "dO6N");
/* harmony import */ var _angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/cdk/coercion */ "8LU1");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _iconify_icons_ic_twotone_check__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @iconify/icons-ic/twotone-check */ "+tDV");
/* harmony import */ var _iconify_icons_ic_twotone_check__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_check__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _iconify_icons_ic_twotone_settings__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @iconify/icons-ic/twotone-settings */ "hF2C");
/* harmony import */ var _iconify_icons_ic_twotone_settings__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_settings__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! rxjs/operators */ "kU1M");
/* harmony import */ var _interfaces_config_name_model__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../interfaces/config-name.model */ "EuI8");
/* harmony import */ var _services_config_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../services/config.service */ "lC2v");
/* harmony import */ var _services_layout_service__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../services/layout.service */ "CtTw");
/* harmony import */ var _services_style_service__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../../services/style.service */ "Z+W5");













let ConfigPanelComponent = class ConfigPanelComponent {
    constructor(configService, styleService, layoutService, route) {
        this.configService = configService;
        this.styleService = styleService;
        this.layoutService = layoutService;
        this.route = route;
        this.configs = this.configService.configs;
        this.config$ = this.configService.config$;
        this.activeConfig$ = this.configService.config$.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_8__["map"])(config => Object.keys(this.configService.configs).find(key => this.configService.configs[key] === config)));
        this.isRTL$ = this.route.queryParamMap.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_8__["map"])(paramMap => Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_3__["coerceBooleanProperty"])(paramMap.get('rtl'))), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_8__["first"])());
        this.icSettings = _iconify_icons_ic_twotone_settings__WEBPACK_IMPORTED_MODULE_7___default.a;
        this.icCheck = _iconify_icons_ic_twotone_check__WEBPACK_IMPORTED_MODULE_6___default.a;
        this.ConfigName = _interfaces_config_name_model__WEBPACK_IMPORTED_MODULE_9__["ConfigName"];
        this.Style = _services_style_service__WEBPACK_IMPORTED_MODULE_12__["Style"];
    }
    ngOnInit() {
    }
    setConfig(layout, style) {
        this.configService.setConfig(layout);
        this.styleService.setStyle(style);
    }
    sidenavOpenChange(change) {
        change.checked ? this.layoutService.openSidenav() : this.layoutService.closeSidenav();
    }
    layoutRTLChange(change) {
        change.checked ? this.layoutService.enableRTL() : this.layoutService.disableRTL();
    }
    toolbarPositionChange(change) {
        this.configService.updateConfig({
            toolbar: {
                fixed: change.value === 'fixed'
            }
        });
    }
    footerVisibleChange(change) {
        this.configService.updateConfig({
            footer: {
                visible: change.checked
            }
        });
    }
    footerPositionChange(change) {
        this.configService.updateConfig({
            footer: {
                fixed: change.value === 'fixed'
            }
        });
    }
};
ConfigPanelComponent.ctorParameters = () => [
    { type: _services_config_service__WEBPACK_IMPORTED_MODULE_10__["ConfigService"] },
    { type: _services_style_service__WEBPACK_IMPORTED_MODULE_12__["StyleService"] },
    { type: _services_layout_service__WEBPACK_IMPORTED_MODULE_11__["LayoutService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_5__["ActivatedRoute"] }
];
ConfigPanelComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_4__["Component"])({
        selector: 'vex-config-panel',
        template: _raw_loader_config_panel_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_config_panel_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], ConfigPanelComponent);



/***/ }),

/***/ "2RYP":
/*!****************************************!*\
  !*** ./src/app/data/schema/project.ts ***!
  \****************************************/
/*! exports provided: Project */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Project", function() { return Project; });
class Project {
    constructor(project) {
        this.id = project.id;
        this.name = project.name;
        this.description = project.description;
        this.createdAt = new Date(project.created_at);
        this.updatedAt = new Date(project.updated_at);
        this.starred = project.starred;
        this.key = project.key;
        this.organizationId = project.organization_id;
        this.mockUrl = project.mock_url;
    }
}


/***/ }),

/***/ "2USq":
/*!*************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/layout/components/toolbar/components/toolbar-user/toolbar-user.component.html ***!
  \*************************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div #originRef\n     (click)=\"showPopover(originRef)\"\n     [class.bg-hover]=\"dropdownOpen\"\n     class=\"flex items-center rounded cursor-pointer relative trans-ease-out select-none py-1 pr-1 pl-3 hover:bg-hover\"\n     matRipple>\n  <div class=\"body-1 font-medium leading-snug ltr:mr-3 rtl:ml-3\" fxHide.xs *ngIf=\"user$ | async as user\">\n    {{ user.name }}\n  </div>\n  <div [style.background-color]=\"theme.colors.primary['500'] | colorFade:0.9\"\n       [style.color]=\"theme.colors.primary['500']\"\n       class=\"rounded-full h-9 w-9 flex items-center justify-center\">\n    <mat-icon [icIcon]=\"icPerson\"></mat-icon>\n  </div>\n</div>\n");

/***/ }),

/***/ "2bXN":
/*!**************************************************!*\
  !*** ./src/app/data/schema/request-component.ts ***!
  \**************************************************/
/*! exports provided: RequestComponent, RequestComponentType */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RequestComponent", function() { return RequestComponent; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RequestComponentType", function() { return RequestComponentType; });
class RequestComponent {
    constructor(type, id, alias) {
        this.type = type;
        this.id = id;
        this.alias = alias;
        if (alias) {
            this.aliasName = alias.name;
        }
    }
}
var RequestComponentType;
(function (RequestComponentType) {
    RequestComponentType[RequestComponentType["Header"] = 1] = "Header";
    RequestComponentType[RequestComponentType["PathSegment"] = 2] = "PathSegment";
    RequestComponentType[RequestComponentType["QueryParam"] = 3] = "QueryParam";
    RequestComponentType[RequestComponentType["BodyParam"] = 4] = "BodyParam";
    RequestComponentType[RequestComponentType["Response"] = 5] = "Response";
    RequestComponentType[RequestComponentType["ResponseHeader"] = 6] = "ResponseHeader";
})(RequestComponentType || (RequestComponentType = {}));


/***/ }),

/***/ "2e3Z":
/*!**************************************************!*\
  !*** ./src/@vex/animations/popover.animation.ts ***!
  \**************************************************/
/*! exports provided: popoverAnimation */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "popoverAnimation", function() { return popoverAnimation; });
/* harmony import */ var _angular_animations__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/animations */ "GS7A");

const popoverAnimation = Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["trigger"])('transformPopover', [
    Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["transition"])(':enter', [
        Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["style"])({
            opacity: 0,
            transform: 'scale(0.6)'
        }),
        Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["group"])([
            Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["animate"])('100ms linear', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["style"])({
                opacity: 1
            })),
            Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["animate"])('150ms cubic-bezier(0, 0, 0.2, 1)', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["style"])({
                transform: 'scale(1)'
            }))
        ])
    ]),
    Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["transition"])(':leave', [
        Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["style"])({
            opacity: 1
        }),
        Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["animate"])('100ms linear', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["style"])({
            opacity: 0
        }))
    ])
]);


/***/ }),

/***/ "3Ncz":
/*!********************************************************!*\
  !*** ./src/app/core/http/scenario-resource.service.ts ***!
  \********************************************************/
/*! exports provided: ScenarioResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ScenarioResource", function() { return ScenarioResource; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _rest_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rest-api.service */ "iCaw");



let ScenarioResource = class ScenarioResource {
    constructor(restApi) {
        this.restApi = restApi;
        this.ENDPOINT = 'scenarios';
    }
    index(queryParams) {
        return this.restApi.index([this.ENDPOINT], queryParams);
    }
    show(id, queryParams) {
        return this.restApi.show([this.ENDPOINT, id], queryParams);
    }
    create(body) {
        return this.restApi.create([this.ENDPOINT], body);
    }
    update(id, body) {
        return this.restApi.update([this.ENDPOINT, id], body);
    }
    destroy(id) {
        return this.restApi.destroy([this.ENDPOINT, id]);
    }
    download(id) {
        return this.restApi.show([this.ENDPOINT, id, 'download']);
    }
};
ScenarioResource.ctorParameters = () => [
    { type: _rest_api_service__WEBPACK_IMPORTED_MODULE_2__["RestApiService"] }
];
ScenarioResource = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], ScenarioResource);



/***/ }),

/***/ "3TZW":
/*!****************************************************!*\
  !*** ./src/@vex/utils/check-router-childs-data.ts ***!
  \****************************************************/
/*! exports provided: checkRouterChildsData */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "checkRouterChildsData", function() { return checkRouterChildsData; });
function checkRouterChildsData(route, compareWith) {
    if (compareWith(route.data)) {
        return true;
    }
    if (!route.firstChild) {
        return false;
    }
    return checkRouterChildsData(route.firstChild, compareWith);
}


/***/ }),

/***/ "3aTg":
/*!*****************************************************************!*\
  !*** ./src/app/core/http/response-resolver-resource.service.ts ***!
  \*****************************************************************/
/*! exports provided: ResponseResolverResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ResponseResolverResource", function() { return ResponseResolverResource; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _rest_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rest-api.service */ "iCaw");



let ResponseResolverResource = class ResponseResolverResource {
    constructor(restApi) {
        this.restApi = restApi;
        this.ENDPOINT_ENDPOINT = 'endpoints';
        this.ENDPOINT = 'response_resolvers';
    }
    index(endpointId, queryParams) {
        return this.restApi.index([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT], queryParams);
    }
    show(endpointId, id, queryParams) {
        return this.restApi.show([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT, id], queryParams);
    }
    create(endpointId, body) {
        return this.restApi.create([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT], body);
    }
    update(endpointId, id, body) {
        return this.restApi.update([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT, id], body);
    }
    destroy(endpointId, id) {
        return this.restApi.destroy([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT, id]);
    }
};
ResponseResolverResource.ctorParameters = () => [
    { type: _rest_api_service__WEBPACK_IMPORTED_MODULE_2__["RestApiService"] }
];
ResponseResolverResource = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], ResponseResolverResource);



/***/ }),

/***/ "3oZ8":
/*!**************************************!*\
  !*** ./src/@vex/services/configs.ts ***!
  \**************************************/
/*! exports provided: configs */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "configs", function() { return configs; });
/* harmony import */ var _interfaces_config_name_model__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../interfaces/config-name.model */ "EuI8");
/* harmony import */ var _utils_merge_deep__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../utils/merge-deep */ "Sl3+");


const defaultConfig = {
    id: _interfaces_config_name_model__WEBPACK_IMPORTED_MODULE_0__["ConfigName"].apollo,
    name: 'Apollo',
    imgSrc: '//vex-landing.visurel.com/assets/img/layouts/apollo.png',
    layout: 'horizontal',
    boxed: false,
    sidenav: {
        title: 'Stoobly',
        imageUrl: 'assets/img/demo/logo.svg',
        showCollapsePin: true,
        state: 'expanded'
    },
    toolbar: {
        fixed: true
    },
    navbar: {
        position: 'below-toolbar'
    },
    footer: {
        visible: true,
        fixed: true
    }
};
const configs = [
    defaultConfig,
    Object(_utils_merge_deep__WEBPACK_IMPORTED_MODULE_1__["mergeDeep"])(Object.assign({}, defaultConfig), {
        id: _interfaces_config_name_model__WEBPACK_IMPORTED_MODULE_0__["ConfigName"].hermes,
        name: 'Hermes',
        imgSrc: '//vex-landing.visurel.com/assets/img/layouts/hermes.png',
        layout: 'vertical',
        boxed: true,
        toolbar: {
            fixed: false
        },
        footer: {
            fixed: false
        }
    }),
    Object(_utils_merge_deep__WEBPACK_IMPORTED_MODULE_1__["mergeDeep"])(Object.assign({}, defaultConfig), {
        id: _interfaces_config_name_model__WEBPACK_IMPORTED_MODULE_0__["ConfigName"].ares,
        name: 'Ares',
        imgSrc: '//vex-landing.visurel.com/assets/img/layouts/ares.png',
        toolbar: {
            fixed: false
        },
        navbar: {
            position: 'in-toolbar'
        },
        footer: {
            fixed: false
        }
    }),
    Object(_utils_merge_deep__WEBPACK_IMPORTED_MODULE_1__["mergeDeep"])(Object.assign({}, defaultConfig), {
        id: _interfaces_config_name_model__WEBPACK_IMPORTED_MODULE_0__["ConfigName"].zeus,
        name: 'Zeus',
        imgSrc: '//vex-landing.visurel.com/assets/img/layouts/zeus.png',
        sidenav: {
            state: 'collapsed'
        },
        footer: {
            fixed: false,
            visible: false,
        }
    }),
    Object(_utils_merge_deep__WEBPACK_IMPORTED_MODULE_1__["mergeDeep"])(Object.assign({}, defaultConfig), {
        id: _interfaces_config_name_model__WEBPACK_IMPORTED_MODULE_0__["ConfigName"].ikaros,
        name: 'Ikaros',
        imgSrc: '//vex-landing.visurel.com/assets/img/layouts/ikaros.png',
        layout: 'vertical',
        boxed: true,
        toolbar: {
            fixed: false
        },
        navbar: {
            position: 'in-toolbar'
        },
        footer: {
            fixed: false,
            visible: false,
        }
    })
];


/***/ }),

/***/ "3v0u":
/*!*****************************************************************************************************************************************!*\
  !*** ./src/app/layout/components/toolbar/components/toolbar-user/toolbar-user-dropdown/services/toolbar-user-dropdown-icons.service.ts ***!
  \*****************************************************************************************************************************************/
/*! exports provided: ToolbarUserDropdownIcons */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ToolbarUserDropdownIcons", function() { return ToolbarUserDropdownIcons; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _iconify_icons_ic_twotone_access_time__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @iconify/icons-ic/twotone-access-time */ "NBim");
/* harmony import */ var _iconify_icons_ic_twotone_access_time__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_access_time__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _iconify_icons_ic_twotone_account_circle__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @iconify/icons-ic/twotone-account-circle */ "6qmq");
/* harmony import */ var _iconify_icons_ic_twotone_account_circle__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_account_circle__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _iconify_icons_ic_twotone_arrow_drop_down__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @iconify/icons-ic/twotone-arrow-drop-down */ "LgSP");
/* harmony import */ var _iconify_icons_ic_twotone_arrow_drop_down__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_arrow_drop_down__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _iconify_icons_ic_twotone_business__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @iconify/icons-ic/twotone-business */ "6uZp");
/* harmony import */ var _iconify_icons_ic_twotone_business__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_business__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _iconify_icons_ic_twotone_check_circle__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @iconify/icons-ic/twotone-check-circle */ "Z5gU");
/* harmony import */ var _iconify_icons_ic_twotone_check_circle__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_check_circle__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _iconify_icons_ic_twotone_chevron_right__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @iconify/icons-ic/twotone-chevron-right */ "uAX/");
/* harmony import */ var _iconify_icons_ic_twotone_chevron_right__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_chevron_right__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _iconify_icons_ic_twotone_do_not_disturb__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @iconify/icons-ic/twotone-do-not-disturb */ "8acV");
/* harmony import */ var _iconify_icons_ic_twotone_do_not_disturb__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_do_not_disturb__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _iconify_icons_ic_twotone_list_alt__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @iconify/icons-ic/twotone-list-alt */ "a5nG");
/* harmony import */ var _iconify_icons_ic_twotone_list_alt__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_list_alt__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _iconify_icons_ic_twotone_lock__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @iconify/icons-ic/twotone-lock */ "QR5W");
/* harmony import */ var _iconify_icons_ic_twotone_lock__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_lock__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _iconify_icons_ic_twotone_notifications_off__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @iconify/icons-ic/twotone-notifications-off */ "nu12");
/* harmony import */ var _iconify_icons_ic_twotone_notifications_off__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_notifications_off__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var _iconify_icons_ic_twotone_offline_bolt__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @iconify/icons-ic/twotone-offline-bolt */ "blfN");
/* harmony import */ var _iconify_icons_ic_twotone_offline_bolt__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_offline_bolt__WEBPACK_IMPORTED_MODULE_12__);
/* harmony import */ var _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @iconify/icons-ic/twotone-person */ "KaaH");
/* harmony import */ var _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_13___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_13__);
/* harmony import */ var _iconify_icons_ic_twotone_settings__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @iconify/icons-ic/twotone-settings */ "hF2C");
/* harmony import */ var _iconify_icons_ic_twotone_settings__WEBPACK_IMPORTED_MODULE_14___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_settings__WEBPACK_IMPORTED_MODULE_14__);
/* harmony import */ var _iconify_icons_ic_twotone_table_chart__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @iconify/icons-ic/twotone-table-chart */ "qrwc");
/* harmony import */ var _iconify_icons_ic_twotone_table_chart__WEBPACK_IMPORTED_MODULE_15___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_table_chart__WEBPACK_IMPORTED_MODULE_15__);
/* harmony import */ var _iconify_icons_ic_twotone_verified_user__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @iconify/icons-ic/twotone-verified-user */ "Xarb");
/* harmony import */ var _iconify_icons_ic_twotone_verified_user__WEBPACK_IMPORTED_MODULE_16___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_verified_user__WEBPACK_IMPORTED_MODULE_16__);

















let ToolbarUserDropdownIcons = class ToolbarUserDropdownIcons {
    constructor() {
        this.icListAlt = _iconify_icons_ic_twotone_list_alt__WEBPACK_IMPORTED_MODULE_9___default.a;
        this.icTableChart = _iconify_icons_ic_twotone_table_chart__WEBPACK_IMPORTED_MODULE_15___default.a;
        this.icAccountCircle = _iconify_icons_ic_twotone_account_circle__WEBPACK_IMPORTED_MODULE_3___default.a;
        this.icPerson = _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_13___default.a;
        this.icSettings = _iconify_icons_ic_twotone_settings__WEBPACK_IMPORTED_MODULE_14___default.a;
        this.icChevronRight = _iconify_icons_ic_twotone_chevron_right__WEBPACK_IMPORTED_MODULE_7___default.a;
        this.icArrowDropDown = _iconify_icons_ic_twotone_arrow_drop_down__WEBPACK_IMPORTED_MODULE_4___default.a;
        this.icBusiness = _iconify_icons_ic_twotone_business__WEBPACK_IMPORTED_MODULE_5___default.a;
        this.icVerifiedUser = _iconify_icons_ic_twotone_verified_user__WEBPACK_IMPORTED_MODULE_16___default.a;
        this.icLock = _iconify_icons_ic_twotone_lock__WEBPACK_IMPORTED_MODULE_10___default.a;
        this.icNotificationsOff = _iconify_icons_ic_twotone_notifications_off__WEBPACK_IMPORTED_MODULE_11___default.a;
        this.icCheckCircle = _iconify_icons_ic_twotone_check_circle__WEBPACK_IMPORTED_MODULE_6___default.a;
        this.icAccessTime = _iconify_icons_ic_twotone_access_time__WEBPACK_IMPORTED_MODULE_2___default.a;
        this.icDoNotDisturb = _iconify_icons_ic_twotone_do_not_disturb__WEBPACK_IMPORTED_MODULE_8___default.a;
        this.icOfflineBolt = _iconify_icons_ic_twotone_offline_bolt__WEBPACK_IMPORTED_MODULE_12___default.a;
    }
};
ToolbarUserDropdownIcons.ctorParameters = () => [];
ToolbarUserDropdownIcons = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], ToolbarUserDropdownIcons);



/***/ }),

/***/ "4/Wj":
/*!*******************************************************!*\
  !*** ./src/app/core/http/request-resource.service.ts ***!
  \*******************************************************/
/*! exports provided: RequestResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RequestResource", function() { return RequestResource; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _rest_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rest-api.service */ "iCaw");



let RequestResource = class RequestResource {
    constructor(restApi) {
        this.restApi = restApi;
        this.ENDPOINT = 'requests';
    }
    index(queryParams) {
        return this.restApi.index([this.ENDPOINT], queryParams);
    }
    show(id, queryParams) {
        return this.restApi.show([this.ENDPOINT, id], queryParams);
    }
    create(body) {
        return this.restApi.create([this.ENDPOINT], body);
    }
    update(id, body) {
        return this.restApi.update([this.ENDPOINT, id], body);
    }
    destroy(id) {
        return this.restApi.destroy([this.ENDPOINT, id]);
    }
    removeEndpoint(id) {
        return this.restApi.destroy([this.ENDPOINT, id, 'endpoint']);
    }
    download(id) {
        return this.restApi.show([this.ENDPOINT, id, 'download']);
    }
};
RequestResource.ctorParameters = () => [
    { type: _rest_api_service__WEBPACK_IMPORTED_MODULE_2__["RestApiService"] }
];
RequestResource = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], RequestResource);



/***/ }),

/***/ "46RW":
/*!*********************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/layout/components/toolbar/components/toolbar-proxy-settings/components/toolbar-record-settings/toolbar-record-settings.component.html ***!
  \*********************************************************************************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<form (ngSubmit)=\"update()\" [formGroup]=\"form\">\n  <div fxLayout=\"row\" fxLayoutAlign=\"start center\" mat-dialog-title>\n    <h2 class=\"headline m-0\" fxFlex=\"auto\">Record Settings</h2>\n\n    <button class=\"subheading\" mat-dialog-close mat-icon-button type=\"button\">\n      <mat-icon [icIcon]=\"icClose\"></mat-icon>\n    </button>\n  </div>\n\n  <mat-divider class=\"-mx-6 text-border\"></mat-divider>\n\n  <mat-tab-group>\n    <mat-tab label=\"General\">\n      <div class=\"mb-3\" fxLayout=\"column\" fxLayoutAlign=\"start start\">\n        <h4 class=\"mt-4 mb-2 subheading\" fxFlex=\"100\">\n          Save Requests To\n        </h4>\n\n        <mat-form-field fxFlex=\"fill\" class=\"w-full\">\n          <mat-label>Project</mat-label>\n          <mat-select \n            (selectionChange)=\"selectProject($event)\"\n            formControlName=\"project\"\n          >\n            <mat-option \n              *ngFor=\"let project of (projects$ | async)\"\n              [value]=\"project\"\n            >\n              {{ project.name }}\n            </mat-option>\n          </mat-select>\n        </mat-form-field>\n\n        <div \n          class=\"w-full\" fxLayout=\"row\" fxLayoutGap=\"10px\"\n        >\n          <mat-form-field fxFlex=\"fill\" class=\"w-full\">\n            <mat-label>Scenario</mat-label>\n            <mat-select formControlName=\"scenario\">\n              <mat-option \n                *ngFor=\"let scenario of scenarios\"\n                [value]=\"scenario\"\n              >\n                {{ scenario.name }}\n              </mat-option>\n            </mat-select>\n\n            <mat-hint>If left blank, defaults to project</mat-hint>\n          </mat-form-field>\n\n          <button \n            *ngIf=\"form.value.scenario\" \n            (click)=\"clearScenario()\"\n            fxFlex=\"40px\" class=\"input-button\" mat-icon-button matSuffix type=\"button\">\n            <div fxLayout=\"row\" fxLayoutAlign=\"center center\">\n              <mat-icon [icIcon]=\"icClose\"></mat-icon>\n            </div>\n          </button>\n        </div>\n      </div>\n    </mat-tab>\n\n    <mat-tab label=\"Policy\">\n      <div class=\"mb-3\" fxLayout=\"column\" fxLayoutAlign=\"start start\">\n        <h4 class=\"mt-4 mb-2 subheading\" fxFlex=\"100\">\n          Record Which Requests\n        </h4>\n\n        <mat-form-field class=\"w-full\">\n          <mat-label>Policy</mat-label>\n          <mat-select formControlName=\"recordPolicy\">\n            <mat-option \n              *ngFor=\"let policy of policies\"\n              [value]=\"policy\"\n            >\n              {{ policy }}\n            </mat-option>\n          </mat-select>\n        </mat-form-field>\n\n        <h4 class=\"mt-0 mb-2 subheading\" fxFlex=\"100\">\n          Reverse Proxy Requests To\n        </h4>\n\n        <div class=\"w-full\" fxLayout=\"row\" fxLayoutGap=\"10px\">\n          <mat-form-field class=\"mb-4 w-full\">\n            <mat-label>Service URL</mat-label>\n            <input matInput formControlName=\"serviceUrl\" type=\"text\">\n            <mat-hint>If left blank, defaults to forward proxy</mat-hint>\n          </mat-form-field>\n\n          <button \n            *ngIf=\"form.value.serviceUrl\" \n            (click)=\"clearServiceUrl()\"\n            fxFlex=\"40px\" class=\"input-button\" mat-icon-button matSuffix type=\"button\">\n            <div fxLayout=\"row\" fxLayoutAlign=\"center center\">\n              <mat-icon [icIcon]=\"icClose\"></mat-icon>\n            </div>\n          </button>\n        </div>\n      </div>\n    </mat-tab>\n\n    <mat-tab label=\"Include\">\n      <div class=\"mb-3\" fxLayout=\"column\" fxLayoutAlign=\"start start\">\n        <h4 class=\"mt-4 mb-2 subheading\" fxFlex=\"100\">\n         Allow Requests Matching\n        </h4>\n\n        <div class=\"w-full\" fxLayout=\"column\" fxLayoutGap=\"5px\">\n          <div\n            formArrayName=\"includePatterns\"\n            *ngFor=\"let control of form.get('includePatterns')['controls']; index as i\"\n          >\n            <div\n              [formGroupName]=\"i\"\n              fxLayout=\"row\"\n              fxLayoutAlign=\"space-around start\"\n              fxLayoutGap=\"10px\"\n            >\n              <mat-form-field fxFlex=\"90\">\n                <mat-label>Pattern</mat-label>\n                <input\n                  matInput\n                  formControlName=\"pattern\"\n                />\n                <mat-hint>e.g. http://localhost:3000/users/.*</mat-hint>\n              </mat-form-field>\n              <button\n                (click)=\"removeIncludePattern(i)\"\n                class=\"mt-2\"\n                color=\"warn\"\n                fxFlex=\"10\"\n                type=\"button\"\n                mat-button\n              >\n                <mat-icon [icIcon]=\"icDelete\"></mat-icon>\n              </button>\n            </div>\n          </div>\n          <button class=\"mb-2\" (click)=\"addIncludePattern()\" color=\"primary\" type=\"button\" mat-raised-button fxFlex=\"100\">\n            New Pattern\n          </button>\n          <!-- <mat-form-field class=\"w-full\">\n            <mat-label>Match Pattern</mat-label>\n            <input matInput formControlName=\"matchPattern\" type=\"text\">\n            <mat-hint>e.g. /users/.* (Optional) </mat-hint>\n          </mat-form-field>\n\n          <button \n            *ngIf=\"form.value.matchPattern\" \n            (click)=\"clearMatchPattern()\"\n            fxFlex=\"40px\" class=\"input-button\" mat-icon-button matSuffix type=\"button\">\n            <div fxLayout=\"row\" fxLayoutAlign=\"center center\">\n              <mat-icon [icIcon]=\"icClose\"></mat-icon>\n            </div>\n          </button> -->\n        </div>\n      </div>\n    </mat-tab>\n    <mat-tab label=\"Exclude\">\n      <div class=\"mt-3 mb-3\" fxLayout=\"column\" fxLayoutAlign=\"start start\">\n        <h4 class=\"mb-2 subheading\" fxFlex=\"100\">\n          Ignore Requests Matching\n        </h4>\n\n        <div class=\"w-full\" fxLayout=\"column\" fxLayoutGap=\"5px\">\n          <div\n            formArrayName=\"excludePatterns\"\n            *ngFor=\"let control of form.get('excludePatterns')['controls']; index as i\"\n          >\n            <div\n              [formGroupName]=\"i\"\n              fxLayout=\"row\"\n              fxLayoutAlign=\"space-around start\"\n              fxLayoutGap=\"10px\"\n            >\n              <mat-form-field fxFlex=\"90\">\n                <mat-label>Pattern</mat-label>\n                <input\n                  matInput\n                  formControlName=\"pattern\"\n                />\n                <mat-hint>e.g. http://localhost:3000/users/.*</mat-hint>\n              </mat-form-field>\n              <button\n                (click)=\"removeExcludePattern(i)\"\n                class=\"mt-2\"\n                color=\"warn\"\n                fxFlex=\"10\"\n                type=\"button\"\n                mat-button\n              >\n                <mat-icon [icIcon]=\"icDelete\"></mat-icon>\n              </button>\n            </div>\n          </div>\n          <button class=\"mb-2\" (click)=\"addExcludePattern()\" color=\"primary\" type=\"button\" mat-raised-button fxFlex=\"100\">\n            New Pattern\n          </button>\n        </div>\n      </div>\n    </mat-tab>\n  </mat-tab-group>\n\n  <mat-divider></mat-divider>\n\n  <mat-dialog-actions align=\"end\">\n    <button [disabled]=\"form.invalid\" color=\"primary\" mat-button type=\"submit\">UPDATE</button>\n    <button mat-button mat-dialog-close type=\"button\">CANCEL</button>\n  </mat-dialog-actions>\n</form>\n");

/***/ }),

/***/ "4GLy":
/*!*****************************************************!*\
  !*** ./src/app/core/http/alias-resource.service.ts ***!
  \*****************************************************/
/*! exports provided: AliasResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AliasResource", function() { return AliasResource; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _rest_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rest-api.service */ "iCaw");



let AliasResource = class AliasResource {
    constructor(restApi) {
        this.restApi = restApi;
        this.ENDPOINT = 'aliases';
    }
    index(queryParams) {
        return this.restApi.index([this.ENDPOINT], queryParams);
    }
    show(id, queryParams) {
        return this.restApi.show([this.ENDPOINT, id], queryParams);
    }
    create(body) {
        return this.restApi.create([this.ENDPOINT], body);
    }
    update(id, body) {
        return this.restApi.update([this.ENDPOINT, id], body);
    }
    destroy(id, queryParams) {
        return this.restApi.destroy([this.ENDPOINT, id], queryParams);
    }
};
AliasResource.ctorParameters = () => [
    { type: _rest_api_service__WEBPACK_IMPORTED_MODULE_2__["RestApiService"] }
];
AliasResource = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], AliasResource);



/***/ }),

/***/ "4UAC":
/*!*******************************************************!*\
  !*** ./src/app/core/http/project-resource.service.ts ***!
  \*******************************************************/
/*! exports provided: ProjectResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectResource", function() { return ProjectResource; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _rest_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rest-api.service */ "iCaw");



let ProjectResource = class ProjectResource {
    constructor(restApi) {
        this.restApi = restApi;
        this.ENDPOINT = 'projects';
    }
    index(queryParams) {
        return this.restApi.index([this.ENDPOINT], queryParams);
    }
    show(id, queryParams) {
        return this.restApi.show([this.ENDPOINT, id], queryParams);
    }
    create(body) {
        return this.restApi.create([this.ENDPOINT], body);
    }
    update(id, body) {
        return this.restApi.update([this.ENDPOINT, id], body);
    }
    destroy(id) {
        return this.restApi.destroy([this.ENDPOINT, id]);
    }
};
ProjectResource.ctorParameters = () => [
    { type: _rest_api_service__WEBPACK_IMPORTED_MODULE_2__["RestApiService"] }
];
ProjectResource = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], ProjectResource);



/***/ }),

/***/ "4mL1":
/*!***************************************************************************************************************************************************!*\
  !*** ./src/app/layout/components/toolbar/components/toolbar-proxy-settings/components/toolbar-mock-settings/toolbar-mock-settings.component.scss ***!
  \***************************************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (".dropdown {\n  background: var(--background-card);\n  border-bottom-left-radius: var(--border-radius);\n  border-bottom-right-radius: var(--border-radius);\n  box-shadow: var(--elevation-z4);\n  max-width: 100vw;\n  overflow: hidden;\n  width: 350px;\n  border-radius: 0.25rem;\n}\n\n.dropdown-header {\n  box-shadow: var(--elevation-z6);\n  padding-top: 1rem;\n  padding-bottom: 1rem;\n  padding-left: 1.5rem;\n  padding-right: 1.5rem;\n}\n\n.dropdown-heading {\n  font: var(--font-title);\n}\n\n.dropdown-content {\n  max-height: 291px;\n  overflow-x: hidden;\n  overflow-y: auto;\n  padding: 10px;\n}\n\n.dropdown-footer {\n  background: var(--background-app-bar);\n  border-top: 1px solid var(--foreground-divider);\n  padding: var(--padding-8) var(--padding);\n}\n\n.notification {\n  color: var(--text-color);\n  padding: var(--padding-16) var(--padding);\n  position: relative;\n  text-decoration: none;\n  transition: var(--trans-ease-out);\n  -webkit-user-select: none;\n     -moz-user-select: none;\n          user-select: none;\n}\n\n.notification:hover {\n  background: var(--background-hover);\n}\n\n.notification:hover .notification-label {\n  --text-opacity: 1;\n  color: #5c77ff;\n  color: rgba(92, 119, 255, var(--text-opacity));\n}\n\n.notification.read {\n  opacity: 0.5;\n}\n\n.notification-icon {\n  -webkit-margin-end: var(--padding);\n          margin-inline-end: var(--padding);\n}\n\n.notification-label {\n  transition: inherit;\n}\n\n.notification-description {\n  color: var(--text-secondary);\n  font: var(--font-caption);\n}\n\n.notification-chevron {\n  color: var(--text-hint);\n  font-size: 18px;\n  height: 18px;\n  width: 18px;\n}\n\n.notification + .notification {\n  border-top: 1px solid var(--foreground-divider);\n}\n\n.input-button {\n  margin-top: 8px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uLy4uLy4uLy4uLy4uL3Rvb2xiYXItbW9jay1zZXR0aW5ncy5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLGtDQUFBO0VBQ0EsK0NBQUE7RUFDQSxnREFBQTtFQUNBLCtCQUFBO0VBQ0EsZ0JBQUE7RUFDQSxnQkFBQTtFQUNBLFlBQUE7RUFDQSxzQkFBQTtBQUNGOztBQUVBO0VBQ0UsK0JBQUE7RUFDQSxpQkFBQTtFQUNBLG9CQUFBO0VBQ0Esb0JBQUE7RUFDQSxxQkFBQTtBQUNGOztBQUVBO0VBQ0UsdUJBQUE7QUFDRjs7QUFFQTtFQUNFLGlCQUFBO0VBQ0Esa0JBQUE7RUFDQSxnQkFBQTtFQUNBLGFBQUE7QUFDRjs7QUFFQTtFQUNFLHFDQUFBO0VBQ0EsK0NBQUE7RUFDQSx3Q0FBQTtBQUNGOztBQUVBO0VBQ0Usd0JBQUE7RUFDQSx5Q0FBQTtFQUNBLGtCQUFBO0VBQ0EscUJBQUE7RUFDQSxpQ0FBQTtFQUNBLHlCQUFBO0tBQUEsc0JBQUE7VUFBQSxpQkFBQTtBQUNGOztBQUVBO0VBQ0UsbUNBQUE7QUFDRjs7QUFFQTtFQUNFLGlCQUFBO0VBQ0EsY0FBQTtFQUNBLDhDQUFBO0FBQ0Y7O0FBRUE7RUFDRSxZQUFBO0FBQ0Y7O0FBRUE7RUFDRSxrQ0FBQTtVQUFBLGlDQUFBO0FBQ0Y7O0FBRUE7RUFDRSxtQkFBQTtBQUNGOztBQUVBO0VBQ0UsNEJBQUE7RUFDQSx5QkFBQTtBQUNGOztBQUVBO0VBQ0UsdUJBQUE7RUFDQSxlQUFBO0VBQ0EsWUFBQTtFQUNBLFdBQUE7QUFDRjs7QUFFQTtFQUNFLCtDQUFBO0FBQ0Y7O0FBRUE7RUFDRSxlQUFBO0FBQ0YiLCJmaWxlIjoidG9vbGJhci1tb2NrLXNldHRpbmdzLmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiLmRyb3Bkb3duIHtcbiAgYmFja2dyb3VuZDogdmFyKC0tYmFja2dyb3VuZC1jYXJkKTtcbiAgYm9yZGVyLWJvdHRvbS1sZWZ0LXJhZGl1czogdmFyKC0tYm9yZGVyLXJhZGl1cyk7XG4gIGJvcmRlci1ib3R0b20tcmlnaHQtcmFkaXVzOiB2YXIoLS1ib3JkZXItcmFkaXVzKTtcbiAgYm94LXNoYWRvdzogdmFyKC0tZWxldmF0aW9uLXo0KTtcbiAgbWF4LXdpZHRoOiAxMDB2dztcbiAgb3ZlcmZsb3c6IGhpZGRlbjtcbiAgd2lkdGg6IDM1MHB4O1xuICBib3JkZXItcmFkaXVzOiAwLjI1cmVtO1xufVxuXG4uZHJvcGRvd24taGVhZGVyIHtcbiAgYm94LXNoYWRvdzogdmFyKC0tZWxldmF0aW9uLXo2KTtcbiAgcGFkZGluZy10b3A6IDFyZW07XG4gIHBhZGRpbmctYm90dG9tOiAxcmVtO1xuICBwYWRkaW5nLWxlZnQ6IDEuNXJlbTtcbiAgcGFkZGluZy1yaWdodDogMS41cmVtO1xufVxuXG4uZHJvcGRvd24taGVhZGluZyB7XG4gIGZvbnQ6IHZhcigtLWZvbnQtdGl0bGUpO1xufVxuXG4uZHJvcGRvd24tY29udGVudCB7XG4gIG1heC1oZWlnaHQ6IDI5MXB4O1xuICBvdmVyZmxvdy14OiBoaWRkZW47XG4gIG92ZXJmbG93LXk6IGF1dG87XG4gIHBhZGRpbmc6IDEwcHg7XG59XG5cbi5kcm9wZG93bi1mb290ZXIge1xuICBiYWNrZ3JvdW5kOiB2YXIoLS1iYWNrZ3JvdW5kLWFwcC1iYXIpO1xuICBib3JkZXItdG9wOiAxcHggc29saWQgdmFyKC0tZm9yZWdyb3VuZC1kaXZpZGVyKTtcbiAgcGFkZGluZzogdmFyKC0tcGFkZGluZy04KSB2YXIoLS1wYWRkaW5nKTtcbn1cblxuLm5vdGlmaWNhdGlvbiB7XG4gIGNvbG9yOiB2YXIoLS10ZXh0LWNvbG9yKTtcbiAgcGFkZGluZzogdmFyKC0tcGFkZGluZy0xNikgdmFyKC0tcGFkZGluZyk7XG4gIHBvc2l0aW9uOiByZWxhdGl2ZTtcbiAgdGV4dC1kZWNvcmF0aW9uOiBub25lO1xuICB0cmFuc2l0aW9uOiB2YXIoLS10cmFucy1lYXNlLW91dCk7XG4gIHVzZXItc2VsZWN0OiBub25lO1xufVxuXG4ubm90aWZpY2F0aW9uOmhvdmVyIHtcbiAgYmFja2dyb3VuZDogdmFyKC0tYmFja2dyb3VuZC1ob3Zlcik7XG59XG5cbi5ub3RpZmljYXRpb246aG92ZXIgLm5vdGlmaWNhdGlvbi1sYWJlbCB7XG4gIC0tdGV4dC1vcGFjaXR5OiAxO1xuICBjb2xvcjogIzVjNzdmZjtcbiAgY29sb3I6IHJnYmEoOTIsIDExOSwgMjU1LCB2YXIoLS10ZXh0LW9wYWNpdHkpKTtcbn1cblxuLm5vdGlmaWNhdGlvbi5yZWFkIHtcbiAgb3BhY2l0eTogMC41O1xufVxuXG4ubm90aWZpY2F0aW9uLWljb24ge1xuICBtYXJnaW4taW5saW5lLWVuZDogdmFyKC0tcGFkZGluZyk7XG59XG5cbi5ub3RpZmljYXRpb24tbGFiZWwge1xuICB0cmFuc2l0aW9uOiBpbmhlcml0O1xufVxuXG4ubm90aWZpY2F0aW9uLWRlc2NyaXB0aW9uIHtcbiAgY29sb3I6IHZhcigtLXRleHQtc2Vjb25kYXJ5KTtcbiAgZm9udDogdmFyKC0tZm9udC1jYXB0aW9uKTtcbn1cblxuLm5vdGlmaWNhdGlvbi1jaGV2cm9uIHtcbiAgY29sb3I6IHZhcigtLXRleHQtaGludCk7XG4gIGZvbnQtc2l6ZTogMThweDtcbiAgaGVpZ2h0OiAxOHB4O1xuICB3aWR0aDogMThweDtcbn1cblxuLm5vdGlmaWNhdGlvbiArIC5ub3RpZmljYXRpb24ge1xuICBib3JkZXItdG9wOiAxcHggc29saWQgdmFyKC0tZm9yZWdyb3VuZC1kaXZpZGVyKTtcbn1cblxuLmlucHV0LWJ1dHRvbiB7XG4gIG1hcmdpbi10b3A6IDhweDtcbn0iXX0= */");

/***/ }),

/***/ "5PI4":
/*!***********************************************************************!*\
  !*** ./src/@vex/components/navigation-item/navigation-item.module.ts ***!
  \***********************************************************************/
/*! exports provided: NavigationItemModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "NavigationItemModule", function() { return NavigationItemModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_material_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/material/core */ "UhP/");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _angular_material_menu__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/menu */ "rJgo");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _navigation_item_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./navigation-item.component */ "yVwa");









let NavigationItemModule = class NavigationItemModule {
};
NavigationItemModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_navigation_item_component__WEBPACK_IMPORTED_MODULE_8__["NavigationItemComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_material_menu__WEBPACK_IMPORTED_MODULE_5__["MatMenuModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_7__["IconModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_4__["MatIconModule"],
            _angular_router__WEBPACK_IMPORTED_MODULE_6__["RouterModule"],
            _angular_material_core__WEBPACK_IMPORTED_MODULE_3__["MatRippleModule"]
        ],
        exports: [_navigation_item_component__WEBPACK_IMPORTED_MODULE_8__["NavigationItemComponent"]]
    })
], NavigationItemModule);



/***/ }),

/***/ "68Yx":
/*!***********************************************************!*\
  !*** ./src/@vex/directives/container/container.module.ts ***!
  \***********************************************************/
/*! exports provided: ContainerModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ContainerModule", function() { return ContainerModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _container_directive__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./container.directive */ "a3ZD");




let ContainerModule = class ContainerModule {
};
ContainerModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_container_directive__WEBPACK_IMPORTED_MODULE_3__["ContainerDirective"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"]
        ],
        exports: [_container_directive__WEBPACK_IMPORTED_MODULE_3__["ContainerDirective"]]
    })
], ContainerModule);



/***/ }),

/***/ "6lMm":
/*!*****************************************************!*\
  !*** ./src/app/layout/custom-layout.component.scss ***!
  \*****************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJjdXN0b20tbGF5b3V0LmNvbXBvbmVudC5zY3NzIn0= */");

/***/ }),

/***/ "71PN":
/*!************************************************!*\
  !*** ./src/app/layout/custom-layout.module.ts ***!
  \************************************************/
/*! exports provided: CustomLayoutModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "CustomLayoutModule", function() { return CustomLayoutModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _vex_components_config_panel_config_panel_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @vex/components/config-panel/config-panel.module */ "mbJQ");
/* harmony import */ var _vex_components_footer_footer_module__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @vex/components/footer/footer.module */ "TphN");
/* harmony import */ var _vex_components_quickpanel_quickpanel_module__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @vex/components/quickpanel/quickpanel.module */ "mQ6f");
/* harmony import */ var _vex_components_sidebar_sidebar_module__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @vex/components/sidebar/sidebar.module */ "zaci");
/* harmony import */ var _vex_layout_layout_module__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @vex/layout/layout.module */ "cwwZ");
/* harmony import */ var _vex_layout_sidenav_sidenav_module__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @vex/layout/sidenav/sidenav.module */ "W9UW");
/* harmony import */ var _components_toolbar_toolbar_module__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./components/toolbar/toolbar.module */ "Hv0H");
/* harmony import */ var _custom_layout_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./custom-layout.component */ "9a6L");











let CustomLayoutModule = class CustomLayoutModule {
};
CustomLayoutModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_custom_layout_component__WEBPACK_IMPORTED_MODULE_10__["CustomLayoutComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _vex_layout_layout_module__WEBPACK_IMPORTED_MODULE_7__["LayoutModule"],
            _vex_layout_sidenav_sidenav_module__WEBPACK_IMPORTED_MODULE_8__["SidenavModule"],
            _components_toolbar_toolbar_module__WEBPACK_IMPORTED_MODULE_9__["ToolbarModule"],
            _vex_components_footer_footer_module__WEBPACK_IMPORTED_MODULE_4__["FooterModule"],
            _vex_components_config_panel_config_panel_module__WEBPACK_IMPORTED_MODULE_3__["ConfigPanelModule"],
            _vex_components_sidebar_sidebar_module__WEBPACK_IMPORTED_MODULE_6__["SidebarModule"],
            _vex_components_quickpanel_quickpanel_module__WEBPACK_IMPORTED_MODULE_5__["QuickpanelModule"],
        ],
    })
], CustomLayoutModule);



/***/ }),

/***/ "7JzS":
/*!******************************************************!*\
  !*** ./src/@vex/layout/sidenav/sidenav.component.ts ***!
  \******************************************************/
/*! exports provided: SidenavComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SidenavComponent", function() { return SidenavComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_sidenav_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./sidenav.component.html */ "bJeg");
/* harmony import */ var _sidenav_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./sidenav.component.scss */ "Li0u");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _iconify_icons_ic_twotone_radio_button_checked__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @iconify/icons-ic/twotone-radio-button-checked */ "vUcO");
/* harmony import */ var _iconify_icons_ic_twotone_radio_button_checked__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_radio_button_checked__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _iconify_icons_ic_twotone_radio_button_unchecked__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @iconify/icons-ic/twotone-radio-button-unchecked */ "8S9z");
/* harmony import */ var _iconify_icons_ic_twotone_radio_button_unchecked__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_radio_button_unchecked__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! rxjs/operators */ "kU1M");
/* harmony import */ var _services_config_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../services/config.service */ "lC2v");
/* harmony import */ var _services_layout_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../services/layout.service */ "CtTw");
/* harmony import */ var _services_navigation_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../services/navigation.service */ "0vMP");
/* harmony import */ var _utils_track_by__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../utils/track-by */ "zK3P");











let SidenavComponent = class SidenavComponent {
    constructor(navigationService, layoutService, configService) {
        this.navigationService = navigationService;
        this.layoutService = layoutService;
        this.configService = configService;
        this.collapsedOpen$ = this.layoutService.sidenavCollapsedOpen$;
        this.title$ = this.configService.config$.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["map"])(config => config.sidenav.title));
        this.imageUrl$ = this.configService.config$.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["map"])(config => config.sidenav.imageUrl));
        this.showCollapsePin$ = this.configService.config$.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["map"])(config => config.sidenav.showCollapsePin));
        this.ready = false;
        this.items = this.navigationService.items;
        this.trackByRoute = _utils_track_by__WEBPACK_IMPORTED_MODULE_10__["trackByRoute"];
        this.icRadioButtonChecked = _iconify_icons_ic_twotone_radio_button_checked__WEBPACK_IMPORTED_MODULE_4___default.a;
        this.icRadioButtonUnchecked = _iconify_icons_ic_twotone_radio_button_unchecked__WEBPACK_IMPORTED_MODULE_5___default.a;
    }
    ngOnInit() {
        // Hack to fix sidenav expanding intially
        // For some reason, if the contents of the sidenav are not rendered, doesn't cause it to expand
        setTimeout(() => {
            this.ready = true;
        });
    }
    onMouseEnter() {
        this.layoutService.collapseOpenSidenav();
    }
    onMouseLeave() {
        this.layoutService.collapseCloseSidenav();
    }
    toggleCollapse() {
        this.collapsed ? this.layoutService.expandSidenav() : this.layoutService.collapseSidenav();
    }
};
SidenavComponent.ctorParameters = () => [
    { type: _services_navigation_service__WEBPACK_IMPORTED_MODULE_9__["NavigationService"] },
    { type: _services_layout_service__WEBPACK_IMPORTED_MODULE_8__["LayoutService"] },
    { type: _services_config_service__WEBPACK_IMPORTED_MODULE_7__["ConfigService"] }
];
SidenavComponent.propDecorators = {
    collapsed: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"] }]
};
SidenavComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'vex-sidenav',
        template: _raw_loader_sidenav_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_sidenav_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], SidenavComponent);



/***/ }),

/***/ "7a8g":
/*!*****************************************************!*\
  !*** ./src/@vex/components/search/search.module.ts ***!
  \*****************************************************/
/*! exports provided: SearchModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SearchModule", function() { return SearchModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "s7LF");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _search_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./search.component */ "x+pQ");








let SearchModule = class SearchModule {
};
SearchModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_search_component__WEBPACK_IMPORTED_MODULE_7__["SearchComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_4__["MatButtonModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_5__["MatIconModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_6__["IconModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_3__["ReactiveFormsModule"]
        ],
        exports: [_search_component__WEBPACK_IMPORTED_MODULE_7__["SearchComponent"]]
    })
], SearchModule);



/***/ }),

/***/ "7v+O":
/*!*********************************************!*\
  !*** ./src/app/data/schema/organization.ts ***!
  \*********************************************/
/*! exports provided: Organization */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Organization", function() { return Organization; });
class Organization {
    constructor(organization) {
        this.id = organization.id;
        this.name = organization.name;
        this.isShadow = organization.is_shadow;
        this.description = organization.description;
        this.currentUserRole = organization.current_user_role;
        this.userCount = organization.user_count;
        this.userId = organization.user_id;
    }
}


/***/ }),

/***/ "87D3":
/*!**************************************************!*\
  !*** ./src/app/core/utils/http-error-handler.ts ***!
  \**************************************************/
/*! exports provided: HttpErrorHandler */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "HttpErrorHandler", function() { return HttpErrorHandler; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/material/snack-bar */ "zHaW");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var angular_token__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! angular-token */ "hU4o");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! rxjs */ "qCKp");
/* harmony import */ var _data_constants_route_constants__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @data/constants/route.constants */ "wZfh");







let HttpErrorHandler = class HttpErrorHandler {
    constructor(router, snackbar, tokenService) {
        this.router = router;
        this.snackbar = snackbar;
        this.tokenService = tokenService;
        this.onlineFlag = navigator.onLine;
    }
    handleError(err) {
        let message = '';
        switch (err.status) {
            case 401:
                this.tokenService.signOut().subscribe(res => {
                    this.router.navigate([_data_constants_route_constants__WEBPACK_IMPORTED_MODULE_6__["RouteConstants"].LOGIN_PAGE]);
                }, res => {
                    this.router.navigate([_data_constants_route_constants__WEBPACK_IMPORTED_MODULE_6__["RouteConstants"].LOGIN_PAGE]);
                });
                break;
            case 404:
                message = 'The requested resource could not be found';
                this.snackbar.open(message, 'close');
                break;
            default:
                if (err.status >= 500) {
                    message = 'An expected error occurred, please try again later';
                }
                else {
                    message = err.error;
                }
                if (typeof message === 'string') {
                    this.snackbar.open(message, 'close');
                }
        }
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_5__["throwError"])(err);
    }
};
HttpErrorHandler.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["Router"] },
    { type: _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_2__["MatSnackBar"] },
    { type: angular_token__WEBPACK_IMPORTED_MODULE_4__["AngularTokenService"] }
];
HttpErrorHandler = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])()
], HttpErrorHandler);



/***/ }),

/***/ "8IoH":
/*!*********************************************!*\
  !*** ./src/app/data/schema/subscription.ts ***!
  \*********************************************/
/*! exports provided: Subscription */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Subscription", function() { return Subscription; });
/* harmony import */ var _plan__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./plan */ "L3CV");

class Subscription {
    constructor(subscription) {
        this.id = subscription.id;
        this.organization_id = subscription.organization_id;
        this.plan = new _plan__WEBPACK_IMPORTED_MODULE_0__["Plan"](subscription.plan);
    }
}


/***/ }),

/***/ "9IlP":
/*!****************************************************!*\
  !*** ./src/app/core/http/user-resource.service.ts ***!
  \****************************************************/
/*! exports provided: UserResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserResource", function() { return UserResource; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _rest_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rest-api.service */ "iCaw");



let UserResource = class UserResource {
    constructor(restApi) {
        this.restApi = restApi;
        this.ENDPOINT = 'users';
    }
    index(queryParams) {
        return this.restApi.index([this.ENDPOINT], queryParams);
    }
    show(id, queryParams) {
        return this.restApi.show([this.ENDPOINT, id], queryParams);
    }
    profile(queryParams) {
        return this.restApi.show([this.ENDPOINT, 'profile'], queryParams);
    }
    create(body) {
        return this.restApi.create([this.ENDPOINT], body);
    }
    update(id, body) {
        return this.restApi.update([this.ENDPOINT, id], body);
    }
    destroy(id) {
        return this.restApi.destroy([this.ENDPOINT, id]);
    }
    subscription(queryParams) {
        return this.restApi.show([this.ENDPOINT, 'subscription'], queryParams);
    }
    payments(queryParams) {
        return this.restApi.index([this.ENDPOINT, 'payments'], queryParams);
    }
};
UserResource.ctorParameters = () => [
    { type: _rest_api_service__WEBPACK_IMPORTED_MODULE_2__["RestApiService"] }
];
UserResource = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], UserResource);



/***/ }),

/***/ "9a6L":
/*!***************************************************!*\
  !*** ./src/app/layout/custom-layout.component.ts ***!
  \***************************************************/
/*! exports provided: CustomLayoutComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "CustomLayoutComponent", function() { return CustomLayoutComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_custom_layout_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./custom-layout.component.html */ "+mfJ");
/* harmony import */ var _custom_layout_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./custom-layout.component.scss */ "6lMm");
/* harmony import */ var _angular_cdk_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/cdk/layout */ "HeVh");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! rxjs/operators */ "kU1M");
/* harmony import */ var _vex_services_config_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @vex/services/config.service */ "lC2v");
/* harmony import */ var _vex_services_layout_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @vex/services/layout.service */ "CtTw");
/* harmony import */ var _vex_utils_check_router_childs_data__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @vex/utils/check-router-childs-data */ "3TZW");
/* harmony import */ var _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @vex/utils/tailwindcss */ "XXSj");











let CustomLayoutComponent = class CustomLayoutComponent {
    constructor(layoutService, configService, breakpointObserver, router) {
        this.layoutService = layoutService;
        this.configService = configService;
        this.breakpointObserver = breakpointObserver;
        this.router = router;
        this.sidenavCollapsed$ = this.layoutService.sidenavCollapsed$;
        this.sidenavCollapsedOpen$ = this.layoutService.sidenavCollapsedOpen$;
        this.isFooterVisible$ = this.configService.config$.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["map"])(config => config.footer.visible));
        this.isDesktop$ = this.breakpointObserver.observe(`(min-width: ${_vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_10__["default"].screens.lg})`).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["map"])(state => state.matches));
        this.toolbarShadowEnabled$ = this.router.events.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["filter"])(event => event instanceof _angular_router__WEBPACK_IMPORTED_MODULE_5__["NavigationEnd"]), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["startWith"])(null), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["map"])(() => Object(_vex_utils_check_router_childs_data__WEBPACK_IMPORTED_MODULE_9__["checkRouterChildsData"])(this.router.routerState.root.snapshot, data => data.toolbarShadowEnabled)));
    }
    ngOnInit() {
        // this.layoutService.configpanelOpen$.pipe(
        //   untilDestroyed(this)
        // ).subscribe(open => open ? this.configpanel.open() : this.configpanel.close());
    }
    ngOnDestroy() { }
};
CustomLayoutComponent.ctorParameters = () => [
    { type: _vex_services_layout_service__WEBPACK_IMPORTED_MODULE_8__["LayoutService"] },
    { type: _vex_services_config_service__WEBPACK_IMPORTED_MODULE_7__["ConfigService"] },
    { type: _angular_cdk_layout__WEBPACK_IMPORTED_MODULE_3__["BreakpointObserver"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_5__["Router"] }
];
CustomLayoutComponent.propDecorators = {
    configpanel: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["ViewChild"], args: ['configpanel', { static: true },] }]
};
CustomLayoutComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_4__["Component"])({
        selector: 'vex-custom-layout',
        template: _raw_loader_custom_layout_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_custom_layout_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], CustomLayoutComponent);



/***/ }),

/***/ "A/vA":
/*!***************************************************************!*\
  !*** ./src/app/core/http/body-param-name-resource.service.ts ***!
  \***************************************************************/
/*! exports provided: BodyParamNameResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "BodyParamNameResource", function() { return BodyParamNameResource; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _rest_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rest-api.service */ "iCaw");



let BodyParamNameResource = class BodyParamNameResource {
    constructor(restApi) {
        this.restApi = restApi;
        this.ENDPOINT_ENDPOINT = 'endpoints';
        this.ENDPOINT = 'body_param_names';
    }
    index(endpointId, queryParams) {
        if (typeof endpointId === 'object') {
            queryParams = endpointId;
            return this.restApi.index([this.ENDPOINT], queryParams);
        }
        else {
            return this.restApi.index([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT], queryParams);
        }
    }
    show(endpointId, id, queryParams) {
        return this.restApi.show([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT, id], queryParams);
    }
    create(endpointId, body) {
        return this.restApi.create([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT], body);
    }
    update(endpointId, id, body) {
        return this.restApi.update([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT, id], body);
    }
    destroy(endpointId, id) {
        return this.restApi.destroy([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT, id]);
    }
};
BodyParamNameResource.ctorParameters = () => [
    { type: _rest_api_service__WEBPACK_IMPORTED_MODULE_2__["RestApiService"] }
];
BodyParamNameResource = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], BodyParamNameResource);



/***/ }),

/***/ "A4cF":
/*!*************************************************!*\
  !*** ./src/@vex/pipes/color/color-fade.pipe.ts ***!
  \*************************************************/
/*! exports provided: ColorFadePipe */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ColorFadePipe", function() { return ColorFadePipe; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var color__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! color */ "aSns");
/* harmony import */ var color__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(color__WEBPACK_IMPORTED_MODULE_2__);



let ColorFadePipe = class ColorFadePipe {
    transform(value, ratio) {
        return color__WEBPACK_IMPORTED_MODULE_2___default()(value).fade(ratio);
    }
};
ColorFadePipe = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Pipe"])({
        name: 'colorFade'
    })
], ColorFadePipe);



/***/ }),

/***/ "A8r0":
/*!******************************************************************!*\
  !*** ./src/@vex/components/quickpanel/quickpanel.component.scss ***!
  \******************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (":host {\n  display: flex;\n  flex-direction: column;\n  height: 100%;\n  max-width: 80vw;\n}\n\nh3 {\n  padding: 16px 16px 0;\n}\n\np {\n  margin: 0;\n}\n\n.list-item {\n  cursor: pointer;\n  display: flex;\n  flex-direction: column;\n  font: var(--font-subheading-2);\n  justify-content: center;\n  min-height: 72px;\n  padding: 0 var(--padding-16);\n  position: relative;\n  -webkit-user-select: none;\n     -moz-user-select: none;\n          user-select: none;\n}\n\n.list-item:hover {\n  background: var(--background-hover);\n}\n\n.progress-bar {\n  margin-top: 8px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uL3F1aWNrcGFuZWwuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSxhQUFBO0VBQ0Esc0JBQUE7RUFDQSxZQUFBO0VBQ0EsZUFBQTtBQUNGOztBQUVBO0VBQ0Usb0JBQUE7QUFDRjs7QUFFQTtFQUNFLFNBQUE7QUFDRjs7QUFFQTtFQUNFLGVBQUE7RUFDQSxhQUFBO0VBQ0Esc0JBQUE7RUFDQSw4QkFBQTtFQUNBLHVCQUFBO0VBQ0EsZ0JBQUE7RUFDQSw0QkFBQTtFQUNBLGtCQUFBO0VBQ0EseUJBQUE7S0FBQSxzQkFBQTtVQUFBLGlCQUFBO0FBQ0Y7O0FBRUE7RUFDRSxtQ0FBQTtBQUNGOztBQUVBO0VBQ0UsZUFBQTtBQUNGIiwiZmlsZSI6InF1aWNrcGFuZWwuY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyI6aG9zdCB7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGZsZXgtZGlyZWN0aW9uOiBjb2x1bW47XG4gIGhlaWdodDogMTAwJTtcbiAgbWF4LXdpZHRoOiA4MHZ3O1xufVxuXG5oMyB7XG4gIHBhZGRpbmc6IDE2cHggMTZweCAwO1xufVxuXG5wIHtcbiAgbWFyZ2luOiAwO1xufVxuXG4ubGlzdC1pdGVtIHtcbiAgY3Vyc29yOiBwb2ludGVyO1xuICBkaXNwbGF5OiBmbGV4O1xuICBmbGV4LWRpcmVjdGlvbjogY29sdW1uO1xuICBmb250OiB2YXIoLS1mb250LXN1YmhlYWRpbmctMik7XG4gIGp1c3RpZnktY29udGVudDogY2VudGVyO1xuICBtaW4taGVpZ2h0OiA3MnB4O1xuICBwYWRkaW5nOiAwIHZhcigtLXBhZGRpbmctMTYpO1xuICBwb3NpdGlvbjogcmVsYXRpdmU7XG4gIHVzZXItc2VsZWN0OiBub25lO1xufVxuXG4ubGlzdC1pdGVtOmhvdmVyIHtcbiAgYmFja2dyb3VuZDogdmFyKC0tYmFja2dyb3VuZC1ob3Zlcik7XG59XG5cbi5wcm9ncmVzcy1iYXIge1xuICBtYXJnaW4tdG9wOiA4cHg7XG59Il19 */");

/***/ }),

/***/ "AKSP":
/*!*******************************************************************************************************!*\
  !*** ./src/app/layout/components/toolbar/components/toolbar-mock-url/toolbar-mock-url.component.scss ***!
  \*******************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (".dropdown {\n  background: var(--background-card);\n  border-bottom-left-radius: var(--border-radius);\n  border-bottom-right-radius: var(--border-radius);\n  box-shadow: var(--elevation-z4);\n  max-width: 100vw;\n  overflow: hidden;\n  width: 350px;\n  border-radius: 0.25rem;\n}\n\n.dropdown-content {\n  max-height: 291px;\n  overflow-x: hidden;\n  overflow-y: auto;\n  padding: 10px;\n}\n\n.dropdown-footer {\n  background: var(--background-app-bar);\n  border-top: 1px solid var(--foreground-divider);\n  padding: var(--padding-8) var(--padding);\n}\n\n.notification {\n  color: var(--text-color);\n  padding: var(--padding-16) var(--padding);\n  position: relative;\n  text-decoration: none;\n  transition: var(--trans-ease-out);\n  -webkit-user-select: none;\n     -moz-user-select: none;\n          user-select: none;\n}\n\n.notification:hover {\n  background: var(--background-hover);\n}\n\n.notification:hover .notification-label {\n  --text-opacity: 1;\n  color: #5c77ff;\n  color: rgba(92, 119, 255, var(--text-opacity));\n}\n\n.notification.read {\n  opacity: 0.5;\n}\n\n.notification-icon {\n  -webkit-margin-end: var(--padding);\n          margin-inline-end: var(--padding);\n}\n\n.notification-label {\n  transition: inherit;\n}\n\n.notification-description {\n  color: var(--text-secondary);\n  font: var(--font-caption);\n}\n\n.notification-chevron {\n  color: var(--text-hint);\n  font-size: 18px;\n  height: 18px;\n  width: 18px;\n}\n\n.notification + .notification {\n  border-top: 1px solid var(--foreground-divider);\n}\n\n.input-button {\n  margin-top: 8px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uLy4uLy4uL3Rvb2xiYXItbW9jay11cmwuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSxrQ0FBQTtFQUNBLCtDQUFBO0VBQ0EsZ0RBQUE7RUFDQSwrQkFBQTtFQUNBLGdCQUFBO0VBQ0EsZ0JBQUE7RUFDQSxZQUFBO0VBQ0Esc0JBQUE7QUFDRjs7QUFFQTtFQUNFLGlCQUFBO0VBQ0Esa0JBQUE7RUFDQSxnQkFBQTtFQUNBLGFBQUE7QUFDRjs7QUFFQTtFQUNFLHFDQUFBO0VBQ0EsK0NBQUE7RUFDQSx3Q0FBQTtBQUNGOztBQUVBO0VBQ0Usd0JBQUE7RUFDQSx5Q0FBQTtFQUNBLGtCQUFBO0VBQ0EscUJBQUE7RUFDQSxpQ0FBQTtFQUNBLHlCQUFBO0tBQUEsc0JBQUE7VUFBQSxpQkFBQTtBQUNGOztBQUVBO0VBQ0UsbUNBQUE7QUFDRjs7QUFFQTtFQUNFLGlCQUFBO0VBQ0EsY0FBQTtFQUNBLDhDQUFBO0FBQ0Y7O0FBRUE7RUFDRSxZQUFBO0FBQ0Y7O0FBRUE7RUFDRSxrQ0FBQTtVQUFBLGlDQUFBO0FBQ0Y7O0FBRUE7RUFDRSxtQkFBQTtBQUNGOztBQUVBO0VBQ0UsNEJBQUE7RUFDQSx5QkFBQTtBQUNGOztBQUVBO0VBQ0UsdUJBQUE7RUFDQSxlQUFBO0VBQ0EsWUFBQTtFQUNBLFdBQUE7QUFDRjs7QUFFQTtFQUNFLCtDQUFBO0FBQ0Y7O0FBRUE7RUFDRSxlQUFBO0FBQ0YiLCJmaWxlIjoidG9vbGJhci1tb2NrLXVybC5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbIi5kcm9wZG93biB7XG4gIGJhY2tncm91bmQ6IHZhcigtLWJhY2tncm91bmQtY2FyZCk7XG4gIGJvcmRlci1ib3R0b20tbGVmdC1yYWRpdXM6IHZhcigtLWJvcmRlci1yYWRpdXMpO1xuICBib3JkZXItYm90dG9tLXJpZ2h0LXJhZGl1czogdmFyKC0tYm9yZGVyLXJhZGl1cyk7XG4gIGJveC1zaGFkb3c6IHZhcigtLWVsZXZhdGlvbi16NCk7XG4gIG1heC13aWR0aDogMTAwdnc7XG4gIG92ZXJmbG93OiBoaWRkZW47XG4gIHdpZHRoOiAzNTBweDtcbiAgYm9yZGVyLXJhZGl1czogMC4yNXJlbTtcbn1cblxuLmRyb3Bkb3duLWNvbnRlbnQge1xuICBtYXgtaGVpZ2h0OiAyOTFweDtcbiAgb3ZlcmZsb3cteDogaGlkZGVuO1xuICBvdmVyZmxvdy15OiBhdXRvO1xuICBwYWRkaW5nOiAxMHB4O1xufVxuXG4uZHJvcGRvd24tZm9vdGVyIHtcbiAgYmFja2dyb3VuZDogdmFyKC0tYmFja2dyb3VuZC1hcHAtYmFyKTtcbiAgYm9yZGVyLXRvcDogMXB4IHNvbGlkIHZhcigtLWZvcmVncm91bmQtZGl2aWRlcik7XG4gIHBhZGRpbmc6IHZhcigtLXBhZGRpbmctOCkgdmFyKC0tcGFkZGluZyk7XG59XG5cbi5ub3RpZmljYXRpb24ge1xuICBjb2xvcjogdmFyKC0tdGV4dC1jb2xvcik7XG4gIHBhZGRpbmc6IHZhcigtLXBhZGRpbmctMTYpIHZhcigtLXBhZGRpbmcpO1xuICBwb3NpdGlvbjogcmVsYXRpdmU7XG4gIHRleHQtZGVjb3JhdGlvbjogbm9uZTtcbiAgdHJhbnNpdGlvbjogdmFyKC0tdHJhbnMtZWFzZS1vdXQpO1xuICB1c2VyLXNlbGVjdDogbm9uZTtcbn1cblxuLm5vdGlmaWNhdGlvbjpob3ZlciB7XG4gIGJhY2tncm91bmQ6IHZhcigtLWJhY2tncm91bmQtaG92ZXIpO1xufVxuXG4ubm90aWZpY2F0aW9uOmhvdmVyIC5ub3RpZmljYXRpb24tbGFiZWwge1xuICAtLXRleHQtb3BhY2l0eTogMTtcbiAgY29sb3I6ICM1Yzc3ZmY7XG4gIGNvbG9yOiByZ2JhKDkyLCAxMTksIDI1NSwgdmFyKC0tdGV4dC1vcGFjaXR5KSk7XG59XG5cbi5ub3RpZmljYXRpb24ucmVhZCB7XG4gIG9wYWNpdHk6IDAuNTtcbn1cblxuLm5vdGlmaWNhdGlvbi1pY29uIHtcbiAgbWFyZ2luLWlubGluZS1lbmQ6IHZhcigtLXBhZGRpbmcpO1xufVxuXG4ubm90aWZpY2F0aW9uLWxhYmVsIHtcbiAgdHJhbnNpdGlvbjogaW5oZXJpdDtcbn1cblxuLm5vdGlmaWNhdGlvbi1kZXNjcmlwdGlvbiB7XG4gIGNvbG9yOiB2YXIoLS10ZXh0LXNlY29uZGFyeSk7XG4gIGZvbnQ6IHZhcigtLWZvbnQtY2FwdGlvbik7XG59XG5cbi5ub3RpZmljYXRpb24tY2hldnJvbiB7XG4gIGNvbG9yOiB2YXIoLS10ZXh0LWhpbnQpO1xuICBmb250LXNpemU6IDE4cHg7XG4gIGhlaWdodDogMThweDtcbiAgd2lkdGg6IDE4cHg7XG59XG5cbi5ub3RpZmljYXRpb24gKyAubm90aWZpY2F0aW9uIHtcbiAgYm9yZGVyLXRvcDogMXB4IHNvbGlkIHZhcigtLWZvcmVncm91bmQtZGl2aWRlcik7XG59XG5cbi5pbnB1dC1idXR0b24ge1xuICBtYXJnaW4tdG9wOiA4cHg7XG59Il19 */");

/***/ }),

/***/ "AQ4D":
/*!****************************************************!*\
  !*** ./src/@vex/services/splash-screen.service.ts ***!
  \****************************************************/
/*! exports provided: SplashScreenService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SplashScreenService", function() { return SplashScreenService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_animations__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/animations */ "GS7A");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! rxjs/operators */ "kU1M");






let SplashScreenService = class SplashScreenService {
    constructor(router, document, animationBuilder) {
        this.router = router;
        this.document = document;
        this.animationBuilder = animationBuilder;
        this.splashScreenElem = this.document.body.querySelector('#vex-splash-screen');
        if (this.splashScreenElem) {
            this.router.events.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["filter"])(event => event instanceof _angular_router__WEBPACK_IMPORTED_MODULE_4__["NavigationEnd"]), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["take"])(1)).subscribe(() => this.hide());
        }
    }
    hide() {
        const player = this.animationBuilder.build([
            Object(_angular_animations__WEBPACK_IMPORTED_MODULE_1__["style"])({
                opacity: 1
            }),
            Object(_angular_animations__WEBPACK_IMPORTED_MODULE_1__["animate"])('400ms cubic-bezier(0.25, 0.8, 0.25, 1)', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_1__["style"])({
                opacity: 0
            }))
        ]).create(this.splashScreenElem);
        player.onDone(() => this.splashScreenElem.remove());
        player.play();
    }
};
SplashScreenService.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["Router"] },
    { type: Document, decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Inject"], args: [_angular_common__WEBPACK_IMPORTED_MODULE_2__["DOCUMENT"],] }] },
    { type: _angular_animations__WEBPACK_IMPORTED_MODULE_1__["AnimationBuilder"] }
];
SplashScreenService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Injectable"])({
        providedIn: 'root'
    })
], SplashScreenService);



/***/ }),

/***/ "AytR":
/*!*****************************************!*\
  !*** ./src/environments/environment.ts ***!
  \*****************************************/
/*! exports provided: environment */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "environment", function() { return environment; });
// This file can be replaced during build by using the `fileReplacements` array.
// `ng build --prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.
const environment = {
    agentUrl: 'http://0.0.0.0:4200',
    apiUrl: 'https://alpha.api.stoobly.com',
    googleOauthClientId: '320365524835-sb4qjo8h93v257gbfbre9k38fv46k0cu.apps.googleusercontent.com',
    homepageUrl: 'http://localhost:4200/login',
    production: false,
    stripeKey: 'pk_test_Pf0dKM9QvXwkm5FPGCaxE5Xt',
};
/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/dist/zone-error';  // Included with Angular CLI.


/***/ }),

/***/ "B1Wa":
/*!***********************************************************!*\
  !*** ./src/app/core/http/header-name-resource.service.ts ***!
  \***********************************************************/
/*! exports provided: HeaderNameResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "HeaderNameResource", function() { return HeaderNameResource; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _rest_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rest-api.service */ "iCaw");



let HeaderNameResource = class HeaderNameResource {
    constructor(restApi) {
        this.restApi = restApi;
        this.ENDPOINT_ENDPOINT = 'endpoints';
        this.ENDPOINT = 'header_names';
    }
    index(endpointId, queryParams) {
        if (typeof endpointId === 'object') {
            queryParams = endpointId;
            return this.restApi.index([this.ENDPOINT], queryParams);
        }
        else {
            return this.restApi.index([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT], queryParams);
        }
    }
    show(endpointId, id, queryParams) {
        return this.restApi.show([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT, id], queryParams);
    }
    create(endpointId, body) {
        return this.restApi.create([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT], body);
    }
    update(endpointId, id, body) {
        return this.restApi.update([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT, id], body);
    }
    destroy(endpointId, id) {
        return this.restApi.destroy([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT, id]);
    }
};
HeaderNameResource.ctorParameters = () => [
    { type: _rest_api_service__WEBPACK_IMPORTED_MODULE_2__["RestApiService"] }
];
HeaderNameResource = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], HeaderNameResource);



/***/ }),

/***/ "BjwJ":
/*!*******************************************!*\
  !*** ./src/app/core/utils/uri.service.ts ***!
  \*******************************************/
/*! exports provided: UriService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UriService", function() { return UriService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");


let UriService = class UriService {
    constructor() {
        this.class = __webpack_require__(/*! url-parse */ "GBY4");
    }
};
UriService.ctorParameters = () => [];
UriService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], UriService);



/***/ }),

/***/ "BrZ/":
/*!*************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/@vex/layout/layout.component.html ***!
  \*************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div [class.boxed]=\"isBoxed$ | async\"\r\n     [class.horizontal-layout]=\"!(isLayoutVertical$ | async)\"\r\n     [class.is-mobile]=\"!(isDesktop$ | async)\"\r\n     [class.vertical-layout]=\"isLayoutVertical$ | async\"\r\n     [class.has-fixed-footer]=\"(isFooterFixed$ | async) && isFooterVisible$ | async\"\r\n     [class.has-footer]=\"isFooterVisible$ | async\"\r\n     [class.scroll-disabled]=\"scrollDisabled$ | async\"\r\n     [class.toolbar-fixed]=\"isToolbarFixed$ | async\"\r\n     [class.sidenav-collapsed]=\"sidenavCollapsed$ | async\"\r\n     [class.content-container]=\"containerEnabled$ | async\"\r\n     [class.with-search]=\"searchOpen$ | async\"\r\n     class=\"page-container\">\r\n\r\n  <vex-progress-bar></vex-progress-bar>\r\n\r\n  <vex-search></vex-search>\r\n\r\n  <mat-sidenav-container \r\n    class=\"sidenav-container\" \r\n    [hasBackdrop]=\"(!(sidenavCollapsed$ | async) || (sidenavCollapsedOpen$ | async))\"\r\n  >\r\n    <mat-sidenav #sidenav\r\n                 [disableClose]=\"isDesktop$ | async\"\r\n                 [fixedInViewport]=\"!(isDesktop$ | async)\"\r\n                 [mode]=\"!(isDesktop$ | async) || (isLayoutVertical$ | async) ? 'over' : 'side'\"\r\n                 [opened]=\"(isDesktop$ | async) && !(isLayoutVertical$ | async)\"\r\n                 class=\"sidenav\">\r\n      <ng-container *ngTemplateOutlet=\"sidenavRef\"></ng-container>\r\n    </mat-sidenav>\r\n\r\n    <mat-sidenav #quickpanel\r\n                 [fixedInViewport]=\"!(isDesktop$ | async)\"\r\n                 class=\"quickpanel\"\r\n                 mode=\"over\"\r\n                 position=\"end\">\r\n      <ng-container *ngTemplateOutlet=\"quickpanelRef\"></ng-container>\r\n    </mat-sidenav>\r\n\r\n    <mat-sidenav-content class=\"sidenav-content\">\r\n      <ng-container *ngTemplateOutlet=\"toolbarRef\"></ng-container>\r\n\r\n      <main class=\"content\">\r\n        <router-outlet></router-outlet>\r\n      </main>\r\n\r\n      <ng-container *ngTemplateOutlet=\"footerRef\"></ng-container>\r\n    </mat-sidenav-content>\r\n  </mat-sidenav-container>\r\n</div>\r\n\r\n");

/***/ }),

/***/ "C6sw":
/*!***********************************************************!*\
  !*** ./src/@vex/components/mega-menu/mega-menu.module.ts ***!
  \***********************************************************/
/*! exports provided: MegaMenuModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MegaMenuModule", function() { return MegaMenuModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _mega_menu_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./mega-menu.component */ "pXZ5");








let MegaMenuModule = class MegaMenuModule {
};
MegaMenuModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_mega_menu_component__WEBPACK_IMPORTED_MODULE_7__["MegaMenuComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_4__["MatButtonModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_6__["IconModule"],
            _angular_router__WEBPACK_IMPORTED_MODULE_5__["RouterModule"]
        ],
        exports: [_mega_menu_component__WEBPACK_IMPORTED_MODULE_7__["MegaMenuComponent"]],
        entryComponents: [_mega_menu_component__WEBPACK_IMPORTED_MODULE_7__["MegaMenuComponent"]]
    })
], MegaMenuModule);



/***/ }),

/***/ "C8+Y":
/*!****************************************************************************!*\
  !*** ./src/@vex/components/navigation-item/navigation-item.component.scss ***!
  \****************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (".navigation-item {\n  border-radius: 0.25rem;\n  cursor: pointer;\n  font-size: 0.875rem;\n  font-weight: 500;\n  padding-left: 1rem;\n  padding-right: 1rem;\n  padding-top: 0.5rem;\n  padding-bottom: 0.5rem;\n  position: relative;\n  -webkit-user-select: none;\n     -moz-user-select: none;\n          user-select: none;\n  text-decoration: none;\n  display: block;\n  -webkit-margin-end: var(--padding-8);\n          margin-inline-end: var(--padding-8);\n  transition: var(--trans-ease-out);\n}\n\n.navigation-color {\n  color: var(--navigation-color);\n}\n\n.navigation-menu-item {\n  transition: var(--trans-ease-out);\n}\n\n.navigation-menu-item:hover {\n  --text-opacity: 1;\n  color: #5c77ff;\n  color: rgba(92, 119, 255, var(--text-opacity));\n}\n\n.navigation-menu-item:hover .mat-icon {\n  --text-opacity: 1;\n  color: #5c77ff;\n  color: rgba(92, 119, 255, var(--text-opacity));\n}\n\n.navigation-menu-item .mat-icon {\n  transition: var(--trans-ease-out);\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uL25hdmlnYXRpb24taXRlbS5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLHNCQUFBO0VBQ0EsZUFBQTtFQUNBLG1CQUFBO0VBQ0EsZ0JBQUE7RUFDQSxrQkFBQTtFQUNBLG1CQUFBO0VBQ0EsbUJBQUE7RUFDQSxzQkFBQTtFQUNBLGtCQUFBO0VBQ0EseUJBQUE7S0FBQSxzQkFBQTtVQUFBLGlCQUFBO0VBQ0EscUJBQUE7RUFDQSxjQUFBO0VBQ0Esb0NBQUE7VUFBQSxtQ0FBQTtFQUNBLGlDQUFBO0FBQ0Y7O0FBRUE7RUFDRSw4QkFBQTtBQUNGOztBQUVBO0VBQ0UsaUNBQUE7QUFDRjs7QUFFQTtFQUNFLGlCQUFBO0VBQ0EsY0FBQTtFQUNBLDhDQUFBO0FBQ0Y7O0FBRUE7RUFDRSxpQkFBQTtFQUNBLGNBQUE7RUFDQSw4Q0FBQTtBQUNGOztBQUVBO0VBQ0UsaUNBQUE7QUFDRiIsImZpbGUiOiJuYXZpZ2F0aW9uLWl0ZW0uY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyIubmF2aWdhdGlvbi1pdGVtIHtcbiAgYm9yZGVyLXJhZGl1czogMC4yNXJlbTtcbiAgY3Vyc29yOiBwb2ludGVyO1xuICBmb250LXNpemU6IDAuODc1cmVtO1xuICBmb250LXdlaWdodDogNTAwO1xuICBwYWRkaW5nLWxlZnQ6IDFyZW07XG4gIHBhZGRpbmctcmlnaHQ6IDFyZW07XG4gIHBhZGRpbmctdG9wOiAwLjVyZW07XG4gIHBhZGRpbmctYm90dG9tOiAwLjVyZW07XG4gIHBvc2l0aW9uOiByZWxhdGl2ZTtcbiAgdXNlci1zZWxlY3Q6IG5vbmU7XG4gIHRleHQtZGVjb3JhdGlvbjogbm9uZTtcbiAgZGlzcGxheTogYmxvY2s7XG4gIG1hcmdpbi1pbmxpbmUtZW5kOiB2YXIoLS1wYWRkaW5nLTgpO1xuICB0cmFuc2l0aW9uOiB2YXIoLS10cmFucy1lYXNlLW91dCk7XG59XG5cbi5uYXZpZ2F0aW9uLWNvbG9yIHtcbiAgY29sb3I6IHZhcigtLW5hdmlnYXRpb24tY29sb3IpO1xufVxuXG4ubmF2aWdhdGlvbi1tZW51LWl0ZW0ge1xuICB0cmFuc2l0aW9uOiB2YXIoLS10cmFucy1lYXNlLW91dCk7XG59XG5cbi5uYXZpZ2F0aW9uLW1lbnUtaXRlbTpob3ZlciB7XG4gIC0tdGV4dC1vcGFjaXR5OiAxO1xuICBjb2xvcjogIzVjNzdmZjtcbiAgY29sb3I6IHJnYmEoOTIsIDExOSwgMjU1LCB2YXIoLS10ZXh0LW9wYWNpdHkpKTtcbn1cblxuLm5hdmlnYXRpb24tbWVudS1pdGVtOmhvdmVyIC5tYXQtaWNvbiB7XG4gIC0tdGV4dC1vcGFjaXR5OiAxO1xuICBjb2xvcjogIzVjNzdmZjtcbiAgY29sb3I6IHJnYmEoOTIsIDExOSwgMjU1LCB2YXIoLS10ZXh0LW9wYWNpdHkpKTtcbn1cblxuLm5hdmlnYXRpb24tbWVudS1pdGVtIC5tYXQtaWNvbiB7XG4gIHRyYW5zaXRpb246IHZhcigtLXRyYW5zLWVhc2Utb3V0KTtcbn0iXX0= */");

/***/ }),

/***/ "CTrj":
/*!**********************************************************************!*\
  !*** ./src/@vex/components/sidenav-item/sidenav-item.component.scss ***!
  \**********************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (".item {\n  align-items: center;\n  box-sizing: border-box;\n  color: var(--sidenav-item-color);\n  cursor: pointer;\n  display: flex;\n  flex-direction: row;\n  min-height: 48px;\n  padding: var(--padding-8) var(--sidenav-item-padding);\n  position: relative;\n  text-decoration: none;\n  transition: var(--trans-ease-out);\n  -webkit-user-select: none;\n     -moz-user-select: none;\n          user-select: none;\n  width: 100%;\n}\n\n.item:hover, .item.active {\n  background: var(--sidenav-item-background-active);\n}\n\n.item:hover .item-icon, .item.active .item-icon {\n  color: var(--sidenav-item-icon-color-active);\n}\n\n.item:hover .item-label, .item.active .item-label {\n  color: var(--sidenav-item-color-active);\n}\n\n.item:hover .item-dropdown-icon, .item.active .item-dropdown-icon {\n  color: var(--sidenav-item-color-active);\n}\n\n.item.open .item-dropdown-icon {\n  transform: rotate(90deg) !important;\n}\n\n:host(.item-level-1) .item {\n  background: var(--sidenav-item-dropdown-background);\n  -webkit-padding-start: calc(var(--sidenav-item-icon-size) + var(--sidenav-item-icon-gap) + var(--sidenav-item-padding) + (var(--sidenav-item-dropdown-gap) * 0));\n          padding-inline-start: calc(var(--sidenav-item-icon-size) + var(--sidenav-item-icon-gap) + var(--sidenav-item-padding) + (var(--sidenav-item-dropdown-gap) * 0));\n}\n\n:host(.item-level-1) .item:hover {\n  background: var(--sidenav-item-dropdown-background-hover);\n}\n\n:host(.item-level-2) .item {\n  background: var(--sidenav-item-dropdown-background);\n  -webkit-padding-start: calc(var(--sidenav-item-icon-size) + var(--sidenav-item-icon-gap) + var(--sidenav-item-padding) + (var(--sidenav-item-dropdown-gap) * 1));\n          padding-inline-start: calc(var(--sidenav-item-icon-size) + var(--sidenav-item-icon-gap) + var(--sidenav-item-padding) + (var(--sidenav-item-dropdown-gap) * 1));\n}\n\n:host(.item-level-2) .item:hover {\n  background: var(--sidenav-item-dropdown-background-hover);\n}\n\n:host(.item-level-3) .item {\n  background: var(--sidenav-item-dropdown-background);\n  -webkit-padding-start: calc(var(--sidenav-item-icon-size) + var(--sidenav-item-icon-gap) + var(--sidenav-item-padding) + (var(--sidenav-item-dropdown-gap) * 2));\n          padding-inline-start: calc(var(--sidenav-item-icon-size) + var(--sidenav-item-icon-gap) + var(--sidenav-item-padding) + (var(--sidenav-item-dropdown-gap) * 2));\n}\n\n:host(.item-level-3) .item:hover {\n  background: var(--sidenav-item-dropdown-background-hover);\n}\n\n:host(.item-level-4) .item {\n  background: var(--sidenav-item-dropdown-background);\n  -webkit-padding-start: calc(var(--sidenav-item-icon-size) + var(--sidenav-item-icon-gap) + var(--sidenav-item-padding) + (var(--sidenav-item-dropdown-gap) * 3));\n          padding-inline-start: calc(var(--sidenav-item-icon-size) + var(--sidenav-item-icon-gap) + var(--sidenav-item-padding) + (var(--sidenav-item-dropdown-gap) * 3));\n}\n\n:host(.item-level-4) .item:hover {\n  background: var(--sidenav-item-dropdown-background-hover);\n}\n\n:host(.item-level-5) .item {\n  background: var(--sidenav-item-dropdown-background);\n  -webkit-padding-start: calc(var(--sidenav-item-icon-size) + var(--sidenav-item-icon-gap) + var(--sidenav-item-padding) + (var(--sidenav-item-dropdown-gap) * 4));\n          padding-inline-start: calc(var(--sidenav-item-icon-size) + var(--sidenav-item-icon-gap) + var(--sidenav-item-padding) + (var(--sidenav-item-dropdown-gap) * 4));\n}\n\n:host(.item-level-5) .item:hover {\n  background: var(--sidenav-item-dropdown-background-hover);\n}\n\n:host(.item-level-6) .item {\n  background: var(--sidenav-item-dropdown-background);\n  -webkit-padding-start: calc(var(--sidenav-item-icon-size) + var(--sidenav-item-icon-gap) + var(--sidenav-item-padding) + (var(--sidenav-item-dropdown-gap) * 5));\n          padding-inline-start: calc(var(--sidenav-item-icon-size) + var(--sidenav-item-icon-gap) + var(--sidenav-item-padding) + (var(--sidenav-item-dropdown-gap) * 5));\n}\n\n:host(.item-level-6) .item:hover {\n  background: var(--sidenav-item-dropdown-background-hover);\n}\n\n.item-icon, .item-label, .item-dropdown-icon {\n  transition: inherit;\n}\n\n.item-icon {\n  color: var(--sidenav-item-icon-color);\n  font-size: var(--sidenav-item-icon-size);\n  height: var(--sidenav-item-icon-size);\n  -webkit-margin-end: var(--sidenav-item-icon-gap);\n          margin-inline-end: var(--sidenav-item-icon-gap);\n  width: var(--sidenav-item-icon-size);\n}\n\n.item-label {\n  flex: 1;\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n}\n\n.item-badge {\n  border-radius: 9999px;\n  font-size: 11px;\n  line-height: 20px;\n  -webkit-margin-start: var(--padding-8);\n          margin-inline-start: var(--padding-8);\n  padding: 0 7px;\n  text-align: center;\n}\n\n.item-dropdown-icon {\n  color: var(--sidenav-item-icon-color);\n  font-size: 18px;\n  height: 18px;\n  line-height: 18px;\n  -webkit-margin-start: var(--padding-8);\n          margin-inline-start: var(--padding-8);\n  transform: rotate(0deg) !important;\n  width: 18px;\n}\n\n.item-dropdown {\n  overflow: hidden;\n}\n\n.subheading {\n  box-sizing: border-box;\n  color: var(--sidenav-item-color);\n  font: var(--font-caption);\n  margin-top: var(--padding);\n  padding: var(--padding-12) var(--padding);\n  text-transform: uppercase;\n  white-space: nowrap;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uL3NpZGVuYXYtaXRlbS5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLG1CQUFBO0VBQ0Esc0JBQUE7RUFDQSxnQ0FBQTtFQUNBLGVBQUE7RUFDQSxhQUFBO0VBQ0EsbUJBQUE7RUFDQSxnQkFBQTtFQUNBLHFEQUFBO0VBQ0Esa0JBQUE7RUFDQSxxQkFBQTtFQUNBLGlDQUFBO0VBQ0EseUJBQUE7S0FBQSxzQkFBQTtVQUFBLGlCQUFBO0VBQ0EsV0FBQTtBQUNGOztBQUVBO0VBQ0UsaURBQUE7QUFDRjs7QUFFQTtFQUNFLDRDQUFBO0FBQ0Y7O0FBRUE7RUFDRSx1Q0FBQTtBQUNGOztBQUVBO0VBQ0UsdUNBQUE7QUFDRjs7QUFFQTtFQUNFLG1DQUFBO0FBQ0Y7O0FBRUE7RUFDRSxtREFBQTtFQUNBLGdLQUFBO1VBQUEsK0pBQUE7QUFDRjs7QUFFQTtFQUNFLHlEQUFBO0FBQ0Y7O0FBRUE7RUFDRSxtREFBQTtFQUNBLGdLQUFBO1VBQUEsK0pBQUE7QUFDRjs7QUFFQTtFQUNFLHlEQUFBO0FBQ0Y7O0FBRUE7RUFDRSxtREFBQTtFQUNBLGdLQUFBO1VBQUEsK0pBQUE7QUFDRjs7QUFFQTtFQUNFLHlEQUFBO0FBQ0Y7O0FBRUE7RUFDRSxtREFBQTtFQUNBLGdLQUFBO1VBQUEsK0pBQUE7QUFDRjs7QUFFQTtFQUNFLHlEQUFBO0FBQ0Y7O0FBRUE7RUFDRSxtREFBQTtFQUNBLGdLQUFBO1VBQUEsK0pBQUE7QUFDRjs7QUFFQTtFQUNFLHlEQUFBO0FBQ0Y7O0FBRUE7RUFDRSxtREFBQTtFQUNBLGdLQUFBO1VBQUEsK0pBQUE7QUFDRjs7QUFFQTtFQUNFLHlEQUFBO0FBQ0Y7O0FBRUE7RUFDRSxtQkFBQTtBQUNGOztBQUVBO0VBQ0UscUNBQUE7RUFDQSx3Q0FBQTtFQUNBLHFDQUFBO0VBQ0EsZ0RBQUE7VUFBQSwrQ0FBQTtFQUNBLG9DQUFBO0FBQ0Y7O0FBRUE7RUFDRSxPQUFBO0VBQ0EsbUJBQUE7RUFDQSxnQkFBQTtFQUNBLHVCQUFBO0FBQ0Y7O0FBRUE7RUFDRSxxQkFBQTtFQUNBLGVBQUE7RUFDQSxpQkFBQTtFQUNBLHNDQUFBO1VBQUEscUNBQUE7RUFDQSxjQUFBO0VBQ0Esa0JBQUE7QUFDRjs7QUFFQTtFQUNFLHFDQUFBO0VBQ0EsZUFBQTtFQUNBLFlBQUE7RUFDQSxpQkFBQTtFQUNBLHNDQUFBO1VBQUEscUNBQUE7RUFDQSxrQ0FBQTtFQUNBLFdBQUE7QUFDRjs7QUFFQTtFQUNFLGdCQUFBO0FBQ0Y7O0FBRUE7RUFDRSxzQkFBQTtFQUNBLGdDQUFBO0VBQ0EseUJBQUE7RUFDQSwwQkFBQTtFQUNBLHlDQUFBO0VBQ0EseUJBQUE7RUFDQSxtQkFBQTtBQUNGIiwiZmlsZSI6InNpZGVuYXYtaXRlbS5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbIi5pdGVtIHtcbiAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbiAgYm94LXNpemluZzogYm9yZGVyLWJveDtcbiAgY29sb3I6IHZhcigtLXNpZGVuYXYtaXRlbS1jb2xvcik7XG4gIGN1cnNvcjogcG9pbnRlcjtcbiAgZGlzcGxheTogZmxleDtcbiAgZmxleC1kaXJlY3Rpb246IHJvdztcbiAgbWluLWhlaWdodDogNDhweDtcbiAgcGFkZGluZzogdmFyKC0tcGFkZGluZy04KSB2YXIoLS1zaWRlbmF2LWl0ZW0tcGFkZGluZyk7XG4gIHBvc2l0aW9uOiByZWxhdGl2ZTtcbiAgdGV4dC1kZWNvcmF0aW9uOiBub25lO1xuICB0cmFuc2l0aW9uOiB2YXIoLS10cmFucy1lYXNlLW91dCk7XG4gIHVzZXItc2VsZWN0OiBub25lO1xuICB3aWR0aDogMTAwJTtcbn1cblxuLml0ZW06aG92ZXIsIC5pdGVtLmFjdGl2ZSB7XG4gIGJhY2tncm91bmQ6IHZhcigtLXNpZGVuYXYtaXRlbS1iYWNrZ3JvdW5kLWFjdGl2ZSk7XG59XG5cbi5pdGVtOmhvdmVyIC5pdGVtLWljb24sIC5pdGVtLmFjdGl2ZSAuaXRlbS1pY29uIHtcbiAgY29sb3I6IHZhcigtLXNpZGVuYXYtaXRlbS1pY29uLWNvbG9yLWFjdGl2ZSk7XG59XG5cbi5pdGVtOmhvdmVyIC5pdGVtLWxhYmVsLCAuaXRlbS5hY3RpdmUgLml0ZW0tbGFiZWwge1xuICBjb2xvcjogdmFyKC0tc2lkZW5hdi1pdGVtLWNvbG9yLWFjdGl2ZSk7XG59XG5cbi5pdGVtOmhvdmVyIC5pdGVtLWRyb3Bkb3duLWljb24sIC5pdGVtLmFjdGl2ZSAuaXRlbS1kcm9wZG93bi1pY29uIHtcbiAgY29sb3I6IHZhcigtLXNpZGVuYXYtaXRlbS1jb2xvci1hY3RpdmUpO1xufVxuXG4uaXRlbS5vcGVuIC5pdGVtLWRyb3Bkb3duLWljb24ge1xuICB0cmFuc2Zvcm06IHJvdGF0ZSg5MGRlZykgIWltcG9ydGFudDtcbn1cblxuOmhvc3QoLml0ZW0tbGV2ZWwtMSkgLml0ZW0ge1xuICBiYWNrZ3JvdW5kOiB2YXIoLS1zaWRlbmF2LWl0ZW0tZHJvcGRvd24tYmFja2dyb3VuZCk7XG4gIHBhZGRpbmctaW5saW5lLXN0YXJ0OiBjYWxjKHZhcigtLXNpZGVuYXYtaXRlbS1pY29uLXNpemUpICsgdmFyKC0tc2lkZW5hdi1pdGVtLWljb24tZ2FwKSArIHZhcigtLXNpZGVuYXYtaXRlbS1wYWRkaW5nKSArICh2YXIoLS1zaWRlbmF2LWl0ZW0tZHJvcGRvd24tZ2FwKSAqIDApKTtcbn1cblxuOmhvc3QoLml0ZW0tbGV2ZWwtMSkgLml0ZW06aG92ZXIge1xuICBiYWNrZ3JvdW5kOiB2YXIoLS1zaWRlbmF2LWl0ZW0tZHJvcGRvd24tYmFja2dyb3VuZC1ob3Zlcik7XG59XG5cbjpob3N0KC5pdGVtLWxldmVsLTIpIC5pdGVtIHtcbiAgYmFja2dyb3VuZDogdmFyKC0tc2lkZW5hdi1pdGVtLWRyb3Bkb3duLWJhY2tncm91bmQpO1xuICBwYWRkaW5nLWlubGluZS1zdGFydDogY2FsYyh2YXIoLS1zaWRlbmF2LWl0ZW0taWNvbi1zaXplKSArIHZhcigtLXNpZGVuYXYtaXRlbS1pY29uLWdhcCkgKyB2YXIoLS1zaWRlbmF2LWl0ZW0tcGFkZGluZykgKyAodmFyKC0tc2lkZW5hdi1pdGVtLWRyb3Bkb3duLWdhcCkgKiAxKSk7XG59XG5cbjpob3N0KC5pdGVtLWxldmVsLTIpIC5pdGVtOmhvdmVyIHtcbiAgYmFja2dyb3VuZDogdmFyKC0tc2lkZW5hdi1pdGVtLWRyb3Bkb3duLWJhY2tncm91bmQtaG92ZXIpO1xufVxuXG46aG9zdCguaXRlbS1sZXZlbC0zKSAuaXRlbSB7XG4gIGJhY2tncm91bmQ6IHZhcigtLXNpZGVuYXYtaXRlbS1kcm9wZG93bi1iYWNrZ3JvdW5kKTtcbiAgcGFkZGluZy1pbmxpbmUtc3RhcnQ6IGNhbGModmFyKC0tc2lkZW5hdi1pdGVtLWljb24tc2l6ZSkgKyB2YXIoLS1zaWRlbmF2LWl0ZW0taWNvbi1nYXApICsgdmFyKC0tc2lkZW5hdi1pdGVtLXBhZGRpbmcpICsgKHZhcigtLXNpZGVuYXYtaXRlbS1kcm9wZG93bi1nYXApICogMikpO1xufVxuXG46aG9zdCguaXRlbS1sZXZlbC0zKSAuaXRlbTpob3ZlciB7XG4gIGJhY2tncm91bmQ6IHZhcigtLXNpZGVuYXYtaXRlbS1kcm9wZG93bi1iYWNrZ3JvdW5kLWhvdmVyKTtcbn1cblxuOmhvc3QoLml0ZW0tbGV2ZWwtNCkgLml0ZW0ge1xuICBiYWNrZ3JvdW5kOiB2YXIoLS1zaWRlbmF2LWl0ZW0tZHJvcGRvd24tYmFja2dyb3VuZCk7XG4gIHBhZGRpbmctaW5saW5lLXN0YXJ0OiBjYWxjKHZhcigtLXNpZGVuYXYtaXRlbS1pY29uLXNpemUpICsgdmFyKC0tc2lkZW5hdi1pdGVtLWljb24tZ2FwKSArIHZhcigtLXNpZGVuYXYtaXRlbS1wYWRkaW5nKSArICh2YXIoLS1zaWRlbmF2LWl0ZW0tZHJvcGRvd24tZ2FwKSAqIDMpKTtcbn1cblxuOmhvc3QoLml0ZW0tbGV2ZWwtNCkgLml0ZW06aG92ZXIge1xuICBiYWNrZ3JvdW5kOiB2YXIoLS1zaWRlbmF2LWl0ZW0tZHJvcGRvd24tYmFja2dyb3VuZC1ob3Zlcik7XG59XG5cbjpob3N0KC5pdGVtLWxldmVsLTUpIC5pdGVtIHtcbiAgYmFja2dyb3VuZDogdmFyKC0tc2lkZW5hdi1pdGVtLWRyb3Bkb3duLWJhY2tncm91bmQpO1xuICBwYWRkaW5nLWlubGluZS1zdGFydDogY2FsYyh2YXIoLS1zaWRlbmF2LWl0ZW0taWNvbi1zaXplKSArIHZhcigtLXNpZGVuYXYtaXRlbS1pY29uLWdhcCkgKyB2YXIoLS1zaWRlbmF2LWl0ZW0tcGFkZGluZykgKyAodmFyKC0tc2lkZW5hdi1pdGVtLWRyb3Bkb3duLWdhcCkgKiA0KSk7XG59XG5cbjpob3N0KC5pdGVtLWxldmVsLTUpIC5pdGVtOmhvdmVyIHtcbiAgYmFja2dyb3VuZDogdmFyKC0tc2lkZW5hdi1pdGVtLWRyb3Bkb3duLWJhY2tncm91bmQtaG92ZXIpO1xufVxuXG46aG9zdCguaXRlbS1sZXZlbC02KSAuaXRlbSB7XG4gIGJhY2tncm91bmQ6IHZhcigtLXNpZGVuYXYtaXRlbS1kcm9wZG93bi1iYWNrZ3JvdW5kKTtcbiAgcGFkZGluZy1pbmxpbmUtc3RhcnQ6IGNhbGModmFyKC0tc2lkZW5hdi1pdGVtLWljb24tc2l6ZSkgKyB2YXIoLS1zaWRlbmF2LWl0ZW0taWNvbi1nYXApICsgdmFyKC0tc2lkZW5hdi1pdGVtLXBhZGRpbmcpICsgKHZhcigtLXNpZGVuYXYtaXRlbS1kcm9wZG93bi1nYXApICogNSkpO1xufVxuXG46aG9zdCguaXRlbS1sZXZlbC02KSAuaXRlbTpob3ZlciB7XG4gIGJhY2tncm91bmQ6IHZhcigtLXNpZGVuYXYtaXRlbS1kcm9wZG93bi1iYWNrZ3JvdW5kLWhvdmVyKTtcbn1cblxuLml0ZW0taWNvbiwgLml0ZW0tbGFiZWwsIC5pdGVtLWRyb3Bkb3duLWljb24ge1xuICB0cmFuc2l0aW9uOiBpbmhlcml0O1xufVxuXG4uaXRlbS1pY29uIHtcbiAgY29sb3I6IHZhcigtLXNpZGVuYXYtaXRlbS1pY29uLWNvbG9yKTtcbiAgZm9udC1zaXplOiB2YXIoLS1zaWRlbmF2LWl0ZW0taWNvbi1zaXplKTtcbiAgaGVpZ2h0OiB2YXIoLS1zaWRlbmF2LWl0ZW0taWNvbi1zaXplKTtcbiAgbWFyZ2luLWlubGluZS1lbmQ6IHZhcigtLXNpZGVuYXYtaXRlbS1pY29uLWdhcCk7XG4gIHdpZHRoOiB2YXIoLS1zaWRlbmF2LWl0ZW0taWNvbi1zaXplKTtcbn1cblxuLml0ZW0tbGFiZWwge1xuICBmbGV4OiAxO1xuICB3aGl0ZS1zcGFjZTogbm93cmFwO1xuICBvdmVyZmxvdzogaGlkZGVuO1xuICB0ZXh0LW92ZXJmbG93OiBlbGxpcHNpcztcbn1cblxuLml0ZW0tYmFkZ2Uge1xuICBib3JkZXItcmFkaXVzOiA5OTk5cHg7XG4gIGZvbnQtc2l6ZTogMTFweDtcbiAgbGluZS1oZWlnaHQ6IDIwcHg7XG4gIG1hcmdpbi1pbmxpbmUtc3RhcnQ6IHZhcigtLXBhZGRpbmctOCk7XG4gIHBhZGRpbmc6IDAgN3B4O1xuICB0ZXh0LWFsaWduOiBjZW50ZXI7XG59XG5cbi5pdGVtLWRyb3Bkb3duLWljb24ge1xuICBjb2xvcjogdmFyKC0tc2lkZW5hdi1pdGVtLWljb24tY29sb3IpO1xuICBmb250LXNpemU6IDE4cHg7XG4gIGhlaWdodDogMThweDtcbiAgbGluZS1oZWlnaHQ6IDE4cHg7XG4gIG1hcmdpbi1pbmxpbmUtc3RhcnQ6IHZhcigtLXBhZGRpbmctOCk7XG4gIHRyYW5zZm9ybTogcm90YXRlKDBkZWcpICFpbXBvcnRhbnQ7XG4gIHdpZHRoOiAxOHB4O1xufVxuXG4uaXRlbS1kcm9wZG93biB7XG4gIG92ZXJmbG93OiBoaWRkZW47XG59XG5cbi5zdWJoZWFkaW5nIHtcbiAgYm94LXNpemluZzogYm9yZGVyLWJveDtcbiAgY29sb3I6IHZhcigtLXNpZGVuYXYtaXRlbS1jb2xvcik7XG4gIGZvbnQ6IHZhcigtLWZvbnQtY2FwdGlvbik7XG4gIG1hcmdpbi10b3A6IHZhcigtLXBhZGRpbmcpO1xuICBwYWRkaW5nOiB2YXIoLS1wYWRkaW5nLTEyKSB2YXIoLS1wYWRkaW5nKTtcbiAgdGV4dC10cmFuc2Zvcm06IHVwcGVyY2FzZTtcbiAgd2hpdGUtc3BhY2U6IG5vd3JhcDtcbn0iXX0= */");

/***/ }),

/***/ "CZ7+":
/*!******************************************************************************************************************************!*\
  !*** ./src/app/layout/components/toolbar/components/toolbar-user/toolbar-user-dropdown/toolbar-user-dropdown.component.scss ***!
  \******************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (".dropdown {\n  background: var(--background-card);\n  border-bottom-left-radius: var(--border-radius);\n  border-bottom-right-radius: var(--border-radius);\n  box-shadow: var(--elevation-z4);\n  max-width: 100vw;\n  overflow: hidden;\n  width: 350px;\n  border-radius: 0.25rem;\n}\n\n.dropdown-header {\n  --bg-opacity: 1;\n  background-color: #5c77ff;\n  background-color: rgba(92, 119, 255, var(--bg-opacity));\n  --text-opacity: 1;\n  color: #FFF;\n  color: rgba(255, 255, 255, var(--text-opacity));\n  padding-top: 1rem;\n  padding-bottom: 1rem;\n  padding-right: 1rem;\n  padding-left: 0.75rem;\n  box-shadow: var(--elevation-z6);\n}\n\n.dropdown-heading-icon {\n  background: rgba(255, 255, 255, 0.2);\n  border-radius: 999999px;\n  margin-right: var(--padding-12);\n  padding: var(--padding-8);\n}\n\n.dropdown-heading-icon .mat-icon {\n  font-size: 32px;\n  height: 32px;\n  width: 32px;\n}\n\n.dropdown-heading {\n  font: var(--font-title);\n}\n\n.dropdown-content {\n  max-height: 300px;\n  overflow-x: hidden;\n  overflow-y: auto;\n}\n\n.dropdown-footer {\n  background: var(--background-app-bar);\n  border-top: 1px solid var(--foreground-divider);\n  padding: var(--padding-8) var(--padding-12);\n}\n\n.dropdown-footer-select {\n  padding-left: var(--padding-12);\n}\n\n.dropdown-footer-select .mat-icon:not(.dropdown-footer-select-caret) {\n  margin-right: var(--padding-8);\n  vertical-align: -7px !important;\n}\n\n.dropdown-footer-select-caret {\n  color: var(--text-hint);\n  font-size: 18px;\n  height: 18px;\n  vertical-align: -4px !important;\n  width: 18px;\n}\n\n.notification {\n  color: var(--text-color);\n  padding: var(--padding-16) var(--padding);\n  position: relative;\n  text-decoration: none;\n  transition: var(--trans-ease-out);\n  -webkit-user-select: none;\n     -moz-user-select: none;\n          user-select: none;\n}\n\n.notification:hover {\n  background: var(--background-hover);\n}\n\n.notification:hover .notification-label {\n  --text-opacity: 1;\n  color: #5c77ff;\n  color: rgba(92, 119, 255, var(--text-opacity));\n}\n\n.notification.read {\n  opacity: 0.5;\n}\n\n.notification-icon {\n  margin-right: var(--padding);\n}\n\n.notification-label {\n  transition: inherit;\n}\n\n.notification-description {\n  color: var(--text-secondary);\n  font: var(--font-caption);\n}\n\n.notification-chevron {\n  color: var(--text-hint);\n  font-size: 18px;\n  height: 18px;\n  width: 18px;\n}\n\n.notification + .notification {\n  border-top: 1px solid var(--foreground-divider);\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uLy4uLy4uLy4uL3Rvb2xiYXItdXNlci1kcm9wZG93bi5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLGtDQUFBO0VBQ0EsK0NBQUE7RUFDQSxnREFBQTtFQUNBLCtCQUFBO0VBQ0EsZ0JBQUE7RUFDQSxnQkFBQTtFQUNBLFlBQUE7RUFDQSxzQkFBQTtBQUNGOztBQUVBO0VBQ0UsZUFBQTtFQUNBLHlCQUFBO0VBQ0EsdURBQUE7RUFDQSxpQkFBQTtFQUNBLFdBQUE7RUFDQSwrQ0FBQTtFQUNBLGlCQUFBO0VBQ0Esb0JBQUE7RUFDQSxtQkFBQTtFQUNBLHFCQUFBO0VBQ0EsK0JBQUE7QUFDRjs7QUFFQTtFQUNFLG9DQUFBO0VBQ0EsdUJBQUE7RUFDQSwrQkFBQTtFQUNBLHlCQUFBO0FBQ0Y7O0FBRUE7RUFDRSxlQUFBO0VBQ0EsWUFBQTtFQUNBLFdBQUE7QUFDRjs7QUFFQTtFQUNFLHVCQUFBO0FBQ0Y7O0FBRUE7RUFDRSxpQkFBQTtFQUNBLGtCQUFBO0VBQ0EsZ0JBQUE7QUFDRjs7QUFFQTtFQUNFLHFDQUFBO0VBQ0EsK0NBQUE7RUFDQSwyQ0FBQTtBQUNGOztBQUVBO0VBQ0UsK0JBQUE7QUFDRjs7QUFFQTtFQUNFLDhCQUFBO0VBQ0EsK0JBQUE7QUFDRjs7QUFFQTtFQUNFLHVCQUFBO0VBQ0EsZUFBQTtFQUNBLFlBQUE7RUFDQSwrQkFBQTtFQUNBLFdBQUE7QUFDRjs7QUFFQTtFQUNFLHdCQUFBO0VBQ0EseUNBQUE7RUFDQSxrQkFBQTtFQUNBLHFCQUFBO0VBQ0EsaUNBQUE7RUFDQSx5QkFBQTtLQUFBLHNCQUFBO1VBQUEsaUJBQUE7QUFDRjs7QUFFQTtFQUNFLG1DQUFBO0FBQ0Y7O0FBRUE7RUFDRSxpQkFBQTtFQUNBLGNBQUE7RUFDQSw4Q0FBQTtBQUNGOztBQUVBO0VBQ0UsWUFBQTtBQUNGOztBQUVBO0VBQ0UsNEJBQUE7QUFDRjs7QUFFQTtFQUNFLG1CQUFBO0FBQ0Y7O0FBRUE7RUFDRSw0QkFBQTtFQUNBLHlCQUFBO0FBQ0Y7O0FBRUE7RUFDRSx1QkFBQTtFQUNBLGVBQUE7RUFDQSxZQUFBO0VBQ0EsV0FBQTtBQUNGOztBQUVBO0VBQ0UsK0NBQUE7QUFDRiIsImZpbGUiOiJ0b29sYmFyLXVzZXItZHJvcGRvd24uY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyIuZHJvcGRvd24ge1xuICBiYWNrZ3JvdW5kOiB2YXIoLS1iYWNrZ3JvdW5kLWNhcmQpO1xuICBib3JkZXItYm90dG9tLWxlZnQtcmFkaXVzOiB2YXIoLS1ib3JkZXItcmFkaXVzKTtcbiAgYm9yZGVyLWJvdHRvbS1yaWdodC1yYWRpdXM6IHZhcigtLWJvcmRlci1yYWRpdXMpO1xuICBib3gtc2hhZG93OiB2YXIoLS1lbGV2YXRpb24tejQpO1xuICBtYXgtd2lkdGg6IDEwMHZ3O1xuICBvdmVyZmxvdzogaGlkZGVuO1xuICB3aWR0aDogMzUwcHg7XG4gIGJvcmRlci1yYWRpdXM6IDAuMjVyZW07XG59XG5cbi5kcm9wZG93bi1oZWFkZXIge1xuICAtLWJnLW9wYWNpdHk6IDE7XG4gIGJhY2tncm91bmQtY29sb3I6ICM1Yzc3ZmY7XG4gIGJhY2tncm91bmQtY29sb3I6IHJnYmEoOTIsIDExOSwgMjU1LCB2YXIoLS1iZy1vcGFjaXR5KSk7XG4gIC0tdGV4dC1vcGFjaXR5OiAxO1xuICBjb2xvcjogI0ZGRjtcbiAgY29sb3I6IHJnYmEoMjU1LCAyNTUsIDI1NSwgdmFyKC0tdGV4dC1vcGFjaXR5KSk7XG4gIHBhZGRpbmctdG9wOiAxcmVtO1xuICBwYWRkaW5nLWJvdHRvbTogMXJlbTtcbiAgcGFkZGluZy1yaWdodDogMXJlbTtcbiAgcGFkZGluZy1sZWZ0OiAwLjc1cmVtO1xuICBib3gtc2hhZG93OiB2YXIoLS1lbGV2YXRpb24tejYpO1xufVxuXG4uZHJvcGRvd24taGVhZGluZy1pY29uIHtcbiAgYmFja2dyb3VuZDogcmdiYSgyNTUsIDI1NSwgMjU1LCAwLjIpO1xuICBib3JkZXItcmFkaXVzOiA5OTk5OTlweDtcbiAgbWFyZ2luLXJpZ2h0OiB2YXIoLS1wYWRkaW5nLTEyKTtcbiAgcGFkZGluZzogdmFyKC0tcGFkZGluZy04KTtcbn1cblxuLmRyb3Bkb3duLWhlYWRpbmctaWNvbiAubWF0LWljb24ge1xuICBmb250LXNpemU6IDMycHg7XG4gIGhlaWdodDogMzJweDtcbiAgd2lkdGg6IDMycHg7XG59XG5cbi5kcm9wZG93bi1oZWFkaW5nIHtcbiAgZm9udDogdmFyKC0tZm9udC10aXRsZSk7XG59XG5cbi5kcm9wZG93bi1jb250ZW50IHtcbiAgbWF4LWhlaWdodDogMzAwcHg7XG4gIG92ZXJmbG93LXg6IGhpZGRlbjtcbiAgb3ZlcmZsb3cteTogYXV0bztcbn1cblxuLmRyb3Bkb3duLWZvb3RlciB7XG4gIGJhY2tncm91bmQ6IHZhcigtLWJhY2tncm91bmQtYXBwLWJhcik7XG4gIGJvcmRlci10b3A6IDFweCBzb2xpZCB2YXIoLS1mb3JlZ3JvdW5kLWRpdmlkZXIpO1xuICBwYWRkaW5nOiB2YXIoLS1wYWRkaW5nLTgpIHZhcigtLXBhZGRpbmctMTIpO1xufVxuXG4uZHJvcGRvd24tZm9vdGVyLXNlbGVjdCB7XG4gIHBhZGRpbmctbGVmdDogdmFyKC0tcGFkZGluZy0xMik7XG59XG5cbi5kcm9wZG93bi1mb290ZXItc2VsZWN0IC5tYXQtaWNvbjpub3QoLmRyb3Bkb3duLWZvb3Rlci1zZWxlY3QtY2FyZXQpIHtcbiAgbWFyZ2luLXJpZ2h0OiB2YXIoLS1wYWRkaW5nLTgpO1xuICB2ZXJ0aWNhbC1hbGlnbjogLTdweCAhaW1wb3J0YW50O1xufVxuXG4uZHJvcGRvd24tZm9vdGVyLXNlbGVjdC1jYXJldCB7XG4gIGNvbG9yOiB2YXIoLS10ZXh0LWhpbnQpO1xuICBmb250LXNpemU6IDE4cHg7XG4gIGhlaWdodDogMThweDtcbiAgdmVydGljYWwtYWxpZ246IC00cHggIWltcG9ydGFudDtcbiAgd2lkdGg6IDE4cHg7XG59XG5cbi5ub3RpZmljYXRpb24ge1xuICBjb2xvcjogdmFyKC0tdGV4dC1jb2xvcik7XG4gIHBhZGRpbmc6IHZhcigtLXBhZGRpbmctMTYpIHZhcigtLXBhZGRpbmcpO1xuICBwb3NpdGlvbjogcmVsYXRpdmU7XG4gIHRleHQtZGVjb3JhdGlvbjogbm9uZTtcbiAgdHJhbnNpdGlvbjogdmFyKC0tdHJhbnMtZWFzZS1vdXQpO1xuICB1c2VyLXNlbGVjdDogbm9uZTtcbn1cblxuLm5vdGlmaWNhdGlvbjpob3ZlciB7XG4gIGJhY2tncm91bmQ6IHZhcigtLWJhY2tncm91bmQtaG92ZXIpO1xufVxuXG4ubm90aWZpY2F0aW9uOmhvdmVyIC5ub3RpZmljYXRpb24tbGFiZWwge1xuICAtLXRleHQtb3BhY2l0eTogMTtcbiAgY29sb3I6ICM1Yzc3ZmY7XG4gIGNvbG9yOiByZ2JhKDkyLCAxMTksIDI1NSwgdmFyKC0tdGV4dC1vcGFjaXR5KSk7XG59XG5cbi5ub3RpZmljYXRpb24ucmVhZCB7XG4gIG9wYWNpdHk6IDAuNTtcbn1cblxuLm5vdGlmaWNhdGlvbi1pY29uIHtcbiAgbWFyZ2luLXJpZ2h0OiB2YXIoLS1wYWRkaW5nKTtcbn1cblxuLm5vdGlmaWNhdGlvbi1sYWJlbCB7XG4gIHRyYW5zaXRpb246IGluaGVyaXQ7XG59XG5cbi5ub3RpZmljYXRpb24tZGVzY3JpcHRpb24ge1xuICBjb2xvcjogdmFyKC0tdGV4dC1zZWNvbmRhcnkpO1xuICBmb250OiB2YXIoLS1mb250LWNhcHRpb24pO1xufVxuXG4ubm90aWZpY2F0aW9uLWNoZXZyb24ge1xuICBjb2xvcjogdmFyKC0tdGV4dC1oaW50KTtcbiAgZm9udC1zaXplOiAxOHB4O1xuICBoZWlnaHQ6IDE4cHg7XG4gIHdpZHRoOiAxOHB4O1xufVxuXG4ubm90aWZpY2F0aW9uICsgLm5vdGlmaWNhdGlvbiB7XG4gIGJvcmRlci10b3A6IDFweCBzb2xpZCB2YXIoLS1mb3JlZ3JvdW5kLWRpdmlkZXIpO1xufSJdfQ== */");

/***/ }),

/***/ "Chvm":
/*!***************************************************!*\
  !*** ./src/@vex/pipes/color/color-fade.module.ts ***!
  \***************************************************/
/*! exports provided: ColorFadeModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ColorFadeModule", function() { return ColorFadeModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _color_fade_pipe__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./color-fade.pipe */ "A4cF");




let ColorFadeModule = class ColorFadeModule {
};
ColorFadeModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_color_fade_pipe__WEBPACK_IMPORTED_MODULE_3__["ColorFadePipe"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"]
        ],
        exports: [_color_fade_pipe__WEBPACK_IMPORTED_MODULE_3__["ColorFadePipe"]]
    })
], ColorFadeModule);



/***/ }),

/***/ "Cq9o":
/*!************************************************************!*\
  !*** ./src/app/core/http/path-segment-resource.service.ts ***!
  \************************************************************/
/*! exports provided: PathSegmentResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PathSegmentResource", function() { return PathSegmentResource; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _rest_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rest-api.service */ "iCaw");



let PathSegmentResource = class PathSegmentResource {
    constructor(restApi) {
        this.restApi = restApi;
        this.REQUEST_ENDPOINT = 'requests';
        this.ENDPOINT = 'path_segments';
    }
    index(requestId, queryParams) {
        return this.restApi.index([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT], queryParams);
    }
    show(requestId, id, queryParams) {
        return this.restApi.show([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT, id], queryParams);
    }
    create(requestId, body) {
        return this.restApi.create([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT], body);
    }
    update(requestId, id, body) {
        return this.restApi.update([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT, id], body);
    }
    destroy(requestId, id, queryParams) {
        return this.restApi.destroy([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT, id], queryParams);
    }
};
PathSegmentResource.ctorParameters = () => [
    { type: _rest_api_service__WEBPACK_IMPORTED_MODULE_2__["RestApiService"] }
];
PathSegmentResource = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], PathSegmentResource);



/***/ }),

/***/ "CtTw":
/*!*********************************************!*\
  !*** ./src/@vex/services/layout.service.ts ***!
  \*********************************************/
/*! exports provided: LayoutService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LayoutService", function() { return LayoutService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs */ "qCKp");




let LayoutService = class LayoutService {
    constructor(router) {
        this.router = router;
        this._quickpanelOpenSubject = new rxjs__WEBPACK_IMPORTED_MODULE_3__["BehaviorSubject"](false);
        this.quickpanelOpen$ = this._quickpanelOpenSubject.asObservable();
        this._sidenavOpenSubject = new rxjs__WEBPACK_IMPORTED_MODULE_3__["BehaviorSubject"](false);
        this.sidenavOpen$ = this._sidenavOpenSubject.asObservable();
        // Controls whether sidenav is expanded false = expanded
        this._sidenavCollapsedSubject = new rxjs__WEBPACK_IMPORTED_MODULE_3__["BehaviorSubject"](true);
        this.sidenavCollapsed$ = this._sidenavCollapsedSubject.asObservable();
        // Controls whether sidenav is overlayed true = expanded
        this._sidenavCollapsedOpenSubject = new rxjs__WEBPACK_IMPORTED_MODULE_3__["BehaviorSubject"](false);
        this.sidenavCollapsedOpen$ = this._sidenavCollapsedOpenSubject.asObservable();
        this._configpanelOpenSubject = new rxjs__WEBPACK_IMPORTED_MODULE_3__["BehaviorSubject"](false);
        this.configpanelOpen$ = this._configpanelOpenSubject.asObservable();
        this._searchOpen = new rxjs__WEBPACK_IMPORTED_MODULE_3__["BehaviorSubject"](false);
        this.searchOpen$ = this._searchOpen.asObservable();
        this.sidenavOpen$.subscribe(e => {
            console.log('sidenavOpen');
            console.log(e);
        });
        this.sidenavCollapsed$.subscribe(e => {
            console.log('sidenavCollapsed');
            console.log(e);
        });
        this.sidenavCollapsedOpen$.subscribe(e => {
            console.log('sidenavCollapsedOpen');
            console.log(e);
        });
    }
    openQuickpanel() {
        this._quickpanelOpenSubject.next(true);
    }
    closeQuickpanel() {
        this._quickpanelOpenSubject.next(false);
    }
    openSidenav() {
        console.log('openSidenav');
        this._sidenavOpenSubject.next(true);
    }
    closeSidenav() {
        console.log('closeSidenav');
        this._sidenavOpenSubject.next(false);
    }
    collapseSidenav() {
        console.log('collapseSidenav');
        this._sidenavCollapsedSubject.next(true);
    }
    expandSidenav() {
        console.log('expandSidenav');
        this._sidenavCollapsedSubject.next(false);
    }
    // Shows sidenav as overlay
    collapseOpenSidenav() {
        console.log('collapseOpenSidenav');
        this._sidenavCollapsedOpenSubject.next(true);
    }
    // Hides sidenav as overlay
    collapseCloseSidenav() {
        console.log('collapseCloseSidenav');
        this._sidenavCollapsedOpenSubject.next(false);
    }
    openConfigpanel() {
        this._configpanelOpenSubject.next(true);
    }
    closeConfigpanel() {
        this._configpanelOpenSubject.next(false);
    }
    openSearch() {
        this._searchOpen.next(true);
    }
    closeSearch() {
        this._searchOpen.next(false);
    }
    enableRTL() {
        this.router.navigate([], {
            queryParams: {
                rtl: 'true'
            }
        }).then(() => {
            if (window) {
                window.location.reload();
            }
        });
    }
    disableRTL() {
        this.router.navigate([], {
            queryParams: {
                rtl: 'false'
            }
        }).then(() => {
            if (window) {
                window.location.reload();
            }
        });
    }
};
LayoutService.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] }
];
LayoutService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], LayoutService);



/***/ }),

/***/ "D1/4":
/*!****************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/@vex/components/toolbar-search/toolbar-search.component.html ***!
  \****************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div fxLayout=\"row\" fxLayoutAlign=\"start center\">\n  <button (click)=\"open()\" mat-icon-button>\n    <mat-icon [icIcon]=\"icSearch\"></mat-icon>\n  </button>\n  <mat-form-field [class.search-open]=\"isOpen\" appearance=\"outline\" class=\"search\" fxFlex=\"auto\">\n    <mat-label>Search&hellip;</mat-label>\n    <input #input (blur)=\"close()\" matInput>\n  </mat-form-field>\n</div>\n");

/***/ }),

/***/ "D9MS":
/*!**********************************************!*\
  !*** ./src/app/data/schema/projects-user.ts ***!
  \**********************************************/
/*! exports provided: ProjectsUser, ProjectsUserRoles, ProjectsUserRoleTitles */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectsUser", function() { return ProjectsUser; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectsUserRoles", function() { return ProjectsUserRoles; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectsUserRoleTitles", function() { return ProjectsUserRoleTitles; });
class ProjectsUser {
    constructor(projectsUser) {
        this.id = projectsUser.id;
        this.name = projectsUser.name;
        this.email = projectsUser.email;
        this.role = projectsUser.role;
    }
}
var ProjectsUserRoles;
(function (ProjectsUserRoles) {
    ProjectsUserRoles[ProjectsUserRoles["project_owner"] = 1] = "project_owner";
    ProjectsUserRoles[ProjectsUserRoles["project_admin"] = 2] = "project_admin";
    ProjectsUserRoles[ProjectsUserRoles["project_editor"] = 3] = "project_editor";
    ProjectsUserRoles[ProjectsUserRoles["project_viewer"] = 4] = "project_viewer";
})(ProjectsUserRoles || (ProjectsUserRoles = {}));
var ProjectsUserRoleTitles;
(function (ProjectsUserRoleTitles) {
    ProjectsUserRoleTitles[ProjectsUserRoleTitles["Owner"] = 1] = "Owner";
    ProjectsUserRoleTitles[ProjectsUserRoleTitles["Admin"] = 2] = "Admin";
    ProjectsUserRoleTitles[ProjectsUserRoleTitles["Editor"] = 3] = "Editor";
    ProjectsUserRoleTitles[ProjectsUserRoleTitles["Viewer"] = 4] = "Viewer";
})(ProjectsUserRoleTitles || (ProjectsUserRoleTitles = {}));


/***/ }),

/***/ "DdkG":
/*!**************************************************************************!*\
  !*** ./src/@vex/components/toolbar-search/toolbar-search.component.scss ***!
  \**************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (".mat-icon {\n  --text-opacity: 1;\n  color: #5c77ff;\n  color: rgba(92, 119, 255, var(--text-opacity));\n}\n\n.search {\n  margin-top: 22px;\n  opacity: 0;\n  overflow: hidden;\n  transition: var(--trans-ease-in-out);\n  visibility: hidden;\n  width: 0;\n}\n\n.search.search-open {\n  margin-left: var(--padding-8);\n  margin-right: var(--padding-8);\n  opacity: 1;\n  visibility: visible;\n  width: 250px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uL3Rvb2xiYXItc2VhcmNoLmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0VBQ0UsaUJBQUE7RUFDQSxjQUFBO0VBQ0EsOENBQUE7QUFDRjs7QUFFQTtFQUNFLGdCQUFBO0VBQ0EsVUFBQTtFQUNBLGdCQUFBO0VBQ0Esb0NBQUE7RUFDQSxrQkFBQTtFQUNBLFFBQUE7QUFDRjs7QUFFQTtFQUNFLDZCQUFBO0VBQ0EsOEJBQUE7RUFDQSxVQUFBO0VBQ0EsbUJBQUE7RUFDQSxZQUFBO0FBQ0YiLCJmaWxlIjoidG9vbGJhci1zZWFyY2guY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyIubWF0LWljb24ge1xuICAtLXRleHQtb3BhY2l0eTogMTtcbiAgY29sb3I6ICM1Yzc3ZmY7XG4gIGNvbG9yOiByZ2JhKDkyLCAxMTksIDI1NSwgdmFyKC0tdGV4dC1vcGFjaXR5KSk7XG59XG5cbi5zZWFyY2gge1xuICBtYXJnaW4tdG9wOiAyMnB4O1xuICBvcGFjaXR5OiAwO1xuICBvdmVyZmxvdzogaGlkZGVuO1xuICB0cmFuc2l0aW9uOiB2YXIoLS10cmFucy1lYXNlLWluLW91dCk7XG4gIHZpc2liaWxpdHk6IGhpZGRlbjtcbiAgd2lkdGg6IDA7XG59XG5cbi5zZWFyY2guc2VhcmNoLW9wZW4ge1xuICBtYXJnaW4tbGVmdDogdmFyKC0tcGFkZGluZy04KTtcbiAgbWFyZ2luLXJpZ2h0OiB2YXIoLS1wYWRkaW5nLTgpO1xuICBvcGFjaXR5OiAxO1xuICB2aXNpYmlsaXR5OiB2aXNpYmxlO1xuICB3aWR0aDogMjUwcHg7XG59Il19 */");

/***/ }),

/***/ "EuI8":
/*!**************************************************!*\
  !*** ./src/@vex/interfaces/config-name.model.ts ***!
  \**************************************************/
/*! exports provided: ConfigName */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ConfigName", function() { return ConfigName; });
var ConfigName;
(function (ConfigName) {
    ConfigName["apollo"] = "vex-layout-apollo";
    ConfigName["zeus"] = "vex-layout-zeus";
    ConfigName["hermes"] = "vex-layout-hermes";
    ConfigName["poseidon"] = "vex-layout-poseidon";
    ConfigName["ares"] = "vex-layout-ares";
    ConfigName["ikaros"] = "vex-layout-ikaros";
})(ConfigName || (ConfigName = {}));


/***/ }),

/***/ "FKU7":
/*!************************************************************!*\
  !*** ./src/app/core/http/subscription-resource.service.ts ***!
  \************************************************************/
/*! exports provided: SubscriptionResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SubscriptionResource", function() { return SubscriptionResource; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _rest_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rest-api.service */ "iCaw");



let SubscriptionResource = class SubscriptionResource {
    constructor(restApi) {
        this.restApi = restApi;
        this.ENDPOINT = 'subscriptions';
    }
    index(queryParams) {
        return this.restApi.index([this.ENDPOINT], queryParams);
    }
    show(id, queryParams) {
        return this.restApi.show([this.ENDPOINT, id], queryParams);
    }
    create(body) {
        return this.restApi.create([this.ENDPOINT], body);
    }
    update(id, body) {
        return this.restApi.update([this.ENDPOINT, id], body);
    }
    destroy(id) {
        return this.restApi.destroy([this.ENDPOINT, id]);
    }
};
SubscriptionResource.ctorParameters = () => [
    { type: _rest_api_service__WEBPACK_IMPORTED_MODULE_2__["RestApiService"] }
];
SubscriptionResource = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], SubscriptionResource);



/***/ }),

/***/ "FKbl":
/*!***************************************************!*\
  !*** ./src/app/data/schema/organizations-user.ts ***!
  \***************************************************/
/*! exports provided: OrganizationsUser, OrganizationsUserRoles, OrganizationsUserRoleTitles */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "OrganizationsUser", function() { return OrganizationsUser; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "OrganizationsUserRoles", function() { return OrganizationsUserRoles; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "OrganizationsUserRoleTitles", function() { return OrganizationsUserRoleTitles; });
class OrganizationsUser {
    constructor(organizationsUser) {
        this.id = organizationsUser.id;
        this.name = organizationsUser.name;
        this.email = organizationsUser.email;
        this.role = organizationsUser.role;
    }
}
var OrganizationsUserRoles;
(function (OrganizationsUserRoles) {
    OrganizationsUserRoles[OrganizationsUserRoles["organization_owner"] = 1] = "organization_owner";
    OrganizationsUserRoles[OrganizationsUserRoles["organization_admin"] = 2] = "organization_admin";
    OrganizationsUserRoles[OrganizationsUserRoles["organization_editor"] = 3] = "organization_editor";
    OrganizationsUserRoles[OrganizationsUserRoles["organization_viewer"] = 4] = "organization_viewer";
})(OrganizationsUserRoles || (OrganizationsUserRoles = {}));
var OrganizationsUserRoleTitles;
(function (OrganizationsUserRoleTitles) {
    OrganizationsUserRoleTitles[OrganizationsUserRoleTitles["Owner"] = 1] = "Owner";
    OrganizationsUserRoleTitles[OrganizationsUserRoleTitles["Admin"] = 2] = "Admin";
    OrganizationsUserRoleTitles[OrganizationsUserRoleTitles["Editor"] = 3] = "Editor";
    OrganizationsUserRoleTitles[OrganizationsUserRoleTitles["Viewer"] = 4] = "Viewer";
})(OrganizationsUserRoleTitles || (OrganizationsUserRoleTitles = {}));


/***/ }),

/***/ "FYDM":
/*!*************************************************************************************************************************************************!*\
  !*** ./src/app/layout/components/toolbar/components/toolbar-proxy-settings/components/toolbar-mock-settings/toolbar-mock-settings.component.ts ***!
  \*************************************************************************************************************************************************/
/*! exports provided: ToolbarMockSettingsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ToolbarMockSettingsComponent", function() { return ToolbarMockSettingsComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_toolbar_mock_settings_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./toolbar-mock-settings.component.html */ "Ys2n");
/* harmony import */ var _toolbar_mock_settings_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./toolbar-mock-settings.component.scss */ "4mL1");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ "s7LF");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/dialog */ "iELJ");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! rxjs/operators */ "kU1M");
/* harmony import */ var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @iconify/icons-ic/twotone-close */ "5mnX");
/* harmony import */ var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @iconify/icons-ic/twotone-delete */ "e3EN");
/* harmony import */ var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _core_http_agent_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @core/http/agent.service */ "/JUU");
/* harmony import */ var _core_http_scenario_resource_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @core/http/scenario-resource.service */ "3Ncz");
/* harmony import */ var _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @projects/services/project-data.service */ "oyjd");
/* harmony import */ var _projects_services_projects_data_service__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @projects/services/projects-data.service */ "mbNh");
/* harmony import */ var _users_services_user_data_service__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @users/services/user-data.service */ "O7ya");
/* harmony import */ var _schema_agent_config__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ../../schema/agent-config */ "nmZq");















let ToolbarMockSettingsComponent = class ToolbarMockSettingsComponent {
    constructor(dialogRef, fb, agentService, projectDataService, projectsDataService, scenarioResource, userDataService) {
        this.dialogRef = dialogRef;
        this.fb = fb;
        this.agentService = agentService;
        this.projectDataService = projectDataService;
        this.projectsDataService = projectsDataService;
        this.scenarioResource = scenarioResource;
        this.userDataService = userDataService;
        this.onProjectChange = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
        this.onScenarioChange = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
        this.scenarios = [];
        this.icClose = _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_7___default.a;
        this.icDelete = _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_8___default.a;
    }
    ngOnInit() {
        // Initialize form
        this.form = this.fb.group({
            includePatterns: this.fb.array([]),
            excludePatterns: this.fb.array([]),
            mockPolicy: new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"]('all', [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required]),
            project: new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"](null, [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required]),
            scenario: new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"](null),
            serviceUrl: new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"](''),
        });
        this.initializePolicies();
        this.initializeConfig().subscribe((res) => {
            this.initializeProjects$(this.config);
            this.initializeProject(this.config);
            this.initializeScenarios(this.config);
        });
    }
    // API Access
    getScenarios(projectId) {
        projectId = projectId || this.project.id;
        return this.scenarioResource.index({ project_id: projectId }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["tap"])((res) => {
            this.scenarios = res.list;
        }));
    }
    // View Access
    clearScenario() {
        this.form.patchValue({
            scenario: null,
        });
    }
    addIncludePattern(pattern) {
        const includePatterns = this.form.get('includePatterns');
        includePatterns.push(this.fb.group({
            pattern: new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"](pattern || '', [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required]),
        }));
    }
    removeIncludePattern(index) {
        const includePatterns = this.form.get('includePatterns');
        includePatterns.removeAt(index);
    }
    addExcludePattern(pattern) {
        const excludePatterns = this.form.get('excludePatterns');
        excludePatterns.push(this.fb.group({
            pattern: new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"](pattern || '', [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required]),
        }));
    }
    removeExcludePattern(index) {
        const excludePatterns = this.form.get('excludePatterns');
        excludePatterns.removeAt(index);
    }
    update() {
        const formValue = this.form.value;
        const user = this.userDataService.user;
        const project = formValue.project;
        const config = {
            mode: {
                mock: {
                    exclude_patterns: formValue.excludePatterns.map(data => data.pattern),
                    include_patterns: formValue.includePatterns.map(data => data.pattern),
                    policy: formValue.mockPolicy,
                    project_key: project.key,
                    scenario_key: '',
                    service_url: formValue.serviceUrl || '',
                },
            },
        };
        if (formValue.scenario) {
            const scenario = formValue.scenario;
            config.mode.mock.scenario_key = scenario.key;
            this.onScenarioChange.emit(scenario);
        }
        this.onProjectChange.emit(project);
        if (this.config) {
            this.agentService.updateConfig(config).subscribe(res => {
                this.dialogRef.close();
            });
        }
        else {
            this.agentService.createConfig(config).subscribe(res => {
                this.dialogRef.close();
            });
        }
    }
    selectProject($event) {
        const project = $event.value;
        this.getScenarios(project.id).subscribe();
        this.form.patchValue({
            scenario: null,
        });
        this.project = project;
    }
    // Helpers
    initializePolicies() {
        this.agentService.showConfigsPolicies().subscribe(res => {
            this.policies = Object.values(res);
        });
    }
    initializeConfig() {
        return this.agentService.showConfig().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["tap"])((res) => {
            const config = res;
            if (config) {
                this.config = new _schema_agent_config__WEBPACK_IMPORTED_MODULE_14__["AgentConfig"](config);
                this.form.patchValue({
                    matchPatterns: this.config.mode.mock.matchPatterns,
                    mockPolicy: this.config.mode.mock.policy,
                    serviceUrl: this.config.mode.mock.serviceUrl,
                });
                this.config.mode.mock.includePatterns.forEach(pattern => {
                    this.addIncludePattern(pattern);
                });
                this.config.mode.mock.excludePatterns.forEach(pattern => {
                    this.addExcludePattern(pattern);
                });
            }
        }));
    }
    // Set projects$ observable
    initializeProjects$(config) {
        if (!this.projectsDataService.projects) {
            const organizationId = this.projectDataService.project.organizationId;
            this.projectsDataService.fetch(organizationId);
        }
        this.projects$ = this.projectsDataService.projects$;
    }
    initializeProject(config) {
        if (!config.mode.mock.projectKey) {
            this.project = this.projectDataService.project;
            this.form.patchValue({
                project: this.project,
            });
            this.update();
        }
        else {
            this.projects$.subscribe((projects) => {
                projects.some(project => {
                    if (config.mode.mock.projectKey === project.key) {
                        this.project = project;
                        this.form.patchValue({
                            project,
                        });
                        return true;
                    }
                });
            });
        }
    }
    initializeScenarios(config) {
        if (this.project) {
            this.getScenarios(this.project.id).subscribe(res => {
                this.scenarios.some(scenario => {
                    if (config.mode.mock.scenarioKey === scenario.key) {
                        this.form.patchValue({
                            scenario,
                        });
                        return true;
                    }
                });
            });
        }
    }
};
ToolbarMockSettingsComponent.ctorParameters = () => [
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MatDialogRef"] },
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormBuilder"] },
    { type: _core_http_agent_service__WEBPACK_IMPORTED_MODULE_9__["AgentService"] },
    { type: _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_11__["ProjectDataService"] },
    { type: _projects_services_projects_data_service__WEBPACK_IMPORTED_MODULE_12__["ProjectsDataService"] },
    { type: _core_http_scenario_resource_service__WEBPACK_IMPORTED_MODULE_10__["ScenarioResource"] },
    { type: _users_services_user_data_service__WEBPACK_IMPORTED_MODULE_13__["UserDataService"] }
];
ToolbarMockSettingsComponent.propDecorators = {
    onProjectChange: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Output"] }],
    onScenarioChange: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Output"] }]
};
ToolbarMockSettingsComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'vex-toolbar-mock-settings',
        template: _raw_loader_toolbar_mock_settings_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_toolbar_mock_settings_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], ToolbarMockSettingsComponent);



/***/ }),

/***/ "FblR":
/*!************************************************************!*\
  !*** ./src/@vex/layout/navigation/navigation.component.ts ***!
  \************************************************************/
/*! exports provided: NavigationComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "NavigationComponent", function() { return NavigationComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_navigation_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./navigation.component.html */ "wuZS");
/* harmony import */ var _navigation_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./navigation.component.scss */ "HiSN");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _services_navigation_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/navigation.service */ "0vMP");





let NavigationComponent = class NavigationComponent {
    constructor(navigationService) {
        this.navigationService = navigationService;
        this.items = this.navigationService.items;
    }
    ngOnInit() {
    }
};
NavigationComponent.ctorParameters = () => [
    { type: _services_navigation_service__WEBPACK_IMPORTED_MODULE_4__["NavigationService"] }
];
NavigationComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'vex-navigation',
        template: _raw_loader_navigation_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_navigation_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], NavigationComponent);



/***/ }),

/***/ "G605":
/*!********************************************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/layout/components/toolbar/components/toolbar-user/toolbar-user-dropdown/toolbar-user-dropdown.component.html ***!
  \********************************************************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div class=\"dropdown\">\n  <div class=\"dropdown-header\" fxLayout=\"row\" fxLayoutAlign=\"space-between center\">\n    <div fxLayout=\"row\" fxLayoutAlign=\"start center\">\n      <div class=\"dropdown-heading-icon\" fxLayout=\"row\" fxLayoutAlign=\"center center\">\n        <mat-icon [icIcon]=\"icons.icPerson\"></mat-icon>\n      </div>\n      <div class=\"dropdown-heading\" *ngIf=\"user$ | async as user\">\n        {{ user.name }}\n      </div>\n    </div>\n\n    <!-- <button [matMenuTriggerFor]=\"settingsMenu\"\n            mat-icon-button\n            matTooltip=\"Settings\"\n            matTooltipPosition=\"before\"\n            type=\"button\">\n      <mat-icon [icIcon]=\"icons.icSettings\" class=\"notifications-header-icon\"></mat-icon>\n    </button> -->\n  </div>\n\n  <div class=\"dropdown-content\">\n    <a *ngFor=\"let item of items; trackBy: trackById\"\n       [routerLink]=\"item.route\"\n       class=\"notification\"\n       fxLayout=\"row\"\n       fxLayoutAlign=\"start center\"\n       matRipple>\n      <mat-icon [icIcon]=\"item.icon\"\n                [ngClass]=\"item.colorClass\"\n                class=\"notification-icon\"\n                fxFlex=\"none\"></mat-icon>\n      <div fxFlex=\"auto\">\n        <div class=\"notification-label\">{{ item.label }}</div>\n        <div class=\"notification-description\">{{ item.description }}</div>\n      </div>\n      <mat-icon [icIcon]=\"icons.icChevronRight\" class=\"notification-chevron\" fxFlex=\"none\"></mat-icon>\n    </a>\n  </div>\n\n  <div class=\"dropdown-footer\" fxLayout=\"row\" fxLayoutAlign=\"space-between center\">\n    <button [matMenuTriggerFor]=\"statusMenu\" class=\"dropdown-footer-select\" mat-button type=\"button\">\n      <ng-container *ngFor=\"let status of statuses; trackBy: trackById\">\n        <span *ngIf=\"status === activeStatus\">\n          <mat-icon [icIcon]=\"status.icon\" [ngClass]=\"status.colorClass\"></mat-icon>\n          <span>{{ status.label }}</span>\n          <mat-icon [icIcon]=\"icons.icArrowDropDown\" class=\"dropdown-footer-select-caret\"></mat-icon>\n        </span>\n      </ng-container>\n    </button>\n    <a (click)=\"logout()\" color=\"primary\" mat-button>LOGOUT</a>\n  </div>\n</div>\n\n<mat-menu #statusMenu=\"matMenu\" xPosition=\"before\" yPosition=\"below\">\n  <button (click)=\"setStatus(status)\"\n          *ngFor=\"let status of statuses; trackBy: trackById\"\n          mat-menu-item>\n    <ic-icon [icon]=\"status.icon\" [ngClass]=\"status.colorClass\" inline=\"true\" size=\"24px\"></ic-icon>\n    <span>{{ status.label }}</span>\n  </button>\n</mat-menu>\n\n\n<mat-menu #settingsMenu=\"matMenu\" xPosition=\"before\" yPosition=\"below\">\n  <button mat-menu-item>\n    <mat-icon [icIcon]=\"icons.icBusiness\"></mat-icon>\n    <span>Change Address</span>\n  </button>\n\n  <button mat-menu-item>\n    <mat-icon [icIcon]=\"icons.icVerifiedUser\"></mat-icon>\n    <span>Change Username</span>\n  </button>\n\n  <button mat-menu-item>\n    <mat-icon [icIcon]=\"icons.icLock\"></mat-icon>\n    <span>Change Password</span>\n  </button>\n\n  <button mat-menu-item>\n    <mat-icon [icIcon]=\"icons.icNotificationsOff\"></mat-icon>\n    <span>Disable Notifications</span>\n  </button>\n</mat-menu>\n");

/***/ }),

/***/ "GK0M":
/*!********************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/layout/components/toolbar/toolbar.component.html ***!
  \********************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div class=\"toolbar w-full px-gutter shadow-b\" fxLayout=\"row\" fxLayoutAlign=\"start center\" vexContainer>\r\n  <button (click)=\"openSidenav()\" [fxHide]=\"!mobileQuery\" mat-icon-button type=\"button\">\r\n    <mat-icon [icIcon]=\"icMenu\"></mat-icon>\r\n  </button>\r\n\r\n  <a *ngIf=\"isVerticalLayout$ | async\"\r\n     [routerLink]=\"['/']\"\r\n     class=\"ltr:mr-4 rtl:ml-4 block\"\r\n     fxLayout=\"row\"\r\n     fxLayoutAlign=\"start center\">\r\n    <img class=\"w-8 select-none\" src=\"assets/img/demo/logo.svg\">\r\n    <h1 [fxHide]=\"mobileQuery\" class=\"title ltr:pl-4 rtl:pr-4 m-0 select-none\">\r\n      Stoobly\r\n    </h1>\r\n  </a>\r\n\r\n  <!-- <button *ngIf=\"isHorizontalLayout$ | async\"\r\n          [fxHide]=\"mobileQuery\"\r\n          [matMenuTriggerFor]=\"addNewMenu\"\r\n          color=\"primary\"\r\n          mat-raised-button\r\n          type=\"button\">ADD NEW\r\n  </button>\r\n\r\n  <mat-menu #addNewMenu=\"matMenu\" [overlapTrigger]=\"false\" xPosition=\"after\" yPosition=\"below\">\r\n    <button mat-menu-item>\r\n      <mat-icon [icIcon]=\"icPersonAdd\"></mat-icon>\r\n      <span>Add Contact</span>\r\n    </button>\r\n\r\n    <button mat-menu-item>\r\n      <mat-icon [icIcon]=\"icDoneAll\"></mat-icon>\r\n      <span>Add Task</span>\r\n    </button>\r\n\r\n    <button mat-menu-item>\r\n      <mat-icon [icIcon]=\"icAssignmentTurnedIn\"></mat-icon>\r\n      <span>Add Project</span>\r\n    </button>\r\n\r\n    <button [matMenuTriggerFor]=\"documentMenu\" mat-menu-item>\r\n      <mat-icon [icIcon]=\"icBallot\"></mat-icon>\r\n      <span>Add Document</span>\r\n    </button>\r\n  </mat-menu>\r\n\r\n  <mat-menu #documentMenu=\"matMenu\">\r\n    <button mat-menu-item>\r\n      <mat-icon [icIcon]=\"icDescription\"></mat-icon>\r\n      <span>Add Quote</span>\r\n    </button>\r\n\r\n    <button mat-menu-item>\r\n      <mat-icon [icIcon]=\"icAssignment\"></mat-icon>\r\n      <span>Add Invoice</span>\r\n    </button>\r\n\r\n    <button mat-menu-item>\r\n      <mat-icon [icIcon]=\"icReceipt\"></mat-icon>\r\n      <span>Add Receipt</span>\r\n    </button>\r\n  </mat-menu>\r\n\r\n  <div #megaMenuOriginRef class=\"ltr:ml-2 rtl:mr-2\">\r\n    <button\r\n      *ngIf=\"isHorizontalLayout$ | async\"\r\n      [fxHide]=\"mobileQuery\"\r\n      (click)=\"openMegaMenu(megaMenuOriginRef)\"\r\n      color=\"primary\"\r\n      mat-button\r\n      type=\"button\">\r\n      MEGA MENU\r\n      <ic-icon [icon]=\"icArrowDropDown\" class=\"ltr:-mr-1 rtl:-ml-1\" inline=\"true\"></ic-icon>\r\n    </button>\r\n  </div> -->\r\n\r\n  <!-- <button\r\n    *ngIf=\"project$ | async; let project\"\r\n    color=\"primary\"\r\n    mat-button\r\n    type=\"button\">\r\n    {{ project.name }}\r\n  </button> -->\r\n\r\n  <div *ngIf=\"isProject && (isVerticalLayout$ | async) && isNavbarInToolbar$ | async\"\r\n       [fxHide]=\"mobileQuery\"\r\n       class=\"px-gutter\"\r\n       fxFlex=\"none\"\r\n       fxLayout=\"row\"\r\n       fxLayoutAlign=\"start center\">\r\n    <vex-navigation-item *ngFor=\"let item of navigationItems\" [item]=\"item\"></vex-navigation-item>\r\n  </div>\r\n\r\n  <div \r\n    *ngIf=\"isProxied\"\r\n    class=\"px-5\"\r\n  >\r\n    <vex-toolbar-proxy-settings></vex-toolbar-proxy-settings>\r\n  </div>\r\n\r\n  <div\r\n    *ngIf=\"isSignedIn && isProject && !isProxied\"\r\n    class=\"px-1\"\r\n  >\r\n    <button \r\n      #originRef \r\n      (click)=\"showMockUrl()\" \r\n      color=\"accent\"\r\n      class=\"button\" \r\n      mat-button \r\n      type=\"button\"\r\n    >\r\n      <ic-icon [icon]=\"icPageView\" class=\"ltr:mr-3 rtl:ml-3\" inline=\"true\" size=\"22px\"></ic-icon>\r\n      VIEW MOCK URL\r\n    </button>\r\n  </div>\r\n\r\n  <span fxFlex></span>\r\n\r\n  <div class=\"-mx-1 flex items-center\">\r\n    <!-- <div class=\"px-1\">\r\n      <button (click)=\"openSearch()\" mat-icon-button type=\"button\">\r\n        <mat-icon [icIcon]=\"icSearch\"></mat-icon>\r\n      </button>\r\n    </div> -->\r\n\r\n    <!-- <div class=\"px-1\">\r\n      <vex-toolbar-notifications></vex-toolbar-notifications>\r\n    </div> -->\r\n\r\n    <!-- <div class=\"px-1\">\r\n      <button (click)=\"openQuickpanel()\" mat-icon-button type=\"button\">\r\n        <mat-icon [icIcon]=\"icBookmarks\"></mat-icon>\r\n      </button>\r\n    </div> -->\r\n\r\n    <!-- <div class=\"px-1\">\r\n      <button [matMenuTriggerFor]=\"languageMenu\" mat-icon-button type=\"button\">\r\n        <mat-icon [icIcon]=\"emojioneUS\"></mat-icon>\r\n      </button>\r\n    </div> -->\r\n\r\n    <div *ngIf=\"isSignedIn\" class=\"px-1\">\r\n      <vex-toolbar-user></vex-toolbar-user>\r\n    </div>\r\n\r\n    <!-- <mat-menu #languageMenu=\"matMenu\" overlapTrigger=\"false\" xPosition=\"before\" yPosition=\"below\">\r\n      <button mat-menu-item>\r\n        <mat-icon [icIcon]=\"emojioneUS\"></mat-icon>\r\n        <span>English</span>\r\n      </button>\r\n\r\n      <button mat-menu-item>\r\n        <mat-icon [icIcon]=\"emojioneDE\"></mat-icon>\r\n        <span>German</span>\r\n      </button>\r\n    </mat-menu> -->\r\n  </div>\r\n</div>\r\n\r\n<vex-navigation *ngIf=\"(isVerticalLayout$ | async) && isNavbarBelowToolbar$ | async\"\r\n                [fxHide]=\"mobileQuery\"></vex-navigation>\r\n");

/***/ }),

/***/ "Gg42":
/*!********************************************************!*\
  !*** ./src/app/core/interceptors/agent.interceptor.ts ***!
  \********************************************************/
/*! exports provided: AgentInterceptor */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AgentInterceptor", function() { return AgentInterceptor; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _core_http_agent_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @core/http/agent.service */ "/JUU");
/* harmony import */ var _core_utils_uri_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @core/utils/uri.service */ "BjwJ");
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @environments/environment */ "AytR");





let AgentInterceptor = class AgentInterceptor {
    constructor(uri, mockApiService) {
        this.uri = uri;
        this.mockApiService = mockApiService;
    }
    intercept(req, next) {
        if (!_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].agentUrl) {
            return next.handle(req);
        }
        else {
            // const serviceUrl = req.headers[this.mockApiService.SERVICE_URL_HEADER];
            // Default to apiUrl, else use X-Service-Url
            const headers = req.headers.
                append(this.mockApiService.DO_PROXY_HEADER, '1');
            // append(this.mockApiService.SERVICE_URL_HEADER, serviceUrl ? serviceUrl : environment.apiUrl);
            // Clone the request to add the new header
            const clonedRequest = req.clone({
                // .url: req.url.replace(environment.apiUrl, environment.agentUrl),
                headers,
            });
            // Pass the cloned request instead of the original request to the next handle
            return next.handle(clonedRequest);
        }
    }
};
AgentInterceptor.ctorParameters = () => [
    { type: _core_utils_uri_service__WEBPACK_IMPORTED_MODULE_3__["UriService"] },
    { type: _core_http_agent_service__WEBPACK_IMPORTED_MODULE_2__["AgentService"] }
];
AgentInterceptor = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])()
], AgentInterceptor);



/***/ }),

/***/ "H5iI":
/*!***********************************************************************************************!*\
  !*** ./src/@vex/components/config-panel/config-panel-toggle/config-panel-toggle.component.ts ***!
  \***********************************************************************************************/
/*! exports provided: ConfigPanelToggleComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ConfigPanelToggleComponent", function() { return ConfigPanelToggleComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_config_panel_toggle_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./config-panel-toggle.component.html */ "Zifb");
/* harmony import */ var _config_panel_toggle_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./config-panel-toggle.component.scss */ "oKEX");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _iconify_icons_ic_twotone_settings__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @iconify/icons-ic/twotone-settings */ "hF2C");
/* harmony import */ var _iconify_icons_ic_twotone_settings__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_settings__WEBPACK_IMPORTED_MODULE_4__);





let ConfigPanelToggleComponent = class ConfigPanelToggleComponent {
    constructor() {
        this.openConfig = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
        this.icSettings = _iconify_icons_ic_twotone_settings__WEBPACK_IMPORTED_MODULE_4___default.a;
    }
    ngOnInit() {
    }
};
ConfigPanelToggleComponent.ctorParameters = () => [];
ConfigPanelToggleComponent.propDecorators = {
    openConfig: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Output"] }]
};
ConfigPanelToggleComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'vex-config-panel-toggle',
        template: _raw_loader_config_panel_toggle_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_config_panel_toggle_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], ConfigPanelToggleComponent);



/***/ }),

/***/ "HiSN":
/*!**************************************************************!*\
  !*** ./src/@vex/layout/navigation/navigation.component.scss ***!
  \**************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (":host {\n  background: var(--navigation-background);\n  display: block;\n  height: var(--navigation-height);\n  position: relative;\n  z-index: 200;\n}\n\n.navigation {\n  height: var(--navigation-height);\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uL25hdmlnYXRpb24uY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSx3Q0FBQTtFQUNBLGNBQUE7RUFDQSxnQ0FBQTtFQUNBLGtCQUFBO0VBQ0EsWUFBQTtBQUNGOztBQUVBO0VBQ0UsZ0NBQUE7QUFDRiIsImZpbGUiOiJuYXZpZ2F0aW9uLmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiOmhvc3Qge1xuICBiYWNrZ3JvdW5kOiB2YXIoLS1uYXZpZ2F0aW9uLWJhY2tncm91bmQpO1xuICBkaXNwbGF5OiBibG9jaztcbiAgaGVpZ2h0OiB2YXIoLS1uYXZpZ2F0aW9uLWhlaWdodCk7XG4gIHBvc2l0aW9uOiByZWxhdGl2ZTtcbiAgei1pbmRleDogMjAwO1xufVxuXG4ubmF2aWdhdGlvbiB7XG4gIGhlaWdodDogdmFyKC0tbmF2aWdhdGlvbi1oZWlnaHQpO1xufSJdfQ== */");

/***/ }),

/***/ "Hv0H":
/*!*************************************************************!*\
  !*** ./src/app/layout/components/toolbar/toolbar.module.ts ***!
  \*************************************************************/
/*! exports provided: ToolbarModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ToolbarModule", function() { return ToolbarModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ "s7LF");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_material_core__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/core */ "UhP/");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/material/dialog */ "iELJ");
/* harmony import */ var _angular_material_divider__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/material/divider */ "BSbQ");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/material/form-field */ "Q2Ze");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @angular/material/input */ "e6WT");
/* harmony import */ var _angular_material_menu__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/material/menu */ "rJgo");
/* harmony import */ var _angular_material_select__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/material/select */ "ZTz/");
/* harmony import */ var _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @angular/material/snack-bar */ "zHaW");
/* harmony import */ var _vex_components_mega_menu_mega_menu_module__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @vex/components/mega-menu/mega-menu.module */ "C6sw");
/* harmony import */ var _vex_components_navigation_item_navigation_item_module__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @vex/components/navigation-item/navigation-item.module */ "5PI4");
/* harmony import */ var _vex_components_toolbar_search_toolbar_search_module__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @vex/components/toolbar-search/toolbar-search.module */ "gDAd");
/* harmony import */ var _vex_directives_container_container_module__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! @vex/directives/container/container.module */ "68Yx");
/* harmony import */ var _vex_layout_navigation_navigation_module__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! @vex/layout/navigation/navigation.module */ "ycnu");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! @projects/services/project-data.service */ "oyjd");
/* harmony import */ var _components_toolbar_mock_url_toolbar_mock_url_component__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! ./components/toolbar-mock-url/toolbar-mock-url.component */ "O4Sr");
/* harmony import */ var _components_toolbar_proxy_settings_toolbar_proxy_settings_module__WEBPACK_IMPORTED_MODULE_24__ = __webpack_require__(/*! ./components/toolbar-proxy-settings/toolbar-proxy-settings.module */ "whvR");
/* harmony import */ var _components_toolbar_user_toolbar_user_module__WEBPACK_IMPORTED_MODULE_25__ = __webpack_require__(/*! ./components/toolbar-user/toolbar-user.module */ "UY+R");
/* harmony import */ var _toolbar_component__WEBPACK_IMPORTED_MODULE_26__ = __webpack_require__(/*! ./toolbar.component */ "cd7D");



























let ToolbarModule = class ToolbarModule {
};
ToolbarModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_toolbar_component__WEBPACK_IMPORTED_MODULE_26__["ToolbarComponent"], _components_toolbar_mock_url_toolbar_mock_url_component__WEBPACK_IMPORTED_MODULE_23__["ToolbarMockUrlComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"],
            _angular_router__WEBPACK_IMPORTED_MODULE_5__["RouterModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_6__["MatButtonModule"],
            _angular_material_core__WEBPACK_IMPORTED_MODULE_7__["MatRippleModule"],
            _angular_material_dialog__WEBPACK_IMPORTED_MODULE_8__["MatDialogModule"],
            _angular_material_divider__WEBPACK_IMPORTED_MODULE_9__["MatDividerModule"],
            _angular_material_form_field__WEBPACK_IMPORTED_MODULE_10__["MatFormFieldModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_11__["MatIconModule"],
            _angular_material_input__WEBPACK_IMPORTED_MODULE_12__["MatInputModule"],
            _angular_material_menu__WEBPACK_IMPORTED_MODULE_13__["MatMenuModule"],
            _angular_material_select__WEBPACK_IMPORTED_MODULE_14__["MatSelectModule"],
            _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_15__["MatSnackBarModule"],
            _vex_directives_container_container_module__WEBPACK_IMPORTED_MODULE_19__["ContainerModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_21__["IconModule"],
            _vex_components_mega_menu_mega_menu_module__WEBPACK_IMPORTED_MODULE_16__["MegaMenuModule"],
            _vex_layout_navigation_navigation_module__WEBPACK_IMPORTED_MODULE_20__["NavigationModule"],
            _vex_components_navigation_item_navigation_item_module__WEBPACK_IMPORTED_MODULE_17__["NavigationItemModule"],
            _components_toolbar_proxy_settings_toolbar_proxy_settings_module__WEBPACK_IMPORTED_MODULE_24__["ToolbarProxySettingsModule"],
            _components_toolbar_user_toolbar_user_module__WEBPACK_IMPORTED_MODULE_25__["ToolbarUserModule"],
            _vex_components_toolbar_search_toolbar_search_module__WEBPACK_IMPORTED_MODULE_18__["ToolbarSearchModule"],
        ],
        entryComponents: [_components_toolbar_mock_url_toolbar_mock_url_component__WEBPACK_IMPORTED_MODULE_23__["ToolbarMockUrlComponent"]],
        exports: [_toolbar_component__WEBPACK_IMPORTED_MODULE_26__["ToolbarComponent"]],
        providers: [_projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_22__["ProjectDataService"]],
    })
], ToolbarModule);



/***/ }),

/***/ "KD9O":
/*!************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/@vex/components/progress-bar/progress-bar.component.html ***!
  \************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<mat-progress-bar [class.visible]=\"loader.progress$ | async\"\n                  [value]=\"loader.progress$ | async\"\n                  class=\"progress-bar\"\n                  mode=\"determinate\"></mat-progress-bar>\n");

/***/ }),

/***/ "L3CV":
/*!*************************************!*\
  !*** ./src/app/data/schema/plan.ts ***!
  \*************************************/
/*! exports provided: Plan */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Plan", function() { return Plan; });
class Plan {
    constructor(plan) {
        this.id = plan.id;
        this.name = plan.name;
        this.description = plan.description;
        this.createdAt = new Date(plan.created_at);
        this.updatedAt = new Date(plan.updated_at);
        this.chargeAmount = plan.charge_amount;
        this.chargeInDays = plan.chage_in_days;
    }
}


/***/ }),

/***/ "Li0u":
/*!********************************************************!*\
  !*** ./src/@vex/layout/sidenav/sidenav.component.scss ***!
  \********************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (".sidenav {\n  color: var(--sidenav-color);\n  height: 100%;\n  transition: var(--trans-ease-out);\n  width: var(--sidenav-width);\n}\n\n.sidenav.collapsed {\n  width: var(--sidenav-collapsed-width);\n}\n\n.sidenav.collapsed:not(.open) .sidenav-toolbar .title {\n  opacity: 0;\n  -webkit-padding-start: var(--sidenav-item-padding);\n          padding-inline-start: var(--sidenav-item-padding);\n}\n\n.sidenav.collapsed:not(.open) ::ng-deep .sidenav-items .item-icon {\n  -webkit-margin-end: var(--sidenav-item-padding);\n          margin-inline-end: var(--sidenav-item-padding);\n}\n\n.sidenav.collapsed:not(.open) ::ng-deep .sidenav-items .subheading, .sidenav.collapsed:not(.open) ::ng-deep .sidenav-items .item-badge, .sidenav.collapsed:not(.open) ::ng-deep .sidenav-items .item-label {\n  opacity: 0;\n}\n\n.sidenav.collapsed:not(.open) ::ng-deep .simplebar-track.simplebar-vertical {\n  visibility: hidden !important;\n}\n\n.sidenav.collapsed ::ng-deep .subheading, .sidenav.collapsed ::ng-deep .item-badge, .sidenav.collapsed ::ng-deep .item-label {\n  transition: all 200ms var(--trans-ease-out-timing-function);\n}\n\n.sidenav.collapsed.open {\n  width: var(--sidenav-width);\n}\n\n.sidenav-toolbar {\n  align-items: center;\n  background: var(--sidenav-toolbar-background);\n  box-sizing: border-box;\n  display: flex;\n  flex-direction: row;\n  height: var(--toolbar-height);\n  padding: 0 var(--padding);\n  white-space: nowrap;\n  width: 100%;\n}\n\n.sidenav-toolbar .title {\n  transition: padding var(--trans-ease-out-duration) var(--trans-ease-out-timing-function), opacity var(--trans-ease-out-duration) var(--trans-ease-out-timing-function);\n}\n\n.sidenav-items {\n  padding-top: var(--padding);\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uL3NpZGVuYXYuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSwyQkFBQTtFQUNBLFlBQUE7RUFDQSxpQ0FBQTtFQUNBLDJCQUFBO0FBQ0Y7O0FBRUE7RUFDRSxxQ0FBQTtBQUNGOztBQUVBO0VBQ0UsVUFBQTtFQUNBLGtEQUFBO1VBQUEsaURBQUE7QUFDRjs7QUFFQTtFQUNFLCtDQUFBO1VBQUEsOENBQUE7QUFDRjs7QUFFQTtFQUNFLFVBQUE7QUFDRjs7QUFFQTtFQUNFLDZCQUFBO0FBQ0Y7O0FBRUE7RUFDRSwyREFBQTtBQUNGOztBQUVBO0VBQ0UsMkJBQUE7QUFDRjs7QUFFQTtFQUNFLG1CQUFBO0VBQ0EsNkNBQUE7RUFDQSxzQkFBQTtFQUNBLGFBQUE7RUFDQSxtQkFBQTtFQUNBLDZCQUFBO0VBQ0EseUJBQUE7RUFDQSxtQkFBQTtFQUNBLFdBQUE7QUFDRjs7QUFFQTtFQUNFLHNLQUFBO0FBQ0Y7O0FBRUE7RUFDRSwyQkFBQTtBQUNGIiwiZmlsZSI6InNpZGVuYXYuY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyIuc2lkZW5hdiB7XG4gIGNvbG9yOiB2YXIoLS1zaWRlbmF2LWNvbG9yKTtcbiAgaGVpZ2h0OiAxMDAlO1xuICB0cmFuc2l0aW9uOiB2YXIoLS10cmFucy1lYXNlLW91dCk7XG4gIHdpZHRoOiB2YXIoLS1zaWRlbmF2LXdpZHRoKTtcbn1cblxuLnNpZGVuYXYuY29sbGFwc2VkIHtcbiAgd2lkdGg6IHZhcigtLXNpZGVuYXYtY29sbGFwc2VkLXdpZHRoKTtcbn1cblxuLnNpZGVuYXYuY29sbGFwc2VkOm5vdCgub3BlbikgLnNpZGVuYXYtdG9vbGJhciAudGl0bGUge1xuICBvcGFjaXR5OiAwO1xuICBwYWRkaW5nLWlubGluZS1zdGFydDogdmFyKC0tc2lkZW5hdi1pdGVtLXBhZGRpbmcpO1xufVxuXG4uc2lkZW5hdi5jb2xsYXBzZWQ6bm90KC5vcGVuKSA6Om5nLWRlZXAgLnNpZGVuYXYtaXRlbXMgLml0ZW0taWNvbiB7XG4gIG1hcmdpbi1pbmxpbmUtZW5kOiB2YXIoLS1zaWRlbmF2LWl0ZW0tcGFkZGluZyk7XG59XG5cbi5zaWRlbmF2LmNvbGxhcHNlZDpub3QoLm9wZW4pIDo6bmctZGVlcCAuc2lkZW5hdi1pdGVtcyAuc3ViaGVhZGluZywgLnNpZGVuYXYuY29sbGFwc2VkOm5vdCgub3BlbikgOjpuZy1kZWVwIC5zaWRlbmF2LWl0ZW1zIC5pdGVtLWJhZGdlLCAuc2lkZW5hdi5jb2xsYXBzZWQ6bm90KC5vcGVuKSA6Om5nLWRlZXAgLnNpZGVuYXYtaXRlbXMgLml0ZW0tbGFiZWwge1xuICBvcGFjaXR5OiAwO1xufVxuXG4uc2lkZW5hdi5jb2xsYXBzZWQ6bm90KC5vcGVuKSA6Om5nLWRlZXAgLnNpbXBsZWJhci10cmFjay5zaW1wbGViYXItdmVydGljYWwge1xuICB2aXNpYmlsaXR5OiBoaWRkZW4gIWltcG9ydGFudDtcbn1cblxuLnNpZGVuYXYuY29sbGFwc2VkIDo6bmctZGVlcCAuc3ViaGVhZGluZywgLnNpZGVuYXYuY29sbGFwc2VkIDo6bmctZGVlcCAuaXRlbS1iYWRnZSwgLnNpZGVuYXYuY29sbGFwc2VkIDo6bmctZGVlcCAuaXRlbS1sYWJlbCB7XG4gIHRyYW5zaXRpb246IGFsbCAyMDBtcyB2YXIoLS10cmFucy1lYXNlLW91dC10aW1pbmctZnVuY3Rpb24pO1xufVxuXG4uc2lkZW5hdi5jb2xsYXBzZWQub3BlbiB7XG4gIHdpZHRoOiB2YXIoLS1zaWRlbmF2LXdpZHRoKTtcbn1cblxuLnNpZGVuYXYtdG9vbGJhciB7XG4gIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG4gIGJhY2tncm91bmQ6IHZhcigtLXNpZGVuYXYtdG9vbGJhci1iYWNrZ3JvdW5kKTtcbiAgYm94LXNpemluZzogYm9yZGVyLWJveDtcbiAgZGlzcGxheTogZmxleDtcbiAgZmxleC1kaXJlY3Rpb246IHJvdztcbiAgaGVpZ2h0OiB2YXIoLS10b29sYmFyLWhlaWdodCk7XG4gIHBhZGRpbmc6IDAgdmFyKC0tcGFkZGluZyk7XG4gIHdoaXRlLXNwYWNlOiBub3dyYXA7XG4gIHdpZHRoOiAxMDAlO1xufVxuXG4uc2lkZW5hdi10b29sYmFyIC50aXRsZSB7XG4gIHRyYW5zaXRpb246IHBhZGRpbmcgdmFyKC0tdHJhbnMtZWFzZS1vdXQtZHVyYXRpb24pIHZhcigtLXRyYW5zLWVhc2Utb3V0LXRpbWluZy1mdW5jdGlvbiksIG9wYWNpdHkgdmFyKC0tdHJhbnMtZWFzZS1vdXQtZHVyYXRpb24pIHZhcigtLXRyYW5zLWVhc2Utb3V0LXRpbWluZy1mdW5jdGlvbik7XG59XG5cbi5zaWRlbmF2LWl0ZW1zIHtcbiAgcGFkZGluZy10b3A6IHZhcigtLXBhZGRpbmcpO1xufSJdfQ== */");

/***/ }),

/***/ "Li13":
/*!*****************************************************************!*\
  !*** ./src/@vex/components/progress-bar/progress-bar.module.ts ***!
  \*****************************************************************/
/*! exports provided: ProgressBarModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProgressBarModule", function() { return ProgressBarModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_material_progress_bar__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/material/progress-bar */ "BTe0");
/* harmony import */ var _ngx_loading_bar_core__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @ngx-loading-bar/core */ "TtxX");
/* harmony import */ var _ngx_loading_bar_router__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @ngx-loading-bar/router */ "lNyj");
/* harmony import */ var _progress_bar_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./progress-bar.component */ "WYjc");







let ProgressBarModule = class ProgressBarModule {
};
ProgressBarModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_progress_bar_component__WEBPACK_IMPORTED_MODULE_6__["ProgressBarComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_material_progress_bar__WEBPACK_IMPORTED_MODULE_3__["MatProgressBarModule"],
            _ngx_loading_bar_core__WEBPACK_IMPORTED_MODULE_4__["LoadingBarModule"],
            _ngx_loading_bar_router__WEBPACK_IMPORTED_MODULE_5__["LoadingBarRouterModule"]
        ],
        exports: [_progress_bar_component__WEBPACK_IMPORTED_MODULE_6__["ProgressBarComponent"]]
    })
], ProgressBarModule);



/***/ }),

/***/ "M0zT":
/*!*****************************************!*\
  !*** ./src/app/data/schema/response.ts ***!
  \*****************************************/
/*! exports provided: Response */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Response", function() { return Response; });
/* harmony import */ var _request_component__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./request-component */ "2bXN");

class Response extends _request_component__WEBPACK_IMPORTED_MODULE_0__["RequestComponent"] {
    constructor(response) {
        super(5, response.id);
        this.text = response.text;
        if (response.is_json !== undefined) {
            this.isJson = response.is_json;
        }
        else {
            this.isJson = true;
        }
    }
}


/***/ }),

/***/ "N/jG":
/*!*****************************************************************************************************************!*\
  !*** ./src/app/layout/components/toolbar/components/toolbar-proxy-settings/toolbar-proxy-settings.component.ts ***!
  \*****************************************************************************************************************/
/*! exports provided: ToolbarProxySettingsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ToolbarProxySettingsComponent", function() { return ToolbarProxySettingsComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_toolbar_proxy_settings_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./toolbar-proxy-settings.component.html */ "z6XH");
/* harmony import */ var _toolbar_proxy_settings_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./toolbar-proxy-settings.component.scss */ "UZWc");
/* harmony import */ var _angular_cdk_clipboard__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/cdk/clipboard */ "Tr4x");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/dialog */ "iELJ");
/* harmony import */ var _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/snack-bar */ "zHaW");
/* harmony import */ var _iconify_icons_ic_twotone_arrow_drop_down__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @iconify/icons-ic/twotone-arrow-drop-down */ "LgSP");
/* harmony import */ var _iconify_icons_ic_twotone_arrow_drop_down__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_arrow_drop_down__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _iconify_icons_ic_twotone_file_copy__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @iconify/icons-ic/twotone-file-copy */ "L5jV");
/* harmony import */ var _iconify_icons_ic_twotone_file_copy__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_file_copy__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _iconify_icons_ic_twotone_play_arrow__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @iconify/icons-ic/twotone-play-arrow */ "UfLF");
/* harmony import */ var _iconify_icons_ic_twotone_play_arrow__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_play_arrow__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _iconify_icons_ic_twotone_settings__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @iconify/icons-ic/twotone-settings */ "hF2C");
/* harmony import */ var _iconify_icons_ic_twotone_settings__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_settings__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _iconify_icons_ic_twotone_stop__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @iconify/icons-ic/twotone-stop */ "KhN+");
/* harmony import */ var _iconify_icons_ic_twotone_stop__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_stop__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var _core_http__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @core/http */ "vAmI");
/* harmony import */ var _core_http_agent_service__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @core/http/agent.service */ "/JUU");
/* harmony import */ var _data_schema__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @data/schema */ "V99k");
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @environments/environment */ "AytR");
/* harmony import */ var _components_toolbar_mock_settings_toolbar_mock_settings_component__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ./components/toolbar-mock-settings/toolbar-mock-settings.component */ "FYDM");
/* harmony import */ var _components_toolbar_record_settings_toolbar_record_settings_component__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! ./components/toolbar-record-settings/toolbar-record-settings.component */ "f/93");


















let ToolbarProxySettingsComponent = class ToolbarProxySettingsComponent {
    constructor(cd, clipboard, dialog, agentService, projectResource, scenarioResource, snackbar) {
        this.cd = cd;
        this.clipboard = clipboard;
        this.dialog = dialog;
        this.agentService = agentService;
        this.projectResource = projectResource;
        this.scenarioResource = scenarioResource;
        this.snackbar = snackbar;
        this.icArrowDropDown = _iconify_icons_ic_twotone_arrow_drop_down__WEBPACK_IMPORTED_MODULE_7___default.a;
        this.icSettings = _iconify_icons_ic_twotone_settings__WEBPACK_IMPORTED_MODULE_10___default.a;
        this.icFileCopy = _iconify_icons_ic_twotone_file_copy__WEBPACK_IMPORTED_MODULE_8___default.a;
        this.icPlayArrow = _iconify_icons_ic_twotone_play_arrow__WEBPACK_IMPORTED_MODULE_9___default.a;
        this.icStop = _iconify_icons_ic_twotone_stop__WEBPACK_IMPORTED_MODULE_11___default.a;
    }
    ngOnInit() {
        this.showModes();
    }
    // API Access
    showModes() {
        this.agentService.showConfigsModes().subscribe((res) => {
            this.modes = res;
            this.showProject();
            this.showScenario();
        });
    }
    showProject() {
        const activeMode = this.modes.active;
        const details = this.modes.details[activeMode];
        if (!details.project_id) {
            this.activeScenario = null;
            this.cd.markForCheck();
        }
        else {
            this.projectResource.show(details.project_id).subscribe((res) => {
                this.activeProject = new _data_schema__WEBPACK_IMPORTED_MODULE_14__["Project"](res);
                this.cd.markForCheck();
            });
        }
    }
    showScenario() {
        const activeMode = this.modes.active;
        const details = this.modes.details[activeMode];
        if (!details.scenario_id) {
            this.activeScenario = null;
            this.cd.markForCheck();
        }
        else {
            this.scenarioResource.show(details.scenario_id).subscribe((res) => {
                this.activeScenario = new _data_schema__WEBPACK_IMPORTED_MODULE_14__["Scenario"](res);
                this.cd.markForCheck();
            });
        }
    }
    // View Access
    showRecordSettings() {
        this.dropdownOpen = true;
        this.cd.markForCheck();
        const popoverRef = this.dialog.open(_components_toolbar_record_settings_toolbar_record_settings_component__WEBPACK_IMPORTED_MODULE_17__["ToolbarRecordSettingsComponent"], {
            width: '600px',
        });
        const onProjectChangeSub = popoverRef.componentInstance.onProjectChange.subscribe((project) => {
            this.activeProject = project;
            this.cd.markForCheck();
        });
        const onScenarioChangeSub = popoverRef.componentInstance.onScenarioChange.subscribe((scenario) => {
            this.activeScenario = scenario;
            this.cd.markForCheck();
        });
        popoverRef.afterClosed().subscribe(() => {
            this.dropdownOpen = false;
            onProjectChangeSub.unsubscribe();
            onScenarioChangeSub.unsubscribe();
            this.cd.markForCheck();
        });
    }
    showMockSettings() {
        this.dropdownOpen = true;
        this.cd.markForCheck();
        const popoverRef = this.dialog.open(_components_toolbar_mock_settings_toolbar_mock_settings_component__WEBPACK_IMPORTED_MODULE_16__["ToolbarMockSettingsComponent"], {
            width: '600px',
        });
        const onProjectChangeSub = popoverRef.componentInstance.onProjectChange.subscribe((project) => {
            this.activeProject = project;
        });
        const onScenarioChangeSub = popoverRef.componentInstance.onScenarioChange.subscribe((scenario) => {
            this.activeScenario = scenario;
        });
        popoverRef.afterClosed().subscribe(() => {
            this.dropdownOpen = false;
            onProjectChangeSub.unsubscribe();
            onScenarioChangeSub.unsubscribe();
            this.cd.markForCheck();
        });
    }
    setMode(modeVal) {
        const mode = {
            active: modeVal,
        };
        mode[modeVal] = {
            enabled: false,
        };
        const body = { mode };
        this.agentService.updateConfig(body).subscribe(res => {
            this.modes.active = modeVal;
            this.modes.enabled = false;
            this.showModes();
        });
    }
    toggleEnabled() {
        const mode = {};
        mode[this.modes.active] = {
            enabled: !this.modes.enabled,
        };
        const body = { mode };
        this.agentService.updateConfig(body).subscribe(res => {
            this.modes.enabled = !this.modes.enabled;
            this.cd.markForCheck();
        });
    }
    copyUrl() {
        this.clipboard.copy(_environments_environment__WEBPACK_IMPORTED_MODULE_15__["environment"].agentUrl);
        this.snackbar.open('URL copied to clipboard!', 'close', {
            duration: 2000,
        });
    }
};
ToolbarProxySettingsComponent.ctorParameters = () => [
    { type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["ChangeDetectorRef"] },
    { type: _angular_cdk_clipboard__WEBPACK_IMPORTED_MODULE_3__["Clipboard"] },
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MatDialog"] },
    { type: _core_http_agent_service__WEBPACK_IMPORTED_MODULE_13__["AgentService"] },
    { type: _core_http__WEBPACK_IMPORTED_MODULE_12__["ProjectResource"] },
    { type: _core_http__WEBPACK_IMPORTED_MODULE_12__["ScenarioResource"] },
    { type: _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_6__["MatSnackBar"] }
];
ToolbarProxySettingsComponent.propDecorators = {
    originRef: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["ViewChild"], args: ['originRef', { static: true, read: _angular_core__WEBPACK_IMPORTED_MODULE_4__["ElementRef"] },] }]
};
ToolbarProxySettingsComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_4__["Component"])({
        selector: 'vex-toolbar-proxy-settings',
        template: _raw_loader_toolbar_proxy_settings_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_4__["ChangeDetectionStrategy"].OnPush,
        styles: [_toolbar_proxy_settings_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], ToolbarProxySettingsComponent);



/***/ }),

/***/ "NEAy":
/*!**********************************************************!*\
  !*** ./src/@vex/components/popover/popover.component.ts ***!
  \**********************************************************/
/*! exports provided: PopoverComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PopoverComponent", function() { return PopoverComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_popover_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./popover.component.html */ "YiRj");
/* harmony import */ var _popover_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./popover.component.scss */ "nW1T");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _animations_popover_animation__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../animations/popover.animation */ "2e3Z");
/* harmony import */ var _popover_ref__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./popover-ref */ "QaI9");






let PopoverComponent = class PopoverComponent {
    constructor(popoverRef) {
        this.popoverRef = popoverRef;
        this.renderMethod = 'component';
    }
    ngOnInit() {
        this.content = this.popoverRef.content;
        if (typeof this.content === 'string') {
            this.renderMethod = 'text';
        }
        if (this.content instanceof _angular_core__WEBPACK_IMPORTED_MODULE_3__["TemplateRef"]) {
            this.renderMethod = 'template';
            this.context = {
                close: this.popoverRef.close.bind(this.popoverRef)
            };
        }
    }
};
PopoverComponent.ctorParameters = () => [
    { type: _popover_ref__WEBPACK_IMPORTED_MODULE_5__["PopoverRef"] }
];
PopoverComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        template: _raw_loader_popover_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        animations: [_animations_popover_animation__WEBPACK_IMPORTED_MODULE_4__["popoverAnimation"]],
        styles: [_popover_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], PopoverComponent);



/***/ }),

/***/ "NUQi":
/*!*******************************************!*\
  !*** ./src/app/core/guards/auth.guard.ts ***!
  \*******************************************/
/*! exports provided: AuthGuard */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AuthGuard", function() { return AuthGuard; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var angular_token__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! angular-token */ "hU4o");




let AuthGuard = class AuthGuard {
    constructor(router, tokenService) {
        this.router = router;
        this.tokenService = tokenService;
    }
    canActivate(next, state) {
        if (this.tokenService.canActivate(next, state)) {
            return true;
        }
        // Navigate to login page
        this.router.navigate(['/login']);
        // Can save redirect url so after authing we can move them back to the page they requested
        return false;
    }
};
AuthGuard.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
    { type: angular_token__WEBPACK_IMPORTED_MODULE_3__["AngularTokenService"] }
];
AuthGuard = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], AuthGuard);



/***/ }),

/***/ "Neo8":
/*!*************************************************************!*\
  !*** ./src/app/core/interceptors/http-error.interceptor.ts ***!
  \*************************************************************/
/*! exports provided: HttpErrorInterceptor */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "HttpErrorInterceptor", function() { return HttpErrorInterceptor; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs/operators */ "kU1M");
/* harmony import */ var _core_utils_http_error_handler__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @core/utils/http-error-handler */ "87D3");




let HttpErrorInterceptor = class HttpErrorInterceptor {
    constructor(errorHandler) {
        this.errorHandler = errorHandler;
    }
    intercept(request, next) {
        return next.handle(request).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["catchError"])(err => {
            return this.errorHandler.handleError(err);
        }));
    }
};
HttpErrorInterceptor.ctorParameters = () => [
    { type: _core_utils_http_error_handler__WEBPACK_IMPORTED_MODULE_3__["HttpErrorHandler"] }
];
HttpErrorInterceptor = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])()
], HttpErrorInterceptor);



/***/ }),

/***/ "O4Sr":
/*!*****************************************************************************************************!*\
  !*** ./src/app/layout/components/toolbar/components/toolbar-mock-url/toolbar-mock-url.component.ts ***!
  \*****************************************************************************************************/
/*! exports provided: ToolbarMockUrlComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ToolbarMockUrlComponent", function() { return ToolbarMockUrlComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_toolbar_mock_url_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./toolbar-mock-url.component.html */ "nvf/");
/* harmony import */ var _toolbar_mock_url_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./toolbar-mock-url.component.scss */ "AKSP");
/* harmony import */ var _angular_cdk_clipboard__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/cdk/clipboard */ "Tr4x");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/forms */ "s7LF");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/dialog */ "iELJ");
/* harmony import */ var _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/snack-bar */ "zHaW");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! rxjs/operators */ "kU1M");
/* harmony import */ var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @iconify/icons-ic/twotone-close */ "5mnX");
/* harmony import */ var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @iconify/icons-ic/twotone-delete */ "e3EN");
/* harmony import */ var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _iconify_icons_ic_twotone_file_copy__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @iconify/icons-ic/twotone-file-copy */ "L5jV");
/* harmony import */ var _iconify_icons_ic_twotone_file_copy__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_file_copy__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var _core_http_scenario_resource_service__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @core/http/scenario-resource.service */ "3Ncz");
/* harmony import */ var _data_schema__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @data/schema */ "V99k");
/* harmony import */ var _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @projects/services/project-data.service */ "oyjd");
/* harmony import */ var _projects_services_projects_data_service__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @projects/services/projects-data.service */ "mbNh");
















let ToolbarMockUrlComponent = class ToolbarMockUrlComponent {
    constructor(clipboard, dialogRef, fb, projectDataService, scenarioResource, snackbar, projectsDataService) {
        this.clipboard = clipboard;
        this.dialogRef = dialogRef;
        this.fb = fb;
        this.projectDataService = projectDataService;
        this.scenarioResource = scenarioResource;
        this.snackbar = snackbar;
        this.projectsDataService = projectsDataService;
        this.scenarios = [];
        this.icClose = _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_9___default.a;
        this.icDelete = _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_10___default.a;
        this.icFileCopy = _iconify_icons_ic_twotone_file_copy__WEBPACK_IMPORTED_MODULE_11___default.a;
    }
    ngOnInit() {
        // Initialize form
        this.form = this.fb.group({
            project: new _angular_forms__WEBPACK_IMPORTED_MODULE_5__["FormControl"](null, [_angular_forms__WEBPACK_IMPORTED_MODULE_5__["Validators"].required]),
            scenario: new _angular_forms__WEBPACK_IMPORTED_MODULE_5__["FormControl"](null),
            mockUrl: new _angular_forms__WEBPACK_IMPORTED_MODULE_5__["FormControl"]('', [_angular_forms__WEBPACK_IMPORTED_MODULE_5__["Validators"].required]),
        });
        // This will only be set if the user is viewing a project
        this.project = this.projectDataService.project;
        this.handleProjectSelect(this.project);
        this.initializeProjects$();
        this.initializeScenarios();
    }
    // API Access
    getScenarios(projectId) {
        projectId = projectId || this.project.id;
        return this.scenarioResource.index({ project_id: projectId }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_8__["tap"])((res) => {
            this.scenarios = res.list.map(s => {
                return new _data_schema__WEBPACK_IMPORTED_MODULE_13__["Scenario"](s);
            });
        }));
    }
    // View Access
    clearScenario() {
        this.form.patchValue({
            scenario: null,
        });
        this.handleProjectSelect(this.project);
    }
    copyUrl($event) {
        const url = this.form.value.mockUrl;
        this.clipboard.copy(url);
        this.snackbar.open('URL copied to clipboard!', 'close', {
            duration: 2000,
        });
    }
    selectProject($event) {
        const project = $event.value;
        this.handleProjectSelect(project);
    }
    selectScenario($event) {
        const scenario = $event.value;
        this.form.patchValue({
            mockUrl: scenario.mockUrl,
        });
    }
    // Helpers
    handleProjectSelect(project) {
        if (!project) {
            return;
        }
        this.getScenarios(project.id).subscribe();
        this.form.patchValue({
            project,
            scenario: null,
            mockUrl: project.mockUrl,
        });
        this.project = project;
    }
    // Set projects$ observable
    initializeProjects$() {
        if (!this.projectsDataService.projects) {
            this.projectsDataService.fetch(this.project.organizationId);
        }
        this.projects$ = this.projectsDataService.projects$;
        this.projects$.subscribe((projects) => {
        });
    }
    initializeScenarios() {
        if (this.project) {
            this.getScenarios(this.project.id).subscribe(res => {
            });
        }
    }
    /**
     *
     * Use to set default value for mat-select with reactive forms
     *
     * @param o1
     * @param o2
     * @returns [Boolean]
     *
     */
    compareProjects(o1, o2) {
        return (o1.name == o2.name);
    }
};
ToolbarMockUrlComponent.ctorParameters = () => [
    { type: _angular_cdk_clipboard__WEBPACK_IMPORTED_MODULE_3__["Clipboard"] },
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_6__["MatDialogRef"] },
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_5__["FormBuilder"] },
    { type: _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_14__["ProjectDataService"] },
    { type: _core_http_scenario_resource_service__WEBPACK_IMPORTED_MODULE_12__["ScenarioResource"] },
    { type: _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_7__["MatSnackBar"] },
    { type: _projects_services_projects_data_service__WEBPACK_IMPORTED_MODULE_15__["ProjectsDataService"] }
];
ToolbarMockUrlComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_4__["Component"])({
        selector: 'vex-toolbar-mock-url',
        template: _raw_loader_toolbar_mock_url_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_toolbar_mock_url_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], ToolbarMockUrlComponent);



/***/ }),

/***/ "O7ya":
/*!*************************************************************!*\
  !*** ./src/app/modules/users/services/user-data.service.ts ***!
  \*************************************************************/
/*! exports provided: UserDataService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserDataService", function() { return UserDataService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "qCKp");
/* harmony import */ var _core_http_user_resource_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @core/http/user-resource.service */ "9IlP");
/* harmony import */ var _data_schema_user__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @data/schema/user */ "/8CK");





let UserDataService = class UserDataService {
    constructor(userResource) {
        this.userResource = userResource;
        this.subject = new rxjs__WEBPACK_IMPORTED_MODULE_2__["BehaviorSubject"](null);
        this.user$ = this.subject.asObservable();
    }
    get() {
        if (this.user) {
            return this.user$;
        }
        this.userResource.profile().subscribe(res => {
            this.set(new _data_schema_user__WEBPACK_IMPORTED_MODULE_4__["User"](res));
        });
        return this.user$;
    }
    set(user) {
        if (user.hasOwnProperty('created_at')) {
            user = new _data_schema_user__WEBPACK_IMPORTED_MODULE_4__["User"](user);
        }
        this.user = user;
        this.subject.next(user);
    }
};
UserDataService.ctorParameters = () => [
    { type: _core_http_user_resource_service__WEBPACK_IMPORTED_MODULE_3__["UserResource"] }
];
UserDataService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], UserDataService);



/***/ }),

/***/ "OTSD":
/*!*********************************************!*\
  !*** ./src/@vex/services/search.service.ts ***!
  \*********************************************/
/*! exports provided: SearchService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SearchService", function() { return SearchService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "qCKp");



let SearchService = class SearchService {
    constructor() {
        this.valueChangesSubject = new rxjs__WEBPACK_IMPORTED_MODULE_2__["BehaviorSubject"](undefined);
        this.valueChanges$ = this.valueChangesSubject.asObservable();
        this.submitSubject = new rxjs__WEBPACK_IMPORTED_MODULE_2__["Subject"]();
        this.submit$ = this.submitSubject.asObservable();
        this.isOpenSubject = new rxjs__WEBPACK_IMPORTED_MODULE_2__["BehaviorSubject"](false);
        this.isOpen$ = this.isOpenSubject.asObservable();
    }
};
SearchService.ctorParameters = () => [];
SearchService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], SearchService);



/***/ }),

/***/ "OZ7D":
/*!******************************************!*\
  !*** ./src/app/core/http/url-builder.ts ***!
  \******************************************/
/*! exports provided: UrlBuilder */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UrlBuilder", function() { return UrlBuilder; });
class UrlBuilder {
    constructor() {
        this.url = '';
        this.query = false;
    }
    withPath(path) {
        if (this.url.length === 0) {
            this.url = path;
        }
        else {
            this.url = this.join(this.url, path);
        }
    }
    search(parameter, value) {
        this.glue();
        this.url += parameter + '=' + value;
        return this;
    }
    join(...args) {
        let path = args[0];
        const len = args.length;
        for (let i = 1; i < len; ++i) {
            const pathLen = path.length;
            let tok = args[i];
            if (tok[0] === '/') {
                tok = tok.replace('/', '');
            }
            if (path[pathLen - 1] === '/') {
                path += tok;
            }
            else {
                path += ('/' + tok);
            }
        }
        return path;
    }
    glue() {
        if (!this.query) {
            this.url += '?';
            this.query = true;
        }
        else {
            this.url += '&';
        }
    }
}


/***/ }),

/***/ "P9CE":
/*!********************************************!*\
  !*** ./src/app/data/schema/alias-value.ts ***!
  \********************************************/
/*! exports provided: AliasValue */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AliasValue", function() { return AliasValue; });
class AliasValue {
    constructor(aliasValue) {
        this.id = aliasValue.id;
        this.value = aliasValue.value;
    }
}


/***/ }),

/***/ "PC2b":
/*!**********************************************************************!*\
  !*** ./src/@vex/components/progress-bar/progress-bar.component.scss ***!
  \**********************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (".progress-bar {\n  left: 0;\n  opacity: 0;\n  position: fixed;\n  right: 0;\n  top: 0;\n  visibility: hidden;\n  z-index: 99999;\n}\n\n.progress-bar.visible {\n  opacity: 1;\n  visibility: visible;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uL3Byb2dyZXNzLWJhci5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLE9BQUE7RUFDQSxVQUFBO0VBQ0EsZUFBQTtFQUNBLFFBQUE7RUFDQSxNQUFBO0VBQ0Esa0JBQUE7RUFDQSxjQUFBO0FBQ0Y7O0FBRUE7RUFDRSxVQUFBO0VBQ0EsbUJBQUE7QUFDRiIsImZpbGUiOiJwcm9ncmVzcy1iYXIuY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyIucHJvZ3Jlc3MtYmFyIHtcbiAgbGVmdDogMDtcbiAgb3BhY2l0eTogMDtcbiAgcG9zaXRpb246IGZpeGVkO1xuICByaWdodDogMDtcbiAgdG9wOiAwO1xuICB2aXNpYmlsaXR5OiBoaWRkZW47XG4gIHotaW5kZXg6IDk5OTk5O1xufVxuXG4ucHJvZ3Jlc3MtYmFyLnZpc2libGUge1xuICBvcGFjaXR5OiAxO1xuICB2aXNpYmlsaXR5OiB2aXNpYmxlO1xufSJdfQ== */");

/***/ }),

/***/ "QaI9":
/*!****************************************************!*\
  !*** ./src/@vex/components/popover/popover-ref.ts ***!
  \****************************************************/
/*! exports provided: PopoverRef */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PopoverRef", function() { return PopoverRef; });
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! rxjs */ "qCKp");

class PopoverRef {
    constructor(overlay, content, data) {
        this.overlay = overlay;
        this.content = content;
        this.data = data;
        this.afterClosed = new rxjs__WEBPACK_IMPORTED_MODULE_0__["Subject"]();
        this.afterClosed$ = this.afterClosed.asObservable();
        overlay.backdropClick().subscribe(() => {
            this._close('backdropClick', null);
        });
    }
    close(data) {
        this._close('close', data);
    }
    _close(type, data) {
        this.overlay.dispose();
        this.afterClosed.next({
            type,
            data
        });
        this.afterClosed.complete();
    }
}


/***/ }),

/***/ "RdP6":
/*!*************************************************************!*\
  !*** ./src/app/core/http/omniauth-callbacks-api.service.ts ***!
  \*************************************************************/
/*! exports provided: OmniauthCallbacksApi */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "OmniauthCallbacksApi", function() { return OmniauthCallbacksApi; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _http_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./http.service */ "gHic");



let OmniauthCallbacksApi = class OmniauthCallbacksApi {
    constructor(httpService) {
        this.httpService = httpService;
        this.ENDPOINT = 'omniauth';
    }
    google(params) {
        const url = this.httpService.buildUrl([this.ENDPOINT, 'google_oauth2', 'callback']);
        return this.httpService.post(url, params);
    }
};
OmniauthCallbacksApi.ctorParameters = () => [
    { type: _http_service__WEBPACK_IMPORTED_MODULE_2__["HttpService"] }
];
OmniauthCallbacksApi = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], OmniauthCallbacksApi);



/***/ }),

/***/ "SEeg":
/*!*******************************************************************************************************************************************************!*\
  !*** ./src/app/layout/components/toolbar/components/toolbar-proxy-settings/components/toolbar-record-settings/toolbar-record-settings.component.scss ***!
  \*******************************************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (".dropdown {\n  background: var(--background-card);\n  border-bottom-left-radius: var(--border-radius);\n  border-bottom-right-radius: var(--border-radius);\n  box-shadow: var(--elevation-z4);\n  max-width: 100vw;\n  overflow: hidden;\n  width: 350px;\n  border-radius: 0.25rem;\n}\n\n.dropdown-header {\n  box-shadow: var(--elevation-z6);\n  padding-top: 1rem;\n  padding-bottom: 1rem;\n  padding-left: 1.5rem;\n  padding-right: 1.5rem;\n}\n\n.dropdown-heading {\n  font: var(--font-title);\n}\n\n.dropdown-content {\n  max-height: 291px;\n  overflow-x: hidden;\n  overflow-y: auto;\n  padding: 10px;\n}\n\n.dropdown-footer {\n  background: var(--background-app-bar);\n  border-top: 1px solid var(--foreground-divider);\n  padding: var(--padding-8) var(--padding);\n}\n\n.notification {\n  color: var(--text-color);\n  padding: var(--padding-16) var(--padding);\n  position: relative;\n  text-decoration: none;\n  transition: var(--trans-ease-out);\n  -webkit-user-select: none;\n     -moz-user-select: none;\n          user-select: none;\n}\n\n.notification:hover {\n  background: var(--background-hover);\n}\n\n.notification:hover .notification-label {\n  --text-opacity: 1;\n  color: #5c77ff;\n  color: rgba(92, 119, 255, var(--text-opacity));\n}\n\n.notification.read {\n  opacity: 0.5;\n}\n\n.notification-icon {\n  -webkit-margin-end: var(--padding);\n          margin-inline-end: var(--padding);\n}\n\n.notification-label {\n  transition: inherit;\n}\n\n.notification-description {\n  color: var(--text-secondary);\n  font: var(--font-caption);\n}\n\n.notification-chevron {\n  color: var(--text-hint);\n  font-size: 18px;\n  height: 18px;\n  width: 18px;\n}\n\n.notification + .notification {\n  border-top: 1px solid var(--foreground-divider);\n}\n\n.input-button {\n  margin-top: 8px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uLy4uLy4uLy4uLy4uL3Rvb2xiYXItcmVjb3JkLXNldHRpbmdzLmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0VBQ0Usa0NBQUE7RUFDQSwrQ0FBQTtFQUNBLGdEQUFBO0VBQ0EsK0JBQUE7RUFDQSxnQkFBQTtFQUNBLGdCQUFBO0VBQ0EsWUFBQTtFQUNBLHNCQUFBO0FBQ0Y7O0FBRUE7RUFDRSwrQkFBQTtFQUNBLGlCQUFBO0VBQ0Esb0JBQUE7RUFDQSxvQkFBQTtFQUNBLHFCQUFBO0FBQ0Y7O0FBRUE7RUFDRSx1QkFBQTtBQUNGOztBQUVBO0VBQ0UsaUJBQUE7RUFDQSxrQkFBQTtFQUNBLGdCQUFBO0VBQ0EsYUFBQTtBQUNGOztBQUVBO0VBQ0UscUNBQUE7RUFDQSwrQ0FBQTtFQUNBLHdDQUFBO0FBQ0Y7O0FBRUE7RUFDRSx3QkFBQTtFQUNBLHlDQUFBO0VBQ0Esa0JBQUE7RUFDQSxxQkFBQTtFQUNBLGlDQUFBO0VBQ0EseUJBQUE7S0FBQSxzQkFBQTtVQUFBLGlCQUFBO0FBQ0Y7O0FBRUE7RUFDRSxtQ0FBQTtBQUNGOztBQUVBO0VBQ0UsaUJBQUE7RUFDQSxjQUFBO0VBQ0EsOENBQUE7QUFDRjs7QUFFQTtFQUNFLFlBQUE7QUFDRjs7QUFFQTtFQUNFLGtDQUFBO1VBQUEsaUNBQUE7QUFDRjs7QUFFQTtFQUNFLG1CQUFBO0FBQ0Y7O0FBRUE7RUFDRSw0QkFBQTtFQUNBLHlCQUFBO0FBQ0Y7O0FBRUE7RUFDRSx1QkFBQTtFQUNBLGVBQUE7RUFDQSxZQUFBO0VBQ0EsV0FBQTtBQUNGOztBQUVBO0VBQ0UsK0NBQUE7QUFDRjs7QUFFQTtFQUNFLGVBQUE7QUFDRiIsImZpbGUiOiJ0b29sYmFyLXJlY29yZC1zZXR0aW5ncy5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbIi5kcm9wZG93biB7XG4gIGJhY2tncm91bmQ6IHZhcigtLWJhY2tncm91bmQtY2FyZCk7XG4gIGJvcmRlci1ib3R0b20tbGVmdC1yYWRpdXM6IHZhcigtLWJvcmRlci1yYWRpdXMpO1xuICBib3JkZXItYm90dG9tLXJpZ2h0LXJhZGl1czogdmFyKC0tYm9yZGVyLXJhZGl1cyk7XG4gIGJveC1zaGFkb3c6IHZhcigtLWVsZXZhdGlvbi16NCk7XG4gIG1heC13aWR0aDogMTAwdnc7XG4gIG92ZXJmbG93OiBoaWRkZW47XG4gIHdpZHRoOiAzNTBweDtcbiAgYm9yZGVyLXJhZGl1czogMC4yNXJlbTtcbn1cblxuLmRyb3Bkb3duLWhlYWRlciB7XG4gIGJveC1zaGFkb3c6IHZhcigtLWVsZXZhdGlvbi16Nik7XG4gIHBhZGRpbmctdG9wOiAxcmVtO1xuICBwYWRkaW5nLWJvdHRvbTogMXJlbTtcbiAgcGFkZGluZy1sZWZ0OiAxLjVyZW07XG4gIHBhZGRpbmctcmlnaHQ6IDEuNXJlbTtcbn1cblxuLmRyb3Bkb3duLWhlYWRpbmcge1xuICBmb250OiB2YXIoLS1mb250LXRpdGxlKTtcbn1cblxuLmRyb3Bkb3duLWNvbnRlbnQge1xuICBtYXgtaGVpZ2h0OiAyOTFweDtcbiAgb3ZlcmZsb3cteDogaGlkZGVuO1xuICBvdmVyZmxvdy15OiBhdXRvO1xuICBwYWRkaW5nOiAxMHB4O1xufVxuXG4uZHJvcGRvd24tZm9vdGVyIHtcbiAgYmFja2dyb3VuZDogdmFyKC0tYmFja2dyb3VuZC1hcHAtYmFyKTtcbiAgYm9yZGVyLXRvcDogMXB4IHNvbGlkIHZhcigtLWZvcmVncm91bmQtZGl2aWRlcik7XG4gIHBhZGRpbmc6IHZhcigtLXBhZGRpbmctOCkgdmFyKC0tcGFkZGluZyk7XG59XG5cbi5ub3RpZmljYXRpb24ge1xuICBjb2xvcjogdmFyKC0tdGV4dC1jb2xvcik7XG4gIHBhZGRpbmc6IHZhcigtLXBhZGRpbmctMTYpIHZhcigtLXBhZGRpbmcpO1xuICBwb3NpdGlvbjogcmVsYXRpdmU7XG4gIHRleHQtZGVjb3JhdGlvbjogbm9uZTtcbiAgdHJhbnNpdGlvbjogdmFyKC0tdHJhbnMtZWFzZS1vdXQpO1xuICB1c2VyLXNlbGVjdDogbm9uZTtcbn1cblxuLm5vdGlmaWNhdGlvbjpob3ZlciB7XG4gIGJhY2tncm91bmQ6IHZhcigtLWJhY2tncm91bmQtaG92ZXIpO1xufVxuXG4ubm90aWZpY2F0aW9uOmhvdmVyIC5ub3RpZmljYXRpb24tbGFiZWwge1xuICAtLXRleHQtb3BhY2l0eTogMTtcbiAgY29sb3I6ICM1Yzc3ZmY7XG4gIGNvbG9yOiByZ2JhKDkyLCAxMTksIDI1NSwgdmFyKC0tdGV4dC1vcGFjaXR5KSk7XG59XG5cbi5ub3RpZmljYXRpb24ucmVhZCB7XG4gIG9wYWNpdHk6IDAuNTtcbn1cblxuLm5vdGlmaWNhdGlvbi1pY29uIHtcbiAgbWFyZ2luLWlubGluZS1lbmQ6IHZhcigtLXBhZGRpbmcpO1xufVxuXG4ubm90aWZpY2F0aW9uLWxhYmVsIHtcbiAgdHJhbnNpdGlvbjogaW5oZXJpdDtcbn1cblxuLm5vdGlmaWNhdGlvbi1kZXNjcmlwdGlvbiB7XG4gIGNvbG9yOiB2YXIoLS10ZXh0LXNlY29uZGFyeSk7XG4gIGZvbnQ6IHZhcigtLWZvbnQtY2FwdGlvbik7XG59XG5cbi5ub3RpZmljYXRpb24tY2hldnJvbiB7XG4gIGNvbG9yOiB2YXIoLS10ZXh0LWhpbnQpO1xuICBmb250LXNpemU6IDE4cHg7XG4gIGhlaWdodDogMThweDtcbiAgd2lkdGg6IDE4cHg7XG59XG5cbi5ub3RpZmljYXRpb24gKyAubm90aWZpY2F0aW9uIHtcbiAgYm9yZGVyLXRvcDogMXB4IHNvbGlkIHZhcigtLWZvcmVncm91bmQtZGl2aWRlcik7XG59XG5cbi5pbnB1dC1idXR0b24ge1xuICBtYXJnaW4tdG9wOiA4cHg7XG59Il19 */");

/***/ }),

/***/ "Sl3+":
/*!**************************************!*\
  !*** ./src/@vex/utils/merge-deep.ts ***!
  \**************************************/
/*! exports provided: mergeDeep */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "mergeDeep", function() { return mergeDeep; });
/**
 * Performs a deep merge of `source` into `target`.
 * Mutates `target` only but not its objects and arrays.
 *
 * @author inspired by [jhildenbiddle](https://stackoverflow.com/a/48218209).
 */
function mergeDeep(target, source) {
    const isObject = (obj) => obj && typeof obj === 'object';
    if (!isObject(target) || !isObject(source)) {
        return source;
    }
    Object.keys(source).forEach(key => {
        const targetValue = target[key];
        const sourceValue = source[key];
        if (Array.isArray(targetValue) && Array.isArray(sourceValue)) {
            target[key] = targetValue.concat(sourceValue);
        }
        else if (isObject(targetValue) && isObject(sourceValue)) {
            target[key] = mergeDeep(Object.assign({}, targetValue), sourceValue);
        }
        else {
            target[key] = sourceValue;
        }
    });
    return target;
}


/***/ }),

/***/ "Sxwf":
/*!*****************************************!*\
  !*** ./src/app/data/schema/scenario.ts ***!
  \*****************************************/
/*! exports provided: Scenario, ScenarioPriorities, ScenarioPriorityData */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Scenario", function() { return Scenario; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ScenarioPriorities", function() { return ScenarioPriorities; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ScenarioPriorityData", function() { return ScenarioPriorityData; });
class Scenario {
    constructor(scenario) {
        this.id = scenario.id;
        this.name = scenario.name;
        this.description = scenario.description;
        this.createdAt = new Date(scenario.created_at);
        this.updatedAt = new Date(scenario.updated_at);
        this.createdBy = scenario.createdBy;
        this.labels = scenario.labels;
        this.requestCount = scenario.request_count;
        this.starred = scenario.starred;
        this.priority = scenario.priority;
        this.mockUrl = scenario.mock_url;
        this.key = scenario.key;
        this.projectId = scenario.project_id;
    }
}
var ScenarioPriorities;
(function (ScenarioPriorities) {
    ScenarioPriorities[ScenarioPriorities["None"] = 0] = "None";
    ScenarioPriorities[ScenarioPriorities["Low"] = 1] = "Low";
    ScenarioPriorities[ScenarioPriorities["Medium"] = 2] = "Medium";
    ScenarioPriorities[ScenarioPriorities["High"] = 3] = "High";
})(ScenarioPriorities || (ScenarioPriorities = {}));
const ScenarioPriorityData = [
    {
        name: ScenarioPriorities[3],
        classes: 'text-primary-500',
        value: 3,
    },
    {
        name: ScenarioPriorities[2],
        classes: 'text-green-500',
        value: 2,
    },
    {
        name: ScenarioPriorities[1],
        classes: 'text-amber-500',
        value: 1,
    },
    {
        name: ScenarioPriorities[0],
        classes: 'text-gray-500',
        value: 0,
    },
];


/***/ }),

/***/ "Sy1n":
/*!**********************************!*\
  !*** ./src/app/app.component.ts ***!
  \**********************************/
/*! exports provided: AppComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AppComponent", function() { return AppComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_app_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./app.component.html */ "VzVu");
/* harmony import */ var _app_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./app.component.scss */ "ynWL");
/* harmony import */ var _angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/cdk/coercion */ "8LU1");
/* harmony import */ var _angular_cdk_platform__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/cdk/platform */ "SCoL");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var luxon__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! luxon */ "ExVU");
/* harmony import */ var luxon__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(luxon__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! rxjs/operators */ "kU1M");
/* harmony import */ var _iconify_icons_ic_collections__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @iconify/icons-ic/collections */ "nn58");
/* harmony import */ var _iconify_icons_ic_collections__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_collections__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _iconify_icons_ic_link__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @iconify/icons-ic/link */ "Pi/6");
/* harmony import */ var _iconify_icons_ic_link__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_link__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var _iconify_icons_ic_list__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @iconify/icons-ic/list */ "mb2K");
/* harmony import */ var _iconify_icons_ic_list__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_list__WEBPACK_IMPORTED_MODULE_12__);
/* harmony import */ var _iconify_icons_ic_settings__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @iconify/icons-ic/settings */ "Ijxr");
/* harmony import */ var _iconify_icons_ic_settings__WEBPACK_IMPORTED_MODULE_13___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_settings__WEBPACK_IMPORTED_MODULE_13__);
/* harmony import */ var _iconify_icons_ic_twotone_layers__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @iconify/icons-ic/twotone-layers */ "7nbV");
/* harmony import */ var _iconify_icons_ic_twotone_layers__WEBPACK_IMPORTED_MODULE_14___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_layers__WEBPACK_IMPORTED_MODULE_14__);
/* harmony import */ var _vex_services_config_service__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @vex/services/config.service */ "lC2v");
/* harmony import */ var _vex_services_layout_service__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @vex/services/layout.service */ "CtTw");
/* harmony import */ var _vex_services_navigation_service__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @vex/services/navigation.service */ "0vMP");
/* harmony import */ var _vex_services_splash_screen_service__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @vex/services/splash-screen.service */ "AQ4D");
/* harmony import */ var _vex_services_style_service__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! @vex/services/style.service */ "Z+W5");
/* harmony import */ var _layout_services_layout_config_service__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! @layout/services/layout-config.service */ "U9Lm");
/* harmony import */ var _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! @projects/services/project-data.service */ "oyjd");






















let AppComponent = class AppComponent {
    constructor(document, localeId, configService, layoutService, layoutConfigService, navigationService, platform, projectDataService, renderer, route, router, splashScreenService, styleService) {
        this.document = document;
        this.localeId = localeId;
        this.configService = configService;
        this.layoutService = layoutService;
        this.layoutConfigService = layoutConfigService;
        this.navigationService = navigationService;
        this.platform = platform;
        this.projectDataService = projectDataService;
        this.renderer = renderer;
        this.route = route;
        this.router = router;
        this.splashScreenService = splashScreenService;
        this.styleService = styleService;
        this.title = 'vex';
        luxon__WEBPACK_IMPORTED_MODULE_8__["Settings"].defaultLocale = this.localeId;
        if (this.platform.BLINK) {
            this.renderer.addClass(this.document.body, 'is-blink');
        }
        // Set theme configurations
        this.configService.setConfig('vex-layout-zeus');
        // this.styleService.setStyle('light' as Style);
        // Define navbar
        this.navigationService.items = [
            {
                type: 'link',
                label: 'Projects',
                route: '/projects',
                isVisible: () => false,
                handleClick: () => {
                    this.showPath('/projects');
                },
                icon: _iconify_icons_ic_collections__WEBPACK_IMPORTED_MODULE_10___default.a,
            },
            {
                type: 'link',
                label: 'Requests',
                route: '/requests',
                isVisible: () => this.isProject(),
                handleClick: () => {
                    this.showPath('/requests');
                },
                icon: _iconify_icons_ic_link__WEBPACK_IMPORTED_MODULE_11___default.a,
            },
            {
                type: 'link',
                label: 'Scenarios',
                route: '/scenarios',
                isVisible: () => this.isProject(),
                handleClick: () => {
                    this.showPath('/scenarios');
                },
                icon: _iconify_icons_ic_list__WEBPACK_IMPORTED_MODULE_12___default.a,
            },
            {
                type: 'link',
                label: 'Endpoints',
                route: '/endpoints',
                isVisible: () => this.isProject(),
                handleClick: () => {
                    this.showPath('/endpoints');
                },
                icon: _iconify_icons_ic_twotone_layers__WEBPACK_IMPORTED_MODULE_14___default.a,
            },
            // {
            //   type: 'link',
            //   label: 'Aliases',
            //   route: '/aliases',
            //   isVisible: () => this.isProject(),
            //   onclick: () => {
            //     this.showPath('/aliases');
            //   },
            //   icon: icLayers
            // },
            {
                type: 'link',
                label: 'Settings',
                route: '/projects',
                isVisible: () => this.isProject(),
                handleClick: () => {
                    this.showSettingsPath();
                },
                icon: _iconify_icons_ic_settings__WEBPACK_IMPORTED_MODULE_13___default.a,
            },
        ];
        /**
         * Config Related Subscriptions
         * You can remove this if you don't need the functionality of being able to enable specific configs with queryParams
         * Example: example.com/?layout=apollo&style=default
         */
        this.route.queryParamMap.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_9__["filter"])(queryParamMap => queryParamMap.has('rtl') && Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_3__["coerceBooleanProperty"])(queryParamMap.get('rtl')))).subscribe(queryParamMap => {
            this.document.body.dir = 'rtl';
            this.configService.updateConfig({
                rtl: true,
            });
        });
        this.route.queryParamMap.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_9__["filter"])(queryParamMap => queryParamMap.has('layout'))).subscribe(queryParamMap => this.configService.setConfig(queryParamMap.get('layout')));
        this.route.queryParamMap.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_9__["filter"])(queryParamMap => queryParamMap.has('style'))).subscribe(queryParamMap => this.styleService.setStyle(queryParamMap.get('style')));
    } // constructor
    // View Access
    showPath(path) {
        const project = this.projectDataService.project || {};
        const snapshot = this.route.snapshot;
        const projectId = snapshot.queryParams.project_id || project.id;
        if (path !== this.getResolvedPath(snapshot)) {
            this.router.navigate([path], {
                queryParams: { project_id: projectId },
            });
        }
    }
    showSettingsPath() {
        const project = this.projectDataService.project || {};
        const snapshot = this.route.snapshot;
        const projectId = snapshot.queryParams.project_id || project.id;
        const path = `/projects/${projectId}/settings`;
        this.router.navigate([path]);
    }
    // Helpers
    getResolvedPath(route) {
        return route.pathFromRoot
            .map(v => v.url.map(segment => segment.toString()).join('/'))
            .join('/');
    }
    isProject() {
        return this.layoutConfigService.isProject();
    }
};
AppComponent.ctorParameters = () => [
    { type: Document, decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Inject"], args: [_angular_common__WEBPACK_IMPORTED_MODULE_5__["DOCUMENT"],] }] },
    { type: String, decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Inject"], args: [_angular_core__WEBPACK_IMPORTED_MODULE_6__["LOCALE_ID"],] }] },
    { type: _vex_services_config_service__WEBPACK_IMPORTED_MODULE_15__["ConfigService"] },
    { type: _vex_services_layout_service__WEBPACK_IMPORTED_MODULE_16__["LayoutService"] },
    { type: _layout_services_layout_config_service__WEBPACK_IMPORTED_MODULE_20__["LayoutConfigService"] },
    { type: _vex_services_navigation_service__WEBPACK_IMPORTED_MODULE_17__["NavigationService"] },
    { type: _angular_cdk_platform__WEBPACK_IMPORTED_MODULE_4__["Platform"] },
    { type: _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_21__["ProjectDataService"] },
    { type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Renderer2"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_7__["ActivatedRoute"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_7__["Router"] },
    { type: _vex_services_splash_screen_service__WEBPACK_IMPORTED_MODULE_18__["SplashScreenService"] },
    { type: _vex_services_style_service__WEBPACK_IMPORTED_MODULE_19__["StyleService"] }
];
AppComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_6__["Component"])({
        selector: 'vex-root',
        template: _raw_loader_app_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_app_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], AppComponent);



/***/ }),

/***/ "T+qy":
/*!********************************************************!*\
  !*** ./src/app/core/http/endpoint-resource.service.ts ***!
  \********************************************************/
/*! exports provided: EndpointResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "EndpointResource", function() { return EndpointResource; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _rest_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rest-api.service */ "iCaw");



let EndpointResource = class EndpointResource {
    constructor(restApi) {
        this.restApi = restApi;
        this.ENDPOINT = 'endpoints';
    }
    index(queryParams) {
        return this.restApi.index([this.ENDPOINT], queryParams);
    }
    show(id, queryParams) {
        return this.restApi.show([this.ENDPOINT, id], queryParams);
    }
    create(body) {
        return this.restApi.create([this.ENDPOINT], body);
    }
    update(id, body) {
        return this.restApi.update([this.ENDPOINT, id], body);
    }
    destroy(id) {
        return this.restApi.destroy([this.ENDPOINT, id]);
    }
};
EndpointResource.ctorParameters = () => [
    { type: _rest_api_service__WEBPACK_IMPORTED_MODULE_2__["RestApiService"] }
];
EndpointResource = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], EndpointResource);



/***/ }),

/***/ "T/nk":
/*!***************************************************!*\
  !*** ./src/@vex/animations/dropdown.animation.ts ***!
  \***************************************************/
/*! exports provided: dropdownAnimation */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "dropdownAnimation", function() { return dropdownAnimation; });
/* harmony import */ var _angular_animations__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/animations */ "GS7A");

const dropdownAnimation = Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["trigger"])('dropdown', [
    Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["state"])('false', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["style"])({
        height: 0,
        opacity: 0
    })),
    Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["state"])('true', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["style"])({
        height: '*',
        opacity: 1
    })),
    Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["transition"])('false <=> true', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["animate"])('300ms cubic-bezier(.35, 0, .25, 1)'))
]);


/***/ }),

/***/ "TE1C":
/*!****************************************************!*\
  !*** ./src/app/core/http/plan-resource.service.ts ***!
  \****************************************************/
/*! exports provided: PlanResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PlanResource", function() { return PlanResource; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _rest_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rest-api.service */ "iCaw");



let PlanResource = class PlanResource {
    constructor(restApi) {
        this.restApi = restApi;
        this.ENDPOINT = 'plans';
    }
    index(queryParams) {
        return this.restApi.index([this.ENDPOINT], queryParams);
    }
    show(id, queryParams) {
        return this.restApi.show([this.ENDPOINT, id], queryParams);
    }
    create(body) {
        return this.restApi.create([this.ENDPOINT], body);
    }
    update(id, body) {
        return this.restApi.update([this.ENDPOINT, id], body);
    }
    destroy(id) {
        return this.restApi.destroy([this.ENDPOINT, id]);
    }
};
PlanResource.ctorParameters = () => [
    { type: _rest_api_service__WEBPACK_IMPORTED_MODULE_2__["RestApiService"] }
];
PlanResource = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], PlanResource);



/***/ }),

/***/ "TphN":
/*!*****************************************************!*\
  !*** ./src/@vex/components/footer/footer.module.ts ***!
  \*****************************************************/
/*! exports provided: FooterModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FooterModule", function() { return FooterModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _directives_container_container_module__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../directives/container/container.module */ "68Yx");
/* harmony import */ var _footer_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./footer.component */ "YUAm");








let FooterModule = class FooterModule {
};
FooterModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_4__["MatButtonModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_5__["IconModule"],
            _directives_container_container_module__WEBPACK_IMPORTED_MODULE_6__["ContainerModule"]
        ],
        declarations: [_footer_component__WEBPACK_IMPORTED_MODULE_7__["FooterComponent"]],
        exports: [_footer_component__WEBPACK_IMPORTED_MODULE_7__["FooterComponent"]]
    })
], FooterModule);



/***/ }),

/***/ "U9Lm":
/*!**********************************************************!*\
  !*** ./src/app/layout/services/layout-config.service.ts ***!
  \**********************************************************/
/*! exports provided: LayoutConfigService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LayoutConfigService", function() { return LayoutConfigService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var angular_token__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! angular-token */ "hU4o");
/* harmony import */ var _vex_services_config_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @vex/services/config.service */ "lC2v");
/* harmony import */ var _vex_services_style_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @vex/services/style.service */ "Z+W5");
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @environments/environment */ "AytR");
/* harmony import */ var _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @projects/services/project-data.service */ "oyjd");








let LayoutConfigService = class LayoutConfigService {
    constructor(configService, projectDataService, route, styleService, tokenService) {
        this.configService = configService;
        this.projectDataService = projectDataService;
        this.route = route;
        this.styleService = styleService;
        this.tokenService = tokenService;
    }
    setIkaros() {
        this.configService.setConfig('vex-layout-ikaros');
        // this.styleService.setStyle('default' as Style);
    }
    setZeus() {
        this.configService.setConfig('vex-layout-zeus');
    }
    isProxied() {
        return !!_environments_environment__WEBPACK_IMPORTED_MODULE_6__["environment"].agentUrl;
    }
    isSignedIn() {
        return this.tokenService.userSignedIn();
    }
    isProject() {
        const pathname = location.pathname;
        if (pathname === '/projects')
            return false;
        const pathSegments = pathname.split('/');
        pathSegments.shift(); // Get rid of empty string
        return ['projects', 'requests', 'endpoints', 'scenarios'].includes(pathSegments[0]);
    }
};
LayoutConfigService.ctorParameters = () => [
    { type: _vex_services_config_service__WEBPACK_IMPORTED_MODULE_4__["ConfigService"] },
    { type: _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_7__["ProjectDataService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"] },
    { type: _vex_services_style_service__WEBPACK_IMPORTED_MODULE_5__["StyleService"] },
    { type: angular_token__WEBPACK_IMPORTED_MODULE_3__["AngularTokenService"] }
];
LayoutConfigService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], LayoutConfigService);



/***/ }),

/***/ "UY+R":
/*!******************************************************************************************!*\
  !*** ./src/app/layout/components/toolbar/components/toolbar-user/toolbar-user.module.ts ***!
  \******************************************************************************************/
/*! exports provided: ToolbarUserModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ToolbarUserModule", function() { return ToolbarUserModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_material_core__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/core */ "UhP/");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _angular_material_menu__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/menu */ "rJgo");
/* harmony import */ var _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/material/tooltip */ "ZFy/");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _vex_components_popover_popover_module__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @vex/components/popover/popover.module */ "gX/z");
/* harmony import */ var _vex_pipes_color_color_fade_module__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @vex/pipes/color/color-fade.module */ "Chvm");
/* harmony import */ var _vex_pipes_relative_date_time_relative_date_time_module__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @vex/pipes/relative-date-time/relative-date-time.module */ "h4uD");
/* harmony import */ var _toolbar_user_dropdown_toolbar_user_dropdown_component__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./toolbar-user-dropdown/toolbar-user-dropdown.component */ "dGqQ");
/* harmony import */ var _toolbar_user_component__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ./toolbar-user.component */ "cD1t");
















let ToolbarUserModule = class ToolbarUserModule {
};
ToolbarUserModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_toolbar_user_component__WEBPACK_IMPORTED_MODULE_15__["ToolbarUserComponent"], _toolbar_user_dropdown_toolbar_user_dropdown_component__WEBPACK_IMPORTED_MODULE_14__["ToolbarUserDropdownComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_6__["MatIconModule"],
            _angular_material_core__WEBPACK_IMPORTED_MODULE_5__["MatRippleModule"],
            _angular_material_menu__WEBPACK_IMPORTED_MODULE_7__["MatMenuModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_4__["MatButtonModule"],
            _vex_pipes_relative_date_time_relative_date_time_module__WEBPACK_IMPORTED_MODULE_13__["RelativeDateTimeModule"],
            _angular_router__WEBPACK_IMPORTED_MODULE_9__["RouterModule"],
            _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_8__["MatTooltipModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_10__["IconModule"],
            _vex_pipes_color_color_fade_module__WEBPACK_IMPORTED_MODULE_12__["ColorFadeModule"],
            _vex_components_popover_popover_module__WEBPACK_IMPORTED_MODULE_11__["PopoverModule"],
        ],
        exports: [_toolbar_user_component__WEBPACK_IMPORTED_MODULE_15__["ToolbarUserComponent"]],
        entryComponents: [_toolbar_user_dropdown_toolbar_user_dropdown_component__WEBPACK_IMPORTED_MODULE_14__["ToolbarUserDropdownComponent"]],
    })
], ToolbarUserModule);



/***/ }),

/***/ "UZWc":
/*!*******************************************************************************************************************!*\
  !*** ./src/app/layout/components/toolbar/components/toolbar-proxy-settings/toolbar-proxy-settings.component.scss ***!
  \*******************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJ0b29sYmFyLXByb3h5LXNldHRpbmdzLmNvbXBvbmVudC5zY3NzIn0= */");

/***/ }),

/***/ "V99k":
/*!**************************************!*\
  !*** ./src/app/data/schema/index.ts ***!
  \**************************************/
/*! exports provided: AliasValue, Alias, BodyParam, Endpoint, EndpointCategories, Header, OrganizationsUser, OrganizationsUserRoles, OrganizationsUserRoleTitles, Organization, PathSegment, Project, QueryParam, RequestComponent, RequestComponentType, Request, RequestPriorities, RequestPriorityData, Response, ResponseHeader, Scenario, ScenarioPriorities, ScenarioPriorityData, User, Plan, Subscription, ProjectsUser, ProjectsUserRoles, ProjectsUserRoleTitles, PaymentMethod, PaymentMethodCard */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _alias_value__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./alias-value */ "P9CE");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "AliasValue", function() { return _alias_value__WEBPACK_IMPORTED_MODULE_0__["AliasValue"]; });

/* harmony import */ var _alias__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./alias */ "tpJP");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Alias", function() { return _alias__WEBPACK_IMPORTED_MODULE_1__["Alias"]; });

/* harmony import */ var _body_param__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./body-param */ "Y7fp");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "BodyParam", function() { return _body_param__WEBPACK_IMPORTED_MODULE_2__["BodyParam"]; });

/* harmony import */ var _endpoint__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./endpoint */ "jBLc");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Endpoint", function() { return _endpoint__WEBPACK_IMPORTED_MODULE_3__["Endpoint"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "EndpointCategories", function() { return _endpoint__WEBPACK_IMPORTED_MODULE_3__["EndpointCategories"]; });

/* harmony import */ var _header__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./header */ "rpPS");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Header", function() { return _header__WEBPACK_IMPORTED_MODULE_4__["Header"]; });

/* harmony import */ var _organizations_user__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./organizations-user */ "FKbl");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "OrganizationsUser", function() { return _organizations_user__WEBPACK_IMPORTED_MODULE_5__["OrganizationsUser"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "OrganizationsUserRoles", function() { return _organizations_user__WEBPACK_IMPORTED_MODULE_5__["OrganizationsUserRoles"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "OrganizationsUserRoleTitles", function() { return _organizations_user__WEBPACK_IMPORTED_MODULE_5__["OrganizationsUserRoleTitles"]; });

/* harmony import */ var _organization__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./organization */ "7v+O");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Organization", function() { return _organization__WEBPACK_IMPORTED_MODULE_6__["Organization"]; });

/* harmony import */ var _path_segment__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./path-segment */ "+fow");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "PathSegment", function() { return _path_segment__WEBPACK_IMPORTED_MODULE_7__["PathSegment"]; });

/* harmony import */ var _project__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./project */ "2RYP");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Project", function() { return _project__WEBPACK_IMPORTED_MODULE_8__["Project"]; });

/* harmony import */ var _query_param__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./query-param */ "u7xO");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "QueryParam", function() { return _query_param__WEBPACK_IMPORTED_MODULE_9__["QueryParam"]; });

/* harmony import */ var _request_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./request-component */ "2bXN");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "RequestComponent", function() { return _request_component__WEBPACK_IMPORTED_MODULE_10__["RequestComponent"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "RequestComponentType", function() { return _request_component__WEBPACK_IMPORTED_MODULE_10__["RequestComponentType"]; });

/* harmony import */ var _request__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./request */ "WYQo");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Request", function() { return _request__WEBPACK_IMPORTED_MODULE_11__["Request"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "RequestPriorities", function() { return _request__WEBPACK_IMPORTED_MODULE_11__["RequestPriorities"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "RequestPriorityData", function() { return _request__WEBPACK_IMPORTED_MODULE_11__["RequestPriorityData"]; });

/* harmony import */ var _response__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./response */ "M0zT");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Response", function() { return _response__WEBPACK_IMPORTED_MODULE_12__["Response"]; });

/* harmony import */ var _response_header__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./response-header */ "j+4c");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "ResponseHeader", function() { return _response_header__WEBPACK_IMPORTED_MODULE_13__["ResponseHeader"]; });

/* harmony import */ var _scenario__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./scenario */ "Sxwf");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Scenario", function() { return _scenario__WEBPACK_IMPORTED_MODULE_14__["Scenario"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "ScenarioPriorities", function() { return _scenario__WEBPACK_IMPORTED_MODULE_14__["ScenarioPriorities"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "ScenarioPriorityData", function() { return _scenario__WEBPACK_IMPORTED_MODULE_14__["ScenarioPriorityData"]; });

/* harmony import */ var _user__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ./user */ "/8CK");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "User", function() { return _user__WEBPACK_IMPORTED_MODULE_15__["User"]; });

/* harmony import */ var _plan__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ./plan */ "L3CV");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Plan", function() { return _plan__WEBPACK_IMPORTED_MODULE_16__["Plan"]; });

/* harmony import */ var _subscription__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! ./subscription */ "8IoH");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Subscription", function() { return _subscription__WEBPACK_IMPORTED_MODULE_17__["Subscription"]; });

/* harmony import */ var _projects_user__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! ./projects-user */ "D9MS");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "ProjectsUser", function() { return _projects_user__WEBPACK_IMPORTED_MODULE_18__["ProjectsUser"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "ProjectsUserRoles", function() { return _projects_user__WEBPACK_IMPORTED_MODULE_18__["ProjectsUserRoles"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "ProjectsUserRoleTitles", function() { return _projects_user__WEBPACK_IMPORTED_MODULE_18__["ProjectsUserRoleTitles"]; });

/* harmony import */ var _payment_method__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! ./payment-method */ "vuK5");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "PaymentMethod", function() { return _payment_method__WEBPACK_IMPORTED_MODULE_19__["PaymentMethod"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "PaymentMethodCard", function() { return _payment_method__WEBPACK_IMPORTED_MODULE_19__["PaymentMethodCard"]; });























/***/ }),

/***/ "VzVu":
/*!**************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/app.component.html ***!
  \**************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<router-outlet></router-outlet>\n\n");

/***/ }),

/***/ "W9UW":
/*!***************************************************!*\
  !*** ./src/@vex/layout/sidenav/sidenav.module.ts ***!
  \***************************************************/
/*! exports provided: SidenavModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SidenavModule", function() { return SidenavModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _angular_material_toolbar__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/toolbar */ "l0rg");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _components_scrollbar_scrollbar_module__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../components/scrollbar/scrollbar.module */ "XVi8");
/* harmony import */ var _components_sidenav_item_sidenav_item_module__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../components/sidenav-item/sidenav-item.module */ "YGXf");
/* harmony import */ var _sidenav_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./sidenav.component */ "7JzS");











let SidenavModule = class SidenavModule {
};
SidenavModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_sidenav_component__WEBPACK_IMPORTED_MODULE_10__["SidenavComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_material_toolbar__WEBPACK_IMPORTED_MODULE_6__["MatToolbarModule"],
            _components_sidenav_item_sidenav_item_module__WEBPACK_IMPORTED_MODULE_9__["SidenavItemModule"],
            _components_scrollbar_scrollbar_module__WEBPACK_IMPORTED_MODULE_8__["ScrollbarModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_4__["MatButtonModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_5__["MatIconModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_7__["IconModule"]
        ],
        exports: [_sidenav_component__WEBPACK_IMPORTED_MODULE_10__["SidenavComponent"]]
    })
], SidenavModule);



/***/ }),

/***/ "WYQo":
/*!****************************************!*\
  !*** ./src/app/data/schema/request.ts ***!
  \****************************************/
/*! exports provided: Request, RequestPriorities, RequestPriorityData */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Request", function() { return Request; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RequestPriorities", function() { return RequestPriorities; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RequestPriorityData", function() { return RequestPriorityData; });
class Request {
    constructor(request) {
        this.components = request.components;
        this.createdAt = new Date(request.created_at);
        this.endpoint = request.endpoint;
        this.endpointId = request.endpoint_id;
        this.host = request.host;
        this.id = request.id;
        this.latency = request.latency;
        this.method = request.method;
        this.port = request.port;
        this.position = request.position;
        this.priority = 0;
        this.rollupId = request.rollup_id;
        this.projectId = request.project_id;
        this.starred = false;
        this.status = request.status;
        this.url = request.url;
        if (request.headers) {
            this.headers = request.headers;
        }
        if (request.queryParams) {
            this.queryParams = request.query_params;
        }
    }
}
var RequestPriorities;
(function (RequestPriorities) {
    RequestPriorities[RequestPriorities["None"] = 0] = "None";
    RequestPriorities[RequestPriorities["Low"] = 1] = "Low";
    RequestPriorities[RequestPriorities["Medium"] = 2] = "Medium";
    RequestPriorities[RequestPriorities["High"] = 3] = "High";
})(RequestPriorities || (RequestPriorities = {}));
const RequestPriorityData = [
    {
        name: RequestPriorities[3],
        classes: 'text-primary-500',
        value: 3,
    },
    {
        name: RequestPriorities[2],
        classes: 'text-green-500',
        value: 2,
    },
    {
        name: RequestPriorities[1],
        classes: 'text-amber-500',
        value: 1,
    },
    {
        name: RequestPriorities[0],
        classes: 'text-gray-500',
        value: 0,
    },
];


/***/ }),

/***/ "WYjc":
/*!********************************************************************!*\
  !*** ./src/@vex/components/progress-bar/progress-bar.component.ts ***!
  \********************************************************************/
/*! exports provided: ProgressBarComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProgressBarComponent", function() { return ProgressBarComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_progress_bar_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./progress-bar.component.html */ "KD9O");
/* harmony import */ var _progress_bar_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./progress-bar.component.scss */ "PC2b");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _ngx_loading_bar_core__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @ngx-loading-bar/core */ "TtxX");





let ProgressBarComponent = class ProgressBarComponent {
    constructor(loader) {
        this.loader = loader;
    }
    ngOnInit() {
    }
};
ProgressBarComponent.ctorParameters = () => [
    { type: _ngx_loading_bar_core__WEBPACK_IMPORTED_MODULE_4__["LoadingBarService"] }
];
ProgressBarComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'vex-progress-bar',
        template: _raw_loader_progress_bar_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_progress_bar_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], ProgressBarComponent);



/***/ }),

/***/ "Wbda":
/*!******************************************************!*\
  !*** ./src/app/core/http/header-resource.service.ts ***!
  \******************************************************/
/*! exports provided: HeaderResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "HeaderResource", function() { return HeaderResource; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _rest_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rest-api.service */ "iCaw");



let HeaderResource = class HeaderResource {
    constructor(restApi) {
        this.restApi = restApi;
        this.REQUEST_ENDPOINT = 'requests';
        this.ENDPOINT = 'headers';
    }
    index(requestId, queryParams) {
        if (typeof requestId === 'object') {
            queryParams = requestId;
            return this.restApi.index([this.ENDPOINT], queryParams);
        }
        else {
            return this.restApi.index([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT], queryParams);
        }
    }
    show(requestId, id, queryParams) {
        return this.restApi.show([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT, id], queryParams);
    }
    create(requestId, body) {
        return this.restApi.create([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT], body);
    }
    update(requestId, id, body) {
        return this.restApi.update([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT, id], body);
    }
    destroy(requestId, id, queryParams) {
        return this.restApi.destroy([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT, id], queryParams);
    }
};
HeaderResource.ctorParameters = () => [
    { type: _rest_api_service__WEBPACK_IMPORTED_MODULE_2__["RestApiService"] }
];
HeaderResource = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], HeaderResource);



/***/ }),

/***/ "XTWy":
/*!*************************************************************!*\
  !*** ./src/app/core/http/projects-user-resource.service.ts ***!
  \*************************************************************/
/*! exports provided: ProjectsUserResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectsUserResource", function() { return ProjectsUserResource; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _rest_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rest-api.service */ "iCaw");



let ProjectsUserResource = class ProjectsUserResource {
    constructor(restApi) {
        this.restApi = restApi;
        this.PROJECT_ENDPOINT = 'projects';
        this.ENDPOINT = 'users';
    }
    index(projectId, queryParams) {
        return this.restApi.index([this.PROJECT_ENDPOINT, projectId, this.ENDPOINT], queryParams);
    }
    show(projectId, id, queryParams) {
        return this.restApi.show([this.PROJECT_ENDPOINT, projectId, this.ENDPOINT, id], queryParams);
    }
    create(projectId, body) {
        return this.restApi.create([this.PROJECT_ENDPOINT, projectId, this.ENDPOINT], body);
    }
    update(projectId, id, body) {
        return this.restApi.update([this.PROJECT_ENDPOINT, projectId, this.ENDPOINT, id], body);
    }
    destroy(projectId, id) {
        return this.restApi.destroy([this.PROJECT_ENDPOINT, projectId, this.ENDPOINT, id]);
    }
};
ProjectsUserResource.ctorParameters = () => [
    { type: _rest_api_service__WEBPACK_IMPORTED_MODULE_2__["RestApiService"] }
];
ProjectsUserResource = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], ProjectsUserResource);



/***/ }),

/***/ "XVi8":
/*!***********************************************************!*\
  !*** ./src/@vex/components/scrollbar/scrollbar.module.ts ***!
  \***********************************************************/
/*! exports provided: ScrollbarModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ScrollbarModule", function() { return ScrollbarModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _scrollbar_directive__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./scrollbar.directive */ "/7a8");




let ScrollbarModule = class ScrollbarModule {
};
ScrollbarModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_scrollbar_directive__WEBPACK_IMPORTED_MODULE_3__["ScrollbarDirective"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"]
        ],
        exports: [_scrollbar_directive__WEBPACK_IMPORTED_MODULE_3__["ScrollbarDirective"]]
    })
], ScrollbarModule);



/***/ }),

/***/ "XXSj":
/*!***************************************!*\
  !*** ./src/@vex/utils/tailwindcss.ts ***!
  \***************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var tailwindcss_resolveConfig__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tailwindcss/resolveConfig */ "HA0i");
/* harmony import */ var tailwindcss_resolveConfig__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(tailwindcss_resolveConfig__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _tailwind_config__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../tailwind.config */ "0mz7");
/* harmony import */ var _tailwind_config__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_tailwind_config__WEBPACK_IMPORTED_MODULE_1__);


const theme = tailwindcss_resolveConfig__WEBPACK_IMPORTED_MODULE_0___default()(_tailwind_config__WEBPACK_IMPORTED_MODULE_1___default.a).theme;
/* harmony default export */ __webpack_exports__["default"] = (theme);


/***/ }),

/***/ "Xuwo":
/*!******************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/@vex/components/mega-menu/mega-menu.component.html ***!
  \******************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div [ngClass.gt-sm]=\"['mr-6']\" class=\"card overflow-auto\" fxLayout=\"row\" fxLayout.lt-md=\"column\">\n  <div class=\"bg-primary-500 text-primary-contrast-500 p-gutter\" fxFlex=\"300px\" fxFlex.lt-md=\"auto\">\n    <h2 class=\"headline mb-4\">Mega Menu</h2>\n\n    <p class=\"caption\">Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there\n      live the blind\n      texts.</p>\n\n    <p class=\"caption\">Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language\n      ocean.</p>\n\n    <button class=\"border border-primary-contrast border-solid mt-4\" mat-button type=\"button\">LEARN MORE</button>\n  </div>\n\n  <div class=\"p-gutter\" fxFlex=\"400px\" fxFlex.lt-md=\"auto\">\n    <h3 class=\"body-2 m-0\">FEATURES</h3>\n\n    <div class=\"mt-4\" gdColumns=\"1fr 1fr 1fr\" gdGap=\"16px\">\n      <a (click)=\"close()\"\n         *ngFor=\"let feature of features\"\n         [routerLink]=\"feature.route\"\n         class=\"text-dark p-3 text-center hover:bg-hover hover:text-primary-500 trans-ease-out rounded block no-underline\">\n        <ic-icon [icon]=\"feature.icon\" class=\"text-primary-500\" size=\"32px\"></ic-icon>\n        <div class=\"body-1 mt-2\">{{ feature.label }}</div>\n      </a>\n    </div>\n  </div>\n\n  <div class=\"p-gutter\" fxFlex=\"350px\" fxFlex.lt-md=\"auto\">\n    <h3 class=\"body-2 m-0\">PAGES</h3>\n\n    <div class=\"mt-6\" gdColumns=\"1fr 1fr\" gdGap=\"16px 48px\">\n      <a (click)=\"close()\"\n         *ngFor=\"let page of pages\"\n         [routerLink]=\"page.route\"\n         class=\"text-dark body-1 no-underline hover:text-primary-500 trans-ease-out\">{{ page.label }}</a>\n    </div>\n  </div>\n</div>\n\n");

/***/ }),

/***/ "Y7fp":
/*!*******************************************!*\
  !*** ./src/app/data/schema/body-param.ts ***!
  \*******************************************/
/*! exports provided: BodyParam */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "BodyParam", function() { return BodyParam; });
/* harmony import */ var _request_component__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./request-component */ "2bXN");

class BodyParam extends _request_component__WEBPACK_IMPORTED_MODULE_0__["RequestComponent"] {
    constructor(bodyParam) {
        super(4, bodyParam.id, bodyParam.alias);
        this.name = bodyParam.name;
        this.value = bodyParam.value;
        this.aliasName = bodyParam.alias_name;
        this.isRequired = bodyParam.is_required;
    }
}


/***/ }),

/***/ "YCZM":
/*!******************************************************************!*\
  !*** ./src/app/core/http/organizations-user-resource.service.ts ***!
  \******************************************************************/
/*! exports provided: OrganizationsUserResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "OrganizationsUserResource", function() { return OrganizationsUserResource; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _rest_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rest-api.service */ "iCaw");



let OrganizationsUserResource = class OrganizationsUserResource {
    constructor(restApi) {
        this.restApi = restApi;
        this.ORGANIZATION_ENDPOINT = 'organizations';
        this.ENDPOINT = 'users';
    }
    index(organizationId, queryParams) {
        return this.restApi.index([this.ORGANIZATION_ENDPOINT, organizationId, this.ENDPOINT], queryParams);
    }
    show(organizationId, id, queryParams) {
        return this.restApi.show([this.ORGANIZATION_ENDPOINT, organizationId, this.ENDPOINT, id], queryParams);
    }
    create(organizationId, body) {
        return this.restApi.create([this.ORGANIZATION_ENDPOINT, organizationId, this.ENDPOINT], body);
    }
    update(organizationId, id, body) {
        return this.restApi.update([this.ORGANIZATION_ENDPOINT, organizationId, this.ENDPOINT, id], body);
    }
    destroy(organizationId, id) {
        return this.restApi.destroy([this.ORGANIZATION_ENDPOINT, organizationId, this.ENDPOINT, id]);
    }
};
OrganizationsUserResource.ctorParameters = () => [
    { type: _rest_api_service__WEBPACK_IMPORTED_MODULE_2__["RestApiService"] }
];
OrganizationsUserResource = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], OrganizationsUserResource);



/***/ }),

/***/ "YGXf":
/*!*****************************************************************!*\
  !*** ./src/@vex/components/sidenav-item/sidenav-item.module.ts ***!
  \*****************************************************************/
/*! exports provided: SidenavItemModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SidenavItemModule", function() { return SidenavItemModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_material_core__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/core */ "UhP/");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _sidenav_item_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./sidenav-item.component */ "zd1o");









let SidenavItemModule = class SidenavItemModule {
};
SidenavItemModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_sidenav_item_component__WEBPACK_IMPORTED_MODULE_8__["SidenavItemComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_router__WEBPACK_IMPORTED_MODULE_6__["RouterModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_5__["MatIconModule"],
            _angular_material_core__WEBPACK_IMPORTED_MODULE_4__["MatRippleModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_7__["IconModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"]
        ],
        exports: [_sidenav_item_component__WEBPACK_IMPORTED_MODULE_8__["SidenavItemComponent"]]
    })
], SidenavItemModule);



/***/ }),

/***/ "YUAm":
/*!********************************************************!*\
  !*** ./src/@vex/components/footer/footer.component.ts ***!
  \********************************************************/
/*! exports provided: FooterComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FooterComponent", function() { return FooterComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_footer_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./footer.component.html */ "xDFx");
/* harmony import */ var _footer_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./footer.component.scss */ "cGA/");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _iconify_icons_ic_twotone_shopping_basket__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @iconify/icons-ic/twotone-shopping-basket */ "RM6X");
/* harmony import */ var _iconify_icons_ic_twotone_shopping_basket__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_shopping_basket__WEBPACK_IMPORTED_MODULE_4__);





let FooterComponent = class FooterComponent {
    constructor() {
        this.icShoppingBasket = _iconify_icons_ic_twotone_shopping_basket__WEBPACK_IMPORTED_MODULE_4___default.a;
    }
    ngOnInit() {
    }
    ngOnDestroy() { }
};
FooterComponent.ctorParameters = () => [];
FooterComponent.propDecorators = {
    customTemplate: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"] }]
};
FooterComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'vex-footer',
        template: _raw_loader_footer_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_footer_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], FooterComponent);



/***/ }),

/***/ "YiRj":
/*!**************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/@vex/components/popover/popover.component.html ***!
  \**************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div @transformPopover class=\"popover\">\r\n  <ng-container [ngSwitch]=\"renderMethod\">\r\n    <div *ngSwitchCase=\"'text'\" [innerHTML]=\"content\"></div>\r\n    <ng-container *ngSwitchCase=\"'template'\">\r\n      <ng-container *ngTemplateOutlet=\"content; context: context\"></ng-container>\r\n    </ng-container>\r\n    <ng-container *ngSwitchCase=\"'component'\">\r\n      <ng-container *ngComponentOutlet=\"content\"></ng-container>\r\n    </ng-container>\r\n  </ng-container>\r\n</div>\r\n");

/***/ }),

/***/ "Ys2n":
/*!*****************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/layout/components/toolbar/components/toolbar-proxy-settings/components/toolbar-mock-settings/toolbar-mock-settings.component.html ***!
  \*****************************************************************************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<form (ngSubmit)=\"update()\" [formGroup]=\"form\">\n  <div fxLayout=\"row\" fxLayoutAlign=\"start center\" mat-dialog-title>\n    <h2 class=\"headline m-0\" fxFlex=\"auto\">Mock Settings</h2>\n\n    <button class=\"subheading\" mat-dialog-close mat-icon-button type=\"button\">\n      <mat-icon [icIcon]=\"icClose\"></mat-icon>\n    </button>\n  </div>\n\n  <mat-divider class=\"-mx-6 text-border\"></mat-divider>\n\n  <mat-tab-group>\n    <mat-tab label=\"General\">\n      <div class=\"mt-3\" fxLayout=\"column\" fxLayoutAlign=\"start start\">\n        <h4 class=\" mb-2 subheading\" fxFlex=\"100\">\n          Mock Requests From\n        </h4>\n\n        <mat-form-field fxFlex=\"fill\" class=\"w-full\">\n          <mat-label>Project</mat-label>\n          <mat-select \n            (selectionChange)=\"selectProject($event)\"\n            formControlName=\"project\"\n          >\n            <mat-option \n              *ngFor=\"let project of (projects$ | async)\"\n              [value]=\"project\"\n            >\n              {{ project.name }}\n            </mat-option>\n          </mat-select>\n        </mat-form-field>\n\n        <div \n          class=\"w-full\" fxLayout=\"row\" fxLayoutGap=\"10px\"\n        >\n          <mat-form-field fxFlex=\"fill\" class=\"w-full\">\n            <mat-label>Scenario</mat-label>\n            <mat-select formControlName=\"scenario\">\n              <mat-option \n                *ngFor=\"let scenario of scenarios\"\n                [value]=\"scenario\"\n              >\n                {{ scenario.name }}\n              </mat-option>\n            </mat-select>\n\n            <mat-hint>If left blank, defaults to project</mat-hint>\n          </mat-form-field>\n\n          <button \n            *ngIf=\"form.value.scenario\" \n            (click)=\"clearScenario()\"\n            fxFlex=\"40px\" class=\"input-button\" mat-icon-button matSuffix type=\"button\">\n            <div fxLayout=\"row\" fxLayoutAlign=\"center center\">\n              <mat-icon [icIcon]=\"icClose\"></mat-icon>\n            </div>\n          </button>\n        </div>\n      </div>\n    </mat-tab>\n    <mat-tab label=\"Policy\">\n      <div class=\"mt-3\" fxLayout=\"column\" fxLayoutAlign=\"start start\">\n        <h4 class=\"mb-2 subheading\" fxFlex=\"100\">\n          Mock Which Requests\n        </h4>\n\n        <mat-form-field class=\"w-full\">\n          <mat-label>Policy</mat-label>\n          <mat-select formControlName=\"mockPolicy\">\n            <mat-option \n              *ngFor=\"let policy of policies\"\n              [value]=\"policy\"\n            >\n              {{ policy }}\n            </mat-option>\n          </mat-select>\n        </mat-form-field>\n      \n        <ng-container *ngIf=\"form.value.mockPolicy !== 'all'\"> \n          <h4 class=\"mb-2 subheading\" fxFlex=\"100\">\n            Proxy Not Found Requests To\n          </h4>\n\n          <mat-form-field class=\"mb-4 w-full\">\n            <mat-label>Service URL</mat-label>\n            <input matInput formControlName=\"serviceUrl\" type=\"text\">\n            <mat-hint>e.g. http(s)://myhost.net</mat-hint>\n          </mat-form-field>\n        </ng-container>\n      </div>\n    </mat-tab>\n    <mat-tab label=\"Include\">\n      <div class=\"mt-3 mb-3\" fxLayout=\"column\" fxLayoutAlign=\"start start\">\n        <h4 class=\"mb-2 subheading\" fxFlex=\"100\">\n          Allow Requests Matching\n        </h4>\n\n        <div class=\"w-full\" fxLayout=\"column\" fxLayoutGap=\"5px\">\n          <div\n            formArrayName=\"includePatterns\"\n            *ngFor=\"let control of form.get('includePatterns')['controls']; index as i\"\n          >\n            <div\n              [formGroupName]=\"i\"\n              fxLayout=\"row\"\n              fxLayoutAlign=\"space-around start\"\n              fxLayoutGap=\"10px\"\n            >\n              <mat-form-field fxFlex=\"90\">\n                <mat-label>Pattern</mat-label>\n                <input\n                  matInput\n                  formControlName=\"pattern\"\n                />\n                <mat-hint>e.g. http://localhost:3000/users/.*</mat-hint>\n              </mat-form-field>\n              <button\n                (click)=\"removeIncludePattern(i)\"\n                class=\"mt-2\"\n                color=\"warn\"\n                fxFlex=\"10\"\n                type=\"button\"\n                mat-button\n              >\n                <mat-icon [icIcon]=\"icDelete\"></mat-icon>\n              </button>\n            </div>\n          </div>\n          <button class=\"mb-2\" (click)=\"addIncludePattern()\" color=\"primary\" type=\"button\" mat-raised-button fxFlex=\"100\">\n            New Pattern\n          </button>\n        </div>\n      </div>\n    </mat-tab>\n    <mat-tab label=\"Exclude\">\n      <div class=\"mt-3 mb-3\" fxLayout=\"column\" fxLayoutAlign=\"start start\">\n        <h4 class=\"mb-2 subheading\" fxFlex=\"100\">\n          Ignore Requests Matching\n        </h4>\n\n        <div class=\"w-full\" fxLayout=\"column\" fxLayoutGap=\"5px\">\n          <div\n            formArrayName=\"excludePatterns\"\n            *ngFor=\"let control of form.get('excludePatterns')['controls']; index as i\"\n          >\n            <div\n              [formGroupName]=\"i\"\n              fxLayout=\"row\"\n              fxLayoutAlign=\"space-around start\"\n              fxLayoutGap=\"10px\"\n            >\n              <mat-form-field fxFlex=\"90\">\n                <mat-label>Pattern</mat-label>\n                <input\n                  matInput\n                  formControlName=\"pattern\"\n                />\n                <mat-hint>e.g. http://localhost:3000/users/.*</mat-hint>\n              </mat-form-field>\n              <button\n                (click)=\"removeExcludePattern(i)\"\n                class=\"mt-2\"\n                color=\"warn\"\n                fxFlex=\"10\"\n                type=\"button\"\n                mat-button\n              >\n                <mat-icon [icIcon]=\"icDelete\"></mat-icon>\n              </button>\n            </div>\n          </div>\n          <button class=\"mb-2\" (click)=\"addExcludePattern()\" color=\"primary\" type=\"button\" mat-raised-button fxFlex=\"100\">\n            New Pattern\n          </button>\n        </div>\n      </div>\n    </mat-tab>\n  </mat-tab-group>\n\n  <mat-divider></mat-divider>\n\n  <mat-dialog-actions align=\"end\">\n    <button [disabled]=\"form.invalid\" color=\"primary\" mat-button type=\"submit\">UPDATE</button>\n    <button mat-button mat-dialog-close type=\"button\">CANCEL</button>\n  </mat-dialog-actions>\n</form>\n");

/***/ }),

/***/ "Z+W5":
/*!********************************************!*\
  !*** ./src/@vex/services/style.service.ts ***!
  \********************************************/
/*! exports provided: Style, StyleService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Style", function() { return Style; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "StyleService", function() { return StyleService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var ngx_take_until_destroy__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ngx-take-until-destroy */ "DnKK");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs */ "qCKp");





var Style;
(function (Style) {
    Style["light"] = "vex-style-light";
    Style["default"] = "vex-style-default";
    Style["dark"] = "vex-style-dark";
})(Style || (Style = {}));
let StyleService = class StyleService {
    constructor(document) {
        this.document = document;
        this.defaultStyle = Style.default;
        this._styleSubject = new rxjs__WEBPACK_IMPORTED_MODULE_4__["BehaviorSubject"](this.defaultStyle);
        this.style$ = this._styleSubject.asObservable();
        this.style$.pipe(Object(ngx_take_until_destroy__WEBPACK_IMPORTED_MODULE_3__["untilDestroyed"])(this)).subscribe(style => this._updateStyle(style));
    }
    setStyle(style) {
        this._styleSubject.next(style);
    }
    ngOnDestroy() { }
    _updateStyle(style) {
        const body = this.document.body;
        Object.values(Style).filter(s => s !== style).forEach(value => {
            if (body.classList.contains(value)) {
                body.classList.remove(value);
            }
        });
        body.classList.add(style);
    }
};
StyleService.ctorParameters = () => [
    { type: Document, decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Inject"], args: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["DOCUMENT"],] }] }
];
StyleService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["Injectable"])({
        providedIn: 'root'
    })
], StyleService);



/***/ }),

/***/ "ZAI4":
/*!*******************************!*\
  !*** ./src/app/app.module.ts ***!
  \*******************************/
/*! exports provided: AppModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AppModule", function() { return AppModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common/http */ "IheW");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_platform_browser__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/platform-browser */ "cUpR");
/* harmony import */ var _angular_platform_browser_animations__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/platform-browser/animations */ "omvX");
/* harmony import */ var angular_token__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! angular-token */ "hU4o");
/* harmony import */ var angularx_social_login__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! angularx-social-login */ "ybVy");
/* harmony import */ var ngx_stripe__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ngx-stripe */ "AZjg");
/* harmony import */ var _vex_vex_module__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @vex/vex.module */ "iB7b");
/* harmony import */ var _core_core_module__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @core/core.module */ "pKmL");
/* harmony import */ var _core_interceptors_agent_interceptor__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @core/interceptors/agent.interceptor */ "Gg42");
/* harmony import */ var _core_interceptors_http_error_interceptor__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @core/interceptors/http-error.interceptor */ "Neo8");
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @environments/environment */ "AytR");
/* harmony import */ var _layout_custom_layout_module__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @layout/custom-layout.module */ "71PN");
/* harmony import */ var _app_routing_module__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./app-routing.module */ "vY5A");
/* harmony import */ var _app_component__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ./app.component */ "Sy1n");
















const googleLoginOptions = {
    scope: 'profile email',
}; // https://developers.google.com/api-client-library/javascript/reference/referencedocs#gapiauth2clientconfig
let AppModule = class AppModule {
};
AppModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_app_component__WEBPACK_IMPORTED_MODULE_15__["AppComponent"]],
        imports: [
            // Standard
            _angular_platform_browser__WEBPACK_IMPORTED_MODULE_3__["BrowserModule"],
            _angular_platform_browser_animations__WEBPACK_IMPORTED_MODULE_4__["BrowserAnimationsModule"],
            _angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpClientModule"],
            // Vex
            _vex_vex_module__WEBPACK_IMPORTED_MODULE_8__["VexModule"],
            // Third Party
            angular_token__WEBPACK_IMPORTED_MODULE_5__["AngularTokenModule"].forRoot({
                apiBase: _environments_environment__WEBPACK_IMPORTED_MODULE_12__["environment"].apiUrl,
            }),
            angularx_social_login__WEBPACK_IMPORTED_MODULE_6__["SocialLoginModule"],
            ngx_stripe__WEBPACK_IMPORTED_MODULE_7__["NgxStripeModule"].forRoot(_environments_environment__WEBPACK_IMPORTED_MODULE_12__["environment"].stripeKey),
            // Application
            _core_core_module__WEBPACK_IMPORTED_MODULE_9__["CoreModule"],
            _app_routing_module__WEBPACK_IMPORTED_MODULE_14__["AppRoutingModule"],
            _layout_custom_layout_module__WEBPACK_IMPORTED_MODULE_13__["CustomLayoutModule"],
        ],
        providers: [
            {
                provide: _angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HTTP_INTERCEPTORS"],
                useClass: _core_interceptors_http_error_interceptor__WEBPACK_IMPORTED_MODULE_11__["HttpErrorInterceptor"],
                multi: true,
            },
            {
                provide: _angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HTTP_INTERCEPTORS"],
                useClass: _core_interceptors_agent_interceptor__WEBPACK_IMPORTED_MODULE_10__["AgentInterceptor"],
                multi: true,
            },
            {
                provide: 'SocialAuthServiceConfig',
                useValue: {
                    autoLogin: false,
                    providers: [
                        {
                            id: angularx_social_login__WEBPACK_IMPORTED_MODULE_6__["GoogleLoginProvider"].PROVIDER_ID,
                            provider: new angularx_social_login__WEBPACK_IMPORTED_MODULE_6__["GoogleLoginProvider"](_environments_environment__WEBPACK_IMPORTED_MODULE_12__["environment"].googleOauthClientId, googleLoginOptions),
                        },
                    ],
                },
            },
        ],
        bootstrap: [_app_component__WEBPACK_IMPORTED_MODULE_15__["AppComponent"]],
    })
], AppModule);



/***/ }),

/***/ "Zifb":
/*!***************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/@vex/components/config-panel/config-panel-toggle/config-panel-toggle.component.html ***!
  \***************************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<button (click)=\"openConfig.emit()\" class=\"config-panel-toggle\" color=\"primary\" mat-fab type=\"button\">\n  <mat-icon [icIcon]=\"icSettings\"></mat-icon>\n</button>\n");

/***/ }),

/***/ "a3ZD":
/*!**************************************************************!*\
  !*** ./src/@vex/directives/container/container.directive.ts ***!
  \**************************************************************/
/*! exports provided: ContainerDirective */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ContainerDirective", function() { return ContainerDirective; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var ngx_take_until_destroy__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ngx-take-until-destroy */ "DnKK");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "kU1M");
/* harmony import */ var _services_config_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/config.service */ "lC2v");





let ContainerDirective = class ContainerDirective {
    constructor(configService, cd) {
        this.configService = configService;
        this.cd = cd;
        this.configService.config$.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["map"])(config => config.boxed), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["distinctUntilChanged"])(), Object(ngx_take_until_destroy__WEBPACK_IMPORTED_MODULE_2__["untilDestroyed"])(this)).subscribe(boxed => {
            this.enabled = boxed;
            this.cd.markForCheck();
        });
    }
    ngOnDestroy() { }
};
ContainerDirective.ctorParameters = () => [
    { type: _services_config_service__WEBPACK_IMPORTED_MODULE_4__["ConfigService"] },
    { type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["ChangeDetectorRef"] }
];
ContainerDirective.propDecorators = {
    enabled: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["HostBinding"], args: ['class.container',] }]
};
ContainerDirective = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Directive"])({
        selector: '[vexContainer]'
    })
], ContainerDirective);



/***/ }),

/***/ "bJeg":
/*!**********************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/@vex/layout/sidenav/sidenav.component.html ***!
  \**********************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div (mouseenter)=\"onMouseEnter()\"\r\n     (mouseleave)=\"onMouseLeave()\"\r\n     [class.collapsed]=\"collapsed\"\r\n     [class.open]=\"collapsed && collapsedOpen$ | async\"\r\n     class=\"sidenav flex flex-col\">\r\n  <div class=\"sidenav-toolbar flex-none flex items-center\">\r\n    <img [src]=\"imageUrl$ | async\" class=\"w-6 select-none flex-none\">\r\n    <h2 class=\"title ltr:pl-4 rtl:pr-4 select-none flex-auto\">{{ title$ | async }}</h2>\r\n    <!-- <button (click)=\"toggleCollapse()\"\r\n            *ngIf=\"showCollapsePin$ | async\"\r\n            class=\"w-8 h-8 -mr-2 leading-none flex-none hidden lg:block\"\r\n            mat-icon-button\r\n            type=\"button\">\r\n      <mat-icon *ngIf=\"!collapsed\" [icIcon]=\"icRadioButtonChecked\" size=\"14px\"></mat-icon>\r\n      <mat-icon *ngIf=\"collapsed\" [icIcon]=\"icRadioButtonUnchecked\" size=\"14px\"></mat-icon>\r\n    </button> -->\r\n  </div>\r\n\r\n  <div *ngIf=\"ready\" class=\"sidenav-items flex-auto\" vexScrollbar>\r\n    <vex-sidenav-item *ngFor=\"let item of items; trackBy: trackByRoute\"\r\n                      [item]=\"item\"\r\n                      [level]=\"0\"></vex-sidenav-item>\r\n  </div>\r\n</div>\r\n");

/***/ }),

/***/ "c7Bs":
/*!**************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/@vex/components/sidebar/sidebar.component.html ***!
  \**************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div (click)=\"close()\" [class.invisible]=\"invisibleBackdrop\" [class.visible]=\"opened\" class=\"backdrop\"></div>\r\n\r\n<div [class.open]=\"opened\" [class.position-left]=\"positionLeft\" [class.position-right]=\"positionRight\" class=\"sidebar\">\r\n  <ng-content></ng-content>\r\n</div>\r\n");

/***/ }),

/***/ "cD1t":
/*!*********************************************************************************************!*\
  !*** ./src/app/layout/components/toolbar/components/toolbar-user/toolbar-user.component.ts ***!
  \*********************************************************************************************/
/*! exports provided: ToolbarUserComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ToolbarUserComponent", function() { return ToolbarUserComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_toolbar_user_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./toolbar-user.component.html */ "2USq");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _vex_components_popover_popover_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @vex/components/popover/popover.service */ "kYjG");
/* harmony import */ var _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @vex/utils/tailwindcss */ "XXSj");
/* harmony import */ var _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @iconify/icons-ic/twotone-person */ "KaaH");
/* harmony import */ var _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _users_services_user_data_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @users/services/user-data.service */ "O7ya");
/* harmony import */ var _toolbar_user_dropdown_toolbar_user_dropdown_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./toolbar-user-dropdown/toolbar-user-dropdown.component */ "dGqQ");









let ToolbarUserComponent = class ToolbarUserComponent {
    constructor(cd, popover, userData, router) {
        this.cd = cd;
        this.popover = popover;
        this.userData = userData;
        this.router = router;
        this.icPerson = _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_6___default.a;
        this.theme = _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_5__["default"];
        this.user$ = this.userData.get();
    }
    ngOnInit() {
    }
    showPopover(originRef) {
        this.dropdownOpen = true;
        this.cd.markForCheck();
        const popoverRef = this.popover.open({
            content: _toolbar_user_dropdown_toolbar_user_dropdown_component__WEBPACK_IMPORTED_MODULE_8__["ToolbarUserDropdownComponent"],
            origin: originRef,
            offsetY: 12,
            position: [
                {
                    originX: 'center',
                    originY: 'top',
                    overlayX: 'center',
                    overlayY: 'bottom',
                },
                {
                    originX: 'end',
                    originY: 'bottom',
                    overlayX: 'end',
                    overlayY: 'top',
                },
            ],
        });
        // Listen to route change event, close popper when route changes
        this.router.events.subscribe((event) => {
            if (event instanceof _angular_router__WEBPACK_IMPORTED_MODULE_3__["NavigationEnd"]) {
                popoverRef.close();
            }
        });
        popoverRef.afterClosed$.subscribe(() => {
            this.dropdownOpen = false;
            this.cd.markForCheck();
        });
    }
};
ToolbarUserComponent.ctorParameters = () => [
    { type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["ChangeDetectorRef"] },
    { type: _vex_components_popover_popover_service__WEBPACK_IMPORTED_MODULE_4__["PopoverService"] },
    { type: _users_services_user_data_service__WEBPACK_IMPORTED_MODULE_7__["UserDataService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["Router"] }
];
ToolbarUserComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["Component"])({
        selector: 'vex-toolbar-user',
        template: _raw_loader_toolbar_user_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_2__["ChangeDetectionStrategy"].OnPush,
    })
], ToolbarUserComponent);



/***/ }),

/***/ "cFcm":
/*!************************************************************!*\
  !*** ./src/@vex/components/sidebar/sidebar.component.scss ***!
  \************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (".sidebar {\n  background: var(--background-card);\n  bottom: 0;\n  box-shadow: var(--elevation-z8);\n  display: flex;\n  flex: 1 0 auto;\n  flex-direction: column;\n  max-width: 80vw;\n  overflow-x: hidden;\n  overflow-y: auto;\n  position: fixed;\n  top: 0;\n  transition-duration: var(--trans-ease-in-duration);\n  transition-property: transform, visibility;\n  transition-timing-function: var(--trans-ease-in-timing-function);\n  visibility: hidden;\n  width: var(--sidenav-width);\n  z-index: 1000;\n}\n\n@media (min-width: 600px) {\n  .sidebar {\n    max-width: unset;\n  }\n}\n\n.sidebar.position-left {\n  left: 0;\n  transform: translateX(-100%);\n}\n\n.sidebar.position-right {\n  right: 0;\n  transform: translateX(100%);\n}\n\n.sidebar.open {\n  transform: translateX(0);\n  visibility: visible;\n}\n\n.backdrop {\n  background-color: transparent;\n  bottom: 0;\n  left: 0;\n  position: absolute;\n  right: 0;\n  top: 0;\n  transition-duration: 400ms;\n  transition-property: background-color, visibility;\n  transition-timing-function: cubic-bezier(0.25, 0.8, 0.25, 1);\n  visibility: hidden;\n  z-index: 800 !important;\n}\n\n.backdrop.visible {\n  background-color: rgba(0, 0, 0, 0.6);\n  visibility: visible;\n}\n\n.backdrop.invisible {\n  background-color: transparent;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uL3NpZGViYXIuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSxrQ0FBQTtFQUNBLFNBQUE7RUFDQSwrQkFBQTtFQUNBLGFBQUE7RUFDQSxjQUFBO0VBQ0Esc0JBQUE7RUFDQSxlQUFBO0VBQ0Esa0JBQUE7RUFDQSxnQkFBQTtFQUNBLGVBQUE7RUFDQSxNQUFBO0VBQ0Esa0RBQUE7RUFDQSwwQ0FBQTtFQUNBLGdFQUFBO0VBQ0Esa0JBQUE7RUFDQSwyQkFBQTtFQUNBLGFBQUE7QUFDRjs7QUFFQTtFQUNFO0lBQ0UsZ0JBQUE7RUFDRjtBQUNGOztBQUVBO0VBQ0UsT0FBQTtFQUNBLDRCQUFBO0FBQUY7O0FBR0E7RUFDRSxRQUFBO0VBQ0EsMkJBQUE7QUFBRjs7QUFHQTtFQUNFLHdCQUFBO0VBQ0EsbUJBQUE7QUFBRjs7QUFHQTtFQUNFLDZCQUFBO0VBQ0EsU0FBQTtFQUNBLE9BQUE7RUFDQSxrQkFBQTtFQUNBLFFBQUE7RUFDQSxNQUFBO0VBQ0EsMEJBQUE7RUFDQSxpREFBQTtFQUNBLDREQUFBO0VBQ0Esa0JBQUE7RUFDQSx1QkFBQTtBQUFGOztBQUdBO0VBQ0Usb0NBQUE7RUFDQSxtQkFBQTtBQUFGOztBQUdBO0VBQ0UsNkJBQUE7QUFBRiIsImZpbGUiOiJzaWRlYmFyLmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiLnNpZGViYXIge1xuICBiYWNrZ3JvdW5kOiB2YXIoLS1iYWNrZ3JvdW5kLWNhcmQpO1xuICBib3R0b206IDA7XG4gIGJveC1zaGFkb3c6IHZhcigtLWVsZXZhdGlvbi16OCk7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGZsZXg6IDEgMCBhdXRvO1xuICBmbGV4LWRpcmVjdGlvbjogY29sdW1uO1xuICBtYXgtd2lkdGg6IDgwdnc7XG4gIG92ZXJmbG93LXg6IGhpZGRlbjtcbiAgb3ZlcmZsb3cteTogYXV0bztcbiAgcG9zaXRpb246IGZpeGVkO1xuICB0b3A6IDA7XG4gIHRyYW5zaXRpb24tZHVyYXRpb246IHZhcigtLXRyYW5zLWVhc2UtaW4tZHVyYXRpb24pO1xuICB0cmFuc2l0aW9uLXByb3BlcnR5OiB0cmFuc2Zvcm0sIHZpc2liaWxpdHk7XG4gIHRyYW5zaXRpb24tdGltaW5nLWZ1bmN0aW9uOiB2YXIoLS10cmFucy1lYXNlLWluLXRpbWluZy1mdW5jdGlvbik7XG4gIHZpc2liaWxpdHk6IGhpZGRlbjtcbiAgd2lkdGg6IHZhcigtLXNpZGVuYXYtd2lkdGgpO1xuICB6LWluZGV4OiAxMDAwO1xufVxuXG5AbWVkaWEgKG1pbi13aWR0aDogNjAwcHgpIHtcbiAgLnNpZGViYXIge1xuICAgIG1heC13aWR0aDogdW5zZXQ7XG4gIH1cbn1cblxuLnNpZGViYXIucG9zaXRpb24tbGVmdCB7XG4gIGxlZnQ6IDA7XG4gIHRyYW5zZm9ybTogdHJhbnNsYXRlWCgtMTAwJSk7XG59XG5cbi5zaWRlYmFyLnBvc2l0aW9uLXJpZ2h0IHtcbiAgcmlnaHQ6IDA7XG4gIHRyYW5zZm9ybTogdHJhbnNsYXRlWCgxMDAlKTtcbn1cblxuLnNpZGViYXIub3BlbiB7XG4gIHRyYW5zZm9ybTogdHJhbnNsYXRlWCgwKTtcbiAgdmlzaWJpbGl0eTogdmlzaWJsZTtcbn1cblxuLmJhY2tkcm9wIHtcbiAgYmFja2dyb3VuZC1jb2xvcjogdHJhbnNwYXJlbnQ7XG4gIGJvdHRvbTogMDtcbiAgbGVmdDogMDtcbiAgcG9zaXRpb246IGFic29sdXRlO1xuICByaWdodDogMDtcbiAgdG9wOiAwO1xuICB0cmFuc2l0aW9uLWR1cmF0aW9uOiA0MDBtcztcbiAgdHJhbnNpdGlvbi1wcm9wZXJ0eTogYmFja2dyb3VuZC1jb2xvciwgdmlzaWJpbGl0eTtcbiAgdHJhbnNpdGlvbi10aW1pbmctZnVuY3Rpb246IGN1YmljLWJlemllcigwLjI1LCAwLjgsIDAuMjUsIDEpO1xuICB2aXNpYmlsaXR5OiBoaWRkZW47XG4gIHotaW5kZXg6IDgwMCAhaW1wb3J0YW50O1xufVxuXG4uYmFja2Ryb3AudmlzaWJsZSB7XG4gIGJhY2tncm91bmQtY29sb3I6IHJnYmEoMCwgMCwgMCwgMC42KTtcbiAgdmlzaWJpbGl0eTogdmlzaWJsZTtcbn1cblxuLmJhY2tkcm9wLmludmlzaWJsZSB7XG4gIGJhY2tncm91bmQtY29sb3I6IHRyYW5zcGFyZW50O1xufSJdfQ== */");

/***/ }),

/***/ "cGA/":
/*!**********************************************************!*\
  !*** ./src/@vex/components/footer/footer.component.scss ***!
  \**********************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (":host {\n  bottom: 0;\n  display: block;\n  width: 100%;\n  z-index: var(--footer-z-index);\n}\n\n.footer {\n  background: var(--footer-background);\n  color: var(--footer-color);\n  height: var(--footer-height);\n  padding-left: var(--padding);\n  padding-right: var(--padding);\n  position: relative;\n  z-index: var(--footer-z-index);\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uL2Zvb3Rlci5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLFNBQUE7RUFDQSxjQUFBO0VBQ0EsV0FBQTtFQUNBLDhCQUFBO0FBQ0Y7O0FBRUE7RUFDRSxvQ0FBQTtFQUNBLDBCQUFBO0VBQ0EsNEJBQUE7RUFDQSw0QkFBQTtFQUNBLDZCQUFBO0VBQ0Esa0JBQUE7RUFDQSw4QkFBQTtBQUNGIiwiZmlsZSI6ImZvb3Rlci5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbIjpob3N0IHtcbiAgYm90dG9tOiAwO1xuICBkaXNwbGF5OiBibG9jaztcbiAgd2lkdGg6IDEwMCU7XG4gIHotaW5kZXg6IHZhcigtLWZvb3Rlci16LWluZGV4KTtcbn1cblxuLmZvb3RlciB7XG4gIGJhY2tncm91bmQ6IHZhcigtLWZvb3Rlci1iYWNrZ3JvdW5kKTtcbiAgY29sb3I6IHZhcigtLWZvb3Rlci1jb2xvcik7XG4gIGhlaWdodDogdmFyKC0tZm9vdGVyLWhlaWdodCk7XG4gIHBhZGRpbmctbGVmdDogdmFyKC0tcGFkZGluZyk7XG4gIHBhZGRpbmctcmlnaHQ6IHZhcigtLXBhZGRpbmcpO1xuICBwb3NpdGlvbjogcmVsYXRpdmU7XG4gIHotaW5kZXg6IHZhcigtLWZvb3Rlci16LWluZGV4KTtcbn0iXX0= */");

/***/ }),

/***/ "cd7D":
/*!****************************************************************!*\
  !*** ./src/app/layout/components/toolbar/toolbar.component.ts ***!
  \****************************************************************/
/*! exports provided: ToolbarComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ToolbarComponent", function() { return ToolbarComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_toolbar_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./toolbar.component.html */ "GK0M");
/* harmony import */ var _toolbar_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./toolbar.component.scss */ "1Fbs");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/dialog */ "iELJ");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! rxjs/operators */ "kU1M");
/* harmony import */ var _iconify_icons_emojione_flag_for_flag_germany__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @iconify/icons-emojione/flag-for-flag-germany */ "t6uZ");
/* harmony import */ var _iconify_icons_emojione_flag_for_flag_germany__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_emojione_flag_for_flag_germany__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _iconify_icons_emojione_flag_for_flag_united_states__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @iconify/icons-emojione/flag-for-flag-united-states */ "6m+4");
/* harmony import */ var _iconify_icons_emojione_flag_for_flag_united_states__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_emojione_flag_for_flag_united_states__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _iconify_icons_ic_twotone_arrow_drop_down__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @iconify/icons-ic/twotone-arrow-drop-down */ "LgSP");
/* harmony import */ var _iconify_icons_ic_twotone_arrow_drop_down__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_arrow_drop_down__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _iconify_icons_ic_twotone_assignment__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @iconify/icons-ic/twotone-assignment */ "16CC");
/* harmony import */ var _iconify_icons_ic_twotone_assignment__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_assignment__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _iconify_icons_ic_twotone_assignment_turned_in__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @iconify/icons-ic/twotone-assignment-turned-in */ "CvgF");
/* harmony import */ var _iconify_icons_ic_twotone_assignment_turned_in__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_assignment_turned_in__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _iconify_icons_ic_twotone_ballot__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @iconify/icons-ic/twotone-ballot */ "8U4E");
/* harmony import */ var _iconify_icons_ic_twotone_ballot__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_ballot__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var _iconify_icons_ic_twotone_bookmarks__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @iconify/icons-ic/twotone-bookmarks */ "+1NE");
/* harmony import */ var _iconify_icons_ic_twotone_bookmarks__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_bookmarks__WEBPACK_IMPORTED_MODULE_12__);
/* harmony import */ var _iconify_icons_ic_twotone_description__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @iconify/icons-ic/twotone-description */ "0nnX");
/* harmony import */ var _iconify_icons_ic_twotone_description__WEBPACK_IMPORTED_MODULE_13___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_description__WEBPACK_IMPORTED_MODULE_13__);
/* harmony import */ var _iconify_icons_ic_twotone_done_all__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @iconify/icons-ic/twotone-done-all */ "mEjI");
/* harmony import */ var _iconify_icons_ic_twotone_done_all__WEBPACK_IMPORTED_MODULE_14___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_done_all__WEBPACK_IMPORTED_MODULE_14__);
/* harmony import */ var _iconify_icons_ic_twotone_menu__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @iconify/icons-ic/twotone-menu */ "cS8l");
/* harmony import */ var _iconify_icons_ic_twotone_menu__WEBPACK_IMPORTED_MODULE_15___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_menu__WEBPACK_IMPORTED_MODULE_15__);
/* harmony import */ var _iconify_icons_ic_twotone_pageview__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @iconify/icons-ic/twotone-pageview */ "9Gk2");
/* harmony import */ var _iconify_icons_ic_twotone_pageview__WEBPACK_IMPORTED_MODULE_16___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_pageview__WEBPACK_IMPORTED_MODULE_16__);
/* harmony import */ var _iconify_icons_ic_twotone_person_add__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @iconify/icons-ic/twotone-person-add */ "+q50");
/* harmony import */ var _iconify_icons_ic_twotone_person_add__WEBPACK_IMPORTED_MODULE_17___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_person_add__WEBPACK_IMPORTED_MODULE_17__);
/* harmony import */ var _iconify_icons_ic_twotone_receipt__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @iconify/icons-ic/twotone-receipt */ "Ehqh");
/* harmony import */ var _iconify_icons_ic_twotone_receipt__WEBPACK_IMPORTED_MODULE_18___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_receipt__WEBPACK_IMPORTED_MODULE_18__);
/* harmony import */ var _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! @iconify/icons-ic/twotone-search */ "sF+I");
/* harmony import */ var _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_19___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_19__);
/* harmony import */ var _vex_components_mega_menu_mega_menu_component__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! @vex/components/mega-menu/mega-menu.component */ "pXZ5");
/* harmony import */ var _vex_components_popover_popover_service__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! @vex/components/popover/popover.service */ "kYjG");
/* harmony import */ var _vex_services_config_service__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! @vex/services/config.service */ "lC2v");
/* harmony import */ var _vex_services_layout_service__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! @vex/services/layout.service */ "CtTw");
/* harmony import */ var _vex_services_navigation_service__WEBPACK_IMPORTED_MODULE_24__ = __webpack_require__(/*! @vex/services/navigation.service */ "0vMP");
/* harmony import */ var _layout_services_layout_config_service__WEBPACK_IMPORTED_MODULE_25__ = __webpack_require__(/*! @layout/services/layout-config.service */ "U9Lm");
/* harmony import */ var _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_26__ = __webpack_require__(/*! @projects/services/project-data.service */ "oyjd");
/* harmony import */ var _components_toolbar_mock_url_toolbar_mock_url_component__WEBPACK_IMPORTED_MODULE_27__ = __webpack_require__(/*! ./components/toolbar-mock-url/toolbar-mock-url.component */ "O4Sr");




























let ToolbarComponent = class ToolbarComponent {
    constructor(dialog, configService, layoutService, layoutConfigService, navigationService, popoverService, projectDataService) {
        this.dialog = dialog;
        this.configService = configService;
        this.layoutService = layoutService;
        this.layoutConfigService = layoutConfigService;
        this.navigationService = navigationService;
        this.popoverService = popoverService;
        this.projectDataService = projectDataService;
        this.isHorizontalLayout$ = this.configService.config$.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["map"])(config => config.layout === 'horizontal'));
        this.isVerticalLayout$ = this.configService.config$.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["map"])(config => config.layout === 'vertical'));
        this.isNavbarInToolbar$ = this.configService.config$.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["map"])(config => config.navbar.position === 'in-toolbar'));
        this.isNavbarBelowToolbar$ = this.configService.config$.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["map"])(config => config.navbar.position === 'below-toolbar'));
        this.icSearch = _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_19___default.a;
        this.icBookmarks = _iconify_icons_ic_twotone_bookmarks__WEBPACK_IMPORTED_MODULE_12___default.a;
        this.emojioneUS = _iconify_icons_emojione_flag_for_flag_united_states__WEBPACK_IMPORTED_MODULE_7___default.a;
        this.emojioneDE = _iconify_icons_emojione_flag_for_flag_germany__WEBPACK_IMPORTED_MODULE_6___default.a;
        this.icMenu = _iconify_icons_ic_twotone_menu__WEBPACK_IMPORTED_MODULE_15___default.a;
        this.icPersonAdd = _iconify_icons_ic_twotone_person_add__WEBPACK_IMPORTED_MODULE_17___default.a;
        this.icAssignmentTurnedIn = _iconify_icons_ic_twotone_assignment_turned_in__WEBPACK_IMPORTED_MODULE_10___default.a;
        this.icBallot = _iconify_icons_ic_twotone_ballot__WEBPACK_IMPORTED_MODULE_11___default.a;
        this.icDescription = _iconify_icons_ic_twotone_description__WEBPACK_IMPORTED_MODULE_13___default.a;
        this.icAssignment = _iconify_icons_ic_twotone_assignment__WEBPACK_IMPORTED_MODULE_9___default.a;
        this.icReceipt = _iconify_icons_ic_twotone_receipt__WEBPACK_IMPORTED_MODULE_18___default.a;
        this.icDoneAll = _iconify_icons_ic_twotone_done_all__WEBPACK_IMPORTED_MODULE_14___default.a;
        this.icArrowDropDown = _iconify_icons_ic_twotone_arrow_drop_down__WEBPACK_IMPORTED_MODULE_8___default.a;
        this.icPageView = _iconify_icons_ic_twotone_pageview__WEBPACK_IMPORTED_MODULE_16___default.a;
    }
    ngOnInit() {
        this.isProject = this.layoutConfigService.isProject();
        this.isProxied = this.layoutConfigService.isProxied();
        this.isSignedIn = this.layoutConfigService.isSignedIn();
        this.navigationItems = this.navigationService.items;
    }
    ngAfterContentInit() {
        this.project$ = this.projectDataService.project$;
    }
    // View Access
    openQuickpanel() {
        this.layoutService.openQuickpanel();
    }
    openSidenav() {
        this.layoutService.openSidenav();
        this.layoutService.expandSidenav();
    }
    openMegaMenu(origin) {
        this.popoverService.open({
            content: _vex_components_mega_menu_mega_menu_component__WEBPACK_IMPORTED_MODULE_20__["MegaMenuComponent"],
            origin,
            position: [
                {
                    originX: 'start',
                    originY: 'bottom',
                    overlayX: 'start',
                    overlayY: 'top',
                },
                {
                    originX: 'end',
                    originY: 'bottom',
                    overlayX: 'end',
                    overlayY: 'top',
                },
            ],
        });
    }
    openSearch() {
        this.layoutService.openSearch();
    }
    showMockUrl() {
        const popoverRef = this.dialog.open(_components_toolbar_mock_url_toolbar_mock_url_component__WEBPACK_IMPORTED_MODULE_27__["ToolbarMockUrlComponent"], {
            width: '600px',
        });
        popoverRef.afterClosed().subscribe(() => {
        });
    }
};
ToolbarComponent.ctorParameters = () => [
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_4__["MatDialog"] },
    { type: _vex_services_config_service__WEBPACK_IMPORTED_MODULE_22__["ConfigService"] },
    { type: _vex_services_layout_service__WEBPACK_IMPORTED_MODULE_23__["LayoutService"] },
    { type: _layout_services_layout_config_service__WEBPACK_IMPORTED_MODULE_25__["LayoutConfigService"] },
    { type: _vex_services_navigation_service__WEBPACK_IMPORTED_MODULE_24__["NavigationService"] },
    { type: _vex_components_popover_popover_service__WEBPACK_IMPORTED_MODULE_21__["PopoverService"] },
    { type: _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_26__["ProjectDataService"] }
];
ToolbarComponent.propDecorators = {
    mobileQuery: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"] }],
    hasShadow: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"] }, { type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["HostBinding"], args: ['class.shadow-b',] }]
};
ToolbarComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'vex-toolbar',
        template: _raw_loader_toolbar_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_toolbar_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], ToolbarComponent);



/***/ }),

/***/ "cwwZ":
/*!******************************************!*\
  !*** ./src/@vex/layout/layout.module.ts ***!
  \******************************************/
/*! exports provided: LayoutModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LayoutModule", function() { return LayoutModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_material_sidenav__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/material/sidenav */ "q7Ft");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _components_progress_bar_progress_bar_module__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../components/progress-bar/progress-bar.module */ "Li13");
/* harmony import */ var _components_search_search_module__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../components/search/search.module */ "7a8g");
/* harmony import */ var _layout_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./layout.component */ "ynKk");








let LayoutModule = class LayoutModule {
};
LayoutModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_layout_component__WEBPACK_IMPORTED_MODULE_7__["LayoutComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_router__WEBPACK_IMPORTED_MODULE_4__["RouterModule"],
            _angular_material_sidenav__WEBPACK_IMPORTED_MODULE_3__["MatSidenavModule"],
            _components_progress_bar_progress_bar_module__WEBPACK_IMPORTED_MODULE_5__["ProgressBarModule"],
            _components_search_search_module__WEBPACK_IMPORTED_MODULE_6__["SearchModule"]
        ],
        exports: [_layout_component__WEBPACK_IMPORTED_MODULE_7__["LayoutComponent"]]
    })
], LayoutModule);



/***/ }),

/***/ "d5u2":
/*!************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/@vex/components/sidenav-item/sidenav-item.component.html ***!
  \************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<a *ngIf=\"isLink(item) && !isFunction(item.handleClick) && item.isVisible()\"\r\n  [class.active]=\"isActive\"\r\n  [fragment]=\"item.fragment\"\r\n  [routerLinkActiveOptions]=\"item.routerLinkActive || { exact: false }\"\r\n  [routerLink]=\"item.route\"\r\n  class=\"item\"\r\n  fxLayout=\"row\"\r\n  matRipple\r\n  routerLinkActive=\"active\">\r\n  <mat-icon *ngIf=\"level === 0\" [icIcon]=\"item.icon\" class=\"item-icon\" fxFlex=\"none\"></mat-icon>\r\n  <span class=\"item-label\" fxFlex=\"auto\">{{ item.label }}</span>\r\n  <span *ngIf=\"item.badge\"\r\n        [style.background]=\"item.badge.background\"\r\n        [style.color]=\"item.badge.color\"\r\n        class=\"item-badge\"\r\n        fxFlex=\"none\">{{ item.badge.value }}</span>\r\n</a>\r\n\r\n<div (click)=\"item.handleClick()\"\r\n  [class.active]=\"isActive\"\r\n  *ngIf=\"item.isVisible() && isLink(item) && isFunction(item.handleClick)\"\r\n  class=\"item\"\r\n  fxLayout=\"row\"\r\n  matRipple\r\n  routerLinkActive=\"active\">\r\n  <mat-icon *ngIf=\"level === 0\" [icIcon]=\"item.icon\" class=\"item-icon\" fxFlex=\"none\"></mat-icon>\r\n  <span class=\"item-label\" fxFlex=\"auto\">{{ item.label }}</span>\r\n  <span *ngIf=\"item.badge\"\r\n        [style.background]=\"item.badge.background\"\r\n        [style.color]=\"item.badge.color\"\r\n        class=\"item-badge\"\r\n        fxFlex=\"none\">{{ item.badge.value }}</span>\r\n</div>\r\n\r\n<ng-container *ngIf=\"isDropdown(item)\">\r\n  <div (click)=\"toggleOpen()\"\r\n    [class.active]=\"isOpen || isActive\"\r\n    [class.open]=\"isOpen\"\r\n    class=\"item\"\r\n    fxLayout=\"row\"\r\n    matRipple>\r\n    <mat-icon *ngIf=\"level === 0\" [icIcon]=\"item.icon\" class=\"item-icon\" fxFlex=\"none\"></mat-icon>\r\n    <span class=\"item-label\" fxFlex=\"auto\">{{ item.label }}</span>\r\n    <span *ngIf=\"item.badge\"\r\n          [style.background]=\"item.badge.background\"\r\n          [style.color]=\"item.badge.color\"\r\n          class=\"item-badge\"\r\n          fxFlex=\"none\">{{ item.badge.value }}</span>\r\n    <mat-icon [icIcon]=\"icKeyboardArrowRight\" class=\"item-dropdown-icon\" fxFlex=\"none\"></mat-icon>\r\n  </div>\r\n  <div [@dropdown]=\"isOpen\" class=\"item-dropdown\">\r\n    <vex-sidenav-item *ngFor=\"let subItem of item.children\" [item]=\"subItem\" [level]=\"level + 1\"></vex-sidenav-item>\r\n  </div>\r\n</ng-container>\r\n\r\n\r\n<ng-container *ngIf=\"isSubheading(item)\">\r\n  <div class=\"subheading\">{{ item.label }}</div>\r\n  <vex-sidenav-item *ngFor=\"let subItem of item.children\" [item]=\"subItem\" [level]=\"0\"></vex-sidenav-item>\r\n</ng-container>\r\n\r\n");

/***/ }),

/***/ "dGqQ":
/*!****************************************************************************************************************************!*\
  !*** ./src/app/layout/components/toolbar/components/toolbar-user/toolbar-user-dropdown/toolbar-user-dropdown.component.ts ***!
  \****************************************************************************************************************************/
/*! exports provided: ToolbarUserDropdownComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ToolbarUserDropdownComponent", function() { return ToolbarUserDropdownComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_toolbar_user_dropdown_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./toolbar-user-dropdown.component.html */ "G605");
/* harmony import */ var _toolbar_user_dropdown_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./toolbar-user-dropdown.component.scss */ "CZ7+");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var angular_token__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! angular-token */ "hU4o");
/* harmony import */ var _vex_components_popover_popover_ref__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @vex/components/popover/popover-ref */ "QaI9");
/* harmony import */ var _vex_utils_track_by__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @vex/utils/track-by */ "zK3P");
/* harmony import */ var _data_constants_route_constants__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @data/constants/route.constants */ "wZfh");
/* harmony import */ var _users_services_user_data_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @users/services/user-data.service */ "O7ya");
/* harmony import */ var _services_toolbar_user_dropdown_icons_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./services/toolbar-user-dropdown-icons.service */ "3v0u");











let ToolbarUserDropdownComponent = class ToolbarUserDropdownComponent {
    constructor(icons, cd, popoverRef, router, tokenService, userData) {
        this.icons = icons;
        this.cd = cd;
        this.popoverRef = popoverRef;
        this.router = router;
        this.tokenService = tokenService;
        this.userData = userData;
        this.trackById = _vex_utils_track_by__WEBPACK_IMPORTED_MODULE_7__["trackById"];
    }
    ngOnInit() {
        this.user$ = this.userData.get();
        this.user$.subscribe(user => {
            this.user = user;
            this.items = [
                {
                    id: '1',
                    icon: this.icons.icAccountCircle,
                    label: 'My Profile',
                    description: 'Personal Information',
                    colorClass: 'text-teal-500',
                    route: `/users/${user.id}/profile`,
                },
                // {
                //   id: '2',
                //   icon: icMoveToInbox,
                //   label: 'My Inbox',
                //   description: 'Messages & Latest News',
                //   colorClass: 'text-primary-500',
                //   route: '/apps/chat'
                // },
                {
                    id: '3',
                    icon: this.icons.icListAlt,
                    label: 'My Projects',
                    description: 'Tasks & Active Projects',
                    colorClass: 'text-amber-500',
                    route: '/projects',
                },
                {
                    id: '4',
                    icon: this.icons.icTableChart,
                    label: 'Billing Information',
                    description: 'Pricing & Current Plan',
                    colorClass: 'text-purple-500',
                    route: `/users/${user.id}/billing`,
                },
            ];
        });
        this.statuses = [
            {
                id: 'online',
                label: 'Online',
                icon: this.icons.icCheckCircle,
                colorClass: 'text-green-500',
            },
            {
                id: 'away',
                label: 'Away',
                icon: this.icons.icAccessTime,
                colorClass: 'text-orange-500',
            },
            {
                id: 'dnd',
                label: 'Do not disturb',
                icon: this.icons.icDoNotDisturb,
                colorClass: 'text-red-500',
            },
            {
                id: 'offline',
                label: 'Offline',
                icon: this.icons.icOfflineBolt,
                colorClass: 'text-gray-500',
            },
        ];
        this.activeStatus = this.statuses[0];
    }
    setStatus(status) {
        this.activeStatus = status;
        this.cd.markForCheck();
    }
    logout() {
        this.tokenService.signOut().subscribe(res => {
            this.popoverRef.close();
            this.router.navigateByUrl(_data_constants_route_constants__WEBPACK_IMPORTED_MODULE_8__["RouteConstants"].LOGIN_PAGE);
        });
    }
};
ToolbarUserDropdownComponent.ctorParameters = () => [
    { type: _services_toolbar_user_dropdown_icons_service__WEBPACK_IMPORTED_MODULE_10__["ToolbarUserDropdownIcons"] },
    { type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ChangeDetectorRef"] },
    { type: _vex_components_popover_popover_ref__WEBPACK_IMPORTED_MODULE_6__["PopoverRef"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["Router"] },
    { type: angular_token__WEBPACK_IMPORTED_MODULE_5__["AngularTokenService"] },
    { type: _users_services_user_data_service__WEBPACK_IMPORTED_MODULE_9__["UserDataService"] }
];
ToolbarUserDropdownComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'vex-toolbar-user-dropdown',
        template: _raw_loader_toolbar_user_dropdown_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ChangeDetectionStrategy"].OnPush,
        styles: [_toolbar_user_dropdown_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], ToolbarUserDropdownComponent);



/***/ }),

/***/ "dO6N":
/*!**********************************************************************!*\
  !*** ./src/@vex/components/config-panel/config-panel.component.scss ***!
  \**********************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (".config-panel {\n  padding: var(--padding-16) var(--padding);\n}\n\n.heading {\n  margin-bottom: var(--padding);\n}\n\n.section {\n  border-bottom: 1px solid var(--foreground-divider);\n  margin-bottom: var(--padding-16);\n  padding-bottom: var(--padding-16);\n}\n\n.section:last-child {\n  border-bottom: none;\n}\n\n.section-content {\n  -webkit-margin-start: var(--padding-12);\n          margin-inline-start: var(--padding-12);\n}\n\n.section-content .subheading {\n  margin-top: var(--padding);\n}\n\n.subheading {\n  margin-top: 1rem;\n  margin-bottom: 1rem;\n  text-transform: uppercase;\n  font-size: 0.75rem;\n  color: var(--text-secondary);\n  font-weight: 500;\n}\n\n.layout + .layout {\n  margin-top: var(--padding);\n}\n\n.layout-image:hover .layout-image-overlay {\n  background: rgba(0, 0, 0, 0.7);\n  opacity: 1;\n  visibility: visible;\n}\n\n.layout-image .layout-image-overlay {\n  border-radius: var(--border-radius);\n  bottom: 0;\n  height: 100%;\n  left: 0;\n  opacity: 0;\n  position: absolute;\n  right: 0;\n  top: 0;\n  transition: var(--trans-ease-out);\n  visibility: hidden;\n  width: 100%;\n}\n\n.layout-image .layout-image-overlay button {\n  padding: 0 8px;\n}\n\n.color {\n  align-items: center;\n  border-radius: 50%;\n  box-shadow: var(--elevation-z8);\n  display: flex;\n  flex-direction: row;\n  height: 36px;\n  justify-content: center;\n  -webkit-margin-end: var(--padding-16);\n          margin-inline-end: var(--padding-16);\n  text-align: center;\n  vertical-align: middle;\n  width: 36px;\n}\n\n.color.light {\n  background: white;\n  color: #000;\n}\n\n.color.dark {\n  background: #303030;\n  color: white;\n}\n\n.color.flat {\n  background: #f5f5f5;\n  color: #000;\n}\n\nmat-slide-toggle + mat-slide-toggle,\nmat-slide-toggle + mat-checkbox,\nmat-checkbox + mat-slide-toggle,\nmat-checkbox + mat-checkbox {\n  display: block;\n  margin-top: var(--padding-12);\n}\n\n.style-name {\n  font: var(--font-body-2);\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uL2NvbmZpZy1wYW5lbC5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLHlDQUFBO0FBQ0Y7O0FBRUE7RUFDRSw2QkFBQTtBQUNGOztBQUVBO0VBQ0Usa0RBQUE7RUFDQSxnQ0FBQTtFQUNBLGlDQUFBO0FBQ0Y7O0FBRUE7RUFDRSxtQkFBQTtBQUNGOztBQUVBO0VBQ0UsdUNBQUE7VUFBQSxzQ0FBQTtBQUNGOztBQUVBO0VBQ0UsMEJBQUE7QUFDRjs7QUFFQTtFQUNFLGdCQUFBO0VBQ0EsbUJBQUE7RUFDQSx5QkFBQTtFQUNBLGtCQUFBO0VBQ0EsNEJBQUE7RUFDQSxnQkFBQTtBQUNGOztBQUVBO0VBQ0UsMEJBQUE7QUFDRjs7QUFFQTtFQUNFLDhCQUFBO0VBQ0EsVUFBQTtFQUNBLG1CQUFBO0FBQ0Y7O0FBRUE7RUFDRSxtQ0FBQTtFQUNBLFNBQUE7RUFDQSxZQUFBO0VBQ0EsT0FBQTtFQUNBLFVBQUE7RUFDQSxrQkFBQTtFQUNBLFFBQUE7RUFDQSxNQUFBO0VBQ0EsaUNBQUE7RUFDQSxrQkFBQTtFQUNBLFdBQUE7QUFDRjs7QUFFQTtFQUNFLGNBQUE7QUFDRjs7QUFFQTtFQUNFLG1CQUFBO0VBQ0Esa0JBQUE7RUFDQSwrQkFBQTtFQUNBLGFBQUE7RUFDQSxtQkFBQTtFQUNBLFlBQUE7RUFDQSx1QkFBQTtFQUNBLHFDQUFBO1VBQUEsb0NBQUE7RUFDQSxrQkFBQTtFQUNBLHNCQUFBO0VBQ0EsV0FBQTtBQUNGOztBQUVBO0VBQ0UsaUJBQUE7RUFDQSxXQUFBO0FBQ0Y7O0FBRUE7RUFDRSxtQkFBQTtFQUNBLFlBQUE7QUFDRjs7QUFFQTtFQUNFLG1CQUFBO0VBQ0EsV0FBQTtBQUNGOztBQUVBOzs7O0VBSUUsY0FBQTtFQUNBLDZCQUFBO0FBQ0Y7O0FBRUE7RUFDRSx3QkFBQTtBQUNGIiwiZmlsZSI6ImNvbmZpZy1wYW5lbC5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbIi5jb25maWctcGFuZWwge1xuICBwYWRkaW5nOiB2YXIoLS1wYWRkaW5nLTE2KSB2YXIoLS1wYWRkaW5nKTtcbn1cblxuLmhlYWRpbmcge1xuICBtYXJnaW4tYm90dG9tOiB2YXIoLS1wYWRkaW5nKTtcbn1cblxuLnNlY3Rpb24ge1xuICBib3JkZXItYm90dG9tOiAxcHggc29saWQgdmFyKC0tZm9yZWdyb3VuZC1kaXZpZGVyKTtcbiAgbWFyZ2luLWJvdHRvbTogdmFyKC0tcGFkZGluZy0xNik7XG4gIHBhZGRpbmctYm90dG9tOiB2YXIoLS1wYWRkaW5nLTE2KTtcbn1cblxuLnNlY3Rpb246bGFzdC1jaGlsZCB7XG4gIGJvcmRlci1ib3R0b206IG5vbmU7XG59XG5cbi5zZWN0aW9uLWNvbnRlbnQge1xuICBtYXJnaW4taW5saW5lLXN0YXJ0OiB2YXIoLS1wYWRkaW5nLTEyKTtcbn1cblxuLnNlY3Rpb24tY29udGVudCAuc3ViaGVhZGluZyB7XG4gIG1hcmdpbi10b3A6IHZhcigtLXBhZGRpbmcpO1xufVxuXG4uc3ViaGVhZGluZyB7XG4gIG1hcmdpbi10b3A6IDFyZW07XG4gIG1hcmdpbi1ib3R0b206IDFyZW07XG4gIHRleHQtdHJhbnNmb3JtOiB1cHBlcmNhc2U7XG4gIGZvbnQtc2l6ZTogMC43NXJlbTtcbiAgY29sb3I6IHZhcigtLXRleHQtc2Vjb25kYXJ5KTtcbiAgZm9udC13ZWlnaHQ6IDUwMDtcbn1cblxuLmxheW91dCArIC5sYXlvdXQge1xuICBtYXJnaW4tdG9wOiB2YXIoLS1wYWRkaW5nKTtcbn1cblxuLmxheW91dC1pbWFnZTpob3ZlciAubGF5b3V0LWltYWdlLW92ZXJsYXkge1xuICBiYWNrZ3JvdW5kOiByZ2JhKDAsIDAsIDAsIDAuNyk7XG4gIG9wYWNpdHk6IDE7XG4gIHZpc2liaWxpdHk6IHZpc2libGU7XG59XG5cbi5sYXlvdXQtaW1hZ2UgLmxheW91dC1pbWFnZS1vdmVybGF5IHtcbiAgYm9yZGVyLXJhZGl1czogdmFyKC0tYm9yZGVyLXJhZGl1cyk7XG4gIGJvdHRvbTogMDtcbiAgaGVpZ2h0OiAxMDAlO1xuICBsZWZ0OiAwO1xuICBvcGFjaXR5OiAwO1xuICBwb3NpdGlvbjogYWJzb2x1dGU7XG4gIHJpZ2h0OiAwO1xuICB0b3A6IDA7XG4gIHRyYW5zaXRpb246IHZhcigtLXRyYW5zLWVhc2Utb3V0KTtcbiAgdmlzaWJpbGl0eTogaGlkZGVuO1xuICB3aWR0aDogMTAwJTtcbn1cblxuLmxheW91dC1pbWFnZSAubGF5b3V0LWltYWdlLW92ZXJsYXkgYnV0dG9uIHtcbiAgcGFkZGluZzogMCA4cHg7XG59XG5cbi5jb2xvciB7XG4gIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG4gIGJvcmRlci1yYWRpdXM6IDUwJTtcbiAgYm94LXNoYWRvdzogdmFyKC0tZWxldmF0aW9uLXo4KTtcbiAgZGlzcGxheTogZmxleDtcbiAgZmxleC1kaXJlY3Rpb246IHJvdztcbiAgaGVpZ2h0OiAzNnB4O1xuICBqdXN0aWZ5LWNvbnRlbnQ6IGNlbnRlcjtcbiAgbWFyZ2luLWlubGluZS1lbmQ6IHZhcigtLXBhZGRpbmctMTYpO1xuICB0ZXh0LWFsaWduOiBjZW50ZXI7XG4gIHZlcnRpY2FsLWFsaWduOiBtaWRkbGU7XG4gIHdpZHRoOiAzNnB4O1xufVxuXG4uY29sb3IubGlnaHQge1xuICBiYWNrZ3JvdW5kOiB3aGl0ZTtcbiAgY29sb3I6ICMwMDA7XG59XG5cbi5jb2xvci5kYXJrIHtcbiAgYmFja2dyb3VuZDogIzMwMzAzMDtcbiAgY29sb3I6IHdoaXRlO1xufVxuXG4uY29sb3IuZmxhdCB7XG4gIGJhY2tncm91bmQ6ICNmNWY1ZjU7XG4gIGNvbG9yOiAjMDAwO1xufVxuXG5tYXQtc2xpZGUtdG9nZ2xlICsgbWF0LXNsaWRlLXRvZ2dsZSxcbm1hdC1zbGlkZS10b2dnbGUgKyBtYXQtY2hlY2tib3gsXG5tYXQtY2hlY2tib3ggKyBtYXQtc2xpZGUtdG9nZ2xlLFxubWF0LWNoZWNrYm94ICsgbWF0LWNoZWNrYm94IHtcbiAgZGlzcGxheTogYmxvY2s7XG4gIG1hcmdpbi10b3A6IHZhcigtLXBhZGRpbmctMTIpO1xufVxuXG4uc3R5bGUtbmFtZSB7XG4gIGZvbnQ6IHZhcigtLWZvbnQtYm9keS0yKTtcbn0iXX0= */");

/***/ }),

/***/ "dPIg":
/*!************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/@vex/components/search/search.component.html ***!
  \************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div (keyup.escape)=\"close()\" [class.show]=\"show$ | async\" class=\"search\">\n  <button (click)=\"close()\"\n          class=\"ltr:right-12 rtl:left-12 top-12 absolute\"\n          color=\"primary\"\n          mat-icon-button\n          type=\"button\">\n    <mat-icon [icIcon]=\"icClose\"></mat-icon>\n  </button>\n\n  <input #searchInput (keyup.enter)=\"search()\" [formControl]=\"searchCtrl\" class=\"search-input\" placeholder=\"Search...\"/>\n  <div class=\"search-hint\">Hit enter to search</div>\n</div>\n\n<div (click)=\"close()\" *ngIf=\"show$ | async\" class=\"search-overlay\"></div>\n\n");

/***/ }),

/***/ "f/93":
/*!*****************************************************************************************************************************************************!*\
  !*** ./src/app/layout/components/toolbar/components/toolbar-proxy-settings/components/toolbar-record-settings/toolbar-record-settings.component.ts ***!
  \*****************************************************************************************************************************************************/
/*! exports provided: ToolbarRecordSettingsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ToolbarRecordSettingsComponent", function() { return ToolbarRecordSettingsComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_toolbar_record_settings_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./toolbar-record-settings.component.html */ "46RW");
/* harmony import */ var _toolbar_record_settings_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./toolbar-record-settings.component.scss */ "SEeg");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ "s7LF");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/dialog */ "iELJ");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! rxjs/operators */ "kU1M");
/* harmony import */ var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @iconify/icons-ic/twotone-close */ "5mnX");
/* harmony import */ var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @iconify/icons-ic/twotone-delete */ "e3EN");
/* harmony import */ var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _core_http_agent_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @core/http/agent.service */ "/JUU");
/* harmony import */ var _core_http_scenario_resource_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @core/http/scenario-resource.service */ "3Ncz");
/* harmony import */ var _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @projects/services/project-data.service */ "oyjd");
/* harmony import */ var _projects_services_projects_data_service__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @projects/services/projects-data.service */ "mbNh");
/* harmony import */ var _users_services_user_data_service__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @users/services/user-data.service */ "O7ya");
/* harmony import */ var _schema_agent_config__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ../../schema/agent-config */ "nmZq");















let ToolbarRecordSettingsComponent = class ToolbarRecordSettingsComponent {
    constructor(dialogRef, fb, agentService, projectDataService, scenarioResource, userDataService, projectsDataService) {
        this.dialogRef = dialogRef;
        this.fb = fb;
        this.agentService = agentService;
        this.projectDataService = projectDataService;
        this.scenarioResource = scenarioResource;
        this.userDataService = userDataService;
        this.projectsDataService = projectsDataService;
        this.onProjectChange = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
        this.onScenarioChange = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
        this.scenarios = [];
        this.icClose = _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_7___default.a;
        this.icDelete = _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_8___default.a;
    }
    ngOnInit() {
        // Initialize form
        this.form = this.fb.group({
            excludePatterns: this.fb.array([]),
            includePatterns: this.fb.array([]),
            project: new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"](null, [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required]),
            recordPolicy: new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"]('all', [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required]),
            scenario: new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"](null),
            serviceUrl: new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"](''),
        });
        this.initializePolicies();
        this.initializeConfig().subscribe((res) => {
            this.initializeProjects$(this.config);
            this.initializeProject(this.config);
            this.initializeScenarios(this.config);
        });
    }
    // API Access
    getScenarios(projectId) {
        projectId = projectId || this.project.id;
        return this.scenarioResource.index({ project_id: projectId }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["tap"])((res) => {
            this.scenarios = res.list;
        }));
    }
    // View Access
    clearScenario() {
        this.form.patchValue({
            scenario: null,
        });
    }
    clearServiceUrl() {
        this.form.patchValue({
            serviceUrl: null,
        });
    }
    addIncludePattern(pattern) {
        const includePatterns = this.form.get('includePatterns');
        includePatterns.push(this.fb.group({
            pattern: new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"](pattern || '', [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required]),
        }));
    }
    removeIncludePattern(index) {
        const includePatterns = this.form.get('includePatterns');
        includePatterns.removeAt(index);
    }
    addExcludePattern(pattern) {
        const excludePatterns = this.form.get('excludePatterns');
        excludePatterns.push(this.fb.group({
            pattern: new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"](pattern || '', [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required]),
        }));
    }
    removeExcludePattern(index) {
        const excludePatterns = this.form.get('excludePatterns');
        excludePatterns.removeAt(index);
    }
    selectProject($event) {
        const project = $event.value;
        this.getScenarios(project.id).subscribe();
        this.form.patchValue({
            scenario: null,
        });
        this.project = project;
    }
    update() {
        const formValue = this.form.value;
        const user = this.userDataService.user;
        const project = formValue.project;
        const config = {
            api_key: user.apiKey,
            mode: {
                record: {
                    active: this.config.mode.record.active,
                    exclude_patterns: formValue.excludePatterns.map(data => data.pattern),
                    include_patterns: formValue.includePatterns.map(data => data.pattern),
                    policy: formValue.recordPolicy,
                    project_key: formValue.project.key,
                    scenario_key: '',
                    service_url: formValue.serviceUrl || '',
                },
            },
        };
        if (formValue.scenario) {
            const scenario = formValue.scenario;
            config.mode.record.scenario_key = scenario.key;
            this.onScenarioChange.emit(scenario);
        }
        this.onProjectChange.emit(project);
        if (config) {
            this.agentService.updateConfig(config).subscribe(res => {
                this.dialogRef.close();
            });
        }
        else {
            this.agentService.createConfig(config).subscribe(res => {
                this.dialogRef.close();
            });
        }
    }
    // Helpers
    initializePolicies() {
        this.agentService.showConfigsPolicies().subscribe(res => {
            this.policies = Object.values(res);
        });
    }
    initializeConfig() {
        return this.agentService.showConfig().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["tap"])((res) => {
            const config = res;
            if (config) {
                this.config = new _schema_agent_config__WEBPACK_IMPORTED_MODULE_14__["AgentConfig"](config);
                this.form.patchValue({
                    recordPolicy: this.config.mode.record.policy,
                    serviceUrl: this.config.mode.record.serviceUrl,
                });
                this.config.mode.record.includePatterns.forEach(pattern => {
                    this.addIncludePattern(pattern);
                });
                this.config.mode.record.excludePatterns.forEach(pattern => {
                    this.addExcludePattern(pattern);
                });
            }
        }));
    }
    // Set projects$ observable
    initializeProjects$(config) {
        if (!this.projectsDataService.projects) {
            const organizationId = this.projectDataService.project.organizationId;
            this.projectsDataService.fetch(organizationId);
        }
        this.projects$ = this.projectsDataService.projects$;
    }
    initializeProject(config) {
        if (!config.mode.record.projectKey) {
            this.project = this.projectDataService.project;
            this.form.patchValue({
                project: this.project,
            });
            this.update();
        }
        else {
            this.projects$.subscribe((projects) => {
                projects.some(project => {
                    if (config.mode.record.projectKey === project.key) {
                        this.project = project;
                        this.form.patchValue({
                            project,
                        });
                        return true;
                    }
                });
            });
        }
    }
    initializeScenarios(config) {
        if (this.project) {
            this.getScenarios(this.project.id).subscribe(res => {
                this.scenarios.some(scenario => {
                    if (config.mode.record.scenarioKey === scenario.key) {
                        this.form.patchValue({
                            scenario,
                        });
                        return true;
                    }
                });
            });
        }
    }
};
ToolbarRecordSettingsComponent.ctorParameters = () => [
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MatDialogRef"] },
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormBuilder"] },
    { type: _core_http_agent_service__WEBPACK_IMPORTED_MODULE_9__["AgentService"] },
    { type: _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_11__["ProjectDataService"] },
    { type: _core_http_scenario_resource_service__WEBPACK_IMPORTED_MODULE_10__["ScenarioResource"] },
    { type: _users_services_user_data_service__WEBPACK_IMPORTED_MODULE_13__["UserDataService"] },
    { type: _projects_services_projects_data_service__WEBPACK_IMPORTED_MODULE_12__["ProjectsDataService"] }
];
ToolbarRecordSettingsComponent.propDecorators = {
    onProjectChange: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Output"] }],
    onScenarioChange: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Output"] }]
};
ToolbarRecordSettingsComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'vex-toolbar-record-settings',
        template: _raw_loader_toolbar_record_settings_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_toolbar_record_settings_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], ToolbarRecordSettingsComponent);



/***/ }),

/***/ "fQJz":
/*!************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/@vex/components/config-panel/config-panel.component.html ***!
  \************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div *ngIf=\"config$ | async as setting\" class=\"config-panel\">\r\n  <h2 class=\"headline mb-4\">\r\n    <ic-icon [icon]=\"icSettings\" class=\"mr-3\" inline=\"true\"></ic-icon>\r\n    <span>Configuration</span>\r\n  </h2>\r\n\r\n  <div class=\"section\">\r\n    <h5 class=\"subheading\">THEME STYLE</h5>\r\n\r\n    <div *ngFor=\"let config of configs; let first = first\"\r\n         [class.mt-6]=\"!first\"\r\n         class=\"rounded\">\r\n      <div class=\"layout-image rounded overflow-hidden relative hover:bg-hover shadow-8\">\r\n        <img [src]=\"config.imgSrc\" class=\"w-full block\">\r\n        <div class=\"layout-image-overlay\" fxLayout=\"row\" fxLayoutAlign=\"center center\" fxLayoutGap=\"4px\">\r\n          <button (click)=\"setConfig(config.id, Style.light)\"\r\n                  class=\"bg-contrast-white text-contrast-black\"\r\n                  fxFlex=\"none\"\r\n                  mat-raised-button\r\n                  type=\"button\">LIGHT\r\n          </button>\r\n          <button (click)=\"setConfig(config.id, Style.default)\"\r\n                  color=\"primary\"\r\n                  fxFlex=\"none\"\r\n                  mat-raised-button\r\n                  type=\"button\">DEFAULT\r\n          </button>\r\n          <button (click)=\"setConfig(config.id, Style.dark)\"\r\n                  class=\"bg-contrast-black text-contrast-white\"\r\n                  fxFlex=\"none\"\r\n                  mat-raised-button\r\n                  type=\"button\">DARK\r\n          </button>\r\n        </div>\r\n      </div>\r\n      <div class=\"text-center body-2 mt-2\">{{ config.name }}</div>\r\n    </div>\r\n  </div>\r\n\r\n  <div class=\"section\">\r\n    <h5 class=\"subheading\">LAYOUT</h5>\r\n\r\n    <div class=\"section-content\">\r\n      <h5 class=\"subheading\">ORIENTATION</h5>\r\n\r\n      <mat-slide-toggle (change)=\"layoutRTLChange($event)\" [checked]=\"isRTL$ | async\">RTL</mat-slide-toggle>\r\n    </div>\r\n  </div>\r\n\r\n  <div class=\"section\">\r\n    <h5 class=\"subheading\">TOOLBAR</h5>\r\n\r\n    <div class=\"section-content\">\r\n      <h5 class=\"subheading\">POSITION</h5>\r\n\r\n      <mat-radio-group (change)=\"toolbarPositionChange($event)\"\r\n                       [value]=\"setting.toolbar.fixed ? 'fixed' : 'static'\"\r\n                       fxLayout=\"column\"\r\n                       fxLayoutGap=\"12px\">\r\n        <mat-radio-button value=\"fixed\">Fixed</mat-radio-button>\r\n        <mat-radio-button value=\"static\">Static</mat-radio-button>\r\n      </mat-radio-group>\r\n    </div>\r\n  </div>\r\n\r\n  <div class=\"section\">\r\n    <h5 class=\"subheading\">FOOTER</h5>\r\n\r\n    <div class=\"section-content\">\r\n      <mat-slide-toggle (change)=\"footerVisibleChange($event)\" [checked]=\"setting.footer.visible\">Visible\r\n      </mat-slide-toggle>\r\n\r\n      <h5 class=\"subheading\">POSITION</h5>\r\n\r\n      <mat-radio-group (change)=\"footerPositionChange($event)\"\r\n                       [value]=\"setting.footer.fixed ? 'fixed' : 'static'\"\r\n                       fxLayout=\"column\"\r\n                       fxLayoutGap=\"12px\">\r\n        <mat-radio-button value=\"fixed\">Fixed</mat-radio-button>\r\n        <mat-radio-button value=\"static\">Static</mat-radio-button>\r\n      </mat-radio-group>\r\n    </div>\r\n  </div>\r\n</div>\r\n");

/***/ }),

/***/ "fzgV":
/*!**********************************************************************!*\
  !*** ./src/@vex/pipes/relative-date-time/relative-date-time.pipe.ts ***!
  \**********************************************************************/
/*! exports provided: RelativeDateTimePipe */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RelativeDateTimePipe", function() { return RelativeDateTimePipe; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");


let RelativeDateTimePipe = class RelativeDateTimePipe {
    transform(value, ...args) {
        return value ? value.toRelative() : null;
    }
};
RelativeDateTimePipe = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Pipe"])({
        name: 'relativeDateTime'
    })
], RelativeDateTimePipe);



/***/ }),

/***/ "gDAd":
/*!*********************************************************************!*\
  !*** ./src/@vex/components/toolbar-search/toolbar-search.module.ts ***!
  \*********************************************************************/
/*! exports provided: ToolbarSearchModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ToolbarSearchModule", function() { return ToolbarSearchModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/input */ "e6WT");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _toolbar_search_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./toolbar-search.component */ "jXNf");









let ToolbarSearchModule = class ToolbarSearchModule {
};
ToolbarSearchModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_toolbar_search_component__WEBPACK_IMPORTED_MODULE_8__["ToolbarSearchComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_material_input__WEBPACK_IMPORTED_MODULE_6__["MatInputModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_4__["MatButtonModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_5__["MatIconModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_7__["IconModule"]
        ],
        exports: [_toolbar_search_component__WEBPACK_IMPORTED_MODULE_8__["ToolbarSearchComponent"]]
    })
], ToolbarSearchModule);



/***/ }),

/***/ "gHic":
/*!*******************************************!*\
  !*** ./src/app/core/http/http.service.ts ***!
  \*******************************************/
/*! exports provided: HttpService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "HttpService", function() { return HttpService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common/http */ "IheW");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @environments/environment */ "AytR");
/* harmony import */ var _url_builder__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./url-builder */ "OZ7D");





let HttpService = class HttpService {
    constructor(http) {
        this.http = http;
    }
    mergeQueryParams(url, params) {
        let queryString = '';
        for (const key in params) {
            if (!queryString) {
                queryString = `?${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`;
            }
            else {
                queryString += `&${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`;
            }
        }
        return url + queryString;
    }
    get(url, params, options) {
        return this.http.get(this.mergeQueryParams(url, params), options);
    }
    post(url, postBody, options) {
        return this.http.post(url, postBody, options);
    }
    delete(url, params, options) {
        return this.http.delete(this.mergeQueryParams(url, params));
    }
    put(url, putData, options) {
        return this.http.put(url, putData, options);
    }
    upload(url, file, options) {
        const formData = new FormData();
        if (file) {
            formData.append('files', file, file.name);
        }
        return this.post(url, formData, options);
    }
    buildUrl(pathComponents, queryParams) {
        const urlBuilder = new _url_builder__WEBPACK_IMPORTED_MODULE_4__["UrlBuilder"]();
        urlBuilder.withPath(_environments_environment__WEBPACK_IMPORTED_MODULE_3__["environment"].apiUrl);
        for (const pathComponent of pathComponents) {
            urlBuilder.
                withPath(pathComponent.toString());
        }
        for (const queryParam in queryParams) {
            if (queryParams.hasOwnProperty(queryParam)) {
                urlBuilder.
                    search(queryParam, queryParams[queryParam]);
            }
        }
        return urlBuilder.url;
    }
};
HttpService.ctorParameters = () => [
    { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpClient"] }
];
HttpService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["Injectable"])({
        providedIn: 'root',
    })
], HttpService);



/***/ }),

/***/ "gX/z":
/*!*******************************************************!*\
  !*** ./src/@vex/components/popover/popover.module.ts ***!
  \*******************************************************/
/*! exports provided: PopoverModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PopoverModule", function() { return PopoverModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_cdk_overlay__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/cdk/overlay */ "1O3W");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _popover_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./popover.component */ "NEAy");





let PopoverModule = class PopoverModule {
};
PopoverModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["NgModule"])({
        declarations: [_popover_component__WEBPACK_IMPORTED_MODULE_4__["PopoverComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _angular_cdk_overlay__WEBPACK_IMPORTED_MODULE_1__["OverlayModule"]
        ],
        entryComponents: [_popover_component__WEBPACK_IMPORTED_MODULE_4__["PopoverComponent"]]
    })
], PopoverModule);



/***/ }),

/***/ "h4uD":
/*!************************************************************************!*\
  !*** ./src/@vex/pipes/relative-date-time/relative-date-time.module.ts ***!
  \************************************************************************/
/*! exports provided: RelativeDateTimeModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RelativeDateTimeModule", function() { return RelativeDateTimeModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _relative_date_time_pipe__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./relative-date-time.pipe */ "fzgV");




let RelativeDateTimeModule = class RelativeDateTimeModule {
};
RelativeDateTimeModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_relative_date_time_pipe__WEBPACK_IMPORTED_MODULE_3__["RelativeDateTimePipe"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"]
        ],
        exports: [_relative_date_time_pipe__WEBPACK_IMPORTED_MODULE_3__["RelativeDateTimePipe"]]
    })
], RelativeDateTimeModule);



/***/ }),

/***/ "hX/M":
/*!*****************************************************************!*\
  !*** ./src/app/core/http/path-segment-name-resource.service.ts ***!
  \*****************************************************************/
/*! exports provided: PathSegmentNameResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PathSegmentNameResource", function() { return PathSegmentNameResource; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _rest_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rest-api.service */ "iCaw");



let PathSegmentNameResource = class PathSegmentNameResource {
    constructor(restApi) {
        this.restApi = restApi;
        this.ENDPOINT_ENDPOINT = 'endpoints';
        this.ENDPOINT = 'path_segment_names';
    }
    index(endpointId, queryParams) {
        return this.restApi.index([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT], queryParams);
    }
    show(endpointId, id, queryParams) {
        return this.restApi.show([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT], queryParams);
    }
    create(endpointId, body) {
        return this.restApi.create([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT], body);
    }
    update(endpointId, id, body) {
        return this.restApi.update([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT], body);
    }
    destroy(endpointId, id) {
        return this.restApi.destroy([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT]);
    }
};
PathSegmentNameResource.ctorParameters = () => [
    { type: _rest_api_service__WEBPACK_IMPORTED_MODULE_2__["RestApiService"] }
];
PathSegmentNameResource = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], PathSegmentNameResource);



/***/ }),

/***/ "iB7b":
/*!********************************!*\
  !*** ./src/@vex/vex.module.ts ***!
  \********************************/
/*! exports provided: VexModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VexModule", function() { return VexModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/material/form-field */ "Q2Ze");
/* harmony import */ var _layout_layout_module__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./layout/layout.module */ "cwwZ");





let VexModule = class VexModule {
};
VexModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _layout_layout_module__WEBPACK_IMPORTED_MODULE_4__["LayoutModule"]
        ],
        exports: [
            _layout_layout_module__WEBPACK_IMPORTED_MODULE_4__["LayoutModule"]
        ],
        providers: [
            {
                provide: _angular_material_form_field__WEBPACK_IMPORTED_MODULE_3__["MAT_FORM_FIELD_DEFAULT_OPTIONS"],
                useValue: {
                    appearance: 'fill'
                }
            }
        ]
    })
], VexModule);



/***/ }),

/***/ "iCaw":
/*!***********************************************!*\
  !*** ./src/app/core/http/rest-api.service.ts ***!
  \***********************************************/
/*! exports provided: RestApiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RestApiService", function() { return RestApiService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _http_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./http.service */ "gHic");



let RestApiService = class RestApiService {
    constructor(httpService) {
        this.httpService = httpService;
    }
    index(pathComponents, queryParams) {
        const url = this.httpService.buildUrl(pathComponents, queryParams);
        return this.httpService.get(url);
    }
    show(pathComponents, queryParams) {
        const url = this.httpService.buildUrl(pathComponents, queryParams);
        return this.httpService.get(url);
    }
    create(pathComponents, body) {
        const url = this.httpService.buildUrl(pathComponents);
        return this.httpService.post(url, body);
    }
    update(pathComponents, body) {
        const url = this.httpService.buildUrl(pathComponents);
        return this.httpService.put(url, body);
    }
    destroy(pathComponents, queryParams) {
        const url = this.httpService.buildUrl(pathComponents, queryParams);
        return this.httpService.delete(url);
    }
    path(pathComponents, queryParams) {
        return this.httpService.buildUrl(pathComponents, queryParams);
    }
};
RestApiService.ctorParameters = () => [
    { type: _http_service__WEBPACK_IMPORTED_MODULE_2__["HttpService"] }
];
RestApiService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], RestApiService);



/***/ }),

/***/ "j+4c":
/*!************************************************!*\
  !*** ./src/app/data/schema/response-header.ts ***!
  \************************************************/
/*! exports provided: ResponseHeader */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ResponseHeader", function() { return ResponseHeader; });
/* harmony import */ var _request_component__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./request-component */ "2bXN");

class ResponseHeader extends _request_component__WEBPACK_IMPORTED_MODULE_0__["RequestComponent"] {
    constructor(header) {
        super(6, header.id);
        this.name = header.name;
        this.value = header.value;
    }
}


/***/ }),

/***/ "jBLc":
/*!*****************************************!*\
  !*** ./src/app/data/schema/endpoint.ts ***!
  \*****************************************/
/*! exports provided: Endpoint, EndpointCategories */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Endpoint", function() { return Endpoint; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "EndpointCategories", function() { return EndpointCategories; });
class Endpoint {
    constructor(endpoint) {
        this.id = endpoint.id;
        this.method = endpoint.method;
        this.path = endpoint.path;
        this.components = endpoint.components;
        this.category = endpoint.category;
    }
}
var EndpointCategories;
(function (EndpointCategories) {
    EndpointCategories[EndpointCategories["Fixed"] = 1] = "Fixed";
    EndpointCategories[EndpointCategories["Alias"] = 2] = "Alias";
    EndpointCategories[EndpointCategories["Unknown"] = 3] = "Unknown";
})(EndpointCategories || (EndpointCategories = {}));


/***/ }),

/***/ "jXNf":
/*!************************************************************************!*\
  !*** ./src/@vex/components/toolbar-search/toolbar-search.component.ts ***!
  \************************************************************************/
/*! exports provided: ToolbarSearchComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ToolbarSearchComponent", function() { return ToolbarSearchComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_toolbar_search_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./toolbar-search.component.html */ "D1/4");
/* harmony import */ var _toolbar_search_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./toolbar-search.component.scss */ "DdkG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @iconify/icons-ic/twotone-search */ "sF+I");
/* harmony import */ var _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_4__);





let ToolbarSearchComponent = class ToolbarSearchComponent {
    constructor(cd) {
        this.cd = cd;
        this.icSearch = _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_4___default.a;
    }
    ngOnInit() {
    }
    open() {
        this.isOpen = true;
        this.cd.markForCheck();
        setTimeout(() => {
            this.input.nativeElement.focus();
        }, 100);
    }
    close() {
        this.isOpen = false;
        this.cd.markForCheck();
    }
};
ToolbarSearchComponent.ctorParameters = () => [
    { type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ChangeDetectorRef"] }
];
ToolbarSearchComponent.propDecorators = {
    input: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ViewChild"], args: ['input', { read: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ElementRef"], static: true },] }]
};
ToolbarSearchComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'vex-toolbar-search',
        template: _raw_loader_toolbar_search_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ChangeDetectionStrategy"].OnPush,
        styles: [_toolbar_search_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], ToolbarSearchComponent);



/***/ }),

/***/ "kYjG":
/*!********************************************************!*\
  !*** ./src/@vex/components/popover/popover.service.ts ***!
  \********************************************************/
/*! exports provided: PopoverService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PopoverService", function() { return PopoverService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_cdk_overlay__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/cdk/overlay */ "1O3W");
/* harmony import */ var _angular_cdk_portal__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/cdk/portal */ "1z/I");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _popover_ref__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./popover-ref */ "QaI9");
/* harmony import */ var _popover_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./popover.component */ "NEAy");






let PopoverService = class PopoverService {
    constructor(overlay, injector) {
        this.overlay = overlay;
        this.injector = injector;
    }
    open({ origin, content, data, width, height, position, offsetX, offsetY }) {
        const overlayRef = this.overlay.create(this.getOverlayConfig({ origin, width, height, position, offsetX, offsetY }));
        const popoverRef = new _popover_ref__WEBPACK_IMPORTED_MODULE_4__["PopoverRef"](overlayRef, content, data);
        const injector = this.createInjector(popoverRef, this.injector);
        overlayRef.attach(new _angular_cdk_portal__WEBPACK_IMPORTED_MODULE_2__["ComponentPortal"](_popover_component__WEBPACK_IMPORTED_MODULE_5__["PopoverComponent"], null, injector));
        return popoverRef;
    }
    createInjector(popoverRef, injector) {
        const tokens = new WeakMap([[_popover_ref__WEBPACK_IMPORTED_MODULE_4__["PopoverRef"], popoverRef]]);
        return new _angular_cdk_portal__WEBPACK_IMPORTED_MODULE_2__["PortalInjector"](injector, tokens);
    }
    getOverlayConfig({ origin, width, height, position, offsetX, offsetY }) {
        return new _angular_cdk_overlay__WEBPACK_IMPORTED_MODULE_1__["OverlayConfig"]({
            hasBackdrop: true,
            width,
            height,
            backdropClass: 'popover-backdrop',
            positionStrategy: this.getOverlayPosition({ origin, position, offsetX, offsetY }),
            scrollStrategy: this.overlay.scrollStrategies.reposition()
        });
    }
    getOverlayPosition({ origin, position, offsetX, offsetY }) {
        const positionStrategy = this.overlay.position()
            .flexibleConnectedTo(origin)
            .withPositions(position || this.getPositions())
            .withFlexibleDimensions(true)
            .withDefaultOffsetY(offsetY || 0)
            .withDefaultOffsetX(offsetX || 0)
            .withTransformOriginOn('.popover')
            .withPush(true);
        return positionStrategy;
    }
    getPositions() {
        return [
            {
                originX: 'center',
                originY: 'top',
                overlayX: 'center',
                overlayY: 'bottom'
            },
            {
                originX: 'center',
                originY: 'bottom',
                overlayX: 'center',
                overlayY: 'top'
            }
        ];
    }
};
PopoverService.ctorParameters = () => [
    { type: _angular_cdk_overlay__WEBPACK_IMPORTED_MODULE_1__["Overlay"] },
    { type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Injector"] }
];
PopoverService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Injectable"])({
        providedIn: 'root'
    })
], PopoverService);



/***/ }),

/***/ "kqhm":
/*!***********************************************************!*\
  !*** ./src/app/core/http/query-param-resource.service.ts ***!
  \***********************************************************/
/*! exports provided: QueryParamResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "QueryParamResource", function() { return QueryParamResource; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _rest_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rest-api.service */ "iCaw");



let QueryParamResource = class QueryParamResource {
    constructor(restApi) {
        this.restApi = restApi;
        this.REQUEST_ENDPOINT = 'requests';
        this.ENDPOINT = 'query_params';
    }
    index(requestId, queryParams) {
        if (typeof requestId === 'object') {
            queryParams = requestId;
            return this.restApi.index([this.ENDPOINT], queryParams);
        }
        else {
            return this.restApi.index([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT], queryParams);
        }
    }
    show(requestId, id, queryParams) {
        return this.restApi.show([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT, id], queryParams);
    }
    create(requestId, body) {
        return this.restApi.create([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT], body);
    }
    update(requestId, id, body) {
        return this.restApi.update([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT, id], body);
    }
    destroy(requestId, id, queryParams) {
        return this.restApi.destroy([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT, id], queryParams);
    }
};
QueryParamResource.ctorParameters = () => [
    { type: _rest_api_service__WEBPACK_IMPORTED_MODULE_2__["RestApiService"] }
];
QueryParamResource = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], QueryParamResource);



/***/ }),

/***/ "lC2v":
/*!*********************************************!*\
  !*** ./src/@vex/services/config.service.ts ***!
  \*********************************************/
/*! exports provided: ConfigService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ConfigService", function() { return ConfigService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs */ "qCKp");
/* harmony import */ var _interfaces_config_name_model__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../interfaces/config-name.model */ "EuI8");
/* harmony import */ var _utils_merge_deep__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../utils/merge-deep */ "Sl3+");
/* harmony import */ var _configs__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./configs */ "3oZ8");
/* harmony import */ var _layout_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./layout.service */ "CtTw");








let ConfigService = class ConfigService {
    constructor(document, layoutService) {
        this.document = document;
        this.layoutService = layoutService;
        this.defaultConfig = _interfaces_config_name_model__WEBPACK_IMPORTED_MODULE_4__["ConfigName"].apollo;
        this.configs = _configs__WEBPACK_IMPORTED_MODULE_6__["configs"];
        this._configSubject = new rxjs__WEBPACK_IMPORTED_MODULE_3__["BehaviorSubject"](this.configs.find(c => c.id === this.defaultConfig));
        this.config$ = this._configSubject.asObservable();
        this.config$.subscribe(config => this._updateConfig(config));
    }
    setConfig(config) {
        const settings = this.configs.find(c => c.id === config);
        if (settings) {
            this._configSubject.next(settings);
        }
    }
    updateConfig(config) {
        this._configSubject.next(Object(_utils_merge_deep__WEBPACK_IMPORTED_MODULE_5__["mergeDeep"])(Object.assign({}, this._configSubject.getValue()), config));
    }
    _updateConfig(config) {
        const body = this.document.body;
        this.configs.forEach(c => {
            if (body.classList.contains(c.id)) {
                body.classList.remove(c.id);
            }
        });
        body.classList.add(config.id);
        //config.sidenav.state === 'expanded' ? this.layoutService.expandSidenav() : this.layoutService.collapseSidenav();
        // Workaround so charts and other externals know they have to resize on Layout switch
        if (window) {
            window.dispatchEvent(new Event('resize'));
            setTimeout(() => {
                window.dispatchEvent(new Event('resize'));
            }, 200);
        }
    }
};
ConfigService.ctorParameters = () => [
    { type: Document, decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Inject"], args: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["DOCUMENT"],] }] },
    { type: _layout_service__WEBPACK_IMPORTED_MODULE_7__["LayoutService"] }
];
ConfigService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["Injectable"])({
        providedIn: 'root'
    })
], ConfigService);



/***/ }),

/***/ "mQ6f":
/*!*************************************************************!*\
  !*** ./src/@vex/components/quickpanel/quickpanel.module.ts ***!
  \*************************************************************/
/*! exports provided: QuickpanelModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "QuickpanelModule", function() { return QuickpanelModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_material_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/material/core */ "UhP/");
/* harmony import */ var _angular_material_list__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/list */ "SqCe");
/* harmony import */ var _angular_material_progress_bar__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/progress-bar */ "BTe0");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _quickpanel_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./quickpanel.component */ "pBFY");








let QuickpanelModule = class QuickpanelModule {
};
QuickpanelModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_quickpanel_component__WEBPACK_IMPORTED_MODULE_7__["QuickpanelComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_material_list__WEBPACK_IMPORTED_MODULE_4__["MatListModule"],
            _angular_material_progress_bar__WEBPACK_IMPORTED_MODULE_5__["MatProgressBarModule"],
            _angular_router__WEBPACK_IMPORTED_MODULE_6__["RouterModule"],
            _angular_material_core__WEBPACK_IMPORTED_MODULE_3__["MatRippleModule"]
        ],
        exports: [_quickpanel_component__WEBPACK_IMPORTED_MODULE_7__["QuickpanelComponent"]]
    })
], QuickpanelModule);



/***/ }),

/***/ "mbJQ":
/*!*****************************************************************!*\
  !*** ./src/@vex/components/config-panel/config-panel.module.ts ***!
  \*****************************************************************/
/*! exports provided: ConfigPanelModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ConfigPanelModule", function() { return ConfigPanelModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_material_core__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/core */ "UhP/");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _angular_material_radio__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/radio */ "zQhy");
/* harmony import */ var _angular_material_slide_toggle__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/material/slide-toggle */ "jMqV");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _config_panel_toggle_config_panel_toggle_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./config-panel-toggle/config-panel-toggle.component */ "H5iI");
/* harmony import */ var _config_panel_component__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./config-panel.component */ "1vXY");












let ConfigPanelModule = class ConfigPanelModule {
};
ConfigPanelModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_4__["MatButtonModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_6__["MatIconModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_9__["IconModule"],
            _angular_material_radio__WEBPACK_IMPORTED_MODULE_7__["MatRadioModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _angular_material_slide_toggle__WEBPACK_IMPORTED_MODULE_8__["MatSlideToggleModule"],
            _angular_material_core__WEBPACK_IMPORTED_MODULE_5__["MatRippleModule"]
        ],
        declarations: [_config_panel_component__WEBPACK_IMPORTED_MODULE_11__["ConfigPanelComponent"], _config_panel_toggle_config_panel_toggle_component__WEBPACK_IMPORTED_MODULE_10__["ConfigPanelToggleComponent"]],
        exports: [_config_panel_component__WEBPACK_IMPORTED_MODULE_11__["ConfigPanelComponent"], _config_panel_toggle_config_panel_toggle_component__WEBPACK_IMPORTED_MODULE_10__["ConfigPanelToggleComponent"]]
    })
], ConfigPanelModule);



/***/ }),

/***/ "mbNh":
/*!********************************************************************!*\
  !*** ./src/app/modules/projects/services/projects-data.service.ts ***!
  \********************************************************************/
/*! exports provided: ProjectsDataService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectsDataService", function() { return ProjectsDataService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "qCKp");
/* harmony import */ var _core_http_project_resource_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @core/http/project-resource.service */ "4UAC");
/* harmony import */ var _data_schema__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @data/schema */ "V99k");





let ProjectsDataService = class ProjectsDataService {
    constructor(projectResource) {
        this.projectResource = projectResource;
        this.subject = new rxjs__WEBPACK_IMPORTED_MODULE_2__["BehaviorSubject"]([]);
        this.projects$ = this.subject.asObservable();
    }
    fetch(organizationId) {
        const queryParams = {
            organization_id: organizationId,
        };
        this.projectResource.index(queryParams).subscribe((projects) => {
            this.set(projects.map(p => {
                return new _data_schema__WEBPACK_IMPORTED_MODULE_4__["Project"](p);
            }));
        });
    }
    get() {
        if (this.projects) {
            return this.projects$;
        }
        return this.projects$;
    }
    set(projects) {
        this.projects = projects;
        this.subject.next(projects);
    }
};
ProjectsDataService.ctorParameters = () => [
    { type: _core_http_project_resource_service__WEBPACK_IMPORTED_MODULE_3__["ProjectResource"] }
];
ProjectsDataService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], ProjectsDataService);



/***/ }),

/***/ "n/pC":
/*!***************************************************************!*\
  !*** ./src/app/core/http/response-header-resource.service.ts ***!
  \***************************************************************/
/*! exports provided: ResponseHeaderResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ResponseHeaderResource", function() { return ResponseHeaderResource; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _rest_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rest-api.service */ "iCaw");



let ResponseHeaderResource = class ResponseHeaderResource {
    constructor(restApi) {
        this.restApi = restApi;
        this.REQUEST_ENDPOINT = 'requests';
        this.ENDPOINT = 'response_headers';
    }
    index(requestId, queryParams) {
        return this.restApi.index([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT], queryParams);
    }
    show(requestId, id, queryParams) {
        return this.restApi.show([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT, id], queryParams);
    }
    create(requestId, body) {
        return this.restApi.create([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT], body);
    }
    update(requestId, id, body) {
        return this.restApi.update([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT, id], body);
    }
    destroy(requestId, id) {
        return this.restApi.destroy([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT, id]);
    }
};
ResponseHeaderResource.ctorParameters = () => [
    { type: _rest_api_service__WEBPACK_IMPORTED_MODULE_2__["RestApiService"] }
];
ResponseHeaderResource = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], ResponseHeaderResource);



/***/ }),

/***/ "nW1T":
/*!************************************************************!*\
  !*** ./src/@vex/components/popover/popover.component.scss ***!
  \************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJwb3BvdmVyLmNvbXBvbmVudC5zY3NzIn0= */");

/***/ }),

/***/ "nmZq":
/*!****************************************************************************************************!*\
  !*** ./src/app/layout/components/toolbar/components/toolbar-proxy-settings/schema/agent-config.ts ***!
  \****************************************************************************************************/
/*! exports provided: AgentConfig */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AgentConfig", function() { return AgentConfig; });
class AgentConfig {
    constructor(config) {
        this.apiUrl = config.api_url;
        this.apiKey = config.api_key;
        const recordConfig = config.mode.record;
        const mockConfig = config.mode.mock;
        this.mode = {
            active: config.mode.active,
            record: {
                active: recordConfig.enabled,
                includePatterns: recordConfig.include_patterns || [],
                excludePatterns: recordConfig.exclude_patterns || [],
                policy: recordConfig.policy,
                projectKey: recordConfig.project_key,
                serviceUrl: recordConfig.service_url,
                scenarioKey: recordConfig.scenario_key,
            },
            mock: {
                active: mockConfig.enabled,
                includePatterns: recordConfig.include_patterns || [],
                excludePatterns: recordConfig.exclude_patterns || [],
                policy: mockConfig.policy,
                projectKey: mockConfig.project_key,
                serviceUrl: mockConfig.service_url,
                scenarioKey: mockConfig.scenario_key,
            },
        };
    }
}


/***/ }),

/***/ "npeK":
/*!**********************************************************!*\
  !*** ./src/app/core/http/body-param-resource.service.ts ***!
  \**********************************************************/
/*! exports provided: BodyParamResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "BodyParamResource", function() { return BodyParamResource; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _rest_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rest-api.service */ "iCaw");



let BodyParamResource = class BodyParamResource {
    constructor(restApi) {
        this.restApi = restApi;
        this.REQUEST_ENDPOINT = 'requests';
        this.ENDPOINT = 'body_params';
    }
    index(requestId, queryParams) {
        if (typeof requestId === 'object') {
            queryParams = requestId;
            return this.restApi.index([this.ENDPOINT], queryParams);
        }
        else {
            return this.restApi.index([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT], queryParams);
        }
    }
    show(requestId, id, queryParams) {
        return this.restApi.show([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT, id], queryParams);
    }
    create(requestId, body) {
        return this.restApi.create([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT], body);
    }
    update(requestId, id, body) {
        return this.restApi.update([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT, id], body);
    }
    destroy(requestId, id, queryParams) {
        return this.restApi.destroy([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT, id], queryParams);
    }
};
BodyParamResource.ctorParameters = () => [
    { type: _rest_api_service__WEBPACK_IMPORTED_MODULE_2__["RestApiService"] }
];
BodyParamResource = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], BodyParamResource);



/***/ }),

/***/ "nvf/":
/*!*********************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/layout/components/toolbar/components/toolbar-mock-url/toolbar-mock-url.component.html ***!
  \*********************************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<form [formGroup]=\"form\">\n  <div fxLayout=\"row\" fxLayoutAlign=\"start center\" mat-dialog-title>\n    <h2 class=\"headline m-0\" fxFlex=\"auto\">View Mock URL</h2>\n\n    <button class=\"subheading\" mat-dialog-close mat-icon-button type=\"button\">\n      <mat-icon [icIcon]=\"icClose\"></mat-icon>\n    </button>\n  </div>\n\n  <mat-divider class=\"-mx-6 text-border\"></mat-divider>\n\n  <div class=\"mt-4\" fxLayout=\"column\" fxLayoutAlign=\"start start\">\n    <h4 class=\"mb-2 subheading\" fxFlex=\"100\">\n      Mock Requests From\n    </h4>\n\n    <mat-form-field fxFlex=\"fill\" class=\"w-full\">\n      <mat-label>Project</mat-label>\n      <mat-select\n        [compareWith]=\"compareProjects\"\n        (selectionChange)=\"selectProject($event)\"\n        formControlName=\"project\"\n      >\n        <mat-option \n          *ngFor=\"let project of (projects$ | async)\"\n          [value]=\"project\"\n        >\n          {{ project.name }}\n        </mat-option>\n      </mat-select>\n    </mat-form-field>\n\n    <div \n      *ngIf=\"scenarios.length\"\n      class=\"w-full\" fxLayout=\"row\" fxLayoutGap=\"10px\"\n    >\n      <mat-form-field fxFlex=\"fill\" class=\"w-full\">\n        <mat-label>Scenario</mat-label>\n        <mat-select \n          (selectionChange)=\"selectScenario($event)\"\n          formControlName=\"scenario\"\n        >\n          <mat-option \n            *ngFor=\"let scenario of scenarios\"\n            [value]=\"scenario\"\n          >\n            {{ scenario.name }}\n          </mat-option>\n        </mat-select>\n\n        <mat-hint>If left blank, defaults to project</mat-hint>\n      </mat-form-field>\n\n      <button \n        *ngIf=\"form.value.scenario\" \n        (click)=\"clearScenario()\"\n        fxFlex=\"40px\" class=\"input-button\" mat-icon-button matSuffix type=\"button\">\n        <div fxLayout=\"row\" fxLayoutAlign=\"center center\">\n          <mat-icon [icIcon]=\"icClose\"></mat-icon>\n        </div>\n      </button>\n    </div>\n  </div>\n\n  <div class=\"mt-4\" fxLayout=\"column\" fxLayoutAlign=\"start start\" *ngIf=\"!form.invalid\">\n    <h4 class=\"mb-2 subheading\" fxFlex=\"100\">\n      Mock URL\n    </h4>\n\n    <div \n      class=\"w-full\" fxLayout=\"row\" fxLayoutGap=\"10px\"\n    >\n      <mat-form-field class=\"w-full\">\n        <mat-label>Mock URL</mat-label>\n        <input [readonly]=\"true\" matInput formControlName=\"mockUrl\" type=\"text\">\n      </mat-form-field>\n\n      <button \n        [disabled]=\"form.invalid\"\n        (click)=\"copyUrl($event)\"\n        fxFlex=\"40px\" class=\"input-button\" mat-icon-button matSuffix type=\"button\">\n        <div fxLayout=\"row\" fxLayoutAlign=\"center center\">\n          <mat-icon [icIcon]=\"icFileCopy\"></mat-icon>\n        </div>\n      </button>\n    </div>\n  </div>\n</form>\n");

/***/ }),

/***/ "oFyy":
/*!***********************************************************!*\
  !*** ./src/app/core/http/alias-value-resource.service.ts ***!
  \***********************************************************/
/*! exports provided: AliasValueResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AliasValueResource", function() { return AliasValueResource; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _rest_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rest-api.service */ "iCaw");



let AliasValueResource = class AliasValueResource {
    constructor(restApi) {
        this.restApi = restApi;
        this.ENDPOINT = 'alias_values';
    }
    index(queryParams) {
        return this.restApi.index([this.ENDPOINT], queryParams);
    }
    show(id, queryParams) {
        return this.restApi.show([this.ENDPOINT, id], queryParams);
    }
    create(body) {
        return this.restApi.create([this.ENDPOINT], body);
    }
    update(id, body) {
        return this.restApi.update([this.ENDPOINT, id], body);
    }
    destroy(id) {
        return this.restApi.destroy([this.ENDPOINT, id]);
    }
};
AliasValueResource.ctorParameters = () => [
    { type: _rest_api_service__WEBPACK_IMPORTED_MODULE_2__["RestApiService"] }
];
AliasValueResource = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], AliasValueResource);



/***/ }),

/***/ "oKEX":
/*!*************************************************************************************************!*\
  !*** ./src/@vex/components/config-panel/config-panel-toggle/config-panel-toggle.component.scss ***!
  \*************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (".config-panel-toggle {\n  bottom: var(--padding);\n  position: fixed;\n  right: var(--padding);\n  z-index: 100;\n}\n\n::ng-deep [dir=rtl] .config-panel-toggle {\n  left: var(--padding);\n  right: unset;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uL2NvbmZpZy1wYW5lbC10b2dnbGUuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSxzQkFBQTtFQUNBLGVBQUE7RUFDQSxxQkFBQTtFQUNBLFlBQUE7QUFDRjs7QUFFQTtFQUNFLG9CQUFBO0VBQ0EsWUFBQTtBQUNGIiwiZmlsZSI6ImNvbmZpZy1wYW5lbC10b2dnbGUuY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyIuY29uZmlnLXBhbmVsLXRvZ2dsZSB7XG4gIGJvdHRvbTogdmFyKC0tcGFkZGluZyk7XG4gIHBvc2l0aW9uOiBmaXhlZDtcbiAgcmlnaHQ6IHZhcigtLXBhZGRpbmcpO1xuICB6LWluZGV4OiAxMDA7XG59XG5cbjo6bmctZGVlcCBbZGlyPXJ0bF0gLmNvbmZpZy1wYW5lbC10b2dnbGUge1xuICBsZWZ0OiB2YXIoLS1wYWRkaW5nKTtcbiAgcmlnaHQ6IHVuc2V0O1xufSJdfQ== */");

/***/ }),

/***/ "og7a":
/*!**********************************************************!*\
  !*** ./src/@vex/components/sidebar/sidebar.component.ts ***!
  \**********************************************************/
/*! exports provided: SidebarComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SidebarComponent", function() { return SidebarComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_sidebar_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./sidebar.component.html */ "c7Bs");
/* harmony import */ var _sidebar_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./sidebar.component.scss */ "cFcm");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/core */ "8Y7J");





let SidebarComponent = class SidebarComponent {
    constructor(document) {
        this.document = document;
        this.position = 'left';
    }
    get opened() {
        return this._opened;
    }
    set opened(opened) {
        this._opened = opened;
        opened ? this.enableScrollblock() : this.disableScrollblock();
    }
    get positionLeft() {
        return this.position === 'left';
    }
    get positionRight() {
        return this.position === 'right';
    }
    enableScrollblock() {
        if (!this.document.body.classList.contains('vex-scrollblock')) {
            this.document.body.classList.add('vex-scrollblock');
        }
    }
    disableScrollblock() {
        if (this.document.body.classList.contains('vex-scrollblock')) {
            this.document.body.classList.remove('vex-scrollblock');
        }
    }
    open() {
        this.opened = true;
    }
    close() {
        this.opened = false;
    }
    ngOnDestroy() { }
};
SidebarComponent.ctorParameters = () => [
    { type: Document, decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Inject"], args: [_angular_common__WEBPACK_IMPORTED_MODULE_3__["DOCUMENT"],] }] }
];
SidebarComponent.propDecorators = {
    position: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Input"] }],
    invisibleBackdrop: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Input"] }],
    opened: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Input"] }]
};
SidebarComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_4__["Component"])({
        selector: 'vex-sidebar',
        template: _raw_loader_sidebar_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        host: {
            class: 'vex-sidebar'
        },
        styles: [_sidebar_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], SidebarComponent);



/***/ }),

/***/ "oyjd":
/*!*******************************************************************!*\
  !*** ./src/app/modules/projects/services/project-data.service.ts ***!
  \*******************************************************************/
/*! exports provided: ProjectDataService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectDataService", function() { return ProjectDataService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "qCKp");
/* harmony import */ var _core_http_project_resource_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @core/http/project-resource.service */ "4UAC");
/* harmony import */ var _data_schema_project__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @data/schema/project */ "2RYP");





let ProjectDataService = class ProjectDataService {
    constructor(projectResource) {
        this.projectResource = projectResource;
        this.subject = new rxjs__WEBPACK_IMPORTED_MODULE_2__["BehaviorSubject"](null);
        this.project$ = this.subject.asObservable();
    }
    fetch(id) {
        this.projectResource.show(id).subscribe((res) => {
            this.set(new _data_schema_project__WEBPACK_IMPORTED_MODULE_4__["Project"](res));
        });
    }
    get() {
        if (this.project) {
            return this.project$;
        }
        return this.project$;
    }
    set(project) {
        this.project = project;
        this.subject.next(project);
    }
};
ProjectDataService.ctorParameters = () => [
    { type: _core_http_project_resource_service__WEBPACK_IMPORTED_MODULE_3__["ProjectResource"] }
];
ProjectDataService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])()
], ProjectDataService);



/***/ }),

/***/ "pBFY":
/*!****************************************************************!*\
  !*** ./src/@vex/components/quickpanel/quickpanel.component.ts ***!
  \****************************************************************/
/*! exports provided: QuickpanelComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "QuickpanelComponent", function() { return QuickpanelComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_quickpanel_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./quickpanel.component.html */ "rTLG");
/* harmony import */ var _quickpanel_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./quickpanel.component.scss */ "A8r0");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var luxon__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! luxon */ "ExVU");
/* harmony import */ var luxon__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(luxon__WEBPACK_IMPORTED_MODULE_4__);





let QuickpanelComponent = class QuickpanelComponent {
    constructor() {
        this.date = luxon__WEBPACK_IMPORTED_MODULE_4__["DateTime"].local().toFormat('DD');
        this.dayName = luxon__WEBPACK_IMPORTED_MODULE_4__["DateTime"].local().toFormat('EEEE');
    }
    ngOnInit() {
    }
};
QuickpanelComponent.ctorParameters = () => [];
QuickpanelComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'vex-quickpanel',
        template: _raw_loader_quickpanel_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_quickpanel_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], QuickpanelComponent);



/***/ }),

/***/ "pKmL":
/*!*************************************!*\
  !*** ./src/app/core/core.module.ts ***!
  \*************************************/
/*! exports provided: CoreModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "CoreModule", function() { return CoreModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/material/snack-bar */ "zHaW");
/* harmony import */ var _core_utils_http_error_handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @core/utils/http-error-handler */ "87D3");





let CoreModule = class CoreModule {
};
CoreModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_3__["MatSnackBarModule"],
        ],
        providers: [
            _core_utils_http_error_handler__WEBPACK_IMPORTED_MODULE_4__["HttpErrorHandler"],
        ],
    })
], CoreModule);



/***/ }),

/***/ "pXZ5":
/*!**************************************************************!*\
  !*** ./src/@vex/components/mega-menu/mega-menu.component.ts ***!
  \**************************************************************/
/*! exports provided: MegaMenuComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MegaMenuComponent", function() { return MegaMenuComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_mega_menu_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./mega-menu.component.html */ "Xuwo");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _iconify_icons_ic_twotone_assessment__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @iconify/icons-ic/twotone-assessment */ "6X9H");
/* harmony import */ var _iconify_icons_ic_twotone_assessment__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_assessment__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _iconify_icons_ic_twotone_assignment__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @iconify/icons-ic/twotone-assignment */ "16CC");
/* harmony import */ var _iconify_icons_ic_twotone_assignment__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_assignment__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _iconify_icons_ic_twotone_book__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @iconify/icons-ic/twotone-book */ "s/ED");
/* harmony import */ var _iconify_icons_ic_twotone_book__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_book__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _iconify_icons_ic_twotone_contact_support__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @iconify/icons-ic/twotone-contact-support */ "rJEJ");
/* harmony import */ var _iconify_icons_ic_twotone_contact_support__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_contact_support__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _iconify_icons_ic_twotone_contacts__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @iconify/icons-ic/twotone-contacts */ "rbx1");
/* harmony import */ var _iconify_icons_ic_twotone_contacts__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_contacts__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _iconify_icons_ic_twotone_layers__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @iconify/icons-ic/twotone-layers */ "7nbV");
/* harmony import */ var _iconify_icons_ic_twotone_layers__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_layers__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _popover_popover_ref__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../popover/popover-ref */ "QaI9");










let MegaMenuComponent = class MegaMenuComponent {
    constructor(popoverRef) {
        this.popoverRef = popoverRef;
        this.features = [
            {
                icon: _iconify_icons_ic_twotone_layers__WEBPACK_IMPORTED_MODULE_8___default.a,
                label: 'Dashboard',
                route: '/'
            },
            {
                icon: _iconify_icons_ic_twotone_assignment__WEBPACK_IMPORTED_MODULE_4___default.a,
                label: 'AIO-Table',
                route: '/apps/aio-table'
            },
            {
                icon: _iconify_icons_ic_twotone_contact_support__WEBPACK_IMPORTED_MODULE_6___default.a,
                label: 'Help Center',
                route: '/apps/help-center'
            },
            {
                icon: _iconify_icons_ic_twotone_contacts__WEBPACK_IMPORTED_MODULE_7___default.a,
                label: 'Contacts',
                route: '/apps/contacts/grid'
            },
            {
                icon: _iconify_icons_ic_twotone_assessment__WEBPACK_IMPORTED_MODULE_3___default.a,
                label: 'Scrumboard',
                route: '/apps/scrumboard/1'
            },
            {
                icon: _iconify_icons_ic_twotone_book__WEBPACK_IMPORTED_MODULE_5___default.a,
                label: 'Documentation',
                route: '/documentation'
            }
        ];
        this.pages = [
            {
                label: 'All-In-One Table',
                route: '/apps/aio-table'
            },
            {
                label: 'Authentication',
                route: '/login'
            },
            {
                label: 'Components',
                route: '/ui/components/overview'
            },
            {
                label: 'Documentation',
                route: '/documentation'
            },
            {
                label: 'FAQ',
                route: '/pages/faq'
            },
            {
                label: 'Form Elements',
                route: '/ui/forms/form-elements'
            },
            {
                label: 'Form Wizard',
                route: '/ui/forms/form-wizard'
            },
            {
                label: 'Guides',
                route: '/pages/guides'
            },
            {
                label: 'Help Center',
                route: '/apps/help-center'
            },
            {
                label: 'Scrumboard',
                route: '/apps/scrumboard'
            }
        ];
    }
    ngOnInit() {
    }
    close() {
        this.popoverRef.close();
    }
};
MegaMenuComponent.ctorParameters = () => [
    { type: _popover_popover_ref__WEBPACK_IMPORTED_MODULE_9__["PopoverRef"] }
];
MegaMenuComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["Component"])({
        selector: 'vex-mega-menu',
        template: _raw_loader_mega_menu_component_html__WEBPACK_IMPORTED_MODULE_1__["default"]
    })
], MegaMenuComponent);



/***/ }),

/***/ "pfe1":
/*!**********************************************!*\
  !*** ./src/app/core/guards/no-auth.guard.ts ***!
  \**********************************************/
/*! exports provided: NoAuthGuard */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "NoAuthGuard", function() { return NoAuthGuard; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var angular_token__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! angular-token */ "hU4o");




let NoAuthGuard = class NoAuthGuard {
    constructor(router, tokenService) {
        this.router = router;
        this.tokenService = tokenService;
    }
    canActivate(next, state) {
        if (!this.tokenService.canActivate(next, state)) {
            return true;
        }
        // Navigate to login page
        this.router.navigate(['/projects']);
        return false;
    }
};
NoAuthGuard.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
    { type: angular_token__WEBPACK_IMPORTED_MODULE_3__["AngularTokenService"] }
];
NoAuthGuard = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], NoAuthGuard);



/***/ }),

/***/ "rTLG":
/*!********************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/@vex/components/quickpanel/quickpanel.component.html ***!
  \********************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div class=\"body-2 p-6 bg-primary-500 text-primary-contrast-500\">\n  <p>TODAY</p>\n  <div class=\"display-1\">{{ dayName }}</div>\n  <div class=\"display-1\">{{ date }}</div>\n</div>\n\n<mat-divider></mat-divider>\n\n<mat-nav-list>\n  <h3 matSubheader>UPCOMING EVENTS</h3>\n  <a [routerLink]=\"[]\" mat-list-item>\n    <h4 matLine>Business Meeting</h4>\n    <p matLine>In 16 Minutes, Meeting Room</p>\n  </a>\n  <a [routerLink]=\"[]\" mat-list-item>\n    <h4 matLine>Ask for Vacation</h4>\n    <p matLine>12:00 PM</p>\n  </a>\n  <a [routerLink]=\"[]\" mat-list-item>\n    <h4 matLine>Dinner with Sophie</h4>\n    <p matLine>18:30 PM</p>\n  </a>\n  <a [routerLink]=\"[]\" mat-list-item>\n    <h4 matLine>Deadline for Project X</h4>\n    <p matLine>21:00 PM</p>\n  </a>\n  <mat-divider></mat-divider>\n  <h3 matSubheader>TODO-LIST</h3>\n  <a [routerLink]=\"[]\" mat-list-item>\n    <h4 matLine>Invite Jack to play golf</h4>\n    <p matLine>Added: 6 hours ago</p>\n  </a>\n  <a [routerLink]=\"[]\" mat-list-item>\n    <h4 matLine>Get to know Angular more</h4>\n    <p matLine>Added: 2 days ago</p>\n  </a>\n  <a [routerLink]=\"[]\" mat-list-item>\n    <h4 matLine>Configure that new router</h4>\n    <p matLine>Added: 5 days ago</p>\n  </a>\n  <mat-divider></mat-divider>\n  <h3 matSubheader>SERVER STATISTICS</h3>\n</mat-nav-list>\n\n<div class=\"list-item\" matRipple>\n  <p>CPU Load (71% / 100%)</p>\n  <p class=\"progress-bar\">\n    <mat-progress-bar color=\"primary\" mode=\"determinate\" value=\"71\"></mat-progress-bar>\n  </p>\n</div>\n\n<div class=\"list-item\" matRipple>\n  <p>RAM Usage (6,175 MB / 16,384 MB)</p>\n  <p class=\"progress-bar\">\n    <mat-progress-bar color=\"accent\" mode=\"determinate\" value=\"34\"></mat-progress-bar>\n  </p>\n</div>\n\n<div class=\"list-item\" matRipple>\n  <p>CPU Temp (43° / 80°)</p>\n  <p class=\"progress-bar\">\n    <mat-progress-bar color=\"warn\" mode=\"determinate\" value=\"54\"></mat-progress-bar>\n  </p>\n</div>\n");

/***/ }),

/***/ "rpPS":
/*!***************************************!*\
  !*** ./src/app/data/schema/header.ts ***!
  \***************************************/
/*! exports provided: Header */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Header", function() { return Header; });
/* harmony import */ var _request_component__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./request-component */ "2bXN");

class Header extends _request_component__WEBPACK_IMPORTED_MODULE_0__["RequestComponent"] {
    constructor(header) {
        super(1, header.id);
        this.name = header.name;
        this.value = header.value;
        this.aliasName = header.alias_name;
        this.isRequired = header.is_required;
    }
}


/***/ }),

/***/ "sh9p":
/*!******************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/@vex/components/navigation-item/navigation-item.component.html ***!
  \******************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<a *ngIf=\"item.isVisible() && isLink(item) && !item.handleClick\"\n   [class.hover:bg-hover]=\"!(isActive$ | async)(item)\"\n   [ngClass]=\"{ 'vex-layout-theme': (isActive$ | async)(item), 'navigation-color': !(isActive$ | async)(item) }\"\n   [routerLink]=\"item.route\"\n   class=\"navigation-item\"\n   matRipple>\n  {{ item.label }}\n</a>\n\n<div *ngIf=\"item.isVisible() && isLink(item) && item.handleClick\"\n     (click)=\"item.handleClick()\"\n     [class.hover:bg-hover]=\"!(isActive$ | async)(item)\"\n     [ngClass]=\"{ 'vex-layout-theme': (isActive$ | async)(item), 'navigation-color': !(isActive$ | async)(item) }\"\n     class=\"navigation-item navigation-color\"\n     matRipple>\n  {{ item.label }}\n</div>\n\n<ng-container *ngIf=\"(isSubheading(item) && item.children?.length > 0) || isDropdown(item)\">\n  <div [class.hover:bg-hover]=\"!(isActive$ | async)(item)\"\n       [matMenuTriggerFor]=\"menu\"\n       [ngClass]=\"{ 'vex-layout-theme': (isActive$ | async)(item), 'navigation-color': !(isActive$ | async)(item) }\"\n       class=\"navigation-item\"\n       matRipple>\n    {{ item.label }}\n  </div>\n\n  <mat-menu #menu=\"matMenu\" yPosition=\"below\">\n    <ng-container *ngFor=\"let child of item.children\">\n      <a *ngIf=\"isLink(child) && !isFunction(child.route)\"\n         [routerLink]=\"child.route\"\n         class=\"navigation-menu-item\"\n         mat-menu-item>\n        <mat-icon [icIcon]=\"child.icon\"></mat-icon>\n        <span>{{ child.label }}</span>\n      </a>\n\n      <div (click)=\"child.route()\"\n           *ngIf=\"isLink(child) && isFunction(child.route)\"\n           class=\"navigation-menu-item\"\n           mat-menu-item>\n        <mat-icon [icIcon]=\"child.icon\"></mat-icon>\n        <span>{{ child.label }}</span>\n      </div>\n\n      <ng-container *ngIf=\"isDropdown(child)\">\n        <button [matMenuTriggerFor]=\"level1\" class=\"navigation-menu-item\" mat-menu-item>\n          <mat-icon [icIcon]=\"child.icon\"></mat-icon>\n          <span>{{ child.label }}</span>\n        </button>\n\n        <mat-menu #level1=\"matMenu\" yPosition=\"below\">\n          <ng-container *ngFor=\"let item of child.children\">\n            <ng-container [ngTemplateOutletContext]=\"{ item: item }\"\n                          [ngTemplateOutlet]=\"linkTemplate\"></ng-container>\n\n            <ng-container *ngIf=\"isDropdown(item)\">\n              <button [matMenuTriggerFor]=\"level2\"\n                      class=\"navigation-menu-item\"\n                      mat-menu-item>{{ item.label }}</button>\n\n              <mat-menu #level2=\"matMenu\" yPosition=\"below\">\n                <ng-container *ngFor=\"let child of item.children\">\n                  <ng-container [ngTemplateOutletContext]=\"{ item: child }\"\n                                [ngTemplateOutlet]=\"linkTemplate\"></ng-container>\n\n                  <ng-container *ngIf=\"isDropdown(child)\">\n                    <button [matMenuTriggerFor]=\"level3\"\n                            class=\"navigation-menu-item\"\n                            mat-menu-item>{{ child.label }}</button>\n\n                    <mat-menu #level3=\"matMenu\" yPosition=\"below\">\n                      <ng-container *ngFor=\"let item of child.children\">\n                        <ng-container [ngTemplateOutletContext]=\"{ item: item }\"\n                                      [ngTemplateOutlet]=\"linkTemplate\"></ng-container>\n\n                        <ng-container *ngIf=\"isDropdown(item)\">\n                          <button [matMenuTriggerFor]=\"level4\"\n                                  class=\"navigation-menu-item\"\n                                  mat-menu-item>{{ item.label }}</button>\n\n                          <mat-menu #level4=\"matMenu\" yPosition=\"below\">\n                            <ng-container *ngFor=\"let child of item.children\">\n                              <ng-container [ngTemplateOutletContext]=\"{ item: child }\"\n                                            [ngTemplateOutlet]=\"linkTemplate\"></ng-container>\n\n                              <ng-container *ngIf=\"isDropdown(child)\">\n                                <button [matMenuTriggerFor]=\"level5\"\n                                        class=\"navigation-menu-item\"\n                                        mat-menu-item>{{ child.label }}</button>\n\n                                <mat-menu #level5=\"matMenu\" yPosition=\"below\">\n                                  <ng-container *ngFor=\"let item of child.children\">\n                                    <ng-container [ngTemplateOutletContext]=\"{ item: item }\"\n                                                  [ngTemplateOutlet]=\"linkTemplate\"></ng-container>\n                                  </ng-container>\n                                </mat-menu>\n                              </ng-container>\n                            </ng-container>\n                          </mat-menu>\n                        </ng-container>\n                      </ng-container>\n                    </mat-menu>\n                  </ng-container>\n                </ng-container>\n              </mat-menu>\n            </ng-container>\n          </ng-container>\n        </mat-menu>\n      </ng-container>\n\n    </ng-container>\n  </mat-menu>\n\n  <ng-template #linkTemplate let-item=\"item\">\n    <a *ngIf=\"item.isVisible() && isLink(item) && !item.handleClick\"\n      [routerLink]=\"item.handleClick\"\n      class=\"navigation-menu-item\"\n      mat-menu-item>{{ item.label }}</a>\n\n    <div *ngIf=\"item.isVisible() && isLink(item) && item.handleClick\"\n        (click)=\"item.handleClick()\"\n        class=\"navigation-menu-item\"\n        mat-menu-item>{{ item.label }}</div>\n  </ng-template>\n</ng-container>\n");

/***/ }),

/***/ "ti5q":
/*!****************************************************************!*\
  !*** ./src/app/core/http/query-param-name-resource.service.ts ***!
  \****************************************************************/
/*! exports provided: QueryParamNameResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "QueryParamNameResource", function() { return QueryParamNameResource; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _rest_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rest-api.service */ "iCaw");



let QueryParamNameResource = class QueryParamNameResource {
    constructor(restApi) {
        this.restApi = restApi;
        this.ENDPOINT_ENDPOINT = 'endpoints';
        this.ENDPOINT = 'query_param_names';
    }
    index(endpointId, queryParams) {
        if (typeof endpointId === 'object') {
            queryParams = endpointId;
            return this.restApi.index([this.ENDPOINT], queryParams);
        }
        else {
            return this.restApi.index([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT], queryParams);
        }
    }
    show(endpointId, id, queryParams) {
        return this.restApi.show([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT, id], queryParams);
    }
    create(endpointId, body) {
        return this.restApi.create([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT], body);
    }
    update(endpointId, id, body) {
        return this.restApi.update([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT, id], body);
    }
    destroy(endpointId, id) {
        return this.restApi.destroy([this.ENDPOINT_ENDPOINT, endpointId, this.ENDPOINT, id]);
    }
};
QueryParamNameResource.ctorParameters = () => [
    { type: _rest_api_service__WEBPACK_IMPORTED_MODULE_2__["RestApiService"] }
];
QueryParamNameResource = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], QueryParamNameResource);



/***/ }),

/***/ "tpJP":
/*!**************************************!*\
  !*** ./src/app/data/schema/alias.ts ***!
  \**************************************/
/*! exports provided: Alias */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Alias", function() { return Alias; });
class Alias {
    constructor(alias) {
        this.id = alias.id;
        this.name = alias.name;
        this.components = alias.components;
    }
}


/***/ }),

/***/ "u7xO":
/*!********************************************!*\
  !*** ./src/app/data/schema/query-param.ts ***!
  \********************************************/
/*! exports provided: QueryParam */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "QueryParam", function() { return QueryParam; });
/* harmony import */ var _request_component__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./request-component */ "2bXN");

class QueryParam extends _request_component__WEBPACK_IMPORTED_MODULE_0__["RequestComponent"] {
    constructor(queryParam) {
        super(3, queryParam.id, queryParam.alias);
        this.name = queryParam.name;
        this.value = queryParam.value;
        this.aliasName = queryParam.alias_name;
        this.isRequired = queryParam.is_required;
    }
}


/***/ }),

/***/ "vAmI":
/*!************************************!*\
  !*** ./src/app/core/http/index.ts ***!
  \************************************/
/*! exports provided: AgentService, AliasResource, AliasValueResource, BodyParamNameResource, BodyParamResource, EndpointResource, HeaderNameResource, HeaderResource, HttpService, OmniauthCallbacksApi, OrganizationResource, OrganizationsUserResource, PathSegmentNameResource, PathSegmentResource, PaymentMethodResource, PlanResource, ProjectResource, ProjectsUserResource, QueryParamNameResource, QueryParamResource, RequestResource, ResponseResolverResource, ResponseResource, ResponseHeaderResource, ScenarioResource, SubscriptionResource, UserResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _agent_service__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./agent.service */ "/JUU");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "AgentService", function() { return _agent_service__WEBPACK_IMPORTED_MODULE_0__["AgentService"]; });

/* harmony import */ var _alias_resource_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./alias-resource.service */ "4GLy");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "AliasResource", function() { return _alias_resource_service__WEBPACK_IMPORTED_MODULE_1__["AliasResource"]; });

/* harmony import */ var _alias_value_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./alias-value-resource.service */ "oFyy");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "AliasValueResource", function() { return _alias_value_resource_service__WEBPACK_IMPORTED_MODULE_2__["AliasValueResource"]; });

/* harmony import */ var _body_param_name_resource_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./body-param-name-resource.service */ "A/vA");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "BodyParamNameResource", function() { return _body_param_name_resource_service__WEBPACK_IMPORTED_MODULE_3__["BodyParamNameResource"]; });

/* harmony import */ var _body_param_resource_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./body-param-resource.service */ "npeK");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "BodyParamResource", function() { return _body_param_resource_service__WEBPACK_IMPORTED_MODULE_4__["BodyParamResource"]; });

/* harmony import */ var _endpoint_resource_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./endpoint-resource.service */ "T+qy");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "EndpointResource", function() { return _endpoint_resource_service__WEBPACK_IMPORTED_MODULE_5__["EndpointResource"]; });

/* harmony import */ var _header_name_resource_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./header-name-resource.service */ "B1Wa");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "HeaderNameResource", function() { return _header_name_resource_service__WEBPACK_IMPORTED_MODULE_6__["HeaderNameResource"]; });

/* harmony import */ var _header_resource_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./header-resource.service */ "Wbda");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "HeaderResource", function() { return _header_resource_service__WEBPACK_IMPORTED_MODULE_7__["HeaderResource"]; });

/* harmony import */ var _http_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./http.service */ "gHic");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "HttpService", function() { return _http_service__WEBPACK_IMPORTED_MODULE_8__["HttpService"]; });

/* harmony import */ var _omniauth_callbacks_api_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./omniauth-callbacks-api.service */ "RdP6");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "OmniauthCallbacksApi", function() { return _omniauth_callbacks_api_service__WEBPACK_IMPORTED_MODULE_9__["OmniauthCallbacksApi"]; });

/* harmony import */ var _organization_resource_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./organization-resource.service */ "wjWB");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "OrganizationResource", function() { return _organization_resource_service__WEBPACK_IMPORTED_MODULE_10__["OrganizationResource"]; });

/* harmony import */ var _organizations_user_resource_service__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./organizations-user-resource.service */ "YCZM");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "OrganizationsUserResource", function() { return _organizations_user_resource_service__WEBPACK_IMPORTED_MODULE_11__["OrganizationsUserResource"]; });

/* harmony import */ var _path_segment_name_resource_service__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./path-segment-name-resource.service */ "hX/M");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "PathSegmentNameResource", function() { return _path_segment_name_resource_service__WEBPACK_IMPORTED_MODULE_12__["PathSegmentNameResource"]; });

/* harmony import */ var _path_segment_resource_service__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./path-segment-resource.service */ "Cq9o");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "PathSegmentResource", function() { return _path_segment_resource_service__WEBPACK_IMPORTED_MODULE_13__["PathSegmentResource"]; });

/* harmony import */ var _payment_method_resource_service__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./payment-method-resource.service */ "z1g2");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "PaymentMethodResource", function() { return _payment_method_resource_service__WEBPACK_IMPORTED_MODULE_14__["PaymentMethodResource"]; });

/* harmony import */ var _plan_resource_service__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ./plan-resource.service */ "TE1C");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "PlanResource", function() { return _plan_resource_service__WEBPACK_IMPORTED_MODULE_15__["PlanResource"]; });

/* harmony import */ var _project_resource_service__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ./project-resource.service */ "4UAC");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "ProjectResource", function() { return _project_resource_service__WEBPACK_IMPORTED_MODULE_16__["ProjectResource"]; });

/* harmony import */ var _projects_user_resource_service__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! ./projects-user-resource.service */ "XTWy");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "ProjectsUserResource", function() { return _projects_user_resource_service__WEBPACK_IMPORTED_MODULE_17__["ProjectsUserResource"]; });

/* harmony import */ var _query_param_name_resource_service__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! ./query-param-name-resource.service */ "ti5q");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "QueryParamNameResource", function() { return _query_param_name_resource_service__WEBPACK_IMPORTED_MODULE_18__["QueryParamNameResource"]; });

/* harmony import */ var _query_param_resource_service__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! ./query-param-resource.service */ "kqhm");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "QueryParamResource", function() { return _query_param_resource_service__WEBPACK_IMPORTED_MODULE_19__["QueryParamResource"]; });

/* harmony import */ var _request_resource_service__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! ./request-resource.service */ "4/Wj");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "RequestResource", function() { return _request_resource_service__WEBPACK_IMPORTED_MODULE_20__["RequestResource"]; });

/* harmony import */ var _response_resolver_resource_service__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! ./response-resolver-resource.service */ "3aTg");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "ResponseResolverResource", function() { return _response_resolver_resource_service__WEBPACK_IMPORTED_MODULE_21__["ResponseResolverResource"]; });

/* harmony import */ var _response_resource_service__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! ./response-resource.service */ "z06h");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "ResponseResource", function() { return _response_resource_service__WEBPACK_IMPORTED_MODULE_22__["ResponseResource"]; });

/* harmony import */ var _response_header_resource_service__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! ./response-header-resource.service */ "n/pC");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "ResponseHeaderResource", function() { return _response_header_resource_service__WEBPACK_IMPORTED_MODULE_23__["ResponseHeaderResource"]; });

/* harmony import */ var _scenario_resource_service__WEBPACK_IMPORTED_MODULE_24__ = __webpack_require__(/*! ./scenario-resource.service */ "3Ncz");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "ScenarioResource", function() { return _scenario_resource_service__WEBPACK_IMPORTED_MODULE_24__["ScenarioResource"]; });

/* harmony import */ var _subscription_resource_service__WEBPACK_IMPORTED_MODULE_25__ = __webpack_require__(/*! ./subscription-resource.service */ "FKU7");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "SubscriptionResource", function() { return _subscription_resource_service__WEBPACK_IMPORTED_MODULE_25__["SubscriptionResource"]; });

/* harmony import */ var _user_resource_service__WEBPACK_IMPORTED_MODULE_26__ = __webpack_require__(/*! ./user-resource.service */ "9IlP");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "UserResource", function() { return _user_resource_service__WEBPACK_IMPORTED_MODULE_26__["UserResource"]; });






























/***/ }),

/***/ "vY5A":
/*!***************************************!*\
  !*** ./src/app/app-routing.module.ts ***!
  \***************************************/
/*! exports provided: AppRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AppRoutingModule", function() { return AppRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _core_guards_auth_guard__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @core/guards/auth.guard */ "NUQi");
/* harmony import */ var _core_guards_no_auth_guard__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @core/guards/no-auth.guard */ "pfe1");
/* harmony import */ var _layout_custom_layout_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @layout/custom-layout.component */ "9a6L");






const routes = [
    {
        path: '',
        loadChildren: () => __webpack_require__.e(/*! import() | home-home-module */ "home-home-module").then(__webpack_require__.bind(null, /*! @home/home.module */ "iydT")).then(m => m.HomeModule),
        pathMatch: 'full',
        canActivate: [_core_guards_no_auth_guard__WEBPACK_IMPORTED_MODULE_4__["NoAuthGuard"]],
    },
    {
        path: 'subscriptions',
        component: _layout_custom_layout_component__WEBPACK_IMPORTED_MODULE_5__["CustomLayoutComponent"],
        children: [
            {
                path: '',
                loadChildren: () => Promise.all(/*! import() | subscriptions-subscriptions-module */[__webpack_require__.e("common"), __webpack_require__.e("subscriptions-subscriptions-module")]).then(__webpack_require__.bind(null, /*! @subscriptions/subscriptions.module */ "XtcF")).then(m => m.SubscriptionsModule),
            },
        ],
    },
    {
        path: 'login',
        loadChildren: () => Promise.all(/*! import() | auth-pages-login-login-module */[__webpack_require__.e("default~aliases-aliases-module~auth-pages-login-login-module~auth-pages-register-register-module~end~16c71568"), __webpack_require__.e("common"), __webpack_require__.e("auth-pages-login-login-module")]).then(__webpack_require__.bind(null, /*! @auth/pages/login/login.module */ "ZFij")).then(m => m.LoginModule),
        canActivate: [_core_guards_no_auth_guard__WEBPACK_IMPORTED_MODULE_4__["NoAuthGuard"]],
    },
    {
        path: 'register',
        loadChildren: () => Promise.all(/*! import() | auth-pages-register-register-module */[__webpack_require__.e("default~aliases-aliases-module~auth-pages-login-login-module~auth-pages-register-register-module~end~16c71568"), __webpack_require__.e("common"), __webpack_require__.e("auth-pages-register-register-module")]).then(__webpack_require__.bind(null, /*! @auth/pages/register/register.module */ "1TiS")).then(m => m.RegisterModule),
        canActivate: [_core_guards_no_auth_guard__WEBPACK_IMPORTED_MODULE_4__["NoAuthGuard"]],
    },
    {
        path: 'forgot-password',
        loadChildren: () => __webpack_require__.e(/*! import() | auth-pages-forgot-password-forgot-password-module */ "auth-pages-forgot-password-forgot-password-module").then(__webpack_require__.bind(null, /*! @auth/pages/forgot-password/forgot-password.module */ "iXA7")).then(m => m.ForgotPasswordModule),
    },
    {
        path: 'projects',
        component: _layout_custom_layout_component__WEBPACK_IMPORTED_MODULE_5__["CustomLayoutComponent"],
        children: [
            {
                path: '',
                loadChildren: () => Promise.all(/*! import() | projects-projects-module */[__webpack_require__.e("default~aliases-aliases-module~auth-pages-login-login-module~auth-pages-register-register-module~end~16c71568"), __webpack_require__.e("default~aliases-aliases-module~endpoints-endpoints-module~organizations-organizations-module~project~eb28f6f5"), __webpack_require__.e("default~aliases-aliases-module~endpoints-endpoints-module~organizations-organizations-module~project~11ec6de4"), __webpack_require__.e("default~organizations-organizations-module~projects-projects-module~requests-requests-module~scenari~04d380cf"), __webpack_require__.e("default~aliases-aliases-module~endpoints-endpoints-module~organizations-organizations-module~project~79418c77"), __webpack_require__.e("default~organizations-organizations-module~projects-projects-module~users-users-module"), __webpack_require__.e("common"), __webpack_require__.e("projects-projects-module")]).then(__webpack_require__.bind(null, /*! @projects/projects.module */ "l1Fo")).then(m => m.ProjectsModule),
                canActivate: [_core_guards_auth_guard__WEBPACK_IMPORTED_MODULE_3__["AuthGuard"]],
            },
        ],
    },
    {
        path: 'scenarios',
        component: _layout_custom_layout_component__WEBPACK_IMPORTED_MODULE_5__["CustomLayoutComponent"],
        children: [
            {
                path: '',
                loadChildren: () => Promise.all(/*! import() | scenarios-scenarios-module */[__webpack_require__.e("default~aliases-aliases-module~auth-pages-login-login-module~auth-pages-register-register-module~end~16c71568"), __webpack_require__.e("default~aliases-aliases-module~endpoints-endpoints-module~organizations-organizations-module~project~eb28f6f5"), __webpack_require__.e("default~aliases-aliases-module~endpoints-endpoints-module~organizations-organizations-module~project~11ec6de4"), __webpack_require__.e("default~organizations-organizations-module~projects-projects-module~requests-requests-module~scenari~04d380cf"), __webpack_require__.e("default~aliases-aliases-module~endpoints-endpoints-module~organizations-organizations-module~project~79418c77"), __webpack_require__.e("default~endpoints-endpoints-module~requests-requests-module~scenarios-scenarios-module"), __webpack_require__.e("default~requests-requests-module~scenarios-scenarios-module~subscriptions-pages-buy-buy-module"), __webpack_require__.e("default~requests-requests-module~scenarios-scenarios-module"), __webpack_require__.e("scenarios-scenarios-module")]).then(__webpack_require__.bind(null, /*! @scenarios/scenarios.module */ "Bavy")).then(m => m.ScenariosModule),
                canActivate: [_core_guards_auth_guard__WEBPACK_IMPORTED_MODULE_3__["AuthGuard"]],
            },
        ],
    },
    {
        path: 'requests',
        component: _layout_custom_layout_component__WEBPACK_IMPORTED_MODULE_5__["CustomLayoutComponent"],
        children: [
            {
                path: '',
                loadChildren: () => Promise.all(/*! import() | requests-requests-module */[__webpack_require__.e("default~aliases-aliases-module~auth-pages-login-login-module~auth-pages-register-register-module~end~16c71568"), __webpack_require__.e("default~aliases-aliases-module~endpoints-endpoints-module~organizations-organizations-module~project~eb28f6f5"), __webpack_require__.e("default~aliases-aliases-module~endpoints-endpoints-module~organizations-organizations-module~project~11ec6de4"), __webpack_require__.e("default~organizations-organizations-module~projects-projects-module~requests-requests-module~scenari~04d380cf"), __webpack_require__.e("default~aliases-aliases-module~endpoints-endpoints-module~organizations-organizations-module~project~79418c77"), __webpack_require__.e("default~endpoints-endpoints-module~requests-requests-module~scenarios-scenarios-module"), __webpack_require__.e("default~requests-requests-module~scenarios-scenarios-module~subscriptions-pages-buy-buy-module"), __webpack_require__.e("default~requests-requests-module~scenarios-scenarios-module"), __webpack_require__.e("requests-requests-module")]).then(__webpack_require__.bind(null, /*! @requests/requests.module */ "+olZ")).then(m => m.RequestsModule),
                canActivate: [_core_guards_auth_guard__WEBPACK_IMPORTED_MODULE_3__["AuthGuard"]],
            },
        ],
    },
    {
        path: 'endpoints',
        component: _layout_custom_layout_component__WEBPACK_IMPORTED_MODULE_5__["CustomLayoutComponent"],
        children: [
            {
                path: '',
                loadChildren: () => Promise.all(/*! import() | endpoints-endpoints-module */[__webpack_require__.e("default~aliases-aliases-module~auth-pages-login-login-module~auth-pages-register-register-module~end~16c71568"), __webpack_require__.e("default~aliases-aliases-module~endpoints-endpoints-module~organizations-organizations-module~project~eb28f6f5"), __webpack_require__.e("default~aliases-aliases-module~endpoints-endpoints-module~organizations-organizations-module~project~11ec6de4"), __webpack_require__.e("default~aliases-aliases-module~endpoints-endpoints-module~organizations-organizations-module~project~79418c77"), __webpack_require__.e("default~endpoints-endpoints-module~requests-requests-module~scenarios-scenarios-module"), __webpack_require__.e("endpoints-endpoints-module")]).then(__webpack_require__.bind(null, /*! @endpoints/endpoints.module */ "a5rT")).then(m => m.EndpointsModule),
                canActivate: [_core_guards_auth_guard__WEBPACK_IMPORTED_MODULE_3__["AuthGuard"]],
            },
        ],
    },
    {
        path: 'aliases',
        component: _layout_custom_layout_component__WEBPACK_IMPORTED_MODULE_5__["CustomLayoutComponent"],
        children: [
            {
                path: '',
                loadChildren: () => Promise.all(/*! import() | aliases-aliases-module */[__webpack_require__.e("default~aliases-aliases-module~auth-pages-login-login-module~auth-pages-register-register-module~end~16c71568"), __webpack_require__.e("default~aliases-aliases-module~endpoints-endpoints-module~organizations-organizations-module~project~eb28f6f5"), __webpack_require__.e("default~aliases-aliases-module~endpoints-endpoints-module~organizations-organizations-module~project~11ec6de4"), __webpack_require__.e("default~aliases-aliases-module~endpoints-endpoints-module~organizations-organizations-module~project~79418c77"), __webpack_require__.e("aliases-aliases-module")]).then(__webpack_require__.bind(null, /*! @aliases/aliases.module */ "jfiX")).then(m => m.AliasesModule),
                canActivate: [_core_guards_auth_guard__WEBPACK_IMPORTED_MODULE_3__["AuthGuard"]],
            },
        ],
    },
    {
        path: 'users',
        component: _layout_custom_layout_component__WEBPACK_IMPORTED_MODULE_5__["CustomLayoutComponent"],
        children: [
            {
                path: '',
                loadChildren: () => Promise.all(/*! import() | users-users-module */[__webpack_require__.e("default~aliases-aliases-module~auth-pages-login-login-module~auth-pages-register-register-module~end~16c71568"), __webpack_require__.e("default~aliases-aliases-module~endpoints-endpoints-module~organizations-organizations-module~project~eb28f6f5"), __webpack_require__.e("default~aliases-aliases-module~endpoints-endpoints-module~organizations-organizations-module~project~11ec6de4"), __webpack_require__.e("default~organizations-organizations-module~projects-projects-module~requests-requests-module~scenari~04d380cf"), __webpack_require__.e("default~organizations-organizations-module~projects-projects-module~users-users-module"), __webpack_require__.e("default~organizations-organizations-module~subscriptions-pages-buy-buy-module~users-users-module"), __webpack_require__.e("common"), __webpack_require__.e("users-users-module")]).then(__webpack_require__.bind(null, /*! @users/users.module */ "BJHQ")).then(m => m.UsersModule),
                canActivate: [_core_guards_auth_guard__WEBPACK_IMPORTED_MODULE_3__["AuthGuard"]],
            },
        ],
    },
    {
        path: 'organizations',
        component: _layout_custom_layout_component__WEBPACK_IMPORTED_MODULE_5__["CustomLayoutComponent"],
        children: [
            {
                path: '',
                loadChildren: () => Promise.all(/*! import() | organizations-organizations-module */[__webpack_require__.e("default~aliases-aliases-module~auth-pages-login-login-module~auth-pages-register-register-module~end~16c71568"), __webpack_require__.e("default~aliases-aliases-module~endpoints-endpoints-module~organizations-organizations-module~project~eb28f6f5"), __webpack_require__.e("default~aliases-aliases-module~endpoints-endpoints-module~organizations-organizations-module~project~11ec6de4"), __webpack_require__.e("default~organizations-organizations-module~projects-projects-module~requests-requests-module~scenari~04d380cf"), __webpack_require__.e("default~aliases-aliases-module~endpoints-endpoints-module~organizations-organizations-module~project~79418c77"), __webpack_require__.e("default~organizations-organizations-module~projects-projects-module~users-users-module"), __webpack_require__.e("default~organizations-organizations-module~subscriptions-pages-buy-buy-module~users-users-module"), __webpack_require__.e("common"), __webpack_require__.e("organizations-organizations-module")]).then(__webpack_require__.bind(null, /*! @organizations/organizations.module */ "fBQL")).then(m => m.OrganizationsModule),
                canActivate: [_core_guards_auth_guard__WEBPACK_IMPORTED_MODULE_3__["AuthGuard"]],
            },
        ],
    },
    {
        path: '**',
        loadChildren: () => __webpack_require__.e(/*! import() | error-pages-404-error-404-module */ "error-pages-404-error-404-module").then(__webpack_require__.bind(null, /*! @error/pages/404/error-404.module */ "y9RA")).then(m => m.Error404Module),
    },
];
let AppRoutingModule = class AppRoutingModule {
};
AppRoutingModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forRoot(routes, {
                // preloadingStrategy: PreloadAllModules,
                scrollPositionRestoration: 'enabled',
                relativeLinkResolution: 'corrected',
                anchorScrolling: 'enabled',
            }),
        ],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
    })
], AppRoutingModule);



/***/ }),

/***/ "vuK5":
/*!***********************************************!*\
  !*** ./src/app/data/schema/payment-method.ts ***!
  \***********************************************/
/*! exports provided: PaymentMethod, PaymentMethodCard */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PaymentMethod", function() { return PaymentMethod; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PaymentMethodCard", function() { return PaymentMethodCard; });
class PaymentMethod {
    constructor(paymentMethod) {
        this.id = paymentMethod.id;
        this.card = new PaymentMethodCard(paymentMethod.card);
        this.isDefault = paymentMethod.is_default;
    }
}
class PaymentMethodCard {
    constructor(card) {
        this.last4 = card.last4;
        this.brand = card.brand;
        this.expMonth = card.exp_month;
        this.expYear = card.exp_year;
    }
}


/***/ }),

/***/ "wZfh":
/*!***************************************************!*\
  !*** ./src/app/data/constants/route.constants.ts ***!
  \***************************************************/
/*! exports provided: RouteConstants */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RouteConstants", function() { return RouteConstants; });
class RouteConstants {
}
RouteConstants.LOGIN_PAGE = '/login';


/***/ }),

/***/ "whvR":
/*!**************************************************************************************************************!*\
  !*** ./src/app/layout/components/toolbar/components/toolbar-proxy-settings/toolbar-proxy-settings.module.ts ***!
  \**************************************************************************************************************/
/*! exports provided: ToolbarProxySettingsModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ToolbarProxySettingsModule", function() { return ToolbarProxySettingsModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ "s7LF");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_material_core__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/core */ "UhP/");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/material/dialog */ "iELJ");
/* harmony import */ var _angular_material_divider__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/material/divider */ "BSbQ");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/material/form-field */ "Q2Ze");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @angular/material/input */ "e6WT");
/* harmony import */ var _angular_material_menu__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/material/menu */ "rJgo");
/* harmony import */ var _angular_material_select__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/material/select */ "ZTz/");
/* harmony import */ var _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @angular/material/snack-bar */ "zHaW");
/* harmony import */ var _angular_material_tabs__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @angular/material/tabs */ "M9ds");
/* harmony import */ var _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @angular/material/tooltip */ "ZFy/");
/* harmony import */ var _vex_pipes_relative_date_time_relative_date_time_module__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @vex/pipes/relative-date-time/relative-date-time.module */ "h4uD");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _components_toolbar_mock_settings_toolbar_mock_settings_component__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! ./components/toolbar-mock-settings/toolbar-mock-settings.component */ "FYDM");
/* harmony import */ var _components_toolbar_record_settings_toolbar_record_settings_component__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! ./components/toolbar-record-settings/toolbar-record-settings.component */ "f/93");
/* harmony import */ var _toolbar_proxy_settings_component__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! ./toolbar-proxy-settings.component */ "N/jG");























let ToolbarProxySettingsModule = class ToolbarProxySettingsModule {
};
ToolbarProxySettingsModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [
            _components_toolbar_mock_settings_toolbar_mock_settings_component__WEBPACK_IMPORTED_MODULE_20__["ToolbarMockSettingsComponent"],
            _toolbar_proxy_settings_component__WEBPACK_IMPORTED_MODULE_22__["ToolbarProxySettingsComponent"],
            _components_toolbar_record_settings_toolbar_record_settings_component__WEBPACK_IMPORTED_MODULE_21__["ToolbarRecordSettingsComponent"],
        ],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"],
            _angular_router__WEBPACK_IMPORTED_MODULE_5__["RouterModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_6__["MatButtonModule"],
            _angular_material_dialog__WEBPACK_IMPORTED_MODULE_8__["MatDialogModule"],
            _angular_material_divider__WEBPACK_IMPORTED_MODULE_9__["MatDividerModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_11__["MatIconModule"],
            _angular_material_input__WEBPACK_IMPORTED_MODULE_12__["MatInputModule"],
            _angular_material_form_field__WEBPACK_IMPORTED_MODULE_10__["MatFormFieldModule"],
            _angular_material_menu__WEBPACK_IMPORTED_MODULE_13__["MatMenuModule"],
            _angular_material_core__WEBPACK_IMPORTED_MODULE_7__["MatRippleModule"],
            _angular_material_select__WEBPACK_IMPORTED_MODULE_14__["MatSelectModule"],
            _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_15__["MatSnackBarModule"],
            _angular_material_tabs__WEBPACK_IMPORTED_MODULE_16__["MatTabsModule"],
            _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_17__["MatTooltipModule"],
            _vex_pipes_relative_date_time_relative_date_time_module__WEBPACK_IMPORTED_MODULE_18__["RelativeDateTimeModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_19__["IconModule"],
        ],
        exports: [_toolbar_proxy_settings_component__WEBPACK_IMPORTED_MODULE_22__["ToolbarProxySettingsComponent"]],
        entryComponents: [
            _components_toolbar_mock_settings_toolbar_mock_settings_component__WEBPACK_IMPORTED_MODULE_20__["ToolbarMockSettingsComponent"],
            _components_toolbar_record_settings_toolbar_record_settings_component__WEBPACK_IMPORTED_MODULE_21__["ToolbarRecordSettingsComponent"],
        ],
    })
], ToolbarProxySettingsModule);



/***/ }),

/***/ "wjWB":
/*!************************************************************!*\
  !*** ./src/app/core/http/organization-resource.service.ts ***!
  \************************************************************/
/*! exports provided: OrganizationResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "OrganizationResource", function() { return OrganizationResource; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _rest_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rest-api.service */ "iCaw");



let OrganizationResource = class OrganizationResource {
    constructor(restApi) {
        this.restApi = restApi;
        this.ENDPOINT = 'organizations';
    }
    index(queryParams) {
        return this.restApi.index([this.ENDPOINT], queryParams);
    }
    show(id, queryParams) {
        return this.restApi.show([this.ENDPOINT, id], queryParams);
    }
    create(body) {
        return this.restApi.create([this.ENDPOINT], body);
    }
    update(id, body) {
        return this.restApi.update([this.ENDPOINT, id], body);
    }
    destroy(id) {
        return this.restApi.destroy([this.ENDPOINT, id]);
    }
    subscription(id, queryParams) {
        return this.restApi.index([this.ENDPOINT, id, 'subscription'], queryParams);
    }
    payments(id, queryParams) {
        return this.restApi.index([this.ENDPOINT, id, 'payments'], queryParams);
    }
};
OrganizationResource.ctorParameters = () => [
    { type: _rest_api_service__WEBPACK_IMPORTED_MODULE_2__["RestApiService"] }
];
OrganizationResource = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], OrganizationResource);



/***/ }),

/***/ "wuZS":
/*!****************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/@vex/layout/navigation/navigation.component.html ***!
  \****************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div class=\"navigation\" fxLayout=\"row\" fxLayoutAlign=\"start center\" vexContainer>\r\n  <vex-navigation-item *ngFor=\"let item of items\" [item]=\"item\"></vex-navigation-item>\r\n</div>\r\n\r\n");

/***/ }),

/***/ "x+pQ":
/*!********************************************************!*\
  !*** ./src/@vex/components/search/search.component.ts ***!
  \********************************************************/
/*! exports provided: SearchComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SearchComponent", function() { return SearchComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_search_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./search.component.html */ "dPIg");
/* harmony import */ var _search_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./search.component.scss */ "0tFB");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ "s7LF");
/* harmony import */ var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @iconify/icons-ic/twotone-close */ "5mnX");
/* harmony import */ var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var ngx_take_until_destroy__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ngx-take-until-destroy */ "DnKK");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! rxjs/operators */ "kU1M");
/* harmony import */ var _services_layout_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../services/layout.service */ "CtTw");
/* harmony import */ var _services_search_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../services/search.service */ "OTSD");










let SearchComponent = class SearchComponent {
    constructor(layoutService, searchService) {
        this.layoutService = layoutService;
        this.searchService = searchService;
        this.show$ = this.layoutService.searchOpen$;
        this.searchCtrl = new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"]();
        this.icClose = _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_5___default.a;
    }
    ngOnInit() {
        this.searchService.isOpenSubject.next(true);
        this.searchCtrl.valueChanges.pipe(Object(ngx_take_until_destroy__WEBPACK_IMPORTED_MODULE_6__["untilDestroyed"])(this)).subscribe(value => this.searchService.valueChangesSubject.next(value));
        this.show$.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_7__["filter"])(show => show), Object(ngx_take_until_destroy__WEBPACK_IMPORTED_MODULE_6__["untilDestroyed"])(this)).subscribe(() => this.input.nativeElement.focus());
    }
    close() {
        this.layoutService.closeSearch();
        this.searchCtrl.setValue(undefined);
        this.searchService.isOpenSubject.next(false);
    }
    search() {
        this.searchService.submitSubject.next(this.searchCtrl.value);
        this.close();
    }
    ngOnDestroy() {
        this.layoutService.closeSearch();
        this.searchCtrl.setValue(undefined);
        this.searchService.isOpenSubject.next(false);
    }
};
SearchComponent.ctorParameters = () => [
    { type: _services_layout_service__WEBPACK_IMPORTED_MODULE_8__["LayoutService"] },
    { type: _services_search_service__WEBPACK_IMPORTED_MODULE_9__["SearchService"] }
];
SearchComponent.propDecorators = {
    input: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ViewChild"], args: ['searchInput', { static: true },] }]
};
SearchComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'vex-search',
        template: _raw_loader_search_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_search_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], SearchComponent);



/***/ }),

/***/ "xDFx":
/*!************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/@vex/components/footer/footer.component.html ***!
  \************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div class=\"footer\" fxLayout=\"row\">\r\n  <div fxFlex=\"auto\" fxLayout=\"row\" fxLayoutAlign=\"start center\" vexContainer>\r\n    <a class=\"action\"\r\n       color=\"primary\"\r\n       fxFlex=\"none\"\r\n       href=\"//themeforest.net/item/vex-angular-8-material-design-admin-template/24472891\"\r\n       id=\"get-vex\"\r\n       mat-raised-button>\r\n      <ic-icon [icon]=\"icShoppingBasket\" class=\"ltr:mr-2 rtl:ml-2\" inline=\"true\" size=\"18px\"></ic-icon>\r\n      <span>Get Vex (Angular 8+)</span>\r\n    </a>\r\n    <div class=\"ltr:ml-4 rtl:mr-4\" fxHide fxShow.gt-sm>\r\n      Vex - Angular 8+ Material Design Admin Template - Save 100s of hours designing and coding\r\n    </div>\r\n  </div>\r\n</div>\r\n");

/***/ }),

/***/ "yVwa":
/*!**************************************************************************!*\
  !*** ./src/@vex/components/navigation-item/navigation-item.component.ts ***!
  \**************************************************************************/
/*! exports provided: NavigationItemComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "NavigationItemComponent", function() { return NavigationItemComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_navigation_item_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./navigation-item.component.html */ "sh9p");
/* harmony import */ var _navigation_item_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./navigation-item.component.scss */ "C8+Y");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! rxjs/operators */ "kU1M");
/* harmony import */ var _services_navigation_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../services/navigation.service */ "0vMP");
/* harmony import */ var _utils_track_by__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../utils/track-by */ "zK3P");








let NavigationItemComponent = class NavigationItemComponent {
    constructor(navigationService, router) {
        this.navigationService = navigationService;
        this.router = router;
        this.isActive$ = this.router.events.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["filter"])(event => event instanceof _angular_router__WEBPACK_IMPORTED_MODULE_4__["NavigationEnd"]), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["startWith"])(null), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["map"])(() => (item) => this.hasActiveChilds(item)));
        this.isLink = this.navigationService.isLink;
        this.isDropdown = this.navigationService.isDropdown;
        this.isSubheading = this.navigationService.isSubheading;
        this.trackByRoute = _utils_track_by__WEBPACK_IMPORTED_MODULE_7__["trackByRoute"];
    }
    ngOnInit() {
    }
    hasActiveChilds(parent) {
        if (this.isLink(parent)) {
            return this.router.isActive(parent.route, false);
        }
        if (this.isDropdown(parent) || this.isSubheading(parent)) {
            return parent.children.some(child => {
                if (this.isDropdown(child)) {
                    return this.hasActiveChilds(child);
                }
                if (this.isLink(child) && !this.isFunction(child.route)) {
                    return this.router.isActive(child.route, false);
                }
                return false;
            });
        }
        return false;
    }
    isFunction(prop) {
        return prop instanceof Function;
    }
};
NavigationItemComponent.ctorParameters = () => [
    { type: _services_navigation_service__WEBPACK_IMPORTED_MODULE_6__["NavigationService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["Router"] }
];
NavigationItemComponent.propDecorators = {
    item: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"] }]
};
NavigationItemComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'vex-navigation-item',
        template: _raw_loader_navigation_item_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_navigation_item_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], NavigationItemComponent);



/***/ }),

/***/ "ycnu":
/*!*********************************************************!*\
  !*** ./src/@vex/layout/navigation/navigation.module.ts ***!
  \*********************************************************/
/*! exports provided: NavigationModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "NavigationModule", function() { return NavigationModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_material_core__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/core */ "UhP/");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _angular_material_menu__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/menu */ "rJgo");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _components_navigation_item_navigation_item_module__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../components/navigation-item/navigation-item.module */ "5PI4");
/* harmony import */ var _directives_container_container_module__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../directives/container/container.module */ "68Yx");
/* harmony import */ var _navigation_component__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./navigation.component */ "FblR");












let NavigationModule = class NavigationModule {
};
NavigationModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_navigation_component__WEBPACK_IMPORTED_MODULE_11__["NavigationComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _angular_material_core__WEBPACK_IMPORTED_MODULE_4__["MatRippleModule"],
            _angular_material_menu__WEBPACK_IMPORTED_MODULE_6__["MatMenuModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_5__["MatIconModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_8__["IconModule"],
            _angular_router__WEBPACK_IMPORTED_MODULE_7__["RouterModule"],
            _components_navigation_item_navigation_item_module__WEBPACK_IMPORTED_MODULE_9__["NavigationItemModule"],
            _directives_container_container_module__WEBPACK_IMPORTED_MODULE_10__["ContainerModule"]
        ],
        exports: [_navigation_component__WEBPACK_IMPORTED_MODULE_11__["NavigationComponent"]]
    })
], NavigationModule);



/***/ }),

/***/ "ynKk":
/*!*********************************************!*\
  !*** ./src/@vex/layout/layout.component.ts ***!
  \*********************************************/
/*! exports provided: LayoutComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LayoutComponent", function() { return LayoutComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_layout_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./layout.component.html */ "BrZ/");
/* harmony import */ var _layout_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./layout.component.scss */ "+f9C");
/* harmony import */ var _angular_cdk_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/cdk/layout */ "HeVh");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_material_sidenav__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/sidenav */ "q7Ft");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var ngx_take_until_destroy__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ngx-take-until-destroy */ "DnKK");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! rxjs/operators */ "kU1M");
/* harmony import */ var _services_config_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../services/config.service */ "lC2v");
/* harmony import */ var _services_layout_service__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../services/layout.service */ "CtTw");
/* harmony import */ var _utils_check_router_childs_data__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../utils/check-router-childs-data */ "3TZW");
/* harmony import */ var _utils_tailwindcss__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ../utils/tailwindcss */ "XXSj");














let LayoutComponent = class LayoutComponent {
    constructor(cd, breakpointObserver, layoutService, configService, router, document) {
        this.cd = cd;
        this.breakpointObserver = breakpointObserver;
        this.layoutService = layoutService;
        this.configService = configService;
        this.router = router;
        this.document = document;
        this.isLayoutVertical$ = this.configService.config$.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_9__["map"])(config => config.layout === 'vertical'));
        this.isBoxed$ = this.configService.config$.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_9__["map"])(config => config.boxed));
        this.isToolbarFixed$ = this.configService.config$.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_9__["map"])(config => config.toolbar.fixed));
        this.isFooterFixed$ = this.configService.config$.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_9__["map"])(config => config.footer.fixed));
        this.isFooterVisible$ = this.configService.config$.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_9__["map"])(config => config.footer.visible));
        this.sidenavCollapsed$ = this.layoutService.sidenavCollapsed$;
        this.sidenavCollapsedOpen$ = this.layoutService.sidenavCollapsedOpen$;
        this.sidenavOpen$ = this.layoutService.sidenavOpen$;
        this.isDesktop$ = this.breakpointObserver.observe(`(min-width: ${_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_13__["default"].screens.lg})`).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_9__["map"])(state => state.matches));
        this.scrollDisabled$ = this.router.events.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_9__["filter"])(event => event instanceof _angular_router__WEBPACK_IMPORTED_MODULE_7__["NavigationEnd"]), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_9__["startWith"])(null), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_9__["map"])(() => Object(_utils_check_router_childs_data__WEBPACK_IMPORTED_MODULE_12__["checkRouterChildsData"])(this.router.routerState.root.snapshot, data => data.scrollDisabled)));
        this.containerEnabled$ = this.router.events.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_9__["filter"])(event => event instanceof _angular_router__WEBPACK_IMPORTED_MODULE_7__["NavigationEnd"]), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_9__["startWith"])(null), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_9__["map"])(() => Object(_utils_check_router_childs_data__WEBPACK_IMPORTED_MODULE_12__["checkRouterChildsData"])(this.router.routerState.root.snapshot, data => data.containerEnabled)));
        this.searchOpen$ = this.layoutService.searchOpen$;
    }
    ngOnInit() {
        // this.isDesktop$.pipe(
        //   filter(matches => !matches),
        //   untilDestroyed(this)
        // ).subscribe(() => this.layoutService.expandSidenav());
        this.layoutService.quickpanelOpen$.pipe(Object(ngx_take_until_destroy__WEBPACK_IMPORTED_MODULE_8__["untilDestroyed"])(this)).subscribe(open => open ? this.quickpanel.open() : this.quickpanel.close());
        this.layoutService.sidenavOpen$.pipe(Object(ngx_take_until_destroy__WEBPACK_IMPORTED_MODULE_8__["untilDestroyed"])(this)).subscribe(open => open ? this.sidenav.open() : this.sidenav.close());
        this.router.events.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_9__["filter"])(event => event instanceof _angular_router__WEBPACK_IMPORTED_MODULE_7__["NavigationEnd"]), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_9__["withLatestFrom"])(this.isDesktop$), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_9__["filter"])(([event, matches]) => !matches), Object(ngx_take_until_destroy__WEBPACK_IMPORTED_MODULE_8__["untilDestroyed"])(this)).subscribe(() => this.sidenav.close());
    }
    ngAfterViewInit() {
        this.router.events.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_9__["filter"])((e) => e instanceof _angular_router__WEBPACK_IMPORTED_MODULE_7__["Scroll"]), Object(ngx_take_until_destroy__WEBPACK_IMPORTED_MODULE_8__["untilDestroyed"])(this)).subscribe(e => {
            if (e.position) {
                // backward navigation
                this.sidenavContainer.scrollable.scrollTo({
                    start: e.position[0],
                    top: e.position[1]
                });
            }
            else if (e.anchor) {
                // anchor navigation
                const scroll = (anchor) => this.sidenavContainer.scrollable.scrollTo({
                    behavior: 'smooth',
                    top: anchor.offsetTop,
                    left: anchor.offsetLeft
                });
                let anchorElem = this.document.getElementById(e.anchor);
                if (anchorElem) {
                    scroll(anchorElem);
                }
                else {
                    setTimeout(() => {
                        anchorElem = this.document.getElementById(e.anchor);
                        scroll(anchorElem);
                    }, 100);
                }
            }
            else {
                // forward navigation
                this.sidenavContainer.scrollable.scrollTo({
                    top: 0,
                    start: 0
                });
            }
        });
    }
    ngOnDestroy() { }
};
LayoutComponent.ctorParameters = () => [
    { type: _angular_core__WEBPACK_IMPORTED_MODULE_5__["ChangeDetectorRef"] },
    { type: _angular_cdk_layout__WEBPACK_IMPORTED_MODULE_3__["BreakpointObserver"] },
    { type: _services_layout_service__WEBPACK_IMPORTED_MODULE_11__["LayoutService"] },
    { type: _services_config_service__WEBPACK_IMPORTED_MODULE_10__["ConfigService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_7__["Router"] },
    { type: Document, decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_5__["Inject"], args: [_angular_common__WEBPACK_IMPORTED_MODULE_4__["DOCUMENT"],] }] }
];
LayoutComponent.propDecorators = {
    sidenavRef: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_5__["Input"] }],
    toolbarRef: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_5__["Input"] }],
    footerRef: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_5__["Input"] }],
    quickpanelRef: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_5__["Input"] }],
    quickpanel: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_5__["ViewChild"], args: ['quickpanel', { static: true },] }],
    sidenav: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_5__["ViewChild"], args: ['sidenav', { static: true },] }],
    sidenavContainer: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_5__["ViewChild"], args: [_angular_material_sidenav__WEBPACK_IMPORTED_MODULE_6__["MatSidenavContainer"], { static: true },] }]
};
LayoutComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_5__["Component"])({
        selector: 'vex-layout',
        template: _raw_loader_layout_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_layout_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], LayoutComponent);



/***/ }),

/***/ "ynWL":
/*!************************************!*\
  !*** ./src/app/app.component.scss ***!
  \************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJhcHAuY29tcG9uZW50LnNjc3MifQ== */");

/***/ }),

/***/ "z06h":
/*!********************************************************!*\
  !*** ./src/app/core/http/response-resource.service.ts ***!
  \********************************************************/
/*! exports provided: ResponseResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ResponseResource", function() { return ResponseResource; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _rest_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rest-api.service */ "iCaw");



let ResponseResource = class ResponseResource {
    constructor(restApi) {
        this.restApi = restApi;
        this.REQUEST_ENDPOINT = 'requests';
        this.ENDPOINT = 'responses';
    }
    index(requestId, queryParams) {
        return this.restApi.index([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT], queryParams);
    }
    show(requestId, id, queryParams) {
        return this.restApi.show([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT, id], queryParams);
    }
    create(requestId, body) {
        return this.restApi.create([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT], body);
    }
    update(requestId, id, body) {
        return this.restApi.update([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT, id], body);
    }
    destroy(requestId, id) {
        return this.restApi.destroy([this.REQUEST_ENDPOINT, requestId, this.ENDPOINT, id]);
    }
};
ResponseResource.ctorParameters = () => [
    { type: _rest_api_service__WEBPACK_IMPORTED_MODULE_2__["RestApiService"] }
];
ResponseResource = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], ResponseResource);



/***/ }),

/***/ "z1g2":
/*!**************************************************************!*\
  !*** ./src/app/core/http/payment-method-resource.service.ts ***!
  \**************************************************************/
/*! exports provided: PaymentMethodResource */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PaymentMethodResource", function() { return PaymentMethodResource; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _rest_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rest-api.service */ "iCaw");



let PaymentMethodResource = class PaymentMethodResource {
    constructor(restApi) {
        this.restApi = restApi;
        this.ENDPOINT = 'payment_methods';
    }
    index(queryParams) {
        return this.restApi.index([this.ENDPOINT], queryParams);
    }
    show(id, queryParams) {
        return this.restApi.show([this.ENDPOINT, id], queryParams);
    }
    create(body) {
        return this.restApi.create([this.ENDPOINT], body);
    }
    update(id, body) {
        return this.restApi.update([this.ENDPOINT, id], body);
    }
    destroy(id) {
        return this.restApi.destroy([this.ENDPOINT, id]);
    }
};
PaymentMethodResource.ctorParameters = () => [
    { type: _rest_api_service__WEBPACK_IMPORTED_MODULE_2__["RestApiService"] }
];
PaymentMethodResource = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], PaymentMethodResource);



/***/ }),

/***/ "z6XH":
/*!*********************************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/layout/components/toolbar/components/toolbar-proxy-settings/toolbar-proxy-settings.component.html ***!
  \*********************************************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<ng-container *ngIf=\"modes\">\n\n  Proxy Mode\n  \n  <button \n    [class.active]=\"dropdownOpen\" \n    [matMenuTriggerFor]=\"menu\"\n    color=\"accent\"\n    class=\"button ml-3 capitalize\" \n    mat-stroked-button \n    type=\"button\"\n  >\n    {{ modes.active }} \n    <ic-icon [icon]=\"icArrowDropDown\" class=\"ltr:-mr-1 rtl:-ml-1\" inline=\"true\"></ic-icon>\n  </button>\n\n  <ng-container *ngIf=\"modes.active === 'record'\">\n    <span class=\"ml-5\" *ngIf=\"activeProject\">\n      {{ activeProject.name }}\n    </span>\n\n    <span *ngIf=\"activeScenario\" class=\"ml-1 mr-1\">\n      •\n    </span>\n\n    <span *ngIf=\"activeScenario\">\n      {{ activeScenario.name }}\n    </span>\n\n    <button \n      (click)=\"toggleEnabled()\" \n      color=\"accent\"\n      class=\"button ml-3\" \n      mat-raised-button \n      type=\"button\"\n    >\n      <mat-icon *ngIf=\"!modes.enabled\" [icIcon]=\"icPlayArrow\" size=\"22px\"></mat-icon>\n      <mat-icon *ngIf=\"modes.enabled\" [icIcon]=\"icStop\" size=\"22px\"></mat-icon>\n      {{ modes.enabled ? 'STOP' : 'RUN' }}\n    </button>\n\n    <button \n      #originRef \n      (click)=\"showRecordSettings()\" \n      color=\"accent\"\n      class=\"button ml-3\" \n      mat-icon-button \n      matTooltip=\"Settings\"\n      type=\"button\"\n    >\n      <mat-icon [icIcon]=\"icSettings\" size=\"22px\"></mat-icon>\n    </button>\n  </ng-container>\n\n  <ng-container *ngIf=\"modes.active === 'mock'\">\n    <span class=\"ml-5\" *ngIf=\"activeProject\">\n      {{ activeProject.name }}\n    </span>\n\n    <span *ngIf=\"activeScenario\" class=\"ml-1 mr-1\">\n      •\n    </span>\n\n    <span *ngIf=\"activeScenario\">\n      {{ activeScenario.name }}\n    </span>\n\n    <button \n      (click)=\"toggleEnabled()\" \n      color=\"accent\"\n      class=\"button ml-3\" \n      mat-raised-button \n      type=\"button\"\n    >\n      <mat-icon *ngIf=\"!modes.enabled\" [icIcon]=\"icPlayArrow\" size=\"22px\"></mat-icon>\n      <mat-icon *ngIf=\"modes.enabled\" [icIcon]=\"icStop\" size=\"22px\"></mat-icon>\n      {{ modes.enabled ? 'STOP' : 'RUN' }}\n    </button>\n\n    <!-- <span class=\"ml-4\">\n      Settings\n    </span> -->\n\n    <button \n      *ngIf=\"modes.active === 'mock'\"\n      (click)=\"showMockSettings()\" \n      color=\"accent\"\n      class=\"button ml-3\"\n      mat-icon-button \n      matTooltip=\"Settings\"\n      type=\"button\"\n    >\n      <mat-icon [icIcon]=\"icSettings\" size=\"22px\"></mat-icon>\n    </button>\n\n    <button \n      (click)=\"copyUrl()\" \n      color=\"accent\"\n      class=\"button\" \n      mat-icon-button\n      matTooltip=\"Mock URL\" \n      type=\"button\"\n    >\n      <mat-icon [icIcon]=\"icFileCopy\" size=\"22px\"></mat-icon>\n    </button>\n  </ng-container>\n\n  <mat-menu #menu=\"matMenu\">\n    <button \n      *ngFor=\"let mode of modes.list\"\n      (click)=\"setMode(mode)\"\n      class=\"capitalize\"\n      mat-menu-item\n    >\n      {{ mode }}\n    </button>\n  </mat-menu>\n</ng-container>");

/***/ }),

/***/ "zK3P":
/*!************************************!*\
  !*** ./src/@vex/utils/track-by.ts ***!
  \************************************/
/*! exports provided: trackByRoute, trackById, trackByKey, trackByValue, trackByLabel */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "trackByRoute", function() { return trackByRoute; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "trackById", function() { return trackById; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "trackByKey", function() { return trackByKey; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "trackByValue", function() { return trackByValue; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "trackByLabel", function() { return trackByLabel; });
function trackByRoute(index, item) {
    return item.route;
}
function trackById(index, item) {
    return item.id;
}
function trackByKey(index, item) {
    return item.key;
}
function trackByValue(index, value) {
    return value;
}
function trackByLabel(index, value) {
    return value.label;
}


/***/ }),

/***/ "zUnb":
/*!*********************!*\
  !*** ./src/main.ts ***!
  \*********************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_platform_browser_dynamic__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/platform-browser-dynamic */ "wAiw");
/* harmony import */ var _app_app_module__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./app/app.module */ "ZAI4");
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./environments/environment */ "AytR");




if (_environments_environment__WEBPACK_IMPORTED_MODULE_3__["environment"].production) {
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["enableProdMode"])();
}
Object(_angular_platform_browser_dynamic__WEBPACK_IMPORTED_MODULE_1__["platformBrowserDynamic"])().bootstrapModule(_app_app_module__WEBPACK_IMPORTED_MODULE_2__["AppModule"])
    .catch(err => console.error(err));


/***/ }),

/***/ "zaci":
/*!*******************************************************!*\
  !*** ./src/@vex/components/sidebar/sidebar.module.ts ***!
  \*******************************************************/
/*! exports provided: SidebarModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SidebarModule", function() { return SidebarModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _sidebar_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./sidebar.component */ "og7a");




let SidebarModule = class SidebarModule {
};
SidebarModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"]
        ],
        declarations: [_sidebar_component__WEBPACK_IMPORTED_MODULE_3__["SidebarComponent"]],
        exports: [_sidebar_component__WEBPACK_IMPORTED_MODULE_3__["SidebarComponent"]]
    })
], SidebarModule);



/***/ }),

/***/ "zd1o":
/*!********************************************************************!*\
  !*** ./src/@vex/components/sidenav-item/sidenav-item.component.ts ***!
  \********************************************************************/
/*! exports provided: SidenavItemComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SidenavItemComponent", function() { return SidenavItemComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_sidenav_item_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./sidenav-item.component.html */ "d5u2");
/* harmony import */ var _sidenav_item_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./sidenav-item.component.scss */ "CTrj");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _iconify_icons_ic_twotone_keyboard_arrow_right__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @iconify/icons-ic/twotone-keyboard-arrow-right */ "DzyE");
/* harmony import */ var _iconify_icons_ic_twotone_keyboard_arrow_right__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_keyboard_arrow_right__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var ngx_take_until_destroy__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ngx-take-until-destroy */ "DnKK");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! rxjs/operators */ "kU1M");
/* harmony import */ var _animations_dropdown_animation__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../animations/dropdown.animation */ "T/nk");
/* harmony import */ var _services_navigation_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../services/navigation.service */ "0vMP");










let SidenavItemComponent = class SidenavItemComponent {
    constructor(router, cd, navigationService) {
        this.router = router;
        this.cd = cd;
        this.navigationService = navigationService;
        this.icKeyboardArrowRight = _iconify_icons_ic_twotone_keyboard_arrow_right__WEBPACK_IMPORTED_MODULE_5___default.a;
        this.isLink = this.navigationService.isLink;
        this.isDropdown = this.navigationService.isDropdown;
        this.isSubheading = this.navigationService.isSubheading;
    }
    get levelClass() {
        return `item-level-${this.level}`;
    }
    ngOnInit() {
        this.router.events.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_7__["filter"])(event => event instanceof _angular_router__WEBPACK_IMPORTED_MODULE_4__["NavigationEnd"]), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_7__["filter"])(() => this.isDropdown(this.item)), Object(ngx_take_until_destroy__WEBPACK_IMPORTED_MODULE_6__["untilDestroyed"])(this)).subscribe(() => this.onRouteChange());
        this.navigationService.openChange$.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_7__["filter"])(() => this.isDropdown(this.item)), Object(ngx_take_until_destroy__WEBPACK_IMPORTED_MODULE_6__["untilDestroyed"])(this)).subscribe(item => this.onOpenChange(item));
        if (this.item) {
            const link = this.item;
            this.isActive = link.route === location.pathname;
        }
    }
    ngOnChanges(changes) {
        if (changes && changes.hasOwnProperty('item') && this.isDropdown(this.item)) {
            this.onRouteChange();
        }
    }
    toggleOpen() {
        this.isOpen = !this.isOpen;
        this.navigationService.triggerOpenChange(this.item);
        this.cd.markForCheck();
    }
    onOpenChange(item) {
        if (this.isChildrenOf(this.item, item)) {
            return;
        }
        if (this.hasActiveChilds(this.item)) {
            return;
        }
        if (this.item !== item) {
            this.isOpen = false;
            this.cd.markForCheck();
        }
    }
    onRouteChange() {
        if (this.hasActiveChilds(this.item)) {
            this.isActive = true;
            this.isOpen = true;
            this.navigationService.triggerOpenChange(this.item);
            this.cd.markForCheck();
        }
        else {
            this.isActive = false;
            this.isOpen = false;
            this.navigationService.triggerOpenChange(this.item);
            this.cd.markForCheck();
        }
    }
    isChildrenOf(parent, item) {
        if (parent.children.indexOf(item) !== -1) {
            return true;
        }
        return parent.children
            .filter(child => this.isDropdown(child))
            .some(child => this.isChildrenOf(child, item));
    }
    hasActiveChilds(parent) {
        return parent.children.some(child => {
            if (this.isDropdown(child)) {
                return this.hasActiveChilds(child);
            }
            if (this.isLink(child) && !this.isFunction(child.route)) {
                return this.router.isActive(child.route, false);
            }
        });
    }
    isFunction(prop) {
        return prop instanceof Function;
    }
    ngOnDestroy() { }
};
SidenavItemComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["Router"] },
    { type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ChangeDetectorRef"] },
    { type: _services_navigation_service__WEBPACK_IMPORTED_MODULE_9__["NavigationService"] }
];
SidenavItemComponent.propDecorators = {
    item: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"] }],
    level: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"] }],
    levelClass: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["HostBinding"], args: ['class',] }]
};
SidenavItemComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'vex-sidenav-item',
        template: _raw_loader_sidenav_item_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        animations: [_animations_dropdown_animation__WEBPACK_IMPORTED_MODULE_8__["dropdownAnimation"]],
        changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ChangeDetectionStrategy"].OnPush,
        styles: [_sidenav_item_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], SidenavItemComponent);



/***/ }),

/***/ "zn8P":
/*!******************************************************!*\
  !*** ./$$_lazy_route_resource lazy namespace object ***!
  \******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

function webpackEmptyAsyncContext(req) {
	// Here Promise.resolve().then() is used instead of new Promise() to prevent
	// uncaught exception popping up in devtools
	return Promise.resolve().then(function() {
		var e = new Error("Cannot find module '" + req + "'");
		e.code = 'MODULE_NOT_FOUND';
		throw e;
	});
}
webpackEmptyAsyncContext.keys = function() { return []; };
webpackEmptyAsyncContext.resolve = webpackEmptyAsyncContext;
module.exports = webpackEmptyAsyncContext;
webpackEmptyAsyncContext.id = "zn8P";

/***/ })

},[[0,"runtime","vendor"]]]);
//# sourceMappingURL=main-es2015.js.map