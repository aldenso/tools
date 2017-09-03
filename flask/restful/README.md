Restful API
===========

Restful api example using standard flask.

Install flask.

```
pip install flask
```

Run api server.

```
(flaskapp)$ python main.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 224-828-976
```

Show all items.

```
(flaskapp)$ curl http://localhost:5000/myapp/api/v1/items -X GET
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

```
(flaskapp)$ curl http://localhost:5000/myapp/api/v1/items -X POST -d '{"name":"item3", "description":"something"}' -H "Content-Type: application/json"
{
  "item": {
    "description": "something",
    "id": 3,
    "name": "item3"
  }
}
```

Show item by id.

```
(flaskapp)$ curl http://localhost:5000/myapp/api/v1/items/id/3 -X GET
{
  "item": {
    "description": "something",
    "id": 3,
    "name": "item3"
  }
}
```

Show item by name.

```
(flaskapp)$ curl http://localhost:5000/myapp/api/v1/items/name/item3 -X GET
{
  "item": {
    "description": "something",
    "id": 3,
    "name": "item3"
  }
}
```

Update item by id.

```
(flaskapp)$ curl http://localhost:5000/myapp/api/v1/items/id/2 -X PUT -d '{"name":"item2", "description":"something new"}' -H "Content-Type: application/json"
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

```
(flaskapp) [aldenso@ansible myapp]$ curl http://localhost:5000/myapp/api/v1/items/id/2 -X DELETE -v
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

(flaskapp)$ curl http://localhost:5000/myapp/api/v1/items/id/2 -X GET
{
  "error": "Not found"
}
(flaskapp)$ curl http://localhost:5000/myapp/api/v1/items -X GET
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