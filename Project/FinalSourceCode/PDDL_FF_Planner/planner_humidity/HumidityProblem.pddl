
(define (problem Health)
(:domain Employee)
(:objects 
r1 - user 
l1 - motor)
(:init 
(stop l1)
;hum
(= (hum_threshold) 29)
(= (hum r1) 32.0 )
)
(:goal (and (run-motor))
)
)