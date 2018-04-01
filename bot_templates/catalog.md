Пицца из нашего меню:

{% for entry in catalog -%}
*{{ entry.title }} #{{loop.index}}*
{{ entry.description }}
    {%- for choice in entry.choices %}
        {{ choice.title }} - *{{ choice.price }} руб.*
    {%- endfor %}

{% endfor %}
