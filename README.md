# http-warmup

Python script / Docker image that waits for an HTTP server to come online and optionally 
warms it up by sending some requests to it.

## Usage

**Wait for a host to reply with an HTTP 2xx response:**

```
docker run --rm -it heyman/http-warmup https://example.org
```

**Send 20 warm-up requests using three threads once the server has come alive:**

```
docker run --rm -it heyman/http-warmup --warmup-requests=20 --warmup-threads=3 https://example.org
```

**Set the max time that we should wait for the server to come alive to 5 minutes**:

```
docker run --rm -it heyman/http-warmup --timeout=300 https://example.org
```

## Options

```
Usage: warmup.py [OPTIONS] URLS...

  At least one URL must be specified. The first URL is pinged until it returns
  a 2xx HTTP response.

  If --warmup-requests is used the URLs will be round robin picked from all
  specified URLS

Options:
  --timeout INTEGER          Number of seconds to wait for the host to come
                             online. Default: 60
  --warmup-requests INTEGER  Number of warm-up requests to send. Default: 0
  --warmup-threads INTEGER   Number of threads used to send the warm-up
                             requests. Default: 1
  --request-timeout INTEGER  Request timeout for individual HTTP requests.
                             Default: 5
  --hostname TEXT            Overrides the `Hostname` HTTP request header if
                             specified
  -v, --verbose
  --help                     Show this message and exit.
```
