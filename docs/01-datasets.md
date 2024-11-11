---
title: Zbiór danych
---

# Zbiór danych

!!! note

    Na podstawie `strokepred/dataset.py` oraz `eda.ipynb`

## Ogólny opis zbioru

Na podstawie przedstawionych statystyk można opisać następujące cechy zbioru danych:

### Struktura danych:

- Zawiera 12 zmiennych (kolumn)
- Składa się z 5110 obserwacji (wierszy)
- Typy zmiennych:
  - 4 zmienne numeryczne
  - 7 zmiennych kategorycznych
  - 1 zmienna logiczna (boolean)

Zbiór danych wydaje się być relatywnie czysty (mało brakujących wartości, brak duplikatów) i dobrze zorganizowany. Dominują w nim zmienne kategoryczne, co może sugerować, że dane dotyczą klasyfikacji lub analizy cech jakościowych.

## Inżynieria cech

### Braki danych/nadwyżki danych

- 201 rekordów nie posiada wartości bmi, można je uzupełnić medianą lub średnią.
- kolumna `id` może zostać pominięta

### Odstające wartości

- Istnieje 1 rekord z `gender = Other`, który można usunąć.
- Wartości `bmi` powyżej 65 można uznać za odstające.

### Normalizacja danych

- Kolumny `ever_married`, `hyperthension`, `heart_disease`, `stroke` można zakodować jako wartości binarne (`bool`).

### Kodowanie

Cały dataset został zakodowany przy pomocy `pd.get_dummies`. Wywołanie tej funkcji spowodowało wykorzystanie kodowania typu _one-hot_.

## Balansowanie zbioru treningowego

Wstępna analiza wykazała, że 70% rekordów dotyczy osób, które nie doświadczyły udaru. W celu zbalansowania zbioru treningowego można zastosować techniki oversamplingu smote.

### Implementacja SMOTE

SMOTE zostało zaimplementowane przy pomocy biblioteki `imbalanced-learn`.

!!! example "Implementacja"

    ```python title="dataset.py"
    --8<-- "strokepred/dataset.py:docs_balanced_dataset"
    ```

## Pozostałe wnioski

### Konfiguracja Pycaret

Po wykonaniu ręcznej inżynierii cech trzeba wyłączyć preprocesing w Pycaret.

```python
from pycaret.classification import setup

setup(..., preprocess=False)
```

> **preprocess: bool, default = True**

> When set to False, no transformations are applied except for train_test_split and custom transformations passed in custom_pipeline param. Data must be ready for modeling (no missing values, no dates, categorical data encoding), when preprocess is set to False.
