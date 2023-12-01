from django import template

register = template.Library()

@register.filter(name="get_item")
def get_item(dictionary, key):
    
      return  dictionary.get(str(key))

@register.filter(name="get_listitem")
def get_listitem(list):
    
    if(len(list) > 0) :
        return  list[0]
    else:
         return''