(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["users-users-module"],{

/***/ "+Ntf":
/*!********************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/users/pages/user-organizations/user-organizations.component.html ***!
  \********************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<vex-page-layout>\r\n\r\n  <!-- <vex-page-layout-header class=\"pb-16\" fxLayout=\"column\" fxLayoutAlign=\"center start\">\r\n    <div [class.container]=\"layoutCtrl.value === 'boxed'\"\r\n         [class.px-gutter]=\"layoutCtrl.value === 'fullwidth'\"\r\n         class=\"w-full flex flex-col sm:flex-row justify-between\">\r\n      <div>\r\n        <h1 class=\"title mt-0 mb-1\">All Members</h1>\r\n        <vex-breadcrumbs [crumbs]=\"crumbs\"></vex-breadcrumbs>\r\n      </div>\r\n    </div>\r\n  </vex-page-layout-header> -->\r\n\r\n  <div [class.px-gutter]=\"layoutCtrl.value === 'fullwidth'\"\r\n                           class=\"mt-5 table-container\">\r\n\r\n    <div class=\"card overflow-auto\">\r\n      <div class=\"bg-app-bar px-6 h-16 border-b sticky left-0\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\r\n        <h2 class=\"title my-0 ltr:pr-4 rtl:pl-4 ltr:mr-4 rtl:ml-4 ltr:border-r rtl:border-l\" fxFlex=\"none\" fxHide.xs>\r\n          <span *ngIf=\"selection.isEmpty()\">Organizations</span>\r\n          <span *ngIf=\"selection.hasValue()\">{{ selection.selected.length }}\r\n            organization<span *ngIf=\"selection.selected.length > 1\">s</span> selected</span>\r\n        </h2>\r\n\r\n        <div *ngIf=\"selection.hasValue()\" class=\"mr-4 pr-4 border-r\" fxFlex=\"none\">\r\n          <button (click)=\"destroyOrganizationsUsers(selection.selected)\"\r\n                  color=\"primary\"\r\n                  mat-icon-button\r\n                  matTooltip=\"Delete selected\"\r\n                  type=\"button\">\r\n            <mat-icon [icIcon]=\"icons.icDelete\"></mat-icon>\r\n          </button>\r\n\r\n          <!-- <button color=\"primary\" mat-icon-button matTooltip=\"Another action\" type=\"button\">\r\n            <mat-icon [icIcon]=\"icFolder\"></mat-icon>\r\n          </button> -->\r\n        </div>\r\n\r\n        <div class=\"bg-card rounded-full border px-4\"\r\n             fxFlex=\"400px\"\r\n             fxFlex.lt-md=\"auto\"\r\n             fxHide.xs\r\n             fxLayout=\"row\"\r\n             fxLayoutAlign=\"start center\">\r\n          <ic-icon [icIcon]=\"icons.icSearch\" size=\"20px\"></ic-icon>\r\n          <input [formControl]=\"searchCtrl\"\r\n                 class=\"px-4 py-3 border-0 outline-none w-full bg-transparent\"\r\n                 placeholder=\"Search...\"\r\n                 type=\"search\">\r\n        </div>\r\n\r\n        <span fxFlex></span>\r\n\r\n        <button class=\"ml-4\" fxFlex=\"none\" fxHide.gt-xs mat-icon-button type=\"button\">\r\n          <mat-icon [icIcon]=\"icons.icSearch\"></mat-icon>\r\n        </button>\r\n\r\n        <button [matMenuTriggerFor]=\"columnFilterMenu\"\r\n                class=\"ml-4\"\r\n                fxFlex=\"none\"\r\n                mat-icon-button\r\n                matTooltip=\"Filter Columns\"\r\n                type=\"button\">\r\n          <mat-icon [icIcon]=\"icons.icFilterList\"></mat-icon>\r\n        </button>\r\n\r\n        <button (click)=\"openCreateDialog()\"\r\n                class=\"ml-4\"\r\n                color=\"primary\"\r\n                fxFlex=\"none\"\r\n                mat-mini-fab\r\n                matTooltip=\"Create Organization\"\r\n                type=\"button\">\r\n          <mat-icon [icIcon]=\"icons.icAdd\"></mat-icon>\r\n        </button>\r\n      </div>\r\n\r\n      <table @stagger [dataSource]=\"dataSource\" class=\"w-full\" mat-table matSort>\r\n\r\n        <!--- Note that these columns can be defined in any order.\r\n              The actual rendered columns are set as a property on the row definition\" -->\r\n\r\n        <!-- Checkbox Column -->\r\n        <ng-container matColumnDef=\"checkbox\">\r\n          <th *matHeaderCellDef mat-header-cell>\r\n            <mat-checkbox (change)=\"$event ? masterToggle() : null\"\r\n                          [checked]=\"selection.hasValue() && isAllSelected()\"\r\n                          [indeterminate]=\"selection.hasValue() && !isAllSelected()\"\r\n                          color=\"primary\">\r\n            </mat-checkbox>\r\n          </th>\r\n          <td *matCellDef=\"let row\" class=\"w-4\" mat-cell>\r\n            <mat-checkbox (change)=\"$event ? selection.toggle(row) : null\"\r\n                          (click)=\"$event.stopPropagation()\"\r\n                          [checked]=\"selection.isSelected(row)\"\r\n                          color=\"primary\">\r\n            </mat-checkbox>\r\n          </td>\r\n        </ng-container>\r\n\r\n        <!-- Image Column -->\r\n        <ng-container matColumnDef=\"image\">\r\n          <th *matHeaderCellDef mat-header-cell></th>\r\n          <td *matCellDef=\"let row\" class=\"w-8 min-w-8 pr-0\" mat-cell>\r\n            <img [src]=\"row['imageSrc']\" class=\"avatar h-8 w-8 align-middle\">\r\n          </td>\r\n        </ng-container>\r\n\r\n        <!-- Text Columns -->\r\n        <ng-container *ngFor=\"let column of columns; trackBy: trackByProperty\">\r\n          <ng-container *ngIf=\"column.type === 'text'\" [matColumnDef]=\"column.property\">\r\n            <th *matHeaderCellDef class=\"uppercase\" mat-header-cell mat-sort-header> {{ column.label }}</th>\r\n            <td *matCellDef=\"let row\" [ngClass]=\"column.cssClasses\" mat-cell>{{ row[column.property] }}</td>\r\n          </ng-container>\r\n        </ng-container>\r\n\r\n        <!-- Date Columns -->\r\n        <ng-container *ngFor=\"let column of columns; trackBy: trackByProperty\">\r\n          <ng-container *ngIf=\"column.type === 'date'\" [matColumnDef]=\"column.property\">\r\n            <th *matHeaderCellDef class=\"uppercase\" mat-header-cell mat-sort-header> {{ column.label }}</th>\r\n            <td *matCellDef=\"let row\" [ngClass]=\"column.cssClasses\" mat-cell>{{ row[column.property] | date }}</td>\r\n          </ng-container>\r\n        </ng-container>\r\n\r\n        <!-- Button Column -->\r\n        <ng-container *ngFor=\"let column of columns; trackBy: trackByProperty\">\r\n          <ng-container *ngIf=\"column.type === 'button'\" matColumnDef=\"button\">\r\n            <th *matHeaderCellDef class=\"uppercase\" mat-header-cell mat-sort-header disabled></th>\r\n            <td *matCellDef=\"let row\" mat-cell>\r\n              <button\r\n                color=\"primary\"\r\n                mat-flat-button\r\n                (click)=\"column.onclick($event, row)\">\r\n                {{ column.label }}\r\n              </button>\r\n            </td>\r\n          </ng-container>\r\n        </ng-container>\r\n\r\n        <!-- Action Column -->\r\n        <ng-container matColumnDef=\"actions\">\r\n          <th *matHeaderCellDef mat-header-cell mat-sort-header></th>\r\n          <td *matCellDef=\"let row\" class=\"w-10 text-secondary\" mat-cell>\r\n            <button (click)=\"$event.stopPropagation()\"\r\n                    [matMenuTriggerData]=\"{ organization: row }\"\r\n                    [matMenuTriggerFor]=\"actionsMenu\"\r\n                    mat-icon-button\r\n                    type=\"button\">\r\n              <mat-icon [icIcon]=\"icons.icMoreHoriz\"></mat-icon>\r\n            </button>\r\n          </td>\r\n        </ng-container>\r\n\r\n        <tr *matHeaderRowDef=\"visibleColumns\" mat-header-row></tr>\r\n        <tr (click)=\"showOrganization(row)\"\r\n            *matRowDef=\"let row; columns: visibleColumns;\"\r\n            @fadeInUp\r\n            class=\"hover:bg-hover trans-ease-out cursor-pointer\"\r\n            mat-row></tr>\r\n      </table>\r\n\r\n      <mat-paginator\r\n        [pageSizeOptions]=\"pageSizeOptions\"\r\n        [pageSize]=\"pageSize\"\r\n        [pageIndex]=\"pageIndex\"\r\n        (page)=\"onPaginateChange($event)\"\r\n        class=\"sticky left-0\">\r\n      </mat-paginator>\r\n    </div>\r\n\r\n  </div>\r\n\r\n</vex-page-layout>\r\n\r\n<mat-menu #columnFilterMenu=\"matMenu\" xPosition=\"before\" yPosition=\"below\">\r\n  <button (click)=\"toggleColumnVisibility(column, $event)\" *ngFor=\"let column of columns\"\r\n          class=\"checkbox-item mat-menu-item\">\r\n    <mat-checkbox (click)=\"$event.stopPropagation()\" [(ngModel)]=\"column.visible\" color=\"primary\">\r\n      {{ column.label }}\r\n    </mat-checkbox>\r\n  </button>\r\n</mat-menu>\r\n\r\n<mat-menu #actionsMenu=\"matMenu\" xPosition=\"before\" yPosition=\"below\">\r\n  <ng-template let-organization=\"organization\" matMenuContent>\r\n    <button (click)=\"destroyOrganizationsUser(organization)\" mat-menu-item>\r\n      <mat-icon [icIcon]=\"icons.icDelete\"></mat-icon>\r\n      <span>Delete</span>\r\n    </button>\r\n  </ng-template>\r\n</mat-menu>\r\n\r\n<mat-menu #categoryMenu=\"matMenu\" xPosition=\"after\" yPosition=\"below\">\r\n  <ng-template let-organization=\"organization\" matMenuContent>\r\n    <button mat-menu-item\r\n      *ngFor=\"let name of organizationsUserRoleData.roleTitles\"\r\n      (click)=\"updateOrganizationsUser(organization, {role: organizationsUserRoleData.titleRolesMap[name] })\">\r\n      {{ name  }}\r\n    </button>\r\n  </ng-template>\r\n</mat-menu>\r\n");

/***/ }),

