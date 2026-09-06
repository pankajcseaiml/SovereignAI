import * as React from "react";
import { CheckCircle2, Circle, Loader2, ArrowRight } from "lucide-react";
import { cn } from "@/lib/utils";
import { Step } from "@/types/chat";

export function AgentProgress({ steps, isRunning }: { steps: Step[]; isRunning: boolean }) {
  return (
    <div className="flex flex-col h-full bg-surface/30">
      <div className="p-5 border-b border-white/5 flex items-center justify-between">
        <h3 className="text-[13px] font-semibold tracking-tight text-[#EDEDED]">Agent Execution</h3>
        {isRunning && (
          <div className="flex items-center gap-2 bg-blue-500/10 px-2.5 py-1 rounded-full border border-blue-500/20">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
            </span>
            <span className="text-xs text-muted font-medium">Running</span>
          </div>
        )}
      </div>
      
      <div className="flex-1 overflow-y-auto p-5 space-y-5 scrollbar-hide">
        {steps.map((step, idx) => (
          <div key={step.id} className="relative flex items-start group">
            {/* Connector Line */}
            {idx !== steps.length - 1 && (
              <div 
                className={cn(
                  "absolute left-[9px] top-6 w-[2px] h-[calc(100%+8px)] transition-colors duration-300",
                  step.status === "completed" ? "bg-primary/30" : "bg-white/5"
                )}
              />
            )}
            
            <div className="flex flex-col z-10">
              <div className="flex items-center justify-center w-5 h-5 bg-transparent rounded-full mt-0.5">
                {step.status === "completed" && <CheckCircle2 className="w-[18px] h-[18px] text-primary" />}
                {step.status === "running" && <Loader2 className="w-[18px] h-[18px] text-primary animate-spin" />}
                {step.status === "pending" && <Circle className="w-[18px] h-[18px] text-white/20" />}
                {step.status === "error" && <Circle className="w-[18px] h-[18px] text-red-500" fill="currentColor" />}
              </div>
            </div>
            
            <div className="ml-4 flex flex-col pt-0.5">
              <span className={cn(
                "text-[13px] font-medium transition-colors duration-300 leading-tight",
                step.status === "completed" ? "text-[#EDEDED]" : 
                step.status === "running" ? "text-primary" : "text-[#A1A1A1]"
              )}>
                {step.label}
              </span>
              {step.duration && (
                <span className="text-[11px] text-[#A1A1A1]/60 mt-1.5 font-mono">{step.duration}</span>
              )}
            </div>
          </div>
        ))}
      </div>
      
      <div className="p-5 border-t border-white/5 mt-auto bg-background/50 backdrop-blur-md">
        <div className="rounded-xl border border-white/10 bg-[#121212] p-4 flex items-start gap-3 shadow-[0_4px_12px_rgba(0,0,0,0.2)] hover:border-white/20 transition-colors cursor-pointer group">
           <div className="mt-0.5 bg-[#1A1A1A] p-1.5 rounded-lg border border-white/5 group-hover:bg-primary/10 group-hover:text-primary transition-colors">
             <ArrowRight className="w-[14px] h-[14px] text-[#A1A1A1] group-hover:text-primary" />
           </div>
           <div className="flex flex-col">
             <span className="text-[11px] text-[#A1A1A1] font-medium uppercase tracking-wider">Latest Artifact</span>
             <span className="text-[13px] text-[#EDEDED] font-medium mt-1 truncate max-w-[200px]">Approval_Note.docx</span>
           </div>
        </div>
      </div>
    </div>
  );
}
