import * as React from "react";
import { cn } from "@/lib/utils";
import { Terminal, User } from "lucide-react";
import { MessageProps } from "@/types/chat";

export function MessageList({ messages }: { messages: MessageProps[] }) {
  const scrollRef = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto px-4 md:px-8 py-6 pb-32">
      <div className="max-w-3xl mx-auto space-y-8">
        {messages.map((msg) => (
          <div key={msg.id} className={cn("flex w-full", msg.role === "user" ? "justify-end" : "justify-start")}>
            <div className={cn(
              "flex gap-4 max-w-[700px]",
              msg.role === "user" ? "flex-row-reverse" : "flex-row"
            )}>
              {/* Avatar */}
              <div className={cn(
                "w-7 h-7 rounded-md flex items-center justify-center flex-shrink-0 mt-1 shadow-sm",
                msg.role === "user" ? "bg-[#121212] border border-white/10" : "bg-gradient-to-br from-primary to-blue-700 text-white shadow-md",
                msg.role === "system" && "bg-[#1A1A1A] border border-white/5 text-[#EDEDED]"
              )}>
                {msg.role === "user" ? <User className="w-4 h-4 text-[#A1A1A1]" /> : 
                 msg.role === "system" ? <Terminal className="w-[14px] h-[14px]" /> : 
                 <span className="font-bold text-[10px] tracking-tighter">AI</span>}
              </div>
              
              {/* Content bubble */}
              <div className={cn(
                "px-5 py-3.5 rounded-2xl text-[15px] leading-7",
                msg.role === "user" ? "bg-[#1A1A1A] border border-white/10 text-white shadow-sm rounded-tr-sm" : 
                msg.role === "assistant" ? "bg-transparent text-[#EDEDED]" : 
                "bg-[#121212] border border-white/5 text-[#A1A1A1] font-mono text-[13px] rounded-xl leading-6"
              )}>
                {msg.content}
              </div>
            </div>
          </div>
        ))}
        
        {messages.length === 0 && (
          <div className="h-full min-h-[50vh] flex flex-col items-center justify-center text-center opacity-0 animate-in fade-in duration-1000">
            <div className="w-12 h-12 rounded-xl bg-surface border border-border flex items-center justify-center mb-6 shadow-sm">
              <span className="font-bold text-lg tracking-tighter">AI</span>
            </div>
            <h2 className="text-xl font-semibold tracking-tight">How can I help you today?</h2>
            <p className="text-muted text-sm mt-2 max-w-sm">
              Upload a document, ask a question, or trigger a multi-step agent workflow.
            </p>
          </div>
        )}
        <div ref={scrollRef} />
      </div>
    </div>
  );
}
