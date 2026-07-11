export function normalizeDomain(value: string) {
    return value.trim().replace(/^https?:\/\//i, "").replace(/\/.*$/, "");
}
