(defpackage #:aoc
  (:use #:cl)
  (:export #:solve-part-one
           #:solve-part-two))
(in-package #:aoc)

(defun floor-delta (char)
  "`(` goes up one floor, `)` goes down one, and anything else leaves the floor alone."
  (case char
    (#\( 1)
    (#\) -1)
    (otherwise 0)))

(defun solve-part-one (input)
  "Solves part one of the puzzle for the given input."
  (loop for char across input
        sum (floor-delta char)))

(defun solve-part-two (input)
  "Solves part two of the puzzle for the given input."
  (loop with floor = 0
        for position from 1
        for char across input
        do (incf floor (floor-delta char))
        when (minusp floor)
          return position
        finally (return 0)))
