from datetime import date
import re
from functools import wraps


class Versioned:
    """
    Class decorator that adds date-based versioning to a class.
    Usage:
        @Versioned
        class MyClass:
            ...
    """
    def __init__(self, cls):
        self.cls = cls
        self._subclass_cache = {}
        self._wrap_methods()

    def _wrap_methods(self):
        # Store original methods
        original_init = self.cls.__init__
        original_get = getattr(self.cls, 'get', None)

        @wraps(original_init)
        def __init__(self, *args, **kwargs):
            self._init_kwargs = kwargs.copy()
            if original_init:
                original_init(self, *args, **kwargs)

        async def get(self, date=None, **kwargs):
            date = date or date.today()
            versioned_cls = self._get_versioned_subclass(date)
            
            if versioned_cls is not self.__class__:
                return await versioned_cls(**self._init_kwargs).get(date=date, **kwargs)
            
            if original_get:
                return await original_get(self, **kwargs)
            raise NotImplementedError("Subclasses must implement get()")

        # Apply the wrapped methods
        self.cls.__init__ = __init__
        self.cls.get = get

    def _get_versioned_subclass(self, target_date):
        if self.cls not in self._subclass_cache:
            self._subclass_cache[self.cls] = self._collect_subclasses()

        for subclass, subclass_date in sorted(
            self._subclass_cache[self.cls].items(),
            key=lambda x: x[1],
            reverse=True
        ):
            if target_date >= subclass_date:
                return subclass
        return self.cls

    def _collect_subclasses(self):
        subclasses = {}

        def _recursive_collect(base_class):
            for subclass in base_class.__subclasses__():
                match = re.search(r'_(\d{4})(\d{2})(\d{2})$', subclass.__name__)
                if match:
                    year, month, day = map(int, match.groups())
                    subclasses[subclass] = date(year, month, day)
                _recursive_collect(subclass)

        _recursive_collect(self.cls)
        return subclasses

    def __call__(self, *args, **kwargs):
        return self.cls(*args, **kwargs)