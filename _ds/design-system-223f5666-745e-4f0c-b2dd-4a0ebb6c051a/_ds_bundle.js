/* @ds-bundle: {"format":3,"namespace":"DesignSystem_223f56","components":[{"name":"Avatar","sourcePath":"components/core/Avatar.jsx"},{"name":"Badge","sourcePath":"components/core/Badge.jsx"},{"name":"Button","sourcePath":"components/core/Button.jsx"},{"name":"Card","sourcePath":"components/core/Card.jsx"},{"name":"Input","sourcePath":"components/core/Input.jsx"},{"name":"ProgressBar","sourcePath":"components/core/ProgressBar.jsx"},{"name":"Tag","sourcePath":"components/core/Tag.jsx"}],"sourceHashes":{"components/core/Avatar.jsx":"8f95a5abf7d1","components/core/Badge.jsx":"7f1c39bba793","components/core/Button.jsx":"9b1d47550313","components/core/Card.jsx":"56a08020b020","components/core/Input.jsx":"dc374e4f0ec8","components/core/ProgressBar.jsx":"e597f8e89b9a","components/core/Tag.jsx":"9242b9a5310d"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.DesignSystem_223f56 = window.DesignSystem_223f56 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/core/Avatar.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Circular avatar with image or auto-generated initials fallback.
 * Used for teacher/student identity across all three products.
 */
