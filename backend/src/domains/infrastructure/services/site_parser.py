from urllib.parse import urljoin, urlparse, urlunparse

import user_agent

from domains.domain.interfaces.service import ServiceI
from domains.infrastructure.services.request import Client
from bs4 import BeautifulSoup


class SiteParser(ServiceI):
    def __init__(self, client: Client | None = None):
        headers = {"User-Agent": user_agent.generate_user_agent()}
        self.client = client or Client(headers=headers)

    async def get_info(self, domain: str) -> dict:
        url = self._normalize_url(domain)

        try:
            html = await self.client.send_request("GET", url, return_json=False)

        except Exception as exc:
            return {
                "available": False,
                "url": url,
                "error": str(exc),
            }

        return self._parse_page(html, url)

    def _parse_page(self, html: str, url: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")
        links = self._get_all_links(html, url)
        internal_links, external_links = self._split_links(url, links)
        forms_info = self._get_forms_info(soup, url)
        suspicious_signals = self._get_suspicious_signals(
            url=url,
            internal_links=internal_links,
            external_links=external_links,
            forms_info=forms_info,
        )

        return {
            "available": True,
            "url": url,
            "title": self._get_title(soup),
            "description": self._get_description(soup),
            "links": {
                "total": len(links),
                "internal": len(internal_links),
                "external": len(external_links),
                "sample": links[:20],
            },
            "forms": forms_info,
            "suspicious_signals": suspicious_signals,
        }

    def _normalize_url(self, domain: str) -> str:
        value = domain.strip()
        if not value.startswith(("http://", "https://")):
            value = f"https://{value}"

        return value

    def _get_all_links(self, html: str, base_url: str) -> list[str]:
        links: list[str] = []
        seen: set[str] = set()
        soup = BeautifulSoup(html, "html.parser")

        for a in soup.find_all("a", href=True):
            url = self._normalize_link(a["href"], base_url)
            if not url or url in seen:
                continue

            seen.add(url)
            links.append(url)

        return links

    def _normalize_link(self, href: str, base_url: str) -> str | None:
        href = href.strip()
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            return None

        url = urljoin(base_url, href)
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            return None

        return urlunparse(parsed._replace(fragment=""))

    def _split_links(self, base_url: str, links: list[str]) -> tuple[list[str], list[str]]:
        base_host = self._host_without_www(base_url)
        internal_links = []
        external_links = []

        for link in links:
            link_host = self._host_without_www(link)
            if link_host == base_host or link_host.endswith(f".{base_host}"):
                internal_links.append(link)
            else:
                external_links.append(link)

        return internal_links, external_links

    def _host_without_www(self, url: str) -> str:
        host = urlparse(url).netloc.lower()
        if host.startswith("www."):
            return host[4:]

        return host

    def _get_title(self, soup: BeautifulSoup) -> str | None:
        if not soup.title or not soup.title.string:
            return None

        return soup.title.string.strip()

    def _get_description(self, soup: BeautifulSoup) -> str | None:
        description = soup.find("meta", attrs={"name": "description"})
        if not description:
            description = soup.find("meta", attrs={"property": "og:description"})

        content = description.get("content") if description else None
        return content.strip() if content else None

    def _get_forms_info(self, soup: BeautifulSoup, base_url: str) -> dict:
        forms = soup.find_all("form")
        password_fields = 0
        external_actions = []
        base_host = self._host_without_www(base_url)

        for form in forms:
            password_fields += len(form.find_all("input", attrs={"type": "password"}))
            action = form.get("action")
            if not action:
                continue

            action_url = self._normalize_link(action, base_url)
            if not action_url:
                continue

            action_host = self._host_without_www(action_url)
            if action_host != base_host and not action_host.endswith(f".{base_host}"):
                external_actions.append(action_url)

        return {
            "total": len(forms),
            "password_fields": password_fields,
            "external_actions": external_actions[:10],
        }

    def _get_suspicious_signals(
        self,
        url: str,
        internal_links: list[str],
        external_links: list[str],
        forms_info: dict,
    ) -> list[str]:
        signals = []

        if urlparse(url).scheme != "https":
            signals.append("not_https")

        if forms_info["password_fields"] > 0:
            signals.append("password_input")

        if forms_info["external_actions"]:
            signals.append("external_form_action")

        if external_links and len(external_links) > max(len(internal_links), 3):
            signals.append("many_external_links")

        return signals
