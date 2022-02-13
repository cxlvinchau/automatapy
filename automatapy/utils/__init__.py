import abc


class SingletonMetaclass(abc.ABCMeta):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.obj = None

    def __call__(cls, *args, **kwargs):
        if cls.obj is None:
            cls.obj = super().__call__(args, kwargs)
        return cls.obj
