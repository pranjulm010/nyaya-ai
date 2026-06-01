"use client";

import { useRef } from "react";
import Link from "next/link";

const USE_CASES = [
  { icon: "📄", title: "Contract Review", desc: "Analyse clauses, flag risks, and extract obligations from any contract in seconds." },
  { icon: "⚖️", title: "Case Law Research", desc: "Search Indian Kanoon precedents and get cited judgments relevant to your matter." },
  { icon: "📜", title: "IPC / CrPC Analysis", desc: "Get plain-language interpretations of sections, with cross-referenced case law." },
  { icon: "🔎", title: "FIR & Judgment Analysis", desc: "Upload FIRs or judgments and interrogate them with targeted follow-up questions." },
  { icon: "✍️", title: "Legal Notice Drafting", desc: "Generate first drafts of notices and letters grounded in relevant statutes." },
  { icon: "🌐", title: "Live Legal News", desc: "Pull in the latest from LiveLaw, Bar & Bench, and PRS India inside your research." },
];

const HOW_IT_WORKS = [
  { step: "01", title: "Upload Your Document", desc: "Drop any PDF — contract, FIR, judgment, or notice. Nyaya AI extracts and indexes it instantly." },
  { step: "02", title: "Ask in Plain Language", desc: "Type your question in English or Hindi. No legal jargon required." },
  { step: "03", title: "Get Sourced Answers", desc: "Receive a detailed response drawing from your document, Indian Kanoon precedents, and live legal news — all cited." },
];

const PRICING = [
  {
    name: "Starter",
    price: "₹1,499",
    period: "/mo",
    target: "Solo advocate · Law student",
    features: [
      "20 PDF uploads / mo",
      "200 chat queries / mo",
      "Max 10 MB per file",
      "50 Indian Kanoon searches",
      "7-day chat history",
      "1 seat",
    ],
    cta: "Get Started",
    highlight: false,
  },
  {
    name: "Professional",
    price: "₹5,999",
    period: "/mo",
    target: "Small firm · 2–10 lawyers",
    features: [
      "100 PDF uploads / mo",
      "1,000 chat queries / mo",
      "Max 25 MB per file",
      "300 Indian Kanoon searches",
      "Web research included",
      "30-day history · 5 seats",
    ],
    cta: "Start Free Trial",
    highlight: true,
  },
  {
    name: "Business",
    price: "₹14,999",
    period: "/mo",
    target: "Mid-size firm · 10–50 lawyers",
    features: [
      "500 PDF uploads / mo",
      "5,000 chat queries / mo",
      "Max 50 MB per file",
      "1,500 Indian Kanoon searches",
      "API access + integrations",
      "90-day history · 20 seats",
    ],
    cta: "Get Started",
    highlight: false,
  },
  {
    name: "Enterprise",
    price: "Custom",
    period: "",
    target: "Large firm · Corporate legal",
    features: [
      "Unlimited uploads & queries",
      "Unlimited Kanoon searches",
      "100 MB+ files",
      "On-premise deployment option",
      "SSO · Audit logs",
      "Dedicated support · Custom seats",
    ],
    cta: "Contact Us",
    highlight: false,
  },
];

const STATS = [
  { value: "800K+", label: "Enrolled advocates in India" },
  { value: "4–8 hrs", label: "Saved per research session" },
  { value: "96%", label: "Answer accuracy rate" },
  { value: "<2s", label: "Median response latency" },
];

