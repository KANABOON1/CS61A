(define (filter-lst fn lst)
  (if (null? lst)  ; '=' can only be used to the numbers
      nil
      (if (fn (car lst))
          (cons (car lst) (filter-lst fn (cdr lst)))
          (filter-lst fn (cdr lst))))
)

;;; Tests
(define (even? x)
  (= (modulo x 2) 0))
(filter-lst even? '(0 1 1 2 3 5 8))
; expect (0 2 8)


(define (interleave first second)
  (cond ((null? first) second) ; the form of the 'cond'
        ((null? second) first)
        (else (cons (car first) (interleave second (cdr first)))))
)

(interleave (list 1 3 5) (list 2 4 6))
; expect (1 2 3 4 5 6)

(interleave (list 1 3 5) nil)
; expect (1 3 5)

(interleave (list 1 3 5) (list 2 4))
; expect (1 2 3 4 5)


(define (accumulate combiner start n term)
  ;Tail-recursion 
  (if (= n 0)
      start
      (accumulate combiner (combiner start (term n)) (- n 1) term)))


(define (no-repeats lst)
  ;YOUR-CODE-HERE
  (cond ((null? lst) nil)
    (else (cons (car lst) (no-repeats (filter-lst (lambda (n) (not (= n (car lst)))) (cdr lst)))))) ;wonderful recursion
    ; process the list excluding the first item
    ; modify the list through function: filter-lst
)

