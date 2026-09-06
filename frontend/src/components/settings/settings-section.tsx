import * as React from "react";
import { cn } from "@/lib/utils";

interface SettingsSectionProps {
  id?: string;
  title: string;
  description: string;
  children: React.ReactNode;
  className?: string;
}

export function SettingsSection({ id, title, description, children, className }: SettingsSectionProps) {
  return (
    <section id={id} className={cn("space-y-6 scroll-mt-24", className)}>
      <div>
        <h3 className="text-lg font-medium text-white">{title}</h3>
        <p className="text-sm text-gray-400 mt-1">{description}</p>
      </div>
      <div className="bg-[#0A0A0A] border border-white/10 rounded-xl overflow-hidden shadow-sm">
        <div className="p-1">
          {children}
        </div>
      </div>
    </section>
  );
}

interface SettingsRowProps {
  label: string;
  description?: string;
  children: React.ReactNode;
  className?: string;
}

export function SettingsRow({ label, description, children, className }: SettingsRowProps) {
  return (
    <div className={cn("flex flex-col sm:flex-row sm:items-center justify-between p-4 gap-4", className)}>
      <div className="flex-1 pr-4">
        <label className="text-sm font-medium text-gray-200 block">{label}</label>
        {description && <p className="text-xs text-gray-500 mt-1">{description}</p>}
      </div>
      <div className="flex-shrink-0 w-full sm:w-auto min-w-[240px]">
        {children}
      </div>
    </div>
  );
}
