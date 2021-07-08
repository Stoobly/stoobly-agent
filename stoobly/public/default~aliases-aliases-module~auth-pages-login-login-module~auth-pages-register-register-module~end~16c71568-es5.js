(function () {
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

  (window["webpackJsonp"] = window["webpackJsonp"] || []).push([["default~aliases-aliases-module~auth-pages-login-login-module~auth-pages-register-register-module~end~16c71568"], {
    /***/
    "pMoy":
    /*!*************************************************************!*\
      !*** ./node_modules/@angular/material/fesm2015/checkbox.js ***!
      \*************************************************************/

    /*! exports provided: MAT_CHECKBOX_CONTROL_VALUE_ACCESSOR, MAT_CHECKBOX_DEFAULT_OPTIONS, MAT_CHECKBOX_DEFAULT_OPTIONS_FACTORY, MAT_CHECKBOX_REQUIRED_VALIDATOR, MatCheckbox, MatCheckboxChange, MatCheckboxModule, MatCheckboxRequiredValidator, _MatCheckboxRequiredValidatorModule */

    /***/
    function pMoy(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MAT_CHECKBOX_CONTROL_VALUE_ACCESSOR", function () {
        return MAT_CHECKBOX_CONTROL_VALUE_ACCESSOR;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MAT_CHECKBOX_DEFAULT_OPTIONS", function () {
        return MAT_CHECKBOX_DEFAULT_OPTIONS;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MAT_CHECKBOX_DEFAULT_OPTIONS_FACTORY", function () {
        return MAT_CHECKBOX_DEFAULT_OPTIONS_FACTORY;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MAT_CHECKBOX_REQUIRED_VALIDATOR", function () {
        return MAT_CHECKBOX_REQUIRED_VALIDATOR;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatCheckbox", function () {
        return MatCheckbox;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatCheckboxChange", function () {
        return MatCheckboxChange;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatCheckboxModule", function () {
        return MatCheckboxModule;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "MatCheckboxRequiredValidator", function () {
        return MatCheckboxRequiredValidator;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "_MatCheckboxRequiredValidatorModule", function () {
        return _MatCheckboxRequiredValidatorModule;
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


      var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(
      /*! @angular/core */
      "8Y7J");
      /* harmony import */


      var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(
      /*! @angular/forms */
      "s7LF");
      /* harmony import */


      var _angular_material_core__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(
      /*! @angular/material/core */
      "UhP/");
      /* harmony import */


      var _angular_platform_browser_animations__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(
      /*! @angular/platform-browser/animations */
      "omvX");
      /* harmony import */


      var _angular_cdk_observers__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(
      /*! @angular/cdk/observers */
      "9b/N");
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /** Injection token to be used to override the default options for `mat-checkbox`. */


      var MAT_CHECKBOX_DEFAULT_OPTIONS = new _angular_core__WEBPACK_IMPORTED_MODULE_2__["InjectionToken"]('mat-checkbox-default-options', {
        providedIn: 'root',
        factory: MAT_CHECKBOX_DEFAULT_OPTIONS_FACTORY
      });
      /** @docs-private */

      function MAT_CHECKBOX_DEFAULT_OPTIONS_FACTORY() {
        return {
          color: 'accent',
          clickAction: 'check-indeterminate'
        };
      }
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */
      // Increasing integer for generating unique ids for checkbox components.


      var nextUniqueId = 0; // Default checkbox configuration.

      var defaults = MAT_CHECKBOX_DEFAULT_OPTIONS_FACTORY();
      /**
       * Provider Expression that allows mat-checkbox to register as a ControlValueAccessor.
       * This allows it to support [(ngModel)].
       * @docs-private
       */

      var MAT_CHECKBOX_CONTROL_VALUE_ACCESSOR = {
        provide: _angular_forms__WEBPACK_IMPORTED_MODULE_3__["NG_VALUE_ACCESSOR"],
        useExisting: Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["forwardRef"])(function () {
          return MatCheckbox;
        }),
        multi: true
      };
      /** Change event object emitted by MatCheckbox. */

      var MatCheckboxChange = function MatCheckboxChange() {
        _classCallCheck(this, MatCheckboxChange);
      }; // Boilerplate for applying mixins to MatCheckbox.

      /** @docs-private */


      var MatCheckboxBase = function MatCheckboxBase(_elementRef) {
        _classCallCheck(this, MatCheckboxBase);

        this._elementRef = _elementRef;
      };

      var _MatCheckboxMixinBase = Object(_angular_material_core__WEBPACK_IMPORTED_MODULE_4__["mixinTabIndex"])(Object(_angular_material_core__WEBPACK_IMPORTED_MODULE_4__["mixinColor"])(Object(_angular_material_core__WEBPACK_IMPORTED_MODULE_4__["mixinDisableRipple"])(Object(_angular_material_core__WEBPACK_IMPORTED_MODULE_4__["mixinDisabled"])(MatCheckboxBase))));
      /**
       * A material design checkbox component. Supports all of the functionality of an HTML5 checkbox,
       * and exposes a similar API. A MatCheckbox can be either checked, unchecked, indeterminate, or
       * disabled. Note that all additional accessibility attributes are taken care of by the component,
       * so there is no need to provide them yourself. However, if you want to omit a label and still
       * have the checkbox be accessible, you may supply an [aria-label] input.
       * See: https://material.io/design/components/selection-controls.html
       */


      var MatCheckbox = /*#__PURE__*/function (_MatCheckboxMixinBase2) {
        _inherits(MatCheckbox, _MatCheckboxMixinBase2);

        var _super = _createSuper(MatCheckbox);

        function MatCheckbox(elementRef, _changeDetectorRef, _focusMonitor, _ngZone, tabIndex, _animationMode, _options) {
          var _this;

          _classCallCheck(this, MatCheckbox);

          _this = _super.call(this, elementRef);
          _this._changeDetectorRef = _changeDetectorRef;
          _this._focusMonitor = _focusMonitor;
          _this._ngZone = _ngZone;
          _this._animationMode = _animationMode;
          _this._options = _options;
          /**
           * Attached to the aria-label attribute of the host element. In most cases, aria-labelledby will
           * take precedence so this may be omitted.
           */

          _this.ariaLabel = '';
          /**
           * Users can specify the `aria-labelledby` attribute which will be forwarded to the input element
           */

          _this.ariaLabelledby = null;
          _this._uniqueId = "mat-checkbox-".concat(++nextUniqueId);
          /** A unique id for the checkbox input. If none is supplied, it will be auto-generated. */

          _this.id = _this._uniqueId;
          /** Whether the label should appear after or before the checkbox. Defaults to 'after' */

          _this.labelPosition = 'after';
          /** Name value will be applied to the input element if present */

          _this.name = null;
          /** Event emitted when the checkbox's `checked` value changes. */

          _this.change = new _angular_core__WEBPACK_IMPORTED_MODULE_2__["EventEmitter"]();
          /** Event emitted when the checkbox's `indeterminate` value changes. */

          _this.indeterminateChange = new _angular_core__WEBPACK_IMPORTED_MODULE_2__["EventEmitter"]();
          /**
           * Called when the checkbox is blurred. Needed to properly implement ControlValueAccessor.
           * @docs-private
           */

          _this._onTouched = function () {};

          _this._currentAnimationClass = '';
          _this._currentCheckState = 0
          /* Init */
          ;

          _this._controlValueAccessorChangeFn = function () {};

          _this._checked = false;
          _this._disabled = false;
          _this._indeterminate = false;
          _this._options = _this._options || defaults;
          _this.color = _this.defaultColor = _this._options.color || defaults.color;
          _this.tabIndex = parseInt(tabIndex) || 0;
          return _this;
        }
        /** Returns the unique id for the visual hidden input. */


        _createClass(MatCheckbox, [{
          key: "ngAfterViewInit",
          value: function ngAfterViewInit() {
            var _this2 = this;

            this._focusMonitor.monitor(this._elementRef, true).subscribe(function (focusOrigin) {
              if (!focusOrigin) {
                // When a focused element becomes disabled, the browser *immediately* fires a blur event.
                // Angular does not expect events to be raised during change detection, so any state change
                // (such as a form control's 'ng-touched') will cause a changed-after-checked error.
                // See https://github.com/angular/angular/issues/17793. To work around this, we defer
                // telling the form control it has been touched until the next tick.
                Promise.resolve().then(function () {
                  _this2._onTouched();

                  _this2._changeDetectorRef.markForCheck();
                });
              }
            });

            this._syncIndeterminate(this._indeterminate);
          } // TODO: Delete next major revision.

        }, {
          key: "ngAfterViewChecked",
          value: function ngAfterViewChecked() {}
        }, {
          key: "ngOnDestroy",
          value: function ngOnDestroy() {
            this._focusMonitor.stopMonitoring(this._elementRef);
          }
          /**
           * Whether the checkbox is checked.
           */

        }, {
          key: "_isRippleDisabled",
          value: function _isRippleDisabled() {
            return this.disableRipple || this.disabled;
          }
          /** Method being called whenever the label text changes. */

        }, {
          key: "_onLabelTextChange",
          value: function _onLabelTextChange() {
            // Since the event of the `cdkObserveContent` directive runs outside of the zone, the checkbox
            // component will be only marked for check, but no actual change detection runs automatically.
            // Instead of going back into the zone in order to trigger a change detection which causes
            // *all* components to be checked (if explicitly marked or not using OnPush), we only trigger
            // an explicit change detection for the checkbox view and its children.
            this._changeDetectorRef.detectChanges();
          } // Implemented as part of ControlValueAccessor.

        }, {
          key: "writeValue",
          value: function writeValue(value) {
            this.checked = !!value;
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
        }, {
          key: "_getAriaChecked",
          value: function _getAriaChecked() {
            if (this.checked) {
              return 'true';
            }

            return this.indeterminate ? 'mixed' : 'false';
          }
        }, {
          key: "_transitionCheckState",
          value: function _transitionCheckState(newState) {
            var oldState = this._currentCheckState;
            var element = this._elementRef.nativeElement;

            if (oldState === newState) {
              return;
            }

            if (this._currentAnimationClass.length > 0) {
              element.classList.remove(this._currentAnimationClass);
            }

            this._currentAnimationClass = this._getAnimationClassForCheckStateTransition(oldState, newState);
            this._currentCheckState = newState;

            if (this._currentAnimationClass.length > 0) {
              element.classList.add(this._currentAnimationClass); // Remove the animation class to avoid animation when the checkbox is moved between containers

              var animationClass = this._currentAnimationClass;

              this._ngZone.runOutsideAngular(function () {
                setTimeout(function () {
                  element.classList.remove(animationClass);
                }, 1000);
              });
            }
          }
        }, {
          key: "_emitChangeEvent",
          value: function _emitChangeEvent() {
            var event = new MatCheckboxChange();
            event.source = this;
            event.checked = this.checked;

            this._controlValueAccessorChangeFn(this.checked);

            this.change.emit(event);
          }
          /** Toggles the `checked` state of the checkbox. */

        }, {
          key: "toggle",
          value: function toggle() {
            this.checked = !this.checked;
          }
          /**
           * Event handler for checkbox input element.
           * Toggles checked state if element is not disabled.
           * Do not toggle on (change) event since IE doesn't fire change event when
           *   indeterminate checkbox is clicked.
           * @param event
           */

        }, {
          key: "_onInputClick",
          value: function _onInputClick(event) {
            var _this3 = this;

            var _a;

            var clickAction = (_a = this._options) === null || _a === void 0 ? void 0 : _a.clickAction; // We have to stop propagation for click events on the visual hidden input element.
            // By default, when a user clicks on a label element, a generated click event will be
            // dispatched on the associated input element. Since we are using a label element as our
            // root container, the click event on the `checkbox` will be executed twice.
            // The real click event will bubble up, and the generated click event also tries to bubble up.
            // This will lead to multiple click events.
            // Preventing bubbling for the second event will solve that issue.

            event.stopPropagation(); // If resetIndeterminate is false, and the current state is indeterminate, do nothing on click

            if (!this.disabled && clickAction !== 'noop') {
              // When user manually click on the checkbox, `indeterminate` is set to false.
              if (this.indeterminate && clickAction !== 'check') {
                Promise.resolve().then(function () {
                  _this3._indeterminate = false;

                  _this3.indeterminateChange.emit(_this3._indeterminate);
                });
              }

              this.toggle();

              this._transitionCheckState(this._checked ? 1
              /* Checked */
              : 2
              /* Unchecked */
              ); // Emit our custom change event if the native input emitted one.
              // It is important to only emit it, if the native input triggered one, because
              // we don't want to trigger a change event, when the `checked` variable changes for example.


              this._emitChangeEvent();
            } else if (!this.disabled && clickAction === 'noop') {
              // Reset native input when clicked with noop. The native checkbox becomes checked after
              // click, reset it to be align with `checked` value of `mat-checkbox`.
              this._inputElement.nativeElement.checked = this.checked;
              this._inputElement.nativeElement.indeterminate = this.indeterminate;
            }
          }
          /** Focuses the checkbox. */

        }, {
          key: "focus",
          value: function focus() {
            var origin = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'keyboard';
            var options = arguments.length > 1 ? arguments[1] : undefined;

            this._focusMonitor.focusVia(this._inputElement, origin, options);
          }
        }, {
          key: "_onInteractionEvent",
          value: function _onInteractionEvent(event) {
            // We always have to stop propagation on the change event.
            // Otherwise the change event, from the input element, will bubble up and
            // emit its event object to the `change` output.
            event.stopPropagation();
          }
        }, {
          key: "_getAnimationClassForCheckStateTransition",
          value: function _getAnimationClassForCheckStateTransition(oldState, newState) {
            // Don't transition if animations are disabled.
            if (this._animationMode === 'NoopAnimations') {
              return '';
            }

            var animSuffix = '';

            switch (oldState) {
              case 0
              /* Init */
              :
                // Handle edge case where user interacts with checkbox that does not have [(ngModel)] or
                // [checked] bound to it.
                if (newState === 1
                /* Checked */
                ) {
                    animSuffix = 'unchecked-checked';
                  } else if (newState == 3
                /* Indeterminate */
                ) {
                    animSuffix = 'unchecked-indeterminate';
                  } else {
                  return '';
                }

                break;

              case 2
              /* Unchecked */
              :
                animSuffix = newState === 1
                /* Checked */
                ? 'unchecked-checked' : 'unchecked-indeterminate';
                break;

              case 1
              /* Checked */
              :
                animSuffix = newState === 2
                /* Unchecked */
                ? 'checked-unchecked' : 'checked-indeterminate';
                break;

              case 3
              /* Indeterminate */
              :
                animSuffix = newState === 1
                /* Checked */
                ? 'indeterminate-checked' : 'indeterminate-unchecked';
                break;
            }

            return "mat-checkbox-anim-".concat(animSuffix);
          }
          /**
           * Syncs the indeterminate value with the checkbox DOM node.
           *
           * We sync `indeterminate` directly on the DOM node, because in Ivy the check for whether a
           * property is supported on an element boils down to `if (propName in element)`. Domino's
           * HTMLInputElement doesn't have an `indeterminate` property so Ivy will warn during
           * server-side rendering.
           */

        }, {
          key: "_syncIndeterminate",
          value: function _syncIndeterminate(value) {
            var nativeCheckbox = this._inputElement;

            if (nativeCheckbox) {
              nativeCheckbox.nativeElement.indeterminate = value;
            }
          }
        }, {
          key: "inputId",
          get: function get() {
            return "".concat(this.id || this._uniqueId, "-input");
          }
          /** Whether the checkbox is required. */

        }, {
          key: "required",
          get: function get() {
            return this._required;
          },
          set: function set(value) {
            this._required = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_1__["coerceBooleanProperty"])(value);
          }
        }, {
          key: "checked",
          get: function get() {
            return this._checked;
          },
          set: function set(value) {
            if (value != this.checked) {
              this._checked = value;

              this._changeDetectorRef.markForCheck();
            }
          }
          /**
           * Whether the checkbox is disabled. This fully overrides the implementation provided by
           * mixinDisabled, but the mixin is still required because mixinTabIndex requires it.
           */

        }, {
          key: "disabled",
          get: function get() {
            return this._disabled;
          },
          set: function set(value) {
            var newValue = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_1__["coerceBooleanProperty"])(value);

            if (newValue !== this.disabled) {
              this._disabled = newValue;

              this._changeDetectorRef.markForCheck();
            }
          }
          /**
           * Whether the checkbox is indeterminate. This is also known as "mixed" mode and can be used to
           * represent a checkbox with three states, e.g. a checkbox that represents a nested list of
           * checkable items. Note that whenever checkbox is manually clicked, indeterminate is immediately
           * set to false.
           */

        }, {
          key: "indeterminate",
          get: function get() {
            return this._indeterminate;
          },
          set: function set(value) {
            var changed = value != this._indeterminate;
            this._indeterminate = Object(_angular_cdk_coercion__WEBPACK_IMPORTED_MODULE_1__["coerceBooleanProperty"])(value);

            if (changed) {
              if (this._indeterminate) {
                this._transitionCheckState(3
                /* Indeterminate */
                );
              } else {
                this._transitionCheckState(this.checked ? 1
                /* Checked */
                : 2
                /* Unchecked */
                );
              }

              this.indeterminateChange.emit(this._indeterminate);
            }

            this._syncIndeterminate(this._indeterminate);
          }
        }]);

        return MatCheckbox;
      }(_MatCheckboxMixinBase);

      MatCheckbox.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Component"],
        args: [{
          selector: 'mat-checkbox',
          template: "<label [attr.for]=\"inputId\" class=\"mat-checkbox-layout\" #label>\n  <span class=\"mat-checkbox-inner-container\"\n       [class.mat-checkbox-inner-container-no-side-margin]=\"!checkboxLabel.textContent || !checkboxLabel.textContent.trim()\">\n    <input #input\n           class=\"mat-checkbox-input cdk-visually-hidden\" type=\"checkbox\"\n           [id]=\"inputId\"\n           [required]=\"required\"\n           [checked]=\"checked\"\n           [attr.value]=\"value\"\n           [disabled]=\"disabled\"\n           [attr.name]=\"name\"\n           [tabIndex]=\"tabIndex\"\n           [attr.aria-label]=\"ariaLabel || null\"\n           [attr.aria-labelledby]=\"ariaLabelledby\"\n           [attr.aria-checked]=\"_getAriaChecked()\"\n           [attr.aria-describedby]=\"ariaDescribedby\"\n           (change)=\"_onInteractionEvent($event)\"\n           (click)=\"_onInputClick($event)\">\n    <span matRipple class=\"mat-checkbox-ripple mat-focus-indicator\"\n         [matRippleTrigger]=\"label\"\n         [matRippleDisabled]=\"_isRippleDisabled()\"\n         [matRippleRadius]=\"20\"\n         [matRippleCentered]=\"true\"\n         [matRippleAnimation]=\"{enterDuration: 150}\">\n      <span class=\"mat-ripple-element mat-checkbox-persistent-ripple\"></span>\n    </span>\n    <span class=\"mat-checkbox-frame\"></span>\n    <span class=\"mat-checkbox-background\">\n      <svg version=\"1.1\"\n           focusable=\"false\"\n           class=\"mat-checkbox-checkmark\"\n           viewBox=\"0 0 24 24\"\n           xml:space=\"preserve\">\n        <path class=\"mat-checkbox-checkmark-path\"\n              fill=\"none\"\n              stroke=\"white\"\n              d=\"M4.1,12.7 9,17.6 20.3,6.3\"/>\n      </svg>\n      <!-- Element for rendering the indeterminate state checkbox. -->\n      <span class=\"mat-checkbox-mixedmark\"></span>\n    </span>\n  </span>\n  <span class=\"mat-checkbox-label\" #checkboxLabel (cdkObserveContent)=\"_onLabelTextChange()\">\n    <!-- Add an invisible span so JAWS can read the label -->\n    <span style=\"display:none\">&nbsp;</span>\n    <ng-content></ng-content>\n  </span>\n</label>\n",
          exportAs: 'matCheckbox',
          host: {
            'class': 'mat-checkbox',
            '[id]': 'id',
            '[attr.tabindex]': 'null',
            '[class.mat-checkbox-indeterminate]': 'indeterminate',
            '[class.mat-checkbox-checked]': 'checked',
            '[class.mat-checkbox-disabled]': 'disabled',
            '[class.mat-checkbox-label-before]': 'labelPosition == "before"',
            '[class._mat-animation-noopable]': "_animationMode === 'NoopAnimations'"
          },
          providers: [MAT_CHECKBOX_CONTROL_VALUE_ACCESSOR],
          inputs: ['disableRipple', 'color', 'tabIndex'],
          encapsulation: _angular_core__WEBPACK_IMPORTED_MODULE_2__["ViewEncapsulation"].None,
          changeDetection: _angular_core__WEBPACK_IMPORTED_MODULE_2__["ChangeDetectionStrategy"].OnPush,
          styles: ["@keyframes mat-checkbox-fade-in-background{0%{opacity:0}50%{opacity:1}}@keyframes mat-checkbox-fade-out-background{0%,50%{opacity:1}100%{opacity:0}}@keyframes mat-checkbox-unchecked-checked-checkmark-path{0%,50%{stroke-dashoffset:22.910259}50%{animation-timing-function:cubic-bezier(0, 0, 0.2, 0.1)}100%{stroke-dashoffset:0}}@keyframes mat-checkbox-unchecked-indeterminate-mixedmark{0%,68.2%{transform:scaleX(0)}68.2%{animation-timing-function:cubic-bezier(0, 0, 0, 1)}100%{transform:scaleX(1)}}@keyframes mat-checkbox-checked-unchecked-checkmark-path{from{animation-timing-function:cubic-bezier(0.4, 0, 1, 1);stroke-dashoffset:0}to{stroke-dashoffset:-22.910259}}@keyframes mat-checkbox-checked-indeterminate-checkmark{from{animation-timing-function:cubic-bezier(0, 0, 0.2, 0.1);opacity:1;transform:rotate(0deg)}to{opacity:0;transform:rotate(45deg)}}@keyframes mat-checkbox-indeterminate-checked-checkmark{from{animation-timing-function:cubic-bezier(0.14, 0, 0, 1);opacity:0;transform:rotate(45deg)}to{opacity:1;transform:rotate(360deg)}}@keyframes mat-checkbox-checked-indeterminate-mixedmark{from{animation-timing-function:cubic-bezier(0, 0, 0.2, 0.1);opacity:0;transform:rotate(-45deg)}to{opacity:1;transform:rotate(0deg)}}@keyframes mat-checkbox-indeterminate-checked-mixedmark{from{animation-timing-function:cubic-bezier(0.14, 0, 0, 1);opacity:1;transform:rotate(0deg)}to{opacity:0;transform:rotate(315deg)}}@keyframes mat-checkbox-indeterminate-unchecked-mixedmark{0%{animation-timing-function:linear;opacity:1;transform:scaleX(1)}32.8%,100%{opacity:0;transform:scaleX(0)}}.mat-checkbox-background,.mat-checkbox-frame{top:0;left:0;right:0;bottom:0;position:absolute;border-radius:2px;box-sizing:border-box;pointer-events:none}.mat-checkbox{display:inline-block;transition:background 400ms cubic-bezier(0.25, 0.8, 0.25, 1),box-shadow 280ms cubic-bezier(0.4, 0, 0.2, 1);cursor:pointer;-webkit-tap-highlight-color:transparent}._mat-animation-noopable.mat-checkbox{transition:none;animation:none}.mat-checkbox .mat-ripple-element:not(.mat-checkbox-persistent-ripple){opacity:.16}.mat-checkbox-layout{-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none;cursor:inherit;align-items:baseline;vertical-align:middle;display:inline-flex;white-space:nowrap}.mat-checkbox-label{-webkit-user-select:auto;-moz-user-select:auto;-ms-user-select:auto;user-select:auto}.mat-checkbox-inner-container{display:inline-block;height:16px;line-height:0;margin:auto;margin-right:8px;order:0;position:relative;vertical-align:middle;white-space:nowrap;width:16px;flex-shrink:0}[dir=rtl] .mat-checkbox-inner-container{margin-left:8px;margin-right:auto}.mat-checkbox-inner-container-no-side-margin{margin-left:0;margin-right:0}.mat-checkbox-frame{background-color:transparent;transition:border-color 90ms cubic-bezier(0, 0, 0.2, 0.1);border-width:2px;border-style:solid}._mat-animation-noopable .mat-checkbox-frame{transition:none}.cdk-high-contrast-active .mat-checkbox.cdk-keyboard-focused .mat-checkbox-frame{border-style:dotted}.mat-checkbox-background{align-items:center;display:inline-flex;justify-content:center;transition:background-color 90ms cubic-bezier(0, 0, 0.2, 0.1),opacity 90ms cubic-bezier(0, 0, 0.2, 0.1)}._mat-animation-noopable .mat-checkbox-background{transition:none}.cdk-high-contrast-active .mat-checkbox .mat-checkbox-background{background:none}.mat-checkbox-persistent-ripple{display:block;width:100%;height:100%;transform:none}.mat-checkbox-inner-container:hover .mat-checkbox-persistent-ripple{opacity:.04}.mat-checkbox.cdk-keyboard-focused .mat-checkbox-persistent-ripple{opacity:.12}.mat-checkbox-persistent-ripple,.mat-checkbox.mat-checkbox-disabled .mat-checkbox-inner-container:hover .mat-checkbox-persistent-ripple{opacity:0}@media(hover: none){.mat-checkbox-inner-container:hover .mat-checkbox-persistent-ripple{display:none}}.mat-checkbox-checkmark{top:0;left:0;right:0;bottom:0;position:absolute;width:100%}.mat-checkbox-checkmark-path{stroke-dashoffset:22.910259;stroke-dasharray:22.910259;stroke-width:2.1333333333px}.cdk-high-contrast-black-on-white .mat-checkbox-checkmark-path{stroke:#000 !important}.mat-checkbox-mixedmark{width:calc(100% - 6px);height:2px;opacity:0;transform:scaleX(0) rotate(0deg);border-radius:2px}.cdk-high-contrast-active .mat-checkbox-mixedmark{height:0;border-top:solid 2px;margin-top:2px}.mat-checkbox-label-before .mat-checkbox-inner-container{order:1;margin-left:8px;margin-right:auto}[dir=rtl] .mat-checkbox-label-before .mat-checkbox-inner-container{margin-left:auto;margin-right:8px}.mat-checkbox-checked .mat-checkbox-checkmark{opacity:1}.mat-checkbox-checked .mat-checkbox-checkmark-path{stroke-dashoffset:0}.mat-checkbox-checked .mat-checkbox-mixedmark{transform:scaleX(1) rotate(-45deg)}.mat-checkbox-indeterminate .mat-checkbox-checkmark{opacity:0;transform:rotate(45deg)}.mat-checkbox-indeterminate .mat-checkbox-checkmark-path{stroke-dashoffset:0}.mat-checkbox-indeterminate .mat-checkbox-mixedmark{opacity:1;transform:scaleX(1) rotate(0deg)}.mat-checkbox-unchecked .mat-checkbox-background{background-color:transparent}.mat-checkbox-disabled{cursor:default}.cdk-high-contrast-active .mat-checkbox-disabled{opacity:.5}.mat-checkbox-anim-unchecked-checked .mat-checkbox-background{animation:180ms linear 0ms mat-checkbox-fade-in-background}.mat-checkbox-anim-unchecked-checked .mat-checkbox-checkmark-path{animation:180ms linear 0ms mat-checkbox-unchecked-checked-checkmark-path}.mat-checkbox-anim-unchecked-indeterminate .mat-checkbox-background{animation:180ms linear 0ms mat-checkbox-fade-in-background}.mat-checkbox-anim-unchecked-indeterminate .mat-checkbox-mixedmark{animation:90ms linear 0ms mat-checkbox-unchecked-indeterminate-mixedmark}.mat-checkbox-anim-checked-unchecked .mat-checkbox-background{animation:180ms linear 0ms mat-checkbox-fade-out-background}.mat-checkbox-anim-checked-unchecked .mat-checkbox-checkmark-path{animation:90ms linear 0ms mat-checkbox-checked-unchecked-checkmark-path}.mat-checkbox-anim-checked-indeterminate .mat-checkbox-checkmark{animation:90ms linear 0ms mat-checkbox-checked-indeterminate-checkmark}.mat-checkbox-anim-checked-indeterminate .mat-checkbox-mixedmark{animation:90ms linear 0ms mat-checkbox-checked-indeterminate-mixedmark}.mat-checkbox-anim-indeterminate-checked .mat-checkbox-checkmark{animation:500ms linear 0ms mat-checkbox-indeterminate-checked-checkmark}.mat-checkbox-anim-indeterminate-checked .mat-checkbox-mixedmark{animation:500ms linear 0ms mat-checkbox-indeterminate-checked-mixedmark}.mat-checkbox-anim-indeterminate-unchecked .mat-checkbox-background{animation:180ms linear 0ms mat-checkbox-fade-out-background}.mat-checkbox-anim-indeterminate-unchecked .mat-checkbox-mixedmark{animation:300ms linear 0ms mat-checkbox-indeterminate-unchecked-mixedmark}.mat-checkbox-input{bottom:0;left:50%}.mat-checkbox .mat-checkbox-ripple{position:absolute;left:calc(50% - 20px);top:calc(50% - 20px);height:40px;width:40px;z-index:1;pointer-events:none}\n"]
        }]
      }];

      MatCheckbox.ctorParameters = function () {
        return [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["ElementRef"]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["ChangeDetectorRef"]
        }, {
          type: _angular_cdk_a11y__WEBPACK_IMPORTED_MODULE_0__["FocusMonitor"]
        }, {
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["NgZone"]
        }, {
          type: String,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Attribute"],
            args: ['tabindex']
          }]
        }, {
          type: String,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Optional"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Inject"],
            args: [_angular_platform_browser_animations__WEBPACK_IMPORTED_MODULE_5__["ANIMATION_MODULE_TYPE"]]
          }]
        }, {
          type: undefined,
          decorators: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Optional"]
          }, {
            type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Inject"],
            args: [MAT_CHECKBOX_DEFAULT_OPTIONS]
          }]
        }];
      };

      MatCheckbox.propDecorators = {
        ariaLabel: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Input"],
          args: ['aria-label']
        }],
        ariaLabelledby: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Input"],
          args: ['aria-labelledby']
        }],
        ariaDescribedby: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Input"],
          args: ['aria-describedby']
        }],
        id: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Input"]
        }],
        required: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Input"]
        }],
        labelPosition: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Input"]
        }],
        name: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Input"]
        }],
        change: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Output"]
        }],
        indeterminateChange: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Output"]
        }],
        value: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Input"]
        }],
        _inputElement: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["ViewChild"],
          args: ['input']
        }],
        ripple: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["ViewChild"],
          args: [_angular_material_core__WEBPACK_IMPORTED_MODULE_4__["MatRipple"]]
        }],
        checked: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Input"]
        }],
        disabled: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Input"]
        }],
        indeterminate: [{
          type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Input"]
        }]
      };
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      var MAT_CHECKBOX_REQUIRED_VALIDATOR = {
        provide: _angular_forms__WEBPACK_IMPORTED_MODULE_3__["NG_VALIDATORS"],
        useExisting: Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["forwardRef"])(function () {
          return MatCheckboxRequiredValidator;
        }),
        multi: true
      };
      /**
       * Validator for Material checkbox's required attribute in template-driven checkbox.
       * Current CheckboxRequiredValidator only work with `input type=checkbox` and does not
       * work with `mat-checkbox`.
       */

      var MatCheckboxRequiredValidator = /*#__PURE__*/function (_angular_forms__WEBPA) {
        _inherits(MatCheckboxRequiredValidator, _angular_forms__WEBPA);

        var _super2 = _createSuper(MatCheckboxRequiredValidator);

        function MatCheckboxRequiredValidator() {
          _classCallCheck(this, MatCheckboxRequiredValidator);

          return _super2.apply(this, arguments);
        }

        return MatCheckboxRequiredValidator;
      }(_angular_forms__WEBPACK_IMPORTED_MODULE_3__["CheckboxRequiredValidator"]);

      MatCheckboxRequiredValidator.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["Directive"],
        args: [{
          selector: "mat-checkbox[required][formControlName],\n             mat-checkbox[required][formControl], mat-checkbox[required][ngModel]",
          providers: [MAT_CHECKBOX_REQUIRED_VALIDATOR]
        }]
      }];
      /**
       * @license
       * Copyright Google LLC All Rights Reserved.
       *
       * Use of this source code is governed by an MIT-style license that can be
       * found in the LICENSE file at https://angular.io/license
       */

      /** This module is used by both original and MDC-based checkbox implementations. */

      var _MatCheckboxRequiredValidatorModule = function _MatCheckboxRequiredValidatorModule() {
        _classCallCheck(this, _MatCheckboxRequiredValidatorModule);
      };

      _MatCheckboxRequiredValidatorModule.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"],
        args: [{
          exports: [MatCheckboxRequiredValidator],
          declarations: [MatCheckboxRequiredValidator]
        }]
      }];

      var MatCheckboxModule = function MatCheckboxModule() {
        _classCallCheck(this, MatCheckboxModule);
      };

      MatCheckboxModule.decorators = [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"],
        args: [{
          imports: [_angular_material_core__WEBPACK_IMPORTED_MODULE_4__["MatRippleModule"], _angular_material_core__WEBPACK_IMPORTED_MODULE_4__["MatCommonModule"], _angular_cdk_observers__WEBPACK_IMPORTED_MODULE_6__["ObserversModule"], _MatCheckboxRequiredValidatorModule],
          exports: [MatCheckbox, _angular_material_core__WEBPACK_IMPORTED_MODULE_4__["MatCommonModule"], _MatCheckboxRequiredValidatorModule],
          declarations: [MatCheckbox]
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
      //# sourceMappingURL=checkbox.js.map

      /***/
    },

    /***/
    "y3Ys":
    /*!*****************************************************!*\
      !*** ./src/@vex/animations/fade-in-up.animation.ts ***!
      \*****************************************************/

    /*! exports provided: fadeInUpAnimation, fadeInUp400ms */

    /***/
    function y3Ys(module, __webpack_exports__, __webpack_require__) {
      "use strict";

      __webpack_require__.r(__webpack_exports__);
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "fadeInUpAnimation", function () {
        return fadeInUpAnimation;
      });
      /* harmony export (binding) */


      __webpack_require__.d(__webpack_exports__, "fadeInUp400ms", function () {
        return fadeInUp400ms;
      });
      /* harmony import */


      var _angular_animations__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(
      /*! @angular/animations */
      "GS7A");

      function fadeInUpAnimation(duration) {
        return Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["trigger"])('fadeInUp', [Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["transition"])(':enter', [Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["style"])({
          transform: 'translateY(20px)',
          opacity: 0
        }), Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["animate"])("".concat(duration, "ms cubic-bezier(0.35, 0, 0.25, 1)"), Object(_angular_animations__WEBPACK_IMPORTED_MODULE_0__["style"])({
          transform: 'translateY(0)',
          opacity: 1
        }))])]);
      }

      var fadeInUp400ms = fadeInUpAnimation(400);
      /***/
    }
  }]);
})();
//# sourceMappingURL=default~aliases-aliases-module~auth-pages-login-login-module~auth-pages-register-register-module~end~16c71568-es5.js.map