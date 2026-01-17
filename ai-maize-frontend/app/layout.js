import "./globals.css";

export const metadata = {
  title: "AI Maize Yield Predictor",
  description: "Smart farming with AI",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <header className="nav">
          <h2>🌽 AI Maize</h2>
        </header>
        <main className="container">{children}</main>
      </body>
    </html>
  );
}
