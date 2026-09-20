"""
PYTHON GELİŞMİŞ ÖZELLİKLER EĞİTİM REHBERİ (PYTHON ADVANCED FEATURES TUTORIAL)
=============================================================================

Bu eğitim rehberi, Python'ın ileri düzey özelliklerini kapsar:
Dekoratörler (Decorators), Özel Metotlar ve Tip İpuçları (Type Hints).

Kod standartlarına (Clean Code / Best Practices) uygun olması açısından tüm 
fonksiyon, sınıf, metot ve değişken isimleri İNGİLİZCE (örneğin my_decorator, 
say_hello, Person, MathOperations) olarak tanımlanmıştır. 
Gelecekte rahatça dönüp hatırlamanız için tüm açıklamalar, docstring'ler, 
yorumlar ve örnek anlatımları TÜRKÇE olarak hazırlanmıştır.

Kapsanan Konular:
1. Basic Decorators (Temel Dekoratörler)
2. Property Decorators (@property, @setter, @deleter)
3. Static Methods (@staticmethod)
4. Class Methods (@classmethod)
5. Abstract Methods (@abstractmethod)
6. Function Overloading (@overload)
7. Final Classes and Methods (@final)
8. Override Decorator (@override)
9. Bonus: Combining Decorators (Çoklu Dekoratör Kullanımı)
10. Summary and Best Practices (Özet ve En İyi Pratikler)
"""

# ============================================================================
# BÖLÜM 1: BASIC DECORATORS (TEMEL DEKORATÖRLER)
# ============================================================================

print("=" * 60)
print("BÖLÜM 1: BASIC DECORATORS (TEMEL DEKORATÖRLER)")
print("=" * 60)

"""
Dekoratör (Decorator) Nedir?
----------------------------
Dekoratör, bir fonksiyonu parametre olarak alıp, onun kodunu doğrudan
değiştirmeden davranışını genişleten/sücelten bir fonksiyondur.
Bunu bir hediye paketine benzetebilirsiniz: Hediye (orijinal fonksiyon) aynı kalır,
ancak etrafına ek özellikler veya ambalaj (ek davranışlar) eklersiniz.
"""


def my_decorator(func):
    """
    Bir fonksiyon çağrılmadan ÖNCE ve SONRA çalışan basit bir dekoratör.

    Args:
        func: Dekore edilecek (süslenecek) fonksiyon
        
    Returns:
        wrapper: Orijinal fonksiyonu sarıp (wrap edip) yeni davranış katan fonksiyon
    """
    def wrapper():
        print("🎁 Fonksiyon çağrılmadan ÖNCE bir şeyler yapılıyor.")
        func()
        print("🎁 Fonksiyon çağrıldıktan SONRA bir şeyler yapılıyor.")
    return wrapper


@my_decorator
def say_hello():
    """Dekore edilecek basit bir fonksiyon."""
    print("👋 Hello!")


# Dekoratör kullanımı
print("\nÖrnek 1: Basic Decorator (Basit Dekoratör)")
say_hello()


def repeat_three_times(func):
    """
    Bir fonksiyonun çağrısını 3 kez tekrarlayan dekoratör.

    Args:
        func: Tekrarlanacak fonksiyon
        
    Returns:
        wrapper: Orijinal fonksiyonu 3 kez çalıştıran kapsayıcı fonksiyon
    """
    def wrapper(*args, **kwargs):
        for i in range(3):
            print(f"  Çağrı #{i+1}:")
            func(*args, **kwargs)
    return wrapper


@repeat_three_times
def greet(name):
    """Birisini ismiyle selamlar."""
    print(f"  Hello, {name}!")


print("\nÖrnek 2: Decorator with Arguments (Parametre Alan Dekoratör)")
greet("Alice")


# ============================================================================
# BÖLÜM 2: PROPERTY DECORATORS (@property, @setter, @deleter)
# ============================================================================

print("\n" + "=" * 60)
print("BÖLÜM 2: PROPERTY DECORATORS (@property, @setter, @deleter)")
print("=" * 60)

"""
Property Dekoratörleri Nedir?
-----------------------------
Property dekoratörleri, bir sınıfın metotlarını birer öznitelik (attribute)
gibi erişilebilir kılmanızı sağlar (örneğin person.name() yerine person.name).

Kullanım Amaçları:
- Veri Doğrulama (Data Validation): Hatalı değer atamasını engelleme
- Hesaplanan Öznitelikler (Computed Attributes): Dinamik değer üretme
- Kapsülleme (Encapsulation): Gizli/özel (private) verilere güvenli erişim sağlama
"""


