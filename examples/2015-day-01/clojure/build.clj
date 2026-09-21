(ns build
  (:require [clojure.tools.build.api :as b]))

(def lib 'aoc/aoc)
(def version "0.1.0")
(def class-dir "target/classes")
(def uber-file "target/aoc.jar")

(defn- basis []
  (b/create-basis {:project "deps.edn"}))

(defn clean
  "Removes all build output."
  [_]
  (b/delete {:path "target"}))

(defn uber
  "AOT compiles the sources and packages an executable uberjar."
  [_]
  (clean nil)
  (b/copy-dir {:src-dirs ["src"]
               :target-dir class-dir})
  (b/compile-clj {:basis (basis)
                  :ns-compile '[aoc]
                  :class-dir class-dir})
  (b/uber {:class-dir class-dir
           :uber-file uber-file
           :basis (basis)
           :main 'aoc}))
