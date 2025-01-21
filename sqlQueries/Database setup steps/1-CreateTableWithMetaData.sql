CREATE TABLE experimentdata (
	id SERIAL PRIMARY KEY,
	time_start BIGINT,
	time_finish BIGINT,
	task1_start BIGINT,
	task1_finish BIGINT,
	task2_start BIGINT,
	task2_finish BIGINT,
	task3_start BIGINT,
	task3_finish BIGINT,
	condition_id SMALLINT,
	first_task SMALLINT,
	second_task SMALLINT,
	third_task SMALLINT,
	first_algorithm SMALLINT,
	second_algorithm SMALLINT,
	third_algorithm SMALLINT
);