"use client";
import { useRouter } from "next/navigation";

type Ad = {
  id: string;
  product: string;
  hook: string;
  angle: string;
  positioning: string;
  copy: string;
  creative: string;
  qa_score: string;
  media: string;
  created_at: string;
};

export default function AdCard({ ad }: { ad: Ad }) {
  const router = useRouter();

  const scoreMatch = ad.qa_score?.match(/\d+/);
  const score = scoreMatch ? scoreMatch[0] : "?";

  const handleReuse = () => {
    localStorage.setItem(
      "reuse_ad",
      JSON.stringify({
        product: ad.product,
        hook: ad.hook,
        angle: ad.angle,
      })
    );
    router.push("/");
  };

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-xl p-5 flex flex-col gap-3">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-lg font-bold text-white">{ad.product}</h3>
          <p className="text-sm text-gray-400">
            {new Date(ad.created_at).toLocaleDateString()}
          </p>
        </div>
        <span className="bg-blue-600 text-white text-sm font-bold px-3 py-1 rounded-full">
          {score}/10
        </span>
      </div>

      <p className="text-gray-200 text-sm italic">&quot;{ad.hook}&quot;</p>

      <div className="flex gap-2 flex-wrap">
        <span className="bg-gray-700 text-gray-300 text-xs px-2 py-1 rounded">
          {ad.angle}
        </span>
        <span className="bg-gray-700 text-gray-300 text-xs px-2 py-1 rounded">
          {ad.positioning}
        </span>
      </div>

      <button
        onClick={handleReuse}
        className="mt-2 bg-blue-600 hover:bg-blue-500 text-white text-sm font-semibold py-2 px-4 rounded-lg transition-colors"
      >
        Reuse This Ad
      </button>
    </div>
  );
}
