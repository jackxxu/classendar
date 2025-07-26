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


class Foo_20250801(Foo_20250701):
    async def get(self, **kwargs):
        return "Foo_20250801 result"


class Foo_20250901(Foo_20250801):
    async def get(self, **kwargs):
        result = await super().get(**kwargs)
        return f"Foo_20250801 result + {result}"


@pytest.mark.asyncio
async def test_base_class():
    foo = Foo(foo_arg="test")
    result = await foo.get(date=date(2025, 6, 15))  
    assert result == 'Base Foo result'    


@pytest.mark.asyncio
async def test_2nd_layer():
    foo = Foo(foo_arg="test")
    result = await foo.get(date=date(2025, 7, 15))  
    assert result == 'Foo_20250701 result'


@pytest.mark.asyncio
async def test_3rd_layer():
    foo = Foo(foo_arg="test")
    result = await foo.get(date=date(2025, 8, 1))  
    assert result == 'Foo_20250801 result'


@pytest.mark.asyncio
async def test_reference_base():
    foo = Foo(foo_arg="test")
    result = await foo.get(date=date(2025, 9, 1))  
    assert result == 'Foo_20250801 result + Foo_20250801 result'

