(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["projects-projects-module"],{

/***/ "+zwo":
/*!*******************************************************************************************************************************!*\
  !*** ./src/app/modules/projects/pages/project-details/components/project-members/services/projects-user-role-data.service.ts ***!
  \*******************************************************************************************************************************/
/*! exports provided: ProjectsUserRoleData */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectsUserRoleData", function() { return ProjectsUserRoleData; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _data_schema_projects_user__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @data/schema/projects-user */ "D9MS");



let ProjectsUserRoleData = class ProjectsUserRoleData {
    constructor() {
        this.roleTitlesMap = {};
        this.titleRolesMap = {};
        let titleKeys = Object.keys(_data_schema_projects_user__WEBPACK_IMPORTED_MODULE_2__["ProjectsUserRoleTitles"]);
        titleKeys = titleKeys.slice(titleKeys.length / 2);
        let roleKeys = Object.keys(_data_schema_projects_user__WEBPACK_IMPORTED_MODULE_2__["ProjectsUserRoles"]);
        roleKeys = roleKeys.slice(roleKeys.length / 2);
        roleKeys.forEach((value, index) => {
            this.roleTitlesMap[value] = titleKeys[index];
            this.titleRolesMap[titleKeys[index]] = value;
        });
        this.roleTitles = Object.values(this.roleTitlesMap);
    }
    getRoleTitle(role) {
        return this.roleTitlesMap[role];
    }
};
ProjectsUserRoleData.ctorParameters = () => [];
ProjectsUserRoleData = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], ProjectsUserRoleData);



/***/ }),

/***/ "2/D2":
/*!******************************************************************************************************************************************************!*\
  !*** ./src/app/modules/projects/pages/project-details/components/project-members/components/project-members-create/project-members-create.module.ts ***!
  \******************************************************************************************************************************************************/
/*! exports provided: ProjectMembersCreateModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectMembersCreateModule", function() { return ProjectMembersCreateModule; });
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
/* harmony import */ var _project_members_create_component__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ./project-members-create.component */ "5DOe");
















let ProjectMembersCreateModule = class ProjectMembersCreateModule {
};
ProjectMembersCreateModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
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
        declarations: [_project_members_create_component__WEBPACK_IMPORTED_MODULE_15__["ProjectMembersCreateComponent"]],
        entryComponents: [_project_members_create_component__WEBPACK_IMPORTED_MODULE_15__["ProjectMembersCreateComponent"]],
        exports: [_project_members_create_component__WEBPACK_IMPORTED_MODULE_15__["ProjectMembersCreateComponent"]],
    })
], ProjectMembersCreateModule);



/***/ }),

/***/ "3XCj":
/*!*************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/projects/pages/project-details/components/project-members/components/project-members-create/project-members-create.component.html ***!
  \*************************************************************************************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<form (ngSubmit)=\"create()\" [formGroup]=\"form\">\r\n  <div fxLayout=\"row\" fxLayoutAlign=\"start center\" mat-dialog-title>\r\n\r\n    <h2 class=\"headline m-0\" fxFlex=\"auto\">New Member</h2>\r\n<!--\r\n    <button [matMenuTriggerFor]=\"settingsMenu\" class=\"text-secondary\" mat-icon-button type=\"button\">\r\n      <mat-icon [icIcon]=\"icMoreVert\"></mat-icon>\r\n    </button>\r\n-->\r\n    <button class=\"text-secondary\" mat-dialog-close mat-icon-button type=\"button\">\r\n      <mat-icon [icIcon]=\"icClose\"></mat-icon>\r\n    </button>\r\n  </div>\r\n\r\n  <mat-divider class=\"-mx-6 text-border\"></mat-divider>\r\n  <mat-dialog-content fxLayout=\"column\">\r\n    <mat-form-field class=\"mt-6\">\r\n      <mat-label>Email</mat-label>\r\n      <input cdkFocusInitial formControlName=\"email\" matInput>\r\n\r\n      <mat-icon [icIcon]=\"icPerson\" class=\"ltr:mr-3 rtl:ml-3\" matPrefix></mat-icon>\r\n    </mat-form-field>\r\n  </mat-dialog-content>\r\n\r\n  <mat-dialog-actions align=\"end\">\r\n    <button mat-button mat-dialog-close type=\"button\">CANCEL</button>\r\n    <button color=\"primary\" mat-button type=\"submit\">ADD</button>\r\n  </mat-dialog-actions>\r\n</form>\r\n\r\n<mat-menu #settingsMenu=\"matMenu\" xPosition=\"before\" yPosition=\"below\">\r\n  <button mat-menu-item>\r\n    <mat-icon [icIcon]=\"icPrint\"></mat-icon>\r\n    <span>Print</span>\r\n  </button>\r\n\r\n  <button mat-menu-item>\r\n    <mat-icon [icIcon]=\"icDownload\"></mat-icon>\r\n    <span>Export</span>\r\n  </button>\r\n\r\n  <button mat-menu-item>\r\n    <mat-icon [icIcon]=\"icDelete\"></mat-icon>\r\n    <span>Delete</span>\r\n  </button>\r\n</mat-menu>\r\n");

/***/ }),

/***/ "5+Rn":
/*!***************************************************************************************!*\
  !*** ./src/app/modules/projects/components/projects-update/projects-update.module.ts ***!
  \***************************************************************************************/
/*! exports provided: ProjectsUpdateModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectsUpdateModule", function() { return ProjectsUpdateModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ "s7LF");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_material_core__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/core */ "UhP/");
/* harmony import */ var _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/datepicker */ "TN/R");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/material/dialog */ "iELJ");
/* harmony import */ var _angular_material_divider__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/material/divider */ "BSbQ");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @angular/material/input */ "e6WT");
/* harmony import */ var _angular_material_menu__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @angular/material/menu */ "rJgo");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _projects_update_component__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./projects-update.component */ "orsw");















let ProjectsUpdateModule = class ProjectsUpdateModule {
};
ProjectsUpdateModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_projects_update_component__WEBPACK_IMPORTED_MODULE_14__["ProjectsUpdateComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_material_dialog__WEBPACK_IMPORTED_MODULE_8__["MatDialogModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_10__["MatIconModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _angular_material_input__WEBPACK_IMPORTED_MODULE_11__["MatInputModule"],
            _angular_material_divider__WEBPACK_IMPORTED_MODULE_9__["MatDividerModule"],
            _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_7__["MatDatepickerModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_13__["IconModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"],
            _angular_material_menu__WEBPACK_IMPORTED_MODULE_12__["MatMenuModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_5__["MatButtonModule"],
            _angular_material_core__WEBPACK_IMPORTED_MODULE_6__["MatNativeDateModule"],
        ],
        entryComponents: [_projects_update_component__WEBPACK_IMPORTED_MODULE_14__["ProjectsUpdateComponent"]],
        exports: [_projects_update_component__WEBPACK_IMPORTED_MODULE_14__["ProjectsUpdateComponent"]],
    })
], ProjectsUpdateModule);



/***/ }),

/***/ "5DOe":
/*!*********************************************************************************************************************************************************!*\
  !*** ./src/app/modules/projects/pages/project-details/components/project-members/components/project-members-create/project-members-create.component.ts ***!
  \*********************************************************************************************************************************************************/
/*! exports provided: ProjectMembersCreateComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectMembersCreateComponent", function() { return ProjectMembersCreateComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_project_members_create_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./project-members-create.component.html */ "3XCj");
/* harmony import */ var _project_members_create_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./project-members-create.component.scss */ "D6Zu");
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
















let ProjectMembersCreateComponent = class ProjectMembersCreateComponent {
    constructor(defaults, dialogRef, fb) {
        this.defaults = defaults;
        this.dialogRef = dialogRef;
        this.fb = fb;
        this.onCreate = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
        this.form = this.fb.group({
            email: '',
        });
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
    ngOnInit() { }
    create() {
        const form = this.form.value;
        const formData = new FormData();
        formData.append('email', form.email);
        this.onCreate.emit(formData);
        this.dialogRef.close();
    }
};
ProjectMembersCreateComponent.ctorParameters = () => [
    { type: undefined, decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Inject"], args: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MAT_DIALOG_DATA"],] }] },
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MatDialogRef"] },
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormBuilder"] }
];
ProjectMembersCreateComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'project-members-create',
        template: _raw_loader_project_members_create_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_project_members_create_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], ProjectMembersCreateComponent);



/***/ }),

/***/ "71Jh":
/*!**********************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/projects/components/projects-update/projects-update.component.html ***!
  \**********************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<form (ngSubmit)=\"save()\" [formGroup]=\"form\">\r\n  <div fxLayout=\"row\" fxLayoutAlign=\"start center\" mat-dialog-title>\r\n    <h2 class=\"headline m-0\" fxFlex=\"auto\">{{ project ? 'Edit' : 'New' }} Project</h2>\r\n\r\n    <button class=\"text-secondary\" mat-dialog-close mat-icon-button type=\"button\">\r\n      <mat-icon [icIcon]=\"icClose\"></mat-icon>\r\n    </button>\r\n  </div>\r\n\r\n  <mat-divider class=\"-mx-6 text-border\"></mat-divider>\r\n\r\n  <mat-dialog-content fxLayout=\"column\">\r\n    <mat-form-field class=\"mt-6\">\r\n      <mat-label>Name</mat-label>\r\n      <input cdkFocusInitial formControlName=\"name\" matInput>\r\n\r\n      <mat-icon [icIcon]=\"icPerson\" class=\"ltr:mr-3 rtl:ml-3\" matPrefix></mat-icon>\r\n    </mat-form-field>\r\n\r\n    <mat-form-field>\r\n      <mat-label>Description</mat-label>\r\n      <textarea formControlName=\"description\" matInput></textarea>\r\n    </mat-form-field>\r\n  </mat-dialog-content>\r\n\r\n  <mat-dialog-actions align=\"end\">\r\n    <button mat-button mat-dialog-close type=\"button\">CANCEL</button>\r\n    <button color=\"primary\" mat-button type=\"submit\">{{ project ? 'UPDATE' : 'CREATE' }}</button>\r\n  </mat-dialog-actions>\r\n</form>\r\n");

/***/ }),

/***/ "7m4f":
/*!*****************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/projects/pages/project-details/project-details.component.html ***!
  \*****************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div class=\"container py-gutter\">\n  <div class=\"card overflow-hidden\">\n    <div class=\"h-64 relative overflow-hidden\">\n      <img class=\"w-full object-cover\" src=\"assets/img/demo/landscape.jpg\">\n      <div class=\"absolute bg-contrast-black opacity-25 top-0 right-0 bottom-0 left-0 w-full h-full z-0\"></div>\n\n      <img class=\"avatar h-24 w-24 absolute top-6 left-4\"\n           fxFlex=\"none\"\n           fxFlexAlign=\"start\"\n           fxHide.gt-xs\n           src=\"assets/img/avatars/1.jpg\">\n    </div>\n\n    <div class=\"z-10 relative -mt-16 px-gutter\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n\n     <ngx-avatar @scaleIn\n          class=\"avatar h-24 w-24\"\n          fxFlex=\"none\"\n          fxFlexAlign=\"start\"\n          fxHide.xs\n          name=\"{{project.name}}\"\n          size=\"100\">\n      </ngx-avatar>\n\n      <div [ngClass.gt-xs]=\"['ltr:ml-6 rtl:mr-6']\" class=\"max-w-full\" fxFlex=\"auto\">\n        <div class=\"h-16\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n          <h1 @fadeInRight class=\"headline text-contrast-white m-0\">{{ project.name }}</h1>\n        </div>\n\n        <nav class=\"vex-tabs vex-tabs-dense border-0\" mat-tab-nav-bar>\n          <a #rla=\"routerLinkActive\"\n             *ngFor=\"let link of links\"\n             [active]=\"rla.isActive\"\n             [disabled]=\"link.disabled\"\n             [routerLink]=\"link.route\"\n             mat-tab-link\n             queryParamsHandling=\"preserve\"\n             routerLinkActive>\n            {{ link.label }}\n          </a>\n        </nav>\n      </div>\n\n    </div>\n  </div>\n\n  <router-outlet></router-outlet>\n</div>\n");

/***/ }),

/***/ "8kLj":
/*!****************************************************************************************************************!*\
  !*** ./src/app/modules/projects/pages/project-details/components/project-members/project-members.component.ts ***!
  \****************************************************************************************************************/
/*! exports provided: ProjectMembersComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectMembersComponent", function() { return ProjectMembersComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_project_members_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./project-members.component.html */ "TJ7c");
/* harmony import */ var _project_members_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./project-members.component.scss */ "aKIO");
/* harmony import */ var _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/cdk/collections */ "CtHx");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/forms */ "s7LF");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/dialog */ "iELJ");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/material/form-field */ "Q2Ze");
/* harmony import */ var _angular_material_paginator__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/material/paginator */ "5QHs");
/* harmony import */ var _angular_material_sort__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/material/sort */ "LUZP");
/* harmony import */ var _angular_material_table__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @angular/material/table */ "OaSA");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var ngx_take_until_destroy__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ngx-take-until-destroy */ "DnKK");
/* harmony import */ var _vex_animations__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @vex/animations */ "ORuP");
/* harmony import */ var _core_http_projects_user_resource_service__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @core/http/projects-user-resource.service */ "XTWy");
/* harmony import */ var _core_utils_file_service__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @core/utils/file.service */ "EGFe");
/* harmony import */ var _data_schema__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @data/schema */ "V99k");
/* harmony import */ var _components_project_members_create_project_members_create_component__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! ./components/project-members-create/project-members-create.component */ "5DOe");
/* harmony import */ var _mock_project_members_data__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! ./mock/project-members-data */ "R12G");
/* harmony import */ var _services_project_members_data_service__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! ./services/project-members-data.service */ "e/UG");
/* harmony import */ var _services_project_members_icons_service__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! ./services/project-members-icons.service */ "Wti8");
/* harmony import */ var _services_projects_user_role_data_service__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! ./services/projects-user-role-data.service */ "+zwo");























