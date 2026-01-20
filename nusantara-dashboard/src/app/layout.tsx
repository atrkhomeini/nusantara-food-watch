import type { Metadata } from "next";
import "./globals.css"; // Make sure this path points to your actual CSS file

export const metadata: Metadata = {
  title: "Nusantara Dashboard",
  description: "Dashboard for Nusantara Food",
};

// ---------------------------------------------------------
// THIS is what was likely missing or malformed:
// ---------------------------------------------------------
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}