function Avatar({
  src,
  name,
  size = 'md',
  online,
  shape = 'circle',
  ...props
}) {
  const pxMap = {
    xs: 24,
    sm: 32,
    md: 40,
    lg: 56,
    xl: 72,
    '2xl': 96
  };
  const px = pxMap[size] || pxMap.md;

  // Derive initials from name (up to 2 chars, supports Chinese)
  const initials = name ? Array.from(name).slice(0, 2).join('') : '?';

  // Deterministic hue from name
  const hues = [258, 200, 145, 55, 25, 300, 180, 320];
  const hue = name ? hues[Array.from(name)[0].codePointAt(0) % hues.length] : 258;
  const indicatorSize = Math.max(8, Math.round(px * 0.26));
  const borderRadius = shape === 'rounded' ? 'var(--radius-lg)' : '50%';
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      position: 'relative',
      display: 'inline-flex',
      flexShrink: 0
    }
  }, props), /*#__PURE__*/React.createElement("div", {
    style: {
      width: px,
      height: px,
      borderRadius,
      overflow: 'hidden',
      background: src ? 'transparent' : `oklch(0.88 0.10 ${hue})`,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: Math.round(px * 0.38),
      fontFamily: 'var(--font-sans)',
      fontWeight: 'var(--weight-semibold)',
      color: `oklch(0.38 0.16 ${hue})`,
      border: '1.5px solid var(--border-subtle)',
      flexShrink: 0,
      userSelect: 'none'
    }
  }, src ? /*#__PURE__*/React.createElement("img", {
    src: src,
    alt: name || 'avatar',
    style: {
      width: '100%',
      height: '100%',
      objectFit: 'cover'
    }
  }) : initials), online !== undefined && /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'absolute',
      bottom: shape === 'rounded' ? -1 : 0,
      right: shape === 'rounded' ? -1 : 0,
      width: indicatorSize,
      height: indicatorSize,
      borderRadius: '50%',
      background: online ? 'var(--color-success-500)' : 'var(--color-neutral-300)',
      border: '2.5px solid white',
      flexShrink: 0
    }
  }));
}
Object.assign(__ds_scope, { Avatar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Avatar.jsx", error: String((e && e.message) || e) }); }

// components/core/Badge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Compact status or category label.
 * Use for grade levels, subject tags, status indicators, counts.
 */
function Badge({
  variant = 'brand',
  size = 'md',
  dot = false,
  children,
  ...props
}) {
  const colors = {
    brand: {
      bg: 'var(--color-brand-100)',
      text: 'var(--color-brand-700)'
    },
    accent: {
      bg: 'var(--color-accent-100)',
      text: 'var(--color-accent-700)'
    },
    success: {
      bg: 'var(--color-success-100)',
      text: 'var(--color-success-700)'
    },
    warning: {
      bg: 'var(--color-warning-100)',
      text: 'var(--color-warning-600)'
    },
    error: {
      bg: 'var(--color-error-100)',
      text: 'var(--color-error-700)'
    },
    info: {
      bg: 'var(--color-info-100)',
      text: 'var(--color-info-600)'
    },
    neutral: {
      bg: 'var(--color-neutral-100)',
      text: 'var(--color-neutral-700)'
    },
    dark: {
      bg: 'var(--color-neutral-900)',
      text: 'var(--color-neutral-0)'
    }
  };
  const sizes = {
    sm: {
      padding: '2px 7px',
      fontSize: 'var(--text-2xs)',
      gap: '3px'
    },
    md: {
      padding: '3px 9px',
      fontSize: 'var(--text-xs)',
      gap: '4px'
    },
    lg: {
      padding: '4px 11px',
      fontSize: 'var(--text-sm)',
      gap: '5px'
    }
  };
  const c = colors[variant] || colors.neutral;
  const s = sizes[size] || sizes.md;
  return /*#__PURE__*/React.createElement("span", _extends({
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: s.gap,
      padding: s.padding,
      fontSize: s.fontSize,
      fontFamily: 'var(--font-sans)',
      fontWeight: 'var(--weight-medium)',
      lineHeight: '1.4',
      borderRadius: 'var(--radius-full)',
      background: c.bg,
      color: c.text,
      whiteSpace: 'nowrap',
      letterSpacing: 'var(--tracking-wide)'
    }
  }, props), dot && /*#__PURE__*/React.createElement("span", {
    style: {
      width: '6px',
      height: '6px',
      borderRadius: '50%',
      background: 'currentColor',
      flexShrink: 0
    }
  }), children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Badge.jsx", error: String((e && e.message) || e) }); }

// components/core/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const {
  useState
} = React;
/**
 * Primary action trigger for 易數教室 UIs.
 * Five variants, four sizes, optional icon, loading state.
 */
function Button({
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  icon = null,
  iconPosition = 'left',
  fullWidth = false,
  type = 'button',
  onClick,
  children,
  ...props
}) {
  const [hov, setHov] = useState(false);
  const [down, setDown] = useState(false);
  const base = {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '6px',
    fontFamily: 'var(--font-sans)',
    fontWeight: 'var(--weight-medium)',
    lineHeight: 'var(--leading-tight)',
    borderRadius: 'var(--radius-md)',
    cursor: disabled || loading ? 'not-allowed' : 'pointer',
    opacity: disabled ? 0.45 : 1,
    transition: 'background var(--duration-base) var(--ease-out), box-shadow var(--duration-base) var(--ease-out), transform var(--duration-fast) var(--ease-out)',
    whiteSpace: 'nowrap',
    width: fullWidth ? '100%' : 'auto',
    outline: 'none',
    border: 'none',
    textDecoration: 'none',
    transform: down && !disabled && !loading ? 'scale(0.975)' : 'scale(1)',
    userSelect: 'none'
  };
  const sizes = {
    xs: {
      padding: '4px 10px',
      fontSize: 'var(--text-xs)'
    },
    sm: {
      padding: '6px 14px',
      fontSize: 'var(--text-sm)'
    },
    md: {
      padding: '9px 20px',
      fontSize: 'var(--text-sm)'
    },
    lg: {
      padding: '12px 24px',
      fontSize: 'var(--text-base)'
    }
  };
  const variants = {
    primary: {
      background: down ? 'var(--color-brand-700)' : hov ? 'var(--color-brand-600)' : 'var(--color-brand-500)',
      color: '#fff',
      border: '1.5px solid transparent',
      boxShadow: hov && !down ? 'var(--shadow-brand)' : 'none'
    },
    secondary: {
      background: down ? 'var(--color-neutral-200)' : hov ? 'var(--color-neutral-100)' : 'var(--bg-base)',
      color: 'var(--text-primary)',
      border: '1.5px solid var(--border-default)',
      boxShadow: 'none'
    },
    ghost: {
      background: down ? 'var(--color-brand-100)' : hov ? 'var(--color-brand-50)' : 'transparent',
      color: 'var(--color-brand-600)',
      border: '1.5px solid transparent',
      boxShadow: 'none'
    },
    accent: {
      background: down ? 'var(--color-accent-700)' : hov ? 'var(--color-accent-600)' : 'var(--color-accent-500)',
      color: '#fff',
      border: '1.5px solid transparent',
      boxShadow: hov && !down ? 'var(--shadow-accent)' : 'none'
    },
    danger: {
      background: down ? 'var(--color-error-700)' : hov ? 'var(--color-error-600)' : 'var(--color-error-500)',
      color: '#fff',
      border: '1.5px solid transparent',
      boxShadow: 'none'
    }
  };
  const vs = disabled ? {
    background: 'var(--color-neutral-100)',
    color: 'var(--color-neutral-400)',
    border: '1.5px solid var(--color-neutral-200)',
    boxShadow: 'none'
  } : variants[variant] || variants.primary;
  const spinner = /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-block',
      width: '1em',
      height: '1em',
      border: '2px solid currentColor',
      borderTopColor: 'transparent',
      borderRadius: '50%',
      animation: 'ys-spin 0.7s linear infinite',
      flexShrink: 0
    }
  });
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("style", null, `@keyframes ys-spin { to { transform: rotate(360deg); } }`), /*#__PURE__*/React.createElement("button", _extends({
    type: type,
    disabled: disabled || loading,
    onClick: onClick,
    onMouseEnter: () => !disabled && !loading && setHov(true),
    onMouseLeave: () => {
      setHov(false);
      setDown(false);
    },
    onMouseDown: () => !disabled && !loading && setDown(true),
    onMouseUp: () => setDown(false),
    style: {
      ...base,
      ...sizes[size],
      ...vs
    }
  }, props), loading && spinner, !loading && icon && iconPosition === 'left' && icon, children, !loading && icon && iconPosition === 'right' && icon));
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Button.jsx", error: String((e && e.message) || e) }); }

