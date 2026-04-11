"use client";
import { useState, useEffect } from "react";

type Props = {
  src: string;
  alt: string;
  delay: number; // milliseconds before loading
};

export default function LazyImage({ src, alt, delay }: Props) {
  const [loadSrc, setLoadSrc] = useState("");
  const [loaded, setLoaded] = useState(false);
  const [error, setError] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setLoadSrc(src);
    }, delay);
    return () => clearTimeout(timer);
  }, [src, delay]);

  if (error) {
    return (
      <div className="bg-gray-700 rounded-lg w-full h-48 flex items-center justify-center text-gray-400 text-sm">
        Image loading...
      </div>
    );
  }

  if (!loadSrc) {
    return (
      <div className="bg-gray-700 rounded-lg w-full h-48 flex items-center justify-center animate-pulse">
        <div className="w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <>
      {!loaded && (
        <div className="bg-gray-700 rounded-lg w-full h-48 flex items-center justify-center animate-pulse">
          <div className="w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
        </div>
      )}
      <img
        src={loadSrc}
        alt={alt}
        className={`rounded-lg w-full ${loaded ? "" : "hidden"}`}
        onLoad={() => setLoaded(true)}
        onError={() => setError(true)}
      />
    </>
  );
}
