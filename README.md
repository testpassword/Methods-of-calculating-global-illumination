> В лабораторных 2-4 `.ray` файлы присутствуют только для минимального значения лучей в качестве примера, ибо это тяжёлые файлы (для 10млн лучей, к примеру, весит 1.5ГБ), которые нет смысла тянуть в репозиторий. Их можно создать заново, выполнив скрипты для соответствующих лаб.

# Лабораторная №1: Расчет глобального освещения на примере фотометрического шара #

***Исходные данные:***

Радиус фотометрического шара, коэффициент диффузного отражения внутренней поверхности шара, световой поток точечного источника света внутри шара, координаты точек в которых следует рассчитать освещенность, площадь участка с искомым коэффициентом отражения.

***Цель работы:***

Овладеть навыками расчета освещенности на внутренней поверхности фотометрического шара и расчета коэффициента отражения части поверхности фотометрического шара как аналитически, так и с помощью компьютерного моделирования с использованием комплекса программ Lumicept.

***Задачи:***

1. Расчет освещенности внутренней поверхности фотометрического шара
    - Провести аналитический расчет освещенности в заданных точках внутренней поверхности фотометрического шара.
    - Сформировать сцену фотометрического шара и провести компьютерное моделирование процесса измерения освещенности в заданных точках с помощью программного комплекса Lumicept с использованием скрипта Python. Моделирование (виртуальное измерение) провести как методом прямой трассировки, используя модель фотоприемника – `Plane illuminance observer`, так методом двунаправленной трассировки – `Path Tracing`.
    - Сравнить значения освещенности, полученные в результате виртуального измерения с соответствующими значениями, полученными аналитически.

2. Расчет коэффициента отражения части поверхности фотометрического шара
    - Сформировать сцену фотометрического шара, состоящего из двух частей в соответствии с индивидуальным заданием. 
    - Провести моделирование процесса измерения освещенности поверхности шара в заданных точках, используя модель фотоприемника – `Plane illuminance observer`. Определить суммарный (средний) коэффициент диффузного отражения `Kd'`. Вычислить коэффициент диффузного отражения `Kd'` исследуемой части шара.
    - Определить погрешность “измерения”, сравнивая плаченное значение `Kd'`, с его истинным значением, указанным в индивидуальном задании.

Отчет представить в электронном виде: Формат MS Word или PowerPoint, эскиз схемы с указанием заданных точек. Для подготовки эскиза можно использовать скриншоты из Lumicept. Результаты моделирования представить в виде таблицы. К отчету приложить файлы скриптов (*.py) и сцен (*.iof).

# Лабораторная №2: Моделирование равномерного распределения лучей внутри плоских фигур (треугольник, круг) #

***Исходные данные:***

Координаты вершин плоского треугольника. Радиус круга.

***Цель работы:***

Овладеть навыками расчета равномерного распределения лучей внутри плоского треугольника и круга, а также навыками визуализации полученного распределения лучей с использованием комплекса программ Lumicept.

***Задачи:***

- Используя лекционный материал по методике расчета равномерного распределения случайной величины, **написать программы** (C/С++, Python) для расчета равномерного распределения лучей внутри плоского треугольника и круга, **сформировать массивы данных** требуемых распределений для различного количества лучей (1000, 10000, 100000, 1000000).
- **Визуализировать полученное распределение** с помощью комплекса программ Lumicept. Для визуализации использовать два способа: Первый способ подразумевает визуализацию распределения в виде изображения с широким динамическим диапазоном HDRI; Второй способ подразумевает формирование источника света типа RaySet, и последующие расчет и визуализацию освещенности на модели плоского приемника (`Plane Observer`). Размер плоского приемника сделать таким, чтобы треугольник и круг были вписаны в прямоугольник приемника.
- **Оценить равномерность полученного распределения** с помощью инструмента “Detector properties” проверяя среднее значение в трех различных зонах изображения приемника.

Отчет представить в электронном виде: Формат MS Word или PowerPoint. Можно использовать скриншоты из Lumicept. Оценку равномерности для трех различных зон представить в виде таблицы. К отчету приложить тексты разработанных программ, исполняемые модули, HDRI (LUX) файлы, файлы сцен (*.iof) и RAY-файлы.