class Person:
    """
    Property dekoratörlerinin kullanımını gösteren bir sınıf.
    
    Property'ler sayesinde person.name = "John" gibi basit öznitelik atama 
    sentaksını kullanırken arka planda doğrulama ve mantık çalıştırabiliriz.
    """

    def __init__(self, name: str, age: int):
        """
        Person nesnesini başlatır.

        Args:
            name (str): Kişinin adı
            age (int): Kişinin yaşı
        """
        self.__name = name  # Private attribute (Python konvansiyonu: __ ile başlar)
        self.__age = age

    @property
    def name(self):
        """
        'name' property'si için Getter (Okuyucu) metodu.

        @property dekoratörü, person.__name değerine person.name() metot çağrısı
        yerine person.name şeklinde normal bir değişken gibi erişmemizi sağlar.

        Returns:
            str: Kişinin adı
        """
        print("  📖 Getter çağrıldı (İsim okunuyor)...")
        return self.__name

    @name.setter
    def name(self, value: str):
        """
        'name' property'si için Setter (Yazıcı/Atayıcı) metodu.

        Değer atamaya çalıştığınızda otomatik çağrılır: person.name = "John"
        Burada veri doğrulama (validation) mantığı ekleyebiliriz.

        Args:
            value (str): Atanmak istenen yeni isim

        Raises:
            ValueError: İsim metin değilse veya boşsa fırlatılır.
        """
        print(f"  ✏️  Setter çağrıldı (Yeni isim atanıyor): {value}")
        if not isinstance(value, str):
            raise ValueError("İsim bir metin (string) olmalıdır!")
        if len(value.strip()) == 0:
            raise ValueError("İsim alanı boş bırakılamaz!")
        self.__name = value

    @name.deleter
    def name(self):
        """
        'name' property'si için Deleter (Silici) metodu.

        'del person.name' komutu çalıştırıldığında tetiklenir.
        Temizlik veya sıfırlama işlemleri için kullanılır.
        """
        print("  🗑️  Deleter çağrıldı (İsim siliniyor/sıfırlanıyor)...")
        self.__name = None

    @property
    def age(self):
        """
        'age' property'si için Getter metodu.

        Returns:
            int: Kişinin yaşı
        """
        return self.__age

    @age.setter
    def age(self, value: int):
        """
        'age' property'si için Setter metodu (Doğrulama içerir).

        Args:
            value (int): Atanmak istenen yeni yaş

        Raises:
            ValueError: Yaş tamsayı değilse, negatifse veya mantıksızsa fırlatılır.
        """
        if not isinstance(value, int):
            raise ValueError("Yaş bir tamsayı (integer) olmalıdır!")
        if value < 0:
            raise ValueError("Yaş negatif bir değer olamaz!")
        if value > 150:
            raise ValueError("Yaş değeri gerçekçi değil (150'den büyük)!")
        self.__age = value

    @property
    def is_adult(self):
        """
        Hesaplanan (Computed) ve Sadece Okunabilir (Read-only) Property.

        Bu property'nin bir setter'ı yoktur, doğrudan 'age' değişkeninden hesaplanır.

        Returns:
            bool: Kişi 18 yaşında veya daha büyükse True döner.
        """
        return self.__age >= 18


# Property dekoratörlerinin kullanımı
print("\nÖrnek 3: @property Kullanımı (Getter)")
person = Person("Bob", 25)
print(f"Name (İsim): {person.name}")  # Getter çalışır
print(f"Age (Yaş): {person.age}")
print(f"Is adult? (Yetişkin mi?): {person.is_adult}")

print("\nÖrnek 4: @setter Kullanımı")
person.name = "Robert"  # Setter çalışır
person.age = 26

print("\nÖrnek 5: Property Veri Doğrulama (Validation)")
try:
    person.age = -5  # Hata fırlatacaktır
except ValueError as e:
    print(f"  ❌ Hata Yakalandı: {e}")

print("\nÖrnek 6: @deleter Kullanımı")
del person.name  # Deleter çalışır
print(f"Silindikten sonra isim: {person.name}")


