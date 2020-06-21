# EduHack

# Run app
Для запуска приложения на Linux в проект добавлен run.sh файл, запускаем 
```bash
./run.sh
```
Для Windows использовать команду 

```bash
docker -compose
```
# Quick Start
При первом запуске будут доступны различные образовательные программы, на которых можно понять, как устроено приложение. 
При нажатии на модель попадаем на страницу с графиками, описывающими ее. Сверху будет график, сгенерированный на основе большого 
количества разнородних, но коллерирующих критериев(30+), нижже можно ознакомиться с 6 наиболее популярными. Остальные графики спрятаны, 
но могут быть развернуты, если есть необходимость. При наведении курсора на график справа появляются возможности анализировать его с 
легкой статистики, возможность сравнить график с каким-либо другим, а также, в случае падения какого-то критерия, представлен 
способ решения и избежания повторного падения при следующем измерении.

# Compare Graphics
Как было описано выше, графики можно сравнивать, выбирая определенные из них. Само сравнение происходит на странице "Сравнение Графиков" в верху экрана 

# Google Forms Data

К проекту можно привязать опросник, при помощи которого можно собирать данные о критериях много проще, чем поиск их вручную, 
функционал добавления полученной с ответов на Google-форму информации к определенной модели реализован сверху в "Импорт из Google Forms"

# Upload Model (Handle-Mode)

Для загрузки собственной модели в систему следует использовать следующих формат: информация о критериях хранится в Excel-файле, первый 
столбец которого называется "date" и содержит дату(!воу!). Дальше идут столбцы с критериями, количество строк которых равно количеству 
строк в столбце "date". 

Сервис поддерживает следующие критерии(следующий пункт)

# Criteria

*Agg_data* – Интегральный критерий  
*percent_hired_first_year* – Процент выпускников устроившхся на работу в топовые места в течении года после выпуска   
*cnt_publication_all* – Количество публикаций работ по данной направлению ОП  
*percent_autors_programm* – Процент авторских курсов именитых преподавателей  
*university_rank* – Место университета в используемом рейтинге страны  
*GOS_avg* – Средние значение Государтственного экзамена(Россия)\n или его аналога в других странах  
*Diplom_avg* – Средняя оценка за защиту диплома  
*number_of_articles* – Количество научных публикаций от преподавателей направления ОП  
*has_p2p_score* – Наличие оценки преподователей друг другом для вывода рейтинга среди них  
*has_stud_score* – Возможность для студентов оценивать преподавателей  
*n_has_phD* – Количество преподавателей со званиев Профессор на направлении ОП  
*percent_high_qval_teachers * – Процент преподавателей проходивших курсы повышения квалификации  
*has_brs* – Наличие Балльно-Рейтинговой Системы обучения  
*percent_working_student* – Процент студентов работающий во время обучения  
*avg_EGE_on_start* – Среднее количество баллов ЕГЭ(или аналогов для других стран) требуемых для поступления  
*percent_foreign_students* – Процент иногородних студентов на направлении ОП  
*percent_additional_subjects* – Количество предметов для самостоятельного(необязательного) обучения   
*которые может предложить данная программа  
*has_partners* – Есть ли у ВУЗа партнеры со стороны топовых компаних  
*has_eng_disc* – Есть ли у направления дисциплины на иностранном языке  
*has_word_accred* – Поддержка ВУЗа мировым сообществом  
*percent_avg_cnt_st_to_all* – Процент посещаемости предметов на данном направлении  
*freq_check_knowledge* – Частота проверки знаний по предмету  
*avg_salary_new/avg_region_sal* – Отношение средней зарплаты выпускника\n к средней зарплате по региону  
*percent_teachers_with_hirsh_noless2* – Процент преводавателей на направлении ОП с рейтингом Хирша не менее 2  
*percent_practic_preps* – Процент преподавателей ведущих также и практику на факультете  
*avg_stud_store_per_year* – Средний бал всех студентов за год  
*p2p_score* – Средняя оценка преподавателя рассчитанная на основе его оценок его коллег  
*student_score* –Средняя оценка преподавателя рассчитанная на основе оценок его студентов  
*number_of_articles.teachers.* – Количество статей выпущенное автором за промежуток времени  


# Example of Data
Для начала пример можно посмотреть в самой форме на странице "Импорт из Google Forms", смысл такой же
Пример данных:
```
date	               |  teacher_id |   p2p_score
2015-09-01 00:00:00	 |     1	     |  1,546972889
2016-09-01 00:00:00	 |     1	     |  4,686970885
2017-09-01 00:00:00	 |     1	     |  1,809467181
2018-09-01 00:00:00	 |     1	     |  4,280270179
2019-09-01 00:00:00	 |     1	     |  1,628968108
```


