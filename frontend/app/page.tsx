
"use client";

import { useRef } from "react";
import Link from "next/link";

const USE_CASES = [
  {
    icon: "📄",
    title: "Document Intelligence",
    desc: "Upload FIRs, contracts, judgments, notices, and court orders for source-backed legal analysis.",
  },
  {
    icon: "⚖️",
    title: "Indian Legal Research",
    desc: "Research Indian case law, constitutional provisions, statutory sections, and legal precedents.",
  },
  {
    icon: "🛡️",
    title: "Guardrailed Legal AI",
    desc: "Built with PII masking, unsafe advice blocking, hallucination checking, citation validation, and confidence scoring.",
  },
  {
    icon: "🌍",
    title: "Multilingual Legal Help",
    desc: "Ask legal questions in Hindi, Urdu, Punjabi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, or English.",
  },
  {
    icon: "🔎",
    title: "OCR + RAG Pipeline",
    desc: "Extract, chunk, embed, retrieve, and reason over uploaded legal documents using semantic search.",
  },
  {
    icon: "🧠",
    title: "Custom Agent Workflow",
    desc: "Intent, Router, Document, API, Web, Translation, Guardrail, and Final Answer agents work together.",
  },
];

const HOW_IT_WORKS = [
  {
    step: "01",
    title: "Upload or Ask",
    desc: "Upload a PDF such as an FIR, judgment, contract, or legal notice — or directly ask a legal question.",
  },
  {
    step: "02",
    title: "Agents Retrieve Context",
    desc: "Nyaya AI routes the query through Document, API, Web, Memory, Translation, and Guardrail agents.",
  },
  {
    step: "03",
    title: "Get Safer Legal Insight",
    desc: "The final answer is generated with source ranking, citation checks, confidence scoring, and legal disclaimer.",
  },
];

const PRICING = [
  {
    name: "Starter",
    price: "₹1,499",
    period: "/mo",
    target: "Students · Citizens · Solo advocates",
    features: [
      "Basic legal Q&A",
      "PDF document analysis",
      "Limited chat queries",
      "Multilingual responses",
      "Basic source-backed answers",
      "Legal disclaimer included",
    ],
    cta: "Get Started",
    highlight: false,
  },
  {
    name: "Professional",
    price: "₹5,999",
    period: "/mo",
    target: "Small law firms · Advocates",
    features: [
      "Higher query limits",
      "Advanced document intelligence",
      "API + web legal retrieval",
      "Citation-aware responses",
      "Conversation memory",
      "Priority support",
    ],
    cta: "Start Free Trial",
    highlight: true,
  },
  {
    name: "Business",
    price: "₹14,999",
    period: "/mo",
    target: "Mid-size firms · Legal teams",
    features: [
      "Team usage",
      "Bulk document analysis",
      "Advanced guardrails",
      "Confidence scoring",
      "Billing and usage tracking",
      "Longer history retention",
    ],
    cta: "Get Started",
    highlight: false,
  },
  {
    name: "Enterprise",
    price: "Custom",
    period: "",
    target: "Corporates · Large firms",
    features: [
      "Custom deployment",
      "SSO and RBAC planned",
      "Audit logs planned",
      "Custom data sources",
      "Dedicated support",
      "Enterprise integrations",
    ],
    cta: "Contact Us",
    highlight: false,
  },
];

const STATS = [
  { value: "8+", label: "Specialized AI agents" },
  { value: "11", label: "Supported Indian languages" },
  { value: "5+", label: "Guardrail layers" },
  { value: "RAG", label: "OCR + Vector retrieval" },
];

const AGENTS = [
  ["Intent Agent", "Detects whether the user needs research, document analysis, translation, or explanation."],
  ["Router Agent", "Controls the custom Python-based multi-agent workflow."],
  ["Document Agent", "Processes PDFs using OCR, chunking, embeddings, and vector search."],
  ["API Agent", "Retrieves structured legal information from legal APIs and databases."],
  ["Web Agent", "Fetches recent legal updates, notifications, and public legal sources."],
  ["Guardrail Agent", "Applies safety, source validation, PII filtering, and unsafe advice blocking."],
  ["Translation Agent", "Supports regional-language queries and translates answers back to the user language."],
  ["Final Answer Agent", "Combines verified context into a structured legal response."],
];

