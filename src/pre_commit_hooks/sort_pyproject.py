#!/usr/bin/env python

import tomlkit


def main():
    with open("pyproject.toml") as f:
        pyproj = tomlkit.load(f)

    deps = pyproj["tool"]["poetry"]["dependencies"]
    dev_deps = pyproj["tool"]["poetry"]["dev-dependencies"]

    deps_sorted = tomlkit.table()
    dev_deps_sorted = tomlkit.table()

    deps_sorted["python"] = deps["python"]
    del deps["python"]

    key_fn = lambda kv: kv[0].lower()

    for key, value in sorted(deps.items(), key=key_fn):
        deps_sorted.append(key, value)

    for key, value in sorted(dev_deps.items(), key=key_fn):
        dev_deps_sorted.append(key, value)

    if deps.value.body[-1][0] is None:
        deps_sorted.add(deps.value.body[-1][1])

    if dev_deps.value.body[-1][0] is None:
        dev_deps_sorted.add(dev_deps.value.body[-1][1])

    pyproj["tool"]["poetry"]["dependencies"] = deps_sorted
    pyproj["tool"]["poetry"]["dev-dependencies"] = dev_deps_sorted

    with open("pyproject.toml", "w") as f:
        tomlkit.dump(pyproj, f)


if __name__ == "__main__":
    main()
