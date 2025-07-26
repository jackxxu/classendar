from classendar.decorator import Versioned


class ParentClass:
    def __init__(self, **kwargs):
        self.parent_arg = kwargs.get("parent_arg")

@Versioned
class Foo(ParentClass):
    def __init__(self, foo_arg=None, **kwargs):
        super().__init__(**kwargs)
        self.foo_arg = foo_arg

    async def get(self, **kwargs):
        return "Base Foo result"

class Foo_20250701(Foo):
    async def get(self, **kwargs):
        return "Foo_20250701 result"

# # Test
# foo = Foo(foo_arg="hello", parent_arg="world")
# result = await foo.get(date=date(2025, 7, 15))  # Returns "Foo_20250701 result"