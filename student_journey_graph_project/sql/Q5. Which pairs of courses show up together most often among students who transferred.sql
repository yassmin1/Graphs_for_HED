-- Replace PROJECT_ID before running.
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`

MATCH
  -- The same student enrolled in course 1...
  (student:Student)
    -[enrollment1:EnrolledIn]->
  (course1:Course),

  -- ...and also enrolled in course 2...
  (student)
    -[enrollment2:EnrolledIn]->
  (course2:Course),

  -- ...and also transferred somewhere (destination not needed here, so left unnamed)
  (student)
    -[:TransferredTo]->
  (:Institution)

WHERE
  enrollment1.passed = TRUE
  AND enrollment2.passed = TRUE
  AND course1.course_id < course2.course_id                   -- avoid double-counting the pair in both orders

RETURN
  course1.course_name AS first_course,
  course2.course_name AS second_course,
  COUNT(DISTINCT student.student_id) AS transferred_students

GROUP BY
  course1.course_name,
  course2.course_name

ORDER BY transferred_students DESC
LIMIT 30;
