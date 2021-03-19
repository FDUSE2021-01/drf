# DRF 后端

简单地做了个API，作测试用，已经部署到服务器上。



## 1 Articles

可以上传、下载、删除文章。



### 1.1 数据格式

以 JSON 格式传输，有三个域，`title`可以为空，`id`不需要提供，由后台自动生成。

```json
{
    "content": "Hi\nThis is article 1\n",
    "id": 1,
    "title": ""
}
```



### 1.2 API

提供2类URI：

- 173.82.119.100:8000/api/articles/
  - GET: 获取所有文章
  - POST: 上传一篇文章
- 173.82.119.100:8000/api/articles/1/(或者任何其它存在的文章ID)
  - GET: 获取这篇文章
  - PUT: 更新这篇文章（上传一篇新的把原来的换掉）
  - DELETE: 删除这篇文章



### 1.3 调用示例

GET  http://173.82.119.100:8000/api/articles/

以下是返回结果：

```
HTTP/1.1 200 OK
Content-Length: 144
Content-Type: application/json
Date: Thu, 18 Mar 2021 11:43:58 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

[
    {
        "content": "Hi\nThis is article 1\n",
        "id": 1,
        "title": ""
    },
    {
        "content": "This is article 2 with a title.\n",
        "id": 2,
        "title": "Number Two"
    }
]
```

