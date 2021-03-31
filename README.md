# DRF 后端

下列接口已部署至服务器端，且已实现 `api_view`，大部分 `GET` 类接口可以通过浏览器直接访问获得可视化的数据表示。

特别好用的 Chrome 接口测试插件：Talend API Tester

好用的 HTTP 接口测试工具：http://tool.chinaz.com/tools/httptest.aspx?jdfwkey=5yvss1



## 1 用户验证

用于进行用户身份验证的 API，采用 JWT 的方式。**暂时未实现用户注册的功能，仅支持现存用户的登录。**

客户端与服务器进行一次用户名-密码验证后得到 Token，此后客户端应保存好 Token，以此向服务器证明自己的身份。Token 的有效期较短（5分钟），在失效前客户端可以向服务器端请求“续费”。用户注销时客户端应妥善销毁 Token。



现存用户名与密码：

```
超级用户
root:se2021

普通用户
lzh:nb
obangw:nb
xiaoas:nb
pryest:nb
```



### 1.1 /api/token/

客户端向 API 发送用户名和密码，API 返回 Access Token 和 Refresh Token。

```
POST /api/token/

Request Header:
Content-Type: application/json

Request Body:
{
	"username": "root",
	"password": "se2021"
}

Response Body:
{
	"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIU......JiO4veZEbTE",
	"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJ......rscsS_r9J39Kt6wyvEY"
}
```



### 1.2 /api/token/refresh/

Token 5分钟后过期，在此之前可以进行 refresh 获取新的 Access Token，并刷新 Refresh Token 的有效期。

```
POST /api/token/refresh/

Request Header:
Content-Type: application/json

Request Body:
{
	"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIU......JiO4veZEbTE"
}

Response Body:
{
	"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1......8I3-qocnoMJl2w"
}
```





## 2 Articles

用户登录以后可以上传、更新、删除文章。未登录用户可以阅读文章。



### 2.1 /api/articles/

支持 GET 和 POST，用于获取文章列表，以及发布新文章。

#### 2.1.1 GET

获取分页后的文章列表，不需要登陆，不需要发送其他信息。在当前的测试阶段，一页中限制最多2篇文章。

Response 中的 `count` 表示文章总数， `next` 和 `previous` 为下一页和上一页的 URI 。

```
GET /api/articles/

Response Body:
{
    "count": 5,
    "next": "http://127.0.0.1:8000/api/articles/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "created": "2021-03-31T08:56:54.086998Z",
            "title": "T1",
            "content": "Hi\nThis is article 1",
            "author": 1
        },
        {
            "id": 2,
            "created": "2021-03-31T10:06:25.610410Z",
            "title": "T2",
            "content": "Hi\nThis is article 2",
            "author": 1
        }
    ]
}
```

请求第3页：

```
GET /api/articles/?page=3

{
    "count": 5,
    "next": null,
    "previous": "http://127.0.0.1:8000/api/articles/?page=2",
    "results": [
        {
            "id": 5,
            "created": "2021-03-31T10:59:41.401458Z",
            "title": "T5",
            "content": "Hi\nThis is article 5",
            "author": 1
        }
    ]
}
```



#### 2.1.2 POST

头部需要带上 JWT Access Token，即放在 `Bearer` 后面的字符串。 

HTTP Body 以 JSON 格式传输，需要包含的内容如下。

```
POST /api/articles/

Request Header:
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1......8I3-qocnoMJl2w
Content-Type: application/json

Request Body:
{
    "title": "T1",
    "content": "Hi\nThis is article 1"
}
```



### 2.2 /api/articles/\<int\>/

例如 `/api/articles/1/` 。

用户登录后，可对自己写的文章进行修改、删除。

GET 则不需要登陆，无需提供 `Authorization` 头部。

- GET: 获取这篇文章
- PUT: 更新这篇文章
- DELETE: 删除这篇文章

以 PUT 为例：

```
PUT /api/articles/2/

Request Header:
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1......8I3-qocnoMJl2w
Content-Type: application/json

Request Body:
{
    "title": "T2",
    "content": "Modified article 2."
}
```




