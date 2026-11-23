import json

from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.html import _json_script_escapes
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=True)
def ld_json(data):
    """Render a dict as a JSON-LD <script>, escaped like json_script so text can't close the tag."""
    if not data:
        return ""
    payload = json.dumps(data, cls=DjangoJSONEncoder, ensure_ascii=False).translate(_json_script_escapes)
    return mark_safe(f'<script type="application/ld+json">{payload}</script>')
