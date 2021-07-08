(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["default~endpoints-endpoints-module~requests-requests-module~scenarios-scenarios-module"],{

/***/ "+V3c":
/*!**************************************************!*\
  !*** ./src/app/shared/components/modal/index.ts ***!
  \**************************************************/
/*! exports provided: CreateModalComponent, EditModalComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _create_modal_create_modal_component__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./create-modal/create-modal.component */ "2yMs");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "CreateModalComponent", function() { return _create_modal_create_modal_component__WEBPACK_IMPORTED_MODULE_0__["CreateModalComponent"]; });

/* harmony import */ var _edit_modal_edit_modal_component__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./edit-modal/edit-modal.component */ "ZyFB");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "EditModalComponent", function() { return _edit_modal_edit_modal_component__WEBPACK_IMPORTED_MODULE_1__["EditModalComponent"]; });





/***/ }),

/***/ "/EtC":
/*!************************************************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/requests/pages/request-details/components/response-aliases-create/response-aliases-create.component.html ***!
  \************************************************************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div class=\"p-5\" fxLayout=\"row\" >\n  <form [formGroup]=\"form\" fxFlex=\"auto\">\n    <h3 class=\"mb-5\">Create Alias</h3>\n    <div>\n       <mat-form-field>\n         <mat-label>Alias Name</mat-label>\n         <input matInput placeholder=':user_id' formControlName=\"aliasName\">\n       </mat-form-field>\n     </div>\n\n     <div>\n       <mat-form-field>\n         <mat-label>Response Resolver</mat-label>\n         <input matInput placeholder='\"id\":\"1\"' formControlName=\"response_resolver\">\n       </mat-form-field>\n     </div>\n\n     <div>\n       <button (click)=\"testResponseResolver()\" mat-button color=\"primary\">\n         TEST\n       </button>\n       <button (click)=\"create()\" mat-button color=\"primary\">\n         CREATE\n       </button>\n     </div>\n  </form>\n  <pre fxFlex=\"auto\">{{ responseResolverValues }}</pre>\n</div>\n");

/***/ }),

/***/ "/vI3":
/*!************************************************************************************!*\
  !*** ./src/app/modules/aliases/components/aliases-create/aliases-create.module.ts ***!
  \************************************************************************************/
/*! exports provided: AliasesCreateModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AliasesCreateModule", function() { return AliasesCreateModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ "s7LF");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/dialog */ "iELJ");
/* harmony import */ var _angular_material_divider__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/divider */ "BSbQ");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/material/input */ "e6WT");
/* harmony import */ var _angular_material_menu__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/material/menu */ "rJgo");
/* harmony import */ var _angular_material_radio__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @angular/material/radio */ "zQhy");
/* harmony import */ var _angular_material_select__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @angular/material/select */ "ZTz/");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var ngx_dropzone__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ngx-dropzone */ "tq8E");
/* harmony import */ var _aliases_create_component__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ./aliases-create.component */ "tedC");
















let AliasesCreateModule = class AliasesCreateModule {
};
AliasesCreateModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _angular_material_dialog__WEBPACK_IMPORTED_MODULE_6__["MatDialogModule"],
            _angular_material_input__WEBPACK_IMPORTED_MODULE_9__["MatInputModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_5__["MatButtonModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_8__["MatIconModule"],
            _angular_material_radio__WEBPACK_IMPORTED_MODULE_11__["MatRadioModule"],
            _angular_material_select__WEBPACK_IMPORTED_MODULE_12__["MatSelectModule"],
            _angular_material_menu__WEBPACK_IMPORTED_MODULE_10__["MatMenuModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_13__["IconModule"],
            _angular_material_divider__WEBPACK_IMPORTED_MODULE_7__["MatDividerModule"],
            ngx_dropzone__WEBPACK_IMPORTED_MODULE_14__["NgxDropzoneModule"],
        ],
        declarations: [_aliases_create_component__WEBPACK_IMPORTED_MODULE_15__["AliasesCreateComponent"]],
        entryComponents: [_aliases_create_component__WEBPACK_IMPORTED_MODULE_15__["AliasesCreateComponent"]],
        exports: [_aliases_create_component__WEBPACK_IMPORTED_MODULE_15__["AliasesCreateComponent"]],
    })
], AliasesCreateModule);



/***/ }),

/***/ "2yMs":
/*!********************************************************************************!*\
  !*** ./src/app/shared/components/modal/create-modal/create-modal.component.ts ***!
  \********************************************************************************/
/*! exports provided: CreateModalComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "CreateModalComponent", function() { return CreateModalComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_create_modal_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./create-modal.component.html */ "ReB1");
/* harmony import */ var _create_modal_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./create-modal.component.scss */ "7DGy");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/dialog */ "iELJ");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/forms */ "s7LF");






let CreateModalComponent = class CreateModalComponent {
    constructor(config, dialogRef, fb) {
        this.config = config;
        this.dialogRef = dialogRef;
        this.fb = fb;
        this.onCreate = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
    }
    ngOnInit() {
        this.title = this.config.title;
        this.fields = this.config.fields;
        const fieldHash = {};
        this.fields.forEach(field => {
            fieldHash[field.id] = null;
        });
        this.form = this.fb.group(fieldHash);
    }
    create() {
        const form = this.form.value;
        this.onCreate.emit(form);
        this.dialogRef.close();
    }
    cancel() {
        this.dialogRef.close();
    }
};
CreateModalComponent.ctorParameters = () => [
    { type: undefined, decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Inject"], args: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_4__["MAT_DIALOG_DATA"],] }] },
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_4__["MatDialogRef"] },
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_5__["FormBuilder"] }
];
CreateModalComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'create-modal',
        template: _raw_loader_create_modal_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_create_modal_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], CreateModalComponent);



/***/ }),

/***/ "7DGy":
/*!**********************************************************************************!*\
  !*** ./src/app/shared/components/modal/create-modal/create-modal.component.scss ***!
  \**********************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("mat-form-field {\n  width: 100%;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uLy4uL2NyZWF0ZS1tb2RhbC5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLFdBQUE7QUFDRiIsImZpbGUiOiJjcmVhdGUtbW9kYWwuY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyJtYXQtZm9ybS1maWVsZCB7XG4gIHdpZHRoOiAxMDAlO1xufSJdfQ== */");

/***/ }),

/***/ "9CFt":
/*!**********************************************************************************!*\
  !*** ./src/app/modules/requests/pages/request-details/request-details.module.ts ***!
  \**********************************************************************************/
/*! exports provided: RequestDetailsModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RequestDetailsModule", function() { return RequestDetailsModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/dialog */ "iELJ");
/* harmony import */ var _angular_material_divider__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/divider */ "BSbQ");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _angular_material_slide_toggle__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/material/slide-toggle */ "jMqV");
/* harmony import */ var _angular_material_tabs__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/material/tabs */ "M9ds");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _vex_components_breadcrumbs_breadcrumbs_module__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @vex/components/breadcrumbs/breadcrumbs.module */ "J0XA");
/* harmony import */ var _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @vex/components/page-layout/page-layout.module */ "7lCJ");
/* harmony import */ var _vex_directives_container_container_module__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @vex/directives/container/container.module */ "68Yx");
/* harmony import */ var _aliases_components_aliases_create_aliases_create_module__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @aliases/components/aliases-create/aliases-create.module */ "/vI3");
/* harmony import */ var _shared_components_modal_modal_module__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @shared/components/modal/modal.module */ "iphE");
/* harmony import */ var _components_request_data_table_request_data_table_module__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ./components/request-data-table/request-data-table.module */ "bLiU");
/* harmony import */ var _components_response_aliases_create_response_aliases_create_module__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! ./components/response-aliases-create/response-aliases-create.module */ "ote9");
/* harmony import */ var _request_details_component__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! ./request-details.component */ "g6n5");
/* harmony import */ var _services_request_details_icons_service__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! ./services/request-details-icons.service */ "rBbm");




















let RequestDetailsModule = class RequestDetailsModule {
};
RequestDetailsModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_request_details_component__WEBPACK_IMPORTED_MODULE_18__["RequestDetailsComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_4__["MatButtonModule"],
            _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MatDialogModule"],
            _angular_material_tabs__WEBPACK_IMPORTED_MODULE_9__["MatTabsModule"],
            _angular_material_divider__WEBPACK_IMPORTED_MODULE_6__["MatDividerModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_7__["MatIconModule"],
            _angular_material_slide_toggle__WEBPACK_IMPORTED_MODULE_8__["MatSlideToggleModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_10__["IconModule"],
            _vex_components_breadcrumbs_breadcrumbs_module__WEBPACK_IMPORTED_MODULE_11__["BreadcrumbsModule"],
            _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_12__["PageLayoutModule"],
            _vex_directives_container_container_module__WEBPACK_IMPORTED_MODULE_13__["ContainerModule"],
            _aliases_components_aliases_create_aliases_create_module__WEBPACK_IMPORTED_MODULE_14__["AliasesCreateModule"],
            _shared_components_modal_modal_module__WEBPACK_IMPORTED_MODULE_15__["ModalModule"],
            _components_request_data_table_request_data_table_module__WEBPACK_IMPORTED_MODULE_16__["RequestDataTableModule"],
            _components_response_aliases_create_response_aliases_create_module__WEBPACK_IMPORTED_MODULE_17__["ResponseAliasesCreateModule"],
        ],
        providers: [_services_request_details_icons_service__WEBPACK_IMPORTED_MODULE_19__["RequestDetailsIcons"]],
    })
], RequestDetailsModule);



/***/ }),

/***/ "A17n":
/*!**********************************************************!*\
  !*** ./node_modules/@iconify/icons-ic/twotone-create.js ***!
  \**********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

var data = {
	"body": "<path opacity=\".3\" d=\"M5 18.08V19h.92l9.06-9.06l-.92-.92z\" fill=\"currentColor\"/><path d=\"M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM5.92 19H5v-.92l9.06-9.06l.92.92L5.92 19zM20.71 5.63l-2.34-2.34c-.2-.2-.45-.29-.71-.29s-.51.1-.7.29l-1.83 1.83l3.75 3.75l1.83-1.83a.996.996 0 0 0 0-1.41z\" fill=\"currentColor\"/>",
	"width": 24,
	"height": 24
};
exports.__esModule = true;
exports.default = data;


/***/ }),

