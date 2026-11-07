import org.gradle.api.tasks.testing.logging.TestExceptionFormat

plugins {
    kotlin("jvm") version "2.4.20"
    application
}

repositories { mavenCentral() }

dependencies {
    // Errors as values (Either, Raise) and persistent data structures, ready for the solutions.
    implementation("io.arrow-kt:arrow-core:2.3.0")
    implementation("org.jetbrains.kotlinx:kotlinx-collections-immutable:0.5.2")
    testImplementation(kotlin("test"))
}

kotlin {
    jvmToolchain(25)
    compilerOptions {
        allWarningsAsErrors = true
        // Report every unused return value, so a dropped result from a pure function is an error.
        freeCompilerArgs.add("-Xreturn-value-checker=full")
    }
}

application { mainClass = "aoc.AocKt" }

// The program reads `input.txt` from the project folder.
tasks.named<JavaExec>("run") { workingDir = projectDir }

tasks.test {
    useJUnitPlatform()
    testLogging {
        events("passed", "failed")
        exceptionFormat = TestExceptionFormat.FULL
    }
}

// An executable jar with the Kotlin standard library inside, which `just benchmark` runs.
tasks.jar {
    manifest { attributes("Main-Class" to application.mainClass) }
    duplicatesStrategy = DuplicatesStrategy.EXCLUDE
    from(configurations.runtimeClasspath.map { classpath -> classpath.map(::zipTree) })
}
