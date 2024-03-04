(define (cddr s)
  (cdr (cdr s)))

(define (cadr s)
  'YOUR-CODE-HERE
  (car (cdr s)))

(define (caddr s)
  'YOUR-CODE-HERE
  (car (cdr (cdr s)))
)


(define (sign num)
  (cond   
  ((< num 0) -1)
  ((> num 0) 1)
  (else 0)
  )
)


(define (square x) (* x x))

(define (pow x y)
  ;通过square的方式使得x的幂呈现指数形式增长,大大减小递归次数
  (cond
  ((= y 1) x)
  ((even? y) (square (pow x (/ y 2))))            
  ((odd? y) (* x (square (pow x (/ (- y 1) 2)))))    
  )
)

