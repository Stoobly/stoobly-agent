(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["aliases-aliases-module"],{

/***/ "+OFh":
/*!*****************************************************************************!*\
  !*** ./src/app/modules/aliases/pages/alias-details/alias-details.module.ts ***!
  \*****************************************************************************/
/*! exports provided: AliasDetailsModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AliasDetailsModule", function() { return AliasDetailsModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/material/dialog */ "iELJ");
/* harmony import */ var _angular_material_tabs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/tabs */ "M9ds");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _vex_components_breadcrumbs_breadcrumbs_module__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @vex/components/breadcrumbs/breadcrumbs.module */ "J0XA");
/* harmony import */ var _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @vex/components/page-layout/page-layout.module */ "7lCJ");
/* harmony import */ var _vex_directives_container_container_module__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @vex/directives/container/container.module */ "68Yx");
/* harmony import */ var _alias_details_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./alias-details.component */ "jFjk");
/* harmony import */ var _components_alias_data_table_alias_data_table_module__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./components/alias-data-table/alias-data-table.module */ "F7bP");
/* harmony import */ var _components_alias_value_create_alias_value_create_module__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./components/alias-value-create/alias-value-create.module */ "XQjC");












let AliasDetailsModule = class AliasDetailsModule {
};
AliasDetailsModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_alias_details_component__WEBPACK_IMPORTED_MODULE_9__["AliasDetailsComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_material_dialog__WEBPACK_IMPORTED_MODULE_3__["MatDialogModule"],
            _angular_material_tabs__WEBPACK_IMPORTED_MODULE_4__["MatTabsModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_5__["IconModule"],
            _vex_components_breadcrumbs_breadcrumbs_module__WEBPACK_IMPORTED_MODULE_6__["BreadcrumbsModule"],
            _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_7__["PageLayoutModule"],
            _vex_directives_container_container_module__WEBPACK_IMPORTED_MODULE_8__["ContainerModule"],
            _components_alias_data_table_alias_data_table_module__WEBPACK_IMPORTED_MODULE_10__["AliasDataTableModule"],
            _components_alias_value_create_alias_value_create_module__WEBPACK_IMPORTED_MODULE_11__["AliasValueCreateModule"],
        ],
    })
], AliasDetailsModule);



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

/***/ "/ywk":
/*!***************************************************************************************************************!*\
  !*** ./src/app/modules/aliases/pages/alias-details/components/alias-data-table/alias-data-table.component.ts ***!
  \***************************************************************************************************************/
/*! exports provided: AliasDataTableComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AliasDataTableComponent", function() { return AliasDataTableComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_alias_data_table_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./alias-data-table.component.html */ "kdjS");
/* harmony import */ var _alias_data_table_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./alias-data-table.component.scss */ "Cr7o");
/* harmony import */ var _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/cdk/collections */ "CtHx");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_material_paginator__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/paginator */ "5QHs");
/* harmony import */ var _angular_material_sort__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/sort */ "LUZP");
/* harmony import */ var _angular_material_table__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/table */ "OaSA");
/* harmony import */ var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @iconify/icons-ic/twotone-add */ "7wwx");
/* harmony import */ var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @iconify/icons-ic/twotone-cloud-download */ "MzEE");
/* harmony import */ var _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @iconify/icons-ic/twotone-delete */ "e3EN");
/* harmony import */ var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _iconify_icons_ic_twotone_link__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @iconify/icons-ic/twotone-link */ "h+Y6");
/* harmony import */ var _iconify_icons_ic_twotone_link__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_link__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var _iconify_icons_ic_twotone_more_horiz__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @iconify/icons-ic/twotone-more-horiz */ "SqwC");
/* harmony import */ var _iconify_icons_ic_twotone_more_horiz__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_more_horiz__WEBPACK_IMPORTED_MODULE_12__);
/* harmony import */ var _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @vex/utils/tailwindcss */ "XXSj");














let AliasDataTableComponent = class AliasDataTableComponent {
    constructor() {
        this.pageSize = 10;
        this.dataSource = new _angular_material_table__WEBPACK_IMPORTED_MODULE_7__["MatTableDataSource"]();
        this.selection = new _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_3__["SelectionModel"](true, []);
        this.icMoreHoriz = _iconify_icons_ic_twotone_more_horiz__WEBPACK_IMPORTED_MODULE_12___default.a;
        this.icCloudDownload = _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_9___default.a;
        this.icLink = _iconify_icons_ic_twotone_link__WEBPACK_IMPORTED_MODULE_11___default.a;
        this.icDelete = _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_10___default.a;
        this.icAdd = _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_8___default.a;
        this.theme = _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_13__["default"];
        this.selectionDelete = new _angular_core__WEBPACK_IMPORTED_MODULE_4__["EventEmitter"]();
        this.createAliasValue = new _angular_core__WEBPACK_IMPORTED_MODULE_4__["EventEmitter"]();
    }
    ngOnInit() { }
    ngOnChanges(changes) {
        if (changes.columns) {
            this.visibleColumns = this.columns.map(column => column.property);
        }
        if (changes.data) {
            this.dataSource.data = this.data;
        }
    }
    ngAfterViewInit() {
        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
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
    deleteSelected() {
        this.selectionDelete.emit(this.selection.selected);
    }
};
AliasDataTableComponent.ctorParameters = () => [];
AliasDataTableComponent.propDecorators = {
    title: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Input"] }],
    data: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Input"] }],
    columns: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Input"] }],
    pageSize: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Input"] }],
    paginator: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["ViewChild"], args: [_angular_material_paginator__WEBPACK_IMPORTED_MODULE_5__["MatPaginator"], { static: true },] }],
    sort: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["ViewChild"], args: [_angular_material_sort__WEBPACK_IMPORTED_MODULE_6__["MatSort"], { static: true },] }],
    selectionDelete: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Output"] }],
    createAliasValue: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Output"] }]
};
AliasDataTableComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_4__["Component"])({
        selector: 'alias-data-table',
        template: _raw_loader_alias_data_table_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_alias_data_table_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], AliasDataTableComponent);



/***/ }),

/***/ "7dOf":
/*!******************************************************************************************!*\
  !*** ./src/app/modules/aliases/pages/aliases-index/services/aliases-resolver.service.ts ***!
  \******************************************************************************************/
/*! exports provided: AliasesResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AliasesResolver", function() { return AliasesResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _core_http_alias_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @core/http/alias-resource.service */ "4GLy");



let AliasesResolver = class AliasesResolver {
    constructor(aliasResource) {
        this.aliasResource = aliasResource;
    }
    resolve(route) {
        return this.aliasResource.index({
            project_id: route.queryParams.project_id,
        });
    }
};
AliasesResolver.ctorParameters = () => [
    { type: _core_http_alias_resource_service__WEBPACK_IMPORTED_MODULE_2__["AliasResource"] }
];
AliasesResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], AliasesResolver);



/***/ }),

/***/ "93nD":
/*!********************************************************************************!*\
  !*** ./src/app/modules/aliases/pages/aliases-index/aliases-index.component.ts ***!
  \********************************************************************************/
