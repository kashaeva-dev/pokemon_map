from django.db import connection


class CountQueriesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        query_count = len(connection.queries)

        print(f"Number of queries: {query_count}")

        return response
