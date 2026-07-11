import {InfoRow} from "./common/InfoRow";
import type {DomainInfo} from "../types/analyze";

type DomainInfoCardProps = {
    domain: string;
    whois?: DomainInfo;
};

export function DomainInfoCard({domain, whois}: DomainInfoCardProps) {
    return (
        <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-panel sm:p-5">
            <h2 className="mb-4 text-lg font-semibold text-slate-950">
                Информация о домене
            </h2>
            <dl className="space-y-3 text-sm">
                <InfoRow label="Создан" value={whois?.created_at}/>
                <InfoRow label="Обновлён" value={whois?.updated_at}/>
                <InfoRow label="Регистратор" value={whois?.registrar}/>
                <InfoRow label="Владелец" value={whois?.registrant}/>
            </dl>
        </section>
    );
}
