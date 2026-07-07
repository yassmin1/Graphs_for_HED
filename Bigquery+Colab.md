# Google Colab notebook + BigQuery 
You can connect your regular Google Colab notebook to the BigQuery project `pj-test1-499320` using the BigQuery Python client.

## 1. Install the required packages

Run this in the first Colab cell:

```python
!pip install -q --upgrade google-cloud-bigquery db-dtypes pyarrow
```

Google’s BigQuery Python client requires an authenticated Google Cloud project with the BigQuery API enabled. ([Google Cloud Documentation][1])

## 2. Authenticate your Google account

```python
from google.colab import auth

auth.authenticate_user()

print("Authentication completed.")
```

Colab will ask you to select a Google account. Select the same account that has access to your Google Cloud project.

## 3. Create the BigQuery connection

```python
from google.cloud import bigquery

PROJECT_ID = "pj-test1-499320"
DATASET_NAME = "student_journey"
LOCATION = "US"

client = bigquery.Client(
    project=PROJECT_ID,
    location=LOCATION
)

print(f"Connected to project: {client.project}")
```

The BigQuery client uses the authenticated credentials from the Colab session. Google Cloud client libraries use Application Default Credentials to authenticate API requests. ([Google Cloud Documentation][2])

## 4. Test the connection

Run a simple query against your `students` table:

```python
query = """
SELECT *
FROM `pj-test1-499320.student_journey.students`
LIMIT 10
"""

students_df = client.query(query).to_dataframe()

students_df
```

You should see the first 10 student records as a pandas DataFrame.

## 5. List all tables in the dataset

```python
dataset_id = f"{PROJECT_ID}.{DATASET_NAME}"

tables = client.list_tables(dataset_id)

for table in tables:
    print(table.table_id)
```

You should see tables such as:

```text
students
courses
programs
enrollments
transfers
services
service_usage
student_terms
```

## 6. Read an entire BigQuery table

```python
table_id = "pj-test1-499320.student_journey.programs"

programs_df = client.list_rows(table_id).to_dataframe()

programs_df
```

For large tables, it is better to use a query with selected columns and a row limit rather than downloading the complete table.

```python
query = """
SELECT
    student_id,
    final_outcome,
    initial_program_id,
    first_generation,
    pell_eligible
FROM `pj-test1-499320.student_journey.students`
LIMIT 100
"""

students_sample = client.query(query).to_dataframe()

students_sample.head()
```

## 7. Run a BigQuery Graph query from Colab

You can submit the same graph queries from Python.

```python
graph_query = """
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`

MATCH
  (student:Student)
    -[transfer:TransferredTo]->
  (institution:Institution)

RETURN
  institution.institution_name,
  COUNT(DISTINCT student.student_id) AS transferred_students,
  ROUND(AVG(transfer.credits_at_transfer), 1) AS average_credits,
  ROUND(AVG(transfer.gpa_at_transfer), 2) AS average_gpa

GROUP BY institution.institution_name

ORDER BY transferred_students DESC
"""

transfer_results = client.query(graph_query).to_dataframe()

transfer_results
```

## 8. Create a chart from the graph result

```python
import matplotlib.pyplot as plt

plot_data = transfer_results.sort_values(
    "transferred_students",
    ascending=True
)

plt.figure(figsize=(10, 6))

plt.barh(
    plot_data["institution_name"],
    plot_data["transferred_students"]
)

plt.xlabel("Number of transferred students")
plt.ylabel("Transfer institution")
plt.title("Synthetic student transfers by institution")
plt.tight_layout()
plt.show()
```

## 9. Analyze course bottlenecks

```python
bottleneck_query = """
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`

MATCH
  (program:Program)
    -[:Requires]->
  (course:Course)
    <-[enrollment:EnrolledIn]-
  (student:Student)

WHERE enrollment.passed = FALSE

RETURN
  course.course_id,
  course.course_name,
  COUNT(DISTINCT student.student_id) AS affected_students,
  COUNTIF(enrollment.final_grade = "W") AS withdrawals,
  COUNTIF(enrollment.final_grade = "D") AS grade_d,
  COUNTIF(enrollment.final_grade = "F") AS grade_f

GROUP BY
  course.course_id,
  course.course_name

ORDER BY affected_students DESC
"""

bottleneck_df = client.query(bottleneck_query).to_dataframe()

bottleneck_df.head(15)
```

## 10. Save query results as a CSV

```python
transfer_results.to_csv(
    "transfer_results.csv",
    index=False
)
```

Download it from Colab:

```python
from google.colab import files

files.download("transfer_results.csv")
```

## Complete connection cell

You can combine the initial setup into one reusable cell:

```python
!pip install -q --upgrade google-cloud-bigquery db-dtypes pyarrow

from google.colab import auth
from google.cloud import bigquery

auth.authenticate_user()

PROJECT_ID = "pj-test1-499320"
DATASET_NAME = "student_journey"
LOCATION = "US"

client = bigquery.Client(
    project=PROJECT_ID,
    location=LOCATION
)

test_query = f"""
SELECT COUNT(*) AS student_count
FROM `{PROJECT_ID}.{DATASET_NAME}.students`
"""

test_result = client.query(test_query).to_dataframe()

print("Successfully connected to BigQuery.")
display(test_result)
```

## Common permission error

If you receive an error such as:

```text
403 Access Denied
```

confirm that the Google account selected in Colab has permission to run jobs and read the dataset. For read-only querying, the relevant predefined roles are generally:

* `BigQuery Job User` on the project, which permits running query jobs.
* `BigQuery Data Viewer` on the dataset, which permits reading the tables and property graph. ([Google Cloud Documentation][3])

Also confirm that your BigQuery dataset location is `US`, matching the location used when the dataset was created.

[1]: https://docs.cloud.google.com/python/docs/reference/bigquery/latest "Python Client for Google BigQuery  |  Python client libraries  |  Google Cloud Documentation"
[2]: https://docs.cloud.google.com/bigquery/docs/authentication "Authenticate to BigQuery  |  Google Cloud Documentation"
[3]: https://docs.cloud.google.com/bigquery/docs/access-control "BigQuery IAM roles and permissions  |  Google Cloud Documentation"
