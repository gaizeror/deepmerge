import os
import subprocess


def main(build):
    build.packages.install(".", develop=True)


def test(build):
    main(build)
    build.packages.install("pytest")
    build.packages.install("pytest-cov")
    pytest = os.path.join(build.root, "bin", "py.test")
    subprocess.call(
        [
            pytest,
            "--cov",
            "deepmerge",
            "deepmerge/tests",
            "--cov-report",
            "term-missing",
        ]
        + build.options.args
    )


def publish(build):
    """ distribute the uranium package """
    build.packages.install("wheel")
    build.packages.install("twine")
    # to use keyring
    build.packages.install("keyring")
    build.packages.install("python3-dbus")
    build.executables.run(
        ["python", "setup.py", "sdist", "bdist_wheel", "--universal", "--release"]
    )
    build.executables.run(["twine", "upload", "dist/*"])


def build_docs(build):
    build.packages.install("sphinx")
    build.packages.install("sphinx_rtd_theme")
    return subprocess.call(["make", "html"], cwd=os.path.join(build.root, "docs"))
