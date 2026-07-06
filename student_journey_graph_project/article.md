# The Student Journey Is Not a Spreadsheet

## Using BigQuery Graph to Connect the Dots in Higher Education

Higher-education institutions rarely suffer from a complete absence of data. They have student records, course registrations, grades, program declarations, advising visits, credentials, and transfer records. The harder problem is that these facts usually live in separate tables, and the question we want to answer is often about the path connecting them.

A dashboard can tell us how many students transferred. A graph-oriented analysis can help us investigate which course sequences, support interactions, program changes, and credit milestones commonly appeared before transfer.

This project demonstrates that idea with a fully synthetic community-college dataset. No record represents a real student, college, or university.

## Why use a graph?

SQL remains the correct tool for counts, rates, compliance reporting, and well-defined joins. A graph becomes useful when the analytical object is a relationship or path:

- a student completed one course before another;
- a program requires a connected set of courses;
- a student used several support services before reaching a milestone;
- many students followed similar routes into the same transfer institution.

The project therefore keeps ordinary BigQuery tables as the source of truth and defines a property graph over them. The graph is an analytical layer, not a replacement data warehouse.

## Model choices

The graph uses six node types: Student, Course, Program, Term, Institution, and SupportService.

The principal edge types are EnrolledIn, AttendedTerm, DeclaredProgram, UsedService, EarnedAward, TransferredTo, Requires, and Precedes.

This design intentionally avoids creating a node for every grade or visit. Those facts are properties of relationships. A grade describes a student's enrollment in a course; it is not an independent entity. A transfer term describes the transfer relationship; it is not the transfer destination itself.

## Synthetic-data logic

The generator creates 1,500 fictional students and simulates enrollment from Fall 2022 through Spring 2026. Each student receives latent preparation and engagement values that are never exported. Those hidden values influence course performance and persistence, while observable factors such as workload, enrollment intensity, advising, tutoring, gateway-course completion, accumulated credits, and transfer-center use shape later events.

The simulation intentionally contains associations that can be discovered by analysis. For example, students who complete English Composition I and College Algebra tend to persist longer. Students who reach the transfer center are more likely to have a transfer event. These are design choices made to produce a useful demonstration; they are not causal claims and should never be presented as findings about real students.

## Questions the project can explore

1. Which gateway-course combinations commonly appear before transfer?
2. Which support services are connected with longer enrollment paths?
3. Which programs send students to the widest range of institutions?
4. What prerequisite paths connect developmental education to advanced courses?
5. Which courses are shared across several successful program pathways?
6. Where do students commonly stop progressing through a required sequence?

## Responsible interpretation

A graph can make a path visually persuasive even when the underlying relationship is only descriptive. Sequence does not prove causation. Students who visit a transfer center may already be more transfer-oriented, and students who receive tutoring may differ from students who do not.

In a real institution, the next step would be to validate definitions, establish an observation window, control access, suppress small groups, de-identify student records, and involve institutional researchers, advisors, faculty, privacy officers, and students in interpreting results.

## Project contents

- `data/`: all synthetic CSV files
- `generate_synthetic_student_journey.py`: deterministic data generator
- `data_dictionary.csv`: table and column descriptions
- `project_metrics.csv`: descriptive checks from the simulation
- `sql/01_load_csv_to_bigquery.sql`: loading template
- `sql/02_create_property_graph.sql`: property-graph definition
- `sql/03_example_graph_queries.sql`: example GQL and SQL
