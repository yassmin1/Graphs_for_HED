-- Replace PROJECT_ID before running.
GRAPH `pj-test1-499320.student_journey.StudentJourneyGraph`

MATCH
  (student:Student)
    -[transfer:TransferredTo]->
  (institution:Institution)

RETURN
  institution.institution_name,
  institution.institution_group,
  COUNT(DISTINCT student.student_id) AS transferred_students,
  ROUND(AVG(transfer.credits_at_transfer), 1) AS average_credits,
  ROUND(AVG(transfer.gpa_at_transfer), 2) AS average_gpa,
  ROUND(
    100 * AVG(CAST(transfer.credential_before_transfer AS INT64)),
    1
  ) AS percent_credentialed_before_transfer

GROUP BY
  institution.institution_name,
  institution.institution_group

ORDER BY transferred_students DESC;
