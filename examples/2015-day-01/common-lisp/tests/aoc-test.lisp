(defpackage #:aoc/tests
  (:use #:cl #:rove #:aoc))
(in-package #:aoc/tests)

(defparameter *part-one-cases*
  '(("(())" . 0)
    ("()()" . 0)
    ("(((" . 3)
    ("(()(()(" . 3)
    ("))(((((" . 3)
    ("())" . -1)
    ("))(" . -1)
    (")))" . -3)
    (")())())" . -3)))

(defparameter *part-two-cases*
  '((")" . 1)
    ("()())" . 5)))

(deftest part-one-solves-the-examples
  (dolist (case *part-one-cases*)
    (testing (prin1-to-string (car case))
      (ok (= (cdr case) (solve-part-one (car case)))))))

(deftest part-two-solves-the-examples
  (dolist (case *part-two-cases*)
    (testing (prin1-to-string (car case))
      (ok (= (cdr case) (solve-part-two (car case)))))))