let ProjectMembersComponent = class ProjectMembersComponent {
    constructor(activatedRoute, dialog, file, location, projectMemberIcons, projectMembersDataService, projectsUserResource, projectsUserRoleData, router, route) {
        this.activatedRoute = activatedRoute;
        this.dialog = dialog;
        this.file = file;
        this.location = location;
        this.projectMemberIcons = projectMemberIcons;
        this.projectMembersDataService = projectMembersDataService;
        this.projectsUserResource = projectsUserResource;
        this.projectsUserRoleData = projectsUserRoleData;
        this.router = router;
        this.route = route;
        this.layoutCtrl = new _angular_forms__WEBPACK_IMPORTED_MODULE_6__["FormControl"]('boxed');
        // Table settings
        this.columns = [
            { label: 'Checkbox', property: 'checkbox', type: 'checkbox', visible: true },
            { label: 'Role', property: 'role', type: 'dropdown', visible: true },
            { label: 'Name', property: 'name', type: 'text', visible: true },
            { label: 'Email', property: 'email', type: 'text', visible: true },
        ];
        this.pageIndex = this.route.snapshot.queryParams.page || 0;
        this.pageSize = 10;
        this.pageSizeOptions = [5, 10, 20, 50];
        this.selection = new _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_3__["SelectionModel"](true, []);
        this.searchCtrl = new _angular_forms__WEBPACK_IMPORTED_MODULE_6__["FormControl"]();
        this.labels = _mock_project_members_data__WEBPACK_IMPORTED_MODULE_19__["aioTableLabels"];
        // Breadcrumb settings
        this.crumbs = [{
                name: 'ProjectsUsers',
            }];
    }
    get visibleColumns() {
        return this.columns.filter(column => column.visible).map(column => column.property);
    }
    ngOnInit() {
        this.dataSource = new _angular_material_table__WEBPACK_IMPORTED_MODULE_11__["MatTableDataSource"]();
        this.projectMembersDataService.members$.subscribe((members) => {
            this.dataSource.data = members;
        });
        const projectMembers = this.route.snapshot.data.members.map(member => {
            return new _data_schema__WEBPACK_IMPORTED_MODULE_17__["ProjectsUser"](member);
        });
        this.projectMembersDataService.set(projectMembers);
        this.searchCtrl.valueChanges.pipe(Object(ngx_take_until_destroy__WEBPACK_IMPORTED_MODULE_13__["untilDestroyed"])(this)).subscribe(value => this.onFilterChange(value));
        this.icons = this.projectMemberIcons;
        this.roleData = this.projectsUserRoleData;
    }
    ngAfterViewInit() {
        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
    }
    getProjectsUsers(params) {
        const projectId = this.getProjectId();
        this.projectsUserResource.index(projectId, params).subscribe((res) => {
            this.projectMembersDataService.set(res);
        }, error => {
        });
    }
    createProjectsUser(data) {
        const projectId = this.getProjectId();
        this.projectsUserResource.create(projectId, data).subscribe(res => {
            const snapshot = this.route.snapshot;
            this.getProjectsUsers(projectId);
        }, error => {
        });
    }
    showProjectsUser(member) {
        const path = this.file.join('/', 'users', member.id, 'profile');
        const snapshot = this.route.snapshot;
        this.router.navigate([path]);
    }
    destroyProjectsUser(member) {
        const projectId = this.getProjectId();
        this.projectsUserResource.destroy(projectId, member.id).subscribe(res => {
            this.projectMembersDataService.delete(member.id);
            this.selection.deselect(member);
        });
    }
    destroyProjectsUsers(projectMembers) {
        projectMembers.forEach(r => this.destroyProjectsUser(r));
    }
    updateProjectsUser(member, params) {
        const projectId = this.getProjectId();
        this.projectsUserResource.update(projectId, member.id, params).subscribe(res => {
            for (const key in params) {
                if (params.hasOwnProperty(key)) {
                    member[key] = params[key];
                }
            }
        });
    }
    /**
     *
     * Table methods
     *
     */
    openCreateDialog() {
        const dialogRef = this.dialog.open(_components_project_members_create_project_members_create_component__WEBPACK_IMPORTED_MODULE_18__["ProjectMembersCreateComponent"], {
            width: '600px',
        });
        const onCreateSub = dialogRef.componentInstance.onCreate.subscribe(($event) => {
            this.createProjectsUser($event);
        });
        dialogRef.afterClosed().subscribe((member) => {
            onCreateSub.unsubscribe();
        });
    }
    onFilterChange(value) {
        if (!this.dataSource) {
            return;
        }
        value = value.trim();
        value = value.toLowerCase();
        this.dataSource.filter = value;
    }
    toggleColumnVisibility(column, event) {
        event.stopPropagation();
        event.stopImmediatePropagation();
        column.visible = !column.visible;
    }
    /** Whether the number of selected elements matches the total number of rows. */
    isAllSelected() {
        const numSelected = this.selection.selected.length;
        const numRows = this.dataSource.data.length;
        return numSelected === numRows;
    }
    /** Selects all rows if they are not all selected; otherwise clear selection. */
    masterToggle() {
        this.isAllSelected() ?
            this.selection.clear() :
            this.dataSource.data.forEach(row => this.selection.select(row));
    }
    trackByProperty(index, column) {
        return column.property;
    }
    /**
     * On page change, add queryParam 'page' to URL
     */
    onPaginateChange($event) {
        const queryParams = Object.assign({}, this.route.snapshot.queryParams);
        queryParams.page = $event.pageIndex;
        const url = this
            .router
            .createUrlTree([], { relativeTo: this.activatedRoute, queryParams })
            .toString();
        this.location.go(url);
    }
    getProjectId() {
        const snapshot = this.route.snapshot;
        const projectId = snapshot.parent.params.projectId;
        return projectId;
    }
    ngOnDestroy() { }
};
ProjectMembersComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_12__["ActivatedRoute"] },
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_7__["MatDialog"] },
    { type: _core_utils_file_service__WEBPACK_IMPORTED_MODULE_16__["FileService"] },
    { type: _angular_common__WEBPACK_IMPORTED_MODULE_4__["Location"] },
    { type: _services_project_members_icons_service__WEBPACK_IMPORTED_MODULE_21__["ProjectMembersIcons"] },
    { type: _services_project_members_data_service__WEBPACK_IMPORTED_MODULE_20__["ProjectMembersDataService"] },
    { type: _core_http_projects_user_resource_service__WEBPACK_IMPORTED_MODULE_15__["ProjectsUserResource"] },
    { type: _services_projects_user_role_data_service__WEBPACK_IMPORTED_MODULE_22__["ProjectsUserRoleData"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_12__["Router"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_12__["ActivatedRoute"] }
];
ProjectMembersComponent.propDecorators = {
    columns: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_5__["Input"] }],
    paginator: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_5__["ViewChild"], args: [_angular_material_paginator__WEBPACK_IMPORTED_MODULE_9__["MatPaginator"], { static: true },] }],
    sort: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_5__["ViewChild"], args: [_angular_material_sort__WEBPACK_IMPORTED_MODULE_10__["MatSort"], { static: true },] }]
};
ProjectMembersComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_5__["Component"])({
        selector: 'project-members',
        template: _raw_loader_project_members_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        animations: [
            _vex_animations__WEBPACK_IMPORTED_MODULE_14__["fadeInUp400ms"],
            _vex_animations__WEBPACK_IMPORTED_MODULE_14__["stagger40ms"],
        ],
        providers: [
            {
                provide: _angular_material_form_field__WEBPACK_IMPORTED_MODULE_8__["MAT_FORM_FIELD_DEFAULT_OPTIONS"],
                useValue: {
                    appearance: 'standard',
                },
            },
        ],
        styles: [_project_members_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], ProjectMembersComponent);



/***/ }),

/***/ "9+z0":
/*!********************************************************************************************!*\
  !*** ./src/app/modules/projects/components/projects-update/projects-update.component.scss ***!
  \********************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJwcm9qZWN0cy11cGRhdGUuY29tcG9uZW50LnNjc3MifQ== */");

/***/ }),

/***/ "D6Zu":
/*!***********************************************************************************************************************************************************!*\
  !*** ./src/app/modules/projects/pages/project-details/components/project-members/components/project-members-create/project-members-create.component.scss ***!
  \***********************************************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJwcm9qZWN0LW1lbWJlcnMtY3JlYXRlLmNvbXBvbmVudC5zY3NzIn0= */");

/***/ }),

/***/ "GFHg":
/*!******************************************************************************************************************!*\
  !*** ./src/app/modules/projects/pages/project-details/components/project-settings/project-settings.component.ts ***!
  \******************************************************************************************************************/
/*! exports provided: ProjectSettingsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectSettingsComponent", function() { return ProjectSettingsComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_project_settings_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./project-settings.component.html */ "KVRE");
/* harmony import */ var _project_settings_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./project-settings.component.scss */ "w3PA");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/dialog */ "iELJ");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _vex_animations__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @vex/animations */ "ORuP");
/* harmony import */ var _core_http_project_resource_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @core/http/project-resource.service */ "4UAC");
/* harmony import */ var _data_schema__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @data/schema */ "V99k");
/* harmony import */ var _projects_components_projects_update_projects_update_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @projects/components/projects-update/projects-update.component */ "orsw");
/* harmony import */ var _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @projects/services/project-data.service */ "oyjd");
/* harmony import */ var _services_project_settings_icons_service__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./services/project-settings-icons.service */ "zGPG");












let ProjectSettingsComponent = class ProjectSettingsComponent {
    constructor(dialog, projectResource, projectDataService, projectSettingsIcons, route, router) {
        this.dialog = dialog;
        this.projectResource = projectResource;
        this.projectDataService = projectDataService;
        this.projectSettingsIcons = projectSettingsIcons;
        this.route = route;
        this.router = router;
        this.links = [
            {
                label: 'MEMBERS',
                route: './',
            },
            {
                label: 'BILLING',
                route: '',
                disabled: false,
            },
        ];
    }
    ngOnInit() {
        this.projectDataService.project$.subscribe(project => {
            this.project = new _data_schema__WEBPACK_IMPORTED_MODULE_8__["Project"](project);
        });
        this.icons = this.projectSettingsIcons;
    }
    scenariosPath() {
        return '/scenarios';
    }
    projectQueryParams(project) {
        return {
            project_id: project.id,
        };
    }
    openUpdateProjectDialog() {
        const dialogRef = this.dialog.open(_projects_components_projects_update_projects_update_component__WEBPACK_IMPORTED_MODULE_9__["ProjectsUpdateComponent"], {
            width: '600px',
            data: this.project,
        });
        const onUpdateSub = dialogRef.componentInstance.onUpdate.subscribe(($event) => {
            this.updateProject($event);
        });
        dialogRef.afterClosed().subscribe(() => {
            onUpdateSub.unsubscribe();
        });
    }
    updateProject(data) {
        this.projectResource.update(this.project.id, data).subscribe((res) => {
            this.project = res;
            this.projectDataService.set(res);
        }, err => {
        });
    }
};
ProjectSettingsComponent.ctorParameters = () => [
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_4__["MatDialog"] },
    { type: _core_http_project_resource_service__WEBPACK_IMPORTED_MODULE_7__["ProjectResource"] },
    { type: _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_10__["ProjectDataService"] },
    { type: _services_project_settings_icons_service__WEBPACK_IMPORTED_MODULE_11__["ProjectSettingsIcons"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_5__["ActivatedRoute"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_5__["Router"] }
];
ProjectSettingsComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'project-settings',
        template: _raw_loader_project_settings_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        animations: [
            _vex_animations__WEBPACK_IMPORTED_MODULE_6__["fadeInUp400ms"],
            _vex_animations__WEBPACK_IMPORTED_MODULE_6__["fadeInRight400ms"],
            _vex_animations__WEBPACK_IMPORTED_MODULE_6__["scaleIn400ms"],
            _vex_animations__WEBPACK_IMPORTED_MODULE_6__["stagger40ms"],
        ],
        styles: [_project_settings_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], ProjectSettingsComponent);



/***/ }),

/***/ "GVnh":
/*!***************************************************************************************************************!*\
  !*** ./src/app/modules/projects/pages/project-details/components/project-settings/project-settings.module.ts ***!
  \***************************************************************************************************************/
/*! exports provided: ProjectSettingsModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectSettingsModule", function() { return ProjectSettingsModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_material_core__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/core */ "UhP/");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @vex/components/page-layout/page-layout.module */ "7lCJ");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _projects_components_projects_update_projects_update_module__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @projects/components/projects-update/projects-update.module */ "5+Rn");
/* harmony import */ var _project_settings_component__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./project-settings.component */ "GFHg");












let ProjectSettingsModule = class ProjectSettingsModule {
};
ProjectSettingsModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_project_settings_component__WEBPACK_IMPORTED_MODULE_11__["ProjectSettingsComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_8__["PageLayoutModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_9__["IconModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_4__["MatButtonModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_6__["MatIconModule"],
            _angular_material_core__WEBPACK_IMPORTED_MODULE_5__["MatRippleModule"],
            _angular_router__WEBPACK_IMPORTED_MODULE_7__["RouterModule"],
            _projects_components_projects_update_projects_update_module__WEBPACK_IMPORTED_MODULE_10__["ProjectsUpdateModule"],
        ],
    })
], ProjectSettingsModule);



/***/ }),

/***/ "Iker":
/*!*************************************************************************************!*\
  !*** ./src/app/modules/projects/pages/project-details/project-details.component.ts ***!
  \*************************************************************************************/
/*! exports provided: ProjectDetailsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectDetailsComponent", function() { return ProjectDetailsComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_project_details_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./project-details.component.html */ "7m4f");
/* harmony import */ var _project_details_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./project-details.component.scss */ "piVU");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _iconify_icons_ic_twotone_access_time__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @iconify/icons-ic/twotone-access-time */ "NBim");
/* harmony import */ var _iconify_icons_ic_twotone_access_time__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_access_time__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @iconify/icons-ic/twotone-add */ "7wwx");
/* harmony import */ var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _iconify_icons_ic_twotone_check__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @iconify/icons-ic/twotone-check */ "+tDV");
/* harmony import */ var _iconify_icons_ic_twotone_check__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_check__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @iconify/icons-ic/twotone-mail */ "6qw8");
/* harmony import */ var _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _iconify_icons_ic_twotone_person_add__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @iconify/icons-ic/twotone-person-add */ "+q50");
/* harmony import */ var _iconify_icons_ic_twotone_person_add__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_person_add__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @iconify/icons-ic/twotone-phone */ "YA1h");
/* harmony import */ var _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _iconify_icons_ic_twotone_whatshot__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @iconify/icons-ic/twotone-whatshot */ "OcYv");
/* harmony import */ var _iconify_icons_ic_twotone_whatshot__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_whatshot__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var _iconify_icons_ic_twotone_work__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @iconify/icons-ic/twotone-work */ "6W+F");
/* harmony import */ var _iconify_icons_ic_twotone_work__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_work__WEBPACK_IMPORTED_MODULE_12__);
/* harmony import */ var _vex_animations__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @vex/animations */ "ORuP");
/* harmony import */ var _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @projects/services/project-data.service */ "oyjd");















