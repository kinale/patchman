# Copyright 2010 VPAC
# Copyright 2013-2021 Marcus Furlong <furlongm@gmail.com>
#
# This file is part of Patchman.
#
# Patchman is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Patchman is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Patchman  If not, see <http://www.gnu.org/licenses/>.

from humanize import naturaltime
from datetime import datetime, timedelta
from urllib.parse import urlencode

from django.conf import settings
from django.template import Library
from django.template.loader import get_template
from django.utils.html import format_html
from django.templatetags.static import static
from django.core.paginator import Paginator

register = Library()


@register.simple_tag
def active(request, pattern):
    import re
    if re.search(f"^{request.META['SCRIPT_NAME']!s}/{pattern!s}",
                 request.path):
        return 'active'
    return ''


@register.simple_tag
def yes_no_img(boolean, alt_yes='Active', alt_no='Not Active'):
    yes_icon = static('img/icon-yes.gif')
    no_icon = static('img/icon-no.gif')
    if boolean:
        html = f'<img src="{yes_icon!s}" alt="{alt_yes!s}" />'
    else:
        html = f'<img src="{no_icon!s}" alt="{alt_no!s}" />'
    return format_html(html)


@register.simple_tag
def no_yes_img(boolean, alt_yes='Not Required', alt_no='Required'):
    yes_icon = static('img/icon-yes.gif')
    no_icon = static('img/icon-no.gif')
    if not boolean:
        html = f'<img src="{yes_icon!s}" alt="{alt_yes!s}" />'
    else:
        html = f'<img src="{no_icon!s}" alt="{alt_no!s}" />'
    return format_html(html)


@register.simple_tag
def gen_table(object_list, template_name=None):
    if not object_list:
        return ''
    if not template_name:
        app_label = object_list.model._meta.app_label
        model_name = object_list.model._meta.verbose_name.replace(' ', '')
        template_name = f'{app_label!s}/{model_name.lower()!s}_table.html'
    template = get_template(template_name)
    html = template.render({'object_list': object_list})
    return html


@register.simple_tag
def object_count(page):
    if isinstance(page.paginator, Paginator):
        if page.paginator.count == 1:
            name = page.paginator.object_list.model._meta.verbose_name
        else:
            name = page.paginator.object_list.model._meta.verbose_name_plural
    return f'{page.paginator.count!s} {name!s}'


@register.simple_tag
def get_querystring(request):
    get = request.GET.copy()
    if 'page' in get:
        del get['page']
    return urlencode(get)


@register.simple_tag
def searchform(terms):
    template = get_template('searchbar.html')
    html = template.render({'post_url': '.', 'terms': terms})
    return html


@register.simple_tag
def reports_timedelta():
    if hasattr(settings, 'DAYS_WITHOUT_REPORT') and \
            isinstance(settings.DAYS_WITHOUT_REPORT, int):
        days = settings.DAYS_WITHOUT_REPORT
    else:
        days = 14
    return naturaltime(datetime.now() - timedelta(days=days))
