import * as React from "react";
import Link from "next/link";
import { MessageSquare, LayoutDashboard, FileText, Database, Settings, Activity } from "lucide-react";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { icon: LayoutDashboard, label: "Dashboard", href: "/dashboard" },
  { icon: MessageSquare, label: "Agents", href: "/chat" },
  { icon: FileText, label: "Documents", href: "/documents" },
  { icon: Database, label: "Knowledge", href: "/knowledge-base" },
  { icon: Activity, label: "Monitoring", href: "/monitoring/network" },
];

export function Sidebar() {
  return (
    <aside className="w-16 md:w-[220px] bg-transparent flex flex-col h-full flex-shrink-0 transition-all duration-300 relative z-0">
      <div className="h-14 flex items-center justify-center md:justify-start md:px-6">
        <div className="w-5 h-5 rounded-md bg-gradient-to-br from-primary to-blue-700 flex-shrink-0 shadow-sm" />
        <span className="ml-3 font-semibold hidden md:block tracking-tight text-[#EDEDED]">SovereignAI</span>
      </div>
      
      <nav className="flex-1 flex flex-col gap-2 p-3">
        {NAV_ITEMS.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={cn(
              "flex items-center justify-center md:justify-start h-9 px-0 md:px-3 mx-2 rounded-md transition-all duration-200",
              item.label === "Agents" 
                ? "bg-[#1A1A1A] text-white shadow-sm ring-1 ring-white/5" 
                : "text-[#A1A1A1] hover:text-white hover:bg-[#121212]",
              "active:scale-95"
            )}
          >
            <item.icon className="w-[18px] h-[18px] flex-shrink-0" />
            <span className="ml-3 text-[13px] font-medium hidden md:block">{item.label}</span>
          </Link>
        ))}
      </nav>
      
      <div className="p-3 mt-auto">
        <Link
          href="/settings"
          className="flex items-center justify-center md:justify-start h-9 px-0 md:px-3 mx-2 rounded-md text-[#A1A1A1] hover:text-white hover:bg-[#121212] transition-colors active:scale-95"
        >
          <Settings className="w-[18px] h-[18px] flex-shrink-0" />
          <span className="ml-3 text-[13px] font-medium hidden md:block">Settings</span>
        </Link>
      </div>
    </aside>
  );
}
