(function () {
  function _get(target, property, receiver) { if (typeof Reflect !== "undefined" && Reflect.get) { _get = Reflect.get; } else { _get = function _get(target, property, receiver) { var base = _superPropBase(target, property); if (!base) return; var desc = Object.getOwnPropertyDescriptor(base, property); if (desc.get) { return desc.get.call(receiver); } return desc.value; }; } return _get(target, property, receiver || target); }

  function _superPropBase(object, property) { while (!Object.prototype.hasOwnProperty.call(object, property)) { object = _getPrototypeOf(object); if (object === null) break; } return object; }

  function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

  function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }

  function _createSuper(Derived) { var hasNativeReflectConstruct = _isNativeReflectConstruct(); return function _createSuperInternal() { var Super = _getPrototypeOf(Derived), result; if (hasNativeReflectConstruct) { var NewTarget = _getPrototypeOf(this).constructor; result = Reflect.construct(Super, arguments, NewTarget); } else { result = Super.apply(this, arguments); } return _possibleConstructorReturn(this, result); }; }

  function _possibleConstructorReturn(self, call) { if (call && (typeof call === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

  function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

  function _isNativeReflectConstruct() { if (typeof Reflect === "undefined" || !Reflect.construct) return false; if (Reflect.construct.sham) return false; if (typeof Proxy === "function") return true; try { Date.prototype.toString.call(Reflect.construct(Date, [], function () {})); return true; } catch (e) { return false; } }

  function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

  function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest(); }

  function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

  function _iterableToArrayLimit(arr, i) { if (typeof Symbol === "undefined" || !(Symbol.iterator in Object(arr))) return; var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

  function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }

  function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread(); }

  function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

  function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

  function _iterableToArray(iter) { if (typeof Symbol !== "undefined" && Symbol.iterator in Object(iter)) return Array.from(iter); }

  function _arrayWithoutHoles(arr) { if (Array.isArray(arr)) return _arrayLikeToArray(arr); }

  function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

  function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

  function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

  function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

  (window["webpackJsonp"] = window["webpackJsonp"] || []).push([["scenarios-scenarios-module"], {
    /***/
    "/74T":
    /*!**************************************************************************************************************************************!*\
      !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/requests/components/scrumboard-dialog/scrumboard-dialog.component.html ***!
      \**************************************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function T(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "<div class=\"mb-0 body-1\" mat-dialog-title>\r\n  <div>\r\n    <h2 class=\"title m-0\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\r\n      {{ request.method }} {{ request.url }}\r\n      <span fxFlex></span>\r\n      <button cdkFocusInitial class=\"text-secondary\" mat-dialog-close mat-icon-button type=\"button\">\r\n        <mat-icon [icIcon]=\"icClose\"></mat-icon>\r\n      </button>\r\n    </h2>\r\n  </div>\r\n\r\n  <mat-divider class=\"-mx-6 mt-6\"></mat-divider>\r\n</div>\r\n\r\n<mat-dialog-content class=\"pb-3 pt-3\">\r\n  <mat-tab-group (selectedTabChange)=\"handleTabChange($event)\">\r\n    <mat-tab [label]=\"response.title\">\r\n      <div class=\"content\">\r\n        <div class=\"p-3\" >\r\n          <h4>Status</h4>\r\n          <mat-divider class=\"my-2\"></mat-divider>\r\n          {{ request.status }}\r\n        </div>\r\n        <div class=\"p-3\" >\r\n          <h4>Body</h4>\r\n          <mat-divider class=\"my-2\"></mat-divider>\r\n          <ng-container *ngIf=\"response.data$ | async as c\" class=\"p-1\">\r\n          <pre>{{ c.length ? prettyJson(c[0].text) : '' }}</pre>\r\n          </ng-container>\r\n        </div>\r\n      </div>\r\n    </mat-tab>\r\n    <mat-tab [label]=\"component.title\"  *ngFor=\"let component of components\">\r\n      <div class=\"content p-3\">\r\n        <ng-container *ngIf=\"component.accessed\">\r\n          <div class=\"p-1\" *ngFor=\"let c of (component.data$ | async)\">\r\n            <b>{{ c.name }}: </b>{{ c.value }}\r\n          </div>\r\n        </ng-container>\r\n      </div>\r\n    </mat-tab>\r\n  </mat-tab-group>\r\n</mat-dialog-content>\r\n";
      /***/
    },

    /***/
    "/7Ly":
    /*!*********************************************************!*\
      !*** ./node_modules/@iconify/icons-ic/twotone-clear.js ***!
      \*********************************************************/

    /*! no static exports found */

    /***/
    function Ly(module, exports) {
      var data = {
        "body": "<path d=\"M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41z\" fill=\"currentColor\"/>",
        "width": 24,
        "height": 24
      };
      exports.__esModule = true;
      exports["default"] = data;
      /***/
    },

    /***/
    "0UTy":
    /*!**********************************************************************************!*\
      !*** ./src/app/modules/requests/services/requests-available-resolver.service.ts ***!
      \**********************************************************************************/

    /*! exports provided: RequestsAvailableResolver */

    /***/
    function UTy(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "RequestsAvailableResolver", function () {
        return RequestsAvailableResolver;
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


      var _core_http_request_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @core/http/request-resource.service */
      "4/Wj");

      var RequestsAvailableResolver = /*#__PURE__*/function () {
        function RequestsAvailableResolver(requestResource) {
          _classCallCheck(this, RequestsAvailableResolver);

          this.requestResource = requestResource;
        }

        _createClass(RequestsAvailableResolver, [{
          key: "resolve",
          value: function resolve(route) {
            return this.requestResource.index({
              project_id: route.queryParams.project_id,
              scenario_id: -1,
              page: route.queryParams.page || 0,
              size: route.queryParams.size || 20
            });
          }
        }]);

        return RequestsAvailableResolver;
      }();

      RequestsAvailableResolver.ctorParameters = function () {
        return [{
          type: _core_http_request_resource_service__WEBPACK_IMPORTED_MODULE_2__["RequestResource"]
        }];
      };

      RequestsAvailableResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], RequestsAvailableResolver);
      /***/
    },

    /***/
    "0w1K":
    /*!*******************************************************************************************************************!*\
      !*** ./src/app/modules/scenarios/pages/scenarios-builder/components/scrumboard-card/scrumboard-card.component.ts ***!
      \*******************************************************************************************************************/

    /*! exports provided: ScrumboardCardComponent */

    /***/
    function w1K(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ScrumboardCardComponent", function () {
        return ScrumboardCardComponent;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _raw_loader_scrumboard_card_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! raw-loader!./scrumboard-card.component.html */
      "Yn9W");
      /* harmony import */


      var _scrumboard_card_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! ./scrumboard-card.component.scss */
      "QMVN");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _iconify_icons_ic_twotone_attach_file__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-attach-file */
      "1kq9");
      /* harmony import */


      var _iconify_icons_ic_twotone_attach_file__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_attach_file__WEBPACK_IMPORTED_MODULE_4__);
      /* harmony import */


      var _iconify_icons_ic_twotone_insert_comment__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-insert-comment */
      "PnnC");
      /* harmony import */


      var _iconify_icons_ic_twotone_insert_comment__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_insert_comment__WEBPACK_IMPORTED_MODULE_5__);
      /* harmony import */


      var _iconify_icons_ic_twotone_notifications__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-notifications */
      "paqc");
      /* harmony import */


      var _iconify_icons_ic_twotone_notifications__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_notifications__WEBPACK_IMPORTED_MODULE_6__);
      /* harmony import */


      var _iconify_icons_ic_twotone_timer__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-timer */
      "De0L");
      /* harmony import */


      var _iconify_icons_ic_twotone_timer__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_timer__WEBPACK_IMPORTED_MODULE_7__);

      var ScrumboardCardComponent = /*#__PURE__*/function () {
        function ScrumboardCardComponent() {
          _classCallCheck(this, ScrumboardCardComponent);

          this.icNotifications = _iconify_icons_ic_twotone_notifications__WEBPACK_IMPORTED_MODULE_6___default.a;
          this.icInsertComment = _iconify_icons_ic_twotone_insert_comment__WEBPACK_IMPORTED_MODULE_5___default.a;
          this.icAttachFile = _iconify_icons_ic_twotone_attach_file__WEBPACK_IMPORTED_MODULE_4___default.a;
          this.icTimer = _iconify_icons_ic_twotone_timer__WEBPACK_IMPORTED_MODULE_7___default.a;
        }

        _createClass(ScrumboardCardComponent, [{
          key: "ngOnInit",
          value: function ngOnInit() {}
        }]);

        return ScrumboardCardComponent;
      }();

      ScrumboardCardComponent.ctorParameters = function () {
        return [];
      };

      ScrumboardCardComponent.propDecorators = {
        wrapped: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"]
        }],
        card: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"]
        }]
      };
      ScrumboardCardComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'scrumboard-card',
        template: _raw_loader_scrumboard_card_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_scrumboard_card_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
      })], ScrumboardCardComponent);
      /***/
    },

    /***/
    "0wNP":
    /*!**********************************************************!*\
      !*** ./src/@vex/pipes/date-tokens/date-tokens.module.ts ***!
      \**********************************************************/

    /*! exports provided: DateTokensModule */

    /***/
    function wNP(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "DateTokensModule", function () {
        return DateTokensModule;
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


      var _date_tokens_pipe__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! ./date-tokens.pipe */
      "W6bZ");

      var DateTokensModule = function DateTokensModule() {
        _classCallCheck(this, DateTokensModule);
      };

      DateTokensModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_date_tokens_pipe__WEBPACK_IMPORTED_MODULE_3__["DateTokensPipe"]],
        exports: [_date_tokens_pipe__WEBPACK_IMPORTED_MODULE_3__["DateTokensPipe"]],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"]]
      })], DateTokensModule);
      /***/
    },

    /***/
    "1kq9":
    /*!***************************************************************!*\
      !*** ./node_modules/@iconify/icons-ic/twotone-attach-file.js ***!
      \***************************************************************/

    /*! no static exports found */

    /***/
    function kq9(module, exports) {
      var data = {
        "body": "<path d=\"M12.5 23c3.04 0 5.5-2.46 5.5-5.5V6h-1.5v11.5c0 2.21-1.79 4-4 4s-4-1.79-4-4V5a2.5 2.5 0 0 1 5 0v10.5c0 .55-.45 1-1 1s-1-.45-1-1V6H10v9.5a2.5 2.5 0 0 0 5 0V5c0-2.21-1.79-4-4-4S7 2.79 7 5v12.5c0 3.04 2.46 5.5 5.5 5.5z\" fill=\"currentColor\"/>",
        "width": 24,
        "height": 24
      };
      exports.__esModule = true;
      exports["default"] = data;
      /***/
    },

    /***/
    "3ZMo":
    /*!******************************************************************************************!*\
      !*** ./src/app/modules/scenarios/components/scenarios-create/scenarios-create.module.ts ***!
      \******************************************************************************************/

    /*! exports provided: ScenariosCreateModule */

    /***/
    function ZMo(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ScenariosCreateModule", function () {
        return ScenariosCreateModule;
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


      var _angular_material_core__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/material/core */
      "UhP/");
      /* harmony import */


      var _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @angular/material/datepicker */
      "TN/R");
      /* harmony import */


      var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @angular/material/dialog */
      "iELJ");
      /* harmony import */


      var _angular_material_divider__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @angular/material/divider */
      "BSbQ");
      /* harmony import */


      var _angular_material_icon__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @angular/material/icon */
      "Tj54");
      /* harmony import */


      var _angular_material_input__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @angular/material/input */
      "e6WT");
      /* harmony import */


      var _angular_material_menu__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @angular/material/menu */
      "rJgo");
      /* harmony import */


      var _angular_material_tabs__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @angular/material/tabs */
      "M9ds");
      /* harmony import */


      var _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! @angular/material/tooltip */
      "ZFy/");
      /* harmony import */


      var ngx_dropzone__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! ngx-dropzone */
      "tq8E");
      /* harmony import */


      var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(
      /*! @visurel/iconify-angular */
      "l+Q0");
      /* harmony import */


      var _scenarios_create_component__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(
      /*! ./scenarios-create.component */
      "lAmD");

      var ScenariosCreateModule = function ScenariosCreateModule() {
        _classCallCheck(this, ScenariosCreateModule);
      };

      ScenariosCreateModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_scenarios_create_component__WEBPACK_IMPORTED_MODULE_17__["ScenariosCreateComponent"]],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"], _angular_material_dialog__WEBPACK_IMPORTED_MODULE_8__["MatDialogModule"], _angular_material_icon__WEBPACK_IMPORTED_MODULE_10__["MatIconModule"], _angular_material_input__WEBPACK_IMPORTED_MODULE_11__["MatInputModule"], _angular_material_divider__WEBPACK_IMPORTED_MODULE_9__["MatDividerModule"], _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_7__["MatDatepickerModule"], _angular_material_menu__WEBPACK_IMPORTED_MODULE_12__["MatMenuModule"], _angular_material_button__WEBPACK_IMPORTED_MODULE_5__["MatButtonModule"], _angular_material_core__WEBPACK_IMPORTED_MODULE_6__["MatNativeDateModule"], _angular_material_tabs__WEBPACK_IMPORTED_MODULE_13__["MatTabsModule"], _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_14__["MatTooltipModule"], _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_16__["IconModule"], ngx_dropzone__WEBPACK_IMPORTED_MODULE_15__["NgxDropzoneModule"]],
        entryComponents: [_scenarios_create_component__WEBPACK_IMPORTED_MODULE_17__["ScenariosCreateComponent"]]
      })], ScenariosCreateModule);
      /***/
    },

    /***/
    "41Lq":
    /*!***************************************************************************************************************!*\
      !*** ./src/app/modules/scenarios/pages/scenario-details/components/requests-create/requests-create.module.ts ***!
      \***************************************************************************************************************/

    /*! exports provided: RequestsCreateModule */

    /***/
    function Lq(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "RequestsCreateModule", function () {
        return RequestsCreateModule;
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


      var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/material/dialog */
      "iELJ");
      /* harmony import */


      var _angular_material_divider__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @angular/material/divider */
      "BSbQ");
      /* harmony import */


      var _angular_material_icon__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @angular/material/icon */
      "Tj54");
      /* harmony import */


      var _angular_material_input__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @angular/material/input */
      "e6WT");
      /* harmony import */


      var _angular_material_menu__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @angular/material/menu */
      "rJgo");
      /* harmony import */


      var _angular_material_radio__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @angular/material/radio */
      "zQhy");
      /* harmony import */


      var _angular_material_select__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @angular/material/select */
      "ZTz/");
      /* harmony import */


      var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @visurel/iconify-angular */
      "l+Q0");
      /* harmony import */


      var ngx_dropzone__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! ngx-dropzone */
      "tq8E");
      /* harmony import */


      var _requests_create_component__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! ./requests-create.component */
      "hnRQ");

      var RequestsCreateModule = function RequestsCreateModule() {
        _classCallCheck(this, RequestsCreateModule);
      };

      RequestsCreateModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"], _angular_material_dialog__WEBPACK_IMPORTED_MODULE_6__["MatDialogModule"], _angular_material_input__WEBPACK_IMPORTED_MODULE_9__["MatInputModule"], _angular_material_button__WEBPACK_IMPORTED_MODULE_5__["MatButtonModule"], _angular_material_icon__WEBPACK_IMPORTED_MODULE_8__["MatIconModule"], _angular_material_radio__WEBPACK_IMPORTED_MODULE_11__["MatRadioModule"], _angular_material_select__WEBPACK_IMPORTED_MODULE_12__["MatSelectModule"], _angular_material_menu__WEBPACK_IMPORTED_MODULE_10__["MatMenuModule"], _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_13__["IconModule"], _angular_material_divider__WEBPACK_IMPORTED_MODULE_7__["MatDividerModule"], ngx_dropzone__WEBPACK_IMPORTED_MODULE_14__["NgxDropzoneModule"]],
        declarations: [_requests_create_component__WEBPACK_IMPORTED_MODULE_15__["RequestsCreateComponent"]],
        entryComponents: [_requests_create_component__WEBPACK_IMPORTED_MODULE_15__["RequestsCreateComponent"]],
        exports: [_requests_create_component__WEBPACK_IMPORTED_MODULE_15__["RequestsCreateComponent"]]
      })], RequestsCreateModule);
      /***/
    },

    /***/
    "4BTo":
    /*!******************************************************************************************!*\
      !*** ./src/app/modules/scenarios/pages/scenarios-builder/scenarios-builder.component.ts ***!
      \******************************************************************************************/

    /*! exports provided: ScenariosBuilderComponent */

    /***/
    function BTo(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ScenariosBuilderComponent", function () {
        return ScenariosBuilderComponent;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _raw_loader_scenarios_builder_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! raw-loader!./scenarios-builder.component.html */
      "AvvF");
      /* harmony import */


      var _scenarios_builder_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! ./scenarios-builder.component.scss */
      "D3rM");
      /* harmony import */


      var _angular_cdk_drag_drop__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/cdk/drag-drop */
      "ltgo");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_forms__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/forms */
      "s7LF");
      /* harmony import */


      var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/material/dialog */
      "iELJ");
      /* harmony import */


      var _angular_router__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @angular/router */
      "iInd");
      /* harmony import */


      var rxjs_operators__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! rxjs/operators */
      "kU1M");
      /* harmony import */


      var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-close */
      "5mnX");
      /* harmony import */


      var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_9__);
      /* harmony import */


      var _vex_animations__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @vex/animations */
      "ORuP");
      /* harmony import */


      var _vex_components_popover_popover_service__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @vex/components/popover/popover.service */
      "kYjG");
      /* harmony import */


      var _core_http_request_resource_service__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @core/http/request-resource.service */
      "4/Wj");
      /* harmony import */


      var _data_schema__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @data/schema */
      "V99k");
      /* harmony import */


      var _requests_components_scrumboard_dialog_scrumboard_dialog_component__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! @requests/components/scrumboard-dialog/scrumboard-dialog.component */
      "QgCS");
      /* harmony import */


      var _services_request_card_adapter_service__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! ./services/request-card-adapter.service */
      "hh0J");
      /* harmony import */


      var _services_scenarios_builder_icons_service__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(
      /*! ./services/scenarios-builder-icons.service */
      "tmbL");

      var ScenariosBuilderComponent = /*#__PURE__*/function () {
        function ScenariosBuilderComponent(dialog, route, popover, requestCardAdapterService, requestResource, icons) {
          _classCallCheck(this, ScenariosBuilderComponent);

          this.dialog = dialog;
          this.route = route;
          this.popover = popover;
          this.requestCardAdapterService = requestCardAdapterService;
          this.requestResource = requestResource;
          this.icons = icons;
          this.layoutCtrl = new _angular_forms__WEBPACK_IMPORTED_MODULE_5__["FormControl"]('fullwidth');
          this.SCENARIO_CONTAINER_ID = 1;
          this.REQUESTS_CONTAINER_ID = 2;
          this.crumbs = [];
          this.board = {
            id: 1,
            label: '',
            children: []
          };
          this.scenarioRequestsList = {
            id: this.SCENARIO_CONTAINER_ID,
            label: 'Requests',
            children: []
          };
          this.availableRequestsList = {
            id: this.REQUESTS_CONTAINER_ID,
            label: 'Available Requests',
            children: []
          }; // this.route.paramMap.pipe(
          //   map(paramMap => +paramMap.get('scrumboardId')),
          //   map(scrumboardId => scrumboards.find(board => board.id === 1))
          // );

          this.addCardCtrl = new _angular_forms__WEBPACK_IMPORTED_MODULE_5__["FormControl"]();
          this.addListCtrl = new _angular_forms__WEBPACK_IMPORTED_MODULE_5__["FormControl"]();
          this.showAddRequests = false;
          this.icClose = _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_9___default.a;
        }

        _createClass(ScenariosBuilderComponent, [{
          key: "ngOnInit",
          value: function ngOnInit() {
            this.scenario = new _data_schema__WEBPACK_IMPORTED_MODULE_13__["Scenario"](this.route.snapshot.data.scenario);
            this.project = new _data_schema__WEBPACK_IMPORTED_MODULE_13__["Project"](this.route.snapshot.data.project);
            this.board.label = this.scenario.name;
            this.board.children.push(this.scenarioRequestsList);
            this.board.children.push(this.availableRequestsList);
            this.buildRequests();
            this.buildAvailableRequests(this.route.snapshot.data.requestsAvailable);
            this.buildCrumbs();
          }
        }, {
          key: "searchAvailableRequests",
          value: function searchAvailableRequests(queryString) {
            var _this2 = this;

            var snapshot = this.route.snapshot;
            var project_id = snapshot.queryParams.project_id;
            var query = {
              project_id: project_id,
              scenario_id: -1,
              q: queryString,
              page: this.availableRequestsList.search.page,
              size: this.availableRequestsList.search.size
            };
            this.requestResource.index(query).subscribe(function (res) {
              _this2.buildAvailableRequests(res);

              _this2.availableRequestsList.search.total = res.total;
              _this2.availableRequestsList.search.q = queryString;
            });
          } // View Access

        }, {
          key: "open",
          value: function open(board, list, card) {
            // this.addCardCtrl.setValue(null);
            var request = this.requests.find(function (request) {
              return request.id === card.id;
            });

            if (!request) {
              request = this.requestsAvailable.find(function (request) {
                return request.id === card.id;
              });
            }

            this.dialog.open(_requests_components_scrumboard_dialog_scrumboard_dialog_component__WEBPACK_IMPORTED_MODULE_14__["ScrumboardDialogComponent"], {
              data: {
                request: request
              },
              width: '750px',
              maxWidth: '100%',
              disableClose: true
            }).beforeClosed().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_8__["filter"])(Boolean)).subscribe(function (value) {// Do something after dialog is closed
            });
          }
          /*
           * Enable dropping requests/endpoints into only scenario container
           *
           */

        }, {
          key: "drop",
          value: function drop(event) {
            var _this3 = this;

            if (event.container.id !== this.SCENARIO_CONTAINER_ID.toString()) {
              return;
            }

            var requestId = event.item.data.id;
            var nextPosition = event.currentIndex;

            if (event.previousContainer === event.container) {
              // If moving position of request in scenario
              var request = this.requests.find(function (request) {
                return request.id === requestId;
              });
              var curPosition = request.position;
              this.requestResource.update(request.id, {
                position: nextPosition
              }).subscribe(function (res) {
                var r1 = _this3.requests[curPosition];
                var r2 = _this3.requests[nextPosition];
                r1.position = nextPosition;
                r2.position = curPosition;

                _this3.buildRequests();
              });
              Object(_angular_cdk_drag_drop__WEBPACK_IMPORTED_MODULE_3__["moveItemInArray"])(event.container.data, event.previousIndex, event.currentIndex);
            } else {
              // If moving request from availableRequests
              this.requestResource.update(event.item.data.id, {
                scenario_id: this.scenario.id,
                position: nextPosition
              }).subscribe(function (res) {
                var request = _this3.requestsAvailable.find(function (request) {
                  return request.id === requestId;
                });

                request.position = nextPosition;

                _this3.requests.splice(nextPosition, 0, request);

                for (var i = 0; i < _this3.requests.length; ++i) {
                  _this3.requests[i].position = i;
                }

                _this3.buildRequests();
              });
              Object(_angular_cdk_drag_drop__WEBPACK_IMPORTED_MODULE_3__["transferArrayItem"])(event.previousContainer.data, event.container.data, event.previousIndex, event.currentIndex);
            }
          }
        }, {
          key: "toggleStar",
          value: function toggleStar(board) {
            board.starred = !board.starred;
          }
        }, {
          key: "toggleAddRequests",
          value: function toggleAddRequests() {
            this.showAddRequests = !this.showAddRequests;
          } // Helpers

        }, {
          key: "getConnectedList",
          value: function getConnectedList(board) {
            return board.children.map(function (x) {
              return "".concat(x.id);
            });
          }
        }, {
          key: "buildCrumbs",
          value: function buildCrumbs() {
            this.crumbs.push({
              name: this.project.name
            });
            this.crumbs.push({
              name: 'Scenarios',
              routerLink: ['/scenarios'],
              queryParams: this.route.snapshot.queryParams
            });
            this.crumbs.push({
              name: this.scenario.name,
              routerLink: ["/scenarios/".concat(this.scenario.id)],
              queryParams: this.route.snapshot.queryParams
            });
            this.crumbs.push({
              name: 'Editor'
            });
          }
        }, {
          key: "buildRequests",
          value: function buildRequests() {
            var requestsData = this.route.snapshot.data.requests;
            this.requests = requestsData.list;
            this.requests.sort(function (a, b) {
              return a.position - b.position;
            });
            this.buildListChildren(this.scenarioRequestsList, this.requests);
          }
        }, {
          key: "buildAvailableRequests",
          value: function buildAvailableRequests(requests) {
            var _this = this;

            var requestsAvailableData = requests;
            this.requestsAvailable = requestsAvailableData.list;
            this.buildListChildren(this.availableRequestsList, requestsAvailableData.list);
            this.availableRequestsList.search = {
              q: '',
              page: 0,
              size: 25,
              total: requestsAvailableData.total,
              // ctrl: new FormControl(),
              label: 'Search Requests...',
              // get str$() {
              //   return this.ctrl.valueChanges.pipe(
              //     debounceTime(1000)
              //   )
              // },
              onScroll: function onScroll() {
                this.page += 1;

                _this.searchAvailableRequests(this.q || '');
              }
            }; // this.availableRequestsList.search.str$.subscribe(this.searchAvailableRequests.bind(this));
          }
        }, {
          key: "buildListChildren",
          value: function buildListChildren(list, requests) {
            var _this4 = this;

            list.children = requests.map(function (request) {
              var scrumboardCard = _this4.requestCardAdapterService.createCard(new _data_schema__WEBPACK_IMPORTED_MODULE_13__["Request"](request));

              return scrumboardCard;
            });
          }
        }]);

        return ScenariosBuilderComponent;
      }();

      ScenariosBuilderComponent.ctorParameters = function () {
        return [{
          type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_6__["MatDialog"]
        }, {
          type: _angular_router__WEBPACK_IMPORTED_MODULE_7__["ActivatedRoute"]
        }, {
          type: _vex_components_popover_popover_service__WEBPACK_IMPORTED_MODULE_11__["PopoverService"]
        }, {
          type: _services_request_card_adapter_service__WEBPACK_IMPORTED_MODULE_15__["RequestCardAdapterService"]
        }, {
          type: _core_http_request_resource_service__WEBPACK_IMPORTED_MODULE_12__["RequestResource"]
        }, {
          type: _services_scenarios_builder_icons_service__WEBPACK_IMPORTED_MODULE_16__["ScenariosBuilderIcons"]
        }];
      };

      ScenariosBuilderComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_4__["Component"])({
        selector: 'vex-scenarios-builder',
        template: _raw_loader_scenarios_builder_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        animations: [_vex_animations__WEBPACK_IMPORTED_MODULE_10__["stagger80ms"], _vex_animations__WEBPACK_IMPORTED_MODULE_10__["fadeInUp400ms"]],
        styles: [_scenarios_builder_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
      })], ScenariosBuilderComponent);
      /***/
    },

    /***/
    "4EXa":
    /*!*********************************************************!*\
      !*** ./node_modules/@iconify/icons-ic/twotone-title.js ***!
      \*********************************************************/

    /*! no static exports found */

    /***/
    function EXa(module, exports) {
      var data = {
        "body": "<path d=\"M5 7h5.5v12h3V7H19V4H5z\" fill=\"currentColor\"/>",
        "width": 24,
        "height": 24
      };
      exports.__esModule = true;
      exports["default"] = data;
      /***/
    },

    /***/
    "5euU":
    /*!*****************************************************************************************************!*\
      !*** ./src/app/modules/scenarios/pages/scenario-details/services/scenario-details-icons.service.ts ***!
      \*****************************************************************************************************/

    /*! exports provided: ScenarioDetailsIcons */

    /***/
    function euU(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ScenarioDetailsIcons", function () {
        return ScenarioDetailsIcons;
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


      var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-add */
      "7wwx");
      /* harmony import */


      var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_2__);
      /* harmony import */


      var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-delete */
      "e3EN");
      /* harmony import */


      var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_3__);
      /* harmony import */


      var _iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-edit */
      "pN9m");
      /* harmony import */


      var _iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_4__);
      /* harmony import */


      var _iconify_icons_ic_twotone_filter_list__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-filter-list */
      "+4LO");
      /* harmony import */


      var _iconify_icons_ic_twotone_filter_list__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_filter_list__WEBPACK_IMPORTED_MODULE_5__);
      /* harmony import */


      var _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-search */
      "sF+I");
      /* harmony import */


      var _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_6__);

      var ScenarioDetailsIcons = function ScenarioDetailsIcons() {
        _classCallCheck(this, ScenarioDetailsIcons);

        this.icSearch = _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_6___default.a;
        this.icDelete = _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_3___default.a;
        this.icAdd = _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_2___default.a;
        this.icFilterList = _iconify_icons_ic_twotone_filter_list__WEBPACK_IMPORTED_MODULE_5___default.a;
        this.icEdit = _iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_4___default.a;
      };

      ScenarioDetailsIcons.ctorParameters = function () {
        return [];
      };

      ScenarioDetailsIcons = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])()], ScenarioDetailsIcons);
      /***/
    },

    /***/
    "5x1r":
    /*!*****************************************************************************************************************************!*\
      !*** ./src/app/modules/scenarios/pages/scenarios-index/components/scenarios-data-table/scenarios-data-table.component.scss ***!
      \*****************************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function x1r(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzY2VuYXJpb3MtZGF0YS10YWJsZS5jb21wb25lbnQuc2NzcyJ9 */";
      /***/
    },

    /***/
    "9Gul":
    /*!***********************************************************************************************!*\
      !*** ./src/app/modules/scenarios/components/scenarios-create/scenarios-create.component.scss ***!
      \***********************************************************************************************/

    /*! exports provided: default */

    /***/
    function Gul(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzY2VuYXJpb3MtY3JlYXRlLmNvbXBvbmVudC5zY3NzIn0= */";
      /***/
    },

    /***/
    "A7TT":
    /*!**************************************************************!*\
      !*** ./src/app/shared/pipes/request-component-label.pipe.ts ***!
      \**************************************************************/

    /*! exports provided: RequestComponentLabelPipe */

    /***/
    function A7TT(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "RequestComponentLabelPipe", function () {
        return RequestComponentLabelPipe;
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


      var _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @vex/utils/tailwindcss */
      "XXSj");
      /* harmony import */


      var color__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! color */
      "aSns");
      /* harmony import */


      var color__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(color__WEBPACK_IMPORTED_MODULE_3__);

      var RequestComponentLabelPipe = /*#__PURE__*/function () {
        function RequestComponentLabelPipe() {
          _classCallCheck(this, RequestComponentLabelPipe);

          this.labels = {
            headers: {
              text: 'Headers',
              backgroundColor: color__WEBPACK_IMPORTED_MODULE_3___default()(_vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_2__["default"].colors.green['500']).fade(0.9),
              color: _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_2__["default"].colors.green['500']
            },
            query_params: {
              text: 'Query Params',
              backgroundColor: color__WEBPACK_IMPORTED_MODULE_3___default()(_vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_2__["default"].colors.cyan['500']).fade(0.9),
              color: _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_2__["default"].colors.cyan['500']
            },
            body_params: {
              text: 'Body Params',
              backgroundColor: color__WEBPACK_IMPORTED_MODULE_3___default()(_vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_2__["default"].colors.teal['500']).fade(0.9),
              color: _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_2__["default"].colors.teal['500']
            },
            response: {
              text: 'Response',
              backgroundColor: color__WEBPACK_IMPORTED_MODULE_3___default()(_vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_2__["default"].colors.purple['500']).fade(0.9),
              color: _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_2__["default"].colors.purple['500']
            }
          };
        }

        _createClass(RequestComponentLabelPipe, [{
          key: "transform",
          value: function transform(labels) {
            var _this5 = this;

            return labels.map(function (label) {
              return _this5.labels[label];
            });
          }
        }]);

        return RequestComponentLabelPipe;
      }();

      RequestComponentLabelPipe = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Pipe"])({
        name: 'requestComponentLabel'
      })], RequestComponentLabelPipe);
      /***/
    },

    /***/
    "AvvF":
    /*!**********************************************************************************************************************************!*\
      !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/scenarios/pages/scenarios-builder/scenarios-builder.component.html ***!
      \**********************************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function AvvF(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "<vex-page-layout>\r\n\r\n  <vex-page-layout-header class=\"pb-16 vex-layout-theme\" fxLayout=\"column\" fxLayoutAlign=\"center start\">\r\n    <div [class.container]=\"layoutCtrl.value === 'boxed'\"\r\n         [class.px-gutter]=\"layoutCtrl.value === 'fullwidth'\"\r\n         class=\"w-full flex flex-col sm:flex-row justify-between\">\r\n      <div>\r\n        <h1 class=\"title mt-0 mb-1\">Scenario Editor</h1>\r\n        <vex-breadcrumbs [crumbs]=\"crumbs\"></vex-breadcrumbs>\r\n      </div>\r\n    </div>\r\n  </vex-page-layout-header>\r\n\r\n  <div class=\"-mt-14 pt-0 overflow-hidden flex\">\r\n    <div class=\"h-full w-full overflow-hidden  scrumboard-list\" fxLayout=\"column\">\r\n      <!-- <div class=\"py-4 px-gutter\" fxFlex=\"none\" fxLayout=\"row\" fxLayoutAlign=\"start center\" vexContainer>\r\n        <button (click)=\"toggleStar(board)\" mat-icon-button type=\"button\">\r\n          <mat-icon *ngIf=\"board.starred\" [icIcon]=\"icons.icStar\" class=\"text-amber-500\"></mat-icon>\r\n          <mat-icon *ngIf=\"!board.starred\" [icIcon]=\"icons.icStarBorder\"></mat-icon>\r\n        </button>\r\n        <h1 class=\"title m-0\">Edit {{ board.label }}</h1>\r\n\r\n        <span fxFlex></span>\r\n\r\n        <div *ngIf=\"scrumboardUsers?.length > 0\" fxFlex fxLayout=\"row\" fxLayoutAlign=\"end center\">\r\n          <img *ngFor=\"let user of scrumboardUsers\"\r\n               [matTooltip]=\"user.name\"\r\n               [src]=\"user.imageSrc\"\r\n               class=\"avatar overlapping\">\r\n        </div>\r\n      </div> -->\r\n\r\n      <div @stagger\r\n           class=\"px-gutter pb-gutter min-h-0 overflow-x-auto\"\r\n           fxFlex=\"auto\"\r\n           fxLayout=\"row\"\r\n           fxLayoutAlign=\"center\"\r\n           fxLayoutGap=\"24px\"\r\n           vexContainer\r\n       >\r\n\r\n       <div\r\n          @fadeInUp\r\n          cdkDropListGroup\r\n          class=\"rounded bg-app-bar overflow-auto card\"\r\n          fxFlex=\"auto\"\r\n          fxLayout=\"column\"\r\n          infiniteScroll\r\n          [scrollWindow]=\"false\"\r\n          [infiniteScrollDistance]=\"2\"\r\n          [infiniteScrollThrottle]=\"50\"\r\n        >\r\n          <div cdkDragHandle class=\"p-4\" fxFlex=\"none\" fxLayoutAlign=\"start center\">\r\n            <!-- <h2 class=\"subheading-2 font-medium m-0 select-none\" fxFlex=\"none\">\r\n              {{ scenarioRequestsList.label }}\r\n            </h2> -->\r\n\r\n            <button\r\n              [disabled]=\"showAddRequests\"\r\n              (click)=\"toggleAddRequests()\"\r\n              mat-raised-button\r\n              color=\"primary\"\r\n            >\r\n              ADD REQUEST\r\n            </button>\r\n          </div>\r\n\r\n          <!--\r\n            For each card...\r\n          -->\r\n          <div class=\"flex-auto vexScrollbar\">\r\n            <div (cdkDropListDropped)=\"drop($event)\"\r\n                 [cdkDropListConnectedTo]=\"getConnectedList(board)\"\r\n                 [cdkDropListData]=\"scenarioRequestsList.children\"\r\n                 cdkDropList\r\n                 class=\"px-4 pb-4 scrumboard-drop-zone\"\r\n                 id=\"{{ scenarioRequestsList.id }}\">\r\n\r\n              <div (click)=\"open(board, scenarioRequestsList, card)\"\r\n                   *ngFor=\"let card of scenarioRequestsList.children\"\r\n                   [cdkDragData]=\"card\"\r\n                   cdkDrag\r\n                   class=\"scrumboard-card card w-full cursor-pointer overflow-hidden\">\r\n                <scrumboard-card [wrapped]=\"showAddRequests\" [card]=\"card\"></scrumboard-card>\r\n              </div>\r\n            </div>\r\n          </div>\r\n        </div>\r\n\r\n        <div\r\n          *ngIf=\"showAddRequests\"\r\n          @fadeInUp\r\n          cdkDropListGroup\r\n          class=\"rounded bg-app-bar overflow-auto card\"\r\n          fxFlex=\"50\"\r\n          fxLayout=\"column\"\r\n          infiniteScroll\r\n          [scrollWindow]=\"false\"\r\n          [infiniteScrollDistance]=\"2\"\r\n          [infiniteScrollThrottle]=\"50\"\r\n          [infiniteScrollDisabled]=\"false\"\r\n          (scrolled)=\"availableRequestsList.search.onScroll()\"\r\n        >\r\n          <div cdkDragHandle class=\"p-4\" fxFlex=\"none\" fxLayoutAlign=\"start center\">\r\n            <h2 class=\"subheading-2 font-medium m-0 select-none\" fxFlex=\"none\">\r\n              {{ availableRequestsList.label }}\r\n            </h2>\r\n            <span fxFlex></span>\r\n            <button\r\n              (click)=\"toggleAddRequests()\"\r\n              mat-icon-button\r\n            >\r\n              <mat-icon [icIcon]=\"icClose\"></mat-icon>\r\n            </button>\r\n          </div>\r\n\r\n          <requests-search\r\n            class=\"pl-4 pr-4 pb-4\"\r\n            *ngIf=\"availableRequestsList.search\"\r\n            [projectId]=\"scenario.projectId\"\r\n            (search)=\"searchAvailableRequests($event)\"\r\n          >\r\n          </requests-search>\r\n\r\n          <!--\r\n            For each card...\r\n          -->\r\n          <div class=\"flex-auto vexScrollbar\">\r\n            <div (cdkDropListDropped)=\"drop($event)\"\r\n                 [cdkDropListConnectedTo]=\"getConnectedList(board)\"\r\n                 [cdkDropListData]=\"availableRequestsList.children\"\r\n                 cdkDropList\r\n                 class=\"px-4 pb-4\"\r\n                 id=\"{{ availableRequestsList.id }}\">\r\n\r\n              <div (click)=\"open(board, availableRequestsList, card)\"\r\n                   *ngFor=\"let card of availableRequestsList.children\"\r\n                   [cdkDragData]=\"card\"\r\n                   cdkDrag\r\n                   class=\"scrumboard-card card w-full cursor-pointer overflow-hidden\">\r\n                <scrumboard-card [wrapped]=\"true\" [card]=\"card\"></scrumboard-card>\r\n              </div>\r\n            </div>\r\n          </div>\r\n        </div>\r\n\r\n        <!-- <div #addListOriginRef class=\"w-full max-w-xxs rounded bg-app-bar\" fxFlex=\"none\">\r\n          <ng-template #addListTemplate let-close=\"close\">\r\n            <div class=\"card px-4 pt-3 pb-2\">\r\n              <mat-form-field class=\"vex-dense-form-field\">\r\n                <mat-label>List Title</mat-label>\r\n                <input [formControl]=\"addListCtrl\" matInput placeholder=\"Enter your title...\">\r\n              </mat-form-field>\r\n\r\n              <div class=\"mt-3\" fxLayout=\"row\" fxLayoutAlign=\"space-between center\">\r\n                <button (click)=\"close()\" class=\"text-secondary w-8 h-8 leading-none\" mat-icon-button type=\"button\">\r\n                  <mat-icon [icIcon]=\"icons.icClose\" size=\"18px\"></mat-icon>\r\n                </button>\r\n                <button (click)=\"createList(board, close)\" color=\"primary\" mat-button type=\"button\">CREATE</button>\r\n              </div>\r\n            </div>\r\n          </ng-template>\r\n\r\n          <button (click)=\"openAddList(board, addListTemplate, addListOriginRef)\"\r\n                  class=\"w-full\"\r\n                  mat-button\r\n                  type=\"button\">\r\n            <ic-icon [icon]=\"icons.icAdd\" class=\"mr-1 -ml-1\" inline=\"true\"></ic-icon>\r\n            <span>ADD LIST</span>\r\n          </button>\r\n        </div> -->\r\n      </div>\r\n    </div>\r\n  </div>\r\n</vex-page-layout>\r\n";
      /***/
    },

    /***/
    "Bavy":
    /*!*******************************************************!*\
      !*** ./src/app/modules/scenarios/scenarios.module.ts ***!
      \*******************************************************/

    /*! exports provided: ScenariosModule */

    /***/
    function Bavy(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ScenariosModule", function () {
        return ScenariosModule;
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


      var _pages_scenario_details_scenario_details_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! ./pages/scenario-details/scenario-details.module */
      "KMsL");
      /* harmony import */


      var _pages_scenarios_builder_scenarios_builder_module__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! ./pages/scenarios-builder/scenarios-builder.module */
      "eha6");
      /* harmony import */


      var _pages_scenarios_index_scenarios_index_module__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! ./pages/scenarios-index/scenarios-index.module */
      "ndZO");
      /* harmony import */


      var _scenarios_routing_module__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! ./scenarios-routing.module */
      "IhNm");
      /* harmony import */


      var _requests_pages_request_details_request_details_module__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @requests/pages/request-details/request-details.module */
      "9CFt");

      var ScenariosModule = function ScenariosModule() {
        _classCallCheck(this, ScenariosModule);
      };

      ScenariosModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _pages_scenarios_builder_scenarios_builder_module__WEBPACK_IMPORTED_MODULE_4__["ScenariosBuilderModule"], _pages_scenarios_index_scenarios_index_module__WEBPACK_IMPORTED_MODULE_5__["ScenariosIndexModule"], _pages_scenario_details_scenario_details_module__WEBPACK_IMPORTED_MODULE_3__["ScenarioDetailsModule"], _scenarios_routing_module__WEBPACK_IMPORTED_MODULE_6__["ScenariosRoutingModule"], _requests_pages_request_details_request_details_module__WEBPACK_IMPORTED_MODULE_7__["RequestDetailsModule"]]
      })], ScenariosModule);
      /***/
    },

    /***/
    "D3rM":
    /*!********************************************************************************************!*\
      !*** ./src/app/modules/scenarios/pages/scenarios-builder/scenarios-builder.component.scss ***!
      \********************************************************************************************/

    /*! exports provided: default */

    /***/
    function D3rM(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "::ng-deep .vex-style-dark vex-scrumboard .scrumboard-card:hover {\n  background: rgba(0, 0, 0, 0.5);\n}\n\n.scrumboard-drop-zone {\n  min-height: 250px;\n}\n\n.scrumboard-list {\n  height: calc(100vh - 65px);\n}\n\n.scrumboard-card {\n  margin-bottom: var(--padding-8);\n  cursor: move;\n}\n\n.scrumboard-card:last-of-type {\n  margin-bottom: 0;\n}\n\n.scrumboard-card:hover {\n  background: rgba(255, 255, 255, 0.5);\n}\n\n.scrumboard-card .label {\n  border-radius: 6px;\n  height: 6px;\n  max-width: 32px;\n}\n\n.scrumboard-card .box {\n  padding: 3px;\n}\n\n.scrumboard-card .box .box-text {\n  font-size: 11px;\n  font-weight: var(--font-weight-medium);\n  margin-left: 3px;\n  margin-right: 3px;\n  vertical-align: bottom;\n}\n\n.avatar.overlapping {\n  border: 2px solid var(--background-card);\n  height: 23px;\n  margin-right: -8px;\n  width: 23px;\n}\n\n.avatar.overlapping:last-of-type {\n  margin-right: 0;\n}\n\n/*\n  Cdk Drag & Drop\n */\n\n.cdk-drag-preview {\n  box-shadow: var(--elevation-z8);\n}\n\n.cdk-drag-placeholder {\n  opacity: 0.2;\n}\n\n.cdk-drop-list-dragging .scrumboard-card:not(.cdk-drag-placeholder) {\n  transition: transform 250ms cubic-bezier(0, 0, 0.2, 1);\n}\n\n.cdk-drag-animating {\n  transition: transform 250ms cubic-bezier(0, 0, 0.2, 1) !important;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uLy4uL3NjZW5hcmlvcy1idWlsZGVyLmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0VBQ0UsOEJBQUE7QUFDRjs7QUFFQTtFQUNFLGlCQUFBO0FBQ0Y7O0FBRUE7RUFDRSwwQkFBQTtBQUNGOztBQUVBO0VBQ0UsK0JBQUE7RUFDQSxZQUFBO0FBQ0Y7O0FBRUE7RUFDRSxnQkFBQTtBQUNGOztBQUVBO0VBQ0Usb0NBQUE7QUFDRjs7QUFFQTtFQUNFLGtCQUFBO0VBQ0EsV0FBQTtFQUNBLGVBQUE7QUFDRjs7QUFFQTtFQUNFLFlBQUE7QUFDRjs7QUFFQTtFQUNFLGVBQUE7RUFDQSxzQ0FBQTtFQUNBLGdCQUFBO0VBQ0EsaUJBQUE7RUFDQSxzQkFBQTtBQUNGOztBQUVBO0VBQ0Usd0NBQUE7RUFDQSxZQUFBO0VBQ0Esa0JBQUE7RUFDQSxXQUFBO0FBQ0Y7O0FBRUE7RUFDRSxlQUFBO0FBQ0Y7O0FBRUE7O0VBQUE7O0FBSUE7RUFDRSwrQkFBQTtBQUFGOztBQUdBO0VBQ0UsWUFBQTtBQUFGOztBQUdBO0VBQ0Usc0RBQUE7QUFBRjs7QUFHQTtFQUNFLGlFQUFBO0FBQUYiLCJmaWxlIjoic2NlbmFyaW9zLWJ1aWxkZXIuY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyI6Om5nLWRlZXAgLnZleC1zdHlsZS1kYXJrIHZleC1zY3J1bWJvYXJkIC5zY3J1bWJvYXJkLWNhcmQ6aG92ZXIge1xuICBiYWNrZ3JvdW5kOiByZ2JhKDAsIDAsIDAsIDAuNSk7XG59XG5cbi5zY3J1bWJvYXJkLWRyb3Atem9uZSB7XG4gIG1pbi1oZWlnaHQ6IDI1MHB4O1xufVxuXG4uc2NydW1ib2FyZC1saXN0IHtcbiAgaGVpZ2h0OiBjYWxjKDEwMHZoIC0gNjVweCk7XG59XG5cbi5zY3J1bWJvYXJkLWNhcmQge1xuICBtYXJnaW4tYm90dG9tOiB2YXIoLS1wYWRkaW5nLTgpO1xuICBjdXJzb3I6IG1vdmU7XG59XG5cbi5zY3J1bWJvYXJkLWNhcmQ6bGFzdC1vZi10eXBlIHtcbiAgbWFyZ2luLWJvdHRvbTogMDtcbn1cblxuLnNjcnVtYm9hcmQtY2FyZDpob3ZlciB7XG4gIGJhY2tncm91bmQ6IHJnYmEoMjU1LCAyNTUsIDI1NSwgMC41KTtcbn1cblxuLnNjcnVtYm9hcmQtY2FyZCAubGFiZWwge1xuICBib3JkZXItcmFkaXVzOiA2cHg7XG4gIGhlaWdodDogNnB4O1xuICBtYXgtd2lkdGg6IDMycHg7XG59XG5cbi5zY3J1bWJvYXJkLWNhcmQgLmJveCB7XG4gIHBhZGRpbmc6IDNweDtcbn1cblxuLnNjcnVtYm9hcmQtY2FyZCAuYm94IC5ib3gtdGV4dCB7XG4gIGZvbnQtc2l6ZTogMTFweDtcbiAgZm9udC13ZWlnaHQ6IHZhcigtLWZvbnQtd2VpZ2h0LW1lZGl1bSk7XG4gIG1hcmdpbi1sZWZ0OiAzcHg7XG4gIG1hcmdpbi1yaWdodDogM3B4O1xuICB2ZXJ0aWNhbC1hbGlnbjogYm90dG9tO1xufVxuXG4uYXZhdGFyLm92ZXJsYXBwaW5nIHtcbiAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tYmFja2dyb3VuZC1jYXJkKTtcbiAgaGVpZ2h0OiAyM3B4O1xuICBtYXJnaW4tcmlnaHQ6IC04cHg7XG4gIHdpZHRoOiAyM3B4O1xufVxuXG4uYXZhdGFyLm92ZXJsYXBwaW5nOmxhc3Qtb2YtdHlwZSB7XG4gIG1hcmdpbi1yaWdodDogMDtcbn1cblxuLypcbiAgQ2RrIERyYWcgJiBEcm9wXG4gKi9cblxuLmNkay1kcmFnLXByZXZpZXcge1xuICBib3gtc2hhZG93OiB2YXIoLS1lbGV2YXRpb24tejgpO1xufVxuXG4uY2RrLWRyYWctcGxhY2Vob2xkZXIge1xuICBvcGFjaXR5OiAwLjI7XG59XG5cbi5jZGstZHJvcC1saXN0LWRyYWdnaW5nIC5zY3J1bWJvYXJkLWNhcmQ6bm90KC5jZGstZHJhZy1wbGFjZWhvbGRlcikge1xuICB0cmFuc2l0aW9uOiB0cmFuc2Zvcm0gMjUwbXMgY3ViaWMtYmV6aWVyKDAsIDAsIDAuMiwgMSk7XG59XG5cbi5jZGstZHJhZy1hbmltYXRpbmcge1xuICB0cmFuc2l0aW9uOiB0cmFuc2Zvcm0gMjUwbXMgY3ViaWMtYmV6aWVyKDAsIDAsIDAuMiwgMSkgIWltcG9ydGFudDtcbn0iXX0= */";
      /***/
    },

    /***/
    "EIze":
    /*!**************************************************************************!*\
      !*** ./src/app/modules/scenarios/services/scenarios-resolver.service.ts ***!
      \**************************************************************************/

    /*! exports provided: ScenariosResolver */

    /***/
    function EIze(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ScenariosResolver", function () {
        return ScenariosResolver;
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


      var _core_http_scenario_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @core/http/scenario-resource.service */
      "3Ncz");

      var ScenariosResolver = /*#__PURE__*/function () {
        function ScenariosResolver(scenarioResource) {
          _classCallCheck(this, ScenariosResolver);

          this.scenarioResource = scenarioResource;
        }

        _createClass(ScenariosResolver, [{
          key: "resolve",
          value: function resolve(route) {
            return this.scenarioResource.index({
              project_id: route.queryParams.project_id
            });
          }
        }]);

        return ScenariosResolver;
      }();

      ScenariosResolver.ctorParameters = function () {
        return [{
          type: _core_http_scenario_resource_service__WEBPACK_IMPORTED_MODULE_2__["ScenarioResource"]
        }];
      };

      ScenariosResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], ScenariosResolver);
      /***/
    },

    /***/
    "EMV3":
    /*!*******************************************************************************************************************************************************************!*\
      !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/scenarios/pages/scenarios-index/components/scenarios-data-table/scenarios-data-table.component.html ***!
      \*******************************************************************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function EMV3(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "<div class=\"h-full relative\" vexScrollbar>\n  <div fxLayout=\"column\" fxLayoutAlign=\"space-between\">\n    <div class=\"bg-app-bar px-6 h-14 border-b sticky left-0\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n\n      <ng-container *ngIf=\"selection.hasValue()\">\n        <h2\n          *ngIf=\"selection.hasValue()\"\n          class=\"title my-0 ltr:pr-4 rtl:pl-4 ltr:mr-4 rtl:ml-4 ltr:border-r rtl:border-l\"\n          fxFlex=\"none\"\n          fxHide.xs\n        >\n          <!-- <span *ngIf=\"!selection.hasValue()\">Scenarios</span> -->\n          {{ selection.selected.length }} scenario<span *ngIf=\"selection.selected.length > 1\">s</span> selected\n        </h2>\n\n        <div class=\"pr-4 mr-4 border-r\">\n          <button (click)=\"removeSelected(selection.selected)\"\n                  color=\"primary\"\n                  mat-icon-button\n                  matTooltip=\"Delete selected\"\n                  type=\"button\">\n            <mat-icon [icIcon]=\"icDelete\"></mat-icon>\n          </button>\n        </div>\n      </ng-container>\n\n      <div class=\"bg-card rounded-full border px-4 full-width\"\n           fxFlex\n           fxFlex.lt-md=\"auto\"\n           fxHide.xs\n           fxLayout=\"row\"\n           fxLayoutAlign=\"start center\">\n        <ic-icon [icIcon]=\"icSearch\" size=\"20px\"></ic-icon>\n        <input\n          [formControl]=\"searchCtrl\"\n          class=\"px-4 py-2 border-0 outline-none w-full bg-transparent\"\n          fxFlex\n          placeholder=\"Search...\"\n          type=\"search\">\n      </div>\n\n      <span fxFlex></span>\n\n      <button class=\"ml-4\" fxFlex=\"none\" fxHide.gt-xs mat-icon-button type=\"button\">\n        <mat-icon [icIcon]=\"icSearch\"></mat-icon>\n      </button>\n\n      <button [matMenuTriggerFor]=\"columnFilterMenu\"\n              class=\"ml-4\"\n              fxFlex=\"none\"\n              mat-icon-button\n              matTooltip=\"Filter Columns\"\n              type=\"button\">\n        <mat-icon [icIcon]=\"icFilterList\"></mat-icon>\n      </button>\n    </div>\n\n    <table [@stagger]=\"dataSource.filteredData\"\n           [dataSource]=\"dataSource\"\n           class=\"w-full\"\n           fxFlex=\"auto\"\n           mat-table\n           matSort>\n\n      <!--- Note that these columns can be defined in any order.\n            The actual rendered columns are set as a property on the row definition\" -->\n\n      <!-- Model Properties Column -->\n      <ng-container *ngFor=\"let column of columns\">\n        <ng-container *ngIf=\"column.type === 'button'\" [matColumnDef]=\"column.property\">\n          <ng-container *ngIf=\"column.property === 'starred'\">\n            <th *matHeaderCellDef mat-header-cell mat-sort-header> {{ column.label }}</th>\n            <td *matCellDef=\"let row\" [ngClass]=\"column.cssClasses\" class=\"w-10\" mat-cell>\n              <button (click)=\"emitToggleStar($event, row.id)\" mat-icon-button type=\"button\">\n                <mat-icon *ngIf=\"row[column.property]\" [icIcon]=\"icStar\" class=\"text-amber-500\"></mat-icon>\n                <mat-icon *ngIf=\"!row[column.property]\" [icIcon]=\"icStarBorder\"></mat-icon>\n              </button>\n            </td>\n          </ng-container>\n\n          <ng-container *ngIf=\"column.property === 'menu'\">\n            <th *matHeaderCellDef mat-header-cell mat-sort-header> {{ column.label }}</th>\n            <td *matCellDef=\"let row\" [ngClass]=\"column.cssClasses\" class=\"w-10\" mat-cell>\n              <button (click)=\"$event.stopPropagation()\"\n                      [matMenuTriggerData]=\"{ row: row }\"\n                      [matMenuTriggerFor]=\"contactMenu\"\n                      mat-icon-button\n                      type=\"button\">\n                <mat-icon [icIcon]=\"icMoreVert\"></mat-icon>\n              </button>\n            </td>\n          </ng-container>\n        </ng-container>\n\n        <ng-container *ngIf=\"column.type === 'checkbox'\" [matColumnDef]=\"column.property\">\n          <th *matHeaderCellDef mat-header-cell>\n            <mat-checkbox\n              [checked]=\"isAllSelected()\"\n              [indeterminate]=\"isPartiallySelected()\"\n              (click)=\"masterToggle($event)\"\n              color=\"primary\"\n            >\n            </mat-checkbox>\n          </th>\n          <td *matCellDef=\"let row\" class=\"w-4\" [ngClass]=\"column.cssClasses\" mat-cell>\n            <mat-checkbox (change)=\"$event ? selection.toggle(row) : null\"\n                          (click)=\"$event.stopPropagation()\"\n                          [checked]=\"isSelected(row)\"\n                          color=\"primary\">\n            </mat-checkbox>\n          </td>\n\n          <!-- <td *matCellDef=\"let row\" [ngClass]=\"column.cssClasses\" mat-cell (click)=\"$event.stopPropagation()\">\n            <mat-checkbox [checked]=\"row[column.property]\"></mat-checkbox>\n          </td> -->\n        </ng-container>\n\n        <ng-container *ngIf=\"column.type === 'date'\" [matColumnDef]=\"column.property\">\n          <th class=\"uppercase\" *matHeaderCellDef mat-header-cell mat-sort-header> {{ column.label }}</th>\n          <td *matCellDef=\"let row\" [ngClass]=\"column.cssClasses\" mat-cell>\n            {{ row[column.property] | date : 'short' }}\n          </td>\n        </ng-container>\n\n        <ng-container *ngIf=\"column.type === 'image'\" [matColumnDef]=\"column.property\">\n          <th *matHeaderCellDef mat-header-cell mat-sort-header> {{ column.label }}</th>\n          <td *matCellDef=\"let row\" [ngClass]=\"column.cssClasses\" mat-cell>\n            <img [src]=\"row[column.property]\" class=\"avatar h-9 w-9 align-middle my-2\">\n          </td>\n        </ng-container>\n\n        <ng-container *ngIf=\"column.type === 'text'\" [matColumnDef]=\"column.property\">\n          <th class=\"uppercase\" *matHeaderCellDef mat-header-cell mat-sort-header> {{ column.label }}</th>\n          <td *matCellDef=\"let row\" [ngClass]=\"column.cssClasses\" mat-cell>{{ row[column.property] }}</td>\n        </ng-container>\n      </ng-container>\n\n      <tr *matHeaderRowDef=\"visibleColumns; sticky: true\" mat-header-row></tr>\n      <!--suppress UnnecessaryLabelJS -->\n      <tr (click)=\"view.emit(row.id)\"\n          *matRowDef=\"let row; columns: visibleColumns;\"\n          @fadeInUp\n          class=\"hover:bg-hover cursor-pointer\"\n          mat-row></tr>\n    </table>\n\n    <div *ngIf=\"dataSource.filteredData.length === 0\"\n         @scaleFadeIn\n         class=\"pb-10\"\n         fxFlex=\"auto\"\n         fxLayout=\"column\"\n         fxLayoutAlign=\"center center\">\n      <img class=\"m-12 h-64\" src=\"assets/img/illustrations/idea.svg\">\n      <h2 class=\"headline m-0 text-center\">No results matching your filters</h2>\n    </div>\n\n    <mat-paginator [fxHide]=\"dataSource.filteredData.length === 0\"\n                   [pageSize]=\"pageSize\"\n                   [pageSizeOptions]=\"pageSizeOptions\"\n                   (page)=\"onPaginateChange($event)\"\n                   class=\"sticky bottom-0 left-0 right-0 border-t\"\n                   fxFlex=\"none\"></mat-paginator>\n  </div>\n</div>\n\n<mat-menu #contactMenu=\"matMenu\" xPosition=\"before\" yPosition=\"below\">\n  <ng-template let-row=\"row\" matMenuContent>\n    <button mat-menu-item (click)=\"edit.emit(row)\">\n      <mat-icon [icIcon]=\"icEdit\"></mat-icon>\n      <span>Edit</span>\n    </button>\n\n    <button mat-menu-item (click)=\"download.emit(row.id)\">\n      <mat-icon [icIcon]=\"icCloudDownload\"></mat-icon>\n      <span>Download</span>\n    </button>\n\n    <button mat-menu-item (click)=\"delete.emit(row.id)\">\n      <mat-icon [icIcon]=\"icDeleteForever\"></mat-icon>\n      <span>Delete</span>\n    </button>\n  </ng-template>\n</mat-menu>\n\n<mat-menu #columnFilterMenu=\"matMenu\" xPosition=\"before\" yPosition=\"below\">\n  <ng-container *ngFor=\"let column of columns; let i = index\">\n    <button\n      *ngIf=\"column.canHide\"\n      (click)=\"toggleColumnVisibility($event, i, column)\"\n      class=\"checkbox-item mat-menu-item\">\n      <mat-checkbox checked=\"column.visible\" color=\"primary\">\n        {{ column.label }}\n      </mat-checkbox>\n    </button>\n  </ng-container>\n</mat-menu>\n";
      /***/
    },

    /***/
    "FAgS":
    /*!**********************************************************************************************************************************************************!*\
      !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/scenarios/pages/scenario-details/components/requests-create/requests-create.component.html ***!
      \**********************************************************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function FAgS(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "<form (ngSubmit)=\"create()\" [formGroup]=\"form\">\r\n  <div fxLayout=\"row\" fxLayoutAlign=\"start center\" mat-dialog-title>\r\n\r\n    <h2 class=\"headline m-0\" fxFlex=\"auto\">Add Requests</h2>\r\n<!--\r\n    <button [matMenuTriggerFor]=\"settingsMenu\" class=\"text-secondary\" mat-icon-button type=\"button\">\r\n      <mat-icon [icIcon]=\"icMoreVert\"></mat-icon>\r\n    </button>\r\n-->\r\n    <button class=\"text-secondary\" mat-dialog-close mat-icon-button type=\"button\">\r\n      <mat-icon [icIcon]=\"icClose\"></mat-icon>\r\n    </button>\r\n  </div>\r\n\r\n  <mat-divider class=\"-mx-6 text-border\"></mat-divider>\r\n\r\n  <ngx-dropzone (change)=\"onSelect($event)\">\r\n    <ngx-dropzone-label>Select or drop a HAR file!</ngx-dropzone-label>\r\n    <ngx-dropzone-preview *ngFor=\"let f of files\" [removable]=\"true\" (removed)=\"onRemove(f)\">\r\n        <ngx-dropzone-label>{{ f.name }} ({{ f.type }})</ngx-dropzone-label>\r\n    </ngx-dropzone-preview>\r\n  </ngx-dropzone>\r\n\r\n  <mat-dialog-actions align=\"end\">\r\n    <button mat-button mat-dialog-close type=\"button\">CANCEL</button>\r\n    <button color=\"primary\" mat-button type=\"submit\">ADD</button>\r\n  </mat-dialog-actions>\r\n</form>\r\n\r\n<mat-menu #settingsMenu=\"matMenu\" xPosition=\"before\" yPosition=\"below\">\r\n  <button mat-menu-item>\r\n    <mat-icon [icIcon]=\"icPrint\"></mat-icon>\r\n    <span>Print</span>\r\n  </button>\r\n\r\n  <button mat-menu-item>\r\n    <mat-icon [icIcon]=\"icDownload\"></mat-icon>\r\n    <span>Export</span>\r\n  </button>\r\n\r\n  <button mat-menu-item>\r\n    <mat-icon [icIcon]=\"icDelete\"></mat-icon>\r\n    <span>Delete</span>\r\n  </button>\r\n</mat-menu>\r\n";
      /***/
    },

    /***/
    "GF+f":
    /*!*********************************************************!*\
      !*** ./node_modules/@angular/cdk/fesm2015/accordion.js ***!
      \*********************************************************/

    /*! exports provided: CdkAccordion, CdkAccordionItem, CdkAccordionModule, ɵangular_material_src_cdk_accordion_accordion_a */

    /***/
    function GFF(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkAccordion", function () {
        return CdkAccordion;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkAccordionItem", function () {
        return CdkAccordionItem;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkAccordionModule", function () {
        return CdkAccordionModule;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ɵangular_material_src_cdk_accordion_accordion_a", function () {
        return CDK_ACCORDION;
      });
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! @angular/cdk/collections */
      "CtHx");
      /* harmony import */


      var _angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @angular/cdk/coercion */
      "8LU1");
      /* harmony import */


      var rxjs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! rxjs */
      "qCKp");
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /** Used to generate unique ID for each accordion. */


      var nextId = 0;
      /**
       * Injection token that can be used to reference instances of `CdkAccordion`. It serves
       * as alternative token to the actual `CdkAccordion` class which could cause unnecessary
       * retention of the class and its directive metadata.
       */

      var CDK_ACCORDION = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["InjectionToken"]('CdkAccordion');
      /**
       * Directive whose purpose is to manage the expanded state of CdkAccordionItem children.
       */

      var CdkAccordion = /*#__PURE__*/function () {
        function CdkAccordion() {
          _classCallCheck(this, CdkAccordion);

          /** Emits when the state of the accordion changes */
          this._stateChanges = new rxjs__WEBPACK_IMPORTED_MODULE_3__["Subject"]();
          /** Stream that emits true/false when openAll/closeAll is triggered. */

          this._openCloseAllActions = new rxjs__WEBPACK_IMPORTED_MODULE_3__["Subject"]();
          /** A readonly id value to use for unique selection coordination. */

          this.id = "cdk-accordion-".concat(nextId++);
          this._multi = false;
        }
        /** Whether the accordion should allow multiple expanded accordion items simultaneously. */


        _createClass(CdkAccordion, [{
          key: "openAll",

          /** Opens all enabled accordion items in an accordion where multi is enabled. */
          value: function openAll() {
            this._openCloseAll(true);
          }
          /** Closes all enabled accordion items in an accordion where multi is enabled. */

        }, {
          key: "closeAll",
          value: function closeAll() {
            this._openCloseAll(false);
          }
        }, {
          key: "ngOnChanges",
          value: function ngOnChanges(changes) {
            this._stateChanges.next(changes);
          }
        }, {
          key: "ngOnDestroy",
          value: function ngOnDestroy() {
            this._stateChanges.complete();
          }
        }, {
          key: "_openCloseAll",
          value: function _openCloseAll(expanded) {
            if (this.multi) {
              this._openCloseAllActions.next(expanded);
            }
          }
        }, {
          key: "multi",
          get: function get() {
            return this._multi;
          },
          set: function set(multi) {
            this._multi = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_2__["coerceBooleanProperty"])(multi);
          }
        }]);

        return CdkAccordion;
      }();

      CdkAccordion.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"],
        args: [{
          selector: 'cdk-accordion, [cdkAccordion]',
          exportAs: 'cdkAccordion',
          providers: [{
            provide: CDK_ACCORDION,
            useExisting: CdkAccordion
          }]
        }]
      }];
      CdkAccordion.propDecorators = {
        multi: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"]
        }]
      };
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /** Used to generate unique ID for each accordion item. */

      var nextId$1 = 0;
      var ɵ0 = undefined;
      /**
       * An basic directive expected to be extended and decorated as a component.  Sets up all
       * events and attributes needed to be managed by a CdkAccordion parent.
       */

      var CdkAccordionItem = /*#__PURE__*/function () {
        function CdkAccordionItem(accordion, _changeDetectorRef, _expansionDispatcher) {
          var _this6 = this;

          _classCallCheck(this, CdkAccordionItem);

          this.accordion = accordion;
          this._changeDetectorRef = _changeDetectorRef;
          this._expansionDispatcher = _expansionDispatcher;
          /** Subscription to openAll/closeAll events. */

          this._openCloseAllSubscription = rxjs__WEBPACK_IMPORTED_MODULE_3__["Subscription"].EMPTY;
          /** Event emitted every time the AccordionItem is closed. */

          this.closed = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"]();
          /** Event emitted every time the AccordionItem is opened. */

          this.opened = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"]();
          /** Event emitted when the AccordionItem is destroyed. */

          this.destroyed = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"]();
          /**
           * Emits whenever the expanded state of the accordion changes.
           * Primarily used to facilitate two-way binding.
           * @docs-private
           */

          this.expandedChange = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"]();
          /** The unique AccordionItem id. */

          this.id = "cdk-accordion-child-".concat(nextId$1++);
          this._expanded = false;
          this._disabled = false;
          /** Unregister function for _expansionDispatcher. */

          this._removeUniqueSelectionListener = function () {};

          this._removeUniqueSelectionListener = _expansionDispatcher.listen(function (id, accordionId) {
            if (_this6.accordion && !_this6.accordion.multi && _this6.accordion.id === accordionId && _this6.id !== id) {
              _this6.expanded = false;
            }
          }); // When an accordion item is hosted in an accordion, subscribe to open/close events.

          if (this.accordion) {
            this._openCloseAllSubscription = this._subscribeToOpenCloseAllActions();
          }
        }
        /** Whether the AccordionItem is expanded. */


        _createClass(CdkAccordionItem, [{
          key: "ngOnDestroy",

          /** Emits an event for the accordion item being destroyed. */
          value: function ngOnDestroy() {
            this.opened.complete();
            this.closed.complete();
            this.destroyed.emit();
            this.destroyed.complete();

            this._removeUniqueSelectionListener();

            this._openCloseAllSubscription.unsubscribe();
          }
          /** Toggles the expanded state of the accordion item. */

        }, {
          key: "toggle",
          value: function toggle() {
            if (!this.disabled) {
              this.expanded = !this.expanded;
            }
          }
          /** Sets the expanded state of the accordion item to false. */

        }, {
          key: "close",
          value: function close() {
            if (!this.disabled) {
              this.expanded = false;
            }
          }
          /** Sets the expanded state of the accordion item to true. */

        }, {
          key: "open",
          value: function open() {
            if (!this.disabled) {
              this.expanded = true;
            }
          }
        }, {
          key: "_subscribeToOpenCloseAllActions",
          value: function _subscribeToOpenCloseAllActions() {
            var _this7 = this;

            return this.accordion._openCloseAllActions.subscribe(function (expanded) {
              // Only change expanded state if item is enabled
              if (!_this7.disabled) {
                _this7.expanded = expanded;
              }
            });
          }
        }, {
          key: "expanded",
          get: function get() {
            return this._expanded;
          },
          set: function set(expanded) {
            expanded = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_2__["coerceBooleanProperty"])(expanded); // Only emit events and update the internal value if the value changes.

            if (this._expanded !== expanded) {
              this._expanded = expanded;
              this.expandedChange.emit(expanded);

              if (expanded) {
                this.opened.emit();
                /**
                 * In the unique selection dispatcher, the id parameter is the id of the CdkAccordionItem,
                 * the name value is the id of the accordion.
                 */

                var accordionId = this.accordion ? this.accordion.id : this.id;

                this._expansionDispatcher.notify(this.id, accordionId);
              } else {
                this.closed.emit();
              } // Ensures that the animation will run when the value is set outside of an `@Input`.
              // This includes cases like the open, close and toggle methods.


              this._changeDetectorRef.markForCheck();
            }
          }
          /** Whether the AccordionItem is disabled. */

        }, {
          key: "disabled",
          get: function get() {
            return this._disabled;
          },
          set: function set(disabled) {
            this._disabled = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_2__["coerceBooleanProperty"])(disabled);
          }
        }]);

        return CdkAccordionItem;
      }();

      CdkAccordionItem.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"],
        args: [{
          selector: 'cdk-accordion-item, [cdkAccordionItem]',
          exportAs: 'cdkAccordionItem',
          providers: [// Provide `CDK_ACCORDION` as undefined to prevent nested accordion items from
          // registering to the same accordion.
          {
            provide: CDK_ACCORDION,
            useValue: ɵ0
          }]
        }]
      }];

      CdkAccordionItem.ctorParameters = function () {
        return [{
          type: CdkAccordion,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Optional"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Inject"],
            args: [CDK_ACCORDION]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["SkipSelf"]
          }]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ChangeDetectorRef"]
        }, {
          type: _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_1__["UniqueSelectionDispatcher"]
        }];
      };

      CdkAccordionItem.propDecorators = {
        closed: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Output"]
        }],
        opened: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Output"]
        }],
        destroyed: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Output"]
        }],
        expandedChange: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Output"]
        }],
        expanded: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"]
        }],
        disabled: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"]
        }]
      };
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      var CdkAccordionModule = function CdkAccordionModule() {
        _classCallCheck(this, CdkAccordionModule);
      };

      CdkAccordionModule.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"],
        args: [{
          exports: [CdkAccordion, CdkAccordionItem],
          declarations: [CdkAccordion, CdkAccordionItem]
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
      //# sourceMappingURL=accordion.js.map

      /***/
    },

    /***/
    "IhNm":
    /*!***************************************************************!*\
      !*** ./src/app/modules/scenarios/scenarios-routing.module.ts ***!
      \***************************************************************/

    /*! exports provided: ScenariosRoutingModule */

    /***/
    function IhNm(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ScenariosRoutingModule", function () {
        return ScenariosRoutingModule;
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


      var _projects_services_project_resolver_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @projects/services/project-resolver.service */
      "Y1jZ");
      /* harmony import */


      var _scenarios_pages_scenario_details_scenario_details_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @scenarios/pages/scenario-details/scenario-details.component */
      "q9PC");
      /* harmony import */


      var _scenarios_pages_scenarios_builder_scenarios_builder_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @scenarios/pages/scenarios-builder/scenarios-builder.component */
      "4BTo");
      /* harmony import */


      var _scenarios_pages_scenarios_index_scenarios_index_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @scenarios/pages/scenarios-index/scenarios-index.component */
      "llVH");
      /* harmony import */


      var _scenarios_services_requests_resolver_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @scenarios/services/requests-resolver.service */
      "xmhw");
      /* harmony import */


      var _scenarios_services_scenario_resolver_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @scenarios/services/scenario-resolver.service */
      "pXOW");
      /* harmony import */


      var _scenarios_services_scenarios_resolver_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @scenarios/services/scenarios-resolver.service */
      "EIze");
      /* harmony import */


      var _requests_pages_request_details_request_details_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @requests/pages/request-details/request-details.component */
      "g6n5");
      /* harmony import */


      var _requests_services_request_resolver_service__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @requests/services/request-resolver.service */
      "a+oo");
      /* harmony import */


      var _requests_services_requests_available_resolver_service__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @requests/services/requests-available-resolver.service */
      "0UTy");
      /* harmony import */


      var _requests_services_response_headers_resolver_service__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @requests/services/response-headers-resolver.service */
      "qeIL");
      /* harmony import */


      var _requests_services_response_resolver_service__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! @requests/services/response-resolver.service */
      "h8gq");

      var routes = [{
        path: '',
        component: _scenarios_pages_scenarios_index_scenarios_index_component__WEBPACK_IMPORTED_MODULE_6__["ScenariosIndexComponent"],
        resolve: {
          scenarios: _scenarios_services_scenarios_resolver_service__WEBPACK_IMPORTED_MODULE_9__["ScenariosResolver"],
          project: _projects_services_project_resolver_service__WEBPACK_IMPORTED_MODULE_3__["ProjectResolver"]
        }
      }, {
        path: ':scenario_id',
        component: _scenarios_pages_scenario_details_scenario_details_component__WEBPACK_IMPORTED_MODULE_4__["ScenarioDetailsComponent"],
        resolve: {
          scenario: _scenarios_services_scenario_resolver_service__WEBPACK_IMPORTED_MODULE_8__["ScenarioResolver"],
          requests: _scenarios_services_requests_resolver_service__WEBPACK_IMPORTED_MODULE_7__["RequestsResolver"]
        }
      }, {
        path: ':scenario_id/editor',
        component: _scenarios_pages_scenarios_builder_scenarios_builder_component__WEBPACK_IMPORTED_MODULE_5__["ScenariosBuilderComponent"],
        resolve: {
          project: _projects_services_project_resolver_service__WEBPACK_IMPORTED_MODULE_3__["ProjectResolver"],
          scenario: _scenarios_services_scenario_resolver_service__WEBPACK_IMPORTED_MODULE_8__["ScenarioResolver"],
          requests: _scenarios_services_requests_resolver_service__WEBPACK_IMPORTED_MODULE_7__["RequestsResolver"],
          requestsAvailable: _requests_services_requests_available_resolver_service__WEBPACK_IMPORTED_MODULE_12__["RequestsAvailableResolver"]
        }
      }, {
        path: ':scenario_id/requests/:request_id',
        component: _requests_pages_request_details_request_details_component__WEBPACK_IMPORTED_MODULE_10__["RequestDetailsComponent"],
        resolve: {
          parentResource: _scenarios_services_scenario_resolver_service__WEBPACK_IMPORTED_MODULE_8__["ScenarioResolver"],
          request: _requests_services_request_resolver_service__WEBPACK_IMPORTED_MODULE_11__["RequestResolver"],
          response: _requests_services_response_resolver_service__WEBPACK_IMPORTED_MODULE_14__["ResponseResolver"],
          responseHeaders: _requests_services_response_headers_resolver_service__WEBPACK_IMPORTED_MODULE_13__["ResponseHeadersResolver"]
        }
      }];

      var ScenariosRoutingModule = function ScenariosRoutingModule() {
        _classCallCheck(this, ScenariosRoutingModule);
      };

      ScenariosRoutingModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]]
      })], ScenariosRoutingModule);
      /***/
    },

    /***/
    "KMsL":
    /*!*************************************************************************************!*\
      !*** ./src/app/modules/scenarios/pages/scenario-details/scenario-details.module.ts ***!
      \*************************************************************************************/

    /*! exports provided: ScenarioDetailsModule */

    /***/
    function KMsL(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ScenarioDetailsModule", function () {
        return ScenarioDetailsModule;
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


      var _angular_router__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/router */
      "iInd");
      /* harmony import */


      var _angular_material_button__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/material/button */
      "Dxy4");
      /* harmony import */


      var _angular_material_button_toggle__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @angular/material/button-toggle */
      "Ynp+");
      /* harmony import */


      var _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @angular/material/checkbox */
      "pMoy");
      /* harmony import */


      var _angular_material_icon__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @angular/material/icon */
      "Tj54");
      /* harmony import */


      var _angular_material_menu__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @angular/material/menu */
      "rJgo");
      /* harmony import */


      var _angular_material_paginator__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @angular/material/paginator */
      "5QHs");
      /* harmony import */


      var _angular_material_select__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @angular/material/select */
      "ZTz/");
      /* harmony import */


      var _angular_material_sort__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @angular/material/sort */
      "LUZP");
      /* harmony import */


      var _angular_material_table__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! @angular/material/table */
      "OaSA");
      /* harmony import */


      var _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! @angular/material/tooltip */
      "ZFy/");
      /* harmony import */


      var _vex_components_breadcrumbs_breadcrumbs_module__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(
      /*! @vex/components/breadcrumbs/breadcrumbs.module */
      "J0XA");
      /* harmony import */


      var _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(
      /*! @vex/components/page-layout/page-layout.module */
      "7lCJ");
      /* harmony import */


      var _vex_directives_container_container_module__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(
      /*! @vex/directives/container/container.module */
      "68Yx");
      /* harmony import */


      var _vex_pipes_color_color_fade_module__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(
      /*! @vex/pipes/color/color-fade.module */
      "Chvm");
      /* harmony import */


      var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(
      /*! @visurel/iconify-angular */
      "l+Q0");
      /* harmony import */


      var _shared_components_data_table_data_table_module__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(
      /*! @shared/components/data-table/data-table.module */
      "MqAd");
      /* harmony import */


      var _shared_components_label_label_module__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(
      /*! @shared/components/label/label.module */
      "W6U6");
      /* harmony import */


      var _shared_shared_module__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(
      /*! @shared/shared.module */
      "PCNd");
      /* harmony import */


      var _components_requests_create_requests_create_module__WEBPACK_IMPORTED_MODULE_24__ = __webpack_require__(
      /*! ./components/requests-create/requests-create.module */
      "41Lq");
      /* harmony import */


      var _scenario_details_component__WEBPACK_IMPORTED_MODULE_25__ = __webpack_require__(
      /*! ./scenario-details.component */
      "q9PC");
      /* harmony import */


      var _services_scenario_details_icons_service__WEBPACK_IMPORTED_MODULE_26__ = __webpack_require__(
      /*! ./services/scenario-details-icons.service */
      "5euU");

      var ScenarioDetailsModule = function ScenarioDetailsModule() {
        _classCallCheck(this, ScenarioDetailsModule);
      };

      ScenarioDetailsModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_scenario_details_component__WEBPACK_IMPORTED_MODULE_25__["ScenarioDetailsComponent"]],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_17__["PageLayoutModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"], _angular_router__WEBPACK_IMPORTED_MODULE_5__["RouterModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormsModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"], _angular_material_paginator__WEBPACK_IMPORTED_MODULE_11__["MatPaginatorModule"], _angular_material_table__WEBPACK_IMPORTED_MODULE_14__["MatTableModule"], _angular_material_sort__WEBPACK_IMPORTED_MODULE_13__["MatSortModule"], _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_8__["MatCheckboxModule"], _angular_material_icon__WEBPACK_IMPORTED_MODULE_9__["MatIconModule"], _angular_material_button__WEBPACK_IMPORTED_MODULE_6__["MatButtonModule"], _angular_material_menu__WEBPACK_IMPORTED_MODULE_10__["MatMenuModule"], _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_15__["MatTooltipModule"], _angular_material_select__WEBPACK_IMPORTED_MODULE_12__["MatSelectModule"], _angular_material_button_toggle__WEBPACK_IMPORTED_MODULE_7__["MatButtonToggleModule"], _vex_components_breadcrumbs_breadcrumbs_module__WEBPACK_IMPORTED_MODULE_16__["BreadcrumbsModule"], _vex_pipes_color_color_fade_module__WEBPACK_IMPORTED_MODULE_19__["ColorFadeModule"], _vex_directives_container_container_module__WEBPACK_IMPORTED_MODULE_18__["ContainerModule"], _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_20__["IconModule"], _shared_shared_module__WEBPACK_IMPORTED_MODULE_23__["SharedModule"], _shared_components_label_label_module__WEBPACK_IMPORTED_MODULE_22__["LabelModule"], _shared_components_data_table_data_table_module__WEBPACK_IMPORTED_MODULE_21__["DataTableModule"], _components_requests_create_requests_create_module__WEBPACK_IMPORTED_MODULE_24__["RequestsCreateModule"]],
        providers: [_services_scenario_details_icons_service__WEBPACK_IMPORTED_MODULE_26__["ScenarioDetailsIcons"]]
      })], ScenarioDetailsModule);
      /***/
    },

    /***/
    "MNke":
    /*!*************************************************************************!*\
      !*** ./node_modules/ngx-infinite-scroll/modules/ngx-infinite-scroll.js ***!
      \*************************************************************************/

    /*! exports provided: InfiniteScrollDirective, InfiniteScrollModule */

    /***/
    function MNke(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "InfiniteScrollDirective", function () {
        return InfiniteScrollDirective;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "InfiniteScrollModule", function () {
        return InfiniteScrollModule;
      });
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var rxjs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! rxjs */
      "qCKp");
      /* harmony import */


      var rxjs_operators__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! rxjs/operators */
      "kU1M");
      /**
       * @fileoverview added by tsickle
       * @suppress {checkTypes,extraRequire,missingOverride,missingReturn,unusedPrivateMembers,uselessCode} checked by tsc
       */

      /**
       * @param {?} selector
       * @param {?} scrollWindow
       * @param {?} defaultElement
       * @param {?} fromRoot
       * @return {?}
       */


      function resolveContainerElement(selector, scrollWindow, defaultElement, fromRoot) {
        /** @type {?} */
        var hasWindow = window && !!window.document && window.document.documentElement;
        /** @type {?} */

        var container = hasWindow && scrollWindow ? window : defaultElement;

        if (selector) {
          /** @type {?} */
          var containerIsString = selector && hasWindow && typeof selector === 'string';
          container = containerIsString ? findElement(selector, defaultElement.nativeElement, fromRoot) : selector;

          if (!container) {
            throw new Error('ngx-infinite-scroll {resolveContainerElement()}: selector for');
          }
        }

        return container;
      }
      /**
       * @param {?} selector
       * @param {?} customRoot
       * @param {?} fromRoot
       * @return {?}
       */


      function findElement(selector, customRoot, fromRoot) {
        /** @type {?} */
        var rootEl = fromRoot ? window.document : customRoot;
        return rootEl.querySelector(selector);
      }
      /**
       * @param {?} prop
       * @return {?}
       */


      function inputPropChanged(prop) {
        return prop && !prop.firstChange;
      }
      /**
       * @return {?}
       */


      function hasWindowDefined() {
        return typeof window !== 'undefined';
      }
      /**
       * @fileoverview added by tsickle
       * @suppress {checkTypes,extraRequire,missingOverride,missingReturn,unusedPrivateMembers,uselessCode} checked by tsc
       */

      /** @type {?} */


      var VerticalProps = {
        clientHeight: "clientHeight",
        offsetHeight: "offsetHeight",
        scrollHeight: "scrollHeight",
        pageYOffset: "pageYOffset",
        offsetTop: "offsetTop",
        scrollTop: "scrollTop",
        top: "top"
      };
      /** @type {?} */

      var HorizontalProps = {
        clientHeight: "clientWidth",
        offsetHeight: "offsetWidth",
        scrollHeight: "scrollWidth",
        pageYOffset: "pageXOffset",
        offsetTop: "offsetLeft",
        scrollTop: "scrollLeft",
        top: "left"
      };

      var AxisResolver = /*#__PURE__*/function () {
        /**
         * @param {?=} vertical
         */
        function AxisResolver() {
          var vertical = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : true;

          _classCallCheck(this, AxisResolver);

          this.vertical = vertical;
          this.propsMap = vertical ? VerticalProps : HorizontalProps;
        }
        /**
         * @return {?}
         */


        _createClass(AxisResolver, [{
          key: "clientHeightKey",
          value: function clientHeightKey() {
            return this.propsMap.clientHeight;
          }
          /**
           * @return {?}
           */

        }, {
          key: "offsetHeightKey",
          value: function offsetHeightKey() {
            return this.propsMap.offsetHeight;
          }
          /**
           * @return {?}
           */

        }, {
          key: "scrollHeightKey",
          value: function scrollHeightKey() {
            return this.propsMap.scrollHeight;
          }
          /**
           * @return {?}
           */

        }, {
          key: "pageYOffsetKey",
          value: function pageYOffsetKey() {
            return this.propsMap.pageYOffset;
          }
          /**
           * @return {?}
           */

        }, {
          key: "offsetTopKey",
          value: function offsetTopKey() {
            return this.propsMap.offsetTop;
          }
          /**
           * @return {?}
           */

        }, {
          key: "scrollTopKey",
          value: function scrollTopKey() {
            return this.propsMap.scrollTop;
          }
          /**
           * @return {?}
           */

        }, {
          key: "topKey",
          value: function topKey() {
            return this.propsMap.top;
          }
        }]);

        return AxisResolver;
      }();
      /**
       * @fileoverview added by tsickle
       * @suppress {checkTypes,extraRequire,missingOverride,missingReturn,unusedPrivateMembers,uselessCode} checked by tsc
       */

      /**
       * @record
       */

      /**
       * @record
       */

      /**
       * @record
       */

      /**
       * @record
       */

      /**
       * @param {?} alwaysCallback
       * @param {?} shouldFireScrollEvent
       * @param {?} isTriggeredCurrentTotal
       * @return {?}
       */


      function shouldTriggerEvents(alwaysCallback, shouldFireScrollEvent, isTriggeredCurrentTotal) {
        if (alwaysCallback && shouldFireScrollEvent) {
          return true;
        }

        if (!isTriggeredCurrentTotal && shouldFireScrollEvent) {
          return true;
        }

        return false;
      }
      /**
       * @fileoverview added by tsickle
       * @suppress {checkTypes,extraRequire,missingOverride,missingReturn,unusedPrivateMembers,uselessCode} checked by tsc
       */

      /**
       * @param {?} __0
       * @return {?}
       */


      function createResolver(_ref) {
        var windowElement = _ref.windowElement,
            axis = _ref.axis;
        return createResolverWithContainer({
          axis: axis,
          isWindow: isElementWindow(windowElement)
        }, windowElement);
      }
      /**
       * @param {?} resolver
       * @param {?} windowElement
       * @return {?}
       */


      function createResolverWithContainer(resolver, windowElement) {
        /** @type {?} */
        var container = resolver.isWindow || windowElement && !windowElement.nativeElement ? windowElement : windowElement.nativeElement;
        return Object.assign(Object.assign({}, resolver), {
          container: container
        });
      }
      /**
       * @param {?} windowElement
       * @return {?}
       */


      function isElementWindow(windowElement) {
        /** @type {?} */
        var isWindow = ['Window', 'global'].some(
        /**
        * @param {?} obj
        * @return {?}
        */
        function (obj) {
          return Object.prototype.toString.call(windowElement).includes(obj);
        });
        return isWindow;
      }
      /**
       * @param {?} isContainerWindow
       * @param {?} windowElement
       * @return {?}
       */


      function getDocumentElement(isContainerWindow, windowElement) {
        return isContainerWindow ? windowElement.document.documentElement : null;
      }
      /**
       * @param {?} element
       * @param {?} resolver
       * @return {?}
       */


      function calculatePoints(element, resolver) {
        /** @type {?} */
        var height = extractHeightForElement(resolver);
        return resolver.isWindow ? calculatePointsForWindow(height, element, resolver) : calculatePointsForElement(height, element, resolver);
      }
      /**
       * @param {?} height
       * @param {?} element
       * @param {?} resolver
       * @return {?}
       */


      function calculatePointsForWindow(height, element, resolver) {
        var axis = resolver.axis,
            container = resolver.container,
            isWindow = resolver.isWindow;

        var _extractHeightPropKey = extractHeightPropKeys(axis),
            offsetHeightKey = _extractHeightPropKey.offsetHeightKey,
            clientHeightKey = _extractHeightPropKey.clientHeightKey; // scrolled until now / current y point

        /** @type {?} */


        var scrolled = height + getElementPageYOffset(getDocumentElement(isWindow, container), axis, isWindow); // total height / most bottom y point

        /** @type {?} */

        var nativeElementHeight = getElementHeight(element.nativeElement, isWindow, offsetHeightKey, clientHeightKey);
        /** @type {?} */

        var totalToScroll = getElementOffsetTop(element.nativeElement, axis, isWindow) + nativeElementHeight;
        return {
          height: height,
          scrolled: scrolled,
          totalToScroll: totalToScroll,
          isWindow: isWindow
        };
      }
      /**
       * @param {?} height
       * @param {?} element
       * @param {?} resolver
       * @return {?}
       */


      function calculatePointsForElement(height, element, resolver) {
        var axis = resolver.axis,
            container = resolver.container; // perhaps use container.offsetTop instead of 'scrollTop'

        /** @type {?} */

        var scrolled = container[axis.scrollTopKey()];
        /** @type {?} */

        var totalToScroll = container[axis.scrollHeightKey()];
        return {
          height: height,
          scrolled: scrolled,
          totalToScroll: totalToScroll,
          isWindow: false
        };
      }
      /**
       * @param {?} axis
       * @return {?}
       */


      function extractHeightPropKeys(axis) {
        return {
          offsetHeightKey: axis.offsetHeightKey(),
          clientHeightKey: axis.clientHeightKey()
        };
      }
      /**
       * @param {?} __0
       * @return {?}
       */


      function extractHeightForElement(_ref2) {
        var container = _ref2.container,
            isWindow = _ref2.isWindow,
            axis = _ref2.axis;

        var _extractHeightPropKey2 = extractHeightPropKeys(axis),
            offsetHeightKey = _extractHeightPropKey2.offsetHeightKey,
            clientHeightKey = _extractHeightPropKey2.clientHeightKey;

        return getElementHeight(container, isWindow, offsetHeightKey, clientHeightKey);
      }
      /**
       * @param {?} elem
       * @param {?} isWindow
       * @param {?} offsetHeightKey
       * @param {?} clientHeightKey
       * @return {?}
       */


      function getElementHeight(elem, isWindow, offsetHeightKey, clientHeightKey) {
        if (isNaN(elem[offsetHeightKey])) {
          /** @type {?} */
          var docElem = getDocumentElement(isWindow, elem);
          return docElem ? docElem[clientHeightKey] : 0;
        } else {
          return elem[offsetHeightKey];
        }
      }
      /**
       * @param {?} elem
       * @param {?} axis
       * @param {?} isWindow
       * @return {?}
       */


      function getElementOffsetTop(elem, axis, isWindow) {
        /** @type {?} */
        var topKey = axis.topKey(); // elem = elem.nativeElement;

        if (!elem.getBoundingClientRect) {
          // || elem.css('none')) {
          return;
        }

        return elem.getBoundingClientRect()[topKey] + getElementPageYOffset(elem, axis, isWindow);
      }
      /**
       * @param {?} elem
       * @param {?} axis
       * @param {?} isWindow
       * @return {?}
       */


      function getElementPageYOffset(elem, axis, isWindow) {
        /** @type {?} */
        var pageYOffset = axis.pageYOffsetKey();
        /** @type {?} */

        var scrollTop = axis.scrollTopKey();
        /** @type {?} */

        var offsetTop = axis.offsetTopKey();

        if (isNaN(window.pageYOffset)) {
          return getDocumentElement(isWindow, elem)[scrollTop];
        } else if (elem.ownerDocument) {
          return elem.ownerDocument.defaultView[pageYOffset];
        } else {
          return elem[offsetTop];
        }
      }
      /**
       * @fileoverview added by tsickle
       * @suppress {checkTypes,extraRequire,missingOverride,missingReturn,unusedPrivateMembers,uselessCode} checked by tsc
       */

      /**
       * @param {?} container
       * @param {?} distance
       * @param {?} scrollingDown
       * @return {?}
       */


      function shouldFireScrollEvent(container, distance, scrollingDown) {
        /** @type {?} */
        var remaining;
        /** @type {?} */

        var containerBreakpoint;

        if (container.totalToScroll <= 0) {
          return false;
        }
        /** @type {?} */


        var scrolledUntilNow = container.isWindow ? container.scrolled : container.height + container.scrolled;

        if (scrollingDown) {
          remaining = (container.totalToScroll - scrolledUntilNow) / container.totalToScroll;
          containerBreakpoint = distance.down / 10;
        } else {
          /** @type {?} */
          var totalHiddenContentHeight = container.scrolled + (container.totalToScroll - scrolledUntilNow);
          remaining = container.scrolled / totalHiddenContentHeight;
          containerBreakpoint = distance.up / 10;
        }
        /** @type {?} */


        var shouldFireEvent = remaining <= containerBreakpoint;
        return shouldFireEvent;
      }
      /**
       * @param {?} lastScrollPosition
       * @param {?} container
       * @return {?}
       */


      function isScrollingDownwards(lastScrollPosition, container) {
        return lastScrollPosition < container.scrolled;
      }
      /**
       * @param {?} lastScrollPosition
       * @param {?} container
       * @param {?} distance
       * @return {?}
       */


      function getScrollStats(lastScrollPosition, container, distance) {
        /** @type {?} */
        var scrollDown = isScrollingDownwards(lastScrollPosition, container);
        return {
          fire: shouldFireScrollEvent(container, distance, scrollDown),
          scrollDown: scrollDown
        };
      }
      /**
       * @param {?} position
       * @param {?} scrollState
       * @return {?}
       */

      /**
       * @param {?} totalToScroll
       * @param {?} scrollState
       * @return {?}
       */

      /**
       * @param {?} scrollState
       * @return {?}
       */

      /**
       * @param {?} scroll
       * @param {?} scrollState
       * @param {?} triggered
       * @param {?} isScrollingDown
       * @return {?}
       */

      /**
       * @param {?} totalToScroll
       * @param {?} scrollState
       * @param {?} isScrollingDown
       * @return {?}
       */

      /**
       * @param {?} scrollState
       * @param {?} scrolledUntilNow
       * @param {?} totalToScroll
       * @return {?}
       */

      /**
       * @fileoverview added by tsickle
       * @suppress {checkTypes,extraRequire,missingOverride,missingReturn,unusedPrivateMembers,uselessCode} checked by tsc
       */


      var ScrollState = /*#__PURE__*/function () {
        /**
         * @param {?} __0
         */
        function ScrollState(_ref3) {
          var totalToScroll = _ref3.totalToScroll;

          _classCallCheck(this, ScrollState);

          this.lastScrollPosition = 0;
          this.lastTotalToScroll = 0;
          this.totalToScroll = 0;
          this.triggered = {
            down: 0,
            up: 0
          };
          this.totalToScroll = totalToScroll;
        }
        /**
         * @param {?} position
         * @return {?}
         */


        _createClass(ScrollState, [{
          key: "updateScrollPosition",
          value: function updateScrollPosition(position) {
            return this.lastScrollPosition = position;
          }
          /**
           * @param {?} totalToScroll
           * @return {?}
           */

        }, {
          key: "updateTotalToScroll",
          value: function updateTotalToScroll(totalToScroll) {
            if (this.lastTotalToScroll !== totalToScroll) {
              this.lastTotalToScroll = this.totalToScroll;
              this.totalToScroll = totalToScroll;
            }
          }
          /**
           * @param {?} scrolledUntilNow
           * @param {?} totalToScroll
           * @return {?}
           */

        }, {
          key: "updateScroll",
          value: function updateScroll(scrolledUntilNow, totalToScroll) {
            this.updateScrollPosition(scrolledUntilNow);
            this.updateTotalToScroll(totalToScroll);
          }
          /**
           * @param {?} scroll
           * @param {?} isScrollingDown
           * @return {?}
           */

        }, {
          key: "updateTriggeredFlag",
          value: function updateTriggeredFlag(scroll, isScrollingDown) {
            if (isScrollingDown) {
              this.triggered.down = scroll;
            } else {
              this.triggered.up = scroll;
            }
          }
          /**
           * @param {?} totalToScroll
           * @param {?} isScrollingDown
           * @return {?}
           */

        }, {
          key: "isTriggeredScroll",
          value: function isTriggeredScroll(totalToScroll, isScrollingDown) {
            return isScrollingDown ? this.triggered.down === totalToScroll : this.triggered.up === totalToScroll;
          }
        }]);

        return ScrollState;
      }();
      /**
       * @fileoverview added by tsickle
       * @suppress {checkTypes,extraRequire,missingOverride,missingReturn,unusedPrivateMembers,uselessCode} checked by tsc
       */

      /**
       * @param {?} config
       * @return {?}
       */


      function createScroller(config) {
        var scrollContainer = config.scrollContainer,
            scrollWindow = config.scrollWindow,
            element = config.element,
            fromRoot = config.fromRoot;
        /** @type {?} */

        var resolver = createResolver({
          axis: new AxisResolver(!config.horizontal),
          windowElement: resolveContainerElement(scrollContainer, scrollWindow, element, fromRoot)
        });
        /** @type {?} */

        var scrollState = new ScrollState({
          totalToScroll: calculatePoints(element, resolver)
        });
        /** @type {?} */

        var options = {
          container: resolver.container,
          throttle: config.throttle
        };
        /** @type {?} */

        var distance = {
          up: config.upDistance,
          down: config.downDistance
        };
        return attachScrollEvent(options).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["mergeMap"])(
        /**
        * @return {?}
        */
        function () {
          return Object(rxjs__WEBPACK_IMPORTED_MODULE_1__["of"])(calculatePoints(element, resolver));
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["map"])(
        /**
        * @param {?} positionStats
        * @return {?}
        */
        function (positionStats) {
          return toInfiniteScrollParams(scrollState.lastScrollPosition, positionStats, distance);
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["tap"])(
        /**
        * @param {?} __0
        * @return {?}
        */
        function (_ref4) {
          var stats = _ref4.stats;
          return scrollState.updateScroll(stats.scrolled, stats.totalToScroll);
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["filter"])(
        /**
        * @param {?} __0
        * @return {?}
        */
        function (_ref5) {
          var fire = _ref5.fire,
              scrollDown = _ref5.scrollDown,
              totalToScroll = _ref5.stats.totalToScroll;
          return shouldTriggerEvents(config.alwaysCallback, fire, scrollState.isTriggeredScroll(totalToScroll, scrollDown));
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["tap"])(
        /**
        * @param {?} __0
        * @return {?}
        */
        function (_ref6) {
          var scrollDown = _ref6.scrollDown,
              totalToScroll = _ref6.stats.totalToScroll;
          scrollState.updateTriggeredFlag(totalToScroll, scrollDown);
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["map"])(toInfiniteScrollAction));
      }
      /**
       * @param {?} options
       * @return {?}
       */


      function attachScrollEvent(options) {
        /** @type {?} */
        var obs = Object(rxjs__WEBPACK_IMPORTED_MODULE_1__["fromEvent"])(options.container, 'scroll'); // For an unknown reason calling `sampleTime()` causes trouble for many users, even with `options.throttle = 0`.
        // Let's avoid calling the function unless needed.
        // See https://github.com/orizens/ngx-infinite-scroll/issues/198

        if (options.throttle) {
          obs = obs.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["sampleTime"])(options.throttle));
        }

        return obs;
      }
      /**
       * @param {?} lastScrollPosition
       * @param {?} stats
       * @param {?} distance
       * @return {?}
       */


      function toInfiniteScrollParams(lastScrollPosition, stats, distance) {
        var _getScrollStats = getScrollStats(lastScrollPosition, stats, distance),
            scrollDown = _getScrollStats.scrollDown,
            fire = _getScrollStats.fire;

        return {
          scrollDown: scrollDown,
          fire: fire,
          stats: stats
        };
      }
      /** @type {?} */


      var InfiniteScrollActions = {
        DOWN: '[NGX_ISE] DOWN',
        UP: '[NGX_ISE] UP'
      };
      /**
       * @param {?} response
       * @return {?}
       */

      function toInfiniteScrollAction(response) {
        var scrollDown = response.scrollDown,
            currentScrollPosition = response.stats.scrolled;
        return {
          type: scrollDown ? InfiniteScrollActions.DOWN : InfiniteScrollActions.UP,
          payload: {
            currentScrollPosition: currentScrollPosition
          }
        };
      }
      /**
       * @fileoverview added by tsickle
       * @suppress {checkTypes,extraRequire,missingOverride,missingReturn,unusedPrivateMembers,uselessCode} checked by tsc
       */


      var InfiniteScrollDirective = /*#__PURE__*/function () {
        /**
         * @param {?} element
         * @param {?} zone
         */
        function InfiniteScrollDirective(element, zone) {
          _classCallCheck(this, InfiniteScrollDirective);

          this.element = element;
          this.zone = zone;
          this.scrolled = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"]();
          this.scrolledUp = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"]();
          this.infiniteScrollDistance = 2;
          this.infiniteScrollUpDistance = 1.5;
          this.infiniteScrollThrottle = 150;
          this.infiniteScrollDisabled = false;
          this.infiniteScrollContainer = null;
          this.scrollWindow = true;
          this.immediateCheck = false;
          this.horizontal = false;
          this.alwaysCallback = false;
          this.fromRoot = false;
        }
        /**
         * @return {?}
         */


        _createClass(InfiniteScrollDirective, [{
          key: "ngAfterViewInit",
          value: function ngAfterViewInit() {
            if (!this.infiniteScrollDisabled) {
              this.setup();
            }
          }
          /**
           * @param {?} __0
           * @return {?}
           */

        }, {
          key: "ngOnChanges",
          value: function ngOnChanges(_ref7) {
            var infiniteScrollContainer = _ref7.infiniteScrollContainer,
                infiniteScrollDisabled = _ref7.infiniteScrollDisabled,
                infiniteScrollDistance = _ref7.infiniteScrollDistance;

            /** @type {?} */
            var containerChanged = inputPropChanged(infiniteScrollContainer);
            /** @type {?} */

            var disabledChanged = inputPropChanged(infiniteScrollDisabled);
            /** @type {?} */

            var distanceChanged = inputPropChanged(infiniteScrollDistance);
            /** @type {?} */

            var shouldSetup = !disabledChanged && !this.infiniteScrollDisabled || disabledChanged && !infiniteScrollDisabled.currentValue || distanceChanged;

            if (containerChanged || disabledChanged || distanceChanged) {
              this.destroyScroller();

              if (shouldSetup) {
                this.setup();
              }
            }
          }
          /**
           * @return {?}
           */

        }, {
          key: "setup",
          value: function setup() {
            var _this8 = this;

            if (hasWindowDefined()) {
              this.zone.runOutsideAngular(
              /**
              * @return {?}
              */
              function () {
                _this8.disposeScroller = createScroller({
                  fromRoot: _this8.fromRoot,
                  alwaysCallback: _this8.alwaysCallback,
                  disable: _this8.infiniteScrollDisabled,
                  downDistance: _this8.infiniteScrollDistance,
                  element: _this8.element,
                  horizontal: _this8.horizontal,
                  scrollContainer: _this8.infiniteScrollContainer,
                  scrollWindow: _this8.scrollWindow,
                  throttle: _this8.infiniteScrollThrottle,
                  upDistance: _this8.infiniteScrollUpDistance
                }).subscribe(
                /**
                * @param {?} payload
                * @return {?}
                */
                function (payload) {
                  return _this8.zone.run(
                  /**
                  * @return {?}
                  */
                  function () {
                    return _this8.handleOnScroll(payload);
                  });
                });
              });
            }
          }
          /**
           * @param {?} __0
           * @return {?}
           */

        }, {
          key: "handleOnScroll",
          value: function handleOnScroll(_ref8) {
            var type = _ref8.type,
                payload = _ref8.payload;

            switch (type) {
              case InfiniteScrollActions.DOWN:
                return this.scrolled.emit(payload);

              case InfiniteScrollActions.UP:
                return this.scrolledUp.emit(payload);

              default:
                return;
            }
          }
          /**
           * @return {?}
           */

        }, {
          key: "ngOnDestroy",
          value: function ngOnDestroy() {
            this.destroyScroller();
          }
          /**
           * @return {?}
           */

        }, {
          key: "destroyScroller",
          value: function destroyScroller() {
            if (this.disposeScroller) {
              this.disposeScroller.unsubscribe();
            }
          }
        }]);

        return InfiniteScrollDirective;
      }();

      InfiniteScrollDirective.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"],
        args: [{
          selector: '[infiniteScroll], [infinite-scroll], [data-infinite-scroll]'
        }]
      }];
      /** @nocollapse */

      InfiniteScrollDirective.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ElementRef"]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["NgZone"]
        }];
      };

      InfiniteScrollDirective.propDecorators = {
        scrolled: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Output"]
        }],
        scrolledUp: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Output"]
        }],
        infiniteScrollDistance: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"]
        }],
        infiniteScrollUpDistance: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"]
        }],
        infiniteScrollThrottle: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"]
        }],
        infiniteScrollDisabled: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"]
        }],
        infiniteScrollContainer: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"]
        }],
        scrollWindow: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"]
        }],
        immediateCheck: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"]
        }],
        horizontal: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"]
        }],
        alwaysCallback: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"]
        }],
        fromRoot: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"]
        }]
      };
      /**
       * @fileoverview added by tsickle
       * @suppress {checkTypes,extraRequire,missingOverride,missingReturn,unusedPrivateMembers,uselessCode} checked by tsc
       */

      var InfiniteScrollModule = function InfiniteScrollModule() {
        _classCallCheck(this, InfiniteScrollModule);
      };

      InfiniteScrollModule.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"],
        args: [{
          declarations: [InfiniteScrollDirective],
          exports: [InfiniteScrollDirective],
          imports: [],
          providers: []
        }]
      }];
      /**
       * @fileoverview added by tsickle
       * @suppress {checkTypes,extraRequire,missingOverride,missingReturn,unusedPrivateMembers,uselessCode} checked by tsc
       */

      /**
       * @fileoverview added by tsickle
       * @suppress {checkTypes,extraRequire,missingOverride,missingReturn,unusedPrivateMembers,uselessCode} checked by tsc
       */

      /**
       * Angular library starter.
       * Build an Angular library compatible with AoT compilation & Tree shaking.
       * Written by Roberto Simonetti.
       * MIT license.
       * https://github.com/robisim74/angular-library-starter
       */

      /**
       * Entry point for all public APIs of the package.
       */

      /**
       * @fileoverview added by tsickle
       * @suppress {checkTypes,extraRequire,missingOverride,missingReturn,unusedPrivateMembers,uselessCode} checked by tsc
       */

      /**
       * Generated bundle index. Do not edit.
       */
      //# sourceMappingURL=ngx-infinite-scroll.js.map

      /***/
    },

    /***/
    "NxIM":
    /*!*********************************************************!*\
      !*** ./node_modules/@iconify/icons-ic/twotone-image.js ***!
      \*********************************************************/

    /*! no static exports found */

    /***/
    function NxIM(module, exports) {
      var data = {
        "body": "<path opacity=\".3\" d=\"M5 19h14V5H5v14zm4-5.86l2.14 2.58l3-3.87L18 17H6l3-3.86z\" fill=\"currentColor\"/><path d=\"M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14zm-4.86-7.14l-3 3.86L9 13.14L6 17h12z\" fill=\"currentColor\"/>",
        "width": 24,
        "height": 24
      };
      exports.__esModule = true;
      exports["default"] = data;
      /***/
    },

    /***/
    "O/8V":
    /*!***************************************************************************************************************************!*\
      !*** ./src/app/modules/scenarios/pages/scenarios-index/components/scenarios-table-menu/scenarios-table-menu.component.ts ***!
      \***************************************************************************************************************************/

    /*! exports provided: ScenariosTableMenuComponent */

    /***/
    function O8V(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ScenariosTableMenuComponent", function () {
        return ScenariosTableMenuComponent;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _raw_loader_scenarios_table_menu_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! raw-loader!./scenarios-table-menu.component.html */
      "VQqO");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-add */
      "7wwx");
      /* harmony import */


      var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_3__);
      /* harmony import */


      var _iconify_icons_ic_twotone_label__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-label */
      "ll2Q");
      /* harmony import */


      var _iconify_icons_ic_twotone_label__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_label__WEBPACK_IMPORTED_MODULE_4__);
      /* harmony import */


      var _iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-star */
      "bE8U");
      /* harmony import */


      var _iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_5__);
      /* harmony import */


      var _iconify_icons_ic_twotone_view_headline__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-view-headline */
      "29B6");
      /* harmony import */


      var _iconify_icons_ic_twotone_view_headline__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_view_headline__WEBPACK_IMPORTED_MODULE_6__);
      /* harmony import */


      var _vex_animations_fade_in_right_animation__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @vex/animations/fade-in-right.animation */
      "yriF");
      /* harmony import */


      var _vex_animations_stagger_animation__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @vex/animations/stagger.animation */
      "UOrl");
      /* harmony import */


      var _scenarios_pages_scenarios_index_services_scenarios_index_paginator_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @scenarios/pages/scenarios-index/services/scenarios-index-paginator.service */
      "crox");

      var ScenariosTableMenuComponent = /*#__PURE__*/function () {
        function ScenariosTableMenuComponent(scenariosIndexPaginatorService) {
          _classCallCheck(this, ScenariosTableMenuComponent);

          this.scenariosIndexPaginatorService = scenariosIndexPaginatorService;
          this.items = [{
            type: 'link',
            id: 'all',
            icon: _iconify_icons_ic_twotone_view_headline__WEBPACK_IMPORTED_MODULE_6___default.a,
            label: 'All'
          }, // {
          //   type: 'link',
          //   id: 'recent',
          //   icon: icHistory,
          //   label: 'Recent'
          // },
          {
            type: 'link',
            id: 'starred',
            icon: _iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_5___default.a,
            label: 'Starred'
          }, {
            type: 'subheading',
            label: 'Priority'
          }, {
            type: 'link',
            id: 'high',
            icon: _iconify_icons_ic_twotone_label__WEBPACK_IMPORTED_MODULE_4___default.a,
            label: 'High',
            classes: {
              icon: 'text-primary-500'
            }
          }, {
            type: 'link',
            id: 'medium',
            icon: _iconify_icons_ic_twotone_label__WEBPACK_IMPORTED_MODULE_4___default.a,
            label: 'Medium',
            classes: {
              icon: 'text-green-500'
            }
          }, {
            type: 'link',
            id: 'low',
            icon: _iconify_icons_ic_twotone_label__WEBPACK_IMPORTED_MODULE_4___default.a,
            label: 'Low',
            classes: {
              icon: 'text-amber-500'
            }
          }, {
            type: 'link',
            id: 'none',
            icon: _iconify_icons_ic_twotone_label__WEBPACK_IMPORTED_MODULE_4___default.a,
            label: 'None',
            classes: {
              icon: 'text-gray-500'
            }
          }];
          this.filter = new _angular_core__WEBPACK_IMPORTED_MODULE_2__["EventEmitter"]();
          this.create = new _angular_core__WEBPACK_IMPORTED_MODULE_2__["EventEmitter"]();
          this.activeCategory = 'all'; // Icons

          this.icAdd = _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_3___default.a;
        }

        _createClass(ScenariosTableMenuComponent, [{
          key: "ngOnInit",
          value: function ngOnInit() {
            var _this9 = this;

            this.scenariosIndexPaginatorService.pageSize.subscribe(function (pageSize) {
              _this9.pageSize = pageSize;
            });
          }
        }, {
          key: "isActive",
          value: function isActive(category) {
            return this.activeCategory === category;
          }
        }, {
          key: "setFilter",
          value: function setFilter(category) {
            this.activeCategory = category;
            var event = {
              filter: undefined
            };

            switch (category) {
              case 'all':
                event.filter = undefined;
                break;

              case 'starred':
                event.filter = 'starred';
                break;

              case 'recent':
                event.filter = 'updated_at';
                break;

              case 'high':
                event.filter = 'high_priority';
                break;

              case 'medium':
                event.filter = 'medium_priority';
                break;

              case 'low':
                event.filter = 'low_priority';
                break;

              case 'none':
                event.filter = 'none_priority';
                break;
            }

            this.filter.emit(event);
          }
        }]);

        return ScenariosTableMenuComponent;
      }();

      ScenariosTableMenuComponent.ctorParameters = function () {
        return [{
          type: _scenarios_pages_scenarios_index_services_scenarios_index_paginator_service__WEBPACK_IMPORTED_MODULE_9__["ScenariosIndexPaginatorService"]
        }];
      };

      ScenariosTableMenuComponent.propDecorators = {
        initialFilter: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Input"]
        }],
        items: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Input"]
        }],
        filter: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Output"]
        }],
        create: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Output"]
        }]
      };
      ScenariosTableMenuComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["Component"])({
        selector: 'scenarios-table-menu',
        template: _raw_loader_scenarios_table_menu_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        animations: [_vex_animations_fade_in_right_animation__WEBPACK_IMPORTED_MODULE_7__["fadeInRight400ms"], _vex_animations_stagger_animation__WEBPACK_IMPORTED_MODULE_8__["stagger40ms"]],
        changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_2__["ChangeDetectionStrategy"].OnPush
      })], ScenariosTableMenuComponent);
      /***/
    },

    /***/
    "PCNd":
    /*!*****************************************!*\
      !*** ./src/app/shared/shared.module.ts ***!
      \*****************************************/

    /*! exports provided: SharedModule */

    /***/
    function PCNd(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "SharedModule", function () {
        return SharedModule;
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


      var _shared_pipes_request_component_label_pipe__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @shared/pipes/request-component-label.pipe */
      "A7TT");

      var SharedModule = function SharedModule() {
        _classCallCheck(this, SharedModule);
      };

      SharedModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_shared_pipes_request_component_label_pipe__WEBPACK_IMPORTED_MODULE_3__["RequestComponentLabelPipe"]],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"]],
        exports: [_shared_pipes_request_component_label_pipe__WEBPACK_IMPORTED_MODULE_3__["RequestComponentLabelPipe"]]
      })], SharedModule);
      /***/
    },

    /***/
    "PnnC":
    /*!******************************************************************!*\
      !*** ./node_modules/@iconify/icons-ic/twotone-insert-comment.js ***!
      \******************************************************************/

    /*! no static exports found */

    /***/
    function PnnC(module, exports) {
      var data = {
        "body": "<path opacity=\".3\" d=\"M4 16h14.83L20 17.17V4H4v12zM6 6h12v2H6V6zm0 3h12v2H6V9zm0 3h12v2H6v-2z\" fill=\"currentColor\"/><path d=\"M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4V4c0-1.1-.9-2-2-2zm0 2v13.17L18.83 16H4V4h16zM6 12h12v2H6zm0-3h12v2H6zm0-3h12v2H6z\" fill=\"currentColor\"/>",
        "width": 24,
        "height": 24
      };
      exports.__esModule = true;
      exports["default"] = data;
      /***/
    },

    /***/
    "QIDy":
    /*!*******************************************************************************************!*\
      !*** ./src/app/modules/scenarios/components/scenarios-edit/scenarios-edit.component.scss ***!
      \*******************************************************************************************/

    /*! exports provided: default */

    /***/
    function QIDy(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzY2VuYXJpb3MtZWRpdC5jb21wb25lbnQuc2NzcyJ9 */";
      /***/
    },

    /***/
    "QIdO":
    /*!********************************************************************************************************************!*\
      !*** ./src/app/modules/scenarios/pages/scenario-details/components/requests-create/requests-create.component.scss ***!
      \********************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function QIdO(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJyZXF1ZXN0cy1jcmVhdGUuY29tcG9uZW50LnNjc3MifQ== */";
      /***/
    },

    /***/
    "QMVN":
    /*!*********************************************************************************************************************!*\
      !*** ./src/app/modules/scenarios/pages/scenarios-builder/components/scrumboard-card/scrumboard-card.component.scss ***!
      \*********************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function QMVN(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = ".tag {\n  width: 25px;\n  text-align: center;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uLy4uLy4uLy4uL3NjcnVtYm9hcmQtY2FyZC5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLFdBQUE7RUFDQSxrQkFBQTtBQUNGIiwiZmlsZSI6InNjcnVtYm9hcmQtY2FyZC5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbIi50YWcge1xuICB3aWR0aDogMjVweDtcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xufSJdfQ== */";
      /***/
    },

    /***/
    "QgCS":
    /*!**********************************************************************************************!*\
      !*** ./src/app/modules/requests/components/scrumboard-dialog/scrumboard-dialog.component.ts ***!
      \**********************************************************************************************/

    /*! exports provided: ScrumboardDialogComponent */

    /***/
    function QgCS(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ScrumboardDialogComponent", function () {
        return ScrumboardDialogComponent;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _raw_loader_scrumboard_dialog_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! raw-loader!./scrumboard-dialog.component.html */
      "/74T");
      /* harmony import */


      var _scrumboard_dialog_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! ./scrumboard-dialog.component.scss */
      "me+b");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/material/dialog */
      "iELJ");
      /* harmony import */


      var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-add */
      "7wwx");
      /* harmony import */


      var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_5__);
      /* harmony import */


      var _iconify_icons_ic_twotone_assignment__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-assignment */
      "16CC");
      /* harmony import */


      var _iconify_icons_ic_twotone_assignment__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_assignment__WEBPACK_IMPORTED_MODULE_6__);
      /* harmony import */


      var _iconify_icons_ic_twotone_attach_file__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-attach-file */
      "1kq9");
      /* harmony import */


      var _iconify_icons_ic_twotone_attach_file__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_attach_file__WEBPACK_IMPORTED_MODULE_7__);
      /* harmony import */


      var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-close */
      "5mnX");
      /* harmony import */


      var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_8__);
      /* harmony import */


      var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-delete */
      "e3EN");
      /* harmony import */


      var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_9__);
      /* harmony import */


      var _iconify_icons_ic_twotone_description__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-description */
      "0nnX");
      /* harmony import */


      var _iconify_icons_ic_twotone_description__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_description__WEBPACK_IMPORTED_MODULE_10__);
      /* harmony import */


      var _iconify_icons_ic_twotone_image__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-image */
      "NxIM");
      /* harmony import */


      var _iconify_icons_ic_twotone_image__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_image__WEBPACK_IMPORTED_MODULE_11__);
      /* harmony import */


      var _iconify_icons_ic_twotone_insert_comment__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-insert-comment */
      "PnnC");
      /* harmony import */


      var _iconify_icons_ic_twotone_insert_comment__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_insert_comment__WEBPACK_IMPORTED_MODULE_12__);
      /* harmony import */


      var _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-more-vert */
      "+Chm");
      /* harmony import */


      var _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_13___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_13__);
      /* harmony import */


      var _iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-star */
      "bE8U");
      /* harmony import */


      var _iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_14___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_14__);
      /* harmony import */


      var _core_http_body_param_resource_service__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! @core/http/body-param-resource.service */
      "npeK");
      /* harmony import */


      var _core_http_header_resource_service__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(
      /*! @core/http/header-resource.service */
      "Wbda");
      /* harmony import */


      var _core_http_query_param_resource_service__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(
      /*! @core/http/query-param-resource.service */
      "kqhm");
      /* harmony import */


      var _core_http_response_resource_service__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(
      /*! @core/http/response-resource.service */
      "z06h");
      /* harmony import */


      var _data_schema__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(
      /*! @data/schema */
      "V99k");

      var ScrumboardDialogComponent = /*#__PURE__*/function () {
        function ScrumboardDialogComponent(data, bodyParamResource, dialogRef, headerResource, queryParamResource, responseResource) {
          _classCallCheck(this, ScrumboardDialogComponent);

          this.data = data;
          this.bodyParamResource = bodyParamResource;
          this.dialogRef = dialogRef;
          this.headerResource = headerResource;
          this.queryParamResource = queryParamResource;
          this.responseResource = responseResource;
          this.components = [];
          this.icAssignment = _iconify_icons_ic_twotone_assignment__WEBPACK_IMPORTED_MODULE_6___default.a;
          this.icDescription = _iconify_icons_ic_twotone_description__WEBPACK_IMPORTED_MODULE_10___default.a;
          this.icClose = _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_8___default.a;
          this.icAdd = _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_5___default.a;
          this.icMoreVert = _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_13___default.a;
          this.icDelete = _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_9___default.a;
          this.icImage = _iconify_icons_ic_twotone_image__WEBPACK_IMPORTED_MODULE_11___default.a;
          this.icAttachFile = _iconify_icons_ic_twotone_attach_file__WEBPACK_IMPORTED_MODULE_7___default.a;
          this.icInsertComment = _iconify_icons_ic_twotone_insert_comment__WEBPACK_IMPORTED_MODULE_12___default.a;
          this.icStar = _iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_14___default.a;
        }

        _createClass(ScrumboardDialogComponent, [{
          key: "ngOnInit",
          value: function ngOnInit() {
            this.request = new _data_schema__WEBPACK_IMPORTED_MODULE_19__["Request"](this.data.request);
            var defaultQueryParams = {
              project_id: this.request.projectId
            };
            var bodyParams$ = this.bodyParamResource.index(this.request.id, defaultQueryParams);
            var headers$ = this.headerResource.index(this.request.id, defaultQueryParams);
            var queryParams$ = this.queryParamResource.index(this.request.id, defaultQueryParams);
            var response$ = this.responseResource.index(this.request.id, defaultQueryParams);
            this.components = [{
              title: 'Headers',
              data$: headers$
            }, {
              title: 'Query Params',
              data$: queryParams$
            }, {
              title: 'Body Params',
              data$: bodyParams$
            }];
            this.response = {
              title: 'Response',
              data$: response$,
              accessed: true
            };
          }
        }, {
          key: "handleTabChange",
          value: function handleTabChange($event) {
            var index = $event.index - 1;

            if (index >= 0) {
              this.components[index].accessed = true;
            }
          } // Helpers

        }, {
          key: "prettyJson",
          value: function prettyJson(json) {
            try {
              return JSON.stringify(JSON.parse(json), null, 2);
            } catch (err) {
              return json;
            }
          }
        }]);

        return ScrumboardDialogComponent;
      }();

      ScrumboardDialogComponent.ctorParameters = function () {
        return [{
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Inject"],
            args: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_4__["MAT_DIALOG_DATA"]]
          }]
        }, {
          type: _core_http_body_param_resource_service__WEBPACK_IMPORTED_MODULE_15__["BodyParamResource"]
        }, {
          type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_4__["MatDialogRef"]
        }, {
          type: _core_http_header_resource_service__WEBPACK_IMPORTED_MODULE_16__["HeaderResource"]
        }, {
          type: _core_http_query_param_resource_service__WEBPACK_IMPORTED_MODULE_17__["QueryParamResource"]
        }, {
          type: _core_http_response_resource_service__WEBPACK_IMPORTED_MODULE_18__["ResponseResource"]
        }];
      };

      ScrumboardDialogComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'vex-scrumboard-dialog',
        template: _raw_loader_scrumboard_dialog_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_scrumboard_dialog_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
      })], ScrumboardDialogComponent);
      /***/
    },

    /***/
    "UAid":
    /*!*************************************************************************************************************************************!*\
      !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/scenarios/components/scenarios-create/scenarios-create.component.html ***!
      \*************************************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function UAid(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "<form (ngSubmit)=\"create()\" [formGroup]=\"form\">\r\n  <div fxLayout=\"row\" fxLayoutAlign=\"start center\" mat-dialog-title>\r\n    <h2 class=\"headline m-0\" fxFlex=\"auto\">{{ form.get('name').value || 'New Scenario' }}</h2>\r\n\r\n    <button [matMenuTriggerFor]=\"settingsMenu\" class=\"text-secondary\" mat-icon-button type=\"button\" matTooltip=\"Priority\">\r\n      <mat-icon [icIcon]=\"icLabel\" [ngClass]=\"selectedPriority.classes\"></mat-icon>\r\n    </button>\r\n\r\n    <button class=\"text-secondary\" mat-dialog-close mat-icon-button type=\"button\">\r\n      <mat-icon [icIcon]=\"icClose\"></mat-icon>\r\n    </button>\r\n  </div>\r\n\r\n  <mat-divider class=\"-mx-6 text-border\"></mat-divider>\r\n\r\n  <mat-dialog-content>\r\n    <mat-tab-group>\r\n      <mat-tab label=\"General\">\r\n        <div fxLayout=\"column\">\r\n          <mat-form-field class=\"mt-6\">\r\n            <mat-label>Name</mat-label>\r\n            <input cdkFocusInitial formControlName=\"name\" matInput>\r\n          </mat-form-field>\r\n\r\n          <mat-form-field>\r\n            <mat-label>Description</mat-label>\r\n            <textarea formControlName=\"description\" matInput></textarea>\r\n          </mat-form-field>\r\n        </div>\r\n      </mat-tab>\r\n      <mat-tab label=\"Requests\">\r\n        <ngx-dropzone class=\"mt-6 mb-3\" (change)=\"onFileSelect($event)\">\r\n          <ngx-dropzone-label>Select or drop a HAR file!</ngx-dropzone-label>\r\n          <ngx-dropzone-preview *ngFor=\"let f of files\" [removable]=\"true\" (removed)=\"onFileRemove(f)\">\r\n              <ngx-dropzone-label>{{ f.name }}</ngx-dropzone-label>\r\n          </ngx-dropzone-preview>\r\n        </ngx-dropzone>\r\n      </mat-tab>\r\n    </mat-tab-group>\r\n  </mat-dialog-content>\r\n\r\n  <mat-dialog-actions align=\"end\">\r\n    <button mat-button mat-dialog-close type=\"button\">CANCEL</button>\r\n    <button [disabled]=\"form.invalid\" color=\"primary\" mat-button type=\"submit\">CREATE</button>\r\n  </mat-dialog-actions>\r\n</form>\r\n\r\n<mat-menu #settingsMenu=\"matMenu\" xPosition=\"before\" yPosition=\"below\">\r\n  <button mat-menu-item *ngFor=\"let priority of scenarioPriorities\" (click)=\"handlePrioritySelect(priority)\">\r\n    <span>{{ priority.name }}</span>\r\n  </button>\r\n</mat-menu>\r\n";
      /***/
    },

    /***/
    "VQqO":
    /*!*******************************************************************************************************************************************************************!*\
      !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/scenarios/pages/scenarios-index/components/scenarios-table-menu/scenarios-table-menu.component.html ***!
      \*******************************************************************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function VQqO(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "<div @stagger class=\"max-w-xxxs w-full\">\n  <div class=\"h-14 mb-6 flex px-gutter sm:px-0\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n    <button (click)=\"create.emit()\" class=\"flex-auto\" mat-raised-button type=\"button\">\n      <ic-icon [icon]=\"icAdd\" class=\"ltr:mr-3 rtl:ml-3\" inline=\"true\" size=\"18px\"></ic-icon>\n      <span>CREATE</span>\n    </button>\n  </div>\n\n  <div class=\"px-gutter sm:px-0\">\n    <ng-container *ngFor=\"let item of items\">\n      <a (click)=\"setFilter(item.id)\"\n         *ngIf=\"item.type === 'link'\"\n         @fadeInRight\n         [class.bg-hover]=\"isActive(item.id)\"\n         [class.text-primary-500]=\"isActive(item.id)\"\n         class=\"list-item mt-2 no-underline flex items-center\"\n         matRipple>\n        <ic-icon [icon]=\"item.icon\" [ngClass]=\"item.classes?.icon\" class=\"ltr:mr-3 rtl:ml-3\" size=\"24px\"></ic-icon>\n        <span>{{ item.label }}</span>\n      </a>\n\n      <h3 *ngIf=\"item.type === 'subheading'\"\n          @fadeInRight\n          class=\"caption text-secondary uppercase font-medium mb-0 mt-6\">{{ item.label }}</h3>\n    </ng-container>\n  </div>\n</div>\n";
      /***/
    },

    /***/
    "W6bZ":
    /*!********************************************************!*\
      !*** ./src/@vex/pipes/date-tokens/date-tokens.pipe.ts ***!
      \********************************************************/

    /*! exports provided: DateTokensPipe */

    /***/
    function W6bZ(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "DateTokensPipe", function () {
        return DateTokensPipe;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");

      var DateTokensPipe = /*#__PURE__*/function () {
        function DateTokensPipe() {
          _classCallCheck(this, DateTokensPipe);
        }

        _createClass(DateTokensPipe, [{
          key: "transform",
          value: function transform(value) {
            if (!(arguments.length <= 1 ? undefined : arguments[1])) {
              throw new Error('[DateTokensPipe]: No args defined, please define your format.');
            }

            return value ? value.toFormat(arguments.length <= 1 ? undefined : arguments[1]) : '';
          }
        }]);

        return DateTokensPipe;
      }();

      DateTokensPipe = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Pipe"])({
        name: 'dateTokens'
      })], DateTokensPipe);
      /***/
    },

    /***/
    "WSkv":
    /*!********************************************************************************************!*\
      !*** ./src/app/modules/scenarios/pages/scenario-details/services/requests-data.service.ts ***!
      \********************************************************************************************/

    /*! exports provided: RequestsDataService */

    /***/
    function WSkv(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "RequestsDataService", function () {
        return RequestsDataService;
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


      var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! rxjs */
      "qCKp");
      /* harmony import */


      var _data_schema_request__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @data/schema/request */
      "WYQo");

      var RequestsDataService = /*#__PURE__*/function () {
        function RequestsDataService() {
          _classCallCheck(this, RequestsDataService);

          this.subject = new rxjs__WEBPACK_IMPORTED_MODULE_2__["BehaviorSubject"]([]);
          this.requests$ = this.subject.asObservable();
        }

        _createClass(RequestsDataService, [{
          key: "set",
          value: function set(requests) {
            this.requests = requests;
            this.subject.next(requests);
          }
        }, {
          key: "add",
          value: function add(request) {
            this.requests.unshift(new _data_schema_request__WEBPACK_IMPORTED_MODULE_3__["Request"](request));
            this.set(this.requests);
          }
        }, {
          key: "delete",
          value: function _delete(id) {
            this.requests.splice(this.requests.findIndex(function (existingRequest) {
              return existingRequest.id === id;
            }), 1);
            this.set(this.requests);
          }
        }]);

        return RequestsDataService;
      }();

      RequestsDataService.ctorParameters = function () {
        return [];
      };

      RequestsDataService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], RequestsDataService);
      /***/
    },

    /***/
    "WZBS":
    /*!***************************************************************************************************!*\
      !*** ./src/app/modules/scenarios/pages/scenarios-index/services/scenarios-index-icons.service.ts ***!
      \***************************************************************************************************/

    /*! exports provided: ScenariosIndexIcons */

    /***/
    function WZBS(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ScenariosIndexIcons", function () {
        return ScenariosIndexIcons;
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


      var _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-cloud-download */
      "MzEE");
      /* harmony import */


      var _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_2__);
      /* harmony import */


      var _iconify_icons_ic_twotone_contacts__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-contacts */
      "rbx1");
      /* harmony import */


      var _iconify_icons_ic_twotone_contacts__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_contacts__WEBPACK_IMPORTED_MODULE_3__);
      /* harmony import */


      var _iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-edit */
      "pN9m");
      /* harmony import */


      var _iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_4__);
      /* harmony import */


      var _iconify_icons_ic_twotone_file_copy__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-file-copy */
      "L5jV");
      /* harmony import */


      var _iconify_icons_ic_twotone_file_copy__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_file_copy__WEBPACK_IMPORTED_MODULE_5__);
      /* harmony import */


      var _iconify_icons_ic_twotone_menu__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-menu */
      "cS8l");
      /* harmony import */


      var _iconify_icons_ic_twotone_menu__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_menu__WEBPACK_IMPORTED_MODULE_6__);
      /* harmony import */


      var _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-search */
      "sF+I");
      /* harmony import */


      var _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_7__);
      /* harmony import */


      var _iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-star */
      "bE8U");
      /* harmony import */


      var _iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_8__);
      /* harmony import */


      var _iconify_icons_ic_twotone_star_border__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-star-border */
      "PNSm");
      /* harmony import */


      var _iconify_icons_ic_twotone_star_border__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_star_border__WEBPACK_IMPORTED_MODULE_9__);

      var ScenariosIndexIcons = function ScenariosIndexIcons() {
        _classCallCheck(this, ScenariosIndexIcons);

        this.icStar = _iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_8___default.a;
        this.icStarBorder = _iconify_icons_ic_twotone_star_border__WEBPACK_IMPORTED_MODULE_9___default.a;
        this.icSearch = _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_7___default.a;
        this.icContacts = _iconify_icons_ic_twotone_contacts__WEBPACK_IMPORTED_MODULE_3___default.a;
        this.icMenu = _iconify_icons_ic_twotone_menu__WEBPACK_IMPORTED_MODULE_6___default.a;
        this.icCloudDownload = _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_2___default.a;
        this.icEdit = _iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_4___default.a;
        this.icFileCopy = _iconify_icons_ic_twotone_file_copy__WEBPACK_IMPORTED_MODULE_5___default.a;
      };

      ScenariosIndexIcons.ctorParameters = function () {
        return [];
      };

      ScenariosIndexIcons = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], ScenariosIndexIcons);
      /***/
    },

    /***/
    "Yn9W":
    /*!***********************************************************************************************************************************************************!*\
      !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/scenarios/pages/scenarios-builder/components/scrumboard-card/scrumboard-card.component.html ***!
      \***********************************************************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function Yn9W(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "<div *ngIf=\"card.cover\" class=\"w-full h-40 overflow-hidden\">\n  <img [src]=\"card.cover.path\" class=\"object-cover w-full h-full\">\n</div>\n\n<div *ngIf=\"!wrapped\" class=\"py-3 px-3\" fxLayout=\"row\" fxLayoutAlign=\"start center\" fxLayoutGap=\"10px\">\n  <div \n    *ngIf=\"card.position !== null\"\n    class=\"tag box bg-app-bar text-secondary rounded caption p-1\"\n    fxFlex=\"0 0 35px\"\n    matTooltip=\"Position\"\n  >\n    <span class=\"box-text\">\n      {{ card.position + 1 }}\n    </span>\n  </div>\n\n  <div fxLayout=\"row wrap\" fxFlex=\"grow\" fxLayoutGap=\"10px\">\n    <h3 fxFlex=\"100px\" class=\"body-2 m-0 select-none text-secondary\">\n      {{ card.method }}\n    </h3>\n\n    <h3 fxFlex=\"85\" class=\"body-2 m-0 select-none\">\n      {{ card.title }}\n    </h3>\n  </div>\n\n  <span fxFlex></span>\n\n  <div fxLayout=\"row\" class=\"mr-0\" fxFlex=\"0 0 150px\">\n    <span fxFlex></span>\n\n    <div class=\"mr-2\" fxFlex=\"50px\" matTooltip=\"Status\">\n      <status-label\n        [okThreshold]=\"399\" \n        [text]=\"card.status\"\n        [status]=\"card.status\"\n        [warningThreshold]=\"499\"\n      >\n      </status-label>\n    </div>\n\n    <div fxFlex=\"75px\" matTooltip=\"Latency\">\n      <status-label\n        [okThreshold]=\"350\" \n        [text]=\"card.latency + ' ms'\"\n        [status]=\"card.latency\"\n        [warningThreshold]=\"1000\"\n      >\n      </status-label>\n    </div>\n  </div>\n</div>\n\n<div *ngIf=\"wrapped\" class=\"py-3 px-3\">\n  <div fxLayout=\"row\" fxLayoutAlign=\"start center\" fxLayoutGap=\"10px\">\n    <div \n      *ngIf=\"card.position !== null\"\n      class=\"tag box bg-app-bar text-secondary rounded caption p-1\"\n      fxFlex=\"0 0 35px\"\n      matTooltip=\"Position\"\n    >\n      <span class=\"box-text\">\n        {{ card.position + 1 }}\n      </span>\n    </div>\n\n    <h3 fxFlex=\"75px\" class=\"body-2 m-0 select-none text-secondary\">\n      {{ card.method }}\n    </h3>\n\n    <h3 class=\"body-2 m-0 select-none\">\n      {{ card.title }}\n    </h3>\n  </div>\n\n  <div css=\"mt-1\" fxLayout=\"row\" fxLayoutAlign=\"start center\" fxLayoutGap=\"10px\">\n    <span fxFlex></span>\n    <div class=\"mr-2\" fxFlex=\"50px\" matTooltip=\"Status\">\n      <status-label\n        [okThreshold]=\"399\" \n        [text]=\"card.status\"\n        [status]=\"card.status\"\n        [warningThreshold]=\"499\"\n      >\n      </status-label>\n    </div>\n\n    <div fxFlex=\"75px\" matTooltip=\"Latency\">\n      <status-label\n        [okThreshold]=\"350\" \n        [text]=\"card.latency + ' ms'\"\n        [status]=\"card.latency\"\n        [warningThreshold]=\"1000\"\n      >\n      </status-label>\n    </div>\n  </div>\n</div>\n";
      /***/
    },

    /***/
    "ZplM":
    /*!******************************************************************************************!*\
      !*** ./src/app/modules/scenarios/pages/scenario-details/scenario-details.component.scss ***!
      \******************************************************************************************/

    /*! exports provided: default */

    /***/
    function ZplM(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = ".table-link {\n  color: #1976d2;\n}\n\n.table-link:hover {\n  text-decoration: underline;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uLy4uL3NjZW5hcmlvLWRldGFpbHMuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSxjQUFBO0FBQ0Y7O0FBRUE7RUFDRSwwQkFBQTtBQUNGIiwiZmlsZSI6InNjZW5hcmlvLWRldGFpbHMuY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyIudGFibGUtbGluayB7XG4gIGNvbG9yOiAjMTk3NmQyO1xufVxuXG4udGFibGUtbGluazpob3ZlciB7XG4gIHRleHQtZGVjb3JhdGlvbjogdW5kZXJsaW5lO1xufSJdfQ== */";
      /***/
    },

    /***/
    "b06q":
    /*!*****************************************************************************************!*\
      !*** ./src/app/modules/scenarios/components/scenarios-edit/scenarios-edit.component.ts ***!
      \*****************************************************************************************/

    /*! exports provided: ScenariosEditComponent */

    /***/
    function b06q(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ScenariosEditComponent", function () {
        return ScenariosEditComponent;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _raw_loader_scenarios_edit_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! raw-loader!./scenarios-edit.component.html */
      "hb0D");
      /* harmony import */


      var _scenarios_edit_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! ./scenarios-edit.component.scss */
      "QIDy");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/forms */
      "s7LF");
      /* harmony import */


      var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/material/dialog */
      "iELJ");
      /* harmony import */


      var _iconify_icons_ic_twotone_business__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-business */
      "6uZp");
      /* harmony import */


      var _iconify_icons_ic_twotone_business__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_business__WEBPACK_IMPORTED_MODULE_6__);
      /* harmony import */


      var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-close */
      "5mnX");
      /* harmony import */


      var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_7__);
      /* harmony import */


      var _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-cloud-download */
      "MzEE");
      /* harmony import */


      var _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_8__);
      /* harmony import */


      var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-delete */
      "e3EN");
      /* harmony import */


      var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_9__);
      /* harmony import */


      var _iconify_icons_ic_twotone_label__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-label */
      "ll2Q");
      /* harmony import */


      var _iconify_icons_ic_twotone_label__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_label__WEBPACK_IMPORTED_MODULE_10__);
      /* harmony import */


      var _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-mail */
      "6qw8");
      /* harmony import */


      var _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_11__);
      /* harmony import */


      var _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-more-vert */
      "+Chm");
      /* harmony import */


      var _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_12__);
      /* harmony import */


      var _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-person */
      "KaaH");
      /* harmony import */


      var _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_13___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_13__);
      /* harmony import */


      var _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-phone */
      "YA1h");
      /* harmony import */


      var _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_14___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_14__);
      /* harmony import */


      var _iconify_icons_ic_twotone_print__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-print */
      "yHIK");
      /* harmony import */


      var _iconify_icons_ic_twotone_print__WEBPACK_IMPORTED_MODULE_15___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_print__WEBPACK_IMPORTED_MODULE_15__);
      /* harmony import */


      var _data_schema__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(
      /*! @data/schema */
      "V99k");

      var ScenariosEditComponent = /*#__PURE__*/function () {
        function ScenariosEditComponent(scenario, dialogRef, fb) {
          _classCallCheck(this, ScenariosEditComponent);

          this.scenario = scenario;
          this.dialogRef = dialogRef;
          this.fb = fb;
          this.form = this.fb.group({
            name: null,
            description: null
          });
          this.onEdit = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"](); // icons

          this.icMoreVert = _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_12___default.a;
          this.icClose = _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_7___default.a;
          this.icPrint = _iconify_icons_ic_twotone_print__WEBPACK_IMPORTED_MODULE_15___default.a;
          this.icDownload = _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_8___default.a;
          this.icDelete = _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_9___default.a;
          this.icBusiness = _iconify_icons_ic_twotone_business__WEBPACK_IMPORTED_MODULE_6___default.a;
          this.icPerson = _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_13___default.a;
          this.icEmail = _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_11___default.a;
          this.icPhone = _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_14___default.a;
          this.icLabel = _iconify_icons_ic_twotone_label__WEBPACK_IMPORTED_MODULE_10___default.a;
          this.scenarioPriorities = _data_schema__WEBPACK_IMPORTED_MODULE_16__["ScenarioPriorityData"];
        }

        _createClass(ScenariosEditComponent, [{
          key: "ngOnInit",
          value: function ngOnInit() {
            this.form.patchValue(this.scenario);
            var priorityIndex = this.scenarioPriorities.length - this.scenario.priority - 1;
            this.selectedPriority = this.scenarioPriorities[priorityIndex];
          }
        }, {
          key: "save",
          value: function save() {
            var form = this.form.value;
            form.priority = this.selectedPriority.value;
            this.onEdit.emit(form);
            this.dialogRef.close();
          }
        }, {
          key: "handlePrioritySelect",
          value: function handlePrioritySelect(priority) {
            this.selectedPriority = priority;
          }
        }]);

        return ScenariosEditComponent;
      }();

      ScenariosEditComponent.ctorParameters = function () {
        return [{
          type: _data_schema__WEBPACK_IMPORTED_MODULE_16__["Scenario"],
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Inject"],
            args: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MAT_DIALOG_DATA"]]
          }]
        }, {
          type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MatDialogRef"]
        }, {
          type: _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormBuilder"]
        }];
      };

      ScenariosEditComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'scenarios-edit',
        template: _raw_loader_scenarios_edit_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_scenarios_edit_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
      })], ScenariosEditComponent);
      /***/
    },

    /***/
    "bhgl":
    /*!***************************************************************************************************************************!*\
      !*** ./src/app/modules/scenarios/pages/scenarios-index/components/scenarios-data-table/scenarios-data-table.component.ts ***!
      \***************************************************************************************************************************/

    /*! exports provided: ScenariosDataTableComponent */

    /***/
    function bhgl(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ScenariosDataTableComponent", function () {
        return ScenariosDataTableComponent;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _raw_loader_scenarios_data_table_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! raw-loader!./scenarios-data-table.component.html */
      "EMV3");
      /* harmony import */


      var _scenarios_data_table_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! ./scenarios-data-table.component.scss */
      "5x1r");
      /* harmony import */


      var _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/cdk/collections */
      "CtHx");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_forms__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/forms */
      "s7LF");
      /* harmony import */


      var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/material/form-field */
      "Q2Ze");
      /* harmony import */


      var _angular_material_paginator__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @angular/material/paginator */
      "5QHs");
      /* harmony import */


      var _angular_material_sort__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @angular/material/sort */
      "LUZP");
      /* harmony import */


      var _angular_material_table__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @angular/material/table */
      "OaSA");
      /* harmony import */


      var rxjs_operators__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! rxjs/operators */
      "kU1M");
      /* harmony import */


      var _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-cloud-download */
      "MzEE");
      /* harmony import */


      var _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_11__);
      /* harmony import */


      var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-delete */
      "e3EN");
      /* harmony import */


      var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_12__);
      /* harmony import */


      var _iconify_icons_ic_twotone_delete_forever__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-delete-forever */
      "74KL");
      /* harmony import */


      var _iconify_icons_ic_twotone_delete_forever__WEBPACK_IMPORTED_MODULE_13___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_delete_forever__WEBPACK_IMPORTED_MODULE_13__);
      /* harmony import */


      var _iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-edit */
      "pN9m");
      /* harmony import */


      var _iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_14___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_14__);
      /* harmony import */


      var _iconify_icons_ic_twotone_filter_list__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-filter-list */
      "+4LO");
      /* harmony import */


      var _iconify_icons_ic_twotone_filter_list__WEBPACK_IMPORTED_MODULE_15___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_filter_list__WEBPACK_IMPORTED_MODULE_15__);
      /* harmony import */


      var _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-more-vert */
      "+Chm");
      /* harmony import */


      var _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_16___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_16__);
      /* harmony import */


      var _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-search */
      "sF+I");
      /* harmony import */


      var _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_17___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_17__);
      /* harmony import */


      var _iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-star */
      "bE8U");
      /* harmony import */


      var _iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_18___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_18__);
      /* harmony import */


      var _iconify_icons_ic_twotone_star_border__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-star-border */
      "PNSm");
      /* harmony import */


      var _iconify_icons_ic_twotone_star_border__WEBPACK_IMPORTED_MODULE_19___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_star_border__WEBPACK_IMPORTED_MODULE_19__);
      /* harmony import */


      var _vex_animations_fade_in_up_animation__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(
      /*! @vex/animations/fade-in-up.animation */
      "y3Ys");
      /* harmony import */


      var _vex_animations_scale_fade_in_animation__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(
      /*! @vex/animations/scale-fade-in.animation */
      "U0RW");
      /* harmony import */


      var _vex_animations_stagger_animation__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(
      /*! @vex/animations/stagger.animation */
      "UOrl");
      /* harmony import */


      var _scenarios_pages_scenarios_index_services_scenarios_index_paginator_service__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(
      /*! @scenarios/pages/scenarios-index/services/scenarios-index-paginator.service */
      "crox");

      var ScenariosDataTableComponent = /*#__PURE__*/function () {
        function ScenariosDataTableComponent(scenariosIndexPaginatorService) {
          _classCallCheck(this, ScenariosDataTableComponent);

          this.scenariosIndexPaginatorService = scenariosIndexPaginatorService;
          this.pageSize = 20;
          this.pageSizeOptions = [10, 20, 50];
          this.toggleStar = new _angular_core__WEBPACK_IMPORTED_MODULE_4__["EventEmitter"]();
          this.edit = new _angular_core__WEBPACK_IMPORTED_MODULE_4__["EventEmitter"]();
          this["delete"] = new _angular_core__WEBPACK_IMPORTED_MODULE_4__["EventEmitter"]();
          this.view = new _angular_core__WEBPACK_IMPORTED_MODULE_4__["EventEmitter"]();
          this.download = new _angular_core__WEBPACK_IMPORTED_MODULE_4__["EventEmitter"](); // Search

          this.searchCtrl = new _angular_forms__WEBPACK_IMPORTED_MODULE_5__["FormControl"]();
          this.searchStr$ = this.searchCtrl.valueChanges.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_10__["debounceTime"])(1000));
          this.dataSource = new _angular_material_table__WEBPACK_IMPORTED_MODULE_9__["MatTableDataSource"]();
          this.selection = new _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_3__["SelectionModel"](true, []);
          this.icMoreVert = _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_16___default.a;
          this.icStar = _iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_18___default.a;
          this.icStarBorder = _iconify_icons_ic_twotone_star_border__WEBPACK_IMPORTED_MODULE_19___default.a;
          this.icDeleteForever = _iconify_icons_ic_twotone_delete_forever__WEBPACK_IMPORTED_MODULE_13___default.a;
          this.icEdit = _iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_14___default.a;
          this.icCloudDownload = _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_11___default.a;
          this.icSearch = _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_17___default.a;
          this.icDelete = _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_12___default.a;
          this.icFilterList = _iconify_icons_ic_twotone_filter_list__WEBPACK_IMPORTED_MODULE_15___default.a;
        }

        _createClass(ScenariosDataTableComponent, [{
          key: "ngOnInit",
          value: function ngOnInit() {
            var _this10 = this;

            this.searchCtrl.patchValue(this.searchStr);
            this.searchStr$.subscribe(function ($event) {
              _this10.dataSource.filter = ($event || '').trim().toLowerCase();
            });
          }
        }, {
          key: "ngAfterViewInit",
          // ngOnChanges(changes: SimpleChanges): void {
          //   if (changes.columns) {
          //     return this.columns.filter(column => column.visible).map(column => column.property);
          //   }
          // }
          value: function ngAfterViewInit() {
            this.dataSource.paginator = this.paginator;
            this.dataSource.sort = this.sort;
          } // Emit Event

        }, {
          key: "emitToggleStar",
          value: function emitToggleStar(event, id) {
            event.stopPropagation();
            this.toggleStar.emit(id);
          }
        }, {
          key: "removeSelected",
          value: function removeSelected(scenarios) {
            var _this11 = this;

            scenarios.forEach(function (s) {
              return _this11["delete"].emit(s.id);
            });
            this.selection.clear();
          } // View Access

        }, {
          key: "toggleColumnVisibility",
          value: function toggleColumnVisibility(event, index, column) {
            event.stopPropagation();
            event.stopImmediatePropagation();
            this.columns[index].visible = !this.columns[index].visible;
          }
        }, {
          key: "onPaginateChange",
          value: function onPaginateChange($event) {
            /*
              previousPageIndex: 0
              pageIndex: 0
              pageSize: 50
              length: 3
            */
            this.scenariosIndexPaginatorService.changePageSize($event.pageSize);
          }
          /** Selects all rows if they are not all selected; otherwise clear selection. */

        }, {
          key: "masterToggle",
          value: function masterToggle($event) {
            var _this12 = this;

            $event.preventDefault();

            if (this.isAllSelected()) {
              this.unselectAll();
            } else {
              if (this.isPartiallySelected()) {
                // If current page has something selected, then clear current page
                // Else select everything in current page
                var hasSelected = false;
                this.dataSource.data.some(function (row) {
                  if (_this12.isSelected(row)) {
                    hasSelected = true;
                    return true;
                  }
                });

                if (hasSelected) {
                  this.unselectAll();
                } else {
                  this.selectAll();
                }
              } else {
                this.selectAll();
              }
            }
          } // Helpers

          /** Whether the number of selected elements matches the total number of rows. */

        }, {
          key: "isAllSelected",
          value: function isAllSelected() {
            if (!this.selection.hasValue()) {
              return false;
            }

            var numSelected = this.selection.selected.length;
            var numRows = this.dataSource.data.length;
            return numSelected === numRows;
          }
        }, {
          key: "isPartiallySelected",
          value: function isPartiallySelected() {
            return this.selection.hasValue() && !this.isAllSelected();
          }
        }, {
          key: "isSelected",
          value: function isSelected(row) {
            return this.selection.isSelected(row);
          }
        }, {
          key: "selectAll",
          value: function selectAll() {
            var _this13 = this;

            this.dataSource.data.forEach(function (row) {
              return _this13.selection.select(row);
            });
          }
        }, {
          key: "unselectAll",
          value: function unselectAll() {
            this.selection.clear();
          }
        }, {
          key: "data",
          set: function set(value) {
            this.dataSource.data = value;
          }
        }, {
          key: "visibleColumns",
          get: function get() {
            return this.columns.filter(function (column) {
              return column.visible;
            }).map(function (column) {
              return column.property;
            });
          }
        }]);

        return ScenariosDataTableComponent;
      }();

      ScenariosDataTableComponent.ctorParameters = function () {
        return [{
          type: _scenarios_pages_scenarios_index_services_scenarios_index_paginator_service__WEBPACK_IMPORTED_MODULE_23__["ScenariosIndexPaginatorService"]
        }];
      };

      ScenariosDataTableComponent.propDecorators = {
        data: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Input"]
        }],
        columns: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Input"]
        }],
        pageSize: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Input"]
        }],
        pageSizeOptions: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Input"]
        }],
        searchStr: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Input"]
        }],
        toggleStar: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Output"]
        }],
        edit: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Output"]
        }],
        "delete": [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Output"]
        }],
        view: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Output"]
        }],
        download: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Output"]
        }],
        paginator: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["ViewChild"],
          args: [_angular_material_paginator__WEBPACK_IMPORTED_MODULE_7__["MatPaginator"], {
            "static": true
          }]
        }],
        sort: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["ViewChild"],
          args: [_angular_material_sort__WEBPACK_IMPORTED_MODULE_8__["MatSort"], {
            "static": true
          }]
        }]
      };
      ScenariosDataTableComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_4__["Component"])({
        selector: 'scenarios-data-table',
        template: _raw_loader_scenarios_data_table_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        providers: [{
          provide: _angular_material_form_field__WEBPACK_IMPORTED_MODULE_6__["MAT_FORM_FIELD_DEFAULT_OPTIONS"],
          useValue: {
            appearance: 'standard'
          }
        }],
        animations: [_vex_animations_stagger_animation__WEBPACK_IMPORTED_MODULE_22__["stagger20ms"], _vex_animations_fade_in_up_animation__WEBPACK_IMPORTED_MODULE_20__["fadeInUp400ms"], _vex_animations_scale_fade_in_animation__WEBPACK_IMPORTED_MODULE_21__["scaleFadeIn400ms"]],
        styles: [_scenarios_data_table_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
      })], ScenariosDataTableComponent);
      /***/
    },

    /***/
    "coQM":
    /*!*******************************************************************************************!*\
      !*** ./src/app/modules/scenarios/pages/scenarios-index/services/scenario-data.service.ts ***!
      \*******************************************************************************************/

    /*! exports provided: ScenarioDataService */

    /***/
    function coQM(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ScenarioDataService", function () {
        return ScenarioDataService;
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


      var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! rxjs */
      "qCKp");

      var ScenarioDataService = /*#__PURE__*/function () {
        function ScenarioDataService() {
          _classCallCheck(this, ScenarioDataService);

          this.subject = new rxjs__WEBPACK_IMPORTED_MODULE_2__["BehaviorSubject"](null);
          this.scenario$ = this.subject.asObservable();
        }

        _createClass(ScenarioDataService, [{
          key: "set",
          value: function set(scenario) {
            this.scenario = scenario;
            this.subject.next(scenario);
          }
        }]);

        return ScenarioDataService;
      }();

      ScenarioDataService.ctorParameters = function () {
        return [];
      };

      ScenarioDataService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], ScenarioDataService);
      /***/
    },

    /***/
    "crox":
    /*!*******************************************************************************************************!*\
      !*** ./src/app/modules/scenarios/pages/scenarios-index/services/scenarios-index-paginator.service.ts ***!
      \*******************************************************************************************************/

    /*! exports provided: ScenariosIndexPaginatorService */

    /***/
    function crox(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ScenariosIndexPaginatorService", function () {
        return ScenariosIndexPaginatorService;
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


      var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! rxjs */
      "qCKp");

      var ScenariosIndexPaginatorService = /*#__PURE__*/function () {
        function ScenariosIndexPaginatorService() {
          _classCallCheck(this, ScenariosIndexPaginatorService);

          this.pageSizeSource = new rxjs__WEBPACK_IMPORTED_MODULE_2__["BehaviorSubject"](20);
          this.pageSize = this.pageSizeSource.asObservable();
        }

        _createClass(ScenariosIndexPaginatorService, [{
          key: "changePageSize",
          value: function changePageSize(size) {
            this.pageSizeSource.next(size);
          }
        }]);

        return ScenariosIndexPaginatorService;
      }();

      ScenariosIndexPaginatorService.ctorParameters = function () {
        return [];
      };

      ScenariosIndexPaginatorService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], ScenariosIndexPaginatorService);
      /***/
    },

    /***/
    "cuMl":
    /*!**************************************************************************************!*\
      !*** ./src/app/modules/scenarios/components/scenarios-edit/scenarios-edit.module.ts ***!
      \**************************************************************************************/

    /*! exports provided: ScenariosEditModule */

    /***/
    function cuMl(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ScenariosEditModule", function () {
        return ScenariosEditModule;
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


      var _angular_material_core__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/material/core */
      "UhP/");
      /* harmony import */


      var _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @angular/material/datepicker */
      "TN/R");
      /* harmony import */


      var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @angular/material/dialog */
      "iELJ");
      /* harmony import */


      var _angular_material_divider__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @angular/material/divider */
      "BSbQ");
      /* harmony import */


      var _angular_material_icon__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @angular/material/icon */
      "Tj54");
      /* harmony import */


      var _angular_material_input__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @angular/material/input */
      "e6WT");
      /* harmony import */


      var _angular_material_menu__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @angular/material/menu */
      "rJgo");
      /* harmony import */


      var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @visurel/iconify-angular */
      "l+Q0");
      /* harmony import */


      var _scenarios_edit_component__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! ./scenarios-edit.component */
      "b06q");

      var ScenariosEditModule = function ScenariosEditModule() {
        _classCallCheck(this, ScenariosEditModule);
      };

      ScenariosEditModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_scenarios_edit_component__WEBPACK_IMPORTED_MODULE_14__["ScenariosEditComponent"]],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _angular_material_dialog__WEBPACK_IMPORTED_MODULE_8__["MatDialogModule"], _angular_material_icon__WEBPACK_IMPORTED_MODULE_10__["MatIconModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"], _angular_material_input__WEBPACK_IMPORTED_MODULE_11__["MatInputModule"], _angular_material_divider__WEBPACK_IMPORTED_MODULE_9__["MatDividerModule"], _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_7__["MatDatepickerModule"], _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_13__["IconModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"], _angular_material_menu__WEBPACK_IMPORTED_MODULE_12__["MatMenuModule"], _angular_material_button__WEBPACK_IMPORTED_MODULE_5__["MatButtonModule"], _angular_material_core__WEBPACK_IMPORTED_MODULE_6__["MatNativeDateModule"]],
        entryComponents: [_scenarios_edit_component__WEBPACK_IMPORTED_MODULE_14__["ScenariosEditComponent"]]
      })], ScenariosEditModule);
      /***/
    },

    /***/
    "eUHj":
    /*!*******************************************************************************************!*\
      !*** ./src/app/modules/requests/components/scrumboard-dialog/scrumboard-dialog.module.ts ***!
      \*******************************************************************************************/

    /*! exports provided: ScrumboardDialogModule */

    /***/
    function eUHj(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ScrumboardDialogModule", function () {
        return ScrumboardDialogModule;
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


      var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/material/dialog */
      "iELJ");
      /* harmony import */


      var _angular_material_divider__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @angular/material/divider */
      "BSbQ");
      /* harmony import */


      var _angular_material_expansion__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @angular/material/expansion */
      "o4Yh");
      /* harmony import */


      var _angular_material_icon__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @angular/material/icon */
      "Tj54");
      /* harmony import */


      var _angular_material_input__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @angular/material/input */
      "e6WT");
      /* harmony import */


      var _angular_material_menu__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @angular/material/menu */
      "rJgo");
      /* harmony import */


      var _angular_material_select__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @angular/material/select */
      "ZTz/");
      /* harmony import */


      var _angular_material_tabs__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @angular/material/tabs */
      "M9ds");
      /* harmony import */


      var _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! @angular/material/tooltip */
      "ZFy/");
      /* harmony import */


      var _vex_pipes_relative_date_time_relative_date_time_module__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! @vex/pipes/relative-date-time/relative-date-time.module */
      "h4uD");
      /* harmony import */


      var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(
      /*! @visurel/iconify-angular */
      "l+Q0");
      /* harmony import */


      var _scrumboard_dialog_component__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(
      /*! ./scrumboard-dialog.component */
      "QgCS");

      var ScrumboardDialogModule = function ScrumboardDialogModule() {
        _classCallCheck(this, ScrumboardDialogModule);
      };

      ScrumboardDialogModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_scrumboard_dialog_component__WEBPACK_IMPORTED_MODULE_17__["ScrumboardDialogComponent"]],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"], _angular_material_dialog__WEBPACK_IMPORTED_MODULE_6__["MatDialogModule"], _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_14__["MatTooltipModule"], _angular_material_select__WEBPACK_IMPORTED_MODULE_12__["MatSelectModule"], _angular_material_button__WEBPACK_IMPORTED_MODULE_5__["MatButtonModule"], _angular_material_icon__WEBPACK_IMPORTED_MODULE_9__["MatIconModule"], _angular_material_input__WEBPACK_IMPORTED_MODULE_10__["MatInputModule"], _angular_material_menu__WEBPACK_IMPORTED_MODULE_11__["MatMenuModule"], _angular_material_divider__WEBPACK_IMPORTED_MODULE_7__["MatDividerModule"], _angular_material_expansion__WEBPACK_IMPORTED_MODULE_8__["MatExpansionModule"], _angular_material_tabs__WEBPACK_IMPORTED_MODULE_13__["MatTabsModule"], _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_16__["IconModule"], _vex_pipes_relative_date_time_relative_date_time_module__WEBPACK_IMPORTED_MODULE_15__["RelativeDateTimeModule"]],
        exports: [_scrumboard_dialog_component__WEBPACK_IMPORTED_MODULE_17__["ScrumboardDialogComponent"]],
        entryComponents: [_scrumboard_dialog_component__WEBPACK_IMPORTED_MODULE_17__["ScrumboardDialogComponent"]]
      })], ScrumboardDialogModule);
      /***/
    },

    /***/
    "eha6":
    /*!***************************************************************************************!*\
      !*** ./src/app/modules/scenarios/pages/scenarios-builder/scenarios-builder.module.ts ***!
      \***************************************************************************************/

    /*! exports provided: ScenariosBuilderModule */

    /***/
    function eha6(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ScenariosBuilderModule", function () {
        return ScenariosBuilderModule;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _angular_cdk_drag_drop__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! @angular/cdk/drag-drop */
      "ltgo");
      /* harmony import */


      var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @angular/common */
      "SVse");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/flex-layout */
      "u9T3");
      /* harmony import */


      var _angular_forms__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/forms */
      "s7LF");
      /* harmony import */


      var _angular_material_button__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/material/button */
      "Dxy4");
      /* harmony import */


      var _angular_material_icon__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @angular/material/icon */
      "Tj54");
      /* harmony import */


      var _angular_material_input__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @angular/material/input */
      "e6WT");
      /* harmony import */


      var _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @angular/material/tooltip */
      "ZFy/");
      /* harmony import */


      var ngx_infinite_scroll__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! ngx-infinite-scroll */
      "MNke");
      /* harmony import */


      var _vex_components_breadcrumbs_breadcrumbs_module__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @vex/components/breadcrumbs/breadcrumbs.module */
      "J0XA");
      /* harmony import */


      var _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @vex/components/page-layout/page-layout.module */
      "7lCJ");
      /* harmony import */


      var _vex_components_popover_popover_module__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @vex/components/popover/popover.module */
      "gX/z");
      /* harmony import */


      var _vex_components_scrollbar_scrollbar_module__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! @vex/components/scrollbar/scrollbar.module */
      "XVi8");
      /* harmony import */


      var _vex_directives_container_container_module__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! @vex/directives/container/container.module */
      "68Yx");
      /* harmony import */


      var _vex_pipes_date_tokens_date_tokens_module__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(
      /*! @vex/pipes/date-tokens/date-tokens.module */
      "0wNP");
      /* harmony import */


      var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(
      /*! @visurel/iconify-angular */
      "l+Q0");
      /* harmony import */


      var _requests_components_requests_search_requests_search_module__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(
      /*! @requests/components/requests-search/requests-search.module */
      "KAKk");
      /* harmony import */


      var _requests_components_scrumboard_dialog_scrumboard_dialog_module__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(
      /*! @requests/components/scrumboard-dialog/scrumboard-dialog.module */
      "eUHj");
      /* harmony import */


      var _shared_components_label_label_module__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(
      /*! @shared/components/label/label.module */
      "W6U6");
      /* harmony import */


      var _components_scrumboard_card_scrumboard_card_component__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(
      /*! ./components/scrumboard-card/scrumboard-card.component */
      "0w1K");
      /* harmony import */


      var _scenarios_builder_component__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(
      /*! ./scenarios-builder.component */
      "4BTo"); // import { ScenariosBuilderRoutingModule } from './scenarios-builder-routing.module';


      var ScenariosBuilderModule = function ScenariosBuilderModule() {
        _classCallCheck(this, ScenariosBuilderModule);
      };

      ScenariosBuilderModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["NgModule"])({
        declarations: [_scenarios_builder_component__WEBPACK_IMPORTED_MODULE_22__["ScenariosBuilderComponent"], _components_scrumboard_card_scrumboard_card_component__WEBPACK_IMPORTED_MODULE_21__["ScrumboardCardComponent"]],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_4__["FlexLayoutModule"], _angular_cdk_drag_drop__WEBPACK_IMPORTED_MODULE_1__["DragDropModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_5__["ReactiveFormsModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_5__["FormsModule"], _angular_material_button__WEBPACK_IMPORTED_MODULE_6__["MatButtonModule"], _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_9__["MatTooltipModule"], _angular_material_input__WEBPACK_IMPORTED_MODULE_8__["MatInputModule"], _angular_material_icon__WEBPACK_IMPORTED_MODULE_7__["MatIconModule"], ngx_infinite_scroll__WEBPACK_IMPORTED_MODULE_10__["InfiniteScrollModule"], _vex_components_breadcrumbs_breadcrumbs_module__WEBPACK_IMPORTED_MODULE_11__["BreadcrumbsModule"], _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_12__["PageLayoutModule"], _vex_components_popover_popover_module__WEBPACK_IMPORTED_MODULE_13__["PopoverModule"], _vex_components_scrollbar_scrollbar_module__WEBPACK_IMPORTED_MODULE_14__["ScrollbarModule"], _vex_directives_container_container_module__WEBPACK_IMPORTED_MODULE_15__["ContainerModule"], _vex_pipes_date_tokens_date_tokens_module__WEBPACK_IMPORTED_MODULE_16__["DateTokensModule"], _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_17__["IconModule"], //  ScenariosBuilderRoutingModule,
        _shared_components_label_label_module__WEBPACK_IMPORTED_MODULE_20__["LabelModule"], _requests_components_scrumboard_dialog_scrumboard_dialog_module__WEBPACK_IMPORTED_MODULE_19__["ScrumboardDialogModule"], _requests_components_requests_search_requests_search_module__WEBPACK_IMPORTED_MODULE_18__["RequestsSearchModule"]]
      })], ScenariosBuilderModule);
      /***/
    },

    /***/
    "hD1B":
    /*!****************************************************************************************!*\
      !*** ./src/app/modules/scenarios/pages/scenarios-index/scenarios-index.component.scss ***!
      \****************************************************************************************/

    /*! exports provided: default */

    /***/
    function hD1B(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = ".vex-page-layout-header {\n  height: 50px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uLy4uL3NjZW5hcmlvcy1pbmRleC5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLFlBQUE7QUFDRiIsImZpbGUiOiJzY2VuYXJpb3MtaW5kZXguY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyIudmV4LXBhZ2UtbGF5b3V0LWhlYWRlciB7XG4gIGhlaWdodDogNTBweDtcbn0iXX0= */";
      /***/
    },

    /***/
    "hb0D":
    /*!*********************************************************************************************************************************!*\
      !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/scenarios/components/scenarios-edit/scenarios-edit.component.html ***!
      \*********************************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function hb0D(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "<form (ngSubmit)=\"save()\" [formGroup]=\"form\">\r\n  <div fxLayout=\"row\" fxLayoutAlign=\"start center\" mat-dialog-title>\r\n    <!-- <img *ngIf=\"scenario?.imageSrc\" [src]=\"scenario?.imageSrc\" class=\"avatar ltr:mr-5 rtl:ml-5\"> -->\r\n    <h2 class=\"headline m-0\" fxFlex=\"auto\">{{ form.get('name').value }}</h2>\r\n\r\n    <button [matMenuTriggerFor]=\"settingsMenu\" class=\"text-secondary\" mat-icon-button type=\"button\" matTooltip=\"Priority\">\r\n      <mat-icon [icIcon]=\"icLabel\" [ngClass]=\"selectedPriority.classes\"></mat-icon>\r\n    </button>\r\n\r\n    <button class=\"text-secondary\" mat-dialog-close mat-icon-button type=\"button\">\r\n      <mat-icon [icIcon]=\"icClose\"></mat-icon>\r\n    </button>\r\n  </div>\r\n\r\n  <mat-divider class=\"-mx-6 text-border\"></mat-divider>\r\n\r\n  <mat-dialog-content fxLayout=\"column\">\r\n    <mat-form-field class=\"mt-6\">\r\n      <mat-label>Name</mat-label>\r\n      <input cdkFocusInitial formControlName=\"name\" matInput>\r\n\r\n      <mat-icon [icIcon]=\"icPerson\" class=\"ltr:mr-3 rtl:ml-3\" matPrefix></mat-icon>\r\n    </mat-form-field>\r\n\r\n    <mat-form-field>\r\n      <mat-label>Description</mat-label>\r\n      <textarea formControlName=\"description\" matInput></textarea>\r\n    </mat-form-field>\r\n  </mat-dialog-content>\r\n\r\n  <mat-dialog-actions align=\"end\">\r\n    <button mat-button mat-dialog-close type=\"button\">CANCEL</button>\r\n    <button color=\"primary\" mat-button type=\"submit\">SAVE CHANGES</button>\r\n  </mat-dialog-actions>\r\n</form>\r\n\r\n<mat-menu #settingsMenu=\"matMenu\" xPosition=\"before\" yPosition=\"below\">\r\n  <button mat-menu-item *ngFor=\"let priority of scenarioPriorities\" (click)=\"handlePrioritySelect(priority)\">\r\n    <span>{{ priority.name }}</span>\r\n  </button>\r\n</mat-menu>\r\n";
      /***/
    },

    /***/
    "hh0J":
    /*!****************************************************************************************************!*\
      !*** ./src/app/modules/scenarios/pages/scenarios-builder/services/request-card-adapter.service.ts ***!
      \****************************************************************************************************/

    /*! exports provided: RequestCardAdapterService */

    /***/
    function hh0J(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "RequestCardAdapterService", function () {
        return RequestCardAdapterService;
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


      var luxon__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! luxon */
      "ExVU");
      /* harmony import */


      var luxon__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(luxon__WEBPACK_IMPORTED_MODULE_2__);

      var RequestCardAdapterService = /*#__PURE__*/function () {
        function RequestCardAdapterService() {
          _classCallCheck(this, RequestCardAdapterService);
        }

        _createClass(RequestCardAdapterService, [{
          key: "createCard",
          value: function createCard(request) {
            return {
              id: request.id,
              title: request.url,
              method: request.method,
              status: request.status,
              position: request.position,
              latency: request.latency,
              dueDate: {
                date: luxon__WEBPACK_IMPORTED_MODULE_2__["DateTime"].fromJSDate(request.createdAt),
                done: false
              },
              attachments: [],
              comments: [],
              users: [],
              labels: []
            };
          }
        }]);

        return RequestCardAdapterService;
      }();

      RequestCardAdapterService.ctorParameters = function () {
        return [];
      };

      RequestCardAdapterService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], RequestCardAdapterService);
      /***/
    },

    /***/
    "hnRQ":
    /*!******************************************************************************************************************!*\
      !*** ./src/app/modules/scenarios/pages/scenario-details/components/requests-create/requests-create.component.ts ***!
      \******************************************************************************************************************/

    /*! exports provided: RequestsCreateComponent */

    /***/
    function hnRQ(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "RequestsCreateComponent", function () {
        return RequestsCreateComponent;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _raw_loader_requests_create_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! raw-loader!./requests-create.component.html */
      "FAgS");
      /* harmony import */


      var _requests_create_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! ./requests-create.component.scss */
      "QIdO");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/forms */
      "s7LF");
      /* harmony import */


      var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/material/dialog */
      "iELJ");
      /* harmony import */


      var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-close */
      "5mnX");
      /* harmony import */


      var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_6__);
      /* harmony import */


      var _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-cloud-download */
      "MzEE");
      /* harmony import */


      var _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_7__);
      /* harmony import */


      var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-delete */
      "e3EN");
      /* harmony import */


      var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_8__);
      /* harmony import */


      var _iconify_icons_ic_twotone_edit_location__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-edit-location */
      "EPGw");
      /* harmony import */


      var _iconify_icons_ic_twotone_edit_location__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_edit_location__WEBPACK_IMPORTED_MODULE_9__);
      /* harmony import */


      var _iconify_icons_ic_twotone_location_city__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-location-city */
      "0I5b");
      /* harmony import */


      var _iconify_icons_ic_twotone_location_city__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_location_city__WEBPACK_IMPORTED_MODULE_10__);
      /* harmony import */


      var _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-more-vert */
      "+Chm");
      /* harmony import */


      var _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_11__);
      /* harmony import */


      var _iconify_icons_ic_twotone_my_location__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-my-location */
      "kSvQ");
      /* harmony import */


      var _iconify_icons_ic_twotone_my_location__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_my_location__WEBPACK_IMPORTED_MODULE_12__);
      /* harmony import */


      var _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-person */
      "KaaH");
      /* harmony import */


      var _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_13___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_13__);
      /* harmony import */


      var _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-phone */
      "YA1h");
      /* harmony import */


      var _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_14___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_14__);
      /* harmony import */


      var _iconify_icons_ic_twotone_print__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-print */
      "yHIK");
      /* harmony import */


      var _iconify_icons_ic_twotone_print__WEBPACK_IMPORTED_MODULE_15___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_print__WEBPACK_IMPORTED_MODULE_15__);

      var RequestsCreateComponent = /*#__PURE__*/function () {
        function RequestsCreateComponent(defaults, dialogRef, fb) {
          _classCallCheck(this, RequestsCreateComponent);

          this.defaults = defaults;
          this.dialogRef = dialogRef;
          this.fb = fb;
          this.onCreate = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
          this.icMoreVert = _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_11___default.a;
          this.icClose = _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_6___default.a;
          this.icPrint = _iconify_icons_ic_twotone_print__WEBPACK_IMPORTED_MODULE_15___default.a;
          this.icDownload = _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_7___default.a;
          this.icDelete = _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_8___default.a;
          this.icPerson = _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_13___default.a;
          this.icMyLocation = _iconify_icons_ic_twotone_my_location__WEBPACK_IMPORTED_MODULE_12___default.a;
          this.icLocationCity = _iconify_icons_ic_twotone_location_city__WEBPACK_IMPORTED_MODULE_10___default.a;
          this.icEditLocation = _iconify_icons_ic_twotone_edit_location__WEBPACK_IMPORTED_MODULE_9___default.a;
          this.icPhone = _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_14___default.a;
          this.files = [];
        }

        _createClass(RequestsCreateComponent, [{
          key: "ngOnInit",
          value: function ngOnInit() {
            this.form = this.fb.group({});
          }
        }, {
          key: "create",
          value: function create() {
            if (!this.files.length) {
              return;
            }

            var form = this.form.value;
            var formData = new FormData();
            formData.append('file', this.files[0]);
            formData.append('project_id', '1');
            this.onCreate.emit(formData);
            this.dialogRef.close();
          }
        }, {
          key: "onSelect",
          value: function onSelect(event) {
            var _this$files;

            console.log(event);

            (_this$files = this.files).push.apply(_this$files, _toConsumableArray(event.addedFiles));
          }
        }, {
          key: "onRemove",
          value: function onRemove(event) {
            console.log(event);
            this.files.splice(this.files.indexOf(event), 1);
          }
        }]);

        return RequestsCreateComponent;
      }();

      RequestsCreateComponent.ctorParameters = function () {
        return [{
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Inject"],
            args: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MAT_DIALOG_DATA"]]
          }]
        }, {
          type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MatDialogRef"]
        }, {
          type: _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormBuilder"]
        }];
      };

      RequestsCreateComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'requests-create',
        template: _raw_loader_requests_create_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_requests_create_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
      })], RequestsCreateComponent);
      /***/
    },

    /***/
    "j/wk":
    /*!********************************************************************************************************************************!*\
      !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/scenarios/pages/scenario-details/scenario-details.component.html ***!
      \********************************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function jWk(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "<vex-page-layout>\r\n\r\n  <vex-page-layout-header class=\"vex-layout-theme pb-16\" fxLayout=\"column\" fxLayoutAlign=\"center start\">\r\n    <div [class.container]=\"layoutCtrl.value === 'boxed'\"\r\n         [class.px-gutter]=\"layoutCtrl.value === 'fullwidth'\"\r\n         class=\"w-full flex flex-col sm:flex-row justify-between\">\r\n      <div>\r\n        <h1 class=\"title mt-0 mb-1\">Scenario Details</h1>\r\n        <vex-breadcrumbs [crumbs]=\"crumbs\"></vex-breadcrumbs>\r\n      </div>\r\n    </div>\r\n  </vex-page-layout-header>\r\n\r\n  <vex-page-layout-content [class.container]=\"layoutCtrl.value === 'boxed'\"\r\n                           [class.px-gutter]=\"layoutCtrl.value === 'fullwidth'\"\r\n                           class=\"-mt-6\">\r\n    <div class=\"card overflow-auto -mt-14\">\r\n      <data-table\r\n        [buttonsTemplate]=\"buttonsTemplate\"\r\n        [columns]=\"tableColumns\"\r\n        [data]=\"requests\"\r\n        [editable]=\"true\"\r\n        [length]=\"totalRequests\"\r\n        [pageSize]=\"pageSize\"\r\n        [page]=\"page\"\r\n        [query]=\"indexParams.q\"\r\n        [resourceName]=\"'request'\"\r\n        [sortBy]=\"indexParams.sort_by\"\r\n        [sortOrder]=\"indexParams.sort_order\"\r\n        [templates]=\"{ components: componentsTemplate, latency: latencyTemplate, position: positionTemplate, status: statusTemplate }\"\r\n        (delete)=\"destroyRequest($event)\"\r\n        (globalEdit)=\"showBuilder()\"\r\n        (paginate)=\"handlePaginateChange($event)\"\r\n        (search)=\"searchRequests($event)\"\r\n        (sort)=\"sortRequests($event)\"\r\n        (view)=\"viewRequest($event)\"\r\n      >\r\n      </data-table>\r\n    </div>\r\n  </vex-page-layout-content>\r\n</vex-page-layout>\r\n\r\n<ng-template #componentsTemplate let-request=\"row\">\r\n  <div (click)=\"$event.stopPropagation()\" fxLayoutAlign=\"start center\" fxLayoutGap=\"4px\">\r\n    <div *ngFor=\"let label of request.components | requestComponentLabel\"\r\n          [style.background-color]=\"label.backgroundColor\"\r\n          [style.color]=\"label.color\"\r\n          class=\"rounded px-2 py-1 font-medium text-xs\"\r\n          fxFlex=\"none\">\r\n      {{ label.text }}\r\n    </div>\r\n  </div>\r\n</ng-template>\r\n\r\n<!-- <ng-template #searchTemplate>\r\n  <div class=\"bg-card rounded-full border px-4\"\r\n        fxFlex=\"400px\"\r\n        fxFlex.lt-md=\"auto\"\r\n        fxHide.xs\r\n        fxLayout=\"row\"\r\n        fxLayoutAlign=\"start center\">\r\n    <ic-icon [icIcon]=\"icons.icSearch\" size=\"20px\"></ic-icon>\r\n    <input [formControl]=\"searchCtrl\"\r\n            class=\"px-4 py-2 border-0 outline-none w-full bg-transparent\"\r\n            placeholder=\"Search...\"\r\n            type=\"search\">\r\n  </div>\r\n</ng-template> -->\r\n\r\n<ng-template #statusTemplate let-request=\"row\">\r\n  <status-label\r\n    [okThreshold]=\"299\"\r\n    [text]=\"request.status\"\r\n    [status]=\"request.status\"\r\n    [warningThreshold]=\"499\"\r\n  >\r\n  </status-label>\r\n</ng-template>\r\n\r\n<ng-template #latencyTemplate let-request=\"row\">\r\n  <status-label\r\n    [okThreshold]=\"350\"\r\n    [text]=\"request.latency + ' ms'\"\r\n    [status]=\"request.latency\"\r\n    [warningThreshold]=\"1000\"\r\n  >\r\n  </status-label>\r\n</ng-template>\r\n\r\n<ng-template #buttonsTemplate let-request=\"row\">\r\n  <button mat-menu-item (click)=\"editRequest(request.id)\">\r\n    <mat-icon [icIcon]=\"icons.icEdit\"></mat-icon>\r\n    <span>Edit</span>\r\n  </button>\r\n</ng-template>\r\n\r\n<ng-template #positionTemplate let-request=\"row\">\r\n  {{ request.position + 1 }}\r\n</ng-template>";
      /***/
    },

    /***/
    "lAmD":
    /*!*********************************************************************************************!*\
      !*** ./src/app/modules/scenarios/components/scenarios-create/scenarios-create.component.ts ***!
      \*********************************************************************************************/

    /*! exports provided: ScenariosCreateComponent */

    /***/
    function lAmD(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ScenariosCreateComponent", function () {
        return ScenariosCreateComponent;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _raw_loader_scenarios_create_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! raw-loader!./scenarios-create.component.html */
      "UAid");
      /* harmony import */


      var _scenarios_create_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! ./scenarios-create.component.scss */
      "9Gul");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/forms */
      "s7LF");
      /* harmony import */


      var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/material/dialog */
      "iELJ");
      /* harmony import */


      var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-close */
      "5mnX");
      /* harmony import */


      var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_6__);
      /* harmony import */


      var _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-cloud-download */
      "MzEE");
      /* harmony import */


      var _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_7__);
      /* harmony import */


      var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-delete */
      "e3EN");
      /* harmony import */


      var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_8__);
      /* harmony import */


      var _iconify_icons_ic_twotone_label__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-label */
      "ll2Q");
      /* harmony import */


      var _iconify_icons_ic_twotone_label__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_label__WEBPACK_IMPORTED_MODULE_9__);
      /* harmony import */


      var _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-more-vert */
      "+Chm");
      /* harmony import */


      var _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_10__);
      /* harmony import */


      var _iconify_icons_ic_twotone_print__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-print */
      "yHIK");
      /* harmony import */


      var _iconify_icons_ic_twotone_print__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_print__WEBPACK_IMPORTED_MODULE_11__);
      /* harmony import */


      var _iconify_icons_ic_twotone_title__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-title */
      "4EXa");
      /* harmony import */


      var _iconify_icons_ic_twotone_title__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_title__WEBPACK_IMPORTED_MODULE_12__);
      /* harmony import */


      var _core_utils_alias_discovery_service__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @core/utils/alias-discovery.service */
      "PbvV");
      /* harmony import */


      var _data_schema__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! @data/schema */
      "V99k");

      var ScenariosCreateComponent = /*#__PURE__*/function () {
        function ScenariosCreateComponent(projectId, dialogRef, fb, aliasDiscovery) {
          _classCallCheck(this, ScenariosCreateComponent);

          this.projectId = projectId;
          this.dialogRef = dialogRef;
          this.fb = fb;
          this.aliasDiscovery = aliasDiscovery; // ngx-dropzone

          this.files = [];
          this.form = this.fb.group({
            name: new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"]('', [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required]),
            description: ''
          }); // icons

          this.icMoreVert = _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_10___default.a;
          this.icClose = _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_6___default.a;
          this.icPrint = _iconify_icons_ic_twotone_print__WEBPACK_IMPORTED_MODULE_11___default.a;
          this.icDownload = _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_7___default.a;
          this.icDelete = _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_8___default.a;
          this.icTitle = _iconify_icons_ic_twotone_title__WEBPACK_IMPORTED_MODULE_12___default.a;
          this.icLabel = _iconify_icons_ic_twotone_label__WEBPACK_IMPORTED_MODULE_9___default.a;
          this.onCreate = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
          this.scenarioPriorities = _data_schema__WEBPACK_IMPORTED_MODULE_14__["ScenarioPriorityData"];
          this.selectedPriority = this.scenarioPriorities[3];
        }

        _createClass(ScenariosCreateComponent, [{
          key: "ngOnInit",
          value: function ngOnInit() {}
        }, {
          key: "create",
          value: function create() {
            var _this14 = this;

            var form = this.form.value;

            if (!this.files.length) {
              var formData = this.buildFormData(form);
              this.onCreate.emit(formData);
              this.dialogRef.close();
            } else {
              var fileReader = new FileReader();

              fileReader.onload = function (e) {
                // let urls: string[] = this.getHarFileUrls(fileReader.result)
                // this.aliasDiscovery.discoverAll(urls).subscribe(aliasMap => {
                var formData = _this14.buildFormData(form); // formData.append('alias_map', JSON.stringify(aliasMap))


                _this14.onCreate.emit(formData);

                _this14.dialogRef.close(); // })

              };

              fileReader.readAsText(this.files[0]);
            }
          }
        }, {
          key: "buildFormData",
          value: function buildFormData(form) {
            var formData = new FormData();
            formData.append('name', form.name);
            formData.append('description', form.description);
            formData.append('priority', this.selectedPriority.value.toString());

            if (this.files[0]) {
              formData.append('file', this.files[0]);
            }

            return formData;
          }
        }, {
          key: "getHarFileUrls",
          value: function getHarFileUrls(contents) {
            var data = JSON.parse(contents);

            if (!data.log) {
              return;
            }

            if (!data.log.entries) {
              return;
            }

            var urls = data.log.entries.map(function (entry) {
              return entry.request.url;
            });
            return urls;
          }
        }, {
          key: "onFileSelect",
          value: function onFileSelect(event) {
            var _this$files2;

            console.log(event);

            (_this$files2 = this.files).push.apply(_this$files2, _toConsumableArray(event.addedFiles));
          }
        }, {
          key: "onFileRemove",
          value: function onFileRemove(event) {
            console.log(event);
            this.files.splice(this.files.indexOf(event), 1);
          }
        }, {
          key: "handlePrioritySelect",
          value: function handlePrioritySelect(priority) {
            this.selectedPriority = priority;
          }
        }]);

        return ScenariosCreateComponent;
      }();

      ScenariosCreateComponent.ctorParameters = function () {
        return [{
          type: Number,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Inject"],
            args: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MAT_DIALOG_DATA"]]
          }]
        }, {
          type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MatDialogRef"]
        }, {
          type: _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormBuilder"]
        }, {
          type: _core_utils_alias_discovery_service__WEBPACK_IMPORTED_MODULE_13__["AliasDiscovery"]
        }];
      };

      ScenariosCreateComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'scenarios-create',
        template: _raw_loader_scenarios_create_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_scenarios_create_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
      })], ScenariosCreateComponent);
      /***/
    },

    /***/
    "llVH":
    /*!**************************************************************************************!*\
      !*** ./src/app/modules/scenarios/pages/scenarios-index/scenarios-index.component.ts ***!
      \**************************************************************************************/

    /*! exports provided: ScenariosIndexComponent */

    /***/
    function llVH(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ScenariosIndexComponent", function () {
        return ScenariosIndexComponent;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _scenarios_index_component_scss__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! ./scenarios-index.component.scss */
      "hD1B");
      /* harmony import */


      var _raw_loader_scenarios_index_component_html__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! raw-loader!./scenarios-index.component.html */
      "pIXh");
      /* harmony import */


      var _angular_cdk_clipboard__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/cdk/clipboard */
      "Tr4x");
      /* harmony import */


      var _angular_common__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/common */
      "SVse");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/material/dialog */
      "iELJ");
      /* harmony import */


      var _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @angular/material/snack-bar */
      "zHaW");
      /* harmony import */


      var _angular_router__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @angular/router */
      "iInd");
      /* harmony import */


      var _vex_animations__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @vex/animations */
      "ORuP");
      /* harmony import */


      var _core_http_scenario_resource_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @core/http/scenario-resource.service */
      "3Ncz");
      /* harmony import */


      var _core_utils__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @core/utils */
      "a+Vh");
      /* harmony import */


      var _data_schema__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @data/schema */
      "V99k");
      /* harmony import */


      var _scenarios_components_scenarios_create_scenarios_create_component__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @scenarios/components/scenarios-create/scenarios-create.component */
      "lAmD");
      /* harmony import */


      var _scenarios_components_scenarios_edit_scenarios_edit_component__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! @scenarios/components/scenarios-edit/scenarios-edit.component */
      "b06q");
      /* harmony import */


      var _services_scenario_data_service__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! ./services/scenario-data.service */
      "coQM");
      /* harmony import */


      var _services_scenarios_index_icons_service__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(
      /*! ./services/scenarios-index-icons.service */
      "WZBS");

      var ScenariosIndexComponent = /*#__PURE__*/function () {
        function ScenariosIndexComponent(icons, activatedRoute, clipboard, dialog, file, fileDownload, location, route, router, scenarioDataService, scenarioResource, snackbar, uri) {
          _classCallCheck(this, ScenariosIndexComponent);

          this.icons = icons;
          this.activatedRoute = activatedRoute;
          this.clipboard = clipboard;
          this.dialog = dialog;
          this.file = file;
          this.fileDownload = fileDownload;
          this.location = location;
          this.route = route;
          this.router = router;
          this.scenarioDataService = scenarioDataService;
          this.scenarioResource = scenarioResource;
          this.snackbar = snackbar;
          this.uri = uri; // Breadcrumb settings

          this.crumbs = [];
          this.indexParams = {}; // Table

          this.scenarios = []; // search
          // searchCtrl = new FormControl();
          // searchStr$ = this.searchCtrl.valueChanges.pipe(
          //   debounceTime(10)
          // );

          this.menuOpen = false;
        }

        _createClass(ScenariosIndexComponent, [{
          key: "ngOnInit",
          value: function ngOnInit() {
            var routeSnapshot = this.route.snapshot;
            this.project = this.route.snapshot.data.project;
            var scenarios = routeSnapshot.data.scenarios;
            this.scenarios = scenarios.list;
            this.totalScenarios = scenarios.total;
            this.indexParams = Object.assign({}, routeSnapshot.queryParams);
            this.indexParams.page = this.indexParams.page || 0;
            this.indexParams.size = this.indexParams.size || 20;
            this.page = this.indexParams.page;
            this.pageSize = this.indexParams.size;
            this.filter = this.indexParams.filter;
            this.crumbs.push({
              name: this.project.name
            });
            this.crumbs.push({
              name: 'Scenarios'
            });
            this.tableColumns = this.buildTableColumns();
          } // API Access

        }, {
          key: "getScenarios",
          value: function getScenarios() {
            var _this15 = this;

            var params = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : this.indexParams;
            var snapshot = this.route.snapshot;
            var project_id = snapshot.queryParams.project_id;
            params.project_id = project_id;
            this.scenarioResource.index(params).subscribe(function (res) {
              _this15.indexParams = params; // Save params for next use

              _this15.scenarios = res.list;
              _this15.totalScenarios = res.total;

              _this15.updateUrlQueryParams(params);
            }, function (error) {});
          }
        }, {
          key: "downloadScenario",
          value: function downloadScenario(scenarioId) {
            var _this16 = this;

            this.scenarioResource.download(scenarioId).subscribe(function (res) {
              _this16.fileDownload.create(res);
            });
          }
        }, {
          key: "createScenario",
          value: function createScenario(data) {
            var _this17 = this;

            var snapshot = this.route.snapshot;
            var project_id = snapshot.queryParams.project_id;
            data.append('project_id', project_id);
            this.scenarioResource.create(data).subscribe(function (res) {
              var clone = _this17.scenarios.slice();

              clone.unshift(res);
              _this17.scenarios = clone;
            }, function (error) {});
          }
        }, {
          key: "updateScenario",
          value: function updateScenario(id, data) {
            var _this18 = this;

            var priority = data.priority;
            var starred = data.starred;
            var description = data.description;
            var name = data.name;
            var body = {
              description: description,
              name: name,
              priority: priority,
              starred: starred
            };
            this.scenarioResource.update(id, body).subscribe(function (res) {
              var clone = _this18.scenarios.slice();

              for (var i = 0; i < clone.length; ++i) {
                if (clone[i].id !== id) {
                  continue;
                }

                clone[i] = new _data_schema__WEBPACK_IMPORTED_MODULE_12__["Scenario"](res);
              }

              _this18.scenarios = clone;
            }, function (error) {});
          }
        }, {
          key: "deleteScenario",
          value: function deleteScenario(scenarioId) {
            var _this19 = this;

            this.scenarioResource.destroy(scenarioId).subscribe(function (res) {
              _this19.scenarios = _this19.scenarios.filter(function (scenario) {
                return scenario.id !== scenarioId;
              });
            });
          }
        }, {
          key: "sortScenarios",
          value: function sortScenarios(event) {
            var column = event.active;
            var direction = event.direction; // desc or asc

            if (!direction) {
              delete this.indexParams.sort_by;
              delete this.indexParams.sort_order;
            } else {
              this.indexParams.sort_by = column;
              this.indexParams.sort_order = direction;
            }

            this.getScenarios();
          }
        }, {
          key: "searchScenarios",
          value: function searchScenarios(queryString) {
            var snapshot = this.route.snapshot;
            var project_id = snapshot.queryParams.project_id;
            this.indexParams.page = 0;
            this.page = 0;

            if (!queryString.length) {
              delete this.indexParams.q;
            } else {
              this.indexParams.q = queryString;
            }

            this.getScenarios();
          }
        }, {
          key: "filterScenarios",
          value: function filterScenarios($event) {
            if (!$event.filter) {
              delete this.indexParams.filter;
            } else {
              this.indexParams.filter = $event.filter;
            }

            this.getScenarios();
          } // View Access

        }, {
          key: "viewScenario",
          value: function viewScenario(scenarioId) {
            var scenario = this.scenarios.find(function (candidate) {
              return candidate.id === scenarioId;
            });
            this.scenarioDataService.set(scenario);
            var uri = new this.uri["class"](this.location.path());
            var path = this.file.join(uri.pathname, scenarioId);
            uri.pathname = path;
            this.router.navigateByUrl(uri.pathname + uri.query);
          }
        }, {
          key: "toggleScenarioStar",
          value: function toggleScenarioStar(id) {
            var scenario = this.scenarios.find(function (s) {
              return s.id === id;
            });

            if (scenario) {
              scenario.starred = !scenario.starred;
              this.updateScenario(id, scenario);
            }
          }
        }, {
          key: "openCreateDialog",
          value: function openCreateDialog() {
            var _this20 = this;

            var dialogRef = this.dialog.open(_scenarios_components_scenarios_create_scenarios_create_component__WEBPACK_IMPORTED_MODULE_13__["ScenariosCreateComponent"], {
              width: '600px'
            });
            var onCreateSub = dialogRef.componentInstance.onCreate.subscribe(function ($event) {
              _this20.createScenario($event);
            });
            dialogRef.afterClosed().subscribe(function () {
              onCreateSub.unsubscribe();
            });
          }
        }, {
          key: "openEditDialog",
          value: function openEditDialog(scenario) {
            var _this21 = this;

            var dialogRef = this.dialog.open(_scenarios_components_scenarios_edit_scenarios_edit_component__WEBPACK_IMPORTED_MODULE_14__["ScenariosEditComponent"], {
              data: scenario,
              width: '600px'
            });
            var onEditSub = dialogRef.componentInstance.onEdit.subscribe(function ($event) {
              _this21.updateScenario(scenario.id, $event);
            });
            dialogRef.afterClosed().subscribe(function () {
              onEditSub.unsubscribe();
            });
          }
        }, {
          key: "closeMenu",
          value: function closeMenu() {
            this.menuOpen = false;
          } // For when the screen size is small

        }, {
          key: "openMenu",
          value: function openMenu() {
            this.menuOpen = true;
          }
          /*
           *
           * $event = {
           *   previousPageIndex: 0
           *   pageIndex: 0
           *   pageSize: 50
           *   length: 3
           * }
           *
           */

        }, {
          key: "handlePaginateChange",
          value: function handlePaginateChange($event) {
            var curIndex = this.page;
            var curSize = this.pageSize;
            var newIndex = $event.pageIndex;
            var newSize = $event.pageSize;

            if (curSize !== newSize) {
              this.pageSize = newSize;
            }

            if (curIndex != newIndex) {
              this.page = newIndex;
            }

            if (curIndex != newIndex || curSize !== newSize) {
              this.indexParams.page = newIndex;
              this.indexParams.size = newSize;
              this.getScenarios();
            }
          }
        }, {
          key: "copyMockUrlToClipBoard",
          value: function copyMockUrlToClipBoard(scenario) {
            this.clipboard.copy(scenario.mock_url);
            this.snackbar.open('URL copied to clipboard!', 'close', {
              duration: 2000
            });
          } // Helpers

        }, {
          key: "updateUrlQueryParams",
          value: function updateUrlQueryParams(newQueryParams) {
            var _this22 = this;

            var queryParams = Object.assign({}, this.indexParams);
            Object.entries(newQueryParams).forEach(function (_ref9) {
              var _ref10 = _slicedToArray(_ref9, 2),
                  key = _ref10[0],
                  value = _ref10[1];

              queryParams[key] = value;
              _this22.indexParams[key] = value;
            });
            var url = this.router.createUrlTree([], {
              relativeTo: this.activatedRoute,
              queryParams: queryParams
            }).toString();
            this.location.go(url);
          }
        }, {
          key: "buildTableColumns",
          value: function buildTableColumns() {
            var _this23 = this;

            return [// {
            //   label: '',
            //   property: 'selected',
            //   type: 'checkbox',
            //   cssClasses: ['w-6'],
            //   visible: true,
            //   canHide: false,
            // },
            // {
            //   label: '',
            //   property: 'imageSrc',
            //   type: 'image',
            //   cssClasses: ['min-w-9']
            // },
            {
              label: 'Name',
              property: 'name',
              type: 'text',
              cssClasses: ['font-medium'],
              visible: true,
              canHide: true
            }, {
              label: 'Requests',
              property: 'request_count',
              type: 'text',
              cssClasses: ['text-secondary'],
              visible: true,
              canHide: true
            }, {
              label: 'Description',
              property: 'description',
              type: 'text',
              cssClasses: ['text-secondary'],
              visible: true,
              canHide: true
            }, {
              label: 'Created At',
              property: 'created_at',
              type: 'date',
              cssClasses: ['text-secondary'],
              visible: false,
              canHide: true
            }, {
              label: 'Mock URL',
              property: 'mock_url',
              type: 'button',
              cssClasses: ['text-secondary'],
              visible: true,
              canHide: true,
              onclick: this.copyMockUrlToClipBoard.bind(this),
              icon: this.icons.icFileCopy
            }, {
              label: '',
              property: 'starred',
              type: 'toggleButton',
              cssClasses: ['text-secondary', 'w-10'],
              visible: true,
              canHide: false,
              icon: function icon(scenario) {
                return scenario.starred ? _this23.icons.icStar : _this23.icons.icStarBorder;
              }
            }, {
              label: '',
              property: 'menu',
              type: 'menuButton',
              cssClasses: ['text-secondary', 'w-10'],
              visible: true,
              canHide: false
            }];
          }
        }]);

        return ScenariosIndexComponent;
      }();

      ScenariosIndexComponent.ctorParameters = function () {
        return [{
          type: _services_scenarios_index_icons_service__WEBPACK_IMPORTED_MODULE_16__["ScenariosIndexIcons"]
        }, {
          type: _angular_router__WEBPACK_IMPORTED_MODULE_8__["ActivatedRoute"]
        }, {
          type: _angular_cdk_clipboard__WEBPACK_IMPORTED_MODULE_3__["Clipboard"]
        }, {
          type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_6__["MatDialog"]
        }, {
          type: _core_utils__WEBPACK_IMPORTED_MODULE_11__["FileService"]
        }, {
          type: _core_utils__WEBPACK_IMPORTED_MODULE_11__["FileDownload"]
        }, {
          type: _angular_common__WEBPACK_IMPORTED_MODULE_4__["Location"]
        }, {
          type: _angular_router__WEBPACK_IMPORTED_MODULE_8__["ActivatedRoute"]
        }, {
          type: _angular_router__WEBPACK_IMPORTED_MODULE_8__["Router"]
        }, {
          type: _services_scenario_data_service__WEBPACK_IMPORTED_MODULE_15__["ScenarioDataService"]
        }, {
          type: _core_http_scenario_resource_service__WEBPACK_IMPORTED_MODULE_10__["ScenarioResource"]
        }, {
          type: _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_7__["MatSnackBar"]
        }, {
          type: _core_utils__WEBPACK_IMPORTED_MODULE_11__["UriService"]
        }];
      };

      ScenariosIndexComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_5__["Component"])({
        selector: 'scenarios-index',
        template: _raw_loader_scenarios_index_component_html__WEBPACK_IMPORTED_MODULE_2__["default"],
        animations: [_vex_animations__WEBPACK_IMPORTED_MODULE_9__["stagger40ms"], _vex_animations__WEBPACK_IMPORTED_MODULE_9__["scaleIn400ms"], _vex_animations__WEBPACK_IMPORTED_MODULE_9__["fadeInRight400ms"]],
        styles: [_scenarios_index_component_scss__WEBPACK_IMPORTED_MODULE_1__["default"]]
      })], ScenariosIndexComponent);
      /***/
    },

    /***/
    "ltgo":
    /*!*********************************************************!*\
      !*** ./node_modules/@angular/cdk/fesm2015/drag-drop.js ***!
      \*********************************************************/

    /*! exports provided: CDK_DRAG_CONFIG, CDK_DRAG_HANDLE, CDK_DRAG_PARENT, CDK_DRAG_PLACEHOLDER, CDK_DRAG_PREVIEW, CDK_DROP_LIST, CDK_DROP_LIST_GROUP, CdkDrag, CdkDragHandle, CdkDragPlaceholder, CdkDragPreview, CdkDropList, CdkDropListGroup, DragDrop, DragDropModule, DragDropRegistry, DragRef, DropListRef, copyArrayItem, moveItemInArray, transferArrayItem */

    /***/
    function ltgo(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CDK_DRAG_CONFIG", function () {
        return CDK_DRAG_CONFIG;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CDK_DRAG_HANDLE", function () {
        return CDK_DRAG_HANDLE;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CDK_DRAG_PARENT", function () {
        return CDK_DRAG_PARENT;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CDK_DRAG_PLACEHOLDER", function () {
        return CDK_DRAG_PLACEHOLDER;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CDK_DRAG_PREVIEW", function () {
        return CDK_DRAG_PREVIEW;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CDK_DROP_LIST", function () {
        return CDK_DROP_LIST;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CDK_DROP_LIST_GROUP", function () {
        return CDK_DROP_LIST_GROUP;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkDrag", function () {
        return CdkDrag;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkDragHandle", function () {
        return CdkDragHandle;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkDragPlaceholder", function () {
        return CdkDragPlaceholder;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkDragPreview", function () {
        return CdkDragPreview;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkDropList", function () {
        return CdkDropList;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkDropListGroup", function () {
        return CdkDropListGroup;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "DragDrop", function () {
        return DragDrop;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "DragDropModule", function () {
        return DragDropModule;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "DragDropRegistry", function () {
        return DragDropRegistry;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "DragRef", function () {
        return DragRef;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "DropListRef", function () {
        return DropListRef;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "copyArrayItem", function () {
        return copyArrayItem;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "moveItemInArray", function () {
        return moveItemInArray;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "transferArrayItem", function () {
        return transferArrayItem;
      });
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! @angular/common */
      "SVse");
      /* harmony import */


      var _angular_cdk_scrolling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @angular/cdk/scrolling */
      "7KAL");
      /* harmony import */


      var _angular_cdk_platform__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/cdk/platform */
      "SCoL");
      /* harmony import */


      var _angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/cdk/coercion */
      "8LU1");
      /* harmony import */


      var rxjs__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! rxjs */
      "qCKp");
      /* harmony import */


      var rxjs_operators__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! rxjs/operators */
      "kU1M");
      /* harmony import */


      var _angular_cdk_bidi__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @angular/cdk/bidi */
      "9gLZ");
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * Shallow-extends a stylesheet object with another stylesheet object.
       * @docs-private
       */


      function extendStyles(dest, source) {
        for (var key in source) {
          if (source.hasOwnProperty(key)) {
            dest[key] = source[key];
          }
        }

        return dest;
      }
      /**
       * Toggles whether the native drag interactions should be enabled for an element.
       * @param element Element on which to toggle the drag interactions.
       * @param enable Whether the drag interactions should be enabled.
       * @docs-private
       */


      function toggleNativeDragInteractions(element, enable) {
        var userSelect = enable ? '' : 'none';
        extendStyles(element.style, {
          touchAction: enable ? '' : 'none',
          webkitUserDrag: enable ? '' : 'none',
          webkitTapHighlightColor: enable ? '' : 'transparent',
          userSelect: userSelect,
          msUserSelect: userSelect,
          webkitUserSelect: userSelect,
          MozUserSelect: userSelect
        });
      }
      /**
       * Toggles whether an element is visible while preserving its dimensions.
       * @param element Element whose visibility to toggle
       * @param enable Whether the element should be visible.
       * @docs-private
       */


      function toggleVisibility(element, enable) {
        var styles = element.style;
        styles.position = enable ? '' : 'fixed';
        styles.top = styles.opacity = enable ? '' : '0';
        styles.left = enable ? '' : '-999em';
      }
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /** Parses a CSS time value to milliseconds. */


      function parseCssTimeUnitsToMs(value) {
        // Some browsers will return it in seconds, whereas others will return milliseconds.
        var multiplier = value.toLowerCase().indexOf('ms') > -1 ? 1 : 1000;
        return parseFloat(value) * multiplier;
      }
      /** Gets the transform transition duration, including the delay, of an element in milliseconds. */


      function getTransformTransitionDurationInMs(element) {
        var computedStyle = getComputedStyle(element);
        var transitionedProperties = parseCssPropertyValue(computedStyle, 'transition-property');
        var property = transitionedProperties.find(function (prop) {
          return prop === 'transform' || prop === 'all';
        }); // If there's no transition for `all` or `transform`, we shouldn't do anything.

        if (!property) {
          return 0;
        } // Get the index of the property that we're interested in and match
        // it up to the same index in `transition-delay` and `transition-duration`.


        var propertyIndex = transitionedProperties.indexOf(property);
        var rawDurations = parseCssPropertyValue(computedStyle, 'transition-duration');
        var rawDelays = parseCssPropertyValue(computedStyle, 'transition-delay');
        return parseCssTimeUnitsToMs(rawDurations[propertyIndex]) + parseCssTimeUnitsToMs(rawDelays[propertyIndex]);
      }
      /** Parses out multiple values from a computed style into an array. */


      function parseCssPropertyValue(computedStyle, name) {
        var value = computedStyle.getPropertyValue(name);
        return value.split(',').map(function (part) {
          return part.trim();
        });
      }
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /** Gets a mutable version of an element's bounding `ClientRect`. */


      function getMutableClientRect(element) {
        var clientRect = element.getBoundingClientRect(); // We need to clone the `clientRect` here, because all the values on it are readonly
        // and we need to be able to update them. Also we can't use a spread here, because
        // the values on a `ClientRect` aren't own properties. See:
        // https://developer.mozilla.org/en-US/docs/Web/API/Element/getBoundingClientRect#Notes

        return {
          top: clientRect.top,
          right: clientRect.right,
          bottom: clientRect.bottom,
          left: clientRect.left,
          width: clientRect.width,
          height: clientRect.height
        };
      }
      /**
       * Checks whether some coordinates are within a `ClientRect`.
       * @param clientRect ClientRect that is being checked.
       * @param x Coordinates along the X axis.
       * @param y Coordinates along the Y axis.
       */


      function isInsideClientRect(clientRect, x, y) {
        var top = clientRect.top,
            bottom = clientRect.bottom,
            left = clientRect.left,
            right = clientRect.right;
        return y >= top && y <= bottom && x >= left && x <= right;
      }
      /**
       * Updates the top/left positions of a `ClientRect`, as well as their bottom/right counterparts.
       * @param clientRect `ClientRect` that should be updated.
       * @param top Amount to add to the `top` position.
       * @param left Amount to add to the `left` position.
       */


      function adjustClientRect(clientRect, top, left) {
        clientRect.top += top;
        clientRect.bottom = clientRect.top + clientRect.height;
        clientRect.left += left;
        clientRect.right = clientRect.left + clientRect.width;
      }
      /**
       * Checks whether the pointer coordinates are close to a ClientRect.
       * @param rect ClientRect to check against.
       * @param threshold Threshold around the ClientRect.
       * @param pointerX Coordinates along the X axis.
       * @param pointerY Coordinates along the Y axis.
       */


      function isPointerNearClientRect(rect, threshold, pointerX, pointerY) {
        var top = rect.top,
            right = rect.right,
            bottom = rect.bottom,
            left = rect.left,
            width = rect.width,
            height = rect.height;
        var xThreshold = width * threshold;
        var yThreshold = height * threshold;
        return pointerY > top - yThreshold && pointerY < bottom + yThreshold && pointerX > left - xThreshold && pointerX < right + xThreshold;
      }
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /** Keeps track of the scroll position and dimensions of the parents of an element. */


      var ParentPositionTracker = /*#__PURE__*/function () {
        function ParentPositionTracker(_document, _viewportRuler) {
          _classCallCheck(this, ParentPositionTracker);

          this._document = _document;
          this._viewportRuler = _viewportRuler;
          /** Cached positions of the scrollable parent elements. */

          this.positions = new Map();
        }
        /** Clears the cached positions. */


        _createClass(ParentPositionTracker, [{
          key: "clear",
          value: function clear() {
            this.positions.clear();
          }
          /** Caches the positions. Should be called at the beginning of a drag sequence. */

        }, {
          key: "cache",
          value: function cache(elements) {
            var _this24 = this;

            this.clear();
            this.positions.set(this._document, {
              scrollPosition: this._viewportRuler.getViewportScrollPosition()
            });
            elements.forEach(function (element) {
              _this24.positions.set(element, {
                scrollPosition: {
                  top: element.scrollTop,
                  left: element.scrollLeft
                },
                clientRect: getMutableClientRect(element)
              });
            });
          }
          /** Handles scrolling while a drag is taking place. */

        }, {
          key: "handleScroll",
          value: function handleScroll(event) {
            var target = event.target;
            var cachedPosition = this.positions.get(target);

            if (!cachedPosition) {
              return null;
            } // Used when figuring out whether an element is inside the scroll parent. If the scrolled
            // parent is the `document`, we use the `documentElement`, because IE doesn't support
            // `contains` on the `document`.


            var scrolledParentNode = target === this._document ? target.documentElement : target;
            var scrollPosition = cachedPosition.scrollPosition;
            var newTop;
            var newLeft;

            if (target === this._document) {
              var viewportScrollPosition = this._viewportRuler.getViewportScrollPosition();

              newTop = viewportScrollPosition.top;
              newLeft = viewportScrollPosition.left;
            } else {
              newTop = target.scrollTop;
              newLeft = target.scrollLeft;
            }

            var topDifference = scrollPosition.top - newTop;
            var leftDifference = scrollPosition.left - newLeft; // Go through and update the cached positions of the scroll
            // parents that are inside the element that was scrolled.

            this.positions.forEach(function (position, node) {
              if (position.clientRect && target !== node && scrolledParentNode.contains(node)) {
                adjustClientRect(position.clientRect, topDifference, leftDifference);
              }
            });
            scrollPosition.top = newTop;
            scrollPosition.left = newLeft;
            return {
              top: topDifference,
              left: leftDifference
            };
          }
        }]);

        return ParentPositionTracker;
      }();
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /** Creates a deep clone of an element. */


      function deepCloneNode(node) {
        var clone = node.cloneNode(true);
        var descendantsWithId = clone.querySelectorAll('[id]');
        var nodeName = node.nodeName.toLowerCase(); // Remove the `id` to avoid having multiple elements with the same id on the page.

        clone.removeAttribute('id');

        for (var i = 0; i < descendantsWithId.length; i++) {
          descendantsWithId[i].removeAttribute('id');
        }

        if (nodeName === 'canvas') {
          transferCanvasData(node, clone);
        } else if (nodeName === 'input' || nodeName === 'select' || nodeName === 'textarea') {
          transferInputData(node, clone);
        }

        transferData('canvas', node, clone, transferCanvasData);
        transferData('input, textarea, select', node, clone, transferInputData);
        return clone;
      }
      /** Matches elements between an element and its clone and allows for their data to be cloned. */


      function transferData(selector, node, clone, callback) {
        var descendantElements = node.querySelectorAll(selector);

        if (descendantElements.length) {
          var cloneElements = clone.querySelectorAll(selector);

          for (var i = 0; i < descendantElements.length; i++) {
            callback(descendantElements[i], cloneElements[i]);
          }
        }
      } // Counter for unique cloned radio button names.


      var cloneUniqueId = 0;
      /** Transfers the data of one input element to another. */

      function transferInputData(source, clone) {
        // Browsers throw an error when assigning the value of a file input programmatically.
        if (clone.type !== 'file') {
          clone.value = source.value;
        } // Radio button `name` attributes must be unique for radio button groups
        // otherwise original radio buttons can lose their checked state
        // once the clone is inserted in the DOM.


        if (clone.type === 'radio' && clone.name) {
          clone.name = "mat-clone-".concat(clone.name, "-").concat(cloneUniqueId++);
        }
      }
      /** Transfers the data of one canvas element to another. */


      function transferCanvasData(source, clone) {
        var context = clone.getContext('2d');

        if (context) {
          // In some cases `drawImage` can throw (e.g. if the canvas size is 0x0).
          // We can't do much about it so just ignore the error.
          try {
            context.drawImage(source, 0, 0);
          } catch (_a) {}
        }
      }
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /** Options that can be used to bind a passive event listener. */


      var passiveEventListenerOptions = Object(_angular_cdk_platform__WEBPACK_IMPORTED_MODULE_3__["normalizePassiveListenerOptions"])({
        passive: true
      });
      /** Options that can be used to bind an active event listener. */

      var activeEventListenerOptions = Object(_angular_cdk_platform__WEBPACK_IMPORTED_MODULE_3__["normalizePassiveListenerOptions"])({
        passive: false
      });
      /**
       * Time in milliseconds for which to ignore mouse events, after
       * receiving a touch event. Used to avoid doing double work for
       * touch devices where the browser fires fake mouse events, in
       * addition to touch events.
       */

      var MOUSE_EVENT_IGNORE_TIME = 800;
      /**
       * Reference to a draggable item. Used to manipulate or dispose of the item.
       */

      var DragRef = /*#__PURE__*/function () {
        function DragRef(element, _config, _document, _ngZone, _viewportRuler, _dragDropRegistry) {
          var _this25 = this;

          _classCallCheck(this, DragRef);

          this._config = _config;
          this._document = _document;
          this._ngZone = _ngZone;
          this._viewportRuler = _viewportRuler;
          this._dragDropRegistry = _dragDropRegistry;
          /**
           * CSS `transform` applied to the element when it isn't being dragged. We need a
           * passive transform in order for the dragged element to retain its new position
           * after the user has stopped dragging and because we need to know the relative
           * position in case they start dragging again. This corresponds to `element.style.transform`.
           */

          this._passiveTransform = {
            x: 0,
            y: 0
          };
          /** CSS `transform` that is applied to the element while it's being dragged. */

          this._activeTransform = {
            x: 0,
            y: 0
          };
          /** Emits when the item is being moved. */

          this._moveEvents = new rxjs__WEBPACK_IMPORTED_MODULE_5__["Subject"]();
          /** Subscription to pointer movement events. */

          this._pointerMoveSubscription = rxjs__WEBPACK_IMPORTED_MODULE_5__["Subscription"].EMPTY;
          /** Subscription to the event that is dispatched when the user lifts their pointer. */

          this._pointerUpSubscription = rxjs__WEBPACK_IMPORTED_MODULE_5__["Subscription"].EMPTY;
          /** Subscription to the viewport being scrolled. */

          this._scrollSubscription = rxjs__WEBPACK_IMPORTED_MODULE_5__["Subscription"].EMPTY;
          /** Subscription to the viewport being resized. */

          this._resizeSubscription = rxjs__WEBPACK_IMPORTED_MODULE_5__["Subscription"].EMPTY;
          /** Cached reference to the boundary element. */

          this._boundaryElement = null;
          /** Whether the native dragging interactions have been enabled on the root element. */

          this._nativeInteractionsEnabled = true;
          /** Elements that can be used to drag the draggable item. */

          this._handles = [];
          /** Registered handles that are currently disabled. */

          this._disabledHandles = new Set();
          /** Layout direction of the item. */

          this._direction = 'ltr';
          /**
           * Amount of milliseconds to wait after the user has put their
           * pointer down before starting to drag the element.
           */

          this.dragStartDelay = 0;
          this._disabled = false;
          /** Emits as the drag sequence is being prepared. */

          this.beforeStarted = new rxjs__WEBPACK_IMPORTED_MODULE_5__["Subject"]();
          /** Emits when the user starts dragging the item. */

          this.started = new rxjs__WEBPACK_IMPORTED_MODULE_5__["Subject"]();
          /** Emits when the user has released a drag item, before any animations have started. */

          this.released = new rxjs__WEBPACK_IMPORTED_MODULE_5__["Subject"]();
          /** Emits when the user stops dragging an item in the container. */

          this.ended = new rxjs__WEBPACK_IMPORTED_MODULE_5__["Subject"]();
          /** Emits when the user has moved the item into a new container. */

          this.entered = new rxjs__WEBPACK_IMPORTED_MODULE_5__["Subject"]();
          /** Emits when the user removes the item its container by dragging it into another container. */

          this.exited = new rxjs__WEBPACK_IMPORTED_MODULE_5__["Subject"]();
          /** Emits when the user drops the item inside a container. */

          this.dropped = new rxjs__WEBPACK_IMPORTED_MODULE_5__["Subject"]();
          /**
           * Emits as the user is dragging the item. Use with caution,
           * because this event will fire for every pixel that the user has dragged.
           */

          this.moved = this._moveEvents;
          /** Handler for the `mousedown`/`touchstart` events. */

          this._pointerDown = function (event) {
            _this25.beforeStarted.next(); // Delegate the event based on whether it started from a handle or the element itself.


            if (_this25._handles.length) {
              var targetHandle = _this25._handles.find(function (handle) {
                var target = event.target;
                return !!target && (target === handle || handle.contains(target));
              });

              if (targetHandle && !_this25._disabledHandles.has(targetHandle) && !_this25.disabled) {
                _this25._initializeDragSequence(targetHandle, event);
              }
            } else if (!_this25.disabled) {
              _this25._initializeDragSequence(_this25._rootElement, event);
            }
          };
          /** Handler that is invoked when the user moves their pointer after they've initiated a drag. */


          this._pointerMove = function (event) {
            var pointerPosition = _this25._getPointerPositionOnPage(event);

            if (!_this25._hasStartedDragging) {
              var distanceX = Math.abs(pointerPosition.x - _this25._pickupPositionOnPage.x);
              var distanceY = Math.abs(pointerPosition.y - _this25._pickupPositionOnPage.y);
              var isOverThreshold = distanceX + distanceY >= _this25._config.dragStartThreshold; // Only start dragging after the user has moved more than the minimum distance in either
              // direction. Note that this is preferrable over doing something like `skip(minimumDistance)`
              // in the `pointerMove` subscription, because we're not guaranteed to have one move event
              // per pixel of movement (e.g. if the user moves their pointer quickly).

              if (isOverThreshold) {
                var isDelayElapsed = Date.now() >= _this25._dragStartTime + _this25._getDragStartDelay(event);

                var container = _this25._dropContainer;

                if (!isDelayElapsed) {
                  _this25._endDragSequence(event);

                  return;
                } // Prevent other drag sequences from starting while something in the container is still
                // being dragged. This can happen while we're waiting for the drop animation to finish
                // and can cause errors, because some elements might still be moving around.


                if (!container || !container.isDragging() && !container.isReceiving()) {
                  _this25._hasStartedDragging = true;

                  _this25._ngZone.run(function () {
                    return _this25._startDragSequence(event);
                  });
                }
              }

              return;
            } // We only need the preview dimensions if we have a boundary element.


            if (_this25._boundaryElement) {
              // Cache the preview element rect if we haven't cached it already or if
              // we cached it too early before the element dimensions were computed.
              if (!_this25._previewRect || !_this25._previewRect.width && !_this25._previewRect.height) {
                _this25._previewRect = (_this25._preview || _this25._rootElement).getBoundingClientRect();
              }
            } // We prevent the default action down here so that we know that dragging has started. This is
            // important for touch devices where doing this too early can unnecessarily block scrolling,
            // if there's a dragging delay.


            event.preventDefault();

            var constrainedPointerPosition = _this25._getConstrainedPointerPosition(pointerPosition);

            _this25._hasMoved = true;
            _this25._lastKnownPointerPosition = pointerPosition;

            _this25._updatePointerDirectionDelta(constrainedPointerPosition);

            if (_this25._dropContainer) {
              _this25._updateActiveDropContainer(constrainedPointerPosition, pointerPosition);
            } else {
              var activeTransform = _this25._activeTransform;
              activeTransform.x = constrainedPointerPosition.x - _this25._pickupPositionOnPage.x + _this25._passiveTransform.x;
              activeTransform.y = constrainedPointerPosition.y - _this25._pickupPositionOnPage.y + _this25._passiveTransform.y;

              _this25._applyRootElementTransform(activeTransform.x, activeTransform.y); // Apply transform as attribute if dragging and svg element to work for IE


              if (typeof SVGElement !== 'undefined' && _this25._rootElement instanceof SVGElement) {
                var appliedTransform = "translate(".concat(activeTransform.x, " ").concat(activeTransform.y, ")");

                _this25._rootElement.setAttribute('transform', appliedTransform);
              }
            } // Since this event gets fired for every pixel while dragging, we only
            // want to fire it if the consumer opted into it. Also we have to
            // re-enter the zone because we run all of the events on the outside.


            if (_this25._moveEvents.observers.length) {
              _this25._ngZone.run(function () {
                _this25._moveEvents.next({
                  source: _this25,
                  pointerPosition: constrainedPointerPosition,
                  event: event,
                  distance: _this25._getDragDistance(constrainedPointerPosition),
                  delta: _this25._pointerDirectionDelta
                });
              });
            }
          };
          /** Handler that is invoked when the user lifts their pointer up, after initiating a drag. */


          this._pointerUp = function (event) {
            _this25._endDragSequence(event);
          };

          this.withRootElement(element);
          this._parentPositions = new ParentPositionTracker(_document, _viewportRuler);

          _dragDropRegistry.registerDragItem(this);
        }
        /** Whether starting to drag this element is disabled. */


        _createClass(DragRef, [{
          key: "getPlaceholderElement",

          /**
           * Returns the element that is being used as a placeholder
           * while the current element is being dragged.
           */
          value: function getPlaceholderElement() {
            return this._placeholder;
          }
          /** Returns the root draggable element. */

        }, {
          key: "getRootElement",
          value: function getRootElement() {
            return this._rootElement;
          }
          /**
           * Gets the currently-visible element that represents the drag item.
           * While dragging this is the placeholder, otherwise it's the root element.
           */

        }, {
          key: "getVisibleElement",
          value: function getVisibleElement() {
            return this.isDragging() ? this.getPlaceholderElement() : this.getRootElement();
          }
          /** Registers the handles that can be used to drag the element. */

        }, {
          key: "withHandles",
          value: function withHandles(handles) {
            var _this26 = this;

            this._handles = handles.map(function (handle) {
              return Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_4__["coerceElement"])(handle);
            });

            this._handles.forEach(function (handle) {
              return toggleNativeDragInteractions(handle, _this26.disabled);
            });

            this._toggleNativeDragInteractions(); // Delete any lingering disabled handles that may have been destroyed. Note that we re-create
            // the set, rather than iterate over it and filter out the destroyed handles, because while
            // the ES spec allows for sets to be modified while they're being iterated over, some polyfills
            // use an array internally which may throw an error.


            var disabledHandles = new Set();

            this._disabledHandles.forEach(function (handle) {
              if (_this26._handles.indexOf(handle) > -1) {
                disabledHandles.add(handle);
              }
            });

            this._disabledHandles = disabledHandles;
            return this;
          }
          /**
           * Registers the template that should be used for the drag preview.
           * @param template Template that from which to stamp out the preview.
           */

        }, {
          key: "withPreviewTemplate",
          value: function withPreviewTemplate(template) {
            this._previewTemplate = template;
            return this;
          }
          /**
           * Registers the template that should be used for the drag placeholder.
           * @param template Template that from which to stamp out the placeholder.
           */

        }, {
          key: "withPlaceholderTemplate",
          value: function withPlaceholderTemplate(template) {
            this._placeholderTemplate = template;
            return this;
          }
          /**
           * Sets an alternate drag root element. The root element is the element that will be moved as
           * the user is dragging. Passing an alternate root element is useful when trying to enable
           * dragging on an element that you might not have access to.
           */

        }, {
          key: "withRootElement",
          value: function withRootElement(rootElement) {
            var _this27 = this;

            var element = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_4__["coerceElement"])(rootElement);

            if (element !== this._rootElement) {
              if (this._rootElement) {
                this._removeRootElementListeners(this._rootElement);
              }

              this._ngZone.runOutsideAngular(function () {
                element.addEventListener('mousedown', _this27._pointerDown, activeEventListenerOptions);
                element.addEventListener('touchstart', _this27._pointerDown, passiveEventListenerOptions);
              });

              this._initialTransform = undefined;
              this._rootElement = element;
            }

            if (typeof SVGElement !== 'undefined' && this._rootElement instanceof SVGElement) {
              this._ownerSVGElement = this._rootElement.ownerSVGElement;
            }

            return this;
          }
          /**
           * Element to which the draggable's position will be constrained.
           */

        }, {
          key: "withBoundaryElement",
          value: function withBoundaryElement(boundaryElement) {
            var _this28 = this;

            this._boundaryElement = boundaryElement ? Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_4__["coerceElement"])(boundaryElement) : null;

            this._resizeSubscription.unsubscribe();

            if (boundaryElement) {
              this._resizeSubscription = this._viewportRuler.change(10).subscribe(function () {
                return _this28._containInsideBoundaryOnResize();
              });
            }

            return this;
          }
          /** Removes the dragging functionality from the DOM element. */

        }, {
          key: "dispose",
          value: function dispose() {
            this._removeRootElementListeners(this._rootElement); // Do this check before removing from the registry since it'll
            // stop being considered as dragged once it is removed.


            if (this.isDragging()) {
              // Since we move out the element to the end of the body while it's being
              // dragged, we have to make sure that it's removed if it gets destroyed.
              removeNode(this._rootElement);
            }

            removeNode(this._anchor);

            this._destroyPreview();

            this._destroyPlaceholder();

            this._dragDropRegistry.removeDragItem(this);

            this._removeSubscriptions();

            this.beforeStarted.complete();
            this.started.complete();
            this.released.complete();
            this.ended.complete();
            this.entered.complete();
            this.exited.complete();
            this.dropped.complete();

            this._moveEvents.complete();

            this._handles = [];

            this._disabledHandles.clear();

            this._dropContainer = undefined;

            this._resizeSubscription.unsubscribe();

            this._parentPositions.clear();

            this._boundaryElement = this._rootElement = this._ownerSVGElement = this._placeholderTemplate = this._previewTemplate = this._anchor = null;
          }
          /** Checks whether the element is currently being dragged. */

        }, {
          key: "isDragging",
          value: function isDragging() {
            return this._hasStartedDragging && this._dragDropRegistry.isDragging(this);
          }
          /** Resets a standalone drag item to its initial position. */

        }, {
          key: "reset",
          value: function reset() {
            this._rootElement.style.transform = this._initialTransform || '';
            this._activeTransform = {
              x: 0,
              y: 0
            };
            this._passiveTransform = {
              x: 0,
              y: 0
            };
          }
          /**
           * Sets a handle as disabled. While a handle is disabled, it'll capture and interrupt dragging.
           * @param handle Handle element that should be disabled.
           */

        }, {
          key: "disableHandle",
          value: function disableHandle(handle) {
            if (!this._disabledHandles.has(handle) && this._handles.indexOf(handle) > -1) {
              this._disabledHandles.add(handle);

              toggleNativeDragInteractions(handle, true);
            }
          }
          /**
           * Enables a handle, if it has been disabled.
           * @param handle Handle element to be enabled.
           */

        }, {
          key: "enableHandle",
          value: function enableHandle(handle) {
            if (this._disabledHandles.has(handle)) {
              this._disabledHandles["delete"](handle);

              toggleNativeDragInteractions(handle, this.disabled);
            }
          }
          /** Sets the layout direction of the draggable item. */

        }, {
          key: "withDirection",
          value: function withDirection(direction) {
            this._direction = direction;
            return this;
          }
          /** Sets the container that the item is part of. */

        }, {
          key: "_withDropContainer",
          value: function _withDropContainer(container) {
            this._dropContainer = container;
          }
          /**
           * Gets the current position in pixels the draggable outside of a drop container.
           */

        }, {
          key: "getFreeDragPosition",
          value: function getFreeDragPosition() {
            var position = this.isDragging() ? this._activeTransform : this._passiveTransform;
            return {
              x: position.x,
              y: position.y
            };
          }
          /**
           * Sets the current position in pixels the draggable outside of a drop container.
           * @param value New position to be set.
           */

        }, {
          key: "setFreeDragPosition",
          value: function setFreeDragPosition(value) {
            this._activeTransform = {
              x: 0,
              y: 0
            };
            this._passiveTransform.x = value.x;
            this._passiveTransform.y = value.y;

            if (!this._dropContainer) {
              this._applyRootElementTransform(value.x, value.y);
            }

            return this;
          }
          /** Updates the item's sort order based on the last-known pointer position. */

        }, {
          key: "_sortFromLastPointerPosition",
          value: function _sortFromLastPointerPosition() {
            var position = this._lastKnownPointerPosition;

            if (position && this._dropContainer) {
              this._updateActiveDropContainer(this._getConstrainedPointerPosition(position), position);
            }
          }
          /** Unsubscribes from the global subscriptions. */

        }, {
          key: "_removeSubscriptions",
          value: function _removeSubscriptions() {
            this._pointerMoveSubscription.unsubscribe();

            this._pointerUpSubscription.unsubscribe();

            this._scrollSubscription.unsubscribe();
          }
          /** Destroys the preview element and its ViewRef. */

        }, {
          key: "_destroyPreview",
          value: function _destroyPreview() {
            if (this._preview) {
              removeNode(this._preview);
            }

            if (this._previewRef) {
              this._previewRef.destroy();
            }

            this._preview = this._previewRef = null;
          }
          /** Destroys the placeholder element and its ViewRef. */

        }, {
          key: "_destroyPlaceholder",
          value: function _destroyPlaceholder() {
            if (this._placeholder) {
              removeNode(this._placeholder);
            }

            if (this._placeholderRef) {
              this._placeholderRef.destroy();
            }

            this._placeholder = this._placeholderRef = null;
          }
          /**
           * Clears subscriptions and stops the dragging sequence.
           * @param event Browser event object that ended the sequence.
           */

        }, {
          key: "_endDragSequence",
          value: function _endDragSequence(event) {
            var _this29 = this;

            // Note that here we use `isDragging` from the service, rather than from `this`.
            // The difference is that the one from the service reflects whether a dragging sequence
            // has been initiated, whereas the one on `this` includes whether the user has passed
            // the minimum dragging threshold.
            if (!this._dragDropRegistry.isDragging(this)) {
              return;
            }

            this._removeSubscriptions();

            this._dragDropRegistry.stopDragging(this);

            this._toggleNativeDragInteractions();

            if (this._handles) {
              this._rootElement.style.webkitTapHighlightColor = this._rootElementTapHighlight;
            }

            if (!this._hasStartedDragging) {
              return;
            }

            this.released.next({
              source: this
            });

            if (this._dropContainer) {
              // Stop scrolling immediately, instead of waiting for the animation to finish.
              this._dropContainer._stopScrolling();

              this._animatePreviewToPlaceholder().then(function () {
                _this29._cleanupDragArtifacts(event);

                _this29._cleanupCachedDimensions();

                _this29._dragDropRegistry.stopDragging(_this29);
              });
            } else {
              // Convert the active transform into a passive one. This means that next time
              // the user starts dragging the item, its position will be calculated relatively
              // to the new passive transform.
              this._passiveTransform.x = this._activeTransform.x;
              this._passiveTransform.y = this._activeTransform.y;

              this._ngZone.run(function () {
                _this29.ended.next({
                  source: _this29,
                  distance: _this29._getDragDistance(_this29._getPointerPositionOnPage(event))
                });
              });

              this._cleanupCachedDimensions();

              this._dragDropRegistry.stopDragging(this);
            }
          }
          /** Starts the dragging sequence. */

        }, {
          key: "_startDragSequence",
          value: function _startDragSequence(event) {
            if (isTouchEvent(event)) {
              this._lastTouchEventTime = Date.now();
            }

            this._toggleNativeDragInteractions();

            var dropContainer = this._dropContainer;

            if (dropContainer) {
              var element = this._rootElement;
              var parent = element.parentNode;

              var preview = this._preview = this._createPreviewElement();

              var placeholder = this._placeholder = this._createPlaceholderElement();

              var anchor = this._anchor = this._anchor || this._document.createComment(''); // Needs to happen before the root element is moved.


              var shadowRoot = this._getShadowRoot(); // Insert an anchor node so that we can restore the element's position in the DOM.


              parent.insertBefore(anchor, element); // We move the element out at the end of the body and we make it hidden, because keeping it in
              // place will throw off the consumer's `:last-child` selectors. We can't remove the element
              // from the DOM completely, because iOS will stop firing all subsequent events in the chain.

              toggleVisibility(element, false);

              this._document.body.appendChild(parent.replaceChild(placeholder, element));

              getPreviewInsertionPoint(this._document, shadowRoot).appendChild(preview);
              this.started.next({
                source: this
              }); // Emit before notifying the container.

              dropContainer.start();
              this._initialContainer = dropContainer;
              this._initialIndex = dropContainer.getItemIndex(this);
            } else {
              this.started.next({
                source: this
              });
              this._initialContainer = this._initialIndex = undefined;
            } // Important to run after we've called `start` on the parent container
            // so that it has had time to resolve its scrollable parents.


            this._parentPositions.cache(dropContainer ? dropContainer.getScrollableParents() : []);
          }
          /**
           * Sets up the different variables and subscriptions
           * that will be necessary for the dragging sequence.
           * @param referenceElement Element that started the drag sequence.
           * @param event Browser event object that started the sequence.
           */

        }, {
          key: "_initializeDragSequence",
          value: function _initializeDragSequence(referenceElement, event) {
            var _this30 = this;

            // Stop propagation if the item is inside another
            // draggable so we don't start multiple drag sequences.
            if (this._config.parentDragRef) {
              event.stopPropagation();
            }

            var isDragging = this.isDragging();
            var isTouchSequence = isTouchEvent(event);
            var isAuxiliaryMouseButton = !isTouchSequence && event.button !== 0;
            var rootElement = this._rootElement;
            var isSyntheticEvent = !isTouchSequence && this._lastTouchEventTime && this._lastTouchEventTime + MOUSE_EVENT_IGNORE_TIME > Date.now(); // If the event started from an element with the native HTML drag&drop, it'll interfere
            // with our own dragging (e.g. `img` tags do it by default). Prevent the default action
            // to stop it from happening. Note that preventing on `dragstart` also seems to work, but
            // it's flaky and it fails if the user drags it away quickly. Also note that we only want
            // to do this for `mousedown` since doing the same for `touchstart` will stop any `click`
            // events from firing on touch devices.

            if (event.target && event.target.draggable && event.type === 'mousedown') {
              event.preventDefault();
            } // Abort if the user is already dragging or is using a mouse button other than the primary one.


            if (isDragging || isAuxiliaryMouseButton || isSyntheticEvent) {
              return;
            } // If we've got handles, we need to disable the tap highlight on the entire root element,
            // otherwise iOS will still add it, even though all the drag interactions on the handle
            // are disabled.


            if (this._handles.length) {
              this._rootElementTapHighlight = rootElement.style.webkitTapHighlightColor || '';
              rootElement.style.webkitTapHighlightColor = 'transparent';
            }

            this._hasStartedDragging = this._hasMoved = false; // Avoid multiple subscriptions and memory leaks when multi touch
            // (isDragging check above isn't enough because of possible temporal and/or dimensional delays)

            this._removeSubscriptions();

            this._pointerMoveSubscription = this._dragDropRegistry.pointerMove.subscribe(this._pointerMove);
            this._pointerUpSubscription = this._dragDropRegistry.pointerUp.subscribe(this._pointerUp);
            this._scrollSubscription = this._dragDropRegistry.scroll.subscribe(function (scrollEvent) {
              _this30._updateOnScroll(scrollEvent);
            });

            if (this._boundaryElement) {
              this._boundaryRect = getMutableClientRect(this._boundaryElement);
            } // If we have a custom preview we can't know ahead of time how large it'll be so we position
            // it next to the cursor. The exception is when the consumer has opted into making the preview
            // the same size as the root element, in which case we do know the size.


            var previewTemplate = this._previewTemplate;
            this._pickupPositionInElement = previewTemplate && previewTemplate.template && !previewTemplate.matchSize ? {
              x: 0,
              y: 0
            } : this._getPointerPositionInElement(referenceElement, event);

            var pointerPosition = this._pickupPositionOnPage = this._lastKnownPointerPosition = this._getPointerPositionOnPage(event);

            this._pointerDirectionDelta = {
              x: 0,
              y: 0
            };
            this._pointerPositionAtLastDirectionChange = {
              x: pointerPosition.x,
              y: pointerPosition.y
            };
            this._dragStartTime = Date.now();

            this._dragDropRegistry.startDragging(this, event);
          }
          /** Cleans up the DOM artifacts that were added to facilitate the element being dragged. */

        }, {
          key: "_cleanupDragArtifacts",
          value: function _cleanupDragArtifacts(event) {
            var _this31 = this;

            // Restore the element's visibility and insert it at its old position in the DOM.
            // It's important that we maintain the position, because moving the element around in the DOM
            // can throw off `NgFor` which does smart diffing and re-creates elements only when necessary,
            // while moving the existing elements in all other cases.
            toggleVisibility(this._rootElement, true);

            this._anchor.parentNode.replaceChild(this._rootElement, this._anchor);

            this._destroyPreview();

            this._destroyPlaceholder();

            this._boundaryRect = this._previewRect = undefined; // Re-enter the NgZone since we bound `document` events on the outside.

            this._ngZone.run(function () {
              var container = _this31._dropContainer;
              var currentIndex = container.getItemIndex(_this31);

              var pointerPosition = _this31._getPointerPositionOnPage(event);

              var distance = _this31._getDragDistance(_this31._getPointerPositionOnPage(event));

              var isPointerOverContainer = container._isOverContainer(pointerPosition.x, pointerPosition.y);

              _this31.ended.next({
                source: _this31,
                distance: distance
              });

              _this31.dropped.next({
                item: _this31,
                currentIndex: currentIndex,
                previousIndex: _this31._initialIndex,
                container: container,
                previousContainer: _this31._initialContainer,
                isPointerOverContainer: isPointerOverContainer,
                distance: distance
              });

              container.drop(_this31, currentIndex, _this31._initialIndex, _this31._initialContainer, isPointerOverContainer, distance);
              _this31._dropContainer = _this31._initialContainer;
            });
          }
          /**
           * Updates the item's position in its drop container, or moves it
           * into a new one, depending on its current drag position.
           */

        }, {
          key: "_updateActiveDropContainer",
          value: function _updateActiveDropContainer(_ref11, _ref12) {
            var _this32 = this;

            var x = _ref11.x,
                y = _ref11.y;
            var rawX = _ref12.x,
                rawY = _ref12.y;

            // Drop container that draggable has been moved into.
            var newContainer = this._initialContainer._getSiblingContainerFromPosition(this, x, y); // If we couldn't find a new container to move the item into, and the item has left its
            // initial container, check whether the it's over the initial container. This handles the
            // case where two containers are connected one way and the user tries to undo dragging an
            // item into a new container.


            if (!newContainer && this._dropContainer !== this._initialContainer && this._initialContainer._isOverContainer(x, y)) {
              newContainer = this._initialContainer;
            }

            if (newContainer && newContainer !== this._dropContainer) {
              this._ngZone.run(function () {
                // Notify the old container that the item has left.
                _this32.exited.next({
                  item: _this32,
                  container: _this32._dropContainer
                });

                _this32._dropContainer.exit(_this32); // Notify the new container that the item has entered.


                _this32._dropContainer = newContainer;

                _this32._dropContainer.enter(_this32, x, y, newContainer === _this32._initialContainer && // If we're re-entering the initial container and sorting is disabled,
                // put item the into its starting index to begin with.
                newContainer.sortingDisabled ? _this32._initialIndex : undefined);

                _this32.entered.next({
                  item: _this32,
                  container: newContainer,
                  currentIndex: newContainer.getItemIndex(_this32)
                });
              });
            }

            this._dropContainer._startScrollingIfNecessary(rawX, rawY);

            this._dropContainer._sortItem(this, x, y, this._pointerDirectionDelta);

            this._preview.style.transform = getTransform(x - this._pickupPositionInElement.x, y - this._pickupPositionInElement.y);
          }
          /**
           * Creates the element that will be rendered next to the user's pointer
           * and will be used as a preview of the element that is being dragged.
           */

        }, {
          key: "_createPreviewElement",
          value: function _createPreviewElement() {
            var previewConfig = this._previewTemplate;
            var previewClass = this.previewClass;
            var previewTemplate = previewConfig ? previewConfig.template : null;
            var preview;

            if (previewTemplate && previewConfig) {
              // Measure the element before we've inserted the preview
              // since the insertion could throw off the measurement.
              var rootRect = previewConfig.matchSize ? this._rootElement.getBoundingClientRect() : null;
              var viewRef = previewConfig.viewContainer.createEmbeddedView(previewTemplate, previewConfig.context);
              viewRef.detectChanges();
              preview = getRootNode(viewRef, this._document);
              this._previewRef = viewRef;

              if (previewConfig.matchSize) {
                matchElementSize(preview, rootRect);
              } else {
                preview.style.transform = getTransform(this._pickupPositionOnPage.x, this._pickupPositionOnPage.y);
              }
            } else {
              var element = this._rootElement;
              preview = deepCloneNode(element);
              matchElementSize(preview, element.getBoundingClientRect());
            }

            extendStyles(preview.style, {
              // It's important that we disable the pointer events on the preview, because
              // it can throw off the `document.elementFromPoint` calls in the `CdkDropList`.
              pointerEvents: 'none',
              // We have to reset the margin, because it can throw off positioning relative to the viewport.
              margin: '0',
              position: 'fixed',
              top: '0',
              left: '0',
              zIndex: "".concat(this._config.zIndex || 1000)
            });
            toggleNativeDragInteractions(preview, false);
            preview.classList.add('cdk-drag-preview');
            preview.setAttribute('dir', this._direction);

            if (previewClass) {
              if (Array.isArray(previewClass)) {
                previewClass.forEach(function (className) {
                  return preview.classList.add(className);
                });
              } else {
                preview.classList.add(previewClass);
              }
            }

            return preview;
          }
          /**
           * Animates the preview element from its current position to the location of the drop placeholder.
           * @returns Promise that resolves when the animation completes.
           */

        }, {
          key: "_animatePreviewToPlaceholder",
          value: function _animatePreviewToPlaceholder() {
            var _this33 = this;

            // If the user hasn't moved yet, the transitionend event won't fire.
            if (!this._hasMoved) {
              return Promise.resolve();
            }

            var placeholderRect = this._placeholder.getBoundingClientRect(); // Apply the class that adds a transition to the preview.


            this._preview.classList.add('cdk-drag-animating'); // Move the preview to the placeholder position.


            this._preview.style.transform = getTransform(placeholderRect.left, placeholderRect.top); // If the element doesn't have a `transition`, the `transitionend` event won't fire. Since
            // we need to trigger a style recalculation in order for the `cdk-drag-animating` class to
            // apply its style, we take advantage of the available info to figure out whether we need to
            // bind the event in the first place.

            var duration = getTransformTransitionDurationInMs(this._preview);

            if (duration === 0) {
              return Promise.resolve();
            }

            return this._ngZone.runOutsideAngular(function () {
              return new Promise(function (resolve) {
                var handler = function handler(event) {
                  if (!event || event.target === _this33._preview && event.propertyName === 'transform') {
                    _this33._preview.removeEventListener('transitionend', handler);

                    resolve();
                    clearTimeout(timeout);
                  }
                }; // If a transition is short enough, the browser might not fire the `transitionend` event.
                // Since we know how long it's supposed to take, add a timeout with a 50% buffer that'll
                // fire if the transition hasn't completed when it was supposed to.


                var timeout = setTimeout(handler, duration * 1.5);

                _this33._preview.addEventListener('transitionend', handler);
              });
            });
          }
          /** Creates an element that will be shown instead of the current element while dragging. */

        }, {
          key: "_createPlaceholderElement",
          value: function _createPlaceholderElement() {
            var placeholderConfig = this._placeholderTemplate;
            var placeholderTemplate = placeholderConfig ? placeholderConfig.template : null;
            var placeholder;

            if (placeholderTemplate) {
              this._placeholderRef = placeholderConfig.viewContainer.createEmbeddedView(placeholderTemplate, placeholderConfig.context);

              this._placeholderRef.detectChanges();

              placeholder = getRootNode(this._placeholderRef, this._document);
            } else {
              placeholder = deepCloneNode(this._rootElement);
            }

            placeholder.classList.add('cdk-drag-placeholder');
            return placeholder;
          }
          /**
           * Figures out the coordinates at which an element was picked up.
           * @param referenceElement Element that initiated the dragging.
           * @param event Event that initiated the dragging.
           */

        }, {
          key: "_getPointerPositionInElement",
          value: function _getPointerPositionInElement(referenceElement, event) {
            var elementRect = this._rootElement.getBoundingClientRect();

            var handleElement = referenceElement === this._rootElement ? null : referenceElement;
            var referenceRect = handleElement ? handleElement.getBoundingClientRect() : elementRect;
            var point = isTouchEvent(event) ? event.targetTouches[0] : event;

            var scrollPosition = this._getViewportScrollPosition();

            var x = point.pageX - referenceRect.left - scrollPosition.left;
            var y = point.pageY - referenceRect.top - scrollPosition.top;
            return {
              x: referenceRect.left - elementRect.left + x,
              y: referenceRect.top - elementRect.top + y
            };
          }
          /** Determines the point of the page that was touched by the user. */

        }, {
          key: "_getPointerPositionOnPage",
          value: function _getPointerPositionOnPage(event) {
            var scrollPosition = this._getViewportScrollPosition();

            var point = isTouchEvent(event) ? // `touches` will be empty for start/end events so we have to fall back to `changedTouches`.
            // Also note that on real devices we're guaranteed for either `touches` or `changedTouches`
            // to have a value, but Firefox in device emulation mode has a bug where both can be empty
            // for `touchstart` and `touchend` so we fall back to a dummy object in order to avoid
            // throwing an error. The value returned here will be incorrect, but since this only
            // breaks inside a developer tool and the value is only used for secondary information,
            // we can get away with it. See https://bugzilla.mozilla.org/show_bug.cgi?id=1615824.
            event.touches[0] || event.changedTouches[0] || {
              pageX: 0,
              pageY: 0
            } : event;
            var x = point.pageX - scrollPosition.left;
            var y = point.pageY - scrollPosition.top; // if dragging SVG element, try to convert from the screen coordinate system to the SVG
            // coordinate system

            if (this._ownerSVGElement) {
              var svgMatrix = this._ownerSVGElement.getScreenCTM();

              if (svgMatrix) {
                var svgPoint = this._ownerSVGElement.createSVGPoint();

                svgPoint.x = x;
                svgPoint.y = y;
                return svgPoint.matrixTransform(svgMatrix.inverse());
              }
            }

            return {
              x: x,
              y: y
            };
          }
          /** Gets the pointer position on the page, accounting for any position constraints. */

        }, {
          key: "_getConstrainedPointerPosition",
          value: function _getConstrainedPointerPosition(point) {
            var dropContainerLock = this._dropContainer ? this._dropContainer.lockAxis : null;

            var _ref13 = this.constrainPosition ? this.constrainPosition(point, this) : point,
                x = _ref13.x,
                y = _ref13.y;

            if (this.lockAxis === 'x' || dropContainerLock === 'x') {
              y = this._pickupPositionOnPage.y;
            } else if (this.lockAxis === 'y' || dropContainerLock === 'y') {
              x = this._pickupPositionOnPage.x;
            }

            if (this._boundaryRect) {
              var _this$_pickupPosition = this._pickupPositionInElement,
                  pickupX = _this$_pickupPosition.x,
                  pickupY = _this$_pickupPosition.y;
              var boundaryRect = this._boundaryRect;
              var previewRect = this._previewRect;
              var minY = boundaryRect.top + pickupY;
              var maxY = boundaryRect.bottom - (previewRect.height - pickupY);
              var minX = boundaryRect.left + pickupX;
              var maxX = boundaryRect.right - (previewRect.width - pickupX);
              x = clamp(x, minX, maxX);
              y = clamp(y, minY, maxY);
            }

            return {
              x: x,
              y: y
            };
          }
          /** Updates the current drag delta, based on the user's current pointer position on the page. */

        }, {
          key: "_updatePointerDirectionDelta",
          value: function _updatePointerDirectionDelta(pointerPositionOnPage) {
            var x = pointerPositionOnPage.x,
                y = pointerPositionOnPage.y;
            var delta = this._pointerDirectionDelta;
            var positionSinceLastChange = this._pointerPositionAtLastDirectionChange; // Amount of pixels the user has dragged since the last time the direction changed.

            var changeX = Math.abs(x - positionSinceLastChange.x);
            var changeY = Math.abs(y - positionSinceLastChange.y); // Because we handle pointer events on a per-pixel basis, we don't want the delta
            // to change for every pixel, otherwise anything that depends on it can look erratic.
            // To make the delta more consistent, we track how much the user has moved since the last
            // delta change and we only update it after it has reached a certain threshold.

            if (changeX > this._config.pointerDirectionChangeThreshold) {
              delta.x = x > positionSinceLastChange.x ? 1 : -1;
              positionSinceLastChange.x = x;
            }

            if (changeY > this._config.pointerDirectionChangeThreshold) {
              delta.y = y > positionSinceLastChange.y ? 1 : -1;
              positionSinceLastChange.y = y;
            }

            return delta;
          }
          /** Toggles the native drag interactions, based on how many handles are registered. */

        }, {
          key: "_toggleNativeDragInteractions",
          value: function _toggleNativeDragInteractions() {
            if (!this._rootElement || !this._handles) {
              return;
            }

            var shouldEnable = this._handles.length > 0 || !this.isDragging();

            if (shouldEnable !== this._nativeInteractionsEnabled) {
              this._nativeInteractionsEnabled = shouldEnable;
              toggleNativeDragInteractions(this._rootElement, shouldEnable);
            }
          }
          /** Removes the manually-added event listeners from the root element. */

        }, {
          key: "_removeRootElementListeners",
          value: function _removeRootElementListeners(element) {
            element.removeEventListener('mousedown', this._pointerDown, activeEventListenerOptions);
            element.removeEventListener('touchstart', this._pointerDown, passiveEventListenerOptions);
          }
          /**
           * Applies a `transform` to the root element, taking into account any existing transforms on it.
           * @param x New transform value along the X axis.
           * @param y New transform value along the Y axis.
           */

        }, {
          key: "_applyRootElementTransform",
          value: function _applyRootElementTransform(x, y) {
            var transform = getTransform(x, y); // Cache the previous transform amount only after the first drag sequence, because
            // we don't want our own transforms to stack on top of each other.

            if (this._initialTransform == null) {
              this._initialTransform = this._rootElement.style.transform || '';
            } // Preserve the previous `transform` value, if there was one. Note that we apply our own
            // transform before the user's, because things like rotation can affect which direction
            // the element will be translated towards.


            this._rootElement.style.transform = this._initialTransform ? transform + ' ' + this._initialTransform : transform;
          }
          /**
           * Gets the distance that the user has dragged during the current drag sequence.
           * @param currentPosition Current position of the user's pointer.
           */

        }, {
          key: "_getDragDistance",
          value: function _getDragDistance(currentPosition) {
            var pickupPosition = this._pickupPositionOnPage;

            if (pickupPosition) {
              return {
                x: currentPosition.x - pickupPosition.x,
                y: currentPosition.y - pickupPosition.y
              };
            }

            return {
              x: 0,
              y: 0
            };
          }
          /** Cleans up any cached element dimensions that we don't need after dragging has stopped. */

        }, {
          key: "_cleanupCachedDimensions",
          value: function _cleanupCachedDimensions() {
            this._boundaryRect = this._previewRect = undefined;

            this._parentPositions.clear();
          }
          /**
           * Checks whether the element is still inside its boundary after the viewport has been resized.
           * If not, the position is adjusted so that the element fits again.
           */

        }, {
          key: "_containInsideBoundaryOnResize",
          value: function _containInsideBoundaryOnResize() {
            var _this$_passiveTransfo = this._passiveTransform,
                x = _this$_passiveTransfo.x,
                y = _this$_passiveTransfo.y;

            if (x === 0 && y === 0 || this.isDragging() || !this._boundaryElement) {
              return;
            }

            var boundaryRect = this._boundaryElement.getBoundingClientRect();

            var elementRect = this._rootElement.getBoundingClientRect(); // It's possible that the element got hidden away after dragging (e.g. by switching to a
            // different tab). Don't do anything in this case so we don't clear the user's position.


            if (boundaryRect.width === 0 && boundaryRect.height === 0 || elementRect.width === 0 && elementRect.height === 0) {
              return;
            }

            var leftOverflow = boundaryRect.left - elementRect.left;
            var rightOverflow = elementRect.right - boundaryRect.right;
            var topOverflow = boundaryRect.top - elementRect.top;
            var bottomOverflow = elementRect.bottom - boundaryRect.bottom; // If the element has become wider than the boundary, we can't
            // do much to make it fit so we just anchor it to the left.

            if (boundaryRect.width > elementRect.width) {
              if (leftOverflow > 0) {
                x += leftOverflow;
              }

              if (rightOverflow > 0) {
                x -= rightOverflow;
              }
            } else {
              x = 0;
            } // If the element has become taller than the boundary, we can't
            // do much to make it fit so we just anchor it to the top.


            if (boundaryRect.height > elementRect.height) {
              if (topOverflow > 0) {
                y += topOverflow;
              }

              if (bottomOverflow > 0) {
                y -= bottomOverflow;
              }
            } else {
              y = 0;
            }

            if (x !== this._passiveTransform.x || y !== this._passiveTransform.y) {
              this.setFreeDragPosition({
                y: y,
                x: x
              });
            }
          }
          /** Gets the drag start delay, based on the event type. */

        }, {
          key: "_getDragStartDelay",
          value: function _getDragStartDelay(event) {
            var value = this.dragStartDelay;

            if (typeof value === 'number') {
              return value;
            } else if (isTouchEvent(event)) {
              return value.touch;
            }

            return value ? value.mouse : 0;
          }
          /** Updates the internal state of the draggable element when scrolling has occurred. */

        }, {
          key: "_updateOnScroll",
          value: function _updateOnScroll(event) {
            var scrollDifference = this._parentPositions.handleScroll(event);

            if (scrollDifference) {
              var target = event.target; // ClientRect dimensions are based on the scroll position of the page and its parent node so
              // we have to update the cached boundary ClientRect if the user has scrolled. Check for
              // the `document` specifically since IE doesn't support `contains` on it.

              if (this._boundaryRect && (target === this._document || target !== this._boundaryElement && target.contains(this._boundaryElement))) {
                adjustClientRect(this._boundaryRect, scrollDifference.top, scrollDifference.left);
              }

              this._pickupPositionOnPage.x += scrollDifference.left;
              this._pickupPositionOnPage.y += scrollDifference.top; // If we're in free drag mode, we have to update the active transform, because
              // it isn't relative to the viewport like the preview inside a drop list.

              if (!this._dropContainer) {
                this._activeTransform.x -= scrollDifference.left;
                this._activeTransform.y -= scrollDifference.top;

                this._applyRootElementTransform(this._activeTransform.x, this._activeTransform.y);
              }
            }
          }
          /** Gets the scroll position of the viewport. */

        }, {
          key: "_getViewportScrollPosition",
          value: function _getViewportScrollPosition() {
            var cachedPosition = this._parentPositions.positions.get(this._document);

            return cachedPosition ? cachedPosition.scrollPosition : this._viewportRuler.getViewportScrollPosition();
          }
          /**
           * Lazily resolves and returns the shadow root of the element. We do this in a function, rather
           * than saving it in property directly on init, because we want to resolve it as late as possible
           * in order to ensure that the element has been moved into the shadow DOM. Doing it inside the
           * constructor might be too early if the element is inside of something like `ngFor` or `ngIf`.
           */

        }, {
          key: "_getShadowRoot",
          value: function _getShadowRoot() {
            if (this._cachedShadowRoot === undefined) {
              this._cachedShadowRoot = Object(_angular_cdk_platform__WEBPACK_IMPORTED_MODULE_3__["_getShadowRoot"])(this._rootElement);
            }

            return this._cachedShadowRoot;
          }
        }, {
          key: "disabled",
          get: function get() {
            return this._disabled || !!(this._dropContainer && this._dropContainer.disabled);
          },
          set: function set(value) {
            var newValue = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_4__["coerceBooleanProperty"])(value);

            if (newValue !== this._disabled) {
              this._disabled = newValue;

              this._toggleNativeDragInteractions();

              this._handles.forEach(function (handle) {
                return toggleNativeDragInteractions(handle, newValue);
              });
            }
          }
        }]);

        return DragRef;
      }();
      /**
       * Gets a 3d `transform` that can be applied to an element.
       * @param x Desired position of the element along the X axis.
       * @param y Desired position of the element along the Y axis.
       */


      function getTransform(x, y) {
        // Round the transforms since some browsers will
        // blur the elements for sub-pixel transforms.
        return "translate3d(".concat(Math.round(x), "px, ").concat(Math.round(y), "px, 0)");
      }
      /** Clamps a value between a minimum and a maximum. */


      function clamp(value, min, max) {
        return Math.max(min, Math.min(max, value));
      }
      /**
       * Helper to remove a node from the DOM and to do all the necessary null checks.
       * @param node Node to be removed.
       */


      function removeNode(node) {
        if (node && node.parentNode) {
          node.parentNode.removeChild(node);
        }
      }
      /** Determines whether an event is a touch event. */


      function isTouchEvent(event) {
        // This function is called for every pixel that the user has dragged so we need it to be
        // as fast as possible. Since we only bind mouse events and touch events, we can assume
        // that if the event's name starts with `t`, it's a touch event.
        return event.type[0] === 't';
      }
      /** Gets the element into which the drag preview should be inserted. */


      function getPreviewInsertionPoint(documentRef, shadowRoot) {
        // We can't use the body if the user is in fullscreen mode,
        // because the preview will render under the fullscreen element.
        // TODO(crisbeto): dedupe this with the `FullscreenOverlayContainer` eventually.
        return shadowRoot || documentRef.fullscreenElement || documentRef.webkitFullscreenElement || documentRef.mozFullScreenElement || documentRef.msFullscreenElement || documentRef.body;
      }
      /**
       * Gets the root HTML element of an embedded view.
       * If the root is not an HTML element it gets wrapped in one.
       */


      function getRootNode(viewRef, _document) {
        var rootNodes = viewRef.rootNodes;

        if (rootNodes.length === 1 && rootNodes[0].nodeType === _document.ELEMENT_NODE) {
          return rootNodes[0];
        }

        var wrapper = _document.createElement('div');

        rootNodes.forEach(function (node) {
          return wrapper.appendChild(node);
        });
        return wrapper;
      }
      /**
       * Matches the target element's size to the source's size.
       * @param target Element that needs to be resized.
       * @param sourceRect Dimensions of the source element.
       */


      function matchElementSize(target, sourceRect) {
        target.style.width = "".concat(sourceRect.width, "px");
        target.style.height = "".concat(sourceRect.height, "px");
        target.style.transform = getTransform(sourceRect.left, sourceRect.top);
      }
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * Moves an item one index in an array to another.
       * @param array Array in which to move the item.
       * @param fromIndex Starting index of the item.
       * @param toIndex Index to which the item should be moved.
       */


      function moveItemInArray(array, fromIndex, toIndex) {
        var from = clamp$1(fromIndex, array.length - 1);
        var to = clamp$1(toIndex, array.length - 1);

        if (from === to) {
          return;
        }

        var target = array[from];
        var delta = to < from ? -1 : 1;

        for (var i = from; i !== to; i += delta) {
          array[i] = array[i + delta];
        }

        array[to] = target;
      }
      /**
       * Moves an item from one array to another.
       * @param currentArray Array from which to transfer the item.
       * @param targetArray Array into which to put the item.
       * @param currentIndex Index of the item in its current array.
       * @param targetIndex Index at which to insert the item.
       */


      function transferArrayItem(currentArray, targetArray, currentIndex, targetIndex) {
        var from = clamp$1(currentIndex, currentArray.length - 1);
        var to = clamp$1(targetIndex, targetArray.length);

        if (currentArray.length) {
          targetArray.splice(to, 0, currentArray.splice(from, 1)[0]);
        }
      }
      /**
       * Copies an item from one array to another, leaving it in its
       * original position in current array.
       * @param currentArray Array from which to copy the item.
       * @param targetArray Array into which is copy the item.
       * @param currentIndex Index of the item in its current array.
       * @param targetIndex Index at which to insert the item.
       *
       */


      function copyArrayItem(currentArray, targetArray, currentIndex, targetIndex) {
        var to = clamp$1(targetIndex, targetArray.length);

        if (currentArray.length) {
          targetArray.splice(to, 0, currentArray[currentIndex]);
        }
      }
      /** Clamps a number between zero and a maximum. */


      function clamp$1(value, max) {
        return Math.max(0, Math.min(max, value));
      }
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * Proximity, as a ratio to width/height, at which a
       * dragged item will affect the drop container.
       */


      var DROP_PROXIMITY_THRESHOLD = 0.05;
      /**
       * Proximity, as a ratio to width/height at which to start auto-scrolling the drop list or the
       * viewport. The value comes from trying it out manually until it feels right.
       */

      var SCROLL_PROXIMITY_THRESHOLD = 0.05;
      /**
       * Number of pixels to scroll for each frame when auto-scrolling an element.
       * The value comes from trying it out manually until it feels right.
       */

      var AUTO_SCROLL_STEP = 2;
      /**
       * Reference to a drop list. Used to manipulate or dispose of the container.
       */

      var DropListRef = /*#__PURE__*/function () {
        function DropListRef(element, _dragDropRegistry, _document, _ngZone, _viewportRuler) {
          var _this34 = this;

          _classCallCheck(this, DropListRef);

          this._dragDropRegistry = _dragDropRegistry;
          this._ngZone = _ngZone;
          this._viewportRuler = _viewportRuler;
          /** Whether starting a dragging sequence from this container is disabled. */

          this.disabled = false;
          /** Whether sorting items within the list is disabled. */

          this.sortingDisabled = false;
          /**
           * Whether auto-scrolling the view when the user
           * moves their pointer close to the edges is disabled.
           */

          this.autoScrollDisabled = false;
          /**
           * Function that is used to determine whether an item
           * is allowed to be moved into a drop container.
           */

          this.enterPredicate = function () {
            return true;
          };
          /** Functions that is used to determine whether an item can be sorted into a particular index. */


          this.sortPredicate = function () {
            return true;
          };
          /** Emits right before dragging has started. */


          this.beforeStarted = new rxjs__WEBPACK_IMPORTED_MODULE_5__["Subject"]();
          /**
           * Emits when the user has moved a new drag item into this container.
           */

          this.entered = new rxjs__WEBPACK_IMPORTED_MODULE_5__["Subject"]();
          /**
           * Emits when the user removes an item from the container
           * by dragging it into another container.
           */

          this.exited = new rxjs__WEBPACK_IMPORTED_MODULE_5__["Subject"]();
          /** Emits when the user drops an item inside the container. */

          this.dropped = new rxjs__WEBPACK_IMPORTED_MODULE_5__["Subject"]();
          /** Emits as the user is swapping items while actively dragging. */

          this.sorted = new rxjs__WEBPACK_IMPORTED_MODULE_5__["Subject"]();
          /** Whether an item in the list is being dragged. */

          this._isDragging = false;
          /** Cache of the dimensions of all the items inside the container. */

          this._itemPositions = [];
          /**
           * Keeps track of the item that was last swapped with the dragged item, as well as what direction
           * the pointer was moving in when the swap occured and whether the user's pointer continued to
           * overlap with the swapped item after the swapping occurred.
           */

          this._previousSwap = {
            drag: null,
            delta: 0,
            overlaps: false
          };
          /** Draggable items in the container. */

          this._draggables = [];
          /** Drop lists that are connected to the current one. */

          this._siblings = [];
          /** Direction in which the list is oriented. */

          this._orientation = 'vertical';
          /** Connected siblings that currently have a dragged item. */

          this._activeSiblings = new Set();
          /** Layout direction of the drop list. */

          this._direction = 'ltr';
          /** Subscription to the window being scrolled. */

          this._viewportScrollSubscription = rxjs__WEBPACK_IMPORTED_MODULE_5__["Subscription"].EMPTY;
          /** Vertical direction in which the list is currently scrolling. */

          this._verticalScrollDirection = 0
          /* NONE */
          ;
          /** Horizontal direction in which the list is currently scrolling. */

          this._horizontalScrollDirection = 0
          /* NONE */
          ;
          /** Used to signal to the current auto-scroll sequence when to stop. */

          this._stopScrollTimers = new rxjs__WEBPACK_IMPORTED_MODULE_5__["Subject"]();
          /** Shadow root of the current element. Necessary for `elementFromPoint` to resolve correctly. */

          this._cachedShadowRoot = null;
          /** Starts the interval that'll auto-scroll the element. */

          this._startScrollInterval = function () {
            _this34._stopScrolling();

            Object(rxjs__WEBPACK_IMPORTED_MODULE_5__["interval"])(0, rxjs__WEBPACK_IMPORTED_MODULE_5__["animationFrameScheduler"]).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["takeUntil"])(_this34._stopScrollTimers)).subscribe(function () {
              var node = _this34._scrollNode;

              if (_this34._verticalScrollDirection === 1
              /* UP */
              ) {
                  incrementVerticalScroll(node, -AUTO_SCROLL_STEP);
                } else if (_this34._verticalScrollDirection === 2
              /* DOWN */
              ) {
                  incrementVerticalScroll(node, AUTO_SCROLL_STEP);
                }

              if (_this34._horizontalScrollDirection === 1
              /* LEFT */
              ) {
                  incrementHorizontalScroll(node, -AUTO_SCROLL_STEP);
                } else if (_this34._horizontalScrollDirection === 2
              /* RIGHT */
              ) {
                  incrementHorizontalScroll(node, AUTO_SCROLL_STEP);
                }
            });
          };

          this.element = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_4__["coerceElement"])(element);
          this._document = _document;
          this.withScrollableParents([this.element]);

          _dragDropRegistry.registerDropContainer(this);

          this._parentPositions = new ParentPositionTracker(_document, _viewportRuler);
        }
        /** Removes the drop list functionality from the DOM element. */


        _createClass(DropListRef, [{
          key: "dispose",
          value: function dispose() {
            this._stopScrolling();

            this._stopScrollTimers.complete();

            this._viewportScrollSubscription.unsubscribe();

            this.beforeStarted.complete();
            this.entered.complete();
            this.exited.complete();
            this.dropped.complete();
            this.sorted.complete();

            this._activeSiblings.clear();

            this._scrollNode = null;

            this._parentPositions.clear();

            this._dragDropRegistry.removeDropContainer(this);
          }
          /** Whether an item from this list is currently being dragged. */

        }, {
          key: "isDragging",
          value: function isDragging() {
            return this._isDragging;
          }
          /** Starts dragging an item. */

        }, {
          key: "start",
          value: function start() {
            this._draggingStarted();

            this._notifyReceivingSiblings();
          }
          /**
           * Emits an event to indicate that the user moved an item into the container.
           * @param item Item that was moved into the container.
           * @param pointerX Position of the item along the X axis.
           * @param pointerY Position of the item along the Y axis.
           * @param index Index at which the item entered. If omitted, the container will try to figure it
           *   out automatically.
           */

        }, {
          key: "enter",
          value: function enter(item, pointerX, pointerY, index) {
            this._draggingStarted(); // If sorting is disabled, we want the item to return to its starting
            // position if the user is returning it to its initial container.


            var newIndex;

            if (index == null) {
              newIndex = this.sortingDisabled ? this._draggables.indexOf(item) : -1;

              if (newIndex === -1) {
                // We use the coordinates of where the item entered the drop
                // zone to figure out at which index it should be inserted.
                newIndex = this._getItemIndexFromPointerPosition(item, pointerX, pointerY);
              }
            } else {
              newIndex = index;
            }

            var activeDraggables = this._activeDraggables;
            var currentIndex = activeDraggables.indexOf(item);
            var placeholder = item.getPlaceholderElement();
            var newPositionReference = activeDraggables[newIndex]; // If the item at the new position is the same as the item that is being dragged,
            // it means that we're trying to restore the item to its initial position. In this
            // case we should use the next item from the list as the reference.

            if (newPositionReference === item) {
              newPositionReference = activeDraggables[newIndex + 1];
            } // Since the item may be in the `activeDraggables` already (e.g. if the user dragged it
            // into another container and back again), we have to ensure that it isn't duplicated.


            if (currentIndex > -1) {
              activeDraggables.splice(currentIndex, 1);
            } // Don't use items that are being dragged as a reference, because
            // their element has been moved down to the bottom of the body.


            if (newPositionReference && !this._dragDropRegistry.isDragging(newPositionReference)) {
              var element = newPositionReference.getRootElement();
              element.parentElement.insertBefore(placeholder, element);
              activeDraggables.splice(newIndex, 0, item);
            } else if (this._shouldEnterAsFirstChild(pointerX, pointerY)) {
              var reference = activeDraggables[0].getRootElement();
              reference.parentNode.insertBefore(placeholder, reference);
              activeDraggables.unshift(item);
            } else {
              Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_4__["coerceElement"])(this.element).appendChild(placeholder);
              activeDraggables.push(item);
            } // The transform needs to be cleared so it doesn't throw off the measurements.


            placeholder.style.transform = ''; // Note that the positions were already cached when we called `start` above,
            // but we need to refresh them since the amount of items has changed and also parent rects.

            this._cacheItemPositions();

            this._cacheParentPositions(); // Notify siblings at the end so that the item has been inserted into the `activeDraggables`.


            this._notifyReceivingSiblings();

            this.entered.next({
              item: item,
              container: this,
              currentIndex: this.getItemIndex(item)
            });
          }
          /**
           * Removes an item from the container after it was dragged into another container by the user.
           * @param item Item that was dragged out.
           */

        }, {
          key: "exit",
          value: function exit(item) {
            this._reset();

            this.exited.next({
              item: item,
              container: this
            });
          }
          /**
           * Drops an item into this container.
           * @param item Item being dropped into the container.
           * @param currentIndex Index at which the item should be inserted.
           * @param previousIndex Index of the item when dragging started.
           * @param previousContainer Container from which the item got dragged in.
           * @param isPointerOverContainer Whether the user's pointer was over the
           *    container when the item was dropped.
           * @param distance Distance the user has dragged since the start of the dragging sequence.
           */

        }, {
          key: "drop",
          value: function drop(item, currentIndex, previousIndex, previousContainer, isPointerOverContainer, distance) {
            this._reset();

            this.dropped.next({
              item: item,
              currentIndex: currentIndex,
              previousIndex: previousIndex,
              container: this,
              previousContainer: previousContainer,
              isPointerOverContainer: isPointerOverContainer,
              distance: distance
            });
          }
          /**
           * Sets the draggable items that are a part of this list.
           * @param items Items that are a part of this list.
           */

        }, {
          key: "withItems",
          value: function withItems(items) {
            var _this35 = this;

            var previousItems = this._draggables;
            this._draggables = items;
            items.forEach(function (item) {
              return item._withDropContainer(_this35);
            });

            if (this.isDragging()) {
              var draggedItems = previousItems.filter(function (item) {
                return item.isDragging();
              }); // If all of the items being dragged were removed
              // from the list, abort the current drag sequence.

              if (draggedItems.every(function (item) {
                return items.indexOf(item) === -1;
              })) {
                this._reset();
              } else {
                this._cacheItems();
              }
            }

            return this;
          }
          /** Sets the layout direction of the drop list. */

        }, {
          key: "withDirection",
          value: function withDirection(direction) {
            this._direction = direction;
            return this;
          }
          /**
           * Sets the containers that are connected to this one. When two or more containers are
           * connected, the user will be allowed to transfer items between them.
           * @param connectedTo Other containers that the current containers should be connected to.
           */

        }, {
          key: "connectedTo",
          value: function connectedTo(_connectedTo) {
            this._siblings = _connectedTo.slice();
            return this;
          }
          /**
           * Sets the orientation of the container.
           * @param orientation New orientation for the container.
           */

        }, {
          key: "withOrientation",
          value: function withOrientation(orientation) {
            this._orientation = orientation;
            return this;
          }
          /**
           * Sets which parent elements are can be scrolled while the user is dragging.
           * @param elements Elements that can be scrolled.
           */

        }, {
          key: "withScrollableParents",
          value: function withScrollableParents(elements) {
            var element = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_4__["coerceElement"])(this.element); // We always allow the current element to be scrollable
            // so we need to ensure that it's in the array.

            this._scrollableElements = elements.indexOf(element) === -1 ? [element].concat(_toConsumableArray(elements)) : elements.slice();
            return this;
          }
          /** Gets the scrollable parents that are registered with this drop container. */

        }, {
          key: "getScrollableParents",
          value: function getScrollableParents() {
            return this._scrollableElements;
          }
          /**
           * Figures out the index of an item in the container.
           * @param item Item whose index should be determined.
           */

        }, {
          key: "getItemIndex",
          value: function getItemIndex(item) {
            if (!this._isDragging) {
              return this._draggables.indexOf(item);
            } // Items are sorted always by top/left in the cache, however they flow differently in RTL.
            // The rest of the logic still stands no matter what orientation we're in, however
            // we need to invert the array when determining the index.


            var items = this._orientation === 'horizontal' && this._direction === 'rtl' ? this._itemPositions.slice().reverse() : this._itemPositions;
            return findIndex(items, function (currentItem) {
              return currentItem.drag === item;
            });
          }
          /**
           * Whether the list is able to receive the item that
           * is currently being dragged inside a connected drop list.
           */

        }, {
          key: "isReceiving",
          value: function isReceiving() {
            return this._activeSiblings.size > 0;
          }
          /**
           * Sorts an item inside the container based on its position.
           * @param item Item to be sorted.
           * @param pointerX Position of the item along the X axis.
           * @param pointerY Position of the item along the Y axis.
           * @param pointerDelta Direction in which the pointer is moving along each axis.
           */

        }, {
          key: "_sortItem",
          value: function _sortItem(item, pointerX, pointerY, pointerDelta) {
            // Don't sort the item if sorting is disabled or it's out of range.
            if (this.sortingDisabled || !this._clientRect || !isPointerNearClientRect(this._clientRect, DROP_PROXIMITY_THRESHOLD, pointerX, pointerY)) {
              return;
            }

            var siblings = this._itemPositions;

            var newIndex = this._getItemIndexFromPointerPosition(item, pointerX, pointerY, pointerDelta);

            if (newIndex === -1 && siblings.length > 0) {
              return;
            }

            var isHorizontal = this._orientation === 'horizontal';
            var currentIndex = findIndex(siblings, function (currentItem) {
              return currentItem.drag === item;
            });
            var siblingAtNewPosition = siblings[newIndex];
            var currentPosition = siblings[currentIndex].clientRect;
            var newPosition = siblingAtNewPosition.clientRect;
            var delta = currentIndex > newIndex ? 1 : -1; // How many pixels the item's placeholder should be offset.

            var itemOffset = this._getItemOffsetPx(currentPosition, newPosition, delta); // How many pixels all the other items should be offset.


            var siblingOffset = this._getSiblingOffsetPx(currentIndex, siblings, delta); // Save the previous order of the items before moving the item to its new index.
            // We use this to check whether an item has been moved as a result of the sorting.


            var oldOrder = siblings.slice(); // Shuffle the array in place.

            moveItemInArray(siblings, currentIndex, newIndex);
            this.sorted.next({
              previousIndex: currentIndex,
              currentIndex: newIndex,
              container: this,
              item: item
            });
            siblings.forEach(function (sibling, index) {
              // Don't do anything if the position hasn't changed.
              if (oldOrder[index] === sibling) {
                return;
              }

              var isDraggedItem = sibling.drag === item;
              var offset = isDraggedItem ? itemOffset : siblingOffset;
              var elementToOffset = isDraggedItem ? item.getPlaceholderElement() : sibling.drag.getRootElement(); // Update the offset to reflect the new position.

              sibling.offset += offset; // Since we're moving the items with a `transform`, we need to adjust their cached
              // client rects to reflect their new position, as well as swap their positions in the cache.
              // Note that we shouldn't use `getBoundingClientRect` here to update the cache, because the
              // elements may be mid-animation which will give us a wrong result.

              if (isHorizontal) {
                // Round the transforms since some browsers will
                // blur the elements, for sub-pixel transforms.
                elementToOffset.style.transform = "translate3d(".concat(Math.round(sibling.offset), "px, 0, 0)");
                adjustClientRect(sibling.clientRect, 0, offset);
              } else {
                elementToOffset.style.transform = "translate3d(0, ".concat(Math.round(sibling.offset), "px, 0)");
                adjustClientRect(sibling.clientRect, offset, 0);
              }
            }); // Note that it's important that we do this after the client rects have been adjusted.

            this._previousSwap.overlaps = isInsideClientRect(newPosition, pointerX, pointerY);
            this._previousSwap.drag = siblingAtNewPosition.drag;
            this._previousSwap.delta = isHorizontal ? pointerDelta.x : pointerDelta.y;
          }
          /**
           * Checks whether the user's pointer is close to the edges of either the
           * viewport or the drop list and starts the auto-scroll sequence.
           * @param pointerX User's pointer position along the x axis.
           * @param pointerY User's pointer position along the y axis.
           */

        }, {
          key: "_startScrollingIfNecessary",
          value: function _startScrollingIfNecessary(pointerX, pointerY) {
            var _this36 = this;

            if (this.autoScrollDisabled) {
              return;
            }

            var scrollNode;
            var verticalScrollDirection = 0
            /* NONE */
            ;
            var horizontalScrollDirection = 0
            /* NONE */
            ; // Check whether we should start scrolling any of the parent containers.

            this._parentPositions.positions.forEach(function (position, element) {
              // We have special handling for the `document` below. Also this would be
              // nicer with a  for...of loop, but it requires changing a compiler flag.
              if (element === _this36._document || !position.clientRect || scrollNode) {
                return;
              }

              if (isPointerNearClientRect(position.clientRect, DROP_PROXIMITY_THRESHOLD, pointerX, pointerY)) {
                var _getElementScrollDire = getElementScrollDirections(element, position.clientRect, pointerX, pointerY);

                var _getElementScrollDire2 = _slicedToArray(_getElementScrollDire, 2);

                verticalScrollDirection = _getElementScrollDire2[0];
                horizontalScrollDirection = _getElementScrollDire2[1];

                if (verticalScrollDirection || horizontalScrollDirection) {
                  scrollNode = element;
                }
              }
            }); // Otherwise check if we can start scrolling the viewport.


            if (!verticalScrollDirection && !horizontalScrollDirection) {
              var _this$_viewportRuler$ = this._viewportRuler.getViewportSize(),
                  width = _this$_viewportRuler$.width,
                  height = _this$_viewportRuler$.height;

              var clientRect = {
                width: width,
                height: height,
                top: 0,
                right: width,
                bottom: height,
                left: 0
              };
              verticalScrollDirection = getVerticalScrollDirection(clientRect, pointerY);
              horizontalScrollDirection = getHorizontalScrollDirection(clientRect, pointerX);
              scrollNode = window;
            }

            if (scrollNode && (verticalScrollDirection !== this._verticalScrollDirection || horizontalScrollDirection !== this._horizontalScrollDirection || scrollNode !== this._scrollNode)) {
              this._verticalScrollDirection = verticalScrollDirection;
              this._horizontalScrollDirection = horizontalScrollDirection;
              this._scrollNode = scrollNode;

              if ((verticalScrollDirection || horizontalScrollDirection) && scrollNode) {
                this._ngZone.runOutsideAngular(this._startScrollInterval);
              } else {
                this._stopScrolling();
              }
            }
          }
          /** Stops any currently-running auto-scroll sequences. */

        }, {
          key: "_stopScrolling",
          value: function _stopScrolling() {
            this._stopScrollTimers.next();
          }
          /** Starts the dragging sequence within the list. */

        }, {
          key: "_draggingStarted",
          value: function _draggingStarted() {
            var styles = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_4__["coerceElement"])(this.element).style;
            this.beforeStarted.next();
            this._isDragging = true; // We need to disable scroll snapping while the user is dragging, because it breaks automatic
            // scrolling. The browser seems to round the value based on the snapping points which means
            // that we can't increment/decrement the scroll position.

            this._initialScrollSnap = styles.msScrollSnapType || styles.scrollSnapType || '';
            styles.scrollSnapType = styles.msScrollSnapType = 'none';

            this._cacheItems();

            this._viewportScrollSubscription.unsubscribe();

            this._listenToScrollEvents();
          }
          /** Caches the positions of the configured scrollable parents. */

        }, {
          key: "_cacheParentPositions",
          value: function _cacheParentPositions() {
            var element = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_4__["coerceElement"])(this.element);

            this._parentPositions.cache(this._scrollableElements); // The list element is always in the `scrollableElements`
            // so we can take advantage of the cached `ClientRect`.


            this._clientRect = this._parentPositions.positions.get(element).clientRect;
          }
          /** Refreshes the position cache of the items and sibling containers. */

        }, {
          key: "_cacheItemPositions",
          value: function _cacheItemPositions() {
            var isHorizontal = this._orientation === 'horizontal';
            this._itemPositions = this._activeDraggables.map(function (drag) {
              var elementToMeasure = drag.getVisibleElement();
              return {
                drag: drag,
                offset: 0,
                clientRect: getMutableClientRect(elementToMeasure)
              };
            }).sort(function (a, b) {
              return isHorizontal ? a.clientRect.left - b.clientRect.left : a.clientRect.top - b.clientRect.top;
            });
          }
          /** Resets the container to its initial state. */

        }, {
          key: "_reset",
          value: function _reset() {
            var _this37 = this;

            this._isDragging = false;
            var styles = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_4__["coerceElement"])(this.element).style;
            styles.scrollSnapType = styles.msScrollSnapType = this._initialScrollSnap; // TODO(crisbeto): may have to wait for the animations to finish.

            this._activeDraggables.forEach(function (item) {
              var rootElement = item.getRootElement();

              if (rootElement) {
                rootElement.style.transform = '';
              }
            });

            this._siblings.forEach(function (sibling) {
              return sibling._stopReceiving(_this37);
            });

            this._activeDraggables = [];
            this._itemPositions = [];
            this._previousSwap.drag = null;
            this._previousSwap.delta = 0;
            this._previousSwap.overlaps = false;

            this._stopScrolling();

            this._viewportScrollSubscription.unsubscribe();

            this._parentPositions.clear();
          }
          /**
           * Gets the offset in pixels by which the items that aren't being dragged should be moved.
           * @param currentIndex Index of the item currently being dragged.
           * @param siblings All of the items in the list.
           * @param delta Direction in which the user is moving.
           */

        }, {
          key: "_getSiblingOffsetPx",
          value: function _getSiblingOffsetPx(currentIndex, siblings, delta) {
            var isHorizontal = this._orientation === 'horizontal';
            var currentPosition = siblings[currentIndex].clientRect;
            var immediateSibling = siblings[currentIndex + delta * -1];
            var siblingOffset = currentPosition[isHorizontal ? 'width' : 'height'] * delta;

            if (immediateSibling) {
              var start = isHorizontal ? 'left' : 'top';
              var end = isHorizontal ? 'right' : 'bottom'; // Get the spacing between the start of the current item and the end of the one immediately
              // after it in the direction in which the user is dragging, or vice versa. We add it to the
              // offset in order to push the element to where it will be when it's inline and is influenced
              // by the `margin` of its siblings.

              if (delta === -1) {
                siblingOffset -= immediateSibling.clientRect[start] - currentPosition[end];
              } else {
                siblingOffset += currentPosition[start] - immediateSibling.clientRect[end];
              }
            }

            return siblingOffset;
          }
          /**
           * Gets the offset in pixels by which the item that is being dragged should be moved.
           * @param currentPosition Current position of the item.
           * @param newPosition Position of the item where the current item should be moved.
           * @param delta Direction in which the user is moving.
           */

        }, {
          key: "_getItemOffsetPx",
          value: function _getItemOffsetPx(currentPosition, newPosition, delta) {
            var isHorizontal = this._orientation === 'horizontal';
            var itemOffset = isHorizontal ? newPosition.left - currentPosition.left : newPosition.top - currentPosition.top; // Account for differences in the item width/height.

            if (delta === -1) {
              itemOffset += isHorizontal ? newPosition.width - currentPosition.width : newPosition.height - currentPosition.height;
            }

            return itemOffset;
          }
          /**
           * Checks if pointer is entering in the first position
           * @param pointerX Position of the user's pointer along the X axis.
           * @param pointerY Position of the user's pointer along the Y axis.
           */

        }, {
          key: "_shouldEnterAsFirstChild",
          value: function _shouldEnterAsFirstChild(pointerX, pointerY) {
            if (!this._activeDraggables.length) {
              return false;
            }

            var itemPositions = this._itemPositions;
            var isHorizontal = this._orientation === 'horizontal'; // `itemPositions` are sorted by position while `activeDraggables` are sorted by child index
            // check if container is using some sort of "reverse" ordering (eg: flex-direction: row-reverse)

            var reversed = itemPositions[0].drag !== this._activeDraggables[0];

            if (reversed) {
              var lastItemRect = itemPositions[itemPositions.length - 1].clientRect;
              return isHorizontal ? pointerX >= lastItemRect.right : pointerY >= lastItemRect.bottom;
            } else {
              var firstItemRect = itemPositions[0].clientRect;
              return isHorizontal ? pointerX <= firstItemRect.left : pointerY <= firstItemRect.top;
            }
          }
          /**
           * Gets the index of an item in the drop container, based on the position of the user's pointer.
           * @param item Item that is being sorted.
           * @param pointerX Position of the user's pointer along the X axis.
           * @param pointerY Position of the user's pointer along the Y axis.
           * @param delta Direction in which the user is moving their pointer.
           */

        }, {
          key: "_getItemIndexFromPointerPosition",
          value: function _getItemIndexFromPointerPosition(item, pointerX, pointerY, delta) {
            var _this38 = this;

            var isHorizontal = this._orientation === 'horizontal';
            var index = findIndex(this._itemPositions, function (_ref14, _, array) {
              var drag = _ref14.drag,
                  clientRect = _ref14.clientRect;

              if (drag === item) {
                // If there's only one item left in the container, it must be
                // the dragged item itself so we use it as a reference.
                return array.length < 2;
              }

              if (delta) {
                var direction = isHorizontal ? delta.x : delta.y; // If the user is still hovering over the same item as last time, their cursor hasn't left
                // the item after we made the swap, and they didn't change the direction in which they're
                // dragging, we don't consider it a direction swap.

                if (drag === _this38._previousSwap.drag && _this38._previousSwap.overlaps && direction === _this38._previousSwap.delta) {
                  return false;
                }
              }

              return isHorizontal ? // Round these down since most browsers report client rects with
              // sub-pixel precision, whereas the pointer coordinates are rounded to pixels.
              pointerX >= Math.floor(clientRect.left) && pointerX < Math.floor(clientRect.right) : pointerY >= Math.floor(clientRect.top) && pointerY < Math.floor(clientRect.bottom);
            });
            return index === -1 || !this.sortPredicate(index, item, this) ? -1 : index;
          }
          /** Caches the current items in the list and their positions. */

        }, {
          key: "_cacheItems",
          value: function _cacheItems() {
            this._activeDraggables = this._draggables.slice();

            this._cacheItemPositions();

            this._cacheParentPositions();
          }
          /**
           * Checks whether the user's pointer is positioned over the container.
           * @param x Pointer position along the X axis.
           * @param y Pointer position along the Y axis.
           */

        }, {
          key: "_isOverContainer",
          value: function _isOverContainer(x, y) {
            return this._clientRect != null && isInsideClientRect(this._clientRect, x, y);
          }
          /**
           * Figures out whether an item should be moved into a sibling
           * drop container, based on its current position.
           * @param item Drag item that is being moved.
           * @param x Position of the item along the X axis.
           * @param y Position of the item along the Y axis.
           */

        }, {
          key: "_getSiblingContainerFromPosition",
          value: function _getSiblingContainerFromPosition(item, x, y) {
            return this._siblings.find(function (sibling) {
              return sibling._canReceive(item, x, y);
            });
          }
          /**
           * Checks whether the drop list can receive the passed-in item.
           * @param item Item that is being dragged into the list.
           * @param x Position of the item along the X axis.
           * @param y Position of the item along the Y axis.
           */

        }, {
          key: "_canReceive",
          value: function _canReceive(item, x, y) {
            if (!this._clientRect || !isInsideClientRect(this._clientRect, x, y) || !this.enterPredicate(item, this)) {
              return false;
            }

            var elementFromPoint = this._getShadowRoot().elementFromPoint(x, y); // If there's no element at the pointer position, then
            // the client rect is probably scrolled out of the view.


            if (!elementFromPoint) {
              return false;
            }

            var nativeElement = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_4__["coerceElement"])(this.element); // The `ClientRect`, that we're using to find the container over which the user is
            // hovering, doesn't give us any information on whether the element has been scrolled
            // out of the view or whether it's overlapping with other containers. This means that
            // we could end up transferring the item into a container that's invisible or is positioned
            // below another one. We use the result from `elementFromPoint` to get the top-most element
            // at the pointer position and to find whether it's one of the intersecting drop containers.

            return elementFromPoint === nativeElement || nativeElement.contains(elementFromPoint);
          }
          /**
           * Called by one of the connected drop lists when a dragging sequence has started.
           * @param sibling Sibling in which dragging has started.
           */

        }, {
          key: "_startReceiving",
          value: function _startReceiving(sibling, items) {
            var _this39 = this;

            var activeSiblings = this._activeSiblings;

            if (!activeSiblings.has(sibling) && items.every(function (item) {
              // Note that we have to add an exception to the `enterPredicate` for items that started off
              // in this drop list. The drag ref has logic that allows an item to return to its initial
              // container, if it has left the initial container and none of the connected containers
              // allow it to enter. See `DragRef._updateActiveDropContainer` for more context.
              return _this39.enterPredicate(item, _this39) || _this39._draggables.indexOf(item) > -1;
            })) {
              activeSiblings.add(sibling);

              this._cacheParentPositions();

              this._listenToScrollEvents();
            }
          }
          /**
           * Called by a connected drop list when dragging has stopped.
           * @param sibling Sibling whose dragging has stopped.
           */

        }, {
          key: "_stopReceiving",
          value: function _stopReceiving(sibling) {
            this._activeSiblings["delete"](sibling);

            this._viewportScrollSubscription.unsubscribe();
          }
          /**
           * Starts listening to scroll events on the viewport.
           * Used for updating the internal state of the list.
           */

        }, {
          key: "_listenToScrollEvents",
          value: function _listenToScrollEvents() {
            var _this40 = this;

            this._viewportScrollSubscription = this._dragDropRegistry.scroll.subscribe(function (event) {
              if (_this40.isDragging()) {
                var scrollDifference = _this40._parentPositions.handleScroll(event);

                if (scrollDifference) {
                  // Since we know the amount that the user has scrolled we can shift all of the
                  // client rectangles ourselves. This is cheaper than re-measuring everything and
                  // we can avoid inconsistent behavior where we might be measuring the element before
                  // its position has changed.
                  _this40._itemPositions.forEach(function (_ref15) {
                    var clientRect = _ref15.clientRect;
                    adjustClientRect(clientRect, scrollDifference.top, scrollDifference.left);
                  }); // We need two loops for this, because we want all of the cached
                  // positions to be up-to-date before we re-sort the item.


                  _this40._itemPositions.forEach(function (_ref16) {
                    var drag = _ref16.drag;

                    if (_this40._dragDropRegistry.isDragging(drag)) {
                      // We need to re-sort the item manually, because the pointer move
                      // events won't be dispatched while the user is scrolling.
                      drag._sortFromLastPointerPosition();
                    }
                  });
                }
              } else if (_this40.isReceiving()) {
                _this40._cacheParentPositions();
              }
            });
          }
          /**
           * Lazily resolves and returns the shadow root of the element. We do this in a function, rather
           * than saving it in property directly on init, because we want to resolve it as late as possible
           * in order to ensure that the element has been moved into the shadow DOM. Doing it inside the
           * constructor might be too early if the element is inside of something like `ngFor` or `ngIf`.
           */

        }, {
          key: "_getShadowRoot",
          value: function _getShadowRoot() {
            if (!this._cachedShadowRoot) {
              var shadowRoot = Object(_angular_cdk_platform__WEBPACK_IMPORTED_MODULE_3__["_getShadowRoot"])(Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_4__["coerceElement"])(this.element));
              this._cachedShadowRoot = shadowRoot || this._document;
            }

            return this._cachedShadowRoot;
          }
          /** Notifies any siblings that may potentially receive the item. */

        }, {
          key: "_notifyReceivingSiblings",
          value: function _notifyReceivingSiblings() {
            var _this41 = this;

            var draggedItems = this._activeDraggables.filter(function (item) {
              return item.isDragging();
            });

            this._siblings.forEach(function (sibling) {
              return sibling._startReceiving(_this41, draggedItems);
            });
          }
        }]);

        return DropListRef;
      }();
      /**
       * Finds the index of an item that matches a predicate function. Used as an equivalent
       * of `Array.prototype.findIndex` which isn't part of the standard Google typings.
       * @param array Array in which to look for matches.
       * @param predicate Function used to determine whether an item is a match.
       */


      function findIndex(array, predicate) {
        for (var i = 0; i < array.length; i++) {
          if (predicate(array[i], i, array)) {
            return i;
          }
        }

        return -1;
      }
      /**
       * Increments the vertical scroll position of a node.
       * @param node Node whose scroll position should change.
       * @param amount Amount of pixels that the `node` should be scrolled.
       */


      function incrementVerticalScroll(node, amount) {
        if (node === window) {
          node.scrollBy(0, amount);
        } else {
          // Ideally we could use `Element.scrollBy` here as well, but IE and Edge don't support it.
          node.scrollTop += amount;
        }
      }
      /**
       * Increments the horizontal scroll position of a node.
       * @param node Node whose scroll position should change.
       * @param amount Amount of pixels that the `node` should be scrolled.
       */


      function incrementHorizontalScroll(node, amount) {
        if (node === window) {
          node.scrollBy(amount, 0);
        } else {
          // Ideally we could use `Element.scrollBy` here as well, but IE and Edge don't support it.
          node.scrollLeft += amount;
        }
      }
      /**
       * Gets whether the vertical auto-scroll direction of a node.
       * @param clientRect Dimensions of the node.
       * @param pointerY Position of the user's pointer along the y axis.
       */


      function getVerticalScrollDirection(clientRect, pointerY) {
        var top = clientRect.top,
            bottom = clientRect.bottom,
            height = clientRect.height;
        var yThreshold = height * SCROLL_PROXIMITY_THRESHOLD;

        if (pointerY >= top - yThreshold && pointerY <= top + yThreshold) {
          return 1
          /* UP */
          ;
        } else if (pointerY >= bottom - yThreshold && pointerY <= bottom + yThreshold) {
          return 2
          /* DOWN */
          ;
        }

        return 0
        /* NONE */
        ;
      }
      /**
       * Gets whether the horizontal auto-scroll direction of a node.
       * @param clientRect Dimensions of the node.
       * @param pointerX Position of the user's pointer along the x axis.
       */


      function getHorizontalScrollDirection(clientRect, pointerX) {
        var left = clientRect.left,
            right = clientRect.right,
            width = clientRect.width;
        var xThreshold = width * SCROLL_PROXIMITY_THRESHOLD;

        if (pointerX >= left - xThreshold && pointerX <= left + xThreshold) {
          return 1
          /* LEFT */
          ;
        } else if (pointerX >= right - xThreshold && pointerX <= right + xThreshold) {
          return 2
          /* RIGHT */
          ;
        }

        return 0
        /* NONE */
        ;
      }
      /**
       * Gets the directions in which an element node should be scrolled,
       * assuming that the user's pointer is already within it scrollable region.
       * @param element Element for which we should calculate the scroll direction.
       * @param clientRect Bounding client rectangle of the element.
       * @param pointerX Position of the user's pointer along the x axis.
       * @param pointerY Position of the user's pointer along the y axis.
       */


      function getElementScrollDirections(element, clientRect, pointerX, pointerY) {
        var computedVertical = getVerticalScrollDirection(clientRect, pointerY);
        var computedHorizontal = getHorizontalScrollDirection(clientRect, pointerX);
        var verticalScrollDirection = 0
        /* NONE */
        ;
        var horizontalScrollDirection = 0
        /* NONE */
        ; // Note that we here we do some extra checks for whether the element is actually scrollable in
        // a certain direction and we only assign the scroll direction if it is. We do this so that we
        // can allow other elements to be scrolled, if the current element can't be scrolled anymore.
        // This allows us to handle cases where the scroll regions of two scrollable elements overlap.

        if (computedVertical) {
          var scrollTop = element.scrollTop;

          if (computedVertical === 1
          /* UP */
          ) {
              if (scrollTop > 0) {
                verticalScrollDirection = 1
                /* UP */
                ;
              }
            } else if (element.scrollHeight - scrollTop > element.clientHeight) {
            verticalScrollDirection = 2
            /* DOWN */
            ;
          }
        }

        if (computedHorizontal) {
          var scrollLeft = element.scrollLeft;

          if (computedHorizontal === 1
          /* LEFT */
          ) {
              if (scrollLeft > 0) {
                horizontalScrollDirection = 1
                /* LEFT */
                ;
              }
            } else if (element.scrollWidth - scrollLeft > element.clientWidth) {
            horizontalScrollDirection = 2
            /* RIGHT */
            ;
          }
        }

        return [verticalScrollDirection, horizontalScrollDirection];
      }
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /** Event options that can be used to bind an active, capturing event. */


      var activeCapturingEventOptions = Object(_angular_cdk_platform__WEBPACK_IMPORTED_MODULE_3__["normalizePassiveListenerOptions"])({
        passive: false,
        capture: true
      });
      /**
       * Service that keeps track of all the drag item and drop container
       * instances, and manages global event listeners on the `document`.
       * @docs-private
       */
      // Note: this class is generic, rather than referencing CdkDrag and CdkDropList directly, in order
      // to avoid circular imports. If we were to reference them here, importing the registry into the
      // classes that are registering themselves will introduce a circular import.

      var DragDropRegistry = /*#__PURE__*/function () {
        function DragDropRegistry(_ngZone, _document) {
          var _this42 = this;

          _classCallCheck(this, DragDropRegistry);

          this._ngZone = _ngZone;
          /** Registered drop container instances. */

          this._dropInstances = new Set();
          /** Registered drag item instances. */

          this._dragInstances = new Set();
          /** Drag item instances that are currently being dragged. */

          this._activeDragInstances = [];
          /** Keeps track of the event listeners that we've bound to the `document`. */

          this._globalListeners = new Map();
          /**
           * Predicate function to check if an item is being dragged.  Moved out into a property,
           * because it'll be called a lot and we don't want to create a new function every time.
           */

          this._draggingPredicate = function (item) {
            return item.isDragging();
          };
          /**
           * Emits the `touchmove` or `mousemove` events that are dispatched
           * while the user is dragging a drag item instance.
           */


          this.pointerMove = new rxjs__WEBPACK_IMPORTED_MODULE_5__["Subject"]();
          /**
           * Emits the `touchend` or `mouseup` events that are dispatched
           * while the user is dragging a drag item instance.
           */

          this.pointerUp = new rxjs__WEBPACK_IMPORTED_MODULE_5__["Subject"]();
          /** Emits when the viewport has been scrolled while the user is dragging an item. */

          this.scroll = new rxjs__WEBPACK_IMPORTED_MODULE_5__["Subject"]();
          /**
           * Event listener that will prevent the default browser action while the user is dragging.
           * @param event Event whose default action should be prevented.
           */

          this._preventDefaultWhileDragging = function (event) {
            if (_this42._activeDragInstances.length > 0) {
              event.preventDefault();
            }
          };
          /** Event listener for `touchmove` that is bound even if no dragging is happening. */


          this._persistentTouchmoveListener = function (event) {
            if (_this42._activeDragInstances.length > 0) {
              // Note that we only want to prevent the default action after dragging has actually started.
              // Usually this is the same time at which the item is added to the `_activeDragInstances`,
              // but it could be pushed back if the user has set up a drag delay or threshold.
              if (_this42._activeDragInstances.some(_this42._draggingPredicate)) {
                event.preventDefault();
              }

              _this42.pointerMove.next(event);
            }
          };

          this._document = _document;
        }
        /** Adds a drop container to the registry. */


        _createClass(DragDropRegistry, [{
          key: "registerDropContainer",
          value: function registerDropContainer(drop) {
            if (!this._dropInstances.has(drop)) {
              this._dropInstances.add(drop);
            }
          }
          /** Adds a drag item instance to the registry. */

        }, {
          key: "registerDragItem",
          value: function registerDragItem(drag) {
            var _this43 = this;

            this._dragInstances.add(drag); // The `touchmove` event gets bound once, ahead of time, because WebKit
            // won't preventDefault on a dynamically-added `touchmove` listener.
            // See https://bugs.webkit.org/show_bug.cgi?id=184250.


            if (this._dragInstances.size === 1) {
              this._ngZone.runOutsideAngular(function () {
                // The event handler has to be explicitly active,
                // because newer browsers make it passive by default.
                _this43._document.addEventListener('touchmove', _this43._persistentTouchmoveListener, activeCapturingEventOptions);
              });
            }
          }
          /** Removes a drop container from the registry. */

        }, {
          key: "removeDropContainer",
          value: function removeDropContainer(drop) {
            this._dropInstances["delete"](drop);
          }
          /** Removes a drag item instance from the registry. */

        }, {
          key: "removeDragItem",
          value: function removeDragItem(drag) {
            this._dragInstances["delete"](drag);

            this.stopDragging(drag);

            if (this._dragInstances.size === 0) {
              this._document.removeEventListener('touchmove', this._persistentTouchmoveListener, activeCapturingEventOptions);
            }
          }
          /**
           * Starts the dragging sequence for a drag instance.
           * @param drag Drag instance which is being dragged.
           * @param event Event that initiated the dragging.
           */

        }, {
          key: "startDragging",
          value: function startDragging(drag, event) {
            var _this44 = this;

            // Do not process the same drag twice to avoid memory leaks and redundant listeners
            if (this._activeDragInstances.indexOf(drag) > -1) {
              return;
            }

            this._activeDragInstances.push(drag);

            if (this._activeDragInstances.length === 1) {
              var _isTouchEvent = event.type.startsWith('touch'); // We explicitly bind __active__ listeners here, because newer browsers will default to
              // passive ones for `mousemove` and `touchmove`. The events need to be active, because we
              // use `preventDefault` to prevent the page from scrolling while the user is dragging.


              this._globalListeners.set(_isTouchEvent ? 'touchend' : 'mouseup', {
                handler: function handler(e) {
                  return _this44.pointerUp.next(e);
                },
                options: true
              }).set('scroll', {
                handler: function handler(e) {
                  return _this44.scroll.next(e);
                },
                // Use capturing so that we pick up scroll changes in any scrollable nodes that aren't
                // the document. See https://github.com/angular/components/issues/17144.
                options: true
              }) // Preventing the default action on `mousemove` isn't enough to disable text selection
              // on Safari so we need to prevent the selection event as well. Alternatively this can
              // be done by setting `user-select: none` on the `body`, however it has causes a style
              // recalculation which can be expensive on pages with a lot of elements.
              .set('selectstart', {
                handler: this._preventDefaultWhileDragging,
                options: activeCapturingEventOptions
              }); // We don't have to bind a move event for touch drag sequences, because
              // we already have a persistent global one bound from `registerDragItem`.


              if (!_isTouchEvent) {
                this._globalListeners.set('mousemove', {
                  handler: function handler(e) {
                    return _this44.pointerMove.next(e);
                  },
                  options: activeCapturingEventOptions
                });
              }

              this._ngZone.runOutsideAngular(function () {
                _this44._globalListeners.forEach(function (config, name) {
                  _this44._document.addEventListener(name, config.handler, config.options);
                });
              });
            }
          }
          /** Stops dragging a drag item instance. */

        }, {
          key: "stopDragging",
          value: function stopDragging(drag) {
            var index = this._activeDragInstances.indexOf(drag);

            if (index > -1) {
              this._activeDragInstances.splice(index, 1);

              if (this._activeDragInstances.length === 0) {
                this._clearGlobalListeners();
              }
            }
          }
          /** Gets whether a drag item instance is currently being dragged. */

        }, {
          key: "isDragging",
          value: function isDragging(drag) {
            return this._activeDragInstances.indexOf(drag) > -1;
          }
        }, {
          key: "ngOnDestroy",
          value: function ngOnDestroy() {
            var _this45 = this;

            this._dragInstances.forEach(function (instance) {
              return _this45.removeDragItem(instance);
            });

            this._dropInstances.forEach(function (instance) {
              return _this45.removeDropContainer(instance);
            });

            this._clearGlobalListeners();

            this.pointerMove.complete();
            this.pointerUp.complete();
          }
          /** Clears out the global event listeners from the `document`. */

        }, {
          key: "_clearGlobalListeners",
          value: function _clearGlobalListeners() {
            var _this46 = this;

            this._globalListeners.forEach(function (config, name) {
              _this46._document.removeEventListener(name, config.handler, config.options);
            });

            this._globalListeners.clear();
          }
        }]);

        return DragDropRegistry;
      }();

      DragDropRegistry.ɵprov = Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineInjectable"])({
        factory: function DragDropRegistry_Factory() {
          return new DragDropRegistry(Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵinject"])(_angular_core__WEBPACK_IMPORTED_MODULE_0__["NgZone"]), Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵinject"])(_angular_common__WEBPACK_IMPORTED_MODULE_1__["DOCUMENT"]));
        },
        token: DragDropRegistry,
        providedIn: "root"
      });
      DragDropRegistry.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"],
        args: [{
          providedIn: 'root'
        }]
      }];

      DragDropRegistry.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["NgZone"]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Inject"],
            args: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["DOCUMENT"]]
          }]
        }];
      };
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /** Default configuration to be used when creating a `DragRef`. */


      var DEFAULT_CONFIG = {
        dragStartThreshold: 5,
        pointerDirectionChangeThreshold: 5
      };
      /**
       * Service that allows for drag-and-drop functionality to be attached to DOM elements.
       */

      var DragDrop = /*#__PURE__*/function () {
        function DragDrop(_document, _ngZone, _viewportRuler, _dragDropRegistry) {
          _classCallCheck(this, DragDrop);

          this._document = _document;
          this._ngZone = _ngZone;
          this._viewportRuler = _viewportRuler;
          this._dragDropRegistry = _dragDropRegistry;
        }
        /**
         * Turns an element into a draggable item.
         * @param element Element to which to attach the dragging functionality.
         * @param config Object used to configure the dragging behavior.
         */


        _createClass(DragDrop, [{
          key: "createDrag",
          value: function createDrag(element) {
            var config = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : DEFAULT_CONFIG;
            return new DragRef(element, config, this._document, this._ngZone, this._viewportRuler, this._dragDropRegistry);
          }
          /**
           * Turns an element into a drop list.
           * @param element Element to which to attach the drop list functionality.
           */

        }, {
          key: "createDropList",
          value: function createDropList(element) {
            return new DropListRef(element, this._dragDropRegistry, this._document, this._ngZone, this._viewportRuler);
          }
        }]);

        return DragDrop;
      }();

      DragDrop.ɵprov = Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineInjectable"])({
        factory: function DragDrop_Factory() {
          return new DragDrop(Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵinject"])(_angular_common__WEBPACK_IMPORTED_MODULE_1__["DOCUMENT"]), Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵinject"])(_angular_core__WEBPACK_IMPORTED_MODULE_0__["NgZone"]), Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵinject"])(_angular_cdk_scrolling__WEBPACK_IMPORTED_MODULE_2__["ViewportRuler"]), Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵinject"])(DragDropRegistry));
        },
        token: DragDrop,
        providedIn: "root"
      });
      DragDrop.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"],
        args: [{
          providedIn: 'root'
        }]
      }];

      DragDrop.ctorParameters = function () {
        return [{
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Inject"],
            args: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["DOCUMENT"]]
          }]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["NgZone"]
        }, {
          type: _angular_cdk_scrolling__WEBPACK_IMPORTED_MODULE_2__["ViewportRuler"]
        }, {
          type: DragDropRegistry
        }];
      };
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * Injection token that can be used for a `CdkDrag` to provide itself as a parent to the
       * drag-specific child directive (`CdkDragHandle`, `CdkDragPreview` etc.). Used primarily
       * to avoid circular imports.
       * @docs-private
       */


      var CDK_DRAG_PARENT = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["InjectionToken"]('CDK_DRAG_PARENT');
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * Injection token that can be used to reference instances of `CdkDropListGroup`. It serves as
       * alternative token to the actual `CdkDropListGroup` class which could cause unnecessary
       * retention of the class and its directive metadata.
       */

      var CDK_DROP_LIST_GROUP = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["InjectionToken"]('CdkDropListGroup');
      /**
       * Declaratively connects sibling `cdkDropList` instances together. All of the `cdkDropList`
       * elements that are placed inside a `cdkDropListGroup` will be connected to each other
       * automatically. Can be used as an alternative to the `cdkDropListConnectedTo` input
       * from `cdkDropList`.
       */

      var CdkDropListGroup = /*#__PURE__*/function () {
        function CdkDropListGroup() {
          _classCallCheck(this, CdkDropListGroup);

          /** Drop lists registered inside the group. */
          this._items = new Set();
          this._disabled = false;
        }
        /** Whether starting a dragging sequence from inside this group is disabled. */


        _createClass(CdkDropListGroup, [{
          key: "ngOnDestroy",
          value: function ngOnDestroy() {
            this._items.clear();
          }
        }, {
          key: "disabled",
          get: function get() {
            return this._disabled;
          },
          set: function set(value) {
            this._disabled = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_4__["coerceBooleanProperty"])(value);
          }
        }]);

        return CdkDropListGroup;
      }();

      CdkDropListGroup.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"],
        args: [{
          selector: '[cdkDropListGroup]',
          exportAs: 'cdkDropListGroup',
          providers: [{
            provide: CDK_DROP_LIST_GROUP,
            useExisting: CdkDropListGroup
          }]
        }]
      }];
      CdkDropListGroup.propDecorators = {
        disabled: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['cdkDropListGroupDisabled']
        }]
      };
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * Injection token that can be used to configure the
       * behavior of the drag&drop-related components.
       */

      var CDK_DRAG_CONFIG = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["InjectionToken"]('CDK_DRAG_CONFIG');
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * Asserts that a particular node is an element.
       * @param node Node to be checked.
       * @param name Name to attach to the error message.
       */

      function assertElementNode(node, name) {
        if (node.nodeType !== 1) {
          throw Error("".concat(name, " must be attached to an element node. ") + "Currently attached to \"".concat(node.nodeName, "\"."));
        }
      }
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /** Counter used to generate unique ids for drop zones. */


      var _uniqueIdCounter = 0;
      /**
       * Injection token that can be used to reference instances of `CdkDropList`. It serves as
       * alternative token to the actual `CdkDropList` class which could cause unnecessary
       * retention of the class and its directive metadata.
       */

      var CDK_DROP_LIST = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["InjectionToken"]('CdkDropList');
      var ɵ0 = undefined;
      /** Container that wraps a set of draggable items. */

      var CdkDropList = /*#__PURE__*/function () {
        function CdkDropList(
        /** Element that the drop list is attached to. */
        element, dragDrop, _changeDetectorRef, _scrollDispatcher, _dir, _group, config) {
          var _this47 = this;

          _classCallCheck(this, CdkDropList);

          this.element = element;
          this._changeDetectorRef = _changeDetectorRef;
          this._scrollDispatcher = _scrollDispatcher;
          this._dir = _dir;
          this._group = _group;
          /** Emits when the list has been destroyed. */

          this._destroyed = new rxjs__WEBPACK_IMPORTED_MODULE_5__["Subject"]();
          /**
           * Other draggable containers that this container is connected to and into which the
           * container's items can be transferred. Can either be references to other drop containers,
           * or their unique IDs.
           */

          this.connectedTo = [];
          /**
           * Unique ID for the drop zone. Can be used as a reference
           * in the `connectedTo` of another `CdkDropList`.
           */

          this.id = "cdk-drop-list-".concat(_uniqueIdCounter++);
          /**
           * Function that is used to determine whether an item
           * is allowed to be moved into a drop container.
           */

          this.enterPredicate = function () {
            return true;
          };
          /** Functions that is used to determine whether an item can be sorted into a particular index. */


          this.sortPredicate = function () {
            return true;
          };
          /** Emits when the user drops an item inside the container. */


          this.dropped = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"]();
          /**
           * Emits when the user has moved a new drag item into this container.
           */

          this.entered = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"]();
          /**
           * Emits when the user removes an item from the container
           * by dragging it into another container.
           */

          this.exited = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"]();
          /** Emits as the user is swapping items while actively dragging. */

          this.sorted = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"]();
          /**
           * Keeps track of the items that are registered with this container. Historically we used to
           * do this with a `ContentChildren` query, however queries don't handle transplanted views very
           * well which means that we can't handle cases like dragging the headers of a `mat-table`
           * correctly. What we do instead is to have the items register themselves with the container
           * and then we sort them based on their position in the DOM.
           */

          this._unsortedItems = new Set();

          if (typeof ngDevMode === 'undefined' || ngDevMode) {
            assertElementNode(element.nativeElement, 'cdkDropList');
          }

          this._dropListRef = dragDrop.createDropList(element);
          this._dropListRef.data = this;

          if (config) {
            this._assignDefaults(config);
          }

          this._dropListRef.enterPredicate = function (drag, drop) {
            return _this47.enterPredicate(drag.data, drop.data);
          };

          this._dropListRef.sortPredicate = function (index, drag, drop) {
            return _this47.sortPredicate(index, drag.data, drop.data);
          };

          this._setupInputSyncSubscription(this._dropListRef);

          this._handleEvents(this._dropListRef);

          CdkDropList._dropLists.push(this);

          if (_group) {
            _group._items.add(this);
          }
        }
        /** Whether starting a dragging sequence from this container is disabled. */


        _createClass(CdkDropList, [{
          key: "addItem",

          /** Registers an items with the drop list. */
          value: function addItem(item) {
            this._unsortedItems.add(item);

            if (this._dropListRef.isDragging()) {
              this._syncItemsWithRef();
            }
          }
          /** Removes an item from the drop list. */

        }, {
          key: "removeItem",
          value: function removeItem(item) {
            this._unsortedItems["delete"](item);

            if (this._dropListRef.isDragging()) {
              this._syncItemsWithRef();
            }
          }
          /** Gets the registered items in the list, sorted by their position in the DOM. */

        }, {
          key: "getSortedItems",
          value: function getSortedItems() {
            return Array.from(this._unsortedItems).sort(function (a, b) {
              var documentPosition = a._dragRef.getVisibleElement().compareDocumentPosition(b._dragRef.getVisibleElement()); // `compareDocumentPosition` returns a bitmask so we have to use a bitwise operator.
              // https://developer.mozilla.org/en-US/docs/Web/API/Node/compareDocumentPosition
              // tslint:disable-next-line:no-bitwise


              return documentPosition & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1;
            });
          }
        }, {
          key: "ngOnDestroy",
          value: function ngOnDestroy() {
            var index = CdkDropList._dropLists.indexOf(this);

            if (index > -1) {
              CdkDropList._dropLists.splice(index, 1);
            }

            if (this._group) {
              this._group._items["delete"](this);
            }

            this._unsortedItems.clear();

            this._dropListRef.dispose();

            this._destroyed.next();

            this._destroyed.complete();
          }
          /** Syncs the inputs of the CdkDropList with the options of the underlying DropListRef. */

        }, {
          key: "_setupInputSyncSubscription",
          value: function _setupInputSyncSubscription(ref) {
            var _this48 = this;

            if (this._dir) {
              this._dir.change.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["startWith"])(this._dir.value), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["takeUntil"])(this._destroyed)).subscribe(function (value) {
                return ref.withDirection(value);
              });
            }

            ref.beforeStarted.subscribe(function () {
              var siblings = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_4__["coerceArray"])(_this48.connectedTo).map(function (drop) {
                if (typeof drop === 'string') {
                  var correspondingDropList = CdkDropList._dropLists.find(function (list) {
                    return list.id === drop;
                  });

                  if (!correspondingDropList && (typeof ngDevMode === 'undefined' || ngDevMode)) {
                    console.warn("CdkDropList could not find connected drop list with id \"".concat(drop, "\""));
                  }

                  return correspondingDropList;
                }

                return drop;
              });

              if (_this48._group) {
                _this48._group._items.forEach(function (drop) {
                  if (siblings.indexOf(drop) === -1) {
                    siblings.push(drop);
                  }
                });
              } // Note that we resolve the scrollable parents here so that we delay the resolution
              // as long as possible, ensuring that the element is in its final place in the DOM.


              if (!_this48._scrollableParentsResolved) {
                var scrollableParents = _this48._scrollDispatcher.getAncestorScrollContainers(_this48.element).map(function (scrollable) {
                  return scrollable.getElementRef().nativeElement;
                });

                _this48._dropListRef.withScrollableParents(scrollableParents); // Only do this once since it involves traversing the DOM and the parents
                // shouldn't be able to change without the drop list being destroyed.


                _this48._scrollableParentsResolved = true;
              }

              ref.disabled = _this48.disabled;
              ref.lockAxis = _this48.lockAxis;
              ref.sortingDisabled = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_4__["coerceBooleanProperty"])(_this48.sortingDisabled);
              ref.autoScrollDisabled = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_4__["coerceBooleanProperty"])(_this48.autoScrollDisabled);
              ref.connectedTo(siblings.filter(function (drop) {
                return drop && drop !== _this48;
              }).map(function (list) {
                return list._dropListRef;
              })).withOrientation(_this48.orientation);
            });
          }
          /** Handles events from the underlying DropListRef. */

        }, {
          key: "_handleEvents",
          value: function _handleEvents(ref) {
            var _this49 = this;

            ref.beforeStarted.subscribe(function () {
              _this49._syncItemsWithRef();

              _this49._changeDetectorRef.markForCheck();
            });
            ref.entered.subscribe(function (event) {
              _this49.entered.emit({
                container: _this49,
                item: event.item.data,
                currentIndex: event.currentIndex
              });
            });
            ref.exited.subscribe(function (event) {
              _this49.exited.emit({
                container: _this49,
                item: event.item.data
              });

              _this49._changeDetectorRef.markForCheck();
            });
            ref.sorted.subscribe(function (event) {
              _this49.sorted.emit({
                previousIndex: event.previousIndex,
                currentIndex: event.currentIndex,
                container: _this49,
                item: event.item.data
              });
            });
            ref.dropped.subscribe(function (event) {
              _this49.dropped.emit({
                previousIndex: event.previousIndex,
                currentIndex: event.currentIndex,
                previousContainer: event.previousContainer.data,
                container: event.container.data,
                item: event.item.data,
                isPointerOverContainer: event.isPointerOverContainer,
                distance: event.distance
              }); // Mark for check since all of these events run outside of change
              // detection and we're not guaranteed for something else to have triggered it.


              _this49._changeDetectorRef.markForCheck();
            });
          }
          /** Assigns the default input values based on a provided config object. */

        }, {
          key: "_assignDefaults",
          value: function _assignDefaults(config) {
            var lockAxis = config.lockAxis,
                draggingDisabled = config.draggingDisabled,
                sortingDisabled = config.sortingDisabled,
                listAutoScrollDisabled = config.listAutoScrollDisabled,
                listOrientation = config.listOrientation;
            this.disabled = draggingDisabled == null ? false : draggingDisabled;
            this.sortingDisabled = sortingDisabled == null ? false : sortingDisabled;
            this.autoScrollDisabled = listAutoScrollDisabled == null ? false : listAutoScrollDisabled;
            this.orientation = listOrientation || 'vertical';

            if (lockAxis) {
              this.lockAxis = lockAxis;
            }
          }
          /** Syncs up the registered drag items with underlying drop list ref. */

        }, {
          key: "_syncItemsWithRef",
          value: function _syncItemsWithRef() {
            this._dropListRef.withItems(this.getSortedItems().map(function (item) {
              return item._dragRef;
            }));
          }
        }, {
          key: "disabled",
          get: function get() {
            return this._disabled || !!this._group && this._group.disabled;
          },
          set: function set(value) {
            // Usually we sync the directive and ref state right before dragging starts, in order to have
            // a single point of failure and to avoid having to use setters for everything. `disabled` is
            // a special case, because it can prevent the `beforeStarted` event from firing, which can lock
            // the user in a disabled state, so we also need to sync it as it's being set.
            this._dropListRef.disabled = this._disabled = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_4__["coerceBooleanProperty"])(value);
          }
        }]);

        return CdkDropList;
      }();
      /** Keeps track of the drop lists that are currently on the page. */


      CdkDropList._dropLists = [];
      CdkDropList.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"],
        args: [{
          selector: '[cdkDropList], cdk-drop-list',
          exportAs: 'cdkDropList',
          providers: [// Prevent child drop lists from picking up the same group as their parent.
          {
            provide: CDK_DROP_LIST_GROUP,
            useValue: ɵ0
          }, {
            provide: CDK_DROP_LIST,
            useExisting: CdkDropList
          }],
          host: {
            'class': 'cdk-drop-list',
            '[attr.id]': 'id',
            '[class.cdk-drop-list-disabled]': 'disabled',
            '[class.cdk-drop-list-dragging]': '_dropListRef.isDragging()',
            '[class.cdk-drop-list-receiving]': '_dropListRef.isReceiving()'
          }
        }]
      }];

      CdkDropList.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ElementRef"]
        }, {
          type: DragDrop
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ChangeDetectorRef"]
        }, {
          type: _angular_cdk_scrolling__WEBPACK_IMPORTED_MODULE_2__["ScrollDispatcher"]
        }, {
          type: _angular_cdk_bidi__WEBPACK_IMPORTED_MODULE_7__["Directionality"],
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Optional"]
          }]
        }, {
          type: CdkDropListGroup,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Optional"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Inject"],
            args: [CDK_DROP_LIST_GROUP]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["SkipSelf"]
          }]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Optional"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Inject"],
            args: [CDK_DRAG_CONFIG]
          }]
        }];
      };

      CdkDropList.propDecorators = {
        connectedTo: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['cdkDropListConnectedTo']
        }],
        data: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['cdkDropListData']
        }],
        orientation: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['cdkDropListOrientation']
        }],
        id: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"]
        }],
        lockAxis: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['cdkDropListLockAxis']
        }],
        disabled: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['cdkDropListDisabled']
        }],
        sortingDisabled: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['cdkDropListSortingDisabled']
        }],
        enterPredicate: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['cdkDropListEnterPredicate']
        }],
        sortPredicate: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['cdkDropListSortPredicate']
        }],
        autoScrollDisabled: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['cdkDropListAutoScrollDisabled']
        }],
        dropped: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Output"],
          args: ['cdkDropListDropped']
        }],
        entered: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Output"],
          args: ['cdkDropListEntered']
        }],
        exited: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Output"],
          args: ['cdkDropListExited']
        }],
        sorted: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Output"],
          args: ['cdkDropListSorted']
        }]
      };
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * Injection token that can be used to reference instances of `CdkDragHandle`. It serves as
       * alternative token to the actual `CdkDragHandle` class which could cause unnecessary
       * retention of the class and its directive metadata.
       */

      var CDK_DRAG_HANDLE = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["InjectionToken"]('CdkDragHandle');
      /** Handle that can be used to drag a CdkDrag instance. */

      var CdkDragHandle = /*#__PURE__*/function () {
        function CdkDragHandle(element, parentDrag) {
          _classCallCheck(this, CdkDragHandle);

          this.element = element;
          /** Emits when the state of the handle has changed. */

          this._stateChanges = new rxjs__WEBPACK_IMPORTED_MODULE_5__["Subject"]();
          this._disabled = false;

          if (typeof ngDevMode === 'undefined' || ngDevMode) {
            assertElementNode(element.nativeElement, 'cdkDragHandle');
          }

          this._parentDrag = parentDrag;
        }
        /** Whether starting to drag through this handle is disabled. */


        _createClass(CdkDragHandle, [{
          key: "ngOnDestroy",
          value: function ngOnDestroy() {
            this._stateChanges.complete();
          }
        }, {
          key: "disabled",
          get: function get() {
            return this._disabled;
          },
          set: function set(value) {
            this._disabled = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_4__["coerceBooleanProperty"])(value);

            this._stateChanges.next(this);
          }
        }]);

        return CdkDragHandle;
      }();

      CdkDragHandle.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"],
        args: [{
          selector: '[cdkDragHandle]',
          host: {
            'class': 'cdk-drag-handle'
          },
          providers: [{
            provide: CDK_DRAG_HANDLE,
            useExisting: CdkDragHandle
          }]
        }]
      }];

      CdkDragHandle.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ElementRef"]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Inject"],
            args: [CDK_DRAG_PARENT]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Optional"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["SkipSelf"]
          }]
        }];
      };

      CdkDragHandle.propDecorators = {
        disabled: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['cdkDragHandleDisabled']
        }]
      };
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * Injection token that can be used to reference instances of `CdkDragPlaceholder`. It serves as
       * alternative token to the actual `CdkDragPlaceholder` class which could cause unnecessary
       * retention of the class and its directive metadata.
       */

      var CDK_DRAG_PLACEHOLDER = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["InjectionToken"]('CdkDragPlaceholder');
      /**
       * Element that will be used as a template for the placeholder of a CdkDrag when
       * it is being dragged. The placeholder is displayed in place of the element being dragged.
       */

      var CdkDragPlaceholder = function CdkDragPlaceholder(templateRef) {
        _classCallCheck(this, CdkDragPlaceholder);

        this.templateRef = templateRef;
      };

      CdkDragPlaceholder.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"],
        args: [{
          selector: 'ng-template[cdkDragPlaceholder]',
          providers: [{
            provide: CDK_DRAG_PLACEHOLDER,
            useExisting: CdkDragPlaceholder
          }]
        }]
      }];

      CdkDragPlaceholder.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["TemplateRef"]
        }];
      };

      CdkDragPlaceholder.propDecorators = {
        data: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"]
        }]
      };
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * Injection token that can be used to reference instances of `CdkDragPreview`. It serves as
       * alternative token to the actual `CdkDragPreview` class which could cause unnecessary
       * retention of the class and its directive metadata.
       */

      var CDK_DRAG_PREVIEW = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["InjectionToken"]('CdkDragPreview');
      /**
       * Element that will be used as a template for the preview
       * of a CdkDrag when it is being dragged.
       */

      var CdkDragPreview = /*#__PURE__*/function () {
        function CdkDragPreview(templateRef) {
          _classCallCheck(this, CdkDragPreview);

          this.templateRef = templateRef;
          this._matchSize = false;
        }
        /** Whether the preview should preserve the same size as the item that is being dragged. */


        _createClass(CdkDragPreview, [{
          key: "matchSize",
          get: function get() {
            return this._matchSize;
          },
          set: function set(value) {
            this._matchSize = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_4__["coerceBooleanProperty"])(value);
          }
        }]);

        return CdkDragPreview;
      }();

      CdkDragPreview.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"],
        args: [{
          selector: 'ng-template[cdkDragPreview]',
          providers: [{
            provide: CDK_DRAG_PREVIEW,
            useExisting: CdkDragPreview
          }]
        }]
      }];

      CdkDragPreview.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["TemplateRef"]
        }];
      };

      CdkDragPreview.propDecorators = {
        data: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"]
        }],
        matchSize: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"]
        }]
      };
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /** Element that can be moved inside a CdkDropList container. */

      var CdkDrag = /*#__PURE__*/function () {
        function CdkDrag(
        /** Element that the draggable is attached to. */
        element,
        /** Droppable container that the draggable is a part of. */
        dropContainer,
        /**
         * @deprecated `_document` parameter no longer being used and will be removed.
         * @breaking-change 12.0.0
         */
        _document, _ngZone, _viewContainerRef, config, _dir, dragDrop, _changeDetectorRef, _selfHandle, parentDrag) {
          var _this50 = this;

          _classCallCheck(this, CdkDrag);

          this.element = element;
          this.dropContainer = dropContainer;
          this._ngZone = _ngZone;
          this._viewContainerRef = _viewContainerRef;
          this._dir = _dir;
          this._changeDetectorRef = _changeDetectorRef;
          this._selfHandle = _selfHandle;
          this._destroyed = new rxjs__WEBPACK_IMPORTED_MODULE_5__["Subject"]();
          /** Emits when the user starts dragging the item. */

          this.started = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"]();
          /** Emits when the user has released a drag item, before any animations have started. */

          this.released = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"]();
          /** Emits when the user stops dragging an item in the container. */

          this.ended = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"]();
          /** Emits when the user has moved the item into a new container. */

          this.entered = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"]();
          /** Emits when the user removes the item its container by dragging it into another container. */

          this.exited = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"]();
          /** Emits when the user drops the item inside a container. */

          this.dropped = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"]();
          /**
           * Emits as the user is dragging the item. Use with caution,
           * because this event will fire for every pixel that the user has dragged.
           */

          this.moved = new rxjs__WEBPACK_IMPORTED_MODULE_5__["Observable"](function (observer) {
            var subscription = _this50._dragRef.moved.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["map"])(function (movedEvent) {
              return {
                source: _this50,
                pointerPosition: movedEvent.pointerPosition,
                event: movedEvent.event,
                delta: movedEvent.delta,
                distance: movedEvent.distance
              };
            })).subscribe(observer);

            return function () {
              subscription.unsubscribe();
            };
          });
          this._dragRef = dragDrop.createDrag(element, {
            dragStartThreshold: config && config.dragStartThreshold != null ? config.dragStartThreshold : 5,
            pointerDirectionChangeThreshold: config && config.pointerDirectionChangeThreshold != null ? config.pointerDirectionChangeThreshold : 5,
            zIndex: config === null || config === void 0 ? void 0 : config.zIndex,
            parentDragRef: parentDrag === null || parentDrag === void 0 ? void 0 : parentDrag._dragRef
          });
          this._dragRef.data = this;

          if (config) {
            this._assignDefaults(config);
          } // Note that usually the container is assigned when the drop list is picks up the item, but in
          // some cases (mainly transplanted views with OnPush, see #18341) we may end up in a situation
          // where there are no items on the first change detection pass, but the items get picked up as
          // soon as the user triggers another pass by dragging. This is a problem, because the item would
          // have to switch from standalone mode to drag mode in the middle of the dragging sequence which
          // is too late since the two modes save different kinds of information. We work around it by
          // assigning the drop container both from here and the list.


          if (dropContainer) {
            this._dragRef._withDropContainer(dropContainer._dropListRef);

            dropContainer.addItem(this);
          }

          this._syncInputs(this._dragRef);

          this._handleEvents(this._dragRef);
        }
        /** Whether starting to drag this element is disabled. */


        _createClass(CdkDrag, [{
          key: "getPlaceholderElement",

          /**
           * Returns the element that is being used as a placeholder
           * while the current element is being dragged.
           */
          value: function getPlaceholderElement() {
            return this._dragRef.getPlaceholderElement();
          }
          /** Returns the root draggable element. */

        }, {
          key: "getRootElement",
          value: function getRootElement() {
            return this._dragRef.getRootElement();
          }
          /** Resets a standalone drag item to its initial position. */

        }, {
          key: "reset",
          value: function reset() {
            this._dragRef.reset();
          }
          /**
           * Gets the pixel coordinates of the draggable outside of a drop container.
           */

        }, {
          key: "getFreeDragPosition",
          value: function getFreeDragPosition() {
            return this._dragRef.getFreeDragPosition();
          }
        }, {
          key: "ngAfterViewInit",
          value: function ngAfterViewInit() {
            var _this51 = this;

            // We need to wait for the zone to stabilize, in order for the reference
            // element to be in the proper place in the DOM. This is mostly relevant
            // for draggable elements inside portals since they get stamped out in
            // their original DOM position and then they get transferred to the portal.
            this._ngZone.onStable.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["take"])(1), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["takeUntil"])(this._destroyed)).subscribe(function () {
              _this51._updateRootElement(); // Listen for any newly-added handles.


              _this51._handles.changes.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["startWith"])(_this51._handles), // Sync the new handles with the DragRef.
              Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["tap"])(function (handles) {
                var childHandleElements = handles.filter(function (handle) {
                  return handle._parentDrag === _this51;
                }).map(function (handle) {
                  return handle.element;
                }); // Usually handles are only allowed to be a descendant of the drag element, but if
                // the consumer defined a different drag root, we should allow the drag element
                // itself to be a handle too.

                if (_this51._selfHandle && _this51.rootElementSelector) {
                  childHandleElements.push(_this51.element);
                }

                _this51._dragRef.withHandles(childHandleElements);
              }), // Listen if the state of any of the handles changes.
              Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["switchMap"])(function (handles) {
                return Object(rxjs__WEBPACK_IMPORTED_MODULE_5__["merge"]).apply(void 0, _toConsumableArray(handles.map(function (item) {
                  return item._stateChanges.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["startWith"])(item));
                })));
              }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["takeUntil"])(_this51._destroyed)).subscribe(function (handleInstance) {
                // Enabled/disable the handle that changed in the DragRef.
                var dragRef = _this51._dragRef;
                var handle = handleInstance.element.nativeElement;
                handleInstance.disabled ? dragRef.disableHandle(handle) : dragRef.enableHandle(handle);
              });

              if (_this51.freeDragPosition) {
                _this51._dragRef.setFreeDragPosition(_this51.freeDragPosition);
              }
            });
          }
        }, {
          key: "ngOnChanges",
          value: function ngOnChanges(changes) {
            var rootSelectorChange = changes['rootElementSelector'];
            var positionChange = changes['freeDragPosition']; // We don't have to react to the first change since it's being
            // handled in `ngAfterViewInit` where it needs to be deferred.

            if (rootSelectorChange && !rootSelectorChange.firstChange) {
              this._updateRootElement();
            } // Skip the first change since it's being handled in `ngAfterViewInit`.


            if (positionChange && !positionChange.firstChange && this.freeDragPosition) {
              this._dragRef.setFreeDragPosition(this.freeDragPosition);
            }
          }
        }, {
          key: "ngOnDestroy",
          value: function ngOnDestroy() {
            if (this.dropContainer) {
              this.dropContainer.removeItem(this);
            }

            this._destroyed.next();

            this._destroyed.complete();

            this._dragRef.dispose();
          }
          /** Syncs the root element with the `DragRef`. */

        }, {
          key: "_updateRootElement",
          value: function _updateRootElement() {
            var element = this.element.nativeElement;
            var rootElement = this.rootElementSelector ? getClosestMatchingAncestor(element, this.rootElementSelector) : element;

            if (rootElement && (typeof ngDevMode === 'undefined' || ngDevMode)) {
              assertElementNode(rootElement, 'cdkDrag');
            }

            this._dragRef.withRootElement(rootElement || element);
          }
          /** Gets the boundary element, based on the `boundaryElement` value. */

        }, {
          key: "_getBoundaryElement",
          value: function _getBoundaryElement() {
            var boundary = this.boundaryElement;

            if (!boundary) {
              return null;
            }

            if (typeof boundary === 'string') {
              return getClosestMatchingAncestor(this.element.nativeElement, boundary);
            }

            var element = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_4__["coerceElement"])(boundary);

            if ((typeof ngDevMode === 'undefined' || ngDevMode) && !element.contains(this.element.nativeElement)) {
              throw Error('Draggable element is not inside of the node passed into cdkDragBoundary.');
            }

            return element;
          }
          /** Syncs the inputs of the CdkDrag with the options of the underlying DragRef. */

        }, {
          key: "_syncInputs",
          value: function _syncInputs(ref) {
            var _this52 = this;

            ref.beforeStarted.subscribe(function () {
              if (!ref.isDragging()) {
                var dir = _this52._dir;
                var dragStartDelay = _this52.dragStartDelay;
                var placeholder = _this52._placeholderTemplate ? {
                  template: _this52._placeholderTemplate.templateRef,
                  context: _this52._placeholderTemplate.data,
                  viewContainer: _this52._viewContainerRef
                } : null;
                var preview = _this52._previewTemplate ? {
                  template: _this52._previewTemplate.templateRef,
                  context: _this52._previewTemplate.data,
                  matchSize: _this52._previewTemplate.matchSize,
                  viewContainer: _this52._viewContainerRef
                } : null;
                ref.disabled = _this52.disabled;
                ref.lockAxis = _this52.lockAxis;
                ref.dragStartDelay = typeof dragStartDelay === 'object' && dragStartDelay ? dragStartDelay : Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_4__["coerceNumberProperty"])(dragStartDelay);
                ref.constrainPosition = _this52.constrainPosition;
                ref.previewClass = _this52.previewClass;
                ref.withBoundaryElement(_this52._getBoundaryElement()).withPlaceholderTemplate(placeholder).withPreviewTemplate(preview);

                if (dir) {
                  ref.withDirection(dir.value);
                }
              }
            });
          }
          /** Handles the events from the underlying `DragRef`. */

        }, {
          key: "_handleEvents",
          value: function _handleEvents(ref) {
            var _this53 = this;

            ref.started.subscribe(function () {
              _this53.started.emit({
                source: _this53
              }); // Since all of these events run outside of change detection,
              // we need to ensure that everything is marked correctly.


              _this53._changeDetectorRef.markForCheck();
            });
            ref.released.subscribe(function () {
              _this53.released.emit({
                source: _this53
              });
            });
            ref.ended.subscribe(function (event) {
              _this53.ended.emit({
                source: _this53,
                distance: event.distance
              }); // Since all of these events run outside of change detection,
              // we need to ensure that everything is marked correctly.


              _this53._changeDetectorRef.markForCheck();
            });
            ref.entered.subscribe(function (event) {
              _this53.entered.emit({
                container: event.container.data,
                item: _this53,
                currentIndex: event.currentIndex
              });
            });
            ref.exited.subscribe(function (event) {
              _this53.exited.emit({
                container: event.container.data,
                item: _this53
              });
            });
            ref.dropped.subscribe(function (event) {
              _this53.dropped.emit({
                previousIndex: event.previousIndex,
                currentIndex: event.currentIndex,
                previousContainer: event.previousContainer.data,
                container: event.container.data,
                isPointerOverContainer: event.isPointerOverContainer,
                item: _this53,
                distance: event.distance
              });
            });
          }
          /** Assigns the default input values based on a provided config object. */

        }, {
          key: "_assignDefaults",
          value: function _assignDefaults(config) {
            var lockAxis = config.lockAxis,
                dragStartDelay = config.dragStartDelay,
                constrainPosition = config.constrainPosition,
                previewClass = config.previewClass,
                boundaryElement = config.boundaryElement,
                draggingDisabled = config.draggingDisabled,
                rootElementSelector = config.rootElementSelector;
            this.disabled = draggingDisabled == null ? false : draggingDisabled;
            this.dragStartDelay = dragStartDelay || 0;

            if (lockAxis) {
              this.lockAxis = lockAxis;
            }

            if (constrainPosition) {
              this.constrainPosition = constrainPosition;
            }

            if (previewClass) {
              this.previewClass = previewClass;
            }

            if (boundaryElement) {
              this.boundaryElement = boundaryElement;
            }

            if (rootElementSelector) {
              this.rootElementSelector = rootElementSelector;
            }
          }
        }, {
          key: "disabled",
          get: function get() {
            return this._disabled || this.dropContainer && this.dropContainer.disabled;
          },
          set: function set(value) {
            this._disabled = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_4__["coerceBooleanProperty"])(value);
            this._dragRef.disabled = this._disabled;
          }
        }]);

        return CdkDrag;
      }();

      CdkDrag.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"],
        args: [{
          selector: '[cdkDrag]',
          exportAs: 'cdkDrag',
          host: {
            'class': 'cdk-drag',
            '[class.cdk-drag-disabled]': 'disabled',
            '[class.cdk-drag-dragging]': '_dragRef.isDragging()'
          },
          providers: [{
            provide: CDK_DRAG_PARENT,
            useExisting: CdkDrag
          }]
        }]
      }];

      CdkDrag.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ElementRef"]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Inject"],
            args: [CDK_DROP_LIST]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Optional"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["SkipSelf"]
          }]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Inject"],
            args: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["DOCUMENT"]]
          }]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["NgZone"]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ViewContainerRef"]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Optional"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Inject"],
            args: [CDK_DRAG_CONFIG]
          }]
        }, {
          type: _angular_cdk_bidi__WEBPACK_IMPORTED_MODULE_7__["Directionality"],
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Optional"]
          }]
        }, {
          type: DragDrop
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ChangeDetectorRef"]
        }, {
          type: CdkDragHandle,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Optional"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Self"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Inject"],
            args: [CDK_DRAG_HANDLE]
          }]
        }, {
          type: CdkDrag,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Optional"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["SkipSelf"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Inject"],
            args: [CDK_DRAG_PARENT]
          }]
        }];
      };

      CdkDrag.propDecorators = {
        _handles: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ContentChildren"],
          args: [CDK_DRAG_HANDLE, {
            descendants: true
          }]
        }],
        _previewTemplate: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ContentChild"],
          args: [CDK_DRAG_PREVIEW]
        }],
        _placeholderTemplate: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ContentChild"],
          args: [CDK_DRAG_PLACEHOLDER]
        }],
        data: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['cdkDragData']
        }],
        lockAxis: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['cdkDragLockAxis']
        }],
        rootElementSelector: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['cdkDragRootElement']
        }],
        boundaryElement: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['cdkDragBoundary']
        }],
        dragStartDelay: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['cdkDragStartDelay']
        }],
        freeDragPosition: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['cdkDragFreeDragPosition']
        }],
        disabled: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['cdkDragDisabled']
        }],
        constrainPosition: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['cdkDragConstrainPosition']
        }],
        previewClass: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['cdkDragPreviewClass']
        }],
        started: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Output"],
          args: ['cdkDragStarted']
        }],
        released: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Output"],
          args: ['cdkDragReleased']
        }],
        ended: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Output"],
          args: ['cdkDragEnded']
        }],
        entered: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Output"],
          args: ['cdkDragEntered']
        }],
        exited: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Output"],
          args: ['cdkDragExited']
        }],
        dropped: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Output"],
          args: ['cdkDragDropped']
        }],
        moved: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Output"],
          args: ['cdkDragMoved']
        }]
      };
      /** Gets the closest ancestor of an element that matches a selector. */

      function getClosestMatchingAncestor(element, selector) {
        var currentElement = element.parentElement;

        while (currentElement) {
          // IE doesn't support `matches` so we have to fall back to `msMatchesSelector`.
          if (currentElement.matches ? currentElement.matches(selector) : currentElement.msMatchesSelector(selector)) {
            return currentElement;
          }

          currentElement = currentElement.parentElement;
        }

        return null;
      }
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */


      var DragDropModule = function DragDropModule() {
        _classCallCheck(this, DragDropModule);
      };

      DragDropModule.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"],
        args: [{
          declarations: [CdkDropList, CdkDropListGroup, CdkDrag, CdkDragHandle, CdkDragPreview, CdkDragPlaceholder],
          exports: [_angular_cdk_scrolling__WEBPACK_IMPORTED_MODULE_2__["CdkScrollableModule"], CdkDropList, CdkDropListGroup, CdkDrag, CdkDragHandle, CdkDragPreview, CdkDragPlaceholder],
          providers: [DragDrop]
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
      //# sourceMappingURL=drag-drop.js.map

      /***/
    },

    /***/
    "me+b":
    /*!************************************************************************************************!*\
      !*** ./src/app/modules/requests/components/scrumboard-dialog/scrumboard-dialog.component.scss ***!
      \************************************************************************************************/

    /*! exports provided: default */

    /***/
    function meB(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = ".members .avatar {\n  border: 2px solid var(--background-card);\n  box-sizing: border-box;\n  height: 36px;\n  margin-right: -8px;\n  margin-top: var(--padding-4);\n  width: 36px;\n}\n\n.members .avatar:last-child {\n  margin-right: 0;\n}\n\n.labels .label {\n  border-radius: var(--border-radius);\n  font: var(--font-caption);\n  height: 32px;\n  line-height: 32px;\n  margin-top: var(--padding-4);\n  min-width: 32px;\n  padding-left: var(--padding-8);\n  padding-right: var(--padding-8);\n  -webkit-user-select: none;\n     -moz-user-select: none;\n          user-select: none;\n}\n\n.labels .label:last-of-type {\n  padding: 0;\n}\n\n.content {\n  max-height: 40vh;\n}\n\n@media (min-width: 600px) {\n  .content {\n    max-height: 50vh;\n  }\n}\n\n.content {\n  height: 400px;\n  overflow-y: auto;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uLy4uL3NjcnVtYm9hcmQtZGlhbG9nLmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0VBQ0Usd0NBQUE7RUFDQSxzQkFBQTtFQUNBLFlBQUE7RUFDQSxrQkFBQTtFQUNBLDRCQUFBO0VBQ0EsV0FBQTtBQUNGOztBQUVBO0VBQ0UsZUFBQTtBQUNGOztBQUVBO0VBQ0UsbUNBQUE7RUFDQSx5QkFBQTtFQUNBLFlBQUE7RUFDQSxpQkFBQTtFQUNBLDRCQUFBO0VBQ0EsZUFBQTtFQUNBLDhCQUFBO0VBQ0EsK0JBQUE7RUFDQSx5QkFBQTtLQUFBLHNCQUFBO1VBQUEsaUJBQUE7QUFDRjs7QUFFQTtFQUNFLFVBQUE7QUFDRjs7QUFFQTtFQUNFLGdCQUFBO0FBQ0Y7O0FBRUE7RUFDRTtJQUNFLGdCQUFBO0VBQ0Y7QUFDRjs7QUFFQTtFQUNFLGFBQUE7RUFDQSxnQkFBQTtBQUFGIiwiZmlsZSI6InNjcnVtYm9hcmQtZGlhbG9nLmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiLm1lbWJlcnMgLmF2YXRhciB7XG4gIGJvcmRlcjogMnB4IHNvbGlkIHZhcigtLWJhY2tncm91bmQtY2FyZCk7XG4gIGJveC1zaXppbmc6IGJvcmRlci1ib3g7XG4gIGhlaWdodDogMzZweDtcbiAgbWFyZ2luLXJpZ2h0OiAtOHB4O1xuICBtYXJnaW4tdG9wOiB2YXIoLS1wYWRkaW5nLTQpO1xuICB3aWR0aDogMzZweDtcbn1cblxuLm1lbWJlcnMgLmF2YXRhcjpsYXN0LWNoaWxkIHtcbiAgbWFyZ2luLXJpZ2h0OiAwO1xufVxuXG4ubGFiZWxzIC5sYWJlbCB7XG4gIGJvcmRlci1yYWRpdXM6IHZhcigtLWJvcmRlci1yYWRpdXMpO1xuICBmb250OiB2YXIoLS1mb250LWNhcHRpb24pO1xuICBoZWlnaHQ6IDMycHg7XG4gIGxpbmUtaGVpZ2h0OiAzMnB4O1xuICBtYXJnaW4tdG9wOiB2YXIoLS1wYWRkaW5nLTQpO1xuICBtaW4td2lkdGg6IDMycHg7XG4gIHBhZGRpbmctbGVmdDogdmFyKC0tcGFkZGluZy04KTtcbiAgcGFkZGluZy1yaWdodDogdmFyKC0tcGFkZGluZy04KTtcbiAgdXNlci1zZWxlY3Q6IG5vbmU7XG59XG5cbi5sYWJlbHMgLmxhYmVsOmxhc3Qtb2YtdHlwZSB7XG4gIHBhZGRpbmc6IDA7XG59XG5cbi5jb250ZW50IHtcbiAgbWF4LWhlaWdodDogNDB2aDtcbn1cblxuQG1lZGlhIChtaW4td2lkdGg6IDYwMHB4KSB7XG4gIC5jb250ZW50IHtcbiAgICBtYXgtaGVpZ2h0OiA1MHZoO1xuICB9XG59XG5cbi5jb250ZW50IHtcbiAgaGVpZ2h0OiA0MDBweDtcbiAgb3ZlcmZsb3cteTogYXV0bztcbn0iXX0= */";
      /***/
    },

    /***/
    "ndZO":
    /*!***********************************************************************************!*\
      !*** ./src/app/modules/scenarios/pages/scenarios-index/scenarios-index.module.ts ***!
      \***********************************************************************************/

    /*! exports provided: ScenariosIndexModule */

    /***/
    function ndZO(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ScenariosIndexModule", function () {
        return ScenariosIndexModule;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _angular_cdk_clipboard__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! @angular/cdk/clipboard */
      "Tr4x");
      /* harmony import */


      var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @angular/common */
      "SVse");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/flex-layout */
      "u9T3");
      /* harmony import */


      var _angular_forms__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/forms */
      "s7LF");
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


      var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @angular/material/dialog */
      "iELJ");
      /* harmony import */


      var _angular_material_icon__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @angular/material/icon */
      "Tj54");
      /* harmony import */


      var _angular_material_menu__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @angular/material/menu */
      "rJgo");
      /* harmony import */


      var _angular_material_paginator__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @angular/material/paginator */
      "5QHs");
      /* harmony import */


      var _angular_material_sidenav__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @angular/material/sidenav */
      "q7Ft");
      /* harmony import */


      var _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! @angular/material/snack-bar */
      "zHaW");
      /* harmony import */


      var _angular_material_sort__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! @angular/material/sort */
      "LUZP");
      /* harmony import */


      var _angular_material_table__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(
      /*! @angular/material/table */
      "OaSA");
      /* harmony import */


      var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(
      /*! @visurel/iconify-angular */
      "l+Q0");
      /* harmony import */


      var _vex_components_breadcrumbs_breadcrumbs_module__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(
      /*! @vex/components/breadcrumbs/breadcrumbs.module */
      "J0XA");
      /* harmony import */


      var _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(
      /*! @vex/components/page-layout/page-layout.module */
      "7lCJ");
      /* harmony import */


      var _vex_components_scrollbar_scrollbar_module__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(
      /*! @vex/components/scrollbar/scrollbar.module */
      "XVi8");
      /* harmony import */


      var _vex_directives_container_container_module__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(
      /*! @vex/directives/container/container.module */
      "68Yx");
      /* harmony import */


      var _scenarios_components_scenarios_create_scenarios_create_module__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(
      /*! @scenarios/components/scenarios-create/scenarios-create.module */
      "3ZMo");
      /* harmony import */


      var _scenarios_components_scenarios_edit_scenarios_edit_module__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(
      /*! @scenarios/components/scenarios-edit/scenarios-edit.module */
      "cuMl");
      /* harmony import */


      var _shared_components_data_table_data_table_module__WEBPACK_IMPORTED_MODULE_24__ = __webpack_require__(
      /*! @shared/components/data-table/data-table.module */
      "MqAd");
      /* harmony import */


      var _components_scenarios_data_table_scenarios_data_table_component__WEBPACK_IMPORTED_MODULE_25__ = __webpack_require__(
      /*! ./components/scenarios-data-table/scenarios-data-table.component */
      "bhgl");
      /* harmony import */


      var _components_scenarios_table_menu_scenarios_table_menu_component__WEBPACK_IMPORTED_MODULE_26__ = __webpack_require__(
      /*! ./components/scenarios-table-menu/scenarios-table-menu.component */
      "O/8V");
      /* harmony import */


      var _scenarios_index_component__WEBPACK_IMPORTED_MODULE_27__ = __webpack_require__(
      /*! ./scenarios-index.component */
      "llVH");
      /* harmony import */


      var _services_scenarios_index_icons_service__WEBPACK_IMPORTED_MODULE_28__ = __webpack_require__(
      /*! ./services/scenarios-index-icons.service */
      "WZBS");

      var ScenariosIndexModule = function ScenariosIndexModule() {
        _classCallCheck(this, ScenariosIndexModule);
      };

      ScenariosIndexModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["NgModule"])({
        declarations: [_scenarios_index_component__WEBPACK_IMPORTED_MODULE_27__["ScenariosIndexComponent"], _components_scenarios_data_table_scenarios_data_table_component__WEBPACK_IMPORTED_MODULE_25__["ScenariosDataTableComponent"], _components_scenarios_table_menu_scenarios_table_menu_component__WEBPACK_IMPORTED_MODULE_26__["ScenariosTableMenuComponent"]],
        imports: [_angular_cdk_clipboard__WEBPACK_IMPORTED_MODULE_1__["ClipboardModule"], _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_4__["FlexLayoutModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_5__["FormsModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_5__["ReactiveFormsModule"], _angular_material_button__WEBPACK_IMPORTED_MODULE_6__["MatButtonModule"], _angular_material_table__WEBPACK_IMPORTED_MODULE_16__["MatTableModule"], _angular_material_paginator__WEBPACK_IMPORTED_MODULE_12__["MatPaginatorModule"], _angular_material_sort__WEBPACK_IMPORTED_MODULE_15__["MatSortModule"], _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_7__["MatCheckboxModule"], _angular_material_icon__WEBPACK_IMPORTED_MODULE_10__["MatIconModule"], _angular_material_menu__WEBPACK_IMPORTED_MODULE_11__["MatMenuModule"], _angular_material_core__WEBPACK_IMPORTED_MODULE_8__["MatRippleModule"], _angular_material_dialog__WEBPACK_IMPORTED_MODULE_9__["MatDialogModule"], _angular_material_sidenav__WEBPACK_IMPORTED_MODULE_13__["MatSidenavModule"], _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_14__["MatSnackBarModule"], _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_17__["IconModule"], _vex_components_breadcrumbs_breadcrumbs_module__WEBPACK_IMPORTED_MODULE_18__["BreadcrumbsModule"], _vex_directives_container_container_module__WEBPACK_IMPORTED_MODULE_21__["ContainerModule"], _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_19__["PageLayoutModule"], _vex_components_scrollbar_scrollbar_module__WEBPACK_IMPORTED_MODULE_20__["ScrollbarModule"], _shared_components_data_table_data_table_module__WEBPACK_IMPORTED_MODULE_24__["DataTableModule"], _scenarios_components_scenarios_edit_scenarios_edit_module__WEBPACK_IMPORTED_MODULE_23__["ScenariosEditModule"], _scenarios_components_scenarios_create_scenarios_create_module__WEBPACK_IMPORTED_MODULE_22__["ScenariosCreateModule"]],
        providers: [_services_scenarios_index_icons_service__WEBPACK_IMPORTED_MODULE_28__["ScenariosIndexIcons"]]
      })], ScenariosIndexModule);
      /***/
    },

    /***/
    "o4Yh":
    /*!**************************************************************!*\
      !*** ./node_modules/@angular/material/fesm2015/expansion.js ***!
      \**************************************************************/

    /*! exports provided: EXPANSION_PANEL_ANIMATION_TIMING, MAT_ACCORDION, MAT_EXPANSION_PANEL_DEFAULT_OPTIONS, MatAccordion, MatExpansionModule, MatExpansionPanel, MatExpansionPanelActionRow, MatExpansionPanelContent, MatExpansionPanelDescription, MatExpansionPanelHeader, MatExpansionPanelTitle, matExpansionAnimations, ɵ0 */

    /***/
    function o4Yh(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "EXPANSION_PANEL_ANIMATION_TIMING", function () {
        return EXPANSION_PANEL_ANIMATION_TIMING;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MAT_ACCORDION", function () {
        return MAT_ACCORDION;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MAT_EXPANSION_PANEL_DEFAULT_OPTIONS", function () {
        return MAT_EXPANSION_PANEL_DEFAULT_OPTIONS;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatAccordion", function () {
        return MatAccordion;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatExpansionModule", function () {
        return MatExpansionModule;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatExpansionPanel", function () {
        return MatExpansionPanel;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatExpansionPanelActionRow", function () {
        return MatExpansionPanelActionRow;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatExpansionPanelContent", function () {
        return MatExpansionPanelContent;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatExpansionPanelDescription", function () {
        return MatExpansionPanelDescription;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatExpansionPanelHeader", function () {
        return MatExpansionPanelHeader;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatExpansionPanelTitle", function () {
        return MatExpansionPanelTitle;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "matExpansionAnimations", function () {
        return matExpansionAnimations;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ɵ0", function () {
        return ɵ0;
      });
      /* harmony import */


      var _angular_cdk_accordion__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! @angular/cdk/accordion */
      "GF+f");
      /* harmony import */


      var _angular_cdk_portal__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! @angular/cdk/portal */
      "1z/I");
      /* harmony import */


      var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @angular/common */
      "SVse");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_material_core__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/material/core */
      "UhP/");
      /* harmony import */


      var _angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/cdk/coercion */
      "8LU1");
      /* harmony import */


      var _angular_cdk_a11y__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/cdk/a11y */
      "YEUz");
      /* harmony import */


      var rxjs_operators__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! rxjs/operators */
      "kU1M");
      /* harmony import */


      var _angular_cdk_keycodes__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @angular/cdk/keycodes */
      "Ht+U");
      /* harmony import */


      var _angular_platform_browser_animations__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @angular/platform-browser/animations */
      "omvX");
      /* harmony import */


      var rxjs__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! rxjs */
      "qCKp");
      /* harmony import */


      var _angular_animations__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @angular/animations */
      "GS7A");
      /* harmony import */


      var _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @angular/cdk/collections */
      "CtHx");
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * Token used to provide a `MatAccordion` to `MatExpansionPanel`.
       * Used primarily to avoid circular imports between `MatAccordion` and `MatExpansionPanel`.
       */


      var MAT_ACCORDION = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["InjectionToken"]('MAT_ACCORDION');
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /** Time and timing curve for expansion panel animations. */
      // Note: Keep this in sync with the Sass variable for the panel header animation.

      var EXPANSION_PANEL_ANIMATION_TIMING = '225ms cubic-bezier(0.4,0.0,0.2,1)';
      /**
       * Animations used by the Material expansion panel.
       *
       * A bug in angular animation's `state` when ViewContainers are moved using ViewContainerRef.move()
       * causes the animation state of moved components to become `void` upon exit, and not update again
       * upon reentry into the DOM.  This can lead a to situation for the expansion panel where the state
       * of the panel is `expanded` or `collapsed` but the animation state is `void`.
       *
       * To correctly handle animating to the next state, we animate between `void` and `collapsed` which
       * are defined to have the same styles. Since angular animates from the current styles to the
       * destination state's style definition, in situations where we are moving from `void`'s styles to
       * `collapsed` this acts a noop since no style values change.
       *
       * In the case where angular's animation state is out of sync with the expansion panel's state, the
       * expansion panel being `expanded` and angular animations being `void`, the animation from the
       * `expanded`'s effective styles (though in a `void` animation state) to the collapsed state will
       * occur as expected.
       *
       * Angular Bug: https://github.com/angular/angular/issues/18847
       *
       * @docs-private
       */

      var matExpansionAnimations = {
        /** Animation that rotates the indicator arrow. */
        indicatorRotate: Object(_angular_animations__WEBPACK_IMPORTED_MODULE_11__["trigger"])('indicatorRotate', [Object(_angular_animations__WEBPACK_IMPORTED_MODULE_11__["state"])('collapsed, void', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_11__["style"])({
          transform: 'rotate(0deg)'
        })), Object(_angular_animations__WEBPACK_IMPORTED_MODULE_11__["state"])('expanded', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_11__["style"])({
          transform: 'rotate(180deg)'
        })), Object(_angular_animations__WEBPACK_IMPORTED_MODULE_11__["transition"])('expanded <=> collapsed, void => collapsed', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_11__["animate"])(EXPANSION_PANEL_ANIMATION_TIMING))]),

        /** Animation that expands and collapses the panel content. */
        bodyExpansion: Object(_angular_animations__WEBPACK_IMPORTED_MODULE_11__["trigger"])('bodyExpansion', [Object(_angular_animations__WEBPACK_IMPORTED_MODULE_11__["state"])('collapsed, void', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_11__["style"])({
          height: '0px',
          visibility: 'hidden'
        })), Object(_angular_animations__WEBPACK_IMPORTED_MODULE_11__["state"])('expanded', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_11__["style"])({
          height: '*',
          visibility: 'visible'
        })), Object(_angular_animations__WEBPACK_IMPORTED_MODULE_11__["transition"])('expanded <=> collapsed, void => collapsed', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_11__["animate"])(EXPANSION_PANEL_ANIMATION_TIMING))])
      };
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * Expansion panel content that will be rendered lazily
       * after the panel is opened for the first time.
       */

      var MatExpansionPanelContent = function MatExpansionPanelContent(_template) {
        _classCallCheck(this, MatExpansionPanelContent);

        this._template = _template;
      };

      MatExpansionPanelContent.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Directive"],
        args: [{
          selector: 'ng-template[matExpansionPanelContent]'
        }]
      }];

      MatExpansionPanelContent.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["TemplateRef"]
        }];
      };
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /** Counter for generating unique element ids. */


      var uniqueId = 0;
      /**
       * Injection token that can be used to configure the defalt
       * options for the expansion panel component.
       */

      var MAT_EXPANSION_PANEL_DEFAULT_OPTIONS = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["InjectionToken"]('MAT_EXPANSION_PANEL_DEFAULT_OPTIONS');
      var ɵ0 = undefined;
      /**
       * This component can be used as a single element to show expandable content, or as one of
       * multiple children of an element with the MatAccordion directive attached.
       */

      var MatExpansionPanel = /*#__PURE__*/function (_angular_cdk_accordio) {
        _inherits(MatExpansionPanel, _angular_cdk_accordio);

        var _super = _createSuper(MatExpansionPanel);

        function MatExpansionPanel(accordion, _changeDetectorRef, _uniqueSelectionDispatcher, _viewContainerRef, _document, _animationMode, defaultOptions) {
          var _this54;

          _classCallCheck(this, MatExpansionPanel);

          _this54 = _super.call(this, accordion, _changeDetectorRef, _uniqueSelectionDispatcher);
          _this54._viewContainerRef = _viewContainerRef;
          _this54._animationMode = _animationMode;
          _this54._hideToggle = false;
          /** An event emitted after the body's expansion animation happens. */

          _this54.afterExpand = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
          /** An event emitted after the body's collapse animation happens. */

          _this54.afterCollapse = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
          /** Stream that emits for changes in `@Input` properties. */

          _this54._inputChanges = new rxjs__WEBPACK_IMPORTED_MODULE_10__["Subject"]();
          /** ID for the associated header element. Used for a11y labelling. */

          _this54._headerId = "mat-expansion-panel-header-".concat(uniqueId++);
          /** Stream of body animation done events. */

          _this54._bodyAnimationDone = new rxjs__WEBPACK_IMPORTED_MODULE_10__["Subject"]();
          _this54.accordion = accordion;
          _this54._document = _document; // We need a Subject with distinctUntilChanged, because the `done` event
          // fires twice on some browsers. See https://github.com/angular/angular/issues/24084

          _this54._bodyAnimationDone.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_7__["distinctUntilChanged"])(function (x, y) {
            return x.fromState === y.fromState && x.toState === y.toState;
          })).subscribe(function (event) {
            if (event.fromState !== 'void') {
              if (event.toState === 'expanded') {
                _this54.afterExpand.emit();
              } else if (event.toState === 'collapsed') {
                _this54.afterCollapse.emit();
              }
            }
          });

          if (defaultOptions) {
            _this54.hideToggle = defaultOptions.hideToggle;
          }

          return _this54;
        }
        /** Whether the toggle indicator should be hidden. */


        _createClass(MatExpansionPanel, [{
          key: "_hasSpacing",

          /** Determines whether the expansion panel should have spacing between it and its siblings. */
          value: function _hasSpacing() {
            if (this.accordion) {
              return this.expanded && this.accordion.displayMode === 'default';
            }

            return false;
          }
          /** Gets the expanded state string. */

        }, {
          key: "_getExpandedState",
          value: function _getExpandedState() {
            return this.expanded ? 'expanded' : 'collapsed';
          }
          /** Toggles the expanded state of the expansion panel. */

        }, {
          key: "toggle",
          value: function toggle() {
            this.expanded = !this.expanded;
          }
          /** Sets the expanded state of the expansion panel to false. */

        }, {
          key: "close",
          value: function close() {
            this.expanded = false;
          }
          /** Sets the expanded state of the expansion panel to true. */

        }, {
          key: "open",
          value: function open() {
            this.expanded = true;
          }
        }, {
          key: "ngAfterContentInit",
          value: function ngAfterContentInit() {
            var _this55 = this;

            if (this._lazyContent) {
              // Render the content as soon as the panel becomes open.
              this.opened.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_7__["startWith"])(null), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_7__["filter"])(function () {
                return _this55.expanded && !_this55._portal;
              }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_7__["take"])(1)).subscribe(function () {
                _this55._portal = new _angular_cdk_portal__WEBPACK_IMPORTED_MODULE_1__["TemplatePortal"](_this55._lazyContent._template, _this55._viewContainerRef);
              });
            }
          }
        }, {
          key: "ngOnChanges",
          value: function ngOnChanges(changes) {
            this._inputChanges.next(changes);
          }
        }, {
          key: "ngOnDestroy",
          value: function ngOnDestroy() {
            _get(_getPrototypeOf(MatExpansionPanel.prototype), "ngOnDestroy", this).call(this);

            this._bodyAnimationDone.complete();

            this._inputChanges.complete();
          }
          /** Checks whether the expansion panel's content contains the currently-focused element. */

        }, {
          key: "_containsFocus",
          value: function _containsFocus() {
            if (this._body) {
              var focusedElement = this._document.activeElement;
              var bodyElement = this._body.nativeElement;
              return focusedElement === bodyElement || bodyElement.contains(focusedElement);
            }

            return false;
          }
        }, {
          key: "hideToggle",
          get: function get() {
            return this._hideToggle || this.accordion && this.accordion.hideToggle;
          },
          set: function set(value) {
            this._hideToggle = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_5__["coerceBooleanProperty"])(value);
          }
          /** The position of the expansion indicator. */

        }, {
          key: "togglePosition",
          get: function get() {
            return this._togglePosition || this.accordion && this.accordion.togglePosition;
          },
          set: function set(value) {
            this._togglePosition = value;
          }
        }]);

        return MatExpansionPanel;
      }(_angular_cdk_accordion__WEBPACK_IMPORTED_MODULE_0__["CdkAccordionItem"]);

      MatExpansionPanel.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"],
        args: [{
          selector: 'mat-expansion-panel',
          exportAs: 'matExpansionPanel',
          template: "<ng-content select=\"mat-expansion-panel-header\"></ng-content>\n<div class=\"mat-expansion-panel-content\"\n     role=\"region\"\n     [@bodyExpansion]=\"_getExpandedState()\"\n     (@bodyExpansion.done)=\"_bodyAnimationDone.next($event)\"\n     [attr.aria-labelledby]=\"_headerId\"\n     [id]=\"id\"\n     #body>\n  <div class=\"mat-expansion-panel-body\">\n    <ng-content></ng-content>\n    <ng-template [cdkPortalOutlet]=\"_portal\"></ng-template>\n  </div>\n  <ng-content select=\"mat-action-row\"></ng-content>\n</div>\n",
          encapsulation: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ViewEncapsulation"].None,
          changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ChangeDetectionStrategy"].OnPush,
          inputs: ['disabled', 'expanded'],
          outputs: ['opened', 'closed', 'expandedChange'],
          animations: [matExpansionAnimations.bodyExpansion],
          providers: [// Provide MatAccordion as undefined to prevent nested expansion panels from registering
          // to the same accordion.
          {
            provide: MAT_ACCORDION,
            useValue: ɵ0
          }],
          host: {
            'class': 'mat-expansion-panel',
            '[class.mat-expanded]': 'expanded',
            '[class._mat-animation-noopable]': '_animationMode === "NoopAnimations"',
            '[class.mat-expansion-panel-spacing]': '_hasSpacing()'
          },
          styles: [".mat-expansion-panel{box-sizing:content-box;display:block;margin:0;border-radius:4px;overflow:hidden;transition:margin 225ms cubic-bezier(0.4, 0, 0.2, 1),box-shadow 280ms cubic-bezier(0.4, 0, 0.2, 1);position:relative}.mat-accordion .mat-expansion-panel:not(.mat-expanded),.mat-accordion .mat-expansion-panel:not(.mat-expansion-panel-spacing){border-radius:0}.mat-accordion .mat-expansion-panel:first-of-type{border-top-right-radius:4px;border-top-left-radius:4px}.mat-accordion .mat-expansion-panel:last-of-type{border-bottom-right-radius:4px;border-bottom-left-radius:4px}.cdk-high-contrast-active .mat-expansion-panel{outline:solid 1px}.mat-expansion-panel.ng-animate-disabled,.ng-animate-disabled .mat-expansion-panel,.mat-expansion-panel._mat-animation-noopable{transition:none}.mat-expansion-panel-content{display:flex;flex-direction:column;overflow:visible}.mat-expansion-panel-body{padding:0 24px 16px}.mat-expansion-panel-spacing{margin:16px 0}.mat-accordion>.mat-expansion-panel-spacing:first-child,.mat-accordion>*:first-child:not(.mat-expansion-panel) .mat-expansion-panel-spacing{margin-top:0}.mat-accordion>.mat-expansion-panel-spacing:last-child,.mat-accordion>*:last-child:not(.mat-expansion-panel) .mat-expansion-panel-spacing{margin-bottom:0}.mat-action-row{border-top-style:solid;border-top-width:1px;display:flex;flex-direction:row;justify-content:flex-end;padding:16px 8px 16px 24px}.mat-action-row button.mat-button-base,.mat-action-row button.mat-mdc-button-base{margin-left:8px}[dir=rtl] .mat-action-row button.mat-button-base,[dir=rtl] .mat-action-row button.mat-mdc-button-base{margin-left:0;margin-right:8px}\n"]
        }]
      }];

      MatExpansionPanel.ctorParameters = function () {
        return [{
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Optional"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["SkipSelf"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Inject"],
            args: [MAT_ACCORDION]
          }]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ChangeDetectorRef"]
        }, {
          type: _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_12__["UniqueSelectionDispatcher"]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ViewContainerRef"]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Inject"],
            args: [_angular_common__WEBPACK_IMPORTED_MODULE_2__["DOCUMENT"]]
          }]
        }, {
          type: String,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Optional"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Inject"],
            args: [_angular_platform_browser_animations__WEBPACK_IMPORTED_MODULE_9__["ANIMATION_MODULE_TYPE"]]
          }]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Inject"],
            args: [MAT_EXPANSION_PANEL_DEFAULT_OPTIONS]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Optional"]
          }]
        }];
      };

      MatExpansionPanel.propDecorators = {
        hideToggle: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"]
        }],
        togglePosition: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"]
        }],
        afterExpand: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Output"]
        }],
        afterCollapse: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Output"]
        }],
        _lazyContent: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ContentChild"],
          args: [MatExpansionPanelContent]
        }],
        _body: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ViewChild"],
          args: ['body']
        }]
      };
      /**
       * Actions of a `<mat-expansion-panel>`.
       */

      var MatExpansionPanelActionRow = function MatExpansionPanelActionRow() {
        _classCallCheck(this, MatExpansionPanelActionRow);
      };

      MatExpansionPanelActionRow.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Directive"],
        args: [{
          selector: 'mat-action-row',
          host: {
            "class": 'mat-action-row'
          }
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
       * Header element of a `<mat-expansion-panel>`.
       */

      var MatExpansionPanelHeader = /*#__PURE__*/function () {
        function MatExpansionPanelHeader(panel, _element, _focusMonitor, _changeDetectorRef, defaultOptions, _animationMode) {
          var _this56 = this;

          _classCallCheck(this, MatExpansionPanelHeader);

          this.panel = panel;
          this._element = _element;
          this._focusMonitor = _focusMonitor;
          this._changeDetectorRef = _changeDetectorRef;
          this._animationMode = _animationMode;
          this._parentChangeSubscription = rxjs__WEBPACK_IMPORTED_MODULE_10__["Subscription"].EMPTY;
          var accordionHideToggleChange = panel.accordion ? panel.accordion._stateChanges.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_7__["filter"])(function (changes) {
            return !!(changes['hideToggle'] || changes['togglePosition']);
          })) : rxjs__WEBPACK_IMPORTED_MODULE_10__["EMPTY"]; // Since the toggle state depends on an @Input on the panel, we
          // need to subscribe and trigger change detection manually.

          this._parentChangeSubscription = Object(rxjs__WEBPACK_IMPORTED_MODULE_10__["merge"])(panel.opened, panel.closed, accordionHideToggleChange, panel._inputChanges.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_7__["filter"])(function (changes) {
            return !!(changes['hideToggle'] || changes['disabled'] || changes['togglePosition']);
          }))).subscribe(function () {
            return _this56._changeDetectorRef.markForCheck();
          }); // Avoids focus being lost if the panel contained the focused element and was closed.

          panel.closed.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_7__["filter"])(function () {
            return panel._containsFocus();
          })).subscribe(function () {
            return _focusMonitor.focusVia(_element, 'program');
          });

          if (defaultOptions) {
            this.expandedHeight = defaultOptions.expandedHeight;
            this.collapsedHeight = defaultOptions.collapsedHeight;
          }
        }
        /**
         * Whether the associated panel is disabled. Implemented as a part of `FocusableOption`.
         * @docs-private
         */


        _createClass(MatExpansionPanelHeader, [{
          key: "_toggle",

          /** Toggles the expanded state of the panel. */
          value: function _toggle() {
            if (!this.disabled) {
              this.panel.toggle();
            }
          }
          /** Gets whether the panel is expanded. */

        }, {
          key: "_isExpanded",
          value: function _isExpanded() {
            return this.panel.expanded;
          }
          /** Gets the expanded state string of the panel. */

        }, {
          key: "_getExpandedState",
          value: function _getExpandedState() {
            return this.panel._getExpandedState();
          }
          /** Gets the panel id. */

        }, {
          key: "_getPanelId",
          value: function _getPanelId() {
            return this.panel.id;
          }
          /** Gets the toggle position for the header. */

        }, {
          key: "_getTogglePosition",
          value: function _getTogglePosition() {
            return this.panel.togglePosition;
          }
          /** Gets whether the expand indicator should be shown. */

        }, {
          key: "_showToggle",
          value: function _showToggle() {
            return !this.panel.hideToggle && !this.panel.disabled;
          }
          /**
           * Gets the current height of the header. Null if no custom height has been
           * specified, and if the default height from the stylesheet should be used.
           */

        }, {
          key: "_getHeaderHeight",
          value: function _getHeaderHeight() {
            var isExpanded = this._isExpanded();

            if (isExpanded && this.expandedHeight) {
              return this.expandedHeight;
            } else if (!isExpanded && this.collapsedHeight) {
              return this.collapsedHeight;
            }

            return null;
          }
          /** Handle keydown event calling to toggle() if appropriate. */

        }, {
          key: "_keydown",
          value: function _keydown(event) {
            switch (event.keyCode) {
              // Toggle for space and enter keys.
              case _angular_cdk_keycodes__WEBPACK_IMPORTED_MODULE_8__["SPACE"]:
              case _angular_cdk_keycodes__WEBPACK_IMPORTED_MODULE_8__["ENTER"]:
                if (!Object(_angular_cdk_keycodes__WEBPACK_IMPORTED_MODULE_8__["hasModifierKey"])(event)) {
                  event.preventDefault();

                  this._toggle();
                }

                break;

              default:
                if (this.panel.accordion) {
                  this.panel.accordion._handleHeaderKeydown(event);
                }

                return;
            }
          }
          /**
           * Focuses the panel header. Implemented as a part of `FocusableOption`.
           * @param origin Origin of the action that triggered the focus.
           * @docs-private
           */

        }, {
          key: "focus",
          value: function focus() {
            var origin = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'program';
            var options = arguments.length > 1 ? arguments[1] : undefined;

            this._focusMonitor.focusVia(this._element, origin, options);
          }
        }, {
          key: "ngAfterViewInit",
          value: function ngAfterViewInit() {
            var _this57 = this;

            this._focusMonitor.monitor(this._element).subscribe(function (origin) {
              if (origin && _this57.panel.accordion) {
                _this57.panel.accordion._handleHeaderFocus(_this57);
              }
            });
          }
        }, {
          key: "ngOnDestroy",
          value: function ngOnDestroy() {
            this._parentChangeSubscription.unsubscribe();

            this._focusMonitor.stopMonitoring(this._element);
          }
        }, {
          key: "disabled",
          get: function get() {
            return this.panel.disabled;
          }
        }]);

        return MatExpansionPanelHeader;
      }();

      MatExpansionPanelHeader.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"],
        args: [{
          selector: 'mat-expansion-panel-header',
          template: "<span class=\"mat-content\">\n  <ng-content select=\"mat-panel-title\"></ng-content>\n  <ng-content select=\"mat-panel-description\"></ng-content>\n  <ng-content></ng-content>\n</span>\n<span [@indicatorRotate]=\"_getExpandedState()\" *ngIf=\"_showToggle()\"\n      class=\"mat-expansion-indicator\"></span>\n",
          encapsulation: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ViewEncapsulation"].None,
          changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ChangeDetectionStrategy"].OnPush,
          animations: [matExpansionAnimations.indicatorRotate],
          host: {
            'class': 'mat-expansion-panel-header mat-focus-indicator',
            'role': 'button',
            '[attr.id]': 'panel._headerId',
            '[attr.tabindex]': 'disabled ? -1 : 0',
            '[attr.aria-controls]': '_getPanelId()',
            '[attr.aria-expanded]': '_isExpanded()',
            '[attr.aria-disabled]': 'panel.disabled',
            '[class.mat-expanded]': '_isExpanded()',
            '[class.mat-expansion-toggle-indicator-after]': "_getTogglePosition() === 'after'",
            '[class.mat-expansion-toggle-indicator-before]': "_getTogglePosition() === 'before'",
            '[class._mat-animation-noopable]': '_animationMode === "NoopAnimations"',
            '[style.height]': '_getHeaderHeight()',
            '(click)': '_toggle()',
            '(keydown)': '_keydown($event)'
          },
          styles: [".mat-expansion-panel-header{display:flex;flex-direction:row;align-items:center;padding:0 24px;border-radius:inherit;transition:height 225ms cubic-bezier(0.4, 0, 0.2, 1)}.mat-expansion-panel-header._mat-animation-noopable{transition:none}.mat-expansion-panel-header:focus,.mat-expansion-panel-header:hover{outline:none}.mat-expansion-panel-header.mat-expanded:focus,.mat-expansion-panel-header.mat-expanded:hover{background:inherit}.mat-expansion-panel-header:not([aria-disabled=true]){cursor:pointer}.mat-expansion-panel-header.mat-expansion-toggle-indicator-before{flex-direction:row-reverse}.mat-expansion-panel-header.mat-expansion-toggle-indicator-before .mat-expansion-indicator{margin:0 16px 0 0}[dir=rtl] .mat-expansion-panel-header.mat-expansion-toggle-indicator-before .mat-expansion-indicator{margin:0 0 0 16px}.mat-content{display:flex;flex:1;flex-direction:row;overflow:hidden}.mat-expansion-panel-header-title,.mat-expansion-panel-header-description{display:flex;flex-grow:1;margin-right:16px}[dir=rtl] .mat-expansion-panel-header-title,[dir=rtl] .mat-expansion-panel-header-description{margin-right:0;margin-left:16px}.mat-expansion-panel-header-description{flex-grow:2}.mat-expansion-indicator::after{border-style:solid;border-width:0 2px 2px 0;content:\"\";display:inline-block;padding:3px;transform:rotate(45deg);vertical-align:middle}\n"]
        }]
      }];

      MatExpansionPanelHeader.ctorParameters = function () {
        return [{
          type: MatExpansionPanel,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Host"]
          }]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ElementRef"]
        }, {
          type: _angular_cdk_a11y__WEBPACK_IMPORTED_MODULE_6__["FocusMonitor"]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ChangeDetectorRef"]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Inject"],
            args: [MAT_EXPANSION_PANEL_DEFAULT_OPTIONS]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Optional"]
          }]
        }, {
          type: String,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Optional"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Inject"],
            args: [_angular_platform_browser_animations__WEBPACK_IMPORTED_MODULE_9__["ANIMATION_MODULE_TYPE"]]
          }]
        }];
      };

      MatExpansionPanelHeader.propDecorators = {
        expandedHeight: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"]
        }],
        collapsedHeight: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"]
        }]
      };
      /**
       * Description element of a `<mat-expansion-panel-header>`.
       */

      var MatExpansionPanelDescription = function MatExpansionPanelDescription() {
        _classCallCheck(this, MatExpansionPanelDescription);
      };

      MatExpansionPanelDescription.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Directive"],
        args: [{
          selector: 'mat-panel-description',
          host: {
            "class": 'mat-expansion-panel-header-description'
          }
        }]
      }];
      /**
       * Title element of a `<mat-expansion-panel-header>`.
       */

      var MatExpansionPanelTitle = function MatExpansionPanelTitle() {
        _classCallCheck(this, MatExpansionPanelTitle);
      };

      MatExpansionPanelTitle.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Directive"],
        args: [{
          selector: 'mat-panel-title',
          host: {
            "class": 'mat-expansion-panel-header-title'
          }
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
       * Directive for a Material Design Accordion.
       */

      var MatAccordion = /*#__PURE__*/function (_angular_cdk_accordio2) {
        _inherits(MatAccordion, _angular_cdk_accordio2);

        var _super2 = _createSuper(MatAccordion);

        function MatAccordion() {
          var _this58;

          _classCallCheck(this, MatAccordion);

          _this58 = _super2.apply(this, arguments);
          /** Headers belonging to this accordion. */

          _this58._ownHeaders = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["QueryList"]();
          _this58._hideToggle = false;
          /**
           * Display mode used for all expansion panels in the accordion. Currently two display
           * modes exist:
           *  default - a gutter-like spacing is placed around any expanded panel, placing the expanded
           *     panel at a different elevation from the rest of the accordion.
           *  flat - no spacing is placed around expanded panels, showing all panels at the same
           *     elevation.
           */

          _this58.displayMode = 'default';
          /** The position of the expansion indicator. */

          _this58.togglePosition = 'after';
          return _this58;
        }
        /** Whether the expansion indicator should be hidden. */


        _createClass(MatAccordion, [{
          key: "ngAfterContentInit",
          value: function ngAfterContentInit() {
            var _this59 = this;

            this._headers.changes.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_7__["startWith"])(this._headers)).subscribe(function (headers) {
              _this59._ownHeaders.reset(headers.filter(function (header) {
                return header.panel.accordion === _this59;
              }));

              _this59._ownHeaders.notifyOnChanges();
            });

            this._keyManager = new _angular_cdk_a11y__WEBPACK_IMPORTED_MODULE_6__["FocusKeyManager"](this._ownHeaders).withWrap().withHomeAndEnd();
          }
          /** Handles keyboard events coming in from the panel headers. */

        }, {
          key: "_handleHeaderKeydown",
          value: function _handleHeaderKeydown(event) {
            this._keyManager.onKeydown(event);
          }
        }, {
          key: "_handleHeaderFocus",
          value: function _handleHeaderFocus(header) {
            this._keyManager.updateActiveItem(header);
          }
        }, {
          key: "ngOnDestroy",
          value: function ngOnDestroy() {
            _get(_getPrototypeOf(MatAccordion.prototype), "ngOnDestroy", this).call(this);

            this._ownHeaders.destroy();
          }
        }, {
          key: "hideToggle",
          get: function get() {
            return this._hideToggle;
          },
          set: function set(show) {
            this._hideToggle = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_5__["coerceBooleanProperty"])(show);
          }
        }]);

        return MatAccordion;
      }(_angular_cdk_accordion__WEBPACK_IMPORTED_MODULE_0__["CdkAccordion"]);

      MatAccordion.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Directive"],
        args: [{
          selector: 'mat-accordion',
          exportAs: 'matAccordion',
          inputs: ['multi'],
          providers: [{
            provide: MAT_ACCORDION,
            useExisting: MatAccordion
          }],
          host: {
            "class": 'mat-accordion',
            // Class binding which is only used by the test harness as there is no other
            // way for the harness to detect if multiple panel support is enabled.
            '[class.mat-accordion-multi]': 'this.multi'
          }
        }]
      }];
      MatAccordion.propDecorators = {
        _headers: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ContentChildren"],
          args: [MatExpansionPanelHeader, {
            descendants: true
          }]
        }],
        hideToggle: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"]
        }],
        displayMode: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"]
        }],
        togglePosition: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"]
        }]
      };
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      var MatExpansionModule = function MatExpansionModule() {
        _classCallCheck(this, MatExpansionModule);
      };

      MatExpansionModule.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["NgModule"],
        args: [{
          imports: [_angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"], _angular_material_core__WEBPACK_IMPORTED_MODULE_4__["MatCommonModule"], _angular_cdk_accordion__WEBPACK_IMPORTED_MODULE_0__["CdkAccordionModule"], _angular_cdk_portal__WEBPACK_IMPORTED_MODULE_1__["PortalModule"]],
          exports: [MatAccordion, MatExpansionPanel, MatExpansionPanelActionRow, MatExpansionPanelHeader, MatExpansionPanelTitle, MatExpansionPanelDescription, MatExpansionPanelContent],
          declarations: [MatAccordion, MatExpansionPanel, MatExpansionPanelActionRow, MatExpansionPanelHeader, MatExpansionPanelTitle, MatExpansionPanelDescription, MatExpansionPanelContent]
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
      //# sourceMappingURL=expansion.js.map

      /***/
    },

    /***/
    "pIXh":
    /*!******************************************************************************************************************************!*\
      !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/scenarios/pages/scenarios-index/scenarios-index.component.html ***!
      \******************************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function pIXh(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "<vex-page-layout>\n  <div class=\"w-full h-full flex flex-col\">\n    <div class=\"px-gutter pt-6 pb-20 vex-layout-theme flex-none\">\n      <div class=\"flex items-center\">\n        <vex-page-layout-header fxLayout=\"column\" fxLayoutAlign=\"center start\">\n          <div class=\"w-full flex flex-col sm:flex-row justify-between\">\n            <div>\n              <!-- <h1 class=\"title mt-0 mb-1\">{{ project.name }}</h1> -->\n              <vex-breadcrumbs [crumbs]=\"crumbs\"></vex-breadcrumbs>\n            </div>\n          </div>\n        </vex-page-layout-header>\n      </div>\n    </div>\n\n    <div class=\"-mt-14 pt-0 overflow-hidden flex\">\n\n      <mat-drawer-container class=\"bg-transparent flex-auto flex\">\n        <mat-drawer [(opened)]=\"menuOpen\" mode=\"over\">\n          <scenarios-table-menu (get)=\"filterScenarios($event)\"\n                                (create)=\"openCreateDialog()\"\n                                class=\"sm:hidden\"></scenarios-table-menu>\n        </mat-drawer>\n        <mat-drawer-content class=\"p-gutter pt-0 flex-auto flex items-start\">\n          <scenarios-table-menu\n            (filter)=\"filterScenarios($event)\"\n            (create)=\"openCreateDialog()\"\n            class=\"hidden sm:block mr-6\">\n          </scenarios-table-menu>\n\n          <div class=\"card h-full overflow-hidden flex-auto\">\n            <data-table\n              [buttonsTemplate]=\"buttonsTemplate\"\n              [columns]=\"tableColumns\"\n              [data]=\"scenarios\"\n              [length]=\"totalScenarios\"\n              [pageSize]=\"pageSize\"\n              [page]=\"page\"\n              [resourceName]=\"'scenario'\"\n              [sortBy]=\"indexParams.sort_by\"\n              [sortOrder]=\"indexParams.sort_order\"\n              (toggleStar)=\"toggleScenarioStar($event)\"\n              (delete)=\"deleteScenario($event)\"\n              (paginate)=\"handlePaginateChange($event)\"\n              (search)=\"searchScenarios($event)\"\n              (sort)=\"sortScenarios($event)\"\n              (view)=\"viewScenario($event)\"\n            >\n            </data-table>\n          </div>\n        </mat-drawer-content>\n\n      </mat-drawer-container>\n    </div>\n  </div>\n</vex-page-layout>\n\n<ng-template #buttonsTemplate let-scenario=\"row\">\n  <button mat-menu-item (click)=\"openEditDialog(scenario)\">\n    <mat-icon [icIcon]=\"icons.icEdit\"></mat-icon>\n    <span>Edit</span>\n  </button>\n\n  <button mat-menu-item (click)=\"downloadScenario(scenario.id)\">\n    <mat-icon [icIcon]=\"icons.icCloudDownload\"></mat-icon>\n    <span>Download</span>\n  </button>\n</ng-template>\n";
      /***/
    },

    /***/
    "pXOW":
    /*!*************************************************************************!*\
      !*** ./src/app/modules/scenarios/services/scenario-resolver.service.ts ***!
      \*************************************************************************/

    /*! exports provided: ScenarioResolver */

    /***/
    function pXOW(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ScenarioResolver", function () {
        return ScenarioResolver;
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


      var _core_http_scenario_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @core/http/scenario-resource.service */
      "3Ncz");

      var ScenarioResolver = /*#__PURE__*/function () {
        function ScenarioResolver(scenarioResource) {
          _classCallCheck(this, ScenarioResolver);

          this.scenarioResource = scenarioResource;
        }

        _createClass(ScenarioResolver, [{
          key: "resolve",
          value: function resolve(route) {
            return this.scenarioResource.show(route.params.scenario_id, {
              project_id: route.queryParams.project_id
            });
          }
        }]);

        return ScenarioResolver;
      }();

      ScenarioResolver.ctorParameters = function () {
        return [{
          type: _core_http_scenario_resource_service__WEBPACK_IMPORTED_MODULE_2__["ScenarioResource"]
        }];
      };

      ScenarioResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], ScenarioResolver);
      /***/
    },

    /***/
    "paqc":
    /*!*****************************************************************!*\
      !*** ./node_modules/@iconify/icons-ic/twotone-notifications.js ***!
      \*****************************************************************/

    /*! no static exports found */

    /***/
    function paqc(module, exports) {
      var data = {
        "body": "<path opacity=\".3\" d=\"M12 6.5c-2.49 0-4 2.02-4 4.5v6h8v-6c0-2.48-1.51-4.5-4-4.5z\" fill=\"currentColor\"/><path d=\"M12 22c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2zm6-6v-5c0-3.07-1.63-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.64 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2zm-2 1H8v-6c0-2.48 1.51-4.5 4-4.5s4 2.02 4 4.5v6z\" fill=\"currentColor\"/>",
        "width": 24,
        "height": 24
      };
      exports.__esModule = true;
      exports["default"] = data;
      /***/
    },

    /***/
    "q9PC":
    /*!****************************************************************************************!*\
      !*** ./src/app/modules/scenarios/pages/scenario-details/scenario-details.component.ts ***!
      \****************************************************************************************/

    /*! exports provided: ScenarioDetailsComponent */

    /***/
    function q9PC(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ScenarioDetailsComponent", function () {
        return ScenarioDetailsComponent;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _raw_loader_scenario_details_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! raw-loader!./scenario-details.component.html */
      "j/wk");
      /* harmony import */


      var _scenario_details_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! ./scenario-details.component.scss */
      "ZplM");
      /* harmony import */


      var _angular_common__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/common */
      "SVse");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_forms__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/forms */
      "s7LF");
      /* harmony import */


      var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/material/dialog */
      "iELJ");
      /* harmony import */


      var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @angular/material/form-field */
      "Q2Ze");
      /* harmony import */


      var _angular_router__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @angular/router */
      "iInd");
      /* harmony import */


      var _vex_animations__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @vex/animations */
      "ORuP");
      /* harmony import */


      var _core_http_request_resource_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @core/http/request-resource.service */
      "4/Wj");
      /* harmony import */


      var _core_utils_file_service__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @core/utils/file.service */
      "EGFe");
      /* harmony import */


      var _data_schema__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @data/schema */
      "V99k");
      /* harmony import */


      var _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @projects/services/project-data.service */
      "oyjd");
      /* harmony import */


      var _requests_components_scrumboard_dialog_scrumboard_dialog_component__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! @requests/components/scrumboard-dialog/scrumboard-dialog.component */
      "QgCS");
      /* harmony import */


      var _components_requests_create_requests_create_component__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! ./components/requests-create/requests-create.component */
      "hnRQ");
      /* harmony import */


      var _services_requests_data_service__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(
      /*! ./services/requests-data.service */
      "WSkv");
      /* harmony import */


      var _services_scenario_details_icons_service__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(
      /*! ./services/scenario-details-icons.service */
      "5euU");

      var ScenarioDetailsComponent = /*#__PURE__*/function () {
        function ScenarioDetailsComponent(icons, activatedRoute, dialog, location, file, projectDataService, requestResource, requestsDataService, route, router) {
          _classCallCheck(this, ScenarioDetailsComponent);

          this.icons = icons;
          this.activatedRoute = activatedRoute;
          this.dialog = dialog;
          this.location = location;
          this.file = file;
          this.projectDataService = projectDataService;
          this.requestResource = requestResource;
          this.requestsDataService = requestsDataService;
          this.route = route;
          this.router = router;
          this.layoutCtrl = new _angular_forms__WEBPACK_IMPORTED_MODULE_5__["FormControl"]('boxed');
          this.crumbs = [];
          this.indexParams = {};
          this.page = 0;
          this.pageSize = 10;
        }

        _createClass(ScenarioDetailsComponent, [{
          key: "ngOnInit",
          value: function ngOnInit() {
            var routeSnapshot = this.route.snapshot;
            this.projectId = routeSnapshot.queryParams.project_id;
            this.scenario = routeSnapshot.data.scenario;
            var requests = routeSnapshot.data.requests;
            this.requests = requests.list;
            this.totalRequests = requests.total;
            this.requestsDataService.set(this.requests.map(function (request) {
              return new _data_schema__WEBPACK_IMPORTED_MODULE_12__["Request"](request);
            }));
            this.indexParams = Object.assign({}, routeSnapshot.queryParams);
            this.indexParams.page = this.indexParams.page || 0;
            this.indexParams.size = this.indexParams.size || 20;
            this.page = this.indexParams.page;
            this.pageSize = this.indexParams.size;
            this.filter = this.indexParams.filter;
            this.buildBreadcrumbs();
            this.tableColumns = this.buildTableColumns();
          }
        }, {
          key: "ngAfterViewInit",
          value: function ngAfterViewInit() {} // API Access

        }, {
          key: "createRequest",
          value: function createRequest(data) {
            var _this60 = this;

            var snapshot = this.route.snapshot;
            var project_id = snapshot.queryParams.project_id;
            data.append('project_id', project_id);
            this.requestResource.create(data).subscribe(function (res) {
              var clone = _this60.requests.slice();

              clone.unshift(res);
              _this60.requests = clone;
            }, function (error) {});
          }
        }, {
          key: "getRequests",
          value: function getRequests() {
            var _this61 = this;

            var params = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : Object.assign({}, this.indexParams);
            var snapshot = this.route.snapshot;
            var project_id = snapshot.queryParams.project_id;
            params.project_id = project_id;
            params.scenario_id = this.scenario.id;
            this.requestResource.index(params).subscribe(function (res) {
              _this61.requests = res.list;
              _this61.totalRequests = res.total;

              _this61.requestsDataService.set(_this61.requests.map(function (request) {
                return new _data_schema__WEBPACK_IMPORTED_MODULE_12__["Request"](request);
              }));

              delete params.scenario_id;

              _this61.updateUrlQueryParams(params);
            }, function (error) {});
          }
        }, {
          key: "destroyRequest",
          value: function destroyRequest(requestId) {
            var _this62 = this;

            this.requestResource.destroy(requestId).subscribe(function (res) {
              var clone = _this62.requests.filter(function (request) {
                return request.id !== requestId;
              });

              for (var i = 0; i < clone.length; ++i) {
                clone[i].position = i;
              }

              _this62.requests = clone;
            });
          }
        }, {
          key: "sortRequests",
          value: function sortRequests(event) {
            var column = event.active;
            var direction = event.direction; // desc or asc

            if (!direction) {
              delete this.indexParams.sort_by;
              delete this.indexParams.sort_order;
            } else {
              this.indexParams.sort_by = column;
              this.indexParams.sort_order = direction;
            }

            this.getRequests();
          }
        }, {
          key: "searchRequests",
          value: function searchRequests(queryString) {
            var snapshot = this.route.snapshot;
            var project_id = snapshot.queryParams.project_id;
            this.indexParams.page = 0;
            this.page = 0;

            if (!queryString.length) {
              delete this.indexParams.q;
            } else {
              this.indexParams.q = queryString;
            }

            this.getRequests();
          } // View Access

        }, {
          key: "viewRequest",
          value: function viewRequest(requestId) {
            var request = this.requests.find(function (r) {
              return r.id === requestId;
            });
            this.dialog.open(_requests_components_scrumboard_dialog_scrumboard_dialog_component__WEBPACK_IMPORTED_MODULE_14__["ScrumboardDialogComponent"], {
              data: {
                request: request
              },
              width: '750px',
              maxWidth: '100%',
              disableClose: true
            });
          }
        }, {
          key: "editRequest",
          value: function editRequest(requestId) {
            var path = this.file.join(location.pathname, '/requests', requestId);
            var snapshot = this.route.snapshot;
            this.router.navigate([path], {
              queryParams: {
                project_id: snapshot.queryParams.project_id
              }
            });
          }
        }, {
          key: "showEndpoint",
          value: function showEndpoint(request) {
            var path = this.file.join('/endpoints', request.rollupId);
            var snapshot = this.route.snapshot;
            this.router.navigate([path], {
              queryParams: {
                project_id: snapshot.queryParams.project_id
              }
            });
          }
        }, {
          key: "openCreateDialog",
          value: function openCreateDialog() {
            var _this63 = this;

            var dialogRef = this.dialog.open(_components_requests_create_requests_create_component__WEBPACK_IMPORTED_MODULE_15__["RequestsCreateComponent"], {
              width: '600px'
            });
            var onCreateSub = dialogRef.componentInstance.onCreate.subscribe(function ($event) {
              _this63.createRequest($event);
            });
            dialogRef.afterClosed().subscribe(function (request) {
              onCreateSub.unsubscribe();
            });
          }
        }, {
          key: "showBuilder",
          value: function showBuilder() {
            var snapshot = this.route.snapshot;
            var path = "".concat(location.pathname, "/editor");
            this.router.navigate([path], {
              queryParams: {
                project_id: snapshot.queryParams.project_id
              }
            });
          }
        }, {
          key: "onComponentChange",
          value: function onComponentChange(change, row) {
            var requests = this.requestsDataService.requests;
            var index = requests.findIndex(function (c) {
              return c === row;
            });
            requests[index].components = change.value;
            this.requestsDataService.set(requests);
          }
          /*
           *
           * $event = {
           *   previousPageIndex: 0
           *   pageIndex: 0
           *   pageSize: 50
           *   length: 3
           * }
           *
           */

        }, {
          key: "handlePaginateChange",
          value: function handlePaginateChange($event) {
            var curIndex = this.page;
            var curSize = this.pageSize;
            var newIndex = $event.pageIndex;
            var newSize = $event.pageSize;

            if (curSize !== newSize) {
              this.pageSize = newSize;
            }

            if (curIndex != newIndex) {
              this.page = newIndex;
            }

            if (curIndex != newIndex || curSize !== newSize) {
              this.indexParams.page = newIndex;
              this.indexParams.size = newSize;
              this.getRequests();
            }
          } // Helpers

        }, {
          key: "updateUrlQueryParams",
          value: function updateUrlQueryParams(newQueryParams) {
            var queryParams = Object.assign({}, this.indexParams);
            Object.entries(newQueryParams).forEach(function (_ref17) {
              var _ref18 = _slicedToArray(_ref17, 2),
                  key = _ref18[0],
                  value = _ref18[1];

              queryParams[key] = value;
            });
            var url = this.router.createUrlTree([], {
              relativeTo: this.activatedRoute,
              queryParams: queryParams
            }).toString();
            this.location.go(url);
          }
        }, {
          key: "projectIdQuery",
          value: function projectIdQuery() {
            return {
              project_id: this.route.snapshot.queryParams.project_id
            };
          }
        }, {
          key: "endpointPath",
          value: function endpointPath(request) {
            if (!request.rollupId) {
              return '';
            }

            return this.file.join('/endpoints', request.rollupId);
          }
        }, {
          key: "buildBreadcrumbs",
          value: function buildBreadcrumbs() {
            var _this64 = this;

            // Build breadcrumb
            if (this.projectDataService.project) {
              this.crumbs.push({
                name: this.projectDataService.project.name
              });
            } else {
              var o = this.projectDataService.project$.subscribe(function (project) {
                if (project) {
                  _this64.crumbs.unshift({
                    name: project.name
                  });

                  o.unsubscribe();
                }
              });
              this.projectDataService.fetch(this.projectId);
            }

            this.crumbs.push({
              name: 'Scenarios',
              routerLink: ['/scenarios'],
              queryParams: this.route.snapshot.queryParams
            });
            this.crumbs.push({
              name: this.scenario.name
            });
          }
        }, {
          key: "buildTableColumns",
          value: function buildTableColumns() {
            var _this65 = this;

            return [{
              label: 'Checkbox',
              property: 'checkbox',
              type: 'checkbox',
              visible: true,
              canHide: false
            }, {
              label: 'Position',
              property: 'position',
              type: 'custom',
              visible: true,
              canHide: true,
              cssClasses: ['text-secondary']
            }, {
              label: 'Method',
              property: 'method',
              type: 'text',
              visible: true,
              canHide: true,
              cssClasses: ['text-secondary']
            }, {
              label: 'URL',
              property: 'url',
              type: 'text',
              visible: true,
              canHide: true,
              cssClasses: ['font-medium']
            }, {
              label: 'Endpoint',
              property: 'endpoint',
              type: 'link',
              visible: true,
              canHide: true,
              routerLink: function routerLink(request) {
                return [_this65.endpointPath(request)];
              },
              queryParams: function queryParams() {
                return _this65.projectIdQuery();
              }
            }, {
              label: 'Status',
              property: 'status',
              type: 'custom',
              visible: true,
              canHide: true
            }, {
              label: 'Latency',
              property: 'latency',
              type: 'custom',
              visible: true,
              canHide: true
            }, {
              label: 'Components',
              property: 'components',
              type: 'custom',
              visible: false,
              canHide: true
            }, {
              label: 'Created At',
              property: 'created_at',
              type: 'date',
              visible: false,
              canHide: true,
              cssClasses: ['text-secondary']
            }, {
              label: '',
              property: 'menu',
              type: 'menuButton',
              cssClasses: ['text-secondary', 'w-10'],
              visible: true,
              canHide: false
            }];
          }
        }, {
          key: "ngOnDestroy",
          value: function ngOnDestroy() {}
        }]);

        return ScenarioDetailsComponent;
      }();

      ScenarioDetailsComponent.ctorParameters = function () {
        return [{
          type: _services_scenario_details_icons_service__WEBPACK_IMPORTED_MODULE_17__["ScenarioDetailsIcons"]
        }, {
          type: _angular_router__WEBPACK_IMPORTED_MODULE_8__["ActivatedRoute"]
        }, {
          type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_6__["MatDialog"]
        }, {
          type: _angular_common__WEBPACK_IMPORTED_MODULE_3__["Location"]
        }, {
          type: _core_utils_file_service__WEBPACK_IMPORTED_MODULE_11__["FileService"]
        }, {
          type: _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_13__["ProjectDataService"]
        }, {
          type: _core_http_request_resource_service__WEBPACK_IMPORTED_MODULE_10__["RequestResource"]
        }, {
          type: _services_requests_data_service__WEBPACK_IMPORTED_MODULE_16__["RequestsDataService"]
        }, {
          type: _angular_router__WEBPACK_IMPORTED_MODULE_8__["ActivatedRoute"]
        }, {
          type: _angular_router__WEBPACK_IMPORTED_MODULE_8__["Router"]
        }];
      };

      ScenarioDetailsComponent.propDecorators = {
        tableColumns: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Input"]
        }]
      };
      ScenarioDetailsComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_4__["Component"])({
        selector: 'scenario-details',
        template: _raw_loader_scenario_details_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        animations: [_vex_animations__WEBPACK_IMPORTED_MODULE_9__["fadeInUp400ms"], _vex_animations__WEBPACK_IMPORTED_MODULE_9__["stagger40ms"]],
        providers: [{
          provide: _angular_material_form_field__WEBPACK_IMPORTED_MODULE_7__["MAT_FORM_FIELD_DEFAULT_OPTIONS"],
          useValue: {
            appearance: 'standard'
          }
        }],
        styles: [_scenario_details_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
      })], ScenarioDetailsComponent);
      /***/
    },

    /***/
    "tmbL":
    /*!*******************************************************************************************************!*\
      !*** ./src/app/modules/scenarios/pages/scenarios-builder/services/scenarios-builder-icons.service.ts ***!
      \*******************************************************************************************************/

    /*! exports provided: ScenariosBuilderIcons */

    /***/
    function tmbL(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ScenariosBuilderIcons", function () {
        return ScenariosBuilderIcons;
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


      var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-add */
      "7wwx");
      /* harmony import */


      var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_2__);
      /* harmony import */


      var _iconify_icons_ic_twotone_attach_file__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-attach-file */
      "1kq9");
      /* harmony import */


      var _iconify_icons_ic_twotone_attach_file__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_attach_file__WEBPACK_IMPORTED_MODULE_3__);
      /* harmony import */


      var _iconify_icons_ic_twotone_clear__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-clear */
      "/7Ly");
      /* harmony import */


      var _iconify_icons_ic_twotone_clear__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_clear__WEBPACK_IMPORTED_MODULE_4__);
      /* harmony import */


      var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-close */
      "5mnX");
      /* harmony import */


      var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_5__);
      /* harmony import */


      var _iconify_icons_ic_twotone_insert_comment__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-insert-comment */
      "PnnC");
      /* harmony import */


      var _iconify_icons_ic_twotone_insert_comment__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_insert_comment__WEBPACK_IMPORTED_MODULE_6__);
      /* harmony import */


      var _iconify_icons_ic_twotone_notifications__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-notifications */
      "paqc");
      /* harmony import */


      var _iconify_icons_ic_twotone_notifications__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_notifications__WEBPACK_IMPORTED_MODULE_7__);
      /* harmony import */


      var _iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-star */
      "bE8U");
      /* harmony import */


      var _iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_8__);
      /* harmony import */


      var _iconify_icons_ic_twotone_star_border__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-star-border */
      "PNSm");
      /* harmony import */


      var _iconify_icons_ic_twotone_star_border__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_star_border__WEBPACK_IMPORTED_MODULE_9__);

      var ScenariosBuilderIcons = function ScenariosBuilderIcons() {
        _classCallCheck(this, ScenariosBuilderIcons);

        this.icNotifications = _iconify_icons_ic_twotone_notifications__WEBPACK_IMPORTED_MODULE_7___default.a;
        this.icInsertComment = _iconify_icons_ic_twotone_insert_comment__WEBPACK_IMPORTED_MODULE_6___default.a;
        this.icAttachFile = _iconify_icons_ic_twotone_attach_file__WEBPACK_IMPORTED_MODULE_3___default.a;
        this.icAdd = _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_2___default.a;
        this.icClose = _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_5___default.a;
        this.icStar = _iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_8___default.a;
        this.icStarBorder = _iconify_icons_ic_twotone_star_border__WEBPACK_IMPORTED_MODULE_9___default.a;
        this.icClear = _iconify_icons_ic_twotone_clear__WEBPACK_IMPORTED_MODULE_4___default.a;
      };

      ScenariosBuilderIcons.ctorParameters = function () {
        return [];
      };

      ScenariosBuilderIcons = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], ScenariosBuilderIcons);
      /***/
    },

    /***/
    "xmhw":
    /*!*************************************************************************!*\
      !*** ./src/app/modules/scenarios/services/requests-resolver.service.ts ***!
      \*************************************************************************/

    /*! exports provided: RequestsResolver */

    /***/
    function xmhw(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "RequestsResolver", function () {
        return RequestsResolver;
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


      var _core_http_request_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @core/http/request-resource.service */
      "4/Wj");

      var RequestsResolver = /*#__PURE__*/function () {
        function RequestsResolver(requestResource) {
          _classCallCheck(this, RequestsResolver);

          this.requestResource = requestResource;
        }

        _createClass(RequestsResolver, [{
          key: "resolve",
          value: function resolve(route) {
            return this.requestResource.index({
              components: true,
              scenario_id: route.params.scenario_id
            });
          }
        }]);

        return RequestsResolver;
      }();

      RequestsResolver.ctorParameters = function () {
        return [{
          type: _core_http_request_resource_service__WEBPACK_IMPORTED_MODULE_2__["RequestResource"]
        }];
      };

      RequestsResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], RequestsResolver);
      /***/
    }
  }]);
})();
//# sourceMappingURL=scenarios-scenarios-module-es5.js.map