/***/ "0+D7":
/*!*************************************************************************!*\
  !*** ./src/app/modules/users/pages/user-profile/user-profile.module.ts ***!
  \*************************************************************************/
/*! exports provided: UserProfileModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserProfileModule", function() { return UserProfileModule; });
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
/* harmony import */ var ngx_avatar__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ngx-avatar */ "UTQ3");
/* harmony import */ var _user_profile_component__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./user-profile.component */ "M3w4");












let UserProfileModule = class UserProfileModule {
};
UserProfileModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_user_profile_component__WEBPACK_IMPORTED_MODULE_11__["UserProfileComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_8__["PageLayoutModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_9__["IconModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_4__["MatButtonModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_6__["MatIconModule"],
            _angular_material_core__WEBPACK_IMPORTED_MODULE_5__["MatRippleModule"],
            _angular_router__WEBPACK_IMPORTED_MODULE_7__["RouterModule"],
            ngx_avatar__WEBPACK_IMPORTED_MODULE_10__["AvatarModule"],
        ],
    })
], UserProfileModule);



/***/ }),

/***/ "5Uws":
/*!****************************************************************************!*\
  !*** ./src/app/modules/users/pages/user-billing/user-billing.component.ts ***!
  \****************************************************************************/
/*! exports provided: UserBillingComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserBillingComponent", function() { return UserBillingComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_user_billing_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./user-billing.component.html */ "LjFg");
/* harmony import */ var _user_billing_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./user-billing.component.scss */ "zREC");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _vex_animations__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @vex/animations */ "ORuP");
/* harmony import */ var _data_schema__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @data/schema */ "V99k");
/* harmony import */ var _layout_services_layout_config_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @layout/services/layout-config.service */ "U9Lm");
/* harmony import */ var _users_services_user_data_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @users/services/user-data.service */ "O7ya");
/* harmony import */ var _services_user_billing_icons_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./services/user-billing-icons.service */ "AzF1");










let UserBillingComponent = class UserBillingComponent {
    constructor(icons, layoutConfigService, route, router, userDataService) {
        this.icons = icons;
        this.layoutConfigService = layoutConfigService;
        this.route = route;
        this.router = router;
        this.userDataService = userDataService;
        this.cardData = {
            network: 'visa',
            last4: 1234,
            name: 'John Doe',
            expDate: '12/21',
            background: 'https://url.to.background.image',
        };
        this.layoutConfigService.setIkaros();
    }
    ngOnInit() {
        this.payments = this.route.snapshot.data.payments;
        this.paymentMethods = this.route.snapshot.data.paymentMethods
            .map(paymentMethod => {
            return new _data_schema__WEBPACK_IMPORTED_MODULE_6__["PaymentMethod"](paymentMethod);
        })
            .sort((a, b) => {
            if (b.isDefault) {
                return 1;
            }
            if (!b.isDefault) {
                return -1;
            }
            return 0;
        });
        this.subscription = this.route.snapshot.data.subscription;
        this.userDataService.user$.subscribe(user => {
            this.user = user;
        });
    }
    scenariosPath() {
        return '/scenarios';
    }
    // projectQueryParams(project) {
    //   return {
    //     project_id: project.id
    //   };
    // }
    update() {
        const path = '/subscriptions/pricing';
        this.router.navigate([path], {
            queryParams: { organization_id: this.subscription.organization_id },
        });
    }
    onPaymentMethodRemove(paymentMethodId) {
        const newPaymentMethods = this.paymentMethods.slice();
        newPaymentMethods.splice(this.paymentMethods.findIndex((paymentMethod) => {
            return paymentMethod.id === paymentMethodId;
        }), 1);
        this.paymentMethods = newPaymentMethods;
    }
    ngOnDestroy() {
        this.layoutConfigService.setZeus();
    }
};
UserBillingComponent.ctorParameters = () => [
    { type: _services_user_billing_icons_service__WEBPACK_IMPORTED_MODULE_9__["UserBillingIcons"] },
    { type: _layout_services_layout_config_service__WEBPACK_IMPORTED_MODULE_7__["LayoutConfigService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["ActivatedRoute"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["Router"] },
    { type: _users_services_user_data_service__WEBPACK_IMPORTED_MODULE_8__["UserDataService"] }
];
UserBillingComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'user-billing',
        template: _raw_loader_user_billing_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        animations: [
            _vex_animations__WEBPACK_IMPORTED_MODULE_5__["fadeInUp400ms"],
            _vex_animations__WEBPACK_IMPORTED_MODULE_5__["fadeInRight400ms"],
            _vex_animations__WEBPACK_IMPORTED_MODULE_5__["scaleIn400ms"],
            _vex_animations__WEBPACK_IMPORTED_MODULE_5__["stagger40ms"],
        ],
        styles: [_user_billing_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], UserBillingComponent);



/***/ }),

/***/ "5xsu":
/*!**************************************************!*\
  !*** ./src/app/modules/users/users.component.ts ***!
  \**************************************************/
