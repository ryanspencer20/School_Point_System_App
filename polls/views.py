from django.http import HttpResponse


def index(request):
    index_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <h1>Hello, world. You're at the polls index.</h1>
        <!--<a href="/polls/next/">Next Page</a>-->
        <button onclick="window.location.href='/polls/next/'">Next Page</button>
    </body>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 50px;
        }
        h1 {
            color: #333;
        }
    </style>
    <script>
        // You can add JavaScript here if needed
        
    </script>
    </html>
    """
    return HttpResponse(index_html)

def next_page(request):
    next_page_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <h1>This is the next page!.</h1>
        <!--<a href="/polls/next/">Next Page</a>-->
        <button onclick="window.location.href='/polls/index/'">Next Page</button>
    </body>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 50px;
        }
        h1 {
            color: #333;
        }
    </style>
    <script>
        // You can add JavaScript here if needed
        
    </script>
    </html>
    """
    return HttpResponse(next_page_html)