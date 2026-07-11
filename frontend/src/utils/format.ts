export function formatValue(value: unknown) {
    if (!value) {
        return "Нет данных";
    }

    if (typeof value === "string" || typeof value === "number") {
        return String(value);
    }

    if (typeof value === "object") {
        const entries = Object.entries(value as Record<string, unknown>);
        const firstTextValue = entries.find(([, item]) => typeof item === "string");
        return firstTextValue ? String(firstTextValue[1]) : "Есть данные";
    }

    return "Нет данных";
}
