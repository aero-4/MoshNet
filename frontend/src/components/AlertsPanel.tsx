import {Flat} from "@alptugidin/react-circular-progress-bar";
import {AlertTriangle, CheckCircle2} from "lucide-react";

import {resolveApiAssetUrl} from "../constants/analyze";
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

    const riskColor = getRiskColor(result.risk_score);
    const screenshotUrl = resolveApiAssetUrl(result.site?.screenshot);

    return (
        <section className="rounded-lg border bg-white p-4 shadow-panel sm:p-5">
            <div className="flex flex-col gap-5 flex-1 w-full">

                {result.risk_score >= 300 && (
                    <div className="flex items-center flex-row gap-2 rounded-md border border-amber-200 bg-red-50 px-3 py-3 text-sm text-red-500">
                        <AlertTriangle className="mt-0.5 h-8 w-8 shrink-0" aria-hidden="true"/>
                        <div className="flex flex-col text-3xl">
                            <span className="">Сайт очень опасен!</span>
                            <span>НЕМЕДЛЕННО выйдите с данного сайта!</span>
                            <span>НИ В КОЕМ СЛУЧАЕ НЕЛЬЗЯ ВВОДИТЬ: коды доступа, пароли, свои персональные данные, скачивать файлы!</span>
                        </div>
                    </div>
                )}

                {result.risk_score < 300 && result.risk_score > 0 && (
                    <div className="flex items-center flex-row gap-2 rounded-md border border-amber-200 bg-orange-50 px-3 py-3 text-sm text-orange-500">
                        <AlertTriangle className="mt-0.5 h-8 w-8 shrink-0" aria-hidden="true"/>
                        <span className="text-xl md:text-2xl">Сайт подозрительный. Будьте внимательны</span>
                    </div>
                )}

                {result.risk_score === 0 && (
                    <div className="flex gap-3 items-center rounded-md border border-emerald-200 bg-emerald-50 px-3 py-3 text-sm text-emerald-800">
                        <CheckCircle2 className="mt-0.5 h-8 w-8 shrink-0" aria-hidden="true"/>
                        <span className="text-xl md:text-2xl">Сайт безопасен</span>
                    </div>
                )}


                <div className="mx-auto flex w-full flex-row flex-wrap items-center justify-center gap-6">


                    <div className="flex min-w-0 flex-1 basis-80 flex-col gap-1">
                        {screenshotUrl ? (
                            <img
                                src={screenshotUrl}
                                alt="Скриншот сайта"
                                className="max-h-[560px] w-full max-w-xs rounded-md border border-slate-300 object-contain"
                            />
                        ) : null}

                        <a href={result.site?.url} className="hover:text-blue-600">Название: {result.site?.title}</a>
                        <span>Описание: {result.site?.description}</span>
                    </div>

                    <div className="flex flex-col gap-2">
                        {result.status.map((status) => (
                            <p className="text-xs bg-red-50 text-red-600 p-3 rounded-full">
                                {status}
                            </p>
                    ))}
                    </div>

                    <div className="w-72 shrink-0 [&_svg]:h-auto [&_svg]:w-full">
                        <Flat
                            progress={result.risk_score}
                            range={{from: 0, to: 1000}}
                            sign={{value: "", position: "end"}}
                            text="Общая оценка опасности"
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

            </div>


        </section>
    );
}


function getRiskColor(score: number) {
    if (score >= 400) {
        return "#bb0000";
    }
    if (score > 200 && score <= 300) {
        return "#dc2626";
    }
    if (score > 100 && score <= 200) {
        return "#FF6A00FF";
    }
    if (score > 50 && score <= 100) {
        return "#FFFA00FF"
    }

    return "#16a34a";
}
