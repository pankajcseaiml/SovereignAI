import * as React from "react";
import { Sidebar } from "./sidebar";

export function SplitWorkspace({
  children,
  contextPanel,
}: {
  children: React.ReactNode;
  contextPanel?: React.ReactNode;
}) {
  return (
    <div className="flex h-screen w-full overflow-hidden bg-[#050505] text-foreground">
      <Sidebar />
      <main className="flex-1 flex min-w-0 overflow-hidden rounded-l-2xl border-l border-border bg-background shadow-2xl relative z-10">
        {/* Main Content Area */}
        <div className="flex-1 overflow-auto flex flex-col relative h-full">
          {children}
        </div>
        
        {/* Context Panel (Right Sidebar) */}
        {contextPanel && (
          <aside className="w-[340px] border-l border-border bg-background/50 backdrop-blur-xl hidden lg:flex flex-col h-full flex-shrink-0 z-20 shadow-[-8px_0_24px_-12px_rgba(0,0,0,0.5)]">
            {contextPanel}
          </aside>
        )}
      </main>
    </div>
  );
}
