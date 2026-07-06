-- Replace PROJECT_ID before running.

-- 1. Students who completed both gateway courses and later transferred.
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`
MATCH
  (s:Student)-[english_enrollment:EnrolledIn]->
  (english:Course {course_id: "C002"}),
  (s)-[math_enrollment:EnrolledIn]->
  (math:Course {course_id: "C005"}),
  (s)-[transfer:TransferredTo]->
  (institution:Institution)
WHERE
  english_enrollment.passed = TRUE
  AND math_enrollment.passed = TRUE
RETURN
  s.student_id,
  institution.institution_name,
  transfer.transfer_term_id,
  transfer.credits_at_transfer,
  transfer.gpa_at_transfer
ORDER BY transfer.credits_at_transfer DESC;


-- 2. Courses most frequently completed by students who transferred.
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`
MATCH
  (s:Student)-[enrollment:EnrolledIn]->(course:Course),
  (s)-[:TransferredTo]->(:Institution)
WHERE enrollment.passed = TRUE
RETURN
  course.course_id,
  course.course_name,
  COUNT(DISTINCT s.student_id) AS transferred_students
GROUP BY course.course_id, course.course_name
ORDER BY transferred_students DESC
LIMIT 15;


-- 3. Support services used by transferred students.
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`
MATCH
  (s:Student)-[:UsedService]->(service:SupportService),
  (s)-[:TransferredTo]->(:Institution)
RETURN
  service.service_name,
  COUNT(DISTINCT s.student_id) AS transferred_students_using_service
GROUP BY service.service_name
ORDER BY transferred_students_using_service DESC;


-- 4. Required courses that a selected student completed.
-- Replace STU00001 with a student identifier returned by query 1.
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`
MATCH
  (student:Student {student_id: "STU00001"})
    -[enrollment:EnrolledIn]->(course:Course)
    <-[:Requires]-(program:Program)
WHERE enrollment.passed = TRUE
RETURN
  student.student_id,
  program.program_name,
  course.course_id,
  course.course_name,
  enrollment.term_id,
  enrollment.final_grade
ORDER BY enrollment.term_id, course.course_id;


-- 5. Course-sequence paths of one to three prerequisite relationships.
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`
MATCH
  (start:Course {course_id: "C004"})
  -[sequence:Precedes]->{1,3}
  (destination:Course)
RETURN
  start.course_name AS starting_course,
  destination.course_name AS reachable_course,
  ARRAY_LENGTH(sequence) AS sequence_length
ORDER BY sequence_length, reachable_course;


-- 6. Relational validation query.
-- This demonstrates why the graph should complement, not replace, ordinary SQL.
WITH student_flags AS (
  SELECT
    s.student_id,
    LOGICAL_OR(su.service_id = "S003") AS used_transfer_center,
    COUNTIF(t.transfer_id IS NOT NULL) > 0 AS transferred
  FROM `pj-test1-499320.student_journey.students` AS s
  LEFT JOIN `pj-test1-499320.student_journey.service_usage` AS su
    USING (student_id)
  LEFT JOIN `pj-test1-499320.student_journey.transfers` AS t
    USING (student_id)
  GROUP BY s.student_id
)
SELECT
  used_transfer_center,
  COUNT(*) AS students,
  AVG(CAST(transferred AS INT64)) AS descriptive_transfer_rate
FROM student_flags
GROUP BY used_transfer_center
ORDER BY used_transfer_center;