/*! exports provided: AliasesIndexComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AliasesIndexComponent", function() { return AliasesIndexComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_aliases_index_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./aliases-index.component.html */ "ZogQ");
/* harmony import */ var _aliases_index_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./aliases-index.component.scss */ "n3JR");
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
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! rxjs/operators */ "kU1M");
/* harmony import */ var _vex_animations__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @vex/animations */ "ORuP");
/* harmony import */ var _core_http_alias_resource_service__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @core/http/alias-resource.service */ "4GLy");
/* harmony import */ var _core_utils_file_service__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @core/utils/file.service */ "EGFe");
/* harmony import */ var _mock_aliases_index_data__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! ./mock/aliases-index-data */ "dnhS");
/* harmony import */ var _services__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! ./services */ "jwPG");




















let AliasesIndexComponent = class AliasesIndexComponent {
    constructor(icons, aliasesDataService, aliasResource, activatedRoute, dialog, location, file, route, router) {
        this.icons = icons;
        this.aliasesDataService = aliasesDataService;
        this.aliasResource = aliasResource;
        this.activatedRoute = activatedRoute;
        this.dialog = dialog;
        this.location = location;
        this.file = file;
        this.route = route;
        this.router = router;
        this.layoutCtrl = new _angular_forms__WEBPACK_IMPORTED_MODULE_6__["FormControl"]('boxed');
        // Table settings
        this.columns = [
            { label: 'Checkbox', property: 'checkbox', type: 'checkbox', visible: true },
            { label: 'Name', property: 'name', type: 'text', visible: true },
            { label: 'Components', property: 'components', type: 'button', visible: true },
        ];
        this.pageIndex = this.route.snapshot.queryParams.page || 0;
        this.pageSize = 10;
        this.pageSizeOptions = [5, 10, 20, 50];
        this.selection = new _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_3__["SelectionModel"](true, []);
        this.searchCtrl = new _angular_forms__WEBPACK_IMPORTED_MODULE_6__["FormControl"]();
        this.labels = _mock_aliases_index_data__WEBPACK_IMPORTED_MODULE_18__["aioTableLabels"];
        // Breadcrumb settings
        this.crumbs = [];
    }
    get visibleColumns() {
        return this.columns.filter(column => column.visible).map(column => column.property);
    }
    ngOnInit() {
        this.aliasesDataService.set(this.route.snapshot.data.aliases);
        this.dataSource = new _angular_material_table__WEBPACK_IMPORTED_MODULE_11__["MatTableDataSource"]();
        this.aliasesDataService.aliases$.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_14__["filter"])(Boolean)).subscribe(aliases => {
            this.dataSource.data = aliases;
        });
        this.searchCtrl.valueChanges.pipe(Object(ngx_take_until_destroy__WEBPACK_IMPORTED_MODULE_13__["untilDestroyed"])(this)).subscribe(value => this.onFilterChange(value));
        this.project = this.route.snapshot.data.project;
        this.crumbs.push({ name: this.project.name });
        this.crumbs.push({ name: 'Aliases' });
    }
    ngAfterViewInit() {
        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
    }
    getAliases(params) {
        this.aliasResource.index(params).subscribe((res) => {
            this.aliasesDataService.set(res);
        }, error => {
        });
    }
    showAlias(alias) {
        const path = this.file.join('/aliases', alias.id);
        const snapshot = this.route.snapshot;
        this.router.navigate([path], {
            queryParams: { project_id: snapshot.queryParams.project_id },
        });
    }
    deleteAlias(alias) {
        const snapshot = this.route.snapshot;
        const queryParams = { project_id: snapshot.queryParams.project_id };
        this.aliasResource.destroy(alias.id, queryParams).subscribe(res => {
            this.aliasesDataService.delete(alias.id);
            this.selection.deselect(alias);
        });
    }
    deleteAliases(aliases) {
        aliases.forEach(r => this.deleteAlias(r));
    }
    updateAlias(alias, params) {
        this.aliasResource.update(alias.id, params).subscribe(res => {
            for (const key in params) {
                if (params.hasOwnProperty(key)) {
                    alias[key] = params[key];
                }
            }
        });
    }
    // openCreateDialog() {
    //   let dialogRef = this.dialog.open(AliasesCreateComponent, {
    //     width: '600px'
    //   });
    //
    //   const onCreateSub = dialogRef.componentInstance.onCreate.subscribe(($event) => {
    //     this.createAlias($event)
    //   });
    //
    //   dialogRef.afterClosed().subscribe(() => {
    //     onCreateSub.unsubscribe();
    //   });
    // }
    // createAlias(alias: Alias) {
    //   const snapshot: ActivatedRouteSnapshot = this.route.snapshot
    //   alias.project_id = snapshot.queryParams.project_id
    //
    //   this.aliasResource.create(alias).subscribe(
    //     (res: Alias) => {
    //       this.dataSource.data.push(res)
    //     },
    //     err => {
    //
    //     })
    // }
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
    onComponentChange(change, row) {
        const aliases = this.aliasesDataService.aliases;
        const index = aliases.findIndex(c => c === row);
        aliases[index].components = change.value;
        this.aliasesDataService.set(aliases);
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
    ngOnDestroy() { }
};
AliasesIndexComponent.ctorParameters = () => [
    { type: _services__WEBPACK_IMPORTED_MODULE_19__["AliasesIndexIcons"] },
    { type: _services__WEBPACK_IMPORTED_MODULE_19__["AliasesDataService"] },
    { type: _core_http_alias_resource_service__WEBPACK_IMPORTED_MODULE_16__["AliasResource"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_12__["ActivatedRoute"] },
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_7__["MatDialog"] },
    { type: _angular_common__WEBPACK_IMPORTED_MODULE_4__["Location"] },
    { type: _core_utils_file_service__WEBPACK_IMPORTED_MODULE_17__["FileService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_12__["ActivatedRoute"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_12__["Router"] }
];
AliasesIndexComponent.propDecorators = {
    columns: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_5__["Input"] }],
    paginator: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_5__["ViewChild"], args: [_angular_material_paginator__WEBPACK_IMPORTED_MODULE_9__["MatPaginator"], { static: true },] }],
    sort: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_5__["ViewChild"], args: [_angular_material_sort__WEBPACK_IMPORTED_MODULE_10__["MatSort"], { static: true },] }]
};
AliasesIndexComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_5__["Component"])({
        selector: 'aliases-index',
        template: _raw_loader_aliases_index_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        animations: [
            _vex_animations__WEBPACK_IMPORTED_MODULE_15__["fadeInUp400ms"],
            _vex_animations__WEBPACK_IMPORTED_MODULE_15__["stagger40ms"],
        ],
        providers: [
            {
                provide: _angular_material_form_field__WEBPACK_IMPORTED_MODULE_8__["MAT_FORM_FIELD_DEFAULT_OPTIONS"],
                useValue: {
                    appearance: 'standard',
                },
            },
        ],
        styles: [_aliases_index_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], AliasesIndexComponent);



/***/ }),

/***/ "A7TT":
/*!**************************************************************!*\
  !*** ./src/app/shared/pipes/request-component-label.pipe.ts ***!
  \**************************************************************/
