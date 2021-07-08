(function () {
  function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

  function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

  function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

  (window["webpackJsonp"] = window["webpackJsonp"] || []).push([["auth-pages-forgot-password-forgot-password-module"], {
    /***/
    "0fkF":
    /*!*************************************************************************************************************************!*\
      !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/auth/pages/forgot-password/forgot-password.component.html ***!
      \*************************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function fkF(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "<div class=\"bg-pattern w-full h-full\" fxLayout=\"column\" fxLayoutAlign=\"center center\">\n  <div [@fadeInUp] class=\"card overflow-hidden w-full max-w-xs\">\n    <div class=\"p-6 pb-0\" fxLayout=\"column\" fxLayoutAlign=\"center center\">\n      <div class=\"fill-current text-center\">\n        <img class=\"w-16\" src=\"assets/img/demo/logo.svg\">\n      </div>\n    </div>\n\n    <div class=\"text-center mt-4\">\n      <h2 class=\"title m-0\">Reset Password</h2>\n      <h4 class=\"body-2 text-secondary m-0\">Enter your email for password recovery.</h4>\n    </div>\n\n    <div [formGroup]=\"form\" class=\"p-6 flex flex-col\">\n      <mat-form-field>\n        <mat-label>E-Mail</mat-label>\n\n        <mat-icon [icIcon]=\"icMail\" class=\"mr-2\" matPrefix></mat-icon>\n        <input formControlName=\"email\" matInput required>\n        <mat-error *ngIf=\"form.get('email').hasError('required')\">\n          We can't recover your password, without your email.\n        </mat-error>\n      </mat-form-field>\n\n      <button (click)=\"reset()\" class=\"mt-2\" color=\"primary\" mat-raised-button type=\"button\">\n        SEND RECOVERY LINK\n      </button>\n    </div>\n  </div>\n</div>\n";
      /***/
    },

    /***/
    "6qw8":
    /*!********************************************************!*\
      !*** ./node_modules/@iconify/icons-ic/twotone-mail.js ***!
      \********************************************************/

    /*! no static exports found */

    /***/
    function qw8(module, exports) {
      var data = {
        "body": "<path opacity=\".3\" d=\"M20 6H4l8 4.99zM4 8v10h16V8l-8 5z\" fill=\"currentColor\"/><path d=\"M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 2l-8 4.99L4 6h16zm0 12H4V8l8 5l8-5v10z\" fill=\"currentColor\"/>",
        "width": 24,
        "height": 24
      };
      exports.__esModule = true;
      exports["default"] = data;
      /***/
    },

    /***/
    "F6xA":
    /*!**************************************************************************************!*\
      !*** ./src/app/modules/auth/pages/forgot-password/forgot-password-routing.module.ts ***!
      \**************************************************************************************/

    /*! exports provided: ForgotPasswordRoutingModule */

    /***/
    function F6xA(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ForgotPasswordRoutingModule", function () {
        return ForgotPasswordRoutingModule;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @angular/router */
      "iInd");
      /* harmony import */


      var _forgot_password_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! ./forgot-password.component */
      "JOb8");

      var routes = [{
        path: '',
        component: _forgot_password_component__WEBPACK_IMPORTED_MODULE_3__["ForgotPasswordComponent"]
      }];

      var ForgotPasswordRoutingModule = function ForgotPasswordRoutingModule() {
        _classCallCheck(this, ForgotPasswordRoutingModule);
      };

      ForgotPasswordRoutingModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]]
      })], ForgotPasswordRoutingModule);
      /***/
    },

    /***/
    "JOb8":
    /*!*********************************************************************************!*\
      !*** ./src/app/modules/auth/pages/forgot-password/forgot-password.component.ts ***!
      \*********************************************************************************/

    /*! exports provided: ForgotPasswordComponent */

    /***/
    function JOb8(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ForgotPasswordComponent", function () {
        return ForgotPasswordComponent;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _raw_loader_forgot_password_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! raw-loader!./forgot-password.component.html */
      "0fkF");
      /* harmony import */


      var _forgot_password_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! ./forgot-password.component.scss */
      "grGc");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/forms */
      "s7LF");
      /* harmony import */


      var _angular_router__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/router */
      "iInd");
      /* harmony import */


      var _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-mail */
      "6qw8");
      /* harmony import */


      var _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_6__);
      /* harmony import */


      var angular_token__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! angular-token */
      "hU4o");
      /* harmony import */


      var _vex_animations_fade_in_up_animation__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @vex/animations/fade-in-up.animation */
      "y3Ys");

      var ForgotPasswordComponent = /*#__PURE__*/function () {
        function ForgotPasswordComponent(router, fb, tokenService) {
          _classCallCheck(this, ForgotPasswordComponent);

          this.router = router;
          this.fb = fb;
          this.tokenService = tokenService;
          this.form = this.fb.group({
            email: [null, _angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required]
          });
          this.icMail = _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_6___default.a;
        }

        _createClass(ForgotPasswordComponent, [{
          key: "ngOnInit",
          value: function ngOnInit() {}
        }, {
          key: "reset",
          value: function reset() {
            var _this = this;

            var form = this.form.value;
            this.tokenService.resetPassword({
              login: form.email
            }).subscribe(function (res) {
              _this.router.navigate(['/']);
            }, function (error) {
              console.log(error);
            });
          }
        }]);

        return ForgotPasswordComponent;
      }();

      ForgotPasswordComponent.ctorParameters = function () {
        return [{
          type: _angular_router__WEBPACK_IMPORTED_MODULE_5__["Router"]
        }, {
          type: _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormBuilder"]
        }, {
          type: angular_token__WEBPACK_IMPORTED_MODULE_7__["AngularTokenService"]
        }];
      };

      ForgotPasswordComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'vex-forgot-password',
        template: _raw_loader_forgot_password_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        animations: [_vex_animations_fade_in_up_animation__WEBPACK_IMPORTED_MODULE_8__["fadeInUp400ms"]],
        styles: [_forgot_password_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
      })], ForgotPasswordComponent);
      /***/
    },

    /***/
    "grGc":
    /*!***********************************************************************************!*\
      !*** ./src/app/modules/auth/pages/forgot-password/forgot-password.component.scss ***!
      \***********************************************************************************/

    /*! exports provided: default */

    /***/
    function grGc(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJmb3Jnb3QtcGFzc3dvcmQuY29tcG9uZW50LnNjc3MifQ== */";
      /***/
    },

    /***/
    "iXA7":
    /*!******************************************************************************!*\
      !*** ./src/app/modules/auth/pages/forgot-password/forgot-password.module.ts ***!
      \******************************************************************************/

    /*! exports provided: ForgotPasswordModule */

    /***/
    function iXA7(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ForgotPasswordModule", function () {
        return ForgotPasswordModule;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! @angular/common */
      "SVse");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/flex-layout */
      "u9T3");
      /* harmony import */


      var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/forms */
      "s7LF");
      /* harmony import */


      var _angular_material_button__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/material/button */
      "Dxy4");
      /* harmony import */


      var _angular_material_icon__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/material/icon */
      "Tj54");
      /* harmony import */


      var _angular_material_input__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @angular/material/input */
      "e6WT");
      /* harmony import */


      var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @visurel/iconify-angular */
      "l+Q0");
      /* harmony import */


      var _forgot_password_routing_module__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! ./forgot-password-routing.module */
      "F6xA");
      /* harmony import */


      var _forgot_password_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! ./forgot-password.component */
      "JOb8");

      var ForgotPasswordModule = function ForgotPasswordModule() {
        _classCallCheck(this, ForgotPasswordModule);
      };

      ForgotPasswordModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_forgot_password_component__WEBPACK_IMPORTED_MODULE_10__["ForgotPasswordComponent"]],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _forgot_password_routing_module__WEBPACK_IMPORTED_MODULE_9__["ForgotPasswordRoutingModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"], _angular_material_input__WEBPACK_IMPORTED_MODULE_7__["MatInputModule"], _angular_material_button__WEBPACK_IMPORTED_MODULE_5__["MatButtonModule"], _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_8__["IconModule"], _angular_material_icon__WEBPACK_IMPORTED_MODULE_6__["MatIconModule"]]
      })], ForgotPasswordModule);
      /***/
    },

    /***/
    "y3Ys":
    /*!*****************************************************!*\
      !*** ./src/@vex/animations/fade-in-up.animation.ts ***!
      \*****************************************************/

    /*! exports provided: fadeInUpAnimation, fadeInUp400ms */

    /***/
    function y3Ys(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "fadeInUpAnimation", function () {
        return fadeInUpAnimation;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "fadeInUp400ms", function () {
        return fadeInUp400ms;
      });
      /* harmony import */


      var _angular_animations__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! @angular/animations */
      "GS7A");

      function fadeInUpAnimation(duration) {
        return Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["trigger"])('fadeInUp', [Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["transition"])(':enter', [Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["style"])({
          transform: 'translateY(20px)',
          opacity: 0
        }), Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["animate"])("".concat(duration, "ms cubic-bezier(0.35, 0, 0.25, 1)"), Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["style"])({
          transform: 'translateY(0)',
          opacity: 1
        }))])]);
      }

      var fadeInUp400ms = fadeInUpAnimation(400);
      /***/
    }
  }]);
})();
//# sourceMappingURL=auth-pages-forgot-password-forgot-password-module-es5.js.map