let ProjectDetailsComponent = class ProjectDetailsComponent {
    constructor(route, projectDataService) {
        this.route = route;
        this.projectDataService = projectDataService;
        this.links = [
            {
                label: 'SETTINGS',
                route: 'settings',
                active: () => this.isActive('settings'),
            },
            {
                label: 'MEMBERS',
                route: 'members',
                active: () => this.isActive('members'),
            },
        ];
        this.icWork = _iconify_icons_ic_twotone_work__WEBPACK_IMPORTED_MODULE_12___default.a;
        this.icPhone = _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_10___default.a;
        this.icPersonAdd = _iconify_icons_ic_twotone_person_add__WEBPACK_IMPORTED_MODULE_9___default.a;
        this.icCheck = _iconify_icons_ic_twotone_check__WEBPACK_IMPORTED_MODULE_7___default.a;
        this.icMail = _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_8___default.a;
        this.icAccessTime = _iconify_icons_ic_twotone_access_time__WEBPACK_IMPORTED_MODULE_5___default.a;
        this.icAdd = _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_6___default.a;
        this.icWhatshot = _iconify_icons_ic_twotone_whatshot__WEBPACK_IMPORTED_MODULE_11___default.a;
    }
    ngOnInit() {
        this.project = this.route.snapshot.data.project;
        this.projectDataService.set(this.project);
    }
    isActive(path) {
        return this.route.firstChild.routeConfig.path === path;
    }
};
ProjectDetailsComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["ActivatedRoute"] },
    { type: _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_14__["ProjectDataService"] }
];
ProjectDetailsComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'project-details',
        template: _raw_loader_project_details_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        animations: [
            _vex_animations__WEBPACK_IMPORTED_MODULE_13__["fadeInUp400ms"],
            _vex_animations__WEBPACK_IMPORTED_MODULE_13__["fadeInRight400ms"],
            _vex_animations__WEBPACK_IMPORTED_MODULE_13__["scaleIn400ms"],
            _vex_animations__WEBPACK_IMPORTED_MODULE_13__["stagger40ms"],
        ],
        styles: [_project_details_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], ProjectDetailsComponent);



/***/ }),

/***/ "JAZM":
/*!***************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/projects/pages/projects-index/projects-index.component.html ***!
  \***************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div class=\"h-full\" fxLayout=\"column\">\n\n  <div class=\"p-4 border-b\" fxFlex=\"none\">\n    <div class=\"container\">\n      <div fxLayout=\"row\" fxLayoutAlign=\"start center\">\n\n        <nav class=\"border-0\" fxFlex=\"row\" fxLayoutAlign=\"start center\">\n          <span @scaleIn\n              [style.background-color]=\"theme.colors.primary['500'] | colorFade:0.9\"\n              class=\"w-12 h-12 rounded-full text-primary-500 ltr:mr-4 rtl:ml-4 flex items-center justify-center\">\n              <ic-icon [icon]=\"icons.icCollections\" size=\"24px\"></ic-icon>\n          </span>\n\n          <h5>Organization</h5>\n\n          <button\n            class=\"ltr:ml-3\"\n            mat-stroked-button\n            [matMenuTriggerFor]=\"categoryMenu\"\n            color=\"primary\">\n            {{ selectedOrganization.isShadow ? 'Personal' : selectedOrganization.name }}\n            <ic-icon [icon]=\"icons.icArrowDropDown\" inline=\"true\"></ic-icon>\n          </button>\n\n          <button\n            class=\"ltr:ml-2\"\n            mat-icon-button\n            color=\"primary\"\n            *ngIf=\"!selectedOrganization.isShadow\"\n            (click)=\"showOrganization()\">\n            <ic-icon [icon]=\"icons.icSettings\" inline=\"true\" size=\"25px\"></ic-icon>\n          </button>\n        </nav>\n      </div>\n    </div>\n  </div>\n\n  <div class=\"p-4\" fxFlex=\"none\">\n    <div class=\"container\">\n      <div fxLayout=\"row\" fxLayoutAlign=\"start center\">\n        <h5 @fadeInRight>Projects</h5>\n\n        <button (click)=\"openCreateDialog()\"\n                class=\"ltr:ml-3 rtl:mr-4\"\n                color=\"primary\"\n                fxFlex=\"none\"\n                fxHide.xs\n                mat-raised-button\n                type=\"button\">\n          <ic-icon [icon]=\"icons.icAdd\"\n                    class=\"ltr:mr-1 rtl:ml-1 ltr:-ml-1 rtl:-mr-1\"\n                    inline=\"true\"></ic-icon>\n\n          <span>CREATE</span>\n        </button>\n      </div>\n    </div>\n  </div>\n\n  <div *ngIf=\"projects.length > 0\"\n       @stagger\n       class=\"overflow-y-auto\"\n       fxFlex=\"auto\">\n    <div class=\"p-gutter container\"\n         gdColumns=\"1fr 1fr 1fr 1fr\"\n         gdColumns.lt-md=\"1fr 1fr\"\n         gdColumns.xs=\"1fr\"\n         gdGap=\"24px\">\n      <projects-card\n        (members)=\"showProjectMembers($event)\"\n        (view)=\"showRequests($event)\"\n        (delete)=\"deleteProject($event)\"\n        (toggleStar)=\"toggleStar($event)\"\n        (update)=\"openUpdateDialog($event)\"\n        *ngFor=\"let project of projects; trackBy: trackById\"\n        @fadeInUp\n        [project]=\"project\"></projects-card>\n    </div>\n  </div>\n\n  <div *ngIf=\"projects.length === 0\"\n       @scaleFadeIn\n       fxFlex=\"auto\"\n       fxLayout=\"column\"\n       fxLayoutAlign=\"center center\">\n    <img class=\"m-12 h-64\" src=\"assets/img/illustrations/idea.svg\">\n    <h2 class=\"headline m-0 text-center\">No projects found</h2>\n  </div>\n</div>\n\n<mat-menu #categoryMenu=\"matMenu\" xPosition=\"before\" yPosition=\"below\">\n  <ng-template matMenuContent>\n    <button mat-menu-item\n      *ngFor=\"let organization of organizations\"\n      (click)=\"viewOrganization(organization)\">\n      {{ organization.isShadow ? 'Personal' : organization.name }}\n    </button>\n  </ng-template>\n  <button mat-menu-item\n    (click)=\"showUserOrganizations()\">\n    <mat-icon [icIcon]=\"icons.icPeople\"></mat-icon>\n    Manage organizations\n  </button>\n  <button mat-menu-item\n    (click)=\"openCreateOrganizationDialog()\">\n    <mat-icon [icIcon]=\"icons.icAdd\"></mat-icon>\n    Create organization\n  </button>\n</mat-menu>\n");

/***/ }),

/***/ "JUG8":
/*!******************************************************************************************!*\
  !*** ./src/app/modules/projects/components/projects-create/projects-create.component.ts ***!
  \******************************************************************************************/
/*! exports provided: ProjectsCreateComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectsCreateComponent", function() { return ProjectsCreateComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_projects_create_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./projects-create.component.html */ "vHR1");
/* harmony import */ var _projects_create_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./projects-create.component.scss */ "sGWm");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ "s7LF");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/dialog */ "iELJ");
/* harmony import */ var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @iconify/icons-ic/twotone-close */ "5mnX");
/* harmony import */ var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @iconify/icons-ic/twotone-delete */ "e3EN");
/* harmony import */ var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @iconify/icons-ic/twotone-mail */ "6qw8");
/* harmony import */ var _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @iconify/icons-ic/twotone-person */ "KaaH");
/* harmony import */ var _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _data_schema__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @data/schema */ "V99k");











let ProjectsCreateComponent = class ProjectsCreateComponent {
    constructor(project, dialogRef, fb) {
        this.project = project;
        this.dialogRef = dialogRef;
        this.fb = fb;
        this.isUpdate = false;
        this.onCreate = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
        this.form = this.fb.group({
            name: null,
            description: null,
        });
        this.icClose = _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_6___default.a;
        this.icDelete = _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_7___default.a;
        this.icPerson = _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_9___default.a;
        this.icEmail = _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_8___default.a;
    }
    ngOnInit() {
        if (this.project) {
            this.isUpdate = true;
        }
        this.form.patchValue(this.project || {});
    }
    save() {
        this.onCreate.emit(this.form.value);
        this.dialogRef.close();
    }
};
ProjectsCreateComponent.ctorParameters = () => [
    { type: _data_schema__WEBPACK_IMPORTED_MODULE_10__["Project"], decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Inject"], args: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MAT_DIALOG_DATA"],] }] },
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MatDialogRef"] },
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormBuilder"] }
];
ProjectsCreateComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'projects-create',
        template: _raw_loader_projects_create_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_projects_create_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], ProjectsCreateComponent);



/***/ }),

/***/ "KVRE":
/*!**********************************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/projects/pages/project-details/components/project-settings/project-settings.component.html ***!
  \**********************************************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div class=\"mt-6\"\n     fxLayout=\"row\"\n     fxLayout.lt-md=\"column\"\n     fxLayoutAlign=\"start start\"\n     fxLayoutAlign.lt-md=\"start stretch\"\n     fxLayoutGap=\"24px\">\n  <div fxFlex=\"calc(70% - 12px)\" fxFlex.lt-md=\"auto\">\n    <div class=\"card\">\n      <div class=\"px-gutter py-4 border-b\">\n        <h2 class=\"block title\">\n          Settings\n        </h2>\n        <!-- <button class=\"text-secondary ltr:ml-3 rtl:mr-4\" fxFlex=\"none\" mat-icon-button type=\"button\">\n          <mat-icon [icIcon]=\"icons.icEdit\"></mat-icon>\n        </button> -->\n      </div>\n\n      <div class=\"px-gutter py-4\" gdColumns=\"1fr\" gdColumns.xs=\"1fr\" gdGap=\"16px\">\n        <div class=\"py-3\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n          <div @scaleIn\n               class=\"w-10 h-10 rounded-full bg-primary-50 text-primary-500 ltr:mr-3 rtl:ml-3 flex items-center justify-center\">\n            <ic-icon [icon]=\"icons.icPhone\" size=\"20px\"></ic-icon>\n          </div>\n\n          <div @fadeInRight>\n            <p class=\"m-0 body-1\">{{ project.name }}</p>\n            <p class=\"m-0 caption text-hint\">Project display name</p>\n          </div>\n        </div>\n\n        <div class=\"py-3\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n          <div @scaleIn\n               class=\"w-10 h-10 rounded-full bg-primary-50 text-primary-500 ltr:mr-3 rtl:ml-3 flex items-center justify-center\">\n            <ic-icon [icon]=\"icons.icWork\" size=\"20px\"></ic-icon>\n          </div>\n\n          <div @fadeInRight>\n            <p class=\"m-0 body-1\">{{ project.description || 'N/A' }}</p>\n            <p class=\"m-0 caption text-hint\">Description</p>\n          </div>\n        </div>\n\n        <div class=\"py-3\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n          <div @scaleIn\n               class=\"w-10 h-10 rounded-full bg-primary-50 text-primary-500 ltr:mr-3 rtl:ml-3 flex items-center justify-center\">\n            <ic-icon [icon]=\"icons.icWork\" size=\"20px\"></ic-icon>\n          </div>\n\n          <div @fadeInRight>\n            <p class=\"m-0 body-1\">{{ project.key }}</p>\n            <p class=\"m-0 caption text-hint\">Project Key</p>\n          </div>\n        </div>\n\n        <div class=\"py-3\" fxLayout=\"row\" fxLayoutAlign=\"start\">\n          <button (click)=\"openUpdateProjectDialog()\"\n                  class=\"rtl:mr-4\"\n                  color=\"primary\"\n                  fxFlex=\"none\"\n                  fxHide.xs\n                  mat-raised-button\n                  type=\"button\">\n            <!-- <ic-icon [icon]=\"icons.icEdit\"\n                     class=\"ltr:mr-1 rtl:ml-1 ltr:-ml-1 rtl:-mr-1\"\n                     inline=\"true\"></ic-icon> -->\n            EDIT\n          </button>\n        </div>\n      </div>\n    </div>\n  </div>\n</div>\n");

/***/ }),

/***/ "MvdI":
/*!**********************************************************************************!*\
  !*** ./src/app/modules/organizations/services/organizations-resolver.service.ts ***!
  \**********************************************************************************/
/*! exports provided: OrganizationsResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "OrganizationsResolver", function() { return OrganizationsResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _core_http_organization_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @core/http/organization-resource.service */ "wjWB");



let OrganizationsResolver = class OrganizationsResolver {
    constructor(organizationResource) {
        this.organizationResource = organizationResource;
    }
    resolve(route) {
        const params = {};
        const routeData = route.data;
        if (routeData.shadow) {
            params.shadow = true;
        }
        return this.organizationResource.index(params);
    }
};
OrganizationsResolver.ctorParameters = () => [
    { type: _core_http_organization_resource_service__WEBPACK_IMPORTED_MODULE_2__["OrganizationResource"] }
];
OrganizationsResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], OrganizationsResolver);



/***/ }),

/***/ "NihL":
/*!*************************************************************!*\
  !*** ./src/app/modules/projects/projects-routing.module.ts ***!
  \*************************************************************/
/*! exports provided: ProjectsRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectsRoutingModule", function() { return ProjectsRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _organizations_services_organizations_resolver_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @organizations/services/organizations-resolver.service */ "MvdI");
/* harmony import */ var _projects_services_project_resolver_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @projects/services/project-resolver.service */ "Y1jZ");
/* harmony import */ var _projects_services_projects_resolver_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @projects/services/projects-resolver.service */ "yVsR");
/* harmony import */ var _pages_project_details_components_project_members_project_members_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./pages/project-details/components/project-members/project-members.component */ "8kLj");
/* harmony import */ var _pages_project_details_components_project_members_services_projects_users_resolver_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./pages/project-details/components/project-members/services/projects-users-resolver.service */ "nMgu");
/* harmony import */ var _pages_project_details_components_project_settings_project_settings_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./pages/project-details/components/project-settings/project-settings.component */ "GFHg");
/* harmony import */ var _pages_project_details_project_details_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./pages/project-details/project-details.component */ "Iker");
/* harmony import */ var _pages_projects_index_projects_index_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./pages/projects-index/projects-index.component */ "Nt3V");











