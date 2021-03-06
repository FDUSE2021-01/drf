

# DRF 后端

下列接口已部署至服务器端，且已实现 `api_view`，大部分 `GET` 类接口（收藏相关接口除外）可以通过浏览器直接访问获得可视化的数据表示。

特别好用的 Chrome 接口测试插件：Talend API Tester

好用的 HTTP 接口测试工具：http://tool.chinaz.com/tools/httptest.aspx?jdfwkey=5yvss1



## 1 用户验证

用于进行用户身份验证的 API，采用 JWT 的方式。

客户端与服务器进行一次用户名-密码验证后得到 Token，此后客户端应保存好 Token，以此向服务器证明自己的身份。Access Token 的有效期较短（60分钟），Refresh Token 的有效期较长（1天），在 Refresh Token 失效前客户端可以向服务器端请求“续费”。用户注销时客户端应妥善销毁 Token。



现存用户名与密码：

```
超级用户
root:se2021 (id:1)

普通用户
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
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJ......rscsS_r9J39Kt6wyvEY",
    "id": "1",
    "username": "root"
}
```



### 1.2 /api/token/refresh/

Access Token 有效较短，Refresh Token 有效期较长，可以通过 refresh 获取新的 Access Token。

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



## 2 用户信息管理

可以以超级用户 (root: se2021) 身份登录 /api/admin/，从后台管理所有用户。



### 2.1 /api/users/registration/

用于用户注册，3个域均为必填，其中邮箱可能在以后会进行验证。

```
POST /api/users/registration/

Request Header:
Content-Type: application/json

Request Body:
{
    "username": "user2",
    "password": "pass2",
    "email": "a@b.com"
}
```

创建成功的回复：
```
201 Created

Response Body:
{
    "id": 18,
    "email": "a@b.com",
    "last_login": null,
    "is_superuser": false,
    "username": "user2",
    "first_name": "",
    "last_name": "",
    "is_staff": false,
    "is_active": false,
    "date_joined": "2021-04-08T12:22:18.514507Z",
    "groups":[],
    "user_permissions":[],
    "favorite_articles":[]
}
```

注意 is_active 为 false 代表需要验证。
后端会检查 `username` 是否被注册，否则以 json 格式返回 `400 Bad Request`：

```
{
    "username":["已存在一位使用该名字的用户。"]
}
```

若有字段未填写，后端将同样以 json 格式返回 `400 Bad Request`：

```
{
    "password":["该字段是必填项。"]
}
```



### 2.2 /api/users/activation?token=\<token\>

用于用户注册后的验证，用户注册后服务器会向用户注册的邮箱发送一条带token的验证邮件，用户点击邮件链接导向前端，前端处理得到token后，给本api发送GET request，若token相同即验证用户邮箱成功。

```
GET /api/users/activation?token=test
```



### 2.3 /api/users/\<int\>/

用户登录后可以查看、更新、删除自己的信息。

更新时可以使用 PUT 或 PATCH，两者格式相同。

- 使用 PUT 时，至少需要提供 `username`, `password`, `email`，其余部分选填，未填的部分在数据库中将保留原值（而不会被置为null）。
- 使用 PATCH 时，可以只提供需要更新的属性（例如只改 `username` ），进行局部更新。

两者的区别是根据 HTTP 方法的语义确定的。一般而言，使用 PATCH 可能会更灵活。

```
GET /api/users/17/

Request Header:
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1......8I3-qocnoMJl2w
```

```
PUT/PATCH /api/users/17/

Request Header:
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1......8I3-qocnoMJl2w
Content-Type: application/json

Request Body:
{
    "username": "user1",
    "password": "pass1",
    "email": "c@d.com"
}
```

```
DELETE /api/users/17/

Request Header:
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1......8I3-qocnoMJl2w
```

### 2.4 /api/users/password_change/

登录状态下更新密码，需要再次提供旧密码以作为验证

```
PUT /api/users/password_change/

Request Header:
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1......8I3-qocnoMJl2w
Content-Type: application/json

Request Body:
{
    "old_password": "123456",
    "new_password": "myNewPassword",
}
```

## 3 Articles

用户登录以后可以上传、更新、删除文章。未登录用户可以阅读文章。



### 3.1 /api/articles/

支持 GET 和 POST，用于获取文章列表，以及发布新文章。

#### 3.1.1 GET

##### 3.1.1.1 基本操作

获取分页后的文章列表，不需要登陆，不需要发送其他信息。

可以通过指定 `page_size` 来控制每一页的文章数（默认为3）

- 例如：`GET /api/articles/?page_size=2&page=1` 

Response 中的 `count` 表示文章总数， `next` 和 `previous` 为下一页和上一页的 URI 。

```
GET /api/articles/ 或 GET /api/articles/?page=1

Response Body:
{
    "count": 5,
    "next": "http://127.0.0.1:8000/api/articles/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "favorite": false,
            "created": "2021-03-31T08:56:54.086998Z",
            "title": "T1",
            "content_html": "Hi\nThis is article 1",
            "content_md": "default markdown content",
            "content_brief": "Default content brief",
            "img_src": "/path/to/img",
            "view_count": 1,
            "fav_count": 0,
            "author": 1
        },
        {
            "id": 2,
            ...
            "author": 1
        }
    ]
}
```

