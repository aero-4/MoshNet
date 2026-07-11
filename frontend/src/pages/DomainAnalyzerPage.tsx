import type {FormEvent} from "react";
import {useMemo, useState} from "react";

import {AlertsPanel} from "../components/AlertsPanel";
import {AnalyzeForm} from "../components/AnalyzeForm";
import {AppHeader} from "../components/AppHeader";
import {DomainInfoCard} from "../components/DomainInfoCard";
import {SiteInfoCard} from "../components/SiteInfoCard";
import {StatusCard} from "../components/StatusCard";
import {analyzeDomain} from "../services/analyze";
import type {AnalyzeResult} from "../types/analyze";
import {normalizeDomain} from "../utils/domain";
import {getAnalyzeCriteria, getSafetyState} from "../utils/safety";

export function DomainAnalyzerPage() {
    const [domain, setDomain] = useState("");
    const [result, setResult] = useState<AnalyzeResult | null>(null);
    const [error, setError] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [criteria, setCriteria] = useState<string[]>([]);

    const virusTotal = useMemo(
        () => (result ? result.virustotal : undefined),
        [result],
    );
    const whois = useMemo(() => (result ? result.whois : undefined), [result]);
    const site = useMemo(() => (result ? result.site : undefined), [result]);
    const badStatuses = virusTotal?.bad_statuses ?? [];
    const stats = virusTotal?.last_analysis_stats ?? {};
    const safetyState = getSafetyState(virusTotal, criteria);

    async function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();

        const normalizedDomain = normalizeDomain(domain);
        if (!normalizedDomain) {
            setError("Введите сайт");
            setResult(null);
            setCriteria([]);
            return;
        }

        setIsLoading(true);
        setError("");
        setResult(null);
        setCriteria([]);

        try {
            const payload = await analyzeDomain(normalizedDomain);
            setResult(payload);
            setDomain(normalizedDomain);
            setCriteria(getAnalyzeCriteria(payload));
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
            <div className="mx-auto flex min-h-screen w-full max-w-6xl flex-col px-4 py-3 sm:px-6 lg:px-8">
                <AppHeader/>

                <section className="gap-3 flex flex-col py-6 lg:grid-cols-[minmax(0,1fr)_360px]">
                    <p className="py-9 text-center text-xl md:text-4xl font-bold text-slate-900">
                        Проверка сайта на мошенничество
                    </p>

                    <AnalyzeForm
                        domain={domain}
                        error={error}
                        isLoading={isLoading}
                        onDomainChange={setDomain}
                        onSubmit={handleSubmit}
                    />
                    <AlertsPanel
                        result={result}
                        badStatuses={badStatuses}
                        criteria={criteria}
                    />

                    <StatusCard
                        domain={domain}
                        isLoading={isLoading}
                        hasResult={Boolean(result)}
                        safetyState={safetyState}
                        stats={stats}
                    />
                    <DomainInfoCard domain={domain} whois={whois}/>
                </section>
            </div>
        </main>
    );
}
