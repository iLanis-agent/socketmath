import json, math

def jsnum(x):
    return int(x) if isinstance(x, float) and x == int(x) else x
def fmt(x): return str(jsnum(x))
def round1(x): return jsnum(math.floor(x * 10 + 0.5) / 10)
def round0(x): return jsnum(math.floor(x + 0.5))

VOLTS = 12
FUSE_A = 10
COMFORT_A = 8
INVERTER_EASE = 0.8
RESERVE = 0.5
INVERTER_EFF = 0.85

def socket_plan(w):
    if not (w > 0):
        return {"error": "the load must be positive"}
    amps = round1(w / VOLTS)
    if amps <= COMFORT_A: verdict = "comfortably under the fuse"
    elif amps <= FUSE_A: verdict = "at the fuse's edge"
    else: verdict = "past the fuse"
    return {"amps": amps, "verdict": verdict}

def inverter_plan(w, inverterW):
    if not (w > 0) or not (inverterW > 0):
        return {"error": "the load and the inverter must be positive"}
    pct = round0(w / inverterW * 100)
    if w <= inverterW * INVERTER_EASE: verdict = "an easy ride"
    elif w <= inverterW: verdict = "at its labeled ceiling"
    else: verdict = "past its ceiling"
    return {"pct": pct, "verdict": verdict}

def runtime_plan(w, ah):
    if not (w > 0) or not (ah > 0):
        return {"error": "the load and the battery must be positive"}
    reserveWh = round0(ah * VOLTS * RESERVE * INVERTER_EFF)
    hours = round1(reserveWh / w)
    if hours < 1: verdict = "a lunch break"
    elif hours < 3: verdict = "an afternoon"
    elif hours < 8: verdict = "a workday"
    else: verdict = "an all-nighter"
    return {"reserveWh": reserveWh, "hours": hours, "verdict": verdict}

def render_socket(r, w):
    return "Your " + fmt(w) + " W load pulls " + fmt(r["amps"]) + " A at a labeled " + fmt(VOLTS) + " V - " + r["verdict"] + "."

def render_inverter(r, w, inverterW):
    return "Your " + fmt(w) + " W load asks for " + fmt(r["pct"]) + "% of a labeled " + fmt(inverterW) + " W inverter - " + r["verdict"] + "."

def render_runtime(r, w, ah):
    return ("A " + fmt(w) + " W load on a labeled " + fmt(ah) + " Ah battery has " + fmt(r["reserveWh"])
            + " Wh of safe reserve - " + fmt(r["hours"]) + " h, " + r["verdict"] + ".")

cases = []
def add(fn, f, rf, args):
    r = f(*args)
    c = {"fn": fn, "args": args, "result": r}
    if "error" not in r: c["render"] = rf(r, *args)
    cases.append(c)

for a in [[60],[90],[96],[110],[130],[150],[45],[75],[100],[0]]:
    add("socketPlan", socket_plan, render_socket, a)
for a in [[90,150],[120,150],[130,150],[160,150],[45,150],[200,300],[250,300],[100,150],[150,150],[0,150],[90,0]]:
    add("inverterPlan", inverter_plan, render_inverter, a)
for a in [[60,48],[100,48],[30,48],[150,48],[60,35],[60,70],[45,60],[90,48],[0,48],[60,0]]:
    add("runtimePlan", runtime_plan, render_runtime, a)
json.dump(cases, open("expected.json", "w"), separators=(",", ":"))
print(len(cases), "cases")