# Лабораторная №3: Моделирование равномерного распределения лучей на сфере (для равноинтенсивной и ламбертовской диаграмм излучения) #

***Исходные данные:***

Радиус сферы.

***Цель работы:***

Овладеть навыками расчета равномерного распределения лучей на сфере (для равноинтенсивной и ламбертовской диаграмм излучения), а также навыками визуализации полученного распределения лучей с использованием комплекса программ Lumicept.

***Задачи:***

- Используя лекционный материал по методике расчета равномерного распределения случайной величины, **написать программы** (C/С++, Python) для расчета равномерного распределения лучей на сфере (для равноинтенсивной и ламбертовской диаграмм излучения), **сформировать массивы данных** требуемых распределений для различного количества лучей (10000, 100000, 1000000).
- **Визуализировать полученное распределение** с помощью комплекса программ Lumicept. Для визуализации можно использовать формирование источника света типа RaySet, и последующие расчет и визуализация освещенности на модели приемника углового распределения излучения (`Gonio Observer`). Разрешение приемника (по углам phi и theta) задавать не менее 180 x 91.
- **Оценить равномерность полученного распределения** с помощью инструмента `Detector properties` проверяя среднее значение в трех различных зонах изображения приемника.

Отчет представить в электронном виде: Формат MS Word или PowerPoint. Можно использовать скриншоты из Lumicept. Оценку равномерности для трех различных зон представить в виде таблицы. К отчету приложить тексты разработанных программ, исполняемые модули, HDRI (LUX) файлы, файлы сцен (*.iof) и RAY-файлы.


# Лабораторная №4: Моделирование равномерного распределения лучей на сфере для диаграммы излучения, заданной таблично #

***Исходные данные:***

Сфера единичного радиуса.

***Цель работы:***

Овладеть навыками формирования распределения лучей на сфере с заданной таблично плотностью распределения интенсивности светового излучения для создания косинусной (относительно направления зенита) диаграммы излучения, а также навыками визуализации полученного распределения лучей с использованием комплекса программ Lumicept.

***Задачи:***

- Используя лекционный материал по методике формирования заданного таблично распределения интенсивности светового излучения на сфере, **написать программу** (C/С++, Python) для создания соответствующего распределения лучей на сфере. 

    | **theta, deg** | **1000*cos(theta)** |
    |----------------|---------------------|
    | 0              | 1000                |
    | 6              | 994.5218954         |
    | 12             | 978.1476007         |
    | 18             | 951.0565163         |
    | 24             | 913.5454576         |
    | 30             | 866.0254038         |
    | 36             | 809.0169944         |
    | 42             | 743.1448255         |
    | 48             | 669.1306064         |
    | 54             | 587.7852523         |
    | 60             | 500                 |
    | 66             | 406.7366431         |
    | 72             | 309.0169944         |
    | 78             | 207.9116908         |
    | 84             | 104.5284633         |
    | 90             | 0                   |

- **Сформировать массив данных** требуемого распределения для различного количества лучей (10000, 100000, 1000000, 10000000). 
- **Визуализировать полученное распределение** с помощью комплекса программ Lumicept. Для визуализации сформировать источник света типа RaySet, а затем рассчитать и визуализировать распределение интенсивности на модели приемника углового распределения излучения (`Gonio Observer`). Разрешение приемника (по углам phi и theta) задавать не менее 180 x 91.
- **Оценить неравномерность полученного распределения** с помощью инструмента “Detector properties” проверяя среднее значение в нескольких малых зонах изображения приемника вдоль сечения по углу theta. А также с помощью графика сечения изображения приемника по углу theta.

Отчет представить в электронном виде: Формат MS Word или PowerPoint. Можно использовать скриншоты из Lumicept. Оценку равномерности для трех различных зон представить в виде таблицы. К отчету приложить тексты разработанных программ, исполняемые модули, HDRI (LUX) файлы, файлы сцен (*.iof) и RAY-файлы.
