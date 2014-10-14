from django.db import connection
from django.template import Template, Context


class SQLLogMiddleware:

    def process_response ( self, request, response ):
        time = 0.0
        #for q in connection.queries:
		#time += float(q['time'])
        time = sum([float(q['time']) for q in connection.queries])

        t = Template('''
            <hr>
            <div class="container">
            <p><em>Total query count:</em> <code>{{ count }}</code><br/>
            <em>Total execution time:</em> <code>{{ time }}s</code></p>
            <ul class="sqllog">
                {% for sql in sqllog %}
                    <li><code>[{{ sql.time }}s]: {{ sql.sql }}</code></li>
                {% endfor %}
            </ul>
            </div>
        ''')

        #response.content = "%s%s" % ( response.content, t.render(Context({'sqllog':connection.queries,'count':len(connection.queries),'time':time})))
        #return response
        content = response.content.decode('utf-8')
        content += t.render(Context({'sqllog':connection.queries,'count':len(connection.queries),'time':time}))
        response.content = content.encode('utf-8')

        return response

from django.conf import settings

#
# Log all SQL statements direct to the console (when running in DEBUG)
# Intended for use with the django development server.
#

class SQLLogToConsoleMiddleware:
    def process_response(self, request, response):
        if settings.DEBUG and connection.queries:
            time = sum([float(q['time']) for q in connection.queries])
            t = Template("{{count}} quer{{count|pluralize:\"y,ies\"}} in {{time}} seconds:\n\n{% for sql in sqllog %}[{{forloop.counter}}] {{sql.time}}s: {{sql.sql|safe}}{% if not forloop.last %}\n\n{% endif %}{% endfor %}")
            print t.render(Context({'sqllog':connection.queries,'count':len(connection.queries),'time':time}))
        return response