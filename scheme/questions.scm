(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))

; Some utility functions that you may find useful to implement

(define (zip pairs)
  (list (map car pairs) (map cadr pairs))) ; use the built-in function map !


;; Problem 15
;; Returns a list of two-element lists
(define (enumerate s)
  ; BEGIN PROBLEM 15
  (define (helper s index) ;index is used to mark the original index
    (cond ((null? s) nil) 
      (else (cons (cons index (cons (car s) nil)) (helper (cdr s) (+ index 1))))))
  (helper s 0))
  ; END PROBLEM 15

;; Problem 16

;; Merge two lists LIST1 and LIST2 according to COMP and return
;; the merged lists.
(define (merge comp list1 list2)
  ; BEGIN PROBLEM 16
  (cond ;((and (null? list1) (null? list2)) nil) ;base case 0
    ((null? list1) list2)  ; base case 1
    ((null? list2) list1)  ; base case 2
    ((comp (car list1) (car list2)) (cons (car list1) (merge comp (cdr list1) list2)))
    ((comp (car list2) (car list1)) (cons (car list2) (merge comp list1 (cdr list2))))
    (else (cons (car list1) (merge comp (cdr list1) (cdr list2)))))
  )
  ; END PROBLEM 16


(merge < '(1 5 7 9) '(4 8 10))
; expect (1 4 5 7 8 9 10)
(merge > '(9 7 5 1) '(10 8 4 3))
; expect (10 9 8 7 5 4 3 1)

;; Problem 17

(define (nondecreaselist s)
    ; BEGIN PROBLEM 17
  (cond ;((null? s) nil)            ; base case 0: 0 element
    ((null? (cdr s)) (cons s nil)) ; base case 1: only one element
    (else (define rest (nondecreaselist (cdr s))) ; do recursion => define: only do once
          (if (> (car s) (car (car rest)))
              (cons (cons (car s) nil) rest)      ; let the ele be the first ele of the result => ((x) (nondecreaselist (cdr s)))
              (cons (cons (car s) (car rest)) (cdr rest))))) ; insert the first ele of s into the first ele of the result
)    
    ; END PROBLEM 17

;; Problem EC
;; Returns a function that checks if an expression is the special form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let?    (check-special 'let))

;; Converts all let special forms in EXPR into equivalent forms using lambda
(define (let-to-lambda expr)
  (cond ((atom? expr)
         ; BEGIN PROBLEM EC
         expr
         ; END PROBLEM EC
         )
        ((quoted? expr)
         ; BEGIN PROBLEM EC
         expr
         ; END PROBLEM EC
         )
        ((or (lambda? expr)
             (define? expr))
         (let ((form   (car expr))
               (params (cadr expr))
               (body   (cddr expr)))
           ; BEGIN PROBLEM EC
           (append (list form params) (map let-to-lambda body))
           ; END PROBLEM EC
           ))
        ((let? expr)
         (let ((values (cadr expr))
               (body   (cddr expr)))
           ; BEGIN PROBLEM EC
           (define paras (map let-to-lambda values)) ; first use the map-to-lambda to evaluate every atom
           (define formals (car (zip paras)))        ; the name of the parameters
           (define values (cadr (zip paras)))        ; the values of the parameters
           (define body (map let-to-lambda body))     ; calculate every element of the body
           (cons (list 'lambda formals (car body)) values) 
           ; END PROBLEM EC
           ))
        (else  ; deal with (+ 1 2)...
         ; BEGIN PROBLEM EC
         (map let-to-lambda expr)
         ; END PROBLEM EC
         )))

