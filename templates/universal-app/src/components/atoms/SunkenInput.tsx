import React, { InputHTMLAttributes, forwardRef, useId } from 'react';

export interface SunkenInputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  helperText?: string;
  errorText?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const SunkenInput = forwardRef<HTMLInputElement, SunkenInputProps>(
  ({ label, helperText, errorText, leftIcon, rightIcon, className = '', id, ...props }, ref) => {
    const generatedId = useId();
    const inputId = id || generatedId;
    const isError = Boolean(errorText);

    return (
      <div className="flex flex-col gap-1.5 w-full">
        {label && (
          <label
            htmlFor={inputId}
            className="text-xs font-medium tracking-wide text-[var(--text-secondary)] select-none"
          >
            {label}
          </label>
        )}

        <div className="relative flex items-center w-full">
          {leftIcon && (
            <div className="absolute left-3.5 flex items-center pointer-events-none text-[var(--text-muted)] shrink-0">
              {leftIcon}
            </div>
          )}

          <input
            ref={ref}
            id={inputId}
            aria-invalid={isError}
            aria-describedby={
              isError ? `${inputId}-error` : helperText ? `${inputId}-helper` : undefined
            }
            className={`
              w-full h-11 px-4
              ${leftIcon ? 'pl-10' : ''}
              ${rightIcon ? 'pr-10' : ''}
              bg-[var(--surface-sunken)]
              text-[var(--text-primary)]
              placeholder:text-[var(--text-muted)]
              text-sm
              rounded-xl
              border border-[var(--border-subtle)]
              shadow-[var(--shadow-tactile-inset)]
              transition-all duration-150 ease-out
              focus-visible:outline-none
              focus-visible:border-[var(--accent-action)]
              focus-visible:ring-2
              focus-visible:ring-[var(--accent-focus)]
              focus-visible:ring-offset-2
              focus-visible:ring-offset-[var(--canvas-bg)]
              disabled:opacity-50 disabled:cursor-not-allowed
              ${isError ? 'border-[var(--status-danger)] focus-visible:ring-[var(--status-danger)]' : ''}
              ${className}
            `}
            {...props}
          />

          {rightIcon && (
            <div className="absolute right-3.5 flex items-center pointer-events-none text-[var(--text-muted)] shrink-0">
              {rightIcon}
            </div>
          )}
        </div>

        {errorText ? (
          <span id={`${inputId}-error`} className="text-xs text-[var(--status-danger)] font-medium">
            {errorText}
          </span>
        ) : helperText ? (
          <span id={`${inputId}-helper`} className="text-xs text-[var(--text-muted)]">
            {helperText}
          </span>
        ) : null}
      </div>
    );
  }
);

SunkenInput.displayName = 'SunkenInput';
