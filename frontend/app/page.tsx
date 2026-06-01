"use client";

import { useState, useRef, useEffect, KeyboardEvent, DragEvent, ChangeEvent } from "react";
import { useSession, signIn, signOut } from "next-auth/react";
import Image from "next/image";
import axios from "axios";

// ─── API helpers ────────────────────────────────────────────────────────────

const BASE_URL = "http://127.0.0.1:8000/api";

const uploadPDF = async (file: File): Promise<{ message?: string }> => {
  const formData = new FormData();
  formData.append("file", file);
  const response = await axios.post(`${BASE_URL}/upload/`, formData);
  return response.data;
};

const sendMessage = async (query: string): Promise<{ response?: string; answer?: string }> => {
  const response = await axios.post(`${BASE_URL}/chat/`, { query });
  return response.data;
};

// ─── Types ───────────────────────────────────────────────────────────────────

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

// ─── Component ───────────────────────────────────────────────────────────────

export default function NyayaAI() {
  const { data: session, status } = useSession();

  const [messages, setMessages] = useState<Message[]>([
    {
      role: "ai",
      text: "Welcome to Nyaya AI. Upload contracts, FIRs, judgments, or legal notices to begin AI-powered analysis.",
    },
  ]);
  const [input, setInput] = useState<string>("");
  const [uploadedFile, setUploadedFile] = useState<UploadedFile | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isDragging, setIsDragging] = useState<boolean>(false);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // ── PDF upload ──────────────────────────────────────────────────────────────

  const handleFileSelect = async (file: File): Promise<void> => {
    if (!file || file.type !== "application/pdf") {
      setMessages((prev) => [
        ...prev,
        { role: "ai", text: "⚠️ Only PDF files are supported at this time." },
      ]);
      return;
    }

    setUploadedFile({ name: file.name, status: "uploading" });
    setMessages((prev) => [
      ...prev,
      { role: "user", text: `📄 Uploading: ${file.name}` },
    ]);

    try {
      const result = await uploadPDF(file);
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
      const detail =
        axios.isAxiosError(err) ? err.response?.data?.detail : undefined;
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: `❌ Failed to upload "${file.name}". ${detail ?? "Please try again."}`,
        },
      ]);
    }
  };

  // ── Chat send ───────────────────────────────────────────────────────────────

  const handleSend = async (): Promise<void> => {
    const query = input.trim();
    if (!query || isLoading) return;

    setInput("");
    setMessages((prev) => [...prev, { role: "user", text: query }]);
    setIsLoading(true);

    try {
      const result = await sendMessage(query);
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: result?.response ?? result?.answer ?? "No response received.",
        },
      ]);
    } catch (err: unknown) {
      const detail =
        axios.isAxiosError(err) ? err.response?.data?.detail : undefined;
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

  // ── Drag & drop ─────────────────────────────────────────────────────────────

  const handleDragOver = (e: DragEvent<HTMLDivElement>): void => {
    e.preventDefault();
    setIsDragging(true);
  };
  const handleDragLeave = (): void => setIsDragging(false);
  const handleDrop = (e: DragEvent<HTMLDivElement>): void => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file) handleFileSelect(file);
  };

  const handleFileInputChange = (e: ChangeEvent<HTMLInputElement>): void => {
    const file = e.target.files?.[0];
    if (file) handleFileSelect(file);
    e.target.value = "";
  };

  // ── Render ──────────────────────────────────────────────────────────────────

  if (status === "loading") {
    return (
      <div className="min-h-screen bg-[#0B1120] flex items-center justify-center text-white">
        <div className="flex gap-1">
          <span className="w-2 h-2 bg-orange-400 rounded-full animate-bounce [animation-delay:0ms]" />
          <span className="w-2 h-2 bg-orange-400 rounded-full animate-bounce [animation-delay:150ms]" />
          <span className="w-2 h-2 bg-orange-400 rounded-full animate-bounce [animation-delay:300ms]" />
        </div>
      </div>
    );
  }

  if (!session) {
    return (
      <div className="min-h-screen bg-[#0B1120] flex items-center justify-center">
        <div className="bg-[#111827] border border-white/10 rounded-3xl p-10 w-full max-w-md text-white text-center shadow-2xl">
          <h1 className="text-3xl font-bold tracking-tight mb-2">
            Nyaya <span className="text-orange-400">AI</span>
          </h1>
          <p className="text-gray-400 text-sm mb-8">Indian Legal Intelligence Platform</p>
          <button
            onClick={() => signIn("google")}
            className="w-full flex items-center justify-center gap-3 bg-white text-gray-800 font-semibold px-6 py-3 rounded-2xl hover:bg-gray-100 transition"
          >
            <svg width="20" height="20" viewBox="0 0 48 48" aria-hidden="true">
              <path fill="#EA4335" d="M24 9.5c3.14 0 5.95 1.08 8.17 2.85l6.1-6.1C34.46 3.19 29.56 1 24 1 14.82 1 7.07 6.48 3.82 14.18l7.1 5.52C12.56 13.09 17.82 9.5 24 9.5z" />
              <path fill="#4285F4" d="M46.52 24.5c0-1.64-.15-3.22-.42-4.75H24v9h12.7c-.55 2.95-2.2 5.45-4.68 7.13l7.18 5.57C43.3 37.3 46.52 31.4 46.52 24.5z" />
              <path fill="#FBBC05" d="M10.93 28.3A14.56 14.56 0 0 1 9.5 24c0-1.49.26-2.93.72-4.29l-7.1-5.52A23.94 23.94 0 0 0 .5 24c0 3.87.93 7.52 2.57 10.74l7.86-6.44z" />
              <path fill="#34A853" d="M24 47c5.56 0 10.23-1.84 13.64-4.99l-7.18-5.57C28.6 38.1 26.45 38.9 24 38.9c-6.18 0-11.44-3.6-13.07-8.6l-7.86 6.44C6.07 41.52 14.41 47 24 47z" />
            </svg>
            Continue with Google
          </button>
          <p className="mt-6 text-xs text-gray-500">
            By continuing, you agree to Nyaya AI&apos;s Terms of Service.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0B1120] text-white flex">
      {/* Sidebar */}
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
                setInput("");
              }}
            >
              + New Legal Chat
            </button>
          </div>

          <nav className="px-3 space-y-2">
            {[
              "Contracts Review",
              "Case Law Research",
              "IPC Analysis",
              "Compliance Drafting",
              "Legal Summaries",
            ].map((item) => (
              <button
                key={item}
                className="w-full text-left px-4 py-3 rounded-xl hover:bg-white/5 transition text-gray-300"
              >
                {item}
              </button>
            ))}
          </nav>
        </div>

        <div className="p-4 border-t border-white/10">
          <div className="bg-white/5 rounded-2xl p-4">
            <p className="text-sm text-gray-400">Signed in as</p>
            <h3 className="font-semibold mt-1 truncate">{session.user?.name ?? session.user?.email}</h3>
            <p className="text-xs text-gray-500 truncate">{session.user?.email}</p>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col">
        {/* Top Navbar */}
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

            {/* Hidden file input — shared by all upload triggers */}
            <input
              ref={fileInputRef}
              type="file"
              accept="application/pdf"
              className="hidden"
              onChange={handleFileInputChange}
            />

            <div className="flex items-center gap-3">
              {session.user?.image ? (
                <Image
                  src={session.user.image}
                  alt={session.user.name ?? "User"}
                  width={40}
                  height={40}
                  className="rounded-full"
                />
              ) : (
                <div className="h-10 w-10 rounded-full bg-orange-500 flex items-center justify-center font-bold">
                  {session.user?.name?.[0]?.toUpperCase() ?? "U"}
                </div>
              )}
              <button
                onClick={() => signOut()}
                className="text-sm text-gray-400 hover:text-white transition"
              >
                Sign out
              </button>
            </div>
          </div>
        </header>

        {/* Dashboard */}
        <section className="p-8 overflow-y-auto flex-1">
          {/* Hero */}
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
              <button className="border border-white/20 px-6 py-3 rounded-2xl hover:bg-white/10 transition">
                Explore Features
              </button>
            </div>
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mt-8">
            {[
              { title: "Documents Uploaded", value: "1,248" },
              { title: "Case Analyses", value: "342" },
              { title: "Research Sessions", value: "89" },
              { title: "AI Accuracy", value: "96%" },
            ].map((card) => (
              <div
                key={card.title}
                className="bg-[#111827] border border-white/10 rounded-3xl p-6"
              >
                <p className="text-gray-400 text-sm">{card.title}</p>
                <h3 className="text-3xl font-bold mt-3">{card.value}</h3>
              </div>
            ))}
          </div>

          {/* Chat Interface */}
          <div className="mt-10 bg-[#111827] border border-white/10 rounded-3xl p-6 flex flex-col h-[500px]">
            {/* Messages */}
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

              {/* Typing indicator */}
              {isLoading && (
                <div className="flex gap-4">
                  <div className="h-10 w-10 shrink-0 rounded-full bg-orange-500 flex items-center justify-center font-bold text-sm">
                    AI
                  </div>
                  <div className="bg-white/5 rounded-2xl p-4">
                    <div className="flex gap-1 items-center h-5">
                      <span className="w-2 h-2 bg-orange-400 rounded-full animate-bounce [animation-delay:0ms]" />
                      <span className="w-2 h-2 bg-orange-400 rounded-full animate-bounce [animation-delay:150ms]" />
                      <span className="w-2 h-2 bg-orange-400 rounded-full animate-bounce [animation-delay:300ms]" />
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="mt-6 border border-white/10 bg-[#0B1120] rounded-2xl p-4">
              <div className="flex items-center gap-3">
                <button
                  className="bg-white/5 hover:bg-white/10 h-12 w-12 rounded-xl text-xl shrink-0 transition"
                  title="Upload PDF"
                  onClick={() => fileInputRef.current?.click()}
                >
                  +
                </button>

                <input
                  ref={inputRef}
                  type="text"
                  value={input}
                  onChange={(e: ChangeEvent<HTMLInputElement>) =>
                    setInput(e.target.value)
                  }
                  onKeyDown={handleKeyDown}
                  placeholder="Ask Nyaya AI about legal documents, contracts, or case law... (हिंदी में भी पूछें)"
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

              {/* Drag & Drop Upload Zone */}
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
                      Supports PDF files only
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