/*! exports provided: UsersComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UsersComponent", function() { return UsersComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_users_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./users.component.html */ "ewzc");
/* harmony import */ var _users_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./users.component.scss */ "73MK");
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
/* harmony import */ var _users_services_user_data_service__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @users/services/user-data.service */ "O7ya");















let UsersComponent = class UsersComponent {
    constructor(route, userDataService) {
        this.route = route;
        this.userDataService = userDataService;
        this.links = [
            {
                label: 'PROFILE',
                route: 'profile',
                active: () => this.isActive('profile'),
            },
            {
                label: 'ORGANIZATIONS',
                route: 'organizations',
                active: () => this.isActive('organization'),
            },
            {
                label: 'BILLING',
                route: 'billing',
                disabled: false,
                active: () => this.isActive('billing'),
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
        this.user = this.route.snapshot.data.user;
        this.userDataService.set(this.user);
    }
    isActive(path) {
        return this.route.firstChild.routeConfig.path === path;
    }
};
UsersComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["ActivatedRoute"] },
    { type: _users_services_user_data_service__WEBPACK_IMPORTED_MODULE_14__["UserDataService"] }
];
UsersComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'vex-users',
        template: _raw_loader_users_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        animations: [
            _vex_animations__WEBPACK_IMPORTED_MODULE_13__["fadeInUp400ms"],
            _vex_animations__WEBPACK_IMPORTED_MODULE_13__["fadeInRight400ms"],
            _vex_animations__WEBPACK_IMPORTED_MODULE_13__["scaleIn400ms"],
            _vex_animations__WEBPACK_IMPORTED_MODULE_13__["stagger40ms"],
        ],
        styles: [_users_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], UsersComponent);



/***/ }),

/***/ "73MK":
/*!****************************************************!*\
  !*** ./src/app/modules/users/users.component.scss ***!
  \****************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJ1c2Vycy5jb21wb25lbnQuc2NzcyJ9 */");

/***/ }),

/***/ "7is+":
/*!*******************************************************************************!*\
  !*** ./src/app/modules/users/services/user-organizations-resolver.service.ts ***!
  \*******************************************************************************/
/*! exports provided: UserOrganizationsResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserOrganizationsResolver", function() { return UserOrganizationsResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _core_http_organization_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @core/http/organization-resource.service */ "wjWB");



let UserOrganizationsResolver = class UserOrganizationsResolver {
    constructor(organizationResource) {
        this.organizationResource = organizationResource;
    }
    resolve(route) {
        return this.organizationResource.index({ roles: true });
    }
};
UserOrganizationsResolver.ctorParameters = () => [
    { type: _core_http_organization_resource_service__WEBPACK_IMPORTED_MODULE_2__["OrganizationResource"] }
];
UserOrganizationsResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], UserOrganizationsResolver);



/***/ }),

/***/ "88Va":
/*!*****************************************************************************************!*\
  !*** ./src/app/modules/users/pages/user-profile/services/user-profile-icons.service.ts ***!
  \*****************************************************************************************/
/*! exports provided: UserProfileIcons */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserProfileIcons", function() { return UserProfileIcons; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _iconify_icons_ic_twotone_access_time__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @iconify/icons-ic/twotone-access-time */ "NBim");
/* harmony import */ var _iconify_icons_ic_twotone_access_time__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_access_time__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @iconify/icons-ic/twotone-add */ "7wwx");
/* harmony import */ var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _iconify_icons_ic_twotone_check__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @iconify/icons-ic/twotone-check */ "+tDV");
/* harmony import */ var _iconify_icons_ic_twotone_check__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_check__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @iconify/icons-ic/twotone-mail */ "6qw8");
/* harmony import */ var _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _iconify_icons_ic_twotone_person_add__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @iconify/icons-ic/twotone-person-add */ "+q50");
/* harmony import */ var _iconify_icons_ic_twotone_person_add__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_person_add__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @iconify/icons-ic/twotone-phone */ "YA1h");
/* harmony import */ var _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _iconify_icons_ic_twotone_whatshot__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @iconify/icons-ic/twotone-whatshot */ "OcYv");
/* harmony import */ var _iconify_icons_ic_twotone_whatshot__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_whatshot__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _iconify_icons_ic_twotone_work__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @iconify/icons-ic/twotone-work */ "6W+F");
/* harmony import */ var _iconify_icons_ic_twotone_work__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_work__WEBPACK_IMPORTED_MODULE_9__);










let UserProfileIcons = class UserProfileIcons {
    constructor() {
        this.icWork = _iconify_icons_ic_twotone_work__WEBPACK_IMPORTED_MODULE_9___default.a;
        this.icPhone = _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_7___default.a;
        this.icPersonAdd = _iconify_icons_ic_twotone_person_add__WEBPACK_IMPORTED_MODULE_6___default.a;
        this.icCheck = _iconify_icons_ic_twotone_check__WEBPACK_IMPORTED_MODULE_4___default.a;
        this.icMail = _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_5___default.a;
        this.icAccessTime = _iconify_icons_ic_twotone_access_time__WEBPACK_IMPORTED_MODULE_2___default.a;
        this.icAdd = _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_3___default.a;
        this.icWhatshot = _iconify_icons_ic_twotone_whatshot__WEBPACK_IMPORTED_MODULE_8___default.a;
    }
};
UserProfileIcons.ctorParameters = () => [];
UserProfileIcons = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], UserProfileIcons);



/***/ }),

/***/ "AzF1":
/*!*****************************************************************************************!*\
  !*** ./src/app/modules/users/pages/user-billing/services/user-billing-icons.service.ts ***!
  \*****************************************************************************************/
/*! exports provided: UserBillingIcons */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserBillingIcons", function() { return UserBillingIcons; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _iconify_icons_ic_twotone_access_time__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @iconify/icons-ic/twotone-access-time */ "NBim");
/* harmony import */ var _iconify_icons_ic_twotone_access_time__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_access_time__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @iconify/icons-ic/twotone-add */ "7wwx");
/* harmony import */ var _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _iconify_icons_ic_twotone_check__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @iconify/icons-ic/twotone-check */ "+tDV");
/* harmony import */ var _iconify_icons_ic_twotone_check__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_check__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @iconify/icons-ic/twotone-mail */ "6qw8");
/* harmony import */ var _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _iconify_icons_ic_twotone_person_add__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @iconify/icons-ic/twotone-person-add */ "+q50");
/* harmony import */ var _iconify_icons_ic_twotone_person_add__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_person_add__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @iconify/icons-ic/twotone-phone */ "YA1h");
/* harmony import */ var _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _iconify_icons_ic_twotone_whatshot__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @iconify/icons-ic/twotone-whatshot */ "OcYv");
/* harmony import */ var _iconify_icons_ic_twotone_whatshot__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_whatshot__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _iconify_icons_ic_twotone_work__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @iconify/icons-ic/twotone-work */ "6W+F");
/* harmony import */ var _iconify_icons_ic_twotone_work__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_work__WEBPACK_IMPORTED_MODULE_9__);










let UserBillingIcons = class UserBillingIcons {
    constructor() {
        this.icWork = _iconify_icons_ic_twotone_work__WEBPACK_IMPORTED_MODULE_9___default.a;
        this.icPhone = _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_7___default.a;
        this.icPersonAdd = _iconify_icons_ic_twotone_person_add__WEBPACK_IMPORTED_MODULE_6___default.a;
        this.icCheck = _iconify_icons_ic_twotone_check__WEBPACK_IMPORTED_MODULE_4___default.a;
        this.icMail = _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_5___default.a;
        this.icAccessTime = _iconify_icons_ic_twotone_access_time__WEBPACK_IMPORTED_MODULE_2___default.a;
        this.icAdd = _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_3___default.a;
        this.icWhatshot = _iconify_icons_ic_twotone_whatshot__WEBPACK_IMPORTED_MODULE_8___default.a;
    }
};
UserBillingIcons.ctorParameters = () => [];
UserBillingIcons = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], UserBillingIcons);



