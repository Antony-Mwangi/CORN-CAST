"use client";
import { useRouter } from "next/navigation";

export default function HomePage() {
  const router = useRouter();

  return (
    <>
      <h1>AI Maize Yield Predictor</h1>
      <p>
        Use artificial intelligence to predict maize yield and get smart
        fertilizer recommendations.
      </p>

      <button onClick={() => router.push("/login")}>Login</button>
      <button onClick={() => router.push("/register")}>Register</button>
    </>
  );
}
