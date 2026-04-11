"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Sidebar() {
  const pathname = usePathname();

  const links = [
    { href: "/", label: "Generate" },
    { href: "/history", label: "History" },
  ];

  return (
    <aside className="w-56 min-h-screen bg-gray-900 text-white flex flex-col p-4 gap-2">
      <div className="text-xl font-bold mb-6 px-2">Ad Factory</div>
      {links.map((link) => (
        <Link
          key={link.href}
          href={link.href}
          className={`px-3 py-2 rounded-lg transition-colors ${
            pathname === link.href
              ? "bg-blue-600 text-white"
              : "text-gray-300 hover:bg-gray-700"
          }`}
        >
          {link.label}
        </Link>
      ))}
    </aside>
  );
}