/***/ }),

/***/ "BJHQ":
/*!***********************************************!*\
  !*** ./src/app/modules/users/users.module.ts ***!
  \***********************************************/
/*! exports provided: UsersModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UsersModule", function() { return UsersModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_material_core__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/core */ "UhP/");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _angular_material_tabs__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/tabs */ "M9ds");
/* harmony import */ var _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @vex/components/page-layout/page-layout.module */ "7lCJ");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var ngx_avatar__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ngx-avatar */ "UTQ3");
/* harmony import */ var _pages_user_billing_user_billing_module__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./pages/user-billing/user-billing.module */ "bxD3");
/* harmony import */ var _pages_user_organizations_user_organizations_module__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./pages/user-organizations/user-organizations.module */ "ROqT");
/* harmony import */ var _pages_user_profile_user_profile_module__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./pages/user-profile/user-profile.module */ "0+D7");
/* harmony import */ var _users_routing_module__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./users-routing.module */ "Voqh");
/* harmony import */ var _users_component__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ./users.component */ "5xsu");
















let UsersModule = class UsersModule {
};
UsersModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_users_component__WEBPACK_IMPORTED_MODULE_15__["UsersComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_8__["PageLayoutModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _angular_material_tabs__WEBPACK_IMPORTED_MODULE_7__["MatTabsModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_9__["IconModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_4__["MatButtonModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_6__["MatIconModule"],
            _angular_material_core__WEBPACK_IMPORTED_MODULE_5__["MatRippleModule"],
            ngx_avatar__WEBPACK_IMPORTED_MODULE_10__["AvatarModule"],
            _users_routing_module__WEBPACK_IMPORTED_MODULE_14__["UsersRoutingModule"],
            _pages_user_profile_user_profile_module__WEBPACK_IMPORTED_MODULE_13__["UserProfileModule"],
            _pages_user_organizations_user_organizations_module__WEBPACK_IMPORTED_MODULE_12__["UserOrganizationsModule"],
            _pages_user_billing_user_billing_module__WEBPACK_IMPORTED_MODULE_11__["UserBillingModule"],
        ],
    })
], UsersModule);



/***/ }),

/***/ "LjFg":
/*!********************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/users/pages/user-billing/user-billing.component.html ***!
  \********************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div class=\"mt-6\"\n     fxLayout=\"row\"\n     fxLayout.lt-md=\"column\"\n     fxLayoutAlign=\"start start\"\n     fxLayoutAlign.lt-md=\"start stretch\"\n     fxLayoutGap=\"24px\">\n  <div fxFlex=\"calc(70% - 12px)\" fxFlex.lt-md=\"auto\">\n    <div class=\"card\">\n      <div class=\"px-gutter py-4 border-b\">\n        <h2 class=\"title m-0\">Information</h2>\n      </div>\n\n      <div class=\"px-gutter py-4\" gdColumns=\"1fr 1fr\" gdColumns.xs=\"1fr\" gdGap=\"16px\">\n        <div class=\"py-3\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n          <div @scaleIn\n               class=\"w-10 h-10 rounded-full bg-primary-50 text-primary-500 ltr:mr-3 rtl:ml-3 flex items-center justify-center\">\n            <ic-icon [icon]=\"icons.icMail\" size=\"20px\"></ic-icon>\n          </div>\n\n          <div @fadeInRight>\n            <p class=\"m-0 body-1\">$0</p>\n            <p class=\"m-0 caption text-hint\">Current Monthly Billing</p>\n          </div>\n        </div>\n\n        <div class=\"py-3\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n          <div @scaleIn\n               class=\"w-10 h-10 rounded-full bg-primary-50 text-primary-500 ltr:mr-3 rtl:ml-3 flex items-center justify-center\">\n            <ic-icon [icon]=\"icons.icAccessTime\" size=\"20px\"></ic-icon>\n          </div>\n\n          <div @fadeInRight>\n            <p class=\"m-0 body-1\">N/A</p>\n            <p class=\"m-0 caption text-hint\">Next payment due</p>\n          </div>\n        </div>\n\n        <!-- <div class=\"py-3\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n          <div @scaleIn\n               class=\"w-10 h-10 rounded-full bg-gray-50 text-dark ltr:mr-3 rtl:ml-3 cursor-pointer flex items-center justify-center\">\n            <ic-icon [icon]=\"icons.icAdd\" size=\"20px\"></ic-icon>\n          </div>\n\n          <p @fadeInRight class=\"m-0 body-1 cursor-pointer\">Add an address</p>\n        </div>\n\n        <div class=\"py-3\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n          <div @scaleIn\n               class=\"w-10 h-10 rounded-full bg-gray-50 text-dark ltr:mr-3 rtl:ml-3 cursor-pointer flex items-center justify-center\">\n            <ic-icon [icon]=\"icons.icWhatshot\" size=\"20px\"></ic-icon>\n          </div>\n\n          <p @fadeInRight class=\"m-0 body-1 cursor-pointer\">Add social profiles</p>\n        </div> -->\n      </div>\n    </div>\n\n    <div class=\"card mt-6\">\n      <div class=\"px-gutter py-4 border-b\">\n        <h2 class=\"title m-0\">Payment History</h2>\n      </div>\n\n      <div class=\"px-gutter py-4\" *ngIf=\"!payments.length\">\n        No payments found\n      </div>\n\n      <div class=\"mt-3\" *ngFor=\"let payment of payments\">\n        <payment-history [data]=\"payment\"></payment-history>\n      </div>\n    </div>\n  </div>\n\n  <div fxFlex=\"calc(30% - 12px)\" fxFlex.lt-md=\"auto\">\n    <div class=\"card px-6 pb-5\">\n      <div \n        class=\"border-b py-3\"\n        fxLayout=\"row\"\n        fxLayoutAlign=\"space-between center\"\n      >\n        <h2 class=\"title m-0\">Subscription Plan</h2>\n        <button\n          class=\"max-w-full w-200\"\n          color=\"primary\"\n          mat-button type=\"button\"\n          (click)=\"update()\">\n          UPDATE\n        </button>\n      </div>\n\n       <div @stagger class=\"py-4\" fxLayout=\"column\" fxLayoutGap=\"16px\">\n         <div\n           *ngIf=\"!subscription\"\n           fxFlex=\"auto\"\n           fxLayout=\"column\"\n           fxLayoutAlign=\"center center\">\n           <img class=\"m-8\" src=\"assets/img/illustrations/idea.svg\">\n          </div>\n\n          <div *ngIf=\"subscription\">\n            <p class=\"m-0 body-1\">{{ subscription.plan.name }}</p>\n            <p class=\"m-0 caption text-hint\">{{ subscription.plan.description }}</p>\n          </div>\n       </div>\n    </div>\n\n    <div class=\"card mt-6 px-6 pb-4\">\n      <payment-methods-list\n        [enableCreateCard]=\"true\"\n        [paymentMethods]=\"paymentMethods\" \n      >\n      </payment-methods-list>\n    </div>\n  </div>\n\n</div>\n");

/***/ }),

/***/ "M3w4":
/*!****************************************************************************!*\
  !*** ./src/app/modules/users/pages/user-profile/user-profile.component.ts ***!
  \****************************************************************************/
/*! exports provided: UserProfileComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserProfileComponent", function() { return UserProfileComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_user_profile_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./user-profile.component.html */ "wDRm");
/* harmony import */ var _user_profile_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./user-profile.component.scss */ "kP3r");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _vex_animations__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @vex/animations */ "ORuP");
/* harmony import */ var _layout_services_layout_config_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @layout/services/layout-config.service */ "U9Lm");
/* harmony import */ var _users_services_user_data_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @users/services/user-data.service */ "O7ya");
/* harmony import */ var _services_user_profile_icons_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./services/user-profile-icons.service */ "88Va");