export default function LandingPage() {
  const featuresRef = useRef<HTMLElement>(null);
  const howItWorksRef = useRef<HTMLElement>(null);
  const pricingRef = useRef<HTMLElement>(null);

  return (
    <div
      className="min-h-screen bg-[#0B1120] text-white"
      style={{ fontFamily: "var(--font-geist-sans, Arial, sans-serif)" }}
    >
      <nav className="sticky top-0 z-50 border-b border-white/10 bg-[#0B1120]/90 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <span className="text-xl font-bold tracking-tight">
            Nyaya <span className="text-orange-400">AI</span>
          </span>

          <div className="hidden md:flex items-center gap-8 text-sm text-gray-400">
            <button onClick={() => featuresRef.current?.scrollIntoView({ behavior: "smooth" })} className="hover:text-white transition">
              Features
            </button>
            <button onClick={() => howItWorksRef.current?.scrollIntoView({ behavior: "smooth" })} className="hover:text-white transition">
              Workflow
            </button>
            <button onClick={() => pricingRef.current?.scrollIntoView({ behavior: "smooth" })} className="hover:text-white transition">
              Pricing
            </button>
          </div>

          <Link href="/app" className="bg-orange-500 hover:bg-orange-600 transition px-5 py-2 rounded-xl text-sm font-semibold">
            Launch App
          </Link>
        </div>
      </nav>

      <section className="relative overflow-hidden">
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-[-100px] left-1/2 -translate-x-1/2 w-[900px] h-[600px] bg-orange-500/10 rounded-full blur-3xl" />
          <div className="absolute top-[220px] left-1/4 w-[420px] h-[420px] bg-red-500/5 rounded-full blur-3xl" />
        </div>

        <div className="relative max-w-7xl mx-auto px-6 pt-28 pb-24 text-center">
          <div className="inline-flex items-center gap-2 bg-orange-500/10 border border-orange-500/20 text-orange-400 text-xs font-medium px-4 py-2 rounded-full mb-8">
            <span className="w-1.5 h-1.5 bg-orange-400 rounded-full animate-pulse" />
            India-specific · Agentic RAG · Guardrailed Legal AI
          </div>

          <h1 className="text-5xl md:text-7xl font-bold tracking-tight leading-[1.1] max-w-5xl mx-auto">
            Multilingual Legal Intelligence
            <br />
            <span className="text-orange-400">Built for India</span>
          </h1>

          <p className="mt-6 text-lg md:text-xl text-gray-400 max-w-3xl mx-auto leading-relaxed">
            Upload FIRs, contracts, judgments, and legal notices. Ask questions in English or Indian regional languages.
            Nyaya AI retrieves sources, applies guardrails, checks citations, and generates structured legal insight.
          </p>

          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              href="/app"
              className="bg-orange-500 hover:bg-orange-600 transition px-8 py-4 rounded-2xl font-semibold text-lg shadow-lg shadow-orange-500/20 hover:shadow-orange-500/40 hover:scale-105"
            >
              Start Legal Research
            </Link>
            <button
              onClick={() => howItWorksRef.current?.scrollIntoView({ behavior: "smooth" })}
              className="border border-white/20 hover:bg-white/5 transition px-8 py-4 rounded-2xl font-semibold text-lg"
            >
              See Agent Workflow
            </button>
          </div>

          <p className="mt-4 text-xs text-gray-500">
            AI-assisted legal information · Not a substitute for professional legal advice
          </p>

          <div className="mt-16 max-w-2xl mx-auto bg-[#111827] border border-white/10 rounded-3xl p-6 text-left shadow-2xl">
            <div className="flex items-center gap-2 mb-5 pb-4 border-b border-white/10">
              <div className="w-3 h-3 rounded-full bg-red-500/70" />
              <div className="w-3 h-3 rounded-full bg-yellow-500/70" />
              <div className="w-3 h-3 rounded-full bg-green-500/70" />
              <span className="ml-3 text-xs text-gray-500">Nyaya AI — Guardrailed Legal Assistant</span>
            </div>

            <div className="space-y-4">
              <div className="flex gap-3">
                <div className="h-8 w-8 shrink-0 rounded-full bg-orange-500 flex items-center justify-center text-xs font-bold">
                  AI
                </div>
                <div className="bg-white/5 rounded-2xl px-4 py-3 text-sm text-gray-300 max-w-sm">
                  Upload a legal document or ask about Indian law in your preferred language.
                </div>
              </div>

              <div className="flex gap-3 justify-end">
                <div className="bg-orange-500 rounded-2xl px-4 py-3 text-sm max-w-sm">
                  Explain this FIR in simple Hindi.
                </div>
              </div>

              <div className="flex gap-3">
                <div className="h-8 w-8 shrink-0 rounded-full bg-orange-500 flex items-center justify-center text-xs font-bold">
                  AI
                </div>
                <div className="bg-white/5 rounded-2xl px-4 py-3 text-sm text-gray-300 max-w-sm">
                  I searched the uploaded document first, extracted relevant facts, checked supporting sources, and prepared a simplified Hindi explanation with a legal disclaimer.
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="border-y border-white/10 bg-[#111827]/40">
        <div className="max-w-7xl mx-auto px-6 py-14 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          {STATS.map((s) => (
            <div key={s.label}>
              <p className="text-3xl md:text-4xl font-bold text-orange-400">{s.value}</p>
              <p className="mt-2 text-sm text-gray-400">{s.label}</p>
            </div>
          ))}
        </div>
      </section>

      <section ref={howItWorksRef} className="max-w-7xl mx-auto px-6 py-24">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold">How Nyaya AI Works</h2>
          <p className="mt-3 text-gray-400 max-w-xl mx-auto">
            A custom Python-based multi-agent workflow for safer legal intelligence.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {HOW_IT_WORKS.map((item) => (
            <div key={item.step} className="bg-[#111827] border border-white/10 rounded-3xl p-8 relative overflow-hidden">
              <span className="text-7xl font-bold text-orange-500/10 absolute -top-2 -right-2 select-none leading-none">
                {item.step}
              </span>
              <div className="relative">
                <span className="text-xs font-semibold text-orange-400 bg-orange-500/10 border border-orange-500/20 px-3 py-1 rounded-full">
                  Step {item.step}
                </span>
                <h3 className="text-xl font-semibold mt-4 mb-3">{item.title}</h3>
                <p className="text-gray-400 leading-relaxed text-sm">{item.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section ref={featuresRef} className="bg-[#111827]/40 border-y border-white/10">
        <div className="max-w-7xl mx-auto px-6 py-24">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold">Production-Ready Legal AI Features</h2>
            <p className="mt-3 text-gray-400 max-w-xl mx-auto">
              Built around document intelligence, legal retrieval, multilingual access, and safety guardrails.
            </p>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {USE_CASES.map((uc) => (
              <div
                key={uc.title}
                className="bg-[#0B1120] border border-white/10 rounded-3xl p-6 hover:border-orange-500/40 hover:bg-orange-500/5 transition group cursor-default"
              >
                <span className="text-3xl">{uc.icon}</span>
                <h3 className="mt-4 text-lg font-semibold group-hover:text-orange-400 transition">{uc.title}</h3>
                <p className="mt-2 text-gray-400 text-sm leading-relaxed">{uc.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="max-w-7xl mx-auto px-6 py-24">
        <div className="grid md:grid-cols-2 gap-16 items-center">
          <div>
            <h2 className="text-3xl md:text-4xl font-bold leading-tight">
              Custom Multi-Agent Orchestration,
              <br />
              <span className="text-orange-400">Not a Simple Chatbot</span>
            </h2>

            <p className="mt-5 text-gray-400 leading-relaxed">
              Nyaya AI uses a custom Python-based router workflow. Each query passes through intent detection,
              translation, document retrieval, API retrieval, web retrieval, guardrails, and final answer generation.
            </p>

            <ul className="mt-8 space-y-4">
              {AGENTS.map(([name, desc]) => (
                <li key={name} className="flex gap-3 text-sm">
                  <span className="w-2 h-2 mt-1.5 shrink-0 rounded-full bg-orange-400" />
                  <span>
                    <span className="font-semibold text-white">{name}</span>
                    <span className="text-gray-400"> — {desc}</span>
                  </span>
                </li>
              ))}
            </ul>
          </div>

          <div className="bg-[#111827] border border-white/10 rounded-3xl p-8 font-mono text-sm leading-loose">
            <p className="text-gray-500 text-xs mb-5">&#47;&#47; Custom router_agent.py flow</p>
            <p><span className="text-orange-400">User Query</span></p>
            <p className="text-gray-600 pl-4">│</p>
            <p className="pl-4"><span className="text-blue-400">Language Detection</span></p>
            <p className="pl-4"><span className="text-green-400">Intent Agent</span></p>
            <p className="pl-4"><span className="text-purple-400">Router Agent</span></p>
            <p className="pl-4"><span className="text-yellow-400">Document + API + Web Agents</span></p>
            <p className="pl-4"><span className="text-red-400">Guardrail Agent</span></p>
            <p className="pl-4"><span className="text-cyan-400">Translation Agent</span></p>
            <p className="pl-4"><span className="text-orange-400">Final Answer Agent</span></p>
            <p className="text-gray-600 pl-4">│</p>
            <p className="pl-4 text-white">Source-backed Legal Response ↓</p>

            <div className="mt-6 pt-6 border-t border-white/10 grid grid-cols-3 gap-3">
              {["OCR + RAG", "Guardrails", "Multilingual"].map((src) => (
                <div key={src} className="bg-white/5 rounded-xl px-3 py-2 text-xs text-gray-400 text-center">
                  {src}
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section ref={pricingRef} className="bg-[#111827]/40 border-t border-white/10">
        <div className="max-w-7xl mx-auto px-6 py-24">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold">Simple Pricing for Indian Legal Workflows</h2>
            <p className="mt-3 text-gray-400 max-w-xl mx-auto">
              Designed for students, citizens, advocates, firms, and corporate legal teams.
            </p>
          </div>

          <div className="grid sm:grid-cols-2 xl:grid-cols-4 gap-6">
            {PRICING.map((plan) => (
              <div
                key={plan.name}
                className={`rounded-3xl p-7 flex flex-col border transition ${
                  plan.highlight
                    ? "border-orange-500 bg-gradient-to-b from-orange-500/10 to-transparent shadow-2xl shadow-orange-500/10"
                    : "border-white/10 bg-[#0B1120]"
                }`}
              >
                {plan.highlight && (
                  <span className="text-xs font-semibold text-orange-400 bg-orange-500/10 border border-orange-500/20 rounded-full px-3 py-1 self-start mb-4">
                    Most Popular
                  </span>
                )}

                <h3 className="text-xl font-bold">{plan.name}</h3>
                <p className="text-xs text-gray-500 mt-1">{plan.target}</p>

                <div className="mt-5 flex items-end gap-1">
                  <span className="text-4xl font-bold">{plan.price}</span>
                  {plan.period && <span className="text-gray-400 text-sm pb-1">{plan.period}</span>}
                </div>

                <ul className="mt-6 space-y-3 flex-1">
                  {plan.features.map((f) => (
                    <li key={f} className="flex items-start gap-2 text-sm text-gray-300">
                      <span className="text-orange-400 mt-0.5 shrink-0">✓</span>
                      {f}
                    </li>
                  ))}
                </ul>

                <Link
                  href="/app"
                  className={`mt-8 text-center py-3 rounded-2xl font-semibold text-sm transition block ${
                    plan.highlight ? "bg-orange-500 hover:bg-orange-600" : "border border-white/20 hover:bg-white/5"
                  }`}
                >
                  {plan.cta}
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="max-w-7xl mx-auto px-6 py-24 text-center">
        <div className="bg-gradient-to-r from-orange-500 to-red-500 rounded-3xl p-14 shadow-2xl shadow-orange-500/20">
          <h2 className="text-3xl md:text-4xl font-bold max-w-2xl mx-auto leading-tight">
            Make Indian Legal Research Faster, Safer, and Multilingual
          </h2>
          <p className="mt-5 text-white/80 max-w-xl mx-auto text-lg">
            Use AI-assisted document intelligence, legal retrieval, guardrails, and regional-language support in one platform.
          </p>
          <Link
            href="/app"
            className="mt-8 inline-block bg-white text-gray-900 px-10 py-4 rounded-2xl font-bold text-lg hover:bg-gray-100 transition shadow-lg hover:scale-105"
          >
            Launch Nyaya AI
          </Link>
          <p className="mt-4 text-white/60 text-sm">
            AI-assisted legal information. Always verify with a qualified legal professional.
          </p>
        </div>
      </section>

      <footer className="border-t border-white/10 bg-[#111827]">
        <div className="max-w-7xl mx-auto px-6 py-10 flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-gray-500">
          <div className="flex items-center gap-2">
            <span className="font-bold text-white">
              Nyaya <span className="text-orange-400">AI</span>
            </span>
            <span>— Indian Legal Intelligence Platform</span>
          </div>

          <div className="flex gap-6">
            <a href="https://livelaw.in" target="_blank" rel="noreferrer" className="hover:text-white transition">
              LiveLaw
            </a>
            <a href="https://barandbench.com" target="_blank" rel="noreferrer" className="hover:text-white transition">
              Bar & Bench
            </a>
            <a href="https://indiankanoon.org" target="_blank" rel="noreferrer" className="hover:text-white transition">
              Indian Kanoon
            </a>
            <a href="mailto:pranjulm@observancegroup.com" className="hover:text-white transition">
              Contact
            </a>
          </div>

          <p>© 2026 Nyaya AI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

