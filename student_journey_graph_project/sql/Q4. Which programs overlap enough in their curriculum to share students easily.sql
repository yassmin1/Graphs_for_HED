-- Replace PROJECT_ID before running.
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`

MATCH
  -- Program 1 requires a course...
  (program1:Program)
    -[:Requires]->
  (course:Course)
    -- ...and the SAME course is required by program 2 (edge direction reversed)
    <-[:Requires]-
  (program2:Program)

-- Avoid counting each pair twice (A,B and B,A) and avoid comparing a program to itself
WHERE program1.program_id < program2.program_id

RETURN
  program1.program_name AS first_program,
  program2.program_name AS second_program,
  COUNT(DISTINCT course.course_id) AS shared_required_courses,
  ARRAY_AGG(
    DISTINCT course.course_name
    ORDER BY course.course_name
  ) AS shared_courses                                          -- lists exactly which courses overlap

GROUP BY
  program1.program_name,
  program2.program_name

ORDER BY shared_required_courses DESC;
