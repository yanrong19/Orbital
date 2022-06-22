from django import template
from django.utils.safestring import mark_safe
register = template.Library()

readmore_showscript = ''.join([
"this.parentNode.style.display='none';",
"this.parentNode.parentNode.getElementsByClassName('more')[0].style.display='inline';",
"return false;",
])

@register.filter
def readmore(txt, maxchara):
    global readmore_showscript
    chara = list(txt)

    if len(chara) <= maxchara:
        return txt

    # wrap the more part
    chara.insert(maxchara, '<span class="more" style="display:none;">')
    chara.append('</span>')

    # insert the readmore part
    chara.insert(maxchara, '<span class="readmore">... <a href="#" onclick="')
    chara.insert(maxchara+1, readmore_showscript)
    chara.insert(maxchara+2, '">read more</a>')
    chara.insert(maxchara+3, '</span>')

    return mark_safe(''.join(chara))

readmore.is_safe = True