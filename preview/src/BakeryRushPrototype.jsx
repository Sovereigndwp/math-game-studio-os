import React, { useEffect, useMemo, useRef, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { motion, AnimatePresence } from "framer-motion";
import {
  ShoppingBag,
  CakeSlice,
  Cookie,
  Croissant,
  CupSoda,
  RotateCcw,
  Heart,
  Clock3,
  Trophy,
  ArrowRight,
  Layers3,
  Lock,
} from "lucide-react";

const MAX_LIVES = 3;
const CONVEYOR_ITEM_COUNT = 10;

const BASE_PASTRIES = {
  cookie:    { id: "cookie",    label: "Cookie",     icon: Cookie,    value: 1 },
  croissant: { id: "croissant", label: "Croissant",  icon: Croissant, value: 1 },
  slice:     { id: "slice",     label: "Cake Slice", icon: CakeSlice, value: 2 },
  drink:     { id: "drink",     label: "Drink",      icon: CupSoda,   value: 5 },
};

const LEVELS = [
  {
    level: 1, title: "Shift 1", subtitle: "Learn the loop",
    shiftSeconds: 70, targetScore: 450, patienceSeconds: 16,
    pastrySet: [BASE_PASTRIES.cookie, BASE_PASTRIES.croissant],
    pastryWeights: [1, 1], targetPool: [1, 2, 3, 4, 5],
    customerCount: 7, conveyorDuration: 9,
  },
  {
    level: 2, title: "Shift 2", subtitle: "Bigger orders",
    shiftSeconds: 65, targetScore: 650, patienceSeconds: 14,
    pastrySet: [BASE_PASTRIES.cookie, BASE_PASTRIES.croissant],
    pastryWeights: [1, 1], targetPool: [6, 7, 8, 9, 10],
    customerCount: 8, conveyorDuration: 8,
  },
  {
    level: 3, title: "Shift 3", subtitle: "Longer counts",
    shiftSeconds: 60, targetScore: 850, patienceSeconds: 12,
    pastrySet: [BASE_PASTRIES.cookie, BASE_PASTRIES.croissant],
    pastryWeights: [1, 1], targetPool: [11, 12, 13, 14, 15],
    customerCount: 9, conveyorDuration: 7,
  },
  {
    level: 4, title: "Shift 4", subtitle: "Choose the right combination",
    shiftSeconds: 65, targetScore: 1050, patienceSeconds: 11,
    pastrySet: [BASE_PASTRIES.cookie, BASE_PASTRIES.slice],
    pastryWeights: [0.65, 0.35],
    targetPool: [6, 7, 8, 9, 10, 12, 14, 15, 16, 18],
    customerCount: 9, conveyorDuration: 6,
  },
  {
    level: 5, title: "Shift 5", subtitle: "Fast mixed value orders",
    shiftSeconds: 70, targetScore: 1250, patienceSeconds: 10,
    pastrySet: [BASE_PASTRIES.cookie, BASE_PASTRIES.slice, BASE_PASTRIES.drink],
    pastryWeights: [0.55, 0.3, 0.15],
    targetPool: [8, 10, 11, 12, 13, 15, 17, 18, 20, 22, 25],
    customerCount: 10, conveyorDuration: 5,
  },
];

function formatTime(seconds) {
  const safe = Math.max(0, seconds);
  const mins = Math.floor(safe / 60);
  const secs = safe % 60;
  return `${mins}:${String(secs).padStart(2, "0")}`;
}

function hearts(lives) {
  return Array.from({ length: MAX_LIVES }, (_, index) => index < lives);
}

function weightedChoice(items, weights) {
  const total = weights.reduce((sum, weight) => sum + weight, 0);
  let roll = Math.random() * total;
  for (let i = 0; i < items.length; i++) {
    roll -= weights[i];
    if (roll <= 0) return items[i];
  }
  return items[items.length - 1];
}

function buildCustomerQueue(config) {
  const names = ["Mia", "Leo", "Ava", "Noah", "Sofia", "Lucas", "Emma", "Mateo", "Luna", "Elena", "Owen", "Nina"];
  const pool = [...config.targetPool];
  const selectedTargets = [];
  for (let i = 0; i < config.customerCount; i++) {
    if (pool.length === 0) pool.push(...config.targetPool);
    const index = Math.floor(Math.random() * pool.length);
    selectedTargets.push(pool.splice(index, 1)[0]);
  }
  return selectedTargets.map((target, index) => ({
    id: index + 1, target, name: names[index % names.length],
  }));
}

function makeConveyorItems(pastrySet, pastryWeights, count = CONVEYOR_ITEM_COUNT) {
  return Array.from({ length: count }, (_, index) => ({
    uid: `${Date.now()}-${index}-${Math.random().toString(36).slice(2, 8)}`,
    pastry: weightedChoice(pastrySet, pastryWeights),
  }));
}

function nextConveyorItem(pastrySet, pastryWeights) {
  return {
    uid: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    pastry: weightedChoice(pastrySet, pastryWeights),
  };
}

function SmallStat({ label, value, valueClassName = "text-amber-400" }) {
  return (
    <div className="rounded-2xl border border-neutral-800 bg-neutral-950 p-4">
      <div className="text-xs uppercase tracking-[0.2em] text-neutral-500">{label}</div>
      <div className={`mt-2 text-3xl font-bold ${valueClassName}`}>{value}</div>
    </div>
  );
}

export default function BakeryRushPrototype() {
  const [screen, setScreen]                         = useState("intro");
  const [levelIndex, setLevelIndex]                 = useState(0);
  const [highestUnlockedLevel, setHighestUnlockedLevel] = useState(0);
  const [queue, setQueue]                           = useState(() => buildCustomerQueue(LEVELS[0]));
  const [customerIndex, setCustomerIndex]           = useState(0);
  const [countdown, setCountdown]                   = useState(3);
  const [shiftSecondsLeft, setShiftSecondsLeft]     = useState(LEVELS[0].shiftSeconds);
  const [patienceLeft, setPatienceLeft]             = useState(LEVELS[0].patienceSeconds);
  const [currentTotal, setCurrentTotal]             = useState(0);
  const [itemsInBox, setItemsInBox]                 = useState([]);
  const [lastItem, setLastItem]                     = useState(null);
  const [score, setScore]                           = useState(0);
  const [completedOrders, setCompletedOrders]       = useState(0);
  const [missedOrders, setMissedOrders]             = useState(0);
  const [wrongMoves, setWrongMoves]                 = useState(0);
  const [streak, setStreak]                         = useState(0);
  const [message, setMessage]                       = useState("Pack the order exactly.");
  const [firstTryForCurrentOrder, setFirstTryForCurrentOrder] = useState(true);
  const [lastAward, setLastAward]                   = useState("");
  const [lives, setLives]                           = useState(MAX_LIVES);
  const [conveyor, setConveyor]                     = useState(() => makeConveyorItems(LEVELS[0].pastrySet, LEVELS[0].pastryWeights));

  const overshootTimerRef = useRef(null);
  const successTimerRef   = useRef(null);

  const currentLevel    = LEVELS[levelIndex];
  const currentCustomer = queue[customerIndex] ?? null;
  const currentTarget   = currentCustomer?.target ?? 0;
  const currentPastries = currentLevel.pastrySet;
  const queuePreview    = queue.slice(customerIndex + 1, customerIndex + 4);
  const patiencePercent = (patienceLeft / currentLevel.patienceSeconds) * 100;
  const scorePercent    = Math.min(100, (score / currentLevel.targetScore) * 100);
  const timerUrgent     = shiftSecondsLeft <= 15;
  const nextLevelExists = levelIndex < LEVELS.length - 1;
  const levelLabel      = useMemo(() => `${currentLevel.title} · ${currentLevel.subtitle}`, [currentLevel]);

  useEffect(() => {
    return () => {
      if (overshootTimerRef.current) window.clearTimeout(overshootTimerRef.current);
      if (successTimerRef.current)   window.clearTimeout(successTimerRef.current);
    };
  }, []);

  useEffect(() => {
    if (screen !== "countdown") return;
    if (countdown === 0) {
      setScreen("playing");
      setMessage("Fill the order before the customer leaves.");
      return;
    }
    const timer = window.setTimeout(() => setCountdown((prev) => prev - 1), 800);
    return () => window.clearTimeout(timer);
  }, [screen, countdown]);

  useEffect(() => {
    if (screen !== "playing") return;
    const timer = window.setInterval(() => {
      setShiftSecondsLeft((prev) => {
        if (prev <= 1) {
          window.clearInterval(timer);
          setScreen("shift_complete");
          setMessage("Shift complete.");
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => window.clearInterval(timer);
  }, [screen]);

  useEffect(() => {
    if (screen !== "playing") return;
    const timer = window.setInterval(() => {
      setPatienceLeft((prev) => {
        if (prev <= 1) {
          window.clearInterval(timer);
          handleMissedOrder();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => window.clearInterval(timer);
  }, [screen, customerIndex, currentLevel.patienceSeconds]);

  useEffect(() => {
    if (screen !== "playing") return;
    if (score < currentLevel.targetScore) return;
    setHighestUnlockedLevel((prev) => Math.max(prev, Math.min(levelIndex + 1, LEVELS.length - 1)));
    setScreen("shift_complete");
    setMessage("Shift goal reached.");
  }, [score, currentLevel.targetScore, screen, levelIndex]);

  function refillConveyorExact(pastrySet, pastryWeights) {
    setConveyor(makeConveyorItems(pastrySet, pastryWeights));
  }

  function resetOrderState(nextMessage, level) {
    setCurrentTotal(0);
    setItemsInBox([]);
    setLastItem(null);
    setPatienceLeft(level.patienceSeconds);
    setFirstTryForCurrentOrder(true);
    setMessage(nextMessage);
    refillConveyorExact(level.pastrySet, level.pastryWeights);
  }

  function setupLevel(nextLevelIndex) {
    const config = LEVELS[nextLevelIndex];
    setLevelIndex(nextLevelIndex);
    setQueue(buildCustomerQueue(config));
    setCustomerIndex(0);
    setCountdown(3);
    setShiftSecondsLeft(config.shiftSeconds);
    setPatienceLeft(config.patienceSeconds);
    setCurrentTotal(0);
    setItemsInBox([]);
    setLastItem(null);
    setScore(0);
    setCompletedOrders(0);
    setMissedOrders(0);
    setWrongMoves(0);
    setStreak(0);
    setMessage("Study the first order.");
    setFirstTryForCurrentOrder(true);
    setLastAward("");
    setLives(MAX_LIVES);
    refillConveyorExact(config.pastrySet, config.pastryWeights);
    setScreen("countdown");
  }

  function startNewShift() { setupLevel(0); }

  function moveToNextCustomer(nextMessage) {
    const levelAtMove = currentLevel;
    setCustomerIndex((prev) => {
      const nextIndex = prev + 1;
      if (nextIndex >= queue.length) {
        setQueue(buildCustomerQueue(levelAtMove));
        return 0;
      }
      return nextIndex;
    });
    resetOrderState(nextMessage, levelAtMove);
  }

  function handleMissedOrder() {
    setMissedOrders((prev) => prev + 1);
    setLives((prev) => {
      const nextLives = prev - 1;
      if (nextLives <= 0) {
        setScreen("game_over");
        setMessage("Too many customers left unhappy.");
        return 0;
      }
      moveToNextCustomer("Customer lost. A new order is waiting.");
      return nextLives;
    });
    setStreak(0);
    setFirstTryForCurrentOrder(false);
    setLastAward("Missed order -1 life");
  }

  function completeOrder() {
    const nextCompleted = completedOrders + 1;
    let earned = firstTryForCurrentOrder ? 100 : 60;
    let awardText = firstTryForCurrentOrder ? "+100 first try" : "+60 completed";
    if (nextCompleted % 3 === 0) { earned += 50; awardText += " · +50 streak"; }
    setCompletedOrders(nextCompleted);
    setScore((prev) => prev + earned);
    setStreak((prev) => prev + 1);
    setLastAward(awardText);
    setScreen("order_success");
    setMessage("Perfect order. Box closed.");
    successTimerRef.current = window.setTimeout(() => {
      moveToNextCustomer("Nice work. Next customer.");
      setScreen("playing");
    }, 900);
  }

  function handlePastryTap(item) {
    if (screen !== "playing") return;
    const pastry = item.pastry;
    const nextTotal = currentTotal + pastry.value;
    setCurrentTotal(nextTotal);
    setItemsInBox((prev) => [...prev, pastry.id]);
    setLastItem(pastry.id);
    setConveyor((prev) => {
      const remaining = prev.filter((entry) => entry.uid !== item.uid);
      return [...remaining, nextConveyorItem(currentLevel.pastrySet, currentLevel.pastryWeights)];
    });
    if (nextTotal === currentTarget) { completeOrder(); return; }
    if (nextTotal > currentTarget) {
      setWrongMoves((prev) => prev + 1);
      setFirstTryForCurrentOrder(false);
      setStreak(0);
      setMessage("Too many. The last pastry bounced out.");
      setLastAward("Overshoot");
      overshootTimerRef.current = window.setTimeout(() => {
        setItemsInBox((prev) => { const clone = [...prev]; clone.pop(); return clone; });
        setCurrentTotal((prev) => prev - pastry.value);
        setLastItem(null);
      }, 450);
      return;
    }
    setMessage("Keep going until the total matches.");
  }

  function goToNextLevel() {
    if (!nextLevelExists) { setScreen("intro"); return; }
    setupLevel(levelIndex + 1);
  }

  return (
    <div className="min-h-screen bg-neutral-950 p-4 text-white md:p-8">
      <div className="mx-auto grid max-w-7xl gap-5">
        <AnimatePresence>
          {screen === "intro" && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="fixed inset-0 z-50 flex items-center justify-center overflow-auto bg-black/90 p-6">
              <Card className="w-full max-w-5xl rounded-3xl border-neutral-800 bg-neutral-950 text-white shadow-2xl">
                <CardContent className="grid gap-6 p-8 md:p-10">
                  <div className="text-center">
                    <p className="text-sm uppercase tracking-[0.35em] text-amber-400">Bakery Rush Prototype</p>
                    <h1 className="mt-3 text-4xl font-semibold md:text-6xl">Pass 1 and Pass 2 are now combined</h1>
                    <p className="mx-auto mt-5 max-w-3xl text-base leading-7 text-neutral-300 md:text-lg">
                      Pass 1 adds level unlocks and a real progression curve. Pass 2 replaces the static tray with a moving conveyor belt so the learner has to click the correct pastries under pressure.
                    </p>
                  </div>
                  <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
                    {LEVELS.map((lvl, index) => {
                      const unlocked = index <= highestUnlockedLevel;
                      const active = index === levelIndex;
                      return (
                        <button key={lvl.level} onClick={() => unlocked && setupLevel(index)} disabled={!unlocked}
                          className={`rounded-3xl border p-4 text-left transition ${unlocked
                            ? "border-neutral-700 bg-neutral-900 hover:border-amber-400 hover:bg-neutral-800"
                            : "cursor-not-allowed border-neutral-800 bg-neutral-950 opacity-45"
                          } ${active ? "ring-2 ring-amber-400/60" : ""}`}>
                          <div className="flex items-center justify-between">
                            <div className="text-xs uppercase tracking-[0.25em] text-neutral-500">Level {lvl.level}</div>
                            {!unlocked && <Lock className="h-4 w-4 text-neutral-500" />}
                          </div>
                          <div className="mt-3 text-lg font-semibold">{lvl.title}</div>
                          <div className="mt-1 min-h-[40px] text-sm text-neutral-400">{lvl.subtitle}</div>
                          <div className="mt-2 text-xs text-neutral-500">Targets {Math.min(...lvl.targetPool)} to {Math.max(...lvl.targetPool)}</div>
                          <div className="mt-1 text-xs text-neutral-500">Goal {lvl.targetScore}</div>
                        </button>
                      );
                    })}
                  </div>
                  <div className="flex flex-wrap justify-center gap-3">
                    <Button onClick={startNewShift} className="rounded-2xl bg-amber-400 px-8 py-6 text-lg font-semibold text-black hover:bg-amber-300">
                      Start level 1 <ArrowRight className="ml-2 h-5 w-5" />
                    </Button>
                    {highestUnlockedLevel > 0 && (
                      <Button onClick={() => setupLevel(highestUnlockedLevel)} variant="outline"
                        className="rounded-2xl border-neutral-700 bg-transparent px-8 py-6 text-lg text-white hover:bg-neutral-900">
                        Resume highest unlocked
                      </Button>
                    )}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>

        <AnimatePresence>
          {screen === "countdown" && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
              <div className="text-center">
                <div className="text-8xl font-bold text-amber-400 drop-shadow-[0_0_20px_rgba(251,191,36,0.7)] md:text-9xl">
                  {countdown === 0 ? "GO" : countdown}
                </div>
                <div className="mt-4 uppercase tracking-[0.4em] text-neutral-300">{levelLabel}</div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <div className="grid gap-4 md:grid-cols-[1.15fr_1fr]">
          <Card className="rounded-3xl border-neutral-800 bg-neutral-900 shadow-2xl">
            <CardContent className="grid gap-5 p-6 md:p-8">
              <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                <div>
                  <p className="text-xs uppercase tracking-[0.3em] text-amber-400">{levelLabel}</p>
                  <h2 className="mt-2 text-2xl font-semibold md:text-3xl">
                    {currentCustomer ? `${currentCustomer.name}'s order` : "Shift finished"}
                  </h2>
                </div>
                <div className="flex flex-wrap gap-3">
                  <div className={`min-w-[120px] rounded-2xl border px-4 py-3 ${timerUrgent ? "border-red-500 bg-red-500/10" : "border-neutral-700 bg-neutral-950"}`}>
                    <div className="flex items-center gap-2 text-xs uppercase tracking-[0.2em] text-neutral-400">
                      <Clock3 className="h-3.5 w-3.5" /> Shift time
                    </div>
                    <div className={`mt-1 text-3xl font-bold ${timerUrgent ? "text-red-400" : "text-amber-400"}`}>{formatTime(shiftSecondsLeft)}</div>
                  </div>
                  <div className="min-w-[120px] rounded-2xl border border-neutral-700 bg-neutral-950 px-4 py-3">
                    <div className="flex items-center gap-2 text-xs uppercase tracking-[0.2em] text-neutral-400">
                      <Trophy className="h-3.5 w-3.5" /> Shift score
                    </div>
                    <div className="mt-1 text-3xl font-bold text-emerald-400">{score}</div>
                  </div>
                </div>
              </div>

              <div className="grid gap-5 md:grid-cols-[0.9fr_1.1fr]">
                <Card className="rounded-3xl border-neutral-800 bg-neutral-950">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-lg">
                      <ShoppingBag className="h-5 w-5 text-amber-400" /> Order ticket
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="grid gap-4">
                    <div className="rounded-3xl bg-amber-50 p-5 text-black">
                      <div className="text-xs uppercase tracking-[0.25em] text-neutral-500">Target value</div>
                      <div className="mt-2 text-6xl font-bold">
                        {screen === "shift_complete" || screen === "game_over" ? "✓" : currentTarget}
                      </div>
                      <div className="mt-3 text-sm text-neutral-600">Click pastries from the conveyor until the box matches exactly.</div>
                    </div>
                    <div className="grid gap-2">
                      <div className="flex items-center justify-between text-sm text-neutral-300">
                        <span>Customer patience</span><span>{patienceLeft}s</span>
                      </div>
                      <Progress value={patiencePercent} className="h-3 bg-neutral-800" />
                    </div>
                    <div className="grid gap-2">
                      <div className="flex items-center justify-between text-sm text-neutral-300">
                        <span>Target score</span><span>{currentLevel.targetScore}</span>
                      </div>
                      <Progress value={scorePercent} className="h-3 bg-neutral-800" />
                    </div>
                    <div className="rounded-2xl border border-neutral-800 bg-neutral-900 p-4 text-sm leading-6 text-neutral-200">
                      <div className="mb-2 text-xs uppercase tracking-[0.2em] text-neutral-400">Status</div>
                      {message}
                    </div>
                    <div className="text-sm text-neutral-300">
                      Last award: <span className="text-amber-400">{lastAward || "—"}</span>
                    </div>
                  </CardContent>
                </Card>

                <Card className="min-h-[470px] rounded-3xl border-neutral-800 bg-neutral-950">
                  <CardHeader>
                    <CardTitle className="text-lg">Pastry box</CardTitle>
                  </CardHeader>
                  <CardContent className="grid gap-5">
                    <div className="relative min-h-[250px] overflow-hidden rounded-3xl border-2 border-dashed border-amber-500/60 bg-neutral-900 p-4">
                      <AnimatePresence>
                        {itemsInBox.length === 0 && screen === "playing" && (
                          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                            className="absolute inset-0 flex items-center justify-center text-sm text-neutral-500">
                            Click pastries from the belt to add them here.
                          </motion.div>
                        )}
                      </AnimatePresence>
                      <div className="relative z-10 grid grid-cols-4 gap-3 sm:grid-cols-5">
                        {itemsInBox.map((item, index) => {
                          const pastry = currentPastries.find((p) => p.id === item);
                          const Icon = pastry?.icon ?? Cookie;
                          const isBounce = item === lastItem && index === itemsInBox.length - 1 && message.includes("bounced out");
                          return (
                            <motion.div key={`${item}-${index}`}
                              initial={{ opacity: 0, scale: 0.75, y: -8 }}
                              animate={isBounce ? { opacity: 0.3, scale: 0.8, y: -20, x: 10 } : { opacity: 1, scale: 1, y: 0, x: 0 }}
                              transition={{ duration: 0.25 }}
                              className="flex flex-col items-center justify-center gap-1 rounded-2xl bg-amber-100 p-3 text-black shadow-lg">
                              <Icon className="h-7 w-7" />
                              <div className="text-xs font-semibold">+{pastry?.value ?? 1}</div>
                            </motion.div>
                          );
                        })}
                      </div>
                      <AnimatePresence>
                        {screen === "order_success" && (
                          <motion.div initial={{ opacity: 0, scale: 0.92 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0 }}
                            className="absolute inset-0 flex items-center justify-center rounded-3xl border border-emerald-400 bg-emerald-500/20 backdrop-blur-sm">
                            <div className="px-6 text-center">
                              <div className="text-3xl font-semibold text-white">Perfect order</div>
                              <div className="mt-2 text-sm text-emerald-100">The box closed right on target.</div>
                            </div>
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <SmallStat label="Running total" value={currentTotal} />
                      <SmallStat label="Orders completed" value={completedOrders} valueClassName="text-emerald-400" />
                    </div>
                  </CardContent>
                </Card>
              </div>

              <Card className="overflow-hidden rounded-3xl border-neutral-800 bg-neutral-950">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-lg">
                    <Layers3 className="h-5 w-5 text-amber-400" /> Conveyor belt
                  </CardTitle>
                </CardHeader>
                <CardContent className="grid gap-4">
                  <div className="text-sm text-neutral-400">Pastries move continuously now. Click the correct ones before patience or time runs out.</div>
                  <div className="relative overflow-hidden rounded-3xl border border-neutral-800 bg-neutral-900 p-4">
                    <div className="absolute inset-x-0 top-1/2 h-16 -translate-y-1/2 rounded-2xl bg-neutral-800 opacity-70" />
                    <motion.div className="relative flex w-max gap-4"
                      animate={{ x: [0, -220] }}
                      transition={{ repeat: Infinity, duration: currentLevel.conveyorDuration, ease: "linear" }}>
                      {[...conveyor, ...conveyor].map((item, index) => {
                        const pastry = item.pastry;
                        const Icon = pastry.icon;
                        const disabled = screen !== "playing";
                        return (
                          <motion.button key={`${item.uid}-${index}`}
                            whileHover={{ scale: disabled ? 1 : 1.04, y: disabled ? 0 : -2 }}
                            whileTap={{ scale: disabled ? 1 : 0.96 }}
                            onClick={() => handlePastryTap(item)}
                            disabled={disabled}
                            className="relative z-10 min-w-[126px] rounded-3xl border border-neutral-700 bg-neutral-950/95 px-4 py-5 text-center shadow-xl disabled:cursor-not-allowed disabled:opacity-50">
                            <div className="flex justify-center">
                              <Icon className="h-8 w-8 text-amber-400" />
                            </div>
                            <div className="mt-3 text-sm font-medium">{pastry.label}</div>
                            <div className="mt-1 text-xs text-neutral-400">Value {pastry.value}</div>
                          </motion.button>
                        );
                      })}
                    </motion.div>
                  </div>
                  <div className="grid gap-3 sm:grid-cols-3">
                    {currentPastries.map((pastry) => (
                      <div key={pastry.id} className="rounded-2xl border border-neutral-800 bg-neutral-900 p-3 text-sm text-neutral-300">
                        <div className="font-medium text-white">{pastry.label}</div>
                        <div className="mt-1 text-neutral-400">Adds {pastry.value}</div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </CardContent>
          </Card>

          <div className="grid gap-4">
            <Card className="rounded-3xl border-neutral-800 bg-neutral-900 shadow-2xl">
              <CardHeader><CardTitle className="text-lg">Shift dashboard</CardTitle></CardHeader>
              <CardContent className="grid gap-4">
                <div className="rounded-2xl border border-neutral-800 bg-neutral-950 p-4">
                  <div className="text-xs uppercase tracking-[0.2em] text-neutral-500">Lives</div>
                  <div className="mt-3 flex gap-2">
                    {hearts(lives).map((filled, index) => (
                      <Heart key={index} className={`h-6 w-6 ${filled ? "fill-red-400 text-red-400" : "text-neutral-700"}`} />
                    ))}
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <SmallStat label="Missed" value={missedOrders} valueClassName="text-red-400" />
                  <SmallStat label="Wrong moves" value={wrongMoves} valueClassName="text-orange-400" />
                </div>
                <div className="rounded-2xl border border-neutral-800 bg-neutral-950 p-4">
                  <div className="text-xs uppercase tracking-[0.2em] text-neutral-500">Streak</div>
                  <div className="mt-2 text-3xl font-bold text-emerald-400">{streak}</div>
                  <div className="mt-2 text-sm text-neutral-400">Every third completed order gives a bonus.</div>
                </div>
              </CardContent>
            </Card>

            <Card className="rounded-3xl border-neutral-800 bg-neutral-900 shadow-2xl">
              <CardHeader><CardTitle className="text-lg">Customer queue</CardTitle></CardHeader>
              <CardContent className="grid gap-3">
                {queuePreview.map((customer, index) => (
                  <div key={customer.id} className="flex items-center justify-between rounded-2xl border border-neutral-800 bg-neutral-950 p-4">
                    <div>
                      <div className="text-xs uppercase tracking-[0.2em] text-neutral-500">Next {index + 1}</div>
                      <div className="mt-1 text-lg font-medium">{customer.name}</div>
                    </div>
                    <div className="text-3xl font-bold text-amber-400">{customer.target}</div>
                  </div>
                ))}
                {queuePreview.length === 0 && <div className="text-sm text-neutral-500">No more queued customers in this preview.</div>}
              </CardContent>
            </Card>

            <Card className="rounded-3xl border-neutral-800 bg-neutral-900 shadow-2xl">
              <CardContent className="p-5 text-sm leading-6 text-neutral-300">
                <div className="mb-2 text-xs uppercase tracking-[0.2em] text-neutral-500">Boundary check</div>
                This stays inside prototype territory. It includes level selection, unlock flow, score thresholds, and a moving conveyor belt, but still avoids stores, accounts, analytics, and other full product systems.
              </CardContent>
            </Card>
          </div>
        </div>

        <AnimatePresence>
          {(screen === "shift_complete" || screen === "game_over") && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-6">
              <Card className="w-full max-w-2xl rounded-3xl border-neutral-800 bg-neutral-950 text-white shadow-2xl">
                <CardContent className="grid gap-6 p-8 text-center md:p-10">
                  <div>
                    <div className={`text-sm uppercase tracking-[0.35em] ${screen === "shift_complete" ? "text-emerald-400" : "text-red-400"}`}>
                      {screen === "shift_complete" ? "Shift complete" : "Shift failed"}
                    </div>
                    <h2 className="mt-3 text-4xl font-semibold md:text-5xl">
                      {screen === "shift_complete" ? `${currentLevel.title} cleared` : "Too many lost orders"}
                    </h2>
                  </div>
                  <div className="grid gap-4 md:grid-cols-4">
                    <SmallStat label="Score" value={score} />
                    <SmallStat label="Completed" value={completedOrders} valueClassName="text-emerald-400" />
                    <SmallStat label="Missed" value={missedOrders} valueClassName="text-red-400" />
                    <SmallStat label="Wrong" value={wrongMoves} valueClassName="text-orange-400" />
                  </div>
                  <div className="mx-auto max-w-xl leading-7 text-neutral-300">
                    {screen === "shift_complete"
                      ? `You cleared ${currentLevel.title}. This level used ${currentPastries.length} pastry values, conveyor speed ${currentLevel.conveyorDuration}s, and a tuned target pool of ${currentLevel.targetPool.join(", ")}.`
                      : "This failure state now tests whether the loop stays fair once the conveyor and progression systems are added."}
                  </div>
                  <div className="flex flex-wrap justify-center gap-3">
                    <Button onClick={() => setupLevel(levelIndex)} className="rounded-2xl bg-amber-400 px-8 py-6 text-lg font-semibold text-black hover:bg-amber-300">
                      Retry level
                    </Button>
                    {screen === "shift_complete" && nextLevelExists && (
                      <Button onClick={goToNextLevel} variant="outline" className="rounded-2xl border-neutral-700 bg-transparent px-8 py-6 text-lg text-white hover:bg-neutral-900">
                        Next level
                      </Button>
                    )}
                    <Button onClick={() => setScreen("intro")} variant="outline" className="rounded-2xl border-neutral-700 bg-transparent px-8 py-6 text-lg text-white hover:bg-neutral-900">
                      <RotateCcw className="mr-2 h-4 w-4" /> Back to briefing
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
