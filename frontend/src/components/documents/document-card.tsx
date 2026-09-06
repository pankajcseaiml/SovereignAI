import * as React from "react";
import { FileText, CheckCircle2, Clock, AlertCircle } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export interface DocumentProps {
  id: number;
  filename: string;
  status: string;
}

export function DocumentCard({ doc }: { doc: DocumentProps }) {
  const isSuccess = doc.status === "success";
  const isError = doc.status === "error";
  const isPending = !isSuccess && !isError;

  return (
    <Card className="group relative overflow-hidden bg-[#0A0A0A] border-white/10 hover:border-white/20 transition-all duration-300 shadow-sm p-4 flex flex-col gap-3">
      <div className="absolute inset-0 bg-gradient-to-br from-white/[0.02] to-transparent pointer-events-none" />
      
      <div className="flex items-start justify-between z-10">
        <div className="p-2 rounded-md bg-white/5 border border-white/5">
          <FileText className="w-5 h-5 text-blue-400" />
        </div>
        
        {isSuccess && (
          <Badge variant="outline" className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20 gap-1.5 py-0.5">
            <CheckCircle2 className="w-3 h-3" /> Processed
          </Badge>
        )}
        {isPending && (
          <Badge variant="outline" className="bg-yellow-500/10 text-yellow-400 border-yellow-500/20 gap-1.5 py-0.5">
            <Clock className="w-3 h-3 animate-pulse" /> Processing
          </Badge>
        )}
        {isError && (
          <Badge variant="outline" className="bg-red-500/10 text-red-400 border-red-500/20 gap-1.5 py-0.5">
            <AlertCircle className="w-3 h-3" /> Error
          </Badge>
        )}
      </div>

      <div className="z-10 mt-2">
        <h3 className="text-sm font-medium text-gray-200 truncate" title={doc.filename}>
          {doc.filename}
        </h3>
        <p className="text-xs text-gray-500 font-mono mt-1">ID: {doc.id}</p>
      </div>
    </Card>
  );
}
