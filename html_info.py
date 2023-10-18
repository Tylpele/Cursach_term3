from urllib.parse import urlparse


def get_website_name(url):
    try:
        parsed_url = urlparse(url)
        host = parsed_url.netloc

        parts = host.split('.')

        if len(parts) >= 2:
            return parts[-2]

        return host
    except:
        return "Некорректная ссылка"
