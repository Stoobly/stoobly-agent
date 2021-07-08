(function () {
  function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

  function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }

  function _createSuper(Derived) { var hasNativeReflectConstruct = _isNativeReflectConstruct(); return function _createSuperInternal() { var Super = _getPrototypeOf(Derived), result; if (hasNativeReflectConstruct) { var NewTarget = _getPrototypeOf(this).constructor; result = Reflect.construct(Super, arguments, NewTarget); } else { result = Super.apply(this, arguments); } return _possibleConstructorReturn(this, result); }; }

  function _possibleConstructorReturn(self, call) { if (call && (typeof call === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

  function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

  function _isNativeReflectConstruct() { if (typeof Reflect === "undefined" || !Reflect.construct) return false; if (Reflect.construct.sham) return false; if (typeof Proxy === "function") return true; try { Date.prototype.toString.call(Reflect.construct(Date, [], function () {})); return true; } catch (e) { return false; } }

  function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

  function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

  function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

  function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

  (window["webpackJsonp"] = window["webpackJsonp"] || []).push([["subscriptions-pages-buy-buy-module"], {
    /***/
    "5B4W":
    /*!******************************************************************************!*\
      !*** ./src/@vex/components/secondary-toolbar/secondary-toolbar.component.ts ***!
      \******************************************************************************/

    /*! exports provided: SecondaryToolbarComponent */

    /***/
    function B4W(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "SecondaryToolbarComponent", function () {
        return SecondaryToolbarComponent;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _raw_loader_secondary_toolbar_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! raw-loader!./secondary-toolbar.component.html */
      "a3I5");
      /* harmony import */


      var _secondary_toolbar_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! ./secondary-toolbar.component.scss */
      "treR");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! rxjs/operators */
      "kU1M");
      /* harmony import */


      var _services_config_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! ../../services/config.service */
      "lC2v");

      var SecondaryToolbarComponent = /*#__PURE__*/function () {
        function SecondaryToolbarComponent(configService) {
          _classCallCheck(this, SecondaryToolbarComponent);

          this.configService = configService;
          this.fixed$ = this.configService.config$.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["map"])(function (config) {
            return config.toolbar.fixed;
          }));
        }

        _createClass(SecondaryToolbarComponent, [{
          key: "ngOnInit",
          value: function ngOnInit() {}
        }]);

        return SecondaryToolbarComponent;
      }();

      SecondaryToolbarComponent.ctorParameters = function () {
        return [{
          type: _services_config_service__WEBPACK_IMPORTED_MODULE_5__["ConfigService"]
        }];
      };

      SecondaryToolbarComponent.propDecorators = {
        current: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"]
        }],
        crumbs: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"]
        }]
      };
      SecondaryToolbarComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'vex-secondary-toolbar',
        template: _raw_loader_secondary_toolbar_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_secondary_toolbar_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
      })], SecondaryToolbarComponent);
      /***/
    },

    /***/
    "6hwn":
    /*!**********************************************************************************************************!*\
      !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/subscriptions/pages/buy/buy.component.html ***!
      \**********************************************************************************************************/

    /*! exports provided: default */

    /***/
    function hwn(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "<vex-secondary-toolbar \r\n  current=\"Update Subscription\"\r\n>\r\n</vex-secondary-toolbar>\r\n\r\n<div [@stagger]=\"true\"\r\n     class=\"p-gutter\"\r\n     vexContainer\r\n     fxLayout=\"row\"\r\n     fxLayoutGap=\"20px\">\r\n\r\n  <div @fadeInUp class=\"p-6\"\r\n       fxFlex=\"40\"\r\n       fxLayout=\"column\"\r\n       fxLayoutAlign=\"start center\">\r\n\r\n    <div class=\"border-b mb-5\" fxLayout=\"column\" fxLayoutAlign=\"start center\">\r\n      <h4>CURRENT PLAN</h4>\r\n      <h2 class=\"headline mt-5 text-secondary\">{{ subscription.plan.name }}</h2>\r\n      <h4 class=\"mb-5 text-secondary\">{{ subscription.plan.description }}</h4>\r\n      <div class=\"mb-10\">\r\n        ${{ subscription.plan.chargeAmount }} per user/month\r\n      </div>\r\n    </div>\r\n\r\n    <h4 class=\"mt-5\">NEW PLAN</h4>\r\n\r\n    <!-- <div [style.background-color]=\"theme.colors.primary['500']\"\r\n         class=\"inline-block p-6 rounded-full text-primary-500 mx-auto mt-5\"\r\n         fxLayout=\"row\"\r\n         fxLayoutAlign=\"center center\">\r\n      <ic-icon [icon]=\"icons.icBeenhere\" size=\"48px\"></ic-icon>\r\n    </div> -->\r\n\r\n    <h2 class=\"headline mt-5 text-secondary\">{{ plan.name }}</h2>\r\n    <h4 class=\"mb-5 text-secondary\">{{ plan.description }}</h4>\r\n    <div>\r\n      ${{ plan.chargeAmount }} per user/month\r\n    </div>\r\n  </div>\r\n\r\n  <div fxLayout=\"row\"\r\n       fxLayout.lt-md=\"column\"\r\n       fxLayoutGap=\"20px\"\r\n       fxFlex\r\n       [formGroup]=\"form\">\r\n\r\n    <div @fadeInUp class=\"card\" fxFlex=\"auto\">\r\n      <div class=\"px-6\">\r\n        <div class=\"py-4 border-b\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\r\n          <h2 class=\"title m-0\">Update Summary</h2>\r\n        </div>\r\n\r\n        <div class=\"py-4\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\r\n          New monthly total\r\n        </div>\r\n\r\n        <h3 class=\"display-1 font-bold\" fxLayout=\"row\"  fxLayoutAlign=\"start center\">\r\n          <span class=\"text-secondary headline align-top\">$</span>{{ plan.chargeAmount }}\r\n        </h3>\r\n\r\n        <div class=\"py-4\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\r\n          Due today\r\n        </div>\r\n\r\n        <div class=\"display-1 font-bold\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\r\n          <span class=\"text-secondary headline align-top\">$</span>{{ plan.chargeAmount }}\r\n        </div>\r\n      </div>\r\n\r\n      <div \r\n        *ngIf=\"paymentMethods.length\"\r\n        class=\"px-6 py-4\"\r\n      >\r\n        <payment-methods-list\r\n          [enableCreateCard]=\"true\"\r\n          [enableSetDefault]=\"true\"\r\n          [(paymentMethods)]=\"paymentMethods\" \r\n        >\r\n        </payment-methods-list>\r\n      </div>\r\n\r\n      <div *ngIf=\"!paymentMethods.length\" class=\"px-6 py-4\">\r\n        <div class=\"py-4 border-b\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\r\n          <h2 class=\"title m-0\">Card Information</h2>\r\n        </div>\r\n\r\n        <div class=\"mt-4\" fxLayout=\"column\">\r\n          <mat-form-field>\r\n            <mat-label>Name on card</mat-label>\r\n            <input matInput required formControlName=\"cardName\">\r\n          </mat-form-field>\r\n\r\n          <mat-form-field>\r\n            <mat-label>Email</mat-label>\r\n            <input matInput required formControlName=\"email\">\r\n          </mat-form-field>\r\n\r\n          <!-- <mat-form-field>\r\n            <mat-label>Card Number</mat-label>\r\n            <input matInput required formControlName=\"cardNumber\" ccNumber type=\"tel\" autocomplete=\"cc-number\">\r\n          </mat-form-field> -->\r\n\r\n          <ngx-stripe-card class=\"border-b\" [options]=\"cardOptions\" [elementsOptions]=\"elementsOptions\"></ngx-stripe-card>\r\n      </div>\r\n    </div>\r\n\r\n    <div class=\"px-6\" fxLayout=\"column\">\r\n      <div class=\"py-4\" fxLayout=\"row\" fxLayoutAlign=\"end center\" fxLayoutGap=\"8px\">\r\n        <button color=\"primary\" mat-raised-button type=\"button\" (click)=\"purchase()\">SUBMIT</button>\r\n        <button mat-button type=\"button\" (click)=\"cancel()\">CANCEL</button>\r\n      </div>\r\n    </div>\r\n</div>\r\n";
      /***/
    },

    /***/
    "Abzj":
    /*!***************************************************************************!*\
      !*** ./src/@vex/components/secondary-toolbar/secondary-toolbar.module.ts ***!
      \***************************************************************************/

    /*! exports provided: SecondaryToolbarModule */

    /***/
    function Abzj(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "SecondaryToolbarModule", function () {
        return SecondaryToolbarModule;
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


      var _angular_material_button__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/material/button */
      "Dxy4");
      /* harmony import */


      var _angular_material_icon__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/material/icon */
      "Tj54");
      /* harmony import */


      var _angular_router__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/router */
      "iInd");
      /* harmony import */


      var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @visurel/iconify-angular */
      "l+Q0");
      /* harmony import */


      var _directives_container_container_module__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! ../../directives/container/container.module */
      "68Yx");
      /* harmony import */


      var _breadcrumbs_breadcrumbs_module__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! ../breadcrumbs/breadcrumbs.module */
      "J0XA");
      /* harmony import */


      var _secondary_toolbar_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! ./secondary-toolbar.component */
      "5B4W");

      var SecondaryToolbarModule = function SecondaryToolbarModule() {
        _classCallCheck(this, SecondaryToolbarModule);
      };

      SecondaryToolbarModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_secondary_toolbar_component__WEBPACK_IMPORTED_MODULE_10__["SecondaryToolbarComponent"]],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"], _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_7__["IconModule"], _angular_router__WEBPACK_IMPORTED_MODULE_6__["RouterModule"], _angular_material_button__WEBPACK_IMPORTED_MODULE_4__["MatButtonModule"], _angular_material_icon__WEBPACK_IMPORTED_MODULE_5__["MatIconModule"], _breadcrumbs_breadcrumbs_module__WEBPACK_IMPORTED_MODULE_9__["BreadcrumbsModule"], _directives_container_container_module__WEBPACK_IMPORTED_MODULE_8__["ContainerModule"]],
        exports: [_secondary_toolbar_component__WEBPACK_IMPORTED_MODULE_10__["SecondaryToolbarComponent"]]
      })], SecondaryToolbarModule);
      /***/
    },

    /***/
    "FI9y":
    /*!***************************************************************!*\
      !*** ./src/app/modules/subscriptions/pages/buy/buy.module.ts ***!
      \***************************************************************/

    /*! exports provided: BuyModule */

    /***/
    function FI9y(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "BuyModule", function () {
        return BuyModule;
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


      var _angular_material_autocomplete__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/material/autocomplete */
      "vrAh");
      /* harmony import */


      var _angular_material_button__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/material/button */
      "Dxy4");
      /* harmony import */


      var _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @angular/material/checkbox */
      "pMoy");
      /* harmony import */


      var _angular_material_core__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @angular/material/core */
      "UhP/");
      /* harmony import */


      var _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @angular/material/datepicker */
      "TN/R");
      /* harmony import */


      var _angular_material_icon__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @angular/material/icon */
      "Tj54");
      /* harmony import */


      var _angular_material_input__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @angular/material/input */
      "e6WT");
      /* harmony import */


      var _angular_material_radio__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @angular/material/radio */
      "zQhy");
      /* harmony import */


      var _angular_material_select__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @angular/material/select */
      "ZTz/");
      /* harmony import */


      var _angular_material_slide_toggle__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! @angular/material/slide-toggle */
      "jMqV");
      /* harmony import */


      var _angular_material_slider__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! @angular/material/slider */
      "mPVK");
      /* harmony import */


      var _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(
      /*! @angular/material/snack-bar */
      "zHaW");
      /* harmony import */


      var ngx_stripe__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(
      /*! ngx-stripe */
      "AZjg");
      /* harmony import */


      var _vex_components_breadcrumbs_breadcrumbs_module__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(
      /*! @vex/components/breadcrumbs/breadcrumbs.module */
      "J0XA");
      /* harmony import */


      var _vex_components_secondary_toolbar_secondary_toolbar_module__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(
      /*! @vex/components/secondary-toolbar/secondary-toolbar.module */
      "Abzj");
      /* harmony import */


      var _vex_directives_container_container_module__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(
      /*! @vex/directives/container/container.module */
      "68Yx");
      /* harmony import */


      var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(
      /*! @visurel/iconify-angular */
      "l+Q0");
      /* harmony import */


      var _shared_components_payment_payment_method__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(
      /*! @shared/components/payment/payment-method */
      "iX9L");
      /* harmony import */


      var _buy_routing_module__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(
      /*! ./buy-routing.module */
      "c4QL");
      /* harmony import */


      var _buy_component__WEBPACK_IMPORTED_MODULE_24__ = __webpack_require__(
      /*! ./buy.component */
      "jzrE");

      var BuyModule = function BuyModule() {
        _classCallCheck(this, BuyModule);
      };

      BuyModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_buy_component__WEBPACK_IMPORTED_MODULE_24__["BuyComponent"]],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _buy_routing_module__WEBPACK_IMPORTED_MODULE_23__["BuyRoutingModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"], _angular_material_input__WEBPACK_IMPORTED_MODULE_11__["MatInputModule"], _angular_material_icon__WEBPACK_IMPORTED_MODULE_10__["MatIconModule"], _angular_material_button__WEBPACK_IMPORTED_MODULE_6__["MatButtonModule"], _angular_material_select__WEBPACK_IMPORTED_MODULE_13__["MatSelectModule"], _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_9__["MatDatepickerModule"], _angular_material_core__WEBPACK_IMPORTED_MODULE_8__["MatNativeDateModule"], _angular_material_autocomplete__WEBPACK_IMPORTED_MODULE_5__["MatAutocompleteModule"], _angular_material_slider__WEBPACK_IMPORTED_MODULE_15__["MatSliderModule"], _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_7__["MatCheckboxModule"], _angular_material_radio__WEBPACK_IMPORTED_MODULE_12__["MatRadioModule"], _angular_material_slide_toggle__WEBPACK_IMPORTED_MODULE_14__["MatSlideToggleModule"], _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_16__["MatSnackBarModule"], ngx_stripe__WEBPACK_IMPORTED_MODULE_17__["NgxStripeModule"], _vex_components_breadcrumbs_breadcrumbs_module__WEBPACK_IMPORTED_MODULE_18__["BreadcrumbsModule"], _vex_directives_container_container_module__WEBPACK_IMPORTED_MODULE_20__["ContainerModule"], _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_21__["IconModule"], _vex_components_secondary_toolbar_secondary_toolbar_module__WEBPACK_IMPORTED_MODULE_19__["SecondaryToolbarModule"], _shared_components_payment_payment_method__WEBPACK_IMPORTED_MODULE_22__["PaymentMethodsListModule"]]
      })], BuyModule);
      /***/
    },

    /***/
    "a3I5":
    /*!**********************************************************************************************************************!*\
      !*** ./node_modules/raw-loader/dist/cjs.js!./src/@vex/components/secondary-toolbar/secondary-toolbar.component.html ***!
      \**********************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function a3I5(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "<div class=\"secondary-toolbar-placeholder\">&nbsp;</div>\n\n<div [ngClass]=\"{ 'fixed': fixed$ | async, 'w-full': !(fixed$ | async) }\"\n     class=\"secondary-toolbar shadow-b py-1 z-40 border-t\"\n     fxLayout=\"row\">\n  <div class=\"px-gutter\" fxFlex=\"auto\" fxLayout=\"row\" fxLayoutAlign=\"start center\" vexContainer>\n    <h1 *ngIf=\"current\"\n        class=\"subheading-2 font-medium m-0 ltr:pr-3 rtl:pl-3 ltr:border-r rtl:border-l ltr:mr-3 rtl:ml-3\"\n        fxFlex.xs=\"auto\">{{ current }}</h1>\n\n    <ng-content></ng-content>\n  </div>\n</div>\n";
      /***/
    },

    /***/
    "c4QL":
    /*!***********************************************************************!*\
      !*** ./src/app/modules/subscriptions/pages/buy/buy-routing.module.ts ***!
      \***********************************************************************/

    /*! exports provided: BuyRoutingModule */

    /***/
    function c4QL(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "BuyRoutingModule", function () {
        return BuyRoutingModule;
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


      var _buy_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! ./buy.component */
      "jzrE");

      var routes = [{
        path: '',
        component: _buy_component__WEBPACK_IMPORTED_MODULE_3__["BuyComponent"]
      }];

      var BuyRoutingModule = function BuyRoutingModule() {
        _classCallCheck(this, BuyRoutingModule);
      };

      BuyRoutingModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]]
      })], BuyRoutingModule);
      /***/
    },

    /***/
    "jzrE":
    /*!******************************************************************!*\
      !*** ./src/app/modules/subscriptions/pages/buy/buy.component.ts ***!
      \******************************************************************/

    /*! exports provided: BuyComponent */

    /***/
    function jzrE(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "BuyComponent", function () {
        return BuyComponent;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _raw_loader_buy_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! raw-loader!./buy.component.html */
      "6hwn");
      /* harmony import */


      var _buy_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! ./buy.component.scss */
      "mc/U");
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


      var ngx_stripe__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! ngx-stripe */
      "AZjg");
      /* harmony import */


      var _vex_animations__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @vex/animations */
      "ORuP");
      /* harmony import */


      var _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @vex/utils/tailwindcss */
      "XXSj");
      /* harmony import */


      var _core_http_payment_method_resource_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @core/http/payment-method-resource.service */
      "z1g2");
      /* harmony import */


      var _core_http_subscription_resource_service__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @core/http/subscription-resource.service */
      "FKU7");
      /* harmony import */


      var _data_schema__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @data/schema */
      "V99k");
      /* harmony import */


      var _layout_services_layout_config_service__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @layout/services/layout-config.service */
      "U9Lm");

      var BuyComponent = /*#__PURE__*/function () {
        function BuyComponent(cd, fb, layoutConfigService, paymentMethodResource, route, router, snackbar, stripeService, subscriptionResource) {
          _classCallCheck(this, BuyComponent);

          this.cd = cd;
          this.fb = fb;
          this.layoutConfigService = layoutConfigService;
          this.paymentMethodResource = paymentMethodResource;
          this.route = route;
          this.router = router;
          this.snackbar = snackbar;
          this.stripeService = stripeService;
          this.subscriptionResource = subscriptionResource;
          this.cardOptions = {
            style: {
              base: {
                iconColor: '#666EE8',
                color: '#31325F',
                lineHeight: '40px',
                fontWeight: '300',
                fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
                fontSize: '18px',
                '::placeholder': {
                  color: '#CFD7E0'
                }
              }
            }
          };
          this.elementsOptions = {
            locale: 'en'
          };
          this.form = this.fb.group({
            cardName: null,
            email: null
          });
          this.months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'];
          this.years = Array.from(Array(20).keys()).map(function (year) {
            return year + new Date().getFullYear();
          });
          this.theme = _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_9__["default"];
          this.layoutConfigService.setIkaros();
        }

        _createClass(BuyComponent, [{
          key: "ngOnInit",
          value: function ngOnInit() {
            var _this$route$snapshot$ = this.route.snapshot.data,
                organization = _this$route$snapshot$.organization,
                paymentMethods = _this$route$snapshot$.paymentMethods,
                plan = _this$route$snapshot$.plan,
                subscription = _this$route$snapshot$.subscription;
            this.organization = new _data_schema__WEBPACK_IMPORTED_MODULE_12__["Organization"](organization);
            this.plan = new _data_schema__WEBPACK_IMPORTED_MODULE_12__["Plan"](plan);
            this.paymentMethods = paymentMethods.map(function (paymentMethod) {
              return new _data_schema__WEBPACK_IMPORTED_MODULE_12__["PaymentMethod"](paymentMethod);
            }).sort(function (a, b) {
              if (b.isDefault) {
                return 1;
              }

              if (!b.isDefault) {
                return -1;
              }

              return 0;
            });
            this.subscription = new _data_schema__WEBPACK_IMPORTED_MODULE_12__["Subscription"](subscription);
          }
        }, {
          key: "createPaymentMethod",
          value: function createPaymentMethod(paymentMethod, callback) {
            var _this = this;

            this.paymentMethodResource.create({
              organization_id: this.organization.id,
              payment_method_id: paymentMethod.id
            }).subscribe(function (res) {
              var newPaymentMethods = _this.paymentMethods.map(function (x) {
                return Object.assign({}, x);
              });

              newPaymentMethods.push(new _data_schema__WEBPACK_IMPORTED_MODULE_12__["PaymentMethod"](res));
              _this.paymentMethods = newPaymentMethods;

              _this.cd.detectChanges();

              if (callback) {
                callback(res);
              }
            });
          }
        }, {
          key: "purchase",
          value: function purchase() {
            var _this2 = this;

            if (!this.paymentMethods.length) {
              this.createStripePaymentMethod().subscribe(function (result) {
                if (result.paymentMethod) {
                  _this2.createPaymentMethod(result.paymentMethod, _this2.createOrUpdateSubscription.bind(_this2));
                } else if (result.error) {
                  _this2.snackbar.open(result.error.message, 'close'); // Error creating the token

                }
              });
            } else {
              this.createOrUpdateSubscription();
            }
          }
        }, {
          key: "createStripePaymentMethod",
          value: function createStripePaymentMethod() {
            var formValues = this.form.value;
            var name = formValues.name;
            return this.stripeService.createPaymentMethod({
              type: 'card',
              card: this.card.getCard(),
              billing_details: {}
            });
          }
        }, {
          key: "createOrUpdateSubscription",
          value: function createOrUpdateSubscription() {
            var _this3 = this;

            var params = {
              organization_id: this.organization.id,
              plan_id: this.plan.id
            };
            var observer;

            if (!this.subscription) {
              observer = this.subscriptionResource.create(params);
            } else {
              observer = this.subscriptionResource.update(this.subscription.id, params);
            }

            observer.subscribe(function (res) {
              _this3.snackbar.open('Subscription successfully updated!', 'close', {
                duration: 5000
              });

              _this3.success();
            });
          }
        }, {
          key: "success",
          value: function success() {
            var path;

            if (this.organization.isShadow) {
              path = "/users/".concat(this.organization.userId, "/billing");
            } else {
              path = "/organizations/".concat(this.organization.id, "/billing");
            }

            this.router.navigate([path], {});
          }
        }, {
          key: "cancel",
          value: function cancel() {
            var path = '/subscriptions/pricing';
            this.router.navigate([path], {
              queryParams: {
                organization_id: this.route.snapshot.queryParams.organization_id
              }
            });
          }
        }, {
          key: "ngOnDestroy",
          value: function ngOnDestroy() {
            this.layoutConfigService.setZeus();
          }
        }]);

        return BuyComponent;
      }();

      BuyComponent.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ChangeDetectorRef"]
        }, {
          type: _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormBuilder"]
        }, {
          type: _layout_services_layout_config_service__WEBPACK_IMPORTED_MODULE_13__["LayoutConfigService"]
        }, {
          type: _core_http_payment_method_resource_service__WEBPACK_IMPORTED_MODULE_10__["PaymentMethodResource"]
        }, {
          type: _angular_router__WEBPACK_IMPORTED_MODULE_6__["ActivatedRoute"]
        }, {
          type: _angular_router__WEBPACK_IMPORTED_MODULE_6__["Router"]
        }, {
          type: _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_5__["MatSnackBar"]
        }, {
          type: ngx_stripe__WEBPACK_IMPORTED_MODULE_7__["StripeService"]
        }, {
          type: _core_http_subscription_resource_service__WEBPACK_IMPORTED_MODULE_11__["SubscriptionResource"]
        }];
      };

      BuyComponent.propDecorators = {
        card: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ViewChild"],
          args: [ngx_stripe__WEBPACK_IMPORTED_MODULE_7__["StripeCardComponent"]]
        }]
      };
      BuyComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'vex-buy',
        template: _raw_loader_buy_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        animations: [_vex_animations__WEBPACK_IMPORTED_MODULE_8__["stagger60ms"], _vex_animations__WEBPACK_IMPORTED_MODULE_8__["fadeInUp400ms"]],
        styles: [_buy_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
      })], BuyComponent);
      /***/
    },

    /***/
    "mPVK":
    /*!***********************************************************!*\
      !*** ./node_modules/@angular/material/fesm2015/slider.js ***!
      \***********************************************************/

    /*! exports provided: MAT_SLIDER_VALUE_ACCESSOR, MatSlider, MatSliderChange, MatSliderModule */

    /***/
    function mPVK(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MAT_SLIDER_VALUE_ACCESSOR", function () {
        return MAT_SLIDER_VALUE_ACCESSOR;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatSlider", function () {
        return MatSlider;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatSliderChange", function () {
        return MatSliderChange;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatSliderModule", function () {
        return MatSliderModule;
      });
      /* harmony import */


      var _angular_common__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! @angular/common */
      "SVse");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_material_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @angular/material/core */
      "UhP/");
      /* harmony import */


      var _angular_cdk_a11y__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/cdk/a11y */
      "YEUz");
      /* harmony import */


      var _angular_cdk_bidi__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/cdk/bidi */
      "9gLZ");
      /* harmony import */


      var _angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/cdk/coercion */
      "8LU1");
      /* harmony import */


      var _angular_cdk_keycodes__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/cdk/keycodes */
      "Ht+U");
      /* harmony import */


      var _angular_forms__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @angular/forms */
      "s7LF");
      /* harmony import */


      var _angular_platform_browser_animations__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @angular/platform-browser/animations */
      "omvX");
      /* harmony import */


      var _angular_cdk_platform__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @angular/cdk/platform */
      "SCoL");
      /* harmony import */


      var rxjs__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! rxjs */
      "qCKp");
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */


      var activeEventOptions = Object(_angular_cdk_platform__WEBPACK_IMPORTED_MODULE_9__["normalizePassiveListenerOptions"])({
        passive: false
      });
      /**
       * Visually, a 30px separation between tick marks looks best. This is very subjective but it is
       * the default separation we chose.
       */

      var MIN_AUTO_TICK_SEPARATION = 30;
      /** The thumb gap size for a disabled slider. */

      var DISABLED_THUMB_GAP = 7;
      /** The thumb gap size for a non-active slider at its minimum value. */

      var MIN_VALUE_NONACTIVE_THUMB_GAP = 7;
      /** The thumb gap size for an active slider at its minimum value. */

      var MIN_VALUE_ACTIVE_THUMB_GAP = 10;
      /**
       * Provider Expression that allows mat-slider to register as a ControlValueAccessor.
       * This allows it to support [(ngModel)] and [formControl].
       * @docs-private
       */

      var MAT_SLIDER_VALUE_ACCESSOR = {
        provide: _angular_forms__WEBPACK_IMPORTED_MODULE_7__["NG_VALUE_ACCESSOR"],
        useExisting: Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["forwardRef"])(function () {
          return MatSlider;
        }),
        multi: true
      };
      /** A simple change event emitted by the MatSlider component. */

      var MatSliderChange = function MatSliderChange() {
        _classCallCheck(this, MatSliderChange);
      }; // Boilerplate for applying mixins to MatSlider.

      /** @docs-private */


      var MatSliderBase = function MatSliderBase(_elementRef) {
        _classCallCheck(this, MatSliderBase);

        this._elementRef = _elementRef;
      };

      var _MatSliderMixinBase = Object(_angular_material_core__WEBPACK_IMPORTED_MODULE_2__["mixinTabIndex"])(Object(_angular_material_core__WEBPACK_IMPORTED_MODULE_2__["mixinColor"])(Object(_angular_material_core__WEBPACK_IMPORTED_MODULE_2__["mixinDisabled"])(MatSliderBase), 'accent'));
      /**
       * Allows users to select from a range of values by moving the slider thumb. It is similar in
       * behavior to the native `<input type="range">` element.
       */


      var MatSlider = /*#__PURE__*/function (_MatSliderMixinBase2) {
        _inherits(MatSlider, _MatSliderMixinBase2);

        var _super = _createSuper(MatSlider);

        function MatSlider(elementRef, _focusMonitor, _changeDetectorRef, _dir, tabIndex, _ngZone, _document, _animationMode) {
          var _this4;

          _classCallCheck(this, MatSlider);

          _this4 = _super.call(this, elementRef);
          _this4._focusMonitor = _focusMonitor;
          _this4._changeDetectorRef = _changeDetectorRef;
          _this4._dir = _dir;
          _this4._ngZone = _ngZone;
          _this4._animationMode = _animationMode;
          _this4._invert = false;
          _this4._max = 100;
          _this4._min = 0;
          _this4._step = 1;
          _this4._thumbLabel = false;
          _this4._tickInterval = 0;
          _this4._value = null;
          _this4._vertical = false;
          /** Event emitted when the slider value has changed. */

          _this4.change = new _angular_core__WEBPACK_IMPORTED_MODULE_1__["EventEmitter"]();
          /** Event emitted when the slider thumb moves. */

          _this4.input = new _angular_core__WEBPACK_IMPORTED_MODULE_1__["EventEmitter"]();
          /**
           * Emits when the raw value of the slider changes. This is here primarily
           * to facilitate the two-way binding for the `value` input.
           * @docs-private
           */

          _this4.valueChange = new _angular_core__WEBPACK_IMPORTED_MODULE_1__["EventEmitter"]();
          /** onTouch function registered via registerOnTouch (ControlValueAccessor). */

          _this4.onTouched = function () {};

          _this4._percent = 0;
          /**
           * Whether or not the thumb is sliding.
           * Used to determine if there should be a transition for the thumb and fill track.
           */

          _this4._isSliding = false;
          /**
           * Whether or not the slider is active (clicked or sliding).
           * Used to shrink and grow the thumb as according to the Material Design spec.
           */

          _this4._isActive = false;
          /** The size of a tick interval as a percentage of the size of the track. */

          _this4._tickIntervalPercent = 0;
          /** The dimensions of the slider. */

          _this4._sliderDimensions = null;

          _this4._controlValueAccessorChangeFn = function () {};
          /** Subscription to the Directionality change EventEmitter. */


          _this4._dirChangeSubscription = rxjs__WEBPACK_IMPORTED_MODULE_10__["Subscription"].EMPTY;
          /** Called when the user has put their pointer down on the slider. */

          _this4._pointerDown = function (event) {
            // Don't do anything if the slider is disabled or the
            // user is using anything other than the main mouse button.
            if (_this4.disabled || _this4._isSliding || !isTouchEvent(event) && event.button !== 0) {
              return;
            }

            _this4._ngZone.run(function () {
              var oldValue = _this4.value;
              var pointerPosition = getPointerPositionOnPage(event);
              _this4._isSliding = true;
              _this4._lastPointerEvent = event;
              event.preventDefault();

              _this4._focusHostElement();

              _this4._onMouseenter(); // Simulate mouseenter in case this is a mobile device.


              _this4._bindGlobalEvents(event);

              _this4._focusHostElement();

              _this4._updateValueFromPosition(pointerPosition);

              _this4._valueOnSlideStart = oldValue; // Emit a change and input event if the value changed.

              if (oldValue != _this4.value) {
                _this4._emitInputEvent();
              }
            });
          };
          /**
           * Called when the user has moved their pointer after
           * starting to drag. Bound on the document level.
           */


          _this4._pointerMove = function (event) {
            if (_this4._isSliding) {
              // Prevent the slide from selecting anything else.
              event.preventDefault();
              var oldValue = _this4.value;
              _this4._lastPointerEvent = event;

              _this4._updateValueFromPosition(getPointerPositionOnPage(event)); // Native range elements always emit `input` events when the value changed while sliding.


              if (oldValue != _this4.value) {
                _this4._emitInputEvent();
              }
            }
          };
          /** Called when the user has lifted their pointer. Bound on the document level. */


          _this4._pointerUp = function (event) {
            if (_this4._isSliding) {
              event.preventDefault();

              _this4._removeGlobalEvents();

              _this4._isSliding = false;

              if (_this4._valueOnSlideStart != _this4.value && !_this4.disabled) {
                _this4._emitChangeEvent();
              }

              _this4._valueOnSlideStart = _this4._lastPointerEvent = null;
            }
          };
          /** Called when the window has lost focus. */


          _this4._windowBlur = function () {
            // If the window is blurred while dragging we need to stop dragging because the
            // browser won't dispatch the `mouseup` and `touchend` events anymore.
            if (_this4._lastPointerEvent) {
              _this4._pointerUp(_this4._lastPointerEvent);
            }
          };

          _this4._document = _document;
          _this4.tabIndex = parseInt(tabIndex) || 0;

          _ngZone.runOutsideAngular(function () {
            var element = elementRef.nativeElement;
            element.addEventListener('mousedown', _this4._pointerDown, activeEventOptions);
            element.addEventListener('touchstart', _this4._pointerDown, activeEventOptions);
          });

          return _this4;
        }
        /** Whether the slider is inverted. */


        _createClass(MatSlider, [{
          key: "focus",

          /** set focus to the host element */
          value: function focus(options) {
            this._focusHostElement(options);
          }
          /** blur the host element */

        }, {
          key: "blur",
          value: function blur() {
            this._blurHostElement();
          }
          /** The percentage of the slider that coincides with the value. */

        }, {
          key: "_shouldInvertAxis",

          /**
           * Whether the axis of the slider is inverted.
           * (i.e. whether moving the thumb in the positive x or y direction decreases the slider's value).
           */
          value: function _shouldInvertAxis() {
            // Standard non-inverted mode for a vertical slider should be dragging the thumb from bottom to
            // top. However from a y-axis standpoint this is inverted.
            return this.vertical ? !this.invert : this.invert;
          }
          /** Whether the slider is at its minimum value. */

        }, {
          key: "_isMinValue",
          value: function _isMinValue() {
            return this.percent === 0;
          }
          /**
           * The amount of space to leave between the slider thumb and the track fill & track background
           * elements.
           */

        }, {
          key: "_getThumbGap",
          value: function _getThumbGap() {
            if (this.disabled) {
              return DISABLED_THUMB_GAP;
            }

            if (this._isMinValue() && !this.thumbLabel) {
              return this._isActive ? MIN_VALUE_ACTIVE_THUMB_GAP : MIN_VALUE_NONACTIVE_THUMB_GAP;
            }

            return 0;
          }
          /** CSS styles for the track background element. */

        }, {
          key: "_getTrackBackgroundStyles",
          value: function _getTrackBackgroundStyles() {
            var axis = this.vertical ? 'Y' : 'X';
            var scale = this.vertical ? "1, ".concat(1 - this.percent, ", 1") : "".concat(1 - this.percent, ", 1, 1");
            var sign = this._shouldInvertMouseCoords() ? '-' : '';
            return {
              // scale3d avoids some rendering issues in Chrome. See #12071.
              transform: "translate".concat(axis, "(").concat(sign).concat(this._getThumbGap(), "px) scale3d(").concat(scale, ")")
            };
          }
          /** CSS styles for the track fill element. */

        }, {
          key: "_getTrackFillStyles",
          value: function _getTrackFillStyles() {
            var percent = this.percent;
            var axis = this.vertical ? 'Y' : 'X';
            var scale = this.vertical ? "1, ".concat(percent, ", 1") : "".concat(percent, ", 1, 1");
            var sign = this._shouldInvertMouseCoords() ? '' : '-';
            return {
              // scale3d avoids some rendering issues in Chrome. See #12071.
              transform: "translate".concat(axis, "(").concat(sign).concat(this._getThumbGap(), "px) scale3d(").concat(scale, ")"),
              // iOS Safari has a bug where it won't re-render elements which start of as `scale(0)` until
              // something forces a style recalculation on it. Since we'll end up with `scale(0)` when
              // the value of the slider is 0, we can easily get into this situation. We force a
              // recalculation by changing the element's `display` when it goes from 0 to any other value.
              display: percent === 0 ? 'none' : ''
            };
          }
          /** CSS styles for the ticks container element. */

        }, {
          key: "_getTicksContainerStyles",
          value: function _getTicksContainerStyles() {
            var axis = this.vertical ? 'Y' : 'X'; // For a horizontal slider in RTL languages we push the ticks container off the left edge
            // instead of the right edge to avoid causing a horizontal scrollbar to appear.

            var sign = !this.vertical && this._getDirection() == 'rtl' ? '' : '-';
            var offset = this._tickIntervalPercent / 2 * 100;
            return {
              'transform': "translate".concat(axis, "(").concat(sign).concat(offset, "%)")
            };
          }
          /** CSS styles for the ticks element. */

        }, {
          key: "_getTicksStyles",
          value: function _getTicksStyles() {
            var tickSize = this._tickIntervalPercent * 100;
            var backgroundSize = this.vertical ? "2px ".concat(tickSize, "%") : "".concat(tickSize, "% 2px");
            var axis = this.vertical ? 'Y' : 'X'; // Depending on the direction we pushed the ticks container, push the ticks the opposite
            // direction to re-center them but clip off the end edge. In RTL languages we need to flip the
            // ticks 180 degrees so we're really cutting off the end edge abd not the start.

            var sign = !this.vertical && this._getDirection() == 'rtl' ? '-' : '';
            var rotate = !this.vertical && this._getDirection() == 'rtl' ? ' rotate(180deg)' : '';
            var styles = {
              'backgroundSize': backgroundSize,
              // Without translateZ ticks sometimes jitter as the slider moves on Chrome & Firefox.
              'transform': "translateZ(0) translate".concat(axis, "(").concat(sign).concat(tickSize / 2, "%)").concat(rotate)
            };

            if (this._isMinValue() && this._getThumbGap()) {
              var shouldInvertAxis = this._shouldInvertAxis();

              var side;

              if (this.vertical) {
                side = shouldInvertAxis ? 'Bottom' : 'Top';
              } else {
                side = shouldInvertAxis ? 'Right' : 'Left';
              }

              styles["padding".concat(side)] = "".concat(this._getThumbGap(), "px");
            }

            return styles;
          }
        }, {
          key: "_getThumbContainerStyles",
          value: function _getThumbContainerStyles() {
            var shouldInvertAxis = this._shouldInvertAxis();

            var axis = this.vertical ? 'Y' : 'X'; // For a horizontal slider in RTL languages we push the thumb container off the left edge
            // instead of the right edge to avoid causing a horizontal scrollbar to appear.

            var invertOffset = this._getDirection() == 'rtl' && !this.vertical ? !shouldInvertAxis : shouldInvertAxis;
            var offset = (invertOffset ? this.percent : 1 - this.percent) * 100;
            return {
              'transform': "translate".concat(axis, "(-").concat(offset, "%)")
            };
          }
          /**
           * Whether mouse events should be converted to a slider position by calculating their distance
           * from the right or bottom edge of the slider as opposed to the top or left.
           */

        }, {
          key: "_shouldInvertMouseCoords",
          value: function _shouldInvertMouseCoords() {
            var shouldInvertAxis = this._shouldInvertAxis();

            return this._getDirection() == 'rtl' && !this.vertical ? !shouldInvertAxis : shouldInvertAxis;
          }
          /** The language direction for this slider element. */

        }, {
          key: "_getDirection",
          value: function _getDirection() {
            return this._dir && this._dir.value == 'rtl' ? 'rtl' : 'ltr';
          }
        }, {
          key: "ngAfterViewInit",
          value: function ngAfterViewInit() {
            var _this5 = this;

            this._focusMonitor.monitor(this._elementRef, true).subscribe(function (origin) {
              _this5._isActive = !!origin && origin !== 'keyboard';

              _this5._changeDetectorRef.detectChanges();
            });

            if (this._dir) {
              this._dirChangeSubscription = this._dir.change.subscribe(function () {
                _this5._changeDetectorRef.markForCheck();
              });
            }
          }
        }, {
          key: "ngOnDestroy",
          value: function ngOnDestroy() {
            var element = this._elementRef.nativeElement;
            element.removeEventListener('mousedown', this._pointerDown, activeEventOptions);
            element.removeEventListener('touchstart', this._pointerDown, activeEventOptions);
            this._lastPointerEvent = null;

            this._removeGlobalEvents();

            this._focusMonitor.stopMonitoring(this._elementRef);

            this._dirChangeSubscription.unsubscribe();
          }
        }, {
          key: "_onMouseenter",
          value: function _onMouseenter() {
            if (this.disabled) {
              return;
            } // We save the dimensions of the slider here so we can use them to update the spacing of the
            // ticks and determine where on the slider click and slide events happen.


            this._sliderDimensions = this._getSliderDimensions();

            this._updateTickIntervalPercent();
          }
        }, {
          key: "_onFocus",
          value: function _onFocus() {
            // We save the dimensions of the slider here so we can use them to update the spacing of the
            // ticks and determine where on the slider click and slide events happen.
            this._sliderDimensions = this._getSliderDimensions();

            this._updateTickIntervalPercent();
          }
        }, {
          key: "_onBlur",
          value: function _onBlur() {
            this.onTouched();
          }
        }, {
          key: "_onKeydown",
          value: function _onKeydown(event) {
            if (this.disabled || Object(_angular_cdk_keycodes__WEBPACK_IMPORTED_MODULE_6__["hasModifierKey"])(event)) {
              return;
            }

            var oldValue = this.value;

            switch (event.keyCode) {
              case _angular_cdk_keycodes__WEBPACK_IMPORTED_MODULE_6__["PAGE_UP"]:
                this._increment(10);

                break;

              case _angular_cdk_keycodes__WEBPACK_IMPORTED_MODULE_6__["PAGE_DOWN"]:
                this._increment(-10);

                break;

              case _angular_cdk_keycodes__WEBPACK_IMPORTED_MODULE_6__["END"]:
                this.value = this.max;
                break;

              case _angular_cdk_keycodes__WEBPACK_IMPORTED_MODULE_6__["HOME"]:
                this.value = this.min;
                break;

              case _angular_cdk_keycodes__WEBPACK_IMPORTED_MODULE_6__["LEFT_ARROW"]:
                // NOTE: For a sighted user it would make more sense that when they press an arrow key on an
                // inverted slider the thumb moves in that direction. However for a blind user, nothing
                // about the slider indicates that it is inverted. They will expect left to be decrement,
                // regardless of how it appears on the screen. For speakers ofRTL languages, they probably
                // expect left to mean increment. Therefore we flip the meaning of the side arrow keys for
                // RTL. For inverted sliders we prefer a good a11y experience to having it "look right" for
                // sighted users, therefore we do not swap the meaning.
                this._increment(this._getDirection() == 'rtl' ? 1 : -1);

                break;

              case _angular_cdk_keycodes__WEBPACK_IMPORTED_MODULE_6__["UP_ARROW"]:
                this._increment(1);

                break;

              case _angular_cdk_keycodes__WEBPACK_IMPORTED_MODULE_6__["RIGHT_ARROW"]:
                // See comment on LEFT_ARROW about the conditions under which we flip the meaning.
                this._increment(this._getDirection() == 'rtl' ? -1 : 1);

                break;

              case _angular_cdk_keycodes__WEBPACK_IMPORTED_MODULE_6__["DOWN_ARROW"]:
                this._increment(-1);

                break;

              default:
                // Return if the key is not one that we explicitly handle to avoid calling preventDefault on
                // it.
                return;
            }

            if (oldValue != this.value) {
              this._emitInputEvent();

              this._emitChangeEvent();
            }

            this._isSliding = true;
            event.preventDefault();
          }
        }, {
          key: "_onKeyup",
          value: function _onKeyup() {
            this._isSliding = false;
          }
          /** Use defaultView of injected document if available or fallback to global window reference */

        }, {
          key: "_getWindow",
          value: function _getWindow() {
            return this._document.defaultView || window;
          }
          /**
           * Binds our global move and end events. They're bound at the document level and only while
           * dragging so that the user doesn't have to keep their pointer exactly over the slider
           * as they're swiping across the screen.
           */

        }, {
          key: "_bindGlobalEvents",
          value: function _bindGlobalEvents(triggerEvent) {
            // Note that we bind the events to the `document`, because it allows us to capture
            // drag cancel events where the user's pointer is outside the browser window.
            var document = this._document;
            var isTouch = isTouchEvent(triggerEvent);
            var moveEventName = isTouch ? 'touchmove' : 'mousemove';
            var endEventName = isTouch ? 'touchend' : 'mouseup';
            document.addEventListener(moveEventName, this._pointerMove, activeEventOptions);
            document.addEventListener(endEventName, this._pointerUp, activeEventOptions);

            if (isTouch) {
              document.addEventListener('touchcancel', this._pointerUp, activeEventOptions);
            }

            var window = this._getWindow();

            if (typeof window !== 'undefined' && window) {
              window.addEventListener('blur', this._windowBlur);
            }
          }
          /** Removes any global event listeners that we may have added. */

        }, {
          key: "_removeGlobalEvents",
          value: function _removeGlobalEvents() {
            var document = this._document;
            document.removeEventListener('mousemove', this._pointerMove, activeEventOptions);
            document.removeEventListener('mouseup', this._pointerUp, activeEventOptions);
            document.removeEventListener('touchmove', this._pointerMove, activeEventOptions);
            document.removeEventListener('touchend', this._pointerUp, activeEventOptions);
            document.removeEventListener('touchcancel', this._pointerUp, activeEventOptions);

            var window = this._getWindow();

            if (typeof window !== 'undefined' && window) {
              window.removeEventListener('blur', this._windowBlur);
            }
          }
          /** Increments the slider by the given number of steps (negative number decrements). */

        }, {
          key: "_increment",
          value: function _increment(numSteps) {
            this.value = this._clamp((this.value || 0) + this.step * numSteps, this.min, this.max);
          }
          /** Calculate the new value from the new physical location. The value will always be snapped. */

        }, {
          key: "_updateValueFromPosition",
          value: function _updateValueFromPosition(pos) {
            if (!this._sliderDimensions) {
              return;
            }

            var offset = this.vertical ? this._sliderDimensions.top : this._sliderDimensions.left;
            var size = this.vertical ? this._sliderDimensions.height : this._sliderDimensions.width;
            var posComponent = this.vertical ? pos.y : pos.x; // The exact value is calculated from the event and used to find the closest snap value.

            var percent = this._clamp((posComponent - offset) / size);

            if (this._shouldInvertMouseCoords()) {
              percent = 1 - percent;
            } // Since the steps may not divide cleanly into the max value, if the user
            // slid to 0 or 100 percent, we jump to the min/max value. This approach
            // is slightly more intuitive than using `Math.ceil` below, because it
            // follows the user's pointer closer.


            if (percent === 0) {
              this.value = this.min;
            } else if (percent === 1) {
              this.value = this.max;
            } else {
              var exactValue = this._calculateValue(percent); // This calculation finds the closest step by finding the closest
              // whole number divisible by the step relative to the min.


              var closestValue = Math.round((exactValue - this.min) / this.step) * this.step + this.min; // The value needs to snap to the min and max.

              this.value = this._clamp(closestValue, this.min, this.max);
            }
          }
          /** Emits a change event if the current value is different from the last emitted value. */

        }, {
          key: "_emitChangeEvent",
          value: function _emitChangeEvent() {
            this._controlValueAccessorChangeFn(this.value);

            this.valueChange.emit(this.value);
            this.change.emit(this._createChangeEvent());
          }
          /** Emits an input event when the current value is different from the last emitted value. */

        }, {
          key: "_emitInputEvent",
          value: function _emitInputEvent() {
            this.input.emit(this._createChangeEvent());
          }
          /** Updates the amount of space between ticks as a percentage of the width of the slider. */

        }, {
          key: "_updateTickIntervalPercent",
          value: function _updateTickIntervalPercent() {
            if (!this.tickInterval || !this._sliderDimensions) {
              return;
            }

            if (this.tickInterval == 'auto') {
              var trackSize = this.vertical ? this._sliderDimensions.height : this._sliderDimensions.width;
              var pixelsPerStep = trackSize * this.step / (this.max - this.min);
              var stepsPerTick = Math.ceil(MIN_AUTO_TICK_SEPARATION / pixelsPerStep);
              var pixelsPerTick = stepsPerTick * this.step;
              this._tickIntervalPercent = pixelsPerTick / trackSize;
            } else {
              this._tickIntervalPercent = this.tickInterval * this.step / (this.max - this.min);
            }
          }
          /** Creates a slider change object from the specified value. */

        }, {
          key: "_createChangeEvent",
          value: function _createChangeEvent() {
            var value = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : this.value;
            var event = new MatSliderChange();
            event.source = this;
            event.value = value;
            return event;
          }
          /** Calculates the percentage of the slider that a value is. */

        }, {
          key: "_calculatePercentage",
          value: function _calculatePercentage(value) {
            return ((value || 0) - this.min) / (this.max - this.min);
          }
          /** Calculates the value a percentage of the slider corresponds to. */

        }, {
          key: "_calculateValue",
          value: function _calculateValue(percentage) {
            return this.min + percentage * (this.max - this.min);
          }
          /** Return a number between two numbers. */

        }, {
          key: "_clamp",
          value: function _clamp(value) {
            var min = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 0;
            var max = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : 1;
            return Math.max(min, Math.min(value, max));
          }
          /**
           * Get the bounding client rect of the slider track element.
           * The track is used rather than the native element to ignore the extra space that the thumb can
           * take up.
           */

        }, {
          key: "_getSliderDimensions",
          value: function _getSliderDimensions() {
            return this._sliderWrapper ? this._sliderWrapper.nativeElement.getBoundingClientRect() : null;
          }
          /**
           * Focuses the native element.
           * Currently only used to allow a blur event to fire but will be used with keyboard input later.
           */

        }, {
          key: "_focusHostElement",
          value: function _focusHostElement(options) {
            this._elementRef.nativeElement.focus(options);
          }
          /** Blurs the native element. */

        }, {
          key: "_blurHostElement",
          value: function _blurHostElement() {
            this._elementRef.nativeElement.blur();
          }
          /**
           * Sets the model value. Implemented as part of ControlValueAccessor.
           * @param value
           */

        }, {
          key: "writeValue",
          value: function writeValue(value) {
            this.value = value;
          }
          /**
           * Registers a callback to be triggered when the value has changed.
           * Implemented as part of ControlValueAccessor.
           * @param fn Callback to be registered.
           */

        }, {
          key: "registerOnChange",
          value: function registerOnChange(fn) {
            this._controlValueAccessorChangeFn = fn;
          }
          /**
           * Registers a callback to be triggered when the component is touched.
           * Implemented as part of ControlValueAccessor.
           * @param fn Callback to be registered.
           */

        }, {
          key: "registerOnTouched",
          value: function registerOnTouched(fn) {
            this.onTouched = fn;
          }
          /**
           * Sets whether the component should be disabled.
           * Implemented as part of ControlValueAccessor.
           * @param isDisabled
           */

        }, {
          key: "setDisabledState",
          value: function setDisabledState(isDisabled) {
            this.disabled = isDisabled;
          }
        }, {
          key: "invert",
          get: function get() {
            return this._invert;
          },
          set: function set(value) {
            this._invert = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_5__["coerceBooleanProperty"])(value);
          }
          /** The maximum value that the slider can have. */

        }, {
          key: "max",
          get: function get() {
            return this._max;
          },
          set: function set(v) {
            this._max = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_5__["coerceNumberProperty"])(v, this._max);
            this._percent = this._calculatePercentage(this._value); // Since this also modifies the percentage, we need to let the change detection know.

            this._changeDetectorRef.markForCheck();
          }
          /** The minimum value that the slider can have. */

        }, {
          key: "min",
          get: function get() {
            return this._min;
          },
          set: function set(v) {
            this._min = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_5__["coerceNumberProperty"])(v, this._min); // If the value wasn't explicitly set by the user, set it to the min.

            if (this._value === null) {
              this.value = this._min;
            }

            this._percent = this._calculatePercentage(this._value); // Since this also modifies the percentage, we need to let the change detection know.

            this._changeDetectorRef.markForCheck();
          }
          /** The values at which the thumb will snap. */

        }, {
          key: "step",
          get: function get() {
            return this._step;
          },
          set: function set(v) {
            this._step = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_5__["coerceNumberProperty"])(v, this._step);

            if (this._step % 1 !== 0) {
              this._roundToDecimal = this._step.toString().split('.').pop().length;
            } // Since this could modify the label, we need to notify the change detection.


            this._changeDetectorRef.markForCheck();
          }
          /** Whether or not to show the thumb label. */

        }, {
          key: "thumbLabel",
          get: function get() {
            return this._thumbLabel;
          },
          set: function set(value) {
            this._thumbLabel = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_5__["coerceBooleanProperty"])(value);
          }
          /**
           * How often to show ticks. Relative to the step so that a tick always appears on a step.
           * Ex: Tick interval of 4 with a step of 3 will draw a tick every 4 steps (every 12 values).
           */

        }, {
          key: "tickInterval",
          get: function get() {
            return this._tickInterval;
          },
          set: function set(value) {
            if (value === 'auto') {
              this._tickInterval = 'auto';
            } else if (typeof value === 'number' || typeof value === 'string') {
              this._tickInterval = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_5__["coerceNumberProperty"])(value, this._tickInterval);
            } else {
              this._tickInterval = 0;
            }
          }
          /** Value of the slider. */

        }, {
          key: "value",
          get: function get() {
            // If the value needs to be read and it is still uninitialized, initialize it to the min.
            if (this._value === null) {
              this.value = this._min;
            }

            return this._value;
          },
          set: function set(v) {
            if (v !== this._value) {
              var value = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_5__["coerceNumberProperty"])(v); // While incrementing by a decimal we can end up with values like 33.300000000000004.
              // Truncate it to ensure that it matches the label and to make it easier to work with.

              if (this._roundToDecimal && value !== this.min && value !== this.max) {
                value = parseFloat(value.toFixed(this._roundToDecimal));
              }

              this._value = value;
              this._percent = this._calculatePercentage(this._value); // Since this also modifies the percentage, we need to let the change detection know.

              this._changeDetectorRef.markForCheck();
            }
          }
          /** Whether the slider is vertical. */

        }, {
          key: "vertical",
          get: function get() {
            return this._vertical;
          },
          set: function set(value) {
            this._vertical = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_5__["coerceBooleanProperty"])(value);
          }
          /** The value to be used for display purposes. */

        }, {
          key: "displayValue",
          get: function get() {
            if (this.displayWith) {
              // Value is never null but since setters and getters cannot have
              // different types, the value getter is also typed to return null.
              return this.displayWith(this.value);
            } // Note that this could be improved further by rounding something like 0.999 to 1 or
            // 0.899 to 0.9, however it is very performance sensitive, because it gets called on
            // every change detection cycle.


            if (this._roundToDecimal && this.value && this.value % 1 !== 0) {
              return this.value.toFixed(this._roundToDecimal);
            }

            return this.value || 0;
          }
        }, {
          key: "percent",
          get: function get() {
            return this._clamp(this._percent);
          }
        }]);

        return MatSlider;
      }(_MatSliderMixinBase);

      MatSlider.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"],
        args: [{
          selector: 'mat-slider',
          exportAs: 'matSlider',
          providers: [MAT_SLIDER_VALUE_ACCESSOR],
          host: {
            '(focus)': '_onFocus()',
            '(blur)': '_onBlur()',
            '(keydown)': '_onKeydown($event)',
            '(keyup)': '_onKeyup()',
            '(mouseenter)': '_onMouseenter()',
            // On Safari starting to slide temporarily triggers text selection mode which
            // show the wrong cursor. We prevent it by stopping the `selectstart` event.
            '(selectstart)': '$event.preventDefault()',
            'class': 'mat-slider mat-focus-indicator',
            'role': 'slider',
            '[tabIndex]': 'tabIndex',
            '[attr.aria-disabled]': 'disabled',
            '[attr.aria-valuemax]': 'max',
            '[attr.aria-valuemin]': 'min',
            '[attr.aria-valuenow]': 'value',
            // NVDA and Jaws appear to announce the `aria-valuenow` by calculating its percentage based
            // on its value between `aria-valuemin` and `aria-valuemax`. Due to how decimals are handled,
            // it can cause the slider to read out a very long value like 0.20000068 if the current value
            // is 0.2 with a min of 0 and max of 1. We work around the issue by setting `aria-valuetext`
            // to the same value that we set on the slider's thumb which will be truncated.
            '[attr.aria-valuetext]': 'valueText == null ? displayValue : valueText',
            '[attr.aria-orientation]': 'vertical ? "vertical" : "horizontal"',
            '[class.mat-slider-disabled]': 'disabled',
            '[class.mat-slider-has-ticks]': 'tickInterval',
            '[class.mat-slider-horizontal]': '!vertical',
            '[class.mat-slider-axis-inverted]': '_shouldInvertAxis()',
            // Class binding which is only used by the test harness as there is no other
            // way for the harness to detect if mouse coordinates need to be inverted.
            '[class.mat-slider-invert-mouse-coords]': '_shouldInvertMouseCoords()',
            '[class.mat-slider-sliding]': '_isSliding',
            '[class.mat-slider-thumb-label-showing]': 'thumbLabel',
            '[class.mat-slider-vertical]': 'vertical',
            '[class.mat-slider-min-value]': '_isMinValue()',
            '[class.mat-slider-hide-last-tick]': 'disabled || _isMinValue() && _getThumbGap() && _shouldInvertAxis()',
            '[class._mat-animation-noopable]': '_animationMode === "NoopAnimations"'
          },
          template: "<div class=\"mat-slider-wrapper\" #sliderWrapper>\n  <div class=\"mat-slider-track-wrapper\">\n    <div class=\"mat-slider-track-background\" [ngStyle]=\"_getTrackBackgroundStyles()\"></div>\n    <div class=\"mat-slider-track-fill\" [ngStyle]=\"_getTrackFillStyles()\"></div>\n  </div>\n  <div class=\"mat-slider-ticks-container\" [ngStyle]=\"_getTicksContainerStyles()\">\n    <div class=\"mat-slider-ticks\" [ngStyle]=\"_getTicksStyles()\"></div>\n  </div>\n  <div class=\"mat-slider-thumb-container\" [ngStyle]=\"_getThumbContainerStyles()\">\n    <div class=\"mat-slider-focus-ring\"></div>\n    <div class=\"mat-slider-thumb\"></div>\n    <div class=\"mat-slider-thumb-label\">\n      <span class=\"mat-slider-thumb-label-text\">{{displayValue}}</span>\n    </div>\n  </div>\n</div>\n",
          inputs: ['disabled', 'color', 'tabIndex'],
          encapsulation: _angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewEncapsulation"].None,
          changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_1__["ChangeDetectionStrategy"].OnPush,
          styles: [".mat-slider{display:inline-block;position:relative;box-sizing:border-box;padding:8px;outline:none;vertical-align:middle}.mat-slider:not(.mat-slider-disabled):active,.mat-slider.mat-slider-sliding:not(.mat-slider-disabled){cursor:-webkit-grabbing;cursor:grabbing}.mat-slider-wrapper{position:absolute}.mat-slider-track-wrapper{position:absolute;top:0;left:0;overflow:hidden}.mat-slider-track-fill{position:absolute;transform-origin:0 0;transition:transform 400ms cubic-bezier(0.25, 0.8, 0.25, 1),background-color 400ms cubic-bezier(0.25, 0.8, 0.25, 1)}.mat-slider-track-background{position:absolute;transform-origin:100% 100%;transition:transform 400ms cubic-bezier(0.25, 0.8, 0.25, 1),background-color 400ms cubic-bezier(0.25, 0.8, 0.25, 1)}.mat-slider-ticks-container{position:absolute;left:0;top:0;overflow:hidden}.mat-slider-ticks{background-repeat:repeat;background-clip:content-box;box-sizing:border-box;opacity:0;transition:opacity 400ms cubic-bezier(0.25, 0.8, 0.25, 1)}.mat-slider-thumb-container{position:absolute;z-index:1;transition:transform 400ms cubic-bezier(0.25, 0.8, 0.25, 1)}.mat-slider-focus-ring{position:absolute;width:30px;height:30px;border-radius:50%;transform:scale(0);opacity:0;transition:transform 400ms cubic-bezier(0.25, 0.8, 0.25, 1),background-color 400ms cubic-bezier(0.25, 0.8, 0.25, 1),opacity 400ms cubic-bezier(0.25, 0.8, 0.25, 1)}.mat-slider.cdk-keyboard-focused .mat-slider-focus-ring,.mat-slider.cdk-program-focused .mat-slider-focus-ring{transform:scale(1);opacity:1}.mat-slider:not(.mat-slider-disabled):not(.mat-slider-sliding) .mat-slider-thumb-label,.mat-slider:not(.mat-slider-disabled):not(.mat-slider-sliding) .mat-slider-thumb{cursor:-webkit-grab;cursor:grab}.mat-slider-thumb{position:absolute;right:-10px;bottom:-10px;box-sizing:border-box;width:20px;height:20px;border:3px solid transparent;border-radius:50%;transform:scale(0.7);transition:transform 400ms cubic-bezier(0.25, 0.8, 0.25, 1),background-color 400ms cubic-bezier(0.25, 0.8, 0.25, 1),border-color 400ms cubic-bezier(0.25, 0.8, 0.25, 1)}.mat-slider-thumb-label{display:none;align-items:center;justify-content:center;position:absolute;width:28px;height:28px;border-radius:50%;transition:transform 400ms cubic-bezier(0.25, 0.8, 0.25, 1),border-radius 400ms cubic-bezier(0.25, 0.8, 0.25, 1),background-color 400ms cubic-bezier(0.25, 0.8, 0.25, 1)}.cdk-high-contrast-active .mat-slider-thumb-label{outline:solid 1px}.mat-slider-thumb-label-text{z-index:1;opacity:0;transition:opacity 400ms cubic-bezier(0.25, 0.8, 0.25, 1)}.mat-slider-sliding .mat-slider-track-fill,.mat-slider-sliding .mat-slider-track-background,.mat-slider-sliding .mat-slider-thumb-container{transition-duration:0ms}.mat-slider-has-ticks .mat-slider-wrapper::after{content:\"\";position:absolute;border-width:0;border-style:solid;opacity:0;transition:opacity 400ms cubic-bezier(0.25, 0.8, 0.25, 1)}.mat-slider-has-ticks.cdk-focused:not(.mat-slider-hide-last-tick) .mat-slider-wrapper::after,.mat-slider-has-ticks:hover:not(.mat-slider-hide-last-tick) .mat-slider-wrapper::after{opacity:1}.mat-slider-has-ticks.cdk-focused:not(.mat-slider-disabled) .mat-slider-ticks,.mat-slider-has-ticks:hover:not(.mat-slider-disabled) .mat-slider-ticks{opacity:1}.mat-slider-thumb-label-showing .mat-slider-focus-ring{display:none}.mat-slider-thumb-label-showing .mat-slider-thumb-label{display:flex}.mat-slider-axis-inverted .mat-slider-track-fill{transform-origin:100% 100%}.mat-slider-axis-inverted .mat-slider-track-background{transform-origin:0 0}.mat-slider:not(.mat-slider-disabled).cdk-focused.mat-slider-thumb-label-showing .mat-slider-thumb{transform:scale(0)}.mat-slider:not(.mat-slider-disabled).cdk-focused .mat-slider-thumb-label{border-radius:50% 50% 0}.mat-slider:not(.mat-slider-disabled).cdk-focused .mat-slider-thumb-label-text{opacity:1}.mat-slider:not(.mat-slider-disabled).cdk-mouse-focused .mat-slider-thumb,.mat-slider:not(.mat-slider-disabled).cdk-touch-focused .mat-slider-thumb,.mat-slider:not(.mat-slider-disabled).cdk-program-focused .mat-slider-thumb{border-width:2px;transform:scale(1)}.mat-slider-disabled .mat-slider-focus-ring{transform:scale(0);opacity:0}.mat-slider-disabled .mat-slider-thumb{border-width:4px;transform:scale(0.5)}.mat-slider-disabled .mat-slider-thumb-label{display:none}.mat-slider-horizontal{height:48px;min-width:128px}.mat-slider-horizontal .mat-slider-wrapper{height:2px;top:23px;left:8px;right:8px}.mat-slider-horizontal .mat-slider-wrapper::after{height:2px;border-left-width:2px;right:0;top:0}.mat-slider-horizontal .mat-slider-track-wrapper{height:2px;width:100%}.mat-slider-horizontal .mat-slider-track-fill{height:2px;width:100%;transform:scaleX(0)}.mat-slider-horizontal .mat-slider-track-background{height:2px;width:100%;transform:scaleX(1)}.mat-slider-horizontal .mat-slider-ticks-container{height:2px;width:100%}.cdk-high-contrast-active .mat-slider-horizontal .mat-slider-ticks-container{height:0;outline:solid 2px;top:1px}.mat-slider-horizontal .mat-slider-ticks{height:2px;width:100%}.mat-slider-horizontal .mat-slider-thumb-container{width:100%;height:0;top:50%}.mat-slider-horizontal .mat-slider-focus-ring{top:-15px;right:-15px}.mat-slider-horizontal .mat-slider-thumb-label{right:-14px;top:-40px;transform:translateY(26px) scale(0.01) rotate(45deg)}.mat-slider-horizontal .mat-slider-thumb-label-text{transform:rotate(-45deg)}.mat-slider-horizontal.cdk-focused .mat-slider-thumb-label{transform:rotate(45deg)}.cdk-high-contrast-active .mat-slider-horizontal.cdk-focused .mat-slider-thumb-label,.cdk-high-contrast-active .mat-slider-horizontal.cdk-focused .mat-slider-thumb-label-text{transform:none}.mat-slider-vertical{width:48px;min-height:128px}.mat-slider-vertical .mat-slider-wrapper{width:2px;top:8px;bottom:8px;left:23px}.mat-slider-vertical .mat-slider-wrapper::after{width:2px;border-top-width:2px;bottom:0;left:0}.mat-slider-vertical .mat-slider-track-wrapper{height:100%;width:2px}.mat-slider-vertical .mat-slider-track-fill{height:100%;width:2px;transform:scaleY(0)}.mat-slider-vertical .mat-slider-track-background{height:100%;width:2px;transform:scaleY(1)}.mat-slider-vertical .mat-slider-ticks-container{width:2px;height:100%}.cdk-high-contrast-active .mat-slider-vertical .mat-slider-ticks-container{width:0;outline:solid 2px;left:1px}.mat-slider-vertical .mat-slider-focus-ring{bottom:-15px;left:-15px}.mat-slider-vertical .mat-slider-ticks{width:2px;height:100%}.mat-slider-vertical .mat-slider-thumb-container{height:100%;width:0;left:50%}.mat-slider-vertical .mat-slider-thumb{-webkit-backface-visibility:hidden;backface-visibility:hidden}.mat-slider-vertical .mat-slider-thumb-label{bottom:-14px;left:-40px;transform:translateX(26px) scale(0.01) rotate(-45deg)}.mat-slider-vertical .mat-slider-thumb-label-text{transform:rotate(45deg)}.mat-slider-vertical.cdk-focused .mat-slider-thumb-label{transform:rotate(-45deg)}[dir=rtl] .mat-slider-wrapper::after{left:0;right:auto}[dir=rtl] .mat-slider-horizontal .mat-slider-track-fill{transform-origin:100% 100%}[dir=rtl] .mat-slider-horizontal .mat-slider-track-background{transform-origin:0 0}[dir=rtl] .mat-slider-horizontal.mat-slider-axis-inverted .mat-slider-track-fill{transform-origin:0 0}[dir=rtl] .mat-slider-horizontal.mat-slider-axis-inverted .mat-slider-track-background{transform-origin:100% 100%}.mat-slider._mat-animation-noopable .mat-slider-track-fill,.mat-slider._mat-animation-noopable .mat-slider-track-background,.mat-slider._mat-animation-noopable .mat-slider-ticks,.mat-slider._mat-animation-noopable .mat-slider-thumb-container,.mat-slider._mat-animation-noopable .mat-slider-focus-ring,.mat-slider._mat-animation-noopable .mat-slider-thumb,.mat-slider._mat-animation-noopable .mat-slider-thumb-label,.mat-slider._mat-animation-noopable .mat-slider-thumb-label-text,.mat-slider._mat-animation-noopable .mat-slider-has-ticks .mat-slider-wrapper::after{transition:none}\n"]
        }]
      }];

      MatSlider.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["ElementRef"]
        }, {
          type: _angular_cdk_a11y__WEBPACK_IMPORTED_MODULE_3__["FocusMonitor"]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["ChangeDetectorRef"]
        }, {
          type: _angular_cdk_bidi__WEBPACK_IMPORTED_MODULE_4__["Directionality"],
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Optional"]
          }]
        }, {
          type: String,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Attribute"],
            args: ['tabindex']
          }]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["NgZone"]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Inject"],
            args: [_angular_common__WEBPACK_IMPORTED_MODULE_0__["DOCUMENT"]]
          }]
        }, {
          type: String,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Optional"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Inject"],
            args: [_angular_platform_browser_animations__WEBPACK_IMPORTED_MODULE_8__["ANIMATION_MODULE_TYPE"]]
          }]
        }];
      };

      MatSlider.propDecorators = {
        invert: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"]
        }],
        max: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"]
        }],
        min: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"]
        }],
        step: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"]
        }],
        thumbLabel: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"]
        }],
        tickInterval: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"]
        }],
        value: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"]
        }],
        displayWith: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"]
        }],
        valueText: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"]
        }],
        vertical: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"]
        }],
        change: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Output"]
        }],
        input: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Output"]
        }],
        valueChange: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Output"]
        }],
        _sliderWrapper: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"],
          args: ['sliderWrapper']
        }]
      };
      /** Returns whether an event is a touch event. */

      function isTouchEvent(event) {
        // This function is called for every pixel that the user has dragged so we need it to be
        // as fast as possible. Since we only bind mouse events and touch events, we can assume
        // that if the event's name starts with `t`, it's a touch event.
        return event.type[0] === 't';
      }
      /** Gets the coordinates of a touch or mouse event relative to the viewport. */


      function getPointerPositionOnPage(event) {
        // `touches` will be empty for start/end events so we have to fall back to `changedTouches`.
        var point = isTouchEvent(event) ? event.touches[0] || event.changedTouches[0] : event;
        return {
          x: point.clientX,
          y: point.clientY
        };
      }
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */


      var MatSliderModule = function MatSliderModule() {
        _classCallCheck(this, MatSliderModule);
      };

      MatSliderModule.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"],
        args: [{
          imports: [_angular_common__WEBPACK_IMPORTED_MODULE_0__["CommonModule"], _angular_material_core__WEBPACK_IMPORTED_MODULE_2__["MatCommonModule"]],
          exports: [MatSlider, _angular_material_core__WEBPACK_IMPORTED_MODULE_2__["MatCommonModule"]],
          declarations: [MatSlider]
        }]
      }];
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * Generated bundle index. Do not edit.
       */
      //# sourceMappingURL=slider.js.map

      /***/
    },

    /***/
    "mc/U":
    /*!********************************************************************!*\
      !*** ./src/app/modules/subscriptions/pages/buy/buy.component.scss ***!
      \********************************************************************/

    /*! exports provided: default */

    /***/
    function mcU(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJidXkuY29tcG9uZW50LnNjc3MifQ== */";
      /***/
    },

    /***/
    "treR":
    /*!********************************************************************************!*\
      !*** ./src/@vex/components/secondary-toolbar/secondary-toolbar.component.scss ***!
      \********************************************************************************/

    /*! exports provided: default */

    /***/
    function treR(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = ".secondary-toolbar {\n  background: var(--secondary-toolbar-background);\n  height: var(--secondary-toolbar-height);\n  margin-top: calc(var(--secondary-toolbar-height) * -1);\n}\n\n.secondary-toolbar.fixed {\n  width: var(--toolbar-width);\n}\n\n.secondary-toolbar-placeholder {\n  height: var(--secondary-toolbar-height);\n}\n\n::ng-deep .is-mobile .fixed {\n  width: 100%;\n}\n\n::ng-deep body .fixed {\n  width: calc(100% - var(--sidenav-width));\n}\n\n::ng-deep vex-breadcrumbs {\n  display: none;\n}\n\n@media (min-width: 600px) {\n  ::ng-deep vex-breadcrumbs {\n    display: block;\n  }\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uL3NlY29uZGFyeS10b29sYmFyLmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0VBQ0UsK0NBQUE7RUFDQSx1Q0FBQTtFQUNBLHNEQUFBO0FBQ0Y7O0FBRUE7RUFDRSwyQkFBQTtBQUNGOztBQUVBO0VBQ0UsdUNBQUE7QUFDRjs7QUFFQTtFQUNFLFdBQUE7QUFDRjs7QUFFQTtFQUNFLHdDQUFBO0FBQ0Y7O0FBRUE7RUFDRSxhQUFBO0FBQ0Y7O0FBRUE7RUFDRTtJQUNFLGNBQUE7RUFDRjtBQUNGIiwiZmlsZSI6InNlY29uZGFyeS10b29sYmFyLmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiLnNlY29uZGFyeS10b29sYmFyIHtcbiAgYmFja2dyb3VuZDogdmFyKC0tc2Vjb25kYXJ5LXRvb2xiYXItYmFja2dyb3VuZCk7XG4gIGhlaWdodDogdmFyKC0tc2Vjb25kYXJ5LXRvb2xiYXItaGVpZ2h0KTtcbiAgbWFyZ2luLXRvcDogY2FsYyh2YXIoLS1zZWNvbmRhcnktdG9vbGJhci1oZWlnaHQpICogLTEpO1xufVxuXG4uc2Vjb25kYXJ5LXRvb2xiYXIuZml4ZWQge1xuICB3aWR0aDogdmFyKC0tdG9vbGJhci13aWR0aCk7XG59XG5cbi5zZWNvbmRhcnktdG9vbGJhci1wbGFjZWhvbGRlciB7XG4gIGhlaWdodDogdmFyKC0tc2Vjb25kYXJ5LXRvb2xiYXItaGVpZ2h0KTtcbn1cblxuOjpuZy1kZWVwIC5pcy1tb2JpbGUgLmZpeGVkIHtcbiAgd2lkdGg6IDEwMCU7XG59XG5cbjo6bmctZGVlcCBib2R5IC5maXhlZCB7XG4gIHdpZHRoOiBjYWxjKDEwMCUgLSB2YXIoLS1zaWRlbmF2LXdpZHRoKSk7XG59XG5cbjo6bmctZGVlcCB2ZXgtYnJlYWRjcnVtYnMge1xuICBkaXNwbGF5OiBub25lO1xufVxuXG5AbWVkaWEgKG1pbi13aWR0aDogNjAwcHgpIHtcbiAgOjpuZy1kZWVwIHZleC1icmVhZGNydW1icyB7XG4gICAgZGlzcGxheTogYmxvY2s7XG4gIH1cbn0iXX0= */";
      /***/
    }
  }]);
})();
//# sourceMappingURL=subscriptions-pages-buy-buy-module-es5.js.map