"use client";

import { useState, useEffect } from "react";
import axios from "axios";
import { API_URL } from "../lib/api";

export default function Home() {
  const [form, setForm] = useState({
    product: "",
    audience: "",
    platform: "",
    goal: "",
  });

  const [result, setResult] = useState<Record<string, string> | null>(null);
  const [loading, setLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState("");
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

  async function pollJob(jobId: string) {
    const poll = async (): Promise<void> => {
      const res = await axios.get(`${API_URL}/jobs/${jobId}`);
      const job = res.data;

      if (job.current_step) {
        setCurrentStep(job.current_step);
      }

      if (job.status === "completed") {
        setResult(job.result);
        setLoading(false);
        setCurrentStep("");
      } else if (job.status === "failed") {
        setError(job.error || "Ad generation failed");
        setLoading(false);
        setCurrentStep("");
      } else {
        await new Promise((r) => setTimeout(r, 2000));
        return poll();
      }
    };
    await poll();
  }

  async function generateAd() {
    setLoading(true);
    setError("");
    setResult(null);
    setCurrentStep("Starting pipeline...");
    try {
      const res = await axios.post(`${API_URL}/generate-ad`, form);
      await pollJob(res.data.job_id);
    } catch {
      setError("Failed to connect to backend. Is it running?");
      setLoading(false);
      setCurrentStep("");
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

      {loading && currentStep && (
        <div className="bg-gray-800 border border-gray-700 rounded-xl p-6 mb-6">
          <div className="flex items-center gap-3">
            <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
            <p className="text-blue-400 font-medium">{currentStep}</p>
          </div>
        </div>
      )}

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
