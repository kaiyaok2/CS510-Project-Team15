import os
import re

PROJECT_ROOT = "."  
SOURCE_FILES = ["../LoggingAspect.java", "../CustomToStringConverter.java"]
BENCHMARK_FILE = os.path.join(PROJECT_ROOT, "src/test/java/org/apache/commons/csv/CSVBenchmark.java")

def remove_benchmark_file():
    """Removes CSV's benchmark file if it exists (containing 3rd part lib dependencies causing version conflicts)."""
    if os.path.exists(BENCHMARK_FILE):
        os.remove(BENCHMARK_FILE)
        print(f"Removed benchmark file: {BENCHMARK_FILE}")
    else:
        print("Benchmark file not found. Skipping removal.")

def find_outermost_java_packages(root_dir):
    """
    Finds outermost Java package directories that directly contain .java files,
    skipping nested sub-packages.
    """
    java_src_root = os.path.join(root_dir, "src/main/java")
    package_dirs = {}

    for dirpath, dirnames, filenames in os.walk(java_src_root):
        java_files = [f for f in filenames if f.endswith(".java")]
        if java_files:
            rel_path = os.path.relpath(dirpath, java_src_root)
            package_name = rel_path.replace(os.sep, ".")
            package_dirs[package_name] = dirpath

    # Filter out nested packages — keep only those not nested inside another
    outermost_packages = set(package_dirs.keys())
    for pkg1 in package_dirs:
        for pkg2 in package_dirs:
            if pkg1 != pkg2 and pkg2.startswith(pkg1 + "."):
                outermost_packages.discard(pkg2)

    return outermost_packages


def copy_and_replace_aspect(package_names):
    """Copies source files to each actual package and replaces package references."""
    if not package_names:
        print("No Java packages found.")
        return

    for package_name in package_names:
        package_path = os.path.join(PROJECT_ROOT, "src/main/java", package_name.replace(".", "/"))
        os.makedirs(package_path, exist_ok=True)

        for source_file in SOURCE_FILES:
            if not os.path.exists(source_file):
                print(f"Error: {source_file} not found, skipping.")
                continue

            target_file = os.path.join(package_path, os.path.basename(source_file))

            with open(source_file, "r", encoding="utf-8") as f:
                content = f.read()

            updated_content = content.replace("org.apache.commons.fileupload", package_name)

            with open(target_file, "w", encoding="utf-8") as f:
                f.write(updated_content)

            print(f"Copied and updated {source_file} to {target_file}")


if __name__ == "__main__":
    packages = find_outermost_java_packages(PROJECT_ROOT)
    if "." in packages:
        packages.remove(".")
    print(f"Detected outermost Java packages with .java files: {packages}")
    remove_benchmark_file()
    copy_and_replace_aspect(packages)
