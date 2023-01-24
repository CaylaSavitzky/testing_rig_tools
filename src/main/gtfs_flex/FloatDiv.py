"""
Acts as a folium plugin to allow text to appear with map
This page i built based on: https://github.com/python-visualization/folium/blob/main/folium/plugins/float_image.py
"""
from branca.element import MacroElement
from jinja2 import Template


class FloatDiv(MacroElement):
    """Adds a floating div in HTML canvas on top of the map.
    Parameters
    ----------
    content: str
        Add anything into this div.
    bottom: int, default 75
        Vertical position from the bottom, as a percentage of screen height.
    left: int, default 75
        Horizontal position from the left, as a percentage of screen width.
    overflow: str, default scroll
        select an option from standard css options
    height: 
    **kwargs
        Additional keyword arguments are applied as CSS properties.
        For example: `width='300px'`.
    """

    _template = Template(
        """
            {% macro header(this,kwargs) %}
                <style>
                    #{{this.get_name()}} {
                        position: absolute;
                        bottom: {{this.bottom}}%;
                        left: {{this.left}}%;
                        height: {{this.height}}%;
                        width: {{this.width}}%;
                        overflow: {{this.overflow}};
                        {%- for property, value in this.css.items() %}
                          {{ property }}: {{ value }};
                        {%- endfor %}
                        }
                </style>
            {% endmacro %}
            {% macro html(this,kwargs) %}
            <div id="{{this.get_name()}}" alt="float_image"
                 style="z-index: 999999">
                 {{this.contents}}
            </div>
            {% endmacro %}
            """
    )

    def __init__(
        self, contents, bottom=75, 
        left=75,height = 100,width = 40, 
        overflow="auto", **kwargs):
        super().__init__()
        self._name = "FloatDiv"
        self.contents = contents
        self.bottom = bottom
        self.left = left
        self.height=height
        self.width=width
        self.overflow = overflow
        self.css = kwargs