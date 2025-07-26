import pytest
from classendar.decorator import dated_class
from datetime import date


@dated_class
class Foo:
    def __init__(self, foo_arg=None, **kwargs):
        self.foo_arg = foo_arg
        print(f"Foo initialized with foo_arg={foo_arg}")

    async def get(self, **kwargs):
        return "Base Foo result"


class Foo_20250701(Foo):
    async def get(self, **kwargs):
        return "Foo_20250701 result"


@pytest.mark.asyncio
async def test_classender():
    # Test
    foo = Foo(foo_arg="test")
    result = await foo.get(date=date(2025, 7, 15))  # Returns "Foo_20250701 result"
    assert result == 'Foo_20250701 result'

    result = await foo.get(date=date(2025, 6, 15))  # Returns "Foo_20250701 result"
    assert result == 'Base Foo result'    