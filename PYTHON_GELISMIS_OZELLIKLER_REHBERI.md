# 📚 PYTHON İLERİ DÜZEY ÖZELLİKLER EĞİTİM VE REFERANS REHBERİ

> **Not:** Bu rehber, Python'daki ileri düzey nesne yönelimli programlama (OOP), dekoratörler, tip ipuçları (type hints) ve yazılım tasarım kalıplarını gelecekte dönüp hatırlamanız için detaylı açıklamalar ve kod örnekleriyle hazırlanmıştır.

---

## 📌 İÇİNDEKİLER
1. [Temel Dekoratörler (Basic Decorators)](#1-temel-dekoratörler-basic-decorators)
2. [Property Dekoratörleri (@property, @setter, @deleter)](#2-property-dekoratörleri-property-setter-deleter)
3. [Statik Metotlar (@staticmethod)](#3-statik-metotlar-staticmethod)
4. [Sınıf Metotları (@classmethod)](#4-sınıf-metotları-classmethod)
5. [Soyut Metotlar (@abstractmethod & ABC)](#5-soyut-metotlar-abstractmethod--abc)
6. [Fonksiyon Aşırı Yükleme (@overload)](#6-fonksiyon-aşırı-yükleme-overload)
7. [Final Dekoratörü (@final)](#7-final-dekoratörü-final)
8. [Override Dekoratörü (@override)](#8-override-dekoratörü-override)
9. [Bonus: Çoklu Dekoratör Kullanımı (Combining Decorators)](#9-bonus-çoklu-dekoratör-kullanımı-combining-decorators)
10. [Özet Karşılaştırma Tablosu & En İyi Pratikler](#10-özet-karşılaştırma-tablosu--en-iyi-pratikler)

---

## 1. TEMEL DEKORATÖRLER (BASIC DECORATORS)

### 💡 Mantığı ve Amacı
Dekoratör, bir fonksiyonu parametre olarak alıp, onun mevcut kodunu değiştirmeden davranışını genişleten bir fonksiyondur.

- **🎁 Benzetme:** Bir hediyeyi ambalaj kağıdı ile kaplamak gibidir. Hediye (orijinal fonksiyon) içerde aynı kalır, ancak etrafına dış ambalaj (ek davranış) sararsınız.
- **🛠 Gerçek Dünya Kullanımı:** 
  - Loglama (Fonksiyon ne zaman ve hangi parametrelerle çağrıldı?)
  - Yetkilendirme (Kullanıcı bu fonksiyonu çalıştırmak için yetkili mi?)
  - Performans Ölçümü (Fonksiyon kaç milisaniyede tamamlandı?)

### 🔍 Kod Örneği ve Çalışma Mantığı
```python
def my_decorator(func):
    """
    Parametre olarak aldığı 'func' fonksiyonunu sarar (wrap eder).
    """
    def wrapper(*args, **kwargs):
        print("🎁 [ÖNCE] Fonksiyon çağrılmadan önce yapılacak işlemler...")
        result = func(*args, **kwargs)  # Orijinal fonksiyon çalıştırılır
        print("🎁 [SONRA] Fonksiyon tamamlandıktan sonra yapılacak işlemler...")
        return result
    return wrapper

@my_decorator  # say_hello = my_decorator(say_hello) ile eşdeğerdir!
def say_hello(name):
    print(f"👋 Hello, {name}!")

# Kullanımı:
say_hello("Alice")
```

---

## 2. PROPERTY DECORATORS (`@property`, `@setter`, `@deleter`)

### 💡 Mantığı ve Amacı
Python'da kapsülleme (Encapsulation) sağlamak için nesne özniteliklerini gizli (`__private`) yaparız. Ancak dışarıdan bu özniteliklere erişirken `person.get_name()` veya `person.set_name("Tuna")` gibi karmaşık metot çağrıları yapmak yerine, **sanki normal bir değişkene erişiyormuş gibi** (`person.name = "Tuna"`) yazabilmemizi sağlar.

- **`@property` (Getter):** Gizli değişkene `person.name` şeklinde parantez kullanmadan erişmeyi sağlar.
- **`@name.setter` (Setter):** `person.name = "Yeni İsim"` ataması yapıldığında otomatik çalışır. Veri doğrulaması (Validation) için kullanılır.
- **`@name.deleter` (Deleter):** `del person.name` silme komutu çalıştırıldığında tetiklenir.

### 🔍 Kod Örneği ve Çalışma Mantığı
```python
class Person:
    def __init__(self, name: str, age: int):
        self.__name = name  # Private (Gizli) değişken
        self.__age = age

    @property  # GETTER: person.name şeklinde okumayı sağlar
    def name(self):
        print("📖 Getter: İsim okunuyor...")
        return self.__name

    @name.setter  # SETTER: person.name = "John" dendiğinde veri doğrular
    def name(self, value: str):
        print(f"✏️ Setter: İsim atanıyor -> {value}")
        if not isinstance(value, str):
            raise TypeError("İsim bir metin (string) olmalıdır!")
        if len(value.strip()) == 0:
            raise ValueError("İsim boş bırakılamaz!")
        self.__name = value

    @name.deleter  # DELETER: del person.name dendiğinde çalışır
    def name(self):
        print("🗑️ Deleter: İsim siliniyor/sıfırlanıyor...")
        self.__name = None

    @property  # Computed (Hesaplanan) ve Sadece Okunabilir (Read-only) Property
    def is_adult(self):
        return self.__age >= 18

# Kullanımı:
person = Person("Bob", 25)
print(person.name)        # Getter çalışır
person.name = "Robert"    # Setter çalışır ve doğrulama yapar
print(person.is_adult)    # Calculated property -> True
del person.name           # Deleter çalışır
```

---

## 3. STATİK METOTLAR (`@staticmethod`)

### 💡 Mantığı me Amacı
Sınıfın içine yazılan ancak ne nesnenin kendisine (`self`) ne de sınıfın kendisine (`cls`) ihtiyaç duyan bağımsız fonksiyonlardır.
- **🛠 Gerçek Dünya Kullanımı:** Sınıfla mantıksal bağı olan matematiksel veya yardımcı (utility/helper) fonksiyonları gruplamak için kullanılır.
- **Çağrı Biçimi:** Nesne türetmeden doğrudan `MathOperations.add(5, 3)` şeklinde çağrılır.

### 🔍 Kod Örneği ve Çalışma Mantığı
```python
class MathOperations:
    @staticmethod
    def add(x: float, y: float) -> float:
        # self veya cls almaz! Sadece aldığı x ve y ile işlem yapar.
        return x + y

    @staticmethod
    def is_even(number: int) -> bool:
        return number % 2 == 0

# Kullanımı:
print(MathOperations.add(10, 20))    # Output: 30
print(MathOperations.is_even(4))     # Output: True
```

---

## 4. SINIF METOTLARI (`@classmethod`)

### 💡 Mantığı ve Amacı
Sınıf metotları, ilk parametre olarak nesne örneği (`self`) yerine **sınıfın kendisini (`cls`)** alır. Sınıf seviyesindeki verilere erişebilir ve değiştirebilir.

- **🛠 Kullanım Alanları:**
  1. **Alternatif Yapıcılar (Alternative Constructors / Factory Methods):** `__init__` dışında farklı formatlarda nesne üretmek.
  2. **Sınıf Seviyesi Durumlar (Class State):** Üretilen toplam nesne sayısını takip etmek.

### 🔍 Kod Örneği ve Çalışma Mantığı
```python
class Pizza:
    total_pizzas_made = 0  # Sınıf değişkeni

    def __init__(self, ingredients: list):
        self.ingredients = ingredients
        Pizza.total_pizzas_made += 1

    @classmethod  # Fabrika Metodu (Factory Method)
    def margherita(cls):
        # cls(...) yazmak Pizza(...) yazmakla birebir aynıdır.
        return cls(["tomato sauce", "mozzarella", "basil"])

    @classmethod  # Fabrika Metodu (Factory Method)
    def pepperoni(cls):
        return cls(["tomato sauce", "mozzarella", "pepperoni"])

    @classmethod
    def get_total_pizzas(cls):
        return cls.total_pizzas_made

# Kullanımı:
pizza1 = Pizza.margherita()  # Hazır malzeme listesiyle pizza üretir
pizza2 = Pizza.pepperoni()
print(Pizza.get_total_pizzas())  # Output: 2
```

---

## 5. SOYUT METOTLAR (`@abstractmethod` & ABC)

### 💡 Mantığı ve Amacı
Soyut sınıflar mimari bir **Sözleşme (Contract / Interface)** gibidir.
- "Bu sınıftan türeyen her alt sınıf, soyut olarak işaretlenen metotları **doldurmak (implement etmek) zorundadır**!"
- `abc` modülündeki `ABC` sınıfından türetilir.
- Soyut bir sınıftan doğrudan nesne üretilemez (`animal = Animal()` hata verir).

### 🔍 Kod Örneği ve Çalışma Mantığı
```python
from abc import ABC, abstractmethod

class Animal(ABC):  # Soyut Temel Sınıf
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def make_sound(self):
        """Her alt sınıf bu metodu yazmak ZORUNDADIR."""
        pass

    @abstractmethod
    def move(self):
        """Her alt sınıf bu metodu yazmak ZORUNDADIR."""
        pass

class Dog(Animal):
    def make_sound(self):
        print(f"{self.name} diyor ki: Woof! Woof! 🐕")

    def move(self):
        print(f"{self.name} koşuyor! 🏃")

# Kullanımı:
dog = Dog("Buddy")
dog.make_sound()
# animal = Animal("Generic")  # ❌ TypeError hatası verir!
```

---

## 6. FONKSİYON AŞIRI YÜKLEME (`@overload`)

### 💡 Mantığı ve Amacı
Python çalışma zamanında (runtime) aynı isimde birden fazla fonksiyon tanımlanmasına izin vermez. `@overload` dekoratörü, statik tip denetleyicilerine (mypy, Pyright) ve IDE'lere bir fonksiyonun **farklı parametre tipleriyle çağrılabileceğini bildirmek** için kullanılır.

- **Önemli:** `@overload` yalnızca tip ipucu verir. Asıl mantık en alttaki tek bir fonksiyon gövdesinde yazılır.

### 🔍 Kod Örneği ve Çalışma Mantığı
```python
from typing import overload, Union

class Calculator:
    @overload
    def process(self, value: int) -> int: ...  # Tip denetleyici için 1. İmza

    @overload
    def process(self, value: str) -> str: ...  # Tip denetleyici için 2. İmza

    def process(self, value: Union[int, str]) -> Union[int, str]:
        # GERÇEK ÇALIŞAN KOD (Runtime)
        if isinstance(value, int):
            return value * 2
        elif isinstance(value, str):
            return value.upper()
        else:
            raise TypeError("Value must be int or str")

# Kullanımı:
calc = Calculator()
print(calc.process(5))        # Output: 10
print(calc.process("hello"))  # Output: "HELLO"
```

---

## 7. FİNAL DEKORATÖRÜ (`@final`)

### 💡 Mantığı ve Amacı
Bir metodun alt sınıflarda ezilmesini (override edilmesini) veya bir sınıfın alt sınıflarının oluşturulmasını (inheritance/subclassing) engellemek için kullanılır.
- **Metot Üzerinde `@final`:** Metodun kritik olduğunu ve değiştirilemeyeceğini söyler.
- **Sınıf Üzerinde `@final`:** Sınıfın kilitli olduğunu ve miras alınamayacağını söyler.

### 🔍 Kod Örneği ve Çalışma Mantığı
```python
from typing import final

class BaseGame:
    @final
    def calculate_score(self, points: int) -> int:
        # Bu skor hesaplama algoritması alt sınıflar tarafından DEĞİŞTİRİLEMEZ!
        return points + 100

class MyGame(BaseGame):
    # def calculate_score(self, points): -> ❌ Tip denetleyici uyarısı verir!
    pass

@final
class SecretAlgorithm:  # Bu sınıftan türetme yapılamaz!
    def process(self):
        print("🔒 Secret algorithm executing...")
```

---

## 8. OVERRIDE DEKORATÖRÜ (`@override`)

### 💡 Mantığı ve Amacı
Python 3.12+ ile eklenen `@override`, bir metodun üst sınıftaki bir metodu ezmek amacıyla yazıldığını açıkça belirtir.
- **Neden Kullanılır?** Yazım hatalarından (typo) doğan hataları engeller. Eğer üst sınıfta ezmeye çalıştığınız isimde bir metot yoksa tip denetleyici sizi hemen uyarır.

### 🔍 Kod Örneği ve Çalışma Mantığı
```python
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

    @override  # Tip denetleyiciye: "Ben üst sınıftaki area() metodunu eziyorum" der.
    def area(self) -> float:
        return self.width * self.height
```

---

## 9. BONUS: ÇOKLU DEKORATÖR KULLANIMI (COMBINING DECORATORS)

### 💡 Mantığı ve Amacı
Bir fonksiyon üzerine birden fazla dekoratör üst üste eklenebilir (stacking).
- **⚠️ KRİTİK KURAL:** Dekoratörler **AŞAĞIDAN YUKARIYA** (fonksiyona en yakın olandan en dıştakine doğru) sırayla uygulanır.

### 🔍 Kod Örneği ve Çalışma Mantığı
```python
def multiply_decorator(func):
    def wrapper(x: int):
        return func(x) * 2
    return wrapper

def other_decorator(func):
    def wrapper(x: int):
        return func(x) * 4
    return wrapper

@multiply_decorator  # 2. Adım: Çıkan sonucu 2 ile çarpar (80 * 2 = 160)
@other_decorator     # 1. Adım: Önce bu çalışır, sonucu 4 ile çarpar (20 * 4 = 80)
def calculate(x: int):
    return x * 2     # Orijinal İşlem: 10 * 2 = 20

print(calculate(10)) # Çıktı: 160
```

---

## 10. ÖZET KARŞILAŞTIRMA TABLOSU & EN İYİ PRATİKLER

| Dekoratör / Kavram | İlk Parametre | Eriştiği Seviye | Temel Kullanım Senaryosu |
| :--- | :--- | :--- | :--- |
| **`@property`** | `self` | Nesne Örnek Seviyesi | Veri doğrulama, gizli değişken okuma/yazma |
| **`@staticmethod`** | *Yok* | Bağımsız Fonksiyon | Sınıfla ilişkili matematiksel/yardımcı metotlar |
| **`@classmethod`** | `cls` | Sınıf Seviyesi | Alternatif nesne yapıcılar (Factory methods) |
| **`@abstractmethod`** | `self` | Alt Sınıf Zorunluluğu | Mimari arayüz ve sözleşme (Interface) tanımı |
| **`@overload`** | `self` | Tip İpucu (Type Hint) | IDE desteği ve çoklu imza tanımları |
| **`@final`** | `self` / *Sınıf* | Kilitli Mantık | Ezilmeyi veya miras alınmayı engelleme |
| **`@override`** | `self` | Alt Sınıf İmzası | Üst sınıf metotlarını güvenli ezme (Typo önleme) |
| **Çoklu Dekoratör** | - | Aşağıdan Yukarıya | Loglama, yetkilendirme, önbellekleme birleştirme |

### 💡 Ne Zaman Hangisini Seçmeliyim?
1. **Nesneye ait verileri doğrulayıp kontrol etmek istiyorsam?** $\rightarrow$ `@property` ve `@setter`
2. **`self` veya `cls` ihtiyacım yoksa, sadece yardımcı bir fonksiyon yazıyorsam?** $\rightarrow$ `@staticmethod`
3. **Farklı parametrelerle nesne oluşturan bir fabrika yazıyorsam?** $\rightarrow$ `@classmethod`
4. **Tüm alt sınıflarda bulunması şart olan metotlar tanımlıyorsam?** $\rightarrow$ `@abstractmethod`
5. **Fonksiyonumun farklı tipler alıp farklı tipler döndürdüğünü bildirmek istiyorsam?** $\rightarrow$ `@overload`
6. **Kritik bir algoritmanın ezilmesini önlemek istiyorsam?** $\rightarrow$ `@final`
7. **Üst sınıftaki metotları ezerken hata yapmaktan kaçınmak istiyorsam?** $\rightarrow$ `@override`

---
*Keyifli Kodlamalar! 🐍✨*
