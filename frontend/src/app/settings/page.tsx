"use client";

import * as React from "react";
import { SplitWorkspace } from "@/components/layout/split-workspace";
import { SettingsSection, SettingsRow } from "@/components/settings/settings-section";
import { ApiKeyInput } from "@/components/settings/api-key-input";
import { Settings as SettingsIcon, Cpu, Key, Monitor, Moon, Save } from "lucide-react";
import { cn } from "@/lib/utils";

const NAV_LINKS = [
  { id: "general", label: "General", icon: Monitor },
  { id: "models", label: "AI Models", icon: Cpu },
  { id: "api-keys", label: "API Keys", icon: Key },
];

export default function SettingsPage() {
  const [activeSection, setActiveSection] = React.useState("general");

  const scrollToSection = (id: string) => {
    setActiveSection(id);
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: "smooth" });
    }
  };

  const ContextPanel = (
    <div className="flex flex-col h-full bg-transparent p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 bg-gray-500/10 rounded-lg">
          <SettingsIcon className="w-5 h-5 text-gray-400" />
        </div>
        <div>
          <h2 className="text-sm font-semibold tracking-tight text-white">Settings</h2>
          <p className="text-xs text-gray-500">Preferences & Config</p>
        </div>
      </div>
      
      <nav className="flex flex-col gap-1">
        {NAV_LINKS.map((link) => (
          <button
            key={link.id}
            onClick={() => scrollToSection(link.id)}
            className={cn(
              "flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors text-left",
              activeSection === link.id 
                ? "bg-[#1A1A1A] text-white" 
                : "text-gray-500 hover:text-gray-300 hover:bg-white/5"
            )}
          >
            <link.icon className={cn("w-4 h-4", activeSection === link.id ? "text-blue-400" : "")} />
            {link.label}
          </button>
        ))}
      </nav>
    </div>
  );

  return (
    <SplitWorkspace contextPanel={ContextPanel}>
      <div className="flex flex-col h-full bg-transparent overflow-y-auto">
        <header className="h-14 border-b border-border bg-background/80 backdrop-blur-xl sticky top-0 z-20 flex items-center justify-between px-6 shrink-0">
          <h1 className="font-medium text-[14px]">System Preferences</h1>
        </header>

        <div className="p-6 md:p-10 max-w-4xl mx-auto w-full space-y-12 pb-24">
          
          <SettingsSection 
            id="general"
            title="General Settings" 
            description="Manage your overarching system preferences."
          >
            <SettingsRow 
              label="Theme Preference" 
              description="SovereignAI defaults to a dark aesthetic for optimal focus."
            >
              <div className="flex items-center gap-2 p-1 bg-[#121212] border border-white/5 rounded-lg">
                <button className="flex items-center justify-center gap-2 px-4 py-1.5 bg-white/10 text-white rounded-md text-xs font-medium shadow-sm border border-white/5">
                  <Moon className="w-3.5 h-3.5" /> Dark
                </button>
              </div>
            </SettingsRow>
          </SettingsSection>

          <SettingsSection 
            id="models"
            title="AI Models (Local)" 
            description="Configure which local LLM handles inference via Ollama."
          >
            <SettingsRow 
              label="Active Model" 
              description="The primary model used for the chat agent and reasoning."
            >
              <select className="w-full sm:w-64 h-9 bg-[#121212] border border-white/10 rounded-md px-3 py-1 text-sm text-gray-200 focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50">
                <option value="qwen2.5:0.5b">Qwen 2.5 (0.5B)</option>
                <option value="llama3">Llama 3 (8B)</option>
                <option value="phi3">Phi-3 Mini</option>
              </select>
            </SettingsRow>
            
            <div className="h-px w-full bg-white/5" />
            
            <SettingsRow 
              label="Embedding Model" 
              description="Used by Qdrant for semantic search vectorization."
            >
              <select className="w-full sm:w-64 h-9 bg-[#121212] border border-white/10 rounded-md px-3 py-1 text-sm text-gray-200 focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50">
                <option value="nomic-embed-text">Nomic Embed Text</option>
                <option value="all-minilm">All-MiniLM-L6-v2</option>
              </select>
            </SettingsRow>
          </SettingsSection>

          <SettingsSection 
            id="api-keys"
            title="External API Keys" 
            description="Configure fallback providers for complex reasoning tasks."
          >
            <SettingsRow 
              label="OpenAI API Key" 
              description="Used as a fallback when local models struggle with a prompt."
            >
              <ApiKeyInput placeholder="sk-proj-..." />
            </SettingsRow>
            
            <div className="h-px w-full bg-white/5" />
            
            <SettingsRow 
              label="Anthropic API Key" 
              description="Used for Claude 3.5 Sonnet integrations."
            >
              <ApiKeyInput placeholder="sk-ant-..." />
            </SettingsRow>
          </SettingsSection>

        </div>
      </div>
    </SplitWorkspace>
  );
}