##### 3.1.1.2 过滤条件

GET 时可添加过滤条件的组合：

```
GET /api/articles/?page=1&ordering=-view_count
```

可选过滤参数如下：

- **page**
  - 获取分页后的第某页：`page=1`
- **ordering**
  - 按某属性排序，默认以升序排列： `ordering=author`
  - 以降序排列：`ordering=-view_count`
  - 先按 `-view_count` 再按 `author` 排序（可叠加多个）：`ordering=-view_count,author`
- **search**
  - 在 `title` , `content_brief` 和  `content_md` 中进行关键字匹配（英文不分大小写）：`search=文本`
- **article 中的任意属性**
  - 例如找到发布者为root的所有文章：`author=1`
  - 例如标题为 `T1` 的文章：`title=T1`



#### 3.1.2 POST

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
    "content_html": "Hi\nThis is article 1",
    "content_md": "default markdown content",
    "img_src": "/path/to/img"
}
```



### 3.2 /api/articles/\<int\>/

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
    "content_html": "Modified article 2.",
    "content_md": "default markdown content",
    "content_brief": "Default content brief",
    "img_src": "/path/to/img"
}
```



## 4 Files

用户登录以后可以上传、更新、删除图片，游戏插件等文件。未登录用户可以浏览与下载用户上传的图片，游戏插件等文件。



### 4.1 /api/upload/

支持 GET 和 POST，用于获取上传文件列表，以及发布新文件。

#### 4.1.1 GET

获取分页后的文件列表，不需要登陆，不需要发送其他信息。

Response 中的 `count` 表示文件总数， `next` 和 `previous` 为下一页和上一页的 URI 。

```
GET /api/upload/

Response Body:
{
    "count": 5,
    "next": "http://127.0.0.1:8000/api/upload/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "created": "2021-04-08T11:03:22.694071Z",
            "name": "Little-Snowman",
            "file": "http://127.0.0.1:8000/upload/IMG_1.jpeg",
            "author": null
        },
        {
            "id": 2,
            "created": "2021-04-08T11:08:58.322979Z",
            "name": "DOTA4",
            "file": "http://127.0.0.1:8000/upload/IMG_1443.jpeg",
            "author": null
        }
    ]
}
```
其余与3.1.1的article接口类似。



#### 4.1.2 POST

头部需要带上 JWT Access Token，即放在 `Bearer` 后面的字符串。 

HTTP Body 以 Form 格式传输，需要包含的内容如下。

```
POST /api/upload/

Request Header:
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1......8I3-qocnoMJl2w
Content-Type: application/json

Request Body:
{
    "name": "DOTA7",
    "file": "http://127.0.0.1:8000/upload/IMG_1443_HO9B90f.jpeg",
}
```

其中name为Text格式，file为File格式。



### 4.2 /api/upload/\<int\>/

例如 `/api/upload/1/` 。

用户登录后，可对自己写的文件进行修改、删除。

GET 则不需要登陆，无需提供 `Authorization` 头部。

- GET: 获取这份文件
- PUT: 更新这份文件
- DELETE: 删除这篇文章

以 GET 为例：

```
GET /api/articles/6/

Request Header:
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1......8I3-qocnoMJl2w
Content-Type: application/json

Response Body:
{
    "name": "DOTA7",
    "file": "http://127.0.0.1:8000/upload/IMG_1443_HO9B90f.jpeg",
}
```



## 5 收藏文章

用户可以收藏自己喜欢的文章。

- 若需要得到用户1的文章收藏列表，可以通过 GET /api/users/1/ ，然后查看其中的 `favorite_articles` 项得到相应文章编号。
- 一篇文章的收藏量可通过其 `fav_count` 属性查看。
- 用户登录后，可查看文章的 `favorite` 属性（取值为 true 或 false）来知道自己是否收藏了它，未登录时永远为 false 。

下面是添加、检查、删除收藏的接口，使用以下接口都需要带 token 。



### 5.1 /api/users/fav-articles/

#### 5.1.1 POST

`article_id` 表示想要收藏的文章的编号。

```
POST /api/users/fav-articles/

Request Header:
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1......8I3-qocnoMJl2w
Content-Type: application/json

Request Body:
{
    "article_id": "1"
}
```



#### 5.1.2 GET

用户在登陆后可以获取分页后的收藏文章列表。

可以通过指定 `page_size` 来控制每一页的文章数（默认为3）

- 例如：`GET /api/users/fav-articles/?page_size=2&page=1` 

```
GET /api/users/fav-articles/

Request Header:
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1......8I3-qocnoMJl2w
Content-Type: application/json

Response Body:
{
    "count": 4,
    "next": "http://127.0.0.1:8000/api/upload/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "favorite": true,
            "title": "任天堂游戏大放送",
            ...
            "author": 1
        },
        {
            ...
        },
        {
        	...
        }
    ]
}
```



### 5.2 /api/users/fav-articles/\<int:pk\>/

- GET: 询问自己是否有收藏编号为 `pk` 的文章
  - 已收藏：返回 HTTP 200 OK
  - 未收藏：返回 HTTP 404 NOT FOUND
- DELETE: 取消收藏编号为 `pk` 的文章
  - 取消成功：返回 HTTP 204 NO CONTENT
  - 未收藏或文章本身不存在：返回 HTTP 404 NOT FOUND
