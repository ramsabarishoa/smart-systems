(define (domain Employee)
  (:requirements 
    :strips 
    :typing 
    :negative-preconditions 
    :disjunctive-preconditions 
    :fluents
  )
  (:types 
   user  motor - object
  )
  
  (:predicates
     (run-motor)
     (stop ?h - motor)
   )

   (:functions
     (hum ?r - user)
     (hum_threshold)
   )

  ;Humidity value if greater than a certain threshold take action temp_humidity_sensing
  
  (:action temp_humidity_sensing
      :parameters (?h - motor ?r - user)
      :precondition (and (stop ?h) (>(hum ?r) (hum_threshold)))
      :effect (and (not(stop ?h)) (run-motor))
   )
   
 )
