
import time
from concurrent.futures import ThreadPoolExecutor

import click
import requests



@click.command()
@click.argument("urls", nargs=-1, required=True)
@click.option("--timeout", default=60, help="Number of seconds to wait for the host to come online. Default: 60")
@click.option("--warmup-requests", default=0, help="Number of warm-up requests to send. Default: 0")
@click.option("--warmup-threads", default=1, help="Number of threads used to send the warm-up requests. Default: 1")
@click.option("--request-timeout", default=5, help="Request timeout for individual HTTP requests. Default: 5")
@click.option("--hostname", help="Overrides the `Hostname` HTTP request header if specified")
@click.option("-v", "--verbose", is_flag=True)
def main(urls, timeout, request_timeout, warmup_requests, warmup_threads, hostname, verbose):
    """
    At least one URL must be specified. The first URL is pinged until it returns a 2xx HTTP response.
    
    If --warmup-requests is used the URLs will be round robin picked from all specified URLS
    """
    def get(url):
        headers = {}
        if hostname:
            headers["Host"] = hostname
        try:
            response = requests.get(url, headers=headers, timeout=request_timeout)
        except requests.exceptions.RequestException as e:
            if verbose:
                print("GET", url, "-->", "FAILED:", str(e))
            raise
        if verbose:
            print("GET", url, "-->", "HTTP", response.status_code, "(%i bytes)" % len(response.content))
        return response

    def wait_for_host():
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = get(urls[0])
            except requests.exceptions.RequestException:
                pass
            else:
                if response.status_code >= 200 and response.status_code < 300:
                    return True
            time.sleep(1)
        return False

    print("Waiting for host: %s" % urls[0])
    if wait_for_host():
        print("Got successful (2xx) HTTP response")
        if warmup_requests:
            print("Sending %i warmup requests to %i URLs (round robin) using %i threads" % (warmup_requests, len(urls), warmup_threads))
            with ThreadPoolExecutor(max_workers=warmup_threads) as executor:
                for i in range(warmup_requests):
                    executor.submit(get, urls[i%len(urls)])
                print("Waiting for requests to finish")
    else:
        print("Did not get a 2xx HTTP response within %s seconds" % timeout)
        return 1


if __name__ == "__main__":
    main()
