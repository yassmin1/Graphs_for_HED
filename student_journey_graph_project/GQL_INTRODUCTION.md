# GQL Command Reference

## The Core Commands of Graph Query Language, Explained for Anyone

GQL (Graph Query Language) is the language BigQuery uses to query property graphs. If you already know SQL, most of this will feel familiar — `WHERE`, `GROUP BY`, `ORDER BY`, and aggregate functions all work the same way. What's different is the part that describes *what to match*: instead of naming tables and writing join conditions, you draw the shape of the relationship you're looking for, using nodes in parentheses and edges in brackets.

Every example below uses the same running graph so the syntax stays grounded in one consistent, familiar context:

```text
pj-test1-499320.student_journey.StudentJourneyGraph
```

with node types `Student`, `Course`, `Program`, `Term`, `Institution`, `SupportService`, and edge types `EnrolledIn`, `AttendedTerm`, `DeclaredProgram`, `UsedService`, `EarnedAward`, `TransferredTo`, `Requires`, and `Precedes`.

---

## 1. `GRAPH` — naming which graph you're querying

Every GQL query starts by declaring which property graph it runs against, the same way a SQL query starts with `FROM`.

```sql
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`

MATCH (student:Student)
RETURN student.student_id
LIMIT 5;
```

**What it does:** Tells BigQuery which graph's node and edge definitions to use for everything that follows. Nothing else in the query works without this line.

---

## 2. `MATCH` — the heart of GQL

`MATCH` describes a pattern you want to find in the graph. This is the one command that has no real equivalent in plain SQL — it replaces joins with a drawing of the relationship.

**Node syntax:** `(variable:Label {property: value})`
**Edge syntax:** `-[variable:Label]->` (the arrow shows direction; a plain `-[...]-` with no arrowhead matches either direction)

```sql
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`

MATCH (student:Student)-[enrollment:EnrolledIn]->(course:Course)
RETURN student.student_id, course.course_name
LIMIT 10;
```

**Reading it left to right:** "Find a `Student` node, connected by an `EnrolledIn` edge, to a `Course` node." The variables (`student`, `enrollment`, `course`) let you refer to each matched piece later, in `WHERE`, `RETURN`, or elsewhere.

**Matching a longer chain** — each additional hop just extends the pattern:

```sql
MATCH
  (student:Student)-[:DeclaredProgram]->(program:Program),
  (student)-[:TransferredTo]->(institution:Institution)
```

Two comma-separated patterns that share the variable `student` are automatically matched against the *same* student — this is how you connect a student to two different things at once without writing a join.

---
`MATCH` is how you tell GQL "here's the shape I'm looking for in the graph." That's really it.

## The core idea

You draw the pattern using two symbols:

- **`( )`** = a thing (a node) — like a student, a course, a program
- **`[ ]`** = a connection (an edge) between two things — like "enrolled in" or "transferred to"

So this:

```sql
MATCH (student:Student)-[:EnrolledIn]->(course:Course)
```

reads exactly like the sentence it looks like: **"Find a Student, connected by an EnrolledIn arrow, to a Course."**

## Think of it like a fill-in-the-blank sentence

- `(student:Student)` → "a student"
- `-[:EnrolledIn]->` → "who enrolled in"
- `(course:Course)` → "a course"

`MATCH` goes and finds every real example in your data that fits that sentence, and gives you back one row per match.

## A longer chain works the same way

```sql
MATCH (student:Student)-[:EnrolledIn]->(course:Course)-[:Precedes]->(nextCourse:Course)
```

= "a student, who took a course, that comes before another course." Each extra `-[ ]->(  )` just adds one more link to the sentence.

## Connecting one thing to two different things

```sql
MATCH
  (student:Student)-[:DeclaredProgram]->(program:Program),
  (student)-[:TransferredTo]->(institution:Institution)
```

The comma just means "and also" — and because both lines reuse the same `student` variable, GQL makes sure it's talking about the *same* student both times. This is the trick that replaces a join in SQL: instead of matching two tables on a shared ID column, you just write the shared variable name twice.

## The one-sentence version

**`MATCH` doesn't fetch rows from a table — it searches the whole graph for anything shaped like the pattern you drew, and hands back every match it finds.**
## 3. Property filters in curly braces — `{property: value}`

You can filter directly inside a node or edge pattern, which is often clearer than a separate `WHERE` clause when you're anchoring the match to one specific thing.