/*! exports provided: RequestComponentLabelPipe */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RequestComponentLabelPipe", function() { return RequestComponentLabelPipe; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @vex/utils/tailwindcss */ "XXSj");
/* harmony import */ var color__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! color */ "aSns");
/* harmony import */ var color__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(color__WEBPACK_IMPORTED_MODULE_3__);




let RequestComponentLabelPipe = class RequestComponentLabelPipe {
    constructor() {
        this.labels = {
            headers: {
                text: 'Headers',
                backgroundColor: color__WEBPACK_IMPORTED_MODULE_3___default()(_vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_2__["default"].colors.green['500']).fade(0.9),
                color: _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_2__["default"].colors.green['500'],
            },
            query_params: {
                text: 'Query Params',
                backgroundColor: color__WEBPACK_IMPORTED_MODULE_3___default()(_vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_2__["default"].colors.cyan['500']).fade(0.9),
                color: _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_2__["default"].colors.cyan['500'],
            },
            body_params: {
                text: 'Body Params',
                backgroundColor: color__WEBPACK_IMPORTED_MODULE_3___default()(_vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_2__["default"].colors.teal['500']).fade(0.9),
                color: _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_2__["default"].colors.teal['500'],
            },
            response: {
                text: 'Response',
                backgroundColor: color__WEBPACK_IMPORTED_MODULE_3___default()(_vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_2__["default"].colors.purple['500']).fade(0.9),
                color: _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_2__["default"].colors.purple['500'],
            },
        };
    }
    transform(labels) {
        return labels.map(label => {
            return this.labels[label];
        });
    }
};
RequestComponentLabelPipe = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Pipe"])({
        name: 'requestComponentLabel',
    })
], RequestComponentLabelPipe);



/***/ }),

/***/ "Bj6G":
/*!************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/aliases/pages/alias-details/alias-details.component.html ***!
  \************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<vex-page-layout mode=\"card\">\n\n<vex-page-layout-header fxLayout=\"column\" fxLayoutAlign=\"center start\">\n    <div vexContainer>\n      <h1 class=\"title mt-0 mb-1\">Alias Values</h1>\n      <vex-breadcrumbs [crumbs]=\"crumbs\"></vex-breadcrumbs>\n    </div>\n  </vex-page-layout-header>\n\n<vex-page-layout-content vexContainer>\n  <div class=\"card\">\n\n    <alias-data-table [title]=\"aliasValueTitle\"\n                      [columns]=\"aliasValueColumns\"\n                      [data]=\"aliasValueData\"\n                      (selectionDelete)=\"deleteAliasValue($event)\"\n                      (createAliasValue)=\"openAliasValueCreateDialog($event)\"\n                      class=\"w-full overflow-auto shadow\" gdColumn=\"1 / span 2\"\n                      gdColumn.lt-md=\"1 / -1\"\n                      gdColumn.lt-sm=\"1\"></alias-data-table>\n\n  </div>\n</vex-page-layout-content>\n");

/***/ }),

/***/ "Cr7o":
/*!*****************************************************************************************************************!*\
  !*** ./src/app/modules/aliases/pages/alias-details/components/alias-data-table/alias-data-table.component.scss ***!
  \*****************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (".table-link {\n  color: #1976d2;\n}\n\n.table-link:hover {\n  text-decoration: underline;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uLy4uLy4uLy4uL2FsaWFzLWRhdGEtdGFibGUuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSxjQUFBO0FBQ0Y7O0FBRUE7RUFDRSwwQkFBQTtBQUNGIiwiZmlsZSI6ImFsaWFzLWRhdGEtdGFibGUuY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyIudGFibGUtbGluayB7XG4gIGNvbG9yOiAjMTk3NmQyO1xufVxuXG4udGFibGUtbGluazpob3ZlciB7XG4gIHRleHQtZGVjb3JhdGlvbjogdW5kZXJsaW5lO1xufSJdfQ== */");

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

/***/ "F7bP":
/*!************************************************************************************************************!*\
  !*** ./src/app/modules/aliases/pages/alias-details/components/alias-data-table/alias-data-table.module.ts ***!
  \************************************************************************************************************/
/*! exports provided: AliasDataTableModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AliasDataTableModule", function() { return AliasDataTableModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/checkbox */ "pMoy");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _angular_material_paginator__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/paginator */ "5QHs");
/* harmony import */ var _angular_material_sort__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/material/sort */ "LUZP");
/* harmony import */ var _angular_material_table__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/material/table */ "OaSA");
/* harmony import */ var _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/material/tooltip */ "ZFy/");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _vex_pipes_color_color_fade_module__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @vex/pipes/color/color-fade.module */ "Chvm");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _alias_data_table_component__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./alias-data-table.component */ "/ywk");















let AliasDataTableModule = class AliasDataTableModule {
};
AliasDataTableModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_alias_data_table_component__WEBPACK_IMPORTED_MODULE_14__["AliasDataTableComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_material_table__WEBPACK_IMPORTED_MODULE_9__["MatTableModule"],
            _angular_material_paginator__WEBPACK_IMPORTED_MODULE_7__["MatPaginatorModule"],
            _angular_material_sort__WEBPACK_IMPORTED_MODULE_8__["MatSortModule"],
            _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_5__["MatCheckboxModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_10__["MatTooltipModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_4__["MatButtonModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_6__["MatIconModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_13__["IconModule"],
            _vex_pipes_color_color_fade_module__WEBPACK_IMPORTED_MODULE_12__["ColorFadeModule"],
            _angular_router__WEBPACK_IMPORTED_MODULE_11__["RouterModule"],
        ],
        exports: [_alias_data_table_component__WEBPACK_IMPORTED_MODULE_14__["AliasDataTableComponent"]],
    })
], AliasDataTableModule);



/***/ }),

/***/ "KUEM":
/*!*********************************************************************************************!*\
  !*** ./src/app/modules/aliases/pages/aliases-index/services/aliases-index-icons.service.ts ***!
  \*********************************************************************************************/
/*! exports provided: AliasesIndexIcons */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AliasesIndexIcons", function() { return AliasesIndexIcons; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @iconify/icons-ic/twotone-add */ "7wwx");
/* harmony import */ var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @iconify/icons-ic/twotone-delete */ "e3EN");
/* harmony import */ var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _iconify_icons_ic_twotone_filter_list__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @iconify/icons-ic/twotone-filter-list */ "+4LO");
/* harmony import */ var _iconify_icons_ic_twotone_filter_list__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_filter_list__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _iconify_icons_ic_twotone_more_horiz__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @iconify/icons-ic/twotone-more-horiz */ "SqwC");
/* harmony import */ var _iconify_icons_ic_twotone_more_horiz__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_more_horiz__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @iconify/icons-ic/twotone-search */ "sF+I");
/* harmony import */ var _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_6__);







let AliasesIndexIcons = class AliasesIndexIcons {
    constructor() {
        this.icSearch = _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_6___default.a;
        this.icDelete = _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_3___default.a;
        this.icAdd = _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_2___default.a;
        this.icFilterList = _iconify_icons_ic_twotone_filter_list__WEBPACK_IMPORTED_MODULE_4___default.a;
        this.icMoreHoriz = _iconify_icons_ic_twotone_more_horiz__WEBPACK_IMPORTED_MODULE_5___default.a;
    }
};
AliasesIndexIcons.ctorParameters = () => [];
AliasesIndexIcons = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])()
], AliasesIndexIcons);



