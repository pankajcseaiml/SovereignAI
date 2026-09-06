"use client";

import * as React from "react";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { Card } from "@/components/ui/card";

const data = [
  { name: 'Mon', tokens: 4000, latency: 240 },
  { name: 'Tue', tokens: 3000, latency: 139 },
  { name: 'Wed', tokens: 2000, latency: 980 },
  { name: 'Thu', tokens: 2780, latency: 390 },
  { name: 'Fri', tokens: 1890, latency: 480 },
  { name: 'Sat', tokens: 2390, latency: 380 },
  { name: 'Sun', tokens: 3490, latency: 430 },
];

export function UsageChart() {
  return (
    <Card className="bg-[#0A0A0A] border-white/10 p-6 flex flex-col h-[400px]">
      <div className="mb-6">
        <h3 className="text-lg font-medium text-white tracking-tight">Token Consumption</h3>
        <p className="text-sm text-gray-500">Weekly usage across all agent sessions</p>
      </div>
      
      <div className="flex-1 w-full min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart
            data={data}
            margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
          >
            <defs>
              <linearGradient id="colorTokens" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#3B82F6" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
            <XAxis 
              dataKey="name" 
              stroke="#666" 
              tick={{fill: '#666', fontSize: 12}} 
              tickLine={false}
              axisLine={false}
              dy={10}
            />
            <YAxis 
              stroke="#666" 
              tick={{fill: '#666', fontSize: 12}}
              tickLine={false}
              axisLine={false}
              dx={-10}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#111', 
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: '8px',
                color: '#fff',
                boxShadow: '0 4px 20px rgba(0,0,0,0.5)'
              }}
              itemStyle={{ color: '#e5e7eb' }}
            />
            <Area 
              type="monotone" 
              dataKey="tokens" 
              stroke="#3B82F6" 
              strokeWidth={2}
              fillOpacity={1} 
              fill="url(#colorTokens)" 
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
