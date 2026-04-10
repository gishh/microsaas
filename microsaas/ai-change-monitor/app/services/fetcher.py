from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


USER_AGENT = "AIChangeMonitor/0.1"


def fetch_page(url: str, timeout: int = 15) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=timeout) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace")
    except (HTTPError, URLError) as exc:
        raise ValueError(f"Failed to fetch page: {exc}") from exc

