import {Metric} from "./common/Metric";
import {StatusIcon} from "./common/StatusIcon";
import type {SafetyState} from "../types/analyze";

type StatusCardProps = {
    domain: string;
    isLoading: boolean;
    hasResult: boolean;
    safetyState: SafetyState;
    stats: Record<string, number>;
};

export function StatusCard({
    domain,
    isLoading,
    hasResult,
    safetyState,
    stats,
}: StatusCardProps) {
    return (
        <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-panel sm:p-5">
            <div className="mb-4 flex items-center gap-3">
                <h1 className="font-bold text-lg">Действия на сайте</h1>
            </div>

            <div className="grid grid-cols-2 gap-3">
                <Metric label="Злонамеренные" value={stats.malicious ?? 0}/>
                <Metric label="Подозрительные" value={stats.suspicious ?? 0}/>
                <Metric label="Безвредные" value={stats.harmless ?? 0}/>
                <Metric label="Пустые" value={stats.undetected ?? 0}/>
            </div>
        </section>
    );
}

function getStatusTitle(state: SafetyState, isLoading: boolean) {
    if (isLoading) {
        return "Проверяем";
    }

    if (state === "danger") {
        return "Сайт опасен";
    }

    if (state === "safe") {
        return "Сайт безопасен";
    }

    return "Нет результатов";
}