// components/core/Card.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const {
  useState
} = React;
/**
 * Surface container for grouped content. The atomic layout unit
 * across teacher dashboard, student app, and video platform.
 */
function Card({
  variant = 'raised',
  padding = 'md',
  radius = 'lg',
  interactive = false,
  selected = false,
  onClick,
  children,
  ...props
}) {
  const [hov, setHov] = useState(false);
  const paddingMap = {
    none: '0',
    xs: 'var(--space-3)',
    sm: 'var(--space-4)',
    md: 'var(--space-5) var(--space-6)',
    lg: 'var(--space-6) var(--space-8)',
    xl: 'var(--space-8) var(--space-10)'
  };
  const radiusMap = {
    sm: 'var(--radius-md)',
    md: 'var(--radius-lg)',
    lg: 'var(--radius-xl)',
    xl: 'var(--radius-2xl)'
  };
  const variantStyles = {
    flat: {
      background: 'var(--bg-subtle)',
      border: 'none',
      boxShadow: 'none'
    },
    raised: {
      background: 'var(--surface-raised)',
      border: '1px solid var(--border-subtle)',
      boxShadow: interactive && hov ? 'var(--shadow-md)' : 'var(--shadow-sm)'
    },
    bordered: {
      background: 'var(--surface-raised)',
      border: `${selected ? '2px solid var(--color-brand-500)' : '1.5px solid var(--border-default)'}`,
      boxShadow: 'none'
    },
    brand: {
      background: 'var(--color-brand-500)',
      border: 'none',
      boxShadow: interactive && hov ? 'var(--shadow-brand)' : 'var(--shadow-sm)',
      color: '#fff'
    },
    success: {
      background: 'var(--surface-success)',
      border: '1px solid var(--color-success-200)',
      boxShadow: 'none'
    },
    warning: {
      background: 'var(--surface-warning)',
      border: '1px solid var(--color-warning-100)',
      boxShadow: 'none'
    },
    error: {
      background: 'var(--surface-error)',
      border: '1px solid var(--color-error-200)',
      boxShadow: 'none'
    }
  };
  return /*#__PURE__*/React.createElement("div", _extends({
    onClick: onClick,
    onMouseEnter: () => interactive && setHov(true),
    onMouseLeave: () => interactive && setHov(false),
    style: {
      padding: paddingMap[padding] || paddingMap.md,
      borderRadius: radiusMap[radius] || radiusMap.md,
      transition: 'box-shadow var(--duration-base) var(--ease-out), transform var(--duration-base) var(--ease-out), border-color var(--duration-base) var(--ease-out)',
      transform: interactive && hov ? 'translateY(-1px)' : 'translateY(0)',
      cursor: interactive ? 'pointer' : 'default',
      boxSizing: 'border-box',
      ...(variantStyles[variant] || variantStyles.raised)
    }
  }, props), children);
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Card.jsx", error: String((e && e.message) || e) }); }

// components/core/Input.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const {
  useState
} = React;
/**
 * Text input with label, hint, error states.
 * Supports prefix/suffix slots for icons, units, or currency.
 */
