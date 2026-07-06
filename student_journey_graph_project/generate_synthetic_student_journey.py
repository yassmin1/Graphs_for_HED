import pandas as pd, numpy as np, math, random, os, json, textwrap, statistics
from pathlib import Path

rng = np.random.default_rng(20260702)
random.seed(20260702)

programs = pd.DataFrame([
    ("P001","Business Administration","Transfer","Business"),
    ("P002","Computer Science","Transfer","STEM"),
    ("P003","Engineering","Transfer","STEM"),
    ("P004","Psychology","Transfer","Liberal Arts"),
    ("P005","Nursing","Workforce","Health"),
    ("P006","Cybersecurity","Workforce","STEM"),
    ("P007","Data Analytics","Hybrid","Business/STEM"),
    ("P008","General Studies","Transfer","Liberal Arts"),
], columns=["program_id","program_name","program_type","division"])

courses_data = [
("C001","College Success Seminar","COLL","1001",1,1.0,"Foundation"),
("C002","English Composition I","ENGL","1301",3,2.0,"Gateway"),
("C003","English Composition II","ENGL","1302",3,2.4,"Core"),
("C004","Developmental Mathematics","MATH","0300",3,2.7,"Developmental"),
("C005","College Algebra","MATH","1314",3,3.0,"Gateway"),
("C006","Statistics","MATH","1342",3,3.0,"Core"),
("C007","Calculus I","MATH","2413",4,4.0,"STEM"),
("C008","Calculus II","MATH","2414",4,4.3,"STEM"),
("C009","Federal Government","GOVT","2305",3,2.2,"Core"),
("C010","Texas Government","GOVT","2306",3,2.2,"Core"),
("C011","U.S. History I","HIST","1301",3,2.1,"Core"),
("C012","U.S. History II","HIST","1302",3,2.2,"Core"),
("C013","General Psychology","PSYC","2301",3,2.1,"Core"),
("C014","Introduction to Sociology","SOCI","1301",3,2.0,"Core"),
("C015","Principles of Macroeconomics","ECON","2301",3,2.8,"Business"),
("C016","Principles of Microeconomics","ECON","2302",3,2.8,"Business"),
("C017","Financial Accounting","ACCT","2301",3,3.1,"Business"),
("C018","Managerial Accounting","ACCT","2302",3,3.3,"Business"),
("C019","Programming Fundamentals I","COSC","1436",4,3.5,"Computing"),
("C020","Programming Fundamentals II","COSC","1437",4,3.8,"Computing"),
("C021","Data Structures","COSC","2436",4,4.2,"Computing"),
("C022","Introduction to Engineering","ENGR","1201",2,2.7,"Engineering"),
("C023","Engineering Physics I","PHYS","2425",4,4.3,"Engineering"),
("C024","Anatomy and Physiology I","BIOL","2401",4,4.1,"Health"),
("C025","Anatomy and Physiology II","BIOL","2402",4,4.3,"Health"),
("C026","Microbiology","BIOL","2420",4,4.0,"Health"),
("C027","Networking Fundamentals","ITNW","1325",3,3.0,"Cybersecurity"),
("C028","Network Security","ITNW","1354",3,3.5,"Cybersecurity"),
("C029","Database Fundamentals","ITSE","1345",3,3.1,"Data"),
("C030","Data Visualization","ITSE","2359",3,3.2,"Data"),
("C031","Python for Data Analysis","ITSE","2317",3,3.6,"Data"),
("C032","Speech Communication","SPCH","1311",3,2.0,"Core"),
("C033","Art Appreciation","ARTS","1301",3,2.0,"Elective"),
("C034","Environmental Science","ENVR","1301",3,2.5,"Elective"),
("C035","Introduction to Philosophy","PHIL","1301",3,2.4,"Elective"),
("C036","World Literature","ENGL","2332",3,2.6,"Elective"),
("C037","Spanish I","SPAN","1411",4,2.8,"Elective"),
("C038","Computer Applications","BCIS","1305",3,2.2,"Elective"),
("C039","Nutrition and Wellness","BIOL","1322",3,2.3,"Elective"),
("C040","Introduction to Ethics","PHIL","2306",3,2.5,"Elective"),
]
courses = pd.DataFrame(courses_data, columns=["course_id","course_name","subject","course_number","credits","difficulty","course_group"])

