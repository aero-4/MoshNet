import {Globe2, Loader2, Search, XCircle} from "lucide-react";
import type {FormEvent} from "react";

type AnalyzeFormProps = {
    domain: string;
    error: string;
    isLoading: boolean;
    onDomainChange: (value: string) => void;
    onSubmit: (event: FormEvent<HTMLFormElement>) => void;
};

export function AnalyzeForm({
    domain,
    error,
    isLoading,
    onDomainChange,
    onSubmit,
}: AnalyzeFormProps) {
    return (
        <form
            onSubmit={onSubmit}
            className="rounded-lg border border-slate-200 bg-white p-4 shadow-panel sm:p-5"
        >
            <label
                htmlFor="domain"
                className="mb-2 block text-sm font-medium text-slate-700"
            >
                Введите ссылку на сайт
            </label>
            <div className="flex flex-col gap-3 text-xl sm:flex-row">
                <div className="relative flex-1">
                    <Globe2
                        className="pointer-events-none absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400"
                        aria-hidden="true"
                    />
                    <input
                        id="domain"
                        value={domain}
                        onChange={(event) => onDomainChange(event.target.value)}
                        placeholder="example.com"
                        className="h-12 w-full rounded-md border border-slate-300 bg-white pl-10 pr-3 text-base text-slate-950 outline-none transition focus:border-slate-900 focus:ring-4 focus:ring-slate-200"
                    />
                </div>
                <button
                    type="submit"
                    disabled={isLoading}
                    className="inline-flex h-12 items-center justify-center gap-2 rounded-md bg-slate-900 px-5 text-sm font-medium text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-400"
                >
                    {isLoading ? (
                        <Loader2 className="h-5 w-5 animate-spin" aria-hidden="true"/>
                    ) : (
                        <Search className="h-5 w-5" aria-hidden="true"/>
                    )}
                    Проверить
                </button>
            </div>
            {error ? (
                <div className="mt-3 flex items-start gap-2 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
                    <XCircle className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true"/>
                    <span>{error}</span>
                </div>
            ) : null}
        </form>
    );
}
