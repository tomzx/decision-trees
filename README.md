# Decision trees
`Decision trees` is a collection of all the processes I follow when I attempt to decide what I'm supposed to do at some point.

`Decision trees` is my attempt at the introspection and modeling of my own decisions processes in order to improve them.

# Requirements
python 3.5 <=

# How to use
Start by taking a look at `main.py`. From there, you will be guided to consult its subprograms and their subprograms and so on like a regular program.

# Debugging/Tracing
It can be useful to determine from where a certain input/output is emitted. In order to display a call stack for each input/ouput, you can pass the `--trace` argument when calling `main.py`

`python main.py --trace`

Which will output something like

```
> C:\decision-trees\day\routine.py:24
 > C:\decision-trees\daily\wake_up.py:6
switch mode to user/conscious
> C:\decision-trees\day\routine.py:24
 > C:\decision-trees\daily\wake_up.py:9
What day is it? (monday,tuesday,wednesday,thursday,friday,saturday,sunday) (default: Thursday)
[...]
```

## References
* https://en.wikipedia.org/wiki/Decision_tree

## License
`Decision trees` is licensed under the [MIT license](http://choosealicense.com/licenses/mit/). See [LICENSE](LICENSE).
