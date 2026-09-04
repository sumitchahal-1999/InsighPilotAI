import React from "react";
import { cn } from "@/lib/utils";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost";
  size?: "sm" | "md" | "lg";
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", children, ...props }, ref) => {
    const variantStyles = {
      primary: "bg-primary text-background font-bold hover:bg-primary-dark shadow-glow",
      secondary: "bg-surface-bright text-on-surface hover:bg-surface-container-high border border-outline-variant",
      outline: "bg-transparent text-primary border border-primary/40 hover:bg-primary/10",
      ghost: "bg-transparent text-on-surface-variant hover:text-on-surface hover:bg-surface-bright/20",
    };

    const sizeStyles = {
      sm: "px-3 py-1.5 text-xs rounded-md",
      md: "px-4 py-2 text-sm rounded-lg",
      lg: "px-6 py-3 text-base rounded-xl font-semibold",
    };

    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center gap-2 font-mono uppercase tracking-wider transition-all duration-150 active:scale-[0.98] disabled:opacity-50 cursor-pointer",
          variantStyles[variant],
          sizeStyles[size],
          className
        )}
        {...props}
      >
        {children}
      </button>
    );
  }
);

Button.displayName = "Button";