/***/ }),

/***/ "O5jT":
/*!**************************************************************************************!*\
  !*** ./src/app/modules/aliases/pages/aliases-index/services/aliases-data.service.ts ***!
  \**************************************************************************************/
/*! exports provided: AliasesDataService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AliasesDataService", function() { return AliasesDataService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "qCKp");
/* harmony import */ var _data_schema_alias__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @data/schema/alias */ "tpJP");




let AliasesDataService = class AliasesDataService {
    constructor() {
        this.subject = new rxjs__WEBPACK_IMPORTED_MODULE_2__["BehaviorSubject"](null);
        this.aliases$ = this.subject.asObservable();
    }
    set(aliases) {
        this.aliases = aliases;
        this.subject.next(aliases);
    }
    add(alias) {
        this.aliases.unshift(new _data_schema_alias__WEBPACK_IMPORTED_MODULE_3__["Alias"](alias));
        this.set(this.aliases);
    }
    delete(id) {
        this.aliases.splice(this.aliases.findIndex((existingAlias) => {
            return existingAlias.id === id;
        }), 1);
        this.set(this.aliases);
    }
};
AliasesDataService.ctorParameters = () => [];
AliasesDataService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], AliasesDataService);



/***/ }),

/***/ "ODkH":
/*!**********************************************************************************!*\
  !*** ./src/app/modules/aliases/pages/alias-details/alias-details.component.scss ***!
  \**********************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJhbGlhcy1kZXRhaWxzLmNvbXBvbmVudC5zY3NzIn0= */");

/***/ }),

/***/ "PCNd":
/*!*****************************************!*\
  !*** ./src/app/shared/shared.module.ts ***!
  \*****************************************/
/*! exports provided: SharedModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SharedModule", function() { return SharedModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _shared_pipes_request_component_label_pipe__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @shared/pipes/request-component-label.pipe */ "A7TT");




let SharedModule = class SharedModule {
};
SharedModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_shared_pipes_request_component_label_pipe__WEBPACK_IMPORTED_MODULE_3__["RequestComponentLabelPipe"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
        ],
        exports: [
            _shared_pipes_request_component_label_pipe__WEBPACK_IMPORTED_MODULE_3__["RequestComponentLabelPipe"],
        ],
    })
], SharedModule);



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

/***/ "W+7z":
/*!***********************************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/aliases/pages/alias-details/components/alias-value-create/alias-value-create.component.html ***!
  \***********************************************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<form (ngSubmit)=\"create()\" [formGroup]=\"form\">\r\n  <div fxLayout=\"row\" fxLayoutAlign=\"start center\" mat-dialog-title>\r\n\r\n    <h2 class=\"headline m-0\" fxFlex=\"auto\">Create Alias Value</h2>\r\n<!--\r\n    <button [matMenuTriggerFor]=\"settingsMenu\" class=\"text-secondary\" mat-icon-button type=\"button\">\r\n      <mat-icon [icIcon]=\"icMoreVert\"></mat-icon>\r\n    </button>\r\n-->\r\n    <button class=\"text-secondary\" mat-dialog-close mat-icon-button type=\"button\">\r\n      <mat-icon [icIcon]=\"icClose\"></mat-icon>\r\n    </button>\r\n  </div>\r\n\r\n  <mat-divider class=\"-mx-6 text-border\"></mat-divider>\r\n\r\n  <mat-dialog-content fxLayout=\"column\">\r\n    <mat-form-field class=\"mt-6\">\r\n      <mat-label>Value</mat-label>\r\n      <input cdkFocusInitial formControlName=\"value\" matInput>\r\n\r\n      <mat-icon [icIcon]=\"icPerson\" class=\"ltr:mr-3 rtl:ml-3\" matPrefix></mat-icon>\r\n    </mat-form-field>\r\n  </mat-dialog-content>\r\n\r\n  <mat-dialog-actions align=\"end\">\r\n    <button mat-button mat-dialog-close type=\"button\">CANCEL</button>\r\n    <button color=\"primary\" mat-button type=\"submit\">SUBMIT</button>\r\n  </mat-dialog-actions>\r\n</form>\r\n");

/***/ }),

/***/ "XQjC":
/*!****************************************************************************************************************!*\
  !*** ./src/app/modules/aliases/pages/alias-details/components/alias-value-create/alias-value-create.module.ts ***!
  \****************************************************************************************************************/
/*! exports provided: AliasValueCreateModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AliasValueCreateModule", function() { return AliasValueCreateModule; });
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
/* harmony import */ var _alias_value_create_component__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ./alias-value-create.component */ "Z0YO");
















let AliasValueCreateModule = class AliasValueCreateModule {
};
AliasValueCreateModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
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
        declarations: [_alias_value_create_component__WEBPACK_IMPORTED_MODULE_15__["AliasValueCreateComponent"]],
        entryComponents: [_alias_value_create_component__WEBPACK_IMPORTED_MODULE_15__["AliasValueCreateComponent"]],
        exports: [_alias_value_create_component__WEBPACK_IMPORTED_MODULE_15__["AliasValueCreateComponent"]],
    })
], AliasValueCreateModule);



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

/***/ "Z0YO":
/*!*******************************************************************************************************************!*\
  !*** ./src/app/modules/aliases/pages/alias-details/components/alias-value-create/alias-value-create.component.ts ***!
  \*******************************************************************************************************************/
/*! exports provided: AliasValueCreateComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AliasValueCreateComponent", function() { return AliasValueCreateComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_alias_value_create_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./alias-value-create.component.html */ "W+7z");
/* harmony import */ var _alias_value_create_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./alias-value-create.component.scss */ "j/A5");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ "s7LF");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/dialog */ "iELJ");
/* harmony import */ var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @iconify/icons-ic/twotone-close */ "5mnX");
/* harmony import */ var _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @iconify/icons-ic/twotone-person */ "KaaH");
/* harmony import */ var _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_7__);








let AliasValueCreateComponent = class AliasValueCreateComponent {
    constructor(data, dialogRef, fb) {
        this.data = data;
        this.dialogRef = dialogRef;
        this.fb = fb;
        this.onCreate = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
        this.icClose = _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_6___default.a;
        this.icPerson = _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_7___default.a;
    }
    ngOnInit() {
        this.form = this.fb.group({
            value: null,
        });
    }
    create() {
        const form = this.form.value;
        this.onCreate.emit(form);
        this.dialogRef.close();
    }
};
AliasValueCreateComponent.ctorParameters = () => [
    { type: undefined, decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Inject"], args: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MAT_DIALOG_DATA"],] }] },
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MatDialogRef"] },
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormBuilder"] }
];
AliasValueCreateComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'alias-value-create',
        template: _raw_loader_alias_value_create_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_alias_value_create_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], AliasValueCreateComponent);



/***/ }),

/***/ "ZPbs":
/*!*****************************************************************************!*\
  !*** ./src/app/modules/aliases/pages/aliases-index/aliases-index.module.ts ***!
  \*****************************************************************************/
