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
  (dolist (example *part-one-cases*)
    (destructuring-bind (input . expected) example
      (testing (prin1-to-string input)
        (ok (= expected (solve-part-one input)))))))

(deftest part-two-solves-the-examples
  (dolist (example *part-two-cases*)
    (destructuring-bind (input . expected) example
      (testing (prin1-to-string input)
        (ok (= expected (solve-part-two input)))))))