# ============================================================================
# BÖLÜM 3: STATIC METHODS (@staticmethod)
# ============================================================================

print("\n" + "=" * 60)
print("BÖLÜM 3: STATIC METHODS (@staticmethod)")
print("=" * 60)

"""
@staticmethod Nedir?
--------------------
Statik metot, ait olduğu sınıfa bağlı olan ancak ne sınıfın kendisine (cls)
ne de sınıfın örneklerine (self) erişim sağlamayan bir metottur.
Normal bir fonksiyondur, ancak mantıksal olarak ilgili olduğu sınıfın 
içinde gruplanmıştır.

Ne Zaman Kullanılır?
- Metodun sınıf değişkenlerine (cls) veya örnek değişkenlerine (self) ihtiyacı yoksa
- Sınıfın amacıyla doğrudan bağlantılı bir yardımcı (utility/helper) fonksiyon ise
"""


class MathOperations:
    """Matematiksel yardımcı fonksiyonları barındıran bir sınıf."""

    @staticmethod
    def add(x, y):
        """
        İki sayıyı toplar.

        Bu bir statik metottur çünkü herhangi bir self veya cls değişkenine
        ihtiyaç duymaz - sadece verilen iki sayıyla hesaplama yapar.

        Args:
            x (float): Birinci sayı
            y (float): İkinci sayı

        Returns:
            float: x ve y'nin toplamı
        """
        return x + y

    @staticmethod
    def multiply(x, y):
        """
        İki sayıyı çarpar.

        Args:
            x (float): Birinci sayı
            y (float): İkinci sayı

        Returns:
            float: x ve y'nin çarpımı
        """
        return x * y

    @staticmethod
    def is_even(number):
        """
        Bir sayının çift olup olmadığını kontrol eder.

        Args:
            number (int): Kontrol edilecek sayı

        Returns:
            bool: Çift ise True, tek ise False
        """
        return number % 2 == 0


# Statik metotların kullanımı
print("\nÖrnek 7: Static Methods")
print(f"5 + 3 = {MathOperations.add(5, 3)}")
print(f"5 * 3 = {MathOperations.multiply(5, 3)}")
print(f"Is 4 even? (4 çift mi?): {MathOperations.is_even(4)}")
print(f"Is 7 even? (7 çift mi?): {MathOperations.is_even(7)}")

# Statik metotlar nesne üzerinden de çağrılabilir
math_ops = MathOperations()
print(f"Nesne üzerinden çağrı: 10 + 5 = {math_ops.add(10, 5)}")


# ============================================================================
# BÖLÜM 4: CLASS METHODS (@classmethod)
# ============================================================================

print("\n" + "=" * 60)
print("BÖLÜM 4: CLASS METHODS (@classmethod)")
print("=" * 60)

"""
@classmethod Nedir?
-------------------
Sınıf metodu, ilk parametre olarak bir nesne örneği (self) yerine 
sınıfın kendisini (cls) alan bir metottur. Sınıf düzeyindeki verilere
erişebilir ve bunları değiştirebilir.

Ne Zaman Kullanılır?
- Alternative Constructors (Alternatif Yapıcılar) / Factory Methods (Fabrika Metotları) için
- Sınıf değişkenlerine (Class Variables) erişmek veya onları güncellemek için
"""


class Pizza:
    """Alternatif yapıcılar için sınıf metotlarını gösteren bir sınıf."""

    # Class Variable (Tüm Pizza nesneleri tarafından ortak paylaşılır)
    total_pizzas_made = 0

    def __init__(self, ingredients: list):
        """
        Belirtilen malzemelerle bir Pizza nesnesi oluşturur.

        Args:
            ingredients (list): Malzeme metinlerinden oluşan liste
        """
        self.ingredients = ingredients
        Pizza.total_pizzas_made += 1

    def __repr__(self):
        """Pizzanın metinsel temsili."""
        return f"Pizza({', '.join(self.ingredients)})"

    @classmethod
    def margherita(cls):
        """
        Margherita pizza oluşturan Fabrika (Factory) Metodu.

        Bu bir sınıf metodudur ve alternatif bir yapıcı (constructor) işlevi görür.
        Pizza(['tomato sauce', 'mozzarella', 'basil']) yazmak yerine
        doğrudan Pizza.margherita() çağrılabilir.

        Returns:
            Pizza: Margherita pizza nesnesi
        """
        return cls(['tomato sauce', 'mozzarella', 'basil'])

    @classmethod
    def pepperoni(cls):
        """
        Pepperoni pizza oluşturan Fabrika (Factory) Metodu.

        Returns:
            Pizza: Pepperoni pizza nesnesi
        """
        return cls(['tomato sauce', 'mozzarella', 'pepperoni'])

    @classmethod
    def get_total_pizzas(cls):
        """
        Şimdiye kadar üretilen toplam pizza sayısını döner.

        Bu sınıf metodu, sınıf seviyesindeki total_pizzas_made değişkenine erişir.

        Returns:
            int: Toplam üretilen pizza sayısı
        """
        return cls.total_pizzas_made


