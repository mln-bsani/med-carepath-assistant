export default function Home() {
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

        <button className="mt-8 rounded-xl bg-blue-600 px-6 py-3 font-semibold text-white shadow-sm transition hover:bg-blue-700">
          Start CarePath
        </button>

      </section>
    </main>
  );
}