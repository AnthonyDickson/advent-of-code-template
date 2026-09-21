(defpackage #:aoc/main
  (:use #:cl)
  (:export #:main))
(in-package #:aoc/main)

(defun main ()
  "Reads `input.txt` and prints both solutions, one per line."
  (let ((input (uiop:read-file-string "input.txt")))
    (format t "~D~%" (aoc:solve-part-one input))
    (format t "~D~%" (aoc:solve-part-two input))))