/***/ "D0Ub":
/*!**********************************************************************************************************************************!*\
  !*** ./src/app/modules/requests/pages/request-details/components/response-aliases-create/response-aliases-create.component.scss ***!
  \**********************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJyZXNwb25zZS1hbGlhc2VzLWNyZWF0ZS5jb21wb25lbnQuc2NzcyJ9 */");

/***/ }),

/***/ "DaE0":
/*!*************************************************************!*\
  !*** ./node_modules/@iconify/icons-ic/twotone-cloud-off.js ***!
  \*************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

var data = {
	"body": "<path opacity=\".3\" d=\"M22 15c0-1.66-1.34-3-3-3h-1.5v-.5C17.5 8.46 15.04 6 12 6c-.77 0-1.49.17-2.16.46L20.79 17.4c.73-.55 1.21-1.41 1.21-2.4zM2 14c0 2.21 1.79 4 4 4h9.73l-8-8H6c-2.21 0-4 1.79-4 4z\" fill=\"currentColor\"/><path d=\"M19.35 10.04A7.49 7.49 0 0 0 12 4c-1.33 0-2.57.36-3.65.97l1.49 1.49C10.51 6.17 11.23 6 12 6c3.04 0 5.5 2.46 5.5 5.5v.5H19a2.996 2.996 0 0 1 1.79 5.4l1.41 1.41c1.09-.92 1.8-2.27 1.8-3.81c0-2.64-2.05-4.78-4.65-4.96zM3 5.27l2.77 2.77h-.42A5.994 5.994 0 0 0 0 14c0 3.31 2.69 6 6 6h11.73l2 2l1.41-1.41L4.41 3.86L3 5.27zM7.73 10l8 8H6c-2.21 0-4-1.79-4-4s1.79-4 4-4h1.73z\" fill=\"currentColor\"/>",
	"width": 24,
	"height": 24
};
exports.__esModule = true;
exports.default = data;


/***/ }),

/***/ "De0L":
/*!*********************************************************!*\
  !*** ./node_modules/@iconify/icons-ic/twotone-timer.js ***!
  \*********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

var data = {
	"body": "<path opacity=\".3\" d=\"M12.07 6.01c-3.87 0-7 3.13-7 7s3.13 7 7 7s7-3.13 7-7s-3.13-7-7-7zm1 8h-2v-6h2v6z\" fill=\"currentColor\"/><path d=\"M9.07 1.01h6v2h-6zm2 7h2v6h-2zm8.03-.62l1.42-1.42c-.43-.51-.9-.99-1.41-1.41l-1.42 1.42A8.962 8.962 0 0 0 12.07 4c-4.97 0-9 4.03-9 9s4.02 9 9 9A8.994 8.994 0 0 0 19.1 7.39zm-7.03 12.62c-3.87 0-7-3.13-7-7s3.13-7 7-7s7 3.13 7 7s-3.13 7-7 7z\" fill=\"currentColor\"/>",
	"width": 24,
	"height": 24
};
exports.__esModule = true;
exports.default = data;


/***/ }),

/***/ "Ell1":
/*!*********************************************************!*\
  !*** ./node_modules/@iconify/icons-ic/twotone-group.js ***!
  \*********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

var data = {
	"body": "<circle cx=\"9\" cy=\"8.5\" opacity=\".3\" r=\"1.5\" fill=\"currentColor\"/><path opacity=\".3\" d=\"M4.34 17h9.32c-.84-.58-2.87-1.25-4.66-1.25s-3.82.67-4.66 1.25z\" fill=\"currentColor\"/><path d=\"M9 12c1.93 0 3.5-1.57 3.5-3.5S10.93 5 9 5S5.5 6.57 5.5 8.5S7.07 12 9 12zm0-5c.83 0 1.5.67 1.5 1.5S9.83 10 9 10s-1.5-.67-1.5-1.5S8.17 7 9 7zm0 6.75c-2.34 0-7 1.17-7 3.5V19h14v-1.75c0-2.33-4.66-3.5-7-3.5zM4.34 17c.84-.58 2.87-1.25 4.66-1.25s3.82.67 4.66 1.25H4.34zm11.7-3.19c1.16.84 1.96 1.96 1.96 3.44V19h4v-1.75c0-2.02-3.5-3.17-5.96-3.44zM15 12c1.93 0 3.5-1.57 3.5-3.5S16.93 5 15 5c-.54 0-1.04.13-1.5.35c.63.89 1 1.98 1 3.15s-.37 2.26-1 3.15c.46.22.96.35 1.5.35z\" fill=\"currentColor\"/>",
	"width": 24,
	"height": 24
};
exports.__esModule = true;
exports.default = data;


/***/ }),

/***/ "GHMy":
/*!******************************************************************************!*\
  !*** ./src/app/shared/components/modal/edit-modal/edit-modal.component.scss ***!
  \******************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("mat-form-field {\n  width: 100%;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uLy4uL2VkaXQtbW9kYWwuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSxXQUFBO0FBQ0YiLCJmaWxlIjoiZWRpdC1tb2RhbC5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbIm1hdC1mb3JtLWZpZWxkIHtcbiAgd2lkdGg6IDEwMCU7XG59Il19 */");

/***/ }),

/***/ "Md2b":
/*!**********************************************************************************************************************!*\
  !*** ./src/app/modules/requests/pages/request-details/components/request-data-table/request-data-table.component.ts ***!
  \**********************************************************************************************************************/
/*! exports provided: RequestDataTableComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RequestDataTableComponent", function() { return RequestDataTableComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_request_data_table_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./request-data-table.component.html */ "iSh1");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_material_paginator__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/material/paginator */ "5QHs");
/* harmony import */ var _angular_material_sort__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/sort */ "LUZP");
/* harmony import */ var _angular_material_table__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/table */ "OaSA");
/* harmony import */ var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @iconify/icons-ic/twotone-add */ "7wwx");
/* harmony import */ var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @iconify/icons-ic/twotone-close */ "5mnX");
/* harmony import */ var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @iconify/icons-ic/twotone-cloud-download */ "MzEE");
/* harmony import */ var _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _iconify_icons_ic_twotone_create__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @iconify/icons-ic/twotone-create */ "A17n");
/* harmony import */ var _iconify_icons_ic_twotone_create__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_create__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @iconify/icons-ic/twotone-delete */ "e3EN");
/* harmony import */ var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @iconify/icons-ic/twotone-edit */ "pN9m");
/* harmony import */ var _iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var _iconify_icons_ic_twotone_link__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @iconify/icons-ic/twotone-link */ "h+Y6");
/* harmony import */ var _iconify_icons_ic_twotone_link__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_link__WEBPACK_IMPORTED_MODULE_12__);
/* harmony import */ var _iconify_icons_ic_twotone_more_horiz__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @iconify/icons-ic/twotone-more-horiz */ "SqwC");
/* harmony import */ var _iconify_icons_ic_twotone_more_horiz__WEBPACK_IMPORTED_MODULE_13___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_more_horiz__WEBPACK_IMPORTED_MODULE_13__);
/* harmony import */ var _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @vex/utils/tailwindcss */ "XXSj");















let RequestDataTableComponent = class RequestDataTableComponent {
    constructor() {
        this.pageSize = 10;
        this.editable = true;
        this.createOrEditAlias = new _angular_core__WEBPACK_IMPORTED_MODULE_2__["EventEmitter"]();
        this.createComponent = new _angular_core__WEBPACK_IMPORTED_MODULE_2__["EventEmitter"]();
        this.editComponent = new _angular_core__WEBPACK_IMPORTED_MODULE_2__["EventEmitter"]();
        this.removeAlias = new _angular_core__WEBPACK_IMPORTED_MODULE_2__["EventEmitter"]();
        this.removeComponent = new _angular_core__WEBPACK_IMPORTED_MODULE_2__["EventEmitter"]();
        this.dataSource = new _angular_material_table__WEBPACK_IMPORTED_MODULE_5__["MatTableDataSource"]();
        this.icMoreHoriz = _iconify_icons_ic_twotone_more_horiz__WEBPACK_IMPORTED_MODULE_13___default.a;
        this.icCloudDownload = _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_8___default.a;
        this.icLink = _iconify_icons_ic_twotone_link__WEBPACK_IMPORTED_MODULE_12___default.a;
        this.icDelete = _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_10___default.a;
        this.icCreate = _iconify_icons_ic_twotone_create__WEBPACK_IMPORTED_MODULE_9___default.a;
        this.icClose = _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_7___default.a;
        this.icAdd = _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_6___default.a;
        this.icEdit = _iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_11___default.a;
        this.theme = _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_14__["default"];
    }
    ngOnInit() { }
    ngOnChanges(changes) {
        if (changes.columns) {
            this.visibleColumns = changes.columns.currentValue.map(column => column.property);
        }
        if (changes.data && changes.data.currentValue) {
            this.dataSource.data = changes.data.currentValue;
        }
    }
    shouldRenderPre(content) {
        if (content === undefined) {
            return false;
        }
        if (typeof content !== 'string') {
            return false;
        }
        return content.indexOf('\n') !== -1;
    }
    renderText(text) {
        if (text === undefined || text === null) {
            return 'N/A';
        }
        return text.length > 80 ? (text.slice(0, 80) + '...') : text;
    }
    ngAfterViewInit() {
        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
    }
};
RequestDataTableComponent.ctorParameters = () => [];
RequestDataTableComponent.propDecorators = {
    componentType: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Input"] }],
    title: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Input"] }],
    data: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Input"] }],
    columns: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Input"] }],
    pageSize: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Input"] }],
    editable: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Input"] }],
    createOrEditAlias: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Output"] }],
    createComponent: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Output"] }],
    editComponent: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Output"] }],
    removeAlias: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Output"] }],
    removeComponent: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Output"] }],
    paginator: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["ViewChild"], args: [_angular_material_paginator__WEBPACK_IMPORTED_MODULE_3__["MatPaginator"], { static: true },] }],
    sort: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["ViewChild"], args: [_angular_material_sort__WEBPACK_IMPORTED_MODULE_4__["MatSort"], { static: true },] }]
};
RequestDataTableComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["Component"])({
        selector: 'request-data-table',
        template: _raw_loader_request_data_table_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
    })
], RequestDataTableComponent);