/*! exports provided: AliasesIndexModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AliasesIndexModule", function() { return AliasesIndexModule; });
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
/* harmony import */ var _aliases_components_aliases_create_aliases_create_module__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! @aliases/components/aliases-create/aliases-create.module */ "/vI3");
/* harmony import */ var _shared_shared_module__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! @shared/shared.module */ "PCNd");
/* harmony import */ var _aliases_index_component__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! ./aliases-index.component */ "93nD");
/* harmony import */ var _services_aliases_index_icons_service__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! ./services/aliases-index-icons.service */ "KUEM");
























let AliasesIndexModule = class AliasesIndexModule {
};
AliasesIndexModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_aliases_index_component__WEBPACK_IMPORTED_MODULE_22__["AliasesIndexComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_16__["PageLayoutModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _vex_components_breadcrumbs_breadcrumbs_module__WEBPACK_IMPORTED_MODULE_15__["BreadcrumbsModule"],
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
            _aliases_components_aliases_create_aliases_create_module__WEBPACK_IMPORTED_MODULE_20__["AliasesCreateModule"],
            _shared_shared_module__WEBPACK_IMPORTED_MODULE_21__["SharedModule"],
        ],
        providers: [_services_aliases_index_icons_service__WEBPACK_IMPORTED_MODULE_23__["AliasesIndexIcons"]],
    })
], AliasesIndexModule);



/***/ }),

/***/ "ZogQ":
/*!************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/aliases/pages/aliases-index/aliases-index.component.html ***!
  \************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<vex-page-layout>\r\n\r\n  <vex-page-layout-header class=\"pb-16\" fxLayout=\"column\" fxLayoutAlign=\"center start\">\r\n    <div [class.container]=\"layoutCtrl.value === 'boxed'\"\r\n         [class.px-gutter]=\"layoutCtrl.value === 'fullwidth'\"\r\n         class=\"w-full flex flex-col sm:flex-row justify-between\">\r\n      <vex-breadcrumbs [crumbs]=\"crumbs\"></vex-breadcrumbs>\r\n    </div>\r\n  </vex-page-layout-header>\r\n\r\n  <vex-page-layout-content [class.container]=\"layoutCtrl.value === 'boxed'\"\r\n                           [class.px-gutter]=\"layoutCtrl.value === 'fullwidth'\"\r\n                           class=\"-mt-6\">\r\n\r\n    <div class=\"card overflow-auto -mt-16\">\r\n      <div class=\"bg-app-bar px-6 h-16 border-b sticky left-0\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\r\n        <h2 class=\"title my-0 ltr:pr-4 rtl:pl-4 ltr:mr-4 rtl:ml-4 ltr:border-r rtl:border-l\" fxFlex=\"none\" fxHide.xs>\r\n          <span *ngIf=\"selection.isEmpty()\">Aliases</span>\r\n          <span *ngIf=\"selection.hasValue()\">{{ selection.selected.length }}\r\n            Alias<span *ngIf=\"selection.selected.length > 1\">s</span> selected</span>\r\n        </h2>\r\n\r\n        <div *ngIf=\"selection.hasValue()\" class=\"mr-4 pr-4 border-r\" fxFlex=\"none\">\r\n          <button (click)=\"deleteAliases(selection.selected)\"\r\n                  color=\"primary\"\r\n                  mat-icon-button\r\n                  matTooltip=\"Delete selected\"\r\n                  type=\"button\">\r\n            <mat-icon [icIcon]=\"icons.icDelete\"></mat-icon>\r\n          </button>\r\n\r\n          <!-- <button color=\"primary\" mat-icon-button matTooltip=\"Another action\" type=\"button\">\r\n            <mat-icon [icIcon]=\"icFolder\"></mat-icon>\r\n          </button> -->\r\n        </div>\r\n\r\n        <div class=\"bg-card rounded-full border px-4\"\r\n             fxFlex=\"400px\"\r\n             fxFlex.lt-md=\"auto\"\r\n             fxHide.xs\r\n             fxLayout=\"row\"\r\n             fxLayoutAlign=\"start center\">\r\n          <ic-icon [icIcon]=\"icons.icSearch\" size=\"20px\"></ic-icon>\r\n          <input [formControl]=\"searchCtrl\"\r\n                 class=\"px-4 py-3 border-0 outline-none w-full bg-transparent\"\r\n                 placeholder=\"Search...\"\r\n                 type=\"search\">\r\n        </div>\r\n\r\n        <span fxFlex></span>\r\n\r\n        <button class=\"ml-4\" fxFlex=\"none\" fxHide.gt-xs mat-icon-button type=\"button\">\r\n          <mat-icon [icIcon]=\"icons.icSearch\"></mat-icon>\r\n        </button>\r\n\r\n        <button [matMenuTriggerFor]=\"columnFilterMenu\"\r\n                class=\"ml-4\"\r\n                fxFlex=\"none\"\r\n                mat-icon-button\r\n                matTooltip=\"Filter Columns\"\r\n                type=\"button\">\r\n          <mat-icon [icIcon]=\"icons.icFilterList\"></mat-icon>\r\n        </button>\r\n\r\n        <!-- <button (click)=\"openCreateDialog()\"\r\n                class=\"ml-4\"\r\n                color=\"primary\"\r\n                fxFlex=\"none\"\r\n                mat-mini-fab\r\n                matTooltip=\"Add Scenario\"\r\n                type=\"button\">\r\n          <mat-icon [icIcon]=\"icons.icAdd\"></mat-icon>\r\n        </button> -->\r\n      </div>\r\n\r\n      <table @stagger [dataSource]=\"dataSource\" class=\"w-full\" mat-table matSort>\r\n\r\n        <!--- Note that these columns can be defined in any order.\r\n              The actual rendered columns are set as a property on the row definition\" -->\r\n\r\n        <!-- Checkbox Column -->\r\n        <ng-container matColumnDef=\"checkbox\">\r\n          <th *matHeaderCellDef mat-header-cell>\r\n            <mat-checkbox (change)=\"$event ? masterToggle() : null\"\r\n                          [checked]=\"selection.hasValue() && isAllSelected()\"\r\n                          [indeterminate]=\"selection.hasValue() && !isAllSelected()\"\r\n                          color=\"primary\">\r\n            </mat-checkbox>\r\n          </th>\r\n          <td *matCellDef=\"let row\" class=\"w-4\" mat-cell (click)=\"$event.stopPropagation()\">\r\n            <mat-checkbox (change)=\"$event ? selection.toggle(row) : null\"\r\n                          [checked]=\"selection.isSelected(row)\"\r\n                          color=\"primary\">\r\n            </mat-checkbox>\r\n          </td>\r\n        </ng-container>\r\n\r\n        <!-- Image Column -->\r\n        <ng-container matColumnDef=\"image\">\r\n          <th *matHeaderCellDef mat-header-cell></th>\r\n          <td *matCellDef=\"let row\" class=\"w-8 min-w-8 pr-0\" mat-cell>\r\n            <img [src]=\"row['imageSrc']\" class=\"avatar h-8 w-8 align-middle\">\r\n          </td>\r\n        </ng-container>\r\n\r\n        <!-- Text Columns -->\r\n        <ng-container *ngFor=\"let column of columns; trackBy: trackByProperty\">\r\n          <ng-container *ngIf=\"column.type === 'text'\" [matColumnDef]=\"column.property\">\r\n            <th *matHeaderCellDef class=\"uppercase\" mat-header-cell mat-sort-header> {{ column.label }}</th>\r\n            <td *matCellDef=\"let row\" [ngClass]=\"column.cssClasses\" mat-cell>{{ row[column.property] }}</td>\r\n          </ng-container>\r\n        </ng-container>\r\n\r\n        <!-- Date Columns -->\r\n        <ng-container *ngFor=\"let column of columns; trackBy: trackByProperty\">\r\n          <ng-container *ngIf=\"column.type === 'date'\" [matColumnDef]=\"column.property\">\r\n            <th *matHeaderCellDef class=\"uppercase\" mat-header-cell mat-sort-header> {{ column.label }}</th>\r\n            <td *matCellDef=\"let row\" [ngClass]=\"column.cssClasses\" mat-cell>{{ row[column.property] | date }}</td>\r\n          </ng-container>\r\n        </ng-container>\r\n\r\n        <!-- Label Column -->\r\n        <ng-container matColumnDef=\"components\">\r\n          <th *matHeaderCellDef class=\"uppercase\" mat-header-cell mat-sort-header>Components</th>\r\n          <td *matCellDef=\"let row\" mat-cell>\r\n            <div (click)=\"$event.stopPropagation()\" fxLayoutAlign=\"start center\" fxLayoutGap=\"4px\">\r\n              <div *ngFor=\"let label of row.components | requestComponentLabel\"\r\n                   [style.background-color]=\"label.backgroundColor\"\r\n                   [style.color]=\"label.color\"\r\n                   class=\"rounded px-2 py-1 font-medium text-xs\"\r\n                   fxFlex=\"none\">\r\n                {{ label.text }}\r\n              </div>\r\n            </div>\r\n          </td>\r\n        </ng-container>\r\n\r\n        <!-- Action Column -->\r\n        <ng-container matColumnDef=\"actions\">\r\n          <th *matHeaderCellDef mat-header-cell mat-sort-header></th>\r\n          <td *matCellDef=\"let row\" class=\"w-10 text-secondary\" mat-cell>\r\n            <button (click)=\"$event.stopPropagation()\"\r\n                    [matMenuTriggerData]=\"{ endpoint: row }\"\r\n                    [matMenuTriggerFor]=\"actionsMenu\"\r\n                    mat-icon-button\r\n                    type=\"button\">\r\n              <mat-icon [icIcon]=\"icons.icMoreHoriz\"></mat-icon>\r\n            </button>\r\n          </td>\r\n        </ng-container>\r\n\r\n        <tr *matHeaderRowDef=\"visibleColumns\" mat-header-row></tr>\r\n        <tr (click)=\"showAlias(row)\"\r\n            *matRowDef=\"let row; columns: visibleColumns;\"\r\n            @fadeInUp\r\n            class=\"hover:bg-hover trans-ease-out cursor-pointer\"\r\n            mat-row></tr>\r\n      </table>\r\n\r\n      <mat-paginator\r\n        [pageSizeOptions]=\"pageSizeOptions\"\r\n        [pageSize]=\"pageSize\"\r\n        [pageIndex]=\"pageIndex\"\r\n        (page)=\"onPaginateChange($event)\"\r\n        class=\"sticky left-0\">\r\n      </mat-paginator>\r\n    </div>\r\n\r\n  </vex-page-layout-content>\r\n\r\n</vex-page-layout>\r\n\r\n<mat-menu #columnFilterMenu=\"matMenu\" xPosition=\"before\" yPosition=\"below\">\r\n  <button (click)=\"toggleColumnVisibility(column, $event)\" *ngFor=\"let column of columns\"\r\n          class=\"checkbox-item mat-menu-item\">\r\n    <mat-checkbox (click)=\"$event.stopPropagation()\" [(ngModel)]=\"column.visible\" color=\"primary\">\r\n      {{ column.label }}\r\n    </mat-checkbox>\r\n  </button>\r\n</mat-menu>\r\n\r\n<mat-menu #actionsMenu=\"matMenu\" xPosition=\"before\" yPosition=\"below\">\r\n  <ng-template let-endpoint=\"endpoint\" matMenuContent>\r\n    <button (click)=\"deleteAlias(endpoint)\" mat-menu-item>\r\n      <mat-icon [icIcon]=\"icons.icDelete\"></mat-icon>\r\n      <span>Delete</span>\r\n    </button>\r\n  </ng-template>\r\n</mat-menu>\r\n");

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

/***/ "c+dE":
/*!***********************************************************!*\
  !*** ./src/app/modules/aliases/aliases-routing.module.ts ***!
  \***********************************************************/