# Sınıf metotlarının kullanımı
print("\nÖrnek 8: Class Methods (Factory Methods)")
pizza1 = Pizza.margherita()
pizza2 = Pizza.pepperoni()
pizza3 = Pizza(['BBQ sauce', 'chicken', 'onions'])

print(f"Pizza 1: {pizza1}")
print(f"Pizza 2: {pizza2}")
print(f"Pizza 3: {pizza3}")
print(f"Total pizzas made (Toplam üretilen pizza): {Pizza.get_total_pizzas()}")


# ============================================================================
# BÖLÜM 5: ABSTRACT METHODS (@abstractmethod)
# ============================================================================

print("\n" + "=" * 60)
print("BÖLÜM 5: ABSTRACT METHODS (@abstractmethod)")
print("=" * 60)

"""
@abstractmethod Nedir?
----------------------
Soyut (Abstract) metot, bir temel sınıfta (base class) tanımlanan ve 
tüm türetilmiş (subclass) sınıflar tarafından doldurulması (implement edilmesi)
ZORUNLU olan metottur. Bir nevi sözleşme (contract) işlevi görür.

Ne Zaman Kullanılır?
- Alt sınıfların uyması gereken bir arayüz (interface) tanımlamak istendiğinde
- Temel sınıfın doğrudan örneklenmesini (instantiation) engellemek istendiğinde
- Belirli metotların alt sınıflarda mutlaka yazıldığından emin olunmak istendiğinde
"""

from abc import ABC, abstractmethod


class Animal(ABC):
    """
    Hayvanlar için soyut temel sınıf (Abstract Base Class).

    Bu sınıftan doğrudan bir nesne üretilemez.
    Türetilen her alt sınıf, soyut metotları doldurmak zorundadır.
    """

    def __init__(self, name: str):
        """
        Bir Animal nesnesi başlatır.

        Args:
            name (str): Hayvanın adı
        """
        self.name = name

    @abstractmethod
    def make_sound(self):
        """
        Ses çıkarma için soyut metot.

        Her hayvan alt sınıfı bu metodu kendi mantığına göre doldurmalıdır.
        """
        pass

    @abstractmethod
    def move(self):
        """
        Hareket etme için soyut metot.

        Her hayvan alt sınıfı bu metodu doldurmalıdır.
        """
        pass

    def sleep(self):
        """
        Somut (Concrete) metot (soyut değil).

        Bu metodun bir gövdesi vardır ve alt sınıflar tarafından 
        ezilmesi (override edilmesi) zorunlu değildir.
        """
        print(f"  {self.name} is sleeping... 😴")


class Dog(Animal):
    """Animal sınıfından türetilen somut Dog sınıfı."""

    def make_sound(self):
        """Köpekler havlar."""
        print(f"  {self.name} says: Woof! Woof! 🐕")

    def move(self):
        """Köpekler koşar."""
        print(f"  {self.name} is running on four legs! 🏃")


class Bird(Animal):
    """Animal sınıfından türetilen somut Bird sınıfı."""

    def make_sound(self):
        """Kuşlar öter."""
        print(f"  {self.name} says: Tweet! Tweet! 🐦")

    def move(self):
        """Kuşlar uçar."""
        print(f"  {self.name} is flying in the sky! 🦅")


# Soyut metotların kullanımı
print("\nÖrnek 9: Abstract Methods")
dog = Dog("Buddy")
dog.make_sound()
dog.move()
dog.sleep()

print()
bird = Bird("Tweety")
bird.make_sound()
bird.move()
bird.sleep()

print("\nÖrnek 10: Soyut Sınıftan Doğrudan Nesne Üretilemez")
try:
    # Bu hata fırlatacaktır çünkü Animal soyut bir sınıftır
    animal = Animal("Generic")
