(define (problem perioperative-process-prob) (:domain perioperative-process)
(:objects 
    d1 - doctor
    d2 - doctor
    n1 - nurse
    n2 - nurse
    p1 - patient
    p2 - patient
    p3 - patient
    p4 - patient
    r1 - room
    r2 - room
    ct1 - equipment
    ct2 - equipment
)

(:init
    (available d1)
    (available d2)
    (available n1)
    (available n2)
    (= (dailyWorkHours n1) 0)
    (= (dailyWorkHours n2) 0)
    (= (workHours n1) 0)
    (= (workHours n2) 0)
    (= (dailyWorkHours d1) 0)
    (= (dailyWorkHours d2) 0)
    (= (workHours d1) 0)
    (= (workHours d2) 0)
    (available ct1)
    (available ct2)
    (empty r1)
    (empty r2)
)

(:goal (and
    (surgeryDone p1)
    (surgeryDone p2)
    (surgeryDone p3)
    (surgeryDone p4)
    (patientAtWard p1)
    (patientAtWard p2)
    (patientAtWard p3)
    (patientAtWard p4)

))
)