/***/ }),

/***/ "ReB1":
/*!************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/shared/components/modal/create-modal/create-modal.component.html ***!
  \************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div class=\"p-5\" fxLayout=\"row\" >\n  <form [formGroup]=\"form\" fxFlex=\"auto\">\n    <h3 class=\"mb-5\">Create {{ title }}</h3>\n    <ng-container *ngFor=\"let field of fields\" [ngSwitch]=\"field.type\">\n      <p *ngSwitchCase=\"'input'\">\n        <mat-form-field>\n          <mat-label>{{ field.label }}</mat-label>\n          <input\n            matInput\n            formControlName=\"{{ field.id }}\"\n          />\n        </mat-form-field>\n      </p>\n    </ng-container>\n    <div>\n      <button (click)=\"create()\" mat-button color=\"primary\">\n        CREATE\n      </button>\n      <button (click)=\"cancel()\" mat-button color=\"default\">\n        CANCEL\n      </button>\n    </div>\n  </form>\n</div>\n");

/***/ }),

/***/ "SqwC":
/*!**************************************************************!*\
  !*** ./node_modules/@iconify/icons-ic/twotone-more-horiz.js ***!
  \**************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

var data = {
	"body": "<path d=\"M6 10c-1.1 0-2 .9-2 2s.9 2 2 2s2-.9 2-2s-.9-2-2-2zm12 0c-1.1 0-2 .9-2 2s.9 2 2 2s2-.9 2-2s-.9-2-2-2zm-6 0c-1.1 0-2 .9-2 2s.9 2 2 2s2-.9 2-2s-.9-2-2-2z\" fill=\"currentColor\"/>",
	"width": 24,
	"height": 24
};
exports.__esModule = true;
exports.default = data;


/***/ }),

/***/ "TbEa":
/*!********************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/shared/components/modal/edit-modal/edit-modal.component.html ***!
  \********************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div class=\"p-3\" fxLayout=\"row\" >\n  <form [formGroup]=\"form\" fxFlex=\"auto\">\n    <div class=\"mb-5\" fxLayout=\"row\" fxLayoutAlign=\"space-between center\">\n      <h3>Edit {{ title }}</h3>\n      <div *ngIf=\"moreActions\">\n        <ng-container *ngTemplateOutlet=\"moreActions\"></ng-container>\n      </div>\n    </div>\n    <ng-container *ngFor=\"let field of fields\" [ngSwitch]=\"field.type\">\n      <p *ngSwitchCase=\"'input'\">\n        <mat-form-field>\n          <mat-label>{{ field.label }}</mat-label>\n          <input\n            matInput\n            formControlName=\"{{ field.id }}\"\n          />\n        </mat-form-field>\n      </p>\n      <p *ngSwitchCase=\"'textarea'\">\n        <mat-form-field>\n          <mat-label>{{ field.label }}</mat-label>\n          <textarea\n            matInput\n            formControlName=\"{{ field.id }}\"\n            rows=\"field.rows || 10\"\n          >\n          </textarea>\n        </mat-form-field>\n      </p>\n    </ng-container>\n    <div fxLayout=\"row\" fxLayoutAlign=\"end center\">\n      <button (click)=\"update()\" mat-button color=\"primary\">\n        UPDATE\n      </button>\n      <button (click)=\"cancel()\" mat-button color=\"default\">\n        CANCEL\n      </button>\n    </div>\n  </form>\n</div>\n");

/***/ }),

/***/ "TdxM":
/*!********************************************************************************************************************************!*\
  !*** ./src/app/modules/requests/pages/request-details/components/response-aliases-create/response-aliases-create.component.ts ***!
  \********************************************************************************************************************************/
/*! exports provided: ResponseAliasesCreateComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ResponseAliasesCreateComponent", function() { return ResponseAliasesCreateComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_response_aliases_create_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./response-aliases-create.component.html */ "/EtC");
/* harmony import */ var _response_aliases_create_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./response-aliases-create.component.scss */ "D0Ub");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/forms */ "s7LF");
/* harmony import */ var _core_http_alias_resource_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @core/http/alias-resource.service */ "4GLy");
/* harmony import */ var _core_http_response_resolver_resource_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @core/http/response-resolver-resource.service */ "3aTg");
/* harmony import */ var _core_utils_json_search_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @core/utils/json-search.service */ "fHeU");









let ResponseAliasesCreateComponent = class ResponseAliasesCreateComponent {
    constructor(jsonSearch, fb, aliasResource, responseResolverResource, route) {
        this.jsonSearch = jsonSearch;
        this.fb = fb;
        this.aliasResource = aliasResource;
        this.responseResolverResource = responseResolverResource;
        this.route = route;
        this.responseResolverValues = '';
    }
    ngOnInit() {
        this.form = this.fb.group({
            aliasName: null,
            response_resolver: null,
        });
    }
    testResponseResolver() {
        const form = this.form.value;
        const query = form.response_resolver;
        const res = this.jsonSearch.search(JSON.parse(this.responseData.text), query);
        this.responseResolverValues = res.join('\n');
    }
    create() {
        const component = this.responseData;
        const form = this.form.value;
        const aliasName = form.aliasName;
        const query = form.response_resolver;
        const snapshot = this.route.snapshot;
        const projectId = snapshot.queryParams.projectId;
        this.aliasResource.create({
            component_id: component.id,
            component_type: component.type,
            name: aliasName,
            project_id: projectId,
        }).subscribe((res) => {
            this.createResponseResolver(this.responseData.id, res.id, query);
        });
    }
    createResponseResolver(responseId, aliasId, query) {
        this.responseResolverResource.create(this.requestData.endpointId, {
            response_id: responseId,
            alias_id: aliasId,
            query,
        }).subscribe((res) => {
        });
    }
};
ResponseAliasesCreateComponent.ctorParameters = () => [
    { type: _core_utils_json_search_service__WEBPACK_IMPORTED_MODULE_8__["JsonSearch"] },
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_5__["FormBuilder"] },
    { type: _core_http_alias_resource_service__WEBPACK_IMPORTED_MODULE_6__["AliasResource"] },
    { type: _core_http_response_resolver_resource_service__WEBPACK_IMPORTED_MODULE_7__["ResponseResolverResource"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["ActivatedRoute"] }
];
ResponseAliasesCreateComponent.propDecorators = {
    requestData: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"] }],
    responseData: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"] }]
};
ResponseAliasesCreateComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'response-aliases-create',
        template: _raw_loader_response_aliases_create_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_response_aliases_create_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], ResponseAliasesCreateComponent);



/***/ }),

/***/ "Y1jZ":
/*!***********************************************************************!*\
  !*** ./src/app/modules/projects/services/project-resolver.service.ts ***!
  \***********************************************************************/
/*! exports provided: ProjectResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectResolver", function() { return ProjectResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs/operators */ "kU1M");
/* harmony import */ var _core_http_project_resource_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @core/http/project-resource.service */ "4UAC");
/* harmony import */ var _data_schema_project__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @data/schema/project */ "2RYP");
/* harmony import */ var _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @projects/services/project-data.service */ "oyjd");






let ProjectResolver = class ProjectResolver {
    constructor(projectResource, projectDataService) {
        this.projectResource = projectResource;
        this.projectDataService = projectDataService;
    }
    resolve(route) {
        const projectId = route.queryParams.project_id || route.params.project_id || route.parent.params.project_id;
        return this.projectResource.show(projectId).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["tap"])((project) => {
            this.projectDataService.set(new _data_schema_project__WEBPACK_IMPORTED_MODULE_4__["Project"](project));
        }));
    }
};
ProjectResolver.ctorParameters = () => [
    { type: _core_http_project_resource_service__WEBPACK_IMPORTED_MODULE_3__["ProjectResource"] },
    { type: _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_5__["ProjectDataService"] }
];
ProjectResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], ProjectResolver);



/***/ }),

/***/ "ZyFB":
/*!****************************************************************************!*\
  !*** ./src/app/shared/components/modal/edit-modal/edit-modal.component.ts ***!
  \****************************************************************************/
/*! exports provided: EditModalComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "EditModalComponent", function() { return EditModalComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_edit_modal_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./edit-modal.component.html */ "TbEa");
/* harmony import */ var _edit_modal_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./edit-modal.component.scss */ "GHMy");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/dialog */ "iELJ");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/forms */ "s7LF");






let EditModalComponent = class EditModalComponent {
    constructor(config, dialogRef, fb) {
        this.config = config;
        this.dialogRef = dialogRef;
        this.fb = fb;
        this.onEdit = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
    }
    ngOnInit() {
        this.title = this.config.title;
        this.fields = this.config.fields;
        this.data = this.config.data || {};
        const fieldHash = {};
        this.fields.forEach(field => {
            fieldHash[field.id] = this.data[field.id];
        });
        this.form = this.fb.group(fieldHash);
    }
    update() {
        const form = this.form.value;
        this.onEdit.emit(form);
        this.dialogRef.close();
    }
    cancel() {
        this.dialogRef.close();
    }
};
EditModalComponent.ctorParameters = () => [
    { type: undefined, decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Inject"], args: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_4__["MAT_DIALOG_DATA"],] }] },
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_4__["MatDialogRef"] },
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_5__["FormBuilder"] }
];
EditModalComponent.propDecorators = {
    moreActions: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"] }]
};
EditModalComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'edit-modal',
        template: _raw_loader_edit_modal_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_edit_modal_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], EditModalComponent);



/***/ }),

/***/ "a+oo":
/*!***********************************************************************!*\
  !*** ./src/app/modules/requests/services/request-resolver.service.ts ***!
  \***********************************************************************/
/*! exports provided: RequestResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RequestResolver", function() { return RequestResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _core_http_request_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @core/http/request-resource.service */ "4/Wj");



let RequestResolver = class RequestResolver {
    constructor(requestResource) {
        this.requestResource = requestResource;
    }
    resolve(route) {
        return this.requestResource.show(route.params.request_id, { project_id: route.queryParams.project_id });
    }
};
RequestResolver.ctorParameters = () => [
    { type: _core_http_request_resource_service__WEBPACK_IMPORTED_MODULE_2__["RequestResource"] }
];
RequestResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], RequestResolver);



