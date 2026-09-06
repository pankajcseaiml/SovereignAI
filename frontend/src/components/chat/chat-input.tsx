import * as React from "react";
import { Button } from "@/components/ui/button";
import { Paperclip, ChevronUp } from "lucide-react";
import { useChatStore } from "@/store/chat-store";
import axios from "axios";

export function ChatInput() {
  const [input, setInput] = React.useState("");
  const { sendMessage } = useChatStore();
  const fileInputRef = React.useRef<HTMLInputElement>(null);

  const handleSend = () => {
    if (!input.trim()) return;
    sendMessage(input);
    setInput("");
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      // Show optimistic message
      sendMessage(`[Uploading file: ${file.name}...]`);
      
      await axios.post("http://localhost:8001/api/v1/documents/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      
      // We could add another message saying upload success, but backend response is enough for now
    } catch (err) {
      console.error("Upload failed", err);
    }
  };

  return (
    <div className="p-6 pt-0 bg-transparent sticky bottom-0 w-full flex justify-center">
      <div className="w-full max-w-3xl relative">
        <div className="overflow-hidden rounded-2xl border border-white/10 bg-[#0A0A0A] shadow-[0_-8px_30px_rgba(0,0,0,0.4)] focus-within:ring-1 focus-within:ring-white/20 focus-within:border-white/20 transition-all">
          <textarea
            className="w-full resize-none bg-transparent px-5 py-4 text-[15px] placeholder:text-[#A1A1A1] focus:outline-none min-h-[60px] max-h-40 scrollbar-hide text-[#EDEDED]"
            placeholder="Ask SovereignAI or upload a document..."
            rows={1}
            style={{ minHeight: "56px" }}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <div className="flex items-center justify-between p-3 pt-0">
            <div className="flex items-center gap-1">
              <input 
                type="file" 
                ref={fileInputRef} 
                className="hidden" 
                onChange={handleFileUpload} 
              />
              <Button 
                variant="ghost" 
                size="icon" 
                className="h-8 w-8 text-[#A1A1A1] hover:text-[#EDEDED] hover:bg-[#121212]"
                onClick={() => fileInputRef.current?.click()}
              >
                <Paperclip className="w-4 h-4" />
              </Button>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-[11px] text-[#A1A1A1]/60 font-medium hidden sm:inline-block mr-2">Use Shift + Enter for new line</span>
              <Button 
                size="icon" 
                className="h-8 w-8 rounded-lg bg-primary hover:bg-blue-600 text-white transition-colors"
                onClick={handleSend}
              >
                <ChevronUp className="w-5 h-5" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