```sql
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`

MATCH (course:Course {course_id: "C004"})<-[:EnrolledIn]-(student:Student)
RETURN student.student_id;
```

**What it does:** Matches only the `Course` node whose `course_id` equals `"C004"` (Developmental Mathematics), then finds every student enrolled in it. This is generally the fastest way to filter, because BigQuery can narrow the search before it even starts traversing.

---

## 4. `WHERE` — filtering after the pattern is matched

`WHERE` filters the matched pattern using conditions that don't fit neatly into a property filter — comparisons between two matched elements, date logic, `IN` lists, and so on.

```sql
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`

MATCH
  (student:Student)-[enrollment:EnrolledIn]->(course:Course)

WHERE
  enrollment.passed = TRUE
  AND course.course_group = "Mathematics"

RETURN student.student_id, course.course_name;
```

**What it does:** Keeps only the rows where the enrollment was passed *and* the course belongs to the Mathematics group. `WHERE` runs after the graph pattern is found, filtering the results the same way it would in SQL.

---

## 5. `FILTER` — the GQL-native alternative to `WHERE`

GQL also has its own keyword, `FILTER`, which does the same job as `WHERE` and is fully interchangeable with it. `WHERE` is actually an optional keyword you can include *inside* a `FILTER` statement — the two queries below are identical:

```sql
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`
MATCH (student:Student)-[enrollment:EnrolledIn]->(course:Course)
FILTER enrollment.passed = TRUE
RETURN student.student_id;
```

```sql
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`
MATCH (student:Student)-[enrollment:EnrolledIn]->(course:Course)
FILTER WHERE enrollment.passed = TRUE
RETURN student.student_id;
```

**When to reach for `FILTER` instead of `WHERE`:** After an aggregation step (see `LET` and `NEXT` below), `FILTER` is the way to filter on an aggregated value, since aggregated results don't have a `WHERE` clause of their own to attach to.

---

## 6. `RETURN` — choosing what comes back

`RETURN` is GQL's version of `SELECT`. It picks which properties to output, lets you rename them with `AS`, and is also where aggregate functions go.

```sql
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`

MATCH (student:Student)-[transfer:TransferredTo]->(institution:Institution)

RETURN
  institution.institution_name,
  COUNT(DISTINCT student.student_id) AS transferred_students,
  ROUND(AVG(transfer.gpa_at_transfer), 2) AS average_gpa;
```

**What it does:** Returns one row per institution, with a count of distinct transferring students and their average GPA at transfer. `RETURN *` returns every property of every matched element instead of naming them individually.

**Implicit grouping:** Notice there's no `GROUP BY` in that query. In GQL, if your `RETURN` list mixes aggregated values (like `COUNT`) with non-aggregated ones (like `institution.institution_name`), BigQuery automatically groups by every non-aggregated item — equivalent to writing `GROUP BY ALL`.

---

## 7. `GROUP BY` — grouping explicitly

You can still write `GROUP BY` yourself, which is useful when you want to be explicit or group by something other than everything in the `RETURN` list.

```sql
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`

MATCH
  (program1:Program)-[:Requires]->(course:Course)<-[:Requires]-(program2:Program)

WHERE program1.program_id < program2.program_id

RETURN
  program1.program_name AS first_program,
  program2.program_name AS second_program,
  COUNT(DISTINCT course.course_id) AS shared_required_courses

GROUP BY
  program1.program_name,
  program2.program_name

ORDER BY shared_required_courses DESC;
```

**What it does:** Groups the matched program pairs and counts how many required courses they share — the explicit `GROUP BY` here matches what would have happened implicitly, but spelling it out makes the intent clearer to a future reader.

---

## 8. `ORDER BY`, `LIMIT`, and `OFFSET` — sorting and paging

These three work exactly as they do in SQL, applied to the final result set.

```sql
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`

MATCH (student:Student)
RETURN student.student_id, student.final_outcome

ORDER BY student.student_id
LIMIT 10
OFFSET 20;
```

**What it does:** Sorts by `student_id`, skips the first 20 rows, and returns the next 10 — useful for paging through a large result set. `LIMIT` is especially important in graph queries, since an unbounded pattern match over a large graph can return far more rows than you actually want to look at.

---

## 9. `OPTIONAL MATCH` — including things that might not exist

A plain `MATCH` only returns rows where the *entire* pattern exists. If you also want to see students who *don't* have a matching relationship — without losing them from the result — use `OPTIONAL MATCH`.

```sql
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`

MATCH (student:Student)
OPTIONAL MATCH (student)-[:UsedService]->(service:SupportService {service_id: "S003"})
RETURN student.student_id, service.service_name AS transfer_center_visit;
```