let UserProfileComponent = class UserProfileComponent {
    constructor(icons, layoutConfigService, route, router, userDataService) {
        this.icons = icons;
        this.layoutConfigService = layoutConfigService;
        this.route = route;
        this.router = router;
        this.userDataService = userDataService;
        this.layoutConfigService.setIkaros();
    }
    ngOnInit() {
        this.projects = this.route.snapshot.data.projects;
        this.userDataService.user$.subscribe(user => {
            this.user = user;
        });
    }
    scenariosPath() {
        return '/scenarios';
    }
    projectQueryParams(project) {
        return {
            project_id: project.id,
        };
    }
    ngOnDestroy() {
        this.layoutConfigService.setZeus();
    }
};
UserProfileComponent.ctorParameters = () => [
    { type: _services_user_profile_icons_service__WEBPACK_IMPORTED_MODULE_8__["UserProfileIcons"] },
    { type: _layout_services_layout_config_service__WEBPACK_IMPORTED_MODULE_6__["LayoutConfigService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["ActivatedRoute"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["Router"] },
    { type: _users_services_user_data_service__WEBPACK_IMPORTED_MODULE_7__["UserDataService"] }
];
UserProfileComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'user-profile',
        template: _raw_loader_user_profile_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        animations: [
            _vex_animations__WEBPACK_IMPORTED_MODULE_5__["fadeInUp400ms"],
            _vex_animations__WEBPACK_IMPORTED_MODULE_5__["fadeInRight400ms"],
            _vex_animations__WEBPACK_IMPORTED_MODULE_5__["scaleIn400ms"],
            _vex_animations__WEBPACK_IMPORTED_MODULE_5__["stagger40ms"],
        ],
        styles: [_user_profile_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], UserProfileComponent);



/***/ }),

/***/ "Pomz":
/*!*****************************************************************************************************!*\
  !*** ./src/app/modules/users/pages/user-organizations/services/user-organizations-icons.service.ts ***!
  \*****************************************************************************************************/
/*! exports provided: UserOrganizationsIcons */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserOrganizationsIcons", function() { return UserOrganizationsIcons; });
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







let UserOrganizationsIcons = class UserOrganizationsIcons {
    constructor() {
        this.icSearch = _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_6___default.a;
        this.icDelete = _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_3___default.a;
        this.icAdd = _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_2___default.a;
        this.icFilterList = _iconify_icons_ic_twotone_filter_list__WEBPACK_IMPORTED_MODULE_4___default.a;
        this.icMoreHoriz = _iconify_icons_ic_twotone_more_horiz__WEBPACK_IMPORTED_MODULE_5___default.a;
    }
};
UserOrganizationsIcons.ctorParameters = () => [];
UserOrganizationsIcons = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])()
], UserOrganizationsIcons);



/***/ }),

/***/ "ROqT":
/*!*************************************************************************************!*\
  !*** ./src/app/modules/users/pages/user-organizations/user-organizations.module.ts ***!
  \*************************************************************************************/
/*! exports provided: UserOrganizationsModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserOrganizationsModule", function() { return UserOrganizationsModule; });
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
/* harmony import */ var _organizations_components_organizations_create_organizations_create_module__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! @organizations/components/organizations-create/organizations-create.module */ "KUDd");
/* harmony import */ var _shared_shared_module__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! @shared/shared.module */ "PCNd");
/* harmony import */ var _services_user_organizations_icons_service__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! ./services/user-organizations-icons.service */ "Pomz");
/* harmony import */ var _user_organizations_component__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! ./user-organizations.component */ "UfMC");
























let UserOrganizationsModule = class UserOrganizationsModule {
};
UserOrganizationsModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_user_organizations_component__WEBPACK_IMPORTED_MODULE_23__["UserOrganizationsComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_16__["PageLayoutModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _vex_components_breadcrumbs_breadcrumbs_module__WEBPACK_IMPORTED_MODULE_15__["BreadcrumbsModule"],
            _organizations_components_organizations_create_organizations_create_module__WEBPACK_IMPORTED_MODULE_20__["OrganizationsCreateModule"],
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
            _shared_shared_module__WEBPACK_IMPORTED_MODULE_21__["SharedModule"],
        ],
        providers: [_services_user_organizations_icons_service__WEBPACK_IMPORTED_MODULE_22__["UserOrganizationsIcons"]],
    })
], UserOrganizationsModule);



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

/***/ "UfMC":
/*!****************************************************************************************!*\
  !*** ./src/app/modules/users/pages/user-organizations/user-organizations.component.ts ***!
  \****************************************************************************************/
/*! exports provided: UserOrganizationsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserOrganizationsComponent", function() { return UserOrganizationsComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _raw_loader_user_organizations_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! raw-loader!./user-organizations.component.html */ "+Ntf");
/* harmony import */ var _user_organizations_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./user-organizations.component.scss */ "qpMz");
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
/* harmony import */ var _core_http_organization_resource_service__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @core/http/organization-resource.service */ "wjWB");
/* harmony import */ var _core_http_organizations_user_resource_service__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @core/http/organizations-user-resource.service */ "YCZM");
/* harmony import */ var _core_utils_file_service__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @core/utils/file.service */ "EGFe");
/* harmony import */ var _data_schema__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @data/schema */ "V99k");
/* harmony import */ var _organizations_components_organizations_create_organizations_create_component__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! @organizations/components/organizations-create/organizations-create.component */ "vb3d");
/* harmony import */ var _users_services_user_data_service__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! @users/services/user-data.service */ "O7ya");
/* harmony import */ var _layout_services_layout_config_service__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! @layout/services/layout-config.service */ "U9Lm");
/* harmony import */ var _mock_user_organizations_data__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! ./mock/user-organizations-data */ "hbMq");
/* harmony import */ var _services_organizations_user_role_data_service__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! ./services/organizations-user-role-data.service */ "rDXh");
/* harmony import */ var _services_user_organizations_data_service__WEBPACK_IMPORTED_MODULE_24__ = __webpack_require__(/*! ./services/user-organizations-data.service */ "kmx+");
/* harmony import */ var _services_user_organizations_icons_service__WEBPACK_IMPORTED_MODULE_25__ = __webpack_require__(/*! ./services/user-organizations-icons.service */ "Pomz");


























