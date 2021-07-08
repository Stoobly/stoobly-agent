(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["auth-pages-register-register-module"],{

/***/ "1TiS":
/*!****************************************************************!*\
  !*** ./src/app/modules/auth/pages/register/register.module.ts ***!
  \****************************************************************/
/*! exports provided: RegisterModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RegisterModule", function() { return RegisterModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ "s7LF");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/checkbox */ "pMoy");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/material/input */ "e6WT");
/* harmony import */ var _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/material/tooltip */ "ZFy/");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _register_routing_module__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./register-routing.module */ "t1MT");
/* harmony import */ var _register_component__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./register.component */ "IKBy");













let RegisterModule = class RegisterModule {
};
RegisterModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_register_component__WEBPACK_IMPORTED_MODULE_12__["RegisterComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _register_routing_module__WEBPACK_IMPORTED_MODULE_11__["RegisterRoutingModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"],
            _angular_material_input__WEBPACK_IMPORTED_MODULE_8__["MatInputModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_7__["MatIconModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_5__["MatButtonModule"],
            _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_9__["MatTooltipModule"],
            _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_6__["MatCheckboxModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_10__["IconModule"],
        ],
    })
], RegisterModule);



/***/ }),

/***/ "6y3L":
/*!*********************************************************************!*\
  !*** ./src/app/modules/auth/pages/register/register.component.scss ***!
  \*********************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (".link {\n  color: #1976d2;\n}\n\n.link:hover {\n  text-decoration: underline;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uLy4uL3JlZ2lzdGVyLmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0VBQ0UsY0FBQTtBQUNGOztBQUVBO0VBQ0UsMEJBQUE7QUFDRiIsImZpbGUiOiJyZWdpc3Rlci5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbIi5saW5rIHtcbiAgY29sb3I6ICMxOTc2ZDI7XG59XG5cbi5saW5rOmhvdmVyIHtcbiAgdGV4dC1kZWNvcmF0aW9uOiB1bmRlcmxpbmU7XG59Il19 */");

/***/ }),

/***/ "IKBy":
/*!*******************************************************************!*\
  !*** ./src/app/modules/auth/pages/register/register.component.ts ***!
  \*******************************************************************/
/*! exports provided: RegisterComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RegisterComponent", function() { return RegisterComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_register_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./register.component.html */ "oFPd");
/* harmony import */ var _register_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./register.component.scss */ "6y3L");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ "s7LF");
/* harmony import */ var _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/snack-bar */ "zHaW");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _iconify_icons_ic_twotone_visibility__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @iconify/icons-ic/twotone-visibility */ "uQ9D");
/* harmony import */ var _iconify_icons_ic_twotone_visibility__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_visibility__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _iconify_icons_ic_twotone_visibility_off__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @iconify/icons-ic/twotone-visibility-off */ "k1zR");
/* harmony import */ var _iconify_icons_ic_twotone_visibility_off__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_visibility_off__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var angular_token__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! angular-token */ "hU4o");
/* harmony import */ var _vex_animations_fade_in_up_animation__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @vex/animations/fade-in-up.animation */ "y3Ys");











let RegisterComponent = class RegisterComponent {
    constructor(router, fb, cd, snackBar, tokenService) {
        this.router = router;
        this.fb = fb;
        this.cd = cd;
        this.snackBar = snackBar;
        this.tokenService = tokenService;
        this.inputType = 'password';
        this.visible = false;
        this.icVisibility = _iconify_icons_ic_twotone_visibility__WEBPACK_IMPORTED_MODULE_7___default.a;
        this.icVisibilityOff = _iconify_icons_ic_twotone_visibility_off__WEBPACK_IMPORTED_MODULE_8___default.a;
    }
    ngOnInit() {
        this.form = this.fb.group({
            name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required],
            email: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required],
            password: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required],
            passwordConfirm: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required],
        });
    }
    register() {
        const form = this.form.value;
        this.tokenService.registerAccount({
            name: form.name,
            login: form.email,
            password: form.password,
            passwordConfirmation: form.passwordConfirmation,
        }).subscribe(res => {
            this.router.navigate(['/']);
        }, res => {
            const { error: { errors: { full_messages } } } = res;
            const message = full_messages.join('\n');
            this.snackBar.open(message, 'Close', {
                duration: 5000,
            });
        });
    } // register
    toggleVisibility() {
        if (this.visible) {
            this.inputType = 'password';
            this.visible = false;
            this.cd.markForCheck();
        }
        else {
            this.inputType = 'text';
            this.visible = true;
            this.cd.markForCheck();
        }
    }
};
RegisterComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_6__["Router"] },
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormBuilder"] },
    { type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ChangeDetectorRef"] },
    { type: _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_5__["MatSnackBar"] },
    { type: angular_token__WEBPACK_IMPORTED_MODULE_9__["AngularTokenService"] }
];
RegisterComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'vex-register',
        template: _raw_loader_register_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        animations: [
            _vex_animations_fade_in_up_animation__WEBPACK_IMPORTED_MODULE_10__["fadeInUp400ms"],
        ],
        styles: [_register_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], RegisterComponent);



