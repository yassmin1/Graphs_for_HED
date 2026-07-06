
-- Replace PROJECT_ID before running.
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`

MATCH
  -- Hop 1: find the student's FINAL declared program (not an earlier, changed one)
  (student:Student)
    -[declaration:DeclaredProgram]->
  (program:Program),

  -- Hop 2: find where that same student later transferred
  (student)
    -[transfer:TransferredTo]->
  (institution:Institution)

-- Only count the program a student ended on, so a student who
-- switched majors twice isn't credited to their abandoned program
WHERE declaration.declaration_status = "Final Program"

RETURN
  program.program_name,
  institution.institution_name,
  COUNT(DISTINCT student.student_id) AS transferred_students,   -- how many students made this exact trip
  ROUND(AVG(transfer.credits_at_transfer), 1) AS average_transfer_credits,
  ROUND(AVG(transfer.gpa_at_transfer), 2) AS average_transfer_gpa

GROUP BY
  program.program_name,
  institution.institution_name

ORDER BY transferred_students DESC
LIMIT 25;
