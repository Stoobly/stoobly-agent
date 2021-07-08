(function () {
  function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread(); }

  function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

  function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

  function _iterableToArray(iter) { if (typeof Symbol !== "undefined" && Symbol.iterator in Object(iter)) return Array.from(iter); }

  function _arrayWithoutHoles(arr) { if (Array.isArray(arr)) return _arrayLikeToArray(arr); }

  function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

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

  (window["webpackJsonp"] = window["webpackJsonp"] || []).push([["default~organizations-organizations-module~projects-projects-module~users-users-module"], {
    /***/
    "176q":
    /*!***********************************************************************************************************!*\
      !*** ./src/app/modules/organizations/components/organizations-create/organizations-create.component.scss ***!
      \***********************************************************************************************************/

    /*! exports provided: default */

    /***/
    function q(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJvcmdhbml6YXRpb25zLWNyZWF0ZS5jb21wb25lbnQuc2NzcyJ9 */";
      /***/
    },

    /***/
    "6W+F":
    /*!********************************************************!*\
      !*** ./node_modules/@iconify/icons-ic/twotone-work.js ***!
      \********************************************************/

    /*! no static exports found */

    /***/
    function WF(module, exports) {
      var data = {
        "body": "<path opacity=\".3\" d=\"M4 8h16v11H4z\" fill=\"currentColor\"/><path d=\"M20 6h-4V4c0-1.11-.89-2-2-2h-4c-1.11 0-2 .89-2 2v2H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zM10 4h4v2h-4V4zm10 15H4V8h16v11z\" fill=\"currentColor\"/>",
        "width": 24,
        "height": 24
      };
      exports.__esModule = true;
      exports["default"] = data;
      /***/
    },

    /***/
    "6qw8":
    /*!********************************************************!*\
      !*** ./node_modules/@iconify/icons-ic/twotone-mail.js ***!
      \********************************************************/

    /*! no static exports found */

    /***/
    function qw8(module, exports) {
      var data = {
        "body": "<path opacity=\".3\" d=\"M20 6H4l8 4.99zM4 8v10h16V8l-8 5z\" fill=\"currentColor\"/><path d=\"M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 2l-8 4.99L4 6h16zm0 12H4V8l8 5l8-5v10z\" fill=\"currentColor\"/>",
        "width": 24,
        "height": 24
      };
      exports.__esModule = true;
      exports["default"] = data;
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
            var _this = this;

            return labels.map(function (label) {
              return _this.labels[label];
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
    "KUDd":
    /*!******************************************************************************************************!*\
      !*** ./src/app/modules/organizations/components/organizations-create/organizations-create.module.ts ***!
      \******************************************************************************************************/

    /*! exports provided: OrganizationsCreateModule */

    /***/
    function KUDd(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "OrganizationsCreateModule", function () {
        return OrganizationsCreateModule;
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


      var _organizations_create_component__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(
      /*! ./organizations-create.component */
      "vb3d");

      var OrganizationsCreateModule = function OrganizationsCreateModule() {
        _classCallCheck(this, OrganizationsCreateModule);
      };

      OrganizationsCreateModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_organizations_create_component__WEBPACK_IMPORTED_MODULE_14__["OrganizationsCreateComponent"]],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _angular_material_dialog__WEBPACK_IMPORTED_MODULE_8__["MatDialogModule"], _angular_material_icon__WEBPACK_IMPORTED_MODULE_10__["MatIconModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"], _angular_material_input__WEBPACK_IMPORTED_MODULE_11__["MatInputModule"], _angular_material_divider__WEBPACK_IMPORTED_MODULE_9__["MatDividerModule"], _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_7__["MatDatepickerModule"], _visurel_iconify_angular__WEBPACK_IMPORTED_MODULE_13__["IconModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"], _angular_material_menu__WEBPACK_IMPORTED_MODULE_12__["MatMenuModule"], _angular_material_button__WEBPACK_IMPORTED_MODULE_5__["MatButtonModule"], _angular_material_core__WEBPACK_IMPORTED_MODULE_6__["MatNativeDateModule"]],
        entryComponents: [_organizations_create_component__WEBPACK_IMPORTED_MODULE_14__["OrganizationsCreateComponent"]],
        exports: [_organizations_create_component__WEBPACK_IMPORTED_MODULE_14__["OrganizationsCreateComponent"]]
      })], OrganizationsCreateModule);
      /***/
    },

    /***/
    "OcYv":
    /*!************************************************************!*\
      !*** ./node_modules/@iconify/icons-ic/twotone-whatshot.js ***!
      \************************************************************/

    /*! no static exports found */

    /***/
    function OcYv(module, exports) {
      var data = {
        "body": "<path opacity=\".3\" d=\"M16.11 6.77c-.53 2.6-2.62 4.43-5.28 4.43c-1.56 0-2.96-.62-3.97-1.63C6.3 10.96 6 12.47 6 14c0 3.31 2.69 6 6 6s6-2.69 6-6c0-2.56-.66-5.03-1.89-7.23zm-4.22 11.22c-1.37 0-2.49-1.08-2.49-2.42c0-1.25.81-2.13 2.17-2.41c1.37-.28 2.78-.93 3.57-1.99c.3 1 .46 2.05.46 3.12c0 2.04-1.66 3.7-3.71 3.7z\" fill=\"currentColor\"/><path d=\"M11.57 13.16c-1.36.28-2.17 1.16-2.17 2.41c0 1.34 1.11 2.42 2.49 2.42c2.05 0 3.71-1.66 3.71-3.71c0-1.07-.15-2.12-.46-3.12c-.79 1.07-2.2 1.72-3.57 2zM13.5.67s.74 2.65.74 4.8c0 2.06-1.35 3.73-3.41 3.73c-2.07 0-3.63-1.67-3.63-3.73l.03-.36C5.21 7.51 4 10.62 4 14c0 4.42 3.58 8 8 8s8-3.58 8-8C20 8.61 17.41 3.8 13.5.67zM12 20c-3.31 0-6-2.69-6-6c0-1.53.3-3.04.86-4.43a5.582 5.582 0 0 0 3.97 1.63c2.66 0 4.75-1.83 5.28-4.43A14.77 14.77 0 0 1 18 14c0 3.31-2.69 6-6 6z\" fill=\"currentColor\"/>",
        "width": 24,
        "height": 24
      };
      exports.__esModule = true;
      exports["default"] = data;
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
    "UTQ3":
    /*!********************************************************!*\
      !*** ./node_modules/ngx-avatar/fesm2015/ngx-avatar.js ***!
      \********************************************************/

    /*! exports provided: AvatarComponent, AvatarModule, AvatarService, AvatarSource, defaultColors, defaultSources, ɵa, ɵb, ɵc */

    /***/
    function UTQ3(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "AvatarComponent", function () {
        return AvatarComponent;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "AvatarModule", function () {
        return AvatarModule;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "AvatarService", function () {
        return AvatarService;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "AvatarSource", function () {
        return AvatarSource;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "defaultColors", function () {
        return defaultColors;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "defaultSources", function () {
        return defaultSources;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ɵa", function () {
        return SourceFactory;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ɵb", function () {
        return AvatarConfigService;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ɵc", function () {
        return AVATAR_CONFIG;
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


      var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @angular/common */
      "SVse");
      /* harmony import */


      var is_retina__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! is-retina */
      "xUpK");
      /* harmony import */


      var is_retina__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(is_retina__WEBPACK_IMPORTED_MODULE_3__);
      /* harmony import */


      var ts_md5__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! ts-md5 */
      "kScs");
      /* harmony import */


      var ts_md5__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(ts_md5__WEBPACK_IMPORTED_MODULE_4__);
      /* harmony import */


      var _angular_common_http__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/common/http */
      "IheW");
      /* harmony import */


      var rxjs_operators__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! rxjs/operators */
      "kU1M");
      /**
       * Contract of all async sources.
       * Every async source must implement the processResponse method that extracts the avatar url from the data
       */


      var AsyncSource = function AsyncSource(sourceId) {
        _classCallCheck(this, AsyncSource);

        this.sourceId = sourceId;
      };

      var AvatarSource;

      (function (AvatarSource) {
        AvatarSource["FACEBOOK"] = "facebook";
        AvatarSource["GOOGLE"] = "google";
        AvatarSource["TWITTER"] = "twitter";
        AvatarSource["INSTAGRAM"] = "instagram";
        AvatarSource["VKONTAKTE"] = "vkontakte";
        AvatarSource["SKYPE"] = "skype";
        AvatarSource["GRAVATAR"] = "gravatar";
        AvatarSource["GITHUB"] = "github";
        AvatarSource["CUSTOM"] = "custom";
        AvatarSource["INITIALS"] = "initials";
        AvatarSource["VALUE"] = "value";
      })(AvatarSource || (AvatarSource = {}));
      /**
       *  Facebook source implementation.
       *  Fetch avatar source based on facebook identifier
       *  and image size
       */


      var Facebook = /*#__PURE__*/function () {
        function Facebook(sourceId) {
          _classCallCheck(this, Facebook);

          this.sourceId = sourceId;
          this.sourceType = AvatarSource.FACEBOOK;
        }

        _createClass(Facebook, [{
          key: "getAvatar",
          value: function getAvatar(size) {
            return 'https://graph.facebook.com/' + "".concat(this.sourceId, "/picture?width=").concat(size, "&height=").concat(size);
          }
        }]);

        return Facebook;
      }();
      /**
       *  Twitter source implementation.
       *  Fetch avatar source based on google identifier
       *  and image size
       */


      var Twitter = /*#__PURE__*/function () {
        function Twitter(sourceId) {
          _classCallCheck(this, Twitter);

          this.sourceId = sourceId;
          this.sourceType = AvatarSource.TWITTER;
        }

        _createClass(Twitter, [{
          key: "getAvatar",
          value: function getAvatar(size) {
            var twitterImgSize = this.getImageSize(size);
            return "https://twitter.com/".concat(this.sourceId, "/profile_image?size=").concat(twitterImgSize);
          }
        }, {
          key: "getImageSize",
          value: function getImageSize(size) {
            if (size <= 24) {
              return 'mini';
            }

            if (size <= 48) {
              return 'normal';
            }

            if (size <= 73) {
              return 'bigger';
            }

            return 'original';
          }
        }]);

        return Twitter;
      }();
      /**
       *  Google source implementation.
       *  Fetch avatar source based on google identifier
       *  and image size
       */


      var Google = /*#__PURE__*/function (_AsyncSource) {
        _inherits(Google, _AsyncSource);

        var _super = _createSuper(Google);

        function Google(sourceId) {
          var _this2;

          _classCallCheck(this, Google);

          _this2 = _super.call(this, sourceId);
          _this2.sourceType = AvatarSource.GOOGLE;
          return _this2;
        }

        _createClass(Google, [{
          key: "getAvatar",
          value: function getAvatar() {
            return "https://picasaweb.google.com/data/entry/api/user/".concat(this.sourceId, "?alt=json");
          }
          /**
           * Extract google avatar from json data
           */

        }, {
          key: "processResponse",
          value: function processResponse(data, size) {
            var avatarSrc = data.entry.gphoto$thumbnail.$t;

            if (avatarSrc) {
              return avatarSrc.replace('s64', 's' + size);
            }

            return null;
          }
        }]);

        return Google;
      }(AsyncSource);
      /**
       *  Instagram source impelementation.
       *  Fetch avatar source based on instagram identifier
       */


      var Instagram = /*#__PURE__*/function (_AsyncSource2) {
        _inherits(Instagram, _AsyncSource2);

        var _super2 = _createSuper(Instagram);

        function Instagram(sourceId) {
          var _this3;

          _classCallCheck(this, Instagram);

          _this3 = _super2.call(this, sourceId);
          _this3.sourceType = AvatarSource.INSTAGRAM;
          return _this3;
        }

        _createClass(Instagram, [{
          key: "getAvatar",
          value: function getAvatar() {
            return "https://www.instagram.com/".concat(this.sourceId, "/?__a=1");
          }
          /**
           * extract instagram avatar from json data
           */

        }, {
          key: "processResponse",
          value: function processResponse(data, size) {
            return "".concat(data.graphql.user.profile_pic_url_hd, "&s=").concat(size);
          }
        }]);

        return Instagram;
      }(AsyncSource);
      /**
       *  Custom source implementation.
       *  return custom image as an avatar
       *
       */


      var Custom = /*#__PURE__*/function () {
        function Custom(sourceId) {
          _classCallCheck(this, Custom);

          this.sourceId = sourceId;
          this.sourceType = AvatarSource.CUSTOM;
        }

        _createClass(Custom, [{
          key: "getAvatar",
          value: function getAvatar() {
            return this.sourceId;
          }
        }]);

        return Custom;
      }();
      /**
       * Initials source implementation.
       * return the initials of the given value
       */


      var Initials = /*#__PURE__*/function () {
        function Initials(sourceId) {
          _classCallCheck(this, Initials);

          this.sourceId = sourceId;
          this.sourceType = AvatarSource.INITIALS;
        }

        _createClass(Initials, [{
          key: "getAvatar",
          value: function getAvatar(size) {
            return this.getInitials(this.sourceId, size);
          }
          /**
           * Returns the initial letters of a name in a string.
           */

        }, {
          key: "getInitials",
          value: function getInitials(name, size) {
            name = name.trim();

            if (!name) {
              return '';
            }

            var initials = name.split(' ');

            if (size && size < initials.length) {
              return this.constructInitials(initials.slice(0, size));
            } else {
              return this.constructInitials(initials);
            }
          }
          /**
           * Iterates a person's name string to get the initials of each word in uppercase.
           */

        }, {
          key: "constructInitials",
          value: function constructInitials(elements) {
            if (!elements || !elements.length) {
              return '';
            }

            return elements.filter(function (element) {
              return element && element.length > 0;
            }).map(function (element) {
              return element[0].toUpperCase();
            }).join('');
          }
        }]);

        return Initials;
      }();
      /**
       *  Gravatar source implementation.
       *  Fetch avatar source based on gravatar email
       */


      var Gravatar = /*#__PURE__*/function () {
        function Gravatar(value) {
          _classCallCheck(this, Gravatar);

          this.value = value;
          this.sourceType = AvatarSource.GRAVATAR;
          this.sourceId = value.match('^[a-f0-9]{32}$') ? value : ts_md5__WEBPACK_IMPORTED_MODULE_4__["Md5"].hashStr(value).toString();
        }

        _createClass(Gravatar, [{
          key: "getAvatar",
          value: function getAvatar(size) {
            var avatarSize = is_retina__WEBPACK_IMPORTED_MODULE_3___default()() ? size * 2 : size;
            return "https://secure.gravatar.com/avatar/".concat(this.sourceId, "?s=").concat(avatarSize, "&d=404");
          }
        }]);

        return Gravatar;
      }();
      /**
       *  Skype source implementation.
       *  Fetch avatar source based on skype identifier
       */


      var Skype = /*#__PURE__*/function () {
        function Skype(sourceId) {
          _classCallCheck(this, Skype);

          this.sourceId = sourceId;
          this.sourceType = AvatarSource.SKYPE;
        }

        _createClass(Skype, [{
          key: "getAvatar",
          value: function getAvatar() {
            return "https://api.skype.com/users/".concat(this.sourceId, "/profile/avatar");
          }
        }]);

        return Skype;
      }();
      /**
       *  Value source implementation.
       *  return the value as avatar
       */


      var Value = /*#__PURE__*/function () {
        function Value(sourceId) {
          _classCallCheck(this, Value);

          this.sourceId = sourceId;
          this.sourceType = AvatarSource.VALUE;
        }

        _createClass(Value, [{
          key: "getAvatar",
          value: function getAvatar() {
            return this.sourceId;
          }
        }]);

        return Value;
      }();
      /**
       *  Vkontakte source implementation.
       *  Fetch avatar source based on vkontakte identifier
       *  and image size
       */


      var apiVersion = 5.8;

      var Vkontakte = /*#__PURE__*/function (_AsyncSource3) {
        _inherits(Vkontakte, _AsyncSource3);

        var _super3 = _createSuper(Vkontakte);

        function Vkontakte(sourceId) {
          var _this4;

          _classCallCheck(this, Vkontakte);

          _this4 = _super3.call(this, sourceId);
          _this4.sourceType = AvatarSource.VKONTAKTE;
          return _this4;
        }

        _createClass(Vkontakte, [{
          key: "getAvatar",
          value: function getAvatar(size) {
            var imgSize = this.getImageSize(size);
            return "https://api.vk.com/method/users.get?user_id=".concat(this.sourceId, "&v=").concat(apiVersion, "&fields=").concat(imgSize);
          }
          /**
           * extract vkontakte avatar from json data
           */

        }, {
          key: "processResponse",
          value: function processResponse(data) {
            // avatar key property is the size used to generate avatar url
            // size property is always the last key in the response object
            var sizeProperty = Object.keys(data['response'][0]).pop();

            if (!sizeProperty) {
              return null;
            } // return avatar src


            return data['response'][0][sizeProperty] || null;
          }
          /**
           * Returns image size related to vkontakte API
           */

        }, {
          key: "getImageSize",
          value: function getImageSize(size) {
            if (size <= 50) {
              return 'photo_50';
            }

            if (size <= 100) {
              return 'photo_100';
            }

            if (size <= 200) {
              return 'photo_200';
            }

            return 'photo_max';
          }
        }]);

        return Vkontakte;
      }(AsyncSource);
      /**
       *  GitHub source implementation.
       *  Fetch avatar source based on github identifier
       */


      var Github = /*#__PURE__*/function (_AsyncSource4) {
        _inherits(Github, _AsyncSource4);

        var _super4 = _createSuper(Github);

        function Github(sourceId) {
          var _this5;

          _classCallCheck(this, Github);

          _this5 = _super4.call(this, sourceId);
          _this5.sourceType = AvatarSource.GITHUB;
          return _this5;
        }

        _createClass(Github, [{
          key: "getAvatar",
          value: function getAvatar() {
            return "https://api.github.com/users/".concat(this.sourceId);
          }
          /**
           * extract github avatar from json data
           */

        }, {
          key: "processResponse",
          value: function processResponse(data, size) {
            if (size) {
              return "".concat(data.avatar_url, "&s=").concat(size);
            }

            return data.avatar_url;
          }
        }]);

        return Github;
      }(AsyncSource);
      /**
       * Factory class that implements factory method pattern.
       * Used to create Source implementation class based
       * on the source Type
       */


      var SourceFactory = /*#__PURE__*/function () {
        function SourceFactory() {
          _classCallCheck(this, SourceFactory);

          this.sources = {};
          this.sources[AvatarSource.FACEBOOK] = Facebook;
          this.sources[AvatarSource.TWITTER] = Twitter;
          this.sources[AvatarSource.GOOGLE] = Google;
          this.sources[AvatarSource.INSTAGRAM] = Instagram;
          this.sources[AvatarSource.SKYPE] = Skype;
          this.sources[AvatarSource.GRAVATAR] = Gravatar;
          this.sources[AvatarSource.CUSTOM] = Custom;
          this.sources[AvatarSource.INITIALS] = Initials;
          this.sources[AvatarSource.VALUE] = Value;
          this.sources[AvatarSource.VKONTAKTE] = Vkontakte;
          this.sources[AvatarSource.GITHUB] = Github;
        }

        _createClass(SourceFactory, [{
          key: "newInstance",
          value: function newInstance(sourceType, sourceValue) {
            return new this.sources[sourceType](sourceValue);
          }
        }]);

        return SourceFactory;
      }();

      SourceFactory = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])(), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [])], SourceFactory);
      /**
       * Token used to inject the AvatarConfig object
       */

      var AVATAR_CONFIG = new _angular_core__WEBPACK_IMPORTED_MODULE_1__["InjectionToken"]('avatar.config');

      var AvatarConfigService = /*#__PURE__*/function () {
        function AvatarConfigService(userConfig) {
          _classCallCheck(this, AvatarConfigService);

          this.userConfig = userConfig;
        }

        _createClass(AvatarConfigService, [{
          key: "getAvatarSources",
          value: function getAvatarSources(defaultSources) {
            if (this.userConfig && this.userConfig.sourcePriorityOrder && this.userConfig.sourcePriorityOrder.length) {
              var uniqueSources = _toConsumableArray(new Set(this.userConfig.sourcePriorityOrder));

              var validSources = uniqueSources.filter(function (source) {
                return defaultSources.includes(source);
              });
              return [].concat(_toConsumableArray(validSources), _toConsumableArray(defaultSources.filter(function (source) {
                return !validSources.includes(source);
              })));
            }

            return defaultSources;
          }
        }, {
          key: "getAvatarColors",
          value: function getAvatarColors(defaultColors) {
            return this.userConfig && this.userConfig.colors && this.userConfig.colors.length && this.userConfig.colors || defaultColors;
          }
        }]);

        return AvatarConfigService;
      }();

      AvatarConfigService.ctorParameters = function () {
        return [{
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Optional"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Inject"],
            args: [AVATAR_CONFIG]
          }]
        }];
      };

      AvatarConfigService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])(), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__param"])(0, Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Optional"])()), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__param"])(0, Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Inject"])(AVATAR_CONFIG)), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [Object])], AvatarConfigService);
      /**
       * list of Supported avatar sources
       */

      var defaultSources = [AvatarSource.FACEBOOK, AvatarSource.GOOGLE, AvatarSource.TWITTER, AvatarSource.INSTAGRAM, AvatarSource.VKONTAKTE, AvatarSource.SKYPE, AvatarSource.GRAVATAR, AvatarSource.GITHUB, AvatarSource.CUSTOM, AvatarSource.INITIALS, AvatarSource.VALUE];
      /**
       * list of default colors
       */

      var defaultColors = ['#1abc9c', '#3498db', '#f1c40f', '#8e44ad', '#e74c3c', '#d35400', '#2c3e50', '#7f8c8d'];
      /**
       * Provides utilities methods related to Avatar component
       */

      var AvatarService = /*#__PURE__*/function () {
        function AvatarService(http, avatarConfigService) {
          _classCallCheck(this, AvatarService);

          this.http = http;
          this.avatarConfigService = avatarConfigService;
          this.avatarSources = defaultSources;
          this.avatarColors = defaultColors;
          this.failedSources = new Map();
          this.overrideAvatarSources();
          this.overrideAvatarColors();
        }

        _createClass(AvatarService, [{
          key: "fetchAvatar",
          value: function fetchAvatar(avatarUrl) {
            return this.http.get(avatarUrl);
          }
        }, {
          key: "getRandomColor",
          value: function getRandomColor(avatarText) {
            if (!avatarText) {
              return 'transparent';
            }

            var asciiCodeSum = this.calculateAsciiCode(avatarText);
            return this.avatarColors[asciiCodeSum % this.avatarColors.length];
          }
        }, {
          key: "compareSources",
          value: function compareSources(sourceType1, sourceType2) {
            return this.getSourcePriority(sourceType1) - this.getSourcePriority(sourceType2);
          }
        }, {
          key: "isSource",
          value: function isSource(source) {
            return this.avatarSources.includes(source);
          }
        }, {
          key: "isTextAvatar",
          value: function isTextAvatar(sourceType) {
            return [AvatarSource.INITIALS, AvatarSource.VALUE].includes(sourceType);
          }
        }, {
          key: "buildSourceKey",
          value: function buildSourceKey(source) {
            return source.sourceType + '-' + source.sourceId;
          }
        }, {
          key: "sourceHasFailedBefore",
          value: function sourceHasFailedBefore(source) {
            return this.failedSources.has(this.buildSourceKey(source));
          }
        }, {
          key: "markSourceAsFailed",
          value: function markSourceAsFailed(source) {
            this.failedSources.set(this.buildSourceKey(source), source);
          }
        }, {
          key: "overrideAvatarSources",
          value: function overrideAvatarSources() {
            this.avatarSources = this.avatarConfigService.getAvatarSources(defaultSources);
          }
        }, {
          key: "overrideAvatarColors",
          value: function overrideAvatarColors() {
            this.avatarColors = this.avatarConfigService.getAvatarColors(defaultColors);
          }
        }, {
          key: "calculateAsciiCode",
          value: function calculateAsciiCode(value) {
            return value.split('').map(function (letter) {
              return letter.charCodeAt(0);
            }).reduce(function (previous, current) {
              return previous + current;
            });
          }
        }, {
          key: "getSourcePriority",
          value: function getSourcePriority(sourceType) {
            return this.avatarSources.indexOf(sourceType);
          }
        }]);

        return AvatarService;
      }();

      AvatarService.ctorParameters = function () {
        return [{
          type: _angular_common_http__WEBPACK_IMPORTED_MODULE_5__["HttpClient"]
        }, {
          type: AvatarConfigService
        }];
      };

      AvatarService = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])(), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [_angular_common_http__WEBPACK_IMPORTED_MODULE_5__["HttpClient"], AvatarConfigService])], AvatarService);
      /**
       * Universal avatar component that
       * generates avatar from different sources
       *
       * export
       * class AvatarComponent
       * implements {OnChanges}
       */

      var AvatarComponent = /*#__PURE__*/function () {
        function AvatarComponent(sourceFactory, avatarService) {
          _classCallCheck(this, AvatarComponent);

          this.sourceFactory = sourceFactory;
          this.avatarService = avatarService;
          this.round = true;
          this.size = 50;
          this.textSizeRatio = 3;
          this.fgColor = '#FFF';
          this.style = {};
          this.cornerRadius = 0;
          this.clickOnAvatar = new _angular_core__WEBPACK_IMPORTED_MODULE_1__["EventEmitter"]();
          this.isAlive = true;
          this.avatarSrc = null;
          this.avatarText = null;
          this.avatarStyle = {};
          this.hostStyle = {};
          this.currentIndex = -1;
          this.sources = [];
        }

        _createClass(AvatarComponent, [{
          key: "onAvatarClicked",
          value: function onAvatarClicked() {
            this.clickOnAvatar.emit(this.sources[this.currentIndex]);
          }
          /**
           * Detect inputs change
           *
           * param {{ [propKey: string]: SimpleChange }} changes
           *
           * memberof AvatarComponent
           */

        }, {
          key: "ngOnChanges",
          value: function ngOnChanges(changes) {
            for (var propName in changes) {
              if (this.avatarService.isSource(propName)) {
                var sourceType = AvatarSource[propName.toUpperCase()];
                var currentValue = changes[propName].currentValue;

                if (currentValue && typeof currentValue === 'string') {
                  this.addSource(sourceType, currentValue);
                } else {
                  this.removeSource(sourceType);
                }
              }
            } // reinitialize the avatar component when a source property value has changed
            // the fallback system must be re-invoked with the new values.


            this.initializeAvatar();
          }
          /**
           * Fetch avatar source
           *
           * param {any} event
           *
           * memberOf AvatarComponent
           */

        }, {
          key: "fetchAvatarSource",
          value: function fetchAvatarSource() {
            var previousSource = this.sources[this.currentIndex];

            if (previousSource) {
              this.avatarService.markSourceAsFailed(previousSource);
            }

            var source = this.findNextSource();

            if (!source) {
              return;
            }

            if (this.avatarService.isTextAvatar(source.sourceType)) {
              this.buildTextAvatar(source);
              this.avatarSrc = null;
            } else {
              this.buildImageAvatar(source);
            }
          }
        }, {
          key: "findNextSource",
          value: function findNextSource() {
            while (++this.currentIndex < this.sources.length) {
              var source = this.sources[this.currentIndex];

              if (source && !this.avatarService.sourceHasFailedBefore(source)) {
                return source;
              }
            }

            return null;
          }
        }, {
          key: "ngOnDestroy",
          value: function ngOnDestroy() {
            this.isAlive = false;
          }
          /**
           * Initialize the avatar component and its fallback system
           */

        }, {
          key: "initializeAvatar",
          value: function initializeAvatar() {
            this.currentIndex = -1;

            if (this.sources.length > 0) {
              this.sortAvatarSources();
              this.fetchAvatarSource();
              this.hostStyle = {
                width: this.size + 'px',
                height: this.size + 'px'
              };
            }
          }
        }, {
          key: "sortAvatarSources",
          value: function sortAvatarSources() {
            var _this6 = this;

            this.sources.sort(function (source1, source2) {
              return _this6.avatarService.compareSources(source1.sourceType, source2.sourceType);
            });
          }
        }, {
          key: "buildTextAvatar",
          value: function buildTextAvatar(avatarSource) {
            this.avatarText = avatarSource.getAvatar(this.initialsSize);
            this.avatarStyle = this.getInitialsStyle(avatarSource.sourceId);
          }
        }, {
          key: "buildImageAvatar",
          value: function buildImageAvatar(avatarSource) {
            this.avatarStyle = this.getImageStyle();

            if (avatarSource instanceof AsyncSource) {
              this.fetchAndProcessAsyncAvatar(avatarSource);
            } else {
              this.avatarSrc = avatarSource.getAvatar(this.size);
            }
          }
          /**
           *
           * returns initials style
           *
           * memberOf AvatarComponent
           */

        }, {
          key: "getInitialsStyle",
          value: function getInitialsStyle(avatarValue) {
            return Object.assign({
              textAlign: 'center',
              borderRadius: this.round ? '100%' : this.cornerRadius + 'px',
              border: this.borderColor ? '1px solid ' + this.borderColor : '',
              textTransform: 'uppercase',
              color: this.fgColor,
              backgroundColor: this.bgColor ? this.bgColor : this.avatarService.getRandomColor(avatarValue),
              font: Math.floor(this.size / this.textSizeRatio) + 'px Helvetica, Arial, sans-serif',
              lineHeight: this.size + 'px'
            }, this.style);
          }
          /**
           *
           * returns image style
           *
           * memberOf AvatarComponent
           */

        }, {
          key: "getImageStyle",
          value: function getImageStyle() {
            return Object.assign({
              maxWidth: '100%',
              borderRadius: this.round ? '50%' : this.cornerRadius + 'px',
              border: this.borderColor ? '1px solid ' + this.borderColor : '',
              width: this.size,
              height: this.size
            }, this.style);
          }
          /**
           * Fetch avatar image asynchronously.
           *
           * param {Source} source represents avatar source
           * memberof AvatarComponent
           */

        }, {
          key: "fetchAndProcessAsyncAvatar",
          value: function fetchAndProcessAsyncAvatar(source) {
            var _this7 = this;

            if (this.avatarService.sourceHasFailedBefore(source)) {
              return;
            }

            this.avatarService.fetchAvatar(source.getAvatar(this.size)).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["takeWhile"])(function () {
              return _this7.isAlive;
            }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["map"])(function (response) {
              return source.processResponse(response, _this7.size);
            })).subscribe(function (avatarSrc) {
              return _this7.avatarSrc = avatarSrc;
            }, function (err) {
              _this7.fetchAvatarSource();
            });
          }
          /**
           * Add avatar source
           *
           * param sourceType avatar source type e.g facebook,twitter, etc.
           * param sourceValue  source value e.g facebookId value, etc.
           */

        }, {
          key: "addSource",
          value: function addSource(sourceType, sourceValue) {
            var source = this.sources.find(function (s) {
              return s.sourceType === sourceType;
            });

            if (source) {
              source.sourceId = sourceValue;
            } else {
              this.sources.push(this.sourceFactory.newInstance(sourceType, sourceValue));
            }
          }
          /**
           * Remove avatar source
           *
           * param sourceType avatar source type e.g facebook,twitter, etc.
           */

        }, {
          key: "removeSource",
          value: function removeSource(sourceType) {
            this.sources = this.sources.filter(function (source) {
              return source.sourceType !== sourceType;
            });
          }
        }]);

        return AvatarComponent;
      }();

      AvatarComponent.ctorParameters = function () {
        return [{
          type: SourceFactory
        }, {
          type: AvatarService
        }];
      };

      Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)], AvatarComponent.prototype, "round", void 0);
      Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)], AvatarComponent.prototype, "size", void 0);
      Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)], AvatarComponent.prototype, "textSizeRatio", void 0);
      Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)], AvatarComponent.prototype, "bgColor", void 0);
      Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)], AvatarComponent.prototype, "fgColor", void 0);
      Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)], AvatarComponent.prototype, "borderColor", void 0);
      Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)], AvatarComponent.prototype, "style", void 0);
      Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])(), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)], AvatarComponent.prototype, "cornerRadius", void 0);
      Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])('facebookId'), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)], AvatarComponent.prototype, "facebook", void 0);
      Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])('twitterId'), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)], AvatarComponent.prototype, "twitter", void 0);
      Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])('googleId'), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)], AvatarComponent.prototype, "google", void 0);
      Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])('instagramId'), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)], AvatarComponent.prototype, "instagram", void 0);
      Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])('vkontakteId'), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)], AvatarComponent.prototype, "vkontakte", void 0);
      Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])('skypeId'), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)], AvatarComponent.prototype, "skype", void 0);
      Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])('gravatarId'), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)], AvatarComponent.prototype, "gravatar", void 0);
      Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])('githubId'), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)], AvatarComponent.prototype, "github", void 0);
      Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])('src'), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)], AvatarComponent.prototype, "custom", void 0);
      Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])('name'), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)], AvatarComponent.prototype, "initials", void 0);
      Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])('value'), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Object)], AvatarComponent.prototype, "value", void 0);
      Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])('placeholder'), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", String)], AvatarComponent.prototype, "placeholder", void 0);
      Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])('initialsSize'), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", Number)], AvatarComponent.prototype, "initialsSize", void 0);
      Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Output"])(), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:type", _angular_core__WEBPACK_IMPORTED_MODULE_1__["EventEmitter"])], AvatarComponent.prototype, "clickOnAvatar", void 0);
      AvatarComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        // tslint:disable-next-line:component-selector
        selector: 'ngx-avatar',
        template: "\n    <div\n      (click)=\"onAvatarClicked()\"\n      class=\"avatar-container\"\n      [ngStyle]=\"hostStyle\"\n    >\n      <img\n        *ngIf=\"avatarSrc; else textAvatar\"\n        [src]=\"avatarSrc\"\n        [width]=\"size\"\n        [height]=\"size\"\n        [ngStyle]=\"avatarStyle\"\n        (error)=\"fetchAvatarSource()\"\n        class=\"avatar-content\"\n      />\n      <ng-template #textAvatar>\n        <div *ngIf=\"avatarText\" class=\"avatar-content\" [ngStyle]=\"avatarStyle\">\n          {{ avatarText }}\n        </div>\n      </ng-template>\n    </div>\n  ",
        styles: ["\n      :host {\n        border-radius: '50%';\n      }\n    "]
      }), Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"])("design:paramtypes", [SourceFactory, AvatarService])], AvatarComponent);
      var AvatarModule_1;

      var AvatarModule = AvatarModule_1 = /*#__PURE__*/function () {
        function AvatarModule() {
          _classCallCheck(this, AvatarModule);
        }

        _createClass(AvatarModule, null, [{
          key: "forRoot",
          value: function forRoot(avatarConfig) {
            return {
              ngModule: AvatarModule_1,
              providers: [{
                provide: AVATAR_CONFIG,
                useValue: avatarConfig ? avatarConfig : {}
              }]
            };
          }
        }]);

        return AvatarModule;
      }();

      AvatarModule = AvatarModule_1 = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"]],
        declarations: [AvatarComponent],
        providers: [SourceFactory, AvatarService, AvatarConfigService],
        exports: [AvatarComponent]
      })], AvatarModule);
      /*
       * Public API Surface of ngx-avatar
       */

      /**
       * Generated bundle index. Do not edit.
       */
      //# sourceMappingURL=ngx-avatar.js.map

      /***/
    },

    /***/
    "kScs":
    /*!*****************************************!*\
      !*** ./node_modules/ts-md5/dist/md5.js ***!
      \*****************************************/

    /*! no static exports found */

    /***/
    function kScs(module, exports, __webpack_require__) {
      "use strict";
      /*
      
      TypeScript Md5
      ==============
      
      Based on work by
      * Joseph Myers: http://www.myersdaily.org/joseph/javascript/md5-text.html
      * André Cruz: https://github.com/satazor/SparkMD5
      * Raymond Hill: https://github.com/gorhill/yamd5.js
      
      Effectively a TypeScrypt re-write of Raymond Hill JS Library
      
      The MIT License (MIT)
      
      Copyright (C) 2014 Raymond Hill
      
      Permission is hereby granted, free of charge, to any person obtaining a copy
      of this software and associated documentation files (the "Software"), to deal
      in the Software without restriction, including without limitation the rights
      to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
      copies of the Software, and to permit persons to whom the Software is
      furnished to do so, subject to the following conditions:
      
      The above copyright notice and this permission notice shall be included in
      all copies or substantial portions of the Software.
      
      THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
      IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
      FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
      AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
      LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
      OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
      THE SOFTWARE.
      
      
      
                  DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                          Version 2, December 2004
      
       Copyright (C) 2015 André Cruz <amdfcruz@gmail.com>
      
       Everyone is permitted to copy and distribute verbatim or modified
       copies of this license document, and changing it is allowed as long
       as the name is changed.
      
                  DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
         TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
      
        0. You just DO WHAT THE FUCK YOU WANT TO.
      
      
      */

      Object.defineProperty(exports, "__esModule", {
        value: true
      });

      var Md5 =
      /** @class */
      function () {
        function Md5() {
          this._state = new Int32Array(4);
          this._buffer = new ArrayBuffer(68);
          this._buffer8 = new Uint8Array(this._buffer, 0, 68);
          this._buffer32 = new Uint32Array(this._buffer, 0, 17);
          this.start();
        } // One time hashing functions


        Md5.hashStr = function (str, raw) {
          if (raw === void 0) {
            raw = false;
          }

          return this.onePassHasher.start().appendStr(str).end(raw);
        };

        Md5.hashAsciiStr = function (str, raw) {
          if (raw === void 0) {
            raw = false;
          }

          return this.onePassHasher.start().appendAsciiStr(str).end(raw);
        };

        Md5._hex = function (x) {
          var hc = Md5.hexChars;
          var ho = Md5.hexOut;
          var n;
          var offset;
          var j;
          var i;

          for (i = 0; i < 4; i += 1) {
            offset = i * 8;
            n = x[i];

            for (j = 0; j < 8; j += 2) {
              ho[offset + 1 + j] = hc.charAt(n & 0x0F);
              n >>>= 4;
              ho[offset + 0 + j] = hc.charAt(n & 0x0F);
              n >>>= 4;
            }
          }

          return ho.join('');
        };

        Md5._md5cycle = function (x, k) {
          var a = x[0];
          var b = x[1];
          var c = x[2];
          var d = x[3]; // ff()

          a += (b & c | ~b & d) + k[0] - 680876936 | 0;
          a = (a << 7 | a >>> 25) + b | 0;
          d += (a & b | ~a & c) + k[1] - 389564586 | 0;
          d = (d << 12 | d >>> 20) + a | 0;
          c += (d & a | ~d & b) + k[2] + 606105819 | 0;
          c = (c << 17 | c >>> 15) + d | 0;
          b += (c & d | ~c & a) + k[3] - 1044525330 | 0;
          b = (b << 22 | b >>> 10) + c | 0;
          a += (b & c | ~b & d) + k[4] - 176418897 | 0;
          a = (a << 7 | a >>> 25) + b | 0;
          d += (a & b | ~a & c) + k[5] + 1200080426 | 0;
          d = (d << 12 | d >>> 20) + a | 0;
          c += (d & a | ~d & b) + k[6] - 1473231341 | 0;
          c = (c << 17 | c >>> 15) + d | 0;
          b += (c & d | ~c & a) + k[7] - 45705983 | 0;
          b = (b << 22 | b >>> 10) + c | 0;
          a += (b & c | ~b & d) + k[8] + 1770035416 | 0;
          a = (a << 7 | a >>> 25) + b | 0;
          d += (a & b | ~a & c) + k[9] - 1958414417 | 0;
          d = (d << 12 | d >>> 20) + a | 0;
          c += (d & a | ~d & b) + k[10] - 42063 | 0;
          c = (c << 17 | c >>> 15) + d | 0;
          b += (c & d | ~c & a) + k[11] - 1990404162 | 0;
          b = (b << 22 | b >>> 10) + c | 0;
          a += (b & c | ~b & d) + k[12] + 1804603682 | 0;
          a = (a << 7 | a >>> 25) + b | 0;
          d += (a & b | ~a & c) + k[13] - 40341101 | 0;
          d = (d << 12 | d >>> 20) + a | 0;
          c += (d & a | ~d & b) + k[14] - 1502002290 | 0;
          c = (c << 17 | c >>> 15) + d | 0;
          b += (c & d | ~c & a) + k[15] + 1236535329 | 0;
          b = (b << 22 | b >>> 10) + c | 0; // gg()

          a += (b & d | c & ~d) + k[1] - 165796510 | 0;
          a = (a << 5 | a >>> 27) + b | 0;
          d += (a & c | b & ~c) + k[6] - 1069501632 | 0;
          d = (d << 9 | d >>> 23) + a | 0;
          c += (d & b | a & ~b) + k[11] + 643717713 | 0;
          c = (c << 14 | c >>> 18) + d | 0;
          b += (c & a | d & ~a) + k[0] - 373897302 | 0;
          b = (b << 20 | b >>> 12) + c | 0;
          a += (b & d | c & ~d) + k[5] - 701558691 | 0;
          a = (a << 5 | a >>> 27) + b | 0;
          d += (a & c | b & ~c) + k[10] + 38016083 | 0;
          d = (d << 9 | d >>> 23) + a | 0;
          c += (d & b | a & ~b) + k[15] - 660478335 | 0;
          c = (c << 14 | c >>> 18) + d | 0;
          b += (c & a | d & ~a) + k[4] - 405537848 | 0;
          b = (b << 20 | b >>> 12) + c | 0;
          a += (b & d | c & ~d) + k[9] + 568446438 | 0;
          a = (a << 5 | a >>> 27) + b | 0;
          d += (a & c | b & ~c) + k[14] - 1019803690 | 0;
          d = (d << 9 | d >>> 23) + a | 0;
          c += (d & b | a & ~b) + k[3] - 187363961 | 0;
          c = (c << 14 | c >>> 18) + d | 0;
          b += (c & a | d & ~a) + k[8] + 1163531501 | 0;
          b = (b << 20 | b >>> 12) + c | 0;
          a += (b & d | c & ~d) + k[13] - 1444681467 | 0;
          a = (a << 5 | a >>> 27) + b | 0;
          d += (a & c | b & ~c) + k[2] - 51403784 | 0;
          d = (d << 9 | d >>> 23) + a | 0;
          c += (d & b | a & ~b) + k[7] + 1735328473 | 0;
          c = (c << 14 | c >>> 18) + d | 0;
          b += (c & a | d & ~a) + k[12] - 1926607734 | 0;
          b = (b << 20 | b >>> 12) + c | 0; // hh()

          a += (b ^ c ^ d) + k[5] - 378558 | 0;
          a = (a << 4 | a >>> 28) + b | 0;
          d += (a ^ b ^ c) + k[8] - 2022574463 | 0;
          d = (d << 11 | d >>> 21) + a | 0;
          c += (d ^ a ^ b) + k[11] + 1839030562 | 0;
          c = (c << 16 | c >>> 16) + d | 0;
          b += (c ^ d ^ a) + k[14] - 35309556 | 0;
          b = (b << 23 | b >>> 9) + c | 0;
          a += (b ^ c ^ d) + k[1] - 1530992060 | 0;
          a = (a << 4 | a >>> 28) + b | 0;
          d += (a ^ b ^ c) + k[4] + 1272893353 | 0;
          d = (d << 11 | d >>> 21) + a | 0;
          c += (d ^ a ^ b) + k[7] - 155497632 | 0;
          c = (c << 16 | c >>> 16) + d | 0;
          b += (c ^ d ^ a) + k[10] - 1094730640 | 0;
          b = (b << 23 | b >>> 9) + c | 0;
          a += (b ^ c ^ d) + k[13] + 681279174 | 0;
          a = (a << 4 | a >>> 28) + b | 0;
          d += (a ^ b ^ c) + k[0] - 358537222 | 0;
          d = (d << 11 | d >>> 21) + a | 0;
          c += (d ^ a ^ b) + k[3] - 722521979 | 0;
          c = (c << 16 | c >>> 16) + d | 0;
          b += (c ^ d ^ a) + k[6] + 76029189 | 0;
          b = (b << 23 | b >>> 9) + c | 0;
          a += (b ^ c ^ d) + k[9] - 640364487 | 0;
          a = (a << 4 | a >>> 28) + b | 0;
          d += (a ^ b ^ c) + k[12] - 421815835 | 0;
          d = (d << 11 | d >>> 21) + a | 0;
          c += (d ^ a ^ b) + k[15] + 530742520 | 0;
          c = (c << 16 | c >>> 16) + d | 0;
          b += (c ^ d ^ a) + k[2] - 995338651 | 0;
          b = (b << 23 | b >>> 9) + c | 0; // ii()

          a += (c ^ (b | ~d)) + k[0] - 198630844 | 0;
          a = (a << 6 | a >>> 26) + b | 0;
          d += (b ^ (a | ~c)) + k[7] + 1126891415 | 0;
          d = (d << 10 | d >>> 22) + a | 0;
          c += (a ^ (d | ~b)) + k[14] - 1416354905 | 0;
          c = (c << 15 | c >>> 17) + d | 0;
          b += (d ^ (c | ~a)) + k[5] - 57434055 | 0;
          b = (b << 21 | b >>> 11) + c | 0;
          a += (c ^ (b | ~d)) + k[12] + 1700485571 | 0;
          a = (a << 6 | a >>> 26) + b | 0;
          d += (b ^ (a | ~c)) + k[3] - 1894986606 | 0;
          d = (d << 10 | d >>> 22) + a | 0;
          c += (a ^ (d | ~b)) + k[10] - 1051523 | 0;
          c = (c << 15 | c >>> 17) + d | 0;
          b += (d ^ (c | ~a)) + k[1] - 2054922799 | 0;
          b = (b << 21 | b >>> 11) + c | 0;
          a += (c ^ (b | ~d)) + k[8] + 1873313359 | 0;
          a = (a << 6 | a >>> 26) + b | 0;
          d += (b ^ (a | ~c)) + k[15] - 30611744 | 0;
          d = (d << 10 | d >>> 22) + a | 0;
          c += (a ^ (d | ~b)) + k[6] - 1560198380 | 0;
          c = (c << 15 | c >>> 17) + d | 0;
          b += (d ^ (c | ~a)) + k[13] + 1309151649 | 0;
          b = (b << 21 | b >>> 11) + c | 0;
          a += (c ^ (b | ~d)) + k[4] - 145523070 | 0;
          a = (a << 6 | a >>> 26) + b | 0;
          d += (b ^ (a | ~c)) + k[11] - 1120210379 | 0;
          d = (d << 10 | d >>> 22) + a | 0;
          c += (a ^ (d | ~b)) + k[2] + 718787259 | 0;
          c = (c << 15 | c >>> 17) + d | 0;
          b += (d ^ (c | ~a)) + k[9] - 343485551 | 0;
          b = (b << 21 | b >>> 11) + c | 0;
          x[0] = a + x[0] | 0;
          x[1] = b + x[1] | 0;
          x[2] = c + x[2] | 0;
          x[3] = d + x[3] | 0;
        };

        Md5.prototype.start = function () {
          this._dataLength = 0;
          this._bufferLength = 0;

          this._state.set(Md5.stateIdentity);

          return this;
        }; // Char to code point to to array conversion:
        // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/charCodeAt
        // #Example.3A_Fixing_charCodeAt_to_handle_non-Basic-Multilingual-Plane_characters_if_their_presence_earlier_in_the_string_is_unknown


        Md5.prototype.appendStr = function (str) {
          var buf8 = this._buffer8;
          var buf32 = this._buffer32;
          var bufLen = this._bufferLength;
          var code;
          var i;

          for (i = 0; i < str.length; i += 1) {
            code = str.charCodeAt(i);

            if (code < 128) {
              buf8[bufLen++] = code;
            } else if (code < 0x800) {
              buf8[bufLen++] = (code >>> 6) + 0xC0;
              buf8[bufLen++] = code & 0x3F | 0x80;
            } else if (code < 0xD800 || code > 0xDBFF) {
              buf8[bufLen++] = (code >>> 12) + 0xE0;
              buf8[bufLen++] = code >>> 6 & 0x3F | 0x80;
              buf8[bufLen++] = code & 0x3F | 0x80;
            } else {
              code = (code - 0xD800) * 0x400 + (str.charCodeAt(++i) - 0xDC00) + 0x10000;

              if (code > 0x10FFFF) {
                throw new Error('Unicode standard supports code points up to U+10FFFF');
              }

              buf8[bufLen++] = (code >>> 18) + 0xF0;
              buf8[bufLen++] = code >>> 12 & 0x3F | 0x80;
              buf8[bufLen++] = code >>> 6 & 0x3F | 0x80;
              buf8[bufLen++] = code & 0x3F | 0x80;
            }

            if (bufLen >= 64) {
              this._dataLength += 64;

              Md5._md5cycle(this._state, buf32);

              bufLen -= 64;
              buf32[0] = buf32[16];
            }
          }

          this._bufferLength = bufLen;
          return this;
        };

        Md5.prototype.appendAsciiStr = function (str) {
          var buf8 = this._buffer8;
          var buf32 = this._buffer32;
          var bufLen = this._bufferLength;
          var i;
          var j = 0;

          for (;;) {
            i = Math.min(str.length - j, 64 - bufLen);

            while (i--) {
              buf8[bufLen++] = str.charCodeAt(j++);
            }

            if (bufLen < 64) {
              break;
            }

            this._dataLength += 64;

            Md5._md5cycle(this._state, buf32);

            bufLen = 0;
          }

          this._bufferLength = bufLen;
          return this;
        };

        Md5.prototype.appendByteArray = function (input) {
          var buf8 = this._buffer8;
          var buf32 = this._buffer32;
          var bufLen = this._bufferLength;
          var i;
          var j = 0;

          for (;;) {
            i = Math.min(input.length - j, 64 - bufLen);

            while (i--) {
              buf8[bufLen++] = input[j++];
            }

            if (bufLen < 64) {
              break;
            }

            this._dataLength += 64;

            Md5._md5cycle(this._state, buf32);

            bufLen = 0;
          }

          this._bufferLength = bufLen;
          return this;
        };

        Md5.prototype.getState = function () {
          var self = this;
          var s = self._state;
          return {
            buffer: String.fromCharCode.apply(null, self._buffer8),
            buflen: self._bufferLength,
            length: self._dataLength,
            state: [s[0], s[1], s[2], s[3]]
          };
        };

        Md5.prototype.setState = function (state) {
          var buf = state.buffer;
          var x = state.state;
          var s = this._state;
          var i;
          this._dataLength = state.length;
          this._bufferLength = state.buflen;
          s[0] = x[0];
          s[1] = x[1];
          s[2] = x[2];
          s[3] = x[3];

          for (i = 0; i < buf.length; i += 1) {
            this._buffer8[i] = buf.charCodeAt(i);
          }
        };

        Md5.prototype.end = function (raw) {
          if (raw === void 0) {
            raw = false;
          }

          var bufLen = this._bufferLength;
          var buf8 = this._buffer8;
          var buf32 = this._buffer32;
          var i = (bufLen >> 2) + 1;
          var dataBitsLen;
          this._dataLength += bufLen;
          buf8[bufLen] = 0x80;
          buf8[bufLen + 1] = buf8[bufLen + 2] = buf8[bufLen + 3] = 0;
          buf32.set(Md5.buffer32Identity.subarray(i), i);

          if (bufLen > 55) {
            Md5._md5cycle(this._state, buf32);

            buf32.set(Md5.buffer32Identity);
          } // Do the final computation based on the tail and length
          // Beware that the final length may not fit in 32 bits so we take care of that


          dataBitsLen = this._dataLength * 8;

          if (dataBitsLen <= 0xFFFFFFFF) {
            buf32[14] = dataBitsLen;
          } else {
            var matches = dataBitsLen.toString(16).match(/(.*?)(.{0,8})$/);

            if (matches === null) {
              return;
            }

            var lo = parseInt(matches[2], 16);
            var hi = parseInt(matches[1], 16) || 0;
            buf32[14] = lo;
            buf32[15] = hi;
          }

          Md5._md5cycle(this._state, buf32);

          return raw ? this._state : Md5._hex(this._state);
        }; // Private Static Variables


        Md5.stateIdentity = new Int32Array([1732584193, -271733879, -1732584194, 271733878]);
        Md5.buffer32Identity = new Int32Array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]);
        Md5.hexChars = '0123456789abcdef';
        Md5.hexOut = []; // Permanent instance is to use for one-call hashing

        Md5.onePassHasher = new Md5();
        return Md5;
      }();

      exports.Md5 = Md5;

      if (Md5.hashStr('hello') !== '5d41402abc4b2a76b9719d911017c592') {
        console.error('Md5 self test failed.');
      } //# sourceMappingURL=md5.js.map

      /***/

    },

    /***/
    "nBEY":
    /*!*************************************************************************************************************************************************!*\
      !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/organizations/components/organizations-create/organizations-create.component.html ***!
      \*************************************************************************************************************************************************/

    /*! exports provided: default */

    /***/
    function nBEY(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "<form (ngSubmit)=\"save()\" [formGroup]=\"form\">\r\n  <div fxLayout=\"row\" fxLayoutAlign=\"start center\" mat-dialog-title>\r\n    <h2 class=\"headline m-0\" fxFlex=\"auto\">{{ organization ? 'Edit' : 'New' }} Organization</h2>\r\n\r\n    <button class=\"text-secondary\" mat-dialog-close mat-icon-button type=\"button\">\r\n      <mat-icon [icIcon]=\"icClose\"></mat-icon>\r\n    </button>\r\n  </div>\r\n\r\n  <mat-divider class=\"-mx-6 text-border\"></mat-divider>\r\n\r\n  <mat-dialog-content fxLayout=\"column\">\r\n    <mat-form-field class=\"mt-6\">\r\n      <mat-label>Name</mat-label>\r\n      <input cdkFocusInitial formControlName=\"name\" matInput>\r\n\r\n      <mat-icon [icIcon]=\"icPerson\" class=\"ltr:mr-3 rtl:ml-3\" matPrefix></mat-icon>\r\n    </mat-form-field>\r\n\r\n    <mat-form-field>\r\n      <mat-label>Description</mat-label>\r\n      <textarea formControlName=\"description\" matInput></textarea>\r\n    </mat-form-field>\r\n  </mat-dialog-content>\r\n\r\n  <mat-dialog-actions align=\"end\">\r\n    <button mat-button mat-dialog-close type=\"button\">CANCEL</button>\r\n    <button color=\"primary\" mat-button type=\"submit\">{{ organization ? 'UPDATE' : 'CREATE' }}</button>\r\n  </mat-dialog-actions>\r\n</form>\r\n";
      /***/
    },

    /***/
    "vb3d":
    /*!*********************************************************************************************************!*\
      !*** ./src/app/modules/organizations/components/organizations-create/organizations-create.component.ts ***!
      \*********************************************************************************************************/

    /*! exports provided: OrganizationsCreateComponent */

    /***/
    function vb3d(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "OrganizationsCreateComponent", function () {
        return OrganizationsCreateComponent;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _raw_loader_organizations_create_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! raw-loader!./organizations-create.component.html */
      "nBEY");
      /* harmony import */


      var _organizations_create_component_scss__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! ./organizations-create.component.scss */
      "176q");
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


      var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-delete */
      "e3EN");
      /* harmony import */


      var _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_7__);
      /* harmony import */


      var _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-mail */
      "6qw8");
      /* harmony import */


      var _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_8__);
      /* harmony import */


      var _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(
      /*! @iconify/icons-ic/twotone-person */
      "KaaH");
      /* harmony import */


      var _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_9__);

      var OrganizationsCreateComponent = /*#__PURE__*/function () {
        function OrganizationsCreateComponent(organization, dialogRef, fb) {
          _classCallCheck(this, OrganizationsCreateComponent);

          this.organization = organization;
          this.dialogRef = dialogRef;
          this.fb = fb;
          this.onCreate = new _angular_core__WEBPACK_IMPORTED_MODULE_3__["EventEmitter"]();
          this.form = this.fb.group({
            name: null,
            description: null
          });
          this.icClose = _iconify_icons_ic_twotone_close__WEBPACK_IMPORTED_MODULE_6___default.a;
          this.icDelete = _iconify_icons_ic_twotone_delete__WEBPACK_IMPORTED_MODULE_7___default.a;
          this.icPerson = _iconify_icons_ic_twotone_person__WEBPACK_IMPORTED_MODULE_9___default.a;
          this.icEmail = _iconify_icons_ic_twotone_mail__WEBPACK_IMPORTED_MODULE_8___default.a;
        }

        _createClass(OrganizationsCreateComponent, [{
          key: "ngOnInit",
          value: function ngOnInit() {
            this.form.patchValue(this.organization || {});
          }
        }, {
          key: "save",
          value: function save() {
            this.onCreate.emit(this.form.value);
            this.dialogRef.close();
          }
        }]);

        return OrganizationsCreateComponent;
      }();

      OrganizationsCreateComponent.ctorParameters = function () {
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

      OrganizationsCreateComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["Component"])({
        selector: 'organizations-create',
        template: _raw_loader_organizations_create_component_html__WEBPACK_IMPORTED_MODULE_1__["default"],
        styles: [_organizations_create_component_scss__WEBPACK_IMPORTED_MODULE_2__["default"]]
      })], OrganizationsCreateComponent);
      /***/
    },

    /***/
    "xUpK":
    /*!*****************************************!*\
      !*** ./node_modules/is-retina/index.js ***!
      \*****************************************/

    /*! no static exports found */

    /***/
    function xUpK(module, exports) {
      module.exports = function () {
        var mediaQuery;

        if (typeof window !== "undefined" && window !== null) {
          mediaQuery = "(-webkit-min-device-pixel-ratio: 1.25), (min--moz-device-pixel-ratio: 1.25), (-o-min-device-pixel-ratio: 5/4), (min-resolution: 1.25dppx)";

          if (window.devicePixelRatio > 1.25) {
            return true;
          }

          if (window.matchMedia && window.matchMedia(mediaQuery).matches) {
            return true;
          }
        }

        return false;
      };
      /***/

    },

    /***/
    "yVsR":
    /*!************************************************************************!*\
      !*** ./src/app/modules/projects/services/projects-resolver.service.ts ***!
      \************************************************************************/

    /*! exports provided: ProjectsResolver */

    /***/
    function yVsR(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "ProjectsResolver", function () {
        return ProjectsResolver;
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


      var _core_http_project_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @core/http/project-resource.service */
      "4UAC");

      var ProjectsResolver = /*#__PURE__*/function () {
        function ProjectsResolver(projectResource) {
          _classCallCheck(this, ProjectsResolver);

          this.projectResource = projectResource;
        }

        _createClass(ProjectsResolver, [{
          key: "resolve",
          value: function resolve(route) {
            var params = {};

            if (route.queryParams.organization_id) {
              params = {
                organization_id: route.queryParams.organization_id
              };
            } else if (route.parent.params.organization_id) {
              params = {
                organization_id: route.parent.params.organization_id
              };
            }

            return this.projectResource.index(params);
          }
        }]);

        return ProjectsResolver;
      }();

      ProjectsResolver.ctorParameters = function () {
        return [{
          type: _core_http_project_resource_service__WEBPACK_IMPORTED_MODULE_2__["ProjectResource"]
        }];
      };

      ProjectsResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], ProjectsResolver);
      /***/
    }
  }]);
})();
//# sourceMappingURL=default~organizations-organizations-module~projects-projects-module~users-users-module-es5.js.map