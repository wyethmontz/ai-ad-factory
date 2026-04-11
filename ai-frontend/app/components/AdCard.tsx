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
  images: string;
  created_at: string;
};

export default function AdCard({ ad }: { ad: Ad }) {
  const router = useRouter();

  let images: string[] = [];
  try {
    images = ad.images ? JSON.parse(ad.images) : [];
  } catch { /* ignore */ }

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
    <div className="bg-gray-800 border border-gray-700 rounded-xl overflow-hidden flex flex-col gap-3">
      {images.length > 0 && (
        <img
          src={images[0]}
          alt={ad.product}
          className="w-full h-40 object-cover"
        />
      )}
      <div className="px-5 pt-3 flex justify-between items-start">
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

      <p className="px-5 text-gray-200 text-sm italic">&quot;{ad.hook}&quot;</p>

      <div className="px-5 flex gap-2 flex-wrap">
        <span className="bg-gray-700 text-gray-300 text-xs px-2 py-1 rounded">
          {ad.angle}
        </span>
        <span className="bg-gray-700 text-gray-300 text-xs px-2 py-1 rounded">
          {ad.positioning}
        </span>
      </div>

      <button
        onClick={handleReuse}
        className="mx-5 mb-5 mt-2 bg-blue-600 hover:bg-blue-500 text-white text-sm font-semibold py-2 px-4 rounded-lg transition-colors"
      >
        Reuse This Ad
      </button>
    </div>
  );
}
