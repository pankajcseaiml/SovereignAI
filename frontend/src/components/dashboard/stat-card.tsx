import * as React from "react";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { LucideIcon } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string;
  change?: string;
  isPositive?: boolean;
  icon: LucideIcon;
  iconColor?: string;
  iconBgColor?: string;
}

export function StatCard({ 
  title, 
  value, 
  change, 
  isPositive = true, 
  icon: Icon,
  iconColor = "text-blue-400",
  iconBgColor = "bg-blue-500/10"
}: StatCardProps) {
  return (
    <Card className="bg-[#0A0A0A] border-white/10 hover:border-white/20 transition-all duration-300 p-5 overflow-hidden relative group">
      <div className="absolute inset-0 bg-gradient-to-br from-white/[0.02] to-transparent pointer-events-none" />
      
      <div className="flex items-center justify-between z-10 relative mb-4">
        <h3 className="text-sm font-medium text-gray-400">{title}</h3>
        <div className={cn("p-2 rounded-lg", iconBgColor)}>
          <Icon className={cn("w-4 h-4", iconColor)} />
        </div>
      </div>
      
      <div className="z-10 relative">
        <div className="text-2xl font-semibold text-white tracking-tight">{value}</div>
        {change && (
          <div className="flex items-center mt-1">
            <span className={cn(
              "text-xs font-medium px-1.5 py-0.5 rounded-sm mr-2",
              isPositive ? "text-emerald-400 bg-emerald-500/10" : "text-red-400 bg-red-500/10"
            )}>
              {isPositive ? "+" : ""}{change}
            </span>
            <span className="text-xs text-gray-500">from last week</span>
          </div>
        )}
      </div>
    </Card>
  );
}
