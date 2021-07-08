(function () {
  function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

  function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

  function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

  (window["webpackJsonp"] = window["webpackJsonp"] || []).push([["home-home-module"], {
    /***/
    "0Pcf":
    /*!************************************************!*\
      !*** ./src/app/modules/home/home.component.ts ***!
      \************************************************/

    /*! exports provided: HomeComponent */

    /***/
    function Pcf(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "HomeComponent", function () {
        return HomeComponent;
      });
      /* harmony import */


      var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! tslib */
      "mrSG");
      /* harmony import */


      var _raw_loader_home_component_html__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(
      /*! raw-loader!./home.component.html */
      "nK7U");
      /* harmony import */


      var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");

      var HomeComponent = /*#__PURE__*/function () {
        function HomeComponent() {
          _classCallCheck(this, HomeComponent);
        }

        _createClass(HomeComponent, [{
          key: "ngOnInit",
          value: function ngOnInit() {}
        }]);

        return HomeComponent;
      }();

      HomeComponent.ctorParameters = function () {
        return [];
      };

      HomeComponent = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["Component"])({
        selector: 'home',
        template: _raw_loader_home_component_html__WEBPACK_IMPORTED_MODULE_1__["default"]
      })], HomeComponent);
      /***/
    },

    /***/
    "3Clk":
    /*!*****************************************************!*\
      !*** ./src/app/modules/home/home-routing.module.ts ***!
      \*****************************************************/

    /*! exports provided: HomeRoutingModule */

    /***/
    function Clk(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "HomeRoutingModule", function () {
        return HomeRoutingModule;
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


      var _core_guards_no_auth_guard__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @core/guards/no-auth.guard */
      "pfe1");
      /* harmony import */


      var _home_resolver_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! ./home-resolver.service */
      "dp3H");
      /* harmony import */


      var _home_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! ./home.component */
      "0Pcf");

      var routes = [{
        path: '',
        component: _home_component__WEBPACK_IMPORTED_MODULE_5__["HomeComponent"],
        canActivate: [_core_guards_no_auth_guard__WEBPACK_IMPORTED_MODULE_3__["NoAuthGuard"]],
        resolve: {
          home: _home_resolver_service__WEBPACK_IMPORTED_MODULE_4__["HomeResolver"]
        }
      }];

      var HomeRoutingModule = function HomeRoutingModule() {
        _classCallCheck(this, HomeRoutingModule);
      };

      HomeRoutingModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]]
      })], HomeRoutingModule);
      /***/
    },

    /***/
    "dp3H":
    /*!*******************************************************!*\
      !*** ./src/app/modules/home/home-resolver.service.ts ***!
      \*******************************************************/

    /*! exports provided: HomeResolver */

    /***/
    function dp3H(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "HomeResolver", function () {
        return HomeResolver;
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


      var _environments_environment__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @environments/environment */
      "AytR");

      var HomeResolver = /*#__PURE__*/function () {
        function HomeResolver() {
          _classCallCheck(this, HomeResolver);
        }

        _createClass(HomeResolver, [{
          key: "resolve",
          value: function resolve(route) {
            window.location.href = _environments_environment__WEBPACK_IMPORTED_MODULE_2__["environment"].homepageUrl || '/login';
          }
        }]);

        return HomeResolver;
      }();

      HomeResolver.ctorParameters = function () {
        return [];
      };

      HomeResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], HomeResolver);
      /***/
    },

    /***/
    "iydT":
    /*!*********************************************!*\
      !*** ./src/app/modules/home/home.module.ts ***!
      \*********************************************/

    /*! exports provided: HomeModule */

    /***/
    function iydT(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "HomeModule", function () {
        return HomeModule;
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


      var _home_routing_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! ./home-routing.module */
      "3Clk");
      /* harmony import */


      var _home_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! ./home.component */
      "0Pcf");

      var HomeModule = function HomeModule() {
        _classCallCheck(this, HomeModule);
      };

      HomeModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [_home_component__WEBPACK_IMPORTED_MODULE_4__["HomeComponent"]],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _home_routing_module__WEBPACK_IMPORTED_MODULE_3__["HomeRoutingModule"]]
      })], HomeModule);
      /***/
    },

    /***/
    "nK7U":
    /*!****************************************************************************************!*\
      !*** ./node_modules/raw-loader/dist/cjs.js!./src/app/modules/home/home.component.html ***!
      \****************************************************************************************/

    /*! exports provided: default */

    /***/
    function nK7U(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony default export */


      __webpack_exports__["default"] = "";
      /***/
    }
  }]);
})();
//# sourceMappingURL=home-home-module-es5.js.map