let UserOrganizationsComponent = class UserOrganizationsComponent {
    constructor(icons, organizationsUserRoleData, activatedRoute, dialog, file, layoutConfigService, location, organizationResource, organizationsUserResource, router, route, userOrganizationsData, userDataService) {
        this.icons = icons;
        this.organizationsUserRoleData = organizationsUserRoleData;
        this.activatedRoute = activatedRoute;
        this.dialog = dialog;
        this.file = file;
        this.layoutConfigService = layoutConfigService;
        this.location = location;
        this.organizationResource = organizationResource;
        this.organizationsUserResource = organizationsUserResource;
        this.router = router;
        this.route = route;
        this.userOrganizationsData = userOrganizationsData;
        this.userDataService = userDataService;
        this.layoutCtrl = new _angular_forms__WEBPACK_IMPORTED_MODULE_6__["FormControl"]('boxed');
        // Table settings
        this.columns = [
            { label: 'Role', property: 'currentUserRole', type: 'text', visible: true },
            { label: 'Name', property: 'name', type: 'text', visible: true },
            { label: 'Description', property: 'description', type: 'text', visible: true },
            { label: 'Leave', property: 'button', type: 'button', visible: true, onclick: ($event, organization) => {
                    $event.stopPropagation();
                    this.destroyOrganizationsUser(organization);
                },
            },
        ];
        this.pageIndex = this.route.snapshot.queryParams.page || 0;
        this.pageSize = 10;
        this.pageSizeOptions = [5, 10, 20, 50];
        this.selection = new _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_3__["SelectionModel"](true, []);
        this.searchCtrl = new _angular_forms__WEBPACK_IMPORTED_MODULE_6__["FormControl"]();
        this.labels = _mock_user_organizations_data__WEBPACK_IMPORTED_MODULE_22__["aioTableLabels"];
        this.layoutConfigService.setIkaros();
    }
    get visibleColumns() {
        return this.columns.filter(column => column.visible).map(column => column.property);
    }
    ngOnInit() {
        this.dataSource = new _angular_material_table__WEBPACK_IMPORTED_MODULE_11__["MatTableDataSource"]();
        this.userOrganizationsData.organizations$.subscribe(curOrganizations => {
            this.dataSource.data = curOrganizations;
        });
        const organizations = this.route.snapshot.data.organizations.filter(organization => {
            return !organization.isShadow;
        }).map(organization => {
            const o = new _data_schema__WEBPACK_IMPORTED_MODULE_18__["Organization"](organization);
            o.currentUserRole = this.organizationsUserRoleData.getRoleTitle(o.currentUserRole);
            return o;
        });
        this.userOrganizationsData.set(organizations);
        this.searchCtrl.valueChanges.pipe(Object(ngx_take_until_destroy__WEBPACK_IMPORTED_MODULE_13__["untilDestroyed"])(this)).subscribe(value => this.onFilterChange(value));
        this.userDataService.user$.subscribe(user => {
            this.user = user;
        });
    }
    ngAfterViewInit() {
        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
    }
    getOrganizations(params) {
        this.organizationResource.index(params).subscribe((organization) => {
            const o = new _data_schema__WEBPACK_IMPORTED_MODULE_18__["Organization"](organization);
            o.currentUserRole = this.organizationsUserRoleData.getRoleTitle(o.currentUserRole);
            this.userOrganizationsData.add(o);
        }, error => {
        });
    }
    createOrganization(data) {
        this.organizationResource.create(data).subscribe((organization) => {
            this.userOrganizationsData.add(organization);
        }, error => {
        });
    }
    showOrganization(organization) {
        const path = this.file.join('/', 'organizations', organization.id, 'settings');
        const snapshot = this.route.snapshot;
        this.router.navigate([path]);
    }
    updateOrganizationsUser(organization, params) {
        this.organizationsUserResource.update(organization.id, this.user.id, params).subscribe(res => {
            // TODO: Update view iwth new role
        });
    }
    destroyOrganizationsUsers(organizations) {
        organizations.forEach(organization => {
            this.destroyOrganizationsUser(organization);
        });
    }
    destroyOrganizationsUser(organization) {
        this.organizationsUserResource.destroy(organization.id, this.user.id).subscribe(res => {
            this.userOrganizationsData.delete(organization.id);
            this.selection.deselect(organization);
        });
    }
    /**
     *
     * Table methods
     *
     */
    openCreateDialog() {
        const dialogRef = this.dialog.open(_organizations_components_organizations_create_organizations_create_component__WEBPACK_IMPORTED_MODULE_19__["OrganizationsCreateComponent"], {
            width: '600px',
        });
        const onCreateSub = dialogRef.componentInstance.onCreate.subscribe(($event) => {
            this.createOrganization($event);
        });
        dialogRef.afterClosed().subscribe((organization) => {
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
    /** On page change, add queryParam 'page' to URL */
    onPaginateChange($event) {
        const queryParams = Object.assign({}, this.route.snapshot.queryParams);
        queryParams.page = $event.pageIndex;
        const url = this
            .router
            .createUrlTree([], { relativeTo: this.activatedRoute, queryParams })
            .toString();
        this.location.go(url);
    }
    ngOnDestroy() {
        this.layoutConfigService.setZeus();
    }
};
UserOrganizationsComponent.ctorParameters = () => [
    { type: _services_user_organizations_icons_service__WEBPACK_IMPORTED_MODULE_25__["UserOrganizationsIcons"] },
    { type: _services_organizations_user_role_data_service__WEBPACK_IMPORTED_MODULE_23__["OrganizationsUserRoleData"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_12__["ActivatedRoute"] },
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_7__["MatDialog"] },
    { type: _core_utils_file_service__WEBPACK_IMPORTED_MODULE_17__["FileService"] },
    { type: _layout_services_layout_config_service__WEBPACK_IMPORTED_MODULE_21__["LayoutConfigService"] },
    { type: _angular_common__WEBPACK_IMPORTED_MODULE_4__["Location"] },
    { type: _core_http_organization_resource_service__WEBPACK_IMPORTED_MODULE_15__["OrganizationResource"] },
    { type: _core_http_organizations_user_resource_service__WEBPACK_IMPORTED_MODULE_16__["OrganizationsUserResource"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_12__["Router"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_12__["ActivatedRoute"] },
    { type: _services_user_organizations_data_service__WEBPACK_IMPORTED_MODULE_24__["UserOrganizationsData"] },
    { type: _users_services_user_data_service__WEBPACK_IMPORTED_MODULE_20__["UserDataService"] }
];
UserOrganizationsComponent.propDecorators = {
    columns: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_5__["Input"] }],
    paginator: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_5__["ViewChild"], args: [_angular_material_paginator__WEBPACK_IMPORTED_MODULE_9__["MatPaginator"], { static: true },] }],
    sort: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_5__["ViewChild"], args: [_angular_material_sort__WEBPACK_IMPORTED_MODULE_10__["MatSort"], { static: true },] }]
};
UserOrganizationsComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_5__["Component"])({
        selector: 'user-organizations',
        template: _raw_loader_user_organizations_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
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
        styles: [_user_organizations_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
    })
], UserOrganizationsComponent);



/***/ }),

/***/ "UpuO":
/*!**************************************************************************!*\
  !*** ./src/app/modules/users/services/user-payments-resolver.service.ts ***!
  \**************************************************************************/
/*! exports provided: UserPaymentsResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserPaymentsResolver", function() { return UserPaymentsResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _core_http_user_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @core/http/user-resource.service */ "9IlP");



let UserPaymentsResolver = class UserPaymentsResolver {
    constructor(userResource) {
        this.userResource = userResource;
    }
    resolve(route) {
        return this.userResource.payments();
    }
};
UserPaymentsResolver.ctorParameters = () => [
    { type: _core_http_user_resource_service__WEBPACK_IMPORTED_MODULE_2__["UserResource"] }
];
UserPaymentsResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], UserPaymentsResolver);



/***/ }),

/***/ "Voqh":
/*!*******************************************************!*\
  !*** ./src/app/modules/users/users-routing.module.ts ***!
  \*******************************************************/
/*! exports provided: UsersRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UsersRoutingModule", function() { return UsersRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _organizations_services_organization_payment_methods_resolver_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @organizations/services/organization-payment-methods-resolver.service */ "Us/2");
/* harmony import */ var _projects_services_projects_resolver_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @projects/services/projects-resolver.service */ "yVsR");
/* harmony import */ var _pages_user_billing_user_billing_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./pages/user-billing/user-billing.component */ "5Uws");
/* harmony import */ var _pages_user_organizations_user_organizations_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./pages/user-organizations/user-organizations.component */ "UfMC");
/* harmony import */ var _pages_user_profile_user_profile_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./pages/user-profile/user-profile.component */ "M3w4");
/* harmony import */ var _services_user_organizations_resolver_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./services/user-organizations-resolver.service */ "7is+");
/* harmony import */ var _services_user_payments_resolver_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./services/user-payments-resolver.service */ "UpuO");
/* harmony import */ var _services_user_resolver_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./services/user-resolver.service */ "fmgd");
/* harmony import */ var _services_user_subscription_resolver_service__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./services/user-subscription-resolver.service */ "I9wA");
/* harmony import */ var _users_component__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./users.component */ "5xsu");













