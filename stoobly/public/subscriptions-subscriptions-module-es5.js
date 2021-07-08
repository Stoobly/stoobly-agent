(function () {
  function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

  function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

  function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

  (window["webpackJsonp"] = window["webpackJsonp"] || []).push([["subscriptions-subscriptions-module"], {
    /***/
    "LUT0":
    /*!************************************************************************************!*\
      !*** ./src/app/modules/subscriptions/services/payment-methods-resolver.service.ts ***!
      \************************************************************************************/

    /*! exports provided: PaymentMethodsResolver */

    /***/
    function LUT0(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "PaymentMethodsResolver", function () {
        return PaymentMethodsResolver;
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


      var _core_http_payment_method_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @core/http/payment-method-resource.service */
      "z1g2");

      var PaymentMethodsResolver = /*#__PURE__*/function () {
        function PaymentMethodsResolver(paymentMethodResource) {
          _classCallCheck(this, PaymentMethodsResolver);

          this.paymentMethodResource = paymentMethodResource;
        }

        _createClass(PaymentMethodsResolver, [{
          key: "resolve",
          value: function resolve(route) {
            var organizationId = route.queryParams.organization_id;

            if (organizationId) {
              return this.paymentMethodResource.index({
                organization_id: organizationId
              });
            } else {
              return this.paymentMethodResource.index();
            }
          }
        }]);

        return PaymentMethodsResolver;
      }();

      PaymentMethodsResolver.ctorParameters = function () {
        return [{
          type: _core_http_payment_method_resource_service__WEBPACK_IMPORTED_MODULE_2__["PaymentMethodResource"]
        }];
      };

      PaymentMethodsResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], PaymentMethodsResolver);
      /***/
    },

    /***/
    "UcrS":
    /*!***************************************************************************************!*\
      !*** ./src/app/modules/subscriptions/pages/pricing/services/plan-resolver.service.ts ***!
      \***************************************************************************************/

    /*! exports provided: PlanResolver */

    /***/
    function UcrS(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "PlanResolver", function () {
        return PlanResolver;
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


      var _core_http_plan_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @core/http/plan-resource.service */
      "TE1C");

      var PlanResolver = /*#__PURE__*/function () {
        function PlanResolver(planResource) {
          _classCallCheck(this, PlanResolver);

          this.planResource = planResource;
        }

        _createClass(PlanResolver, [{
          key: "resolve",
          value: function resolve(route) {
            return this.planResource.show(route.queryParams.plan_id);
          }
        }]);

        return PlanResolver;
      }();

      PlanResolver.ctorParameters = function () {
        return [{
          type: _core_http_plan_resource_service__WEBPACK_IMPORTED_MODULE_2__["PlanResource"]
        }];
      };

      PlanResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], PlanResolver);
      /***/
    },

    /***/
    "VnbV":
    /*!****************************************************************************************!*\
      !*** ./src/app/modules/subscriptions/pages/pricing/services/plans-resolver.service.ts ***!
      \****************************************************************************************/

    /*! exports provided: PlansResolver */

    /***/
    function VnbV(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "PlansResolver", function () {
        return PlansResolver;
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


      var _core_http_plan_resource_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @core/http/plan-resource.service */
      "TE1C");

      var PlansResolver = /*#__PURE__*/function () {
        function PlansResolver(planResource) {
          _classCallCheck(this, PlansResolver);

          this.planResource = planResource;
        }

        _createClass(PlansResolver, [{
          key: "resolve",
          value: function resolve(route) {
            return this.planResource.index();
          }
        }]);

        return PlansResolver;
      }();

      PlansResolver.ctorParameters = function () {
        return [{
          type: _core_http_plan_resource_service__WEBPACK_IMPORTED_MODULE_2__["PlanResource"]
        }];
      };

      PlansResolver = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
      })], PlansResolver);
      /***/
    },

    /***/
    "XtcF":
    /*!***************************************************************!*\
      !*** ./src/app/modules/subscriptions/subscriptions.module.ts ***!
      \***************************************************************/

    /*! exports provided: SubscriptionsModule */

    /***/
    function XtcF(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "SubscriptionsModule", function () {
        return SubscriptionsModule;
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


      var _subscriptions_routing_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! ./subscriptions-routing.module */
      "Z8/A");

      var SubscriptionsModule = function SubscriptionsModule() {
        _classCallCheck(this, SubscriptionsModule);
      };

      SubscriptionsModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [],
        imports: [_angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"], _subscriptions_routing_module__WEBPACK_IMPORTED_MODULE_3__["SubscriptionsRoutingModule"]]
      })], SubscriptionsModule);
      /***/
    },

    /***/
    "Z8/A":
    /*!***********************************************************************!*\
      !*** ./src/app/modules/subscriptions/subscriptions-routing.module.ts ***!
      \***********************************************************************/

    /*! exports provided: SubscriptionsRoutingModule */

    /***/
    function Z8A(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "SubscriptionsRoutingModule", function () {
        return SubscriptionsRoutingModule;
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


      var _organizations_services_organization_resolver_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @organizations/services/organization-resolver.service */
      "J3qe");
      /* harmony import */


      var _users_services_user_subscription_resolver_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @users/services/user-subscription-resolver.service */
      "I9wA");
      /* harmony import */


      var _pages_pricing_services_plan_resolver_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! ./pages/pricing/services/plan-resolver.service */
      "UcrS");
      /* harmony import */


      var _pages_pricing_services_plans_resolver_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! ./pages/pricing/services/plans-resolver.service */
      "VnbV");
      /* harmony import */


      var _services_payment_methods_resolver_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(
      /*! ./services/payment-methods-resolver.service */
      "LUT0");

      var routes = [{
        path: 'pricing',
        loadChildren: function loadChildren() {
          return __webpack_require__.e(
          /*! import() | subscriptions-pages-pricing-pricing-module */
          "subscriptions-pages-pricing-pricing-module").then(__webpack_require__.bind(null,
          /*! @subscriptions/pages/pricing/pricing.module */
          "Uqjg")).then(function (m) {
            return m.PricingModule;
          });
        },
        resolve: {
          plans: _pages_pricing_services_plans_resolver_service__WEBPACK_IMPORTED_MODULE_6__["PlansResolver"],
          subscription: _users_services_user_subscription_resolver_service__WEBPACK_IMPORTED_MODULE_4__["UserSubscriptionResolver"]
        }
      }, {
        path: 'buy',
        loadChildren: function loadChildren() {
          return Promise.all(
          /*! import() | subscriptions-pages-buy-buy-module */
          [__webpack_require__.e("default~aliases-aliases-module~auth-pages-login-login-module~auth-pages-register-register-module~end~16c71568"), __webpack_require__.e("default~aliases-aliases-module~endpoints-endpoints-module~organizations-organizations-module~project~eb28f6f5"), __webpack_require__.e("default~organizations-organizations-module~projects-projects-module~requests-requests-module~scenari~04d380cf"), __webpack_require__.e("default~requests-requests-module~scenarios-scenarios-module~subscriptions-pages-buy-buy-module"), __webpack_require__.e("default~organizations-organizations-module~subscriptions-pages-buy-buy-module~users-users-module"), __webpack_require__.e("subscriptions-pages-buy-buy-module")]).then(__webpack_require__.bind(null,
          /*! @subscriptions/pages/buy/buy.module */
          "FI9y")).then(function (m) {
            return m.BuyModule;
          });
        },
        resolve: {
          organization: _organizations_services_organization_resolver_service__WEBPACK_IMPORTED_MODULE_3__["OrganizationResolver"],
          plan: _pages_pricing_services_plan_resolver_service__WEBPACK_IMPORTED_MODULE_5__["PlanResolver"],
          paymentMethods: _services_payment_methods_resolver_service__WEBPACK_IMPORTED_MODULE_7__["PaymentMethodsResolver"],
          subscription: _users_services_user_subscription_resolver_service__WEBPACK_IMPORTED_MODULE_4__["UserSubscriptionResolver"]
        }
      }, {
        path: '**',
        loadChildren: function loadChildren() {
          return __webpack_require__.e(
          /*! import() | error-pages-404-error-404-module */
          "error-pages-404-error-404-module").then(__webpack_require__.bind(null,
          /*! @error/pages/404/error-404.module */
          "y9RA")).then(function (m) {
            return m.Error404Module;
          });
        }
      }];

      var SubscriptionsRoutingModule = function SubscriptionsRoutingModule() {
        _classCallCheck(this, SubscriptionsRoutingModule);
      };

      SubscriptionsRoutingModule = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"])([Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]]
      })], SubscriptionsRoutingModule);
      /***/
    }
  }]);
})();
//# sourceMappingURL=subscriptions-subscriptions-module-es5.js.map