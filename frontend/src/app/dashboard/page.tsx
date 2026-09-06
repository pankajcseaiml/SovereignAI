"use client";

import * as React from "react";
import { SplitWorkspace } from "@/components/layout/split-workspace";
import { Activity, Users, Database, Zap, Clock, ShieldCheck } from "lucide-react";
import { StatCard } from "@/components/dashboard/stat-card";
import { UsageChart } from "@/components/dashboard/usage-chart";

export default function DashboardPage() {
  const ContextPanel = (
    <div className="flex flex-col h-full bg-transparent p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 bg-purple-500/10 rounded-lg">
          <Activity className="w-5 h-5 text-purple-400" />
        </div>
        <div>
          <h2 className="text-sm font-semibold tracking-tight text-white">System Status</h2>
          <p className="text-xs text-gray-500">Live Telemetry</p>
        </div>
      </div>
      
      <div className="bg-[#121212] rounded-xl p-4 border border-white/5 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-xs font-medium text-gray-400">Database</span>
          </div>
          <span className="text-xs font-medium text-emerald-400">Connected</span>
        </div>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-xs font-medium text-gray-400">Qdrant Vector DB</span>
          </div>
          <span className="text-xs font-medium text-emerald-400">Connected</span>
        </div>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-xs font-medium text-gray-400">Ollama API</span>
          </div>
          <span className="text-xs font-medium text-emerald-400">Connected</span>
        </div>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-xs font-medium text-gray-400">Celery Worker</span>
          </div>
          <span className="text-xs font-medium text-emerald-400">Online</span>
        </div>
      </div>
    </div>
  );

  return (
    <SplitWorkspace contextPanel={ContextPanel}>
      <div className="flex flex-col h-full bg-transparent overflow-y-auto">
        <header className="h-14 border-b border-border bg-background/80 backdrop-blur-xl sticky top-0 z-20 flex items-center justify-between px-6 shrink-0">
          <h1 className="font-medium text-[14px]">Analytics Dashboard</h1>
        </header>

        <div className="p-6 md:p-8 max-w-6xl mx-auto w-full space-y-8">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <StatCard 
              title="Active Sessions" 
              value="12" 
              change="2.5%" 
              icon={Users} 
              iconColor="text-blue-400"
              iconBgColor="bg-blue-500/10"
            />
            <StatCard 
              title="Documents Indexed" 
              value="1,284" 
              change="18.2%" 
              icon={Database} 
              iconColor="text-purple-400"
              iconBgColor="bg-purple-500/10"
            />
            <StatCard 
              title="Avg. Response Time" 
              value="1.2s" 
              change="0.4s"
              isPositive={false} 
              icon={Zap} 
              iconColor="text-yellow-400"
              iconBgColor="bg-yellow-500/10"
            />
            <StatCard 
              title="System Uptime" 
              value="99.9%" 
              icon={ShieldCheck} 
              iconColor="text-emerald-400"
              iconBgColor="bg-emerald-500/10"
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <UsageChart />
            </div>
            
            <div className="flex flex-col gap-6">
              <div className="bg-[#0A0A0A] border border-white/10 rounded-xl p-6 flex-1 relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-white/[0.02] to-transparent pointer-events-none" />
                <h3 className="text-sm font-medium text-gray-400 mb-6">Recent Activity</h3>
                
                <div className="space-y-6">
                  <div className="flex gap-4">
                    <div className="w-8 h-8 rounded-full bg-blue-500/10 flex items-center justify-center shrink-0">
                      <Database className="w-4 h-4 text-blue-400" />
                    </div>
                    <div>
                      <p className="text-sm text-gray-200">New document ingested</p>
                      <p className="text-xs text-gray-500 mt-1">2 mins ago • Qdrant sync complete</p>
                    </div>
                  </div>
                  
                  <div className="flex gap-4">
                    <div className="w-8 h-8 rounded-full bg-emerald-500/10 flex items-center justify-center shrink-0">
                      <Users className="w-4 h-4 text-emerald-400" />
                    </div>
                    <div>
                      <p className="text-sm text-gray-200">Agent session completed</p>
                      <p className="text-xs text-gray-500 mt-1">15 mins ago • Qwen2.5-0.5B</p>
                    </div>
                  </div>
                  
                  <div className="flex gap-4">
                    <div className="w-8 h-8 rounded-full bg-yellow-500/10 flex items-center justify-center shrink-0">
                      <Zap className="w-4 h-4 text-yellow-400" />
                    </div>
                    <div>
                      <p className="text-sm text-gray-200">System latency spike detected</p>
                      <p className="text-xs text-gray-500 mt-1">2 hours ago • Auto-resolved</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </SplitWorkspace>
  );
}
