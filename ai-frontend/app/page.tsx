"use client";

import { useState, useEffect } from "react";
import axios from "axios";

const API = "http://127.0.0.1:8000";

export default function Home() {
  const [form, setForm] = useState({
    product: "",
    audience: "",
    platform: "",
    goal: "",
  });

  const [result, setResult] = useState<Record<string, string> | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Check if user clicked "Reuse" from the History page
  useEffect(() => {
    const saved = localStorage.getItem("reuse_ad");
    if (saved) {
      const data = JSON.parse(saved);
      setForm((prev) => ({
        ...prev,
        product: data.product || "",
      }));
      localStorage.removeItem("reuse_ad");
    }
  }, []);

  function updateField(e: React.ChangeEvent<HTMLInputElement>) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function generateAd() {
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await axios.post(`${API}/generate-ad`, form);
      setResult(res.data);
    } catch {
      setError("Failed to generate ad. Is your backend running?");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">Generate Ad</h1>
      <p className="text-gray-400 mb-8">Fill in the details and let AI create your ad</p>

      <div className="flex flex-col gap-4 mb-6">
        <input
          name="product"
          placeholder="Product (e.g. Lip Tint)"
          value={form.product}
          onChange={updateField}
          className="bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500"
        />
        <input
          name="audience"
          placeholder="Audience (e.g. Gen Z women)"
          value={form.audience}
          onChange={updateField}
          className="bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500"
        />
        <input
          name="platform"
          placeholder="Platform (e.g. TikTok)"
          value={form.platform}
          onChange={updateField}
          className="bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500"
        />
        <input
          name="goal"
          placeholder="Goal (e.g. Increase sales)"
          value={form.goal}
          onChange={updateField}
          className="bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500"
        />

        <button
          onClick={generateAd}
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-500 disabled:bg-gray-600 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
        >
          {loading ? "Generating..." : "Generate Ad"}
        </button>
      </div>

      {error && (
        <p className="text-red-400 text-center py-4">{error}</p>
      )}

      {result && (
        <div className="bg-gray-800 border border-gray-700 rounded-xl p-6 flex flex-col gap-4">
          <h2 className="text-xl font-bold">Result</h2>

          <div>
            <h3 className="text-sm font-semibold text-gray-400 mb-1">Hook</h3>
            <p className="text-white">{result.hook}</p>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-gray-400 mb-1">Angle</h3>
            <p className="text-white">{result.angle}</p>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-gray-400 mb-1">Positioning</h3>
            <p className="text-white">{result.positioning}</p>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-gray-400 mb-1">Copy</h3>
            <p className="text-white whitespace-pre-wrap">{result.copy}</p>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-gray-400 mb-1">Creative</h3>
            <p className="text-white whitespace-pre-wrap">{result.creative}</p>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-gray-400 mb-1">QA Score</h3>
            <p className="text-white whitespace-pre-wrap">{result.qa_score}</p>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-gray-400 mb-1">Media Prompts</h3>
            <p className="text-white whitespace-pre-wrap">{result.media}</p>
          </div>
        </div>
      )}
    </div>
  );
}
