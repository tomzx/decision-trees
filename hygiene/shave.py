import generic.go_to
import location


def call(person):
    generic.go_to.call(person, location.BathRoom)
    print("pick razor")
    print("pick shaving cream")
    print("put shaving cream on face")
    print("wash hands")
    print("start running water in sink")
    # todo: add razor cleaning procedure
    print("shave neck")
    print("shave chin")
    print("shave lower lip")
    print("shave upper lip")
    print("shave left cheek")
    print("shave left sideburn")
    print("shave right cheek")
    print("shave right sideburn")
    print("clean razor")
    generic.go_to.call(person, "bedroom")
    print("store shaving cream")
    print("store razor")
