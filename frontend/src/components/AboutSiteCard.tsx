import {InfoRow} from "./common/InfoRow";
import type {DomainInfo} from "../types/analyze";
import {Metric} from "./common/Metric";
import {InfoBlock} from "./common/InfoBlock";

type DomainInfoCardProps = {
    domain: string;
    whois?: DomainInfo;
};

export function AboutSiteCard() {
    return (
        <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-panel sm:p-5">
            <h2 className="mb-4 text-lg font-semibold text-slate-950">
                Вопросы и ответы
            </h2>
            <dl className="space-y-3">
                <InfoBlock label="Зачем нужен этот сайт?" value="Мы специализируемся на проверки и анализе всей информации о домене и выдаем краткую статистику, можно ли доверять этому сайту и является ли он мошенническим."/>
                <InfoBlock label="Это бесплатно?" value="Да, для всех пользователей кто зашел на наш сайт анализ домена бесплатен."/>
                <InfoBlock label="Вы собираете информацию о моих поисках?" value="Мы не собираем и не храним никакую информацию о ваших анализах доменов. Вся информация, которую вы здесь получаете, обрабатывается как строго конфиденциальная в соответствии с общими правилами безопасности, что гарантирует защиту от доступа третьих лиц."/>
            </dl>
        </section>
    );
}
