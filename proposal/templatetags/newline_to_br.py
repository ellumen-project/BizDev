from django import template
from django.utils.html import mark_safe
from django.template.defaulttags import register


register = template.Library()

@register.filter(name='newline_to_br')
def newline_to_br(value):
    return mark_safe(value.replace('\n', '<br>'))

# sections = text.split('\n\n')
# results={}

# for section in sections:
#     if ': ' in section:
#         question, result =section.split(':',1)
#         results[question]=result


# t = Template("""
# {% load newline_to_br %}
# {% for question, result in results.items %}
#     <h2>{{question}}</h2>
#     <p>{{result|newline_to_br|safe}}</p>
# {% endfor %}
# """)

# c = Context({"results": results})
# formatted_text = t.render(c)