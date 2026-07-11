import {API_URL} from "../constants/analyze";
import type {AnalyzeResult} from "../types/analyze";

export async function analyzeDomain(domain: string): Promise<AnalyzeResult> {
    const response = await fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({domain}),
    });

    if (!response.ok) {
        const detail = await response.json().catch(() => null);
        throw new Error(detail?.detail ?? `Ошибка запроса: ${response.status}`);
    }

    return response.json() as Promise<AnalyzeResult>;
}
