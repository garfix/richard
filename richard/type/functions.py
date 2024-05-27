from typing import Callable


Binary = Callable[[any, any], any]
Unary = Callable[[any], any]
Nonary = Callable[[], any]