except TypeError as e:
    print(f"  ❌ Hata Yakalandı: {e}")


# ============================================================================
# BÖLÜM 6: FUNCTION OVERLOADING (@overload)
# ============================================================================

print("\n" + "=" * 60)
print("BÖLÜM 6: FUNCTION OVERLOADING (@overload)")
print("=" * 60)

"""
@overload Nedir?
----------------
Python, C++ veya Java dillerindeki klasik fonksiyon aşırı yükleme (overloading) 
mekanizmasına çalışma zamanında (runtime) doğrudan sahip değildir.
@overload dekoratörü, statik tip denetleyicilerine (mypy, Pyright) ve IDE'lere
bir metodun farklı parametre tipleri ile çağrılabileceğini bildirmek için kullanılır.

Not: @overload yalnızca Tip İpuçları (Type Hints) sağlar. Gerçek fonksiyon 
gövdesini tek bir ana fonksiyon altında kendimiz yazmalıyız.
"""

from typing import overload, Union


class Calculator:
    """Tip ipuçları ile fonksiyon aşırı yüklemeyi gösteren sınıf."""

    @overload
    def add(self, a: int, b: int) -> int:
        ...

    @overload
    def add(self, a: int, b: int, c: int) -> int:
        ...

    def add(self, a: int, b: int, c: int | None = None) -> int:
        """Toplama işleminin gerçek uygulanışı."""
        if c is None:
            return a + b
        return a + b + c

    @overload
    def process(self, value: int) -> int:
        """Tamsayı parametre kabul eden imza."""
        ...

    @overload
    def process(self, value: str) -> str:
        """Metin parametre kabul eden imza."""
        ...

    def process(self, value: Union[int, str]) -> Union[int, str]:
        """
        Değeri işleyen gerçek metot uygulaması.

        Yukarıdaki @overload dekoratörleri yalnızca tip denetleyicileri içindir.
        Bu metot ise her iki durumu da ele alan asıl koddur.

        Args:
            value: int veya str tipinde bir değer

        Returns:
            int ise: değeri 2 ile çarpar
            str ise: metni büyük harflere dönüştürür
        """
        if isinstance(value, int):
            print(f"  Processing integer: {value}")
            return value * 2
        elif isinstance(value, str):
            print(f"  Processing string: {value}")
            return value.upper()
        else:
            raise TypeError("Value must be int or str")


# Aşırı yüklenmiş fonksiyonların kullanımı
print("\nÖrnek 11: Function Overloading (@overload)")
calc = Calculator()
result1 = calc.process(5)
print(f"  Result (Sonuç): {result1}")

result2 = calc.process("hello")
print(f"  Result (Sonuç): {result2}")


# ============================================================================
# BÖLÜM 7: FINAL DECORATOR (@final)
# ============================================================================

print("\n" + "=" * 60)
print("BÖLÜM 7: FINAL DECORATOR (@final)")
print("=" * 60)

"""
@final Nedir?
-------------
@final dekoratörü, bir sınıfın türetilemeyeceğini (subclass yapılamayacağını) 
veya bir metodun alt sınıflarda ezilemeyeceğini (override edilemeyeceğini) belirtir.
Bu özellik statik tip denetleyicilerine (mypy gibi) yönelik bir ipucudur.

Not: Python çalışma zamanında (runtime) miras almayı tamamen engellemez,
ancak tip denetleyicileri ve IDE'ler sizi uyarır.
"""

from typing import final


class BaseGame:
    """Final ve final olmayan metotlara sahip temel oyun sınıfı."""

    def start(self):
        """Oyunu başlatır - Alt sınıflar tarafından ezilebilir."""
        print("  🎮 Game starting...")

    @final
    def calculate_score(self, points: int) -> int:
        """
        Skoru hesaplar - Final olarak işaretlenmiştir.

        Bu metot alt sınıflar tarafından EZİLMEMELİDİR.
        Çünkü skorlama mantığının her yerde tutarlı kalması gerekir.

        Args:
            points (int): Kazanılan temel puan

        Returns:
            int: Bonus eklenmiş nihai skor
        """
        bonus = 100
        return points + bonus

    def end(self):
        """Oyunu bitirir - Alt sınıflar tarafından ezilebilir."""
        print("  🏁 Game over!")


