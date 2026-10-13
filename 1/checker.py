import requests

SITES = [
  
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
 
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
   
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
 
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    host = host.rstrip("/")
    path = path.lstrip("/")
    return f"https://{host}/{path}"


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.startswith("https://")


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    try:
        response = requests.get(url, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
    except Exception as e:
        print(f"Erore la cerere: {e}")


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        response = requests.get(url, timeout=5)
        content_type = response.headers.get("Content-Type", "").split(";")[0].strip()
        server = response.headers.get("Server", "unknown")
        return {
            "status": response.status_code,
            "content_type": content_type,
            "length": len(response.content),
            "server": server,
        }
    except requests.Timeout:
        return {"status": None, "error": "Timeout"}
    except requests.ConnectionError:
        return {"status": None, "error": "Erore conexiune"}
    except Exception as e:
        return {"status": None, "error": str(e)}


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    success_count = 0
    fail_count = 0

    for site in SITES:
        res = check_site(site)
        if res.get("status") == 200:
            success_count += 1
            print(f"{site} -> 200, {res['length']} octeți")
        else:
            fail_count += 1

    print(f"Reușite: {success_count} Eșuate: {fail_count}")


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        response = requests.get(url, timeout=5)
        response_headers_lower = {k.lower(): v for k, v in response.headers.items()}
        
        present = []
        missing = []

        for header in SECURITY_HEADERS:
            if header.lower() in response_headers_lower:
                present.append(header)
            else:
                missing.append(header)

        score = int((len(present) / len(SECURITY_HEADERS)) * 100)
        return {
            "present": present,
            "missing": missing,
            "score": score,
        }
    except Exception as e:
        return {"status": None, "error": str(e)}


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    last_status = None
    last_error = None
    
    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(url, timeout=5)
            last_status = response.status_code
            
            if last_status < 500:
                return {"status": last_status, "attempts": attempt}
                
        except (requests.Timeout, requests.ConnectionError) as e:
            last_error = str(e)
            last_status = None
        except Exception as e:
            last_error = str(e)
            last_status = None

    result = {"status": last_status, "attempts": attempts}
    if last_status is None and last_error:
        result["error"] = last_error
    return result