function Input({
  label,
  hint,
  error,
  size = 'md',
  type = 'text',
  disabled = false,
  placeholder,
  value,
  defaultValue,
  onChange,
  prefix,
  suffix,
  required,
  id,
  ...props
}) {
  const [focused, setFocused] = useState(false);
  const inputId = id || (label ? `ys-input-${label.replace(/\s/g, '-')}` : undefined);
  const sizes = {
    sm: {
      inputPad: '6px 10px',
      labelSize: 'var(--text-xs)',
      hintSize: 'var(--text-xs)'
    },
    md: {
      inputPad: '9px 12px',
      labelSize: 'var(--text-sm)',
      hintSize: 'var(--text-xs)'
    },
    lg: {
      inputPad: '12px 14px',
      labelSize: 'var(--text-sm)',
      hintSize: 'var(--text-sm)'
    }
  };
  const s = sizes[size] || sizes.md;
  const hasError = !!error;
  const borderColor = hasError ? 'var(--color-error-500)' : focused ? 'var(--color-brand-500)' : 'var(--border-default)';
  const ringColor = hasError ? 'var(--color-error-100)' : 'var(--color-brand-100)';
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: '5px',
      width: '100%'
    }
  }, label && /*#__PURE__*/React.createElement("label", {
    htmlFor: inputId,
    style: {
      fontSize: s.labelSize,
      fontFamily: 'var(--font-sans)',
      fontWeight: 'var(--weight-medium)',
      color: hasError ? 'var(--color-error-600)' : 'var(--text-primary)',
      lineHeight: 'var(--leading-snug)'
    }
  }, label, required && /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--color-error-500)',
      marginLeft: '2px'
    }
  }, "*")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      padding: s.inputPad,
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--text-sm)',
      background: disabled ? 'var(--color-neutral-50)' : 'var(--bg-base)',
      border: `1.5px solid ${borderColor}`,
      borderRadius: 'var(--radius-md)',
      boxShadow: focused ? `0 0 0 3px ${ringColor}` : 'none',
      transition: 'border-color var(--duration-base) var(--ease-out), box-shadow var(--duration-base) var(--ease-out)',
      opacity: disabled ? 0.6 : 1
    }
  }, prefix && /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--text-secondary)',
      flexShrink: 0,
      display: 'flex',
      alignItems: 'center'
    }
  }, prefix), /*#__PURE__*/React.createElement("input", _extends({
    id: inputId,
    type: type,
    disabled: disabled,
    placeholder: placeholder,
    value: value,
    defaultValue: defaultValue,
    onChange: onChange,
    required: required,
    onFocus: () => setFocused(true),
    onBlur: () => setFocused(false),
    style: {
      flex: 1,
      border: 'none',
      outline: 'none',
      background: 'transparent',
      fontSize: 'inherit',
      fontFamily: 'inherit',
      color: 'var(--text-primary)',
      padding: 0,
      minWidth: 0
    }
  }, props)), suffix && /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--text-secondary)',
      flexShrink: 0,
      display: 'flex',
      alignItems: 'center'
    }
  }, suffix)), (hint || error) && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: s.hintSize,
      fontFamily: 'var(--font-sans)',
      color: hasError ? 'var(--color-error-600)' : 'var(--text-secondary)',
      lineHeight: 'var(--leading-normal)'
    }
  }, error || hint));
}
Object.assign(__ds_scope, { Input });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Input.jsx", error: String((e && e.message) || e) }); }

// components/core/ProgressBar.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const {
  useEffect,
  useState
} = React;
/**
 * Horizontal progress bar for learning progress, assignment completion,
 * and quiz scores throughout 易數教室.
 */
