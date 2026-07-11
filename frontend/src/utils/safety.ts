import {SITE_SIGNAL_LABELS} from "../constants/analyze";
import type {AnalyzeResult, DomainInfo, SafetyState} from "../types/analyze";

export function getSafetyState(
    virusTotal: DomainInfo | undefined,
    criteria: string[],
): SafetyState {
    if (criteria.length > 0) {
        return "danger";
    }

    if (!virusTotal?.last_analysis_stats && !virusTotal?.bad_statuses?.length) {
        return "unknown";
    }

    const stats = virusTotal.last_analysis_stats ?? {};
    const hasBadStats = (stats.malicious ?? 0) > 0 || (stats.suspicious ?? 0) > 0;
    const hasBadStatuses = Boolean(virusTotal.bad_statuses?.length);

    return hasBadStats || hasBadStatuses ? "danger" : "safe";
}

export function getAnalyzeCriteria(data: AnalyzeResult) {
    return [
        getAgeCriterion(data),
        ...getSiteCriteria(data),
    ].filter((item): item is string => Boolean(item));
}

function getSiteCriteria(data: AnalyzeResult) {
    const signals = data.site?.suspicious_signals ?? [];
    const criteria = [];

    if (signals.includes("not_https")) {
        criteria.push(SITE_SIGNAL_LABELS.not_https);
    }

    if (signals.includes("external_form_action")) {
        criteria.push(SITE_SIGNAL_LABELS.external_form_action);
    }

    if (signals.includes("many_external_links")) {
        criteria.push(SITE_SIGNAL_LABELS.many_external_links);
    }

    return criteria;
}

function getAgeCriterion(data: AnalyzeResult) {
    const createdAt = data.whois?.created_at;

    if (!createdAt) {
        return null;
    }

    const createdAtDate = new Date(createdAt);

    if (Number.isNaN(createdAtDate.getTime())) {
        return null;
    }

    const diffMs = Date.now() - createdAtDate.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    return diffDays < 90 ? "Домен младше 3 месяцев" : null;
}
