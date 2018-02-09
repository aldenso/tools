# Restful API

Restful api example using standard flask and flask-limiter (rate limiter).

Create you virtual environment and activate it.

```sh
$ python -m venv flaskapp
$ source flaskapp/bin/activate
(flaskapp)$
```

Install flask and flask-limiter.

```sh
(flaskapp)$ pip install flask flask-limiter
```

or use the requirements file.

```sh
(flaskapp)$ pip install -r requirements.txt
```

Run the api server.

```sh
(flaskapp)$ python main.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 224-828-976
```

Show all items.

```sh
$ curl http://localhost:5000/myapp/api/v1/items -X GET
{
  "items": [
    {
      "description": "some description for item1",
      "id": 1,
      "name": "item1"
    },
    {
      "description": "something",
      "id": 3,
      "name": "item3"
    }
  ]
}
```

Create item.

```sh
$ curl http://localhost:5000/myapp/api/v1/items -X POST -d '{"name":"item3", "description":"something"}' -H "Content-Type: application/json"
{
  "item": {
    "description": "something",
    "id": 3,
    "name": "item3"
  }
}
```

Show item by id.

```sh
$ curl http://localhost:5000/myapp/api/v1/items/id/3 -X GET
{
  "item": {
    "description": "something",
    "id": 3,
    "name": "item3"
  }
}
```

Show item by name.

```sh
$ curl http://localhost:5000/myapp/api/v1/items/name/item3 -X GET
{
  "item": {
    "description": "something",
    "id": 3,
    "name": "item3"
  }
}
```

Update item by id.

```sh
$ curl http://localhost:5000/myapp/api/v1/items/id/2 -X PUT -d '{"name":"item2", "description":"something new"}' -H "Content-Type: application/json"
{
  "item": [
    {
      "description": "something new",
      "id": 2,
      "name": "item2"
    }
  ]
}
```

Delete item by id.

```sh
$ curl http://localhost:5000/myapp/api/v1/items/id/2 -X DELETE -v
* About to connect() to localhost port 5000 (#0)
*   Trying ::1...
* Connection refused
*   Trying 127.0.0.1...
* Connected to localhost (127.0.0.1) port 5000 (#0)
> DELETE /myapp/api/v1/items/id/2 HTTP/1.1
> User-Agent: curl/7.29.0
> Host: localhost:5000
> Accept: */*
>
* HTTP 1.0, assume close after body
< HTTP/1.0 204 NO CONTENT
< Content-Type: text/html; charset=utf-8
< Content-Length: 0
< Server: Werkzeug/0.12.2 Python/3.4.5
< Date: Sun, 03 Sep 2017 22:35:23 GMT
<
* Closing connection 0

$ curl http://localhost:5000/myapp/api/v1/items/id/2 -X GET
{
  "error": "Not found"
}
$ curl http://localhost:5000/myapp/api/v1/items -X GET
{
  "items": [
    {
      "description": "some description for item1",
      "id": 1,
      "name": "item1"
    },
    {
      "description": "something",
      "id": 3,
      "name": "item3"
    }
  ]
}
```

When you hit some rate limiter, you'll see a response like this.

```sh
{
  "error": "Too Many Requests"
}
```
