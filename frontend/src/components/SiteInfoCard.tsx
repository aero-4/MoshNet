import {AlertTriangle} from "lucide-react";

import {resolveApiAssetUrl, SITE_SIGNAL_LABELS} from "../constants/analyze";
import type {SiteInfo} from "../types/analyze";
import {InfoRow} from "./common/InfoRow";
import {Metric} from "./common/Metric";

type SiteInfoCardProps = {
    site?: SiteInfo;
};

export function SiteInfoCard({site}: SiteInfoCardProps) {
    const siteSignals = site?.suspicious_signals ?? [];
    const screenshotUrl = resolveApiAssetUrl(site?.screenshot);

    return (
        <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-panel sm:p-5">
            <h2 className="mb-4 text-lg font-semibold text-slate-950">Страница сайта</h2>
            {site?.available === false ? (
                <div className="rounded-md border border-amber-200 bg-amber-50 px-3 py-3 text-sm text-amber-800">
                    {site.error ?? "Не удалось загрузить страницу"}
                </div>
            ) : (
                <>
                    <dl className="space-y-3 text-sm">
                        <InfoRow label="URL" value={site?.url}/>
                        <InfoRow label="Заголовок" value={site?.title}/>
                        <InfoRow label="Описание" value={site?.description}/>
                    </dl>

                    <div className="mt-4 grid grid-cols-2 gap-3">
                        <Metric label="Ссылки" value={site?.links?.total ?? 0}/>
                        <Metric label="Внешние" value={site?.links?.external ?? 0}/>
                        <Metric label="Формы" value={site?.forms?.total ?? 0}/>
                        <Metric label="Пароли" value={site?.forms?.password_fields ?? 0}/>
                    </div>

                    {screenshotUrl ? (
                        <div className="mt-4 overflow-hidden rounded-md border border-slate-200 bg-slate-100">
                            <img
                                src={screenshotUrl}
                                alt="Скриншот сайта"
                                className="h-auto w-full object-contain"
                            />
                        </div>
                    ) : null}

                    {siteSignals.length > 0 ? (
                        <div className="mt-4 space-y-2 rounded-md border border-amber-200 bg-amber-50 px-3 py-3 text-sm text-amber-800">
                            {siteSignals.map((signal) => (
                                <div key={signal} className="flex items-start gap-2">
                                    <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true"/>
                                    <span>{SITE_SIGNAL_LABELS[signal] ?? signal}</span>
                                </div>
                            ))}
                        </div>
                    ) : null}
                </>
            )}
        </section>
    );
}
