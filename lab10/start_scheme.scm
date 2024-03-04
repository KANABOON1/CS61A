;学习scheme的初步
;scheme中的基本单位是表达式,所以有众多的()来计算表达式的值

(define (length item)
    (if (null? item)
        0
        (+ 1 (length (cdr item)))))
(define (getitem linked-list index)
    (if (= index 1)
        (car linked-list)
        (getitem (cdr linked-list) (- index 1))))

(define (repeat fn k)
    (if (> k 0)
        (begin (fn) (repeat fn (- k 1)))   ; note:begin(() ())用于在一个表达式中按顺序计算表达式的值,并返回后一个表达式
        nil))                              ; nil表示空序列,一般用nil表示程序结束或者无结果

(define x 20)
(cond 
    ((> x 0) 'positive)
    ((< x 0) 'negative)
    (else 'zero))
(print "Hello world")