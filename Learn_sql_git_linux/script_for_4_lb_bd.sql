-- Определяем функцию вывода списка группы
create or replace function get_group(gr_id text) returns refcursor as 
$$
declare
	curs1 refcursor := 'curs1';
begin
	open curs1 for select * from students where groupid = gr_id;
	return curs1;
end;
$$ language plpgsql;

-- Вызов созданной функции
select * from get_group('Б::2022::3');

-- Определяем функцию подсчета фактического числа студентов на факультете
create or replace function faculty_amount(fac_id text) returns integer as
$$
declare
	amount integer := 0;
	r edu%rowtype;
	fac_code text := null;
begin
	select faculty_code into fac_code from faculties where faculty_code = fac_id;
	if fac_code is null then
		raise exception 'ERROR: Факультет с кодом % не найден!', fac_id;
	else
		for r in (select * from edu where groupid like (fac_id || '%')) loop
			amount := amount + r.students_amount;
		end loop;
	end if;
	return amount;
end;
$$ language plpgsql;

-- Вызов сделанной функции
select * from faculty_amount('П');

/*
Преимущество функций перед представлениями заключается в их универсальности. Имеется в виду, что функции могут возвращать любые типы данных, в том числе и сущности(таблицы), тем самым включая в себя функционал представлений.
*/

------------------------


-- Оценка работы индексов на запросах с фильтрацией над одной таблицей
select * from edu
where students_amount between 49 and 52 and groupid ~ '::2019::' limit 5;

explain (analyze, costs off)
select * from edu
where students_amount between 49 and 52 and groupid ~ '::2019::' limit 5;

create index idx_edu_49_stud_amount_52_group_2019 on edu (students_amount, groupid);

set enable_seqscan = off;

explain (analyze, costs off)
select * from edu
where students_amount between 49 and 52 and groupid ~ '::2019::' limit 5;

set enable_seqscan = on;

-- Оценка работы индексов на запросах с фильтрацией над несколькими таблицами

-- Число студентов из городов, код которых кончается на "Б"
select c.name, count(id) 
from cities c join students s on c.name = s.city
where s.admission_year in (2018, 2019)
and c.name like '%Б'
group by c.name;

explain (analyze, costs off) select c.name, count(id) 
from cities c join students s on c.name = s.city
where s.admission_year in (2018, 2019)
and c.name like '%Б'
group by c.name;

create index idx_students_adm_year on students(admission_year);
create index idx_cities_name on cities(name);

set enable_seqscan = off;

explain (analyze, costs off) select c.name, count(id) 
from cities c join students s on c.name = s.city
where s.admission_year in (2018, 2019)
and c.name like '%Б'
group by c.name;

set enable_seqscan = on;

------------------
-- Работа с полнотекстовым поиском

-- просто текст

create index idx_faculty_describe_lang
on faculties using gin(to_tsvector('russian', description));

explain analyze
select faculty_code, description from faculties
where to_tsvector('russian', description) @@ to_tsquery('english');

-- массивы

create index idx_faculty_exams 
on faculties using gin (exams);

explain analyze
select faculty_code, exams from faculties
where exists (
        select * from unnest(exams) as elem -- с помощью unnest делаем массив таблицей
        where elem ~ '#tech'
);

-- json

create index idx_faculty_specs 
on faculties using gin(specs);

explain analyze
select faculty_code, specs from faculties
where specs @> '{"rating": "High"}';

----
-- Оптимизируем вставку/удаление/изменение занчений в большую таблицу

-- для чтения добавим популярные индексы
create index idx_students_groupid on students (groupid);
create index idx_students_name on students (name);
create index idx_students_adm_year on students (admission_year);

-- для удаления разделим данные на секции (секционирование)
-- Cоздадим партиционированную таблицу-клон 
create table modern_students (
	id bigserial,
	name text not null,
	groupID text not null,
	dateOfBirth date,
	city text,
	admission_year integer
)partition by range(admission_year);

-- Разбиваем ее на части
create table students_before_2019 partition of modern_students
for values from (0) to (2019);
create table students_after_2019 partition of modern_students
for values from (2019) to (2030);

--запишем старые данные в новую партиционную таблицу
insert into moder_students select * from students;

--для добавления большого объема данных следует очищать ресурсозатратные индексы
drop index idx_students_pkey;

insert into students values <новые данные>;

create index idx_students_pkey on students (id);

