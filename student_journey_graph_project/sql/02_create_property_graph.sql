-- Replace PROJECT_ID before running.
-- BigQuery Graph was a Preview feature when this project was prepared.
-- Keep the graph and all referenced tables in the same BigQuery location.

CREATE OR REPLACE PROPERTY GRAPH
  `pj-test1-499320.student_journey.StudentJourneyGraph`
NODE TABLES (
  `pj-test1-499320.student_journey.students` AS Students
    KEY (student_id)
    LABEL Student PROPERTIES ALL COLUMNS,

  `pj-test1-499320.student_journey.courses` AS Courses
    KEY (course_id)
    LABEL Course PROPERTIES ALL COLUMNS,

  `pj-test1-499320.student_journey.programs` AS Programs
    KEY (program_id)
    LABEL Program PROPERTIES ALL COLUMNS,

  `pj-test1-499320.student_journey.terms` AS Terms
    KEY (term_id)
    LABEL Term PROPERTIES ALL COLUMNS,

  `pj-test1-499320.student_journey.institutions` AS Institutions
    KEY (institution_id)
    LABEL Institution PROPERTIES ALL COLUMNS,

  `pj-test1-499320.student_journey.services` AS Services
    KEY (service_id)
    LABEL SupportService PROPERTIES ALL COLUMNS
)
EDGE TABLES (
  `pj-test1-499320.student_journey.enrollments` AS Enrollments
    KEY (enrollment_id)
    SOURCE KEY (student_id) REFERENCES Students (student_id)
    DESTINATION KEY (course_id) REFERENCES Courses (course_id)
    LABEL EnrolledIn PROPERTIES ALL COLUMNS,

  `pj-test1-499320.student_journey.student_terms` AS StudentTerms
    KEY (student_term_id)
    SOURCE KEY (student_id) REFERENCES Students (student_id)
    DESTINATION KEY (term_id) REFERENCES Terms (term_id)
    LABEL AttendedTerm PROPERTIES ALL COLUMNS,

  `pj-test1-499320.student_journey.program_history` AS ProgramHistory
    KEY (declaration_id)
    SOURCE KEY (student_id) REFERENCES Students (student_id)
    DESTINATION KEY (program_id) REFERENCES Programs (program_id)
    LABEL DeclaredProgram PROPERTIES ALL COLUMNS,

  `pj-test1-499320.student_journey.service_usage` AS ServiceUsage
    KEY (service_use_id)
    SOURCE KEY (student_id) REFERENCES Students (student_id)
    DESTINATION KEY (service_id) REFERENCES Services (service_id)
    LABEL UsedService PROPERTIES ALL COLUMNS,

  `pj-test1-499320.student_journey.awards` AS Awards
    KEY (award_id)
    SOURCE KEY (student_id) REFERENCES Students (student_id)
    DESTINATION KEY (program_id) REFERENCES Programs (program_id)
    LABEL EarnedAward PROPERTIES ALL COLUMNS,

  `pj-test1-499320.student_journey.transfers` AS Transfers
    KEY (transfer_id)
    SOURCE KEY (student_id) REFERENCES Students (student_id)
    DESTINATION KEY (institution_id) REFERENCES Institutions (institution_id)
    LABEL TransferredTo PROPERTIES ALL COLUMNS,

  `pj-test1-499320.student_journey.program_requirements` AS ProgramRequirements
    KEY (requirement_id)
    SOURCE KEY (program_id) REFERENCES Programs (program_id)
    DESTINATION KEY (course_id) REFERENCES Courses (course_id)
    LABEL Requires PROPERTIES ALL COLUMNS,

  `pj-test1-499320.student_journey.course_prerequisites` AS CoursePrerequisites
    KEY (prerequisite_id)
    SOURCE KEY (source_course_id) REFERENCES Courses (course_id)
    DESTINATION KEY (destination_course_id) REFERENCES Courses (course_id)
    LABEL Precedes PROPERTIES ALL COLUMNS
);