/***/ }),

/***/ "bLiU":
/*!*******************************************************************************************************************!*\
  !*** ./src/app/modules/requests/pages/request-details/components/request-data-table/request-data-table.module.ts ***!
  \*******************************************************************************************************************/
/*! exports provided: RequestDataTableModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RequestDataTableModule", function() { return RequestDataTableModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _angular_material_paginator__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/paginator */ "5QHs");
/* harmony import */ var _angular_material_sort__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/sort */ "LUZP");
/* harmony import */ var _angular_material_table__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/material/table */ "OaSA");
/* harmony import */ var _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/material/tooltip */ "ZFy/");
/* harmony import */ var _vex_pipes_color_color_fade_module__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @vex/pipes/color/color-fade.module */ "Chvm");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _request_data_table_component__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./request-data-table.component */ "Md2b");













let RequestDataTableModule = class RequestDataTableModule {
};
RequestDataTableModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_request_data_table_component__WEBPACK_IMPORTED_MODULE_12__["RequestDataTableComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_material_table__WEBPACK_IMPORTED_MODULE_8__["MatTableModule"],
            _angular_material_paginator__WEBPACK_IMPORTED_MODULE_6__["MatPaginatorModule"],
            _angular_material_sort__WEBPACK_IMPORTED_MODULE_7__["MatSortModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_9__["MatTooltipModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_4__["MatButtonModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_5__["MatIconModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_11__["IconModule"],
            _vex_pipes_color_color_fade_module__WEBPACK_IMPORTED_MODULE_10__["ColorFadeModule"],
        ],
        exports: [_request_data_table_component__WEBPACK_IMPORTED_MODULE_12__["RequestDataTableComponent"]],
    })
], RequestDataTableModule);



/***/ }),

/***/ "bdKA":
/*!*****************************************************************************************!*\
  !*** ./src/app/modules/aliases/components/aliases-create/aliases-create.component.scss ***!
  \*****************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJhbGlhc2VzLWNyZWF0ZS5jb21wb25lbnQuc2NzcyJ9 */");

/***/ }),

/***/ "csGO":
/*!*****************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/requests/pages/request-details/request-details.component.html ***!
  \*****************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<vex-page-layout mode=\"card\">\n\n<vex-page-layout-header class=\"vex-layout-theme\" fxLayout=\"column\" fxLayoutAlign=\"center start\">\n  <div class=\"container\">\n    <h1 class=\"title mt-0 mb-1\">Request Details</h1>\n    <vex-breadcrumbs [crumbs]=\"crumbs\"></vex-breadcrumbs>\n  </div>\n</vex-page-layout-header>\n\n<vex-page-layout-content class=\"container\">\n  <div class=\"card\">\n    <mat-tab-group (selectedTabChange)=\"handleTabChange($event)\">\n      <mat-tab label=\"Response\">\n        <div class=\"p-3\">\n          <div class=\"overflow-auto w-full\" fxLayout=\"column\">\n            <!-- Latency -->\n            <div class=\"border-b py-4 px-6 flex-container\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n              <h2 class=\"m-0 title\" fxFlex=\"auto\">Latency</h2>\n\n              <button (click)=\"openEditResponseLatencyDialog()\" mat-icon-button type=\"button\">\n                <mat-icon [icIcon]=\"icons.icEdit\" class=\"text-secondary\"></mat-icon>\n              </button>\n            </div>\n\n            <div class=\"px-6 py-2\">\n              {{ request.latency }} ms\n            </div>\n\n            <!-- Status -->\n            <div class=\"border-b py-4 px-6 flex-container\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n              <h2 class=\"m-0 title\" fxFlex=\"auto\">Status</h2>\n\n              <button (click)=\"openEditResponseLatencyDialog()\" mat-icon-button type=\"button\">\n                <mat-icon [icIcon]=\"icons.icEdit\" class=\"text-secondary\"></mat-icon>\n              </button>\n            </div>\n\n            <div class=\"px-6 py-2\">\n              {{ request.status }}\n            </div>\n\n            <mat-tab-group class=\"mt-2\" [color]=\"'warn'\">\n\n              <!-- Body -->\n              <mat-tab label=\"Body\">\n                <div class=\"border-b py-4 px-6 flex-container\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n                  <mat-slide-toggle\n                    [checked]=\"renderPrettyResponse\"\n                    (change)=\"toggleRenderPrettyResponse($event)\"\n                  >\n                    {{ renderPrettyResponse ? 'Pretty' : 'Raw' }}\n                  </mat-slide-toggle>\n                  \n                  <span fxFlex></span>\n\n                  <button (click)=\"openEditComponentDialog(responseData, editResponseMoreActions)\" mat-icon-button type=\"button\">\n                    <mat-icon [icIcon]=\"icons.icEdit\" class=\"text-secondary\"></mat-icon>\n                  </button>\n                </div>\n\n                <div class=\"px-3\" *ngIf=\"responseData\">\n                  <pre class=\"m-3 response-text\">{{ responseData.text }}</pre>\n                </div>\n              </mat-tab>\n\n              <mat-tab label=\"Headers\">\n                <request-data-table\n                  [componentType]=\"componentTypes.ResponseHeader\"\n                  [title]=\"responseHeaderTitle\"\n                  [columns]=\"responseHeaderColumns\"\n                  [data]=\"responseHeaderData\"\n                  [editable]=\"true\"\n                  (createComponent)=\"openCreateComponentDialog($event)\"\n                  (editComponent)=\"openEditComponentDialog($event)\"\n                  (removeComponent)=\"removeComponent($event)\"\n                  class=\"w-full overflow-auto shadow\" gdColumn=\"1 / span 2\"\n                  gdColumn.lt-md=\"1 / -1\"\n                  gdColumn.lt-sm=\"1\"></request-data-table>\n              </mat-tab>\n            </mat-tab-group>\n          </div>\n        </div>\n\n        <!-- <response-aliases-create *ngIf=\"responseData.isJson\"\n          [responseData]=\"responseData\"\n          [request]=\"request\"></response-aliases-create> -->\n      </mat-tab>\n\n      <mat-tab label=\"General\">\n        <div class=\"p-3\">\n          <!-- <request-data-table\n            [componentType]=\"componentTypes.PathSegment\"\n            [title]=\"pathSegmentTitle\"\n            [columns]=\"pathSegmentColumns\"\n            [data]=\"pathSegmentData\"\n            [editable]=\"false\"\n            (createOrEditAlias)=\"openAliasDialog($event)\"\n            (removeAlias)=\"removeAlias($event)\"\n            (removeComponent)=\"removeComponent($event)\"\n            class=\"w-full overflow-auto shadow\" gdColumn=\"1 / span 2\"\n            gdColumn.lt-md=\"1 / -1\"\n            gdColumn.lt-sm=\"1\"></request-data-table> -->\n\n          <!-- Method -->\n          <div class=\"border-b py-4 px-6 flex-container\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n            <h2 class=\"m-0 title\" fxFlex=\"auto\">Method</h2>\n\n            <button (click)=\"openEditResponseLatencyDialog()\" mat-icon-button type=\"button\">\n              <mat-icon [icIcon]=\"icons.icEdit\" class=\"text-secondary\"></mat-icon>\n            </button>\n          </div>\n\n          <div class=\"px-6 py-3\">\n            {{ request.method }}\n          </div>\n\n          <!-- URL -->\n          <div class=\"border-b py-4 px-6 flex-container\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n            <h2 class=\"m-0 title\" fxFlex=\"auto\">URL</h2>\n\n            <button (click)=\"openEditResponseLatencyDialog()\" mat-icon-button type=\"button\">\n              <mat-icon [icIcon]=\"icons.icEdit\" class=\"text-secondary\"></mat-icon>\n            </button>\n          </div>\n\n          <div class=\"px-6 py-3\">\n            {{ request.url }}\n          </div>\n        </div>\n      </mat-tab>\n\n      <mat-tab label=\"Query Params\">\n        <div class=\"p-3\">\n          <request-data-table\n            [componentType]=\"componentTypes.QueryParam\"\n            [title]=\"queryParamTitle\"\n            [columns]=\"queryParamColumns\"\n            [data]=\"queryParamData\"\n            (createComponent)=\"openCreateComponentDialog($event)\"\n            (createOrEditAlias)=\"openAliasDialog($event)\"\n            (editComponent)=\"openEditComponentDialog($event)\"\n            (removeAlias)=\"removeAlias($event)\"\n            (removeComponent)=\"removeComponent($event)\"\n            class=\"w-full overflow-auto shadow\" gdColumn=\"3 / span 2\"\n            gdColumn.lt-md=\"1 / -1\"\n            gdColumn.lt-sm=\"1\"></request-data-table>\n\n        </div>\n      </mat-tab>\n\n      <mat-tab label=\"Headers\">\n        <div class=\"p-3\">\n          <request-data-table\n            [componentType]=\"componentTypes.Header\"\n            [title]=\"headerTitle\"\n            [columns]=\"headerColumns\"\n            [data]=\"headerData\"\n            (createComponent)=\"openCreateComponentDialog($event)\"\n            (createOrEditAlias)=\"openAliasDialog($event)\"\n            (editComponent)=\"openEditComponentDialog($event)\"\n            (removeAlias)=\"removeAlias($event)\"\n            (removeComponent)=\"removeComponent($event)\"\n            class=\"w-full overflow-auto shadow\" gdColumn=\"1 / span 2\"\n            gdColumn.lt-md=\"1 / -1\"\n            gdColumn.lt-sm=\"1\"></request-data-table>\n        </div>\n      </mat-tab>\n\n      <mat-tab label=\"Body Params\">\n        <div class=\"p-3\">\n          <request-data-table\n            [componentType]=\"componentTypes.BodyParam\"\n            [title]=\"bodyParamTitle\"\n            [columns]=\"bodyParamColumns\"\n            [data]=\"bodyParamData\"\n            (createComponent)=\"openCreateComponentDialog($event)\"\n            (createOrEditAlias)=\"openAliasDialog($event)\"\n            (editComponent)=\"openEditComponentDialog($event)\"\n            (removeAlias)=\"removeAlias($event)\"\n            (removeComponent)=\"removeComponent($event)\"\n            class=\"w-full overflow-auto shadow\" gdColumn=\"1 / span 2\"\n            gdColumn.lt-md=\"1 / -1\"\n            gdColumn.lt-sm=\"1\"></request-data-table>\n\n        </div>\n      </mat-tab>\n    </mat-tab-group>\n  </div>\n</vex-page-layout-content>\n\n<ng-template #editResponseMoreActions>\n  <button \n    *ngIf=\"layoutConfigService.isProxied()\"\n    (click)=\"sendRequest()\" \n    class=\"mr-3\"\n    color=\"primary\" \n    mat-raised-button type=\"button\"\n    >\n    REPLAY\n  </button>\n</ng-template>");

/***/ }),

