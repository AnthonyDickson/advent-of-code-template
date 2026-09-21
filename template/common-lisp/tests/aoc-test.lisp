(defpackage #:aoc/tests
  (:use #:cl #:rove #:aoc))
(in-package #:aoc/tests)

(deftest part-one-solves-the-example
  (testing "the placeholder input still returns the placeholder answer"
    (ok (= 0 (solve-part-one "")))))

(deftest part-two-solves-the-example
  (testing "the placeholder input still returns the placeholder answer"
    (ok (= 0 (solve-part-two "")))))
