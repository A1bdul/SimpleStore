from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict


class CustomPagination(pagination.PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 36
    page_query_param = 'p'
    
    def get_paginated_response(self, data):
        return Response({
            'count' : self.page.paginator.count,
            'next' : self.get_next_link(),
            'previous': self.get_previous_link(),
            'pages' : self.page.paginator.num_pages,
            'size': len(data),
            'current_page' :self.page.number,
            'result': data
        })
    