terms = pd.DataFrame([
("2022FA","Fall 2022","2022-08-22","2022-12-16",1),
("2023SP","Spring 2023","2023-01-17","2023-05-12",2),
("2023SU","Summer 2023","2023-06-05","2023-08-04",3),
("2023FA","Fall 2023","2023-08-21","2023-12-15",4),
("2024SP","Spring 2024","2024-01-16","2024-05-10",5),
("2024SU","Summer 2024","2024-06-03","2024-08-02",6),
("2024FA","Fall 2024","2024-08-26","2024-12-13",7),
("2025SP","Spring 2025","2025-01-21","2025-05-16",8),
("2025SU","Summer 2025","2025-06-02","2025-08-01",9),
("2025FA","Fall 2025","2025-08-25","2025-12-12",10),
("2026SP","Spring 2026","2026-01-20","2026-05-15",11),
], columns=["term_id","term_name","start_date","end_date","term_sequence"])

institutions = pd.DataFrame([
("I001","North Valley University","Public University","Regional"),
("I002","Metro State University","Public University","Regional"),
("I003","Lone Star Technical University","Public University","STEM"),
("I004","Central City University","Public University","Urban"),
("I005","St. Anne University","Private University","Private"),
("I006","Riverbend University","Public University","Regional"),
("I007","Western Plains University","Public University","Regional"),
("I008","Online State University","Public University","Online"),
], columns=["institution_id","institution_name","institution_type","institution_group"])

services = pd.DataFrame([
("S001","Academic Advising","Advising"),
("S002","Tutoring Center","Academic Support"),
("S003","Transfer Center","Transfer Support"),
("S004","Career Services","Career Support"),
("S005","Emergency Grant Office","Financial Support"),
], columns=["service_id","service_name","service_category"])

# program course pools
common = ["C001","C002","C003","C005","C006","C009","C010","C011","C012","C013","C014","C032"]
program_pools = {
"P001": common + ["C015","C016","C017","C018","C029","C030"],
"P002": common + ["C007","C008","C019","C020","C021","C029"],
"P003": common + ["C007","C008","C022","C023","C019"],
"P004": common + ["C013","C014","C006","C003","C032"],
"P005": common + ["C024","C025","C026","C013","C006"],
"P006": common + ["C019","C020","C027","C028","C029"],
"P007": common + ["C015","C019","C029","C030","C031","C006"],
"P008": common + ["C015","C016","C013","C014","C032"],
}
elective_pool = ["C033","C034","C035","C036","C037","C038","C039","C040"]
for _program_id in program_pools:
    program_pools[_program_id] = program_pools[_program_id] + elective_pool
# course order rankings for progression
rank = {cid:i for i,cid in enumerate(["C001","C002","C004","C005","C003","C006","C009","C010","C011","C012","C013","C014","C032",
                                      "C015","C016","C017","C018","C019","C020","C021","C022","C007","C008","C023","C024","C025","C026","C027","C028","C029","C030","C031"])}
# prerequisites
prereqs = [
("PR001","C004","C005","Developmental placement pathway"),
("PR002","C002","C003","Composition sequence"),
("PR003","C005","C007","Algebra before calculus"),
("PR004","C007","C008","Calculus sequence"),
("PR005","C019","C020","Programming sequence"),
("PR006","C020","C021","Programming before data structures"),
("PR007","C024","C025","Anatomy sequence"),
("PR008","C027","C028","Networking before security"),
("PR009","C029","C030","Database before visualization"),
]
course_prerequisites = pd.DataFrame(prereqs, columns=["prerequisite_id","source_course_id","destination_course_id","relationship_note"])

# requirements edges
req_rows=[]
rid=1
for pid,pool in program_pools.items():
    # choose program-specific + key common set
    required = []
    for cid in pool:
        if cid in ["C001","C002","C005","C006","C009","C010","C011","C012","C032"] or cid not in common:
            required.append(cid)
    for cid in dict.fromkeys(required):
        req_rows.append((f"R{rid:04d}",pid,cid,"Required" if cid not in ["C013","C014","C015","C016"] else "Recommended"))
        rid+=1
program_requirements=pd.DataFrame(req_rows,columns=["requirement_id","program_id","course_id","requirement_type"])

# helpers
def sigmoid(x): return 1/(1+math.exp(-x))
entry_terms = ["2022FA","2023SP","2023FA","2024SP","2024FA","2025SP","2025FA"]
entry_probs = np.array([0.16,0.08,0.20,0.10,0.20,0.08,0.18]); entry_probs/=entry_probs.sum()

