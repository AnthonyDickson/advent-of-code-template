(defsystem "aoc"
  :description "Advent of Code solution"
  :license "MIT"
  :version "0.1.0"
  :serial t
  :components ((:module "src"
                :components ((:file "aoc")
                             (:file "main"))))
  :build-operation "program-op"
  :build-pathname "aoc"
  :entry-point "aoc/main:main"
  :in-order-to ((test-op (test-op "aoc/tests"))))

(defsystem "aoc/tests"
  :description "Tests for the Advent of Code solution"
  :license "MIT"
  :version "0.1.0"
  :depends-on ("aoc" "rove")
  :serial t
  :components ((:module "tests"
                :components ((:file "aoc-test"))))
  :perform (test-op (operation component)
             (declare (ignore operation))
             (unless (uiop:symbol-call :rove :run component)
               (error "Tests failed."))))
