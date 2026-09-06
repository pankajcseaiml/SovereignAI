import * as React from "react";
import { cn } from "@/lib/utils";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost";
  size?: "sm" | "md" | "lg" | "icon";
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center rounded-md text-sm font-medium transition-all active:scale-95 disabled:opacity-50 disabled:pointer-events-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/50",
          {
            "bg-primary text-white shadow-sm hover:brightness-110": variant === "primary",
            "bg-surface text-foreground hover:bg-surface-hover": variant === "secondary",
            "border border-border bg-transparent hover:bg-surface text-foreground": variant === "outline",
            "bg-transparent hover:bg-surface text-muted hover:text-foreground": variant === "ghost",
            "h-8 px-3 text-xs": size === "sm",
            "h-9 px-4": size === "md",
            "h-11 px-6": size === "lg",
            "h-9 w-9 p-0": size === "icon",
          },
          className
        )}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";

export { Button };
