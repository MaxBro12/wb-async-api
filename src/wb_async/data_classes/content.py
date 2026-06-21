from typing import Tuple
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BaseObjects:
    error: bool = False
    errorText: str = ""
    additionalErrors: str | None = None


@dataclass(frozen=True, slots=True)
class ParentProductCategory:
    name: str
    id: int
    is_visible: bool = False


@dataclass(frozen=True, slots=True)
class ParentProductCategories(BaseObjects):
    data: Tuple[ParentProductCategory, ...] = tuple()


@dataclass(frozen=True, slots=True)
class Product:
    subjectID: int # ID предмета
    parentID: int # ID родительской категории
    subjectName: str # Название предмета
    parentName: str # Название родительской категории


@dataclass(frozen=True, slots=True)
class ProductsList(BaseObjects):
    data: Tuple[Product, ...] = tuple()


@dataclass(frozen=True, slots=True)
class Characteristic:
    charcID: int # id характеристики
    subjectName: str # название характеристики
    subjectID: int # id продукта
    name: str # название характеристики
    required: bool # обязательность характеристики
    unitName: str # единица измерения
    maxCount: int # Максимальное количество значений, которое можно присвоить характеристике при создании или редактировании карточек товаров.
    popular: bool # Характеристика популярна у пользователей (true - да, false - нет)
    charcType: int # Тип данных характеристики, который необходимо использовать при создании или редактировании карточек товаров:
                   # 1 — массив строк
                   # 4 — число (целое либо с десятичной дробью)
                   # 0 — характеристика не используется


@dataclass(frozen=True, slots=True)
class CharacteristicsList(BaseObjects):
    data: Tuple[Characteristic, ...] = tuple()
