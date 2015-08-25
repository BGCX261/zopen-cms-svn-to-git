# -*- encoding:utf-8 -*-
from string import Template

navitem_template = Template(r"""
        <li class="navTreeItem visualNoMarker ${class_str}"
            kssattr:nodeurl="${node_url}">
            <div class="visualIcon contenttype-folder">
                <a border="0" href="${node_url}${view_name}" class="visualIconPadding 
                ${a_class_str}" name="${node_name}" onfocus="this.blur()">
                ${mi_str}
                ${pl_str}
                <img src="${icon_src}" href="" border="0" />
                ${node_title}
                    </a>
            </div>
            ${children_str}
        </li>
            """)