const routes = [
    {
        path: '',
        component: _pages_projects_index_projects_index_component__WEBPACK_IMPORTED_MODULE_10__["ProjectsIndexComponent"],
        resolve: {
            projects: _projects_services_projects_resolver_service__WEBPACK_IMPORTED_MODULE_5__["ProjectsResolver"],
            organizations: _organizations_services_organizations_resolver_service__WEBPACK_IMPORTED_MODULE_3__["OrganizationsResolver"],
        },
        data: {
            shadow: true,
        },
    },
    {
        path: ':project_id',
        component: _pages_project_details_project_details_component__WEBPACK_IMPORTED_MODULE_9__["ProjectDetailsComponent"],
        resolve: {
            project: _projects_services_project_resolver_service__WEBPACK_IMPORTED_MODULE_4__["ProjectResolver"],
        },
        children: [
            {
                path: '',
                component: _pages_project_details_components_project_members_project_members_component__WEBPACK_IMPORTED_MODULE_6__["ProjectMembersComponent"],
                resolve: {
                    members: _pages_project_details_components_project_members_services_projects_users_resolver_service__WEBPACK_IMPORTED_MODULE_7__["ProjectsUsersResolver"],
                },
            },
            {
                path: 'settings',
                component: _pages_project_details_components_project_settings_project_settings_component__WEBPACK_IMPORTED_MODULE_8__["ProjectSettingsComponent"],
                resolve: {
                    project: _projects_services_project_resolver_service__WEBPACK_IMPORTED_MODULE_4__["ProjectResolver"],
                },
            },
            {
                path: 'members',
                component: _pages_project_details_components_project_members_project_members_component__WEBPACK_IMPORTED_MODULE_6__["ProjectMembersComponent"],
                resolve: {
                    members: _pages_project_details_components_project_members_services_projects_users_resolver_service__WEBPACK_IMPORTED_MODULE_7__["ProjectsUsersResolver"],
                },
            },
        ],
    },
];
let ProjectsRoutingModule = class ProjectsRoutingModule {
};
ProjectsRoutingModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes),
        ],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
    })
], ProjectsRoutingModule);



/***/ }),

/***/ "Nt3V":
/*!***********************************************************************************!*\
  !*** ./src/app/modules/projects/pages/projects-index/projects-index.component.ts ***!
  \***********************************************************************************/
/*! exports provided: ProjectsIndexComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectsIndexComponent", function() { return ProjectsIndexComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_projects_index_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./projects-index.component.html */ "JAZM");
/* harmony import */ var _projects_index_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./projects-index.component.scss */ "szr6");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/dialog */ "iELJ");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _vex_animations__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @vex/animations */ "ORuP");
/* harmony import */ var _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @vex/utils/tailwindcss */ "XXSj");
/* harmony import */ var _vex_utils_track_by__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @vex/utils/track-by */ "zK3P");
/* harmony import */ var _core_http_organization_resource_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @core/http/organization-resource.service */ "wjWB");
/* harmony import */ var _core_http_project_resource_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @core/http/project-resource.service */ "4UAC");
/* harmony import */ var _data_schema__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @data/schema */ "V99k");
/* harmony import */ var _organizations_components_organizations_create_organizations_create_component__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @organizations/components/organizations-create/organizations-create.component */ "vb3d");
/* harmony import */ var _organizations_services_organization_data_service__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @organizations/services/organization-data.service */ "vGUX");
/* harmony import */ var _projects_components_projects_create_projects_create_component__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @projects/components/projects-create/projects-create.component */ "JUG8");
/* harmony import */ var _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @projects/services/project-data.service */ "oyjd");
/* harmony import */ var _projects_services_projects_data_service__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @projects/services/projects-data.service */ "mbNh");
/* harmony import */ var _users_services_user_data_service__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @users/services/user-data.service */ "O7ya");
/* harmony import */ var _layout_services_layout_config_service__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @layout/services/layout-config.service */ "U9Lm");
/* harmony import */ var _services_projects_index_icons_service__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! ./services/projects-index-icons.service */ "VKCF");




















let ProjectsIndexComponent = class ProjectsIndexComponent {
    constructor(dialog, layoutConfigService, projectDataService, projectsDataService, projectIndexIcons, projectResource, organizationDataService, organizationResource, route, router, userData) {
        this.dialog = dialog;
        this.layoutConfigService = layoutConfigService;
        this.projectDataService = projectDataService;
        this.projectsDataService = projectsDataService;
        this.projectIndexIcons = projectIndexIcons;
        this.projectResource = projectResource;
        this.organizationDataService = organizationDataService;
        this.organizationResource = organizationResource;
        this.route = route;
        this.router = router;
        this.userData = userData;
        this.trackById = _vex_utils_track_by__WEBPACK_IMPORTED_MODULE_8__["trackById"];
        this.theme = _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_7__["default"];
        this.layoutConfigService.setIkaros();
    }
    ngOnInit() {
        const snapshot = this.route.snapshot;
        this.projects = snapshot.data.projects.map(project => {
            return new _data_schema__WEBPACK_IMPORTED_MODULE_11__["Project"](project);
        });
        this.projectsDataService.set(this.projects);
        this.organizations = this.route.snapshot.data.organizations.map(org => {
            return new _data_schema__WEBPACK_IMPORTED_MODULE_11__["Organization"](org);
        });
        this.selectedOrganization = this.organizations.find(organization => {
            return organization.id === snapshot.queryParams.organization_id;
        });
        this.selectedOrganization = this.selectedOrganization || this.organizations[0];
        this.organizationDataService.set(this.selectedOrganization);
        // Set no project as selected
        this.projectDataService.set(null);
        // Expose icons to view
        this.icons = this.projectIndexIcons;
    }
    createProject(data) {
        data.organization_id = this.selectedOrganization.id;
        this.projectResource.create(data).subscribe((res) => {
            this.projects.unshift(res);
        }, err => {
        });
    }
    updateProject(id, data) {
        this.projectResource.update(id, data).subscribe((res) => {
            this.getProjects();
        }, err => {
        });
    }
    getProjects(organizationId) {
        const params = {};
        if (organizationId) {
            params.organization_id = organizationId;
        }
        this.projectResource.index(params).subscribe((res) => {
            this.projects = res;
        }, error => {
        });
    }
    deleteProject(projectId) {
        this.projectResource.destroy(projectId).subscribe((res) => {
            this.projects = this.projects.filter((project) => {
                return project.id !== projectId;
            });
        }, error => {
        });
    }
    getOrganizations() {
        this.organizationResource.index().subscribe((res) => {
            this.organizations = res;
        }, err => {
        });
    }
    createOrganization(data) {
        this.organizationResource.create(data).subscribe((res) => {
            this.organizations.push(res);
            this.organizations = this.organizations.slice(0);
        }, err => {
        });
    }
    viewOrganization(organization) {
        this.getProjects(organization.id);
        this.selectedOrganization = organization;
        this.organizationDataService.set(this.selectedOrganization);
        // Add queryParam to URL
        this.router.navigate([], {
            queryParams: organization.isShadow ? {} : { organization_id: organization.id },
        });
    }
    openCreateDialog() {
        const dialogRef = this.dialog.open(_projects_components_projects_create_projects_create_component__WEBPACK_IMPORTED_MODULE_14__["ProjectsCreateComponent"], {
            width: '600px',
        });
        const onCreateSub = dialogRef.componentInstance.onCreate.subscribe(($event) => {
            this.createProject($event);
        });
        dialogRef.afterClosed().subscribe(() => {
            onCreateSub.unsubscribe();
        });
    }
    openUpdateDialog(project) {
        const dialogRef = this.dialog.open(_projects_components_projects_create_projects_create_component__WEBPACK_IMPORTED_MODULE_14__["ProjectsCreateComponent"], {
            width: '600px',
            data: project,
        });
        const onCreateSub = dialogRef.componentInstance.onCreate.subscribe(($event) => {
            this.updateProject(project.id, $event);
        });
        dialogRef.afterClosed().subscribe(() => {
            onCreateSub.unsubscribe();
        });
    }
    showRequests(projectId) {
        const path = '/requests?project_id=' + projectId;
        this.router.navigateByUrl(path);
    }
    showProjectMembers(projectId) {
        const path = `/projects/${projectId}/members`;
        this.router.navigateByUrl(path);
    }
    showUserOrganizations() {
        const path = `/users/${this.userData.user.id}/organizations`;
        this.router.navigateByUrl(path);
    }
    showOrganization() {
        const path = `/organizations/${this.selectedOrganization.id}/settings`;
        this.router.navigateByUrl(path);
    }
    toggleStar(id) {
        const project = this.projects.find(c => c.id === id);
        if (project) {
            project.starred = !project.starred;
            this.updateProject(project.id, project);
        }
    }
    openCreateOrganizationDialog() {
        const dialogRef = this.dialog.open(_organizations_components_organizations_create_organizations_create_component__WEBPACK_IMPORTED_MODULE_12__["OrganizationsCreateComponent"], {
            width: '600px',
        });
        const onCreateSub = dialogRef.componentInstance.onCreate.subscribe(($event) => {
            this.createOrganization($event);
        });
        dialogRef.afterClosed().subscribe(() => {
            onCreateSub.unsubscribe();
        });
    }
    ngOnDestroy() {
        this.layoutConfigService.setZeus();
    }
};
ProjectsIndexComponent.ctorParameters = () => [
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_4__["MatDialog"] },
    { type: _layout_services_layout_config_service__WEBPACK_IMPORTED_MODULE_18__["LayoutConfigService"] },
    { type: _projects_services_project_data_service__WEBPACK_IMPORTED_MODULE_15__["ProjectDataService"] },
    { type: _projects_services_projects_data_service__WEBPACK_IMPORTED_MODULE_16__["ProjectsDataService"] },
    { type: _services_projects_index_icons_service__WEBPACK_IMPORTED_MODULE_19__["ProjectsIndexIcons"] },
    { type: _core_http_project_resource_service__WEBPACK_IMPORTED_MODULE_10__["ProjectResource"] },
    { type: _organizations_services_organization_data_service__WEBPACK_IMPORTED_MODULE_13__["OrganizationDataService"] },
    { type: _core_http_organization_resource_service__WEBPACK_IMPORTED_MODULE_9__["OrganizationResource"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_5__["ActivatedRoute"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_5__["Router"] },
    { type: _users_services_user_data_service__WEBPACK_IMPORTED_MODULE_17__["UserDataService"] }
];
ProjectsIndexComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'projects-index',
        template: _raw_loader_projects_index_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        animations: [
            _vex_animations__WEBPACK_IMPORTED_MODULE_6__["scaleIn400ms"],
            _vex_animations__WEBPACK_IMPORTED_MODULE_6__["fadeInRight400ms"],
            _vex_animations__WEBPACK_IMPORTED_MODULE_6__["stagger40ms"],
            _vex_animations__WEBPACK_IMPORTED_MODULE_6__["fadeInUp400ms"],
            _vex_animations__WEBPACK_IMPORTED_MODULE_6__["scaleFadeIn400ms"],
        ],
        styles: [_projects_index_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], ProjectsIndexComponent);



/***/ }),

/***/ "PNSm":
/*!***************************************************************!*\
  !*** ./node_modules/@iconify/icons-ic/twotone-star-border.js ***!
  \***************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

var data = {
	"body": "<path d=\"M22 9.24l-7.19-.62L12 2L9.19 8.63L2 9.24l5.46 4.73L5.82 21L12 17.27L18.18 21l-1.63-7.03L22 9.24zM12 15.4l-3.76 2.27l1-4.28l-3.32-2.88l4.38-.38L12 6.1l1.71 4.04l4.38.38l-3.32 2.88l1 4.28L12 15.4z\" fill=\"currentColor\"/>",
	"width": 24,
	"height": 24
};
exports.__esModule = true;
exports.default = data;


/***/ }),

/***/ "R12G":
/*!****************************************************************************************************************!*\
  !*** ./src/app/modules/projects/pages/project-details/components/project-members/mock/project-members-data.ts ***!
  \****************************************************************************************************************/
/*! exports provided: aioTableLabels, aioTableData */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "aioTableLabels", function() { return aioTableLabels; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "aioTableData", function() { return aioTableData; });
/* harmony import */ var _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @vex/utils/tailwindcss */ "XXSj");
/* harmony import */ var color__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! color */ "aSns");
/* harmony import */ var color__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(color__WEBPACK_IMPORTED_MODULE_1__);


