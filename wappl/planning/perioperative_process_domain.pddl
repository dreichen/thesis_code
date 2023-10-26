(define (domain perioperative-process)

    ;remove requirements that are not needed
    (:requirements :strips :durative-actions :typing :disjunctive-preconditions :fluents :negative-preconditions :equality)

    (:types
    	humanResource nonhumanResource patient - object
        doctor nurse - humanResource 
    	room equipment - nonhumanResource
    )
        
    (:predicates
        (available ?agent - object)
        (busy ?agent - object)
        (patientIn ?patient - patient ?room - room)
        (empty ?room - room)
        (using ?agent - object ?equipment - equipment)
        (surgeryDone ?patient - patient)
		(patientAtWard ?patient - patient)
		(diagnosticsDone ?patient - patient)
    )

    (:functions
        (workHours ?h - humanResource)
        (dailyWorkHours ?h - humanResource)
    )
    
	(:durative-action pauseNurse
        :parameters
            (?h - nurse)

        :duration
            (= ?duration 1)

        :condition
	        (and
	            (at start (available ?h))
	            (at start (>= (workHours ?h) 12))
	        	(at start (<= (dailyWorkHours ?h) 24))
	        )

        :effect
	        (and
	            (at start (not (available ?h)))
	            (at end (available ?h))
	            (at end (assign (workHours ?h) 0))
	            (at end (increase (dailyWorkHours ?h) 12))
            )
	)

	(:durative-action shiftOverNurse
        :parameters
            (?h - nurse)

        :duration
            (= ?duration 24)

        :condition
	        (and
	            (at start (available ?h))
	        	(at start (>= (dailyWorkHours ?h) 24))
	        )

        :effect
	        (and
	            (at start (not (available ?h)))
	            (at end (available ?h))
	            (at end (assign (workHours ?h) 0))
	            (at end (assign (dailyWorkHours ?h) 0))
            )
	)

	(:durative-action pauseDoctor
        :parameters
            (?h - doctor)

        :duration
            (= ?duration 1)

        :condition
	        (and
	            (at start (available ?h))
	            (at start (>= (workHours ?h) 12))
	        	(at start (<= (dailyWorkHours ?h) 20))
	        )

        :effect
	        (and
	            (at start (not (available ?h)))
	            (at end (available ?h))
	            (at end (assign (workHours ?h) 0))
	            (at end (increase (dailyWorkHours ?h) 20))
            )
	)

	(:durative-action shiftOverDoctor
        :parameters
            (?h - doctor)

        :duration
            (= ?duration 24)

        :condition
	        (and
	            (at start (available ?h))
	        	(at start (>= (dailyWorkHours ?h) 20))
	        )

        :effect
	        (and
	            (at start (not (available ?h)))
	            (at end (available ?h))
	            (at end (assign (workHours ?h) 0))
	            (at end (assign (dailyWorkHours ?h) 0))
            )
	)

	(:durative-action admitAtWard
        :parameters
            (?patient - patient ?nurse - nurse)

        :duration
            (= ?duration 1)

        :condition
	        (and
	            (at start (not (busy ?patient)))
	            (at start (available ?nurse))
	            (at start (not (patientAtWard ?patient)))
	            (at start (< (dailyWorkHours ?nurse) 25))
	            (at start (< (workHours ?nurse) 13))
	            (at start (not (surgeryDone ?patient)))
	        )

        :effect
	        (and
	            (at start (not (available ?nurse)))
	            (at start (busy ?patient))
	            (at end (not (busy ?patient)))
	            (at end (patientAtWard ?patient))
	            (at end (available ?nurse))
	            (at start (increase (workHours ?nurse) 1))
            )
	)
	
		
    (:durative-action doDiagnostics
        :parameters
            (?patient - patient ?nurse - nurse ?ct - equipment)

        :duration
            (= ?duration 2)

        :condition
	        (and
	            (at start (not (busy ?patient)))
	            (at start (not (diagnosticsDone ?patient)))
	            (at start (available ?nurse))
	            (at start (patientAtWard ?patient))
	            (at start (available ?ct))
	            (at start (< (dailyWorkHours ?nurse) 25))
	            (at start (< (workHours ?nurse) 13))
	        )

        :effect
	        (and
	            (at start (not (available ?nurse)))
	            (at start (not (available ?ct)))
	            (at start (busy ?patient))
	            (at end (not (busy ?patient)))
	            (at end (available ?nurse))
	            (at end (available ?ct))
	            (at start (diagnosticsDone ?patient))
	            (at start (increase (workHours ?nurse) 2))
	            
            )
	)
    
	(:durative-action enterOR
        :parameters
            (?patient - patient ?room - room ?nurse - nurse)

        :duration
            (= ?duration 1)

        :condition
	        (and
	            (at start (not (busy ?patient)))
	            (at start (available ?nurse))
	            (at start (patientAtWard ?patient))
	            (at start (empty ?room))
	            (at start (diagnosticsDone ?patient))
	            (at start (not (patientIn ?patient ?room)))
	            (at start (< (dailyWorkHours ?nurse) 25))
	            (at start (< (workHours ?nurse) 13))
				
	        )

        :effect
	        (and
	            (at start (not (available ?nurse)))
	            (at start (not (empty ?room)))
	            (at start (patientIn ?patient ?room))
	            
	            (at end (increase (workHours ?nurse) 1))
	            (at end (not (patientAtWard ?patient)))
	            (at end (available ?nurse))

            )
	)

    (:durative-action doSurgery
        :parameters
            (?patient - patient ?doctor - doctor ?nurse - nurse ?room - room ?equipment - equipment)

        :duration
            (= ?duration 8)

        :condition
	        (and 
	            (at start (not (busy ?patient) ))
	            (at start (available ?doctor) )
	            (at start (available ?nurse))
	            (at start (patientIn ?patient ?room) )
	            (at start (not (patientAtWard ?patient) ))
	            (at start (not (using ?doctor ?equipment)))
	            (at start (< (dailyWorkHours ?nurse) 25))
	            (at start (< (workHours ?nurse) 13))
	            (at start (< (workHours ?doctor) 13))
	            (at start (< (dailyWorkHours ?doctor) 20))
	        )

        :effect
	        (and 
	            (at start (using ?doctor ?equipment))
	            (at start (not (available ?doctor)))
	            (at start (not (available ?nurse)))
	            (at start (busy ?patient))
	            (at end (not (busy ?patient)))
	            (at end (not (using ?doctor ?equipment)))
	            (at end (available ?doctor))
	            (at end (available ?nurse))
	            (at end (not (busy ?patient)))
	            (at end (surgeryDone ?patient))
	            (at end (increase (workHours ?nurse) 8))
	            (at end (increase (workHours ?doctor) 8))
	        )
	)
    
    (:durative-action leaveORAndReadmitAtWard
        :parameters
            (?patient - patient ?room - room ?nurse - nurse)

        :duration
            (= ?duration 1)

        :condition
	        (and
	            (at start (not (busy ?patient)))
	            (at start (available ?nurse))
	            (at start (not (patientAtWard ?patient)))
	            (at start (patientIn ?patient ?room))
	            (at start (< (dailyWorkHours ?nurse) 25))
	            (at start (< (workHours ?nurse) 13))
	        )

        :effect
	        (and
	            (at start (not (available ?nurse)))
	            (at start (busy ?patient))
	            (at end (patientAtWard ?patient))
	            (at end (available ?nurse))
	            (at end (not (patientIn ?patient ?room)))
	            (at end (empty ?room))
	            (at end (not (busy ?patient)))
	            (at start (increase (workHours ?nurse) 1))
            )
	)
)