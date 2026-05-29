"use client";

import { signIn } from "next-auth/react";

export default function SignInPage() {
  return (
    <div className="min-h-screen bg-[#0B1120] flex items-center justify-center">
      <div className="bg-[#111827] border border-white/10 rounded-3xl p-10 w-full max-w-md text-white text-center shadow-2xl">
        <h1 className="text-3xl font-bold tracking-tight mb-2">
          Nyaya <span className="text-orange-400">AI</span>
        </h1>
        <p className="text-gray-400 text-sm mb-8">
          Indian Legal Intelligence Platform
        </p>

        <button
          onClick={() => signIn("google", { callbackUrl: "/" })}
          className="w-full flex items-center justify-center gap-3 bg-white text-gray-800 font-semibold px-6 py-3 rounded-2xl hover:bg-gray-100 transition"
        >
          <GoogleIcon />
          Continue with Google
        </button>

        <p className="mt-6 text-xs text-gray-500">
          By continuing, you agree to Nyaya AI&apos;s Terms of Service and Privacy Policy.
        </p>
      </div>
    </div>
  );
}

function GoogleIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 48 48" aria-hidden="true">
      <path
        fill="#EA4335"
        d="M24 9.5c3.14 0 5.95 1.08 8.17 2.85l6.1-6.1C34.46 3.19 29.56 1 24 1 14.82 1 7.07 6.48 3.82 14.18l7.1 5.52C12.56 13.09 17.82 9.5 24 9.5z"
      />
      <path
        fill="#4285F4"
        d="M46.52 24.5c0-1.64-.15-3.22-.42-4.75H24v9h12.7c-.55 2.95-2.2 5.45-4.68 7.13l7.18 5.57C43.3 37.3 46.52 31.4 46.52 24.5z"
      />
      <path
        fill="#FBBC05"
        d="M10.93 28.3A14.56 14.56 0 0 1 9.5 24c0-1.49.26-2.93.72-4.29l-7.1-5.52A23.94 23.94 0 0 0 .5 24c0 3.87.93 7.52 2.57 10.74l7.86-6.44z"
      />
      <path
        fill="#34A853"
        d="M24 47c5.56 0 10.23-1.84 13.64-4.99l-7.18-5.57C28.6 38.1 26.45 38.9 24 38.9c-6.18 0-11.44-3.6-13.07-8.6l-7.86 6.44C6.07 41.52 14.41 47 24 47z"
      />
    </svg>
  );
}
