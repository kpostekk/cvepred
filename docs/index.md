*[Dokumentacja w formie PDF](pdf/document.pdf)*

# Predykcja Udarów Mózgu

Celem tego projektu jest opracowanie modelu predykcyjnego, który na podstawie danych medycznych i demograficznych będzie w stanie oszacować prawdopodobieństwo wystąpienia udaru u pacjenta.

Udar mózgu to nagłe zaburzenie krążenia krwi w mózgu, które prowadzi do uszkodzenia tkanki mózgowej. Może wystąpić w wyniku zatkania naczynia krwionośnego (udar niedokrwienny) lub pęknięcia naczynia i wylewu krwi do mózgu (udar krwotoczny). Udar prowadzi do niedotlenienia obszarów mózgu, co powoduje śmierć komórek nerwowych i może skutkować trwałymi uszkodzeniami neurologicznymi. Objawy udaru często pojawiają się nagle i obejmują m.in. osłabienie lub paraliż jednej strony ciała, zaburzenia mowy, problemy z widzeniem, zawroty głowy oraz silny ból głowy. Udar jest stanem zagrażającym życiu i wymaga natychmiastowej pomocy medycznej, ponieważ szybkie leczenie zwiększa szanse na ograniczenie skutków uszkodzenia mózgu.

Wykorzystując techniki uczenia maszynowego, dążymy do stworzenia narzędzia wspierającego personel medyczny w identyfikacji pacjentów wysokiego ryzyka i podejmowaniu decyzji klinicznych.

Udar mózgu jest jedną z głównych przyczyn niepełnosprawności i zgonów na świecie. Występuje nagle i może prowadzić do poważnych konsekwencji zdrowotnych, wpływając na jakość życia pacjentów oraz ich rodzin. Wczesne wykrycie osób narażonych na wysokie ryzyko udaru jest kluczowe dla podjęcia odpowiednich działań profilaktycznych i terapeutycznych.

**Źródło danych:** [Stroke Prediction Dataset](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset/code?datasetId=1120859&sortBy=voteCount) dostępny na platformie Kaggle.

**Licencja**: Data files © Original Authors

**Autor zbioru:** https://www.kaggle.com/fedesoriano

## Uzasadnienie wyboru zbioru danych

Zbiór danych zawiera kluczowe informacje niezbędne do przeprowadzenia analizy ryzyka wystąpienia udaru, łącząc dane medyczne z danymi demograficznymi.

Jest on publicznie dostępny i może być wykorzystywany zarówno do celów edukacyjnych, jak i badawczych. Zawarte atrybuty pozwalają na analizę oraz modelowanie różnych czynników wpływających na ryzyko udaru, takich jak wiek, płeć, historia chorób przewlekłych, czy styl życia.

Dane odzwierciedlają aktualne trendy i problemy zdrowotne związane z udarami mózgu.

## Charakterystyka zbioru danych

Zbiór danych zawiera 5110 rekordów, z których każdy reprezentuje indywidualnego pacjenta wraz z następującymi atrybutami:

| Nazwa atrybutu    | Opis                                                                                          |
| ----------------- | --------------------------------------------------------------------------------------------- |
| id                | Unikalny identyfikator pacjenta                                                               |
| gender            | Płeć pacjenta ("Male", "Female", "Other")                                                     |
| age               | Wiek pacjenta                                                                                 |
| hypertension      | Informacja o nadciśnieniu (0 - brak, 1 - występuje)                                           |
| heart_disease     | Informacja o chorobach serca (0 - brak, 1 - występuje)                                        |
| ever_married      | Stan cywilny pacjenta ("No", "Yes")                                                           |
| work_type         | Rodzaj wykonywanej pracy ("children", "Govt_job", "Never_worked", "Private", "Self-employed") |
| Residence_type    | Miejsce zamieszkania pacjenta ("Rural", "Urban")                                              |
| avg_glucose_level | Średni poziom glukozy we krwi                                                                 |
| bmi               | Wskaźnik masy ciała pacjenta                                                                  |
| smoking_status    | Status palenia ("formerly smoked", "never smoked", "smokes", "Unknown")                       |
| stroke            | Informacja o wystąpieniu udaru (0 - nie wystąpił, 1 - wystąpił)                               |

## Cele projektu

W projekcie dążyć będę do spełnienia dwóch następujących celów:

- Identyfikacja kluczowych czynników ryzyka - analiza i określenie najważniejszych zmiennych wpływających na zwiększone ryzyko udaru.
- Stworzenie skutecznego modelu predykcyjnego ryzyka udaru mózgu - opracowanie modelu uczenia maszynowego, który na podstawie danych medycznych i demograficznych przewiduje wystąpienie udaru mózgu.
