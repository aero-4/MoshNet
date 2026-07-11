import {Flat} from "@alptugidin/react-circular-progress-bar";
import {AlertTriangle, CheckCircle2} from "lucide-react";

import type {AnalyzeResult, BadStatus} from "../types/analyze";

type AlertsPanelProps = {
    result: AnalyzeResult | null;
    badStatuses: BadStatus[];
    criteria: string[];
};

export function AlertsPanel({result, badStatuses, criteria}: AlertsPanelProps) {
    if (!result) {
        return null;
    }

    const riskScore = normalizeRiskScore(result.risk_score);
    const riskColor = getRiskColor(riskScore);

    return (
        <section className="rounded-lg border bg-white p-4 shadow-panel sm:p-5">
            <div className="flex flex-col gap-5 flex-1 w-full">
                {riskScore >= 0 && (
                    <div className="flex gap-3 items-center rounded-md border border-emerald-200 bg-emerald-50 px-3 py-3 text-sm text-emerald-800">
                        <CheckCircle2 className="mt-0.5 h-8 w-8 shrink-0" aria-hidden="true"/>
                        <span className="text-xl md:text-2xl">Сайт безопасен</span>
                    </div>
                )}

                {riskScore >= 100 && (
                    <div className="flex items-center flex-row gap-2 rounded-md border border-amber-200 bg-orange-50 px-3 py-3 text-sm text-orange-500">
                        <AlertTriangle className="mt-0.5 h-8 w-8 shrink-0" aria-hidden="true"/>
                        <span className="text-xl md:text-2xl">Сайт подозрительный. Будьте внимательны</span>
                    </div>
                )}

                {riskScore >= 300 && (
                    <div className="flex items-center flex-row gap-2 rounded-md border border-amber-200 bg-red-50 px-3 py-3 text-sm text-red-500">
                        <AlertTriangle className="mt-0.5 h-8 w-8 shrink-0" aria-hidden="true"/>
                        <span className="text-xl md:text-2xl">Сайт опасен! Не вводите здесь никакие свои персональные данные, банковские карты, номера!</span>
                    </div>
                )}

                <div className="max-w-xs justify-center items-center mx-auto w-full">
                    <Flat
                        progress={result.risk_score}
                        range={{from: 0, to: 1000}}
                        sign={{value: "", position: "end"}}
                        text="Оценка небезоспасности"
                        showMiniCircle={true}
                        showValue={true}
                        sx={{
                            strokeColor: riskColor,
                            bgStrokeColor: "#e2e8f0",
                            bgColor: {value: "#ffffff", transparency: "00"},
                            barWidth: 3,
                            shape: "full",
                            strokeLinecap: "round",
                            valueSize: 12,
                            valueWeight: "bold",
                            valueColor: "#0f172a",
                            textSize: 5,
                            textWeight: "bold",
                            textColor: "#475569",
                            loadingTime: 500,
                            miniCircleColor: riskColor,
                            miniCircleSize: 2,
                            valueAnimation: true,
                            intersectionEnabled: false,
                        }}
                    />
                </div>

            </div>


        </section>
    );
}

function normalizeRiskScore(score: number) {
    return Math.min(100, Math.max(0, Math.round(score)));
}

function getRiskColor(score: number) {
    if (score >= 100) {
        return "#FFFA00FF"
    }
    if (score >= 200) {
        return "#FF6A00FF";
    }
    if (score >= 300) {
        return "#dc2626";
    }

    if (score >= 400) {
        return "#bb0000";
    }


    return "#16a34a";
}
