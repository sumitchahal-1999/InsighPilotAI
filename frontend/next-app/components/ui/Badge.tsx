import React from "react";
import { cn } from "@/lib/utils";

interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "primary" | "error" | "warning" | "success" | "outline" | "secondary";
}

export function Badge({ className, variant = "primary", children, ...props }: BadgeProps) {
  const variantStyles = {
    primary: "bg-primary-container/30 text-primary border-primary/30",
    error: "bg-error-container/30 text-error border-error/30",
    warning: "bg-warning-container/30 text-warning border-warning/30",
    success: "bg-success-container/30 text-success border-success/30",
    outline: "bg-surface-container text-on-surface-variant border-outline-variant",
    secondary: "bg-secondary-container/30 text-secondary border-secondary/30",
  };

  return (
    <div
      className={cn(
        "inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-mono font-medium border uppercase tracking-wider",
        variantStyles[variant],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}
