# -*- coding: utf-8 -*-

from inspect import isclass, getmembers, isroutine


class Feature(object):
    """
    Base class for feature.

    :param obj: Object providing this feature
    :type obj: any
    """

    name = None

    def __init__(self, obj, *args, **kwargs):
        super(Feature, self).__init__(*args, **kwargs)

        self.obj = obj


def addfeatures(features):
    """
    Add features to a class.

    :param features: Features to add
    :type features: list

    :returns: decorator
    :rtype: callable
    """

    for feature in features:
        if not isclass(feature) or Feature not in feature.mro():
            raise TypeError('Expecting a Feature class, got: {0}'.format(
                feature.__name__
                if hasattr(feature, '__name__')
                else type(feature)
            ))

    def decorator(cls):
        features_list = getattr(cls, '__features__', [])
        features_list.extend(features)
        cls.__features__ = features_list

        return cls

    return decorator


def getfeatures(obj):
    """
    Get list of features provided by an object's class.

    :param obj: Object
    :type obj: any

    :returns: List of provided features
    :rtype: list
    """

    def _getfeatures(obj, cache):
        result = []

        if obj not in cache:
            cache.add(obj)
            bases = obj.__class__.mro()

            for base in reversed(bases):
                result += [
                    (obj, feature_cls)
                    for feature_cls in getattr(base, '__features__', [])
                ]

            members = [
                m
                for n, m in getmembers(obj)
                if not isroutine(m)
                and not isclass(m)
                and not n.startswith('__')
            ]

            for member in members:
                result += _getfeatures(member, cache)

        return result

    cache = set()
    return _getfeatures(obj, cache)


def hasfeature(obj, name):
    """
    Check if object's class provides a feature.

    :param obj: Object
    :type obj: any

    :param name: Feature's name
    :type name: str

    :returns: True if feature is provided
    :rtype: bool
    """

    for _, feature in getfeatures(obj):
        if feature.name == name:
            return True

    return False


def getfeature(obj, name, *args, **kwargs):
    """
    Instantiate a feature.

    :param obj: Object
    :type obj: any

    :param name: Feature's name
    :type name: str

    :param args: Positional arguments for feature's constructor
    :type args: Iterable

    :param kwargs: Keyword arguments for feature's constructor
    :type kwargs: dict

    :returns: Instance of feature
    :rtype: Feature

    :raises AttributeError: if feature is not provided by object's class
    """

    for _obj, feature in getfeatures(obj):
        if feature.name == name:
            return feature(_obj, *args, **kwargs)

    raise AttributeError('No such feature: {0}'.format(name))