export default function LandingPage() {
  const featuresRef = useRef<HTMLElement>(null);
  const howItWorksRef = useRef<HTMLElement>(null);
  const pricingRef = useRef<HTMLElement>(null);

  return (
    <div className="min-h-screen bg-[#0B1120] text-white" style={{ fontFamily: "var(--font-geist-sans, Arial, sans-serif)" }}>

      {/* ── Nav ─────────────────────────────────────────────────────────────── */}
      <nav className="sticky top-0 z-50 border-b border-white/10 bg-[#0B1120]/90 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <span className="text-xl font-bold tracking-tight">
            Nyaya <span className="text-orange-400">AI</span>
          </span>

          <div className="hidden md:flex items-center gap-8 text-sm text-gray-400">
            <button
              onClick={() => featuresRef.current?.scrollIntoView({ behavior: "smooth" })}
              className="hover:text-white transition"
            >
              Features
            </button>
            <button
              onClick={() => howItWorksRef.current?.scrollIntoView({ behavior: "smooth" })}
              className="hover:text-white transition"
            >
              How It Works
            </button>
            <button
              onClick={() => pricingRef.current?.scrollIntoView({ behavior: "smooth" })}
              className="hover:text-white transition"
            >
              Pricing
            </button>
          </div>

          <Link
            href="/app"
            className="bg-orange-500 hover:bg-orange-600 transition px-5 py-2 rounded-xl text-sm font-semibold"
          >
            Launch App
          </Link>
        </div>
      </nav>

      {/* ── Hero ─────────────────────────────────────────────────────────────── */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-[-100px] left-1/2 -translate-x-1/2 w-[900px] h-[600px] bg-orange-500/8 rounded-full blur-3xl" />
          <div className="absolute top-[200px] left-1/4 w-[400px] h-[400px] bg-red-500/5 rounded-full blur-3xl" />
        </div>

        <div className="relative max-w-7xl mx-auto px-6 pt-28 pb-24 text-center">
          <div className="inline-flex items-center gap-2 bg-orange-500/10 border border-orange-500/20 text-orange-400 text-xs font-medium px-4 py-2 rounded-full mb-8">
            <span className="w-1.5 h-1.5 bg-orange-400 rounded-full animate-pulse" />
            India-specific · Indian Kanoon · Llama 3.3 70B via Groq
          </div>

          <h1 className="text-5xl md:text-7xl font-bold tracking-tight leading-[1.1] max-w-4xl mx-auto">
            AI Legal Research
            <br />
            <span className="text-orange-400">Built for India</span>
          </h1>

          <p className="mt-6 text-lg md:text-xl text-gray-400 max-w-2xl mx-auto leading-relaxed">
            Upload contracts, FIRs, and judgments. Ask in plain English or Hindi.
            Get sourced answers from your document, Indian Kanoon precedents, and
            live legal news — in seconds, not hours.
          </p>

          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              href="/app"
              className="bg-orange-500 hover:bg-orange-600 transition px-8 py-4 rounded-2xl font-semibold text-lg shadow-lg shadow-orange-500/20 hover:shadow-orange-500/40 hover:scale-105"
            >
              Start Free Research
            </Link>
            <button
              onClick={() => howItWorksRef.current?.scrollIntoView({ behavior: "smooth" })}
              className="border border-white/20 hover:bg-white/5 transition px-8 py-4 rounded-2xl font-semibold text-lg"
            >
              See How It Works
            </button>
          </div>

          <p className="mt-4 text-xs text-gray-500">No credit card required · Free Starter tier available</p>

          {/* Demo chat preview */}
          <div className="mt-16 max-w-2xl mx-auto bg-[#111827] border border-white/10 rounded-3xl p-6 text-left shadow-2xl">
            <div className="flex items-center gap-2 mb-5 pb-4 border-b border-white/10">
              <div className="w-3 h-3 rounded-full bg-red-500/70" />
              <div className="w-3 h-3 rounded-full bg-yellow-500/70" />
              <div className="w-3 h-3 rounded-full bg-green-500/70" />
              <span className="ml-3 text-xs text-gray-500">Nyaya AI — Legal Research Assistant</span>
            </div>
            <div className="space-y-4">
              <div className="flex gap-3">
                <div className="h-8 w-8 shrink-0 rounded-full bg-orange-500 flex items-center justify-center text-xs font-bold">AI</div>
                <div className="bg-white/5 rounded-2xl px-4 py-3 text-sm text-gray-300 max-w-sm">
                  Welcome. Upload a contract, FIR, or judgment, then ask me anything about it.
                </div>
              </div>
              <div className="flex gap-3 justify-end">
                <div className="bg-orange-500 rounded-2xl px-4 py-3 text-sm max-w-sm">
                  What are the termination clauses in this contract?
                </div>
              </div>
              <div className="flex gap-3">
                <div className="h-8 w-8 shrink-0 rounded-full bg-orange-500 flex items-center justify-center text-xs font-bold">AI</div>
                <div className="bg-white/5 rounded-2xl px-4 py-3 text-sm text-gray-300 max-w-sm">
                  The contract contains three termination clauses: <span className="text-orange-400">Clause 12.1</span> (convenience, 30-day notice), <span className="text-orange-400">Clause 12.2</span> (material breach), and <span className="text-orange-400">Clause 12.3</span> (insolvency)...
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Stats ────────────────────────────────────────────────────────────── */}
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

      {/* ── How It Works ─────────────────────────────────────────────────────── */}
      <section ref={howItWorksRef} className="max-w-7xl mx-auto px-6 py-24">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold">How It Works</h2>
          <p className="mt-3 text-gray-400 max-w-xl mx-auto">
            Three steps from document to actionable legal insight.
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

      {/* ── Features ─────────────────────────────────────────────────────────── */}
      <section ref={featuresRef} className="bg-[#111827]/40 border-y border-white/10">
        <div className="max-w-7xl mx-auto px-6 py-24">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold">Built for Every Legal Workflow</h2>
            <p className="mt-3 text-gray-400 max-w-xl mx-auto">
              From solo advocates to large firms — covering the full spectrum of Indian legal research.
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

      {/* ── Architecture ─────────────────────────────────────────────────────── */}
      <section className="max-w-7xl mx-auto px-6 py-24">
        <div className="grid md:grid-cols-2 gap-16 items-center">
          <div>
            <h2 className="text-3xl md:text-4xl font-bold leading-tight">
              Multi-Agent Intelligence,
              <br />
              <span className="text-orange-400">India-First Sources</span>
            </h2>
            <p className="mt-5 text-gray-400 leading-relaxed">
              Nyaya AI orchestrates five specialised agents via LangGraph. Your
              query is automatically routed to the right combination — PDF
              analysis, case law lookup, live news scraping — and synthesised
              into a single, sourced answer.
            </p>
            <ul className="mt-8 space-y-4">
              {[
                ["Memory Agent", "Retains context across your entire session"],
                ["PDF Agent", "Vector-searches your uploaded document (top-5 chunks)"],
                ["Kanoon Agent", "Queries Indian Kanoon for relevant judgments and statutes"],
                ["Web Scraper Agent", "Pulls live content from LiveLaw, Bar & Bench, PRS India"],
                ["Drafting Agent", "Synthesises everything into a coherent, cited response"],
              ].map(([name, desc]) => (
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
            <p className="text-gray-500 text-xs mb-5">&#47;&#47; LangGraph router flow</p>
            <p><span className="text-orange-400">User Query</span></p>
            <p className="text-gray-600 pl-4">│</p>
            <p className="pl-4"><span className="text-blue-400">Memory Agent</span>     <span className="text-gray-600 text-xs">always</span></p>
            <p className="pl-4"><span className="text-blue-400">PDF Agent</span>        <span className="text-gray-600 text-xs">always</span></p>
            <p className="pl-4"><span className="text-green-400">Kanoon Agent</span>    <span className="text-gray-600 text-xs">legal keywords</span></p>
            <p className="pl-4"><span className="text-purple-400">Web Scraper</span>     <span className="text-gray-600 text-xs">news / URL</span></p>
            <p className="text-gray-600 pl-4">│</p>
            <p className="pl-4"><span className="text-orange-400">Drafting Agent</span></p>
            <p className="text-gray-600 pl-4">│</p>
            <p className="pl-4 text-white">Sourced Answer ↓</p>

            <div className="mt-6 pt-6 border-t border-white/10 grid grid-cols-3 gap-3">
              {["Indian Kanoon", "LiveLaw", "Bar & Bench"].map((src) => (
                <div key={src} className="bg-white/5 rounded-xl px-3 py-2 text-xs text-gray-400 text-center">
                  {src}
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ── Pricing ──────────────────────────────────────────────────────────── */}
      <section ref={pricingRef} className="bg-[#111827]/40 border-t border-white/10">
        <div className="max-w-7xl mx-auto px-6 py-24">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold">Simple, Transparent Pricing</h2>
            <p className="mt-3 text-gray-400 max-w-xl mx-auto">
              Designed for the Indian legal market — from solo advocates to large firms.
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
                    plan.highlight
                      ? "bg-orange-500 hover:bg-orange-600"
                      : "border border-white/20 hover:bg-white/5"
                  }`}
                >
                  {plan.cta}
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Final CTA ────────────────────────────────────────────────────────── */}
      <section className="max-w-7xl mx-auto px-6 py-24 text-center">
        <div className="bg-gradient-to-r from-orange-500 to-red-500 rounded-3xl p-14 shadow-2xl shadow-orange-500/20">
          <h2 className="text-3xl md:text-4xl font-bold max-w-2xl mx-auto leading-tight">
            Compress 8 Hours of Legal Research Into 2 Minutes
          </h2>
          <p className="mt-5 text-white/80 max-w-xl mx-auto text-lg">
            Join advocates, law firms, and in-house counsel across India already using Nyaya AI.
          </p>
          <Link
            href="/app"
            className="mt-8 inline-block bg-white text-gray-900 px-10 py-4 rounded-2xl font-bold text-lg hover:bg-gray-100 transition shadow-lg hover:scale-105"
          >
            Start for Free
          </Link>
          <p className="mt-4 text-white/50 text-sm">No credit card · Starter tier is free</p>
        </div>
      </section>

      {/* ── Footer ───────────────────────────────────────────────────────────── */}
      <footer className="border-t border-white/10 bg-[#111827]">
        <div className="max-w-7xl mx-auto px-6 py-10 flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-gray-500">
          <div className="flex items-center gap-2">
            <span className="font-bold text-white">
              Nyaya <span className="text-orange-400">AI</span>
            </span>
            <span>— Indian Legal Intelligence Platform</span>
          </div>
          <div className="flex gap-6">
            <a href="https://livelaw.in" target="_blank" rel="noreferrer" className="hover:text-white transition">LiveLaw</a>
            <a href="https://barandbench.com" target="_blank" rel="noreferrer" className="hover:text-white transition">Bar & Bench</a>
            <a href="https://indiankanoon.org" target="_blank" rel="noreferrer" className="hover:text-white transition">Indian Kanoon</a>
            <a href="mailto:harsh.shukla@raga.ai" className="hover:text-white transition">Contact</a>
          </div>
          <p>© 2026 Nyaya AI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
