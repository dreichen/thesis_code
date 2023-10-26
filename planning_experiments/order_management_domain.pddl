(define (domain order-management-task)

;remove requirements that are not needed
(:requirements :strips :fluents :durative-actions :typing :disjunctive-preconditions :conditional-effects :negative-preconditions :duration-inequalities :equality)

(:types
    Entity Step
    Configuration Company Contact Order Role - Entity
    AccountingClerk Configurator - Role
)

(:constants
    addOrderDocument - Step
    fillOrder - Step
    forwardOrder - Step
    uploadOrderConfirmation - Step
    acceptOrderConfirmation - Step
    uploadInvoice - Step
    confirmInvoices - Step
    payProvision - Step
    completeOrder - Step
    cancelOrder - Step
)

(:predicates
    ;; Order predicates -> entity references
    (clerk ?o - Order ?a - AccountingClerk)
    (customer ?o - Order ?c - Company)
    (contact ?o - Order ?c - Contact)
    (brand ?o - Order ?c - Company)

    ;; Task Predicates
    (reachedFinalStep)
    (canceled)
    (supplierPoNumberProvided ?o - Order ?s - Step)
    (orderDocumentProvided ?o - Order ?s - Step)
    (orderFilled ?o - Order ?s - Step)
    (orderForwarded ?o - Order ?s - Step)
    (orderConfirmationProvided ?o - Order ?s - Step)
    (poNumberProvided ?o - Order ?s - Step)
    (quantityProvided ?o - Order ?s - Step)
    (amountProvided ?o - Order ?s - Step)
    ;; General predicates
    (stepReached ?s - Step)

)

;(:functions
;    ;; general
;    (DateTimeNow)
;    (DateNow)
;    ;; Order Properties
;    (provisionClerk ?o - Order) ; number
;    (deadline ?o - Order) ; date -> timestamp
;    (paymentGoal ?o - Order) ; date -> timestamp
;    (poNumber ?o - Order) ; number
;    (amount ?o - Order) ; number
;    (quantity ?o - Order) ; number
;    (discount ?o - Order) ; number
;    (provision ?o - Order) ; number
;
;
;)

    (:durative-action addOrderDocument
        :parameters
            (?o - Order)

        :duration
            (= ?duration 1)

        :condition
	        (and
	            (at start (not (canceled)))
	        )

        :effect
	        (and
	            (at end (supplierPoNumberProvided ?o addOrderDocument))
	            (at end (orderDocumentProvided ?o addOrderDocument))
            )
	)

    (:durative-action fillOrder
        :parameters
            (?o - Order)

        :duration
            (= ?duration 1)

        :condition
	        (and
	            (at start (not (canceled)))
	            (at start (supplierPoNumberProvided ?o addOrderDocument))
	            (at start (orderDocumentProvided ?o addOrderDocument))
	        )

        :effect
	        (and
	            (at end (orderFilled ?o fillOrder))
                )
	)

    (:durative-action forwardOrder
        :parameters
            (?o - Order)

        :duration
            (= ?duration 1)

        :condition
	        (and
	            (at start (not (canceled)))
	            (at start (orderFilled ?o fillOrder))
	        )

        :effect
	        (and
	            (at end (orderForwarded ?o forwardOrder))
                )
	)

    (:durative-action uploadOrderConfirmation
        :parameters
            (?o - Order)

        :duration
            (= ?duration 1)

        :condition
	        (and
	            (at start (not (canceled)))
	            (at start (orderFilled ?o fillOrder))
	        )

        :effect
	        (and
	            (at end (orderConfirmationProvided ?o uploadOrderConfirmation))
	            (at end (poNumberProvided ?o uploadOrderConfirmation))
	            (at end (amountProvided ?o uploadOrderConfirmation))
	            (at end (quantityProvided ?o uploadOrderConfirmation))
	            (at end (reachedFinalStep))
                )
	)
)