/***/ "fHeU":
/*!***************************************************!*\
  !*** ./src/app/core/utils/json-search.service.ts ***!
  \***************************************************/
/*! exports provided: JsonSearch */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "JsonSearch", function() { return JsonSearch; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");


let JsonSearch = class JsonSearch {
    constructor() { }
    search(data, query) {
        const res = [];
        this.searchHelper(data, query.split('.'), res);
        return res;
    }
    searchHelper(data, query, res) {
        if (!query.length) {
            return;
        }
        if (typeof data !== 'object') {
            return;
        }
        // Jump over arrays
        if (Array.isArray(data)) {
            for (const ele of data) {
                const clone = query.slice(0);
                this.searchHelper(ele, clone, res);
            }
        }
        else {
            data = data[query[0]];
            if (query.length === 1) {
                res.push(data);
            }
            query.pop();
            this.searchHelper(data, query, res);
        }
    }
};
JsonSearch.ctorParameters = () => [];
JsonSearch = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], JsonSearch);



/***/ }),

/***/ "g6n5":
/*!*************************************************************************************!*\
  !*** ./src/app/modules/requests/pages/request-details/request-details.component.ts ***!
  \*************************************************************************************/
/*! exports provided: RequestDetailsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RequestDetailsComponent", function() { return RequestDetailsComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_request_details_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./request-details.component.html */ "csGO");
/* harmony import */ var _request_details_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./request-details.component.scss */ "hQO2");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/dialog */ "iELJ");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _aliases_components_aliases_create_aliases_create_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @aliases/components/aliases-create/aliases-create.component */ "tedC");
/* harmony import */ var _core_http__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @core/http */ "vAmI");
/* harmony import */ var _data_schema__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @data/schema */ "V99k");
/* harmony import */ var _layout_services_layout_config_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @layout/services/layout-config.service */ "U9Lm");
/* harmony import */ var _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @projects/services/project-data.service */ "oyjd");
/* harmony import */ var _shared_components_modal__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @shared/components/modal */ "+V3c");
/* harmony import */ var _services_request_details_icons_service__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./services/request-details-icons.service */ "rBbm");













