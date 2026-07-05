import {
    AlertTriangle,
    CheckCircle2,
    Globe2,
    Loader2,
    Search,
    ShieldAlert,
    ShieldCheck,
    XCircle,
} from "lucide-react";
import {FormEvent, useMemo, useState} from "react";

type BadStatus = {
    source: string;
    category?: string | null;
    result?: string | null;
};

type DomainInfo = {
    domain_org?: string | null;
    created_at?: string | null;
    updated_at?: string | null;
    registrar?: Record<string, unknown> | null;
    registrant?: Record<string, unknown> | null;
    last_analysis_stats?: Record<string, number> | null;
    bad_statuses?: BadStatus[];
};

type SafetyState = "safe" | "danger" | "unknown";

const API_URL =
    import.meta.env.VITE_API_URL ?? "http://localhost:8000/domains/analyze/";

const statLabels: Record<string, string> = {
    harmless: "Безопасно",
    malicious: "Вредоносно",
    suspicious: "Подозрительно",
    undetected: "Не обнаружено",
    timeout: "Таймаут",
};

function normalizeDomain(value: string) {
    return value.trim().replace(/^https?:\/\//i, "").replace(/\/.*$/, "");
}

function getVirusTotalInfo(items: DomainInfo[]) {
    return items.find(
        (item) => item.last_analysis_stats || item.bad_statuses?.length,
    );
}

function getWhoisInfo(items: DomainInfo[]) {
    return items.find((item) => item.registrar || item.registrant || item.created_at);
}

function getSafetyState(virusTotal?: DomainInfo): SafetyState {
    if (!virusTotal?.last_analysis_stats && !virusTotal?.bad_statuses?.length) {
        return "unknown";
    }

    const stats = virusTotal.last_analysis_stats ?? {};
    const hasBadStats = (stats.malicious ?? 0) > 0 || (stats.suspicious ?? 0) > 0;
    const hasBadStatuses = Boolean(virusTotal.bad_statuses?.length);

    return hasBadStats || hasBadStatuses ? "danger" : "safe";
}

function formatValue(value: unknown) {
    if (!value) {
        return "Нет данных";
    }

    if (typeof value === "string" || typeof value === "number") {
        return String(value);
    }

    if (typeof value === "object") {
        const entries = Object.entries(value as Record<string, unknown>);
        const firstTextValue = entries.find(([, item]) => typeof item === "string");
        return firstTextValue ? String(firstTextValue[1]) : "Есть данные";
    }

    return "Нет данных";
}

export default function App() {
    const [domain, setDomain] = useState("");
    const [result, setResult] = useState<DomainInfo[] | null>(null);
    const [error, setError] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const virusTotal = useMemo(
        () => (result ? getVirusTotalInfo(result) : undefined),
        [result],
    );
    const whois = useMemo(() => (result ? getWhoisInfo(result) : undefined), [result]);
    const safetyState = getSafetyState(virusTotal);
    const badStatuses = virusTotal?.bad_statuses ?? [];
    const stats = virusTotal?.last_analysis_stats ?? {};

    async function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();

        const normalizedDomain = normalizeDomain(domain);
        if (!normalizedDomain) {
            setError("Введите сайт");
            setResult(null);
            return;
        }

        setIsLoading(true);
        setError("");
        setResult(null);

        try {
            const response = await fetch(API_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({domain: normalizedDomain}),
            });

            if (!response.ok) {
                const detail = await response.json().catch(() => null);
                throw new Error(detail?.detail ?? `Ошибка запроса: ${response.status}`);
            }

            const payload = (await response.json()) as DomainInfo[];
            setResult(payload);
            setDomain(normalizedDomain);
        } catch (requestError) {
            setError(
                requestError instanceof Error
                    ? requestError.message
                    : "Не удалось проверить сайт",
            );
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <main className="min-h-screen bg-[#f4f7fb] text-slate-900">
            <div className="mx-auto flex min-h-screen w-full max-w-6xl flex-col px-4 py-6 sm:px-6 lg:px-8">
                <header className="flex flex-col gap-4 border-b border-slate-200 pb-5 sm:flex-row sm:items-center sm:justify-between">
                    <div className="flex items-center gap-3">
                        <div className="flex h-11 w-11 items-center justify-center rounded-lg bg-slate-900 text-white">
                            <ShieldCheck className="h-6 w-6" aria-hidden="true"/>
                        </div>
                        <div>
                            <h1 className="text-2xl font-semibold tracking-normal text-slate-950">
                                NetMoshen
                            </h1>
                        </div>
                    </div>
                </header>

                <section className="flex flex-col gap-3 gap-6 py-6 lg:grid-cols-[minmax(0,1fr)_360px]">

                    <p className="text-2xl text-center text-slate-900 font-bold">
                        Проверка сайта на мошенничество
                    </p>

                    <div className="space-y-1">
                        <form
                            onSubmit={handleSubmit}
                            className="rounded-lg border border-slate-200 bg-white p-4 shadow-panel sm:p-5"
                        >
                            <label
                                htmlFor="domain"
                                className="mb-2 block text-sm font-medium text-slate-700"
                            >
                                Введите ссылку на сайт
                            </label>
                            <div className="flex flex-col gap-3 sm:flex-row text-xl">
                                <div className="relative flex-1">
                                    <Globe2
                                        className="pointer-events-none absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400"
                                        aria-hidden="true"
                                    />
                                    <input
                                        id="domain"
                                        value={domain}
                                        onChange={(event) => setDomain(event.target.value)}
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

                        <section className="rounded-lg border shadow-panel">

                            {result && badStatuses.length === 0 ? (
                                <div className="flex items-start gap-3 rounded-md border border-emerald-200 bg-emerald-50 px-3 py-3 text-sm text-emerald-800">
                                    <CheckCircle2 className="mt-0.5 h-5 w-5 shrink-0" aria-hidden="true"/>
                                    <span>Сайт полностью безопасен.</span>
                                </div>
                            ) : null}


                            {badStatuses.length > 0 ? (
                                <div className="overflow-hidden rounded-md border border-slate-200">
                                    <div className="grid grid-cols-[1.2fr_0.8fr_1fr] bg-slate-50 px-3 py-2 text-xs font-medium uppercase text-slate-500">
                                        <span>Источник</span>
                                        <span>Категория</span>
                                        <span>Вердикт</span>
                                    </div>
                                    <div className="divide-y divide-slate-200">
                                        {badStatuses.map((status) => (
                                            <div
                                                key={`${status.source}-${status.result}`}
                                                className="grid grid-cols-[1.2fr_0.8fr_1fr] gap-2 px-3 py-3 text-sm"
                                            >
                        <span className="break-words font-medium text-slate-800">
                          {status.source}
                        </span>
                                                <span className="text-red-700">
                          {status.category ?? "Нет данных"}
                        </span>
                                                <span className="break-words text-slate-700">
                          {status.result ?? "Нет данных"}
                        </span>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            ) : null}
                        </section>
                    </div>

                    <aside className="space-y-5">
                        <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-panel sm:p-5">
                            <div className="mb-4 flex items-center gap-3">
                                <StatusIcon state={safetyState} isLoading={isLoading}/>
                                <div>
                                    <h2 className="text-lg font-semibold text-slate-950">
                                        {getStatusTitle(safetyState, isLoading)}
                                    </h2>
                                    <p className="text-sm text-slate-600">
                                        {result ? domain : "Ожидает проверки"}
                                    </p>
                                </div>


                            </div>

                            <div className="grid grid-cols-2 gap-3">
                                <Metric label="Злонамеренно" value={stats.malicious ?? 0}/>
                                <Metric label="Подозрительный" value={stats.suspicious ?? 0}/>
                                <Metric label="Безвредно" value={stats.harmless ?? 0}/>
                                <Metric label="Не найдено" value={stats.undetected ?? 0}/>
                            </div>

                        </section>


                        <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-panel sm:p-5">
                            <h2 className="mb-4 text-lg font-semibold text-slate-950">Информация о домене</h2>
                            <dl className="space-y-3 text-sm">
                                <InfoRow label="Домен" value={whois?.domain_org ?? domain}/>
                                <InfoRow label="Создан" value={whois?.created_at}/>
                                <InfoRow label="Обновлён" value={whois?.updated_at}/>
                                <InfoRow label="Регистратор" value={formatValue(whois?.registrar)}/>
                                <InfoRow label="Владелец" value={formatValue(whois?.registrant)}/>
                            </dl>
                        </section>
                    </aside>
                </section>
            </div>
        </main>
    );
}

function StatusIcon({
                        state,
                        isLoading,
                    }: {
    state: SafetyState;
    isLoading: boolean;
}) {
    const baseClasses = "flex h-12 w-12 items-center justify-center rounded-lg";

    if (isLoading) {
        return (
            <div className={`${baseClasses} bg-slate-100 text-slate-600`}>
                <Loader2 className="h-6 w-6 animate-spin" aria-hidden="true"/>
            </div>
        );
    }

    if (state === "danger") {
        return (
            <div className={`${baseClasses} bg-red-100 text-red-700`}>
                <ShieldAlert className="h-6 w-6" aria-hidden="true"/>
            </div>
        );
    }

    if (state === "safe") {
        return (
            <div className={`${baseClasses} bg-emerald-100 text-emerald-700`}>
                <ShieldCheck className="h-6 w-6" aria-hidden="true"/>
            </div>
        );
    }

    return (
        <div className={`${baseClasses} bg-amber-100 text-amber-700`}>
            <AlertTriangle className="h-6 w-6" aria-hidden="true"/>
        </div>
    );
}

function getStatusTitle(state: SafetyState, isLoading: boolean) {
    if (isLoading) {
        return "Проверяем";
    }

    if (state === "danger") {
        return "Ссылка опасна";
    }

    if (state === "safe") {
        return "Ссылка безопасна";
    }

    return "Нет результата";
}

function Metric({label, value}: { label: string; value: number }) {
    return (
        <div className="rounded-md bg-slate-50 px-3 py-3">
            <div className="text-xs font-medium uppercase text-slate-500">{label}</div>
            <div className="mt-1 text-2xl font-semibold text-slate-950">{value}</div>
        </div>
    );
}

function InfoRow({label, value}: { label: string; value: unknown }) {
    return (
        <div>
            <dt className="text-xs font-medium uppercase text-slate-500">{label}</dt>
            <dd className="mt-1 break-words text-slate-800">{formatValue(value)}</dd>
        </div>
    );
}
