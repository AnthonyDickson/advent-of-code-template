(ns aoc
  (:gen-class))

(defn- step
  "`(` goes up one floor, `)` goes down one, and anything else leaves the floor alone."
  [char]
  (case char
    \( 1
    \) -1
    0))

(defn solve-part-one
  "Solves part one of the puzzle for the given input."
  [input]
  (reduce (fn [floor char] (+ floor (step char))) 0 input))

(defn solve-part-two
  "Solves part two of the puzzle for the given input."
  [input]
  (or (->> (reductions + 0 (map step input))
           (keep-indexed (fn [position floor] (when (neg? floor) position)))
           first)
      0))

(defn -main
  "Reads `input.txt` and prints both solutions, one per line."
  [& _args]
  (let [input (slurp "input.txt")]
    (println (solve-part-one input))
    (println (solve-part-two input))))
