# SECTION 1: DECORATORS

print("=" * 60)
print("SECTION 1: DECORATORS")
print("=" * 60)

def my_decorator(func):
    def wrapper():
        print("wrapper function executed")
        func()
        print("wrapper function executed")

    return wrapper

@my_decorator
def hello():
    print("hello")

hello()


# SECTION 2: PROPERTY DECORATORS

print("=" * 60)
print("SECTION 2: PROPERTY DECORATORS")
print("=" * 60)

# data validation, private / public (encapsulation)

class Person:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    # getter
    @property
    def name(self):
        return self.__name

    @name.setter  # değerini değiştirebilecek bir şey olduğunda kullanılabilir
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        if len(value) < 2:
            raise ValueError("name must be at least 2 characters")
        self.__name = value

    @name.deleter
    def name(self):
        self.__name = None

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        if not isinstance(value, int):
            raise TypeError("age must be an integer")
        if value < 0:
            raise ValueError("age must be >= 0")
        if value > 150:
            raise ValueError("age must be <= 150")
        self.__age = value

tuna = Person("Tuna", 18)
print(tuna.name)
tuna.name = "tuuuna"
print(tuna.name)
del tuna.name
print(tuna.name)
tuna.age = 43
print(tuna.age)


# SECTION 3: STATIC METHODS

print("=" * 60)
print("SECTION 3: STATIC METHODS")
print("=" * 60)

class MathOperations:

    @staticmethod
    def add(x, y):
        return x + y

    @staticmethod
    def divide(x, y):
        return x / y


print(MathOperations.add(10, 20))
print(MathOperations.divide(10, 20))


# SECTION 4: CLASS METHODS

print("=" * 60)
print("SECTION 4: CLASS METHODS")
print("=" * 60)

# alternative constructor

class Pizza:

    total_pizzas = 0

    def __init__(self, ingredients):
        self.ingredients = ingredients
        Pizza.total_pizzas += 1

    @classmethod
    def margherita(cls):
        return cls(["peynir", "domates", "fesleğen"])

    @classmethod
    def pepperoni(cls):
        return cls(["peynir", "sucuk", "domates"])

    @classmethod
    def get_total_pizzas(cls):
        return cls.total_pizzas


pizza1 = Pizza.margherita()
print(pizza1.ingredients)
pizza2 = Pizza.pepperoni()
print(pizza2.ingredients)
print(Pizza.get_total_pizzas())


# SECTION 5: ABSTRACT METHODS

print("=" * 60)
print("SECTION 5: ABSTRACT METHODS")
print("=" * 60)

from abc import ABC, abstractmethod


class Animal(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def make_sound(self):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def sleep(self):
        pass


class Dog(Animal):

    def make_sound(self):
        print("hav hav")

    def move(self):
        print("köpek yürüdü")

    def sleep(self):
        print("köpek uyudu")


barley = Dog("Barley")
barley.move()


# SECTION 6: FUNCTION OVERLOADING

print("=" * 60)
print("SECTION 6: FUNCTION OVERLOADING (@overload)")
print("=" * 60)

from typing import overload, Union


class Calculator:

    @overload
    def add(self, a: int, b: int) -> int:
        ...

    @overload
    def add(self, a: int, b: int, c: int) -> int:
        ...

    def add(self, a: int, b: int, c: int | None = None) -> int:
        if c is None:
            return a + b
        return a + b + c

    @overload
    def process(self, value: int) -> int:
        ...

    @overload
    def process(self, value: str) -> str:
        ...

    def process(self, value: Union[int, str]) -> Union[int, str]:
        if isinstance(value, int):
            return value * 2
        elif isinstance(value, str):
            return value.upper()
        else:
            raise ValueError("Value must be a string or an integer")


calculator = Calculator()
print(calculator.add(10, 20))
result = calculator.process("a")
print(result)


# SECTION 7: FINAL DECORATOR

print("=" * 60)
print("SECTION 7: FINAL DECORATOR (@final)")
print("=" * 60)

from typing import final


class BaseGame:

    def start(self):
        print("Game starting")

    @final
    def calculate_score(self, points: int) -> int:
        return points + 100


class MyGame(BaseGame):

    def start(self):
        print("MyGame starting")


@final
class SecretAlgorithm:

    def process(self):
        print("Secret algorithm running")


game = MyGame()
game.start()
print("Score:", game.calculate_score(50))

secret = SecretAlgorithm()
secret.process()


# SECTION 8: OVERRIDE DECORATOR

print("=" * 60)
print("SECTION 8: OVERRIDE DECORATOR (@override)")
print("=" * 60)

try:
    from typing import override
except ImportError:
    from typing_extensions import override


class Shape:

    def area(self) -> float:
        return 0.0


class Rectangle(Shape):

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    @override
    def area(self) -> float:
        return self.width * self.height


rect = Rectangle(5.0, 4.0)
print("Rectangle area:", rect.area())


# BONUS: COMBINING DECORATORS

print("=" * 60)
print("BONUS: COMBINING DECORATORS")
print("=" * 60)


def multiply_decorator(func):
    def wrapper(x: int):
        return func(x) * 2

    return wrapper


def other_decorator(func):
    def wrapper(x: int):
        return func(x) * 4

    return wrapper


@multiply_decorator
@other_decorator
def calculate(x: int):
    return x * 2


print("Combined decorators result:", calculate(10))