/*! exports provided: AliasesRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AliasesRoutingModule", function() { return AliasesRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _aliases_pages_alias_details_alias_details_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @aliases/pages/alias-details/alias-details.component */ "jFjk");
/* harmony import */ var _aliases_pages_aliases_index_aliases_index_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @aliases/pages/aliases-index/aliases-index.component */ "93nD");
/* harmony import */ var _aliases_pages_aliases_index_services_aliases_resolver_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @aliases/pages/aliases-index/services/aliases-resolver.service */ "7dOf");
/* harmony import */ var _aliases_pages_alias_details_services_alias_resolver_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @aliases/pages/alias-details/services/alias-resolver.service */ "jeXO");
/* harmony import */ var _aliases_pages_alias_details_services_alias_values_resolver_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @aliases/pages/alias-details/services/alias-values-resolver.service */ "vYmi");
/* harmony import */ var _projects_services_project_resolver_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @projects/services/project-resolver.service */ "Y1jZ");









const routes = [
    {
        path: '',
        component: _aliases_pages_aliases_index_aliases_index_component__WEBPACK_IMPORTED_MODULE_4__["AliasesIndexComponent"],
        resolve: {
            aliases: _aliases_pages_aliases_index_services_aliases_resolver_service__WEBPACK_IMPORTED_MODULE_5__["AliasesResolver"],
            project: _projects_services_project_resolver_service__WEBPACK_IMPORTED_MODULE_8__["ProjectResolver"],
        },
    },
    {
        path: ':alias_id',
        component: _aliases_pages_alias_details_alias_details_component__WEBPACK_IMPORTED_MODULE_3__["AliasDetailsComponent"],
        resolve: {
            alias: _aliases_pages_alias_details_services_alias_resolver_service__WEBPACK_IMPORTED_MODULE_6__["AliasResolver"],
            alias_values: _aliases_pages_alias_details_services_alias_values_resolver_service__WEBPACK_IMPORTED_MODULE_7__["AliasValuesResolver"],
        },
    },
];
let AliasesRoutingModule = class AliasesRoutingModule {
};
AliasesRoutingModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [
            _angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes),
        ],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
    })
], AliasesRoutingModule);



/***/ }),

/***/ "dnhS":
/*!********************************************************************************!*\
  !*** ./src/app/modules/aliases/pages/aliases-index/mock/aliases-index-data.ts ***!
  \********************************************************************************/
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

/***/ "j/A5":
/*!*********************************************************************************************************************!*\
  !*** ./src/app/modules/aliases/pages/alias-details/components/alias-value-create/alias-value-create.component.scss ***!
  \*********************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJhbGlhcy12YWx1ZS1jcmVhdGUuY29tcG9uZW50LnNjc3MifQ== */");

