-- Create the BigQuery dataset
CREATE SCHEMA IF NOT EXISTS `pj-test1-499320.student_journey`
OPTIONS (
  location = "US"
);

-- CSV files should be uploaded to:
-- gs://sql_graph/


LOAD DATA OVERWRITE `pj-test1-499320.student_journey.students`
FROM FILES (
  format = 'CSV',
  uris = ['gs://sql_graph/students.csv'],
  skip_leading_rows = 1,
  source_column_match = 'NAME'

);


LOAD DATA OVERWRITE `pj-test1-499320.student_journey.programs`
FROM FILES (
  format = 'CSV',
  uris = ['gs://sql_graph/programs.csv'],
  skip_leading_rows = 1,
  source_column_match = 'NAME'

);


LOAD DATA OVERWRITE `pj-test1-499320.student_journey.courses`
FROM FILES (
  format = 'CSV',
  uris = ['gs://sql_graph/courses.csv'],
  skip_leading_rows = 1,
  source_column_match = 'NAME'

);


LOAD DATA OVERWRITE `pj-test1-499320.student_journey.terms`
FROM FILES (
  format = 'CSV',
  uris = ['gs://sql_graph/terms.csv'],
  skip_leading_rows = 1,
  source_column_match = 'NAME'

);


LOAD DATA OVERWRITE `pj-test1-499320.student_journey.institutions`
FROM FILES (
  format = 'CSV',
  uris = ['gs://sql_graph/institutions.csv'],
  skip_leading_rows = 1,
  source_column_match = 'NAME'

);


LOAD DATA OVERWRITE `pj-test1-499320.student_journey.services`
FROM FILES (
  format = 'CSV',
  uris = ['gs://sql_graph/services.csv'],
  skip_leading_rows = 1,
  source_column_match = 'NAME'

);


LOAD DATA OVERWRITE `pj-test1-499320.student_journey.enrollments`
FROM FILES (
  format = 'CSV',
  uris = ['gs://sql_graph/enrollments.csv'],
  skip_leading_rows = 1,
  source_column_match = 'NAME'

);


LOAD DATA OVERWRITE `pj-test1-499320.student_journey.student_terms`
FROM FILES (
  format = 'CSV',
  uris = ['gs://sql_graph/student_terms.csv'],
  skip_leading_rows = 1,
  source_column_match = 'NAME'

);


LOAD DATA OVERWRITE `pj-test1-499320.student_journey.service_usage`
FROM FILES (
  format = 'CSV',
  uris = ['gs://sql_graph/service_usage.csv'],
  skip_leading_rows = 1,
  source_column_match = 'NAME'

);


LOAD DATA OVERWRITE `pj-test1-499320.student_journey.program_history`
FROM FILES (
  format = 'CSV',
  uris = ['gs://sql_graph/program_history.csv'],
  skip_leading_rows = 1,
  source_column_match = 'NAME'

);


LOAD DATA OVERWRITE `pj-test1-499320.student_journey.awards`
FROM FILES (
  format = 'CSV',
  uris = ['gs://sql_graph/awards.csv'],
  skip_leading_rows = 1,
  source_column_match = 'NAME'

);


LOAD DATA OVERWRITE `pj-test1-499320.student_journey.transfers`
FROM FILES (
  format = 'CSV',
  uris = ['gs://sql_graph/transfers.csv'],
  skip_leading_rows = 1,
  source_column_match = 'NAME'

);


LOAD DATA OVERWRITE `pj-test1-499320.student_journey.program_requirements`
FROM FILES (
  format = 'CSV',
  uris = ['gs://sql_graph/program_requirements.csv'],
  skip_leading_rows = 1,
  source_column_match = 'NAME'

);


LOAD DATA OVERWRITE `pj-test1-499320.student_journey.course_prerequisites`
FROM FILES (
  format = 'CSV',
  uris = ['gs://sql_graph/course_prerequisites.csv'],
  skip_leading_rows = 1,
  source_column_match = 'NAME'

);