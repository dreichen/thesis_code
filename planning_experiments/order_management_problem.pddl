(define (problem order-management-task-prob) (:domain order-management-task)
(:objects 
    order - Order
)

(:init
    
)

(:goal (and
    (not canceled)
    (orderFilled order fillOrder)
))

;un-comment the following line if metric is needed
;(:metric minimize (???))
)