student_rows=[]
student_latent={}
for i in range(1,1501):
    sid=f"STU{i:05d}"
    entry=rng.choice(entry_terms,p=entry_probs)
    age_band=rng.choice(["17-19","20-24","25-34","35+"],p=[0.44,0.28,0.20,0.08])
    first_gen=bool(rng.random()<0.48)
    pell=bool(rng.random()<0.56)
    ft=bool(rng.random()< (0.67 if age_band in ["17-19","20-24"] else 0.38))
    modality=rng.choice(["Mostly In Person","Mixed","Mostly Online"],p=[0.45,0.37,0.18] if age_band!="35+" else [0.25,0.35,0.40])
    pid=rng.choice(programs.program_id,p=[0.16,0.15,0.11,0.10,0.12,0.11,0.10,0.15])
    prep=float(np.clip(rng.normal(0,0.9) - 0.15*first_gen, -2.2,2.2))
    engagement=float(np.clip(rng.normal(0,0.9)+0.2*ft, -2.2,2.2))
    work_load=rng.choice(["Low","Moderate","High"],p=[0.25,0.50,0.25] if ft else [0.15,0.45,0.40])
    dev_math=bool(rng.random() < sigmoid(-0.15-0.9*prep))
    student_rows.append([sid,entry,age_band,first_gen,pell,ft,modality,pid,work_load,dev_math])
    student_latent[sid]=(prep,engagement)
students=pd.DataFrame(student_rows,columns=["student_id","entry_term_id","entry_age_band","first_generation","pell_eligible","full_time_at_entry","modality_preference","initial_program_id","work_commitment","developmental_math_start"])

# map data
course_map=courses.set_index("course_id").to_dict("index")
term_seq=terms.set_index("term_id")["term_sequence"].to_dict()
term_ids=terms.term_id.tolist()

enroll_rows=[]
term_rows=[]
service_rows=[]
program_hist=[]
award_rows=[]
transfer_rows=[]
eid=tid=usid=did=aid=xid=1