const aioTableLabels = [
    {
        text: 'Headers',
        backgroundColor: color__WEBPACK_IMPORTED_MODULE_1___default()(_vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_0__["default"].colors.green['500']).fade(0.9),
        color: _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_0__["default"].colors.green['500'],
    },
    {
        text: 'Queries',
        backgroundColor: color__WEBPACK_IMPORTED_MODULE_1___default()(_vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_0__["default"].colors.cyan['500']).fade(0.9),
        color: _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_0__["default"].colors.cyan['500'],
    },
    {
        text: 'Body',
        backgroundColor: color__WEBPACK_IMPORTED_MODULE_1___default()(_vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_0__["default"].colors.teal['500']).fade(0.9),
        color: _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_0__["default"].colors.teal['500'],
    },
    {
        text: 'Response',
        backgroundColor: color__WEBPACK_IMPORTED_MODULE_1___default()(_vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_0__["default"].colors.purple['500']).fade(0.9),
        color: _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_0__["default"].colors.purple['500'],
    },
];
const aioTableData = [
    {
        id: 1,
        url: 'https://scenario.io/users',
        endpoint: '/users',
        components: [aioTableLabels[0], aioTableLabels[1], aioTableLabels[2], aioTableLabels[3]],
        position: 1,
    },
    {
        id: 2,
        url: 'https://scenario.io/users/1',
        endpoint: '/users/{:user_id}',
        components: [aioTableLabels[0], aioTableLabels[2], aioTableLabels[3]],
        position: 2,
    },
];
// export const aioTableData = [
//   {
//     id: 0,
//     imageSrc: 'assets/img/avatars/20.jpg',
//     firstName: 'Dejesus',
//     lastName: 'Chang',
//     street: '899 Raleigh Place',
//     zipcode: 8057,
//     city: 'Munjor',
//     phoneNumber: '+32 (818) 580-3557',
//     mail: 'dejesus.chang@yourcompany.biz',
//     labels: [aioTableLabels[0], aioTableLabels[1]]
//   },
//   {
//     id: 1,
//     imageSrc: 'assets/img/avatars/1.jpg',
//     firstName: 'Short',
//     lastName: 'Lowe',
//     street: '548 Cypress Avenue',
//     zipcode: 5943,
//     city: 'Temperanceville',
//     phoneNumber: '+11 (977) 574-3636',
//     mail: 'short.lowe@yourcompany.ca',
//     labels: [aioTableLabels[1]]
//   },
//   {
//     id: 2,
//     imageSrc: 'assets/img/avatars/2.jpg',
//     firstName: 'Antoinette',
//     lastName: 'Carson',
//     street: '299 Roder Avenue',
//     zipcode: 7894,
//     city: 'Crayne',
//     phoneNumber: '+49 (969) 505-3323',
//     mail: 'antoinette.carson@yourcompany.net',
//     labels: [aioTableLabels[3]]
//   },
//   {
//     id: 3,
//     imageSrc: 'assets/img/avatars/3.jpg',
//     firstName: 'Lynnette',
//     lastName: 'Adkins',
//     street: '158 Cyrus Avenue',
//     zipcode: 4831,
//     city: 'Coyote',
//     phoneNumber: '+48 (836) 545-3237',
//     mail: 'lynnette.adkins@yourcompany.info',
//     labels: [aioTableLabels[3]]
//   },
//   {
//     id: 4,
//     imageSrc: 'assets/img/avatars/4.jpg',
//     firstName: 'Patrica',
//     lastName: 'Good',
//     street: '995 Kansas Place',
//     zipcode: 4679,
//     city: 'Whitmer',
//     phoneNumber: '+36 (955) 485-3652',
//     mail: 'patrica.good@yourcompany.me',
//     labels: [aioTableLabels[0]]
//   },
//   {
//     id: 5,
//     imageSrc: 'assets/img/avatars/5.jpg',
//     firstName: 'Kane',
//     lastName: 'Koch',
//     street: '779 Lynch Street',
//     zipcode: 6178,
//     city: 'Newcastle',
//     phoneNumber: '+35 (983) 587-3423',
//     mail: 'kane.koch@yourcompany.org',
//     labels: [aioTableLabels[1]]
//   },
//   {
//     id: 6,
//     imageSrc: 'assets/img/avatars/6.jpg',
//     firstName: 'Donovan',
//     lastName: 'Gonzalez',
//     street: '781 Knickerbocker Avenue',
//     zipcode: 532,
//     city: 'Frizzleburg',
//     phoneNumber: '+47 (914) 469-3270',
//     mail: 'donovan.gonzalez@yourcompany.tv',
//     labels: [aioTableLabels[2]]
//   },
//   {
//     id: 7,
//     imageSrc: 'assets/img/avatars/7.jpg',
//     firstName: 'Sabrina',
//     lastName: 'Logan',
//     street: '112 Glen Street',
//     zipcode: 4763,
//     city: 'Frystown',
//     phoneNumber: '+37 (896) 474-3143',
//     mail: 'sabrina.logan@yourcompany.co.uk',
//     labels: [aioTableLabels[0], aioTableLabels[1]]
//   },
//   {
//     id: 8,
//     imageSrc: 'assets/img/avatars/8.jpg',
//     firstName: 'Estela',
//     lastName: 'Jordan',
//     street: '626 Stryker Court',
//     zipcode: 9966,
//     city: 'Blende',
//     phoneNumber: '+2 (993) 445-3626',
//     mail: 'estela.jordan@yourcompany.name',
//     labels: [aioTableLabels[0]]
//   },
//   {
//     id: 9,
//     imageSrc: 'assets/img/avatars/9.jpg',
//     firstName: 'Rosanna',
//     lastName: 'Cross',
//     street: '540 Fiske Place',
//     zipcode: 4204,
//     city: 'Bellfountain',
//     phoneNumber: '+12 (877) 563-2737',
//     mail: 'rosanna.cross@yourcompany.biz',
//     labels: [aioTableLabels[2]]
//   },
//   {
//     id: 10,
//     imageSrc: 'assets/img/avatars/10.jpg',
//     firstName: 'Mary',
//     lastName: 'Jane',
//     street: '233 Glen Place',
//     zipcode: 4221,
//     city: 'Louisville',
//     phoneNumber: '+15 (877) 334-2231',
//     mail: 'Mary.jane@yourcompany.biz',
//     labels: [aioTableLabels[1]]
//   },
//   {
//     id: 11,
//     imageSrc: 'assets/img/avatars/11.jpg',
//     firstName: 'Lane',
//     lastName: 'Delaney',
//     street: 'Langham Street',
//     zipcode: 6411,
//     city: 'Avoca',
//     phoneNumber: '+1 (969) 570-2843',
//     mail: 'lane.delaney@yourcompany.ca',
//     labels: [aioTableLabels[3]]
//   },
//   {
//     id: 12,
//     imageSrc: 'assets/img/avatars/12.jpg',
//     firstName: 'Cooper',
//     lastName: 'Odom',
//     street: 'Shale Street',
//     zipcode: 5286,
//     city: 'Joes',
//     phoneNumber: '+1 (812) 535-2368',
//     mail: 'cooper.odom@yourcompany.info',
//     labels: [aioTableLabels[3]]
//   },
//   {
//     id: 13,
//     imageSrc: 'assets/img/avatars/13.jpg',
//     firstName: 'Kirby',
//     lastName: 'Hardin',
//     street: 'Rodney Street',
//     zipcode: 4864,
//     city: 'Finzel',
//     phoneNumber: '+1 (838) 519-3416',
//     mail: 'kirby.hardin@yourcompany.us',
//     labels: [aioTableLabels[3]]
//   },
//   {
//     id: 14,
//     imageSrc: 'assets/img/avatars/14.jpg',
//     firstName: 'Marquita',
//     lastName: 'Haynes',
//     street: 'Townsend Street',
//     zipcode: 9000,
//     city: 'Walland',
//     phoneNumber: '+1 (965) 482-2100',
//     mail: 'marquita.haynes@yourcompany.me',
//     labels: [aioTableLabels[2]]
//   },
//   {
//     id: 15,
//     imageSrc: 'assets/img/avatars/15.jpg',
//     firstName: 'Horton',
//     lastName: 'Townsend',
//     street: 'Gunnison Court',
//     zipcode: 9519,
//     city: 'Nettie',
//     phoneNumber: '+1 (941) 434-2481',
//     mail: 'horton.townsend@yourcompany.biz',
//     labels: [aioTableLabels[0]]
//   },
//   {
//     id: 16,
//     imageSrc: 'assets/img/avatars/16.jpg',
//     firstName: 'Carrie',
//     lastName: 'Bond',
//     street: 'Bushwick Court',
//     zipcode: 4345,
//     city: 'Colton',
//     phoneNumber: '+1 (854) 556-2844',
//     mail: 'carrie.bond@yourcompany.biz',
//     labels: [aioTableLabels[0]]
//   },
//   {
//     id: 17,
//     imageSrc: 'assets/img/avatars/17.jpg',
//     firstName: 'Carroll',
//     lastName: 'Pugh',
//     street: 'Baltic Street',
//     zipcode: 8174,
//     city: 'Innsbrook',
//     phoneNumber: '+1 (989) 561-2440',
//     mail: 'carroll.pugh@yourcompany.tv',
//     labels: [aioTableLabels[0]]
//   },
//   {
//     id: 18,
//     imageSrc: 'assets/img/avatars/18.jpg',
//     firstName: 'Fuller',
//     lastName: 'Espinoza',
//     street: 'Dooley Street',
//     zipcode: 9034,
//     city: 'Maybell',
//     phoneNumber: '+1 (807) 417-3508',
//     mail: 'fuller.espinoza@yourcompany.name',
//     labels: [aioTableLabels[1]]
//   },
//   {
//     id: 19,
//     imageSrc: 'assets/img/avatars/19.jpg',
//     firstName: 'Lamb',
//     lastName: 'Herring',
//     street: 'Exeter Street',
//     zipcode: 2246,
//     city: 'Fowlerville',
//     phoneNumber: '+1 (950) 429-3240',
//     mail: 'lamb.herring@yourcompany.com',
//     labels: [aioTableLabels[2]]
//   },
//   {
//     id: 20,
//     imageSrc: 'assets/img/avatars/20.jpg',
//     firstName: 'Liza',
//     lastName: 'Price',
//     street: 'Homecrest Avenue',
//     zipcode: 8843,
//     city: 'Idledale',
//     phoneNumber: '+1 (989) 483-2305',
//     mail: 'liza.price@yourcompany.net',
//     labels: [aioTableLabels[1]]
//   },
//   {
//     id: 21,
//     imageSrc: 'assets/img/avatars/1.jpg',
//     firstName: 'Monroe',
//     lastName: 'Head',
//     street: 'Arlington Avenue',
//     zipcode: 2792,
//     city: 'Garberville',
//     phoneNumber: '+1 (921) 598-2475',
//     mail: 'monroe.head@yourcompany.io',
//     labels: [aioTableLabels[1]]
//   },
//   {
//     id: 22,
//     imageSrc: 'assets/img/avatars/2.jpg',
//     firstName: 'Lucile',
//     lastName: 'Harding',
//     street: 'Division Place',
//     zipcode: 8572,
//     city: 'Celeryville',
//     phoneNumber: '+1 (823) 429-3500',
//     mail: 'lucile.harding@yourcompany.org',
//     labels: [aioTableLabels[0]]
//   },
//   {
//     id: 23,
//     imageSrc: 'assets/img/avatars/3.jpg',
//     firstName: 'Edna',
//     lastName: 'Richard',
//     street: 'Harbor Lane',
//     zipcode: 8323,
//     city: 'Lindisfarne',
//     phoneNumber: '+1 (970) 580-3162',
//     mail: 'edna.richard@yourcompany.ca',
//     labels: [aioTableLabels[0]]
//   },
//   {
//     id: 24,
//     imageSrc: 'assets/img/avatars/4.jpg',
//     firstName: 'Avila',
//     lastName: 'Lancaster',
//     street: 'Kay Court',
//     zipcode: 9294,
//     city: 'Welch',
//     phoneNumber: '+1 (817) 412-3752',
//     mail: 'avila.lancaster@yourcompany.info',
//     labels: [aioTableLabels[0]]
//   },
//   {
//     id: 25,
//     imageSrc: 'assets/img/avatars/5.jpg',
//     firstName: 'Carlene',
//     lastName: 'Newman',
//     street: 'Atlantic Avenue',
//     zipcode: 2230,
//     city: 'Eagleville',
//     phoneNumber: '+1 (953) 483-3110',
//     mail: 'carlene.newman@yourcompany.us',
//     labels: [aioTableLabels[3]]
//   },
//   {
//     id: 26,
//     imageSrc: 'assets/img/avatars/6.jpg',
//     firstName: 'Griffith',
//     lastName: 'Wise',
//     street: 'Perry Terrace',
//     zipcode: 9564,
//     city: 'Iola',
//     phoneNumber: '+1 (992) 447-3392',
//     mail: 'griffith.wise@yourcompany.me',
//     labels: [aioTableLabels[0]]
//   },
//   {
//     id: 27,
//     imageSrc: 'assets/img/avatars/7.jpg',
//     firstName: 'Schwartz',
//     lastName: 'Dodson',
//     street: 'Dorset Street',
//     zipcode: 4425,
//     city: 'Dexter',
//     phoneNumber: '+1 (923) 504-2799',
//     mail: 'schwartz.dodson@yourcompany.biz',
//     labels: [aioTableLabels[1]]
//   },
//   {
//     id: 28,
//     imageSrc: 'assets/img/avatars/8.jpg',
//     firstName: 'Susanna',
//     lastName: 'Kidd',
//     street: 'Loring Avenue',
//     zipcode: 6432,
//     city: 'Cascades',
//     phoneNumber: '+1 (854) 456-2734',
//     mail: 'susanna.kidd@yourcompany.biz',
//     labels: [aioTableLabels[1]]
//   },
//   {
//     id: 29,
//     imageSrc: 'assets/img/avatars/9.jpg',
//     firstName: 'Deborah',
//     lastName: 'Weiss',
//     street: 'Haring Street',
//     zipcode: 2989,
//     city: 'Barstow',
//     phoneNumber: '+1 (833) 465-3036',
//     mail: 'deborah.weiss@yourcompany.tv',
//     labels: [aioTableLabels[2]]
//   }
// ];


/***/ }),

/***/ "T4Vo":
/*!********************************************************************************************************!*\
  !*** ./src/app/modules/projects/pages/projects-index/components/projects-card/projects-card.module.ts ***!
  \********************************************************************************************************/
/*! exports provided: ProjectsCardModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectsCardModule", function() { return ProjectsCardModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_material_core__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/core */ "UhP/");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var ngx_avatar__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ngx-avatar */ "UTQ3");
/* harmony import */ var _projects_card_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./projects-card.component */ "ffwo");










let ProjectsCardModule = class ProjectsCardModule {
};
ProjectsCardModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_projects_card_component__WEBPACK_IMPORTED_MODULE_9__["ProjectsCardComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_7__["IconModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_4__["MatButtonModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_6__["MatIconModule"],
            _angular_material_core__WEBPACK_IMPORTED_MODULE_5__["MatRippleModule"],
            ngx_avatar__WEBPACK_IMPORTED_MODULE_8__["AvatarModule"],
        ],
        exports: [_projects_card_component__WEBPACK_IMPORTED_MODULE_9__["ProjectsCardComponent"]],
    })
], ProjectsCardModule);



/***/ }),