let RequestDetailsComponent = class RequestDetailsComponent {
    constructor(icons, layoutConfigService, aliasResource, bodyParamResource, dialog, headerResource, agentService, projectDataService, queryParamResource, requestResource, responseResource, responseHeaderResource, route) {
        this.icons = icons;
        this.layoutConfigService = layoutConfigService;
        this.aliasResource = aliasResource;
        this.bodyParamResource = bodyParamResource;
        this.dialog = dialog;
        this.headerResource = headerResource;
        this.agentService = agentService;
        this.projectDataService = projectDataService;
        this.queryParamResource = queryParamResource;
        this.requestResource = requestResource;
        this.responseResource = responseResource;
        this.responseHeaderResource = responseHeaderResource;
        this.route = route;
        this.queryParamTitle = 'Query Params';
        this.queryParamData = [];
        this.headerTitle = 'Headers';
        this.headerData = [];
        this.bodyParamTitle = 'Body Params';
        this.bodyParamData = [];
        this.responseTitle = 'Response';
        this.responseHeaderTitle = 'Headers';
        this.responseHeaderData = [];
        this.renderPrettyResponse = true;
        this.componentTypes = _data_schema__WEBPACK_IMPORTED_MODULE_8__["RequestComponentType"];
        this.crumbs = [];
    }
    ngOnInit() {
        const snapshot = this.route.snapshot;
        this.projectId = snapshot.queryParams.project_id;
        this.request = new _data_schema__WEBPACK_IMPORTED_MODULE_8__["Request"](snapshot.data.request);
        this.buildCrumbs(snapshot);
        this.responseHeaderData = snapshot.data.responseHeaders.map(responseHeader => {
            return new _data_schema__WEBPACK_IMPORTED_MODULE_8__["ResponseHeader"](responseHeader);
        });
        this.responseData = snapshot.data.response.map(response => {
            try {
                const text = JSON.stringify(JSON.parse(response.text), null, 2);
                response.text = text;
            }
            catch (err) {
                response.isJson = false;
            }
            return new _data_schema__WEBPACK_IMPORTED_MODULE_8__["Response"](response);
        })[0];
        this.headerColumns = this.buildTableColumns(true);
        this.queryParamColumns = this.buildTableColumns(true);
        this.bodyParamColumns = this.buildTableColumns(true);
        this.responseHeaderColumns = this.buildTableColumns(false);
    }
    // API Access
    createOrEditAlias(component, aliasName) {
        const snapshot = this.route.snapshot;
        if (!component.alias) {
            this.aliasResource.create({
                component_id: component.id,
                component_type: component.type,
                name: aliasName,
                project_id: this.projectId,
            }).subscribe((res) => {
                component.alias = res;
                component.aliasName = res.name;
            });
        }
        else {
            this.aliasResource.update(component.alias.id, {
                name: aliasName,
                project_id: this.projectId,
            }).subscribe(res => {
                component.alias.name = aliasName;
            });
        }
    }
    removeAlias(component) {
        const snapshot = this.route.snapshot;
        this.aliasResource.destroy(component.alias.id, {
            project_id: this.projectId,
            component_id: component.id,
            component_type: component.type,
        }).subscribe(res => {
            component.alias = null;
            component.aliasName = undefined;
        });
    }
    createComponent(component, componentType) {
        const resource = this.componentTypeToResource(componentType);
        if (resource) {
            component.project_id = this.projectId;
            resource.create(this.request.id, component).subscribe(res => {
                const componentData = this.componentTypeToData(componentType);
                const clone = componentData.slice();
                switch (componentType) {
                    case _data_schema__WEBPACK_IMPORTED_MODULE_8__["RequestComponentType"].Header:
                        clone.unshift(new _data_schema__WEBPACK_IMPORTED_MODULE_8__["Header"](res));
                        this.headerData = clone;
                        break;
                    case _data_schema__WEBPACK_IMPORTED_MODULE_8__["RequestComponentType"].QueryParam:
                        clone.unshift(new _data_schema__WEBPACK_IMPORTED_MODULE_8__["QueryParam"](res));
                        this.queryParamData = clone;
                        break;
                    case _data_schema__WEBPACK_IMPORTED_MODULE_8__["RequestComponentType"].BodyParam:
                        clone.unshift(new _data_schema__WEBPACK_IMPORTED_MODULE_8__["BodyParam"](res));
                        this.bodyParamData = clone;
                        break;
                }
            });
        }
    }
    updateComponent(component, componentType) {
        const resource = this.componentTypeToResource(componentType);
        if (resource) {
            component.project_id = this.projectId;
            resource.update(this.request.id, component.id, component).subscribe(res => {
                const componentData = this.componentTypeToData(componentType);
                if (componentType === _data_schema__WEBPACK_IMPORTED_MODULE_8__["RequestComponentType"].Response) {
                    this.responseData.text = res.text;
                }
                else {
                    const clone = componentData.slice();
                    clone.forEach((data, i) => {
                        if (data.id === component.id) {
                            clone[i] = res;
                        }
                    });
                    this.updateComponentData(clone, componentType);
                }
            });
        }
    }
    removeComponent(component) {
        const resource = this.componentTypeToResource(component.type);
        if (resource) {
            const queryParams = { project_id: this.projectId };
            resource.destroy(this.request.id, component.id, queryParams).subscribe(res => {
                const componentData = this.componentTypeToData(component.type);
                const clone = componentData.filter((c) => {
                    return c.id !== component.id;
                });
                this.updateComponentData(clone, component.type);
            });
        }
    }
    // View Access
    openAliasDialog(component) {
        const dialogRef = this.dialog.open(_aliases_components_aliases_create_aliases_create_component__WEBPACK_IMPORTED_MODULE_6__["AliasesCreateComponent"], {
            width: '600px',
            data: component || {},
        });
        const onCreateSub = dialogRef.componentInstance.onCreate.subscribe(($event) => {
            const snapshot = this.route.snapshot;
            const request_id = snapshot.params.request_id;
            this.createOrEditAlias(component, $event.name);
        });
        dialogRef.afterClosed().subscribe(() => {
            onCreateSub.unsubscribe();
        });
    }
    /**
     *
     * @param {RequestComponentType} componentType enum value representing component type
     *
     */
    openCreateComponentDialog(componentType) {
        const dialogRef = this.dialog.open(_shared_components_modal__WEBPACK_IMPORTED_MODULE_11__["CreateModalComponent"], {
            width: '600px',
            data: this.buildComponentFields(componentType),
        });
        const onCreateSub = dialogRef.componentInstance.onCreate.subscribe((component) => {
            this.createComponent(component, componentType);
        });
        dialogRef.afterClosed().subscribe(() => {
            onCreateSub.unsubscribe();
        });
    }
    /**
     *
     * @param {RequestComponentType} componentType enum value representing component type
     *
     */
    openEditComponentDialog(component, moreActions) {
        const data = this.buildComponentFields(component.type);
        data.data = component;
        const dialogRef = this.dialog.open(_shared_components_modal__WEBPACK_IMPORTED_MODULE_11__["EditModalComponent"], {
            data,
            width: '750px',
        });
        if (moreActions) {
            const instance = dialogRef.componentInstance;
            instance.moreActions = moreActions;
        }
        const onCreateSub = dialogRef.componentInstance.onEdit.subscribe((updatedComponent) => {
            updatedComponent.id = component.id;
            this.updateComponent(updatedComponent, component.type);
        });
        dialogRef.afterClosed().subscribe(() => {
            onCreateSub.unsubscribe();
        });
    }
    openEditResponseLatencyDialog() {
        const data = {
            title: 'Latency',
            fields: [
                {
                    id: 'latency',
                    label: 'Latency (ms)',
                    type: 'input',
                },
            ],
        };
        data.data = this.request;
        const dialogRef = this.dialog.open(_shared_components_modal__WEBPACK_IMPORTED_MODULE_11__["EditModalComponent"], {
            width: '600px',
            data,
        });
        const onCreateSub = dialogRef.componentInstance.onEdit.subscribe((updatedRequest) => {
            this.requestResource.update(this.request.id, { latency: updatedRequest.latency }).subscribe(res => {
                this.request.latency = updatedRequest.latency;
            });
        });
        dialogRef.afterClosed().subscribe(() => {
            onCreateSub.unsubscribe();
        });
    }
    handleTabChange($event) {
        const defaultQueryParams = { project_id: this.request.projectId };
        switch ($event.tab.textLabel) {
            case this.headerTitle:
                this.headerResource.index(this.request.id, defaultQueryParams).subscribe((res) => {
                    this.headerData = res.map(header => {
                        return new _data_schema__WEBPACK_IMPORTED_MODULE_8__["Header"](header);
                    });
                });
                break;
            case this.queryParamTitle:
                this.queryParamResource.index(this.request.id, defaultQueryParams).subscribe((res) => {
                    this.queryParamData = res.map(queryParam => {
                        return new _data_schema__WEBPACK_IMPORTED_MODULE_8__["QueryParam"](queryParam);
                    });
                });
                break;
            case this.bodyParamTitle:
                this.bodyParamResource.index(this.request.id, defaultQueryParams).subscribe((res) => {
                    this.bodyParamData = res.map(bodyParam => {
                        return new _data_schema__WEBPACK_IMPORTED_MODULE_8__["BodyParam"](bodyParam);
                    });
                });
                break;
            case this.responseTitle:
                break;
        }
    }
    sendRequest() {
        const defaultQueryParams = { project_id: this.request.projectId };
        const headers = {};
        this.requestResource.show(this.request.id, {
            headers: 1,
            queryParams: 1,
        }).subscribe((res) => {
            this.agentService.sendRequest(new _data_schema__WEBPACK_IMPORTED_MODULE_8__["Request"](res)).subscribe(res => {
                console.log(res);
            });
        });
    }
    toggleRenderPrettyResponse(event) {
        this.renderPrettyResponse = !this.renderPrettyResponse;
    }
    // Helpers
    buildCrumbs(snapshot) {
        if (this.projectDataService.project) {
            this.crumbs.push({
                name: this.projectDataService.project.name,
            });
        }
        else {
            const o = this.projectDataService.project$.subscribe((project) => {
                if (project) {
                    this.crumbs.unshift({
                        name: project.name,
                    });
                    o.unsubscribe();
                }
            });
            this.projectDataService.fetch(this.projectId);
        }
        const pathSegments = location.pathname.split('/');
        pathSegments.shift(); // Get rid of empty first element
        this.crumbs.push({
            name: this.capitalize(pathSegments[0]),
            routerLink: ['/' + pathSegments[0]],
            queryParams: snapshot.queryParams,
        });
        // If referer URL was /endpoints or /requests
        if (pathSegments.length > 2) {
            this.addParentResourcePath(pathSegments);
        }
        this.crumbs.push({
            name: this.request.url,
        });
    }
    singularize(s) {
        if (s[s.length - 1] !== 's') {
            return s;
        }
        return s.substring(0, s.length - 1);
    }
    capitalize(s) {
        return s.charAt(0).toUpperCase() + s.slice(1);
    }
    addParentResourcePath(pathSegments) {
        const snapshot = this.route.snapshot;
        const parentResource = snapshot.data.parentResource;
        const routerLink = pathSegments.slice(0, pathSegments.length / 2).join('/');
        this.crumbs.push({
            name: parentResource.name || parentResource.path,
            routerLink: ['/' + routerLink],
            queryParams: this.route.snapshot.queryParams,
        });
    }
    componentTypeToResource(componentType) {
        let resource;
        switch (componentType) {
            case _data_schema__WEBPACK_IMPORTED_MODULE_8__["RequestComponentType"].Header:
                resource = this.headerResource;
                break;
            case _data_schema__WEBPACK_IMPORTED_MODULE_8__["RequestComponentType"].QueryParam:
                resource = this.queryParamResource;
                break;
            case _data_schema__WEBPACK_IMPORTED_MODULE_8__["RequestComponentType"].BodyParam:
                resource = this.bodyParamResource;
                break;
            case _data_schema__WEBPACK_IMPORTED_MODULE_8__["RequestComponentType"].Response:
                resource = this.responseResource;
                break;
            case _data_schema__WEBPACK_IMPORTED_MODULE_8__["RequestComponentType"].ResponseHeader:
                resource = this.responseHeaderResource;
                break;
        }
        return resource;
    }
    componentTypeToData(componentType) {
        let resource;
        switch (componentType) {
            case _data_schema__WEBPACK_IMPORTED_MODULE_8__["RequestComponentType"].Header:
                return this.headerData;
                break;
            case _data_schema__WEBPACK_IMPORTED_MODULE_8__["RequestComponentType"].QueryParam:
                return this.queryParamData;
                break;
            case _data_schema__WEBPACK_IMPORTED_MODULE_8__["RequestComponentType"].BodyParam:
                return this.bodyParamData;
                break;
            case _data_schema__WEBPACK_IMPORTED_MODULE_8__["RequestComponentType"].Response:
                return this.responseData;
                break;
            case _data_schema__WEBPACK_IMPORTED_MODULE_8__["RequestComponentType"].ResponseHeader:
                return this.responseHeaderData;
                break;
        }
        return resource;
    }
    buildComponentFields(componentType) {
        let title = '';
        switch (componentType) {
            case _data_schema__WEBPACK_IMPORTED_MODULE_8__["RequestComponentType"].Header:
                title = 'Request Header';
                break;
            case _data_schema__WEBPACK_IMPORTED_MODULE_8__["RequestComponentType"].QueryParam:
                title = 'Query Param';
                break;
            case _data_schema__WEBPACK_IMPORTED_MODULE_8__["RequestComponentType"].BodyParam:
                title = 'Body Param';
                break;
            case _data_schema__WEBPACK_IMPORTED_MODULE_8__["RequestComponentType"].Response:
                title = 'Response';
                return {
                    title,
                    fields: [
                        {
                            id: 'text',
                            label: 'Body',
                            type: 'textarea',
                        },
                    ],
                };
                break;
            case _data_schema__WEBPACK_IMPORTED_MODULE_8__["RequestComponentType"].ResponseHeader:
                title = 'Response Heaer';
                break;
        }
        return {
            title,
            fields: [
                {
                    id: 'name',
                    label: 'Name',
                    type: 'input',
                },
                {
                    id: 'value',
                    label: 'Value',
                    rows: 3,
                    type: 'textarea',
                },
            ],
        };
    }
    updateComponentData(clone, componentType) {
        switch (componentType) {
            case _data_schema__WEBPACK_IMPORTED_MODULE_8__["RequestComponentType"].Header:
                this.headerData = clone;
                break;
            case _data_schema__WEBPACK_IMPORTED_MODULE_8__["RequestComponentType"].QueryParam:
                this.queryParamData = clone;
                break;
            case _data_schema__WEBPACK_IMPORTED_MODULE_8__["RequestComponentType"].BodyParam:
                this.bodyParamData = clone;
                break;
            case _data_schema__WEBPACK_IMPORTED_MODULE_8__["RequestComponentType"].ResponseHeader:
                this.responseHeaderData = clone;
                break;
        }
    }
    buildTableColumns(canAlias) {
        if (canAlias) {
            return [
                { label: 'NAME', property: 'name', type: 'text' },
                // { label: '', property: 'link-button', type: 'button', visible: true },
                { label: 'ALIAS', property: 'aliasName', type: 'custom', visible: true },
                { label: 'VALUE', property: 'value', type: 'text' },
                { label: '', property: 'edit', type: 'custom', visible: true },
            ];
        }
        else {
            return [
                { label: 'NAME', property: 'name', type: 'text' },
                { label: 'VALUE', property: 'value', type: 'text' },
                { label: '', property: 'edit', type: 'custom', visible: true },
            ];
        }
    }
};
RequestDetailsComponent.ctorParameters = () => [
    { type: _services_request_details_icons_service__WEBPACK_IMPORTED_MODULE_12__["RequestDetailsIcons"] },
    { type: _layout_services_layout_config_service__WEBPACK_IMPORTED_MODULE_9__["LayoutConfigService"] },
    { type: _core_http__WEBPACK_IMPORTED_MODULE_7__["AliasResource"] },
    { type: _core_http__WEBPACK_IMPORTED_MODULE_7__["BodyParamResource"] },
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_4__["MatDialog"] },
    { type: _core_http__WEBPACK_IMPORTED_MODULE_7__["HeaderResource"] },
    { type: _core_http__WEBPACK_IMPORTED_MODULE_7__["AgentService"] },
    { type: _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_10__["ProjectDataService"] },
    { type: _core_http__WEBPACK_IMPORTED_MODULE_7__["QueryParamResource"] },
    { type: _core_http__WEBPACK_IMPORTED_MODULE_7__["RequestResource"] },
    { type: _core_http__WEBPACK_IMPORTED_MODULE_7__["ResponseResource"] },
    { type: _core_http__WEBPACK_IMPORTED_MODULE_7__["ResponseHeaderResource"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_5__["ActivatedRoute"] }
];
RequestDetailsComponent.propDecorators = {
    template: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ViewChild"], args: ['editResponseMoreActions',] }]
};
RequestDetailsComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'request-details',
        template: _raw_loader_request_details_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_request_details_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], RequestDetailsComponent);



/***/ }),

/***/ "h+Y6":
/*!********************************************************!*\
  !*** ./node_modules/@iconify/icons-ic/twotone-link.js ***!
  \********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

var data = {
	"body": "<path d=\"M17 7h-4v2h4c1.65 0 3 1.35 3 3s-1.35 3-3 3h-4v2h4c2.76 0 5-2.24 5-5s-2.24-5-5-5zm-6 8H7c-1.65 0-3-1.35-3-3s1.35-3 3-3h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-2zm-3-4h8v2H8z\" fill=\"currentColor\"/>",
	"width": 24,
	"height": 24
};
exports.__esModule = true;
exports.default = data;


/***/ }),