class MyGame(BaseGame):
    """Özel bir oyun uygulaması."""

    def start(self):
        """'start' metodunu eziyoruz (Buna izin verilir)."""
        print("  🎮 MyGame starting with custom intro!")

    # Eğer aşağıdaki kodu açarsanız, tip denetleyici uyarısı verecektir:
    # def calculate_score(self, points: int) -> int:
    #     # ❌ Type checker warning: Cannot override final method
    #     return points * 2


@final
class SecretAlgorithm:
    """
    Final olarak işaretlenmiş sınıf - Alt sınıfı oluşturulmamalıdır.

    Güvenlik veya tutarlılık nedenleriyle bir sınıfın genişletilmesini 
    istemediğinizde @final kullanabilirsiniz.
    """

    def process(self):
        """Gizli algoritma ile veriyi işler."""
        print("  🔒 Processing with secret algorithm...")


# Final dekoratörünün kullanımı
print("\nÖrnek 12: Final Methods")
game = MyGame()
game.start()
score = game.calculate_score(50)
print(f"  Final score (Skor): {score}")
game.end()

print("\nÖrnek 13: Final Class")
secret = SecretAlgorithm()
secret.process()

# Eğer alt sınıf oluşturmaya çalışırsanız tip denetleyici uyarır:
# class MySecretAlgorithm(SecretAlgorithm):  # ❌ Type checker warning
#     pass


# ============================================================================
# BÖLÜM 8: OVERRIDE DECORATOR (@override)
# ============================================================================

print("\n" + "=" * 60)
print("BÖLÜM 8: OVERRIDE DECORATOR (@override)")
print("=" * 60)

"""
@override Nedir?
----------------
@override dekoratörü (Python 3.12+ ile gelmiştir), bir metodun üst sınıftaki
bir metodu ezmek (override etmek) amacıyla yazıldığını açıkça belirtir.
Yazım hataları (typo) veya isim uyumsuzlukları yüzünden aslında ezmediğiniz
hata durumlarını yakalamanıza yardımcı olur.

Not: Python sürümünüz < 3.12 ise 'typing_extensions' kütüphanesinden içe aktarabilirsiniz.
"""

try:
    from typing import override
except ImportError:
    # Python < 3.12 sürümleri için yedek içe aktarma
    from typing_extensions import override


class Shape:
    """Şekiller için temel sınıf."""

    def area(self) -> float:
        """
        Şeklin alanını hesaplar.

        Returns:
            float: Alan değeri
        """
        return 0.0

    def perimeter(self) -> float:
        """
        Şeklin çevresini hesaplar.

        Returns:
            float: Çevre değeri
        """
        return 0.0


class Rectangle(Shape):
    """Dikdörtgen şekli uygulaması."""

    def __init__(self, width: float, height: float):
        """
        Rectangle nesnesini başlatır.

        Args:
            width (float): Genişlik
            height (float): Yükseklik
        """
        self.width = width
        self.height = height

    @override
    def area(self) -> float:
        """
        Dikdörtgen alanını hesaplar.

        @override dekoratörü tip denetleyicilere şunu söyler:
        "Ben üst sınıftaki 'area' metodunu bilerek eziyorum."
        Eğer üst sınıfta 'area' adında bir metot olmasaydı tip denetleyici sizi uyarırırdı.
        """
        return self.width * self.height

    @override
    def perimeter(self) -> float:
        """Dikdörtgen çevresini hesaplar."""
        return 2 * (self.width + self.height)


class Circle(Shape):
    """Daire şekli uygulaması."""

    def __init__(self, radius: float):
        """
        Circle nesnesini başlatır.

        Args:
            radius (float): Dairenin yarıçapı
        """
        self.radius = radius

    @override
    def area(self) -> float:
        """Daire alanını hesaplar: π * r²"""
        import math
        return math.pi * self.radius ** 2

    @override
    def perimeter(self) -> float:
        """Daire çevresini hesaplar: 2 * π * r"""
        import math
        return 2 * math.pi * self.radius


# Override dekoratörünün kullanımı
print("\nÖrnek 14: Override Decorator")
rect = Rectangle(5, 3)
print("Rectangle (5x3):")
print(f"  Area (Alan): {rect.area():.2f}")
print(f"  Perimeter (Çevre): {rect.perimeter():.2f}")