/***/ "TJ7c":
/*!********************************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/projects/pages/project-details/components/project-members/project-members.component.html ***!
  \********************************************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<vex-page-layout>\r\n\r\n  <!-- <vex-page-layout-header class=\"pb-16\" fxLayout=\"column\" fxLayoutAlign=\"center start\">\r\n    <div [class.container]=\"layoutCtrl.value === 'boxed'\"\r\n         [class.px-gutter]=\"layoutCtrl.value === 'fullwidth'\"\r\n         class=\"w-full flex flex-col sm:flex-row justify-between\">\r\n      <div>\r\n        <h1 class=\"title mt-0 mb-1\">All Members</h1>\r\n        <vex-breadcrumbs [crumbs]=\"crumbs\"></vex-breadcrumbs>\r\n      </div>\r\n    </div>\r\n  </vex-page-layout-header> -->\r\n\r\n  <div\r\n    [class.px-gutter]=\"layoutCtrl.value === 'fullwidth'\"\r\n    class=\"mt-5 table-container\">\r\n\r\n    <div class=\"card overflow-auto\">\r\n      <div class=\"bg-app-bar px-6 h-16 border-b sticky left-0\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\r\n        <h2 class=\"title my-0 ltr:pr-4 rtl:pl-4 ltr:mr-4 rtl:ml-4 ltr:border-r rtl:border-l\" fxFlex=\"none\" fxHide.xs>\r\n          <span *ngIf=\"selection.isEmpty()\">Members</span>\r\n          <span *ngIf=\"selection.hasValue()\">{{ selection.selected.length }}\r\n            member<span *ngIf=\"selection.selected.length > 1\">s</span> selected</span>\r\n        </h2>\r\n\r\n        <div *ngIf=\"selection.hasValue()\" class=\"mr-4 pr-4 border-r\" fxFlex=\"none\">\r\n          <button (click)=\"destroyProjectsUsers(selection.selected)\"\r\n                  color=\"primary\"\r\n                  mat-icon-button\r\n                  matTooltip=\"Remove selected\"\r\n                  type=\"button\">\r\n            <mat-icon [icIcon]=\"icons.icDelete\"></mat-icon>\r\n          </button>\r\n\r\n          <!-- <button color=\"primary\" mat-icon-button matTooltip=\"Another action\" type=\"button\">\r\n            <mat-icon [icIcon]=\"icFolder\"></mat-icon>\r\n          </button> -->\r\n        </div>\r\n\r\n        <div class=\"bg-card rounded-full border px-4\"\r\n             fxFlex=\"400px\"\r\n             fxFlex.lt-md=\"auto\"\r\n             fxHide.xs\r\n             fxLayout=\"row\"\r\n             fxLayoutAlign=\"start center\">\r\n          <ic-icon [icIcon]=\"icons.icSearch\" size=\"20px\"></ic-icon>\r\n          <input [formControl]=\"searchCtrl\"\r\n                 class=\"px-4 py-3 border-0 outline-none w-full bg-transparent\"\r\n                 placeholder=\"Search...\"\r\n                 type=\"search\">\r\n        </div>\r\n\r\n        <span fxFlex></span>\r\n\r\n        <button class=\"ml-4\" fxFlex=\"none\" fxHide.gt-xs mat-icon-button type=\"button\">\r\n          <mat-icon [icIcon]=\"icons.icSearch\"></mat-icon>\r\n        </button>\r\n\r\n        <button [matMenuTriggerFor]=\"columnFilterMenu\"\r\n                class=\"ml-4\"\r\n                fxFlex=\"none\"\r\n                mat-icon-button\r\n                matTooltip=\"Filter Columns\"\r\n                type=\"button\">\r\n          <mat-icon [icIcon]=\"icons.icFilterList\"></mat-icon>\r\n        </button>\r\n\r\n        <button (click)=\"openCreateDialog()\"\r\n                class=\"ml-4\"\r\n                color=\"primary\"\r\n                fxFlex=\"none\"\r\n                mat-mini-fab\r\n                matTooltip=\"Create Member\"\r\n                type=\"button\">\r\n          <mat-icon [icIcon]=\"icons.icAdd\"></mat-icon>\r\n        </button>\r\n      </div>\r\n\r\n      <table @stagger [dataSource]=\"dataSource\" class=\"w-full\" mat-table matSort>\r\n\r\n        <!--- Note that these columns can be defined in any order.\r\n              The actual rendered columns are set as a property on the row definition\" -->\r\n\r\n        <!-- Checkbox Column -->\r\n        <ng-container matColumnDef=\"checkbox\">\r\n          <th *matHeaderCellDef mat-header-cell>\r\n            <mat-checkbox (change)=\"$event ? masterToggle() : null\"\r\n                          [checked]=\"selection.hasValue() && isAllSelected()\"\r\n                          [indeterminate]=\"selection.hasValue() && !isAllSelected()\"\r\n                          color=\"primary\">\r\n            </mat-checkbox>\r\n          </th>\r\n          <td *matCellDef=\"let row\" class=\"w-4\" mat-cell>\r\n            <mat-checkbox (change)=\"$event ? selection.toggle(row) : null\"\r\n                          (click)=\"$event.stopPropagation()\"\r\n                          [checked]=\"selection.isSelected(row)\"\r\n                          color=\"primary\">\r\n            </mat-checkbox>\r\n          </td>\r\n        </ng-container>\r\n\r\n        <!-- Image Column -->\r\n        <ng-container matColumnDef=\"image\">\r\n          <th *matHeaderCellDef mat-header-cell></th>\r\n          <td *matCellDef=\"let row\" class=\"w-8 min-w-8 pr-0\" mat-cell>\r\n            <img [src]=\"row['imageSrc']\" class=\"avatar h-8 w-8 align-middle\">\r\n          </td>\r\n        </ng-container>\r\n\r\n        <!-- Text Columns -->\r\n        <ng-container *ngFor=\"let column of columns; trackBy: trackByProperty\">\r\n          <ng-container *ngIf=\"column.type === 'text'\" [matColumnDef]=\"column.property\">\r\n            <th *matHeaderCellDef class=\"uppercase\" mat-header-cell mat-sort-header> {{ column.label }}</th>\r\n            <td *matCellDef=\"let row\" [ngClass]=\"column.cssClasses\" mat-cell>{{ row[column.property] }}</td>\r\n          </ng-container>\r\n        </ng-container>\r\n\r\n        <!-- Date Columns -->\r\n        <ng-container *ngFor=\"let column of columns; trackBy: trackByProperty\">\r\n          <ng-container *ngIf=\"column.type === 'date'\" [matColumnDef]=\"column.property\">\r\n            <th *matHeaderCellDef class=\"uppercase\" mat-header-cell mat-sort-header> {{ column.label }}</th>\r\n            <td *matCellDef=\"let row\" [ngClass]=\"column.cssClasses\" mat-cell>{{ row[column.property] | date }}</td>\r\n          </ng-container>\r\n        </ng-container>\r\n\r\n        <!-- Role Column -->\r\n        <ng-container matColumnDef=\"role\">\r\n          <th *matHeaderCellDef class=\"uppercase\" mat-header-cell mat-sort-header>Role</th>\r\n          <td *matCellDef=\"let row\" mat-cell>\r\n            <button\r\n              color=\"primary\"\r\n              mat-flat-button\r\n              [matMenuTriggerFor]=\"categoryMenu\"\r\n              (click)=\"$event.stopPropagation()\"\r\n              [matMenuTriggerData]=\"{ member: row }\">\r\n              {{ roleData.getRoleTitle(row.role) }}\r\n            </button>\r\n          </td>\r\n        </ng-container>\r\n\r\n        <!-- Action Column -->\r\n        <ng-container matColumnDef=\"actions\">\r\n          <th *matHeaderCellDef mat-header-cell mat-sort-header></th>\r\n          <td *matCellDef=\"let row\" class=\"w-10 text-secondary\" mat-cell>\r\n            <button (click)=\"$event.stopPropagation()\"\r\n                    [matMenuTriggerData]=\"{ member: row }\"\r\n                    [matMenuTriggerFor]=\"actionsMenu\"\r\n                    mat-icon-button\r\n                    type=\"button\">\r\n              <mat-icon [icIcon]=\"icons.icMoreHoriz\"></mat-icon>\r\n            </button>\r\n          </td>\r\n        </ng-container>\r\n\r\n        <tr *matHeaderRowDef=\"visibleColumns\" mat-header-row></tr>\r\n        <tr (click)=\"showProjectsUser(row)\"\r\n            *matRowDef=\"let row; columns: visibleColumns;\"\r\n            @fadeInUp\r\n            class=\"hover:bg-hover trans-ease-out cursor-pointer\"\r\n            mat-row></tr>\r\n      </table>\r\n\r\n      <mat-paginator\r\n        [pageSizeOptions]=\"pageSizeOptions\"\r\n        [pageSize]=\"pageSize\"\r\n        [pageIndex]=\"pageIndex\"\r\n        (page)=\"onPaginateChange($event)\"\r\n        class=\"sticky left-0\">\r\n      </mat-paginator>\r\n    </div>\r\n\r\n  </div>\r\n\r\n</vex-page-layout>\r\n\r\n<mat-menu #columnFilterMenu=\"matMenu\" xPosition=\"before\" yPosition=\"below\">\r\n  <button (click)=\"toggleColumnVisibility(column, $event)\" *ngFor=\"let column of columns\"\r\n          class=\"checkbox-item mat-menu-item\">\r\n    <mat-checkbox (click)=\"$event.stopPropagation()\" [(ngModel)]=\"column.visible\" color=\"primary\">\r\n      {{ column.label }}\r\n    </mat-checkbox>\r\n  </button>\r\n</mat-menu>\r\n\r\n<mat-menu #actionsMenu=\"matMenu\" xPosition=\"before\" yPosition=\"below\">\r\n  <ng-template let-member=\"member\" matMenuContent>\r\n    <button (click)=\"destroyProjectsUser(member)\" mat-menu-item>\r\n      <mat-icon [icIcon]=\"icons.icDelete\"></mat-icon>\r\n      <span>Delete</span>\r\n    </button>\r\n  </ng-template>\r\n</mat-menu>\r\n\r\n<mat-menu #categoryMenu=\"matMenu\" xPosition=\"after\" yPosition=\"below\">\r\n  <ng-template let-member=\"member\" matMenuContent>\r\n    <button mat-menu-item\r\n      *ngFor=\"let name of roleData.roleTitles\"\r\n      (click)=\"updateProjectsUser(member, {role: roleData.titleRolesMap[name] })\">\r\n      {{ name  }}\r\n    </button>\r\n  </ng-template>\r\n</mat-menu>\r\n");

/***/ }),

/***/ "VKCF":
/*!************************************************************************************************!*\
  !*** ./src/app/modules/projects/pages/projects-index/services/projects-index-icons.service.ts ***!
  \************************************************************************************************/
/*! exports provided: ProjectsIndexIcons */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectsIndexIcons", function() { return ProjectsIndexIcons; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @iconify/icons-ic/twotone-add */ "7wwx");
/* harmony import */ var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _iconify_icons_ic_twotone_arrow_drop_down__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @iconify/icons-ic/twotone-arrow-drop-down */ "LgSP");
/* harmony import */ var _iconify_icons_ic_twotone_arrow_drop_down__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_arrow_drop_down__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @iconify/icons-ic/twotone-cloud-download */ "MzEE");
/* harmony import */ var _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _iconify_icons_ic_twotone_collections__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @iconify/icons-ic/twotone-collections */ "baq9");
/* harmony import */ var _iconify_icons_ic_twotone_collections__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_collections__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _iconify_icons_ic_twotone_filter_list__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @iconify/icons-ic/twotone-filter-list */ "+4LO");
/* harmony import */ var _iconify_icons_ic_twotone_filter_list__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_filter_list__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _iconify_icons_ic_twotone_people__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @iconify/icons-ic/twotone-people */ "rwX0");
/* harmony import */ var _iconify_icons_ic_twotone_people__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_people__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @iconify/icons-ic/twotone-search */ "sF+I");
/* harmony import */ var _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _iconify_icons_ic_twotone_settings__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @iconify/icons-ic/twotone-settings */ "hF2C");
/* harmony import */ var _iconify_icons_ic_twotone_settings__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_settings__WEBPACK_IMPORTED_MODULE_9__);










let ProjectsIndexIcons = class ProjectsIndexIcons {
    constructor() {
        this.icSearch = _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_8___default.a;
        this.icCloudDownload = _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_4___default.a;
        this.icFilterList = _iconify_icons_ic_twotone_filter_list__WEBPACK_IMPORTED_MODULE_6___default.a;
        this.icArrowDropDown = _iconify_icons_ic_twotone_arrow_drop_down__WEBPACK_IMPORTED_MODULE_3___default.a;
        this.icAdd = _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_2___default.a;
        this.icPeople = _iconify_icons_ic_twotone_people__WEBPACK_IMPORTED_MODULE_7___default.a;
        this.icCollections = _iconify_icons_ic_twotone_collections__WEBPACK_IMPORTED_MODULE_5___default.a;
        this.icSettings = _iconify_icons_ic_twotone_settings__WEBPACK_IMPORTED_MODULE_9___default.a;
    }
};
ProjectsIndexIcons.ctorParameters = () => [];
ProjectsIndexIcons = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], ProjectsIndexIcons);



/***/ }),

/***/ "Wti8":
/*!*****************************************************************************************************************************!*\
  !*** ./src/app/modules/projects/pages/project-details/components/project-members/services/project-members-icons.service.ts ***!
  \*****************************************************************************************************************************/
/*! exports provided: ProjectMembersIcons */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectMembersIcons", function() { return ProjectMembersIcons; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @iconify/icons-ic/twotone-add */ "7wwx");
/* harmony import */ var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @iconify/icons-ic/twotone-delete */ "e3EN");
/* harmony import */ var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _iconify_icons_ic_twotone_filter_list__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @iconify/icons-ic/twotone-filter-list */ "+4LO");
/* harmony import */ var _iconify_icons_ic_twotone_filter_list__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_filter_list__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @iconify/icons-ic/twotone-search */ "sF+I");
/* harmony import */ var _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_5__);






let ProjectMembersIcons = class ProjectMembersIcons {
    constructor() {
        this.icSearch = _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_5___default.a;
        this.icDelete = _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_3___default.a;
        this.icAdd = _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_2___default.a;
        this.icFilterList = _iconify_icons_ic_twotone_filter_list__WEBPACK_IMPORTED_MODULE_4___default.a;
    }
};
ProjectMembersIcons.ctorParameters = () => [];
ProjectMembersIcons = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])()
], ProjectMembersIcons);



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

/***/ "Z9mU":
/*!*************************************************************************************************************!*\
  !*** ./src/app/modules/projects/pages/project-details/components/project-members/project-members.module.ts ***!
  \*************************************************************************************************************/
/*! exports provided: ProjectMembersModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectMembersModule", function() { return ProjectMembersModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ "s7LF");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_material_button_toggle__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/button-toggle */ "Ynp+");
/* harmony import */ var _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/checkbox */ "pMoy");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _angular_material_menu__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/material/menu */ "rJgo");
/* harmony import */ var _angular_material_paginator__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/material/paginator */ "5QHs");
/* harmony import */ var _angular_material_select__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @angular/material/select */ "ZTz/");
/* harmony import */ var _angular_material_sort__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @angular/material/sort */ "LUZP");
/* harmony import */ var _angular_material_table__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/material/table */ "OaSA");
/* harmony import */ var _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/material/tooltip */ "ZFy/");
/* harmony import */ var _vex_components_breadcrumbs_breadcrumbs_module__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @vex/components/breadcrumbs/breadcrumbs.module */ "J0XA");
/* harmony import */ var _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @vex/components/page-layout/page-layout.module */ "7lCJ");
/* harmony import */ var _vex_directives_container_container_module__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @vex/directives/container/container.module */ "68Yx");
/* harmony import */ var _vex_pipes_color_color_fade_module__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @vex/pipes/color/color-fade.module */ "Chvm");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _components_project_members_create_project_members_create_module__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! ./components/project-members-create/project-members-create.module */ "2/D2");
/* harmony import */ var _project_members_component__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! ./project-members.component */ "8kLj");
/* harmony import */ var _shared_shared_module__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! @shared/shared.module */ "PCNd");
/* harmony import */ var _services_project_members_icons_service__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! ./services/project-members-icons.service */ "Wti8");
