**What it does:** Returns every student. For students who never used the transfer center, `transfer_center_visit` comes back as `NULL` instead of the student disappearing from the results entirely. This solves a common gap: a plain `MATCH` can't produce "students with no matching edge," because a pattern that doesn't exist can't match.

---

## 10. Variable-length paths — `{m, n}`

Sometimes you don't know how many hops separate two things. Adding `{minimum, maximum}` after an edge pattern tells GQL to follow that edge type repeatedly, anywhere between `m` and `n` times.

```sql
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`

MATCH
  (start:Course {course_id: "C004"})-[:Precedes]->{1,5}(destination:Course)

RETURN destination.course_name;
```

**What it does:** Starting from Developmental Mathematics, follows the `Precedes` relationship anywhere from 1 to 5 hops deep, returning every course reachable through some chain of prerequisites — without anyone having to know or specify the chain's exact length in advance.

---

## 11. `ANY`, `ANY SHORTEST`, and `ANY CHEAPEST` — controlling which paths come back

When a variable-length pattern could match many different paths between the same two points, these keywords control how many of those paths you actually get back.

```sql
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`

MATCH path = ANY SHORTEST
  (start:Course {course_id: "C004"})-[:Precedes]->{1,5}(destination:Course)

RETURN
  destination.course_name,
  PATH_LENGTH(path) AS number_of_steps

ORDER BY number_of_steps;
```

- **`ANY`** returns one arbitrary path per matching pair of endpoints, instead of every possible path — useful when you only care *that* a connection exists, not every way to make it.
- **`ANY SHORTEST`** returns the shortest path (fewest hops) between each pair of endpoints.
- **`ANY CHEAPEST`** returns the lowest-cost path, based on a `COST` expression you attach to the edge pattern — useful when "shortest" should mean something other than fewest hops (for example, lowest total credits rather than fewest courses).

**Why this matters:** Without one of these, a variable-length pattern can return an enormous number of redundant paths between well-connected nodes. These keywords collapse that down to the one path per pair that actually answers the question.

---

## 12. `LET` — defining a named value mid-query

`LET` lets you compute a value once and reuse it later in the same query, similar to declaring a variable. It's especially useful with **group variables** — values bound to an entire array of matched elements inside a variable-length pattern.

```sql
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`

MATCH
  (student:Student)-[enrollments:EnrolledIn]->{1,10}(course:Course)

LET total_credits = SUM(enrollments.credits_attempted)

RETURN student.student_id, total_credits
ORDER BY total_credits DESC;
```

**What it does:** `enrollments` here is bound to an *array* of every `EnrolledIn` edge matched along the path (a group variable), and `LET` uses a horizontal aggregate (`SUM`) to add up the credits across that whole array for each student — a calculation that would be awkward to express any other way.

---

## 13. `NEXT` — chaining multiple query steps

`NEXT` lets you take the output of one linear query statement and feed it into another, similar to a pipeline. Each step can `MATCH`, `LET`, `FILTER`, and `RETURN` independently.

```sql
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`

MATCH (student:Student)-[:UsedService]->(service:SupportService {service_id: "S003"})
RETURN student.student_id

NEXT

MATCH (student:Student {student_id: student_id})-[transfer:TransferredTo]->(institution:Institution)
RETURN student_id, institution.institution_name;
```

**What it does:** The first step finds every student who used the transfer center and passes their IDs forward. The second step takes just those IDs and finds where they transferred — two focused steps chained together instead of one large, tangled pattern.

---

## 14. `UNION ALL` — combining results from different patterns

Just like in SQL, `UNION ALL` stacks the results of two separately matched patterns into one result set, as long as the column names and types line up.

```sql
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`

MATCH (student:Student)-[:EarnedAward]->(:Program)
RETURN student.student_id, "Credentialed" AS path_type

UNION ALL

