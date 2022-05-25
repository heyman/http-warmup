# http-warmup

Python script / Docker image for waiting for an HTTP server to come up and optionally warm it up 
by sending some requests to it.

## Usage

**Just wait for a host to reply with a HTTP 2xx response:**

```
docker run --rm -it heyman/http-warmup https://example.org
```

**Send 20 warm-up requests using 3 threads, once the server has come alive:**

```
docker run --rm -it heyman/http-warmup --warmup-requests=20 --warmup-threads=3 https://example.org
```

**Set the max time that we should wait for the server to come alive to 5 minutes**:

```
docker run --rm -it heyman/http-warmup --timeout=300 https://example.org
```

