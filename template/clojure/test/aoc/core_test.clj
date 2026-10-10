(ns aoc.core-test
  (:require [aoc.core :as aoc]
            [clojure.test :refer [deftest is]]))

(deftest part-one-solves-the-example
  (is (= 0 (aoc/solve-part-one ""))))

(deftest part-two-solves-the-example
  (is (= 0 (aoc/solve-part-two ""))))