MATCH (student:Student)-[:TransferredTo]->(:Institution)
RETURN student.student_id, "Transferred" AS path_type;
```

**What it does:** Produces one combined list of students tagged by which outcome they achieved, even though the two patterns being matched are completely different shapes.

---

## 15. Subqueries — `EXISTS`, `IN`, and `VALUE`

GQL supports subqueries for checking existence or membership without pulling back a full result set.

```sql
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`

RETURN EXISTS {
  MATCH (s:Student {student_id: "1042"})-[:TransferredTo]->(:Institution)
} AS has_transferred;
```

**What it does:** `EXISTS { ... }` returns `TRUE` or `FALSE` depending on whether the inner pattern matches at least once — never `NULL` — which makes it a clean way to ask a yes/no question about one student without listing every matching row.

`VALUE { ... }` works similarly but pulls back a single scalar value from a subquery, and a subquery can also be used with `IN` / `NOT IN` to check whether a value appears in a subquery's results.

---

## 16. `GRAPH_TABLE` — using a graph pattern inside ordinary SQL

`GRAPH_TABLE` is the bridge between GQL and regular GoogleSQL. It runs a graph match and hands the result back as a normal table, so you can apply anything standard SQL can do — window functions, additional joins to non-graph tables, `QUALIFY`, and so on.

```sql
SELECT
  institution_name,
  course_name,
  transferred_students
FROM GRAPH_TABLE(
  `pj-test1-499320.student_journey.StudentJourneyGraph`

  MATCH
    (student:Student)-[enrollment:EnrolledIn]->(course:Course),
    (student)-[:TransferredTo]->(institution:Institution)

  WHERE enrollment.passed = TRUE

  RETURN
    institution.institution_name AS institution_name,
    course.course_name AS course_name,
    COUNT(DISTINCT student.student_id) AS transferred_students

  GROUP BY institution.institution_name, course.course_name
)

QUALIFY ROW_NUMBER() OVER (
  PARTITION BY institution_name
  ORDER BY transferred_students DESC
) <= 5;
```

**What it does:** The `GRAPH_TABLE(...)` block runs entirely in GQL and produces rows; everything outside it — `SELECT`, `QUALIFY`, the window function — is plain SQL. This is the pattern to reach for whenever a question needs graph traversal for part of the answer and standard relational tools (ranking, further joins) for the rest.

---

## Useful GQL Functions

| Function | What it returns |
|---|---|
| `PATH_LENGTH(path)` | Number of edges (hops) in a matched path |
| `NODES(path)` | An array of every node in a matched path |
| `PATH_FIRST(path)` / `PATH_LAST(path)` | The first or last element in a path |
| `LABELS(element)` | The label(s) of a matched node or edge |
| `SOURCE_NODE_ID(edge)` / `DESTINATION_NODE_ID(edge)` | Internal identifiers for an edge's endpoints |
| `TO_JSON(element)` | Converts a full graph element (with all its properties) to JSON — required for graph visualization tools |

---

## Quick Reference: What to Use When

| You want to... | Use |
|---|---|
| Say which graph you're querying | `GRAPH` |
| Describe a relationship shape to find | `MATCH` |
| Filter to one specific node up front | `{property: value}` inline filter |
| Filter on a comparison or condition | `WHERE` or `FILTER` |
| Choose and rename output columns | `RETURN ... AS ...` |
| Aggregate (with or without explicit grouping) | `RETURN` with aggregate functions, or `GROUP BY` |
| Sort, limit, or page results | `ORDER BY`, `LIMIT`, `OFFSET` |
| Include non-matches instead of dropping them | `OPTIONAL MATCH` |
| Follow a relationship an unknown number of times | `-[:EdgeType]->{m,n}` |
| Get only the shortest or one path, not all of them | `ANY`, `ANY SHORTEST`, `ANY CHEAPEST` |
| Compute a reusable value mid-query | `LET` |
| Chain multiple query steps together | `NEXT` |
| Combine two different patterns' results | `UNION ALL` |
| Ask a yes/no or single-value question | `EXISTS { }`, `VALUE { }`, `IN { }` |
| Mix a graph match into regular SQL | `GRAPH_TABLE( ... )` |

---

## A Closing Note on Performance

Two habits go a long way with any GQL query: **start from something selective** — a specific ID, a narrow label, a tight property filter — rather than matching every node of a type first and filtering afterward; and **prefer one `MATCH` with comma-separated patterns** over several separate `MATCH` statements when you're connecting the same entity to multiple things. Both give BigQuery's graph engine less to enumerate before your filters even apply.