function ProgressBar({
  value = 0,
  max = 100,
  size = 'md',
  variant = 'brand',
  label,
  showValue = false,
  valueFormat,
  animated = true,
  ...props
}) {
  const [displayed, setDisplayed] = useState(0);
  useEffect(() => {
    // Animate in on mount
    const t = setTimeout(() => setDisplayed(value), 50);
    return () => clearTimeout(t);
  }, [value]);
  const pct = Math.min(100, Math.max(0, displayed / max * 100));
  const heights = {
    xs: 4,
    sm: 6,
    md: 8,
    lg: 12,
    xl: 16
  };
  const h = heights[size] || heights.md;
  const colors = {
    brand: 'var(--color-brand-500)',
    accent: 'var(--color-accent-500)',
    success: 'var(--color-success-500)',
    warning: 'var(--color-warning-500)',
    error: 'var(--color-error-500)'
  };
  const formattedValue = valueFormat ? valueFormat(displayed, max) : `${Math.round(pct)}%`;
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: '6px',
      width: '100%'
    }
  }, props), (label || showValue) && /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'baseline'
    }
  }, label && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--text-sm)',
      fontFamily: 'var(--font-sans)',
      fontWeight: 'var(--weight-medium)',
      color: 'var(--text-secondary)',
      lineHeight: 'var(--leading-tight)'
    }
  }, label), showValue && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--text-xs)',
      fontFamily: 'var(--font-mono)',
      fontWeight: 'var(--weight-medium)',
      color: 'var(--text-primary)',
      letterSpacing: 'var(--tracking-wide)'
    }
  }, formattedValue)), /*#__PURE__*/React.createElement("div", {
    style: {
      height: h,
      borderRadius: 'var(--radius-full)',
      background: 'var(--color-neutral-100)',
      overflow: 'hidden',
      position: 'relative'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      height: '100%',
      width: `${pct}%`,
      borderRadius: 'var(--radius-full)',
      background: colors[variant] || colors.brand,
      transition: animated ? `width var(--duration-slower) var(--ease-smooth)` : 'none'
    }
  })));
}
Object.assign(__ds_scope, { ProgressBar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/ProgressBar.jsx", error: String((e && e.message) || e) }); }

// components/core/Tag.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const {
  useState
} = React;
/**
 * Filterable pill tag for subjects, topics, and difficulty labels.
 * Supports an optional remove (×) button for tag-input patterns.
 */
function Tag({
  variant = 'neutral',
  size = 'md',
  onRemove,
  icon,
  children,
  onClick,
  ...props
}) {
  const [hov, setHov] = useState(false);
  const colors = {
    neutral: {
      bg: hov ? 'var(--color-neutral-200)' : 'var(--color-neutral-100)',
      text: 'var(--color-neutral-700)',
      border: 'var(--color-neutral-200)'
    },
    brand: {
      bg: hov ? 'var(--color-brand-100)' : 'var(--color-brand-50)',
      text: 'var(--color-brand-700)',
      border: 'var(--color-brand-200)'
    },
    accent: {
      bg: hov ? 'var(--color-accent-100)' : 'var(--color-accent-50)',
      text: 'var(--color-accent-700)',
      border: 'var(--color-accent-200)'
    },
    success: {
      bg: hov ? 'var(--color-success-100)' : 'var(--color-success-50)',
      text: 'var(--color-success-700)',
      border: 'var(--color-success-200)'
    },
    error: {
      bg: hov ? 'var(--color-error-100)' : 'var(--color-error-50)',
      text: 'var(--color-error-600)',
      border: 'var(--color-error-200)'
    }
  };
  const sizes = {
    sm: {
      padding: '2px 8px',
      fontSize: 'var(--text-xs)',
      gap: '4px'
    },
    md: {
      padding: '4px 10px',
      fontSize: 'var(--text-sm)',
      gap: '5px'
    }
  };
  const c = colors[variant] || colors.neutral;
  const s = sizes[size] || sizes.md;
  const isInteractive = !!onClick || !!onRemove;
  return /*#__PURE__*/React.createElement("span", _extends({
    onClick: onClick,
    onMouseEnter: () => setHov(true),
    onMouseLeave: () => setHov(false),
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: s.gap,
      padding: s.padding,
      fontSize: s.fontSize,
      fontFamily: 'var(--font-sans)',
      fontWeight: 'var(--weight-medium)',
      lineHeight: '1.4',
      borderRadius: 'var(--radius-full)',
      background: c.bg,
      color: c.text,
      border: `1px solid ${c.border}`,
      transition: 'background var(--duration-fast) var(--ease-out)',
      whiteSpace: 'nowrap',
      cursor: isInteractive ? 'pointer' : 'default',
      userSelect: 'none'
    }
  }, props), icon && /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'flex',
      alignItems: 'center',
      flexShrink: 0
    }
  }, icon), children, onRemove && /*#__PURE__*/React.createElement("button", {
    onClick: e => {
      e.stopPropagation();
      onRemove();
    },
    style: {
      background: 'none',
      border: 'none',
      cursor: 'pointer',
      padding: '0 0 0 2px',
      display: 'flex',
      alignItems: 'center',
      color: 'inherit',
      opacity: 0.55,
      fontSize: '1.1em',
      lineHeight: 1,
      fontFamily: 'inherit'
    },
    "aria-label": "\u79FB\u9664"
  }, "\xD7"));
}
Object.assign(__ds_scope, { Tag });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Tag.jsx", error: String((e && e.message) || e) }); }

__ds_ns.Avatar = __ds_scope.Avatar;

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.Input = __ds_scope.Input;

__ds_ns.ProgressBar = __ds_scope.ProgressBar;

__ds_ns.Tag = __ds_scope.Tag;

})();
