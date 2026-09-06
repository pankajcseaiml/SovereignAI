import * as React from "react";
import { cn } from "@/lib/utils";

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "secondary" | "outline" | "success" | "warning";
}

function Badge({ className, variant = "default", ...props }: BadgeProps) {
  return (
    <div
      className={cn(
        "inline-flex items-center rounded-sm px-2 py-0.5 text-xs font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2",
        {
          "bg-primary text-primary-foreground": variant === "default",
          "bg-surface-hover text-foreground": variant === "secondary",
          "border border-border text-foreground": variant === "outline",
          "bg-emerald-500/10 text-emerald-500 border border-emerald-500/20": variant === "success",
          "bg-amber-500/10 text-amber-500 border border-amber-500/20": variant === "warning",
        },
        className
      )}
      {...props}
    />
  );
}

export { Badge };