/***/ "h8gq":
/*!************************************************************************!*\
  !*** ./src/app/modules/requests/services/response-resolver.service.ts ***!
  \************************************************************************/
/*! exports provided: ResponseResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ResponseResolver", function() { return ResponseResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _core_http_response_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @core/http/response-resource.service */ "z06h");



let ResponseResolver = class ResponseResolver {
    constructor(responseResource) {
        this.responseResource = responseResource;
    }
    resolve(route) {
        return this.responseResource.index(route.params.request_id, { project_id: route.queryParams.project_id });
    }
};
ResponseResolver.ctorParameters = () => [
    { type: _core_http_response_resource_service__WEBPACK_IMPORTED_MODULE_2__["ResponseResource"] }
];
ResponseResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], ResponseResolver);



/***/ }),

/***/ "hQO2":
/*!***************************************************************************************!*\
  !*** ./src/app/modules/requests/pages/request-details/request-details.component.scss ***!
  \***************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (".response-text {\n  max-height: 350px;\n  overflow-y: auto;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uLy4uL3JlcXVlc3QtZGV0YWlscy5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLGlCQUFBO0VBQ0EsZ0JBQUE7QUFDRiIsImZpbGUiOiJyZXF1ZXN0LWRldGFpbHMuY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyIucmVzcG9uc2UtdGV4dCB7XG4gIG1heC1oZWlnaHQ6IDM1MHB4O1xuICBvdmVyZmxvdy15OiBhdXRvO1xufSJdfQ== */");

/***/ }),

/***/ "iSh1":
/*!**************************************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/requests/pages/request-details/components/request-data-table/request-data-table.component.html ***!
  \**************************************************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div class=\"overflow-auto w-full\" fxLayout=\"column\">\n  <div class=\"border-b py-4 px-6\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n    <h2 class=\"m-0 title\" fxFlex=\"auto\">{{ title }}</h2>\n\n    <ng-container *ngIf=\"editable\">\n      <button (click)=\"createComponent.emit(componentType)\" mat-icon-button type=\"button\">\n        <mat-icon [icIcon]=\"icAdd\" class=\"text-secondary\"></mat-icon>\n      </button>\n    </ng-container>\n\n    <!-- <button mat-icon-button type=\"button\">\n      <mat-icon [icIcon]=\"icMoreHoriz\" class=\"text-secondary\"></mat-icon>\n    </button> -->\n  </div>\n\n  <table [dataSource]=\"dataSource\" class=\"w-full overflow-auto\" mat-table matSort>\n\n    <!--- Note that these columns can be defined in any order.\n          The actual rendered columns are set as a property on the row definition\" -->\n\n    <!-- Model Properties Column -->\n    <ng-container *ngFor=\"let column of columns\">\n      <ng-container *ngIf=\"column.type === 'text'\" [matColumnDef]=\"column.property\">\n        <th *matHeaderCellDef mat-header-cell mat-sort-header> {{ column.label }}</th>\n        <td *matCellDef=\"let row\" [ngClass]=\"column.cssClasses\" mat-cell>\n          <pre class=\"pt-3\" *ngIf=\"shouldRenderPre(row[column.property]); else templateName\">\n            {{ row[column.property] }}\n          </pre>\n\n          <ng-template #templateName>\n            {{ renderText(row[column.property]) }}\n          </ng-template>\n        </td>\n      </ng-container>\n\n      <ng-container *ngIf=\"column.type === 'badge'\" [matColumnDef]=\"column.property\">\n        <th *matHeaderCellDef mat-header-cell mat-sort-header> {{ column.label }}</th>\n        <td *matCellDef=\"let row\" [ngClass]=\"column.cssClasses\" mat-cell>\n          <div *ngIf=\"row[column.property] === 'ready'\"\n               class=\"w-3 h-3 rounded-full bg-green-500 cursor-pointer\"\n               matTooltip=\"Ready to ship\"></div>\n          <div *ngIf=\"row[column.property] === 'pending'\"\n               class=\"w-3 h-3 rounded-full bg-orange-500 cursor-pointer\"\n               matTooltip=\"Pending Payment\"></div>\n          <div *ngIf=\"row[column.property] === 'warn'\"\n               class=\"w-3 h-3 rounded-full bg-red-500 cursor-pointer\"\n               matTooltip=\"Missing Payment\"></div>\n        </td>\n      </ng-container>\n\n      <ng-container *ngIf=\"column.property === 'aliasName'\" [matColumnDef]=\"column.property\">\n        <th *matHeaderCellDef mat-header-cell mat-sort-header>{{ column.label }}</th>\n        <td *matCellDef=\"let row\" mat-cell>\n          <div class=\"flex\">\n            <ng-container *ngIf=\"!row.alias\">\n              <a (click)=\"createOrEditAlias.emit(row)\"\n                 [style.background-color]=\"theme.colors.green['500'] | colorFade:0.9\"\n                 [style.color]=\"theme.colors.green['500']\"\n                 class=\"w-8 h-8 leading-none flex items-center justify-center hover:bg-hover\"\n                 mat-icon-button\n              >\n                <mat-icon [icIcon]=\"icLink\" size=\"18px\"></mat-icon>\n              </a>\n            </ng-container>\n            <ng-container *ngIf=\"row.alias\">\n              <a (click)=\"createOrEditAlias.emit(row)\"\n                 [style.background-color]=\"theme.colors.cyan['500'] | colorFade:0.9\"\n                 [style.color]=\"theme.colors.cyan['500']\"\n                 class=\"w-8 h-8 leading-none items-center justify-center hover:bg-hover flex\"\n                 mat-icon-button\n              >\n                <mat-icon [icIcon]=\"icCreate\" size=\"18px\"></mat-icon>\n              </a>\n              <a (click)=\"removeAlias.emit(row)\"\n                 [style.background-color]=\"theme.colors.gray['700'] | colorFade:0.9\"\n                 [style.color]=\"theme.colors.gray['700']\"\n                 class=\"ml-2 w-8 h-8 leading-none items-center justify-center hover:bg-hover flex\"\n                 mat-icon-button\n              >\n                <mat-icon [icIcon]=\"icDelete\" size=\"18px\"></mat-icon>\n              </a>\n            </ng-container>\n            <span class=\"ml-3 mt-2 leading-none items-center justify-center\">\n              {{ row[column.property] === undefined ? 'N/A' : row[column.property] }}\n            </span>\n          </div>\n        </td>\n      </ng-container>\n    </ng-container>\n\n    <ng-container matColumnDef=\"edit\">\n      <th *matHeaderCellDef mat-header-cell></th>\n      <td *matCellDef=\"let row\" mat-cell>\n        <div class=\"flex\">\n          <a (click)=\"editComponent.emit(row)\"\n             [style.background-color]=\"theme.colors.gray['500'] | colorFade:0.9\"\n             [style.color]=\"theme.colors.gray['500']\"\n             class=\"ml-auto w-8 h-8 leading-none flex items-center justify-center hover:bg-hover\"\n             mat-icon-button>\n            <mat-icon [icIcon]=\"icEdit\" size=\"18px\"></mat-icon>\n          </a>\n          <a (click)=\"removeComponent.emit(row)\"\n             [style.background-color]=\"theme.colors.red['500'] | colorFade:0.9\"\n             [style.color]=\"theme.colors.red['500']\"\n             class=\"ml-3 w-8 h-8 leading-none flex items-center justify-center hover:bg-hover\"\n             mat-icon-button>\n            <mat-icon [icIcon]=\"icClose\" size=\"18px\"></mat-icon>\n          </a>\n        </div>\n      </td>\n    </ng-container>\n\n    <tr *matHeaderRowDef=\"visibleColumns\" mat-header-row></tr>\n    <!--suppress UnnecessaryLabelJS -->\n    <tr *matRowDef=\"let row; columns: visibleColumns;\" mat-row></tr>\n  </table>\n\n  <mat-paginator [pageSize]=\"pageSize\" class=\"paginator\"></mat-paginator>\n\n</div>\n");

/***/ }),

/***/ "iphE":
/*!*********************************************************!*\
  !*** ./src/app/shared/components/modal/modal.module.ts ***!
  \*********************************************************/
/*! exports provided: ModalModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ModalModule", function() { return ModalModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ "s7LF");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/form-field */ "Q2Ze");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/input */ "e6WT");
/* harmony import */ var _create_modal_create_modal_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./create-modal/create-modal.component */ "2yMs");
/* harmony import */ var _edit_modal_edit_modal_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./edit-modal/edit-modal.component */ "ZyFB");










let ModalModule = class ModalModule {
};
ModalModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_create_modal_create_modal_component__WEBPACK_IMPORTED_MODULE_8__["CreateModalComponent"], _edit_modal_edit_modal_component__WEBPACK_IMPORTED_MODULE_9__["EditModalComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"],
            _angular_material_input__WEBPACK_IMPORTED_MODULE_7__["MatInputModule"],
            _angular_material_form_field__WEBPACK_IMPORTED_MODULE_6__["MatFormFieldModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_5__["MatButtonModule"],
        ],
        exports: [_create_modal_create_modal_component__WEBPACK_IMPORTED_MODULE_8__["CreateModalComponent"], _edit_modal_edit_modal_component__WEBPACK_IMPORTED_MODULE_9__["EditModalComponent"]],
        // In the case of a dynamically loaded component and in order for a ComponentFactory to be generated,
        // the component must also be added to the module’s entryComponents:
        entryComponents: [_create_modal_create_modal_component__WEBPACK_IMPORTED_MODULE_8__["CreateModalComponent"], _edit_modal_edit_modal_component__WEBPACK_IMPORTED_MODULE_9__["EditModalComponent"]],
    })
], ModalModule);



/***/ }),

