"use client";

import * as React from "react";
import { SplitWorkspace } from "@/components/layout/split-workspace";
import { ChatInput } from "@/components/chat/chat-input";
import { MessageList } from "@/components/chat/message-list";
import { AgentProgress } from "@/components/chat/agent-progress";
import { Badge } from "@/components/ui/badge";
import { ShieldCheck } from "lucide-react";
import { useChatStore } from "@/store/chat-store";

export default function ChatPage() {
  const { messages, agentSteps, isRunning, connectSocket } = useChatStore();

  React.useEffect(() => {
    // Connect to backend WebSocket for conversation "1"
    connectSocket("1");
  }, [connectSocket]);
  
  const ContextPanel = (
    <div className="flex flex-col h-full bg-transparent">
      <div className="h-14 border-b border-border flex items-center px-5 justify-between">
        <Badge variant="outline" className="gap-1.5 py-1 px-2.5 bg-[#0A0A0A]/50 border-white/10 shadow-sm backdrop-blur-md">
          <ShieldCheck className="w-[14px] h-[14px] text-emerald-500" />
          <span className="font-mono text-[11px] tracking-tight text-[#EDEDED]">0 External Calls</span>
        </Badge>
        <span className="text-[11px] text-[#A1A1A1] font-mono tracking-tighter">SovereignAI v1.0</span>
      </div>
      <div className="flex-1 overflow-hidden">
        <AgentProgress steps={agentSteps} isRunning={isRunning} />
      </div>
    </div>
  );

  return (
    <SplitWorkspace contextPanel={ContextPanel}>
      <div className="flex flex-col h-full relative bg-transparent">
        {/* Top Header */}
        <header className="h-14 border-b border-border bg-background/80 backdrop-blur-xl sticky top-0 z-10 flex items-center px-6 shrink-0">
          <div className="flex items-center gap-3">
            <h1 className="font-medium text-[14px]">Agent Workspace</h1>
            <Badge variant="secondary" className="font-mono text-[11px] bg-[#1A1A1A] text-[#EDEDED] border border-white/5">Qwen3.6-27B</Badge>
          </div>
        </header>
        
        {/* Chat Feed */}
        <MessageList messages={messages} />
        
        {/* Input Area */}
        <ChatInput />
      </div>
    </SplitWorkspace>
  );
}
