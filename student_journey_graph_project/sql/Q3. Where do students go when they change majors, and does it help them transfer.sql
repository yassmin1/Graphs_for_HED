-- Replace PROJECT_ID before running.
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`

MATCH
  -- The program the student declared before changing
  (student:Student)
    -[old_declaration:DeclaredProgram]->
  (old_program:Program),

  -- The program the same student ended on
  (student)
    -[final_declaration:DeclaredProgram]->
  (final_program:Program)

WHERE
  old_declaration.declaration_status = "Changed Program"
  AND final_declaration.declaration_status = "Final Program"
  AND old_program.program_id <> final_program.program_id      -- exclude students who "changed" into the same program

RETURN
  old_program.program_name AS previous_program,
  final_program.program_name AS final_program,
  COUNT(DISTINCT student.student_id) AS students_changing_program,

  -- Count, within this same group, how many eventually transferred
  COUNT(
    DISTINCT IF(
      student.final_outcome IN (
        "Transferred",
        "Credentialed and Transferred"
      ),
      student.student_id,
      NULL
    )
  ) AS students_later_transferred

GROUP BY
  old_program.program_name,
  final_program.program_name

ORDER BY students_changing_program DESC;