/***/ }),

/***/ "jFjk":
/*!********************************************************************************!*\
  !*** ./src/app/modules/aliases/pages/alias-details/alias-details.component.ts ***!
  \********************************************************************************/
/*! exports provided: AliasDetailsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AliasDetailsComponent", function() { return AliasDetailsComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_alias_details_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./alias-details.component.html */ "Bj6G");
/* harmony import */ var _alias_details_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./alias-details.component.scss */ "ODkH");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/dialog */ "iELJ");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _iconify_icons_ic_twotone_cloud_off__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @iconify/icons-ic/twotone-cloud-off */ "DaE0");
/* harmony import */ var _iconify_icons_ic_twotone_cloud_off__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_cloud_off__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _iconify_icons_ic_twotone_group__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @iconify/icons-ic/twotone-group */ "Ell1");
/* harmony import */ var _iconify_icons_ic_twotone_group__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_group__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @iconify/icons-ic/twotone-more-vert */ "+Chm");
/* harmony import */ var _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _iconify_icons_ic_twotone_pageview__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @iconify/icons-ic/twotone-pageview */ "9Gk2");
/* harmony import */ var _iconify_icons_ic_twotone_pageview__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_pageview__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _iconify_icons_ic_twotone_timer__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @iconify/icons-ic/twotone-timer */ "De0L");
/* harmony import */ var _iconify_icons_ic_twotone_timer__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_timer__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _core_http_alias_value_resource_service__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @core/http/alias-value-resource.service */ "oFyy");
/* harmony import */ var _data_schema__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @data/schema */ "V99k");
/* harmony import */ var _components_alias_value_create_alias_value_create_component__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./components/alias-value-create/alias-value-create.component */ "Z0YO");














let AliasDetailsComponent = class AliasDetailsComponent {
    constructor(dialog, route, aliasValueResource) {
        this.dialog = dialog;
        this.route = route;
        this.aliasValueResource = aliasValueResource;
        this.aliasValueTitle = 'Alias Values';
        this.aliasValueColumns = [
            { label: 'Checkbox', property: 'checkbox', type: 'checkbox', visible: true },
            { label: 'Value', property: 'value', type: 'text', visible: true },
        ];
        this.icGroup = _iconify_icons_ic_twotone_group__WEBPACK_IMPORTED_MODULE_7___default.a;
        this.icPageView = _iconify_icons_ic_twotone_pageview__WEBPACK_IMPORTED_MODULE_9___default.a;
        this.icCloudOff = _iconify_icons_ic_twotone_cloud_off__WEBPACK_IMPORTED_MODULE_6___default.a;
        this.icTimer = _iconify_icons_ic_twotone_timer__WEBPACK_IMPORTED_MODULE_10___default.a;
        this.icMoreVert = _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_8___default.a;
        this.crumbs = [{
                name: 'Aliases',
                routerLink: ['/aliases'],
                queryParams: this.route.snapshot.queryParams,
            }];
    }
    ngOnInit() {
        const snapshot = this.route.snapshot;
        this.aliasValueData = snapshot.data.alias_values.map(aliasValue => {
            return new _data_schema__WEBPACK_IMPORTED_MODULE_12__["AliasValue"](aliasValue);
        });
        this.alias = new _data_schema__WEBPACK_IMPORTED_MODULE_12__["Alias"](snapshot.data.alias);
        this.crumbs.push({
            name: this.alias.name,
        });
    }
    openAliasValueCreateDialog($event) {
        const dialogRef = this.dialog.open(_components_alias_value_create_alias_value_create_component__WEBPACK_IMPORTED_MODULE_13__["AliasValueCreateComponent"], {
            width: '600px',
        });
        const onCreateSub = dialogRef.componentInstance.onCreate.subscribe(($event) => {
            this.createAliasValue($event.value);
        });
        dialogRef.afterClosed().subscribe(() => {
            onCreateSub.unsubscribe();
        });
    }
    createAliasValue(value) {
        const aliasValue = { value, alias_id: this.alias.id };
        this.aliasValueResource.create(aliasValue).subscribe(res => {
            this.aliasValueData = this.aliasValueData.concat(new _data_schema__WEBPACK_IMPORTED_MODULE_12__["AliasValue"](aliasValue));
        });
    }
    deleteAliasValue(aliasValues) {
        aliasValues.forEach(aliasValue => {
            const aliasValueId = aliasValue.id;
            this.aliasValueResource.destroy(aliasValueId).subscribe(res => {
                this.aliasValueData = this.aliasValueData.filter((candidate) => {
                    return candidate.id !== aliasValueId;
                });
            });
        });
    }
};
AliasDetailsComponent.ctorParameters = () => [
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_4__["MatDialog"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_5__["ActivatedRoute"] },
    { type: _core_http_alias_value_resource_service__WEBPACK_IMPORTED_MODULE_11__["AliasValueResource"] }
];
AliasDetailsComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'alias-details',
        template: _raw_loader_alias_details_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_alias_details_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], AliasDetailsComponent);



/***/ }),

/***/ "jeXO":
/*!****************************************************************************************!*\
  !*** ./src/app/modules/aliases/pages/alias-details/services/alias-resolver.service.ts ***!
  \****************************************************************************************/
/*! exports provided: AliasResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AliasResolver", function() { return AliasResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _core_http_alias_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @core/http/alias-resource.service */ "4GLy");



let AliasResolver = class AliasResolver {
    constructor(aliasResource) {
        this.aliasResource = aliasResource;
    }
    resolve(route) {
        return this.aliasResource.show(route.params.alias_id, { project_id: route.queryParams.project_id });
    }
};
AliasResolver.ctorParameters = () => [
    { type: _core_http_alias_resource_service__WEBPACK_IMPORTED_MODULE_2__["AliasResource"] }
];
AliasResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], AliasResolver);



/***/ }),

/***/ "jfiX":
/*!***************************************************!*\
  !*** ./src/app/modules/aliases/aliases.module.ts ***!
  \***************************************************/
/*! exports provided: AliasesModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AliasesModule", function() { return AliasesModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _aliases_routing_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./aliases-routing.module */ "c+dE");
/* harmony import */ var _pages_alias_details_alias_details_module__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./pages/alias-details/alias-details.module */ "+OFh");
/* harmony import */ var _pages_aliases_index_aliases_index_module__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./pages/aliases-index/aliases-index.module */ "ZPbs");






let AliasesModule = class AliasesModule {
};
AliasesModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _aliases_routing_module__WEBPACK_IMPORTED_MODULE_3__["AliasesRoutingModule"],
            _pages_aliases_index_aliases_index_module__WEBPACK_IMPORTED_MODULE_5__["AliasesIndexModule"],
            _pages_alias_details_alias_details_module__WEBPACK_IMPORTED_MODULE_4__["AliasDetailsModule"],
        ],
    })
], AliasesModule);



/***/ }),

/***/ "jwPG":
/*!***********************************************************************!*\
  !*** ./src/app/modules/aliases/pages/aliases-index/services/index.ts ***!
  \***********************************************************************/