let ProjectMembersModule = class ProjectMembersModule {
};
ProjectMembersModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_project_members_component__WEBPACK_IMPORTED_MODULE_21__["ProjectMembersComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_16__["PageLayoutModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _vex_components_breadcrumbs_breadcrumbs_module__WEBPACK_IMPORTED_MODULE_15__["BreadcrumbsModule"],
            _components_project_members_create_project_members_create_module__WEBPACK_IMPORTED_MODULE_20__["ProjectMembersCreateModule"],
            _angular_material_paginator__WEBPACK_IMPORTED_MODULE_10__["MatPaginatorModule"],
            _angular_material_table__WEBPACK_IMPORTED_MODULE_13__["MatTableModule"],
            _angular_material_sort__WEBPACK_IMPORTED_MODULE_12__["MatSortModule"],
            _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_7__["MatCheckboxModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_8__["MatIconModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_5__["MatButtonModule"],
            _angular_material_menu__WEBPACK_IMPORTED_MODULE_9__["MatMenuModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_19__["IconModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormsModule"],
            _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_14__["MatTooltipModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"],
            _vex_directives_container_container_module__WEBPACK_IMPORTED_MODULE_17__["ContainerModule"],
            _angular_material_select__WEBPACK_IMPORTED_MODULE_11__["MatSelectModule"],
            _vex_pipes_color_color_fade_module__WEBPACK_IMPORTED_MODULE_18__["ColorFadeModule"],
            _angular_material_button_toggle__WEBPACK_IMPORTED_MODULE_6__["MatButtonToggleModule"],
            _shared_shared_module__WEBPACK_IMPORTED_MODULE_22__["SharedModule"],
        ],
        providers: [_services_project_members_icons_service__WEBPACK_IMPORTED_MODULE_23__["ProjectMembersIcons"]],
    })
], ProjectMembersModule);



/***/ }),

/***/ "aKIO":
/*!******************************************************************************************************************!*\
  !*** ./src/app/modules/projects/pages/project-details/components/project-members/project-members.component.scss ***!
  \******************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (".table-container {\n  box-sizing: border-box;\n  display: block;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uLy4uLy4uLy4uL3Byb2plY3QtbWVtYmVycy5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLHNCQUFBO0VBQ0EsY0FBQTtBQUNGIiwiZmlsZSI6InByb2plY3QtbWVtYmVycy5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbIi50YWJsZS1jb250YWluZXIge1xuICBib3gtc2l6aW5nOiBib3JkZXItYm94O1xuICBkaXNwbGF5OiBibG9jaztcbn0iXX0= */");

/***/ }),

/***/ "bE8U":
/*!********************************************************!*\
  !*** ./node_modules/@iconify/icons-ic/twotone-star.js ***!
  \********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

var data = {
	"body": "<path opacity=\".3\" d=\"M12 15.4l-3.76 2.27l1-4.28l-3.32-2.88l4.38-.38L12 6.1l1.71 4.04l4.38.38l-3.32 2.88l1 4.28z\" fill=\"currentColor\"/><path d=\"M22 9.24l-7.19-.62L12 2L9.19 8.63L2 9.24l5.46 4.73L5.82 21L12 17.27L18.18 21l-1.63-7.03L22 9.24zM12 15.4l-3.76 2.27l1-4.28l-3.32-2.88l4.38-.38L12 6.1l1.71 4.04l4.38.38l-3.32 2.88l1 4.28L12 15.4z\" fill=\"currentColor\"/>",
	"width": 24,
	"height": 24
};
exports.__esModule = true;
exports.default = data;


/***/ }),

/***/ "baq9":
/*!***************************************************************!*\
  !*** ./node_modules/@iconify/icons-ic/twotone-collections.js ***!
  \***************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

var data = {
	"body": "<path opacity=\".3\" d=\"M8 16h12V4H8v12zm3.5-4.33l1.69 2.26l2.48-3.09L19 15H9l2.5-3.33z\" fill=\"currentColor\"/><path d=\"M8 2c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2H8zm12 14H8V4h12v12zm-4.33-5.17l-2.48 3.09l-1.69-2.25L9 15h10zM4 22h14v-2H4V6H2v14c0 1.1.9 2 2 2z\" fill=\"currentColor\"/>",
	"width": 24,
	"height": 24
};
exports.__esModule = true;
exports.default = data;


/***/ }),

/***/ "bx88":
/*!***************************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/projects/pages/projects-index/components/projects-card/projects-card.component.html ***!
  \***************************************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div class=\"card overflow-hidden\">\r\n  <div (click)=\"view.emit(project.id)\"\r\n       class=\"p-4 text-center hover:bg-hover trans-ease-out cursor-pointer relative\"\r\n       matRipple>\r\n    <div class=\"mx-auto h-24 w-24\">\r\n      <ngx-avatar\r\n        name=\"{{project.name}}\"\r\n        class=\"avatar\"\r\n        size=\"100\">\r\n      </ngx-avatar>\r\n    </div>\r\n\r\n    <h2 class=\"title mb-1 mt-3\">{{ project?.name }}</h2>\r\n    <div class=\"body-2 text-secondary\" [ngClass]=\"project.description ? '' : 'text-transparent'\">\r\n      <span>{{ project.description ? project.description : 'N/A' }}</span>\r\n    </div>\r\n\r\n    <button (click)=\"emitToggleStar($event, project?.id)\" class=\"absolute top-2 right-2\" mat-icon-button type=\"button\">\r\n      <mat-icon *ngIf=\"project?.starred\" [icIcon]=\"icStar\" class=\"text-amber-500\"></mat-icon>\r\n      <mat-icon *ngIf=\"!project?.starred\" [icIcon]=\"icStarBorder\"></mat-icon>\r\n    </button>\r\n  </div>\r\n\r\n  <div class=\"bg-app-bar p-2\" fxLayout=\"row\" fxLayoutAlign=\"space-around center\">\r\n    <button\r\n      class=\"text-secondary\"\r\n      mat-icon-button type=\"button\"\r\n      (click)=\"update.emit(project)\">\r\n      <mat-icon [icIcon]=\"icEdit\"></mat-icon>\r\n    </button>\r\n\r\n    <button\r\n      class=\"text-secondary\"\r\n      mat-icon-button type=\"button\"\r\n      (click)=\"members.emit(project.id)\">\r\n      <mat-icon [icIcon]=\"icPeople\"></mat-icon>\r\n    </button>\r\n\r\n    <button\r\n      class=\"text-secondary\"\r\n      mat-icon-button type=\"button\"\r\n      (click)=\"delete.emit(project.id)\">\r\n      <mat-icon [icIcon]=\"icDelete\"></mat-icon>\r\n    </button>\r\n  </div>\r\n</div>\r\n");

/***/ }),

/***/ "e/UG":
/*!****************************************************************************************************************************!*\
  !*** ./src/app/modules/projects/pages/project-details/components/project-members/services/project-members-data.service.ts ***!
  \****************************************************************************************************************************/
/*! exports provided: ProjectMembersDataService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectMembersDataService", function() { return ProjectMembersDataService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "qCKp");
/* harmony import */ var _data_schema_projects_user__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @data/schema/projects-user */ "D9MS");




let ProjectMembersDataService = class ProjectMembersDataService {
    constructor() {
        this.subject = new rxjs__WEBPACK_IMPORTED_MODULE_2__["BehaviorSubject"](null);
        this.members$ = this.subject.asObservable();
    }
    set(members) {
        this.members = members;
        this.subject.next(members);
    }
    add(member) {
        this.members.unshift(new _data_schema_projects_user__WEBPACK_IMPORTED_MODULE_3__["ProjectsUser"](member));
        this.set(this.members);
    }
    delete(id) {
        this.members.splice(this.members.findIndex((existingProjectsUser) => {
            return existingProjectsUser.id === id;
        }), 1);
        this.set(this.members);
    }
};
ProjectMembersDataService.ctorParameters = () => [];
ProjectMembersDataService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], ProjectMembersDataService);



/***/ }),

/***/ "ffwo":
/*!***********************************************************************************************************!*\
  !*** ./src/app/modules/projects/pages/projects-index/components/projects-card/projects-card.component.ts ***!
  \***********************************************************************************************************/
/*! exports provided: ProjectsCardComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectsCardComponent", function() { return ProjectsCardComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_projects_card_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./projects-card.component.html */ "bx88");
/* harmony import */ var _projects_card_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./projects-card.component.scss */ "nT6z");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _iconify_icons_ic_twotone_business__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @iconify/icons-ic/twotone-business */ "6uZp");
/* harmony import */ var _iconify_icons_ic_twotone_business__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_business__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _iconify_icons_ic_twotone_chat__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @iconify/icons-ic/twotone-chat */ "om0Q");
/* harmony import */ var _iconify_icons_ic_twotone_chat__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_chat__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @iconify/icons-ic/twotone-delete */ "e3EN");
/* harmony import */ var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @iconify/icons-ic/twotone-mail */ "6qw8");
/* harmony import */ var _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _iconify_icons_ic_twotone_people__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @iconify/icons-ic/twotone-people */ "rwX0");
/* harmony import */ var _iconify_icons_ic_twotone_people__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_people__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @iconify/icons-ic/twotone-phone */ "YA1h");
/* harmony import */ var _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @iconify/icons-ic/twotone-star */ "bE8U");
/* harmony import */ var _iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _iconify_icons_ic_twotone_star_border__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @iconify/icons-ic/twotone-star-border */ "PNSm");
/* harmony import */ var _iconify_icons_ic_twotone_star_border__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_star_border__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var _iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @iconify/icons-ic/twotone-edit */ "pN9m");
/* harmony import */ var _iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_12__);
/* harmony import */ var _iconify_icons_ic_twotone_link__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @iconify/icons-ic/twotone-link */ "h+Y6");
/* harmony import */ var _iconify_icons_ic_twotone_link__WEBPACK_IMPORTED_MODULE_13___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_link__WEBPACK_IMPORTED_MODULE_13__);














let ProjectsCardComponent = class ProjectsCardComponent {
    constructor() {
        this.members = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
        this.toggleStar = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
        this.delete = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
        this.update = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
        this.view = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
        this.icBusiness = _iconify_icons_ic_twotone_business__WEBPACK_IMPORTED_MODULE_4___default.a;
        this.icPhone = _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_9___default.a;
        this.icMail = _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_7___default.a;
        this.icChat = _iconify_icons_ic_twotone_chat__WEBPACK_IMPORTED_MODULE_5___default.a;
        this.icStar = _iconify_icons_ic_twotone_star__WEBPACK_IMPORTED_MODULE_10___default.a;
        this.icStarBorder = _iconify_icons_ic_twotone_star_border__WEBPACK_IMPORTED_MODULE_11___default.a;
        this.icPeople = _iconify_icons_ic_twotone_people__WEBPACK_IMPORTED_MODULE_8___default.a;
        this.icEdit = _iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_12___default.a;
        this.icLink = _iconify_icons_ic_twotone_link__WEBPACK_IMPORTED_MODULE_13___default.a;
        this.icDelete = _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_6___default.a;
    }
    ngOnInit() {
    }
    emitToggleStar(event, projectId) {
        event.stopPropagation();
        this.toggleStar.emit(projectId);
    }
};
ProjectsCardComponent.ctorParameters = () => [];
ProjectsCardComponent.propDecorators = {
    project: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"] }],
    members: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Output"] }],
    toggleStar: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Output"] }],
    delete: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Output"] }],
    update: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Output"] }],
    view: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Output"] }]
};
ProjectsCardComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'projects-card',
        template: _raw_loader_projects_card_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_projects_card_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], ProjectsCardComponent);



/***/ }),

/***/ "gKTl":
/*!***************************************************************************************!*\
  !*** ./src/app/modules/projects/components/projects-create/projects-create.module.ts ***!
  \***************************************************************************************/
/*! exports provided: ProjectsCreateModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectsCreateModule", function() { return ProjectsCreateModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ "s7LF");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_material_core__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/core */ "UhP/");
/* harmony import */ var _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/datepicker */ "TN/R");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/material/dialog */ "iELJ");
/* harmony import */ var _angular_material_divider__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/material/divider */ "BSbQ");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @angular/material/input */ "e6WT");
/* harmony import */ var _angular_material_menu__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @angular/material/menu */ "rJgo");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _projects_create_component__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./projects-create.component */ "JUG8");















let ProjectsCreateModule = class ProjectsCreateModule {
};
ProjectsCreateModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_projects_create_component__WEBPACK_IMPORTED_MODULE_14__["ProjectsCreateComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_material_dialog__WEBPACK_IMPORTED_MODULE_8__["MatDialogModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_10__["MatIconModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _angular_material_input__WEBPACK_IMPORTED_MODULE_11__["MatInputModule"],
            _angular_material_divider__WEBPACK_IMPORTED_MODULE_9__["MatDividerModule"],
            _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_7__["MatDatepickerModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_13__["IconModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"],
            _angular_material_menu__WEBPACK_IMPORTED_MODULE_12__["MatMenuModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_5__["MatButtonModule"],
            _angular_material_core__WEBPACK_IMPORTED_MODULE_6__["MatNativeDateModule"],
        ],
        entryComponents: [_projects_create_component__WEBPACK_IMPORTED_MODULE_14__["ProjectsCreateComponent"]],
    })
], ProjectsCreateModule);



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

/***/ "l1Fo":
/*!*****************************************************!*\
  !*** ./src/app/modules/projects/projects.module.ts ***!
  \*****************************************************/
/*! exports provided: ProjectsModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectsModule", function() { return ProjectsModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _pages_project_details_project_details_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./pages/project-details/project-details.module */ "uhjP");
/* harmony import */ var _pages_projects_index_projects_index_module__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./pages/projects-index/projects-index.module */ "v8qk");
/* harmony import */ var _projects_routing_module__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./projects-routing.module */ "NihL");






