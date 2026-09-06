"use client";

import * as React from "react";
import { UploadCloud, FileText, X, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface UploadZoneProps {
  onSuccess?: () => void;
}

export function UploadZone({ onSuccess }: UploadZoneProps) {
  const [isDragging, setIsDragging] = React.useState(false);
  const [file, setFile] = React.useState<File | null>(null);
  const [isUploading, setIsUploading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const inputRef = React.useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setIsDragging(true);
    } else if (e.type === "dragleave") {
      setIsDragging(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (selectedFile: File) => {
    setError(null);
    if (selectedFile.type !== "application/pdf") {
      setError("Please upload a valid PDF document.");
      return;
    }
    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) return;
    
    setIsUploading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append("file", file);
    
    try {
      const response = await fetch("http://localhost:8001/api/v1/documents/upload", {
        method: "POST",
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error("Upload failed. Please try again.");
      }
      
      if (onSuccess) {
        onSuccess();
      }
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <div 
        className={cn(
          "relative border-2 border-dashed rounded-xl p-8 flex flex-col items-center justify-center transition-all duration-300 ease-in-out cursor-pointer overflow-hidden",
          isDragging 
            ? "border-blue-500 bg-blue-500/5 shadow-[0_0_30px_rgba(59,130,246,0.1)] scale-[1.02]" 
            : "border-white/10 bg-[#0A0A0A] hover:border-white/20 hover:bg-white/[0.02]",
          file && !isUploading ? "border-emerald-500/50 bg-emerald-500/5" : ""
        )}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => !file && inputRef.current?.click()}
      >
        <input 
          type="file" 
          ref={inputRef}
          onChange={handleChange}
          accept="application/pdf"
          className="hidden" 
        />
        
        {isUploading ? (
          <div className="flex flex-col items-center animate-in fade-in zoom-in duration-300">
            <Loader2 className="w-10 h-10 text-blue-500 animate-spin mb-4" />
            <p className="text-sm font-medium text-gray-200">Uploading Document...</p>
            <p className="text-xs text-gray-500 mt-1">Please wait</p>
          </div>
        ) : file ? (
          <div className="flex flex-col items-center w-full animate-in fade-in zoom-in duration-300">
            <div className="w-12 h-12 rounded-full bg-emerald-500/20 flex items-center justify-center mb-4 relative group">
              <FileText className="w-6 h-6 text-emerald-400 group-hover:opacity-0 transition-opacity" />
              <button 
                onClick={(e) => { e.stopPropagation(); setFile(null); }}
                className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
              >
                <X className="w-6 h-6 text-red-400" />
              </button>
            </div>
            <p className="text-sm font-medium text-gray-200 text-center truncate w-full px-4">{file.name}</p>
            <p className="text-xs text-gray-500 mt-1">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
            
            <button 
              onClick={(e) => { e.stopPropagation(); handleUpload(); }}
              className="mt-6 px-6 py-2 bg-white text-black text-sm font-medium rounded-full hover:bg-gray-200 transition-colors active:scale-95 shadow-[0_0_20px_rgba(255,255,255,0.3)]"
            >
              Confirm Upload
            </button>
          </div>
        ) : (
          <div className="flex flex-col items-center pointer-events-none">
            <div className="w-12 h-12 rounded-full bg-white/5 flex items-center justify-center mb-4">
              <UploadCloud className={cn("w-6 h-6 transition-colors", isDragging ? "text-blue-400" : "text-gray-400")} />
            </div>
            <p className="text-sm font-medium text-gray-200">
              Drag & drop your PDF here
            </p>
            <p className="text-xs text-gray-500 mt-1">
              or click to browse from your computer
            </p>
          </div>
        )}
      </div>
      
      {error && (
        <div className="mt-4 p-3 rounded-md bg-red-500/10 border border-red-500/20 flex items-center animate-in slide-in-from-top-2">
          <p className="text-xs text-red-400 font-medium">{error}</p>
        </div>
      )}
    </div>
  );
}