/***/ }),

/***/ "oFPd":
/*!***********************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/auth/pages/register/register.component.html ***!
  \***********************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div class=\"w-full h-full bg-pattern\" fxLayout=\"column\" fxLayoutAlign=\"center center\">\n  <div @fadeInUp class=\"card overflow-hidden w-full max-w-xs\">\n    <div class=\"p-6 pb-0\" fxLayout=\"column\" fxLayoutAlign=\"center center\">\n      <div class=\"fill-current text-center\">\n        <img class=\"w-16\" src=\"assets/img/demo/logo.svg\">\n      </div>\n    </div>\n\n    <div class=\"text-center mt-4\">\n      <h2 class=\"title m-0\">Register an Account</h2>\n      <h4 class=\"body-2 text-secondary m-0\">Simply fill out the form below</h4>\n    </div>\n\n    <div [formGroup]=\"form\" class=\"p-6\" fxLayout=\"column\" fxLayoutGap=\"16px\">\n      <div fxFlex=\"auto\" fxLayout=\"column\">\n        <mat-form-field fxFlex=\"grow\">\n          <mat-label>Name</mat-label>\n          <input formControlName=\"name\" matInput required>\n        </mat-form-field>\n\n        <mat-form-field fxFlex=\"grow\">\n          <mat-label>E-Mail</mat-label>\n          <input formControlName=\"email\" matInput required>\n        </mat-form-field>\n\n        <mat-form-field fxFlex=\"grow\">\n          <mat-label>Password</mat-label>\n          <input [type]=\"inputType\" formControlName=\"password\" matInput required>\n          <button (click)=\"toggleVisibility()\" mat-icon-button matSuffix matTooltip=\"Toggle Visibility\" type=\"button\">\n            <mat-icon *ngIf=\"visible\" [icIcon]=\"icVisibility\"></mat-icon>\n            <mat-icon *ngIf=\"!visible\" [icIcon]=\"icVisibilityOff\"></mat-icon>\n          </button>\n          <mat-hint>Click the eye to toggle visibility</mat-hint>\n        </mat-form-field>\n\n        <mat-form-field fxFlex=\"grow\">\n          <mat-label>Password (Confirm)</mat-label>\n          <input [type]=\"inputType\" formControlName=\"passwordConfirm\" matInput required>\n          <button (click)=\"toggleVisibility()\" mat-icon-button matSuffix matTooltip=\"Toggle Visibility\" type=\"button\">\n            <mat-icon *ngIf=\"visible\" [icIcon]=\"icVisibility\"></mat-icon>\n            <mat-icon *ngIf=\"!visible\" [icIcon]=\"icVisibilityOff\"></mat-icon>\n          </button>\n          <mat-hint>Please repeat your password from above</mat-hint>\n        </mat-form-field>\n      </div>\n\n      <div fxLayout=\"row\" fxLayoutAlign=\"center center\">\n        <mat-checkbox class=\"caption\">I accept the <a>terms and conditions.</a></mat-checkbox>\n      </div>\n      <button (click)=\"register()\" color=\"primary\" mat-raised-button type=\"button\">\n        CREATE ACCOUNT\n      </button>\n      <p class=\"text-center\">\n        <span class=\"text-secondary\">Already have an account?</span><br/>\n        <a class=\"link\" [routerLink]=\"['/login']\">Sign in here</a>\n      </p>\n    </div>\n  </div>\n</div>\n");

/***/ }),

/***/ "t1MT":
/*!************************************************************************!*\
  !*** ./src/app/modules/auth/pages/register/register-routing.module.ts ***!
  \************************************************************************/
/*! exports provided: RegisterRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RegisterRoutingModule", function() { return RegisterRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _register_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./register.component */ "IKBy");




const routes = [
    {
        path: '',
        component: _register_component__WEBPACK_IMPORTED_MODULE_3__["RegisterComponent"],
    },
];
let RegisterRoutingModule = class RegisterRoutingModule {
};
RegisterRoutingModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
    })
], RegisterRoutingModule);



/***/ })

}]);
//# sourceMappingURL=auth-pages-register-register-module-es2015.js.map