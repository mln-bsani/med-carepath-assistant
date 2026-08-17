"use client";

import { useEffect, useState } from "react";
import { doc, getDoc } from "firebase/firestore";
import { db } from "@/lib/firebase";

export default function Home() {
  const [started, setStarted] = useState(false);
  const [firebaseStatus, setFirebaseStatus] = useState<
    "checking" | "connected" | "error"
  >("checking");

  useEffect(() => {
    async function testFirebase() {
      try {
        const testDoc = await getDoc(
          doc(db, "system", "connection-test")
        );

        console.log("Firebase connected:", testDoc.exists());
        setFirebaseStatus("connected");
      } catch (error) {
        console.error("Firebase connection error:", error);
        setFirebaseStatus("error");
      }
    }

    testFirebase();
  }, []);

  if (!started) {
    return (
      <main className="min-h-screen bg-slate-50">
        <section className="mx-auto flex min-h-screen max-w-4xl flex-col items-center justify-center px-6 text-center">
          <div className="mb-6 rounded-full bg-blue-100 px-4 py-2 text-sm font-medium text-blue-700">
            Med CarePath Assistant
          </div>

          <h1 className="max-w-3xl text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">
            Your Healthcare Workflow & Navigation Assistant
          </h1>

          <p className="mt-5 max-w-2xl text-lg leading-8 text-slate-600">
            Helping clients understand where to go, what to do,
            and what to expect during their healthcare journey.
          </p>

          <button
            onClick={() => setStarted(true)}
            className="mt-8 rounded-xl bg-blue-600 px-6 py-3 font-semibold text-white shadow-sm transition hover:bg-blue-700"
          >
            Start CarePath
          </button>

          <div className="mt-6 text-sm">
            {firebaseStatus === "checking" && (
              <span className="text-slate-500">
                Connecting to CarePath services...
              </span>
            )}

            {firebaseStatus === "connected" && (
              <span className="text-green-600">
                ● CarePath services connected
              </span>
            )}

            {firebaseStatus === "error" && (
              <span className="text-red-600">
                ● Service connection error
              </span>
            )}
          </div>
        </section>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-50">
      <section className="mx-auto max-w-4xl px-6 py-12">
        <div className="mb-8">
          <p className="text-sm font-medium text-blue-600">
            Med CarePath Assistant
          </p>

          <h1 className="mt-2 text-3xl font-bold text-slate-900">
            What do you need help with?
          </h1>

          <p className="mt-3 text-slate-600">
            Choose the service that best matches what you need today.
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <button className="rounded-2xl border border-slate-200 bg-white p-6 text-left shadow-sm transition hover:border-blue-400 hover:shadow-md">
            <h2 className="text-lg font-semibold text-slate-900">
              🧪 Laboratory Services
            </h2>

            <p className="mt-2 text-sm text-slate-600">
              Find the right unit, understand sample requirements,
              and know what to expect.
            </p>
          </button>

          <button className="rounded-2xl border border-slate-200 bg-white p-6 text-left shadow-sm transition hover:border-blue-400 hover:shadow-md">
            <h2 className="text-lg font-semibold text-slate-900">
              🏥 Clinic / Consultation
            </h2>

            <p className="mt-2 text-sm text-slate-600">
              Get help finding the appropriate clinic or service.
            </p>
          </button>
          <button className="rounded-2xl border border-slate-200 bg-white p-6 text-left shadow-sm transition hover:border-blue-400 hover:shadow-md">
            <h2 className="text-lg font-semibold text-slate-900">
              📋 Test Information
            </h2>

            <p className="mt-2 text-sm text-slate-600">
              Learn what a test generally involves and what to
              prepare.
            </p>
          </button>

          <button className="rounded-2xl border border-slate-200 bg-white p-6 text-left shadow-sm transition hover:border-blue-400 hover:shadow-md">
            <h2 className="text-lg font-semibold text-slate-900">
              📍 Find a Unit
            </h2>

            <p className="mt-2 text-sm text-slate-600">
              Get guidance on where to take your request or sample.
            </p>
          </button>
        </div>

        <div className="mt-8 text-center">
          <button
            onClick={() => setStarted(false)}
            className="text-sm font-medium text-slate-500 hover:text-slate-800"
          >
            ← Back
          </button>
        </div>
      </section>
    </main>
  );
}