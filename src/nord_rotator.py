from requests_ip_rotator  import ApiGateway, EXTRA_REGIONS, ALL_REGIONS

# Gateway to outbound HTTP IP and port for only two regions
gateway_1 = ApiGateway("http://1.1.1.1:8080", regions=["eu-west-1"])

# Gateway to HTTPS google for the extra regions pack, with specified access key pair
gateway_2 = ApiGateway("https://www.google.com", regions=EXTRA_REGIONS, access_key_id="AKIAUFNRUFUP4J4ES2Z7", access_key_secret="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")
with ApiGateway("https://google.com") as g:
    session = requests.Session()
    session.mount("https://google.com", g)

    response = session.get("https://google.com/")
    print(response.status_code)