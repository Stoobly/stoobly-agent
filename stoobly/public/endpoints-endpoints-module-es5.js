(function () {
  function _createForOfIteratorHelper(o, allowArrayLike) { var it; if (typeof Symbol === "undefined" || o[Symbol.iterator] == null) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = o[Symbol.iterator](); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it["return"] != null) it["return"](); } finally { if (didErr) throw err; } } }; }

  function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

  function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

  function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

  function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

  function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

  (window["webpackJsonp"] = window["webpackJsonp"] || []).push([["endpoints-endpoints-module"], {
    /***/
    "+JNM":
    /*!***********************************************************************************************************************!*\
      !*** ./src/app/modules/endpoints/pages/endpoint-details/components/endpoint-data-table/endpoint-data-table.module.ts ***!
      \***********************************************************************************************************************/

    /*! exports provided: EndpointDataTableModule */

    /***/
    function JNM(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "EndpointDataTableModule", function () {
        return EndpointDataTableModule;
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


      var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/router */
      "iInd");
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


      var _angular_material_paginator__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @angular/material/paginator */
      "5QHs");
      /* harmony import */


      var _angular_material_slide_toggle__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @angular/material/slide-toggle */
      "jMqV");
      /* harmony import */


      var _angular_material_sort__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @angular/material/sort */
      "LUZP");
      /* harmony import */


      var _angular_material_table__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @angular/material/table */
      "OaSA");
      /* harmony import */


      var _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @angular/material/tooltip */
      "ZFy/");
      /* harmony import */


      var _vex_pipes_color_color_fade_module__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @vex/pipes/color/color-fade.module */
      "Chvm");
      /* harmony import */


      var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! @visurel/iconify-angular */
      "l+Q0");
      /* harmony import */


      var _endpoint_data_table_component__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! ./endpoint-data-table.component */
      "CM3U");

      var EndpointDataTableModule = function EndpointDataTableModule() {
        _classCallCheck(this, EndpointDataTableModule);
      };

      EndpointDataTableModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_endpoint_data_table_component__WEBPACK_IMPORTED_MODULE_15__["EndpointDataTableComponent"]],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"], _angular_router__WEBPACK_IMPORTED_MODULE_4__["RouterModule"], _angular_material_table__WEBPACK_IMPORTED_MODULE_11__["MatTableModule"], _angular_material_paginator__WEBPACK_IMPORTED_MODULE_8__["MatPaginatorModule"], _angular_material_sort__WEBPACK_IMPORTED_MODULE_10__["MatSortModule"], _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_6__["MatCheckboxModule"], _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_12__["MatTooltipModule"], _angular_material_button__WEBPACK_IMPORTED_MODULE_5__["MatButtonModule"], _angular_material_icon__WEBPACK_IMPORTED_MODULE_7__["MatIconModule"], _angular_material_slide_toggle__WEBPACK_IMPORTED_MODULE_9__["MatSlideToggleModule"], _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_14__["IconModule"], _vex_pipes_color_color_fade_module__WEBPACK_IMPORTED_MODULE_13__["ColorFadeModule"]],
        exports: [_endpoint_data_table_component__WEBPACK_IMPORTED_MODULE_15__["EndpointDataTableComponent"]]
      })], EndpointDataTableModule);
      /***/
    },

    /***/
    "/dKF":
    /*!****************************************************************************************!*\
      !*** ./src/app/modules/endpoints/pages/endpoint-details/endpoint-details.component.ts ***!
      \****************************************************************************************/

    /*! exports provided: EndpointDetailsComponent */

    /***/
    function dKF(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "EndpointDetailsComponent", function () {
        return EndpointDetailsComponent;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _raw_loader_endpoint_details_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! raw-loader!./endpoint-details.component.html */
      "8DGB");
      /* harmony import */


      var _endpoint_details_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! ./endpoint-details.component.scss */
      "1/Qu");
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


      var _iconify_icons_ic_twotone_cloud_off__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-cloud-off */
      "DaE0");
      /* harmony import */


      var _iconify_icons_ic_twotone_cloud_off__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_cloud_off__WEBPACK_IMPORTED_MODULE_7__);
      /* harmony import */


      var _iconify_icons_ic_twotone_group__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-group */
      "Ell1");
      /* harmony import */


      var _iconify_icons_ic_twotone_group__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_group__WEBPACK_IMPORTED_MODULE_8__);
      /* harmony import */


      var _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-more-vert */
      "+Chm");
      /* harmony import */


      var _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_9__);
      /* harmony import */


      var _iconify_icons_ic_twotone_pageview__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-pageview */
      "9Gk2");
      /* harmony import */


      var _iconify_icons_ic_twotone_pageview__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_pageview__WEBPACK_IMPORTED_MODULE_10__);
      /* harmony import */


      var _iconify_icons_ic_twotone_timer__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-timer */
      "De0L");
      /* harmony import */


      var _iconify_icons_ic_twotone_timer__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_timer__WEBPACK_IMPORTED_MODULE_11__);
      /* harmony import */


      var _aliases_components_aliases_create_aliases_create_component__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @aliases/components/aliases-create/aliases-create.component */
      "tedC");
      /* harmony import */


      var _core_http__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @core/http */
      "vAmI");
      /* harmony import */


      var _core_utils_file_service__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! @core/utils/file.service */
      "EGFe");
      /* harmony import */


      var _core_utils_uri_service__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! @core/utils/uri.service */
      "BjwJ");
      /* harmony import */


      var _data_schema__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(
      /*! @data/schema */
      "V99k");

      var EndpointDetailsComponent = /*#__PURE__*/function () {
        function EndpointDetailsComponent(dialog, route, requestResource, uri, location, file, router, aliasResource, headerNameResource, queryParamNameResource, bodyParamNameResource) {
          _classCallCheck(this, EndpointDetailsComponent);

          this.dialog = dialog;
          this.route = route;
          this.requestResource = requestResource;
          this.uri = uri;
          this.location = location;
          this.file = file;
          this.router = router;
          this.aliasResource = aliasResource;
          this.headerNameResource = headerNameResource;
          this.queryParamNameResource = queryParamNameResource;
          this.bodyParamNameResource = bodyParamNameResource;
          this.requestTitle = 'Requests';
          this.requestColumns = [];
          this.pathSegmentNameTitle = 'Path Segments';
          this.pathSegmentNameColumns = [];
          this.queryParamNameTitle = 'Query Params';
          this.queryParamNameColumns = [];
          this.headerNameTitle = 'Headers';
          this.headerNameColumns = [];
          this.bodyParamNameTitle = 'Body Params';
          this.bodyParamNameColumns = [];
          this.icGroup = _iconify_icons_ic_twotone_group__WEBPACK_IMPORTED_MODULE_8___default.a;
          this.icPageView = _iconify_icons_ic_twotone_pageview__WEBPACK_IMPORTED_MODULE_10___default.a;
          this.icCloudOff = _iconify_icons_ic_twotone_cloud_off__WEBPACK_IMPORTED_MODULE_7___default.a;
          this.icTimer = _iconify_icons_ic_twotone_timer__WEBPACK_IMPORTED_MODULE_11___default.a;
          this.icMoreVert = _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_9___default.a;
          this.crumbs = [];
        }

        _createClass(EndpointDetailsComponent, [{
          key: "ngOnInit",
          value: function ngOnInit() {
            var snapshot = this.route.snapshot;
            this.projectId = snapshot.queryParams.project_id;
            this.endpoint = new _data_schema__WEBPACK_IMPORTED_MODULE_16__["Endpoint"](snapshot.data.endpoint);
            this.buildCrumbs();
            this.requestData = snapshot.data.requests.list.map(function (request) {
              return new _data_schema__WEBPACK_IMPORTED_MODULE_16__["Request"](request);
            });
            this.headerNameData = snapshot.data.headerNames.map(function (header) {
              return new _data_schema__WEBPACK_IMPORTED_MODULE_16__["Header"](header);
            });
            this.queryParamNameData = snapshot.data.queryParamNames.map(function (queryParam) {
              return new _data_schema__WEBPACK_IMPORTED_MODULE_16__["QueryParam"](queryParam);
            });
            this.pathSegmentNameData = snapshot.data.pathSegmentNames.map(function (pathSegment) {
              return new _data_schema__WEBPACK_IMPORTED_MODULE_16__["PathSegment"](pathSegment);
            });
            this.bodyParamNameData = snapshot.data.bodyParamNames.map(function (bodyParam) {
              return new _data_schema__WEBPACK_IMPORTED_MODULE_16__["BodyParam"](bodyParam);
            });
            this.requestColumns = this.buildRequestsTableColumns();
            this.pathSegmentNameColumns = this.buildPathSegmentNameColumns();
            this.headerNameColumns = this.buildComponentNameTableColumns();
            this.queryParamNameColumns = this.buildComponentNameTableColumns();
            this.bodyParamNameColumns = this.buildComponentNameTableColumns();
          } // API Access

        }, {
          key: "createOrEditAlias",
          value: function createOrEditAlias(component, aliasName) {
            var _this = this;

            var snapshot = this.route.snapshot;
            var projectId = snapshot.queryParams.project_id;
            var endpointId = snapshot.params.endpoint_id;

            if (component.alias === undefined) {
              this.aliasResource.create({
                component_name_id: component.id,
                component_type: component.type,
                name: aliasName,
                project_id: projectId,
                endpoint_id: endpointId
              }).subscribe(function (res) {
                // Once an endpoint has been aliased, a new endpoint is created and the current endopint no longer exists
                var uri = new _this.uri["class"](_this.location.path());

                var path = _this.file.dirname(uri.pathname);

                uri.pathname = path;

                _this.router.navigateByUrl(uri.pathname + uri.query);
              });
            } else {
              this.aliasResource.update(component.alias.id, {
                name: aliasName,
                project_id: projectId,
                endpoint_id: endpointId
              }).subscribe(function (res) {
                component.alias.name = aliasName;
              });
            }
          }
        }, {
          key: "removeAlias",
          value: function removeAlias(component) {
            var snapshot = this.route.snapshot;
            var project_id = snapshot.queryParams.project_id;
            this.aliasResource.destroy(component.alias.id, {
              project_id: project_id,
              component_id: component.id,
              component_type: component.type
            }).subscribe(function (res) {
              component.alias = null;
              component.aliasName = undefined;
            });
          }
        }, {
          key: "removeRequestEndpoint",
          value: function removeRequestEndpoint(requests) {
            var _this2 = this;

            requests.forEach(function (r) {
              _this2.requestResource.removeEndpoint(r.id).subscribe(function (res) {
                _this2.requestData = _this2.requestData.filter(function (request) {
                  return request.id !== r.id;
                });
              });
            });
          }
        }, {
          key: "updateComponentName",
          value: function updateComponentName(component) {
            var resource;

            switch (component.type) {
              case _data_schema__WEBPACK_IMPORTED_MODULE_16__["RequestComponentType"].Header:
                resource = this.headerNameResource;
                break;

              case _data_schema__WEBPACK_IMPORTED_MODULE_16__["RequestComponentType"].QueryParam:
                resource = this.queryParamNameResource;
                break;

              case _data_schema__WEBPACK_IMPORTED_MODULE_16__["RequestComponentType"].BodyParam:
                resource = this.bodyParamNameResource;
                break;
            }

            if (resource) {
              resource.update(this.endpoint.id, component.id, {
                project_id: this.projectId,
                is_required: component.isRequired
              }).subscribe(function (res) {});
            }
          } // API Access

        }, {
          key: "openAliasDialog",
          value: function openAliasDialog(component) {
            var _this3 = this;

            var dialogRef = this.dialog.open(_aliases_components_aliases_create_aliases_create_component__WEBPACK_IMPORTED_MODULE_12__["AliasesCreateComponent"], {
              width: '600px',
              data: component || {}
            });
            var onCreateSub = dialogRef.componentInstance.onCreate.subscribe(function ($event) {
              _this3.createOrEditAlias(component, $event.name);
            });
            dialogRef.afterClosed().subscribe(function (request) {
              onCreateSub.unsubscribe();
            });
          } // Helpers

        }, {
          key: "projectIdQuery",
          value: function projectIdQuery() {
            return {
              project_id: this.route.snapshot.queryParams.project_id
            };
          }
        }, {
          key: "requestPath",
          value: function requestPath(request) {
            return this.file.join(location.pathname, '/requests', request.id);
          }
        }, {
          key: "buildCrumbs",
          value: function buildCrumbs() {
            this.crumbs.push({
              name: 'Endpoints',
              routerLink: ['/endpoints'],
              queryParams: this.route.snapshot.queryParams
            });
            this.crumbs.push({
              name: this.endpoint.path
            });
          }
        }, {
          key: "buildPathSegmentNameColumns",
          value: function buildPathSegmentNameColumns() {
            return [{
              label: 'POSITION',
              property: 'position',
              type: 'text'
            }, {
              label: 'NAME',
              property: 'name',
              type: 'text'
            }, {
              label: '',
              property: 'link-button',
              type: 'button',
              visible: true
            }, {
              label: 'ALIAS',
              property: 'aliasName',
              type: 'text',
              visible: true
            }];
          }
        }, {
          key: "buildRequestsTableColumns",
          value: function buildRequestsTableColumns() {
            var _this4 = this;

            return [{
              label: 'Checkbox',
              property: 'checkbox',
              type: 'checkbox',
              visible: true
            }, {
              label: 'METHOD',
              property: 'method',
              type: 'text',
              visible: true
            }, {
              label: 'URL',
              property: 'url',
              type: 'link',
              routerLink: function routerLink(request) {
                return [_this4.requestPath(request)];
              },
              queryParams: function queryParams() {
                return _this4.projectIdQuery();
              }
            }, {
              label: 'STATUS',
              property: 'status',
              type: 'text',
              visible: true
            }, {
              label: 'LATENCY',
              property: 'latency',
              type: 'text',
              visible: true
            }, {
              label: 'CREATED AT',
              property: 'createdAt',
              type: 'text',
              visible: true
            }];
          }
        }, {
          key: "buildComponentNameTableColumns",
          value: function buildComponentNameTableColumns() {
            var _this5 = this;

            return [{
              label: 'NAME',
              property: 'name',
              type: 'text'
            }, // { label: '', property: 'link-button', type: 'button', visible: true },
            // { label: 'ALIAS', property: 'aliasName', type: 'text', visible: true }
            {
              label: 'REQUIRED',
              property: 'isRequired',
              type: 'slideToggle',
              visible: true,
              onclick: function onclick(component) {
                component.isRequired = !component.isRequired;

                _this5.updateComponentName(component);
              }
            }];
          }
        }]);

        return EndpointDetailsComponent;
      }();

      EndpointDetailsComponent.ctorParameters = function () {
        return [{
          type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MatDialog"]
        }, {
          type: _angular_router__WEBPACK_IMPORTED_MODULE_6__["ActivatedRoute"]
        }, {
          type: _core_http__WEBPACK_IMPORTED_MODULE_13__["RequestResource"]
        }, {
          type: _core_utils_uri_service__WEBPACK_IMPORTED_MODULE_15__["UriService"]
        }, {
          type: _angular_common__WEBPACK_IMPORTED_MODULE_3__["Location"]
        }, {
          type: _core_utils_file_service__WEBPACK_IMPORTED_MODULE_14__["FileService"]
        }, {
          type: _angular_router__WEBPACK_IMPORTED_MODULE_6__["Router"]
        }, {
          type: _core_http__WEBPACK_IMPORTED_MODULE_13__["AliasResource"]
        }, {
          type: _core_http__WEBPACK_IMPORTED_MODULE_13__["HeaderNameResource"]
        }, {
          type: _core_http__WEBPACK_IMPORTED_MODULE_13__["QueryParamNameResource"]
        }, {
          type: _core_http__WEBPACK_IMPORTED_MODULE_13__["BodyParamNameResource"]
        }];
      };

      EndpointDetailsComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_4__["Component"])({
        selector: 'vex-endpoint-details',
        template: _raw_loader_endpoint_details_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_endpoint_details_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
      })], EndpointDetailsComponent);
      /***/
    },

    /***/
    "1/Qu":
    /*!******************************************************************************************!*\
      !*** ./src/app/modules/endpoints/pages/endpoint-details/endpoint-details.component.scss ***!
      \******************************************************************************************/

    /*! exports provided: default */

    /***/
    function Qu(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJlbmRwb2ludC1kZXRhaWxzLmNvbXBvbmVudC5zY3NzIn0= */";
      /***/
    },

    /***/
    "8DGB":
    /*!********************************************************************************************************************************!*\
      !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/endpoints/pages/endpoint-details/endpoint-details.component.html ***!
      \********************************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function DGB(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "<vex-page-layout mode=\"card\">\n\n<vex-page-layout-header class=\"vex-layout-theme\" fxLayout=\"column\" fxLayoutAlign=\"center start\">\n  <div class=\"container\">\n    <h1 class=\"title mt-0 mb-1\">Endpoint Details</h1>\n    <vex-breadcrumbs [crumbs]=\"crumbs\"></vex-breadcrumbs>\n  </div>\n</vex-page-layout-header>\n\n<vex-page-layout-content class=\"container\">\n  <div class=\"card\">\n    <mat-tab-group>\n      <mat-tab label=\"Requests\">\n        <div class=\"p-3\">\n          <endpoint-data-table [title]=\"requestTitle\"\n                            [columns]=\"requestColumns\"\n                            [data]=\"requestData\"\n                            (selectionDelete)=\"removeRequestEndpoint($event)\"\n                            class=\"w-full overflow-auto shadow\" gdColumn=\"1 / span 2\"\n                            gdColumn.lt-md=\"1 / -1\"\n                            gdColumn.lt-sm=\"1\"></endpoint-data-table>\n        </div>\n      </mat-tab>\n      <mat-tab label=\"Path Segments\">\n        <div class=\"p-3\">\n          <endpoint-data-table [title]=\"pathSegmentNameTitle\"\n                            [columns]=\"pathSegmentNameColumns\"\n                            [data]=\"pathSegmentNameData\"\n                            (createOrEditAlias)=\"openAliasDialog($event)\"\n                            (removeAlias)=\"removeAlias($event)\"\n                            class=\"w-full overflow-auto shadow\" gdColumn=\"1 / span 2\"\n                            gdColumn.lt-md=\"1 / -1\"\n                            gdColumn.lt-sm=\"1\"></endpoint-data-table>\n        </div>\n      </mat-tab>\n      <mat-tab label=\"Queries\">\n        <div class=\"p-3\">\n          <endpoint-data-table [title]=\"queryParamNameTitle\"\n                            [columns]=\"queryParamNameColumns\"\n                            [data]=\"queryParamNameData\"\n                            (createOrEditAlias)=\"openAliasDialog($event)\"\n                            (removeAlias)=\"removeAlias($event)\"\n                            class=\"w-full overflow-auto shadow\" gdColumn=\"3 / span 2\"\n                            gdColumn.lt-md=\"1 / -1\"\n                            gdColumn.lt-sm=\"1\"></endpoint-data-table>\n\n        </div>\n      </mat-tab>\n      <mat-tab label=\"Headers\">\n        <div class=\"p-3\">\n          <endpoint-data-table [title]=\"headerNameTitle\"\n                            [columns]=\"headerNameColumns\"\n                            [data]=\"headerNameData\"\n                            (createOrEditAlias)=\"openAliasDialog($event)\"\n                            (removeAlias)=\"removeAlias($event)\"\n                            class=\"w-full overflow-auto shadow\" gdColumn=\"1 / span 2\"\n                            gdColumn.lt-md=\"1 / -1\"\n                            gdColumn.lt-sm=\"1\"></endpoint-data-table>\n\n        </div>\n      </mat-tab>\n      <mat-tab label=\"Body Params\">\n        <div class=\"p-3\">\n          <endpoint-data-table [title]=\"bodyParamNameTitle\"\n                            [columns]=\"bodyParamNameColumns\"\n                            [data]=\"bodyParamNameData\"\n                            (createOrEditAlias)=\"openAliasDialog($event)\"\n                            (removeAlias)=\"removeAlias($event)\"\n                            class=\"w-full overflow-auto shadow\" gdColumn=\"1 / span 2\"\n                            gdColumn.lt-md=\"1 / -1\"\n                            gdColumn.lt-sm=\"1\"></endpoint-data-table>\n\n        </div>\n      </mat-tab>\n    </mat-tab-group>\n  </div>\n</vex-page-layout-content>\n";
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
            var _this6 = this;

            return labels.map(function (label) {
              return _this6.labels[label];
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
    "BhTb":
    /*!**************************************************************************************!*\
      !*** ./src/app/modules/endpoints/pages/endpoints-index/endpoints-index.component.ts ***!
      \**************************************************************************************/

    /*! exports provided: EndpointsIndexComponent */

    /***/
    function BhTb(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "EndpointsIndexComponent", function () {
        return EndpointsIndexComponent;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _raw_loader_endpoints_index_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! raw-loader!./endpoints-index.component.html */
      "luMs");
      /* harmony import */


      var _endpoints_index_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! ./endpoints-index.component.scss */
      "byb6");
      /* harmony import */


      var _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/cdk/collections */
      "CtHx");
      /* harmony import */


      var _angular_common__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/common */
      "SVse");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_forms__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/forms */
      "s7LF");
      /* harmony import */


      var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @angular/material/dialog */
      "iELJ");
      /* harmony import */


      var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @angular/material/form-field */
      "Q2Ze");
      /* harmony import */


      var _angular_material_paginator__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @angular/material/paginator */
      "5QHs");
      /* harmony import */


      var _angular_material_sort__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @angular/material/sort */
      "LUZP");
      /* harmony import */


      var _angular_material_table__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @angular/material/table */
      "OaSA");
      /* harmony import */


      var _angular_router__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @angular/router */
      "iInd");
      /* harmony import */


      var ngx_take_until_destroy__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! ngx-take-until-destroy */
      "DnKK");
      /* harmony import */


      var rxjs_operators__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! rxjs/operators */
      "kU1M");
      /* harmony import */


      var _vex_animations__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! @vex/animations */
      "ORuP");
      /* harmony import */


      var _core_http_endpoint_resource_service__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(
      /*! @core/http/endpoint-resource.service */
      "T+qy");
      /* harmony import */


      var _core_utils_file_service__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(
      /*! @core/utils/file.service */
      "EGFe");
      /* harmony import */


      var _core_utils_uri_service__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(
      /*! @core/utils/uri.service */
      "BjwJ");
      /* harmony import */


      var _data_schema__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(
      /*! @data/schema */
      "V99k");
      /* harmony import */


      var _endpoints_components_endpoints_create_endpoints_create_component__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(
      /*! @endpoints/components/endpoints-create/endpoints-create.component */
      "bU6V");
      /* harmony import */


      var _mock_endpoints_index_data__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(
      /*! ./mock/endpoints-index-data */
      "I+wY");
      /* harmony import */


      var _services_endpoints_data_service__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(
      /*! ./services/endpoints-data.service */
      "fDgC");
      /* harmony import */


      var _services_endpoints_index_icons_service__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(
      /*! ./services/endpoints-index-icons.service */
      "cWny");

      var EndpointsIndexComponent = /*#__PURE__*/function () {
        function EndpointsIndexComponent(icons, activatedRoute, dialog, endpointsDataService, endpointResource, file, location, router, route, uri) {
          _classCallCheck(this, EndpointsIndexComponent);

          this.icons = icons;
          this.activatedRoute = activatedRoute;
          this.dialog = dialog;
          this.endpointsDataService = endpointsDataService;
          this.endpointResource = endpointResource;
          this.file = file;
          this.location = location;
          this.router = router;
          this.route = route;
          this.uri = uri;
          this.layoutCtrl = new _angular_forms__WEBPACK_IMPORTED_MODULE_6__["FormControl"]('boxed'); // Table settings

          this.columns = [{
            label: 'Checkbox',
            property: 'checkbox',
            type: 'checkbox',
            visible: true
          }, {
            label: 'Category',
            property: 'category',
            type: 'dropdown',
            visible: true
          }, {
            label: 'Method',
            property: 'method',
            type: 'text',
            visible: true
          }, {
            label: 'Path',
            property: 'path',
            type: 'text',
            visible: true
          }, {
            label: 'Requests',
            property: 'request_count',
            type: 'text',
            visible: true
          }];
          this.pageIndex = this.route.snapshot.queryParams.page || 0;
          this.pageSize = 10;
          this.pageSizeOptions = [5, 10, 20, 50];
          this.selection = new _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_3__["SelectionModel"](true, []);
          this.searchCtrl = new _angular_forms__WEBPACK_IMPORTED_MODULE_6__["FormControl"]();
          this.labels = _mock_endpoints_index_data__WEBPACK_IMPORTED_MODULE_21__["aioTableLabels"];
          this.endpointCategories = _data_schema__WEBPACK_IMPORTED_MODULE_19__["EndpointCategories"]; // Breadcrumb settings

          this.crumbs = [];
        }

        _createClass(EndpointsIndexComponent, [{
          key: "ngOnInit",
          value: function ngOnInit() {
            var _this7 = this;

            this.endpointsDataService.set(this.route.snapshot.data.endpoints);
            this.dataSource = new _angular_material_table__WEBPACK_IMPORTED_MODULE_11__["MatTableDataSource"]();
            this.endpointsDataService.endpoints$.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_14__["filter"])(Boolean)).subscribe(function (endpoints) {
              _this7.dataSource.data = endpoints;
            });
            this.searchCtrl.valueChanges.pipe(Object(ngx_take_until_destroy__WEBPACK_IMPORTED_MODULE_13__["untilDestroyed"])(this)).subscribe(function (value) {
              return _this7.onFilterChange(value);
            });
            var keys = Object.keys(_data_schema__WEBPACK_IMPORTED_MODULE_19__["EndpointCategories"]);
            this.endpointCategoryNames = keys.slice(keys.length / 2);
            this.project = this.route.snapshot.data.project;
            this.crumbs.push({
              name: this.project.name
            });
            this.crumbs.push({
              name: 'Endpoints'
            });
          }
        }, {
          key: "ngAfterViewInit",
          value: function ngAfterViewInit() {
            this.dataSource.paginator = this.paginator;
            this.dataSource.sort = this.sort;
          }
        }, {
          key: "openCreateDialog",
          value: function openCreateDialog() {
            var _this8 = this;

            var dialogRef = this.dialog.open(_endpoints_components_endpoints_create_endpoints_create_component__WEBPACK_IMPORTED_MODULE_20__["EndpointsCreateComponent"], {
              width: '600px'
            });
            var onCreateSub = dialogRef.componentInstance.onCreate.subscribe(function ($event) {
              _this8.createEndpoint($event);
            });
            dialogRef.afterClosed().subscribe(function (endpoint) {
              onCreateSub.unsubscribe();
            });
          }
        }, {
          key: "getEndpoints",
          value: function getEndpoints(params) {
            var _this9 = this;

            this.endpointResource.index(params).subscribe(function (res) {
              _this9.endpointsDataService.set(res);
            }, function (error) {});
          }
        }, {
          key: "createEndpoint",
          value: function createEndpoint(data) {
            var _this10 = this;

            var snapshot = this.route.snapshot;
            var project_id = snapshot.queryParams.project_id;
            data.append('project_id', project_id);
            this.endpointResource.create(data).subscribe(function (res) {
              var curSnapshot = _this10.route.snapshot;

              _this10.getEndpoints({
                project_id: curSnapshot.queryParams.project_id
              });
            }, function (error) {});
          }
        }, {
          key: "showEndpoint",
          value: function showEndpoint(endpoint) {
            var path = this.file.join('/endpoints', endpoint.id);
            var snapshot = this.route.snapshot;
            this.router.navigate([path], {
              queryParams: {
                project_id: snapshot.queryParams.project_id
              }
            });
          }
        }, {
          key: "deleteEndpoint",
          value: function deleteEndpoint(endpoint) {
            var _this11 = this;

            this.endpointResource.destroy(endpoint.id).subscribe(function (res) {
              _this11.endpointsDataService["delete"](endpoint.id);

              _this11.selection.deselect(endpoint);
            });
          }
        }, {
          key: "deleteEndpoints",
          value: function deleteEndpoints(endpoints) {
            var _this12 = this;

            endpoints.forEach(function (r) {
              return _this12.deleteEndpoint(r);
            });
          }
        }, {
          key: "updateEndpoint",
          value: function updateEndpoint(endpoint, params) {
            this.endpointResource.update(endpoint.id, params).subscribe(function (res) {
              for (var key in params) {
                if (params.hasOwnProperty(key)) {
                  endpoint[key] = params[key];
                }
              }
            });
          }
        }, {
          key: "onFilterChange",
          value: function onFilterChange(value) {
            if (!this.dataSource) {
              return;
            }

            value = value.trim();
            value = value.toLowerCase();
            this.dataSource.filter = value;
          }
        }, {
          key: "toggleColumnVisibility",
          value: function toggleColumnVisibility(column, event) {
            event.stopPropagation();
            event.stopImmediatePropagation();
            column.visible = !column.visible;
          }
          /** Whether the number of selected elements matches the total number of rows. */

        }, {
          key: "isAllSelected",
          value: function isAllSelected() {
            var numSelected = this.selection.selected.length;
            var numRows = this.dataSource.data.length;
            return numSelected === numRows;
          }
          /** Selects all rows if they are not all selected; otherwise clear selection. */

        }, {
          key: "masterToggle",
          value: function masterToggle() {
            var _this13 = this;

            this.isAllSelected() ? this.selection.clear() : this.dataSource.data.forEach(function (row) {
              return _this13.selection.select(row);
            });
          }
        }, {
          key: "trackByProperty",
          value: function trackByProperty(index, column) {
            return column.property;
          }
        }, {
          key: "onComponentChange",
          value: function onComponentChange(change, row) {
            var endpoints = this.endpointsDataService.endpoints;
            var index = endpoints.findIndex(function (c) {
              return c === row;
            });
            endpoints[index].components = change.value;
            this.endpointsDataService.set(endpoints);
          }
          /**
           * On page change, add queryParam 'page' to URL
           */

        }, {
          key: "onPaginateChange",
          value: function onPaginateChange($event) {
            var queryParams = Object.assign({}, this.route.snapshot.queryParams);
            queryParams.page = $event.pageIndex;
            var url = this.router.createUrlTree([], {
              relativeTo: this.activatedRoute,
              queryParams: queryParams
            }).toString();
            this.location.go(url);
          }
        }, {
          key: "ngOnDestroy",
          value: function ngOnDestroy() {}
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

        return EndpointsIndexComponent;
      }();

      EndpointsIndexComponent.ctorParameters = function () {
        return [{
          type: _services_endpoints_index_icons_service__WEBPACK_IMPORTED_MODULE_23__["EndpointsIndexIcons"]
        }, {
          type: _angular_router__WEBPACK_IMPORTED_MODULE_12__["ActivatedRoute"]
        }, {
          type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_7__["MatDialog"]
        }, {
          type: _services_endpoints_data_service__WEBPACK_IMPORTED_MODULE_22__["EndpointsDataService"]
        }, {
          type: _core_http_endpoint_resource_service__WEBPACK_IMPORTED_MODULE_16__["EndpointResource"]
        }, {
          type: _core_utils_file_service__WEBPACK_IMPORTED_MODULE_17__["FileService"]
        }, {
          type: _angular_common__WEBPACK_IMPORTED_MODULE_4__["Location"]
        }, {
          type: _angular_router__WEBPACK_IMPORTED_MODULE_12__["Router"]
        }, {
          type: _angular_router__WEBPACK_IMPORTED_MODULE_12__["ActivatedRoute"]
        }, {
          type: _core_utils_uri_service__WEBPACK_IMPORTED_MODULE_18__["UriService"]
        }];
      };

      EndpointsIndexComponent.propDecorators = {
        columns: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_5__["Input"]
        }],
        paginator: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_5__["ViewChild"],
          args: [_angular_material_paginator__WEBPACK_IMPORTED_MODULE_9__["MatPaginator"], {
            "static": true
          }]
        }],
        sort: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_5__["ViewChild"],
          args: [_angular_material_sort__WEBPACK_IMPORTED_MODULE_10__["MatSort"], {
            "static": true
          }]
        }]
      };
      EndpointsIndexComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_5__["Component"])({
        selector: 'endpoints-index',
        template: _raw_loader_endpoints_index_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        animations: [_vex_animations__WEBPACK_IMPORTED_MODULE_15__["fadeInUp400ms"], _vex_animations__WEBPACK_IMPORTED_MODULE_15__["stagger40ms"]],
        providers: [{
          provide: _angular_material_form_field__WEBPACK_IMPORTED_MODULE_8__["MAT_FORM_FIELD_DEFAULT_OPTIONS"],
          useValue: {
            appearance: 'standard'
          }
        }],
        styles: [_endpoints_index_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
      })], EndpointsIndexComponent);
      /***/
    },

    /***/
    "CM3U":
    /*!**************************************************************************************************************************!*\
      !*** ./src/app/modules/endpoints/pages/endpoint-details/components/endpoint-data-table/endpoint-data-table.component.ts ***!
      \**************************************************************************************************************************/

    /*! exports provided: EndpointDataTableComponent */

    /***/
    function CM3U(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "EndpointDataTableComponent", function () {
        return EndpointDataTableComponent;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _raw_loader_endpoint_data_table_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! raw-loader!./endpoint-data-table.component.html */
      "b2rO");
      /* harmony import */


      var _endpoint_data_table_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! ./endpoint-data-table.component.scss */
      "JKv7");
      /* harmony import */


      var _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/cdk/collections */
      "CtHx");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_material_paginator__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/material/paginator */
      "5QHs");
      /* harmony import */


      var _angular_material_sort__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/material/sort */
      "LUZP");
      /* harmony import */


      var _angular_material_table__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @angular/material/table */
      "OaSA");
      /* harmony import */


      var _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-cloud-download */
      "MzEE");
      /* harmony import */


      var _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_8__);
      /* harmony import */


      var _iconify_icons_ic_twotone_create__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-create */
      "A17n");
      /* harmony import */


      var _iconify_icons_ic_twotone_create__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_create__WEBPACK_IMPORTED_MODULE_9__);
      /* harmony import */


      var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-delete */
      "e3EN");
      /* harmony import */


      var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_10__);
      /* harmony import */


      var _iconify_icons_ic_twotone_link__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-link */
      "h+Y6");
      /* harmony import */


      var _iconify_icons_ic_twotone_link__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_link__WEBPACK_IMPORTED_MODULE_11__);
      /* harmony import */


      var _iconify_icons_ic_twotone_more_horiz__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-more-horiz */
      "SqwC");
      /* harmony import */


      var _iconify_icons_ic_twotone_more_horiz__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_more_horiz__WEBPACK_IMPORTED_MODULE_12__);
      /* harmony import */


      var _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @vex/utils/tailwindcss */
      "XXSj");

      var EndpointDataTableComponent = /*#__PURE__*/function () {
        function EndpointDataTableComponent() {
          _classCallCheck(this, EndpointDataTableComponent);

          this.pageSize = 6;
          this.dataSource = new _angular_material_table__WEBPACK_IMPORTED_MODULE_7__["MatTableDataSource"]();
          this.selection = new _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_3__["SelectionModel"](true, []);
          this.icMoreHoriz = _iconify_icons_ic_twotone_more_horiz__WEBPACK_IMPORTED_MODULE_12___default.a;
          this.icCloudDownload = _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_8___default.a;
          this.icLink = _iconify_icons_ic_twotone_link__WEBPACK_IMPORTED_MODULE_11___default.a;
          this.icDelete = _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_10___default.a;
          this.icCreate = _iconify_icons_ic_twotone_create__WEBPACK_IMPORTED_MODULE_9___default.a;
          this.theme = _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_13__["default"];
          this.selectionDelete = new _angular_core__WEBPACK_IMPORTED_MODULE_4__["EventEmitter"]();
          this.createOrEditAlias = new _angular_core__WEBPACK_IMPORTED_MODULE_4__["EventEmitter"]();
          this.removeAlias = new _angular_core__WEBPACK_IMPORTED_MODULE_4__["EventEmitter"]();
        }

        _createClass(EndpointDataTableComponent, [{
          key: "ngOnInit",
          value: function ngOnInit() {}
        }, {
          key: "ngOnChanges",
          value: function ngOnChanges(changes) {
            if (changes.columns) {
              this.visibleColumns = this.columns.map(function (column) {
                return column.property;
              });
            }

            if (changes.data) {
              this.dataSource.data = this.data;
            }
          }
        }, {
          key: "ngAfterViewInit",
          value: function ngAfterViewInit() {
            this.dataSource.paginator = this.paginator;
            this.dataSource.sort = this.sort;
          }
          /** Whether the number of selected elements matches the total number of rows. */

        }, {
          key: "isAllSelected",
          value: function isAllSelected() {
            var numSelected = this.selection.selected.length;
            var numRows = this.dataSource.data.length;
            return numSelected === numRows;
          }
          /** Selects all rows if they are not all selected; otherwise clear selection. */

        }, {
          key: "masterToggle",
          value: function masterToggle() {
            var _this14 = this;

            this.isAllSelected() ? this.selection.clear() : this.dataSource.data.forEach(function (row) {
              return _this14.selection.select(row);
            });
          }
        }, {
          key: "deleteSelected",
          value: function deleteSelected() {
            this.selectionDelete.emit(this.selection.selected);
          }
        }]);

        return EndpointDataTableComponent;
      }();

      EndpointDataTableComponent.ctorParameters = function () {
        return [];
      };

      EndpointDataTableComponent.propDecorators = {
        title: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Input"]
        }],
        data: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Input"]
        }],
        columns: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Input"]
        }],
        pageSize: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Input"]
        }],
        paginator: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["ViewChild"],
          args: [_angular_material_paginator__WEBPACK_IMPORTED_MODULE_5__["MatPaginator"], {
            "static": true
          }]
        }],
        sort: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["ViewChild"],
          args: [_angular_material_sort__WEBPACK_IMPORTED_MODULE_6__["MatSort"], {
            "static": true
          }]
        }],
        selectionDelete: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Output"]
        }],
        createOrEditAlias: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Output"]
        }],
        removeAlias: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_4__["Output"]
        }]
      };
      EndpointDataTableComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_4__["Component"])({
        selector: 'endpoint-data-table',
        template: _raw_loader_endpoint_data_table_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_endpoint_data_table_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
      })], EndpointDataTableComponent);
      /***/
    },

    /***/
    "Fiip":
    /*!*************************************************************************************!*\
      !*** ./src/app/modules/endpoints/pages/endpoint-details/endpoint-details.module.ts ***!
      \*************************************************************************************/

    /*! exports provided: EndpointDetailsModule */

    /***/
    function Fiip(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "EndpointDetailsModule", function () {
        return EndpointDetailsModule;
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


      var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/material/dialog */
      "iELJ");
      /* harmony import */


      var _angular_material_tabs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/material/tabs */
      "M9ds");
      /* harmony import */


      var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @visurel/iconify-angular */
      "l+Q0");
      /* harmony import */


      var _vex_components_breadcrumbs_breadcrumbs_module__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @vex/components/breadcrumbs/breadcrumbs.module */
      "J0XA");
      /* harmony import */


      var _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @vex/components/page-layout/page-layout.module */
      "7lCJ");
      /* harmony import */


      var _vex_directives_container_container_module__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @vex/directives/container/container.module */
      "68Yx");
      /* harmony import */


      var _aliases_components_aliases_create_aliases_create_module__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @aliases/components/aliases-create/aliases-create.module */
      "/vI3");
      /* harmony import */


      var _components_endpoint_data_table_endpoint_data_table_module__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! ./components/endpoint-data-table/endpoint-data-table.module */
      "+JNM");
      /* harmony import */


      var _endpoint_details_component__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! ./endpoint-details.component */
      "/dKF");

      var EndpointDetailsModule = function EndpointDetailsModule() {
        _classCallCheck(this, EndpointDetailsModule);
      };

      EndpointDetailsModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_endpoint_details_component__WEBPACK_IMPORTED_MODULE_11__["EndpointDetailsComponent"]],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _angular_material_dialog__WEBPACK_IMPORTED_MODULE_3__["MatDialogModule"], _angular_material_tabs__WEBPACK_IMPORTED_MODULE_4__["MatTabsModule"], _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_5__["IconModule"], _vex_components_breadcrumbs_breadcrumbs_module__WEBPACK_IMPORTED_MODULE_6__["BreadcrumbsModule"], _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_7__["PageLayoutModule"], _vex_directives_container_container_module__WEBPACK_IMPORTED_MODULE_8__["ContainerModule"], _aliases_components_aliases_create_aliases_create_module__WEBPACK_IMPORTED_MODULE_9__["AliasesCreateModule"], _components_endpoint_data_table_endpoint_data_table_module__WEBPACK_IMPORTED_MODULE_10__["EndpointDataTableModule"]]
      })], EndpointDetailsModule);
      /***/
    },

    /***/
    "HtCn":
    /*!***********************************************************************************!*\
      !*** ./src/app/modules/endpoints/pages/endpoints-index/endpoints-index.module.ts ***!
      \***********************************************************************************/

    /*! exports provided: EndpointsIndexModule */

    /***/
    function HtCn(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "EndpointsIndexModule", function () {
        return EndpointsIndexModule;
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


      var _angular_material_button_toggle__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/material/button-toggle */
      "Ynp+");
      /* harmony import */


      var _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @angular/material/checkbox */
      "pMoy");
      /* harmony import */


      var _angular_material_icon__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @angular/material/icon */
      "Tj54");
      /* harmony import */


      var _angular_material_menu__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @angular/material/menu */
      "rJgo");
      /* harmony import */


      var _angular_material_paginator__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @angular/material/paginator */
      "5QHs");
      /* harmony import */


      var _angular_material_select__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @angular/material/select */
      "ZTz/");
      /* harmony import */


      var _angular_material_sort__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @angular/material/sort */
      "LUZP");
      /* harmony import */


      var _angular_material_table__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @angular/material/table */
      "OaSA");
      /* harmony import */


      var _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! @angular/material/tooltip */
      "ZFy/");
      /* harmony import */


      var _vex_components_breadcrumbs_breadcrumbs_module__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! @vex/components/breadcrumbs/breadcrumbs.module */
      "J0XA");
      /* harmony import */


      var _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(
      /*! @vex/components/page-layout/page-layout.module */
      "7lCJ");
      /* harmony import */


      var _vex_directives_container_container_module__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(
      /*! @vex/directives/container/container.module */
      "68Yx");
      /* harmony import */


      var _vex_pipes_color_color_fade_module__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(
      /*! @vex/pipes/color/color-fade.module */
      "Chvm");
      /* harmony import */


      var _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(
      /*! @visurel/iconify-angular */
      "l+Q0");
      /* harmony import */


      var _endpoints_components_endpoints_create_endpoints_create_module__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(
      /*! @endpoints/components/endpoints-create/endpoints-create.module */
      "bu14");
      /* harmony import */


      var _shared_shared_module__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(
      /*! @shared/shared.module */
      "PCNd");
      /* harmony import */


      var _endpoints_index_component__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(
      /*! ./endpoints-index.component */
      "BhTb");
      /* harmony import */


      var _services_endpoints_index_icons_service__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(
      /*! ./services/endpoints-index-icons.service */
      "cWny");

      var EndpointsIndexModule = function EndpointsIndexModule() {
        _classCallCheck(this, EndpointsIndexModule);
      };

      EndpointsIndexModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_endpoints_index_component__WEBPACK_IMPORTED_MODULE_22__["EndpointsIndexComponent"]],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _vex_components_page_layout_page_layout_module__WEBPACK_IMPORTED_MODULE_16__["PageLayoutModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"], _vex_components_breadcrumbs_breadcrumbs_module__WEBPACK_IMPORTED_MODULE_15__["BreadcrumbsModule"], _endpoints_components_endpoints_create_endpoints_create_module__WEBPACK_IMPORTED_MODULE_20__["EndpointsCreateModule"], _angular_material_paginator__WEBPACK_IMPORTED_MODULE_10__["MatPaginatorModule"], _angular_material_table__WEBPACK_IMPORTED_MODULE_13__["MatTableModule"], _angular_material_sort__WEBPACK_IMPORTED_MODULE_12__["MatSortModule"], _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_7__["MatCheckboxModule"], _angular_material_icon__WEBPACK_IMPORTED_MODULE_8__["MatIconModule"], _angular_material_button__WEBPACK_IMPORTED_MODULE_5__["MatButtonModule"], _angular_material_menu__WEBPACK_IMPORTED_MODULE_9__["MatMenuModule"], _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_19__["IconModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormsModule"], _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_14__["MatTooltipModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"], _vex_directives_container_container_module__WEBPACK_IMPORTED_MODULE_17__["ContainerModule"], _angular_material_select__WEBPACK_IMPORTED_MODULE_11__["MatSelectModule"], _vex_pipes_color_color_fade_module__WEBPACK_IMPORTED_MODULE_18__["ColorFadeModule"], _angular_material_button_toggle__WEBPACK_IMPORTED_MODULE_6__["MatButtonToggleModule"], _shared_shared_module__WEBPACK_IMPORTED_MODULE_21__["SharedModule"]],
        providers: [_services_endpoints_index_icons_service__WEBPACK_IMPORTED_MODULE_23__["EndpointsIndexIcons"]]
      })], EndpointsIndexModule);
      /***/
    },

    /***/
    "I+wY":
    /*!**************************************************************************************!*\
      !*** ./src/app/modules/endpoints/pages/endpoints-index/mock/endpoints-index-data.ts ***!
      \**************************************************************************************/

    /*! exports provided: aioTableLabels, aioTableData */

    /***/
    function IWY(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "aioTableLabels", function () {
        return aioTableLabels;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "aioTableData", function () {
        return aioTableData;
      });
      /* harmony import */


      var _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! @vex/utils/tailwindcss */
      "XXSj");
      /* harmony import */


      var color__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! color */
      "aSns");
      /* harmony import */


      var color__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(color__WEBPACK_IMPORTED_MODULE_1__);

      var aioTableLabels = [{
        text: 'Headers',
        backgroundColor: color__WEBPACK_IMPORTED_MODULE_1___default()(_vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_0__["default"].colors.green['500']).fade(0.9),
        color: _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_0__["default"].colors.green['500']
      }, {
        text: 'Queries',
        backgroundColor: color__WEBPACK_IMPORTED_MODULE_1___default()(_vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_0__["default"].colors.cyan['500']).fade(0.9),
        color: _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_0__["default"].colors.cyan['500']
      }, {
        text: 'Body',
        backgroundColor: color__WEBPACK_IMPORTED_MODULE_1___default()(_vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_0__["default"].colors.teal['500']).fade(0.9),
        color: _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_0__["default"].colors.teal['500']
      }, {
        text: 'Response',
        backgroundColor: color__WEBPACK_IMPORTED_MODULE_1___default()(_vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_0__["default"].colors.purple['500']).fade(0.9),
        color: _vex_utils_tailwindcss__WEBPACK_IMPORTED_MODULE_0__["default"].colors.purple['500']
      }];
      var aioTableData = [{
        id: 1,
        url: 'https://scenario.io/users',
        endpoint: '/users',
        components: [aioTableLabels[0], aioTableLabels[1], aioTableLabels[2], aioTableLabels[3]],
        position: 1
      }, {
        id: 2,
        url: 'https://scenario.io/users/1',
        endpoint: '/users/{:user_id}',
        components: [aioTableLabels[0], aioTableLabels[2], aioTableLabels[3]],
        position: 2
      }]; // export const aioTableData = [
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

      /***/
    },

    /***/
    "Ib5P":
    /*!*************************************************************************************************************************************!*\
      !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/endpoints/components/endpoints-create/endpoints-create.component.html ***!
      \*************************************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function Ib5P(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "<form (ngSubmit)=\"create()\" [formGroup]=\"form\">\r\n  <div fxLayout=\"row\" fxLayoutAlign=\"start center\" mat-dialog-title>\r\n\r\n    <h2 class=\"headline m-0\" fxFlex=\"auto\">New Endpoint</h2>\r\n<!--\r\n    <button [matMenuTriggerFor]=\"settingsMenu\" class=\"text-secondary\" mat-icon-button type=\"button\">\r\n      <mat-icon [icIcon]=\"icMoreVert\"></mat-icon>\r\n    </button>\r\n-->\r\n    <button class=\"text-secondary\" mat-dialog-close mat-icon-button type=\"button\">\r\n      <mat-icon [icIcon]=\"icClose\"></mat-icon>\r\n    </button>\r\n  </div>\r\n\r\n  <mat-divider></mat-divider>\r\n\r\n  <mat-dialog-content>\r\n    <div class=\"mt-5 mb-3\" fxLayout=\"row\" fxLayoutGap=\"10px\">\r\n      <mat-form-field fxFlex=\"80\">\r\n        <mat-label>Host</mat-label>\r\n        <input cdkFocusInitial formControlName=\"host\" matInput>\r\n        <mat-hint>e.g. localhost</mat-hint>\r\n      </mat-form-field>\r\n      <mat-form-field fxFlex=\"20\">\r\n        <mat-label>Port</mat-label>\r\n        <input cdkFocusInitial formControlName=\"port\" matInput>\r\n        <mat-hint>e.g. 443</mat-hint>\r\n      </mat-form-field>\r\n    </div>\r\n\r\n    <div class=\"mt-3 mb-3\" fxLayout=\"row\" fxLayoutGap=\"10px\">\r\n      <mat-form-field fxFlex=\"20\">\r\n        <mat-label>Method</mat-label>\r\n        <mat-select formControlName=\"method\">\r\n          <mat-option *ngFor=\"let method of formOptions.methods\" [value]=\"method\">\r\n            {{ method }}\r\n          </mat-option>\r\n        </mat-select>\r\n      </mat-form-field>\r\n      <mat-form-field fxFlex=\"80\">\r\n        <mat-label>Path</mat-label>\r\n        <input cdkFocusInitial formControlName=\"path\" matInput>\r\n        <mat-hint>e.g. /users/:user_id</mat-hint>\r\n      </mat-form-field>\r\n    </div>\r\n\r\n    <mat-divider></mat-divider>\r\n\r\n    <div fxLayout=\"column\" class=\"mt-3 mb-0 request-component-wrapper\">\r\n      <h4\r\n        *ngIf=\"form.get('pathSegments')['controls'].length\"\r\n        class=\"mb-2\"\r\n        fxFlex=\"auto\">\r\n        Path Segments\r\n      </h4>\r\n      \r\n      <div\r\n        formArrayName=\"pathSegments\"\r\n        *ngFor=\"let control of form.get('pathSegments')['controls']; index as i\"\r\n      >\r\n        <div\r\n          [formGroupName]=\"i\"\r\n          fxLayout=\"row\"\r\n          fxLayoutAlign=\"space-around start\"\r\n          fxLayoutGap=\"10px\"\r\n        >\r\n          <mat-form-field fxFlex=\"80\">\r\n            <mat-label>Name</mat-label>\r\n            <input\r\n              type=\"text\"\r\n              matInput\r\n              formControlName=\"name\"\r\n            >\r\n          </mat-form-field>\r\n          <mat-form-field fxFlex=\"20\">\r\n            <mat-label>Type</mat-label>\r\n            <mat-select formControlName=\"type\">\r\n              <mat-option *ngFor=\"let type of formOptions.pathSegmentTypes\" [value]=\"type\">\r\n                {{ type }}\r\n              </mat-option>\r\n            </mat-select>\r\n          </mat-form-field>\r\n        </div>\r\n      </div>\r\n    </div>\r\n  </mat-dialog-content>\r\n\r\n  <mat-dialog-actions align=\"end\">\r\n    <button [disabled]=\"form.invalid\" color=\"primary\" mat-button type=\"submit\">CREATE</button>\r\n    <button mat-button mat-dialog-close type=\"button\">CANCEL</button>\r\n  </mat-dialog-actions>\r\n</form>\r\n\r\n<mat-menu #settingsMenu=\"matMenu\" xPosition=\"before\" yPosition=\"below\">\r\n  <button mat-menu-item>\r\n    <mat-icon [icIcon]=\"icPrint\"></mat-icon>\r\n    <span>Print</span>\r\n  </button>\r\n\r\n  <button mat-menu-item>\r\n    <mat-icon [icIcon]=\"icDownload\"></mat-icon>\r\n    <span>Export</span>\r\n  </button>\r\n\r\n  <button mat-menu-item>\r\n    <mat-icon [icIcon]=\"icDelete\"></mat-icon>\r\n    <span>Delete</span>\r\n  </button>\r\n</mat-menu>\r\n";
      /***/
    },

    /***/
    "JKv7":
    /*!****************************************************************************************************************************!*\
      !*** ./src/app/modules/endpoints/pages/endpoint-details/components/endpoint-data-table/endpoint-data-table.component.scss ***!
      \****************************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function JKv7(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = ".table-link {\n  color: #1976d2;\n}\n\n.table-link:hover {\n  text-decoration: underline;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uLy4uLy4uLy4uL2VuZHBvaW50LWRhdGEtdGFibGUuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSxjQUFBO0FBQ0Y7O0FBRUE7RUFDRSwwQkFBQTtBQUNGIiwiZmlsZSI6ImVuZHBvaW50LWRhdGEtdGFibGUuY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyIudGFibGUtbGluayB7XG4gIGNvbG9yOiAjMTk3NmQyO1xufVxuXG4udGFibGUtbGluazpob3ZlciB7XG4gIHRleHQtZGVjb3JhdGlvbjogdW5kZXJsaW5lO1xufSJdfQ== */";
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
    "Wupf":
    /*!************************************************************************************************!*\
      !*** ./src/app/modules/endpoints/pages/endpoint-details/services/requests-resolver.service.ts ***!
      \************************************************************************************************/

    /*! exports provided: RequestsResolver */

    /***/
    function Wupf(module, __webpack_exports__, __webpack_require__) {
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
              endpoint_id: route.params.endpoint_id,
              project_id: route.queryParams.project_id
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
    },

    /***/
    "a5rT":
    /*!*******************************************************!*\
      !*** ./src/app/modules/endpoints/endpoints.module.ts ***!
      \*******************************************************/

    /*! exports provided: EndpointsModule */

    /***/
    function a5rT(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "EndpointsModule", function () {
        return EndpointsModule;
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


      var _requests_pages_request_details_request_details_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @requests/pages/request-details/request-details.module */
      "9CFt");
      /* harmony import */


      var _endpoints_routing_module__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! ./endpoints-routing.module */
      "wSzF");
      /* harmony import */


      var _pages_endpoint_details_endpoint_details_module__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! ./pages/endpoint-details/endpoint-details.module */
      "Fiip");
      /* harmony import */


      var _pages_endpoints_index_endpoints_index_module__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! ./pages/endpoints-index/endpoints-index.module */
      "HtCn");

      var EndpointsModule = function EndpointsModule() {
        _classCallCheck(this, EndpointsModule);
      };

      EndpointsModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _endpoints_routing_module__WEBPACK_IMPORTED_MODULE_4__["EndpointsRoutingModule"], _pages_endpoints_index_endpoints_index_module__WEBPACK_IMPORTED_MODULE_6__["EndpointsIndexModule"], _pages_endpoint_details_endpoint_details_module__WEBPACK_IMPORTED_MODULE_5__["EndpointDetailsModule"], _requests_pages_request_details_request_details_module__WEBPACK_IMPORTED_MODULE_3__["RequestDetailsModule"]]
      })], EndpointsModule);
      /***/
    },

    /***/
    "b2rO":
    /*!******************************************************************************************************************************************************************!*\
      !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/endpoints/pages/endpoint-details/components/endpoint-data-table/endpoint-data-table.component.html ***!
      \******************************************************************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function b2rO(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "<div class=\"overflow-auto w-full\" fxLayout=\"column\">\n  <div class=\"border-b py-4 px-6\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\n    <h2 class=\"m-0 title\" fxFlex=\"auto\">{{ title }}</h2>\n\n    <div *ngIf=\"selection.hasValue()\" class=\"mr-4 pr-4 border-r\" fxFlex=\"none\">\n      <button (click)=\"deleteSelected()\"\n              color=\"primary\"\n              mat-icon-button\n              matTooltip=\"Delete selected\"\n              type=\"button\">\n        <mat-icon [icIcon]=\"icDelete\"></mat-icon>\n      </button>\n    </div>\n\n    <!-- <button mat-icon-button type=\"button\">\n      <mat-icon [icIcon]=\"icCloudDownload\" class=\"text-secondary\"></mat-icon>\n    </button>\n\n    <button mat-icon-button type=\"button\">\n      <mat-icon [icIcon]=\"icMoreHoriz\" class=\"text-secondary\"></mat-icon>\n    </button> -->\n  </div>\n\n  <table [dataSource]=\"dataSource\" class=\"w-full overflow-auto\" mat-table matSort>\n    <!--- Note that these columns can be defined in any order.\n          The actual rendered columns are set as a property on the row definition\" -->\n\n    <!-- Checkbox Column -->\n    <ng-container matColumnDef=\"checkbox\">\n      <th *matHeaderCellDef mat-header-cell>\n        <mat-checkbox (change)=\"$event ? masterToggle() : null\"\n                      [checked]=\"selection.hasValue() && isAllSelected()\"\n                      [indeterminate]=\"selection.hasValue() && !isAllSelected()\"\n                      color=\"primary\">\n        </mat-checkbox>\n      </th>\n      <td *matCellDef=\"let row\" class=\"w-4\" mat-cell>\n        <mat-checkbox (change)=\"$event ? selection.toggle(row) : null\"\n                      (click)=\"$event.stopPropagation()\"\n                      [checked]=\"selection.isSelected(row)\"\n                      color=\"primary\">\n        </mat-checkbox>\n      </td>\n    </ng-container>\n\n    <!-- Model Properties Column -->\n    <ng-container *ngFor=\"let column of columns\">\n      <ng-container *ngIf=\"column.type === 'text'\" [matColumnDef]=\"column.property\">\n        <th *matHeaderCellDef mat-header-cell mat-sort-header> {{ column.label }}</th>\n        <td *matCellDef=\"let row\" [ngClass]=\"column.cssClasses\" mat-cell>\n          {{ row[column.property] === undefined ? 'N/A' : row[column.property] }}\n        </td>\n      </ng-container>\n\n      <ng-container *ngIf=\"column.type === 'slideToggle'\" [matColumnDef]=\"column.property\">\n        <th *matHeaderCellDef mat-header-cell> {{ column.label }}</th>\n        <td *matCellDef=\"let row\" class=\"w-4\" mat-cell>\n          <mat-slide-toggle\n            [checked]=\"row[column.property]\"\n            (change)=\"column.onclick(row)\"\n          >\n          </mat-slide-toggle>\n        </td>\n      </ng-container>\n\n      <!-- Link Column -->\n      <ng-container *ngIf=\"column.type === 'link'\" [matColumnDef]=\"column.property\">\n        <th *matHeaderCellDef mat-header-cell mat-sort-header>{{ column.label }}</th>\n        <td *matCellDef=\"let row\" mat-cell>\n          <a class=\"table-link\"\n             [routerLink]=\"column.routerLink(row)\"\n             [queryParams]=\"column.queryParams()\"\n             (click)=\"column.onclick($event, row)\">{{ row[column.property] }}</a>\n        </td>\n      </ng-container>\n\n      <ng-container *ngIf=\"column.type === 'badge'\" [matColumnDef]=\"column.property\">\n        <th *matHeaderCellDef mat-header-cell mat-sort-header> {{ column.label }}</th>\n        <td *matCellDef=\"let row\" [ngClass]=\"column.cssClasses\" mat-cell>\n          <div *ngIf=\"row[column.property] === 'ready'\"\n               class=\"w-3 h-3 rounded-full bg-green-500 cursor-pointer\"\n               matTooltip=\"Ready to ship\"></div>\n          <div *ngIf=\"row[column.property] === 'pending'\"\n               class=\"w-3 h-3 rounded-full bg-orange-500 cursor-pointer\"\n               matTooltip=\"Pending Payment\"></div>\n          <div *ngIf=\"row[column.property] === 'warn'\"\n               class=\"w-3 h-3 rounded-full bg-red-500 cursor-pointer\"\n               matTooltip=\"Missing Payment\"></div>\n        </td>\n      </ng-container>\n    </ng-container>\n\n    <ng-container matColumnDef=\"link-button\">\n      <th *matHeaderCellDef mat-header-cell disabled></th>\n      <td *matCellDef=\"let row\" mat-cell>\n        <div class=\"flex ml-3\">\n          <a (click)=\"createOrEditAlias.emit(row)\"\n             [style.background-color]=\"theme.colors.green['500'] | colorFade:0.9\"\n             [style.color]=\"theme.colors.green['500']\"\n             class=\"ml-auto w-8 h-8 leading-none flex items-center justify-center hover:bg-hover\"\n             mat-icon-button\n             *ngIf=\"!row.alias\">\n            <mat-icon [icIcon]=\"icLink\" size=\"18px\"></mat-icon>\n          </a>\n          <a (click)=\"createOrEditAlias.emit(row)\"\n             [style.background-color]=\"theme.colors.cyan['500'] | colorFade:0.9\"\n             [style.color]=\"theme.colors.cyan['500']\"\n             class=\"ml-auto w-8 h-8 leading-none flex items-center justify-center hover:bg-hover\"\n             mat-icon-button\n             *ngIf=\"row.alias\">\n            <mat-icon [icIcon]=\"icCreate\" size=\"18px\"></mat-icon>\n          </a>\n          <a (click)=\"removeAlias.emit(row)\"\n             [style.background-color]=\"theme.colors.gray['700'] | colorFade:0.9\"\n             [style.color]=\"theme.colors.gray['700']\"\n             class=\"ml-3 w-8 h-8 leading-none flex items-center justify-center hover:bg-hover\"\n             mat-icon-button\n             *ngIf=\"row.alias\">\n            <mat-icon [icIcon]=\"icDelete\" size=\"18px\"></mat-icon>\n          </a>\n        </div>\n      </td>\n    </ng-container>\n\n    <tr *matHeaderRowDef=\"visibleColumns\" mat-header-row></tr>\n    <!--suppress UnnecessaryLabelJS -->\n    <tr *matRowDef=\"let row; columns: visibleColumns;\" mat-row></tr>\n  </table>\n\n  <mat-paginator [pageSize]=\"pageSize\" class=\"paginator\"></mat-paginator>\n\n</div>\n";
      /***/
    },

    /***/
    "bU6V":
    /*!*********************************************************************************************!*\
      !*** ./src/app/modules/endpoints/components/endpoints-create/endpoints-create.component.ts ***!
      \*********************************************************************************************/

    /*! exports provided: EndpointsCreateComponent */

    /***/
    function bU6V(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "EndpointsCreateComponent", function () {
        return EndpointsCreateComponent;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _raw_loader_endpoints_create_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! raw-loader!./endpoints-create.component.html */
      "Ib5P");
      /* harmony import */


      var _endpoints_create_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! ./endpoints-create.component.scss */
      "g4jc");
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


      var _iconify_icons_ic_twotone_edit_location__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-edit-location */
      "EPGw");
      /* harmony import */


      var _iconify_icons_ic_twotone_edit_location__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_edit_location__WEBPACK_IMPORTED_MODULE_10__);
      /* harmony import */


      var _iconify_icons_ic_twotone_location_city__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-location-city */
      "0I5b");
      /* harmony import */


      var _iconify_icons_ic_twotone_location_city__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_location_city__WEBPACK_IMPORTED_MODULE_11__);
      /* harmony import */


      var _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-more-vert */
      "+Chm");
      /* harmony import */


      var _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_12__);
      /* harmony import */


      var _iconify_icons_ic_twotone_my_location__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-my-location */
      "kSvQ");
      /* harmony import */


      var _iconify_icons_ic_twotone_my_location__WEBPACK_IMPORTED_MODULE_13___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_my_location__WEBPACK_IMPORTED_MODULE_13__);
      /* harmony import */


      var _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-person */
      "KaaH");
      /* harmony import */


      var _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_14___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_14__);
      /* harmony import */


      var _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-phone */
      "YA1h");
      /* harmony import */


      var _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_15___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_15__);
      /* harmony import */


      var _iconify_icons_ic_twotone_print__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-print */
      "yHIK");
      /* harmony import */


      var _iconify_icons_ic_twotone_print__WEBPACK_IMPORTED_MODULE_16___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_print__WEBPACK_IMPORTED_MODULE_16__);

      var EndpointsCreateComponent = /*#__PURE__*/function () {
        function EndpointsCreateComponent(defaults, dialogRef, fb) {
          _classCallCheck(this, EndpointsCreateComponent);

          this.defaults = defaults;
          this.dialogRef = dialogRef;
          this.fb = fb;
          this.onCreate = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
          this.formOptions = {
            methods: ['GET', 'OPTIONS', 'POST', 'PUT', 'DELETE'],
            pathSegmentTypes: ['Static', 'Alias']
          };
          this.icMoreVert = _iconify_icons_ic_twotone_more_vert__WEBPACK_IMPORTED_MODULE_12___default.a;
          this.icClose = _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_7___default.a;
          this.icPrint = _iconify_icons_ic_twotone_print__WEBPACK_IMPORTED_MODULE_16___default.a;
          this.icDownload = _iconify_icons_ic_twotone_cloud_download__WEBPACK_IMPORTED_MODULE_8___default.a;
          this.icDelete = _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_9___default.a;
          this.icPerson = _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_14___default.a;
          this.icMyLocation = _iconify_icons_ic_twotone_my_location__WEBPACK_IMPORTED_MODULE_13___default.a;
          this.icLocationCity = _iconify_icons_ic_twotone_location_city__WEBPACK_IMPORTED_MODULE_11___default.a;
          this.icEditLocation = _iconify_icons_ic_twotone_edit_location__WEBPACK_IMPORTED_MODULE_10___default.a;
          this.icPhone = _iconify_icons_ic_twotone_phone__WEBPACK_IMPORTED_MODULE_15___default.a;
        }

        _createClass(EndpointsCreateComponent, [{
          key: "ngOnInit",
          value: function ngOnInit() {
            var _this15 = this;

            var pathControl = new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"]('', [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required]);
            pathControl.valueChanges.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["debounceTime"])(500)).subscribe(function (path) {
              _this15.renderPath(path);
            });
            this.form = this.fb.group({
              host: new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"]('', [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required]),
              method: new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"]('', [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required]),
              path: pathControl,
              pathSegments: this.fb.array([]),
              port: new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"]('', [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required, _angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].pattern('^[0-9]*$'), _angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].minLength(1), _angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].maxLength(5)])
            });
          }
        }, {
          key: "create",
          value: function create() {
            var form = this.form.value;
            var formData = new FormData();
            formData.append('host', form.host);
            formData.append('method', form.method);
            formData.append('path', form.path);
            formData.append('path_segments', JSON.stringify(form.pathSegments));
            formData.append('port', form.port);
            this.onCreate.emit(formData);
            this.dialogRef.close();
          } // Helpers

        }, {
          key: "renderPath",
          value: function renderPath(path) {
            var pathSegmentStrings = path.split('/').filter(function (s) {
              return s.length > 0;
            });
            var pathSegments = this.form.get('pathSegments');
            var i = 0;

            var _iterator = _createForOfIteratorHelper(pathSegments.controls),
                _step;

            try {
              for (_iterator.s(); !(_step = _iterator.n()).done;) {
                var control = _step.value;

                if (i === pathSegmentStrings.length) {
                  break;
                }

                var _pathSegmentName = pathSegmentStrings[i];

                if (_pathSegmentName.length && control.value.name !== _pathSegmentName) {
                  control.patchValue({
                    name: _pathSegmentName
                  });
                }

                i += 1;
              }
            } catch (err) {
              _iterator.e(err);
            } finally {
              _iterator.f();
            }

            if (pathSegmentStrings.length > pathSegments.length) {
              for (var _i = pathSegments.length; _i < pathSegmentStrings.length; ++_i) {
                var pathSegmentName = pathSegmentStrings[_i];

                if (pathSegmentName.length === 0) {
                  continue;
                }

                var formControl = this.createPathSegmentFormGroup(pathSegmentName);
                pathSegments.push(formControl);
              }
            } else if (pathSegmentStrings.length < pathSegments.length) {
              for (var _i2 = pathSegmentStrings.length; _i2 < pathSegments.length; ++_i2) {
                pathSegments.removeAt(_i2);
              }
            }
          }
        }, {
          key: "renderPathSegments",
          value: function renderPathSegments() {
            var pathSegmentStrings = [];
            var pathSegments = this.form.get('pathSegments');

            var _iterator2 = _createForOfIteratorHelper(pathSegments.controls),
                _step2;

            try {
              for (_iterator2.s(); !(_step2 = _iterator2.n()).done;) {
                var control = _step2.value;
                pathSegmentStrings.push(control.value.name);
              }
            } catch (err) {
              _iterator2.e(err);
            } finally {
              _iterator2.f();
            }

            this.form.patchValue({
              path: "/".concat(pathSegmentStrings.join('/'))
            });
          }
        }, {
          key: "createPathSegmentFormGroup",
          value: function createPathSegmentFormGroup(pathSegmentName) {
            var _this16 = this;

            var pathSegmentNameControl = new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"](pathSegmentName, [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required]);
            pathSegmentNameControl.valueChanges.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["debounceTime"])(500)).subscribe(function () {
              _this16.renderPathSegments();
            });
            return this.fb.group({
              name: pathSegmentNameControl,
              type: new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"](this.formOptions.pathSegmentTypes[0], [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["Validators"].required])
            });
          }
        }]);

        return EndpointsCreateComponent;
      }();

      EndpointsCreateComponent.ctorParameters = function () {
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

      EndpointsCreateComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'endpoints-create',
        template: _raw_loader_endpoints_create_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_endpoints_create_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
      })], EndpointsCreateComponent);
      /***/
    },

    /***/
    "bu14":
    /*!******************************************************************************************!*\
      !*** ./src/app/modules/endpoints/components/endpoints-create/endpoints-create.module.ts ***!
      \******************************************************************************************/

    /*! exports provided: EndpointsCreateModule */

    /***/
    function bu14(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "EndpointsCreateModule", function () {
        return EndpointsCreateModule;
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


      var _endpoints_create_component__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! ./endpoints-create.component */
      "bU6V");

      var EndpointsCreateModule = function EndpointsCreateModule() {
        _classCallCheck(this, EndpointsCreateModule);
      };

      EndpointsCreateModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"], _angular_material_dialog__WEBPACK_IMPORTED_MODULE_6__["MatDialogModule"], _angular_material_input__WEBPACK_IMPORTED_MODULE_9__["MatInputModule"], _angular_material_button__WEBPACK_IMPORTED_MODULE_5__["MatButtonModule"], _angular_material_icon__WEBPACK_IMPORTED_MODULE_8__["MatIconModule"], _angular_material_radio__WEBPACK_IMPORTED_MODULE_11__["MatRadioModule"], _angular_material_select__WEBPACK_IMPORTED_MODULE_12__["MatSelectModule"], _angular_material_menu__WEBPACK_IMPORTED_MODULE_10__["MatMenuModule"], _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_13__["IconModule"], _angular_material_divider__WEBPACK_IMPORTED_MODULE_7__["MatDividerModule"], ngx_dropzone__WEBPACK_IMPORTED_MODULE_14__["NgxDropzoneModule"]],
        declarations: [_endpoints_create_component__WEBPACK_IMPORTED_MODULE_15__["EndpointsCreateComponent"]],
        entryComponents: [_endpoints_create_component__WEBPACK_IMPORTED_MODULE_15__["EndpointsCreateComponent"]],
        exports: [_endpoints_create_component__WEBPACK_IMPORTED_MODULE_15__["EndpointsCreateComponent"]]
      })], EndpointsCreateModule);
      /***/
    },

    /***/
    "byb6":
    /*!****************************************************************************************!*\
      !*** ./src/app/modules/endpoints/pages/endpoints-index/endpoints-index.component.scss ***!
      \****************************************************************************************/

    /*! exports provided: default */

    /***/
    function byb6(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJlbmRwb2ludHMtaW5kZXguY29tcG9uZW50LnNjc3MifQ== */";
      /***/
    },

    /***/
    "cWny":
    /*!***************************************************************************************************!*\
      !*** ./src/app/modules/endpoints/pages/endpoints-index/services/endpoints-index-icons.service.ts ***!
      \***************************************************************************************************/

    /*! exports provided: EndpointsIndexIcons */

    /***/
    function cWny(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "EndpointsIndexIcons", function () {
        return EndpointsIndexIcons;
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


      var _iconify_icons_ic_twotone_more_horiz__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-more-horiz */
      "SqwC");
      /* harmony import */


      var _iconify_icons_ic_twotone_more_horiz__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_more_horiz__WEBPACK_IMPORTED_MODULE_6__);
      /* harmony import */


      var _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-search */
      "sF+I");
      /* harmony import */


      var _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_7__);

      var EndpointsIndexIcons = function EndpointsIndexIcons() {
        _classCallCheck(this, EndpointsIndexIcons);

        this.icSearch = _iconify_icons_ic_twotone_search__WEBPACK_IMPORTED_MODULE_7___default.a;
        this.icDelete = _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_3___default.a;
        this.icAdd = _iconify_icons_ic_twotone_add__WEBPACK_IMPORTED_MODULE_2___default.a;
        this.icFilterList = _iconify_icons_ic_twotone_filter_list__WEBPACK_IMPORTED_MODULE_5___default.a;
        this.icEdit = _iconify_icons_ic_twotone_edit__WEBPACK_IMPORTED_MODULE_4___default.a;
        this.icMoreHoriz = _iconify_icons_ic_twotone_more_horiz__WEBPACK_IMPORTED_MODULE_6___default.a;
      };

      EndpointsIndexIcons.ctorParameters = function () {
        return [];
      };

      EndpointsIndexIcons = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])()], EndpointsIndexIcons);
      /***/
    },

    /***/
    "cjJl":
    /*!*********************************************************************************************************!*\
      !*** ./src/app/modules/endpoints/pages/endpoint-details/services/query-param-names-resolver.service.ts ***!
      \*********************************************************************************************************/

    /*! exports provided: QueryParamNamesResolver */

    /***/
    function cjJl(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "QueryParamNamesResolver", function () {
        return QueryParamNamesResolver;
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


      var _core_http_query_param_name_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @core/http/query-param-name-resource.service */
      "ti5q");

      var QueryParamNamesResolver = /*#__PURE__*/function () {
        function QueryParamNamesResolver(queryParamNameResource) {
          _classCallCheck(this, QueryParamNamesResolver);

          this.queryParamNameResource = queryParamNameResource;
        }

        _createClass(QueryParamNamesResolver, [{
          key: "resolve",
          value: function resolve(route) {
            return this.queryParamNameResource.index(route.params.endpoint_id, {
              project_id: route.queryParams.project_id
            });
          }
        }]);

        return QueryParamNamesResolver;
      }();

      QueryParamNamesResolver.ctorParameters = function () {
        return [{
          type: _core_http_query_param_name_resource_service__WEBPACK_IMPORTED_MODULE_2__["QueryParamNameResource"]
        }];
      };

      QueryParamNamesResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], QueryParamNamesResolver);
      /***/
    },

    /***/
    "coH6":
    /*!********************************************************************************************************!*\
      !*** ./src/app/modules/endpoints/pages/endpoint-details/services/body-param-names-resolver.service.ts ***!
      \********************************************************************************************************/

    /*! exports provided: BodyParamNamesResolver */

    /***/
    function coH6(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "BodyParamNamesResolver", function () {
        return BodyParamNamesResolver;
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


      var _core_http_body_param_name_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @core/http/body-param-name-resource.service */
      "A/vA");

      var BodyParamNamesResolver = /*#__PURE__*/function () {
        function BodyParamNamesResolver(bodyParamNameResource) {
          _classCallCheck(this, BodyParamNamesResolver);

          this.bodyParamNameResource = bodyParamNameResource;
        }

        _createClass(BodyParamNamesResolver, [{
          key: "resolve",
          value: function resolve(route) {
            return this.bodyParamNameResource.index(route.params.endpoint_id, {
              project_id: route.queryParams.project_id
            });
          }
        }]);

        return BodyParamNamesResolver;
      }();

      BodyParamNamesResolver.ctorParameters = function () {
        return [{
          type: _core_http_body_param_name_resource_service__WEBPACK_IMPORTED_MODULE_2__["BodyParamNameResource"]
        }];
      };

      BodyParamNamesResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], BodyParamNamesResolver);
      /***/
    },

    /***/
    "e3m2":
    /*!****************************************************************************************************!*\
      !*** ./src/app/modules/endpoints/pages/endpoint-details/services/header-names-resolver.service.ts ***!
      \****************************************************************************************************/

    /*! exports provided: HeaderNamesResolver */

    /***/
    function e3m2(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "HeaderNamesResolver", function () {
        return HeaderNamesResolver;
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


      var _core_http_header_name_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @core/http/header-name-resource.service */
      "B1Wa");

      var HeaderNamesResolver = /*#__PURE__*/function () {
        function HeaderNamesResolver(headerNameResource) {
          _classCallCheck(this, HeaderNamesResolver);

          this.headerNameResource = headerNameResource;
        }

        _createClass(HeaderNamesResolver, [{
          key: "resolve",
          value: function resolve(route) {
            return this.headerNameResource.index(route.params.endpoint_id, {
              project_id: route.queryParams.project_id
            });
          }
        }]);

        return HeaderNamesResolver;
      }();

      HeaderNamesResolver.ctorParameters = function () {
        return [{
          type: _core_http_header_name_resource_service__WEBPACK_IMPORTED_MODULE_2__["HeaderNameResource"]
        }];
      };

      HeaderNamesResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], HeaderNamesResolver);
      /***/
    },

    /***/
    "fDgC":
    /*!********************************************************************************************!*\
      !*** ./src/app/modules/endpoints/pages/endpoints-index/services/endpoints-data.service.ts ***!
      \********************************************************************************************/

    /*! exports provided: EndpointsDataService */

    /***/
    function fDgC(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "EndpointsDataService", function () {
        return EndpointsDataService;
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


      var _data_schema_endpoint__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @data/schema/endpoint */
      "jBLc");

      var EndpointsDataService = /*#__PURE__*/function () {
        function EndpointsDataService() {
          _classCallCheck(this, EndpointsDataService);

          this.subject = new rxjs__WEBPACK_IMPORTED_MODULE_2__["BehaviorSubject"](null);
          this.endpoints$ = this.subject.asObservable();
        }

        _createClass(EndpointsDataService, [{
          key: "set",
          value: function set(endpoints) {
            this.endpoints = endpoints;
            this.subject.next(endpoints);
          }
        }, {
          key: "add",
          value: function add(endpoint) {
            this.endpoints.unshift(new _data_schema_endpoint__WEBPACK_IMPORTED_MODULE_3__["Endpoint"](endpoint));
            this.set(this.endpoints);
          }
        }, {
          key: "delete",
          value: function _delete(id) {
            this.endpoints.splice(this.endpoints.findIndex(function (existingEndpoint) {
              return existingEndpoint.id === id;
            }), 1);
            this.set(this.endpoints);
          }
        }]);

        return EndpointsDataService;
      }();

      EndpointsDataService.ctorParameters = function () {
        return [];
      };

      EndpointsDataService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], EndpointsDataService);
      /***/
    },

    /***/
    "g4jc":
    /*!***********************************************************************************************!*\
      !*** ./src/app/modules/endpoints/components/endpoints-create/endpoints-create.component.scss ***!
      \***********************************************************************************************/

    /*! exports provided: default */

    /***/
    function g4jc(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJlbmRwb2ludHMtY3JlYXRlLmNvbXBvbmVudC5zY3NzIn0= */";
      /***/
    },

    /***/
    "iCON":
    /*!************************************************************************************************!*\
      !*** ./src/app/modules/endpoints/pages/endpoint-details/services/endpoint-resolver.service.ts ***!
      \************************************************************************************************/

    /*! exports provided: EndpointResolver */

    /***/
    function iCON(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "EndpointResolver", function () {
        return EndpointResolver;
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


      var _core_http_endpoint_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @core/http/endpoint-resource.service */
      "T+qy");

      var EndpointResolver = /*#__PURE__*/function () {
        function EndpointResolver(endpointResource) {
          _classCallCheck(this, EndpointResolver);

          this.endpointResource = endpointResource;
        }

        _createClass(EndpointResolver, [{
          key: "resolve",
          value: function resolve(route) {
            return this.endpointResource.show(route.params.endpoint_id, {
              project_id: route.queryParams.project_id
            });
          }
        }]);

        return EndpointResolver;
      }();

      EndpointResolver.ctorParameters = function () {
        return [{
          type: _core_http_endpoint_resource_service__WEBPACK_IMPORTED_MODULE_2__["EndpointResource"]
        }];
      };

      EndpointResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], EndpointResolver);
      /***/
    },

    /***/
    "luMs":
    /*!******************************************************************************************************************************!*\
      !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/endpoints/pages/endpoints-index/endpoints-index.component.html ***!
      \******************************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function luMs(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "<vex-page-layout>\r\n\r\n  <vex-page-layout-header class=\"pb-16 vex-layout-theme-bg\" fxLayout=\"column\" fxLayoutAlign=\"center start\">\r\n    <div [class.container]=\"layoutCtrl.value === 'boxed'\"\r\n         [class.px-gutter]=\"layoutCtrl.value === 'fullwidth'\"\r\n         class=\"w-full flex flex-col sm:flex-row justify-between\">\r\n      <vex-breadcrumbs [crumbs]=\"crumbs\"></vex-breadcrumbs>\r\n    </div>\r\n  </vex-page-layout-header>\r\n\r\n  <vex-page-layout-content [class.container]=\"layoutCtrl.value === 'boxed'\"\r\n                           [class.px-gutter]=\"layoutCtrl.value === 'fullwidth'\"\r\n                           class=\"-mt-6\">\r\n\r\n    <div class=\"card overflow-auto -mt-16\">\r\n      <div class=\"bg-app-bar px-6 h-16 border-b sticky left-0\" fxLayout=\"row\" fxLayoutAlign=\"start center\">\r\n        <h2 class=\"title my-0 ltr:pr-4 rtl:pl-4 ltr:mr-4 rtl:ml-4 ltr:border-r rtl:border-l\" fxFlex=\"none\" fxHide.xs>\r\n          <span *ngIf=\"selection.isEmpty()\">Endpoints</span>\r\n          <span *ngIf=\"selection.hasValue()\">{{ selection.selected.length }}\r\n            endpoint<span *ngIf=\"selection.selected.length > 1\">s</span> selected</span>\r\n        </h2>\r\n\r\n        <div *ngIf=\"selection.hasValue()\" class=\"mr-4 pr-4 border-r\" fxFlex=\"none\">\r\n          <button (click)=\"deleteEndpoints(selection.selected)\"\r\n                  color=\"primary\"\r\n                  mat-icon-button\r\n                  matTooltip=\"Delete selected\"\r\n                  type=\"button\">\r\n            <mat-icon [icIcon]=\"icons.icDelete\"></mat-icon>\r\n          </button>\r\n\r\n          <!-- <button color=\"primary\" mat-icon-button matTooltip=\"Another action\" type=\"button\">\r\n            <mat-icon [icIcon]=\"icFolder\"></mat-icon>\r\n          </button> -->\r\n        </div>\r\n\r\n        <div class=\"bg-card rounded-full border px-4\"\r\n             fxFlex=\"400px\"\r\n             fxFlex.lt-md=\"auto\"\r\n             fxHide.xs\r\n             fxLayout=\"row\"\r\n             fxLayoutAlign=\"start center\">\r\n          <ic-icon [icIcon]=\"icons.icSearch\" size=\"20px\"></ic-icon>\r\n          <input [formControl]=\"searchCtrl\"\r\n                 class=\"px-4 py-2 border-0 outline-none w-full bg-transparent\"\r\n                 placeholder=\"Search...\"\r\n                 type=\"search\">\r\n        </div>\r\n\r\n        <span fxFlex></span>\r\n\r\n        <button class=\"ml-4\" fxFlex=\"none\" fxHide.gt-xs mat-icon-button type=\"button\">\r\n          <mat-icon [icIcon]=\"icons.icSearch\"></mat-icon>\r\n        </button>\r\n\r\n        <button [matMenuTriggerFor]=\"columnFilterMenu\"\r\n                class=\"ml-4\"\r\n                fxFlex=\"none\"\r\n                mat-icon-button\r\n                matTooltip=\"Filter Columns\"\r\n                type=\"button\">\r\n          <mat-icon [icIcon]=\"icons.icFilterList\"></mat-icon>\r\n        </button>\r\n\r\n        <button (click)=\"openCreateDialog()\"\r\n                class=\"ml-4\"\r\n                color=\"primary\"\r\n                fxFlex=\"none\"\r\n                mat-mini-fab\r\n                matTooltip=\"Create Endpoint\"\r\n                type=\"button\">\r\n          <mat-icon [icIcon]=\"icons.icAdd\"></mat-icon>\r\n        </button>\r\n      </div>\r\n\r\n      <table @stagger [dataSource]=\"dataSource\" class=\"w-full\" mat-table matSort>\r\n\r\n        <!--- Note that these columns can be defined in any order.\r\n              The actual rendered columns are set as a property on the row definition\" -->\r\n\r\n        <!-- Checkbox Column -->\r\n        <ng-container matColumnDef=\"checkbox\">\r\n          <th *matHeaderCellDef mat-header-cell>\r\n            <mat-checkbox (change)=\"$event ? masterToggle() : null\"\r\n                          [checked]=\"selection.hasValue() && isAllSelected()\"\r\n                          [indeterminate]=\"selection.hasValue() && !isAllSelected()\"\r\n                          color=\"primary\">\r\n            </mat-checkbox>\r\n          </th>\r\n          <td *matCellDef=\"let row\" class=\"w-4\" mat-cell (click)=\"$event.stopPropagation()\">\r\n            <mat-checkbox (change)=\"$event ? selection.toggle(row) : null\"\r\n                          [checked]=\"selection.isSelected(row)\"\r\n                          color=\"primary\">\r\n            </mat-checkbox>\r\n          </td>\r\n        </ng-container>\r\n\r\n        <!-- Image Column -->\r\n        <ng-container matColumnDef=\"image\">\r\n          <th *matHeaderCellDef mat-header-cell></th>\r\n          <td *matCellDef=\"let row\" class=\"w-8 min-w-8 pr-0\" mat-cell>\r\n            <img [src]=\"row['imageSrc']\" class=\"avatar h-8 w-8 align-middle\">\r\n          </td>\r\n        </ng-container>\r\n\r\n        <!-- Text Columns -->\r\n        <ng-container *ngFor=\"let column of columns; trackBy: trackByProperty\">\r\n          <ng-container *ngIf=\"column.type === 'text'\" [matColumnDef]=\"column.property\">\r\n            <th *matHeaderCellDef class=\"uppercase\" mat-header-cell mat-sort-header> {{ column.label }}</th>\r\n            <td *matCellDef=\"let row\" [ngClass]=\"column.cssClasses\" mat-cell>{{ row[column.property] }}</td>\r\n          </ng-container>\r\n        </ng-container>\r\n\r\n        <!-- Date Columns -->\r\n        <ng-container *ngFor=\"let column of columns; trackBy: trackByProperty\">\r\n          <ng-container *ngIf=\"column.type === 'date'\" [matColumnDef]=\"column.property\">\r\n            <th *matHeaderCellDef class=\"uppercase\" mat-header-cell mat-sort-header> {{ column.label }}</th>\r\n            <td *matCellDef=\"let row\" [ngClass]=\"column.cssClasses\" mat-cell>{{ row[column.property] | date }}</td>\r\n          </ng-container>\r\n        </ng-container>\r\n\r\n        <!-- Category Column -->\r\n        <ng-container matColumnDef=\"category\">\r\n          <th *matHeaderCellDef class=\"uppercase\" mat-header-cell mat-sort-header>Category</th>\r\n          <td *matCellDef=\"let row\" mat-cell>\r\n            <button\r\n              color=\"primary\"\r\n              mat-flat-button\r\n              [matMenuTriggerFor]=\"categoryMenu\"\r\n              (click)=\"$event.stopPropagation()\"\r\n              [matMenuTriggerData]=\"{ endpoint: row }\">\r\n              {{ endpointCategories[row.category] }}\r\n            </button>\r\n          </td>\r\n        </ng-container>\r\n\r\n        <!-- Label Column -->\r\n        <ng-container matColumnDef=\"components\">\r\n          <th *matHeaderCellDef class=\"uppercase\" mat-header-cell mat-sort-header>Components</th>\r\n          <td *matCellDef=\"let row\" mat-cell>\r\n            <div (click)=\"$event.stopPropagation()\" fxLayoutAlign=\"start center\" fxLayoutGap=\"4px\">\r\n              <div *ngFor=\"let label of row.components | requestComponentLabel\"\r\n                   [style.background-color]=\"label.backgroundColor\"\r\n                   [style.color]=\"label.color\"\r\n                   class=\"rounded px-2 py-1 font-medium text-xs\"\r\n                   fxFlex=\"none\">\r\n                {{ label.text }}\r\n              </div>\r\n            </div>\r\n          </td>\r\n        </ng-container>\r\n\r\n        <!-- Action Column -->\r\n        <ng-container matColumnDef=\"actions\">\r\n          <th *matHeaderCellDef mat-header-cell mat-sort-header></th>\r\n          <td *matCellDef=\"let row\" class=\"w-10 text-secondary\" mat-cell>\r\n            <button (click)=\"$event.stopPropagation()\"\r\n                    [matMenuTriggerData]=\"{ endpoint: row }\"\r\n                    [matMenuTriggerFor]=\"actionsMenu\"\r\n                    mat-icon-button\r\n                    type=\"button\">\r\n              <mat-icon [icIcon]=\"icons.icMoreHoriz\"></mat-icon>\r\n            </button>\r\n          </td>\r\n        </ng-container>\r\n\r\n        <tr *matHeaderRowDef=\"visibleColumns\" mat-header-row></tr>\r\n        <tr (click)=\"showEndpoint(row)\"\r\n            *matRowDef=\"let row; columns: visibleColumns;\"\r\n            @fadeInUp\r\n            class=\"hover:bg-hover trans-ease-out cursor-pointer\"\r\n            mat-row></tr>\r\n      </table>\r\n\r\n      <mat-paginator\r\n        [pageSizeOptions]=\"pageSizeOptions\"\r\n        [pageSize]=\"pageSize\"\r\n        [pageIndex]=\"pageIndex\"\r\n        (page)=\"onPaginateChange($event)\"\r\n        class=\"sticky left-0\">\r\n      </mat-paginator>\r\n    </div>\r\n\r\n  </vex-page-layout-content>\r\n\r\n</vex-page-layout>\r\n\r\n<mat-menu #columnFilterMenu=\"matMenu\" xPosition=\"before\" yPosition=\"below\">\r\n  <button (click)=\"toggleColumnVisibility(column, $event)\" *ngFor=\"let column of columns\"\r\n          class=\"checkbox-item mat-menu-item\">\r\n    <mat-checkbox (click)=\"$event.stopPropagation()\" [(ngModel)]=\"column.visible\" color=\"primary\">\r\n      {{ column.label }}\r\n    </mat-checkbox>\r\n  </button>\r\n</mat-menu>\r\n\r\n<mat-menu #actionsMenu=\"matMenu\" xPosition=\"before\" yPosition=\"below\">\r\n  <ng-template let-endpoint=\"endpoint\" matMenuContent>\r\n    <button (click)=\"deleteEndpoint(endpoint)\" mat-menu-item>\r\n      <mat-icon [icIcon]=\"icons.icDelete\"></mat-icon>\r\n      <span>Delete</span>\r\n    </button>\r\n  </ng-template>\r\n</mat-menu>\r\n\r\n<mat-menu #categoryMenu=\"matMenu\" xPosition=\"after\" yPosition=\"below\">\r\n  <ng-template let-endpoint=\"endpoint\" matMenuContent>\r\n    <button mat-menu-item\r\n      *ngFor=\"let name of endpointCategoryNames\"\r\n      (click)=\"updateEndpoint(endpoint, {category: endpointCategories[name] })\">\r\n      {{ name  }}\r\n    </button>\r\n  </ng-template>\r\n</mat-menu>\r\n";
      /***/
    },

    /***/
    "n7Re":
    /*!************************************************************************************************!*\
      !*** ./src/app/modules/endpoints/pages/endpoints-index/services/endpoints-resolver.service.ts ***!
      \************************************************************************************************/

    /*! exports provided: EndpointsResolver */

    /***/
    function n7Re(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "EndpointsResolver", function () {
        return EndpointsResolver;
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


      var _core_http_endpoint_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @core/http/endpoint-resource.service */
      "T+qy");

      var EndpointsResolver = /*#__PURE__*/function () {
        function EndpointsResolver(endpointResource) {
          _classCallCheck(this, EndpointsResolver);

          this.endpointResource = endpointResource;
        }

        _createClass(EndpointsResolver, [{
          key: "resolve",
          value: function resolve(route) {
            return this.endpointResource.index({
              project_id: route.queryParams.project_id
            });
          }
        }]);

        return EndpointsResolver;
      }();

      EndpointsResolver.ctorParameters = function () {
        return [{
          type: _core_http_endpoint_resource_service__WEBPACK_IMPORTED_MODULE_2__["EndpointResource"]
        }];
      };

      EndpointsResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], EndpointsResolver);
      /***/
    },

    /***/
    "okMl":
    /*!**********************************************************************************************************!*\
      !*** ./src/app/modules/endpoints/pages/endpoint-details/services/path-segment-names-resolver.service.ts ***!
      \**********************************************************************************************************/

    /*! exports provided: PathSegmentNamesResolver */

    /***/
    function okMl(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "PathSegmentNamesResolver", function () {
        return PathSegmentNamesResolver;
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


      var _core_http_path_segment_name_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @core/http/path-segment-name-resource.service */
      "hX/M");

      var PathSegmentNamesResolver = /*#__PURE__*/function () {
        function PathSegmentNamesResolver(pathSegmentNameResource) {
          _classCallCheck(this, PathSegmentNamesResolver);

          this.pathSegmentNameResource = pathSegmentNameResource;
        }

        _createClass(PathSegmentNamesResolver, [{
          key: "resolve",
          value: function resolve(route) {
            return this.pathSegmentNameResource.index(route.params.endpoint_id, {
              project_id: route.queryParams.project_id
            });
          }
        }]);

        return PathSegmentNamesResolver;
      }();

      PathSegmentNamesResolver.ctorParameters = function () {
        return [{
          type: _core_http_path_segment_name_resource_service__WEBPACK_IMPORTED_MODULE_2__["PathSegmentNameResource"]
        }];
      };

      PathSegmentNamesResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], PathSegmentNamesResolver);
      /***/
    },

    /***/
    "wSzF":
    /*!***************************************************************!*\
      !*** ./src/app/modules/endpoints/endpoints-routing.module.ts ***!
      \***************************************************************/

    /*! exports provided: EndpointsRoutingModule */

    /***/
    function wSzF(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "EndpointsRoutingModule", function () {
        return EndpointsRoutingModule;
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


      var _endpoints_pages_endpoint_details_endpoint_details_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @endpoints/pages/endpoint-details/endpoint-details.component */
      "/dKF");
      /* harmony import */


      var _endpoints_pages_endpoints_index_endpoints_index_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @endpoints/pages/endpoints-index/endpoints-index.component */
      "BhTb");
      /* harmony import */


      var _endpoints_pages_endpoints_index_services_endpoints_resolver_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @endpoints/pages/endpoints-index/services/endpoints-resolver.service */
      "n7Re");
      /* harmony import */


      var _endpoints_pages_endpoint_details_services_body_param_names_resolver_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @endpoints/pages/endpoint-details/services/body-param-names-resolver.service */
      "coH6");
      /* harmony import */


      var _endpoints_pages_endpoint_details_services_endpoint_resolver_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @endpoints/pages/endpoint-details/services/endpoint-resolver.service */
      "iCON");
      /* harmony import */


      var _endpoints_pages_endpoint_details_services_header_names_resolver_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @endpoints/pages/endpoint-details/services/header-names-resolver.service */
      "e3m2");
      /* harmony import */


      var _endpoints_pages_endpoint_details_services_path_segment_names_resolver_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @endpoints/pages/endpoint-details/services/path-segment-names-resolver.service */
      "okMl");
      /* harmony import */


      var _endpoints_pages_endpoint_details_services_query_param_names_resolver_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(
      /*! @endpoints/pages/endpoint-details/services/query-param-names-resolver.service */
      "cjJl");
      /* harmony import */


      var _endpoints_pages_endpoint_details_services_requests_resolver_service__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(
      /*! @endpoints/pages/endpoint-details/services/requests-resolver.service */
      "Wupf");
      /* harmony import */


      var _projects_services_project_resolver_service__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(
      /*! @projects/services/project-resolver.service */
      "Y1jZ");
      /* harmony import */


      var _requests_pages_request_details_request_details_component__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(
      /*! @requests/pages/request-details/request-details.component */
      "g6n5");
      /* harmony import */


      var _requests_services_request_resolver_service__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! @requests/services/request-resolver.service */
      "a+oo");
      /* harmony import */


      var _requests_services_response_headers_resolver_service__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(
      /*! @requests/services/response-headers-resolver.service */
      "qeIL");
      /* harmony import */


      var _requests_services_response_resolver_service__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(
      /*! @requests/services/response-resolver.service */
      "h8gq");

      var routes = [{
        path: '',
        component: _endpoints_pages_endpoints_index_endpoints_index_component__WEBPACK_IMPORTED_MODULE_4__["EndpointsIndexComponent"],
        resolve: {
          endpoints: _endpoints_pages_endpoints_index_services_endpoints_resolver_service__WEBPACK_IMPORTED_MODULE_5__["EndpointsResolver"],
          project: _projects_services_project_resolver_service__WEBPACK_IMPORTED_MODULE_12__["ProjectResolver"]
        }
      }, {
        path: ':endpoint_id',
        component: _endpoints_pages_endpoint_details_endpoint_details_component__WEBPACK_IMPORTED_MODULE_3__["EndpointDetailsComponent"],
        resolve: {
          endpoint: _endpoints_pages_endpoint_details_services_endpoint_resolver_service__WEBPACK_IMPORTED_MODULE_7__["EndpointResolver"],
          requests: _endpoints_pages_endpoint_details_services_requests_resolver_service__WEBPACK_IMPORTED_MODULE_11__["RequestsResolver"],
          headerNames: _endpoints_pages_endpoint_details_services_header_names_resolver_service__WEBPACK_IMPORTED_MODULE_8__["HeaderNamesResolver"],
          bodyParamNames: _endpoints_pages_endpoint_details_services_body_param_names_resolver_service__WEBPACK_IMPORTED_MODULE_6__["BodyParamNamesResolver"],
          queryParamNames: _endpoints_pages_endpoint_details_services_query_param_names_resolver_service__WEBPACK_IMPORTED_MODULE_10__["QueryParamNamesResolver"],
          pathSegmentNames: _endpoints_pages_endpoint_details_services_path_segment_names_resolver_service__WEBPACK_IMPORTED_MODULE_9__["PathSegmentNamesResolver"]
        }
      }, {
        path: ':endpoint_id/requests/:request_id',
        component: _requests_pages_request_details_request_details_component__WEBPACK_IMPORTED_MODULE_13__["RequestDetailsComponent"],
        resolve: {
          request: _requests_services_request_resolver_service__WEBPACK_IMPORTED_MODULE_14__["RequestResolver"],
          response: _requests_services_response_resolver_service__WEBPACK_IMPORTED_MODULE_16__["ResponseResolver"],
          responseHeaders: _requests_services_response_headers_resolver_service__WEBPACK_IMPORTED_MODULE_15__["ResponseHeadersResolver"],
          parentResource: _endpoints_pages_endpoint_details_services_endpoint_resolver_service__WEBPACK_IMPORTED_MODULE_7__["EndpointResolver"]
        }
      }];

      var EndpointsRoutingModule = function EndpointsRoutingModule() {
        _classCallCheck(this, EndpointsRoutingModule);
      };

      EndpointsRoutingModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]]
      })], EndpointsRoutingModule);
      /***/
    }
  }]);
})();
//# sourceMappingURL=endpoints-endpoints-module-es5.js.map