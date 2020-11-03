(define (domain Employee)
  (:requirements 
    :strips 
    :typing 
    :negative-preconditions 
    :disjunctive-preconditions 
    :fluents
  )
  (:types 
   user led - object
  )
  
  (:predicates
     (on-led)
     (off ?l - led)
   )

   (:functions
	 (pos ?r - user)
     (pos_threshold)
   )

  ;Flex value if greater than a certain threshold take action posture_sensing
   
  (:action posture_sensing
      :parameters (?l - led ?r - user)
      :precondition (and (off ?l) (>(pos ?r) (pos_threshold)))
      :effect (and(not(off ?l)) (on-led))
   )
   
 )
