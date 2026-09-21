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
  :entry-point "aoc/main:main")

(defsystem "aoc/tests"
  :description "Tests for the Advent of Code solution"
  :license "MIT"
  :version "0.1.0"
  :depends-on ("aoc" "rove")
  :serial t
  :components ((:module "tests"
                :components ((:file "aoc-test")))))
