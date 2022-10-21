#!/usr/bin/env python

import tomlkit


def sort_deps(poetry: tomlkit.table, *args: list[str]) -> tomlkit.table:
    deps_sorted = tomlkit.table()

    deps = poetry
    for item in args:
        deps = deps[item]

    for key, value in sorted(deps.items(), key=lambda kv: kv[0].lower()):
        deps_sorted.append(key, value)

    if deps.value.body[-1][0] is None:
        deps_sorted.add(deps.value.body[-1][1])

    return deps_sorted


def main():
    with open("pyproject.toml") as f:
        pyproj = tomlkit.load(f)

    poetry = pyproj["tool"]["poetry"]

    deps_sorted = tomlkit.table()
    deps_sorted["python"] = poetry["dependencies"].pop("python")
    deps_sorted.update(sort_deps(poetry, "dependencies"))
    poetry["dependencies"] = deps_sorted

    if "dev-dependencies" in poetry:
        poetry["dev-dependencies"] = sort_deps(poetry, "dev-dependencies")

    if "group" in poetry:
        for group in poetry["group"]:
            poetry["group"][group]["dependencies"] = sort_deps(
                poetry, "group", group, "dependencies"
            )

    with open("pyproject.toml", "w") as f:
        tomlkit.dump(pyproj, f)


if __name__ == "__main__":
    main()