/*! exports provided: AliasesDataService, AliasesIndexIcons, AliasesResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _aliases_data_service__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./aliases-data.service */ "O5jT");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "AliasesDataService", function() { return _aliases_data_service__WEBPACK_IMPORTED_MODULE_0__["AliasesDataService"]; });

/* harmony import */ var _aliases_index_icons_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./aliases-index-icons.service */ "KUEM");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "AliasesIndexIcons", function() { return _aliases_index_icons_service__WEBPACK_IMPORTED_MODULE_1__["AliasesIndexIcons"]; });

/* harmony import */ var _aliases_resolver_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./aliases-resolver.service */ "7dOf");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "AliasesResolver", function() { return _aliases_resolver_service__WEBPACK_IMPORTED_MODULE_2__["AliasesResolver"]; });






/***/ }),

/***/ "kdjS":
/*!*******************************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/aliases/pages/alias-details/components/alias-data-table/alias-data-table.component.html ***!
  \*******************************************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div class=\"overflow-auto w-full\" fxLayout=\"column\">\n  <div class=\"border-b py-4 px-6\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n    <h2 class=\"m-0 title\" fxFlex=\"auto\">{{ title }}</h2>\n\n    <div *ngIf=\"selection.hasValue()\" class=\"mr-4 pr-4 border-r\" fxFlex=\"none\">\n      <button (click)=\"deleteSelected()\"\n              color=\"primary\"\n              mat-icon-button\n              matTooltip=\"Delete selected\"\n              type=\"button\">\n        <mat-icon [icIcon]=\"icDelete\"></mat-icon>\n      </button>\n    </div>\n  </div>\n\n  <table [dataSource]=\"dataSource\" class=\"w-full overflow-auto\" mat-table matSort>\n    <!--- Note that these columns can be defined in any order.\n          The actual rendered columns are set as a property on the row definition\" -->\n\n    <!-- Checkbox Column -->\n    <ng-container matColumnDef=\"checkbox\">\n      <th *matHeaderCellDef mat-header-cell>\n        <mat-checkbox (change)=\"$event ? masterToggle() : null\"\n                      [checked]=\"selection.hasValue() && isAllSelected()\"\n                      [indeterminate]=\"selection.hasValue() && !isAllSelected()\"\n                      color=\"primary\">\n        </mat-checkbox>\n      </th>\n      <td *matCellDef=\"let row\" class=\"w-4\" mat-cell (click)=\"$event.stopPropagation()\">\n        <mat-checkbox (change)=\"$event ? selection.toggle(row) : null\"\n                      [checked]=\"selection.isSelected(row)\"\n                      color=\"primary\">\n        </mat-checkbox>\n      </td>\n    </ng-container>\n\n    <!-- Model Properties Column -->\n    <ng-container *ngFor=\"let column of columns\">\n      <ng-container *ngIf=\"column.type === 'text'\" [matColumnDef]=\"column.property\">\n        <th *matHeaderCellDef mat-header-cell mat-sort-header> {{ column.label }}</th>\n        <td *matCellDef=\"let row\" [ngClass]=\"column.cssClasses\" mat-cell>\n          {{ row[column.property] === undefined ? 'N/A' : row[column.property] }}\n        </td>\n      </ng-container>\n\n      <!-- Link Column -->\n      <ng-container *ngIf=\"column.type === 'link'\" [matColumnDef]=\"column.property\">\n        <th *matHeaderCellDef mat-header-cell mat-sort-header>{{ column.label }}</th>\n        <td *matCellDef=\"let row\" mat-cell>\n          <a class=\"table-link\"\n             [routerLink]=\"column.routerLink(row)\"\n             [queryParams]=\"column.queryParams()\"\n             (click)=\"column.onclick($event, row)\">{{ row[column.property] }}</a>\n        </td>\n      </ng-container>\n\n\n      <ng-container *ngIf=\"column.type === 'badge'\" [matColumnDef]=\"column.property\">\n        <th *matHeaderCellDef mat-header-cell mat-sort-header> {{ column.label }}</th>\n        <td *matCellDef=\"let row\" [ngClass]=\"column.cssClasses\" mat-cell>\n          <div *ngIf=\"row[column.property] === 'ready'\"\n               class=\"w-3 h-3 rounded-full bg-green-500 cursor-pointer\"\n               matTooltip=\"Ready to ship\"></div>\n          <div *ngIf=\"row[column.property] === 'pending'\"\n               class=\"w-3 h-3 rounded-full bg-orange-500 cursor-pointer\"\n               matTooltip=\"Pending Payment\"></div>\n          <div *ngIf=\"row[column.property] === 'warn'\"\n               class=\"w-3 h-3 rounded-full bg-red-500 cursor-pointer\"\n               matTooltip=\"Missing Payment\"></div>\n        </td>\n      </ng-container>\n    </ng-container>\n\n    <ng-container matColumnDef=\"link-button\">\n      <th *matHeaderCellDef mat-header-cell mat-sort-header></th>\n      <td *matCellDef=\"let row\" mat-cell>\n        <div class=\"flex  ml-3\">\n          <a (click)=\"$event.stopPropagation()\"\n             [style.background-color]=\"theme.colors.green['500'] | colorFade:0.9\"\n             [style.color]=\"theme.colors.green['500']\"\n             class=\"ml-auto w-8 h-8 leading-none flex items-center justify-center hover:bg-hover\"\n             mat-icon-button>\n            <mat-icon [icIcon]=\"icLink\" size=\"18px\"></mat-icon>\n          </a>\n        </div>\n      </td>\n    </ng-container>\n\n    <tr *matHeaderRowDef=\"visibleColumns\" mat-header-row></tr>\n    <!--suppress UnnecessaryLabelJS -->\n    <tr *matRowDef=\"let row; columns: visibleColumns;\" mat-row></tr>\n  </table>\n\n  <mat-paginator [pageSize]=\"pageSize\" class=\"paginator\"></mat-paginator>\n\n</div>\n");

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

/***/ "n3JR":
/*!**********************************************************************************!*\
  !*** ./src/app/modules/aliases/pages/aliases-index/aliases-index.component.scss ***!
  \**********************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJhbGlhc2VzLWluZGV4LmNvbXBvbmVudC5zY3NzIn0= */");

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



/***/ }),

/***/ "vYmi":
/*!***********************************************************************************************!*\
  !*** ./src/app/modules/aliases/pages/alias-details/services/alias-values-resolver.service.ts ***!
  \***********************************************************************************************/
/*! exports provided: AliasValuesResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AliasValuesResolver", function() { return AliasValuesResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _core_http_alias_value_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @core/http/alias-value-resource.service */ "oFyy");



let AliasValuesResolver = class AliasValuesResolver {
    constructor(aliasValueResource) {
        this.aliasValueResource = aliasValueResource;
    }
    resolve(route) {
        return this.aliasValueResource.index({ project_id: route.queryParams.project_id, alias_id: route.params.alias_id });
    }
};
AliasValuesResolver.ctorParameters = () => [
    { type: _core_http_alias_value_resource_service__WEBPACK_IMPORTED_MODULE_2__["AliasValueResource"] }
];
AliasValuesResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], AliasValuesResolver);



/***/ })

}]);
//# sourceMappingURL=aliases-aliases-module-es2015.js.map