const routes = [
    {
        path: ':user_id',
        component: _users_component__WEBPACK_IMPORTED_MODULE_12__["UsersComponent"],
        data: {
            toolbarShadowEnabled: true,
            containerEnabled: true,
        },
        resolve: {
            user: _services_user_resolver_service__WEBPACK_IMPORTED_MODULE_10__["UserResolver"],
        },
        children: [
            {
                path: '',
                component: _pages_user_profile_user_profile_component__WEBPACK_IMPORTED_MODULE_7__["UserProfileComponent"],
                resolve: {
                    organizations: _services_user_organizations_resolver_service__WEBPACK_IMPORTED_MODULE_8__["UserOrganizationsResolver"],
                    projects: _projects_services_projects_resolver_service__WEBPACK_IMPORTED_MODULE_4__["ProjectsResolver"],
                },
            },
            {
                path: 'profile',
                component: _pages_user_profile_user_profile_component__WEBPACK_IMPORTED_MODULE_7__["UserProfileComponent"],
                resolve: {
                    organizations: _services_user_organizations_resolver_service__WEBPACK_IMPORTED_MODULE_8__["UserOrganizationsResolver"],
                    projects: _projects_services_projects_resolver_service__WEBPACK_IMPORTED_MODULE_4__["ProjectsResolver"],
                },
            },
            {
                path: 'organizations',
                component: _pages_user_organizations_user_organizations_component__WEBPACK_IMPORTED_MODULE_6__["UserOrganizationsComponent"],
                resolve: {
                    organizations: _services_user_organizations_resolver_service__WEBPACK_IMPORTED_MODULE_8__["UserOrganizationsResolver"],
                },
            },
            {
                path: 'billing',
                component: _pages_user_billing_user_billing_component__WEBPACK_IMPORTED_MODULE_5__["UserBillingComponent"],
                resolve: {
                    subscription: _services_user_subscription_resolver_service__WEBPACK_IMPORTED_MODULE_11__["UserSubscriptionResolver"],
                    payments: _services_user_payments_resolver_service__WEBPACK_IMPORTED_MODULE_9__["UserPaymentsResolver"],
                    paymentMethods: _organizations_services_organization_payment_methods_resolver_service__WEBPACK_IMPORTED_MODULE_3__["OrganizationPaymentMethodsResolver"],
                },
            },
        ],
    },
];
let UsersRoutingModule = class UsersRoutingModule {
};
UsersRoutingModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
    })
], UsersRoutingModule);



/***/ }),

/***/ "bxD3":
/*!*************************************************************************!*\
  !*** ./src/app/modules/users/pages/user-billing/user-billing.module.ts ***!
  \*************************************************************************/
/*! exports provided: UserBillingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserBillingModule", function() { return UserBillingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "SVse");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "u9T3");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/button */ "Dxy4");
/* harmony import */ var _angular_material_core__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/core */ "UhP/");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/icon */ "Tj54");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/router */ "iInd");
/* harmony import */ var _shared_components_payment_payment_history_payment_history_module__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @shared/components/payment/payment-history/payment-history.module */ "nziB");
/* harmony import */ var _shared_components_payment_payment_method_card__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @shared/components/payment/payment-method/card */ "VadD");
/* harmony import */ var _shared_components_payment_payment_method__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @shared/components/payment/payment-method */ "iX9L");
/* harmony import */ var _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @vex/components/page-layout/page-layout.module */ "7lCJ");
/* harmony import */ var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @visurel/iconify-angular */ "l+Q0");
/* harmony import */ var _user_billing_component__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./user-billing.component */ "5Uws");














let UserBillingModule = class UserBillingModule {
};
UserBillingModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_user_billing_component__WEBPACK_IMPORTED_MODULE_13__["UserBillingComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_4__["MatButtonModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_6__["MatIconModule"],
            _angular_material_core__WEBPACK_IMPORTED_MODULE_5__["MatRippleModule"],
            _angular_router__WEBPACK_IMPORTED_MODULE_7__["RouterModule"],
            _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_11__["PageLayoutModule"],
            _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_12__["IconModule"],
            _shared_components_payment_payment_history_payment_history_module__WEBPACK_IMPORTED_MODULE_8__["PaymentHistoryModule"],
            _shared_components_payment_payment_method_card__WEBPACK_IMPORTED_MODULE_9__["PaymentMethodCardModule"],
            _shared_components_payment_payment_method__WEBPACK_IMPORTED_MODULE_10__["PaymentMethodsListModule"],
        ],
    })
], UserBillingModule);



/***/ }),

/***/ "ewzc":
/*!******************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/users/users.component.html ***!
  \******************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div class=\"container py-gutter\">\n  <div class=\"card overflow-hidden\">\n    <div class=\"h-64 relative overflow-hidden\">\n      <img class=\"w-full object-cover\" src=\"assets/img/demo/landscape.jpg\">\n      <div class=\"absolute bg-contrast-black opacity-25 top-0 right-0 bottom-0 left-0 w-full h-full z-0\"></div>\n\n      <img class=\"avatar h-24 w-24 absolute top-6 left-4\"\n           fxFlex=\"none\"\n           fxFlexAlign=\"start\"\n           fxHide.gt-xs\n           src=\"assets/img/avatars/1.jpg\">\n    </div>\n\n    <div class=\"z-10 relative -mt-16 px-gutter\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n      \n     <ngx-avatar @scaleIn\n          class=\"avatar h-24 w-24\"\n          fxFlex=\"none\"\n          fxFlexAlign=\"start\"\n          fxHide.xs\n          name=\"{{user.name}}\"\n          size=\"100\">\n      </ngx-avatar>\n\n      <div [ngClass.gt-xs]=\"['ltr:ml-6 rtl:mr-6']\" class=\"max-w-full\" fxFlex=\"auto\">\n        <div class=\"h-16\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n          <h1 @fadeInRight class=\"headline text-contrast-white m-0\">{{ user.name }}</h1>\n        </div>\n\n        <nav class=\"vex-tabs vex-tabs-dense border-0\" mat-tab-nav-bar>\n          <a #rla=\"routerLinkActive\"\n             *ngFor=\"let link of links\"\n             [active]=\"rla.isActive\"\n             [disabled]=\"link.disabled\"\n             [routerLink]=\"link.route\"\n             mat-tab-link\n             queryParamsHandling=\"preserve\"\n             routerLinkActive>\n            {{ link.label }}\n          </a>\n        </nav>\n      </div>\n\n    </div>\n  </div>\n\n  <router-outlet></router-outlet>\n</div>\n");

/***/ }),

/***/ "fmgd":
/*!*****************************************************************!*\
  !*** ./src/app/modules/users/services/user-resolver.service.ts ***!
  \*****************************************************************/
/*! exports provided: UserResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserResolver", function() { return UserResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _core_http_user_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @core/http/user-resource.service */ "9IlP");



let UserResolver = class UserResolver {
    constructor(userResource) {
        this.userResource = userResource;
    }
    resolve(route) {
        return this.userResource.show(route.params.user_id);
    }
};
UserResolver.ctorParameters = () => [
    { type: _core_http_user_resource_service__WEBPACK_IMPORTED_MODULE_2__["UserResource"] }
];
UserResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], UserResolver);



/***/ }),

/***/ "hbMq":
/*!****************************************************************************************!*\
  !*** ./src/app/modules/users/pages/user-organizations/mock/user-organizations-data.ts ***!
  \****************************************************************************************/
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

/***/ "kP3r":
/*!******************************************************************************!*\
  !*** ./src/app/modules/users/pages/user-profile/user-profile.component.scss ***!
  \******************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJ1c2VyLXByb2ZpbGUuY29tcG9uZW50LnNjc3MifQ== */");

/***/ }),

/***/ "kmx+":
/*!****************************************************************************************************!*\
  !*** ./src/app/modules/users/pages/user-organizations/services/user-organizations-data.service.ts ***!
  \****************************************************************************************************/
/*! exports provided: UserOrganizationsData */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserOrganizationsData", function() { return UserOrganizationsData; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "qCKp");
/* harmony import */ var _data_schema_organization__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @data/schema/organization */ "7v+O");




