from urllib.parse import urlparse
import sites_list


def get_website_name(url):
    try:
        parsed_url = urlparse(url)
        host = parsed_url.netloc

        parts = host.split('.')

        if len(parts) >= 2:
            return parts[-2]

        return host
    except:
        return None


def is_correct_link(url):
    correct_sites = sites_list.static_sites + sites_list.dynamic_sites

    website_name = get_website_name(url)

    if website_name is None:
        return False

    return website_name in correct_sites


def make_standart_link(new_url):
    if not new_url.startswith("https://www.") and not new_url.startswith("http://www."):
        if not new_url.startswith("www."):
            if not new_url.startswith("https://"):
                return "https://www." + new_url
            return new_url
        return "https://" + new_url

    return new_url
