def call(person):
    print("switch mode to user/conscious")
    person.state["overall"] = "awake"
    print("open eyes")
    person.state["eyes"] = "open"
