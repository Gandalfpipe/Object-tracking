from src.config import conf

def createTracker(name:str):
    module =  getattr(getattr(__import__("src.trackers." + name), "trackers"), name)
    assert hasattr(module, "create"), f"No create func in module {name}"
    create_func = getattr(module, "create")
    return create_func(conf())