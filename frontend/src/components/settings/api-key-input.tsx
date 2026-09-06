"use client";

import * as React from "react";
import { Eye, EyeOff, Save, Check } from "lucide-react";
import { cn } from "@/lib/utils";

interface ApiKeyInputProps {
  initialValue?: string;
  placeholder?: string;
  onSave?: (value: string) => void;
}

export function ApiKeyInput({ initialValue = "", placeholder = "sk-...", onSave }: ApiKeyInputProps) {
  const [value, setValue] = React.useState(initialValue);
  const [isVisible, setIsVisible] = React.useState(false);
  const [isSaved, setIsSaved] = React.useState(false);

  const handleSave = () => {
    if (onSave) {
      onSave(value);
    }
    setIsSaved(true);
    setTimeout(() => setIsSaved(false), 2000);
  };

  return (
    <div className="flex w-full gap-2 relative group">
      <div className="relative flex-1">
        <input
          type={isVisible ? "text" : "password"}
          value={value}
          onChange={(e) => {
            setValue(e.target.value);
            setIsSaved(false);
          }}
          placeholder={placeholder}
          className="w-full h-9 bg-[#121212] border border-white/10 rounded-md px-3 py-1 text-sm text-gray-200 placeholder:text-gray-600 focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 transition-all font-mono"
        />
        <button
          type="button"
          onClick={() => setIsVisible(!isVisible)}
          className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300 transition-colors"
        >
          {isVisible ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
        </button>
      </div>
      
      <button
        type="button"
        onClick={handleSave}
        disabled={value === initialValue && !isSaved}
        className={cn(
          "h-9 px-3 rounded-md flex items-center justify-center text-sm font-medium transition-all shadow-sm flex-shrink-0 min-w-[70px]",
          isSaved 
            ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/20" 
            : value !== initialValue
              ? "bg-white text-black hover:bg-gray-200"
              : "bg-[#1A1A1A] text-gray-500 border border-white/5 cursor-not-allowed"
        )}
      >
        {isSaved ? <Check className="w-4 h-4" /> : <span className="flex items-center gap-1.5"><Save className="w-3.5 h-3.5" /> Save</span>}
      </button>
    </div>
  );
}
