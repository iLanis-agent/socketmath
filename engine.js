(function (root) {
  "use strict";
  var VOLTS = 12;            // labeled socket voltage
  var FUSE_A = 10;           // labeled socket fuse, amps
  var COMFORT_A = 8;         // 80% continuous rule on the fuse
  var INVERTER_EASE = 0.8;   // share of the inverter ceiling called easy
  var RESERVE = 0.5;         // half the battery kept back so the engine starts
  var INVERTER_EFF = 0.85;   // labeled inverter efficiency

  function round1(x) { return Math.round(x * 10) / 10; }

  function socketPlan(w) {
    if (!(w > 0)) return { error: "the load must be positive" };
    var amps = round1(w / VOLTS);
    var verdict;
    if (amps <= COMFORT_A) verdict = "comfortably under the fuse";
    else if (amps <= FUSE_A) verdict = "at the fuse's edge";
    else verdict = "past the fuse";
    return { amps: amps, verdict: verdict };
  }

  function inverterPlan(w, inverterW) {
    if (!(w > 0) || !(inverterW > 0)) return { error: "the load and the inverter must be positive" };
    var pct = Math.round(w / inverterW * 100);
    var verdict;
    if (w <= inverterW * INVERTER_EASE) verdict = "an easy ride";
    else if (w <= inverterW) verdict = "at its labeled ceiling";
    else verdict = "past its ceiling";
    return { pct: pct, verdict: verdict };
  }

  function runtimePlan(w, ah) {
    if (!(w > 0) || !(ah > 0)) return { error: "the load and the battery must be positive" };
    var reserveWh = Math.round(ah * VOLTS * RESERVE * INVERTER_EFF);
    var hours = round1(reserveWh / w);
    var verdict;
    if (hours < 1) verdict = "a lunch break";
    else if (hours < 3) verdict = "an afternoon";
    else if (hours < 8) verdict = "a workday";
    else verdict = "an all-nighter";
    return { reserveWh: reserveWh, hours: hours, verdict: verdict };
  }

  function renderSocket(r, w) {
    return "Your " + w + " W load pulls " + r.amps + " A at a labeled " + VOLTS + " V - " + r.verdict + ".";
  }

  function renderInverter(r, w, inverterW) {
    return "Your " + w + " W load asks for " + r.pct + "% of a labeled " + inverterW + " W inverter - " + r.verdict + ".";
  }

  function renderRuntime(r, w, ah) {
    return "A " + w + " W load on a labeled " + ah + " Ah battery has " + r.reserveWh
      + " Wh of safe reserve - " + r.hours + " h, " + r.verdict + ".";
  }

  var api = { socketPlan: socketPlan, inverterPlan: inverterPlan, runtimePlan: runtimePlan, renderSocket: renderSocket, renderInverter: renderInverter, renderRuntime: renderRuntime };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.SocketMath = api;
})(this);
