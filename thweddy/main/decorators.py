from django.core import serializers
from django.http import HttpResponse
from django.utils import simplejson
from django.db.models import Model

def jsonify(fn, *args, **kwargs):
    """ Decorator that serializes the output of a function, most likely
    a view, as JSON, and returns the JSON in a HttpResponse.
    Inspired by Pylon's jsonify controller decorator.
    """
    def wrapper(*args, **kwargs):
        output = fn(*args, **kwargs)
        try:
            value = simplejson.dumps(output)
        except TypeError:
            json_serializer = serializers.get_serializer('json')
            serializer = json_serializer()
            try:
                serializer.serialize(output)
                value = serializer.getvalue()
            except TypeError, e:
                # Try using jsonpickle if available
                try:
                    import jsonpickle
                    value = jsonpickle.encode(output)
                except ImportError:
                    raise e

        return HttpResponse(value)
    return wrapper