from rest_framework import pagination


# https://www.sankalpjonna.com/learn-django/pagination-made-easy-with-django-rest-framework
class MyPageNumberPagination(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 50
    # page_query_param = 'page'
