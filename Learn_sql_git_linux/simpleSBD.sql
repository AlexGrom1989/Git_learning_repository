-- Создаем студентов
create table students (
	id bigserial primary key,
	name text not null,
	groupID text not null,
	dateOfBirth date,
	city text,
	admission_year integer
);


-- Создаем города
create table cities (
	name text not null
);
-- Заполняем города
insert into cities 
values ('МСК'), ('СПБ'), ('ЕКБ'), ('ЧЛБ'), ('НН'), ('ВН'), ('КРД'), ('УФА'), ('СЕВ'), ('КРОП');


-- Заполняем студентов
create or replace function insert_func() returns void as $$
declare
	i integer;
	j integer;
	fio_code text := '';
	st_date date := '2000-01-01';
	fin_date date := '2006-01-01';
	birth date;
	admis_date integer;
	letter text[] := array['П', 'К', 'З', 'Ж', 'Е', 'Д', 'Г', 'В', 'Б', 'А', 'Ч', 'Т', 'С', 'Р', 'Ф', 'Л', 'М', 'Н', 'О', 'Ш'];
	
begin
	for i in 1..100000000 loop
		
		for j in 1..3 loop
			fio_code := fio_code || letter[1+floor(random()*19)];
		end loop;
		
		birth := st_date + (random() * (fin_date - st_date + 1))::int;
		admis_date := date_part('YEAR', birth) + 18;
		
		insert into students (name, groupID, dateOfBirth, city, admission_year)
		values (
			'Student ' || fio_code || '_' || i,
			letter[1+floor(random()*19)] || '::' || admis_date || '::' || (i % 17000),
			birth,
			(select name from cities order by random() limit 1),
			admis_date
		);
		
		fio_code := '';
		birth := NULL;
		admis_date := NULL;
		
	end loop;
end $$ language plpgsql;

select insert_func();

-- Создаем факультеты
create table faculties (
	faculty_code text primary key,
	name text,
	students_amount integer default 1050000,
	specs jsonb default '{"specs": ["Basic", "Intermediate", "Professional"]}',
	dekan text
);

-- Заполняем факультеты
insert into faculties (faculty_code, name, dekan)
values 
('П', 'Психология', 'Петров Петр Петрович'),
('К', 'Кибернетика', 'Кузнецов Сергей Иванович'),
('З', 'Здравоохранение', 'Зайцева Анна Викторовна'),
('Ж', 'Журналистика', 'Жукова Мария Александровна'),
('Е', 'Экономика', 'Егоров Алексей Дмитриевич'),
('Д', 'Дизайн', 'Дмитриев Денис Сергеевич'),
('Г', 'География', 'Горшков Игорь Николаевич'),
('В', 'Востоковедение', 'Васильев Николай Андреевич'),
('Б', 'Биология', 'Баранов Алексей Владимирович'),
('А', 'Архитектура', 'Александрова Ольга Петровна'),
('Ч', 'Человеческие ресурсы', 'Чернов Илья Владимирович'),
('Т', 'Технологии', 'Тимофеев Андрей Сергеевич'),
('С', 'Социология', 'Смирнова Наталья Васильевна'),
('Р', 'Реклама', 'Рябов Максим Анатольевич'),
('Ф', 'Филология', 'Федорова Татьяна Сергеевна'),
('Л', 'Логистика', 'Лебедев Владислав Константинович'),
('М', 'Медицинские науки', 'Мартынова Екатерина Юрьевна'),
('Н', 'Неврология', 'Никитин Виктор Павлович'),
('О', 'Огневое искусство', 'Овчинникова Светлана Алексеевна'),
('Ш', 'Шумовые технологии', 'Широков Юрий Валентинович');

-- Создаем таблицу обучения
create table edu (
	groupID text primary key,
	students_amount integer,
	mean_stipend integer default 2700,
	faculty_code text references faculties(faculty_code),
	edu_year integer default 2024
);

-- Заполняем таблицу обучения
create or replace function insert_edu() returns void as $$
declare 
	stipends integer[] := array[0, 2700, 3500, 4500];
begin
	insert into edu (groupID, students_amount)
	select groupid, count(*) from students group by groupid order by groupid;
	
	update edu set 
		mean_stipend = stipends[1 + floor(random() * 3)],
		faculty_code = left(groupid, 1);
end
$$ language plpgsql;

select insert_edu();

