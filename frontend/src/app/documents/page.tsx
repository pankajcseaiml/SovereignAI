"use client";

import * as React from "react";
import Link from "next/link";
import { Plus, Database, FileText } from "lucide-react";
import { SplitWorkspace } from "@/components/layout/split-workspace";
import { DocumentCard, DocumentProps } from "@/components/documents/document-card";

export default function DocumentsPage() {
  const [documents, setDocuments] = React.useState<DocumentProps[]>([]);
  const [loading, setLoading] = React.useState(true);

  const fetchDocuments = async () => {
    try {
      const res = await fetch("http://localhost:8001/api/v1/documents/");
      if (res.ok) {
        const data = await res.json();
        setDocuments(data);
      }
    } catch (err) {
      console.error("Failed to fetch documents:", err);
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => {
    fetchDocuments();
    // Poll every 3 seconds
    const interval = setInterval(fetchDocuments, 3000);
    return () => clearInterval(interval);
  }, []);

  const ContextPanel = (
    <div className="flex flex-col h-full bg-transparent p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 bg-blue-500/10 rounded-lg">
          <Database className="w-5 h-5 text-blue-400" />
        </div>
        <div>
          <h2 className="text-sm font-semibold tracking-tight text-white">Knowledge Base</h2>
          <p className="text-xs text-gray-500">Vectorized Documents</p>
        </div>
      </div>
      
      <div className="bg-[#121212] rounded-xl p-4 border border-white/5 shadow-sm">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-medium text-gray-400">Total Documents</span>
          <span className="text-sm font-bold text-white">{documents.length}</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-xs font-medium text-gray-400">Ready for Agent</span>
          <span className="text-sm font-bold text-emerald-400">
            {documents.filter(d => d.status === 'success').length}
          </span>
        </div>
      </div>
    </div>
  );

  return (
    <SplitWorkspace contextPanel={ContextPanel}>
      <div className="flex flex-col h-full bg-transparent relative">
        <header className="h-14 border-b border-border bg-background/80 backdrop-blur-xl sticky top-0 z-20 flex items-center justify-between px-6 shrink-0">
          <div className="flex items-center gap-3">
            <h1 className="font-medium text-[14px]">Document Library</h1>
          </div>
          <Link 
            href="/documents/upload"
            className="flex items-center gap-2 px-3 py-1.5 bg-white text-black text-xs font-medium rounded-md hover:bg-gray-200 transition-colors active:scale-95"
          >
            <Plus className="w-3.5 h-3.5" />
            Upload Document
          </Link>
        </header>

        <div className="flex-1 overflow-y-auto p-6">
          {loading ? (
            <div className="flex items-center justify-center h-40">
              <div className="animate-pulse flex flex-col items-center">
                <FileText className="w-8 h-8 text-gray-600 mb-2" />
                <span className="text-xs text-gray-500">Loading documents...</span>
              </div>
            </div>
          ) : documents.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-[60vh] border border-dashed border-white/10 rounded-xl bg-[#0A0A0A]">
              <div className="w-12 h-12 rounded-full bg-white/5 flex items-center justify-center mb-4">
                <FileText className="w-6 h-6 text-gray-400" />
              </div>
              <h3 className="text-sm font-medium text-white mb-1">No documents yet</h3>
              <p className="text-xs text-gray-500 mb-4">Upload a PDF to start building your knowledge base.</p>
              <Link 
                href="/documents/upload"
                className="px-4 py-2 bg-[#1A1A1A] border border-white/10 text-white text-xs font-medium rounded-md hover:bg-[#2A2A2A] transition-colors"
              >
                Upload your first document
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {documents.map((doc) => (
                <DocumentCard key={doc.id} doc={doc} />
              ))}
            </div>
          )}
        </div>
      </div>
    </SplitWorkspace>
  );
}