/***/ "n0rh":
/*!*******************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/aliases/components/aliases-create/aliases-create.component.html ***!
  \*******************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<form (ngSubmit)=\"create()\" [formGroup]=\"form\">\r\n  <div fxLayout=\"row\" fxLayoutAlign=\"start center\" mat-dialog-title>\r\n\r\n    <h2 class=\"headline m-0\" fxFlex=\"auto\">Set Alias</h2>\r\n<!--\r\n    <button [matMenuTriggerFor]=\"settingsMenu\" class=\"text-secondary\" mat-icon-button type=\"button\">\r\n      <mat-icon [icIcon]=\"icMoreVert\"></mat-icon>\r\n    </button>\r\n-->\r\n    <button class=\"text-secondary\" mat-dialog-close mat-icon-button type=\"button\">\r\n      <mat-icon [icIcon]=\"icClose\"></mat-icon>\r\n    </button>\r\n  </div>\r\n\r\n  <mat-divider class=\"-mx-6 text-border\"></mat-divider>\r\n\r\n  <mat-dialog-content fxLayout=\"column\">\r\n    <mat-form-field class=\"mt-6\">\r\n      <mat-label>Name</mat-label>\r\n      <input cdkFocusInitial formControlName=\"name\" matInput>\r\n\r\n      <mat-icon [icIcon]=\"icPerson\" class=\"ltr:mr-3 rtl:ml-3\" matPrefix></mat-icon>\r\n    </mat-form-field>\r\n  </mat-dialog-content>\r\n\r\n  <mat-dialog-actions align=\"end\">\r\n    <button mat-button mat-dialog-close type=\"button\">CANCEL</button>\r\n    <button color=\"primary\" mat-button type=\"submit\">SUBMIT</button>\r\n  </mat-dialog-actions>\r\n</form>\r\n\r\n<mat-menu #settingsMenu=\"matMenu\" xPosition=\"before\" yPosition=\"below\">\r\n  <button mat-menu-item>\r\n    <mat-icon [icIcon]=\"icPrint\"></mat-icon>\r\n    <span>Print</span>\r\n  </button>\r\n\r\n  <button mat-menu-item>\r\n    <mat-icon [icIcon]=\"icDownload\"></mat-icon>\r\n    <span>Export</span>\r\n  </button>\r\n\r\n  <button mat-menu-item>\r\n    <mat-icon [icIcon]=\"icDelete\"></mat-icon>\r\n    <span>Delete</span>\r\n  </button>\r\n</mat-menu>\r\n");

/***/ }),

/***/ "ote9":
/*!*****************************************************************************************************************************!*\
  !*** ./src/app/modules/requests/pages/request-details/components/response-aliases-create/response-aliases-create.module.ts ***!
  \*****************************************************************************************************************************/
/*! exports provided: ResponseAliasesCreateModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ResponseAliasesCreateModule", function() { return ResponseAliasesCreateModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ "s7LF");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/input */ "e6WT");
/* harmony import */ var _response_aliases_create_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./response-aliases-create.component */ "TdxM");








let ResponseAliasesCreateModule = class ResponseAliasesCreateModule {
};
ResponseAliasesCreateModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_response_aliases_create_component__WEBPACK_IMPORTED_MODULE_7__["ResponseAliasesCreateComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"],
            _angular_material_input__WEBPACK_IMPORTED_MODULE_6__["MatInputModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_5__["MatButtonModule"],
        ],
        exports: [_response_aliases_create_component__WEBPACK_IMPORTED_MODULE_7__["ResponseAliasesCreateComponent"]],
    })
], ResponseAliasesCreateModule);



/***/ }),

/***/ "pN9m":
/*!********************************************************!*\
  !*** ./node_modules/@iconify/icons-ic/twotone-edit.js ***!
  \********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

var data = {
	"body": "<path opacity=\".3\" d=\"M5 18.08V19h.92l9.06-9.06l-.92-.92z\" fill=\"currentColor\"/><path d=\"M20.71 7.04a.996.996 0 0 0 0-1.41l-2.34-2.34c-.2-.2-.45-.29-.71-.29s-.51.1-.7.29l-1.83 1.83l3.75 3.75l1.83-1.83zM3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM5.92 19H5v-.92l9.06-9.06l.92.92L5.92 19z\" fill=\"currentColor\"/>",
	"width": 24,
	"height": 24
};
exports.__esModule = true;
exports.default = data;


/***/ }),

/***/ "qeIL":
/*!********************************************************************************!*\
  !*** ./src/app/modules/requests/services/response-headers-resolver.service.ts ***!
  \********************************************************************************/
/*! exports provided: ResponseHeadersResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ResponseHeadersResolver", function() { return ResponseHeadersResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _core_http_response_header_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @core/http/response-header-resource.service */ "n/pC");



let ResponseHeadersResolver = class ResponseHeadersResolver {
    constructor(responseHeaderResource) {
        this.responseHeaderResource = responseHeaderResource;
    }
    resolve(route) {
        return this.responseHeaderResource.index(route.params.request_id, { project_id: route.queryParams.project_id });
    }
};
ResponseHeadersResolver.ctorParameters = () => [
    { type: _core_http_response_header_resource_service__WEBPACK_IMPORTED_MODULE_2__["ResponseHeaderResource"] }
];
ResponseHeadersResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], ResponseHeadersResolver);



/***/ }),

/***/ "rBbm":
/*!**************************************************************************************************!*\
  !*** ./src/app/modules/requests/pages/request-details/services/request-details-icons.service.ts ***!
  \**************************************************************************************************/
/*! exports provided: RequestDetailsIcons */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RequestDetailsIcons", function() { return RequestDetailsIcons; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _iconify_icons_ic_twotone_cloud_off__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @iconify/icons-ic/twotone-cloud-off */ "DaE0");
/* harmony import */ var _iconify_icons_ic_twotone_cloud_off__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_cloud_off__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @iconify/icons-ic/twotone-edit */ "pN9m");
/* harmony import */ var _iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _iconify_icons_ic_twotone_group__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @iconify/icons-ic/twotone-group */ "Ell1");
/* harmony import */ var _iconify_icons_ic_twotone_group__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_group__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @iconify/icons-ic/twotone-more-vert */ "+Chm");
/* harmony import */ var _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _iconify_icons_ic_twotone_pageview__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @iconify/icons-ic/twotone-pageview */ "9Gk2");
/* harmony import */ var _iconify_icons_ic_twotone_pageview__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_pageview__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _iconify_icons_ic_twotone_timer__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @iconify/icons-ic/twotone-timer */ "De0L");
/* harmony import */ var _iconify_icons_ic_twotone_timer__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_timer__WEBPACK_IMPORTED_MODULE_7__);








let RequestDetailsIcons = class RequestDetailsIcons {
    constructor() {
        this.icGroup = _iconify_icons_ic_twotone_group__WEBPACK_IMPORTED_MODULE_4___default.a;
        this.icPageView = _iconify_icons_ic_twotone_pageview__WEBPACK_IMPORTED_MODULE_6___default.a;
        this.icCloudOff = _iconify_icons_ic_twotone_cloud_off__WEBPACK_IMPORTED_MODULE_2___default.a;
        this.icTimer = _iconify_icons_ic_twotone_timer__WEBPACK_IMPORTED_MODULE_7___default.a;
        this.icMoreVert = _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_5___default.a;
        this.icEdit = _iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_3___default.a;
    }
};
RequestDetailsIcons.ctorParameters = () => [];
RequestDetailsIcons = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])()
], RequestDetailsIcons);



/***/ }),

/***/ "tedC":
/*!***************************************************************************************!*\
  !*** ./src/app/modules/aliases/components/aliases-create/aliases-create.component.ts ***!
  \***************************************************************************************/
/*! exports provided: AliasesCreateComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AliasesCreateComponent", function() { return AliasesCreateComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_aliases_create_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./aliases-create.component.html */ "n0rh");
/* harmony import */ var _aliases_create_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./aliases-create.component.scss */ "bdKA");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ "s7LF");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/dialog */ "iELJ");
/* harmony import */ var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @iconify/icons-ic/twotone-close */ "5mnX");
/* harmony import */ var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @iconify/icons-ic/twotone-cloud-download */ "MzEE");
/* harmony import */ var _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @iconify/icons-ic/twotone-delete */ "e3EN");
/* harmony import */ var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _iconify_icons_ic_twotone_edit_location__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @iconify/icons-ic/twotone-edit-location */ "EPGw");
/* harmony import */ var _iconify_icons_ic_twotone_edit_location__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_edit_location__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _iconify_icons_ic_twotone_location_city__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @iconify/icons-ic/twotone-location-city */ "0I5b");
/* harmony import */ var _iconify_icons_ic_twotone_location_city__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_location_city__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @iconify/icons-ic/twotone-more-vert */ "+Chm");
/* harmony import */ var _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var _iconify_icons_ic_twotone_my_location__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @iconify/icons-ic/twotone-my-location */ "kSvQ");
/* harmony import */ var _iconify_icons_ic_twotone_my_location__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_my_location__WEBPACK_IMPORTED_MODULE_12__);
/* harmony import */ var _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @iconify/icons-ic/twotone-person */ "KaaH");
/* harmony import */ var _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_13___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_13__);
/* harmony import */ var _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @iconify/icons-ic/twotone-phone */ "YA1h");
/* harmony import */ var _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_14___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_14__);
/* harmony import */ var _iconify_icons_ic_twotone_print__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @iconify/icons-ic/twotone-print */ "yHIK");
/* harmony import */ var _iconify_icons_ic_twotone_print__WEBPACK_IMPORTED_MODULE_15___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_print__WEBPACK_IMPORTED_MODULE_15__);
















let AliasesCreateComponent = class AliasesCreateComponent {
    constructor(data, dialogRef, fb) {
        this.data = data;
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
    }
    ngOnInit() {
        this.form = this.fb.group({
            name: null,
        });
        this.form.patchValue(this.data.alias || {});
    }
    create() {
        const form = this.form.value;
        this.onCreate.emit(form);
        this.dialogRef.close();
    }
};
AliasesCreateComponent.ctorParameters = () => [
    { type: undefined, decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Inject"], args: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MAT_DIALOG_DATA"],] }] },
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MatDialogRef"] },
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormBuilder"] }
];
AliasesCreateComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'aliases-create',
        template: _raw_loader_aliases_create_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_aliases_create_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], AliasesCreateComponent);



/***/ })

}]);
//# sourceMappingURL=default~endpoints-endpoints-module~requests-requests-module~scenarios-scenarios-module-es2015.js.map