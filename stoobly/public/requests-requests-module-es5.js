(function () {
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

  function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

  function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

  function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

  (window["webpackJsonp"] = window["webpackJsonp"] || []).push([["requests-requests-module"], {
    /***/
    "+olZ":
    /*!*****************************************************!*\
      !*** ./src/app/modules/requests/requests.module.ts ***!
      \*****************************************************/

    /*! exports provided: RequestsModule */

    /***/
    function olZ(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "RequestsModule", function () {
        return RequestsModule;
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


      var _pages_request_details_request_details_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! ./pages/request-details/request-details.module */
      "9CFt");
      /* harmony import */


      var _pages_requests_index_requests_index_module__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! ./pages/requests-index/requests-index.module */
      "3yKH");
      /* harmony import */


      var _requests_routing_module__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! ./requests-routing.module */
      "bcfj");

      var RequestsModule = function RequestsModule() {
        _classCallCheck(this, RequestsModule);
      };

      RequestsModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _requests_routing_module__WEBPACK_IMPORTED_MODULE_5__["RequestsRoutingModule"], _pages_request_details_request_details_module__WEBPACK_IMPORTED_MODULE_3__["RequestDetailsModule"], _pages_requests_index_requests_index_module__WEBPACK_IMPORTED_MODULE_4__["RequestsIndexModule"]]
      })], RequestsModule);
      /***/
    },

    /***/
    "2FU7":
    /*!***********************************************************************************!*\
      !*** ./src/app/modules/requests/components/requests-edit/requests-edit.module.ts ***!
      \***********************************************************************************/

    /*! exports provided: RequestsEditModule */

    /***/
    function FU7(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "RequestsEditModule", function () {
        return RequestsEditModule;
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


      var _requests_edit_component__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! ./requests-edit.component */
      "VBGS");

      var RequestsEditModule = function RequestsEditModule() {
        _classCallCheck(this, RequestsEditModule);
      };

      RequestsEditModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_requests_edit_component__WEBPACK_IMPORTED_MODULE_14__["RequestsEditComponent"]],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _angular_material_dialog__WEBPACK_IMPORTED_MODULE_8__["MatDialogModule"], _angular_material_icon__WEBPACK_IMPORTED_MODULE_10__["MatIconModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"], _angular_material_input__WEBPACK_IMPORTED_MODULE_11__["MatInputModule"], _angular_material_divider__WEBPACK_IMPORTED_MODULE_9__["MatDividerModule"], _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_7__["MatDatepickerModule"], _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_13__["IconModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"], _angular_material_menu__WEBPACK_IMPORTED_MODULE_12__["MatMenuModule"], _angular_material_button__WEBPACK_IMPORTED_MODULE_5__["MatButtonModule"], _angular_material_core__WEBPACK_IMPORTED_MODULE_6__["MatNativeDateModule"]],
        entryComponents: [_requests_edit_component__WEBPACK_IMPORTED_MODULE_14__["RequestsEditComponent"]]
      })], RequestsEditModule);
      /***/
    },

    /***/
    "3yKH":
    /*!********************************************************************************!*\
      !*** ./src/app/modules/requests/pages/requests-index/requests-index.module.ts ***!
      \********************************************************************************/

    /*! exports provided: RequestsIndexModule */

    /***/
    function yKH(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "RequestsIndexModule", function () {
        return RequestsIndexModule;
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


      var _angular_material_core__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @angular/material/core */
      "UhP/");
      /* harmony import */


      var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @angular/material/dialog */
      "iELJ");
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


      var _angular_material_sidenav__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @angular/material/sidenav */
      "q7Ft");
      /* harmony import */


      var _angular_material_sort__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @angular/material/sort */
      "LUZP");
      /* harmony import */


      var _angular_material_table__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! @angular/material/table */
      "OaSA");
      /* harmony import */


      var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! @visurel/iconify-angular */
      "l+Q0");
      /* harmony import */


      var _vex_components_breadcrumbs_breadcrumbs_module__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(
      /*! @vex/components/breadcrumbs/breadcrumbs.module */
      "J0XA");
      /* harmony import */


      var _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(
      /*! @vex/components/page-layout/page-layout.module */
      "7lCJ");
      /* harmony import */


      var _vex_components_scrollbar_scrollbar_module__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(
      /*! @vex/components/scrollbar/scrollbar.module */
      "XVi8");
      /* harmony import */


      var _vex_directives_container_container_module__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(
      /*! @vex/directives/container/container.module */
      "68Yx");
      /* harmony import */


      var _shared_components_data_table_data_table_module__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(
      /*! @shared/components/data-table/data-table.module */
      "MqAd");
      /* harmony import */


      var _shared_components_label_label_module__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(
      /*! @shared/components/label/label.module */
      "W6U6");
      /* harmony import */


      var _requests_components_requests_create_requests_create_module__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(
      /*! @requests/components/requests-create/requests-create.module */
      "CTtz");
      /* harmony import */


      var _requests_components_requests_edit_requests_edit_module__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(
      /*! @requests/components/requests-edit/requests-edit.module */
      "2FU7");
      /* harmony import */


      var _requests_components_requests_search_requests_search_module__WEBPACK_IMPORTED_MODULE_24__ = __webpack_require__(
      /*! @requests/components/requests-search/requests-search.module */
      "KAKk");
      /* harmony import */


      var _components_requests_table_menu_requests_table_menu_component__WEBPACK_IMPORTED_MODULE_25__ = __webpack_require__(
      /*! ./components/requests-table-menu/requests-table-menu.component */
      "Q4Vm");
      /* harmony import */


      var _requests_index_component__WEBPACK_IMPORTED_MODULE_26__ = __webpack_require__(
      /*! ./requests-index.component */
      "Zf3l");
      /* harmony import */


      var _services_requests_index_icons_service__WEBPACK_IMPORTED_MODULE_27__ = __webpack_require__(
      /*! ./services/requests-index-icons.service */
      "DXlN");

      var RequestsIndexModule = function RequestsIndexModule() {
        _classCallCheck(this, RequestsIndexModule);
      };

      RequestsIndexModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_requests_index_component__WEBPACK_IMPORTED_MODULE_26__["RequestsIndexComponent"], _components_requests_table_menu_requests_table_menu_component__WEBPACK_IMPORTED_MODULE_25__["RequestsTableMenuComponent"]],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormsModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"], _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_15__["IconModule"], _angular_material_button__WEBPACK_IMPORTED_MODULE_5__["MatButtonModule"], _angular_material_table__WEBPACK_IMPORTED_MODULE_14__["MatTableModule"], _angular_material_paginator__WEBPACK_IMPORTED_MODULE_11__["MatPaginatorModule"], _angular_material_sort__WEBPACK_IMPORTED_MODULE_13__["MatSortModule"], _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_6__["MatCheckboxModule"], _angular_material_icon__WEBPACK_IMPORTED_MODULE_9__["MatIconModule"], _angular_material_menu__WEBPACK_IMPORTED_MODULE_10__["MatMenuModule"], _angular_material_core__WEBPACK_IMPORTED_MODULE_7__["MatRippleModule"], _angular_material_dialog__WEBPACK_IMPORTED_MODULE_8__["MatDialogModule"], _vex_components_scrollbar_scrollbar_module__WEBPACK_IMPORTED_MODULE_18__["ScrollbarModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"], _vex_directives_container_container_module__WEBPACK_IMPORTED_MODULE_19__["ContainerModule"], _angular_material_sidenav__WEBPACK_IMPORTED_MODULE_12__["MatSidenavModule"], _vex_components_breadcrumbs_breadcrumbs_module__WEBPACK_IMPORTED_MODULE_16__["BreadcrumbsModule"], _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_17__["PageLayoutModule"], _shared_components_data_table_data_table_module__WEBPACK_IMPORTED_MODULE_20__["DataTableModule"], _shared_components_label_label_module__WEBPACK_IMPORTED_MODULE_21__["LabelModule"], _requests_components_requests_edit_requests_edit_module__WEBPACK_IMPORTED_MODULE_23__["RequestsEditModule"], _requests_components_requests_create_requests_create_module__WEBPACK_IMPORTED_MODULE_22__["RequestsCreateModule"], _requests_components_requests_search_requests_search_module__WEBPACK_IMPORTED_MODULE_24__["RequestsSearchModule"]],
        providers: [_services_requests_index_icons_service__WEBPACK_IMPORTED_MODULE_27__["RequestsIndexIcons"]]
      })], RequestsIndexModule);
      /***/
    },

    /***/
    "CTtz":
    /*!***************************************************************************************!*\
      !*** ./src/app/modules/requests/components/requests-create/requests-create.module.ts ***!
      \***************************************************************************************/

    /*! exports provided: RequestsCreateModule */

    /***/
    function CTtz(module, __webpack_exports__, __webpack_require__) {
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


      var _angular_cdk_text_field__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! @angular/cdk/text-field */
      "8sFK");
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


      var _angular_material_autocomplete__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/material/autocomplete */
      "vrAh");
      /* harmony import */


      var _angular_material_button__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @angular/material/button */
      "Dxy4");
      /* harmony import */


      var _angular_material_core__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @angular/material/core */
      "UhP/");
      /* harmony import */


      var _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @angular/material/datepicker */
      "TN/R");
      /* harmony import */


      var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @angular/material/dialog */
      "iELJ");
      /* harmony import */


      var _angular_material_divider__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @angular/material/divider */
      "BSbQ");
      /* harmony import */


      var _angular_material_icon__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @angular/material/icon */
      "Tj54");
      /* harmony import */


      var _angular_material_input__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @angular/material/input */
      "e6WT");
      /* harmony import */


      var _angular_material_menu__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! @angular/material/menu */
      "rJgo");
      /* harmony import */


      var _angular_material_select__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! @angular/material/select */
      "ZTz/");
      /* harmony import */


      var _angular_material_tabs__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(
      /*! @angular/material/tabs */
      "M9ds");
      /* harmony import */


      var _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(
      /*! @angular/material/tooltip */
      "ZFy/");
      /* harmony import */


      var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(
      /*! @visurel/iconify-angular */
      "l+Q0");
      /* harmony import */


      var ngx_dropzone__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(
      /*! ngx-dropzone */
      "tq8E");
      /* harmony import */


      var _requests_create_component__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(
      /*! ./requests-create.component */
      "MeZh");

      var RequestsCreateModule = function RequestsCreateModule() {
        _classCallCheck(this, RequestsCreateModule);
      };

      RequestsCreateModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["NgModule"])({
        declarations: [_requests_create_component__WEBPACK_IMPORTED_MODULE_20__["RequestsCreateComponent"]],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_4__["FlexLayoutModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_5__["ReactiveFormsModule"], _angular_cdk_text_field__WEBPACK_IMPORTED_MODULE_1__["TextFieldModule"], _angular_material_autocomplete__WEBPACK_IMPORTED_MODULE_6__["MatAutocompleteModule"], _angular_material_button__WEBPACK_IMPORTED_MODULE_7__["MatButtonModule"], _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_9__["MatDatepickerModule"], _angular_material_dialog__WEBPACK_IMPORTED_MODULE_10__["MatDialogModule"], _angular_material_divider__WEBPACK_IMPORTED_MODULE_11__["MatDividerModule"], _angular_material_icon__WEBPACK_IMPORTED_MODULE_12__["MatIconModule"], _angular_material_input__WEBPACK_IMPORTED_MODULE_13__["MatInputModule"], _angular_material_menu__WEBPACK_IMPORTED_MODULE_14__["MatMenuModule"], _angular_material_core__WEBPACK_IMPORTED_MODULE_8__["MatNativeDateModule"], _angular_material_select__WEBPACK_IMPORTED_MODULE_15__["MatSelectModule"], _angular_material_tabs__WEBPACK_IMPORTED_MODULE_16__["MatTabsModule"], _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_17__["MatTooltipModule"], _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_18__["IconModule"], ngx_dropzone__WEBPACK_IMPORTED_MODULE_19__["NgxDropzoneModule"]],
        entryComponents: [_requests_create_component__WEBPACK_IMPORTED_MODULE_20__["RequestsCreateComponent"]]
      })], RequestsCreateModule);
      /***/
    },

    /***/
    "DXlN":
    /*!************************************************************************************************!*\
      !*** ./src/app/modules/requests/pages/requests-index/services/requests-index-icons.service.ts ***!
      \************************************************************************************************/

    /*! exports provided: RequestsIndexIcons */

    /***/
    function DXlN(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "RequestsIndexIcons", function () {
        return RequestsIndexIcons;
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


      var _iconify_icons_ic_twotone_menu__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-menu */
      "cS8l");
      /* harmony import */


      var _iconify_icons_ic_twotone_menu__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_menu__WEBPACK_IMPORTED_MODULE_4__);
      /* harmony import */


      var _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-search */
      "sF+I");
      /* harmony import */


      var _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_5__);
      /* harmony import */


      var _iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-star */
      "bE8U");
      /* harmony import */


      var _iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_6__);
      /* harmony import */


      var _iconify_icons_ic_twotone_star_border__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-star-border */
      "PNSm");
      /* harmony import */


      var _iconify_icons_ic_twotone_star_border__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_star_border__WEBPACK_IMPORTED_MODULE_7__);

      var RequestsIndexIcons = function RequestsIndexIcons() {
        _classCallCheck(this, RequestsIndexIcons);

        this.icStar = _iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_6___default.a;
        this.icStarBorder = _iconify_icons_ic_twotone_star_border__WEBPACK_IMPORTED_MODULE_7___default.a;
        this.icSearch = _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_5___default.a;
        this.icContacts = _iconify_icons_ic_twotone_contacts__WEBPACK_IMPORTED_MODULE_3___default.a;
        this.icMenu = _iconify_icons_ic_twotone_menu__WEBPACK_IMPORTED_MODULE_4___default.a;
        this.icCloudDownload = _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_2___default.a;
      };

      RequestsIndexIcons.ctorParameters = function () {
        return [];
      };

      RequestsIndexIcons = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], RequestsIndexIcons);
      /***/
    },

    /***/
    "E3RN":
    /*!*************************************************************************************************!*\
      !*** ./src/app/modules/requests/pages/requests-index/services/requests-table-config.service.ts ***!
      \*************************************************************************************************/

    /*! exports provided: RequestsTableConfig */

    /***/
    function E3RN(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "RequestsTableConfig", function () {
        return RequestsTableConfig;
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

      var RequestsTableConfig = /*#__PURE__*/function () {
        function RequestsTableConfig() {
          _classCallCheck(this, RequestsTableConfig);

          this.data = [];
          this.dataSubject = new rxjs__WEBPACK_IMPORTED_MODULE_2__["BehaviorSubject"](this.data);
          this.data$ = this.dataSubject.asObservable();
          this.pageSize = 20;
          this.pageSizeSubject = new rxjs__WEBPACK_IMPORTED_MODULE_2__["BehaviorSubject"](this.pageSize);
          this.pageSize$ = this.pageSizeSubject.asObservable();
          this.pageIndex = 0;
          this.pageIndexSubject = new rxjs__WEBPACK_IMPORTED_MODULE_2__["BehaviorSubject"](this.pageIndex);
          this.pageIndex$ = this.pageIndexSubject.asObservable();
          this.pages = 0;
          this.pagesSubject = new rxjs__WEBPACK_IMPORTED_MODULE_2__["BehaviorSubject"](this.pages);
          this.pages$ = this.pagesSubject.asObservable();
        }

        _createClass(RequestsTableConfig, [{
          key: "updateProjectId",
          value: function updateProjectId(id) {
            this.projectId = id;
          }
        }, {
          key: "updateData",
          value: function updateData(data) {
            this.dataSubject.next(data);
            this.data = data;
          }
        }, {
          key: "updatePageSize",
          value: function updatePageSize(size) {
            this.pageSizeSubject.next(size);
            this.pageSize = size;
          }
        }, {
          key: "updatePageIndex",
          value: function updatePageIndex(index) {
            this.pageIndexSubject.next(index);
            this.pageIndex = index;
          }
        }, {
          key: "updatePages",
          value: function updatePages(pages) {
            this.pagesSubject.next(pages);
            this.pages = pages;
          }
        }]);

        return RequestsTableConfig;
      }();

      RequestsTableConfig.ctorParameters = function () {
        return [];
      };

      RequestsTableConfig = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], RequestsTableConfig);
      /***/
    },

    /***/
    "FC6b":
    /*!*************************************************************************************!*\
      !*** ./src/app/modules/requests/pages/requests-index/requests-index.component.scss ***!
      \*************************************************************************************/

    /*! exports provided: default */

    /***/
    function FC6b(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = ".vex-page-layout-header {\n  height: 50px;\n}\n\nrequests-search {\n  width: 100%;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uLy4uL3JlcXVlc3RzLWluZGV4LmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0VBQ0UsWUFBQTtBQUNGOztBQUVBO0VBQ0UsV0FBQTtBQUNGIiwiZmlsZSI6InJlcXVlc3RzLWluZGV4LmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiLnZleC1wYWdlLWxheW91dC1oZWFkZXIge1xuICBoZWlnaHQ6IDUwcHg7XG59XG5cbnJlcXVlc3RzLXNlYXJjaCB7XG4gIHdpZHRoOiAxMDAlO1xufSJdfQ== */";
      /***/
    },

    /***/
    "FCmF":
    /*!****************************************************************************************!*\
      !*** ./src/app/modules/requests/pages/requests-index/services/request-data.service.ts ***!
      \****************************************************************************************/

    /*! exports provided: RequestDataService */

    /***/
    function FCmF(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "RequestDataService", function () {
        return RequestDataService;
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

      var RequestDataService = /*#__PURE__*/function () {
        function RequestDataService() {
          _classCallCheck(this, RequestDataService);

          this.subject = new rxjs__WEBPACK_IMPORTED_MODULE_2__["BehaviorSubject"](null);
          this.request$ = this.subject.asObservable();
        }

        _createClass(RequestDataService, [{
          key: "set",
          value: function set(request) {
            this.request = request;
            this.subject.next(request);
          }
        }]);

        return RequestDataService;
      }();

      RequestDataService.ctorParameters = function () {
        return [];
      };

      RequestDataService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], RequestDataService);
      /***/
    },

    /***/
    "FtDj":
    /*!***************************************************************************************************************************!*\
      !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/requests/pages/requests-index/requests-index.component.html ***!
      \***************************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function FtDj(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "<vex-page-layout>\n  <div class=\"w-full h-full flex flex-col\">\n\n    <div class=\"px-gutter pt-6 pb-20 vex-layout-theme flex-none\">\n      <div class=\"flex items-center\">\n        <vex-page-layout-header fxLayout=\"column\" fxLayoutAlign=\"center start\">\n          <div class=\"w-full flex flex-col sm:flex-row justify-between\">\n            <vex-breadcrumbs [crumbs]=\"crumbs\"></vex-breadcrumbs>\n          </div>\n        </vex-page-layout-header>\n      </div>\n    </div>\n\n    <div class=\"-mt-14 pt-0 overflow-hidden flex\">\n\n      <mat-drawer-container class=\"bg-transparent flex-auto flex\">\n        <mat-drawer [(opened)]=\"menuOpen\" mode=\"over\">\n          <requests-table-menu\n            [initialFilter]=\"filter\"\n            (filter)=\"filterRequests($event)\"\n            (create)=\"openCreateDialog()\"\n            class=\"sm:hidden\">\n          </requests-table-menu>\n        </mat-drawer>\n\n        <mat-drawer-content class=\"p-gutter pt-0 flex-auto flex items-start\">\n          <requests-table-menu\n            [initialFilter]=\"filter\"\n            (filter)=\"filterRequests($event)\"\n            (create)=\"openCreateDialog()\"\n            class=\"hidden sm:block mr-6\">\n          </requests-table-menu>\n\n          <div class=\"card h-full overflow-hidden flex-auto\">\n            <data-table\n              [buttonsTemplate]=\"buttonsTemplate\"\n              [columns]=\"tableColumns\"\n              [data]=\"requests\"\n              [length]=\"totalRequests\"\n              [pageSize]=\"pageSize\"\n              [page]=\"page\"\n              [resourceName]=\"'request'\"\n              [searchTemplate]=\"searchTemplate\"\n              [sortBy]=\"indexParams.sort_by\"\n              [sortOrder]=\"indexParams.sort_order\"\n              [templates]=\"{ latency: latencyTemplate, status: statusTemplate }\"\n              (edit)=\"openEditDialog($event)\"\n              (toggleStar)=\"toggleRequestStar($event)\"\n              (delete)=\"deleteRequest($event)\"\n              (download)=\"downloadRequest($event)\"\n              (view)=\"viewRequest($event)\"\n              (paginate)=\"handlePaginateChange($event)\"\n              (sort)=\"sortRequests($event)\"\n            >\n            </data-table>\n                        <!-- [searchStr]=\"searchStr$ | async\"  -->\n          </div>\n        </mat-drawer-content>\n\n      </mat-drawer-container>\n    </div>\n  </div>\n<vex-page-layout>\n\n<ng-template #buttonsTemplate let-id=\"id\">\n  <button mat-menu-item (click)=\"downloadRequest(id)\">\n    <mat-icon [icIcon]=\"icons.icCloudDownload\"></mat-icon>\n    <span>Download</span>\n  </button>\n</ng-template>\n\n<ng-template #searchTemplate>\n  <requests-search\n    [projectId]=\"project.id\"\n    [query]=\"indexParams.q || ''\"\n    [page]=\"page\"\n    [pageSize]=\"pageSize\"\n    (search)=\"searchRequests($event)\"\n  >\n  </requests-search>\n</ng-template>\n\n<ng-template #statusTemplate let-request=\"row\">\n  <status-label\n    [okThreshold]=\"299\"\n    [text]=\"request.status\"\n    [status]=\"request.status\"\n    [warningThreshold]=\"499\"\n  >\n  </status-label>\n</ng-template>\n\n<ng-template #latencyTemplate let-request=\"row\">\n  <status-label\n    [okThreshold]=\"350\"\n    [text]=\"request.latency + ' ms'\"\n    [status]=\"request.latency\"\n    [warningThreshold]=\"1000\"\n  >\n  </status-label>\n</ng-template>";
      /***/
    },

    /***/
    "H1bl":
    /*!****************************************************************************************!*\
      !*** ./src/app/modules/requests/components/requests-edit/requests-edit.component.scss ***!
      \****************************************************************************************/

    /*! exports provided: default */

    /***/
    function H1bl(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJyZXF1ZXN0cy1lZGl0LmNvbXBvbmVudC5zY3NzIn0= */";
      /***/
    },

    /***/
    "MeZh":
    /*!******************************************************************************************!*\
      !*** ./src/app/modules/requests/components/requests-create/requests-create.component.ts ***!
      \******************************************************************************************/

    /*! exports provided: RequestsCreateComponent */

    /***/
    function MeZh(module, __webpack_exports__, __webpack_require__) {
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
      "T8up");
      /* harmony import */


      var _requests_create_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! ./requests-create.component.scss */
      "m354");
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


      var rxjs_operators__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! rxjs/operators */
      "kU1M");
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


      var _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-more-vert */
      "+Chm");
      /* harmony import */


      var _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_11__);
      /* harmony import */


      var _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-person */
      "KaaH");
      /* harmony import */


      var _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_12__);
      /* harmony import */


      var _iconify_icons_ic_twotone_print__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-print */
      "yHIK");
      /* harmony import */


      var _iconify_icons_ic_twotone_print__WEBPACK_IMPORTED_MODULE_13___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_print__WEBPACK_IMPORTED_MODULE_13__);
      /* harmony import */


      var _core_utils_alias_discovery_service__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! @core/utils/alias-discovery.service */
      "PbvV");
      /* harmony import */


      var _data_builders_request_string__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! @data/builders/request-string */
      "z1KO");
      /* harmony import */


      var _data_builders_response_string__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(
      /*! @data/builders/response-string */
      "UdVG");
      /* harmony import */


      var _data_schema__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(
      /*! @data/schema */
      "V99k");

      var RequestsCreateComponent = /*#__PURE__*/function () {
        function RequestsCreateComponent(projectId, dialogRef, fb, aliasDiscovery) {
          _classCallCheck(this, RequestsCreateComponent);

          this.projectId = projectId;
          this.dialogRef = dialogRef;
          this.fb = fb;
          this.aliasDiscovery = aliasDiscovery;
          this.onCreate = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
          this.formOptions = {
            headers: ['Accept', 'Accept-CH', 'Accept-CH-Lifetime', 'Accept-Charset', 'Accept-Encoding', 'Accept-Language', 'Accept-Patch', 'Accept-Post', 'Accept-Ranges', 'Access-Control-Allow-Credentials', 'Access-Control-Allow-Headers', 'Access-Control-Allow-Methods', 'Access-Control-Allow-Origin', 'Access-Control-Expose-Headers', 'Access-Control-Max-Age', 'Access-Control-Request-Headers', 'Access-Control-Request-Method', 'Age', 'Allow', 'Alt-Svc', 'Authorization', 'Cache-Control', 'Clear-Site-Data', 'Connection', 'Content-Disposition', 'Content-Encoding', 'Content-Language', 'Content-Length', 'Content-Location', 'Content-Range', 'Content-Security-Policy', 'Content-Security-Policy-Report-Only', 'Content-Type', 'Cookie', 'Cookie2', 'Cross-Origin-Embedder-Policy', 'Cross-Origin-Opener-Policy', 'Cross-Origin-Resource-Policy', 'DNT', 'DPR', 'Date', 'Device-Memory', 'Digest', 'ETag', 'Early-Data', 'Expect', 'Expect-CT', 'Expires', 'Feature-Policy', 'Forwarded', 'From', 'Host', 'If-Match', 'If-Modified-Since', 'If-None-Match', 'If-Range', 'If-Unmodified-Since', 'Index', 'Keep-Alive', 'Large-Allocation', 'Last-Modified', 'Link', 'Location', 'NEL', 'Origin', 'Pragma', 'Proxy-Authenticate', 'Proxy-Authorization', 'Public-Key-Pins', 'Public-Key-Pins-Report-Only', 'Range', 'Referer', 'Referrer-Policy', 'Retry-After', 'Save-Data', 'Sec-Fetch-Dest', 'Sec-Fetch-Mode', 'Sec-Fetch-Site', 'Sec-Fetch-User', 'Sec-WebSocket-Accept', 'Server', 'Server-Timing', 'Set-Cookie', 'Set-Cookie2', 'SourceMap', 'Strict-Transport-Security', 'TE', 'Timing-Allow-Origin', 'Tk', 'Trailer', 'Transfer-Encoding', 'Upgrade', 'Upgrade-Insecure-Requests', 'User-Agent', 'Vary', 'Via', 'WWW-Authenticate', 'Want-Digest', 'Warning', 'X-Content-Type-Options', 'X-DNS-Prefetch-Control', 'X-Forwarded-For', 'X-Forwarded-Host', 'X-Forwarded-Proto', 'X-Frame-Options', 'X-XSS-Protection'],
            filteredHeaders: null,
            filteredResponseHeaders: null,
            methods: ['GET', 'OPTIONS', 'POST', 'PUT', 'DELETE'],
            requestTypes: ['Custom', 'text/plain', 'multipart/form-data', 'application/json', 'application/xml', 'application/x-www-form-urlencoded'],
            responseTypes: ['Custom', 'text/plain', 'text/html', 'text/csv', 'application/json', 'application/xml']
          };
          this.formSettings = {
            bodyParameterized: false
          };
          this.formNames = {
            headers: 'headers',
            responseHeaders: 'responseHeaders',
            bodyParams: 'bodyParams'
          }; // ngx-dropzone

          this.files = [];
          this.requestPriorities = _data_schema__WEBPACK_IMPORTED_MODULE_17__["RequestPriorityData"];
          this.selectedPriority = this.requestPriorities[3]; // icons

          this.icMoreVert = _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_11___default.a;
          this.icClose = _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_7___default.a;
          this.icPrint = _iconify_icons_ic_twotone_print__WEBPACK_IMPORTED_MODULE_13___default.a;
          this.icDownload = _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_8___default.a;
          this.icDelete = _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_9___default.a;
          this.icPerson = _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_12___default.a;
          this.icLabel = _iconify_icons_ic_twotone_label__WEBPACK_IMPORTED_MODULE_10___default.a;
        }

        _createClass(RequestsCreateComponent, [{
          key: "ngOnInit",
          value: function ngOnInit() {
            this.form = this.fb.group({
              body: null,
              bodyParams: this.fb.array([]),
              contentType: this.formOptions.responseTypes[0],
              headers: this.fb.array([]),
              method: new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"]('', [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required]),
              responseHeaders: this.fb.array([]),
              responseBody: null,
              responseContentType: this.formOptions.responseTypes[0],
              status: new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"](200, [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required, _angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].min(100), _angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].max(999)]),
              url: new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"]('', [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required])
            });
          }
        }, {
          key: "handlePrioritySelect",
          value: function handlePrioritySelect(priority) {
            this.selectedPriority = priority;
          }
        }, {
          key: "create",
          value: function create() {
            var form = this.form.value;

            if (!this.files.length) {
              this.build(form);
            } else {
              this.upload(form, this.files);
            }
          }
        }, {
          key: "onFileSelect",
          value: function onFileSelect(event) {
            var _this$files;

            console.log(event);

            (_this$files = this.files).push.apply(_this$files, _toConsumableArray(event.addedFiles));
          }
        }, {
          key: "onFileRemove",
          value: function onFileRemove(event) {
            console.log(event);
            this.files.splice(this.files.indexOf(event), 1);
          }
          /**
           *
           * Headers / Response Headers
           *
           */

        }, {
          key: "addHeader",
          value: function addHeader(formName) {
            var _this = this;

            formName = formName || this.formNames.headers;
            var headers = this.form.get(formName);
            var headerNameControl = new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"]('', [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required]);
            var filteredSet = headerNameControl.valueChanges.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["startWith"])(''), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["map"])(function (value) {
              return _this._filter(_this.formOptions.headers, value);
            }));

            if (formName === this.formNames.responseHeaders) {
              this.formOptions.filteredResponseHeaders = filteredSet;
            } else {
              this.formOptions.filteredHeaders = filteredSet;
            }

            headers.push(this.fb.group({
              name: headerNameControl,
              value: new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"]('', [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required])
            }));
          }
        }, {
          key: "removeHeader",
          value: function removeHeader(index, formName) {
            formName = formName || this.formNames.headers;
            var headers = this.form.get(formName);
            headers.removeAt(index);
          }
        }, {
          key: "addResponseHeader",
          value: function addResponseHeader() {
            this.addHeader(this.formNames.responseHeaders);
          }
        }, {
          key: "removeResponseHeader",
          value: function removeResponseHeader(index) {
            this.removeHeader(index, this.formNames.responseHeaders);
          }
          /**
           *
           * Body / Response Body
           *
           */

        }, {
          key: "updateContentTypeHeader",
          value: function updateContentTypeHeader(contentType, formName) {
            var _this2 = this;

            formName = formName || this.formNames.headers;
            var headers = this.form.get(formName);
            var updated = false;
            headers.value.some(function (header, i) {
              if (header.name !== 'Content-Type') {
                return false;
              }

              if (contentType === 'Custom') {
                var contentTypes;

                if (formName === _this2.formNames.responseHeaders) {
                  contentTypes = _this2.formOptions.responseTypes;
                } else {
                  contentTypes = _this2.formOptions.requestTypes;
                } // If Content-Type is a provided one, remove it


                if (contentTypes.indexOf(header.value) !== -1) {
                  _this2.removeHeader(i, formName);
                }
              } else {
                var newHeaders = headers.value.slice();
                newHeaders[i].value = contentType;
                headers.setValue(newHeaders);
              }

              updated = true;
              return true;
            });
            return updated;
          }
        }, {
          key: "handleContentTypeChange",
          value: function handleContentTypeChange(event, formName) {
            formName = formName || this.formNames.headers;
            var contentType = event.value;
            var headers = this.form.get(formName);

            switch (contentType) {
              case 'application/json':
              case 'application/x-www-form-urlencoded':
                if (formName === this.formNames.headers) {
                  this.formSettings.bodyParameterized = true;
                }

            }

            if (!this.updateContentTypeHeader(contentType, formName)) {
              headers.push(this.fb.group({
                name: 'Content-Type',
                value: contentType
              }));
            }
          }
        }, {
          key: "handleResponseContentTypeChange",
          value: function handleResponseContentTypeChange(event) {
            this.handleContentTypeChange(event, this.formNames.responseHeaders);
          }
        }, {
          key: "addBodyParam",
          value: function addBodyParam() {
            var formName = this.formNames.bodyParams;
            var bodyParams = this.form.get(formName);
            bodyParams.push(this.fb.group({
              name: new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"]('', [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required]),
              value: new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"]('', [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required])
            }));
          }
        }, {
          key: "removeBodyParam",
          value: function removeBodyParam(index) {
            var formName = this.formNames.bodyParams;
            var bodyParams = this.form.get(formName);
            bodyParams.removeAt(index);
          }
          /**
           *
           * Helpers
           *
           */

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
          key: "build",
          value: function build(form) {
            var requestId = Math.random().toString(36).substr(2);
            var requestString = new _data_builders_request_string__WEBPACK_IMPORTED_MODULE_15__["RequestString"]({
              id: requestId,
              url: form.url,
              method: form.method,
              headers: form.headers,
              body: this.buildBody(form)
            });
            var responseString = new _data_builders_response_string__WEBPACK_IMPORTED_MODULE_16__["ResponseString"]({
              id: requestId,
              status: form.status,
              headers: form.responseHeaders,
              body: form.responseBody
            });
            var formData = new FormData();
            formData.append('requests', [requestString.get(), responseString.get()].join('🐵🙈🙉\n'));
            formData.append('importer', 'gor');
            this.onCreate.emit(formData);
            this.dialogRef.close();
          }
        }, {
          key: "buildBody",
          value: function buildBody(form) {
            if (this.formSettings.bodyParameterized) {
              switch (form.contentType) {
                case 'application/json':
                  return this.serializeJSON(form.bodyParams);
                  break;

                case 'application/x-www-form-urlencoded':
                  return this.serializeURLEncoded(form.bodyParams);
                  break;
              }
            } else {
              return form.body;
            }
          }
        }, {
          key: "upload",
          value: function upload(form, files) {
            var _this3 = this;

            var fileReader = new FileReader();

            fileReader.onload = function (e) {
              var formData = new FormData();
              formData.append('requests', files[0]);
              formData.append('importer', 'har');

              _this3.onCreate.emit(formData);

              _this3.dialogRef.close();
            };

            fileReader.readAsText(files[0]);
          }
        }, {
          key: "_filter",
          value: function _filter(options, value) {
            var filterValue = value.toLowerCase();
            return options.filter(function (option) {
              return option.toLowerCase().includes(filterValue);
            });
          }
        }, {
          key: "serializeJSON",
          value: function serializeJSON(params) {
            var obj = {};
            params.forEach(function (param) {
              obj[param.name] = param.value;
            });
            return JSON.stringify(obj);
          }
        }, {
          key: "serializeURLEncoded",
          value: function serializeURLEncoded(params) {
            var toks = [];
            params.forEach(function (param) {
              toks.push("".concat(encodeURIComponent(param.name), "=").concat(encodeURIComponent(param.value)));
            });
            return toks.join('&');
          }
        }]);

        return RequestsCreateComponent;
      }();

      RequestsCreateComponent.ctorParameters = function () {
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
          type: _core_utils_alias_discovery_service__WEBPACK_IMPORTED_MODULE_14__["AliasDiscovery"]
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
    "Q4Vm":
    /*!***********************************************************************************************************************!*\
      !*** ./src/app/modules/requests/pages/requests-index/components/requests-table-menu/requests-table-menu.component.ts ***!
      \***********************************************************************************************************************/

    /*! exports provided: RequestsTableMenuComponent */

    /***/
    function Q4Vm(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "RequestsTableMenuComponent", function () {
        return RequestsTableMenuComponent;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _raw_loader_requests_table_menu_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! raw-loader!./requests-table-menu.component.html */
      "QcGu");
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


      var _iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-star */
      "bE8U");
      /* harmony import */


      var _iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_4__);
      /* harmony import */


      var _iconify_icons_ic_twotone_view_headline__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-view-headline */
      "29B6");
      /* harmony import */


      var _iconify_icons_ic_twotone_view_headline__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_view_headline__WEBPACK_IMPORTED_MODULE_5__);
      /* harmony import */


      var _vex_animations_fade_in_right_animation__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @vex/animations/fade-in-right.animation */
      "yriF");
      /* harmony import */


      var _vex_animations_stagger_animation__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @vex/animations/stagger.animation */
      "UOrl");

      var RequestsTableMenuComponent = /*#__PURE__*/function () {
        function RequestsTableMenuComponent() {
          _classCallCheck(this, RequestsTableMenuComponent);

          this.items = [{
            type: 'link',
            id: 'all',
            icon: _iconify_icons_ic_twotone_view_headline__WEBPACK_IMPORTED_MODULE_5___default.a,
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
            icon: _iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_4___default.a,
            label: 'Starred'
          }];
          this.filter = new _angular_core__WEBPACK_IMPORTED_MODULE_2__["EventEmitter"]();
          this.create = new _angular_core__WEBPACK_IMPORTED_MODULE_2__["EventEmitter"](); // Icons

          this.icAdd = _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_3___default.a;
        }

        _createClass(RequestsTableMenuComponent, [{
          key: "ngOnInit",
          value: function ngOnInit() {
            this.activeCategory = this.initialFilter || 'all';
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
            }

            this.filter.emit(event);
          }
        }]);

        return RequestsTableMenuComponent;
      }();

      RequestsTableMenuComponent.ctorParameters = function () {
        return [];
      };

      RequestsTableMenuComponent.propDecorators = {
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
      RequestsTableMenuComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["Component"])({
        selector: 'requests-table-menu',
        template: _raw_loader_requests_table_menu_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        animations: [_vex_animations_fade_in_right_animation__WEBPACK_IMPORTED_MODULE_6__["fadeInRight400ms"], _vex_animations_stagger_animation__WEBPACK_IMPORTED_MODULE_7__["stagger40ms"]],
        changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_2__["ChangeDetectionStrategy"].OnPush
      })], RequestsTableMenuComponent);
      /***/
    },

    /***/
    "QcGu":
    /*!***************************************************************************************************************************************************************!*\
      !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/requests/pages/requests-index/components/requests-table-menu/requests-table-menu.component.html ***!
      \***************************************************************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function QcGu(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "<div @stagger class=\"max-w-xxxs w-full\">\n  <div class=\"h-14 mb-6 flex vex-layout-theme-bg px-gutter sm:px-0\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n    <button (click)=\"create.emit()\" class=\"flex-auto\" mat-raised-button type=\"button\">\n      <ic-icon [icon]=\"icAdd\" class=\"ltr:mr-3 rtl:ml-3\" inline=\"true\" size=\"18px\"></ic-icon>\n      <span>CREATE</span>\n    </button>\n  </div>\n\n  <div class=\"px-gutter sm:px-0\">\n    <ng-container *ngFor=\"let item of items\">\n      <a (click)=\"setFilter(item.id)\"\n         *ngIf=\"item.type === 'link'\"\n         @fadeInRight\n         [class.bg-hover]=\"isActive(item.id)\"\n         [class.text-primary-500]=\"isActive(item.id)\"\n         class=\"list-item mt-2 no-underline flex items-center\"\n         matRipple>\n        <ic-icon [icon]=\"item.icon\" [ngClass]=\"item.classes?.icon\" class=\"ltr:mr-3 rtl:ml-3\" size=\"24px\"></ic-icon>\n        <span>{{ item.label }}</span>\n      </a>\n\n      <h3 *ngIf=\"item.type === 'subheading'\"\n          @fadeInRight\n          class=\"caption text-secondary uppercase font-medium mb-0 mt-6\">{{ item.label }}</h3>\n    </ng-container>\n  </div>\n</div>\n";
      /***/
    },

    /***/
    "T8up":
    /*!**********************************************************************************************************************************!*\
      !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/requests/components/requests-create/requests-create.component.html ***!
      \**********************************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function T8up(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "<form (ngSubmit)=\"create()\" [formGroup]=\"form\">\r\n  <div fxLayout=\"row\" fxLayoutAlign=\"start center\" mat-dialog-title>\r\n    <h2 class=\"headline m-0\" fxFlex=\"auto\">New Request</h2>\r\n\r\n    <!-- <button [matMenuTriggerFor]=\"settingsMenu\" class=\"text-secondary\" mat-icon-button type=\"button\" matTooltip=\"Priority\">\r\n      <mat-icon [icIcon]=\"icLabel\" [ngClass]=\"selectedPriority.classes\"></mat-icon>\r\n    </button> -->\r\n\r\n    <button class=\"text-secondary\" mat-dialog-close mat-icon-button type=\"button\">\r\n      <mat-icon [icIcon]=\"icClose\"></mat-icon>\r\n    </button>\r\n  </div>\r\n\r\n  <mat-divider class=\"-mx-6 text-border\"></mat-divider>\r\n\r\n  <mat-tab-group>\r\n    <mat-tab label=\"Build\">\r\n      <div fxLayout=\"row\" fxLayoutGap=\"10px\" class=\"mt-3\">\r\n        <mat-form-field fxFlex=\"15\" appearance=\"fill\">\r\n          <mat-label>Method</mat-label>\r\n          <mat-select formControlName=\"method\">\r\n            <mat-option *ngFor=\"let method of formOptions.methods\" [value]=\"method\">\r\n              {{ method }}\r\n            </mat-option>\r\n          </mat-select>\r\n        </mat-form-field>\r\n        <mat-form-field fxFlex=\"70\">\r\n          <mat-label>URL</mat-label>\r\n          <input\r\n            matInput\r\n            formControlName=\"url\"\r\n          />\r\n        </mat-form-field>\r\n        <mat-form-field fxFlex=\"15\">\r\n          <mat-label>Status Code</mat-label>\r\n          <input\r\n            matInput\r\n            formControlName=\"status\"\r\n          />\r\n        </mat-form-field>\r\n      </div>\r\n\r\n      <mat-divider></mat-divider>\r\n\r\n      <mat-tab-group class=\"p-3\">\r\n        <!-- Headers -->\r\n        <mat-tab label=\"Headers\">\r\n          <div fxLayout=\"column\" class=\"mt-3 mb-0 request-component-wrapper\">\r\n            <div\r\n              formArrayName=\"headers\"\r\n              *ngFor=\"let control of form.get(formNames.headers)['controls']; index as i\"\r\n            >\r\n              <div\r\n                [formGroupName]=\"i\"\r\n                fxLayout=\"row\"\r\n                fxLayoutAlign=\"space-around start\"\r\n                fxLayoutGap=\"10px\"\r\n              >\r\n                <mat-form-field fxFlex=\"40\">\r\n                  <mat-label>Name</mat-label>\r\n                  <input\r\n                    type=\"text\"\r\n                    matInput\r\n                    formControlName=\"name\"\r\n                    [matAutocomplete]=\"auto\"\r\n                  >\r\n                  <mat-autocomplete #auto=\"matAutocomplete\">\r\n                    <mat-option *ngFor=\"let option of formOptions.filteredHeaders | async\" [value]=\"option\">\r\n                      {{ option }}\r\n                    </mat-option>\r\n                  </mat-autocomplete>\r\n                </mat-form-field>\r\n                <mat-form-field fxFlex=\"40\">\r\n                  <mat-label>Value</mat-label>\r\n                  <input\r\n                    matInput\r\n                    formControlName=\"value\"\r\n                  />\r\n                </mat-form-field>\r\n                <button\r\n                  (click)=\"removeHeader(i)\"\r\n                  class=\"mt-2\"\r\n                  color=\"warn\"\r\n                  fxFlex=\"10\"\r\n                  type=\"button\"\r\n                  mat-button\r\n                >\r\n                  <mat-icon [icIcon]=\"icDelete\"></mat-icon>\r\n                </button>\r\n              </div>\r\n            </div>\r\n            <button (click)=\"addHeader()\" color=\"primary\" type=\"button\" mat-raised-button fxFlex=\"100\">\r\n              ADD\r\n            </button>\r\n          </div>\r\n        </mat-tab>\r\n\r\n        <!-- Body -->\r\n        <mat-tab label=\"Body\">\r\n          <div fxLayout=\"column\" class=\"mt-3 mb-0 request-component-wrapper\">\r\n            <mat-form-field appearance=\"fill\">\r\n              <mat-label>Content Type</mat-label>\r\n              <mat-select\r\n                (selectionChange)=\"handleContentTypeChange($event)\"\r\n                formControlName=\"contentType\"\r\n              >\r\n                <mat-option *ngFor=\"let option of formOptions.requestTypes\" [value]=\"option\">\r\n                  {{ option }}\r\n                </mat-option>\r\n              </mat-select>\r\n            </mat-form-field>\r\n            <mat-form-field *ngIf=\"!formSettings.bodyParameterized\">\r\n              <mat-label>Content</mat-label>\r\n              <textarea\r\n                cdkTextareaAutosize\r\n                cdkAutosizeMinRows=\"1\"\r\n                formControlName=\"body\"\r\n                matInput\r\n              >\r\n              </textarea>\r\n            </mat-form-field>\r\n            <ng-container *ngIf=\"formSettings.bodyParameterized\">\r\n              <div\r\n                formArrayName=\"bodyParams\"\r\n                *ngFor=\"let control of form.get(formNames.bodyParams)['controls']; index as i\"\r\n              >\r\n                <div\r\n                  [formGroupName]=\"i\"\r\n                  fxLayout=\"row\"\r\n                  fxLayoutAlign=\"space-around start\"\r\n                  fxLayoutGap=\"10px\"\r\n                >\r\n                  <mat-form-field fxFlex=\"40\">\r\n                    <mat-label>Name</mat-label>\r\n                    <input\r\n                      matInput\r\n                      formControlName=\"name\"\r\n                    />\r\n                  </mat-form-field>\r\n                  <mat-form-field fxFlex=\"40\">\r\n                    <mat-label>Value</mat-label>\r\n                    <input\r\n                      matInput\r\n                      formControlName=\"value\"\r\n                    />\r\n                  </mat-form-field>\r\n                  <button\r\n                    (click)=\"removeBodyParam(i)\"\r\n                    class=\"mt-2\"\r\n                    color=\"warn\"\r\n                    fxFlex=\"10\"\r\n                    type=\"button\"\r\n                    mat-button\r\n                  >\r\n                    <mat-icon [icIcon]=\"icDelete\"></mat-icon>\r\n                  </button>\r\n                </div>\r\n              </div>\r\n              <button (click)=\"addBodyParam()\" color=\"primary\" type=\"button\" mat-raised-button fxFlex=\"100\">\r\n                ADD\r\n              </button>\r\n            </ng-container>\r\n          </div>\r\n        </mat-tab>\r\n\r\n        <!-- Response Headers -->\r\n        <mat-tab label=\"Response Headers\">\r\n          <div fxLayout=\"column\" class=\"mt-3 mb-0 request-component-wrapper\">\r\n            <div\r\n              formArrayName=\"responseHeaders\"\r\n              *ngFor=\"let control of form.get(formNames.responseHeaders)['controls']; index as i\"\r\n            >\r\n              <div\r\n                [formGroupName]=\"i\"\r\n                fxLayout=\"row\"\r\n                fxLayoutAlign=\"space-around start\"\r\n                fxLayoutGap=\"10px\"\r\n              >\r\n                <mat-form-field fxFlex=\"40\">\r\n                  <mat-label>Name</mat-label>\r\n                  <input\r\n                    type=\"text\"\r\n                    matInput\r\n                    formControlName=\"name\"\r\n                    [matAutocomplete]=\"auto\"\r\n                  >\r\n                  <mat-autocomplete #auto=\"matAutocomplete\">\r\n                    <mat-option *ngFor=\"let option of formOptions.filteredResponseHeaders | async\" [value]=\"option\">\r\n                      {{ option }}\r\n                    </mat-option>\r\n                  </mat-autocomplete>\r\n                </mat-form-field>\r\n                <mat-form-field fxFlex=\"40\">\r\n                  <mat-label>Value</mat-label>\r\n                  <input\r\n                    matInput\r\n                    formControlName=\"value\"\r\n                  />\r\n                </mat-form-field>\r\n                <button\r\n                  (click)=\"removeResponseHeader(i)\"\r\n                  class=\"mt-2\"\r\n                  color=\"warn\"\r\n                  fxFlex=\"10\"\r\n                  type=\"button\"\r\n                  mat-button\r\n                >\r\n                  <mat-icon [icIcon]=\"icDelete\"></mat-icon>\r\n                </button>\r\n              </div>\r\n            </div>\r\n            <button (click)=\"addResponseHeader()\" color=\"primary\" type=\"button\" mat-raised-button fxFlex=\"100\">\r\n              ADD\r\n            </button>\r\n          </div>\r\n        </mat-tab>\r\n\r\n        <!-- Response Body -->\r\n        <mat-tab label=\"Response Body\">\r\n          <div fxLayout=\"column\" class=\"mt-3 mb-0 request-component-wrapper\">\r\n            <mat-form-field appearance=\"fill\">\r\n              <mat-label>Content Type</mat-label>\r\n              <mat-select\r\n                (selectionChange)=\"handleResponseContentTypeChange($event)\"\r\n                formControlName=\"responseContentType\"\r\n              >\r\n                <mat-option *ngFor=\"let option of formOptions.responseTypes\" [value]=\"option\">\r\n                  {{ option }}\r\n                </mat-option>\r\n              </mat-select>\r\n            </mat-form-field>\r\n            <mat-form-field class=\"p-0\">\r\n              <mat-label>Content</mat-label>\r\n              <textarea\r\n                cdkTextareaAutosize\r\n                cdkAutosizeMinRows=\"1\"\r\n                formControlName=\"responseBody\"\r\n                matInput\r\n              >\r\n              </textarea>\r\n            </mat-form-field>\r\n          </div>\r\n        </mat-tab>\r\n      </mat-tab-group>\r\n    </mat-tab>\r\n\r\n    <mat-tab label=\"Upload\">\r\n      <div class=\"mt-3\">\r\n        <ngx-dropzone (change)=\"onFileSelect($event)\">\r\n          <ngx-dropzone-label>Select or drop a HAR file!</ngx-dropzone-label>\r\n          <ngx-dropzone-preview *ngFor=\"let f of files\" [removable]=\"true\" (removed)=\"onFileRemove(f)\">\r\n              <ngx-dropzone-label>{{ f.name }}</ngx-dropzone-label>\r\n          </ngx-dropzone-preview>\r\n        </ngx-dropzone>\r\n      </div>\r\n    </mat-tab>\r\n  </mat-tab-group>\r\n\r\n  <mat-divider></mat-divider>\r\n\r\n  <mat-dialog-actions align=\"end\">\r\n    <button [disabled]=\"form.invalid && !files.length\" color=\"primary\" mat-button type=\"submit\">CREATE</button>\r\n    <button mat-button mat-dialog-close type=\"button\">CANCEL</button>\r\n  </mat-dialog-actions>\r\n</form>\r\n\r\n<mat-menu #settingsMenu=\"matMenu\" xPosition=\"before\" yPosition=\"below\">\r\n  <button mat-menu-item *ngFor=\"let priority of requestPriorities\" (click)=\"handlePrioritySelect(priority)\">\r\n    <span>{{ priority.name }}</span>\r\n  </button>\r\n</mat-menu>\r\n";
      /***/
    },

    /***/
    "UdVG":
    /*!**************************************************!*\
      !*** ./src/app/data/builders/response-string.ts ***!
      \**************************************************/

    /*! exports provided: ResponseString */

    /***/
    function UdVG(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ResponseString", function () {
        return ResponseString;
      });

      var ResponseString = /*#__PURE__*/function () {
        function ResponseString(response) {
          _classCallCheck(this, ResponseString);

          this.RESPONSE_TYPE = 2;
          this.CLRF = '\n';
          this.response = response;
          this.lines = [];
          this.responseLine();
          this.headers();
          this.body();
          this.control();
        }

        _createClass(ResponseString, [{
          key: "control",
          value: function control() {
            this.lines.unshift("".concat(this.RESPONSE_TYPE, " ").concat(this.response.id, " ").concat(new Date().getTime() * 1000));
          }
        }, {
          key: "responseLine",
          value: function responseLine() {
            this.lines.push("HTTP/1.1 ".concat(this.response.status));
          }
        }, {
          key: "headers",
          value: function headers() {
            var _this4 = this;

            this.response.headers.forEach(function (header) {
              _this4.lines.push("".concat(header.name, ": ").concat(header.value));
            });
          }
        }, {
          key: "body",
          value: function body() {
            this.lines.push("".concat(this.CLRF).concat(this.response.body || ''));
          }
        }, {
          key: "get",
          value: function get() {
            return this.lines.join(this.CLRF);
          }
        }]);

        return ResponseString;
      }();
      /***/

    },

    /***/
    "VBGS":
    /*!**************************************************************************************!*\
      !*** ./src/app/modules/requests/components/requests-edit/requests-edit.component.ts ***!
      \**************************************************************************************/

    /*! exports provided: RequestsEditComponent */

    /***/
    function VBGS(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "RequestsEditComponent", function () {
        return RequestsEditComponent;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _raw_loader_requests_edit_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! raw-loader!./requests-edit.component.html */
      "la/H");
      /* harmony import */


      var _requests_edit_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! ./requests-edit.component.scss */
      "H1bl");
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

      var RequestsEditComponent = /*#__PURE__*/function () {
        function RequestsEditComponent(request, dialogRef, fb) {
          _classCallCheck(this, RequestsEditComponent);

          this.request = request;
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
          this.requestPriorities = _data_schema__WEBPACK_IMPORTED_MODULE_16__["RequestPriorityData"];
        }

        _createClass(RequestsEditComponent, [{
          key: "ngOnInit",
          value: function ngOnInit() {
            this.form.patchValue(this.request);
            var priorityIndex = this.requestPriorities.length - this.request.priority - 1;
            this.selectedPriority = this.requestPriorities[priorityIndex];
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

        return RequestsEditComponent;
      }();

      RequestsEditComponent.ctorParameters = function () {
        return [{
          type: _data_schema__WEBPACK_IMPORTED_MODULE_16__["Request"],
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

      RequestsEditComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'requests-edit',
        template: _raw_loader_requests_edit_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_requests_edit_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
      })], RequestsEditComponent);
      /***/
    },

    /***/
    "Zf3l":
    /*!***********************************************************************************!*\
      !*** ./src/app/modules/requests/pages/requests-index/requests-index.component.ts ***!
      \***********************************************************************************/

    /*! exports provided: RequestsIndexComponent */

    /***/
    function Zf3l(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "RequestsIndexComponent", function () {
        return RequestsIndexComponent;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _requests_index_component_scss__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! ./requests-index.component.scss */
      "FC6b");
      /* harmony import */


      var _raw_loader_requests_index_component_html__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! raw-loader!./requests-index.component.html */
      "FtDj");
      /* harmony import */


      var _angular_common__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/common */
      "SVse");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/material/dialog */
      "iELJ");
      /* harmony import */


      var _angular_router__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/router */
      "iInd");
      /* harmony import */


      var _vex_animations__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @vex/animations */
      "ORuP");
      /* harmony import */


      var _core_http__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @core/http */
      "vAmI");
      /* harmony import */


      var _core_utils__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @core/utils */
      "a+Vh");
      /* harmony import */


      var _requests_components_requests_create_requests_create_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @requests/components/requests-create/requests-create.component */
      "MeZh");
      /* harmony import */


      var _requests_components_requests_edit_requests_edit_component__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @requests/components/requests-edit/requests-edit.component */
      "VBGS");
      /* harmony import */


      var _layout_services_layout_config_service__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @layout/services/layout-config.service */
      "U9Lm");
      /* harmony import */


      var _services_request_data_service__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! ./services/request-data.service */
      "FCmF");
      /* harmony import */


      var _services_requests_index_icons_service__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! ./services/requests-index-icons.service */
      "DXlN");
      /* harmony import */


      var _services_requests_table_config_service__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! ./services/requests-table-config.service */
      "E3RN");

      var RequestsIndexComponent = /*#__PURE__*/function () {
        function RequestsIndexComponent(icons, activatedRoute, agentService, dialog, file, fileDownload, layoutConfigService, location, requestDataService, requestResource, requestsTableConfig, router, route, uri) {
          _classCallCheck(this, RequestsIndexComponent);

          this.icons = icons;
          this.activatedRoute = activatedRoute;
          this.agentService = agentService;
          this.dialog = dialog;
          this.file = file;
          this.fileDownload = fileDownload;
          this.layoutConfigService = layoutConfigService;
          this.location = location;
          this.requestDataService = requestDataService;
          this.requestResource = requestResource;
          this.requestsTableConfig = requestsTableConfig;
          this.router = router;
          this.route = route;
          this.uri = uri;
          this.crumbs = []; // Breadcrumb settings

          this.menuOpen = false;
        }

        _createClass(RequestsIndexComponent, [{
          key: "ngOnInit",
          value: function ngOnInit() {
            var _this5 = this;

            var routeSnapshot = this.route.snapshot;
            this.project = routeSnapshot.data.project;
            this.requestsTableConfig.updateProjectId(this.project.id);
            var requests = routeSnapshot.data.requests;
            this.requests = requests.list;
            this.totalRequests = requests.total;
            this.indexParams = Object.assign({}, routeSnapshot.queryParams);
            this.indexParams.page = this.indexParams.page || 0;
            this.indexParams.size = this.indexParams.size || 20;
            this.page = this.indexParams.page;
            this.pageSize = this.indexParams.size;
            this.filter = this.indexParams.filter;
            this.requestsTableConfig.updatePageSize(this.pageSize);
            this.requestsTableConfig.updatePageIndex(this.page);
            this.crumbs.push({
              name: this.project.name
            });
            this.crumbs.push({
              name: 'Requests'
            });
            this.tableColumns = this.buildTableColumns();

            if (this.layoutConfigService.isProxied()) {
              this.pollRequestsInterval = setInterval(function () {
                _this5.agentService.showStatus('requests-modified').subscribe(function (res) {
                  if (res && res === _this5.project.id) {
                    console.log('New requests detected...');

                    _this5.getRequests();
                  }
                });
              }, 10000);
            }
          }
        }, {
          key: "ngOnDestroy",
          value: function ngOnDestroy() {
            if (this.pollRequestsInterval) {
              clearInterval(this.pollRequestsInterval);
            }
          } // API Access

        }, {
          key: "createRequest",
          value: function createRequest(data) {
            var _this6 = this;

            var snapshot = this.route.snapshot;
            var project_id = snapshot.queryParams.project_id;
            data.append('project_id', project_id);
            this.requestResource.create(data).subscribe(function (res) {
              _this6.requests = res.list.concat(_this6.requests);
            }, function (error) {});
          }
        }, {
          key: "getRequests",
          value: function getRequests() {
            var _this7 = this;

            var params = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : this.indexParams;
            var snapshot = this.route.snapshot;
            var project_id = snapshot.queryParams.project_id;
            params.project_id = project_id;
            this.requestResource.index(params).subscribe(function (res) {
              _this7.requests = res.list;
              _this7.totalRequests = res.total;

              _this7.updateUrlQueryParams(params);
            }, function (error) {});
          }
        }, {
          key: "updateRequest",
          value: function updateRequest(id, data) {
            var _this8 = this;

            this.requestResource.update(id, data).subscribe(function (res) {
              _this8.getRequests();
            }, function (error) {});
          }
        }, {
          key: "deleteRequest",
          value: function deleteRequest(requestId) {
            var _this9 = this;

            this.requestResource.destroy(requestId).subscribe(function (res) {
              _this9.requests = _this9.requests.filter(function (request) {
                return request.id !== requestId;
              });
            });
          }
        }, {
          key: "downloadRequest",
          value: function downloadRequest(requestId) {
            var _this10 = this;

            this.requestResource.download(requestId).subscribe(function (res) {
              _this10.fileDownload.create(res);
            });
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
          key: "filterRequests",
          value: function filterRequests($event) {
            if (!$event.filter) {
              delete this.indexParams.filter;
            } else {
              this.indexParams.filter = $event.filter;
            }

            this.getRequests();
          } // View Access

        }, {
          key: "openCreateDialog",
          value: function openCreateDialog() {
            var _this11 = this;

            var dialogRef = this.dialog.open(_requests_components_requests_create_requests_create_component__WEBPACK_IMPORTED_MODULE_10__["RequestsCreateComponent"], {
              width: '750px'
            });
            var onCreateSub = dialogRef.componentInstance.onCreate.subscribe(function ($event) {
              _this11.createRequest($event);
            });
            dialogRef.afterClosed().subscribe(function () {
              onCreateSub.unsubscribe();
            });
          }
        }, {
          key: "openEditDialog",
          value: function openEditDialog(request) {
            var _this12 = this;

            var dialogRef = this.dialog.open(_requests_components_requests_edit_requests_edit_component__WEBPACK_IMPORTED_MODULE_11__["RequestsEditComponent"], {
              data: request,
              width: '600px'
            });
            var onEditSub = dialogRef.componentInstance.onEdit.subscribe(function ($event) {
              _this12.updateRequest(request.id, $event);
            });
            dialogRef.afterClosed().subscribe(function () {
              onEditSub.unsubscribe();
            });
          }
        }, {
          key: "viewRequest",
          value: function viewRequest(requestId) {
            var request = this.requests.find(function (candidate) {
              return candidate.id === requestId;
            });
            this.requestDataService.set(request);
            var uri = new this.uri["class"](this.location.path());
            var path = this.file.join(uri.pathname, requestId);
            uri.pathname = path;
            this.router.navigateByUrl(uri.pathname + uri.query);
          }
        }, {
          key: "toggleRequestStar",
          value: function toggleRequestStar(id) {
            var request = this.requests.find(function (s) {
              return s.id === id;
            });

            if (request) {
              request.starred = !request.starred;
              this.updateRequest(id, request);
            }
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
            var curIndex = this.requestsTableConfig.pageIndex;
            var curSize = this.requestsTableConfig.pageSize;
            var newIndex = $event.pageIndex;
            var newSize = $event.pageSize;

            if (curSize !== newSize) {
              this.pageSize = newSize;
              this.requestsTableConfig.updatePageSize(newSize);
            }

            if (curIndex != newIndex) {
              this.page = newIndex;
              this.requestsTableConfig.updatePageIndex(newIndex);
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
            var _this13 = this;

            var queryParams = Object.assign({}, this.indexParams);
            Object.entries(newQueryParams).forEach(function (_ref) {
              var _ref2 = _slicedToArray(_ref, 2),
                  key = _ref2[0],
                  value = _ref2[1];

              queryParams[key] = value;
              _this13.indexParams[key] = value;
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
            var _this14 = this;

            return [{
              label: '',
              property: 'selected',
              type: 'checkbox',
              cssClasses: ['w-6'],
              visible: true,
              canHide: false
            }, {
              label: 'Method',
              property: 'method',
              type: 'text',
              cssClasses: ['text-secondary'],
              visible: true,
              canHide: true
            }, {
              label: 'Host',
              property: 'host',
              type: 'text',
              cssClasses: ['font-medium'],
              visible: true,
              canHide: true
            }, {
              label: 'Path',
              property: 'path',
              type: 'text',
              cssClasses: ['font-medium'],
              visible: true,
              canHide: true
            }, {
              label: 'Status',
              property: 'status',
              type: 'custom',
              cssClasses: ['text-secondary'],
              visible: true,
              canHide: true
            }, {
              label: 'Latency',
              property: 'latency',
              type: 'custom',
              cssClasses: ['text-secondary'],
              visible: true,
              canHide: true
            }, {
              label: 'Created At',
              property: 'created_at',
              type: 'date',
              cssClasses: ['text-secondary'],
              visible: true,
              canHide: true
            }, {
              label: '',
              property: 'starred',
              type: 'toggleButton',
              cssClasses: ['text-secondary', 'w-10'],
              visible: false,
              canHide: false,
              icon: function icon(scenario) {
                return scenario.starred ? _this14.icons.icStar : _this14.icons.icStarBorder;
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

        return RequestsIndexComponent;
      }();

      RequestsIndexComponent.ctorParameters = function () {
        return [{
          type: _services_requests_index_icons_service__WEBPACK_IMPORTED_MODULE_14__["RequestsIndexIcons"]
        }, {
          type: _angular_router__WEBPACK_IMPORTED_MODULE_6__["ActivatedRoute"]
        }, {
          type: _core_http__WEBPACK_IMPORTED_MODULE_8__["AgentService"]
        }, {
          type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MatDialog"]
        }, {
          type: _core_utils__WEBPACK_IMPORTED_MODULE_9__["FileService"]
        }, {
          type: _core_utils__WEBPACK_IMPORTED_MODULE_9__["FileDownload"]
        }, {
          type: _layout_services_layout_config_service__WEBPACK_IMPORTED_MODULE_12__["LayoutConfigService"]
        }, {
          type: _angular_common__WEBPACK_IMPORTED_MODULE_3__["Location"]
        }, {
          type: _services_request_data_service__WEBPACK_IMPORTED_MODULE_13__["RequestDataService"]
        }, {
          type: _core_http__WEBPACK_IMPORTED_MODULE_8__["RequestResource"]
        }, {
          type: _services_requests_table_config_service__WEBPACK_IMPORTED_MODULE_15__["RequestsTableConfig"]
        }, {
          type: _angular_router__WEBPACK_IMPORTED_MODULE_6__["Router"]
        }, {
          type: _angular_router__WEBPACK_IMPORTED_MODULE_6__["ActivatedRoute"]
        }, {
          type: _core_utils__WEBPACK_IMPORTED_MODULE_9__["UriService"]
        }];
      };

      RequestsIndexComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_4__["Component"])({
        selector: 'requests-index',
        template: _raw_loader_requests_index_component_html__WEBPACK_IMPORTED_MODULE_2__["default"],
        animations: [_vex_animations__WEBPACK_IMPORTED_MODULE_7__["stagger40ms"], _vex_animations__WEBPACK_IMPORTED_MODULE_7__["scaleIn400ms"], _vex_animations__WEBPACK_IMPORTED_MODULE_7__["fadeInRight400ms"]],
        styles: [_requests_index_component_scss__WEBPACK_IMPORTED_MODULE_1__["default"]]
      })], RequestsIndexComponent);
      /***/
    },

    /***/
    "ZhHk":
    /*!************************************************************************!*\
      !*** ./src/app/modules/requests/services/requests-resolver.service.ts ***!
      \************************************************************************/

    /*! exports provided: RequestsResolver */

    /***/
    function ZhHk(module, __webpack_exports__, __webpack_require__) {
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
            var queryParams = Object.assign({}, route.queryParams);
            return this.requestResource.index(queryParams);
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
    },

    /***/
    "bcfj":
    /*!*************************************************************!*\
      !*** ./src/app/modules/requests/requests-routing.module.ts ***!
      \*************************************************************/

    /*! exports provided: RequestsRoutingModule */

    /***/
    function bcfj(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "RequestsRoutingModule", function () {
        return RequestsRoutingModule;
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


      var _requests_pages_request_details_request_details_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @requests/pages/request-details/request-details.component */
      "g6n5");
      /* harmony import */


      var _requests_pages_requests_index_requests_index_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @requests/pages/requests-index/requests-index.component */
      "Zf3l");
      /* harmony import */


      var _projects_services_project_resolver_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @projects/services/project-resolver.service */
      "Y1jZ");
      /* harmony import */


      var _requests_services_request_resolver_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @requests/services/request-resolver.service */
      "a+oo");
      /* harmony import */


      var _requests_services_requests_resolver_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @requests/services/requests-resolver.service */
      "ZhHk");
      /* harmony import */


      var _requests_services_response_headers_resolver_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @requests/services/response-headers-resolver.service */
      "qeIL");
      /* harmony import */


      var _requests_services_response_resolver_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @requests/services/response-resolver.service */
      "h8gq");

      var routes = [{
        path: '',
        component: _requests_pages_requests_index_requests_index_component__WEBPACK_IMPORTED_MODULE_4__["RequestsIndexComponent"],
        resolve: {
          requests: _requests_services_requests_resolver_service__WEBPACK_IMPORTED_MODULE_7__["RequestsResolver"],
          project: _projects_services_project_resolver_service__WEBPACK_IMPORTED_MODULE_5__["ProjectResolver"]
        }
      }, {
        path: ':request_id',
        component: _requests_pages_request_details_request_details_component__WEBPACK_IMPORTED_MODULE_3__["RequestDetailsComponent"],
        resolve: {
          request: _requests_services_request_resolver_service__WEBPACK_IMPORTED_MODULE_6__["RequestResolver"],
          response: _requests_services_response_resolver_service__WEBPACK_IMPORTED_MODULE_9__["ResponseResolver"],
          responseHeaders: _requests_services_response_headers_resolver_service__WEBPACK_IMPORTED_MODULE_8__["ResponseHeadersResolver"]
        }
      }];

      var RequestsRoutingModule = function RequestsRoutingModule() {
        _classCallCheck(this, RequestsRoutingModule);
      };

      RequestsRoutingModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]]
      })], RequestsRoutingModule);
      /***/
    },

    /***/
    "la/H":
    /*!******************************************************************************************************************************!*\
      !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/requests/components/requests-edit/requests-edit.component.html ***!
      \******************************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function laH(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "<form (ngSubmit)=\"save()\" [formGroup]=\"form\">\r\n  <div fxLayout=\"row\" fxLayoutAlign=\"start center\" mat-dialog-title>\r\n      <!-- <img *ngIf=\"contact?.imageSrc\" [src]=\"contact?.imageSrc\" class=\"avatar ltr:mr-5 rtl:ml-5\"> -->\r\n    <h2 class=\"headline m-0\" fxFlex=\"auto\">{{ form.get('name').value }}</h2>\r\n\r\n    <button [matMenuTriggerFor]=\"settingsMenu\" class=\"text-secondary\" mat-icon-button type=\"button\" matTooltip=\"Priority\">\r\n      <mat-icon [icIcon]=\"icLabel\" [ngClass]=\"selectedPriority.classes\"></mat-icon>\r\n    </button>\r\n\r\n    <button class=\"text-secondary\" mat-dialog-close mat-icon-button type=\"button\">\r\n      <mat-icon [icIcon]=\"icClose\"></mat-icon>\r\n    </button>\r\n  </div>\r\n\r\n  <mat-divider class=\"-mx-6 text-border\"></mat-divider>\r\n\r\n  <mat-dialog-content fxLayout=\"column\">\r\n    <mat-form-field class=\"mt-6\">\r\n      <mat-label>Name</mat-label>\r\n      <input cdkFocusInitial formControlName=\"name\" matInput>\r\n\r\n      <mat-icon [icIcon]=\"icPerson\" class=\"ltr:mr-3 rtl:ml-3\" matPrefix></mat-icon>\r\n    </mat-form-field>\r\n\r\n    <mat-form-field>\r\n      <mat-label>Description</mat-label>\r\n      <textarea formControlName=\"description\" matInput></textarea>\r\n    </mat-form-field>\r\n  </mat-dialog-content>\r\n\r\n  <mat-dialog-actions align=\"end\">\r\n    <button mat-button mat-dialog-close type=\"button\">CANCEL</button>\r\n    <button color=\"primary\" mat-button type=\"submit\">SAVE CHANGES</button>\r\n  </mat-dialog-actions>\r\n</form>\r\n\r\n<mat-menu #settingsMenu=\"matMenu\" xPosition=\"before\" yPosition=\"below\">\r\n  <button mat-menu-item *ngFor=\"let priority of requestPriorities\" (click)=\"handlePrioritySelect(priority)\">\r\n    <span>{{ priority.name }}</span>\r\n  </button>\r\n</mat-menu>\r\n";
      /***/
    },

    /***/
    "m354":
    /*!********************************************************************************************!*\
      !*** ./src/app/modules/requests/components/requests-create/requests-create.component.scss ***!
      \********************************************************************************************/

    /*! exports provided: default */

    /***/
    function m354(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = ".request-component-wrapper {\n  max-height: 250px;\n  overflow-y: auto;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uLy4uL3JlcXVlc3RzLWNyZWF0ZS5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLGlCQUFBO0VBQ0EsZ0JBQUE7QUFDRiIsImZpbGUiOiJyZXF1ZXN0cy1jcmVhdGUuY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyIucmVxdWVzdC1jb21wb25lbnQtd3JhcHBlciB7XG4gIG1heC1oZWlnaHQ6IDI1MHB4O1xuICBvdmVyZmxvdy15OiBhdXRvO1xufSJdfQ== */";
      /***/
    },

    /***/
    "z1KO":
    /*!*************************************************!*\
      !*** ./src/app/data/builders/request-string.ts ***!
      \*************************************************/

    /*! exports provided: RequestString */

    /***/
    function z1KO(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "RequestString", function () {
        return RequestString;
      });

      var RequestString = /*#__PURE__*/function () {
        function RequestString(request) {
          _classCallCheck(this, RequestString);

          this.REQUEST_TYPE = 1;
          this.CLRF = '\n';

          var uriParser = __webpack_require__(
          /*! url-parse */
          "GBY4");

          var uri = uriParser(request.url);
          var pathname = uri.pathname; // Backend raw request parser errors out if pathname is empty

          if (uri.pathname === '') {
            uri.pathname = '/';
            request.url = uri.toString();
          }

          this.request = request;
          this.lines = [];
          this.requestLine();
          this.headers();
          this.body();
          this.control();
        }

        _createClass(RequestString, [{
          key: "control",
          value: function control() {
            this.lines.unshift("".concat(this.REQUEST_TYPE, " ").concat(this.request.id, " ").concat(new Date().getTime() * 1000));
          }
        }, {
          key: "requestLine",
          value: function requestLine() {
            this.lines.push("".concat(this.request.method, " ").concat(this.request.url, " HTTP/1.1"));
          }
        }, {
          key: "headers",
          value: function headers() {
            var _this15 = this;

            this.request.headers.forEach(function (header) {
              _this15.lines.push("".concat(header.name, ": ").concat(header.value));
            });
          }
        }, {
          key: "body",
          value: function body() {
            this.lines.push("".concat(this.CLRF).concat(this.request.body || ''));
          }
        }, {
          key: "get",
          value: function get() {
            return this.lines.join(this.CLRF);
          }
        }]);

        return RequestString;
      }();
      /***/

    }
  }]);
})();
//# sourceMappingURL=requests-requests-module-es5.js.map