let UserOrganizationsData = class UserOrganizationsData {
    constructor() {
        this.subject = new rxjs__WEBPACK_IMPORTED_MODULE_2__["BehaviorSubject"](null);
        this.organizations$ = this.subject.asObservable();
        this.organizations = [];
    }
    set(organizations) {
        this.organizations = organizations;
        this.subject.next(organizations);
    }
    add(organization) {
        this.organizations.unshift(new _data_schema_organization__WEBPACK_IMPORTED_MODULE_3__["Organization"](organization));
        this.set(this.organizations);
    }
    delete(id) {
        this.organizations.splice(this.organizations.findIndex((existingOrganization) => {
            return existingOrganization.id === id;
        }), 1);
        this.set(this.organizations);
    }
};
UserOrganizationsData.ctorParameters = () => [];
UserOrganizationsData = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], UserOrganizationsData);



/***/ }),

/***/ "qpMz":
/*!******************************************************************************************!*\
  !*** ./src/app/modules/users/pages/user-organizations/user-organizations.component.scss ***!
  \******************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (".table-container {\n  box-sizing: border-box;\n  display: block;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uLy4uL3VzZXItb3JnYW5pemF0aW9ucy5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLHNCQUFBO0VBQ0EsY0FBQTtBQUNGIiwiZmlsZSI6InVzZXItb3JnYW5pemF0aW9ucy5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbIi50YWJsZS1jb250YWluZXIge1xuICBib3gtc2l6aW5nOiBib3JkZXItYm94O1xuICBkaXNwbGF5OiBibG9jaztcbn0iXX0= */");

/***/ }),

/***/ "rDXh":
/*!*********************************************************************************************************!*\
  !*** ./src/app/modules/users/pages/user-organizations/services/organizations-user-role-data.service.ts ***!
  \*********************************************************************************************************/
/*! exports provided: OrganizationsUserRoleData */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "OrganizationsUserRoleData", function() { return OrganizationsUserRoleData; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "mrSG");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "8Y7J");
/* harmony import */ var _data_schema_organizations_user__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @data/schema/organizations-user */ "FKbl");



let OrganizationsUserRoleData = class OrganizationsUserRoleData {
    constructor() {
        this.roleTitlesMap = {};
        this.titleRolesMap = {};
        let titleKeys = Object.keys(_data_schema_organizations_user__WEBPACK_IMPORTED_MODULE_2__["OrganizationsUserRoleTitles"]);
        titleKeys = titleKeys.slice(titleKeys.length / 2);
        let roleKeys = Object.keys(_data_schema_organizations_user__WEBPACK_IMPORTED_MODULE_2__["OrganizationsUserRoles"]);
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
OrganizationsUserRoleData.ctorParameters = () => [];
OrganizationsUserRoleData = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], OrganizationsUserRoleData);



/***/ }),

/***/ "wDRm":
/*!********************************************************************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/users/pages/user-profile/user-profile.component.html ***!
  \********************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<div class=\"mt-6\"\n     fxLayout=\"row\"\n     fxLayout.lt-md=\"column\"\n     fxLayoutAlign=\"start start\"\n     fxLayoutAlign.lt-md=\"start stretch\"\n     fxLayoutGap=\"24px\">\n  <div fxFlex=\"calc(70% - 12px)\" fxFlex.lt-md=\"auto\">\n    <div class=\"card\">\n      <div class=\"px-gutter py-4 border-b\">\n        <h2 class=\"title m-0\">About</h2>\n      </div>\n\n      <div class=\"px-gutter py-4\" gdColumns=\"1fr 1fr\" gdColumns.xs=\"1fr\" gdGap=\"16px\">\n        <div class=\"py-3\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n          <div @scaleIn\n               class=\"w-10 h-10 rounded-full bg-primary-50 text-primary-500 ltr:mr-3 rtl:ml-3 flex items-center justify-center\">\n            <ic-icon [icon]=\"icons.icMail\" size=\"20px\"></ic-icon>\n          </div>\n\n          <div @fadeInRight>\n            <p class=\"m-0 body-1\">{{ user.email }}</p>\n            <p class=\"m-0 caption text-hint\">Email</p>\n          </div>\n        </div>\n\n        <div class=\"py-3\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n          <div @scaleIn\n               class=\"w-10 h-10 rounded-full bg-primary-50 text-primary-500 ltr:mr-3 rtl:ml-3 cursor-pointer flex items-center justify-center\">\n            <ic-icon [icon]=\"icons.icWhatshot\" size=\"20px\"></ic-icon>\n          </div>\n\n          <div @fadeInRight>\n            <p class=\"m-0 body-1\">{{ user.apiKey }}</p>\n            <p @fadeInRight class=\"m-0 caption text-hint\">API Key</p>\n          </div>\n        </div>\n\n\n        <div class=\"py-3\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n          <div @scaleIn\n               class=\"w-10 h-10 rounded-full bg-primary-50 text-primary-500 ltr:mr-3 rtl:ml-3 flex items-center justify-center\">\n            <ic-icon [icon]=\"icons.icAccessTime\" size=\"20px\"></ic-icon>\n          </div>\n\n          <div @fadeInRight>\n            <p class=\"m-0 body-1\">{{ user.lastSignInAt | date : 'short' }}</p>\n            <p class=\"m-0 caption text-hint\">Last Logged In</p>\n          </div>\n        </div>\n\n        <div class=\"py-3\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n          <div @scaleIn\n               class=\"w-10 h-10 rounded-full bg-primary-50 text-primary-500 ltr:mr-3 rtl:ml-3 flex items-center justify-center\">\n            <ic-icon [icon]=\"icons.icAccessTime\" size=\"20px\"></ic-icon>\n          </div>\n\n          <div @fadeInRight>\n            <p class=\"m-0 body-1\">{{ user.createdAt | date: 'short' }}</p>\n            <p @fadeInRight class=\"m-0 caption text-hint\">Member Since</p>\n          </div>\n        </div>\n      </div>\n    </div>\n\n    <div class=\"card mt-6\" *ngIf=\"projects.length > 0\">\n      <div class=\"px-gutter py-4 border-b\">\n        <h2 class=\"title m-0\">Projects</h2>\n      </div>\n\n      <div @stagger\n           class=\"px-gutter py-4\"\n           gdColumns=\"1fr 1fr 1fr 1fr\"\n           gdColumns.lt-lg=\"1fr 1fr 1fr\"\n           gdColumns.xs=\"1fr 1fr\"\n           gdGap=\"24px\">\n        <!-- <img *ngFor=\"let project of projects\"\n             @scaleIn\n             class=\"rounded w-full\"\n             gdGridAlign=\"center\"\n             src=\"assets/img/avatars/{{ i }}.jpg\"> -->\n         <div *ngFor=\"let project of projects\" gdGridAlign=\"left\" fxLayoutAlign=\"start center\">\n           <!-- <img @scaleIn [src]=\"project.imageSrc\" class=\"avatar ltr:mr-3 rtl:ml-3\" fxFlex=\"none\"> -->\n\n           <ngx-avatar @scaleIn\n              class=\"avatar ltr:mr-3 rtl:ml-3\"\n              name=\"{{project.name}}\"\n              size=\"41\">\n            </ngx-avatar>\n\n           <div @fadeInRight fxFlex=\"auto\">\n             <a class=\"body-2 m-0 leading-snug\"\n                [routerLink]=\"scenariosPath()\"\n                [queryParams]=\"projectQueryParams(project)\">\n               {{ project.name }}\n             </a>\n             <!-- <h5 class=\"text-secondary m-0 caption leading-none\">{{ project.updatedAt }}</h5> -->\n           </div>\n         </div>\n       </div>\n     </div>\n   </div>\n</div>\n");

/***/ }),

/***/ "zREC":
/*!******************************************************************************!*\
  !*** ./src/app/modules/users/pages/user-billing/user-billing.component.scss ***!
  \******************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJ1c2VyLWJpbGxpbmcuY29tcG9uZW50LnNjc3MifQ== */");

/***/ })

}]);
//# sourceMappingURL=users-users-module-es2015.js.map