let ProjectsModule = class ProjectsModule {
};
ProjectsModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _pages_projects_index_projects_index_module__WEBPACK_IMPORTED_MODULE_4__["ProjectsIndexModule"],
            _pages_project_details_project_details_module__WEBPACK_IMPORTED_MODULE_3__["ProjectDetailsModule"],
            _projects_routing_module__WEBPACK_IMPORTED_MODULE_5__["ProjectsRoutingModule"],
        ],
    })
], ProjectsModule);



/***/ }),

/***/ "nMgu":
/*!*******************************************************************************************************************************!*\
  !*** ./src/app/modules/projects/pages/project-details/components/project-members/services/projects-users-resolver.service.ts ***!
  \*******************************************************************************************************************************/
/*! exports provided: ProjectsUsersResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectsUsersResolver", function() { return ProjectsUsersResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _core_http_projects_user_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @core/http/projects-user-resource.service */ "XTWy");



let ProjectsUsersResolver = class ProjectsUsersResolver {
    constructor(projectsUserResource) {
        this.projectsUserResource = projectsUserResource;
    }
    resolve(route) {
        return this.projectsUserResource.index(route.parent.params.project_id);
    }
};
ProjectsUsersResolver.ctorParameters = () => [
    { type: _core_http_projects_user_resource_service__WEBPACK_IMPORTED_MODULE_2__["ProjectsUserResource"] }
];
ProjectsUsersResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], ProjectsUsersResolver);



/***/ }),

/***/ "nT6z":
/*!*************************************************************************************************************!*\
  !*** ./src/app/modules/projects/pages/projects-index/components/projects-card/projects-card.component.scss ***!
  \*************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJwcm9qZWN0cy1jYXJkLmNvbXBvbmVudC5zY3NzIn0= */");

/***/ }),

/***/ "om0Q":
/*!********************************************************!*\
  !*** ./node_modules/@iconify/icons-ic/twotone-chat.js ***!
  \********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

var data = {
	"body": "<path opacity=\".3\" d=\"M20 4H4v13.17L5.17 16H20V4zm-6 10H6v-2h8v2zm4-3H6V9h12v2zm0-3H6V6h12v2z\" fill=\"currentColor\"/><path d=\"M20 18c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14zm-16-.83V4h16v12H5.17L4 17.17zM6 12h8v2H6zm0-3h12v2H6zm0-3h12v2H6z\" fill=\"currentColor\"/>",
	"width": 24,
	"height": 24
};
exports.__esModule = true;
exports.default = data;


/***/ }),

/***/ "orsw":
/*!******************************************************************************************!*\
  !*** ./src/app/modules/projects/components/projects-update/projects-update.component.ts ***!
  \******************************************************************************************/
/*! exports provided: ProjectsUpdateComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectsUpdateComponent", function() { return ProjectsUpdateComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_projects_update_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./projects-update.component.html */ "71Jh");
/* harmony import */ var _projects_update_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./projects-update.component.scss */ "9+z0");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ "s7LF");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/dialog */ "iELJ");
/* harmony import */ var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @iconify/icons-ic/twotone-close */ "5mnX");
/* harmony import */ var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @iconify/icons-ic/twotone-delete */ "e3EN");
/* harmony import */ var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @iconify/icons-ic/twotone-mail */ "6qw8");
/* harmony import */ var _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @iconify/icons-ic/twotone-person */ "KaaH");
/* harmony import */ var _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_9__);










let ProjectsUpdateComponent = class ProjectsUpdateComponent {
    constructor(project, dialogRef, fb) {
        this.project = project;
        this.dialogRef = dialogRef;
        this.fb = fb;
        this.onUpdate = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
        this.form = this.fb.group({
            name: null,
            description: null,
        });
        this.icClose = _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_6___default.a;
        this.icDelete = _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_7___default.a;
        this.icPerson = _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_9___default.a;
        this.icEmail = _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_8___default.a;
    }
    ngOnInit() {
        this.form.patchValue(this.project || {});
    }
    save() {
        this.onUpdate.emit(this.form.value);
        this.dialogRef.close();
    }
};
ProjectsUpdateComponent.ctorParameters = () => [
    { type: undefined, decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Inject"], args: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MAT_DIALOG_DATA"],] }] },
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MatDialogRef"] },
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormBuilder"] }
];
ProjectsUpdateComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'projects-update',
        template: _raw_loader_projects_update_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_projects_update_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], ProjectsUpdateComponent);



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

/***/ "piVU":
/*!***************************************************************************************!*\
  !*** ./src/app/modules/projects/pages/project-details/project-details.component.scss ***!
  \***************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJwcm9qZWN0LWRldGFpbHMuY29tcG9uZW50LnNjc3MifQ== */");

/***/ }),

/***/ "rwX0":
/*!**********************************************************!*\
  !*** ./node_modules/@iconify/icons-ic/twotone-people.js ***!
  \**********************************************************/
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

/***/ "sGWm":
/*!********************************************************************************************!*\
  !*** ./src/app/modules/projects/components/projects-create/projects-create.component.scss ***!
  \********************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJwcm9qZWN0cy1jcmVhdGUuY29tcG9uZW50LnNjc3MifQ== */");

/***/ }),

/***/ "szr6":
/*!*************************************************************************************!*\
  !*** ./src/app/modules/projects/pages/projects-index/projects-index.component.scss ***!
  \*************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJwcm9qZWN0cy1pbmRleC5jb21wb25lbnQuc2NzcyJ9 */");

/***/ }),

/***/ "uhjP":
/*!**********************************************************************************!*\
  !*** ./src/app/modules/projects/pages/project-details/project-details.module.ts ***!
  \**********************************************************************************/
/*! exports provided: ProjectDetailsModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectDetailsModule", function() { return ProjectDetailsModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_material_core__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/core */ "UhP/");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _angular_material_tabs__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/tabs */ "M9ds");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @vex/components/page-layout/page-layout.module */ "7lCJ");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var ngx_avatar__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ngx-avatar */ "UTQ3");
/* harmony import */ var _components_project_members_project_members_module__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./components/project-members/project-members.module */ "Z9mU");
/* harmony import */ var _components_project_settings_project_settings_module__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./components/project-settings/project-settings.module */ "GVnh");
/* harmony import */ var _project_details_component__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./project-details.component */ "Iker");















let ProjectDetailsModule = class ProjectDetailsModule {
};
ProjectDetailsModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_project_details_component__WEBPACK_IMPORTED_MODULE_14__["ProjectDetailsComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_9__["PageLayoutModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _angular_material_tabs__WEBPACK_IMPORTED_MODULE_7__["MatTabsModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_10__["IconModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_4__["MatButtonModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_6__["MatIconModule"],
            _angular_material_core__WEBPACK_IMPORTED_MODULE_5__["MatRippleModule"],
            _angular_router__WEBPACK_IMPORTED_MODULE_8__["RouterModule"],
            ngx_avatar__WEBPACK_IMPORTED_MODULE_11__["AvatarModule"],
            _components_project_members_project_members_module__WEBPACK_IMPORTED_MODULE_12__["ProjectMembersModule"],
            _components_project_settings_project_settings_module__WEBPACK_IMPORTED_MODULE_13__["ProjectSettingsModule"],
        ],
    })
], ProjectDetailsModule);



/***/ }),

/***/ "v8qk":
/*!********************************************************************************!*\
  !*** ./src/app/modules/projects/pages/projects-index/projects-index.module.ts ***!
  \********************************************************************************/
/*! exports provided: ProjectsIndexModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectsIndexModule", function() { return ProjectsIndexModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/dialog */ "iELJ");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _angular_material_menu__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/menu */ "rJgo");
/* harmony import */ var _angular_material_tabs__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/material/tabs */ "M9ds");
/* harmony import */ var _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/material/tooltip */ "ZFy/");
/* harmony import */ var _vex_directives_container_container_module__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @vex/directives/container/container.module */ "68Yx");
/* harmony import */ var _vex_pipes_color_color_fade_module__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @vex/pipes/color/color-fade.module */ "Chvm");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _organizations_components_organizations_create_organizations_create_module__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @organizations/components/organizations-create/organizations-create.module */ "KUDd");
/* harmony import */ var _projects_components_projects_create_projects_create_module__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @projects/components/projects-create/projects-create.module */ "gKTl");
/* harmony import */ var _components_projects_card_projects_card_module__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ./components/projects-card/projects-card.module */ "T4Vo");
/* harmony import */ var _projects_index_component__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ./projects-index.component */ "Nt3V");

















let ProjectsIndexModule = class ProjectsIndexModule {
};
ProjectsIndexModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_projects_index_component__WEBPACK_IMPORTED_MODULE_16__["ProjectsIndexComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_material_tabs__WEBPACK_IMPORTED_MODULE_8__["MatTabsModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_4__["MatButtonModule"],
            _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MatDialogModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_6__["MatIconModule"],
            _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_9__["MatTooltipModule"],
            _angular_material_menu__WEBPACK_IMPORTED_MODULE_7__["MatMenuModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_12__["IconModule"],
            _vex_directives_container_container_module__WEBPACK_IMPORTED_MODULE_10__["ContainerModule"],
            _vex_pipes_color_color_fade_module__WEBPACK_IMPORTED_MODULE_11__["ColorFadeModule"],
            _components_projects_card_projects_card_module__WEBPACK_IMPORTED_MODULE_15__["ProjectsCardModule"],
            _organizations_components_organizations_create_organizations_create_module__WEBPACK_IMPORTED_MODULE_13__["OrganizationsCreateModule"],
            _projects_components_projects_create_projects_create_module__WEBPACK_IMPORTED_MODULE_14__["ProjectsCreateModule"],
        ],
    })
], ProjectsIndexModule);



/***/ }),

/***/ "vHR1":
/*!**********************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/projects/components/projects-create/projects-create.component.html ***!
  \**********************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<form (ngSubmit)=\"save()\" [formGroup]=\"form\">\r\n  <div fxLayout=\"row\" fxLayoutAlign=\"start center\" mat-dialog-title>\r\n    <h2 class=\"headline m-0\" fxFlex=\"auto\">{{ isUpdate ? 'Edit' : 'New' }} Project</h2>\r\n\r\n    <button class=\"text-secondary\" mat-dialog-close mat-icon-button type=\"button\">\r\n      <mat-icon [icIcon]=\"icClose\"></mat-icon>\r\n    </button>\r\n  </div>\r\n\r\n  <mat-divider class=\"-mx-6 text-border\"></mat-divider>\r\n\r\n  <mat-dialog-content fxLayout=\"column\">\r\n    <mat-form-field class=\"mt-6\">\r\n      <mat-label>Name</mat-label>\r\n      <input cdkFocusInitial formControlName=\"name\" matInput>\r\n\r\n      <mat-icon [icIcon]=\"icPerson\" class=\"ltr:mr-3 rtl:ml-3\" matPrefix></mat-icon>\r\n    </mat-form-field>\r\n\r\n    <mat-form-field>\r\n      <mat-label>Description</mat-label>\r\n      <textarea formControlName=\"description\" matInput></textarea>\r\n    </mat-form-field>\r\n  </mat-dialog-content>\r\n\r\n  <mat-dialog-actions align=\"end\">\r\n    <button mat-button mat-dialog-close type=\"button\">CANCEL</button>\r\n    <button color=\"primary\" mat-button type=\"submit\">{{ isUpdate ? 'UPDATE' : 'CREATE' }}</button>\r\n  </mat-dialog-actions>\r\n</form>\r\n");

/***/ }),

/***/ "w3PA":
/*!********************************************************************************************************************!*\
  !*** ./src/app/modules/projects/pages/project-details/components/project-settings/project-settings.component.scss ***!
  \********************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJwcm9qZWN0LXNldHRpbmdzLmNvbXBvbmVudC5zY3NzIn0= */");

/***/ }),

/***/ "zGPG":
/*!*******************************************************************************************************************************!*\
  !*** ./src/app/modules/projects/pages/project-details/components/project-settings/services/project-settings-icons.service.ts ***!
  \*******************************************************************************************************************************/
/*! exports provided: ProjectSettingsIcons */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ProjectSettingsIcons", function() { return ProjectSettingsIcons; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _iconify_icons_ic_twotone_access_time__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @iconify/icons-ic/twotone-access-time */ "NBim");
/* harmony import */ var _iconify_icons_ic_twotone_access_time__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_access_time__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @iconify/icons-ic/twotone-add */ "7wwx");
/* harmony import */ var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _iconify_icons_ic_twotone_check__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @iconify/icons-ic/twotone-check */ "+tDV");
/* harmony import */ var _iconify_icons_ic_twotone_check__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_check__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @iconify/icons-ic/twotone-edit */ "pN9m");
/* harmony import */ var _iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @iconify/icons-ic/twotone-mail */ "6qw8");
/* harmony import */ var _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _iconify_icons_ic_twotone_person_add__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @iconify/icons-ic/twotone-person-add */ "+q50");
/* harmony import */ var _iconify_icons_ic_twotone_person_add__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_person_add__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @iconify/icons-ic/twotone-phone */ "YA1h");
/* harmony import */ var _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _iconify_icons_ic_twotone_whatshot__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @iconify/icons-ic/twotone-whatshot */ "OcYv");
/* harmony import */ var _iconify_icons_ic_twotone_whatshot__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_whatshot__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _iconify_icons_ic_twotone_work__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @iconify/icons-ic/twotone-work */ "6W+F");
/* harmony import */ var _iconify_icons_ic_twotone_work__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_work__WEBPACK_IMPORTED_MODULE_10__);











let ProjectSettingsIcons = class ProjectSettingsIcons {
    constructor() {
        this.icWork = _iconify_icons_ic_twotone_work__WEBPACK_IMPORTED_MODULE_10___default.a;
        this.icPhone = _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_8___default.a;
        this.icPersonAdd = _iconify_icons_ic_twotone_person_add__WEBPACK_IMPORTED_MODULE_7___default.a;
        this.icCheck = _iconify_icons_ic_twotone_check__WEBPACK_IMPORTED_MODULE_4___default.a;
        this.icMail = _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_6___default.a;
        this.icAccessTime = _iconify_icons_ic_twotone_access_time__WEBPACK_IMPORTED_MODULE_2___default.a;
        this.icAdd = _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_3___default.a;
        this.icWhatshot = _iconify_icons_ic_twotone_whatshot__WEBPACK_IMPORTED_MODULE_9___default.a;
        this.icEdit = _iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_5___default.a;
    }
};
ProjectSettingsIcons.ctorParameters = () => [];
ProjectSettingsIcons = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], ProjectSettingsIcons);



/***/ })

}]);
//# sourceMappingURL=projects-projects-module-es2015.js.map