for row in students.itertuples(index=False):
    sid=row.student_id
    prep, engagement=student_latent[sid]
    current_program=row.initial_program_id
    entry_idx=term_ids.index(row.entry_term_id)
    completed=set()
    attempted=set()
    cum_credits=0.0
    quality_points=0.0
    gpa_credits=0.0
    ever_advising=0
    ever_tutoring=0
    ever_transfer_center=0
    failed_gateway=False
    active=True
    transfer_done=False
    award_done=False
    declaration_start=row.entry_term_id
    # max terms available
    available=term_ids[entry_idx:]
    # maybe program change after 2+ terms
    change_term=None
    if len(available)>=4 and rng.random()<0.18:
        change_term=available[int(rng.integers(2,min(5,len(available))))]
    for local_index,term in enumerate(available):
        if not active: break
        # skip many summers; if skip summer don't count as stopout
        is_summer=term.endswith("SU")
        if is_summer and rng.random() < (0.68 if row.full_time_at_entry else 0.78):
            continue
        if change_term==term:
            old=current_program
            candidates=[p for p in programs.program_id if p!=old]
            current_program=rng.choice(candidates)
            program_hist.append((f"D{did:06d}",sid,old,declaration_start,term,"Changed Program"))
            did+=1
            declaration_start=term
        # services early term
        p_adv=sigmoid(-0.25 + 0.45*row.first_generation + 0.25*row.pell_eligible + 0.25*(engagement<0) + 0.20*local_index)
        adv_visits=int(rng.poisson(0.8 if rng.random()<p_adv else 0.15))
        if adv_visits>0:
            ever_advising+=adv_visits
            for v in range(adv_visits):
                service_rows.append((f"U{usid:07d}",sid,"S001",term,int(rng.integers(20,61)),"Academic planning"))
                usid+=1
        # transfer center for transfer programs after credits
        p_tc=sigmoid(-3.0 + 0.055*cum_credits + 0.35*ever_advising)
        if programs.set_index("program_id").loc[current_program,"program_type"] in ["Transfer","Hybrid"] and rng.random()<p_tc:
            ever_transfer_center+=1
            service_rows.append((f"U{usid:07d}",sid,"S003",term,int(rng.integers(25,61)),"Transfer planning"))
            usid+=1
        # emergency grants more likely pell/high work
        if row.pell_eligible and rng.random() < (0.04 + 0.05*(row.work_commitment=="High")):
            service_rows.append((f"U{usid:07d}",sid,"S005",term,int(rng.integers(15,46)),"Emergency aid consultation"))
            usid+=1

        n_courses=int(rng.choice([2,3,4,5],p=[0.36,0.39,0.20,0.05] if not row.full_time_at_entry else [0.08,0.27,0.43,0.22]))
        pool=list(dict.fromkeys(program_pools[current_program]))
        # developmental path
        if row.developmental_math_start and "C004" not in attempted and local_index<=1:
            candidates=["C004"]
        else:
            candidates=[]
        # prioritize success seminar and English first
        priority=[]
        if local_index==0 and "C001" not in attempted: priority.append("C001")
        if local_index<=1 and "C002" not in attempted: priority.append("C002")
        if "C004" in completed and "C005" not in attempted: priority.append("C005")
        elif not row.developmental_math_start and local_index<=1 and "C005" not in attempted: priority.append("C005")
        # prereq eligibility
        prereq_map={"C003":"C002","C005":"C004" if row.developmental_math_start else None,"C007":"C005","C008":"C007",
                    "C020":"C019","C021":"C020","C025":"C024","C028":"C027","C030":"C029"}
        eligible=[]
        for cid in pool:
            if cid in attempted: continue
            pr=prereq_map.get(cid)
            if pr and pr not in completed: continue
            eligible.append(cid)
        selected=[]
        for cid in candidates+priority:
            if cid in eligible or cid=="C004":
                if cid not in selected: selected.append(cid)
        remaining=[c for c in sorted(eligible,key=lambda x:rank.get(x,99)) if c not in selected]
        # weighted toward lower rank early
        while len(selected)<n_courses and remaining:
            weights=np.array([1/(1+max(0,rank.get(c,99)-local_index*4)) for c in remaining],dtype=float)
            weights/=weights.sum()
            pick=rng.choice(remaining,p=weights)
            selected.append(pick); remaining.remove(pick)
        # if no eligible, stop
        if not selected:
            break
        term_attempted=0
        term_earned=0
        term_qp=0
        term_gpa_cred=0
        term_failed=0
        for cid in selected:
            c=course_map[cid]
            attempted.add(cid)
            # modality
            mode = rng.choice(["In Person","Hybrid","Online"],p=[0.68,0.22,0.10] if row.modality_preference=="Mostly In Person" else ([0.20,0.50,0.30] if row.modality_preference=="Mixed" else [0.08,0.27,0.65]))
            # support tutoring probability for difficult courses
            if c["difficulty"]>=3 and rng.random()<sigmoid(-1.2 + 0.45*(prep<0)+0.25*ever_advising):
                ever_tutoring+=1
                service_rows.append((f"U{usid:07d}",sid,"S002",term,int(rng.integers(30,91)),f"Tutoring related to {cid}"))
                usid+=1
                tutor_bonus=0.30
            else:
                tutor_bonus=0
            load_penalty=0.35*(row.work_commitment=="High")+0.12*(n_courses>=5)
            online_mismatch=0.28*(mode=="Online" and row.modality_preference=="Mostly In Person")
            score = 3.15 + 0.72*prep + 0.28*engagement + 0.20*ever_advising + tutor_bonus - 0.24*c["difficulty"] - load_penalty - online_mismatch + rng.normal(0,0.75)
            # grade cutoffs
            if score>=3.2: grade="A"; gp=4
            elif score>=2.45: grade="B"; gp=3
            elif score>=1.75: grade="C"; gp=2
            elif score>=1.15: grade="D"; gp=1
            else:
                grade=rng.choice(["F","W"],p=[0.67,0.33]); gp=0
            passed=grade in ["A","B","C"]
            completed_course=grade!="W"
            credits=c["credits"]
            term_attempted+=credits
            if passed:
                term_earned+=credits; completed.add(cid)
            if grade!="W":
                term_qp+=gp*credits; term_gpa_cred+=credits
            if not passed: term_failed+=1
            if cid in ["C002","C004","C005"] and not passed: failed_gateway=True
            enroll_rows.append((f"E{eid:08d}",sid,cid,term,current_program,credits,grade,passed,completed_course,mode))
            eid+=1
        cum_credits += term_earned
        quality_points += term_qp
        gpa_credits += term_gpa_cred
        cum_gpa = quality_points/gpa_credits if gpa_credits else 0
        term_rows.append((f"T{tid:07d}",sid,term,current_program,term_attempted,term_earned,round(cum_credits,1),round(cum_gpa,2),
                          "Full Time" if term_attempted>=12 else "Part Time"))
        tid+=1

        # Award logic: workforce certificates can be earned after 30 credits;
        # associate degrees require at least 60 credits.
        ptype=programs.set_index("program_id").loc[current_program,"program_type"]
        eligible_certificate = ptype in ["Workforce", "Hybrid"] and cum_credits >= 30
        eligible_associate = cum_credits >= 60
        if not award_done and (eligible_certificate or eligible_associate):
            if eligible_associate:
                award_type = "Associate Degree"
                award_prob = 0.70
            else:
                award_type = "Certificate"
                award_prob = sigmoid(-3.3 + 0.095*cum_credits + 0.45*(cum_gpa>=2.5) + 0.20*ever_advising)
            if rng.random() < award_prob:
                award_rows.append((f"A{aid:06d}",sid,current_program,term,award_type,round(cum_credits,1),round(cum_gpa,2)))
                aid+=1; award_done=True
        # transfer probability
        gateway_complete=("C002" in completed and "C005" in completed)
        if not transfer_done and ptype in ["Transfer","Hybrid"] and cum_credits>=15:
            lp=-4.65+0.07*cum_credits+0.55*(cum_gpa>=2.75)+0.75*ever_transfer_center+0.45*gateway_complete+0.25*ever_advising
            if rng.random()<sigmoid(lp):
                # choose institution based on program
                if current_program in ["P002","P003","P007"]:
                    inst=rng.choice(["I003","I002","I004","I008"],p=[0.40,0.25,0.20,0.15])
                else:
                    inst=rng.choice(institutions.institution_id)
                transfer_rows.append((f"X{xid:06d}",sid,inst,term,current_program,round(cum_credits,1),round(cum_gpa,2),
                                      "Verified Enrollment", bool(award_done)))
                xid+=1; transfer_done=True; active=False
                break
        # persistence to next non-summer term
        success_rate=term_earned/term_attempted if term_attempted else 0
        lp_continue=1.65+0.55*engagement+0.35*row.full_time_at_entry+0.22*ever_advising+0.55*success_rate-0.50*(term_failed>=2)-0.35*(row.work_commitment=="High")
        # completion can end enrollment
        if award_done and rng.random()<0.62:
            active=False; break
        if rng.random()>sigmoid(lp_continue):
            active=False; break
    # close program history
    last_term = term_rows[-1][2] if term_rows and term_rows[-1][1]==sid else row.entry_term_id
    program_hist.append((f"D{did:06d}",sid,current_program,declaration_start,last_term,"Final Program"))
    did+=1

