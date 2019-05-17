def classify_disk(model):
    mapping = {
        "LK1600GEYMV": "ssd3610",
        "INTEL SSDSC2BB016T4": "ssd3500",
        "HP MO0200FCTRN": "ssd-journal",
        }
    if model in mapping:
        return mapping[model]

    if model.startswith("HP EH0146F"):
        return "sas15k-system"
    if model.startswith("HP EG0600F"):
        return "sas600"
    if model.startswith("HP EG1200F"):
        return "sas1200"

    return "undefined"
