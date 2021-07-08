(function () {
  function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest(); }

  function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

  function _iterableToArrayLimit(arr, i) { if (typeof Symbol === "undefined" || !(Symbol.iterator in Object(arr))) return; var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

  function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }

  function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread(); }

  function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

  function _iterableToArray(iter) { if (typeof Symbol !== "undefined" && Symbol.iterator in Object(iter)) return Array.from(iter); }

  function _arrayWithoutHoles(arr) { if (Array.isArray(arr)) return _arrayLikeToArray(arr); }

  function _get(target, property, receiver) { if (typeof Reflect !== "undefined" && Reflect.get) { _get = Reflect.get; } else { _get = function _get(target, property, receiver) { var base = _superPropBase(target, property); if (!base) return; var desc = Object.getOwnPropertyDescriptor(base, property); if (desc.get) { return desc.get.call(receiver); } return desc.value; }; } return _get(target, property, receiver || target); }

  function _superPropBase(object, property) { while (!Object.prototype.hasOwnProperty.call(object, property)) { object = _getPrototypeOf(object); if (object === null) break; } return object; }

  function _createForOfIteratorHelper(o, allowArrayLike) { var it; if (typeof Symbol === "undefined" || o[Symbol.iterator] == null) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e2) { throw _e2; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = o[Symbol.iterator](); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e3) { didErr = true; err = _e3; }, f: function f() { try { if (!normalCompletion && it["return"] != null) it["return"](); } finally { if (didErr) throw err; } } }; }

  function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

  function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

  function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

  function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

  function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

  function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }

  function _createSuper(Derived) { var hasNativeReflectConstruct = _isNativeReflectConstruct(); return function _createSuperInternal() { var Super = _getPrototypeOf(Derived), result; if (hasNativeReflectConstruct) { var NewTarget = _getPrototypeOf(this).constructor; result = Reflect.construct(Super, arguments, NewTarget); } else { result = Super.apply(this, arguments); } return _possibleConstructorReturn(this, result); }; }

  function _possibleConstructorReturn(self, call) { if (call && (typeof call === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

  function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

  function _isNativeReflectConstruct() { if (typeof Reflect === "undefined" || !Reflect.construct) return false; if (Reflect.construct.sham) return false; if (typeof Proxy === "function") return true; try { Date.prototype.toString.call(Reflect.construct(Date, [], function () {})); return true; } catch (e) { return false; } }

  function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

  function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

  (window["webpackJsonp"] = window["webpackJsonp"] || []).push([["default~aliases-aliases-module~endpoints-endpoints-module~organizations-organizations-module~project~11ec6de4"], {
    /***/
    "+4LO":
    /*!***************************************************************!*\
      !*** ./node_modules/@iconify/icons-ic/twotone-filter-list.js ***!
      \***************************************************************/

    /*! no static exports found */

    /***/
    function LO(module, exports) {
      var data = {
        "body": "<path d=\"M10 18h4v-2h-4v2zM3 6v2h18V6H3zm3 7h12v-2H6v2z\" fill=\"currentColor\"/>",
        "width": 24,
        "height": 24
      };
      exports.__esModule = true;
      exports["default"] = data;
      /***/
    },

    /***/
    "5QHs":
    /*!**************************************************************!*\
      !*** ./node_modules/@angular/material/fesm2015/paginator.js ***!
      \**************************************************************/

    /*! exports provided: MAT_PAGINATOR_DEFAULT_OPTIONS, MAT_PAGINATOR_INTL_PROVIDER, MAT_PAGINATOR_INTL_PROVIDER_FACTORY, MatPaginator, MatPaginatorIntl, MatPaginatorModule, PageEvent, _MatPaginatorBase */

    /***/
    function QHs(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MAT_PAGINATOR_DEFAULT_OPTIONS", function () {
        return MAT_PAGINATOR_DEFAULT_OPTIONS;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MAT_PAGINATOR_INTL_PROVIDER", function () {
        return MAT_PAGINATOR_INTL_PROVIDER;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MAT_PAGINATOR_INTL_PROVIDER_FACTORY", function () {
        return MAT_PAGINATOR_INTL_PROVIDER_FACTORY;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatPaginator", function () {
        return MatPaginator;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatPaginatorIntl", function () {
        return MatPaginatorIntl;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatPaginatorModule", function () {
        return MatPaginatorModule;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "PageEvent", function () {
        return PageEvent;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "_MatPaginatorBase", function () {
        return _MatPaginatorBase;
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


      var _angular_material_button__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/material/button */
      "Dxy4");
      /* harmony import */


      var _angular_material_select__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/material/select */
      "ZTz/");
      /* harmony import */


      var _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/material/tooltip */
      "ZFy/");
      /* harmony import */


      var _angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/cdk/coercion */
      "8LU1");
      /* harmony import */


      var rxjs__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! rxjs */
      "qCKp");
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * To modify the labels and text displayed, create a new instance of MatPaginatorIntl and
       * include it in a custom provider
       */


      var MatPaginatorIntl = function MatPaginatorIntl() {
        _classCallCheck(this, MatPaginatorIntl);

        /**
         * Stream to emit from when labels are changed. Use this to notify components when the labels have
         * changed after initialization.
         */
        this.changes = new rxjs__WEBPACK_IMPORTED_MODULE_7__["Subject"]();
        /** A label for the page size selector. */

        this.itemsPerPageLabel = 'Items per page:';
        /** A label for the button that increments the current page. */

        this.nextPageLabel = 'Next page';
        /** A label for the button that decrements the current page. */

        this.previousPageLabel = 'Previous page';
        /** A label for the button that moves to the first page. */

        this.firstPageLabel = 'First page';
        /** A label for the button that moves to the last page. */

        this.lastPageLabel = 'Last page';
        /** A label for the range of items within the current page and the length of the whole list. */

        this.getRangeLabel = function (page, pageSize, length) {
          if (length == 0 || pageSize == 0) {
            return "0 of ".concat(length);
          }

          length = Math.max(length, 0);
          var startIndex = page * pageSize; // If the start index exceeds the list length, do not try and fix the end index to the end.

          var endIndex = startIndex < length ? Math.min(startIndex + pageSize, length) : startIndex + pageSize;
          return "".concat(startIndex + 1, " \u2013 ").concat(endIndex, " of ").concat(length);
        };
      };

      MatPaginatorIntl.ɵprov = Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineInjectable"])({
        factory: function MatPaginatorIntl_Factory() {
          return new MatPaginatorIntl();
        },
        token: MatPaginatorIntl,
        providedIn: "root"
      });
      MatPaginatorIntl.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"],
        args: [{
          providedIn: 'root'
        }]
      }];
      /** @docs-private */

      function MAT_PAGINATOR_INTL_PROVIDER_FACTORY(parentIntl) {
        return parentIntl || new MatPaginatorIntl();
      }
      /** @docs-private */


      var MAT_PAGINATOR_INTL_PROVIDER = {
        // If there is already an MatPaginatorIntl available, use that. Otherwise, provide a new one.
        provide: MatPaginatorIntl,
        deps: [[new _angular_core__WEBPACK_IMPORTED_MODULE_1__["Optional"](), new _angular_core__WEBPACK_IMPORTED_MODULE_1__["SkipSelf"](), MatPaginatorIntl]],
        useFactory: MAT_PAGINATOR_INTL_PROVIDER_FACTORY
      };
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /** The default page size if there is no page size and there are no provided page size options. */

      var DEFAULT_PAGE_SIZE = 50;
      /**
       * Change event object that is emitted when the user selects a
       * different page size or navigates to another page.
       */

      var PageEvent = function PageEvent() {
        _classCallCheck(this, PageEvent);
      };
      /** Injection token that can be used to provide the default options for the paginator module. */


      var MAT_PAGINATOR_DEFAULT_OPTIONS = new _angular_core__WEBPACK_IMPORTED_MODULE_1__["InjectionToken"]('MAT_PAGINATOR_DEFAULT_OPTIONS'); // Boilerplate for applying mixins to _MatPaginatorBase.

      /** @docs-private */

      var MatPaginatorMixinBase = function MatPaginatorMixinBase() {
        _classCallCheck(this, MatPaginatorMixinBase);
      };

      var _MatPaginatorMixinBase = Object(_angular_material_core__WEBPACK_IMPORTED_MODULE_2__["mixinDisabled"])(Object(_angular_material_core__WEBPACK_IMPORTED_MODULE_2__["mixinInitialized"])(MatPaginatorMixinBase));
      /**
       * Base class with all of the `MatPaginator` functionality.
       * @docs-private
       */


      var _MatPaginatorBase = /*#__PURE__*/function (_MatPaginatorMixinBas) {
        _inherits(_MatPaginatorBase, _MatPaginatorMixinBas);

        var _super = _createSuper(_MatPaginatorBase);

        function _MatPaginatorBase(_intl, _changeDetectorRef, defaults) {
          var _this;

          _classCallCheck(this, _MatPaginatorBase);

          _this = _super.call(this);
          _this._intl = _intl;
          _this._changeDetectorRef = _changeDetectorRef;
          _this._pageIndex = 0;
          _this._length = 0;
          _this._pageSizeOptions = [];
          _this._hidePageSize = false;
          _this._showFirstLastButtons = false;
          /** Event emitted when the paginator changes the page size or page index. */

          _this.page = new _angular_core__WEBPACK_IMPORTED_MODULE_1__["EventEmitter"]();
          _this._intlChanges = _intl.changes.subscribe(function () {
            return _this._changeDetectorRef.markForCheck();
          });

          if (defaults) {
            var pageSize = defaults.pageSize,
                pageSizeOptions = defaults.pageSizeOptions,
                hidePageSize = defaults.hidePageSize,
                showFirstLastButtons = defaults.showFirstLastButtons;

            if (pageSize != null) {
              _this._pageSize = pageSize;
            }

            if (pageSizeOptions != null) {
              _this._pageSizeOptions = pageSizeOptions;
            }

            if (hidePageSize != null) {
              _this._hidePageSize = hidePageSize;
            }

            if (showFirstLastButtons != null) {
              _this._showFirstLastButtons = showFirstLastButtons;
            }
          }

          return _this;
        }
        /** The zero-based page index of the displayed list of items. Defaulted to 0. */


        _createClass(_MatPaginatorBase, [{
          key: "ngOnInit",
          value: function ngOnInit() {
            this._initialized = true;

            this._updateDisplayedPageSizeOptions();

            this._markInitialized();
          }
        }, {
          key: "ngOnDestroy",
          value: function ngOnDestroy() {
            this._intlChanges.unsubscribe();
          }
          /** Advances to the next page if it exists. */

        }, {
          key: "nextPage",
          value: function nextPage() {
            if (!this.hasNextPage()) {
              return;
            }

            var previousPageIndex = this.pageIndex;
            this.pageIndex++;

            this._emitPageEvent(previousPageIndex);
          }
          /** Move back to the previous page if it exists. */

        }, {
          key: "previousPage",
          value: function previousPage() {
            if (!this.hasPreviousPage()) {
              return;
            }

            var previousPageIndex = this.pageIndex;
            this.pageIndex--;

            this._emitPageEvent(previousPageIndex);
          }
          /** Move to the first page if not already there. */

        }, {
          key: "firstPage",
          value: function firstPage() {
            // hasPreviousPage being false implies at the start
            if (!this.hasPreviousPage()) {
              return;
            }

            var previousPageIndex = this.pageIndex;
            this.pageIndex = 0;

            this._emitPageEvent(previousPageIndex);
          }
          /** Move to the last page if not already there. */

        }, {
          key: "lastPage",
          value: function lastPage() {
            // hasNextPage being false implies at the end
            if (!this.hasNextPage()) {
              return;
            }

            var previousPageIndex = this.pageIndex;
            this.pageIndex = this.getNumberOfPages() - 1;

            this._emitPageEvent(previousPageIndex);
          }
          /** Whether there is a previous page. */

        }, {
          key: "hasPreviousPage",
          value: function hasPreviousPage() {
            return this.pageIndex >= 1 && this.pageSize != 0;
          }
          /** Whether there is a next page. */

        }, {
          key: "hasNextPage",
          value: function hasNextPage() {
            var maxPageIndex = this.getNumberOfPages() - 1;
            return this.pageIndex < maxPageIndex && this.pageSize != 0;
          }
          /** Calculate the number of pages */

        }, {
          key: "getNumberOfPages",
          value: function getNumberOfPages() {
            if (!this.pageSize) {
              return 0;
            }

            return Math.ceil(this.length / this.pageSize);
          }
          /**
           * Changes the page size so that the first item displayed on the page will still be
           * displayed using the new page size.
           *
           * For example, if the page size is 10 and on the second page (items indexed 10-19) then
           * switching so that the page size is 5 will set the third page as the current page so
           * that the 10th item will still be displayed.
           */

        }, {
          key: "_changePageSize",
          value: function _changePageSize(pageSize) {
            // Current page needs to be updated to reflect the new page size. Navigate to the page
            // containing the previous page's first item.
            var startIndex = this.pageIndex * this.pageSize;
            var previousPageIndex = this.pageIndex;
            this.pageIndex = Math.floor(startIndex / pageSize) || 0;
            this.pageSize = pageSize;

            this._emitPageEvent(previousPageIndex);
          }
          /** Checks whether the buttons for going forwards should be disabled. */

        }, {
          key: "_nextButtonsDisabled",
          value: function _nextButtonsDisabled() {
            return this.disabled || !this.hasNextPage();
          }
          /** Checks whether the buttons for going backwards should be disabled. */

        }, {
          key: "_previousButtonsDisabled",
          value: function _previousButtonsDisabled() {
            return this.disabled || !this.hasPreviousPage();
          }
          /**
           * Updates the list of page size options to display to the user. Includes making sure that
           * the page size is an option and that the list is sorted.
           */

        }, {
          key: "_updateDisplayedPageSizeOptions",
          value: function _updateDisplayedPageSizeOptions() {
            if (!this._initialized) {
              return;
            } // If no page size is provided, use the first page size option or the default page size.


            if (!this.pageSize) {
              this._pageSize = this.pageSizeOptions.length != 0 ? this.pageSizeOptions[0] : DEFAULT_PAGE_SIZE;
            }

            this._displayedPageSizeOptions = this.pageSizeOptions.slice();

            if (this._displayedPageSizeOptions.indexOf(this.pageSize) === -1) {
              this._displayedPageSizeOptions.push(this.pageSize);
            } // Sort the numbers using a number-specific sort function.


            this._displayedPageSizeOptions.sort(function (a, b) {
              return a - b;
            });

            this._changeDetectorRef.markForCheck();
          }
          /** Emits an event notifying that a change of the paginator's properties has been triggered. */

        }, {
          key: "_emitPageEvent",
          value: function _emitPageEvent(previousPageIndex) {
            this.page.emit({
              previousPageIndex: previousPageIndex,
              pageIndex: this.pageIndex,
              pageSize: this.pageSize,
              length: this.length
            });
          }
        }, {
          key: "pageIndex",
          get: function get() {
            return this._pageIndex;
          },
          set: function set(value) {
            this._pageIndex = Math.max(Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_6__["coerceNumberProperty"])(value), 0);

            this._changeDetectorRef.markForCheck();
          }
          /** The length of the total number of items that are being paginated. Defaulted to 0. */

        }, {
          key: "length",
          get: function get() {
            return this._length;
          },
          set: function set(value) {
            this._length = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_6__["coerceNumberProperty"])(value);

            this._changeDetectorRef.markForCheck();
          }
          /** Number of items to display on a page. By default set to 50. */

        }, {
          key: "pageSize",
          get: function get() {
            return this._pageSize;
          },
          set: function set(value) {
            this._pageSize = Math.max(Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_6__["coerceNumberProperty"])(value), 0);

            this._updateDisplayedPageSizeOptions();
          }
          /** The set of provided page size options to display to the user. */

        }, {
          key: "pageSizeOptions",
          get: function get() {
            return this._pageSizeOptions;
          },
          set: function set(value) {
            this._pageSizeOptions = (value || []).map(function (p) {
              return Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_6__["coerceNumberProperty"])(p);
            });

            this._updateDisplayedPageSizeOptions();
          }
          /** Whether to hide the page size selection UI from the user. */

        }, {
          key: "hidePageSize",
          get: function get() {
            return this._hidePageSize;
          },
          set: function set(value) {
            this._hidePageSize = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_6__["coerceBooleanProperty"])(value);
          }
          /** Whether to show the first/last buttons UI to the user. */

        }, {
          key: "showFirstLastButtons",
          get: function get() {
            return this._showFirstLastButtons;
          },
          set: function set(value) {
            this._showFirstLastButtons = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_6__["coerceBooleanProperty"])(value);
          }
        }]);

        return _MatPaginatorBase;
      }(_MatPaginatorMixinBase);

      _MatPaginatorBase.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Directive"]
      }];

      _MatPaginatorBase.ctorParameters = function () {
        return [{
          type: MatPaginatorIntl
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["ChangeDetectorRef"]
        }, {
          type: undefined
        }];
      };

      _MatPaginatorBase.propDecorators = {
        color: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"]
        }],
        pageIndex: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"]
        }],
        length: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"]
        }],
        pageSize: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"]
        }],
        pageSizeOptions: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"]
        }],
        hidePageSize: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"]
        }],
        showFirstLastButtons: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"]
        }],
        page: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Output"]
        }]
      };
      /**
       * Component to provide navigation between paged information. Displays the size of the current
       * page, user-selectable options to change that size, what items are being shown, and
       * navigational button to go to the previous or next page.
       */

      var MatPaginator = /*#__PURE__*/function (_MatPaginatorBase2) {
        _inherits(MatPaginator, _MatPaginatorBase2);

        var _super2 = _createSuper(MatPaginator);

        function MatPaginator(intl, changeDetectorRef, defaults) {
          var _this2;

          _classCallCheck(this, MatPaginator);

          _this2 = _super2.call(this, intl, changeDetectorRef, defaults);

          if (defaults && defaults.formFieldAppearance != null) {
            _this2._formFieldAppearance = defaults.formFieldAppearance;
          }

          return _this2;
        }

        return MatPaginator;
      }(_MatPaginatorBase);

      MatPaginator.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"],
        args: [{
          selector: 'mat-paginator',
          exportAs: 'matPaginator',
          template: "<div class=\"mat-paginator-outer-container\">\n  <div class=\"mat-paginator-container\">\n    <div class=\"mat-paginator-page-size\" *ngIf=\"!hidePageSize\">\n      <div class=\"mat-paginator-page-size-label\">\n        {{_intl.itemsPerPageLabel}}\n      </div>\n\n      <mat-form-field\n        *ngIf=\"_displayedPageSizeOptions.length > 1\"\n        [appearance]=\"_formFieldAppearance!\"\n        [color]=\"color\"\n        class=\"mat-paginator-page-size-select\">\n        <mat-select\n          [value]=\"pageSize\"\n          [disabled]=\"disabled\"\n          [aria-label]=\"_intl.itemsPerPageLabel\"\n          (selectionChange)=\"_changePageSize($event.value)\">\n          <mat-option *ngFor=\"let pageSizeOption of _displayedPageSizeOptions\" [value]=\"pageSizeOption\">\n            {{pageSizeOption}}\n          </mat-option>\n        </mat-select>\n      </mat-form-field>\n\n      <div\n        class=\"mat-paginator-page-size-value\"\n        *ngIf=\"_displayedPageSizeOptions.length <= 1\">{{pageSize}}</div>\n    </div>\n\n    <div class=\"mat-paginator-range-actions\">\n      <div class=\"mat-paginator-range-label\">\n        {{_intl.getRangeLabel(pageIndex, pageSize, length)}}\n      </div>\n\n      <button mat-icon-button type=\"button\"\n              class=\"mat-paginator-navigation-first\"\n              (click)=\"firstPage()\"\n              [attr.aria-label]=\"_intl.firstPageLabel\"\n              [matTooltip]=\"_intl.firstPageLabel\"\n              [matTooltipDisabled]=\"_previousButtonsDisabled()\"\n              [matTooltipPosition]=\"'above'\"\n              [disabled]=\"_previousButtonsDisabled()\"\n              *ngIf=\"showFirstLastButtons\">\n        <svg class=\"mat-paginator-icon\" viewBox=\"0 0 24 24\" focusable=\"false\">\n          <path d=\"M18.41 16.59L13.82 12l4.59-4.59L17 6l-6 6 6 6zM6 6h2v12H6z\"/>\n        </svg>\n      </button>\n      <button mat-icon-button type=\"button\"\n              class=\"mat-paginator-navigation-previous\"\n              (click)=\"previousPage()\"\n              [attr.aria-label]=\"_intl.previousPageLabel\"\n              [matTooltip]=\"_intl.previousPageLabel\"\n              [matTooltipDisabled]=\"_previousButtonsDisabled()\"\n              [matTooltipPosition]=\"'above'\"\n              [disabled]=\"_previousButtonsDisabled()\">\n        <svg class=\"mat-paginator-icon\" viewBox=\"0 0 24 24\" focusable=\"false\">\n          <path d=\"M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z\"/>\n        </svg>\n      </button>\n      <button mat-icon-button type=\"button\"\n              class=\"mat-paginator-navigation-next\"\n              (click)=\"nextPage()\"\n              [attr.aria-label]=\"_intl.nextPageLabel\"\n              [matTooltip]=\"_intl.nextPageLabel\"\n              [matTooltipDisabled]=\"_nextButtonsDisabled()\"\n              [matTooltipPosition]=\"'above'\"\n              [disabled]=\"_nextButtonsDisabled()\">\n        <svg class=\"mat-paginator-icon\" viewBox=\"0 0 24 24\" focusable=\"false\">\n          <path d=\"M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z\"/>\n        </svg>\n      </button>\n      <button mat-icon-button type=\"button\"\n              class=\"mat-paginator-navigation-last\"\n              (click)=\"lastPage()\"\n              [attr.aria-label]=\"_intl.lastPageLabel\"\n              [matTooltip]=\"_intl.lastPageLabel\"\n              [matTooltipDisabled]=\"_nextButtonsDisabled()\"\n              [matTooltipPosition]=\"'above'\"\n              [disabled]=\"_nextButtonsDisabled()\"\n              *ngIf=\"showFirstLastButtons\">\n        <svg class=\"mat-paginator-icon\" viewBox=\"0 0 24 24\" focusable=\"false\">\n          <path d=\"M5.59 7.41L10.18 12l-4.59 4.59L7 18l6-6-6-6zM16 6h2v12h-2z\"/>\n        </svg>\n      </button>\n    </div>\n  </div>\n</div>\n",
          inputs: ['disabled'],
          host: {
            'class': 'mat-paginator'
          },
          changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_1__["ChangeDetectionStrategy"].OnPush,
          encapsulation: _angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewEncapsulation"].None,
          styles: [".mat-paginator{display:block}.mat-paginator-outer-container{display:flex}.mat-paginator-container{display:flex;align-items:center;justify-content:flex-end;padding:0 8px;flex-wrap:wrap-reverse;width:100%}.mat-paginator-page-size{display:flex;align-items:baseline;margin-right:8px}[dir=rtl] .mat-paginator-page-size{margin-right:0;margin-left:8px}.mat-paginator-page-size-label{margin:0 4px}.mat-paginator-page-size-select{margin:6px 4px 0 4px;width:56px}.mat-paginator-page-size-select.mat-form-field-appearance-outline{width:64px}.mat-paginator-page-size-select.mat-form-field-appearance-fill{width:64px}.mat-paginator-range-label{margin:0 32px 0 24px}.mat-paginator-range-actions{display:flex;align-items:center}.mat-paginator-icon{width:28px;fill:currentColor}[dir=rtl] .mat-paginator-icon{transform:rotate(180deg)}\n"]
        }]
      }];

      MatPaginator.ctorParameters = function () {
        return [{
          type: MatPaginatorIntl
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["ChangeDetectorRef"]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Optional"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Inject"],
            args: [MAT_PAGINATOR_DEFAULT_OPTIONS]
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


      var MatPaginatorModule = function MatPaginatorModule() {
        _classCallCheck(this, MatPaginatorModule);
      };

      MatPaginatorModule.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"],
        args: [{
          imports: [_angular_common__WEBPACK_IMPORTED_MODULE_0__["CommonModule"], _angular_material_button__WEBPACK_IMPORTED_MODULE_3__["MatButtonModule"], _angular_material_select__WEBPACK_IMPORTED_MODULE_4__["MatSelectModule"], _angular_material_tooltip__WEBPACK_IMPORTED_MODULE_5__["MatTooltipModule"], _angular_material_core__WEBPACK_IMPORTED_MODULE_2__["MatCommonModule"]],
          exports: [MatPaginator],
          declarations: [MatPaginator],
          providers: [MAT_PAGINATOR_INTL_PROVIDER]
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
      //# sourceMappingURL=paginator.js.map

      /***/
    },

    /***/
    "7lCJ":
    /*!***************************************************************!*\
      !*** ./src/@vex/components/page-layout/page-layout.module.ts ***!
      \***************************************************************/

    /*! exports provided: PageLayoutModule */

    /***/
    function lCJ(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "PageLayoutModule", function () {
        return PageLayoutModule;
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


      var _page_layout_content_directive__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! ./page-layout-content.directive */
      "C0s9");
      /* harmony import */


      var _page_layout_header_directive__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! ./page-layout-header.directive */
      "uwSD");
      /* harmony import */


      var _page_layout_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! ./page-layout.component */
      "ZuBe");

      var PageLayoutModule = function PageLayoutModule() {
        _classCallCheck(this, PageLayoutModule);
      };

      PageLayoutModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"]],
        declarations: [_page_layout_component__WEBPACK_IMPORTED_MODULE_5__["PageLayoutComponent"], _page_layout_header_directive__WEBPACK_IMPORTED_MODULE_4__["PageLayoutHeaderDirective"], _page_layout_content_directive__WEBPACK_IMPORTED_MODULE_3__["PageLayoutContentDirective"]],
        exports: [_page_layout_component__WEBPACK_IMPORTED_MODULE_5__["PageLayoutComponent"], _page_layout_header_directive__WEBPACK_IMPORTED_MODULE_4__["PageLayoutHeaderDirective"], _page_layout_content_directive__WEBPACK_IMPORTED_MODULE_3__["PageLayoutContentDirective"]]
      })], PageLayoutModule);
      /***/
    },

    /***/
    "7wwx":
    /*!*******************************************************!*\
      !*** ./node_modules/@iconify/icons-ic/twotone-add.js ***!
      \*******************************************************/

    /*! no static exports found */

    /***/
    function wwx(module, exports) {
      var data = {
        "body": "<path d=\"M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z\" fill=\"currentColor\"/>",
        "width": 24,
        "height": 24
      };
      exports.__esModule = true;
      exports["default"] = data;
      /***/
    },

    /***/
    "8FT2":
    /*!********************************************************************!*\
      !*** ./src/@vex/components/page-layout/page-layout.component.scss ***!
      \********************************************************************/

    /*! exports provided: default */

    /***/
    function FT2(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = ".vex-layout-theme-contrast {\n  --text-opacity: 1;\n  color: #FFF;\n  color: rgba(255, 255, 255, var(--text-opacity));\n}\n\n.vex-layout-theme-bg {\n  --bg-opacity: 1;\n  background-color: #5c77ff;\n  background-color: rgba(92, 119, 255, var(--bg-opacity));\n}\n\n.vex-layout-theme {\n  --bg-opacity: 1;\n  background-color: #5c77ff;\n  background-color: rgba(92, 119, 255, var(--bg-opacity));\n  --text-opacity: 1;\n  color: #FFF;\n  color: rgba(255, 255, 255, var(--text-opacity));\n}\n\n.vex-page-layout {\n  display: block;\n}\n\n.vex-page-layout-simple .vex-page-layout-content {\n  padding-bottom: var(--padding-gutter);\n  padding-top: var(--padding-gutter);\n}\n\n.vex-page-layout-card {\n  padding-bottom: var(--padding);\n}\n\n.vex-page-layout-card .vex-page-layout-header {\n  margin-bottom: calc(var(--page-layout-toolbar-height) * -1);\n  padding-bottom: var(--page-layout-toolbar-height);\n}\n\n.vex-page-layout-card .vex-page-layout-content > * > .mat-tab-group .mat-tab-label,\n.vex-page-layout-card .vex-page-layout-content > .mat-tab-group .mat-tab-label {\n  height: var(--page-layout-toolbar-height);\n}\n\n.vex-page-layout-card .vex-page-layout-content > * > .mat-tab-group .mat-tab-label.mat-tab-label-active,\n.vex-page-layout-card .vex-page-layout-content > .mat-tab-group .mat-tab-label.mat-tab-label-active {\n  opacity: 1;\n}\n\n.vex-page-layout-header {\n  align-items: center;\n  box-sizing: content-box !important;\n  display: flex;\n  flex-direction: row;\n  height: calc(var(--page-layout-header-height) - var(--page-layout-toolbar-height));\n  padding-left: var(--padding);\n  padding-right: var(--padding);\n  place-content: center flex-start;\n}\n\n.vex-page-layout-header .vex-breadcrumb a {\n  --text-opacity: 1;\n  color: #FFF;\n  color: rgba(255, 255, 255, var(--text-opacity));\n  opacity: 0.5;\n}\n\n.vex-page-layout-header .vex-breadcrumb a:hover {\n  --text-opacity: 1;\n  color: #FFF;\n  color: rgba(255, 255, 255, var(--text-opacity));\n  opacity: 1;\n}\n\n.vex-page-layout-header .vex-breadcrumb span {\n  --text-opacity: 1;\n  color: #FFF;\n  color: rgba(255, 255, 255, var(--text-opacity));\n  opacity: 1;\n}\n\n.vex-page-layout-content {\n  box-sizing: border-box;\n  display: block;\n  padding-left: var(--padding-gutter);\n  padding-right: var(--padding-gutter);\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uL3BhZ2UtbGF5b3V0LmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0VBQ0UsaUJBQUE7RUFDQSxXQUFBO0VBQ0EsK0NBQUE7QUFDRjs7QUFFQTtFQUNFLGVBQUE7RUFDQSx5QkFBQTtFQUNBLHVEQUFBO0FBQ0Y7O0FBRUE7RUFDRSxlQUFBO0VBQ0EseUJBQUE7RUFDQSx1REFBQTtFQUNBLGlCQUFBO0VBQ0EsV0FBQTtFQUNBLCtDQUFBO0FBQ0Y7O0FBRUE7RUFDRSxjQUFBO0FBQ0Y7O0FBRUE7RUFDRSxxQ0FBQTtFQUNBLGtDQUFBO0FBQ0Y7O0FBRUE7RUFDRSw4QkFBQTtBQUNGOztBQUVBO0VBQ0UsMkRBQUE7RUFDQSxpREFBQTtBQUNGOztBQUVBOztFQUVFLHlDQUFBO0FBQ0Y7O0FBRUE7O0VBRUUsVUFBQTtBQUNGOztBQUVBO0VBQ0UsbUJBQUE7RUFDQSxrQ0FBQTtFQUNBLGFBQUE7RUFDQSxtQkFBQTtFQUNBLGtGQUFBO0VBQ0EsNEJBQUE7RUFDQSw2QkFBQTtFQUNBLGdDQUFBO0FBQ0Y7O0FBRUE7RUFDRSxpQkFBQTtFQUNBLFdBQUE7RUFDQSwrQ0FBQTtFQUNBLFlBQUE7QUFDRjs7QUFFQTtFQUNFLGlCQUFBO0VBQ0EsV0FBQTtFQUNBLCtDQUFBO0VBQ0EsVUFBQTtBQUNGOztBQUVBO0VBQ0UsaUJBQUE7RUFDQSxXQUFBO0VBQ0EsK0NBQUE7RUFDQSxVQUFBO0FBQ0Y7O0FBRUE7RUFDRSxzQkFBQTtFQUNBLGNBQUE7RUFDQSxtQ0FBQTtFQUNBLG9DQUFBO0FBQ0YiLCJmaWxlIjoicGFnZS1sYXlvdXQuY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyIudmV4LWxheW91dC10aGVtZS1jb250cmFzdCB7XG4gIC0tdGV4dC1vcGFjaXR5OiAxO1xuICBjb2xvcjogI0ZGRjtcbiAgY29sb3I6IHJnYmEoMjU1LCAyNTUsIDI1NSwgdmFyKC0tdGV4dC1vcGFjaXR5KSk7XG59XG5cbi52ZXgtbGF5b3V0LXRoZW1lLWJnIHtcbiAgLS1iZy1vcGFjaXR5OiAxO1xuICBiYWNrZ3JvdW5kLWNvbG9yOiAjNWM3N2ZmO1xuICBiYWNrZ3JvdW5kLWNvbG9yOiByZ2JhKDkyLCAxMTksIDI1NSwgdmFyKC0tYmctb3BhY2l0eSkpO1xufVxuXG4udmV4LWxheW91dC10aGVtZSB7XG4gIC0tYmctb3BhY2l0eTogMTtcbiAgYmFja2dyb3VuZC1jb2xvcjogIzVjNzdmZjtcbiAgYmFja2dyb3VuZC1jb2xvcjogcmdiYSg5MiwgMTE5LCAyNTUsIHZhcigtLWJnLW9wYWNpdHkpKTtcbiAgLS10ZXh0LW9wYWNpdHk6IDE7XG4gIGNvbG9yOiAjRkZGO1xuICBjb2xvcjogcmdiYSgyNTUsIDI1NSwgMjU1LCB2YXIoLS10ZXh0LW9wYWNpdHkpKTtcbn1cblxuLnZleC1wYWdlLWxheW91dCB7XG4gIGRpc3BsYXk6IGJsb2NrO1xufVxuXG4udmV4LXBhZ2UtbGF5b3V0LXNpbXBsZSAudmV4LXBhZ2UtbGF5b3V0LWNvbnRlbnQge1xuICBwYWRkaW5nLWJvdHRvbTogdmFyKC0tcGFkZGluZy1ndXR0ZXIpO1xuICBwYWRkaW5nLXRvcDogdmFyKC0tcGFkZGluZy1ndXR0ZXIpO1xufVxuXG4udmV4LXBhZ2UtbGF5b3V0LWNhcmQge1xuICBwYWRkaW5nLWJvdHRvbTogdmFyKC0tcGFkZGluZyk7XG59XG5cbi52ZXgtcGFnZS1sYXlvdXQtY2FyZCAudmV4LXBhZ2UtbGF5b3V0LWhlYWRlciB7XG4gIG1hcmdpbi1ib3R0b206IGNhbGModmFyKC0tcGFnZS1sYXlvdXQtdG9vbGJhci1oZWlnaHQpICogLTEpO1xuICBwYWRkaW5nLWJvdHRvbTogdmFyKC0tcGFnZS1sYXlvdXQtdG9vbGJhci1oZWlnaHQpO1xufVxuXG4udmV4LXBhZ2UtbGF5b3V0LWNhcmQgLnZleC1wYWdlLWxheW91dC1jb250ZW50ID4gKiA+IC5tYXQtdGFiLWdyb3VwIC5tYXQtdGFiLWxhYmVsLFxuLnZleC1wYWdlLWxheW91dC1jYXJkIC52ZXgtcGFnZS1sYXlvdXQtY29udGVudCA+IC5tYXQtdGFiLWdyb3VwIC5tYXQtdGFiLWxhYmVsIHtcbiAgaGVpZ2h0OiB2YXIoLS1wYWdlLWxheW91dC10b29sYmFyLWhlaWdodCk7XG59XG5cbi52ZXgtcGFnZS1sYXlvdXQtY2FyZCAudmV4LXBhZ2UtbGF5b3V0LWNvbnRlbnQgPiAqID4gLm1hdC10YWItZ3JvdXAgLm1hdC10YWItbGFiZWwubWF0LXRhYi1sYWJlbC1hY3RpdmUsXG4udmV4LXBhZ2UtbGF5b3V0LWNhcmQgLnZleC1wYWdlLWxheW91dC1jb250ZW50ID4gLm1hdC10YWItZ3JvdXAgLm1hdC10YWItbGFiZWwubWF0LXRhYi1sYWJlbC1hY3RpdmUge1xuICBvcGFjaXR5OiAxO1xufVxuXG4udmV4LXBhZ2UtbGF5b3V0LWhlYWRlciB7XG4gIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG4gIGJveC1zaXppbmc6IGNvbnRlbnQtYm94ICFpbXBvcnRhbnQ7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGZsZXgtZGlyZWN0aW9uOiByb3c7XG4gIGhlaWdodDogY2FsYyh2YXIoLS1wYWdlLWxheW91dC1oZWFkZXItaGVpZ2h0KSAtIHZhcigtLXBhZ2UtbGF5b3V0LXRvb2xiYXItaGVpZ2h0KSk7XG4gIHBhZGRpbmctbGVmdDogdmFyKC0tcGFkZGluZyk7XG4gIHBhZGRpbmctcmlnaHQ6IHZhcigtLXBhZGRpbmcpO1xuICBwbGFjZS1jb250ZW50OiBjZW50ZXIgZmxleC1zdGFydDtcbn1cblxuLnZleC1wYWdlLWxheW91dC1oZWFkZXIgLnZleC1icmVhZGNydW1iIGEge1xuICAtLXRleHQtb3BhY2l0eTogMTtcbiAgY29sb3I6ICNGRkY7XG4gIGNvbG9yOiByZ2JhKDI1NSwgMjU1LCAyNTUsIHZhcigtLXRleHQtb3BhY2l0eSkpO1xuICBvcGFjaXR5OiAwLjU7XG59XG5cbi52ZXgtcGFnZS1sYXlvdXQtaGVhZGVyIC52ZXgtYnJlYWRjcnVtYiBhOmhvdmVyIHtcbiAgLS10ZXh0LW9wYWNpdHk6IDE7XG4gIGNvbG9yOiAjRkZGO1xuICBjb2xvcjogcmdiYSgyNTUsIDI1NSwgMjU1LCB2YXIoLS10ZXh0LW9wYWNpdHkpKTtcbiAgb3BhY2l0eTogMTtcbn1cblxuLnZleC1wYWdlLWxheW91dC1oZWFkZXIgLnZleC1icmVhZGNydW1iIHNwYW4ge1xuICAtLXRleHQtb3BhY2l0eTogMTtcbiAgY29sb3I6ICNGRkY7XG4gIGNvbG9yOiByZ2JhKDI1NSwgMjU1LCAyNTUsIHZhcigtLXRleHQtb3BhY2l0eSkpO1xuICBvcGFjaXR5OiAxO1xufVxuXG4udmV4LXBhZ2UtbGF5b3V0LWNvbnRlbnQge1xuICBib3gtc2l6aW5nOiBib3JkZXItYm94O1xuICBkaXNwbGF5OiBibG9jaztcbiAgcGFkZGluZy1sZWZ0OiB2YXIoLS1wYWRkaW5nLWd1dHRlcik7XG4gIHBhZGRpbmctcmlnaHQ6IHZhcigtLXBhZGRpbmctZ3V0dGVyKTtcbn0iXX0= */";
      /***/
    },

    /***/
    "C0s9":
    /*!**************************************************************************!*\
      !*** ./src/@vex/components/page-layout/page-layout-content.directive.ts ***!
      \**************************************************************************/

    /*! exports provided: PageLayoutContentDirective */

    /***/
    function C0s9(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "PageLayoutContentDirective", function () {
        return PageLayoutContentDirective;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");

      var PageLayoutContentDirective = function PageLayoutContentDirective() {
        _classCallCheck(this, PageLayoutContentDirective);
      };

      PageLayoutContentDirective.ctorParameters = function () {
        return [];
      };

      PageLayoutContentDirective = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Directive"])({
        selector: '[vexPageLayoutContent],vex-page-layout-content',
        host: {
          "class": 'vex-page-layout-content'
        }
      })], PageLayoutContentDirective);
      /***/
    },

    /***/
    "EGFe":
    /*!********************************************!*\
      !*** ./src/app/core/utils/file.service.ts ***!
      \********************************************/

    /*! exports provided: FileService */

    /***/
    function EGFe(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "FileService", function () {
        return FileService;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");

      var FileService = /*#__PURE__*/function () {
        function FileService() {
          _classCallCheck(this, FileService);
        }

        _createClass(FileService, [{
          key: "basename",
          value: function basename(path) {
            var slashIndex = path.lastIndexOf('/');
            return path.substr(slashIndex + 1);
          }
        }, {
          key: "join",
          value: function join() {
            var path = arguments.length <= 0 ? undefined : arguments[0];
            var len = arguments.length;

            for (var i = 1; i < len; ++i) {
              var pathLen = path.length;
              var tok = i < 0 || arguments.length <= i ? undefined : arguments[i];

              if (tok[0] === '/') {
                tok = tok.replace('/', '');
              }

              if (path[pathLen - 1] === '/') {
                path += tok;
              } else {
                path += '/' + tok;
              }
            }

            return path;
          }
        }, {
          key: "dirname",
          value: function dirname(path) {
            if (!path) {
              return;
            }

            var slashIndex = path.lastIndexOf('/');

            if (slashIndex === 0) {
              return '/';
            }

            return path.substr(0, slashIndex);
          }
        }, {
          key: "extension",
          value: function extension(path) {
            var dotIndex = path.lastIndexOf('.');

            if (dotIndex === -1) {
              return undefined;
            }

            return path.substr(dotIndex + 1);
          }
        }, {
          key: "hrefAppend",
          value: function hrefAppend(href, path) {
            var index = href.indexOf('?');
            var p = href.substring(0, index);
            p = this.join(p.length === 0 ? href : p, path);

            if (index !== -1) {
              return p + href.substr(index);
            } else {
              return p;
            }
          }
        }]);

        return FileService;
      }();

      FileService.ctorParameters = function () {
        return [];
      };

      FileService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], FileService);
      /***/
    },

    /***/
    "GXRp":
    /*!*****************************************************!*\
      !*** ./node_modules/@angular/cdk/fesm2015/table.js ***!
      \*****************************************************/

    /*! exports provided: DataSource, BaseCdkCell, BaseRowDef, CDK_ROW_TEMPLATE, CDK_TABLE, CDK_TABLE_TEMPLATE, CdkCell, CdkCellDef, CdkCellOutlet, CdkColumnDef, CdkFooterCell, CdkFooterCellDef, CdkFooterRow, CdkFooterRowDef, CdkHeaderCell, CdkHeaderCellDef, CdkHeaderRow, CdkHeaderRowDef, CdkNoDataRow, CdkRow, CdkRowDef, CdkTable, CdkTableModule, CdkTextColumn, DataRowOutlet, FooterRowOutlet, HeaderRowOutlet, NoDataRowOutlet, STICKY_DIRECTIONS, StickyStyler, TEXT_COLUMN_OPTIONS, _COALESCED_STYLE_SCHEDULER, _CoalescedStyleScheduler, _Schedule, mixinHasStickyInput */

    /***/
    function GXRp(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "BaseCdkCell", function () {
        return BaseCdkCell;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "BaseRowDef", function () {
        return BaseRowDef;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CDK_ROW_TEMPLATE", function () {
        return CDK_ROW_TEMPLATE;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CDK_TABLE", function () {
        return CDK_TABLE;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CDK_TABLE_TEMPLATE", function () {
        return CDK_TABLE_TEMPLATE;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkCell", function () {
        return CdkCell;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkCellDef", function () {
        return CdkCellDef;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkCellOutlet", function () {
        return CdkCellOutlet;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkColumnDef", function () {
        return CdkColumnDef;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkFooterCell", function () {
        return CdkFooterCell;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkFooterCellDef", function () {
        return CdkFooterCellDef;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkFooterRow", function () {
        return CdkFooterRow;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkFooterRowDef", function () {
        return CdkFooterRowDef;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkHeaderCell", function () {
        return CdkHeaderCell;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkHeaderCellDef", function () {
        return CdkHeaderCellDef;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkHeaderRow", function () {
        return CdkHeaderRow;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkHeaderRowDef", function () {
        return CdkHeaderRowDef;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkNoDataRow", function () {
        return CdkNoDataRow;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkRow", function () {
        return CdkRow;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkRowDef", function () {
        return CdkRowDef;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkTable", function () {
        return CdkTable;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkTableModule", function () {
        return CdkTableModule;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "CdkTextColumn", function () {
        return CdkTextColumn;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "DataRowOutlet", function () {
        return DataRowOutlet;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "FooterRowOutlet", function () {
        return FooterRowOutlet;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "HeaderRowOutlet", function () {
        return HeaderRowOutlet;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "NoDataRowOutlet", function () {
        return NoDataRowOutlet;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "STICKY_DIRECTIONS", function () {
        return STICKY_DIRECTIONS;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "StickyStyler", function () {
        return StickyStyler;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "TEXT_COLUMN_OPTIONS", function () {
        return TEXT_COLUMN_OPTIONS;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "_COALESCED_STYLE_SCHEDULER", function () {
        return _COALESCED_STYLE_SCHEDULER;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "_CoalescedStyleScheduler", function () {
        return _CoalescedStyleScheduler;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "_Schedule", function () {
        return _Schedule;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "mixinHasStickyInput", function () {
        return mixinHasStickyInput;
      });
      /* harmony import */


      var _angular_cdk_bidi__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! @angular/cdk/bidi */
      "9gLZ");
      /* harmony import */


      var _angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! @angular/cdk/coercion */
      "8LU1");
      /* harmony import */


      var _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @angular/cdk/collections */
      "CtHx");
      /* harmony reexport (safe) */


      __webpack_require__.d(__webpack_exports__, "DataSource", function () {
        return _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_2__["DataSource"];
      });
      /* harmony import */


      var _angular_cdk_platform__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/cdk/platform */
      "SCoL");
      /* harmony import */


      var _angular_cdk_scrolling__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/cdk/scrolling */
      "7KAL");
      /* harmony import */


      var _angular_common__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/common */
      "SVse");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var rxjs__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! rxjs */
      "qCKp");
      /* harmony import */


      var rxjs_operators__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! rxjs/operators */
      "kU1M");
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * Mixin to provide a directive with a function that checks if the sticky input has been
       * changed since the last time the function was called. Essentially adds a dirty-check to the
       * sticky value.
       * @docs-private
       */


      function mixinHasStickyInput(base) {
        return /*#__PURE__*/function (_base) {
          _inherits(_class, _base);

          var _super3 = _createSuper(_class);

          function _class() {
            var _this3;

            _classCallCheck(this, _class);

            for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
              args[_key] = arguments[_key];
            }

            _this3 = _super3.call.apply(_super3, [this].concat(args));
            _this3._sticky = false;
            /** Whether the sticky input has changed since it was last checked. */

            _this3._hasStickyChanged = false;
            return _this3;
          }
          /** Whether sticky positioning should be applied. */


          _createClass(_class, [{
            key: "hasStickyChanged",

            /** Whether the sticky value has changed since this was last called. */
            value: function hasStickyChanged() {
              var hasStickyChanged = this._hasStickyChanged;
              this._hasStickyChanged = false;
              return hasStickyChanged;
            }
            /** Resets the dirty check for cases where the sticky state has been used without checking. */

          }, {
            key: "resetStickyChanged",
            value: function resetStickyChanged() {
              this._hasStickyChanged = false;
            }
          }, {
            key: "sticky",
            get: function get() {
              return this._sticky;
            },
            set: function set(v) {
              var prevValue = this._sticky;
              this._sticky = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_1__["coerceBooleanProperty"])(v);
              this._hasStickyChanged = prevValue !== this._sticky;
            }
          }]);

          return _class;
        }(base);
      }
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * Used to provide a table to some of the sub-components without causing a circular dependency.
       * @docs-private
       */


      var CDK_TABLE = new _angular_core__WEBPACK_IMPORTED_MODULE_6__["InjectionToken"]('CDK_TABLE');
      /** Injection token that can be used to specify the text column options. */

      var TEXT_COLUMN_OPTIONS = new _angular_core__WEBPACK_IMPORTED_MODULE_6__["InjectionToken"]('text-column-options');
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * Cell definition for a CDK table.
       * Captures the template of a column's data row cell as well as cell-specific properties.
       */

      var CdkCellDef = function CdkCellDef(
      /** @docs-private */
      template) {
        _classCallCheck(this, CdkCellDef);

        this.template = template;
      };

      CdkCellDef.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Directive"],
        args: [{
          selector: '[cdkCellDef]'
        }]
      }];

      CdkCellDef.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["TemplateRef"]
        }];
      };
      /**
       * Header cell definition for a CDK table.
       * Captures the template of a column's header cell and as well as cell-specific properties.
       */


      var CdkHeaderCellDef = function CdkHeaderCellDef(
      /** @docs-private */
      template) {
        _classCallCheck(this, CdkHeaderCellDef);

        this.template = template;
      };

      CdkHeaderCellDef.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Directive"],
        args: [{
          selector: '[cdkHeaderCellDef]'
        }]
      }];

      CdkHeaderCellDef.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["TemplateRef"]
        }];
      };
      /**
       * Footer cell definition for a CDK table.
       * Captures the template of a column's footer cell and as well as cell-specific properties.
       */


      var CdkFooterCellDef = function CdkFooterCellDef(
      /** @docs-private */
      template) {
        _classCallCheck(this, CdkFooterCellDef);

        this.template = template;
      };

      CdkFooterCellDef.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Directive"],
        args: [{
          selector: '[cdkFooterCellDef]'
        }]
      }];

      CdkFooterCellDef.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["TemplateRef"]
        }];
      }; // Boilerplate for applying mixins to CdkColumnDef.

      /** @docs-private */


      var CdkColumnDefBase = function CdkColumnDefBase() {
        _classCallCheck(this, CdkColumnDefBase);
      };

      var _CdkColumnDefBase = mixinHasStickyInput(CdkColumnDefBase);
      /**
       * Column definition for the CDK table.
       * Defines a set of cells available for a table column.
       */


      var CdkColumnDef = /*#__PURE__*/function (_CdkColumnDefBase2) {
        _inherits(CdkColumnDef, _CdkColumnDefBase2);

        var _super4 = _createSuper(CdkColumnDef);

        function CdkColumnDef(_table) {
          var _this4;

          _classCallCheck(this, CdkColumnDef);

          _this4 = _super4.call(this);
          _this4._table = _table;
          _this4._stickyEnd = false;
          return _this4;
        }
        /** Unique name for this column. */


        _createClass(CdkColumnDef, [{
          key: "_updateColumnCssClassName",

          /**
           * Overridable method that sets the css classes that will be added to every cell in this
           * column.
           * In the future, columnCssClassName will change from type string[] to string and this
           * will set a single string value.
           * @docs-private
           */
          value: function _updateColumnCssClassName() {
            this._columnCssClassName = ["cdk-column-".concat(this.cssClassFriendlyName)];
          }
          /**
           * This has been extracted to a util because of TS 4 and VE.
           * View Engine doesn't support property rename inheritance.
           * TS 4.0 doesn't allow properties to override accessors or vice-versa.
           * @docs-private
           */

        }, {
          key: "_setNameInput",
          value: function _setNameInput(value) {
            // If the directive is set without a name (updated programatically), then this setter will
            // trigger with an empty string and should not overwrite the programatically set value.
            if (value) {
              this._name = value;
              this.cssClassFriendlyName = value.replace(/[^a-z0-9_-]/ig, '-');

              this._updateColumnCssClassName();
            }
          }
        }, {
          key: "name",
          get: function get() {
            return this._name;
          },
          set: function set(name) {
            this._setNameInput(name);
          }
          /**
           * Whether this column should be sticky positioned on the end of the row. Should make sure
           * that it mimics the `CanStick` mixin such that `_hasStickyChanged` is set to true if the value
           * has been changed.
           */

        }, {
          key: "stickyEnd",
          get: function get() {
            return this._stickyEnd;
          },
          set: function set(v) {
            var prevValue = this._stickyEnd;
            this._stickyEnd = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_1__["coerceBooleanProperty"])(v);
            this._hasStickyChanged = prevValue !== this._stickyEnd;
          }
        }]);

        return CdkColumnDef;
      }(_CdkColumnDefBase);

      CdkColumnDef.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Directive"],
        args: [{
          selector: '[cdkColumnDef]',
          inputs: ['sticky'],
          providers: [{
            provide: 'MAT_SORT_HEADER_COLUMN_DEF',
            useExisting: CdkColumnDef
          }]
        }]
      }];

      CdkColumnDef.ctorParameters = function () {
        return [{
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Inject"],
            args: [CDK_TABLE]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Optional"]
          }]
        }];
      };

      CdkColumnDef.propDecorators = {
        name: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Input"],
          args: ['cdkColumnDef']
        }],
        stickyEnd: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Input"],
          args: ['stickyEnd']
        }],
        cell: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ContentChild"],
          args: [CdkCellDef]
        }],
        headerCell: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ContentChild"],
          args: [CdkHeaderCellDef]
        }],
        footerCell: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ContentChild"],
          args: [CdkFooterCellDef]
        }]
      };
      /** Base class for the cells. Adds a CSS classname that identifies the column it renders in. */

      var BaseCdkCell = function BaseCdkCell(columnDef, elementRef) {
        _classCallCheck(this, BaseCdkCell);

        // If IE 11 is dropped before we switch to setting a single class name, change to multi param
        // with destructuring.
        var classList = elementRef.nativeElement.classList;

        var _iterator = _createForOfIteratorHelper(columnDef._columnCssClassName),
            _step;

        try {
          for (_iterator.s(); !(_step = _iterator.n()).done;) {
            var className = _step.value;
            classList.add(className);
          }
        } catch (err) {
          _iterator.e(err);
        } finally {
          _iterator.f();
        }
      };
      /** Header cell template container that adds the right classes and role. */


      var CdkHeaderCell = /*#__PURE__*/function (_BaseCdkCell) {
        _inherits(CdkHeaderCell, _BaseCdkCell);

        var _super5 = _createSuper(CdkHeaderCell);

        function CdkHeaderCell(columnDef, elementRef) {
          _classCallCheck(this, CdkHeaderCell);

          return _super5.call(this, columnDef, elementRef);
        }

        return CdkHeaderCell;
      }(BaseCdkCell);

      CdkHeaderCell.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Directive"],
        args: [{
          selector: 'cdk-header-cell, th[cdk-header-cell]',
          host: {
            'class': 'cdk-header-cell',
            'role': 'columnheader'
          }
        }]
      }];

      CdkHeaderCell.ctorParameters = function () {
        return [{
          type: CdkColumnDef
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ElementRef"]
        }];
      };
      /** Footer cell template container that adds the right classes and role. */


      var CdkFooterCell = /*#__PURE__*/function (_BaseCdkCell2) {
        _inherits(CdkFooterCell, _BaseCdkCell2);

        var _super6 = _createSuper(CdkFooterCell);

        function CdkFooterCell(columnDef, elementRef) {
          _classCallCheck(this, CdkFooterCell);

          return _super6.call(this, columnDef, elementRef);
        }

        return CdkFooterCell;
      }(BaseCdkCell);

      CdkFooterCell.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Directive"],
        args: [{
          selector: 'cdk-footer-cell, td[cdk-footer-cell]',
          host: {
            'class': 'cdk-footer-cell',
            'role': 'gridcell'
          }
        }]
      }];

      CdkFooterCell.ctorParameters = function () {
        return [{
          type: CdkColumnDef
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ElementRef"]
        }];
      };
      /** Cell template container that adds the right classes and role. */


      var CdkCell = /*#__PURE__*/function (_BaseCdkCell3) {
        _inherits(CdkCell, _BaseCdkCell3);

        var _super7 = _createSuper(CdkCell);

        function CdkCell(columnDef, elementRef) {
          _classCallCheck(this, CdkCell);

          return _super7.call(this, columnDef, elementRef);
        }

        return CdkCell;
      }(BaseCdkCell);

      CdkCell.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Directive"],
        args: [{
          selector: 'cdk-cell, td[cdk-cell]',
          host: {
            'class': 'cdk-cell',
            'role': 'gridcell'
          }
        }]
      }];

      CdkCell.ctorParameters = function () {
        return [{
          type: CdkColumnDef
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ElementRef"]
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
       * @docs-private
       */


      var _Schedule = function _Schedule() {
        _classCallCheck(this, _Schedule);

        this.tasks = [];
        this.endTasks = [];
      };
      /** Injection token used to provide a coalesced style scheduler. */


      var _COALESCED_STYLE_SCHEDULER = new _angular_core__WEBPACK_IMPORTED_MODULE_6__["InjectionToken"]('_COALESCED_STYLE_SCHEDULER');
      /**
       * Allows grouping up CSSDom mutations after the current execution context.
       * This can significantly improve performance when separate consecutive functions are
       * reading from the CSSDom and then mutating it.
       *
       * @docs-private
       */


      var _CoalescedStyleScheduler = /*#__PURE__*/function () {
        function _CoalescedStyleScheduler(_ngZone) {
          _classCallCheck(this, _CoalescedStyleScheduler);

          this._ngZone = _ngZone;
          this._currentSchedule = null;
          this._destroyed = new rxjs__WEBPACK_IMPORTED_MODULE_7__["Subject"]();
        }
        /**
         * Schedules the specified task to run at the end of the current VM turn.
         */


        _createClass(_CoalescedStyleScheduler, [{
          key: "schedule",
          value: function schedule(task) {
            this._createScheduleIfNeeded();

            this._currentSchedule.tasks.push(task);
          }
          /**
           * Schedules the specified task to run after other scheduled tasks at the end of the current
           * VM turn.
           */

        }, {
          key: "scheduleEnd",
          value: function scheduleEnd(task) {
            this._createScheduleIfNeeded();

            this._currentSchedule.endTasks.push(task);
          }
          /** Prevent any further tasks from running. */

        }, {
          key: "ngOnDestroy",
          value: function ngOnDestroy() {
            this._destroyed.next();

            this._destroyed.complete();
          }
        }, {
          key: "_createScheduleIfNeeded",
          value: function _createScheduleIfNeeded() {
            var _this5 = this;

            if (this._currentSchedule) {
              return;
            }

            this._currentSchedule = new _Schedule();

            this._getScheduleObservable().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_8__["takeUntil"])(this._destroyed)).subscribe(function () {
              while (_this5._currentSchedule.tasks.length || _this5._currentSchedule.endTasks.length) {
                var schedule = _this5._currentSchedule; // Capture new tasks scheduled by the current set of tasks.

                _this5._currentSchedule = new _Schedule();

                var _iterator2 = _createForOfIteratorHelper(schedule.tasks),
                    _step2;

                try {
                  for (_iterator2.s(); !(_step2 = _iterator2.n()).done;) {
                    var task = _step2.value;
                    task();
                  }
                } catch (err) {
                  _iterator2.e(err);
                } finally {
                  _iterator2.f();
                }

                var _iterator3 = _createForOfIteratorHelper(schedule.endTasks),
                    _step3;

                try {
                  for (_iterator3.s(); !(_step3 = _iterator3.n()).done;) {
                    var _task = _step3.value;

                    _task();
                  }
                } catch (err) {
                  _iterator3.e(err);
                } finally {
                  _iterator3.f();
                }
              }

              _this5._currentSchedule = null;
            });
          }
        }, {
          key: "_getScheduleObservable",
          value: function _getScheduleObservable() {
            // Use onStable when in the context of an ongoing change detection cycle so that we
            // do not accidentally trigger additional cycles.
            return this._ngZone.isStable ? Object(rxjs__WEBPACK_IMPORTED_MODULE_7__["from"])(Promise.resolve(undefined)) : this._ngZone.onStable.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_8__["take"])(1));
          }
        }]);

        return _CoalescedStyleScheduler;
      }();

      _CoalescedStyleScheduler.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Injectable"]
      }];

      _CoalescedStyleScheduler.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["NgZone"]
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
       * The row template that can be used by the mat-table. Should not be used outside of the
       * material library.
       */


      var CDK_ROW_TEMPLATE = "<ng-container cdkCellOutlet></ng-container>";
      /**
       * Base class for the CdkHeaderRowDef and CdkRowDef that handles checking their columns inputs
       * for changes and notifying the table.
       */

      var BaseRowDef = /*#__PURE__*/function () {
        function BaseRowDef(
        /** @docs-private */
        template, _differs) {
          _classCallCheck(this, BaseRowDef);

          this.template = template;
          this._differs = _differs;
        }

        _createClass(BaseRowDef, [{
          key: "ngOnChanges",
          value: function ngOnChanges(changes) {
            // Create a new columns differ if one does not yet exist. Initialize it based on initial value
            // of the columns property or an empty array if none is provided.
            if (!this._columnsDiffer) {
              var columns = changes['columns'] && changes['columns'].currentValue || [];
              this._columnsDiffer = this._differs.find(columns).create();

              this._columnsDiffer.diff(columns);
            }
          }
          /**
           * Returns the difference between the current columns and the columns from the last diff, or null
           * if there is no difference.
           */

        }, {
          key: "getColumnsDiff",
          value: function getColumnsDiff() {
            return this._columnsDiffer.diff(this.columns);
          }
          /** Gets this row def's relevant cell template from the provided column def. */

        }, {
          key: "extractCellTemplate",
          value: function extractCellTemplate(column) {
            if (this instanceof CdkHeaderRowDef) {
              return column.headerCell.template;
            }

            if (this instanceof CdkFooterRowDef) {
              return column.footerCell.template;
            } else {
              return column.cell.template;
            }
          }
        }]);

        return BaseRowDef;
      }();

      BaseRowDef.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Directive"]
      }];

      BaseRowDef.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["TemplateRef"]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["IterableDiffers"]
        }];
      }; // Boilerplate for applying mixins to CdkHeaderRowDef.

      /** @docs-private */


      var CdkHeaderRowDefBase = /*#__PURE__*/function (_BaseRowDef) {
        _inherits(CdkHeaderRowDefBase, _BaseRowDef);

        var _super8 = _createSuper(CdkHeaderRowDefBase);

        function CdkHeaderRowDefBase() {
          _classCallCheck(this, CdkHeaderRowDefBase);

          return _super8.apply(this, arguments);
        }

        return CdkHeaderRowDefBase;
      }(BaseRowDef);

      var _CdkHeaderRowDefBase = mixinHasStickyInput(CdkHeaderRowDefBase);
      /**
       * Header row definition for the CDK table.
       * Captures the header row's template and other header properties such as the columns to display.
       */


      var CdkHeaderRowDef = /*#__PURE__*/function (_CdkHeaderRowDefBase2) {
        _inherits(CdkHeaderRowDef, _CdkHeaderRowDefBase2);

        var _super9 = _createSuper(CdkHeaderRowDef);

        function CdkHeaderRowDef(template, _differs, _table) {
          var _this6;

          _classCallCheck(this, CdkHeaderRowDef);

          _this6 = _super9.call(this, template, _differs);
          _this6._table = _table;
          return _this6;
        } // Prerender fails to recognize that ngOnChanges in a part of this class through inheritance.
        // Explicitly define it so that the method is called as part of the Angular lifecycle.


        _createClass(CdkHeaderRowDef, [{
          key: "ngOnChanges",
          value: function ngOnChanges(changes) {
            _get(_getPrototypeOf(CdkHeaderRowDef.prototype), "ngOnChanges", this).call(this, changes);
          }
        }]);

        return CdkHeaderRowDef;
      }(_CdkHeaderRowDefBase);

      CdkHeaderRowDef.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Directive"],
        args: [{
          selector: '[cdkHeaderRowDef]',
          inputs: ['columns: cdkHeaderRowDef', 'sticky: cdkHeaderRowDefSticky']
        }]
      }];

      CdkHeaderRowDef.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["TemplateRef"]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["IterableDiffers"]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Inject"],
            args: [CDK_TABLE]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Optional"]
          }]
        }];
      }; // Boilerplate for applying mixins to CdkFooterRowDef.

      /** @docs-private */


      var CdkFooterRowDefBase = /*#__PURE__*/function (_BaseRowDef2) {
        _inherits(CdkFooterRowDefBase, _BaseRowDef2);

        var _super10 = _createSuper(CdkFooterRowDefBase);

        function CdkFooterRowDefBase() {
          _classCallCheck(this, CdkFooterRowDefBase);

          return _super10.apply(this, arguments);
        }

        return CdkFooterRowDefBase;
      }(BaseRowDef);

      var _CdkFooterRowDefBase = mixinHasStickyInput(CdkFooterRowDefBase);
      /**
       * Footer row definition for the CDK table.
       * Captures the footer row's template and other footer properties such as the columns to display.
       */


      var CdkFooterRowDef = /*#__PURE__*/function (_CdkFooterRowDefBase2) {
        _inherits(CdkFooterRowDef, _CdkFooterRowDefBase2);

        var _super11 = _createSuper(CdkFooterRowDef);

        function CdkFooterRowDef(template, _differs, _table) {
          var _this7;

          _classCallCheck(this, CdkFooterRowDef);

          _this7 = _super11.call(this, template, _differs);
          _this7._table = _table;
          return _this7;
        } // Prerender fails to recognize that ngOnChanges in a part of this class through inheritance.
        // Explicitly define it so that the method is called as part of the Angular lifecycle.


        _createClass(CdkFooterRowDef, [{
          key: "ngOnChanges",
          value: function ngOnChanges(changes) {
            _get(_getPrototypeOf(CdkFooterRowDef.prototype), "ngOnChanges", this).call(this, changes);
          }
        }]);

        return CdkFooterRowDef;
      }(_CdkFooterRowDefBase);

      CdkFooterRowDef.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Directive"],
        args: [{
          selector: '[cdkFooterRowDef]',
          inputs: ['columns: cdkFooterRowDef', 'sticky: cdkFooterRowDefSticky']
        }]
      }];

      CdkFooterRowDef.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["TemplateRef"]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["IterableDiffers"]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Inject"],
            args: [CDK_TABLE]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Optional"]
          }]
        }];
      };
      /**
       * Data row definition for the CDK table.
       * Captures the header row's template and other row properties such as the columns to display and
       * a when predicate that describes when this row should be used.
       */


      var CdkRowDef = /*#__PURE__*/function (_BaseRowDef3) {
        _inherits(CdkRowDef, _BaseRowDef3);

        var _super12 = _createSuper(CdkRowDef);

        // TODO(andrewseguin): Add an input for providing a switch function to determine
        //   if this template should be used.
        function CdkRowDef(template, _differs, _table) {
          var _this8;

          _classCallCheck(this, CdkRowDef);

          _this8 = _super12.call(this, template, _differs);
          _this8._table = _table;
          return _this8;
        }

        return CdkRowDef;
      }(BaseRowDef);

      CdkRowDef.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Directive"],
        args: [{
          selector: '[cdkRowDef]',
          inputs: ['columns: cdkRowDefColumns', 'when: cdkRowDefWhen']
        }]
      }];

      CdkRowDef.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["TemplateRef"]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["IterableDiffers"]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Inject"],
            args: [CDK_TABLE]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Optional"]
          }]
        }];
      };
      /**
       * Outlet for rendering cells inside of a row or header row.
       * @docs-private
       */


      var CdkCellOutlet = /*#__PURE__*/function () {
        function CdkCellOutlet(_viewContainer) {
          _classCallCheck(this, CdkCellOutlet);

          this._viewContainer = _viewContainer;
          CdkCellOutlet.mostRecentCellOutlet = this;
        }

        _createClass(CdkCellOutlet, [{
          key: "ngOnDestroy",
          value: function ngOnDestroy() {
            // If this was the last outlet being rendered in the view, remove the reference
            // from the static property after it has been destroyed to avoid leaking memory.
            if (CdkCellOutlet.mostRecentCellOutlet === this) {
              CdkCellOutlet.mostRecentCellOutlet = null;
            }
          }
        }]);

        return CdkCellOutlet;
      }();
      /**
       * Static property containing the latest constructed instance of this class.
       * Used by the CDK table when each CdkHeaderRow and CdkRow component is created using
       * createEmbeddedView. After one of these components are created, this property will provide
       * a handle to provide that component's cells and context. After init, the CdkCellOutlet will
       * construct the cells with the provided context.
       */


      CdkCellOutlet.mostRecentCellOutlet = null;
      CdkCellOutlet.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Directive"],
        args: [{
          selector: '[cdkCellOutlet]'
        }]
      }];

      CdkCellOutlet.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ViewContainerRef"]
        }];
      };
      /** Header template container that contains the cell outlet. Adds the right class and role. */


      var CdkHeaderRow = function CdkHeaderRow() {
        _classCallCheck(this, CdkHeaderRow);
      };

      CdkHeaderRow.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Component"],
        args: [{
          selector: 'cdk-header-row, tr[cdk-header-row]',
          template: CDK_ROW_TEMPLATE,
          host: {
            'class': 'cdk-header-row',
            'role': 'row'
          },
          // See note on CdkTable for explanation on why this uses the default change detection strategy.
          // tslint:disable-next-line:validate-decorators
          changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ChangeDetectionStrategy"].Default,
          encapsulation: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ViewEncapsulation"].None
        }]
      }];
      /** Footer template container that contains the cell outlet. Adds the right class and role. */

      var CdkFooterRow = function CdkFooterRow() {
        _classCallCheck(this, CdkFooterRow);
      };

      CdkFooterRow.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Component"],
        args: [{
          selector: 'cdk-footer-row, tr[cdk-footer-row]',
          template: CDK_ROW_TEMPLATE,
          host: {
            'class': 'cdk-footer-row',
            'role': 'row'
          },
          // See note on CdkTable for explanation on why this uses the default change detection strategy.
          // tslint:disable-next-line:validate-decorators
          changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ChangeDetectionStrategy"].Default,
          encapsulation: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ViewEncapsulation"].None
        }]
      }];
      /** Data row template container that contains the cell outlet. Adds the right class and role. */

      var CdkRow = function CdkRow() {
        _classCallCheck(this, CdkRow);
      };

      CdkRow.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Component"],
        args: [{
          selector: 'cdk-row, tr[cdk-row]',
          template: CDK_ROW_TEMPLATE,
          host: {
            'class': 'cdk-row',
            'role': 'row'
          },
          // See note on CdkTable for explanation on why this uses the default change detection strategy.
          // tslint:disable-next-line:validate-decorators
          changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ChangeDetectionStrategy"].Default,
          encapsulation: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ViewEncapsulation"].None
        }]
      }];
      /** Row that can be used to display a message when no data is shown in the table. */

      var CdkNoDataRow = function CdkNoDataRow(templateRef) {
        _classCallCheck(this, CdkNoDataRow);

        this.templateRef = templateRef;
      };

      CdkNoDataRow.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Directive"],
        args: [{
          selector: 'ng-template[cdkNoDataRow]'
        }]
      }];

      CdkNoDataRow.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["TemplateRef"]
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
       * List of all possible directions that can be used for sticky positioning.
       * @docs-private
       */


      var STICKY_DIRECTIONS = ['top', 'bottom', 'left', 'right'];
      /**
       * Applies and removes sticky positioning styles to the `CdkTable` rows and columns cells.
       * @docs-private
       */

      var StickyStyler = /*#__PURE__*/function () {
        /**
         * @param _isNativeHtmlTable Whether the sticky logic should be based on a table
         *     that uses the native `<table>` element.
         * @param _stickCellCss The CSS class that will be applied to every row/cell that has
         *     sticky positioning applied.
         * @param direction The directionality context of the table (ltr/rtl); affects column positioning
         *     by reversing left/right positions.
         * @param _isBrowser Whether the table is currently being rendered on the server or the client.
         * @param _needsPositionStickyOnElement Whether we need to specify position: sticky on cells
         *     using inline styles. If false, it is assumed that position: sticky is included in
         *     the component stylesheet for _stickCellCss.
         */
        function StickyStyler(_isNativeHtmlTable, _stickCellCss, direction,
        /**
         * @deprecated `_coalescedStyleScheduler` parameter to become required.
         * @breaking-change 11.0.0
         */
        _coalescedStyleScheduler) {
          var _isBrowser = arguments.length > 4 && arguments[4] !== undefined ? arguments[4] : true;

          var _needsPositionStickyOnElement = arguments.length > 5 && arguments[5] !== undefined ? arguments[5] : true;

          _classCallCheck(this, StickyStyler);

          this._isNativeHtmlTable = _isNativeHtmlTable;
          this._stickCellCss = _stickCellCss;
          this.direction = direction;
          this._coalescedStyleScheduler = _coalescedStyleScheduler;
          this._isBrowser = _isBrowser;
          this._needsPositionStickyOnElement = _needsPositionStickyOnElement;
          this._cachedCellWidths = [];
        }
        /**
         * Clears the sticky positioning styles from the row and its cells by resetting the `position`
         * style, setting the zIndex to 0, and unsetting each provided sticky direction.
         * @param rows The list of rows that should be cleared from sticking in the provided directions
         * @param stickyDirections The directions that should no longer be set as sticky on the rows.
         */


        _createClass(StickyStyler, [{
          key: "clearStickyPositioning",
          value: function clearStickyPositioning(rows, stickyDirections) {
            var _this9 = this;

            var elementsToClear = [];

            var _iterator4 = _createForOfIteratorHelper(rows),
                _step4;

            try {
              for (_iterator4.s(); !(_step4 = _iterator4.n()).done;) {
                var row = _step4.value;

                // If the row isn't an element (e.g. if it's an `ng-container`),
                // it won't have inline styles or `children` so we skip it.
                if (row.nodeType !== row.ELEMENT_NODE) {
                  continue;
                }

                elementsToClear.push(row);

                for (var i = 0; i < row.children.length; i++) {
                  elementsToClear.push(row.children[i]);
                }
              } // Coalesce with sticky row/column updates (and potentially other changes like column resize).

            } catch (err) {
              _iterator4.e(err);
            } finally {
              _iterator4.f();
            }

            this._scheduleStyleChanges(function () {
              var _iterator5 = _createForOfIteratorHelper(elementsToClear),
                  _step5;

              try {
                for (_iterator5.s(); !(_step5 = _iterator5.n()).done;) {
                  var element = _step5.value;

                  _this9._removeStickyStyle(element, stickyDirections);
                }
              } catch (err) {
                _iterator5.e(err);
              } finally {
                _iterator5.f();
              }
            });
          }
          /**
           * Applies sticky left and right positions to the cells of each row according to the sticky
           * states of the rendered column definitions.
           * @param rows The rows that should have its set of cells stuck according to the sticky states.
           * @param stickyStartStates A list of boolean states where each state represents whether the cell
           *     in this index position should be stuck to the start of the row.
           * @param stickyEndStates A list of boolean states where each state represents whether the cell
           *     in this index position should be stuck to the end of the row.
           * @param recalculateCellWidths Whether the sticky styler should recalculate the width of each
           *     column cell. If `false` cached widths will be used instead.
           */

        }, {
          key: "updateStickyColumns",
          value: function updateStickyColumns(rows, stickyStartStates, stickyEndStates) {
            var _this10 = this;

            var recalculateCellWidths = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : true;

            if (!rows.length || !this._isBrowser || !(stickyStartStates.some(function (state) {
              return state;
            }) || stickyEndStates.some(function (state) {
              return state;
            }))) {
              return;
            }

            var firstRow = rows[0];
            var numCells = firstRow.children.length;

            var cellWidths = this._getCellWidths(firstRow, recalculateCellWidths);

            var startPositions = this._getStickyStartColumnPositions(cellWidths, stickyStartStates);

            var endPositions = this._getStickyEndColumnPositions(cellWidths, stickyEndStates); // Coalesce with sticky row updates (and potentially other changes like column resize).


            this._scheduleStyleChanges(function () {
              var isRtl = _this10.direction === 'rtl';
              var start = isRtl ? 'right' : 'left';
              var end = isRtl ? 'left' : 'right';

              var _iterator6 = _createForOfIteratorHelper(rows),
                  _step6;

              try {
                for (_iterator6.s(); !(_step6 = _iterator6.n()).done;) {
                  var row = _step6.value;

                  for (var i = 0; i < numCells; i++) {
                    var cell = row.children[i];

                    if (stickyStartStates[i]) {
                      _this10._addStickyStyle(cell, start, startPositions[i]);
                    }

                    if (stickyEndStates[i]) {
                      _this10._addStickyStyle(cell, end, endPositions[i]);
                    }
                  }
                }
              } catch (err) {
                _iterator6.e(err);
              } finally {
                _iterator6.f();
              }
            });
          }
          /**
           * Applies sticky positioning to the row's cells if using the native table layout, and to the
           * row itself otherwise.
           * @param rowsToStick The list of rows that should be stuck according to their corresponding
           *     sticky state and to the provided top or bottom position.
           * @param stickyStates A list of boolean states where each state represents whether the row
           *     should be stuck in the particular top or bottom position.
           * @param position The position direction in which the row should be stuck if that row should be
           *     sticky.
           *
           */

        }, {
          key: "stickRows",
          value: function stickRows(rowsToStick, stickyStates, position) {
            var _this11 = this;

            // Since we can't measure the rows on the server, we can't stick the rows properly.
            if (!this._isBrowser) {
              return;
            } // If positioning the rows to the bottom, reverse their order when evaluating the sticky
            // position such that the last row stuck will be "bottom: 0px" and so on. Note that the
            // sticky states need to be reversed as well.


            var rows = position === 'bottom' ? rowsToStick.slice().reverse() : rowsToStick;
            var states = position === 'bottom' ? stickyStates.slice().reverse() : stickyStates; // Measure row heights all at once before adding sticky styles to reduce layout thrashing.

            var stickyHeights = [];
            var elementsToStick = [];

            for (var rowIndex = 0, stickyHeight = 0; rowIndex < rows.length; rowIndex++) {
              stickyHeights[rowIndex] = stickyHeight;

              if (!states[rowIndex]) {
                continue;
              }

              var row = rows[rowIndex];
              elementsToStick[rowIndex] = this._isNativeHtmlTable ? Array.from(row.children) : [row];

              if (rowIndex !== rows.length - 1) {
                stickyHeight += row.getBoundingClientRect().height;
              }
            } // Coalesce with other sticky row updates (top/bottom), sticky columns updates
            // (and potentially other changes like column resize).


            this._scheduleStyleChanges(function () {
              for (var _rowIndex = 0; _rowIndex < rows.length; _rowIndex++) {
                if (!states[_rowIndex]) {
                  continue;
                }

                var height = stickyHeights[_rowIndex];

                var _iterator7 = _createForOfIteratorHelper(elementsToStick[_rowIndex]),
                    _step7;

                try {
                  for (_iterator7.s(); !(_step7 = _iterator7.n()).done;) {
                    var element = _step7.value;

                    _this11._addStickyStyle(element, position, height);
                  }
                } catch (err) {
                  _iterator7.e(err);
                } finally {
                  _iterator7.f();
                }
              }
            });
          }
          /**
           * When using the native table in Safari, sticky footer cells do not stick. The only way to stick
           * footer rows is to apply sticky styling to the tfoot container. This should only be done if
           * all footer rows are sticky. If not all footer rows are sticky, remove sticky positioning from
           * the tfoot element.
           */

        }, {
          key: "updateStickyFooterContainer",
          value: function updateStickyFooterContainer(tableElement, stickyStates) {
            var _this12 = this;

            if (!this._isNativeHtmlTable) {
              return;
            }

            var tfoot = tableElement.querySelector('tfoot'); // Coalesce with other sticky updates (and potentially other changes like column resize).

            this._scheduleStyleChanges(function () {
              if (stickyStates.some(function (state) {
                return !state;
              })) {
                _this12._removeStickyStyle(tfoot, ['bottom']);
              } else {
                _this12._addStickyStyle(tfoot, 'bottom', 0);
              }
            });
          }
          /**
           * Removes the sticky style on the element by removing the sticky cell CSS class, re-evaluating
           * the zIndex, removing each of the provided sticky directions, and removing the
           * sticky position if there are no more directions.
           */

        }, {
          key: "_removeStickyStyle",
          value: function _removeStickyStyle(element, stickyDirections) {
            var _iterator8 = _createForOfIteratorHelper(stickyDirections),
                _step8;

            try {
              for (_iterator8.s(); !(_step8 = _iterator8.n()).done;) {
                var dir = _step8.value;
                element.style[dir] = '';
              } // If the element no longer has any more sticky directions, remove sticky positioning and
              // the sticky CSS class.
              // Short-circuit checking element.style[dir] for stickyDirections as they
              // were already removed above.

            } catch (err) {
              _iterator8.e(err);
            } finally {
              _iterator8.f();
            }

            var hasDirection = STICKY_DIRECTIONS.some(function (dir) {
              return stickyDirections.indexOf(dir) === -1 && element.style[dir];
            });

            if (hasDirection) {
              element.style.zIndex = this._getCalculatedZIndex(element);
            } else {
              // When not hasDirection, _getCalculatedZIndex will always return ''.
              element.style.zIndex = '';

              if (this._needsPositionStickyOnElement) {
                element.style.position = '';
              }

              element.classList.remove(this._stickCellCss);
            }
          }
          /**
           * Adds the sticky styling to the element by adding the sticky style class, changing position
           * to be sticky (and -webkit-sticky), setting the appropriate zIndex, and adding a sticky
           * direction and value.
           */

        }, {
          key: "_addStickyStyle",
          value: function _addStickyStyle(element, dir, dirValue) {
            element.classList.add(this._stickCellCss);
            element.style[dir] = "".concat(dirValue, "px");
            element.style.zIndex = this._getCalculatedZIndex(element);

            if (this._needsPositionStickyOnElement) {
              element.style.cssText += 'position: -webkit-sticky; position: sticky; ';
            }
          }
          /**
           * Calculate what the z-index should be for the element, depending on what directions (top,
           * bottom, left, right) have been set. It should be true that elements with a top direction
           * should have the highest index since these are elements like a table header. If any of those
           * elements are also sticky in another direction, then they should appear above other elements
           * that are only sticky top (e.g. a sticky column on a sticky header). Bottom-sticky elements
           * (e.g. footer rows) should then be next in the ordering such that they are below the header
           * but above any non-sticky elements. Finally, left/right sticky elements (e.g. sticky columns)
           * should minimally increment so that they are above non-sticky elements but below top and bottom
           * elements.
           */

        }, {
          key: "_getCalculatedZIndex",
          value: function _getCalculatedZIndex(element) {
            var zIndexIncrements = {
              top: 100,
              bottom: 10,
              left: 1,
              right: 1
            };
            var zIndex = 0; // Use `Iterable` instead of `Array` because TypeScript, as of 3.6.3,
            // loses the array generic type in the `for of`. But we *also* have to use `Array` because
            // typescript won't iterate over an `Iterable` unless you compile with `--downlevelIteration`

            var _iterator9 = _createForOfIteratorHelper(STICKY_DIRECTIONS),
                _step9;

            try {
              for (_iterator9.s(); !(_step9 = _iterator9.n()).done;) {
                var dir = _step9.value;

                if (element.style[dir]) {
                  zIndex += zIndexIncrements[dir];
                }
              }
            } catch (err) {
              _iterator9.e(err);
            } finally {
              _iterator9.f();
            }

            return zIndex ? "".concat(zIndex) : '';
          }
          /** Gets the widths for each cell in the provided row. */

        }, {
          key: "_getCellWidths",
          value: function _getCellWidths(row) {
            var recalculateCellWidths = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : true;

            if (!recalculateCellWidths && this._cachedCellWidths.length) {
              return this._cachedCellWidths;
            }

            var cellWidths = [];
            var firstRowCells = row.children;

            for (var i = 0; i < firstRowCells.length; i++) {
              var cell = firstRowCells[i];
              cellWidths.push(cell.getBoundingClientRect().width);
            }

            this._cachedCellWidths = cellWidths;
            return cellWidths;
          }
          /**
           * Determines the left and right positions of each sticky column cell, which will be the
           * accumulation of all sticky column cell widths to the left and right, respectively.
           * Non-sticky cells do not need to have a value set since their positions will not be applied.
           */

        }, {
          key: "_getStickyStartColumnPositions",
          value: function _getStickyStartColumnPositions(widths, stickyStates) {
            var positions = [];
            var nextPosition = 0;

            for (var i = 0; i < widths.length; i++) {
              if (stickyStates[i]) {
                positions[i] = nextPosition;
                nextPosition += widths[i];
              }
            }

            return positions;
          }
          /**
           * Determines the left and right positions of each sticky column cell, which will be the
           * accumulation of all sticky column cell widths to the left and right, respectively.
           * Non-sticky cells do not need to have a value set since their positions will not be applied.
           */

        }, {
          key: "_getStickyEndColumnPositions",
          value: function _getStickyEndColumnPositions(widths, stickyStates) {
            var positions = [];
            var nextPosition = 0;

            for (var i = widths.length; i > 0; i--) {
              if (stickyStates[i]) {
                positions[i] = nextPosition;
                nextPosition += widths[i];
              }
            }

            return positions;
          }
          /**
           * Schedules styles to be applied when the style scheduler deems appropriate.
           * @breaking-change 11.0.0 This method can be removed in favor of calling
           * `CoalescedStyleScheduler.schedule` directly once the scheduler is a required parameter.
           */

        }, {
          key: "_scheduleStyleChanges",
          value: function _scheduleStyleChanges(changes) {
            if (this._coalescedStyleScheduler) {
              this._coalescedStyleScheduler.schedule(changes);
            } else {
              changes();
            }
          }
        }]);

        return StickyStyler;
      }();
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * Returns an error to be thrown when attempting to find an unexisting column.
       * @param id Id whose lookup failed.
       * @docs-private
       */


      function getTableUnknownColumnError(id) {
        return Error("Could not find column with id \"".concat(id, "\"."));
      }
      /**
       * Returns an error to be thrown when two column definitions have the same name.
       * @docs-private
       */


      function getTableDuplicateColumnNameError(name) {
        return Error("Duplicate column definition name provided: \"".concat(name, "\"."));
      }
      /**
       * Returns an error to be thrown when there are multiple rows that are missing a when function.
       * @docs-private
       */


      function getTableMultipleDefaultRowDefsError() {
        return Error("There can only be one default row without a when predicate function.");
      }
      /**
       * Returns an error to be thrown when there are no matching row defs for a particular set of data.
       * @docs-private
       */


      function getTableMissingMatchingRowDefError(data) {
        return Error("Could not find a matching row definition for the" + "provided row data: ".concat(JSON.stringify(data)));
      }
      /**
       * Returns an error to be thrown when there is no row definitions present in the content.
       * @docs-private
       */


      function getTableMissingRowDefsError() {
        return Error('Missing definitions for header, footer, and row; ' + 'cannot determine which columns should be rendered.');
      }
      /**
       * Returns an error to be thrown when the data source does not match the compatible types.
       * @docs-private
       */


      function getTableUnknownDataSourceError() {
        return Error("Provided data source did not match an array, Observable, or DataSource");
      }
      /**
       * Returns an error to be thrown when the text column cannot find a parent table to inject.
       * @docs-private
       */


      function getTableTextColumnMissingParentTableError() {
        return Error("Text column could not find a parent table for registration.");
      }
      /**
       * Returns an error to be thrown when a table text column doesn't have a name.
       * @docs-private
       */


      function getTableTextColumnMissingNameError() {
        return Error("Table text column must have a name.");
      }
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * Provides a handle for the table to grab the view container's ng-container to insert data rows.
       * @docs-private
       */


      var DataRowOutlet = function DataRowOutlet(viewContainer, elementRef) {
        _classCallCheck(this, DataRowOutlet);

        this.viewContainer = viewContainer;
        this.elementRef = elementRef;
      };

      DataRowOutlet.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Directive"],
        args: [{
          selector: '[rowOutlet]'
        }]
      }];

      DataRowOutlet.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ViewContainerRef"]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ElementRef"]
        }];
      };
      /**
       * Provides a handle for the table to grab the view container's ng-container to insert the header.
       * @docs-private
       */


      var HeaderRowOutlet = function HeaderRowOutlet(viewContainer, elementRef) {
        _classCallCheck(this, HeaderRowOutlet);

        this.viewContainer = viewContainer;
        this.elementRef = elementRef;
      };

      HeaderRowOutlet.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Directive"],
        args: [{
          selector: '[headerRowOutlet]'
        }]
      }];

      HeaderRowOutlet.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ViewContainerRef"]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ElementRef"]
        }];
      };
      /**
       * Provides a handle for the table to grab the view container's ng-container to insert the footer.
       * @docs-private
       */


      var FooterRowOutlet = function FooterRowOutlet(viewContainer, elementRef) {
        _classCallCheck(this, FooterRowOutlet);

        this.viewContainer = viewContainer;
        this.elementRef = elementRef;
      };

      FooterRowOutlet.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Directive"],
        args: [{
          selector: '[footerRowOutlet]'
        }]
      }];

      FooterRowOutlet.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ViewContainerRef"]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ElementRef"]
        }];
      };
      /**
       * Provides a handle for the table to grab the view
       * container's ng-container to insert the no data row.
       * @docs-private
       */


      var NoDataRowOutlet = function NoDataRowOutlet(viewContainer, elementRef) {
        _classCallCheck(this, NoDataRowOutlet);

        this.viewContainer = viewContainer;
        this.elementRef = elementRef;
      };

      NoDataRowOutlet.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Directive"],
        args: [{
          selector: '[noDataRowOutlet]'
        }]
      }];

      NoDataRowOutlet.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ViewContainerRef"]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ElementRef"]
        }];
      };
      /**
       * The table template that can be used by the mat-table. Should not be used outside of the
       * material library.
       * @docs-private
       */


      var CDK_TABLE_TEMPLATE = // Note that according to MDN, the `caption` element has to be projected as the **first**
      // element in the table. See https://developer.mozilla.org/en-US/docs/Web/HTML/Element/caption
      "\n  <ng-content select=\"caption\"></ng-content>\n  <ng-content select=\"colgroup, col\"></ng-content>\n  <ng-container headerRowOutlet></ng-container>\n  <ng-container rowOutlet></ng-container>\n  <ng-container noDataRowOutlet></ng-container>\n  <ng-container footerRowOutlet></ng-container>\n";
      /**
       * Class used to conveniently type the embedded view ref for rows with a context.
       * @docs-private
       */

      var RowViewRef = /*#__PURE__*/function (_angular_core__WEBPAC) {
        _inherits(RowViewRef, _angular_core__WEBPAC);

        var _super13 = _createSuper(RowViewRef);

        function RowViewRef() {
          _classCallCheck(this, RowViewRef);

          return _super13.apply(this, arguments);
        }

        return RowViewRef;
      }(_angular_core__WEBPACK_IMPORTED_MODULE_6__["EmbeddedViewRef"]);
      /**
       * A data table that can render a header row, data rows, and a footer row.
       * Uses the dataSource input to determine the data to be rendered. The data can be provided either
       * as a data array, an Observable stream that emits the data array to render, or a DataSource with a
       * connect function that will return an Observable stream that emits the data array to render.
       */


      var CdkTable = /*#__PURE__*/function () {
        function CdkTable(_differs, _changeDetectorRef, _elementRef, role, _dir, _document, _platform,
        /**
         * @deprecated `_coalescedStyleScheduler`, `_viewRepeater` and `_viewportRuler`
         *    parameters to become required.
         * @breaking-change 11.0.0
         */
        _viewRepeater, _coalescedStyleScheduler, // Optional for backwards compatibility. The viewport ruler is provided in root. Therefore,
        // this property will never be null.
        // tslint:disable-next-line: lightweight-tokens
        _viewportRuler) {
          _classCallCheck(this, CdkTable);

          this._differs = _differs;
          this._changeDetectorRef = _changeDetectorRef;
          this._elementRef = _elementRef;
          this._dir = _dir;
          this._platform = _platform;
          this._viewRepeater = _viewRepeater;
          this._coalescedStyleScheduler = _coalescedStyleScheduler;
          this._viewportRuler = _viewportRuler;
          /** Subject that emits when the component has been destroyed. */

          this._onDestroy = new rxjs__WEBPACK_IMPORTED_MODULE_7__["Subject"]();
          /**
           * Map of all the user's defined columns (header, data, and footer cell template) identified by
           * name. Collection populated by the column definitions gathered by `ContentChildren` as well as
           * any custom column definitions added to `_customColumnDefs`.
           */

          this._columnDefsByName = new Map();
          /**
           * Column definitions that were defined outside of the direct content children of the table.
           * These will be defined when, e.g., creating a wrapper around the cdkTable that has
           * column definitions as *its* content child.
           */

          this._customColumnDefs = new Set();
          /**
           * Data row definitions that were defined outside of the direct content children of the table.
           * These will be defined when, e.g., creating a wrapper around the cdkTable that has
           * built-in data rows as *its* content child.
           */

          this._customRowDefs = new Set();
          /**
           * Header row definitions that were defined outside of the direct content children of the table.
           * These will be defined when, e.g., creating a wrapper around the cdkTable that has
           * built-in header rows as *its* content child.
           */

          this._customHeaderRowDefs = new Set();
          /**
           * Footer row definitions that were defined outside of the direct content children of the table.
           * These will be defined when, e.g., creating a wrapper around the cdkTable that has a
           * built-in footer row as *its* content child.
           */

          this._customFooterRowDefs = new Set();
          /**
           * Whether the header row definition has been changed. Triggers an update to the header row after
           * content is checked. Initialized as true so that the table renders the initial set of rows.
           */

          this._headerRowDefChanged = true;
          /**
           * Whether the footer row definition has been changed. Triggers an update to the footer row after
           * content is checked. Initialized as true so that the table renders the initial set of rows.
           */

          this._footerRowDefChanged = true;
          /**
           * Whether the sticky column styles need to be updated. Set to `true` when the visible columns
           * change.
           */

          this._stickyColumnStylesNeedReset = true;
          /**
           * Whether the sticky styler should recalculate cell widths when applying sticky styles. If
           * `false`, cached values will be used instead. This is only applicable to tables with
           * {@link fixedLayout} enabled. For other tables, cell widths will always be recalculated.
           */

          this._forceRecalculateCellWidths = true;
          /**
           * Cache of the latest rendered `RenderRow` objects as a map for easy retrieval when constructing
           * a new list of `RenderRow` objects for rendering rows. Since the new list is constructed with
           * the cached `RenderRow` objects when possible, the row identity is preserved when the data
           * and row template matches, which allows the `IterableDiffer` to check rows by reference
           * and understand which rows are added/moved/removed.
           *
           * Implemented as a map of maps where the first key is the `data: T` object and the second is the
           * `CdkRowDef<T>` object. With the two keys, the cache points to a `RenderRow<T>` object that
           * contains an array of created pairs. The array is necessary to handle cases where the data
           * array contains multiple duplicate data objects and each instantiated `RenderRow` must be
           * stored.
           */

          this._cachedRenderRowsMap = new Map();
          /**
           * CSS class added to any row or cell that has sticky positioning applied. May be overriden by
           * table subclasses.
           */

          this.stickyCssClass = 'cdk-table-sticky';
          /**
           * Whether to manually add positon: sticky to all sticky cell elements. Not needed if
           * the position is set in a selector associated with the value of stickyCssClass. May be
           * overridden by table subclasses
           */

          this.needsPositionStickyOnElement = true;
          /** Whether the no data row is currently showing anything. */

          this._isShowingNoDataRow = false;
          this._multiTemplateDataRows = false;
          this._fixedLayout = false; // TODO(andrewseguin): Remove max value as the end index
          //   and instead calculate the view on init and scroll.

          /**
           * Stream containing the latest information on what rows are being displayed on screen.
           * Can be used by the data source to as a heuristic of what data should be provided.
           *
           * @docs-private
           */

          this.viewChange = new rxjs__WEBPACK_IMPORTED_MODULE_7__["BehaviorSubject"]({
            start: 0,
            end: Number.MAX_VALUE
          });

          if (!role) {
            this._elementRef.nativeElement.setAttribute('role', 'grid');
          }

          this._document = _document;
          this._isNativeHtmlTable = this._elementRef.nativeElement.nodeName === 'TABLE';
        }
        /**
         * Tracking function that will be used to check the differences in data changes. Used similarly
         * to `ngFor` `trackBy` function. Optimize row operations by identifying a row based on its data
         * relative to the function to know if a row should be added/removed/moved.
         * Accepts a function that takes two parameters, `index` and `item`.
         */


        _createClass(CdkTable, [{
          key: "ngOnInit",
          value: function ngOnInit() {
            var _this13 = this;

            this._setupStickyStyler();

            if (this._isNativeHtmlTable) {
              this._applyNativeTableSections();
            } // Set up the trackBy function so that it uses the `RenderRow` as its identity by default. If
            // the user has provided a custom trackBy, return the result of that function as evaluated
            // with the values of the `RenderRow`'s data and index.


            this._dataDiffer = this._differs.find([]).create(function (_i, dataRow) {
              return _this13.trackBy ? _this13.trackBy(dataRow.dataIndex, dataRow.data) : dataRow;
            }); // Table cell dimensions may change after resizing the window. Signal the sticky styler to
            // refresh its cache of cell widths the next time sticky styles are updated.
            // @breaking-change 11.0.0 Remove null check for _viewportRuler once it's a required parameter.

            if (this._viewportRuler) {
              this._viewportRuler.change().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_8__["takeUntil"])(this._onDestroy)).subscribe(function () {
                _this13._forceRecalculateCellWidths = true;
              });
            }
          }
        }, {
          key: "ngAfterContentChecked",
          value: function ngAfterContentChecked() {
            // Cache the row and column definitions gathered by ContentChildren and programmatic injection.
            this._cacheRowDefs();

            this._cacheColumnDefs(); // Make sure that the user has at least added header, footer, or data row def.


            if (!this._headerRowDefs.length && !this._footerRowDefs.length && !this._rowDefs.length && (typeof ngDevMode === 'undefined' || ngDevMode)) {
              throw getTableMissingRowDefsError();
            } // Render updates if the list of columns have been changed for the header, row, or footer defs.


            var columnsChanged = this._renderUpdatedColumns();

            var rowDefsChanged = columnsChanged || this._headerRowDefChanged || this._footerRowDefChanged; // Ensure sticky column styles are reset if set to `true` elsewhere.

            this._stickyColumnStylesNeedReset = this._stickyColumnStylesNeedReset || rowDefsChanged;
            this._forceRecalculateCellWidths = rowDefsChanged; // If the header row definition has been changed, trigger a render to the header row.

            if (this._headerRowDefChanged) {
              this._forceRenderHeaderRows();

              this._headerRowDefChanged = false;
            } // If the footer row definition has been changed, trigger a render to the footer row.


            if (this._footerRowDefChanged) {
              this._forceRenderFooterRows();

              this._footerRowDefChanged = false;
            } // If there is a data source and row definitions, connect to the data source unless a
            // connection has already been made.


            if (this.dataSource && this._rowDefs.length > 0 && !this._renderChangeSubscription) {
              this._observeRenderChanges();
            } else if (this._stickyColumnStylesNeedReset) {
              // In the above case, _observeRenderChanges will result in updateStickyColumnStyles being
              // called when it row data arrives. Otherwise, we need to call it proactively.
              this.updateStickyColumnStyles();
            }

            this._checkStickyStates();
          }
        }, {
          key: "ngOnDestroy",
          value: function ngOnDestroy() {
            this._rowOutlet.viewContainer.clear();

            this._noDataRowOutlet.viewContainer.clear();

            this._headerRowOutlet.viewContainer.clear();

            this._footerRowOutlet.viewContainer.clear();

            this._cachedRenderRowsMap.clear();

            this._onDestroy.next();

            this._onDestroy.complete();

            if (Object(_angular_cdk_collections__WEBPACK_IMPORTED_MODULE_2__["isDataSource"])(this.dataSource)) {
              this.dataSource.disconnect(this);
            }
          }
          /**
           * Renders rows based on the table's latest set of data, which was either provided directly as an
           * input or retrieved through an Observable stream (directly or from a DataSource).
           * Checks for differences in the data since the last diff to perform only the necessary
           * changes (add/remove/move rows).
           *
           * If the table's data source is a DataSource or Observable, this will be invoked automatically
           * each time the provided Observable stream emits a new data array. Otherwise if your data is
           * an array, this function will need to be called to render any changes.
           */

        }, {
          key: "renderRows",
          value: function renderRows() {
            var _this14 = this;

            this._renderRows = this._getAllRenderRows();

            var changes = this._dataDiffer.diff(this._renderRows);

            if (!changes) {
              this._updateNoDataRow();

              return;
            }

            var viewContainer = this._rowOutlet.viewContainer; // @breaking-change 11.0.0 Remove null check for `_viewRepeater` and the
            // `else` clause once `_viewRepeater` is turned into a required parameter.

            if (this._viewRepeater) {
              this._viewRepeater.applyChanges(changes, viewContainer, function (record, _adjustedPreviousIndex, currentIndex) {
                return _this14._getEmbeddedViewArgs(record.item, currentIndex);
              }, function (record) {
                return record.item.data;
              }, function (change) {
                if (change.operation === 1
                /* INSERTED */
                && change.context) {
                  _this14._renderCellTemplateForItem(change.record.item.rowDef, change.context);
                }
              });
            } else {
              changes.forEachOperation(function (record, prevIndex, currentIndex) {
                if (record.previousIndex == null) {
                  var renderRow = record.item;
                  var rowDef = renderRow.rowDef;
                  var context = {
                    $implicit: renderRow.data
                  };

                  _this14._renderRow(_this14._rowOutlet, rowDef, currentIndex, context);
                } else if (currentIndex == null) {
                  viewContainer.remove(prevIndex);
                } else {
                  var view = viewContainer.get(prevIndex);
                  viewContainer.move(view, currentIndex);
                }
              });
            } // Update the meta context of a row's context data (index, count, first, last, ...)


            this._updateRowIndexContext(); // Update rows that did not get added/removed/moved but may have had their identity changed,
            // e.g. if trackBy matched data on some property but the actual data reference changed.


            changes.forEachIdentityChange(function (record) {
              var rowView = viewContainer.get(record.currentIndex);
              rowView.context.$implicit = record.item.data;
            });

            this._updateNoDataRow();

            this.updateStickyColumnStyles();
          }
          /** Adds a column definition that was not included as part of the content children. */

        }, {
          key: "addColumnDef",
          value: function addColumnDef(columnDef) {
            this._customColumnDefs.add(columnDef);
          }
          /** Removes a column definition that was not included as part of the content children. */

        }, {
          key: "removeColumnDef",
          value: function removeColumnDef(columnDef) {
            this._customColumnDefs["delete"](columnDef);
          }
          /** Adds a row definition that was not included as part of the content children. */

        }, {
          key: "addRowDef",
          value: function addRowDef(rowDef) {
            this._customRowDefs.add(rowDef);
          }
          /** Removes a row definition that was not included as part of the content children. */

        }, {
          key: "removeRowDef",
          value: function removeRowDef(rowDef) {
            this._customRowDefs["delete"](rowDef);
          }
          /** Adds a header row definition that was not included as part of the content children. */

        }, {
          key: "addHeaderRowDef",
          value: function addHeaderRowDef(headerRowDef) {
            this._customHeaderRowDefs.add(headerRowDef);

            this._headerRowDefChanged = true;
          }
          /** Removes a header row definition that was not included as part of the content children. */

        }, {
          key: "removeHeaderRowDef",
          value: function removeHeaderRowDef(headerRowDef) {
            this._customHeaderRowDefs["delete"](headerRowDef);

            this._headerRowDefChanged = true;
          }
          /** Adds a footer row definition that was not included as part of the content children. */

        }, {
          key: "addFooterRowDef",
          value: function addFooterRowDef(footerRowDef) {
            this._customFooterRowDefs.add(footerRowDef);

            this._footerRowDefChanged = true;
          }
          /** Removes a footer row definition that was not included as part of the content children. */

        }, {
          key: "removeFooterRowDef",
          value: function removeFooterRowDef(footerRowDef) {
            this._customFooterRowDefs["delete"](footerRowDef);

            this._footerRowDefChanged = true;
          }
          /** Sets a no data row definition that was not included as a part of the content children. */

        }, {
          key: "setNoDataRow",
          value: function setNoDataRow(noDataRow) {
            this._customNoDataRow = noDataRow;
          }
          /**
           * Updates the header sticky styles. First resets all applied styles with respect to the cells
           * sticking to the top. Then, evaluating which cells need to be stuck to the top. This is
           * automatically called when the header row changes its displayed set of columns, or if its
           * sticky input changes. May be called manually for cases where the cell content changes outside
           * of these events.
           */

        }, {
          key: "updateStickyHeaderRowStyles",
          value: function updateStickyHeaderRowStyles() {
            var headerRows = this._getRenderedRows(this._headerRowOutlet);

            var tableElement = this._elementRef.nativeElement; // Hide the thead element if there are no header rows. This is necessary to satisfy
            // overzealous a11y checkers that fail because the `rowgroup` element does not contain
            // required child `row`.

            var thead = tableElement.querySelector('thead');

            if (thead) {
              thead.style.display = headerRows.length ? '' : 'none';
            }

            var stickyStates = this._headerRowDefs.map(function (def) {
              return def.sticky;
            });

            this._stickyStyler.clearStickyPositioning(headerRows, ['top']);

            this._stickyStyler.stickRows(headerRows, stickyStates, 'top'); // Reset the dirty state of the sticky input change since it has been used.


            this._headerRowDefs.forEach(function (def) {
              return def.resetStickyChanged();
            });
          }
          /**
           * Updates the footer sticky styles. First resets all applied styles with respect to the cells
           * sticking to the bottom. Then, evaluating which cells need to be stuck to the bottom. This is
           * automatically called when the footer row changes its displayed set of columns, or if its
           * sticky input changes. May be called manually for cases where the cell content changes outside
           * of these events.
           */

        }, {
          key: "updateStickyFooterRowStyles",
          value: function updateStickyFooterRowStyles() {
            var footerRows = this._getRenderedRows(this._footerRowOutlet);

            var tableElement = this._elementRef.nativeElement; // Hide the tfoot element if there are no footer rows. This is necessary to satisfy
            // overzealous a11y checkers that fail because the `rowgroup` element does not contain
            // required child `row`.

            var tfoot = tableElement.querySelector('tfoot');

            if (tfoot) {
              tfoot.style.display = footerRows.length ? '' : 'none';
            }

            var stickyStates = this._footerRowDefs.map(function (def) {
              return def.sticky;
            });

            this._stickyStyler.clearStickyPositioning(footerRows, ['bottom']);

            this._stickyStyler.stickRows(footerRows, stickyStates, 'bottom');

            this._stickyStyler.updateStickyFooterContainer(this._elementRef.nativeElement, stickyStates); // Reset the dirty state of the sticky input change since it has been used.


            this._footerRowDefs.forEach(function (def) {
              return def.resetStickyChanged();
            });
          }
          /**
           * Updates the column sticky styles. First resets all applied styles with respect to the cells
           * sticking to the left and right. Then sticky styles are added for the left and right according
           * to the column definitions for each cell in each row. This is automatically called when
           * the data source provides a new set of data or when a column definition changes its sticky
           * input. May be called manually for cases where the cell content changes outside of these events.
           */

        }, {
          key: "updateStickyColumnStyles",
          value: function updateStickyColumnStyles() {
            var _this15 = this;

            var headerRows = this._getRenderedRows(this._headerRowOutlet);

            var dataRows = this._getRenderedRows(this._rowOutlet);

            var footerRows = this._getRenderedRows(this._footerRowOutlet); // For tables not using a fixed layout, the column widths may change when new rows are rendered.
            // In a table using a fixed layout, row content won't affect column width, so sticky styles
            // don't need to be cleared unless either the sticky column config changes or one of the row
            // defs change.


            if (this._isNativeHtmlTable && !this._fixedLayout || this._stickyColumnStylesNeedReset) {
              // Clear the left and right positioning from all columns in the table across all rows since
              // sticky columns span across all table sections (header, data, footer)
              this._stickyStyler.clearStickyPositioning([].concat(_toConsumableArray(headerRows), _toConsumableArray(dataRows), _toConsumableArray(footerRows)), ['left', 'right']);

              this._stickyColumnStylesNeedReset = false;
            } // Update the sticky styles for each header row depending on the def's sticky state


            headerRows.forEach(function (headerRow, i) {
              _this15._addStickyColumnStyles([headerRow], _this15._headerRowDefs[i]);
            }); // Update the sticky styles for each data row depending on its def's sticky state

            this._rowDefs.forEach(function (rowDef) {
              // Collect all the rows rendered with this row definition.
              var rows = [];

              for (var i = 0; i < dataRows.length; i++) {
                if (_this15._renderRows[i].rowDef === rowDef) {
                  rows.push(dataRows[i]);
                }
              }

              _this15._addStickyColumnStyles(rows, rowDef);
            }); // Update the sticky styles for each footer row depending on the def's sticky state


            footerRows.forEach(function (footerRow, i) {
              _this15._addStickyColumnStyles([footerRow], _this15._footerRowDefs[i]);
            }); // Reset the dirty state of the sticky input change since it has been used.

            Array.from(this._columnDefsByName.values()).forEach(function (def) {
              return def.resetStickyChanged();
            });
          }
          /**
           * Get the list of RenderRow objects to render according to the current list of data and defined
           * row definitions. If the previous list already contained a particular pair, it should be reused
           * so that the differ equates their references.
           */

        }, {
          key: "_getAllRenderRows",
          value: function _getAllRenderRows() {
            var renderRows = []; // Store the cache and create a new one. Any re-used RenderRow objects will be moved into the
            // new cache while unused ones can be picked up by garbage collection.

            var prevCachedRenderRows = this._cachedRenderRowsMap;
            this._cachedRenderRowsMap = new Map(); // For each data object, get the list of rows that should be rendered, represented by the
            // respective `RenderRow` object which is the pair of `data` and `CdkRowDef`.

            for (var i = 0; i < this._data.length; i++) {
              var data = this._data[i];

              var renderRowsForData = this._getRenderRowsForData(data, i, prevCachedRenderRows.get(data));

              if (!this._cachedRenderRowsMap.has(data)) {
                this._cachedRenderRowsMap.set(data, new WeakMap());
              }

              for (var j = 0; j < renderRowsForData.length; j++) {
                var renderRow = renderRowsForData[j];

                var cache = this._cachedRenderRowsMap.get(renderRow.data);

                if (cache.has(renderRow.rowDef)) {
                  cache.get(renderRow.rowDef).push(renderRow);
                } else {
                  cache.set(renderRow.rowDef, [renderRow]);
                }

                renderRows.push(renderRow);
              }
            }

            return renderRows;
          }
          /**
           * Gets a list of `RenderRow<T>` for the provided data object and any `CdkRowDef` objects that
           * should be rendered for this data. Reuses the cached RenderRow objects if they match the same
           * `(T, CdkRowDef)` pair.
           */

        }, {
          key: "_getRenderRowsForData",
          value: function _getRenderRowsForData(data, dataIndex, cache) {
            var rowDefs = this._getRowDefs(data, dataIndex);

            return rowDefs.map(function (rowDef) {
              var cachedRenderRows = cache && cache.has(rowDef) ? cache.get(rowDef) : [];

              if (cachedRenderRows.length) {
                var dataRow = cachedRenderRows.shift();
                dataRow.dataIndex = dataIndex;
                return dataRow;
              } else {
                return {
                  data: data,
                  rowDef: rowDef,
                  dataIndex: dataIndex
                };
              }
            });
          }
          /** Update the map containing the content's column definitions. */

        }, {
          key: "_cacheColumnDefs",
          value: function _cacheColumnDefs() {
            var _this16 = this;

            this._columnDefsByName.clear();

            var columnDefs = mergeArrayAndSet(this._getOwnDefs(this._contentColumnDefs), this._customColumnDefs);
            columnDefs.forEach(function (columnDef) {
              if (_this16._columnDefsByName.has(columnDef.name) && (typeof ngDevMode === 'undefined' || ngDevMode)) {
                throw getTableDuplicateColumnNameError(columnDef.name);
              }

              _this16._columnDefsByName.set(columnDef.name, columnDef);
            });
          }
          /** Update the list of all available row definitions that can be used. */

        }, {
          key: "_cacheRowDefs",
          value: function _cacheRowDefs() {
            this._headerRowDefs = mergeArrayAndSet(this._getOwnDefs(this._contentHeaderRowDefs), this._customHeaderRowDefs);
            this._footerRowDefs = mergeArrayAndSet(this._getOwnDefs(this._contentFooterRowDefs), this._customFooterRowDefs);
            this._rowDefs = mergeArrayAndSet(this._getOwnDefs(this._contentRowDefs), this._customRowDefs); // After all row definitions are determined, find the row definition to be considered default.

            var defaultRowDefs = this._rowDefs.filter(function (def) {
              return !def.when;
            });

            if (!this.multiTemplateDataRows && defaultRowDefs.length > 1 && (typeof ngDevMode === 'undefined' || ngDevMode)) {
              throw getTableMultipleDefaultRowDefsError();
            }

            this._defaultRowDef = defaultRowDefs[0];
          }
          /**
           * Check if the header, data, or footer rows have changed what columns they want to display or
           * whether the sticky states have changed for the header or footer. If there is a diff, then
           * re-render that section.
           */

        }, {
          key: "_renderUpdatedColumns",
          value: function _renderUpdatedColumns() {
            var columnsDiffReducer = function columnsDiffReducer(acc, def) {
              return acc || !!def.getColumnsDiff();
            }; // Force re-render data rows if the list of column definitions have changed.


            var dataColumnsChanged = this._rowDefs.reduce(columnsDiffReducer, false);

            if (dataColumnsChanged) {
              this._forceRenderDataRows();
            } // Force re-render header/footer rows if the list of column definitions have changed.


            var headerColumnsChanged = this._headerRowDefs.reduce(columnsDiffReducer, false);

            if (headerColumnsChanged) {
              this._forceRenderHeaderRows();
            }

            var footerColumnsChanged = this._footerRowDefs.reduce(columnsDiffReducer, false);

            if (footerColumnsChanged) {
              this._forceRenderFooterRows();
            }

            return dataColumnsChanged || headerColumnsChanged || footerColumnsChanged;
          }
          /**
           * Switch to the provided data source by resetting the data and unsubscribing from the current
           * render change subscription if one exists. If the data source is null, interpret this by
           * clearing the row outlet. Otherwise start listening for new data.
           */

        }, {
          key: "_switchDataSource",
          value: function _switchDataSource(dataSource) {
            this._data = [];

            if (Object(_angular_cdk_collections__WEBPACK_IMPORTED_MODULE_2__["isDataSource"])(this.dataSource)) {
              this.dataSource.disconnect(this);
            } // Stop listening for data from the previous data source.


            if (this._renderChangeSubscription) {
              this._renderChangeSubscription.unsubscribe();

              this._renderChangeSubscription = null;
            }

            if (!dataSource) {
              if (this._dataDiffer) {
                this._dataDiffer.diff([]);
              }

              this._rowOutlet.viewContainer.clear();
            }

            this._dataSource = dataSource;
          }
          /** Set up a subscription for the data provided by the data source. */

        }, {
          key: "_observeRenderChanges",
          value: function _observeRenderChanges() {
            var _this17 = this;

            // If no data source has been set, there is nothing to observe for changes.
            if (!this.dataSource) {
              return;
            }

            var dataStream;

            if (Object(_angular_cdk_collections__WEBPACK_IMPORTED_MODULE_2__["isDataSource"])(this.dataSource)) {
              dataStream = this.dataSource.connect(this);
            } else if (Object(rxjs__WEBPACK_IMPORTED_MODULE_7__["isObservable"])(this.dataSource)) {
              dataStream = this.dataSource;
            } else if (Array.isArray(this.dataSource)) {
              dataStream = Object(rxjs__WEBPACK_IMPORTED_MODULE_7__["of"])(this.dataSource);
            }

            if (dataStream === undefined && (typeof ngDevMode === 'undefined' || ngDevMode)) {
              throw getTableUnknownDataSourceError();
            }

            this._renderChangeSubscription = dataStream.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_8__["takeUntil"])(this._onDestroy)).subscribe(function (data) {
              _this17._data = data || [];

              _this17.renderRows();
            });
          }
          /**
           * Clears any existing content in the header row outlet and creates a new embedded view
           * in the outlet using the header row definition.
           */

        }, {
          key: "_forceRenderHeaderRows",
          value: function _forceRenderHeaderRows() {
            var _this18 = this;

            // Clear the header row outlet if any content exists.
            if (this._headerRowOutlet.viewContainer.length > 0) {
              this._headerRowOutlet.viewContainer.clear();
            }

            this._headerRowDefs.forEach(function (def, i) {
              return _this18._renderRow(_this18._headerRowOutlet, def, i);
            });

            this.updateStickyHeaderRowStyles();
          }
          /**
           * Clears any existing content in the footer row outlet and creates a new embedded view
           * in the outlet using the footer row definition.
           */

        }, {
          key: "_forceRenderFooterRows",
          value: function _forceRenderFooterRows() {
            var _this19 = this;

            // Clear the footer row outlet if any content exists.
            if (this._footerRowOutlet.viewContainer.length > 0) {
              this._footerRowOutlet.viewContainer.clear();
            }

            this._footerRowDefs.forEach(function (def, i) {
              return _this19._renderRow(_this19._footerRowOutlet, def, i);
            });

            this.updateStickyFooterRowStyles();
          }
          /** Adds the sticky column styles for the rows according to the columns' stick states. */

        }, {
          key: "_addStickyColumnStyles",
          value: function _addStickyColumnStyles(rows, rowDef) {
            var _this20 = this;

            var columnDefs = Array.from(rowDef.columns || []).map(function (columnName) {
              var columnDef = _this20._columnDefsByName.get(columnName);

              if (!columnDef && (typeof ngDevMode === 'undefined' || ngDevMode)) {
                throw getTableUnknownColumnError(columnName);
              }

              return columnDef;
            });
            var stickyStartStates = columnDefs.map(function (columnDef) {
              return columnDef.sticky;
            });
            var stickyEndStates = columnDefs.map(function (columnDef) {
              return columnDef.stickyEnd;
            });

            this._stickyStyler.updateStickyColumns(rows, stickyStartStates, stickyEndStates, !this._fixedLayout || this._forceRecalculateCellWidths);
          }
          /** Gets the list of rows that have been rendered in the row outlet. */

        }, {
          key: "_getRenderedRows",
          value: function _getRenderedRows(rowOutlet) {
            var renderedRows = [];

            for (var i = 0; i < rowOutlet.viewContainer.length; i++) {
              var viewRef = rowOutlet.viewContainer.get(i);
              renderedRows.push(viewRef.rootNodes[0]);
            }

            return renderedRows;
          }
          /**
           * Get the matching row definitions that should be used for this row data. If there is only
           * one row definition, it is returned. Otherwise, find the row definitions that has a when
           * predicate that returns true with the data. If none return true, return the default row
           * definition.
           */

        }, {
          key: "_getRowDefs",
          value: function _getRowDefs(data, dataIndex) {
            if (this._rowDefs.length == 1) {
              return [this._rowDefs[0]];
            }

            var rowDefs = [];

            if (this.multiTemplateDataRows) {
              rowDefs = this._rowDefs.filter(function (def) {
                return !def.when || def.when(dataIndex, data);
              });
            } else {
              var rowDef = this._rowDefs.find(function (def) {
                return def.when && def.when(dataIndex, data);
              }) || this._defaultRowDef;

              if (rowDef) {
                rowDefs.push(rowDef);
              }
            }

            if (!rowDefs.length && (typeof ngDevMode === 'undefined' || ngDevMode)) {
              throw getTableMissingMatchingRowDefError(data);
            }

            return rowDefs;
          }
        }, {
          key: "_getEmbeddedViewArgs",
          value: function _getEmbeddedViewArgs(renderRow, index) {
            var rowDef = renderRow.rowDef;
            var context = {
              $implicit: renderRow.data
            };
            return {
              templateRef: rowDef.template,
              context: context,
              index: index
            };
          }
          /**
           * Creates a new row template in the outlet and fills it with the set of cell templates.
           * Optionally takes a context to provide to the row and cells, as well as an optional index
           * of where to place the new row template in the outlet.
           */

        }, {
          key: "_renderRow",
          value: function _renderRow(outlet, rowDef, index) {
            var context = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : {};
            // TODO(andrewseguin): enforce that one outlet was instantiated from createEmbeddedView
            var view = outlet.viewContainer.createEmbeddedView(rowDef.template, context, index);

            this._renderCellTemplateForItem(rowDef, context);

            return view;
          }
        }, {
          key: "_renderCellTemplateForItem",
          value: function _renderCellTemplateForItem(rowDef, context) {
            var _iterator10 = _createForOfIteratorHelper(this._getCellTemplates(rowDef)),
                _step10;

            try {
              for (_iterator10.s(); !(_step10 = _iterator10.n()).done;) {
                var cellTemplate = _step10.value;

                if (CdkCellOutlet.mostRecentCellOutlet) {
                  CdkCellOutlet.mostRecentCellOutlet._viewContainer.createEmbeddedView(cellTemplate, context);
                }
              }
            } catch (err) {
              _iterator10.e(err);
            } finally {
              _iterator10.f();
            }

            this._changeDetectorRef.markForCheck();
          }
          /**
           * Updates the index-related context for each row to reflect any changes in the index of the rows,
           * e.g. first/last/even/odd.
           */

        }, {
          key: "_updateRowIndexContext",
          value: function _updateRowIndexContext() {
            var viewContainer = this._rowOutlet.viewContainer;

            for (var renderIndex = 0, count = viewContainer.length; renderIndex < count; renderIndex++) {
              var viewRef = viewContainer.get(renderIndex);
              var context = viewRef.context;
              context.count = count;
              context.first = renderIndex === 0;
              context.last = renderIndex === count - 1;
              context.even = renderIndex % 2 === 0;
              context.odd = !context.even;

              if (this.multiTemplateDataRows) {
                context.dataIndex = this._renderRows[renderIndex].dataIndex;
                context.renderIndex = renderIndex;
              } else {
                context.index = this._renderRows[renderIndex].dataIndex;
              }
            }
          }
          /** Gets the column definitions for the provided row def. */

        }, {
          key: "_getCellTemplates",
          value: function _getCellTemplates(rowDef) {
            var _this21 = this;

            if (!rowDef || !rowDef.columns) {
              return [];
            }

            return Array.from(rowDef.columns, function (columnId) {
              var column = _this21._columnDefsByName.get(columnId);

              if (!column && (typeof ngDevMode === 'undefined' || ngDevMode)) {
                throw getTableUnknownColumnError(columnId);
              }

              return rowDef.extractCellTemplate(column);
            });
          }
          /** Adds native table sections (e.g. tbody) and moves the row outlets into them. */

        }, {
          key: "_applyNativeTableSections",
          value: function _applyNativeTableSections() {
            var documentFragment = this._document.createDocumentFragment();

            var sections = [{
              tag: 'thead',
              outlets: [this._headerRowOutlet]
            }, {
              tag: 'tbody',
              outlets: [this._rowOutlet, this._noDataRowOutlet]
            }, {
              tag: 'tfoot',
              outlets: [this._footerRowOutlet]
            }];

            for (var _i2 = 0, _sections = sections; _i2 < _sections.length; _i2++) {
              var section = _sections[_i2];

              var element = this._document.createElement(section.tag);

              element.setAttribute('role', 'rowgroup');

              var _iterator11 = _createForOfIteratorHelper(section.outlets),
                  _step11;

              try {
                for (_iterator11.s(); !(_step11 = _iterator11.n()).done;) {
                  var outlet = _step11.value;
                  element.appendChild(outlet.elementRef.nativeElement);
                }
              } catch (err) {
                _iterator11.e(err);
              } finally {
                _iterator11.f();
              }

              documentFragment.appendChild(element);
            } // Use a DocumentFragment so we don't hit the DOM on each iteration.


            this._elementRef.nativeElement.appendChild(documentFragment);
          }
          /**
           * Forces a re-render of the data rows. Should be called in cases where there has been an input
           * change that affects the evaluation of which rows should be rendered, e.g. toggling
           * `multiTemplateDataRows` or adding/removing row definitions.
           */

        }, {
          key: "_forceRenderDataRows",
          value: function _forceRenderDataRows() {
            this._dataDiffer.diff([]);

            this._rowOutlet.viewContainer.clear();

            this.renderRows();
          }
          /**
           * Checks if there has been a change in sticky states since last check and applies the correct
           * sticky styles. Since checking resets the "dirty" state, this should only be performed once
           * during a change detection and after the inputs are settled (after content check).
           */

        }, {
          key: "_checkStickyStates",
          value: function _checkStickyStates() {
            var stickyCheckReducer = function stickyCheckReducer(acc, d) {
              return acc || d.hasStickyChanged();
            }; // Note that the check needs to occur for every definition since it notifies the definition
            // that it can reset its dirty state. Using another operator like `some` may short-circuit
            // remaining definitions and leave them in an unchecked state.


            if (this._headerRowDefs.reduce(stickyCheckReducer, false)) {
              this.updateStickyHeaderRowStyles();
            }

            if (this._footerRowDefs.reduce(stickyCheckReducer, false)) {
              this.updateStickyFooterRowStyles();
            }

            if (Array.from(this._columnDefsByName.values()).reduce(stickyCheckReducer, false)) {
              this._stickyColumnStylesNeedReset = true;
              this.updateStickyColumnStyles();
            }
          }
          /**
           * Creates the sticky styler that will be used for sticky rows and columns. Listens
           * for directionality changes and provides the latest direction to the styler. Re-applies column
           * stickiness when directionality changes.
           */

        }, {
          key: "_setupStickyStyler",
          value: function _setupStickyStyler() {
            var _this22 = this;

            var direction = this._dir ? this._dir.value : 'ltr';
            this._stickyStyler = new StickyStyler(this._isNativeHtmlTable, this.stickyCssClass, direction, this._coalescedStyleScheduler, this._platform.isBrowser, this.needsPositionStickyOnElement);
            (this._dir ? this._dir.change : Object(rxjs__WEBPACK_IMPORTED_MODULE_7__["of"])()).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_8__["takeUntil"])(this._onDestroy)).subscribe(function (value) {
              _this22._stickyStyler.direction = value;

              _this22.updateStickyColumnStyles();
            });
          }
          /** Filters definitions that belong to this table from a QueryList. */

        }, {
          key: "_getOwnDefs",
          value: function _getOwnDefs(items) {
            var _this23 = this;

            return items.filter(function (item) {
              return !item._table || item._table === _this23;
            });
          }
          /** Creates or removes the no data row, depending on whether any data is being shown. */

        }, {
          key: "_updateNoDataRow",
          value: function _updateNoDataRow() {
            var noDataRow = this._customNoDataRow || this._noDataRow;

            if (noDataRow) {
              var shouldShow = this._rowOutlet.viewContainer.length === 0;

              if (shouldShow !== this._isShowingNoDataRow) {
                var container = this._noDataRowOutlet.viewContainer;
                shouldShow ? container.createEmbeddedView(noDataRow.templateRef) : container.clear();
                this._isShowingNoDataRow = shouldShow;
              }
            }
          }
        }, {
          key: "trackBy",
          get: function get() {
            return this._trackByFn;
          },
          set: function set(fn) {
            if ((typeof ngDevMode === 'undefined' || ngDevMode) && fn != null && typeof fn !== 'function') {
              console.warn("trackBy must be a function, but received ".concat(JSON.stringify(fn), "."));
            }

            this._trackByFn = fn;
          }
          /**
           * The table's source of data, which can be provided in three ways (in order of complexity):
           *   - Simple data array (each object represents one table row)
           *   - Stream that emits a data array each time the array changes
           *   - `DataSource` object that implements the connect/disconnect interface.
           *
           * If a data array is provided, the table must be notified when the array's objects are
           * added, removed, or moved. This can be done by calling the `renderRows()` function which will
           * render the diff since the last table render. If the data array reference is changed, the table
           * will automatically trigger an update to the rows.
           *
           * When providing an Observable stream, the table will trigger an update automatically when the
           * stream emits a new array of data.
           *
           * Finally, when providing a `DataSource` object, the table will use the Observable stream
           * provided by the connect function and trigger updates when that stream emits new data array
           * values. During the table's ngOnDestroy or when the data source is removed from the table, the
           * table will call the DataSource's `disconnect` function (may be useful for cleaning up any
           * subscriptions registered during the connect process).
           */

        }, {
          key: "dataSource",
          get: function get() {
            return this._dataSource;
          },
          set: function set(dataSource) {
            if (this._dataSource !== dataSource) {
              this._switchDataSource(dataSource);
            }
          }
          /**
           * Whether to allow multiple rows per data object by evaluating which rows evaluate their 'when'
           * predicate to true. If `multiTemplateDataRows` is false, which is the default value, then each
           * dataobject will render the first row that evaluates its when predicate to true, in the order
           * defined in the table, or otherwise the default row which does not have a when predicate.
           */

        }, {
          key: "multiTemplateDataRows",
          get: function get() {
            return this._multiTemplateDataRows;
          },
          set: function set(v) {
            this._multiTemplateDataRows = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_1__["coerceBooleanProperty"])(v); // In Ivy if this value is set via a static attribute (e.g. <table multiTemplateDataRows>),
            // this setter will be invoked before the row outlet has been defined hence the null check.

            if (this._rowOutlet && this._rowOutlet.viewContainer.length) {
              this._forceRenderDataRows();

              this.updateStickyColumnStyles();
            }
          }
          /**
           * Whether to use a fixed table layout. Enabling this option will enforce consistent column widths
           * and optimize rendering sticky styles for native tables. No-op for flex tables.
           */

        }, {
          key: "fixedLayout",
          get: function get() {
            return this._fixedLayout;
          },
          set: function set(v) {
            this._fixedLayout = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_1__["coerceBooleanProperty"])(v); // Toggling `fixedLayout` may change column widths. Sticky column styles should be recalculated.

            this._forceRecalculateCellWidths = true;
            this._stickyColumnStylesNeedReset = true;
          }
        }]);

        return CdkTable;
      }();

      CdkTable.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Component"],
        args: [{
          selector: 'cdk-table, table[cdk-table]',
          exportAs: 'cdkTable',
          template: CDK_TABLE_TEMPLATE,
          host: {
            'class': 'cdk-table',
            '[class.cdk-table-fixed-layout]': 'fixedLayout'
          },
          encapsulation: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ViewEncapsulation"].None,
          // The "OnPush" status for the `MatTable` component is effectively a noop, so we are removing it.
          // The view for `MatTable` consists entirely of templates declared in other views. As they are
          // declared elsewhere, they are checked when their declaration points are checked.
          // tslint:disable-next-line:validate-decorators
          changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ChangeDetectionStrategy"].Default,
          providers: [{
            provide: CDK_TABLE,
            useExisting: CdkTable
          }, {
            provide: _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_2__["_VIEW_REPEATER_STRATEGY"],
            useClass: _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_2__["_DisposeViewRepeaterStrategy"]
          }, {
            provide: _COALESCED_STYLE_SCHEDULER,
            useClass: _CoalescedStyleScheduler
          }],
          styles: [".cdk-table-fixed-layout{table-layout:fixed}\n"]
        }]
      }];

      CdkTable.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["IterableDiffers"]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ChangeDetectorRef"]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ElementRef"]
        }, {
          type: String,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Attribute"],
            args: ['role']
          }]
        }, {
          type: _angular_cdk_bidi__WEBPACK_IMPORTED_MODULE_0__["Directionality"],
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Optional"]
          }]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Inject"],
            args: [_angular_common__WEBPACK_IMPORTED_MODULE_5__["DOCUMENT"]]
          }]
        }, {
          type: _angular_cdk_platform__WEBPACK_IMPORTED_MODULE_3__["Platform"]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Optional"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Inject"],
            args: [_angular_cdk_collections__WEBPACK_IMPORTED_MODULE_2__["_VIEW_REPEATER_STRATEGY"]]
          }]
        }, {
          type: _CoalescedStyleScheduler,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Optional"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Inject"],
            args: [_COALESCED_STYLE_SCHEDULER]
          }]
        }, {
          type: _angular_cdk_scrolling__WEBPACK_IMPORTED_MODULE_4__["ViewportRuler"],
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Optional"]
          }]
        }];
      };

      CdkTable.propDecorators = {
        trackBy: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Input"]
        }],
        dataSource: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Input"]
        }],
        multiTemplateDataRows: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Input"]
        }],
        fixedLayout: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Input"]
        }],
        _rowOutlet: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ViewChild"],
          args: [DataRowOutlet, {
            "static": true
          }]
        }],
        _headerRowOutlet: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ViewChild"],
          args: [HeaderRowOutlet, {
            "static": true
          }]
        }],
        _footerRowOutlet: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ViewChild"],
          args: [FooterRowOutlet, {
            "static": true
          }]
        }],
        _noDataRowOutlet: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ViewChild"],
          args: [NoDataRowOutlet, {
            "static": true
          }]
        }],
        _contentColumnDefs: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ContentChildren"],
          args: [CdkColumnDef, {
            descendants: true
          }]
        }],
        _contentRowDefs: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ContentChildren"],
          args: [CdkRowDef, {
            descendants: true
          }]
        }],
        _contentHeaderRowDefs: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ContentChildren"],
          args: [CdkHeaderRowDef, {
            descendants: true
          }]
        }],
        _contentFooterRowDefs: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ContentChildren"],
          args: [CdkFooterRowDef, {
            descendants: true
          }]
        }],
        _noDataRow: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ContentChild"],
          args: [CdkNoDataRow]
        }]
      };
      /** Utility function that gets a merged list of the entries in an array and values of a Set. */

      function mergeArrayAndSet(array, set) {
        return array.concat(Array.from(set));
      }
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * Column that simply shows text content for the header and row cells. Assumes that the table
       * is using the native table implementation (`<table>`).
       *
       * By default, the name of this column will be the header text and data property accessor.
       * The header text can be overridden with the `headerText` input. Cell values can be overridden with
       * the `dataAccessor` input. Change the text justification to the start or end using the `justify`
       * input.
       */


      var CdkTextColumn = /*#__PURE__*/function () {
        function CdkTextColumn( // `CdkTextColumn` is always requiring a table, but we just assert it manually
        // for better error reporting.
        // tslint:disable-next-line: lightweight-tokens
        _table, _options) {
          _classCallCheck(this, CdkTextColumn);

          this._table = _table;
          this._options = _options;
          /** Alignment of the cell values. */

          this.justify = 'start';
          this._options = _options || {};
        }
        /** Column name that should be used to reference this column. */


        _createClass(CdkTextColumn, [{
          key: "ngOnInit",
          value: function ngOnInit() {
            this._syncColumnDefName();

            if (this.headerText === undefined) {
              this.headerText = this._createDefaultHeaderText();
            }

            if (!this.dataAccessor) {
              this.dataAccessor = this._options.defaultDataAccessor || function (data, name) {
                return data[name];
              };
            }

            if (this._table) {
              // Provide the cell and headerCell directly to the table with the static `ViewChild` query,
              // since the columnDef will not pick up its content by the time the table finishes checking
              // its content and initializing the rows.
              this.columnDef.cell = this.cell;
              this.columnDef.headerCell = this.headerCell;

              this._table.addColumnDef(this.columnDef);
            } else if (typeof ngDevMode === 'undefined' || ngDevMode) {
              throw getTableTextColumnMissingParentTableError();
            }
          }
        }, {
          key: "ngOnDestroy",
          value: function ngOnDestroy() {
            if (this._table) {
              this._table.removeColumnDef(this.columnDef);
            }
          }
          /**
           * Creates a default header text. Use the options' header text transformation function if one
           * has been provided. Otherwise simply capitalize the column name.
           */

        }, {
          key: "_createDefaultHeaderText",
          value: function _createDefaultHeaderText() {
            var name = this.name;

            if (!name && (typeof ngDevMode === 'undefined' || ngDevMode)) {
              throw getTableTextColumnMissingNameError();
            }

            if (this._options && this._options.defaultHeaderTextTransform) {
              return this._options.defaultHeaderTextTransform(name);
            }

            return name[0].toUpperCase() + name.slice(1);
          }
          /** Synchronizes the column definition name with the text column name. */

        }, {
          key: "_syncColumnDefName",
          value: function _syncColumnDefName() {
            if (this.columnDef) {
              this.columnDef.name = this.name;
            }
          }
        }, {
          key: "name",
          get: function get() {
            return this._name;
          },
          set: function set(name) {
            this._name = name; // With Ivy, inputs can be initialized before static query results are
            // available. In that case, we defer the synchronization until "ngOnInit" fires.

            this._syncColumnDefName();
          }
        }]);

        return CdkTextColumn;
      }();

      CdkTextColumn.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Component"],
        args: [{
          selector: 'cdk-text-column',
          template: "\n    <ng-container cdkColumnDef>\n      <th cdk-header-cell *cdkHeaderCellDef [style.text-align]=\"justify\">\n        {{headerText}}\n      </th>\n      <td cdk-cell *cdkCellDef=\"let data\" [style.text-align]=\"justify\">\n        {{dataAccessor(data, name)}}\n      </td>\n    </ng-container>\n  ",
          encapsulation: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ViewEncapsulation"].None,
          // Change detection is intentionally not set to OnPush. This component's template will be provided
          // to the table to be inserted into its view. This is problematic when change detection runs since
          // the bindings in this template will be evaluated _after_ the table's view is evaluated, which
          // mean's the template in the table's view will not have the updated value (and in fact will cause
          // an ExpressionChangedAfterItHasBeenCheckedError).
          // tslint:disable-next-line:validate-decorators
          changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ChangeDetectionStrategy"].Default
        }]
      }];

      CdkTextColumn.ctorParameters = function () {
        return [{
          type: CdkTable,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Optional"]
          }]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Optional"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Inject"],
            args: [TEXT_COLUMN_OPTIONS]
          }]
        }];
      };

      CdkTextColumn.propDecorators = {
        name: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Input"]
        }],
        headerText: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Input"]
        }],
        dataAccessor: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Input"]
        }],
        justify: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["Input"]
        }],
        columnDef: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ViewChild"],
          args: [CdkColumnDef, {
            "static": true
          }]
        }],
        cell: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ViewChild"],
          args: [CdkCellDef, {
            "static": true
          }]
        }],
        headerCell: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["ViewChild"],
          args: [CdkHeaderCellDef, {
            "static": true
          }]
        }]
      };
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      var EXPORTED_DECLARATIONS = [CdkTable, CdkRowDef, CdkCellDef, CdkCellOutlet, CdkHeaderCellDef, CdkFooterCellDef, CdkColumnDef, CdkCell, CdkRow, CdkHeaderCell, CdkFooterCell, CdkHeaderRow, CdkHeaderRowDef, CdkFooterRow, CdkFooterRowDef, DataRowOutlet, HeaderRowOutlet, FooterRowOutlet, CdkTextColumn, CdkNoDataRow, NoDataRowOutlet];

      var CdkTableModule = function CdkTableModule() {
        _classCallCheck(this, CdkTableModule);
      };

      CdkTableModule.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_6__["NgModule"],
        args: [{
          exports: EXPORTED_DECLARATIONS,
          declarations: EXPORTED_DECLARATIONS,
          imports: [_angular_cdk_scrolling__WEBPACK_IMPORTED_MODULE_4__["ScrollingModule"]]
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
      //# sourceMappingURL=table.js.map

      /***/
    },

    /***/
    "LUZP":
    /*!*********************************************************!*\
      !*** ./node_modules/@angular/material/fesm2015/sort.js ***!
      \*********************************************************/

    /*! exports provided: MAT_SORT_HEADER_INTL_PROVIDER, MAT_SORT_HEADER_INTL_PROVIDER_FACTORY, MatSort, MatSortHeader, MatSortHeaderIntl, MatSortModule, matSortAnimations */

    /***/
    function LUZP(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MAT_SORT_HEADER_INTL_PROVIDER", function () {
        return MAT_SORT_HEADER_INTL_PROVIDER;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MAT_SORT_HEADER_INTL_PROVIDER_FACTORY", function () {
        return MAT_SORT_HEADER_INTL_PROVIDER_FACTORY;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatSort", function () {
        return MatSort;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatSortHeader", function () {
        return MatSortHeader;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatSortHeaderIntl", function () {
        return MatSortHeaderIntl;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatSortModule", function () {
        return MatSortModule;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "matSortAnimations", function () {
        return matSortAnimations;
      });
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! @angular/cdk/coercion */
      "8LU1");
      /* harmony import */


      var _angular_material_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @angular/material/core */
      "UhP/");
      /* harmony import */


      var _angular_cdk_a11y__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/cdk/a11y */
      "YEUz");
      /* harmony import */


      var _angular_cdk_keycodes__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/cdk/keycodes */
      "Ht+U");
      /* harmony import */


      var rxjs__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! rxjs */
      "qCKp");
      /* harmony import */


      var _angular_animations__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/animations */
      "GS7A");
      /* harmony import */


      var _angular_common__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @angular/common */
      "SVse");
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /** @docs-private */


      function getSortDuplicateSortableIdError(id) {
        return Error("Cannot have two MatSortables with the same id (".concat(id, ")."));
      }
      /** @docs-private */


      function getSortHeaderNotContainedWithinSortError() {
        return Error("MatSortHeader must be placed within a parent element with the MatSort directive.");
      }
      /** @docs-private */


      function getSortHeaderMissingIdError() {
        return Error("MatSortHeader must be provided with a unique id.");
      }
      /** @docs-private */


      function getSortInvalidDirectionError(direction) {
        return Error("".concat(direction, " is not a valid sort direction ('asc' or 'desc')."));
      }
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */
      // Boilerplate for applying mixins to MatSort.

      /** @docs-private */


      var MatSortBase = function MatSortBase() {
        _classCallCheck(this, MatSortBase);
      };

      var _MatSortMixinBase = Object(_angular_material_core__WEBPACK_IMPORTED_MODULE_2__["mixinInitialized"])(Object(_angular_material_core__WEBPACK_IMPORTED_MODULE_2__["mixinDisabled"])(MatSortBase));
      /** Container for MatSortables to manage the sort state and provide default sort parameters. */


      var MatSort = /*#__PURE__*/function (_MatSortMixinBase2) {
        _inherits(MatSort, _MatSortMixinBase2);

        var _super14 = _createSuper(MatSort);

        function MatSort() {
          var _this24;

          _classCallCheck(this, MatSort);

          _this24 = _super14.apply(this, arguments);
          /** Collection of all registered sortables that this directive manages. */

          _this24.sortables = new Map();
          /** Used to notify any child components listening to state changes. */

          _this24._stateChanges = new rxjs__WEBPACK_IMPORTED_MODULE_5__["Subject"]();
          /**
           * The direction to set when an MatSortable is initially sorted.
           * May be overriden by the MatSortable's sort start.
           */

          _this24.start = 'asc';
          _this24._direction = '';
          /** Event emitted when the user changes either the active sort or sort direction. */

          _this24.sortChange = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"]();
          return _this24;
        }
        /** The sort direction of the currently active MatSortable. */


        _createClass(MatSort, [{
          key: "register",

          /**
           * Register function to be used by the contained MatSortables. Adds the MatSortable to the
           * collection of MatSortables.
           */
          value: function register(sortable) {
            if (typeof ngDevMode === 'undefined' || ngDevMode) {
              if (!sortable.id) {
                throw getSortHeaderMissingIdError();
              }

              if (this.sortables.has(sortable.id)) {
                throw getSortDuplicateSortableIdError(sortable.id);
              }
            }

            this.sortables.set(sortable.id, sortable);
          }
          /**
           * Unregister function to be used by the contained MatSortables. Removes the MatSortable from the
           * collection of contained MatSortables.
           */

        }, {
          key: "deregister",
          value: function deregister(sortable) {
            this.sortables["delete"](sortable.id);
          }
          /** Sets the active sort id and determines the new sort direction. */

        }, {
          key: "sort",
          value: function sort(sortable) {
            if (this.active != sortable.id) {
              this.active = sortable.id;
              this.direction = sortable.start ? sortable.start : this.start;
            } else {
              this.direction = this.getNextSortDirection(sortable);
            }

            this.sortChange.emit({
              active: this.active,
              direction: this.direction
            });
          }
          /** Returns the next sort direction of the active sortable, checking for potential overrides. */

        }, {
          key: "getNextSortDirection",
          value: function getNextSortDirection(sortable) {
            if (!sortable) {
              return '';
            } // Get the sort direction cycle with the potential sortable overrides.


            var disableClear = sortable.disableClear != null ? sortable.disableClear : this.disableClear;
            var sortDirectionCycle = getSortDirectionCycle(sortable.start || this.start, disableClear); // Get and return the next direction in the cycle

            var nextDirectionIndex = sortDirectionCycle.indexOf(this.direction) + 1;

            if (nextDirectionIndex >= sortDirectionCycle.length) {
              nextDirectionIndex = 0;
            }

            return sortDirectionCycle[nextDirectionIndex];
          }
        }, {
          key: "ngOnInit",
          value: function ngOnInit() {
            this._markInitialized();
          }
        }, {
          key: "ngOnChanges",
          value: function ngOnChanges() {
            this._stateChanges.next();
          }
        }, {
          key: "ngOnDestroy",
          value: function ngOnDestroy() {
            this._stateChanges.complete();
          }
        }, {
          key: "direction",
          get: function get() {
            return this._direction;
          },
          set: function set(direction) {
            if (direction && direction !== 'asc' && direction !== 'desc' && (typeof ngDevMode === 'undefined' || ngDevMode)) {
              throw getSortInvalidDirectionError(direction);
            }

            this._direction = direction;
          }
          /**
           * Whether to disable the user from clearing the sort by finishing the sort direction cycle.
           * May be overriden by the MatSortable's disable clear input.
           */

        }, {
          key: "disableClear",
          get: function get() {
            return this._disableClear;
          },
          set: function set(v) {
            this._disableClear = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_1__["coerceBooleanProperty"])(v);
          }
        }]);

        return MatSort;
      }(_MatSortMixinBase);

      MatSort.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"],
        args: [{
          selector: '[matSort]',
          exportAs: 'matSort',
          host: {
            'class': 'mat-sort'
          },
          inputs: ['disabled: matSortDisabled']
        }]
      }];
      MatSort.propDecorators = {
        active: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['matSortActive']
        }],
        start: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['matSortStart']
        }],
        direction: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['matSortDirection']
        }],
        disableClear: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['matSortDisableClear']
        }],
        sortChange: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Output"],
          args: ['matSortChange']
        }]
      };
      /** Returns the sort direction cycle to use given the provided parameters of order and clear. */

      function getSortDirectionCycle(start, disableClear) {
        var sortOrder = ['asc', 'desc'];

        if (start == 'desc') {
          sortOrder.reverse();
        }

        if (!disableClear) {
          sortOrder.push('');
        }

        return sortOrder;
      }
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */


      var SORT_ANIMATION_TRANSITION = _angular_material_core__WEBPACK_IMPORTED_MODULE_2__["AnimationDurations"].ENTERING + ' ' + _angular_material_core__WEBPACK_IMPORTED_MODULE_2__["AnimationCurves"].STANDARD_CURVE;
      /**
       * Animations used by MatSort.
       * @docs-private
       */

      var matSortAnimations = {
        /** Animation that moves the sort indicator. */
        indicator: Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["trigger"])('indicator', [Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["state"])('active-asc, asc', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["style"])({
          transform: 'translateY(0px)'
        })), // 10px is the height of the sort indicator, minus the width of the pointers
        Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["state"])('active-desc, desc', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["style"])({
          transform: 'translateY(10px)'
        })), Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["transition"])('active-asc <=> active-desc', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["animate"])(SORT_ANIMATION_TRANSITION))]),

        /** Animation that rotates the left pointer of the indicator based on the sorting direction. */
        leftPointer: Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["trigger"])('leftPointer', [Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["state"])('active-asc, asc', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["style"])({
          transform: 'rotate(-45deg)'
        })), Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["state"])('active-desc, desc', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["style"])({
          transform: 'rotate(45deg)'
        })), Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["transition"])('active-asc <=> active-desc', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["animate"])(SORT_ANIMATION_TRANSITION))]),

        /** Animation that rotates the right pointer of the indicator based on the sorting direction. */
        rightPointer: Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["trigger"])('rightPointer', [Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["state"])('active-asc, asc', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["style"])({
          transform: 'rotate(45deg)'
        })), Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["state"])('active-desc, desc', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["style"])({
          transform: 'rotate(-45deg)'
        })), Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["transition"])('active-asc <=> active-desc', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["animate"])(SORT_ANIMATION_TRANSITION))]),

        /** Animation that controls the arrow opacity. */
        arrowOpacity: Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["trigger"])('arrowOpacity', [Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["state"])('desc-to-active, asc-to-active, active', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["style"])({
          opacity: 1
        })), Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["state"])('desc-to-hint, asc-to-hint, hint', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["style"])({
          opacity: .54
        })), Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["state"])('hint-to-desc, active-to-desc, desc, hint-to-asc, active-to-asc, asc, void', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["style"])({
          opacity: 0
        })), // Transition between all states except for immediate transitions
        Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["transition"])('* => asc, * => desc, * => active, * => hint, * => void', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["animate"])('0ms')), Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["transition"])('* <=> *', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["animate"])(SORT_ANIMATION_TRANSITION))]),

        /**
         * Animation for the translation of the arrow as a whole. States are separated into two
         * groups: ones with animations and others that are immediate. Immediate states are asc, desc,
         * peek, and active. The other states define a specific animation (source-to-destination)
         * and are determined as a function of their prev user-perceived state and what the next state
         * should be.
         */
        arrowPosition: Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["trigger"])('arrowPosition', [// Hidden Above => Hint Center
        Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["transition"])('* => desc-to-hint, * => desc-to-active', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["animate"])(SORT_ANIMATION_TRANSITION, Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["keyframes"])([Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["style"])({
          transform: 'translateY(-25%)'
        }), Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["style"])({
          transform: 'translateY(0)'
        })]))), // Hint Center => Hidden Below
        Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["transition"])('* => hint-to-desc, * => active-to-desc', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["animate"])(SORT_ANIMATION_TRANSITION, Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["keyframes"])([Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["style"])({
          transform: 'translateY(0)'
        }), Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["style"])({
          transform: 'translateY(25%)'
        })]))), // Hidden Below => Hint Center
        Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["transition"])('* => asc-to-hint, * => asc-to-active', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["animate"])(SORT_ANIMATION_TRANSITION, Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["keyframes"])([Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["style"])({
          transform: 'translateY(25%)'
        }), Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["style"])({
          transform: 'translateY(0)'
        })]))), // Hint Center => Hidden Above
        Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["transition"])('* => hint-to-asc, * => active-to-asc', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["animate"])(SORT_ANIMATION_TRANSITION, Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["keyframes"])([Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["style"])({
          transform: 'translateY(0)'
        }), Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["style"])({
          transform: 'translateY(-25%)'
        })]))), Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["state"])('desc-to-hint, asc-to-hint, hint, desc-to-active, asc-to-active, active', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["style"])({
          transform: 'translateY(0)'
        })), Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["state"])('hint-to-desc, active-to-desc, desc', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["style"])({
          transform: 'translateY(-25%)'
        })), Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["state"])('hint-to-asc, active-to-asc, asc', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["style"])({
          transform: 'translateY(25%)'
        }))]),

        /** Necessary trigger that calls animate on children animations. */
        allowChildren: Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["trigger"])('allowChildren', [Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["transition"])('* <=> *', [Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["query"])('@*', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_6__["animateChild"])(), {
          optional: true
        })])])
      };
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * To modify the labels and text displayed, create a new instance of MatSortHeaderIntl and
       * include it in a custom provider.
       */

      var MatSortHeaderIntl = function MatSortHeaderIntl() {
        _classCallCheck(this, MatSortHeaderIntl);

        /**
         * Stream that emits whenever the labels here are changed. Use this to notify
         * components if the labels have changed after initialization.
         */
        this.changes = new rxjs__WEBPACK_IMPORTED_MODULE_5__["Subject"]();
        /**
         * ARIA label for the sorting button.
         * @deprecated Not used anymore. To be removed.
         * @breaking-change 8.0.0
         */

        this.sortButtonLabel = function (id) {
          return "Change sorting for ".concat(id);
        };
      };

      MatSortHeaderIntl.ɵprov = Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineInjectable"])({
        factory: function MatSortHeaderIntl_Factory() {
          return new MatSortHeaderIntl();
        },
        token: MatSortHeaderIntl,
        providedIn: "root"
      });
      MatSortHeaderIntl.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"],
        args: [{
          providedIn: 'root'
        }]
      }];
      /** @docs-private */

      function MAT_SORT_HEADER_INTL_PROVIDER_FACTORY(parentIntl) {
        return parentIntl || new MatSortHeaderIntl();
      }
      /** @docs-private */


      var MAT_SORT_HEADER_INTL_PROVIDER = {
        // If there is already an MatSortHeaderIntl available, use that. Otherwise, provide a new one.
        provide: MatSortHeaderIntl,
        deps: [[new _angular_core__WEBPACK_IMPORTED_MODULE_0__["Optional"](), new _angular_core__WEBPACK_IMPORTED_MODULE_0__["SkipSelf"](), MatSortHeaderIntl]],
        useFactory: MAT_SORT_HEADER_INTL_PROVIDER_FACTORY
      };
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */
      // Boilerplate for applying mixins to the sort header.

      /** @docs-private */

      var MatSortHeaderBase = function MatSortHeaderBase() {
        _classCallCheck(this, MatSortHeaderBase);
      };

      var _MatSortHeaderMixinBase = Object(_angular_material_core__WEBPACK_IMPORTED_MODULE_2__["mixinDisabled"])(MatSortHeaderBase);
      /**
       * Applies sorting behavior (click to change sort) and styles to an element, including an
       * arrow to display the current sort direction.
       *
       * Must be provided with an id and contained within a parent MatSort directive.
       *
       * If used on header cells in a CdkTable, it will automatically default its id from its containing
       * column definition.
       */


      var MatSortHeader = /*#__PURE__*/function (_MatSortHeaderMixinBa) {
        _inherits(MatSortHeader, _MatSortHeaderMixinBa);

        var _super15 = _createSuper(MatSortHeader);

        function MatSortHeader(_intl, _changeDetectorRef, // `MatSort` is not optionally injected, but just asserted manually w/ better error.
        // tslint:disable-next-line: lightweight-tokens
        _sort, _columnDef, _focusMonitor, _elementRef) {
          var _this25;

          _classCallCheck(this, MatSortHeader);

          // Note that we use a string token for the `_columnDef`, because the value is provided both by
          // `material/table` and `cdk/table` and we can't have the CDK depending on Material,
          // and we want to avoid having the sort header depending on the CDK table because
          // of this single reference.
          _this25 = _super15.call(this);
          _this25._intl = _intl;
          _this25._changeDetectorRef = _changeDetectorRef;
          _this25._sort = _sort;
          _this25._columnDef = _columnDef;
          _this25._focusMonitor = _focusMonitor;
          _this25._elementRef = _elementRef;
          /**
           * Flag set to true when the indicator should be displayed while the sort is not active. Used to
           * provide an affordance that the header is sortable by showing on focus and hover.
           */

          _this25._showIndicatorHint = false;
          /** The direction the arrow should be facing according to the current state. */

          _this25._arrowDirection = '';
          /**
           * Whether the view state animation should show the transition between the `from` and `to` states.
           */

          _this25._disableViewStateAnimation = false;
          /** Sets the position of the arrow that displays when sorted. */

          _this25.arrowPosition = 'after';

          if (!_sort && (typeof ngDevMode === 'undefined' || ngDevMode)) {
            throw getSortHeaderNotContainedWithinSortError();
          }

          _this25._rerenderSubscription = Object(rxjs__WEBPACK_IMPORTED_MODULE_5__["merge"])(_sort.sortChange, _sort._stateChanges, _intl.changes).subscribe(function () {
            if (_this25._isSorted()) {
              _this25._updateArrowDirection();
            } // If this header was recently active and now no longer sorted, animate away the arrow.


            if (!_this25._isSorted() && _this25._viewState && _this25._viewState.toState === 'active') {
              _this25._disableViewStateAnimation = false;

              _this25._setAnimationTransitionState({
                fromState: 'active',
                toState: _this25._arrowDirection
              });
            }

            _changeDetectorRef.markForCheck();
          });
          return _this25;
        }
        /** Overrides the disable clear value of the containing MatSort for this MatSortable. */


        _createClass(MatSortHeader, [{
          key: "ngOnInit",
          value: function ngOnInit() {
            if (!this.id && this._columnDef) {
              this.id = this._columnDef.name;
            } // Initialize the direction of the arrow and set the view state to be immediately that state.


            this._updateArrowDirection();

            this._setAnimationTransitionState({
              toState: this._isSorted() ? 'active' : this._arrowDirection
            });

            this._sort.register(this);
          }
        }, {
          key: "ngAfterViewInit",
          value: function ngAfterViewInit() {
            var _this26 = this;

            // We use the focus monitor because we also want to style
            // things differently based on the focus origin.
            this._focusMonitor.monitor(this._elementRef, true).subscribe(function (origin) {
              var newState = !!origin;

              if (newState !== _this26._showIndicatorHint) {
                _this26._setIndicatorHintVisible(newState);

                _this26._changeDetectorRef.markForCheck();
              }
            });
          }
        }, {
          key: "ngOnDestroy",
          value: function ngOnDestroy() {
            this._focusMonitor.stopMonitoring(this._elementRef);

            this._sort.deregister(this);

            this._rerenderSubscription.unsubscribe();
          }
          /**
           * Sets the "hint" state such that the arrow will be semi-transparently displayed as a hint to the
           * user showing what the active sort will become. If set to false, the arrow will fade away.
           */

        }, {
          key: "_setIndicatorHintVisible",
          value: function _setIndicatorHintVisible(visible) {
            // No-op if the sort header is disabled - should not make the hint visible.
            if (this._isDisabled() && visible) {
              return;
            }

            this._showIndicatorHint = visible;

            if (!this._isSorted()) {
              this._updateArrowDirection();

              if (this._showIndicatorHint) {
                this._setAnimationTransitionState({
                  fromState: this._arrowDirection,
                  toState: 'hint'
                });
              } else {
                this._setAnimationTransitionState({
                  fromState: 'hint',
                  toState: this._arrowDirection
                });
              }
            }
          }
          /**
           * Sets the animation transition view state for the arrow's position and opacity. If the
           * `disableViewStateAnimation` flag is set to true, the `fromState` will be ignored so that
           * no animation appears.
           */

        }, {
          key: "_setAnimationTransitionState",
          value: function _setAnimationTransitionState(viewState) {
            this._viewState = viewState; // If the animation for arrow position state (opacity/translation) should be disabled,
            // remove the fromState so that it jumps right to the toState.

            if (this._disableViewStateAnimation) {
              this._viewState = {
                toState: viewState.toState
              };
            }
          }
          /** Triggers the sort on this sort header and removes the indicator hint. */

        }, {
          key: "_toggleOnInteraction",
          value: function _toggleOnInteraction() {
            this._sort.sort(this); // Do not show the animation if the header was already shown in the right position.


            if (this._viewState.toState === 'hint' || this._viewState.toState === 'active') {
              this._disableViewStateAnimation = true;
            } // If the arrow is now sorted, animate the arrow into place. Otherwise, animate it away into
            // the direction it is facing.


            var viewState = this._isSorted() ? {
              fromState: this._arrowDirection,
              toState: 'active'
            } : {
              fromState: 'active',
              toState: this._arrowDirection
            };

            this._setAnimationTransitionState(viewState);

            this._showIndicatorHint = false;
          }
        }, {
          key: "_handleClick",
          value: function _handleClick() {
            if (!this._isDisabled()) {
              this._toggleOnInteraction();
            }
          }
        }, {
          key: "_handleKeydown",
          value: function _handleKeydown(event) {
            if (!this._isDisabled() && (event.keyCode === _angular_cdk_keycodes__WEBPACK_IMPORTED_MODULE_4__["SPACE"] || event.keyCode === _angular_cdk_keycodes__WEBPACK_IMPORTED_MODULE_4__["ENTER"])) {
              event.preventDefault();

              this._toggleOnInteraction();
            }
          }
          /** Whether this MatSortHeader is currently sorted in either ascending or descending order. */

        }, {
          key: "_isSorted",
          value: function _isSorted() {
            return this._sort.active == this.id && (this._sort.direction === 'asc' || this._sort.direction === 'desc');
          }
          /** Returns the animation state for the arrow direction (indicator and pointers). */

        }, {
          key: "_getArrowDirectionState",
          value: function _getArrowDirectionState() {
            return "".concat(this._isSorted() ? 'active-' : '').concat(this._arrowDirection);
          }
          /** Returns the arrow position state (opacity, translation). */

        }, {
          key: "_getArrowViewState",
          value: function _getArrowViewState() {
            var fromState = this._viewState.fromState;
            return (fromState ? "".concat(fromState, "-to-") : '') + this._viewState.toState;
          }
          /**
           * Updates the direction the arrow should be pointing. If it is not sorted, the arrow should be
           * facing the start direction. Otherwise if it is sorted, the arrow should point in the currently
           * active sorted direction. The reason this is updated through a function is because the direction
           * should only be changed at specific times - when deactivated but the hint is displayed and when
           * the sort is active and the direction changes. Otherwise the arrow's direction should linger
           * in cases such as the sort becoming deactivated but we want to animate the arrow away while
           * preserving its direction, even though the next sort direction is actually different and should
           * only be changed once the arrow displays again (hint or activation).
           */

        }, {
          key: "_updateArrowDirection",
          value: function _updateArrowDirection() {
            this._arrowDirection = this._isSorted() ? this._sort.direction : this.start || this._sort.start;
          }
        }, {
          key: "_isDisabled",
          value: function _isDisabled() {
            return this._sort.disabled || this.disabled;
          }
          /**
           * Gets the aria-sort attribute that should be applied to this sort header. If this header
           * is not sorted, returns null so that the attribute is removed from the host element. Aria spec
           * says that the aria-sort property should only be present on one header at a time, so removing
           * ensures this is true.
           */

        }, {
          key: "_getAriaSortAttribute",
          value: function _getAriaSortAttribute() {
            if (!this._isSorted()) {
              return 'none';
            }

            return this._sort.direction == 'asc' ? 'ascending' : 'descending';
          }
          /** Whether the arrow inside the sort header should be rendered. */

        }, {
          key: "_renderArrow",
          value: function _renderArrow() {
            return !this._isDisabled() || this._isSorted();
          }
        }, {
          key: "disableClear",
          get: function get() {
            return this._disableClear;
          },
          set: function set(v) {
            this._disableClear = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_1__["coerceBooleanProperty"])(v);
          }
        }]);

        return MatSortHeader;
      }(_MatSortHeaderMixinBase);

      MatSortHeader.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"],
        args: [{
          selector: '[mat-sort-header]',
          exportAs: 'matSortHeader',
          template: "<!--\n  We set the `tabindex` on an element inside the table header, rather than the header itself,\n  because of a bug in NVDA where having a `tabindex` on a `th` breaks keyboard navigation in the\n  table (see https://github.com/nvaccess/nvda/issues/7718). This allows for the header to both\n  be focusable, and have screen readers read out its `aria-sort` state. We prefer this approach\n  over having a button with an `aria-label` inside the header, because the button's `aria-label`\n  will be read out as the user is navigating the table's cell (see #13012).\n\n  The approach is based off of: https://dequeuniversity.com/library/aria/tables/sf-sortable-grid\n-->\n<div class=\"mat-sort-header-container mat-focus-indicator\"\n     [class.mat-sort-header-sorted]=\"_isSorted()\"\n     [class.mat-sort-header-position-before]=\"arrowPosition == 'before'\"\n     [attr.tabindex]=\"_isDisabled() ? null : 0\"\n     role=\"button\">\n\n  <!--\n    TODO(crisbeto): this div isn't strictly necessary, but we have to keep it due to a large\n    number of screenshot diff failures. It should be removed eventually. Note that the difference\n    isn't visible with a shorter header, but once it breaks up into multiple lines, this element\n    causes it to be center-aligned, whereas removing it will keep the text to the left.\n  -->\n  <div class=\"mat-sort-header-content\">\n    <ng-content></ng-content>\n  </div>\n\n  <!-- Disable animations while a current animation is running -->\n  <div class=\"mat-sort-header-arrow\"\n       *ngIf=\"_renderArrow()\"\n       [@arrowOpacity]=\"_getArrowViewState()\"\n       [@arrowPosition]=\"_getArrowViewState()\"\n       [@allowChildren]=\"_getArrowDirectionState()\"\n       (@arrowPosition.start)=\"_disableViewStateAnimation = true\"\n       (@arrowPosition.done)=\"_disableViewStateAnimation = false\">\n    <div class=\"mat-sort-header-stem\"></div>\n    <div class=\"mat-sort-header-indicator\" [@indicator]=\"_getArrowDirectionState()\">\n      <div class=\"mat-sort-header-pointer-left\" [@leftPointer]=\"_getArrowDirectionState()\"></div>\n      <div class=\"mat-sort-header-pointer-right\" [@rightPointer]=\"_getArrowDirectionState()\"></div>\n      <div class=\"mat-sort-header-pointer-middle\"></div>\n    </div>\n  </div>\n</div>\n",
          host: {
            'class': 'mat-sort-header',
            '(click)': '_handleClick()',
            '(keydown)': '_handleKeydown($event)',
            '(mouseenter)': '_setIndicatorHintVisible(true)',
            '(mouseleave)': '_setIndicatorHintVisible(false)',
            '[attr.aria-sort]': '_getAriaSortAttribute()',
            '[class.mat-sort-header-disabled]': '_isDisabled()'
          },
          encapsulation: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ViewEncapsulation"].None,
          changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ChangeDetectionStrategy"].OnPush,
          inputs: ['disabled'],
          animations: [matSortAnimations.indicator, matSortAnimations.leftPointer, matSortAnimations.rightPointer, matSortAnimations.arrowOpacity, matSortAnimations.arrowPosition, matSortAnimations.allowChildren],
          styles: [".mat-sort-header-container{display:flex;cursor:pointer;align-items:center;letter-spacing:normal;outline:0}[mat-sort-header].cdk-keyboard-focused .mat-sort-header-container,[mat-sort-header].cdk-program-focused .mat-sort-header-container{border-bottom:solid 1px currentColor}.mat-sort-header-disabled .mat-sort-header-container{cursor:default}.mat-sort-header-content{text-align:center;display:flex;align-items:center}.mat-sort-header-position-before{flex-direction:row-reverse}.mat-sort-header-arrow{height:12px;width:12px;min-width:12px;position:relative;display:flex;opacity:0}.mat-sort-header-arrow,[dir=rtl] .mat-sort-header-position-before .mat-sort-header-arrow{margin:0 0 0 6px}.mat-sort-header-position-before .mat-sort-header-arrow,[dir=rtl] .mat-sort-header-arrow{margin:0 6px 0 0}.mat-sort-header-stem{background:currentColor;height:10px;width:2px;margin:auto;display:flex;align-items:center}.cdk-high-contrast-active .mat-sort-header-stem{width:0;border-left:solid 2px}.mat-sort-header-indicator{width:100%;height:2px;display:flex;align-items:center;position:absolute;top:0;left:0}.mat-sort-header-pointer-middle{margin:auto;height:2px;width:2px;background:currentColor;transform:rotate(45deg)}.cdk-high-contrast-active .mat-sort-header-pointer-middle{width:0;height:0;border-top:solid 2px;border-left:solid 2px}.mat-sort-header-pointer-left,.mat-sort-header-pointer-right{background:currentColor;width:6px;height:2px;position:absolute;top:0}.cdk-high-contrast-active .mat-sort-header-pointer-left,.cdk-high-contrast-active .mat-sort-header-pointer-right{width:0;height:0;border-left:solid 6px;border-top:solid 2px}.mat-sort-header-pointer-left{transform-origin:right;left:0}.mat-sort-header-pointer-right{transform-origin:left;right:0}\n"]
        }]
      }];

      MatSortHeader.ctorParameters = function () {
        return [{
          type: MatSortHeaderIntl
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ChangeDetectorRef"]
        }, {
          type: MatSort,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Optional"]
          }]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Inject"],
            args: ['MAT_SORT_HEADER_COLUMN_DEF']
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Optional"]
          }]
        }, {
          type: _angular_cdk_a11y__WEBPACK_IMPORTED_MODULE_3__["FocusMonitor"]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ElementRef"]
        }];
      };

      MatSortHeader.propDecorators = {
        id: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['mat-sort-header']
        }],
        arrowPosition: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"]
        }],
        start: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"]
        }],
        disableClear: [{
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

      var MatSortModule = function MatSortModule() {
        _classCallCheck(this, MatSortModule);
      };

      MatSortModule.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"],
        args: [{
          imports: [_angular_common__WEBPACK_IMPORTED_MODULE_7__["CommonModule"], _angular_material_core__WEBPACK_IMPORTED_MODULE_2__["MatCommonModule"]],
          exports: [MatSort, MatSortHeader],
          declarations: [MatSort, MatSortHeader],
          providers: [MAT_SORT_HEADER_INTL_PROVIDER]
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
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * Generated bundle index. Do not edit.
       */
      //# sourceMappingURL=sort.js.map

      /***/
    },

    /***/
    "OaSA":
    /*!**********************************************************!*\
      !*** ./node_modules/@angular/material/fesm2015/table.js ***!
      \**********************************************************/

    /*! exports provided: MatCell, MatCellDef, MatColumnDef, MatFooterCell, MatFooterCellDef, MatFooterRow, MatFooterRowDef, MatHeaderCell, MatHeaderCellDef, MatHeaderRow, MatHeaderRowDef, MatNoDataRow, MatRow, MatRowDef, MatTable, MatTableDataSource, MatTableModule, MatTextColumn */

    /***/
    function OaSA(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatCell", function () {
        return MatCell;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatCellDef", function () {
        return MatCellDef;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatColumnDef", function () {
        return MatColumnDef;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatFooterCell", function () {
        return MatFooterCell;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatFooterCellDef", function () {
        return MatFooterCellDef;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatFooterRow", function () {
        return MatFooterRow;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatFooterRowDef", function () {
        return MatFooterRowDef;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatHeaderCell", function () {
        return MatHeaderCell;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatHeaderCellDef", function () {
        return MatHeaderCellDef;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatHeaderRow", function () {
        return MatHeaderRow;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatHeaderRowDef", function () {
        return MatHeaderRowDef;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatNoDataRow", function () {
        return MatNoDataRow;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatRow", function () {
        return MatRow;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatRowDef", function () {
        return MatRowDef;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatTable", function () {
        return MatTable;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatTableDataSource", function () {
        return MatTableDataSource;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatTableModule", function () {
        return MatTableModule;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatTextColumn", function () {
        return MatTextColumn;
      });
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! @angular/cdk/table */
      "GXRp");
      /* harmony import */


      var _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @angular/cdk/collections */
      "CtHx");
      /* harmony import */


      var _angular_material_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/material/core */
      "UhP/");
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
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * Wrapper for the CdkTable with Material design styles.
       */


      var MatTable = /*#__PURE__*/function (_angular_cdk_table__W) {
        _inherits(MatTable, _angular_cdk_table__W);

        var _super16 = _createSuper(MatTable);

        function MatTable() {
          var _this27;

          _classCallCheck(this, MatTable);

          _this27 = _super16.apply(this, arguments);
          /** Overrides the sticky CSS class set by the `CdkTable`. */

          _this27.stickyCssClass = 'mat-table-sticky';
          /** Overrides the need to add position: sticky on every sticky cell element in `CdkTable`. */

          _this27.needsPositionStickyOnElement = false;
          return _this27;
        }

        return MatTable;
      }(_angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkTable"]);

      MatTable.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"],
        args: [{
          selector: 'mat-table, table[mat-table]',
          exportAs: 'matTable',
          template: _angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CDK_TABLE_TEMPLATE"],
          host: {
            'class': 'mat-table',
            '[class.mat-table-fixed-layout]': 'fixedLayout'
          },
          providers: [// TODO(michaeljamesparsons) Abstract the view repeater strategy to a directive API so this code
          //  is only included in the build if used.
          {
            provide: _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_2__["_VIEW_REPEATER_STRATEGY"],
            useClass: _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_2__["_DisposeViewRepeaterStrategy"]
          }, {
            provide: _angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkTable"],
            useExisting: MatTable
          }, {
            provide: _angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CDK_TABLE"],
            useExisting: MatTable
          }, {
            provide: _angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["_COALESCED_STYLE_SCHEDULER"],
            useClass: _angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["_CoalescedStyleScheduler"]
          }],
          encapsulation: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ViewEncapsulation"].None,
          // See note on CdkTable for explanation on why this uses the default change detection strategy.
          // tslint:disable-next-line:validate-decorators
          changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ChangeDetectionStrategy"].Default,
          styles: ["mat-table{display:block}mat-header-row{min-height:56px}mat-row,mat-footer-row{min-height:48px}mat-row,mat-header-row,mat-footer-row{display:flex;border-width:0;border-bottom-width:1px;border-style:solid;align-items:center;box-sizing:border-box}mat-row::after,mat-header-row::after,mat-footer-row::after{display:inline-block;min-height:inherit;content:\"\"}mat-cell:first-of-type,mat-header-cell:first-of-type,mat-footer-cell:first-of-type{padding-left:24px}[dir=rtl] mat-cell:first-of-type:not(:only-of-type),[dir=rtl] mat-header-cell:first-of-type:not(:only-of-type),[dir=rtl] mat-footer-cell:first-of-type:not(:only-of-type){padding-left:0;padding-right:24px}mat-cell:last-of-type,mat-header-cell:last-of-type,mat-footer-cell:last-of-type{padding-right:24px}[dir=rtl] mat-cell:last-of-type:not(:only-of-type),[dir=rtl] mat-header-cell:last-of-type:not(:only-of-type),[dir=rtl] mat-footer-cell:last-of-type:not(:only-of-type){padding-right:0;padding-left:24px}mat-cell,mat-header-cell,mat-footer-cell{flex:1;display:flex;align-items:center;overflow:hidden;word-wrap:break-word;min-height:inherit}table.mat-table{border-spacing:0}tr.mat-header-row{height:56px}tr.mat-row,tr.mat-footer-row{height:48px}th.mat-header-cell{text-align:left}[dir=rtl] th.mat-header-cell{text-align:right}th.mat-header-cell,td.mat-cell,td.mat-footer-cell{padding:0;border-bottom-width:1px;border-bottom-style:solid}th.mat-header-cell:first-of-type,td.mat-cell:first-of-type,td.mat-footer-cell:first-of-type{padding-left:24px}[dir=rtl] th.mat-header-cell:first-of-type:not(:only-of-type),[dir=rtl] td.mat-cell:first-of-type:not(:only-of-type),[dir=rtl] td.mat-footer-cell:first-of-type:not(:only-of-type){padding-left:0;padding-right:24px}th.mat-header-cell:last-of-type,td.mat-cell:last-of-type,td.mat-footer-cell:last-of-type{padding-right:24px}[dir=rtl] th.mat-header-cell:last-of-type:not(:only-of-type),[dir=rtl] td.mat-cell:last-of-type:not(:only-of-type),[dir=rtl] td.mat-footer-cell:last-of-type:not(:only-of-type){padding-right:0;padding-left:24px}.mat-table-sticky{position:-webkit-sticky !important;position:sticky !important}.mat-table-fixed-layout{table-layout:fixed}\n"]
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
       * Cell definition for the mat-table.
       * Captures the template of a column's data row cell as well as cell-specific properties.
       */

      var MatCellDef = /*#__PURE__*/function (_angular_cdk_table__W2) {
        _inherits(MatCellDef, _angular_cdk_table__W2);

        var _super17 = _createSuper(MatCellDef);

        function MatCellDef() {
          _classCallCheck(this, MatCellDef);

          return _super17.apply(this, arguments);
        }

        return MatCellDef;
      }(_angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkCellDef"]);

      MatCellDef.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"],
        args: [{
          selector: '[matCellDef]',
          providers: [{
            provide: _angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkCellDef"],
            useExisting: MatCellDef
          }]
        }]
      }];
      /**
       * Header cell definition for the mat-table.
       * Captures the template of a column's header cell and as well as cell-specific properties.
       */

      var MatHeaderCellDef = /*#__PURE__*/function (_angular_cdk_table__W3) {
        _inherits(MatHeaderCellDef, _angular_cdk_table__W3);

        var _super18 = _createSuper(MatHeaderCellDef);

        function MatHeaderCellDef() {
          _classCallCheck(this, MatHeaderCellDef);

          return _super18.apply(this, arguments);
        }

        return MatHeaderCellDef;
      }(_angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkHeaderCellDef"]);

      MatHeaderCellDef.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"],
        args: [{
          selector: '[matHeaderCellDef]',
          providers: [{
            provide: _angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkHeaderCellDef"],
            useExisting: MatHeaderCellDef
          }]
        }]
      }];
      /**
       * Footer cell definition for the mat-table.
       * Captures the template of a column's footer cell and as well as cell-specific properties.
       */

      var MatFooterCellDef = /*#__PURE__*/function (_angular_cdk_table__W4) {
        _inherits(MatFooterCellDef, _angular_cdk_table__W4);

        var _super19 = _createSuper(MatFooterCellDef);

        function MatFooterCellDef() {
          _classCallCheck(this, MatFooterCellDef);

          return _super19.apply(this, arguments);
        }

        return MatFooterCellDef;
      }(_angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkFooterCellDef"]);

      MatFooterCellDef.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"],
        args: [{
          selector: '[matFooterCellDef]',
          providers: [{
            provide: _angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkFooterCellDef"],
            useExisting: MatFooterCellDef
          }]
        }]
      }];
      /**
       * Column definition for the mat-table.
       * Defines a set of cells available for a table column.
       */

      var MatColumnDef = /*#__PURE__*/function (_angular_cdk_table__W5) {
        _inherits(MatColumnDef, _angular_cdk_table__W5);

        var _super20 = _createSuper(MatColumnDef);

        function MatColumnDef() {
          _classCallCheck(this, MatColumnDef);

          return _super20.apply(this, arguments);
        }

        _createClass(MatColumnDef, [{
          key: "_updateColumnCssClassName",

          /**
           * Add "mat-column-" prefix in addition to "cdk-column-" prefix.
           * In the future, this will only add "mat-column-" and columnCssClassName
           * will change from type string[] to string.
           * @docs-private
           */
          value: function _updateColumnCssClassName() {
            _get(_getPrototypeOf(MatColumnDef.prototype), "_updateColumnCssClassName", this).call(this);

            this._columnCssClassName.push("mat-column-".concat(this.cssClassFriendlyName));
          }
        }, {
          key: "name",

          /** Unique name for this column. */
          get: function get() {
            return this._name;
          },
          set: function set(name) {
            this._setNameInput(name);
          }
        }]);

        return MatColumnDef;
      }(_angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkColumnDef"]);

      MatColumnDef.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"],
        args: [{
          selector: '[matColumnDef]',
          inputs: ['sticky'],
          providers: [{
            provide: _angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkColumnDef"],
            useExisting: MatColumnDef
          }, {
            provide: 'MAT_SORT_HEADER_COLUMN_DEF',
            useExisting: MatColumnDef
          }]
        }]
      }];
      MatColumnDef.propDecorators = {
        name: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"],
          args: ['matColumnDef']
        }]
      };
      /** Header cell template container that adds the right classes and role. */

      var MatHeaderCell = /*#__PURE__*/function (_angular_cdk_table__W6) {
        _inherits(MatHeaderCell, _angular_cdk_table__W6);

        var _super21 = _createSuper(MatHeaderCell);

        function MatHeaderCell() {
          _classCallCheck(this, MatHeaderCell);

          return _super21.apply(this, arguments);
        }

        return MatHeaderCell;
      }(_angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkHeaderCell"]);

      MatHeaderCell.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"],
        args: [{
          selector: 'mat-header-cell, th[mat-header-cell]',
          host: {
            'class': 'mat-header-cell',
            'role': 'columnheader'
          }
        }]
      }];
      /** Footer cell template container that adds the right classes and role. */

      var MatFooterCell = /*#__PURE__*/function (_angular_cdk_table__W7) {
        _inherits(MatFooterCell, _angular_cdk_table__W7);

        var _super22 = _createSuper(MatFooterCell);

        function MatFooterCell() {
          _classCallCheck(this, MatFooterCell);

          return _super22.apply(this, arguments);
        }

        return MatFooterCell;
      }(_angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkFooterCell"]);

      MatFooterCell.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"],
        args: [{
          selector: 'mat-footer-cell, td[mat-footer-cell]',
          host: {
            'class': 'mat-footer-cell',
            'role': 'gridcell'
          }
        }]
      }];
      /** Cell template container that adds the right classes and role. */

      var MatCell = /*#__PURE__*/function (_angular_cdk_table__W8) {
        _inherits(MatCell, _angular_cdk_table__W8);

        var _super23 = _createSuper(MatCell);

        function MatCell() {
          _classCallCheck(this, MatCell);

          return _super23.apply(this, arguments);
        }

        return MatCell;
      }(_angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkCell"]);

      MatCell.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"],
        args: [{
          selector: 'mat-cell, td[mat-cell]',
          host: {
            'class': 'mat-cell',
            'role': 'gridcell'
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
       * Header row definition for the mat-table.
       * Captures the header row's template and other header properties such as the columns to display.
       */

      var MatHeaderRowDef = /*#__PURE__*/function (_angular_cdk_table__W9) {
        _inherits(MatHeaderRowDef, _angular_cdk_table__W9);

        var _super24 = _createSuper(MatHeaderRowDef);

        function MatHeaderRowDef() {
          _classCallCheck(this, MatHeaderRowDef);

          return _super24.apply(this, arguments);
        }

        return MatHeaderRowDef;
      }(_angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkHeaderRowDef"]);

      MatHeaderRowDef.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"],
        args: [{
          selector: '[matHeaderRowDef]',
          providers: [{
            provide: _angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkHeaderRowDef"],
            useExisting: MatHeaderRowDef
          }],
          inputs: ['columns: matHeaderRowDef', 'sticky: matHeaderRowDefSticky']
        }]
      }];
      /**
       * Footer row definition for the mat-table.
       * Captures the footer row's template and other footer properties such as the columns to display.
       */

      var MatFooterRowDef = /*#__PURE__*/function (_angular_cdk_table__W10) {
        _inherits(MatFooterRowDef, _angular_cdk_table__W10);

        var _super25 = _createSuper(MatFooterRowDef);

        function MatFooterRowDef() {
          _classCallCheck(this, MatFooterRowDef);

          return _super25.apply(this, arguments);
        }

        return MatFooterRowDef;
      }(_angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkFooterRowDef"]);

      MatFooterRowDef.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"],
        args: [{
          selector: '[matFooterRowDef]',
          providers: [{
            provide: _angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkFooterRowDef"],
            useExisting: MatFooterRowDef
          }],
          inputs: ['columns: matFooterRowDef', 'sticky: matFooterRowDefSticky']
        }]
      }];
      /**
       * Data row definition for the mat-table.
       * Captures the data row's template and other properties such as the columns to display and
       * a when predicate that describes when this row should be used.
       */

      var MatRowDef = /*#__PURE__*/function (_angular_cdk_table__W11) {
        _inherits(MatRowDef, _angular_cdk_table__W11);

        var _super26 = _createSuper(MatRowDef);

        function MatRowDef() {
          _classCallCheck(this, MatRowDef);

          return _super26.apply(this, arguments);
        }

        return MatRowDef;
      }(_angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkRowDef"]);

      MatRowDef.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"],
        args: [{
          selector: '[matRowDef]',
          providers: [{
            provide: _angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkRowDef"],
            useExisting: MatRowDef
          }],
          inputs: ['columns: matRowDefColumns', 'when: matRowDefWhen']
        }]
      }];
      /** Header template container that contains the cell outlet. Adds the right class and role. */

      var MatHeaderRow = /*#__PURE__*/function (_angular_cdk_table__W12) {
        _inherits(MatHeaderRow, _angular_cdk_table__W12);

        var _super27 = _createSuper(MatHeaderRow);

        function MatHeaderRow() {
          _classCallCheck(this, MatHeaderRow);

          return _super27.apply(this, arguments);
        }

        return MatHeaderRow;
      }(_angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkHeaderRow"]);

      MatHeaderRow.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"],
        args: [{
          selector: 'mat-header-row, tr[mat-header-row]',
          template: _angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CDK_ROW_TEMPLATE"],
          host: {
            'class': 'mat-header-row',
            'role': 'row'
          },
          // See note on CdkTable for explanation on why this uses the default change detection strategy.
          // tslint:disable-next-line:validate-decorators
          changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ChangeDetectionStrategy"].Default,
          encapsulation: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ViewEncapsulation"].None,
          exportAs: 'matHeaderRow',
          providers: [{
            provide: _angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkHeaderRow"],
            useExisting: MatHeaderRow
          }]
        }]
      }];
      /** Footer template container that contains the cell outlet. Adds the right class and role. */

      var MatFooterRow = /*#__PURE__*/function (_angular_cdk_table__W13) {
        _inherits(MatFooterRow, _angular_cdk_table__W13);

        var _super28 = _createSuper(MatFooterRow);

        function MatFooterRow() {
          _classCallCheck(this, MatFooterRow);

          return _super28.apply(this, arguments);
        }

        return MatFooterRow;
      }(_angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkFooterRow"]);

      MatFooterRow.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"],
        args: [{
          selector: 'mat-footer-row, tr[mat-footer-row]',
          template: _angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CDK_ROW_TEMPLATE"],
          host: {
            'class': 'mat-footer-row',
            'role': 'row'
          },
          // See note on CdkTable for explanation on why this uses the default change detection strategy.
          // tslint:disable-next-line:validate-decorators
          changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ChangeDetectionStrategy"].Default,
          encapsulation: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ViewEncapsulation"].None,
          exportAs: 'matFooterRow',
          providers: [{
            provide: _angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkFooterRow"],
            useExisting: MatFooterRow
          }]
        }]
      }];
      /** Data row template container that contains the cell outlet. Adds the right class and role. */

      var MatRow = /*#__PURE__*/function (_angular_cdk_table__W14) {
        _inherits(MatRow, _angular_cdk_table__W14);

        var _super29 = _createSuper(MatRow);

        function MatRow() {
          _classCallCheck(this, MatRow);

          return _super29.apply(this, arguments);
        }

        return MatRow;
      }(_angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkRow"]);

      MatRow.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"],
        args: [{
          selector: 'mat-row, tr[mat-row]',
          template: _angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CDK_ROW_TEMPLATE"],
          host: {
            'class': 'mat-row',
            'role': 'row'
          },
          // See note on CdkTable for explanation on why this uses the default change detection strategy.
          // tslint:disable-next-line:validate-decorators
          changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ChangeDetectionStrategy"].Default,
          encapsulation: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ViewEncapsulation"].None,
          exportAs: 'matRow',
          providers: [{
            provide: _angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkRow"],
            useExisting: MatRow
          }]
        }]
      }];
      /** Row that can be used to display a message when no data is shown in the table. */

      var MatNoDataRow = /*#__PURE__*/function (_angular_cdk_table__W15) {
        _inherits(MatNoDataRow, _angular_cdk_table__W15);

        var _super30 = _createSuper(MatNoDataRow);

        function MatNoDataRow() {
          _classCallCheck(this, MatNoDataRow);

          return _super30.apply(this, arguments);
        }

        return MatNoDataRow;
      }(_angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkNoDataRow"]);

      MatNoDataRow.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"],
        args: [{
          selector: 'ng-template[matNoDataRow]',
          providers: [{
            provide: _angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkNoDataRow"],
            useExisting: MatNoDataRow
          }]
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
       * Column that simply shows text content for the header and row cells. Assumes that the table
       * is using the native table implementation (`<table>`).
       *
       * By default, the name of this column will be the header text and data property accessor.
       * The header text can be overridden with the `headerText` input. Cell values can be overridden with
       * the `dataAccessor` input. Change the text justification to the start or end using the `justify`
       * input.
       */

      var MatTextColumn = /*#__PURE__*/function (_angular_cdk_table__W16) {
        _inherits(MatTextColumn, _angular_cdk_table__W16);

        var _super31 = _createSuper(MatTextColumn);

        function MatTextColumn() {
          _classCallCheck(this, MatTextColumn);

          return _super31.apply(this, arguments);
        }

        return MatTextColumn;
      }(_angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkTextColumn"]);

      MatTextColumn.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"],
        args: [{
          selector: 'mat-text-column',
          template: "\n    <ng-container matColumnDef>\n      <th mat-header-cell *matHeaderCellDef [style.text-align]=\"justify\">\n        {{headerText}}\n      </th>\n      <td mat-cell *matCellDef=\"let data\" [style.text-align]=\"justify\">\n        {{dataAccessor(data, name)}}\n      </td>\n    </ng-container>\n  ",
          encapsulation: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ViewEncapsulation"].None,
          // Change detection is intentionally not set to OnPush. This component's template will be provided
          // to the table to be inserted into its view. This is problematic when change detection runs since
          // the bindings in this template will be evaluated _after_ the table's view is evaluated, which
          // mean's the template in the table's view will not have the updated value (and in fact will cause
          // an ExpressionChangedAfterItHasBeenCheckedError).
          // tslint:disable-next-line:validate-decorators
          changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ChangeDetectionStrategy"].Default
        }]
      }];
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      var EXPORTED_DECLARATIONS = [// Table
      MatTable, // Template defs
      MatHeaderCellDef, MatHeaderRowDef, MatColumnDef, MatCellDef, MatRowDef, MatFooterCellDef, MatFooterRowDef, // Cell directives
      MatHeaderCell, MatCell, MatFooterCell, // Row directives
      MatHeaderRow, MatRow, MatFooterRow, MatNoDataRow, MatTextColumn];

      var MatTableModule = function MatTableModule() {
        _classCallCheck(this, MatTableModule);
      };

      MatTableModule.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"],
        args: [{
          imports: [_angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["CdkTableModule"], _angular_material_core__WEBPACK_IMPORTED_MODULE_3__["MatCommonModule"]],
          exports: [_angular_material_core__WEBPACK_IMPORTED_MODULE_3__["MatCommonModule"], EXPORTED_DECLARATIONS],
          declarations: EXPORTED_DECLARATIONS
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
       * Corresponds to `Number.MAX_SAFE_INTEGER`. Moved out into a variable here due to
       * flaky browser support and the value not being defined in Closure's typings.
       */

      var MAX_SAFE_INTEGER = 9007199254740991;
      /**
       * Data source that accepts a client-side data array and includes native support of filtering,
       * sorting (using MatSort), and pagination (using MatPaginator).
       *
       * Allows for sort customization by overriding sortingDataAccessor, which defines how data
       * properties are accessed. Also allows for filter customization by overriding filterTermAccessor,
       * which defines how row data is converted to a string for filter matching.
       *
       * **Note:** This class is meant to be a simple data source to help you get started. As such
       * it isn't equipped to handle some more advanced cases like robust i18n support or server-side
       * interactions. If your app needs to support more advanced use cases, consider implementing your
       * own `DataSource`.
       */

      var MatTableDataSource = /*#__PURE__*/function (_angular_cdk_table__W17) {
        _inherits(MatTableDataSource, _angular_cdk_table__W17);

        var _super32 = _createSuper(MatTableDataSource);

        function MatTableDataSource() {
          var _this28;

          var initialData = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : [];

          _classCallCheck(this, MatTableDataSource);

          _this28 = _super32.call(this);
          /** Stream emitting render data to the table (depends on ordered data changes). */

          _this28._renderData = new rxjs__WEBPACK_IMPORTED_MODULE_5__["BehaviorSubject"]([]);
          /** Stream that emits when a new filter string is set on the data source. */

          _this28._filter = new rxjs__WEBPACK_IMPORTED_MODULE_5__["BehaviorSubject"]('');
          /** Used to react to internal changes of the paginator that are made by the data source itself. */

          _this28._internalPageChanges = new rxjs__WEBPACK_IMPORTED_MODULE_5__["Subject"]();
          /**
           * Subscription to the changes that should trigger an update to the table's rendered rows, such
           * as filtering, sorting, pagination, or base data changes.
           */

          _this28._renderChangesSubscription = rxjs__WEBPACK_IMPORTED_MODULE_5__["Subscription"].EMPTY;
          /**
           * Data accessor function that is used for accessing data properties for sorting through
           * the default sortData function.
           * This default function assumes that the sort header IDs (which defaults to the column name)
           * matches the data's properties (e.g. column Xyz represents data['Xyz']).
           * May be set to a custom function for different behavior.
           * @param data Data object that is being accessed.
           * @param sortHeaderId The name of the column that represents the data.
           */

          _this28.sortingDataAccessor = function (data, sortHeaderId) {
            var value = data[sortHeaderId];

            if (Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_4__["_isNumberValue"])(value)) {
              var numberValue = Number(value); // Numbers beyond `MAX_SAFE_INTEGER` can't be compared reliably so we
              // leave them as strings. For more info: https://goo.gl/y5vbSg

              return numberValue < MAX_SAFE_INTEGER ? numberValue : value;
            }

            return value;
          };
          /**
           * Gets a sorted copy of the data array based on the state of the MatSort. Called
           * after changes are made to the filtered data or when sort changes are emitted from MatSort.
           * By default, the function retrieves the active sort and its direction and compares data
           * by retrieving data using the sortingDataAccessor. May be overridden for a custom implementation
           * of data ordering.
           * @param data The array of data that should be sorted.
           * @param sort The connected MatSort that holds the current sort state.
           */


          _this28.sortData = function (data, sort) {
            var active = sort.active;
            var direction = sort.direction;

            if (!active || direction == '') {
              return data;
            }

            return data.sort(function (a, b) {
              var valueA = _this28.sortingDataAccessor(a, active);

              var valueB = _this28.sortingDataAccessor(b, active); // If there are data in the column that can be converted to a number,
              // it must be ensured that the rest of the data
              // is of the same type so as not to order incorrectly.


              var valueAType = typeof valueA;
              var valueBType = typeof valueB;

              if (valueAType !== valueBType) {
                if (valueAType === 'number') {
                  valueA += '';
                }

                if (valueBType === 'number') {
                  valueB += '';
                }
              } // If both valueA and valueB exist (truthy), then compare the two. Otherwise, check if
              // one value exists while the other doesn't. In this case, existing value should come last.
              // This avoids inconsistent results when comparing values to undefined/null.
              // If neither value exists, return 0 (equal).


              var comparatorResult = 0;

              if (valueA != null && valueB != null) {
                // Check if one value is greater than the other; if equal, comparatorResult should remain 0.
                if (valueA > valueB) {
                  comparatorResult = 1;
                } else if (valueA < valueB) {
                  comparatorResult = -1;
                }
              } else if (valueA != null) {
                comparatorResult = 1;
              } else if (valueB != null) {
                comparatorResult = -1;
              }

              return comparatorResult * (direction == 'asc' ? 1 : -1);
            });
          };
          /**
           * Checks if a data object matches the data source's filter string. By default, each data object
           * is converted to a string of its properties and returns true if the filter has
           * at least one occurrence in that string. By default, the filter string has its whitespace
           * trimmed and the match is case-insensitive. May be overridden for a custom implementation of
           * filter matching.
           * @param data Data object used to check against the filter.
           * @param filter Filter string that has been set on the data source.
           * @returns Whether the filter matches against the data
           */


          _this28.filterPredicate = function (data, filter) {
            // Transform the data into a lowercase string of all property values.
            var dataStr = Object.keys(data).reduce(function (currentTerm, key) {
              // Use an obscure Unicode character to delimit the words in the concatenated string.
              // This avoids matches where the values of two columns combined will match the user's query
              // (e.g. `Flute` and `Stop` will match `Test`). The character is intended to be something
              // that has a very low chance of being typed in by somebody in a text field. This one in
              // particular is "White up-pointing triangle with dot" from
              // https://en.wikipedia.org/wiki/List_of_Unicode_characters
              return currentTerm + data[key] + '◬';
            }, '').toLowerCase(); // Transform the filter by converting it to lowercase and removing whitespace.

            var transformedFilter = filter.trim().toLowerCase();
            return dataStr.indexOf(transformedFilter) != -1;
          };

          _this28._data = new rxjs__WEBPACK_IMPORTED_MODULE_5__["BehaviorSubject"](initialData);

          _this28._updateChangeSubscription();

          return _this28;
        }
        /** Array of data that should be rendered by the table, where each object represents one row. */


        _createClass(MatTableDataSource, [{
          key: "_updateChangeSubscription",

          /**
           * Subscribe to changes that should trigger an update to the table's rendered rows. When the
           * changes occur, process the current state of the filter, sort, and pagination along with
           * the provided base data and send it to the table for rendering.
           */
          value: function _updateChangeSubscription() {
            var _this29 = this;

            // Sorting and/or pagination should be watched if MatSort and/or MatPaginator are provided.
            // The events should emit whenever the component emits a change or initializes, or if no
            // component is provided, a stream with just a null event should be provided.
            // The `sortChange` and `pageChange` acts as a signal to the combineLatests below so that the
            // pipeline can progress to the next step. Note that the value from these streams are not used,
            // they purely act as a signal to progress in the pipeline.
            var sortChange = this._sort ? Object(rxjs__WEBPACK_IMPORTED_MODULE_5__["merge"])(this._sort.sortChange, this._sort.initialized) : Object(rxjs__WEBPACK_IMPORTED_MODULE_5__["of"])(null);
            var pageChange = this._paginator ? Object(rxjs__WEBPACK_IMPORTED_MODULE_5__["merge"])(this._paginator.page, this._internalPageChanges, this._paginator.initialized) : Object(rxjs__WEBPACK_IMPORTED_MODULE_5__["of"])(null);
            var dataStream = this._data; // Watch for base data or filter changes to provide a filtered set of data.

            var filteredData = Object(rxjs__WEBPACK_IMPORTED_MODULE_5__["combineLatest"])([dataStream, this._filter]).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["map"])(function (_ref) {
              var _ref2 = _slicedToArray(_ref, 1),
                  data = _ref2[0];

              return _this29._filterData(data);
            })); // Watch for filtered data or sort changes to provide an ordered set of data.

            var orderedData = Object(rxjs__WEBPACK_IMPORTED_MODULE_5__["combineLatest"])([filteredData, sortChange]).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["map"])(function (_ref3) {
              var _ref4 = _slicedToArray(_ref3, 1),
                  data = _ref4[0];

              return _this29._orderData(data);
            })); // Watch for ordered data or page changes to provide a paged set of data.

            var paginatedData = Object(rxjs__WEBPACK_IMPORTED_MODULE_5__["combineLatest"])([orderedData, pageChange]).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["map"])(function (_ref5) {
              var _ref6 = _slicedToArray(_ref5, 1),
                  data = _ref6[0];

              return _this29._pageData(data);
            })); // Watched for paged data changes and send the result to the table to render.

            this._renderChangesSubscription.unsubscribe();

            this._renderChangesSubscription = paginatedData.subscribe(function (data) {
              return _this29._renderData.next(data);
            });
          }
          /**
           * Returns a filtered data array where each filter object contains the filter string within
           * the result of the filterTermAccessor function. If no filter is set, returns the data array
           * as provided.
           */

        }, {
          key: "_filterData",
          value: function _filterData(data) {
            var _this30 = this;

            // If there is a filter string, filter out data that does not contain it.
            // Each data object is converted to a string using the function defined by filterTermAccessor.
            // May be overridden for customization.
            this.filteredData = this.filter == null || this.filter === '' ? data : data.filter(function (obj) {
              return _this30.filterPredicate(obj, _this30.filter);
            });

            if (this.paginator) {
              this._updatePaginator(this.filteredData.length);
            }

            return this.filteredData;
          }
          /**
           * Returns a sorted copy of the data if MatSort has a sort applied, otherwise just returns the
           * data array as provided. Uses the default data accessor for data lookup, unless a
           * sortDataAccessor function is defined.
           */

        }, {
          key: "_orderData",
          value: function _orderData(data) {
            // If there is no active sort or direction, return the data without trying to sort.
            if (!this.sort) {
              return data;
            }

            return this.sortData(data.slice(), this.sort);
          }
          /**
           * Returns a paged slice of the provided data array according to the provided MatPaginator's page
           * index and length. If there is no paginator provided, returns the data array as provided.
           */

        }, {
          key: "_pageData",
          value: function _pageData(data) {
            if (!this.paginator) {
              return data;
            }

            var startIndex = this.paginator.pageIndex * this.paginator.pageSize;
            return data.slice(startIndex, startIndex + this.paginator.pageSize);
          }
          /**
           * Updates the paginator to reflect the length of the filtered data, and makes sure that the page
           * index does not exceed the paginator's last page. Values are changed in a resolved promise to
           * guard against making property changes within a round of change detection.
           */

        }, {
          key: "_updatePaginator",
          value: function _updatePaginator(filteredDataLength) {
            var _this31 = this;

            Promise.resolve().then(function () {
              var paginator = _this31.paginator;

              if (!paginator) {
                return;
              }

              paginator.length = filteredDataLength; // If the page index is set beyond the page, reduce it to the last page.

              if (paginator.pageIndex > 0) {
                var lastPageIndex = Math.ceil(paginator.length / paginator.pageSize) - 1 || 0;
                var newPageIndex = Math.min(paginator.pageIndex, lastPageIndex);

                if (newPageIndex !== paginator.pageIndex) {
                  paginator.pageIndex = newPageIndex; // Since the paginator only emits after user-generated changes,
                  // we need our own stream so we know to should re-render the data.

                  _this31._internalPageChanges.next();
                }
              }
            });
          }
          /**
           * Used by the MatTable. Called when it connects to the data source.
           * @docs-private
           */

        }, {
          key: "connect",
          value: function connect() {
            return this._renderData;
          }
          /**
           * Used by the MatTable. Called when it is destroyed. No-op.
           * @docs-private
           */

        }, {
          key: "disconnect",
          value: function disconnect() {}
        }, {
          key: "data",
          get: function get() {
            return this._data.value;
          },
          set: function set(data) {
            this._data.next(data);
          }
          /**
           * Filter term that should be used to filter out objects from the data array. To override how
           * data objects match to this filter string, provide a custom function for filterPredicate.
           */

        }, {
          key: "filter",
          get: function get() {
            return this._filter.value;
          },
          set: function set(filter) {
            this._filter.next(filter);
          }
          /**
           * Instance of the MatSort directive used by the table to control its sorting. Sort changes
           * emitted by the MatSort will trigger an update to the table's rendered data.
           */

        }, {
          key: "sort",
          get: function get() {
            return this._sort;
          },
          set: function set(sort) {
            this._sort = sort;

            this._updateChangeSubscription();
          }
          /**
           * Instance of the MatPaginator component used by the table to control what page of the data is
           * displayed. Page changes emitted by the MatPaginator will trigger an update to the
           * table's rendered data.
           *
           * Note that the data source uses the paginator's properties to calculate which page of data
           * should be displayed. If the paginator receives its properties as template inputs,
           * e.g. `[pageLength]=100` or `[pageIndex]=1`, then be sure that the paginator's view has been
           * initialized before assigning it to this data source.
           */

        }, {
          key: "paginator",
          get: function get() {
            return this._paginator;
          },
          set: function set(paginator) {
            this._paginator = paginator;

            this._updateChangeSubscription();
          }
        }]);

        return MatTableDataSource;
      }(_angular_cdk_table__WEBPACK_IMPORTED_MODULE_1__["DataSource"]);
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
      //# sourceMappingURL=table.js.map

      /***/

    },

    /***/
    "Ynp+":
    /*!******************************************************************!*\
      !*** ./node_modules/@angular/material/fesm2015/button-toggle.js ***!
      \******************************************************************/

    /*! exports provided: MAT_BUTTON_TOGGLE_DEFAULT_OPTIONS, MAT_BUTTON_TOGGLE_GROUP, MAT_BUTTON_TOGGLE_GROUP_VALUE_ACCESSOR, MatButtonToggle, MatButtonToggleChange, MatButtonToggleGroup, MatButtonToggleModule */

    /***/
    function Ynp(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MAT_BUTTON_TOGGLE_DEFAULT_OPTIONS", function () {
        return MAT_BUTTON_TOGGLE_DEFAULT_OPTIONS;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MAT_BUTTON_TOGGLE_GROUP", function () {
        return MAT_BUTTON_TOGGLE_GROUP;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MAT_BUTTON_TOGGLE_GROUP_VALUE_ACCESSOR", function () {
        return MAT_BUTTON_TOGGLE_GROUP_VALUE_ACCESSOR;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatButtonToggle", function () {
        return MatButtonToggle;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatButtonToggleChange", function () {
        return MatButtonToggleChange;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatButtonToggleGroup", function () {
        return MatButtonToggleGroup;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatButtonToggleModule", function () {
        return MatButtonToggleModule;
      });
      /* harmony import */


      var _angular_cdk_a11y__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! @angular/cdk/a11y */
      "YEUz");
      /* harmony import */


      var _angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! @angular/cdk/coercion */
      "8LU1");
      /* harmony import */


      var _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @angular/cdk/collections */
      "CtHx");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/forms */
      "s7LF");
      /* harmony import */


      var _angular_material_core__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/material/core */
      "UhP/");
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /**
       * Injection token that can be used to configure the
       * default options for all button toggles within an app.
       */


      var MAT_BUTTON_TOGGLE_DEFAULT_OPTIONS = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["InjectionToken"]('MAT_BUTTON_TOGGLE_DEFAULT_OPTIONS');
      /**
       * Injection token that can be used to reference instances of `MatButtonToggleGroup`.
       * It serves as alternative token to the actual `MatButtonToggleGroup` class which
       * could cause unnecessary retention of the class and its component metadata.
       */

      var MAT_BUTTON_TOGGLE_GROUP = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["InjectionToken"]('MatButtonToggleGroup');
      /**
       * Provider Expression that allows mat-button-toggle-group to register as a ControlValueAccessor.
       * This allows it to support [(ngModel)].
       * @docs-private
       */

      var MAT_BUTTON_TOGGLE_GROUP_VALUE_ACCESSOR = {
        provide: _angular_forms__WEBPACK_IMPORTED_MODULE_4__["NG_VALUE_ACCESSOR"],
        useExisting: Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["forwardRef"])(function () {
          return MatButtonToggleGroup;
        }),
        multi: true
      };
      var _uniqueIdCounter = 0;
      /** Change event object emitted by MatButtonToggle. */

      var MatButtonToggleChange = function MatButtonToggleChange(
      /** The MatButtonToggle that emits the event. */
      source,
      /** The value assigned to the MatButtonToggle. */
      value) {
        _classCallCheck(this, MatButtonToggleChange);

        this.source = source;
        this.value = value;
      };
      /** Exclusive selection button toggle group that behaves like a radio-button group. */


      var MatButtonToggleGroup = /*#__PURE__*/function () {
        function MatButtonToggleGroup(_changeDetector, defaultOptions) {
          _classCallCheck(this, MatButtonToggleGroup);

          this._changeDetector = _changeDetector;
          this._vertical = false;
          this._multiple = false;
          this._disabled = false;
          /**
           * The method to be called in order to update ngModel.
           * Now `ngModel` binding is not supported in multiple selection mode.
           */

          this._controlValueAccessorChangeFn = function () {};
          /** onTouch function registered via registerOnTouch (ControlValueAccessor). */


          this._onTouched = function () {};

          this._name = "mat-button-toggle-group-".concat(_uniqueIdCounter++);
          /**
           * Event that emits whenever the value of the group changes.
           * Used to facilitate two-way data binding.
           * @docs-private
           */

          this.valueChange = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
          /** Event emitted when the group's value changes. */

          this.change = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
          this.appearance = defaultOptions && defaultOptions.appearance ? defaultOptions.appearance : 'standard';
        }
        /** `name` attribute for the underlying `input` element. */


        _createClass(MatButtonToggleGroup, [{
          key: "ngOnInit",
          value: function ngOnInit() {
            this._selectionModel = new _angular_cdk_collections__WEBPACK_IMPORTED_MODULE_2__["SelectionModel"](this.multiple, undefined, false);
          }
        }, {
          key: "ngAfterContentInit",
          value: function ngAfterContentInit() {
            var _this$_selectionModel;

            (_this$_selectionModel = this._selectionModel).select.apply(_this$_selectionModel, _toConsumableArray(this._buttonToggles.filter(function (toggle) {
              return toggle.checked;
            })));
          }
          /**
           * Sets the model value. Implemented as part of ControlValueAccessor.
           * @param value Value to be set to the model.
           */

        }, {
          key: "writeValue",
          value: function writeValue(value) {
            this.value = value;

            this._changeDetector.markForCheck();
          } // Implemented as part of ControlValueAccessor.

        }, {
          key: "registerOnChange",
          value: function registerOnChange(fn) {
            this._controlValueAccessorChangeFn = fn;
          } // Implemented as part of ControlValueAccessor.

        }, {
          key: "registerOnTouched",
          value: function registerOnTouched(fn) {
            this._onTouched = fn;
          } // Implemented as part of ControlValueAccessor.

        }, {
          key: "setDisabledState",
          value: function setDisabledState(isDisabled) {
            this.disabled = isDisabled;
          }
          /** Dispatch change event with current selection and group value. */

        }, {
          key: "_emitChangeEvent",
          value: function _emitChangeEvent() {
            var selected = this.selected;
            var source = Array.isArray(selected) ? selected[selected.length - 1] : selected;
            var event = new MatButtonToggleChange(source, this.value);

            this._controlValueAccessorChangeFn(event.value);

            this.change.emit(event);
          }
          /**
           * Syncs a button toggle's selected state with the model value.
           * @param toggle Toggle to be synced.
           * @param select Whether the toggle should be selected.
           * @param isUserInput Whether the change was a result of a user interaction.
           * @param deferEvents Whether to defer emitting the change events.
           */

        }, {
          key: "_syncButtonToggle",
          value: function _syncButtonToggle(toggle, select) {
            var _this32 = this;

            var isUserInput = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
            var deferEvents = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : false;

            // Deselect the currently-selected toggle, if we're in single-selection
            // mode and the button being toggled isn't selected at the moment.
            if (!this.multiple && this.selected && !toggle.checked) {
              this.selected.checked = false;
            }

            if (this._selectionModel) {
              if (select) {
                this._selectionModel.select(toggle);
              } else {
                this._selectionModel.deselect(toggle);
              }
            } else {
              deferEvents = true;
            } // We need to defer in some cases in order to avoid "changed after checked errors", however
            // the side-effect is that we may end up updating the model value out of sequence in others
            // The `deferEvents` flag allows us to decide whether to do it on a case-by-case basis.


            if (deferEvents) {
              Promise.resolve().then(function () {
                return _this32._updateModelValue(isUserInput);
              });
            } else {
              this._updateModelValue(isUserInput);
            }
          }
          /** Checks whether a button toggle is selected. */

        }, {
          key: "_isSelected",
          value: function _isSelected(toggle) {
            return this._selectionModel && this._selectionModel.isSelected(toggle);
          }
          /** Determines whether a button toggle should be checked on init. */

        }, {
          key: "_isPrechecked",
          value: function _isPrechecked(toggle) {
            if (typeof this._rawValue === 'undefined') {
              return false;
            }

            if (this.multiple && Array.isArray(this._rawValue)) {
              return this._rawValue.some(function (value) {
                return toggle.value != null && value === toggle.value;
              });
            }

            return toggle.value === this._rawValue;
          }
          /** Updates the selection state of the toggles in the group based on a value. */

        }, {
          key: "_setSelectionByValue",
          value: function _setSelectionByValue(value) {
            var _this33 = this;

            this._rawValue = value;

            if (!this._buttonToggles) {
              return;
            }

            if (this.multiple && value) {
              if (!Array.isArray(value) && (typeof ngDevMode === 'undefined' || ngDevMode)) {
                throw Error('Value must be an array in multiple-selection mode.');
              }

              this._clearSelection();

              value.forEach(function (currentValue) {
                return _this33._selectValue(currentValue);
              });
            } else {
              this._clearSelection();

              this._selectValue(value);
            }
          }
          /** Clears the selected toggles. */

        }, {
          key: "_clearSelection",
          value: function _clearSelection() {
            this._selectionModel.clear();

            this._buttonToggles.forEach(function (toggle) {
              return toggle.checked = false;
            });
          }
          /** Selects a value if there's a toggle that corresponds to it. */

        }, {
          key: "_selectValue",
          value: function _selectValue(value) {
            var correspondingOption = this._buttonToggles.find(function (toggle) {
              return toggle.value != null && toggle.value === value;
            });

            if (correspondingOption) {
              correspondingOption.checked = true;

              this._selectionModel.select(correspondingOption);
            }
          }
          /** Syncs up the group's value with the model and emits the change event. */

        }, {
          key: "_updateModelValue",
          value: function _updateModelValue(isUserInput) {
            // Only emit the change event for user input.
            if (isUserInput) {
              this._emitChangeEvent();
            } // Note: we emit this one no matter whether it was a user interaction, because
            // it is used by Angular to sync up the two-way data binding.


            this.valueChange.emit(this.value);
          }
        }, {
          key: "name",
          get: function get() {
            return this._name;
          },
          set: function set(value) {
            var _this34 = this;

            this._name = value;

            if (this._buttonToggles) {
              this._buttonToggles.forEach(function (toggle) {
                toggle.name = _this34._name;

                toggle._markForCheck();
              });
            }
          }
          /** Whether the toggle group is vertical. */

        }, {
          key: "vertical",
          get: function get() {
            return this._vertical;
          },
          set: function set(value) {
            this._vertical = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_1__["coerceBooleanProperty"])(value);
          }
          /** Value of the toggle group. */

        }, {
          key: "value",
          get: function get() {
            var selected = this._selectionModel ? this._selectionModel.selected : [];

            if (this.multiple) {
              return selected.map(function (toggle) {
                return toggle.value;
              });
            }

            return selected[0] ? selected[0].value : undefined;
          },
          set: function set(newValue) {
            this._setSelectionByValue(newValue);

            this.valueChange.emit(this.value);
          }
          /** Selected button toggles in the group. */

        }, {
          key: "selected",
          get: function get() {
            var selected = this._selectionModel ? this._selectionModel.selected : [];
            return this.multiple ? selected : selected[0] || null;
          }
          /** Whether multiple button toggles can be selected. */

        }, {
          key: "multiple",
          get: function get() {
            return this._multiple;
          },
          set: function set(value) {
            this._multiple = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_1__["coerceBooleanProperty"])(value);
          }
          /** Whether multiple button toggle group is disabled. */

        }, {
          key: "disabled",
          get: function get() {
            return this._disabled;
          },
          set: function set(value) {
            this._disabled = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_1__["coerceBooleanProperty"])(value);

            if (this._buttonToggles) {
              this._buttonToggles.forEach(function (toggle) {
                return toggle._markForCheck();
              });
            }
          }
        }]);

        return MatButtonToggleGroup;
      }();

      MatButtonToggleGroup.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Directive"],
        args: [{
          selector: 'mat-button-toggle-group',
          providers: [MAT_BUTTON_TOGGLE_GROUP_VALUE_ACCESSOR, {
            provide: MAT_BUTTON_TOGGLE_GROUP,
            useExisting: MatButtonToggleGroup
          }],
          host: {
            'role': 'group',
            'class': 'mat-button-toggle-group',
            '[attr.aria-disabled]': 'disabled',
            '[class.mat-button-toggle-vertical]': 'vertical',
            '[class.mat-button-toggle-group-appearance-standard]': 'appearance === "standard"'
          },
          exportAs: 'matButtonToggleGroup'
        }]
      }];

      MatButtonToggleGroup.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ChangeDetectorRef"]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Optional"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Inject"],
            args: [MAT_BUTTON_TOGGLE_DEFAULT_OPTIONS]
          }]
        }];
      };

      MatButtonToggleGroup.propDecorators = {
        _buttonToggles: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ContentChildren"],
          args: [Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["forwardRef"])(function () {
            return MatButtonToggle;
          }), {
            // Note that this would technically pick up toggles
            // from nested groups, but that's not a case that we support.
            descendants: true
          }]
        }],
        appearance: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"]
        }],
        name: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"]
        }],
        vertical: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"]
        }],
        value: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"]
        }],
        valueChange: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Output"]
        }],
        multiple: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"]
        }],
        disabled: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"]
        }],
        change: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Output"]
        }]
      }; // Boilerplate for applying mixins to the MatButtonToggle class.

      /** @docs-private */

      var MatButtonToggleBase = function MatButtonToggleBase() {
        _classCallCheck(this, MatButtonToggleBase);
      };

      var _MatButtonToggleMixinBase = Object(_angular_material_core__WEBPACK_IMPORTED_MODULE_5__["mixinDisableRipple"])(MatButtonToggleBase);
      /** Single button inside of a toggle group. */


      var MatButtonToggle = /*#__PURE__*/function (_MatButtonToggleMixin) {
        _inherits(MatButtonToggle, _MatButtonToggleMixin);

        var _super33 = _createSuper(MatButtonToggle);

        function MatButtonToggle(toggleGroup, _changeDetectorRef, _elementRef, _focusMonitor, defaultTabIndex, defaultOptions) {
          var _this35;

          _classCallCheck(this, MatButtonToggle);

          _this35 = _super33.call(this);
          _this35._changeDetectorRef = _changeDetectorRef;
          _this35._elementRef = _elementRef;
          _this35._focusMonitor = _focusMonitor;
          _this35._isSingleSelector = false;
          _this35._checked = false;
          /**
           * Users can specify the `aria-labelledby` attribute which will be forwarded to the input element
           */

          _this35.ariaLabelledby = null;
          _this35._disabled = false;
          /** Event emitted when the group value changes. */

          _this35.change = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
          var parsedTabIndex = Number(defaultTabIndex);
          _this35.tabIndex = parsedTabIndex || parsedTabIndex === 0 ? parsedTabIndex : null;
          _this35.buttonToggleGroup = toggleGroup;
          _this35.appearance = defaultOptions && defaultOptions.appearance ? defaultOptions.appearance : 'standard';
          return _this35;
        }
        /** Unique ID for the underlying `button` element. */


        _createClass(MatButtonToggle, [{
          key: "ngOnInit",
          value: function ngOnInit() {
            var group = this.buttonToggleGroup;
            this._isSingleSelector = group && !group.multiple;
            this.id = this.id || "mat-button-toggle-".concat(_uniqueIdCounter++);

            if (this._isSingleSelector) {
              this.name = group.name;
            }

            if (group) {
              if (group._isPrechecked(this)) {
                this.checked = true;
              } else if (group._isSelected(this) !== this._checked) {
                // As as side effect of the circular dependency between the toggle group and the button,
                // we may end up in a state where the button is supposed to be checked on init, but it
                // isn't, because the checked value was assigned too early. This can happen when Ivy
                // assigns the static input value before the `ngOnInit` has run.
                group._syncButtonToggle(this, this._checked);
              }
            }
          }
        }, {
          key: "ngAfterViewInit",
          value: function ngAfterViewInit() {
            this._focusMonitor.monitor(this._elementRef, true);
          }
        }, {
          key: "ngOnDestroy",
          value: function ngOnDestroy() {
            var group = this.buttonToggleGroup;

            this._focusMonitor.stopMonitoring(this._elementRef); // Remove the toggle from the selection once it's destroyed. Needs to happen
            // on the next tick in order to avoid "changed after checked" errors.


            if (group && group._isSelected(this)) {
              group._syncButtonToggle(this, false, false, true);
            }
          }
          /** Focuses the button. */

        }, {
          key: "focus",
          value: function focus(options) {
            this._buttonElement.nativeElement.focus(options);
          }
          /** Checks the button toggle due to an interaction with the underlying native button. */

        }, {
          key: "_onButtonClick",
          value: function _onButtonClick() {
            var newChecked = this._isSingleSelector ? true : !this._checked;

            if (newChecked !== this._checked) {
              this._checked = newChecked;

              if (this.buttonToggleGroup) {
                this.buttonToggleGroup._syncButtonToggle(this, this._checked, true);

                this.buttonToggleGroup._onTouched();
              }
            } // Emit a change event when it's the single selector


            this.change.emit(new MatButtonToggleChange(this, this.value));
          }
          /**
           * Marks the button toggle as needing checking for change detection.
           * This method is exposed because the parent button toggle group will directly
           * update bound properties of the radio button.
           */

        }, {
          key: "_markForCheck",
          value: function _markForCheck() {
            // When the group value changes, the button will not be notified.
            // Use `markForCheck` to explicit update button toggle's status.
            this._changeDetectorRef.markForCheck();
          }
        }, {
          key: "buttonId",
          get: function get() {
            return "".concat(this.id, "-button");
          }
          /** The appearance style of the button. */

        }, {
          key: "appearance",
          get: function get() {
            return this.buttonToggleGroup ? this.buttonToggleGroup.appearance : this._appearance;
          },
          set: function set(value) {
            this._appearance = value;
          }
          /** Whether the button is checked. */

        }, {
          key: "checked",
          get: function get() {
            return this.buttonToggleGroup ? this.buttonToggleGroup._isSelected(this) : this._checked;
          },
          set: function set(value) {
            var newValue = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_1__["coerceBooleanProperty"])(value);

            if (newValue !== this._checked) {
              this._checked = newValue;

              if (this.buttonToggleGroup) {
                this.buttonToggleGroup._syncButtonToggle(this, this._checked);
              }

              this._changeDetectorRef.markForCheck();
            }
          }
          /** Whether the button is disabled. */

        }, {
          key: "disabled",
          get: function get() {
            return this._disabled || this.buttonToggleGroup && this.buttonToggleGroup.disabled;
          },
          set: function set(value) {
            this._disabled = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_1__["coerceBooleanProperty"])(value);
          }
        }]);

        return MatButtonToggle;
      }(_MatButtonToggleMixinBase);

      MatButtonToggle.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"],
        args: [{
          selector: 'mat-button-toggle',
          template: "<button #button class=\"mat-button-toggle-button mat-focus-indicator\"\n        type=\"button\"\n        [id]=\"buttonId\"\n        [attr.tabindex]=\"disabled ? -1 : tabIndex\"\n        [attr.aria-pressed]=\"checked\"\n        [disabled]=\"disabled || null\"\n        [attr.name]=\"name || null\"\n        [attr.aria-label]=\"ariaLabel\"\n        [attr.aria-labelledby]=\"ariaLabelledby\"\n        (click)=\"_onButtonClick()\">\n  <span class=\"mat-button-toggle-label-content\">\n    <ng-content></ng-content>\n  </span>\n</button>\n\n<span class=\"mat-button-toggle-focus-overlay\"></span>\n<span class=\"mat-button-toggle-ripple\" matRipple\n     [matRippleTrigger]=\"button\"\n     [matRippleDisabled]=\"this.disableRipple || this.disabled\">\n</span>\n",
          encapsulation: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ViewEncapsulation"].None,
          exportAs: 'matButtonToggle',
          changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ChangeDetectionStrategy"].OnPush,
          inputs: ['disableRipple'],
          host: {
            '[class.mat-button-toggle-standalone]': '!buttonToggleGroup',
            '[class.mat-button-toggle-checked]': 'checked',
            '[class.mat-button-toggle-disabled]': 'disabled',
            '[class.mat-button-toggle-appearance-standard]': 'appearance === "standard"',
            'class': 'mat-button-toggle',
            '[attr.aria-label]': 'null',
            '[attr.aria-labelledby]': 'null',
            '[attr.id]': 'id',
            '[attr.name]': 'null',
            '(focus)': 'focus()',
            'role': 'presentation'
          },
          styles: [".mat-button-toggle-standalone,.mat-button-toggle-group{position:relative;display:inline-flex;flex-direction:row;white-space:nowrap;overflow:hidden;border-radius:2px;-webkit-tap-highlight-color:transparent}.cdk-high-contrast-active .mat-button-toggle-standalone,.cdk-high-contrast-active .mat-button-toggle-group{outline:solid 1px}.mat-button-toggle-standalone.mat-button-toggle-appearance-standard,.mat-button-toggle-group-appearance-standard{border-radius:4px}.cdk-high-contrast-active .mat-button-toggle-standalone.mat-button-toggle-appearance-standard,.cdk-high-contrast-active .mat-button-toggle-group-appearance-standard{outline:0}.mat-button-toggle-vertical{flex-direction:column}.mat-button-toggle-vertical .mat-button-toggle-label-content{display:block}.mat-button-toggle{white-space:nowrap;position:relative}.mat-button-toggle .mat-icon svg{vertical-align:top}.mat-button-toggle.cdk-keyboard-focused .mat-button-toggle-focus-overlay{opacity:1}.cdk-high-contrast-active .mat-button-toggle.cdk-keyboard-focused .mat-button-toggle-focus-overlay{opacity:.5}.mat-button-toggle-appearance-standard:not(.mat-button-toggle-disabled):hover .mat-button-toggle-focus-overlay{opacity:.04}.mat-button-toggle-appearance-standard.cdk-keyboard-focused:not(.mat-button-toggle-disabled) .mat-button-toggle-focus-overlay{opacity:.12}.cdk-high-contrast-active .mat-button-toggle-appearance-standard.cdk-keyboard-focused:not(.mat-button-toggle-disabled) .mat-button-toggle-focus-overlay{opacity:.5}@media(hover: none){.mat-button-toggle-appearance-standard:not(.mat-button-toggle-disabled):hover .mat-button-toggle-focus-overlay{display:none}}.mat-button-toggle-label-content{-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none;display:inline-block;line-height:36px;padding:0 16px;position:relative}.mat-button-toggle-appearance-standard .mat-button-toggle-label-content{padding:0 12px}.mat-button-toggle-label-content>*{vertical-align:middle}.mat-button-toggle-focus-overlay{border-radius:inherit;pointer-events:none;opacity:0;top:0;left:0;right:0;bottom:0;position:absolute}.mat-button-toggle-checked .mat-button-toggle-focus-overlay{border-bottom:solid 36px}.cdk-high-contrast-active .mat-button-toggle-checked .mat-button-toggle-focus-overlay{opacity:.5;height:0}.cdk-high-contrast-active .mat-button-toggle-checked.mat-button-toggle-appearance-standard .mat-button-toggle-focus-overlay{border-bottom:solid 500px}.mat-button-toggle .mat-button-toggle-ripple{top:0;left:0;right:0;bottom:0;position:absolute;pointer-events:none}.mat-button-toggle-button{border:0;background:none;color:inherit;padding:0;margin:0;font:inherit;outline:none;width:100%;cursor:pointer}.mat-button-toggle-disabled .mat-button-toggle-button{cursor:default}.mat-button-toggle-button::-moz-focus-inner{border:0}\n"]
        }]
      }];

      MatButtonToggle.ctorParameters = function () {
        return [{
          type: MatButtonToggleGroup,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Optional"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Inject"],
            args: [MAT_BUTTON_TOGGLE_GROUP]
          }]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ChangeDetectorRef"]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ElementRef"]
        }, {
          type: _angular_cdk_a11y__WEBPACK_IMPORTED_MODULE_0__["FocusMonitor"]
        }, {
          type: String,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Attribute"],
            args: ['tabindex']
          }]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Optional"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Inject"],
            args: [MAT_BUTTON_TOGGLE_DEFAULT_OPTIONS]
          }]
        }];
      };

      MatButtonToggle.propDecorators = {
        ariaLabel: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"],
          args: ['aria-label']
        }],
        ariaLabelledby: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"],
          args: ['aria-labelledby']
        }],
        _buttonElement: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["ViewChild"],
          args: ['button']
        }],
        id: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"]
        }],
        name: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"]
        }],
        value: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"]
        }],
        tabIndex: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"]
        }],
        appearance: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"]
        }],
        checked: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"]
        }],
        disabled: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Input"]
        }],
        change: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["Output"]
        }]
      };
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      var MatButtonToggleModule = function MatButtonToggleModule() {
        _classCallCheck(this, MatButtonToggleModule);
      };

      MatButtonToggleModule.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_3__["NgModule"],
        args: [{
          imports: [_angular_material_core__WEBPACK_IMPORTED_MODULE_5__["MatCommonModule"], _angular_material_core__WEBPACK_IMPORTED_MODULE_5__["MatRippleModule"]],
          exports: [_angular_material_core__WEBPACK_IMPORTED_MODULE_5__["MatCommonModule"], MatButtonToggleGroup, MatButtonToggle],
          declarations: [MatButtonToggleGroup, MatButtonToggle]
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
      //# sourceMappingURL=button-toggle.js.map

      /***/
    },

    /***/
    "ZuBe":
    /*!******************************************************************!*\
      !*** ./src/@vex/components/page-layout/page-layout.component.ts ***!
      \******************************************************************/

    /*! exports provided: PageLayoutComponent */

    /***/
    function ZuBe(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "PageLayoutComponent", function () {
        return PageLayoutComponent;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _page_layout_component_scss__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! ./page-layout.component.scss */
      "8FT2");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");

      var PageLayoutComponent = /*#__PURE__*/function () {
        function PageLayoutComponent() {
          _classCallCheck(this, PageLayoutComponent);

          this.mode = 'simple';
        }

        _createClass(PageLayoutComponent, [{
          key: "isCard",
          get: function get() {
            return this.mode === 'card';
          }
        }, {
          key: "isSimple",
          get: function get() {
            return this.mode === 'simple';
          }
        }]);

        return PageLayoutComponent;
      }();

      PageLayoutComponent.ctorParameters = function () {
        return [];
      };

      PageLayoutComponent.propDecorators = {
        mode: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Input"]
        }],
        isCard: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["HostBinding"],
          args: ['class.vex-page-layout-card']
        }],
        isSimple: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["HostBinding"],
          args: ['class.vex-page-layout-simple']
        }]
      };
      PageLayoutComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["Component"])({
        selector: 'vex-page-layout',
        template: '<ng-content></ng-content>',
        host: {
          "class": 'vex-page-layout'
        },
        encapsulation: _angular_core__WEBPACK_IMPORTED_MODULE_2__["ViewEncapsulation"].None,
        styles: [_page_layout_component_scss__WEBPACK_IMPORTED_MODULE_1__["default"]]
      })], PageLayoutComponent);
      /***/
    },

    /***/
    "uwSD":
    /*!*************************************************************************!*\
      !*** ./src/@vex/components/page-layout/page-layout-header.directive.ts ***!
      \*************************************************************************/

    /*! exports provided: PageLayoutHeaderDirective */

    /***/
    function uwSD(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "PageLayoutHeaderDirective", function () {
        return PageLayoutHeaderDirective;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");

      var PageLayoutHeaderDirective = function PageLayoutHeaderDirective() {
        _classCallCheck(this, PageLayoutHeaderDirective);
      };

      PageLayoutHeaderDirective.ctorParameters = function () {
        return [];
      };

      PageLayoutHeaderDirective = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Directive"])({
        selector: '[vexPageLayoutHeader],vex-page-layout-header',
        host: {
          "class": 'vex-page-layout-header'
        }
      })], PageLayoutHeaderDirective);
      /***/
    }
  }]);
})();
//# sourceMappingURL=default~aliases-aliases-module~endpoints-endpoints-module~organizations-organizations-module~project~11ec6de4-es5.js.map