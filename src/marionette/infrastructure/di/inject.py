# pyright: reportExplicitAny=false
from collections.abc import Callable
from functools import wraps
from typing import (
    Annotated,
    Any,
    AsyncContextManager,
    TypeVar,
    cast,
    get_args,
    get_origin,
    get_type_hints,
)

T = TypeVar("T")
_InjectMarker = type("_InjectMarker", (), {})
_MARKER = _InjectMarker()

type Inject[T] = Annotated[T, _MARKER]


# typing.Any momento
def inject(
    get_container: Callable[[], AsyncContextManager[Any]],
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Any:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            async with get_container() as container:
                hints = get_type_hints(func, include_extras=True)
                
                annotations = {
                    name: get_args(hint)[0]
                    for name, hint in hints.items()
                    if get_origin(hint) is Inject
                }
                injected = {
                    name: await container.get(dependency)
                    for name, dependency in annotations.items()
                }
                return await func(*args, **kwargs, **injected)

        # Заставляем crescent думать, что там на самом деле Any - он это съест и всем будет хорошо
        # Решение не лучшее да и вообще лучше так было не делать, но...
        # мне плевать.
        return cast(Any, wrapper)

    return decorator
