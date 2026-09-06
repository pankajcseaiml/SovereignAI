"use client";

import * as React from "react";
import { useRouter } from "next/navigation";
import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import { SplitWorkspace } from "@/components/layout/split-workspace";
import { UploadZone } from "@/components/documents/upload-zone";

export default function DocumentUploadPage() {
  const router = useRouter();

  const handleSuccess = () => {
    // Redirect back to documents page after successful upload
    router.push("/documents");
  };

  const ContextPanel = (
    <div className="flex flex-col h-full bg-transparent p-6">
      <h2 className="text-sm font-semibold tracking-tight text-white mb-2">Upload Instructions</h2>
      <p className="text-xs text-gray-400 mb-4">
        Upload PDF documents to be processed by the SovereignAI ingestion pipeline.
      </p>
      <ul className="text-xs text-gray-500 space-y-2 list-disc list-inside">
        <li>Only PDF format is currently supported</li>
        <li>Maximum file size is 50MB</li>
        <li>Documents will be automatically vectorized and stored in Qdrant</li>
        <li>Once processed, they will be available to the Agent</li>
      </ul>
    </div>
  );

  return (
    <SplitWorkspace contextPanel={ContextPanel}>
      <div className="flex flex-col h-full bg-transparent">
        <header className="h-14 border-b border-border bg-background/80 backdrop-blur-xl sticky top-0 z-10 flex items-center px-6 shrink-0">
          <Link 
            href="/documents" 
            className="flex items-center text-sm font-medium text-gray-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Documents
          </Link>
        </header>

        <div className="flex-1 overflow-y-auto p-6 md:p-12 flex flex-col items-center justify-center">
          <div className="w-full max-w-lg">
            <div className="text-center mb-8">
              <h1 className="text-2xl font-semibold tracking-tight text-white mb-2">Upload New Document</h1>
              <p className="text-sm text-gray-400">Add a file to your SovereignAI knowledge base.</p>
            </div>
            
            <UploadZone onSuccess={handleSuccess} />
          </div>
        </div>
      </div>
    </SplitWorkspace>
  );
}