print()
circle = Circle(4)
print("Circle (radius=4):")
print(f"  Area (Alan): {circle.area():.2f}")
print(f"  Perimeter (Çevre): {circle.perimeter():.2f}")


# ============================================================================
# BONUS BÖLÜMÜ: COMBINING MULTIPLE DECORATORS
# ============================================================================

print("\n" + "=" * 60)
print("BONUS: COMBINING MULTIPLE DECORATORS")
print("=" * 60)

"""
Aynı fonksiyon veya metot üzerine birden fazla dekoratör ekleyebilirsiniz (stacking).
Dekoratörler aşağıdan yukarıya doğru (fonksiyona en yakın olandan başlayarak) uygulanır.
"""


def multiply_decorator(func):
    def wrapper(x: int):
        return func(x) * 2
    return wrapper


def other_decorator(func):
    def wrapper(x: int):
        return func(x) * 4
    return wrapper


# İşlem sırası: Önce other_decorator, sonra multiply_decorator uygulanır.
@multiply_decorator
@other_decorator
def calculate(x: int):
    return x * 2


print(f"calculate(10) result: {calculate(10)}")
# Hesaplama Adımları:
# 1. calculate(10) -> 10 * 2 = 20
# 2. other_decorator -> 20 * 4 = 80
# 3. multiply_decorator -> 80 * 2 = 160


# ============================================================================
# ÖZET VE EN İYİ PRATİKLER (SUMMARY AND BEST PRACTICES)
# ============================================================================

print("\n" + "=" * 60)
print("SUMMARY AND BEST PRACTICES")
print("=" * 60)

print("""
📚 Neler Öğrendik?

1. BASIC DECORATORS
   - Fonksiyonları değiştirmeden genişleten yapılar.
   - Kullanım: Kod tekrarını önlemek, loglama, yetkilendirme vb.

2. @property, @setter, @deleter
   - Metotlara öznitelik gibi erişilmesini sağlar.
   - Kullanım: Veri doğrulama (validation) ve dinamik hesaplanan değerler.

3. @staticmethod
   - Sınıfa veya örneğe (self/cls) erişmeyen fonksiyonlar.
   - Kullanım: Sınıfla ilişkili yardımcı (utility/helper) fonksiyonlar.

4. @classmethod
   - İlk parametre olarak sınıfın kendisini (cls) alan metotlar.
   - Kullanım: Alternatif yapıcılar (factory methods), sınıf değişkenlerine erişim.

5. @abstractmethod
   - Alt sınıflar tarafından uygulanması zorunlu kılınan metotlar.
   - Kullanım: Arayüz (interface) ve standart mimari oluşturma.

6. @overload
   - Farklı parametre tipleri için tip ipucu sağlama.
   - Kullanım: Gelişmiş IDE ve tip denetleyici (mypy) desteği.

7. @final
   - Metot ezilmesini veya sınıf türetilmesini engelleme ipucu.
   - Kullanım: Kritik mantıkların korunması ve güvenlik.

8. @override
   - Üst sınıftaki bir metodun bilerek ezildiğini belirtme.
   - Kullanım: Yazım hatalarının önüne geçme, kod okunabilirliğini artırma.

💡 En İyi Pratikler (Best Practices):
- Veri doğrulama ve hesaplanan öznitelikler için @property + @setter tercih edin.
- Yardımcı bağımsız fonksiyonlar için @staticmethod kullanın.
- Nesne oluşturma alternatifleri (Fabrika metotları) için @classmethod kullanın.
- Zorunlu mimari kurallar için @abstractmethod ile soyut sınıflar tasarlayın.
- Üst sınıf metotlarını ezerken hatayı önlemek için @override ekleyin.
- Dekoratörleri aşırı kullanmayın; kodun okunabilir kalmasına özen gösterin.

🎯 Ne Zaman Hangisi Kullanılmalı?
- Doğrulama gerekiyor mu? → @property + @setter
- Bağımsız yardımcı fonksiyon mu? → @staticmethod
- Fabrika metodu mu lazım? → @classmethod
- Standart bir arayüz/sözleşme mi gerekiyor? → @abstractmethod
- Esnek tip ipuçları mı lazım? → @overload
- Ezilmesi istenmeyen metot mu var? → @final
- Üst metot eziliyor mu? → @override

Happy Coding! 🐍✨
""")

print("\n" + "=" * 60)
print("END OF TUTORIAL")
print("=" * 60)
