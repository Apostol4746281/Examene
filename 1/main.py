from checker import build_url, is_https, show_response, check_site, scan_sites, check_headers, retry_check

print("--- Testare Atestare 1 ---")


print("\n[Partea 1]")
print("build_url:", build_url("example.com", "login"))
print("build_url cu /:", build_url("example.com", "/login"))
print("is_https (True):", is_https("https://example.com"))
print("is_https (False):", is_https("http://example.com"))


print("\n[Partea 2]")
show_response("https://example.com")


print("\n[Partea 3]")
print("check_site valid:", check_site("https://example.com"))
print("check_site invalid:", check_site("http://site-care-nu-exista-12345.invalid"))


print("\n[Partea 4]")
scan_sites()


print("\n[Partea 5]")
print("check_headers:", check_headers("https://example.com"))


print("\n[Partea 6]")
print("retry_check 200:", retry_check("https://httpbin.org/status/200"))
print("retry_check 404:", retry_check("https://httpbin.org/status/404"))
