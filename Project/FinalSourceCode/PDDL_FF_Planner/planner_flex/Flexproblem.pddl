
(define (problem Health)
(:domain Employee)
(:objects 
r1 - user 
l1 - led)
(:init 
(off l1)
;pos
(= (pos_threshold) 100)
(= (pos r1) 131 )
)
(:goal (and (on-led))
)
)