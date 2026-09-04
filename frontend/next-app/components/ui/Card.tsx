import React from "react";
import { cn } from "@/lib/utils";

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  glow?: boolean;
}

export function Card({ className, glow = false, children, ...props }: CardProps) {
  return (
    <div
      className={cn(
        "glass-panel rounded-xl p-5 relative overflow-hidden",
        glow && "border-primary/30 shadow-glow",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}
