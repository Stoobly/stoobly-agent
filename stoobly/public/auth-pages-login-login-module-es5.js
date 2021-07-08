(function () {
  function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

  function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

  function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

  (window["webpackJsonp"] = window["webpackJsonp"] || []).push([["auth-pages-login-login-module"], {
    /***/
    "Di+n":
    /*!***************************************************************!*\
      !*** ./src/app/modules/auth/pages/login/login.component.scss ***!
      \***************************************************************/

    /*! exports provided: default */

    /***/
    function DiN(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = ".ui.button.google-auth__button {\n  padding: 6px 16px;\n  background: #FFFFFF;\n  box-shadow: 0 0 1px 0 rgba(0, 0, 0, 0.12), 0 1px 1px 0 rgba(0, 0, 0, 0.24);\n  border-radius: 2px;\n  font-size: 16px;\n  line-height: 1.5em;\n  letter-spacing: 0.22px;\n  color: rgba(0, 0, 0, 0.54);\n}\n\n.ui.button.google-auth__button:hover {\n  box-shadow: 0 0 2px 0 rgba(0, 0, 0, 0.12), 0 2px 2px 0 rgba(0, 0, 0, 0.24);\n}\n\n.ui.button.google-auth__button .google-auth__logo {\n  display: inline-block;\n  margin-right: 16px;\n  height: 24px;\n  width: 24px;\n  line-height: 24px;\n  vertical-align: top;\n}\n\n.ui.button.google-auth__button.disabled, .ui.button.google-auth__button:disabled {\n  background: #EEEEEE;\n  box-shadow: 0 0 2px 0 rgba(0, 0, 0, 0.12), 0 2px 2px 0 rgba(0, 0, 0, 0.24);\n}\n\n.link {\n  color: #1976d2;\n}\n\n.link:hover {\n  text-decoration: underline;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uLy4uL2xvZ2luLmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0VBQ0UsaUJBQUE7RUFDQSxtQkFBQTtFQUNBLDBFQUFBO0VBQ0Esa0JBQUE7RUFDQSxlQUFBO0VBQ0Esa0JBQUE7RUFDQSxzQkFBQTtFQUNBLDBCQUFBO0FBQ0Y7O0FBRUE7RUFDRSwwRUFBQTtBQUNGOztBQUVBO0VBQ0UscUJBQUE7RUFDQSxrQkFBQTtFQUNBLFlBQUE7RUFDQSxXQUFBO0VBQ0EsaUJBQUE7RUFDQSxtQkFBQTtBQUNGOztBQUVBO0VBQ0UsbUJBQUE7RUFDQSwwRUFBQTtBQUNGOztBQUVBO0VBQ0UsY0FBQTtBQUNGOztBQUVBO0VBQ0UsMEJBQUE7QUFDRiIsImZpbGUiOiJsb2dpbi5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbIi51aS5idXR0b24uZ29vZ2xlLWF1dGhfX2J1dHRvbiB7XG4gIHBhZGRpbmc6IDZweCAxNnB4O1xuICBiYWNrZ3JvdW5kOiAjRkZGRkZGO1xuICBib3gtc2hhZG93OiAwIDAgMXB4IDAgcmdiYSgwLCAwLCAwLCAwLjEyKSwgMCAxcHggMXB4IDAgcmdiYSgwLCAwLCAwLCAwLjI0KTtcbiAgYm9yZGVyLXJhZGl1czogMnB4O1xuICBmb250LXNpemU6IDE2cHg7XG4gIGxpbmUtaGVpZ2h0OiAxLjVlbTtcbiAgbGV0dGVyLXNwYWNpbmc6IDAuMjJweDtcbiAgY29sb3I6IHJnYmEoMCwgMCwgMCwgMC41NCk7XG59XG5cbi51aS5idXR0b24uZ29vZ2xlLWF1dGhfX2J1dHRvbjpob3ZlciB7XG4gIGJveC1zaGFkb3c6IDAgMCAycHggMCByZ2JhKDAsIDAsIDAsIDAuMTIpLCAwIDJweCAycHggMCByZ2JhKDAsIDAsIDAsIDAuMjQpO1xufVxuXG4udWkuYnV0dG9uLmdvb2dsZS1hdXRoX19idXR0b24gLmdvb2dsZS1hdXRoX19sb2dvIHtcbiAgZGlzcGxheTogaW5saW5lLWJsb2NrO1xuICBtYXJnaW4tcmlnaHQ6IDE2cHg7XG4gIGhlaWdodDogMjRweDtcbiAgd2lkdGg6IDI0cHg7XG4gIGxpbmUtaGVpZ2h0OiAyNHB4O1xuICB2ZXJ0aWNhbC1hbGlnbjogdG9wO1xufVxuXG4udWkuYnV0dG9uLmdvb2dsZS1hdXRoX19idXR0b24uZGlzYWJsZWQsIC51aS5idXR0b24uZ29vZ2xlLWF1dGhfX2J1dHRvbjpkaXNhYmxlZCB7XG4gIGJhY2tncm91bmQ6ICNFRUVFRUU7XG4gIGJveC1zaGFkb3c6IDAgMCAycHggMCByZ2JhKDAsIDAsIDAsIDAuMTIpLCAwIDJweCAycHggMCByZ2JhKDAsIDAsIDAsIDAuMjQpO1xufVxuXG4ubGluayB7XG4gIGNvbG9yOiAjMTk3NmQyO1xufVxuXG4ubGluazpob3ZlciB7XG4gIHRleHQtZGVjb3JhdGlvbjogdW5kZXJsaW5lO1xufSJdfQ== */";
      /***/
    },

    /***/
    "OZYT":
    /*!*****************************************************************************************************!*\
      !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/auth/pages/login/login.component.html ***!
      \*****************************************************************************************************/

    /*! exports provided: default */

    /***/
    function OZYT(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "<div class=\"w-full h-full bg-pattern\" fxLayout=\"column\" fxLayoutAlign=\"center center\">\n  <div @fadeInUp class=\"card overflow-hidden w-full max-w-xs\">\n    <div class=\"p-6 pb-0\" fxLayout=\"column\" fxLayoutAlign=\"center center\">\n      <div class=\"fill-current text-center\">\n        <img class=\"w-16\" src=\"assets/img/demo/logo.svg\">\n      </div>\n    </div>\n\n    <div class=\"text-center mt-4\">\n      <h2 class=\"title m-0\">Welcome Back</h2>\n      <h4 class=\"body-2 text-secondary m-0\">Sign in with your credentials below</h4>\n    </div>\n\n    <div [formGroup]=\"form\" class=\"p-6\" fxLayout=\"column\" fxLayoutGap=\"16px\">\n      <div fxFlex=\"auto\" fxLayout=\"column\">\n        <mat-form-field fxFlex=\"grow\">\n          <mat-label>E-Mail</mat-label>\n          <input formControlName=\"email\" matInput required>\n          <mat-error *ngIf=\"form.get('email').hasError('required')\">We need an email address to log you in</mat-error>\n        </mat-form-field>\n        <mat-form-field fxFlex=\"grow\">\n          <mat-label>Password</mat-label>\n          <input [type]=\"inputType\" formControlName=\"password\" matInput required>\n          <button (click)=\"toggleVisibility()\" mat-icon-button matSuffix matTooltip=\"Toggle Visibility\" type=\"button\">\n            <mat-icon *ngIf=\"visible\" [icIcon]=\"icVisibility\"></mat-icon>\n            <mat-icon *ngIf=\"!visible\" [icIcon]=\"icVisibilityOff\"></mat-icon>\n          </button>\n          <mat-hint>Click the eye to toggle visibility</mat-hint>\n          <mat-error *ngIf=\"form.get('password').hasError('required')\">We need a password to log you in</mat-error>\n        </mat-form-field>\n      </div>\n\n      <div class=\"mb-5\" fxLayout=\"row\" fxLayoutAlign=\"space-between center\">\n        <mat-checkbox class=\"caption\" color=\"primary\">Remember Me</mat-checkbox>\n        <a [routerLink]=\"['/forgot-password']\" class=\"caption\">Forgot Password?</a>\n      </div>\n\n      <button (click)=\"login()\" color=\"primary\" mat-raised-button type=\"button\">\n        SIGN IN\n      </button>\n\n      <p class=\"text-secondary text-center\">\n        OR\n      </p>\n\n      <button class=\"ui button google-auth__button\" (click)=\"loginWithGoogle()\">\n        <img class=\"google-auth__logo\" src=\"https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg\" />\n        Sign in with Google\n      </button>\n\n      <p class=\"mt-5 text-center\">\n        <span class=\"text-secondary\">Don't have an account?</span><br/>\n        <a class=\"link\" [routerLink]=\"['/register']\">Click here to create one</a>\n      </p>\n    </div>\n  </div>\n</div>\n";
      /***/
    },

    /***/
    "Vuo0":
    /*!******************************************************************!*\
      !*** ./src/app/modules/auth/pages/login/login-routing.module.ts ***!
      \******************************************************************/

    /*! exports provided: LoginRoutingModule */

    /***/
    function Vuo0(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "LoginRoutingModule", function () {
        return LoginRoutingModule;
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


      var _login_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! ./login.component */
      "wLjx");

      var routes = [{
        path: '',
        component: _login_component__WEBPACK_IMPORTED_MODULE_3__["LoginComponent"]
      }];

      var LoginRoutingModule = function LoginRoutingModule() {
        _classCallCheck(this, LoginRoutingModule);
      };

      LoginRoutingModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]]
      })], LoginRoutingModule);
      /***/
    },

    /***/
    "ZFij":
    /*!**********************************************************!*\
      !*** ./src/app/modules/auth/pages/login/login.module.ts ***!
      \**********************************************************/

    /*! exports provided: LoginModule */

    /***/
    function ZFij(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "LoginModule", function () {
        return LoginModule;
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


      var _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/material/checkbox */
      "pMoy");
      /* harmony import */


      var _angular_material_icon__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @angular/material/icon */
      "Tj54");
      /* harmony import */


      var _angular_material_input__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @angular/material/input */
      "e6WT");
      /* harmony import */


      var _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @angular/material/snack-bar */
      "zHaW");
      /* harmony import */


      var _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @angular/material/tooltip */
      "ZFy/");
      /* harmony import */


      var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @visurel/iconify-angular */
      "l+Q0");
      /* harmony import */


      var _login_routing_module__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! ./login-routing.module */
      "Vuo0");
      /* harmony import */


      var _login_component__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! ./login.component */
      "wLjx");

      var LoginModule = function LoginModule() {
        _classCallCheck(this, LoginModule);
      };

      LoginModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_login_component__WEBPACK_IMPORTED_MODULE_13__["LoginComponent"]],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _login_routing_module__WEBPACK_IMPORTED_MODULE_12__["LoginRoutingModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"], _angular_material_input__WEBPACK_IMPORTED_MODULE_8__["MatInputModule"], _angular_material_icon__WEBPACK_IMPORTED_MODULE_7__["MatIconModule"], _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_9__["MatSnackBarModule"], _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_11__["IconModule"], _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_10__["MatTooltipModule"], _angular_material_button__WEBPACK_IMPORTED_MODULE_5__["MatButtonModule"], _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_6__["MatCheckboxModule"]]
      })], LoginModule);
      /***/
    },

    /***/
    "wLjx":
    /*!*************************************************************!*\
      !*** ./src/app/modules/auth/pages/login/login.component.ts ***!
      \*************************************************************/

    /*! exports provided: LoginComponent */

    /***/
    function wLjx(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "LoginComponent", function () {
        return LoginComponent;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _raw_loader_login_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! raw-loader!./login.component.html */
      "OZYT");
      /* harmony import */


      var _login_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! ./login.component.scss */
      "Di+n");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/forms */
      "s7LF");
      /* harmony import */


      var _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/material/snack-bar */
      "zHaW");
      /* harmony import */


      var _angular_router__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/router */
      "iInd");
      /* harmony import */


      var angular_token__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! angular-token */
      "hU4o");
      /* harmony import */


      var _iconify_icons_ic_twotone_visibility__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-visibility */
      "uQ9D");
      /* harmony import */


      var _iconify_icons_ic_twotone_visibility__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_visibility__WEBPACK_IMPORTED_MODULE_8__);
      /* harmony import */


      var _iconify_icons_ic_twotone_visibility_off__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-visibility-off */
      "k1zR");
      /* harmony import */


      var _iconify_icons_ic_twotone_visibility_off__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_visibility_off__WEBPACK_IMPORTED_MODULE_9__);
      /* harmony import */


      var _vex_animations_fade_in_up_animation__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @vex/animations/fade-in-up.animation */
      "y3Ys");
      /* harmony import */


      var _core_http_omniauth_callbacks_api_service__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @core/http/omniauth-callbacks-api.service */
      "RdP6");
      /* harmony import */


      var _environments_environment__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @environments/environment */
      "AytR");

      var LoginComponent = /*#__PURE__*/function () {
        function LoginComponent(router, fb, cd, snackbar, tokenService, omniauthCallbacksApi) {
          _classCallCheck(this, LoginComponent);

          this.router = router;
          this.fb = fb;
          this.cd = cd;
          this.snackbar = snackbar;
          this.tokenService = tokenService;
          this.omniauthCallbacksApi = omniauthCallbacksApi;
          this.inputType = 'password';
          this.visible = false;
          this.icVisibility = _iconify_icons_ic_twotone_visibility__WEBPACK_IMPORTED_MODULE_8___default.a;
          this.icVisibilityOff = _iconify_icons_ic_twotone_visibility_off__WEBPACK_IMPORTED_MODULE_9___default.a;
        }

        _createClass(LoginComponent, [{
          key: "ngOnInit",
          value: function ngOnInit() {
            this.form = this.fb.group({
              email: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required],
              password: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required]
            });
          }
        }, {
          key: "loginWithGoogle",
          value: function loginWithGoogle() {
            var _this = this;

            this.tokenService.tokenOptions.oAuthBase = _environments_environment__WEBPACK_IMPORTED_MODULE_12__["environment"].apiUrl; // this.tokenService.tokenOptions.oAuthWindowType = 'sameWindow';

            this.tokenService.signInOAuth('google_oauth2').subscribe(function (res) {
              _this.router.navigate(['/']);
            }, function (error) {});
          }
        }, {
          key: "login",
          value: function login() {
            var _this2 = this;

            var form = this.form.value;
            this.tokenService.signIn({
              login: form.email,
              password: form.password
            }).subscribe(function (res) {
              _this2.router.navigate(['/']);
            }, function (error) {
              if (error.status === 401) {
                _this2.snackbar.open('Incorrect username or password', 'close', {
                  duration: 2000
                });
              } else {
                _this2.snackbar.open('An unexpected error occurred, please try again later', 'close', {
                  duration: 2000
                });
              }
            });
          }
        }, {
          key: "toggleVisibility",
          value: function toggleVisibility() {
            if (this.visible) {
              this.inputType = 'password';
              this.visible = false;
              this.cd.markForCheck();
            } else {
              this.inputType = 'text';
              this.visible = true;
              this.cd.markForCheck();
            }
          }
        }]);

        return LoginComponent;
      }();

      LoginComponent.ctorParameters = function () {
        return [{
          type: _angular_router__WEBPACK_IMPORTED_MODULE_6__["Router"]
        }, {
          type: _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormBuilder"]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ChangeDetectorRef"]
        }, {
          type: _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_5__["MatSnackBar"]
        }, {
          type: angular_token__WEBPACK_IMPORTED_MODULE_7__["AngularTokenService"]
        }, {
          type: _core_http_omniauth_callbacks_api_service__WEBPACK_IMPORTED_MODULE_11__["OmniauthCallbacksApi"]
        }];
      };

      LoginComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'vex-login',
        template: _raw_loader_login_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ChangeDetectionStrategy"].OnPush,
        animations: [_vex_animations_fade_in_up_animation__WEBPACK_IMPORTED_MODULE_10__["fadeInUp400ms"]],
        styles: [_login_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
      })], LoginComponent);
      /***/
    }
  }]);
})();
//# sourceMappingURL=auth-pages-login-login-module-es5.js.map