enrollments=pd.DataFrame(enroll_rows,columns=["enrollment_id","student_id","course_id","term_id","program_id","credits_attempted","final_grade","passed","course_completed","instruction_mode"])
student_terms=pd.DataFrame(term_rows,columns=["student_term_id","student_id","term_id","program_id","credits_attempted","credits_earned","cumulative_credits","cumulative_gpa","enrollment_intensity"])
service_usage=pd.DataFrame(service_rows,columns=["service_use_id","student_id","service_id","term_id","minutes","visit_reason"])
program_history=pd.DataFrame(program_hist,columns=["declaration_id","student_id","program_id","start_term_id","end_term_id","declaration_status"])
awards=pd.DataFrame(award_rows,columns=["award_id","student_id","program_id","award_term_id","award_type","credits_at_award","gpa_at_award"])
transfers=pd.DataFrame(transfer_rows,columns=["transfer_id","student_id","institution_id","transfer_term_id","program_id_at_transfer","credits_at_transfer","gpa_at_transfer","transfer_status","credential_before_transfer"])

# derive final outcome
award_students=set(awards.student_id)
transfer_students=set(transfers.student_id)
last_term_by=student_terms.groupby("student_id")["term_id"].last().to_dict()
outcomes=[]
for sid in students.student_id:
    a=sid in award_students;t=sid in transfer_students
    if a and t:o="Credentialed and Transferred"
    elif t:o="Transferred"
    elif a:o="Credentialed"
    elif last_term_by.get(sid)=="2026SP":o="Active"
    else:o="Stopped Out"
    outcomes.append(o)
students["final_outcome"]=outcomes

[len(df) for df in [students,enrollments,student_terms,service_usage,program_history,awards,transfers]]

if __name__ == "__main__":
    from pathlib import Path

    output_dir = Path(__file__).resolve().parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_tables = {
        "students": students,
        "programs": programs,
        "courses": courses,
        "terms": terms,
        "institutions": institutions,
        "services": services,
        "enrollments": enrollments,
        "student_terms": student_terms,
        "service_usage": service_usage,
        "program_history": program_history,
        "awards": awards,
        "transfers": transfers,
        "program_requirements": program_requirements,
        "course_prerequisites": course_prerequisites,
    }
    for table_name, table in generated_tables.items():
        table.to_csv(output_dir / f"{table_name}.csv", index=False)

    print(f"Synthetic data written to {output_dir}")
    for table_name, table in generated_tables.items():
        print(f"{table_name}: {len(table):,} rows")
