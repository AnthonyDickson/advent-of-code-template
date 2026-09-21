(ns aoc-test
  (:require [aoc :as aoc]
            [clojure.test :refer [deftest is]]))

(def part-one-cases
  [["(())" 0]
   ["()()" 0]
   ["(((" 3]
   ["(()(()(" 3]
   ["))(((((" 3]
   ["())" -1]
   ["))(" -1]
   [")))" -3]
   [")())())" -3]])

(def part-two-cases
  [[")" 1]
   ["()())" 5]])

(deftest part-one-solves-the-examples
  (doseq [[input expected] part-one-cases]
    (is (= expected (aoc/solve-part-one input))
        (str "failed on input " (pr-str input)))))

(deftest part-two-solves-the-examples
  (doseq [[input expected] part-two-cases]
    (is (= expected (aoc/solve-part-two input))
        (str "failed on input " (pr-str input)))))
