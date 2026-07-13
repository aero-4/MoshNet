export const API_URL =
    import.meta.env.VITE_API_URL ?? "http://localhost:8000/domains/analyze/";

export function resolveApiAssetUrl(path?: string | null) {
    if (!path) {
        return null;
    }

    return new URL(path, API_URL).toString();
}

export const SITE_SIGNAL_LABELS: Record<string, string> = {
    not_https: "Страница открывается без HTTPS",
    password_input: "На странице есть поле ввода пароля",
    external_form_action: "Форма отправляет данные на другой домен",
    many_external_links: "Внешних ссылок больше, чем внутренних",
};
