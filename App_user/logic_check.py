LOGIC=[
        "L10 flange",
        "HS Pachage",
        "HS Rolling"
        ]

def logic_check(logic,boxes):

    if LOGIC.index(logic)==0:
        num=len(list(boxes.cls))
        result=True if num >0 else False
        return result
    if LOGIC.index(logic)==1:
        num=len(list(boxes.cls))
        result=True if num >0 else False
        return result
    if LOGIC.index(logic)==2:
        num=len(list(boxes.cls))
        result=False if num >0 else True
        return result