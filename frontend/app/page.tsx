"use client";

import {
  useState,
  useRef,
  useEffect,
  KeyboardEvent,
  DragEvent,
  ChangeEvent,
} from "react";

import axios from "axios";
import { uploadDocument, sendMessage } from "@/lib/api";

type MessageRole = "ai" | "user";

interface Message {
  role: MessageRole;
  text: string;
}

type UploadStatus = "uploading" | "done" | "error";

interface UploadedFile {
  name: string;
  status: UploadStatus;
}

export default function NyayaAI() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "ai",
      text: "Welcome to Nyaya AI. Upload contracts, FIRs, judgments, or legal notices to begin AI-powered analysis.",
    },
  ]);

  const [input, setInput] = useState("");
  const [uploadedFile, setUploadedFile] = useState<UploadedFile | null>(null);
  const [documentId, setDocumentId] = useState<string | null>(null);
  const [documentType, setDocumentType] = useState<string | null>(null);
  const [sessionId] = useState(() => crypto.randomUUID());
  const [isLoading, setIsLoading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleFileSelect = async (file: File): Promise<void> => {
    const allowedExtensions = [".pdf", ".docx", ".txt", ".md"];

    const isAllowed = allowedExtensions.some((ext) =>
      file.name.toLowerCase().endsWith(ext)
    );

    if (!file || !isAllowed) {
      setMessages((prev) => [
        ...prev,
        { role: "ai", text: "⚠️ Supported files: PDF, DOCX, TXT, MD." },
      ]);
      return;
    }

    setUploadedFile({ name: file.name, status: "uploading" });

    setMessages((prev) => [
      ...prev,
      { role: "user", text: `📄 Uploading: ${file.name}` },
    ]);

    try {
      const result = await uploadDocument(file, "anonymous");

      console.log("UPLOAD RESULT:", result);

      setDocumentId(result.document_id || null);
      setDocumentType(result.document_type || null);

      console.log("ACTIVE DOCUMENT ID:", result.document_id);

      setUploadedFile({ name: file.name, status: "done" });

      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text:
            result?.message ??
            `✅ "${file.name}" uploaded successfully. You can now ask questions about this document.`,
        },
      ]);
    } catch (err: unknown) {
      setUploadedFile({ name: file.name, status: "error" });

      const detail = axios.isAxiosError(err)
        ? err.response?.data?.message || err.response?.data?.error
        : undefined;

      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: `❌ Failed to upload "${file.name}". ${
            detail ?? "Please try again."
          }`,
        },
      ]);
    }
  };

  const handleSend = async (): Promise<void> => {
    const query = input.trim();

    if (!query || isLoading) return;

    setInput("");
    setMessages((prev) => [...prev, { role: "user", text: query }]);
    setIsLoading(true);

    try {
      console.log("CHAT DOCUMENT ID:", documentId);

      const result = await sendMessage({
        query,
        userId: "anonymous",
        sessionId,
        userType: "public",
        documentId: documentId || undefined,
        documentType: documentType || undefined,
      });

      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text:
            result?.answer ??
            result?.response ??
            result?.message ??
            "No response received.",
        },
      ]);
    } catch (err: unknown) {
      const detail = axios.isAxiosError(err)
        ? err.response?.data?.message || err.response?.data?.error
        : undefined;

      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: `❌ Error: ${detail ?? "Unable to reach the server."}`,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>): void => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>): void => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (): void => {
    setIsDragging(false);
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>): void => {
    e.preventDefault();
    setIsDragging(false);

    const file = e.dataTransfer.files?.[0];

    if (file) {
      handleFileSelect(file);
    }
  };

  const handleFileInputChange = (e: ChangeEvent<HTMLInputElement>): void => {
    const file = e.target.files?.[0];

    if (file) {
      handleFileSelect(file);
    }

    e.target.value = "";
  };

  return (
    <div className="min-h-screen bg-[#0B1120] text-white flex">
      <aside className="w-72 border-r border-white/10 bg-[#111827] flex flex-col justify-between">
        <div>
          <div className="p-6 border-b border-white/10">
            <h1 className="text-2xl font-bold tracking-tight">
              Nyaya <span className="text-orange-400">AI</span>
            </h1>
            <p className="text-sm text-gray-400 mt-1">
              Indian Legal Intelligence Platform
            </p>
          </div>

          <div className="p-4">
            <button
              className="w-full bg-orange-500 hover:bg-orange-600 transition rounded-2xl py-3 font-medium"
              onClick={() => {
                setMessages([
                  {
                    role: "ai",
                    text: "Welcome to Nyaya AI. Upload contracts, FIRs, judgments, or legal notices to begin AI-powered analysis.",
                  },
                ]);
                setUploadedFile(null);
                setDocumentId(null);
                setDocumentType(null);
                setInput("");
              }}
            >
              + New Legal Chat
            </button>
          </div>
        </div>

        <div className="p-4 border-t border-white/10">
          <div className="bg-white/5 rounded-2xl p-4">
            <p className="text-sm text-gray-400">Workspace</p>
            <h3 className="font-semibold mt-1">Nyaya Enterprise</h3>
          </div>
        </div>
      </aside>

      <main className="flex-1 flex flex-col">
        <header className="h-16 border-b border-white/10 bg-[#0F172A] flex items-center justify-between px-8">
          <div>
            <h2 className="text-lg font-semibold">Legal Research Assistant</h2>

            {uploadedFile && (
              <p className="text-xs mt-0.5">
                {uploadedFile.status === "uploading" && (
                  <span className="text-yellow-400">
                    ⏳ Uploading: {uploadedFile.name}
                  </span>
                )}

                {uploadedFile.status === "done" && (
                  <span className="text-green-400">
                    ✅ Active: {uploadedFile.name}
                  </span>
                )}

                {uploadedFile.status === "error" && (
                  <span className="text-red-400">
                    ❌ Failed: {uploadedFile.name}
                  </span>
                )}
              </p>
            )}
          </div>

          <div className="flex items-center gap-4">
            <button
              className="bg-white/5 hover:bg-white/10 px-4 py-2 rounded-xl text-sm transition"
              onClick={() => fileInputRef.current?.click()}
            >
              Upload Case Files
            </button>

            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.docx,.txt,.md"
              className="hidden"
              onChange={handleFileInputChange}
            />

            <div className="h-10 w-10 rounded-full bg-orange-500 flex items-center justify-center font-bold">
              N
            </div>
          </div>
        </header>

        <section className="p-8 overflow-y-auto flex-1">
          <div className="bg-gradient-to-r from-orange-500 to-red-500 rounded-3xl p-8 shadow-2xl">
            <h1 className="text-4xl font-bold max-w-2xl leading-tight">
              AI-Powered Indian Legal Research Platform
            </h1>

            <p className="mt-4 text-white/80 max-w-3xl text-lg">
              Upload legal documents, search precedents, summarize case laws,
              and interact with an intelligent legal assistant trained for
              Indian judiciary workflows.
            </p>

            <div className="mt-6 flex gap-4">
              <button
                className="bg-white text-black px-6 py-3 rounded-2xl font-semibold hover:scale-105 transition"
                onClick={() => inputRef.current?.focus()}
              >
                Start Research
              </button>
            </div>
          </div>

          <div className="mt-10 bg-[#111827] border border-white/10 rounded-3xl p-6 flex flex-col h-[500px]">
            <div className="flex-1 overflow-y-auto space-y-6 pr-2">
              {messages.map((msg, i) =>
                msg.role === "ai" ? (
                  <div key={i} className="flex gap-4">
                    <div className="h-10 w-10 shrink-0 rounded-full bg-orange-500 flex items-center justify-center font-bold text-sm">
                      AI
                    </div>

                    <div className="bg-white/5 rounded-2xl p-4 max-w-3xl">
                      <p className="text-gray-200 leading-relaxed whitespace-pre-wrap">
                        {msg.text}
                      </p>
                    </div>
                  </div>
                ) : (
                  <div key={i} className="flex gap-4 justify-end">
                    <div className="bg-orange-500 rounded-2xl p-4 max-w-2xl">
                      <p className="whitespace-pre-wrap">{msg.text}</p>
                    </div>
                  </div>
                )
              )}

              {isLoading && (
                <div className="flex gap-4">
                  <div className="h-10 w-10 shrink-0 rounded-full bg-orange-500 flex items-center justify-center font-bold text-sm">
                    AI
                  </div>

                  <div className="bg-white/5 rounded-2xl p-4">
                    <div className="flex gap-1 items-center h-5">
                      <span className="w-2 h-2 bg-orange-400 rounded-full animate-bounce" />
                      <span className="w-2 h-2 bg-orange-400 rounded-full animate-bounce" />
                      <span className="w-2 h-2 bg-orange-400 rounded-full animate-bounce" />
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            <div className="mt-6 border border-white/10 bg-[#0B1120] rounded-2xl p-4">
              <div className="flex items-center gap-3">
                <button
                  className="bg-white/5 hover:bg-white/10 h-12 w-12 rounded-xl text-xl shrink-0 transition"
                  title="Upload Document"
                  onClick={() => fileInputRef.current?.click()}
                >
                  +
                </button>

                <input
                  ref={inputRef}
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask Nyaya AI about legal documents, contracts, or case law..."
                  className="flex-1 bg-transparent outline-none text-gray-200 placeholder:text-gray-500"
                  disabled={isLoading}
                />

                <button
                  className="bg-orange-500 hover:bg-orange-600 disabled:opacity-40 disabled:cursor-not-allowed px-6 py-3 rounded-xl font-medium transition shrink-0"
                  onClick={handleSend}
                  disabled={isLoading || !input.trim()}
                >
                  {isLoading ? "..." : "Send"}
                </button>
              </div>

              <div
                className={`mt-4 border border-dashed rounded-2xl p-6 text-center transition cursor-pointer select-none ${
                  isDragging
                    ? "border-orange-400 bg-orange-500/10"
                    : "border-white/20 hover:border-orange-400"
                }`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
              >
                {uploadedFile?.status === "uploading" ? (
                  <p className="text-yellow-400 text-sm">
                    ⏳ Uploading {uploadedFile.name}...
                  </p>
                ) : uploadedFile?.status === "done" ? (
                  <p className="text-green-400 text-sm">
                    ✅ {uploadedFile.name} — ready for questions
                  </p>
                ) : (
                  <>
                    <p className="text-gray-400">
                      Drag & drop legal documents here or click to upload
                    </p>
                    <p className="text-xs text-gray-500 mt-2">
                      Supports PDF, DOCX, TXT, MD
                    </p>
                  </>
                )}
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}