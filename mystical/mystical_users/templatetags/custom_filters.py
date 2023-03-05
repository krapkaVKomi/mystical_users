from django import forms
from django import template

register = template.Library()


@register.filter
def add_class_and_placeholder_to_field(field, class_name):
    widget = field.field.widget
    label_text = field.label
    field.label = ''
    if isinstance(widget, forms.CheckboxInput):
        return field.as_widget(attrs={'class': class_name})
    else:
        attrs = widget.attrs
        attrs['class'] = attrs.get('class', '') + ' ' + class_name
        attrs['placeholder'] = label_text
        return field.as_widget(attrs=attrs)


