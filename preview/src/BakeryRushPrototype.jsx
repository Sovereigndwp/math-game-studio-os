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
const REFLECTION_TRIGGER_THRESHOLD = 2; // consecutive same-category errors before reflection fires
const MAX_REFLECTIONS_PER_LEVEL = 2;
const REFLECTION_DISMISS_MS = 0; // manual dismiss only

// Reflection prompts from the misconception library, keyed by category
const REFLECTION_PROMPTS = {
  impulsive_guess: "Before you tapped, did you know how much you still needed? What would you check first next time?",
  procedure_slip: "What was your running total right before you tapped the last item? Could you see it clearly?",
  representation_mismatch: "Which number on the belt mattered most for filling this order? How did you use it?",
  concept_confusion: "What were the numbers on the pastries you picked? Did they add up to what the customer wanted?",
  rule_misunderstanding: "When the item slipped back, what was your total? What did you need to do next?",
  strategic_overload: "What made it harder this level? Was it the speed, the numbers, or trying to do both at once?",
};

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
    customerCount: 7, conveyorDuration: 9, overshootPenaltySeconds: 2,
  },
  {
    level: 2, title: "Shift 2", subtitle: "Bigger orders",
    shiftSeconds: 65, targetScore: 650, patienceSeconds: 14,
    pastrySet: [BASE_PASTRIES.cookie, BASE_PASTRIES.croissant],
    pastryWeights: [1, 1], targetPool: [6, 7, 8, 9, 10],
    customerCount: 8, conveyorDuration: 8, overshootPenaltySeconds: 2,
  },
  {
    level: 3, title: "Shift 3", subtitle: "Longer counts",
    shiftSeconds: 60, targetScore: 850, patienceSeconds: 12,
    pastrySet: [BASE_PASTRIES.cookie, BASE_PASTRIES.croissant],
    pastryWeights: [1, 1], targetPool: [11, 12, 13, 14, 15],
    customerCount: 9, conveyorDuration: 7, overshootPenaltySeconds: 3,
  },
  {
    level: 4, title: "Shift 4", subtitle: "Choose the right combination",
    shiftSeconds: 65, targetScore: 1050, patienceSeconds: 11,
    pastrySet: [BASE_PASTRIES.cookie, BASE_PASTRIES.slice],
    pastryWeights: [0.65, 0.35],
    targetPool: [6, 7, 8, 9, 10, 12, 14, 15, 16, 18],
    customerCount: 9, conveyorDuration: 6, overshootPenaltySeconds: 3,
  },
  {
    level: 5, title: "Shift 5", subtitle: "Fast mixed value orders",
    shiftSeconds: 70, targetScore: 1250, patienceSeconds: 10,
    pastrySet: [BASE_PASTRIES.cookie, BASE_PASTRIES.slice, BASE_PASTRIES.drink],
    pastryWeights: [0.55, 0.3, 0.15],
    targetPool: [8, 10, 11, 12, 13, 15, 17, 18, 20, 22, 25],
    customerCount: 10, conveyorDuration: 5, overshootPenaltySeconds: 4,
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

const CUSTOMER_TEMPLATES = [
  { name: "Mia",    emoji: "👩",  requestLine: "For my daughter's birthday party!",   successLine: "She'll love these!",          overshootLine: "Careful with those!" },
  { name: "Leo",    emoji: "👨",  requestLine: "Office meeting in 10 minutes.",       successLine: "Perfect, right on time!",     overshootLine: "I'm in a rush here..." },
  { name: "Ava",    emoji: "👧",  requestLine: "My friends are waiting outside!",     successLine: "You're the best!",            overshootLine: "That's too many..." },
  { name: "Noah",   emoji: "🧑",  requestLine: "Breakfast for the whole family.",     successLine: "Just what we needed!",        overshootLine: "That won't fit the box..." },
  { name: "Sofia",  emoji: "👩‍🍳", requestLine: "I need this exact amount, please.",    successLine: "Precision! Love it.",         overshootLine: "I said exact!" },
  { name: "Lucas",  emoji: "👦",  requestLine: "Saving up for a big picnic.",         successLine: "Picnic is going to be great!",overshootLine: "Whoa, slow down!" },
  { name: "Emma",   emoji: "👵",  requestLine: "For my book club this evening.",      successLine: "They'll be so pleased!",      overshootLine: "Oh dear, that's extra..." },
  { name: "Mateo",  emoji: "👨‍🍳", requestLine: "I know what I want — let's go.",       successLine: "Fast and clean. Respect.",    overshootLine: "Come on, focus!" },
  { name: "Luna",   emoji: "🧒",  requestLine: "Can I get exactly this many? Please?",successLine: "Yay!! Thank you!!",           overshootLine: "Oops! Too many!" },
  { name: "Elena",  emoji: "👩‍💼", requestLine: "Client meeting in an hour.",           successLine: "Professional. Thank you.",    overshootLine: "I don't have time for this." },
  { name: "Owen",   emoji: "🧓",  requestLine: "Same order as every Tuesday.",        successLine: "You remembered! Wonderful.",   overshootLine: "That's not my usual..." },
  { name: "Nina",   emoji: "👩‍🎨", requestLine: "Treats for the studio crew!",          successLine: "The crew will love you!",     overshootLine: "We don't need that many!" },
];

function buildCustomerQueue(config) {
  const pool = [...config.targetPool];
  const templates = [...CUSTOMER_TEMPLATES].sort(() => Math.random() - 0.5);
  const selectedTargets = [];
  for (let i = 0; i < config.customerCount; i++) {
    if (pool.length === 0) pool.push(...config.targetPool);
    const index = Math.floor(Math.random() * pool.length);
    selectedTargets.push(pool.splice(index, 1)[0]);
  }
  return selectedTargets.map((target, i) => ({
    id: i + 1,
    target,
    ...templates[i % templates.length],
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
    <div className="rounded-2xl border border-amber-900/15 bg-[#1a1412] p-4">
      <div className="text-xs uppercase tracking-[0.2em] text-neutral-500">{label}</div>
      <div className={`mt-2 text-3xl font-bold ${valueClassName}`}>{value}</div>
    </div>
  );
}

function getBakeryStatus(completed, missed, streak, lives) {
  if (lives === 1) return { text: "🚨 Last chance — don't lose another customer!", color: "#fca5a5" };
  if (missed >= 2) return { text: "😬 Boss is watching... 👀", color: "#fcd34d" };
  if (missed === 1) return { text: "😬 The line is getting longer...", color: "#fcd34d" };
  if (streak >= 4) return { text: "🔥 Rush hour! You're unstoppable!", color: "#86efac" };
  if (streak >= 2) return { text: "🔥 Nice streak — keep it going!", color: "#fbbf24" };
  if (completed >= 3) return { text: "☕ Getting busy now...", color: "#d6d3d1" };
  if (completed >= 1) return { text: "☕ Good start. Next customer!", color: "#d6d3d1" };
  return { text: "☕ Quiet morning. First customer of the day.", color: "#a8a29e" };
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
  const [customerMood, setCustomerMood]             = useState("neutral"); // "neutral" | "annoyed"
  const [overshootsThisOrder, setOvershootsThisOrder] = useState(0);

  const overshootTimerRef = useRef(null);
  const successTimerRef   = useRef(null);

  // --- Reflection beat state ---
  const [reflectionPrompt, setReflectionPrompt]     = useState(null);
  const [reflectionCategory, setReflectionCategory] = useState(null);
  const tapTimestamps                               = useRef([]);
  const consecutiveErrors                           = useRef([]); // [{category, orderIndex}]
  const reflectionsFiredThisLevel                   = useRef(0);
  const reflectionCategoriesFiredThisLevel           = useRef(new Set());

  // --- Session diagnostics for reflection beats ---
  const [sessionDiagnostics, setSessionDiagnostics] = useState({
    totalReflections: 0,
    reflectionsByLevel: {},   // { levelIndex: count }
    reflectionsByCategory: {}, // { category: count }
    reflectionLog: [],        // [{ level, order, category, prompt }]
  });

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

  // --- Misconception detection ---
  function classifyError(nextTotal, target, pastryValue, tapTimes) {
    // impulsive_guess: 3+ taps within 1500ms total
    if (tapTimes.length >= 3) {
      const recent = tapTimes.slice(-3);
      const span = recent[recent.length - 1] - recent[0];
      if (span < 1500) return "impulsive_guess";
    }
    // procedure_slip: overshoot by small amount (1-2), deliberate pace (last gap > 800ms)
    const overshootAmount = nextTotal - target;
    if (overshootAmount <= 2 && tapTimes.length >= 2) {
      const lastGap = tapTimes[tapTimes.length - 1] - tapTimes[tapTimes.length - 2];
      if (lastGap > 800) return "procedure_slip";
    }
    // concept_confusion: at L4+ where items have mixed values,
    // if item count equals target but total doesn't (count-not-sum error)
    if (itemsInBox.length + 1 === target && nextTotal !== target && pastryValue > 1) {
      return "concept_confusion";
    }
    // Default: rule_misunderstanding (generic overshoot confusion)
    return "rule_misunderstanding";
  }

  function checkReflectionTrigger(category) {
    // Already at cap for this level?
    if (reflectionsFiredThisLevel.current >= MAX_REFLECTIONS_PER_LEVEL) return;
    // Already fired for this category this level?
    if (reflectionCategoriesFiredThisLevel.current.has(category)) return;

    consecutiveErrors.current.push({ category, orderIndex: customerIndex });

    // Check for N consecutive same-category errors
    const recent = consecutiveErrors.current.slice(-REFLECTION_TRIGGER_THRESHOLD);
    if (recent.length < REFLECTION_TRIGGER_THRESHOLD) return;
    const allSame = recent.every(e => e.category === category);
    if (!allSame) return;

    // Fire reflection beat
    const prompt = REFLECTION_PROMPTS[category] || REFLECTION_PROMPTS.rule_misunderstanding;
    setReflectionPrompt(prompt);
    setReflectionCategory(category);
    setScreen("reflection");

    reflectionsFiredThisLevel.current += 1;
    reflectionCategoriesFiredThisLevel.current.add(category);

    setSessionDiagnostics(prev => ({
      totalReflections: prev.totalReflections + 1,
      reflectionsByLevel: {
        ...prev.reflectionsByLevel,
        [levelIndex]: (prev.reflectionsByLevel[levelIndex] || 0) + 1,
      },
      reflectionsByCategory: {
        ...prev.reflectionsByCategory,
        [category]: (prev.reflectionsByCategory[category] || 0) + 1,
      },
      reflectionLog: [
        ...prev.reflectionLog,
        { level: levelIndex + 1, order: customerIndex + 1, category, prompt },
      ],
    }));
  }

  function dismissReflection() {
    setReflectionPrompt(null);
    setReflectionCategory(null);
    setScreen("playing");
  }

  function refillConveyorExact(pastrySet, pastryWeights) {
    setConveyor(makeConveyorItems(pastrySet, pastryWeights));
  }

  function resetOrderState(nextMessage, level) {
    setCurrentTotal(0);
    setItemsInBox([]);
    setLastItem(null);
    setPatienceLeft(level.patienceSeconds);
    setFirstTryForCurrentOrder(true);
    setCustomerMood("neutral");
    setOvershootsThisOrder(0);
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
    tapTimestamps.current = [];
    consecutiveErrors.current = [];
    reflectionsFiredThisLevel.current = 0;
    reflectionCategoriesFiredThisLevel.current = new Set();
    setReflectionPrompt(null);
    setReflectionCategory(null);
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

    // Tiered celebration based on target difficulty and performance
    const target = currentCustomer?.target ?? 0;
    const customerSuccess = currentCustomer?.successLine ?? "Thank you!";
    const isFlawless = firstTryForCurrentOrder && target > 8;
    const isHard = target > 10;
    const isMedium = target >= 6;

    if (isFlawless) {
      setMessage(`💎 FLAWLESS! ${customerSuccess}`);
      setScreen("order_success");
      successTimerRef.current = window.setTimeout(() => {
        moveToNextCustomer("Incredible work. Next customer!");
        setScreen("playing");
      }, 1200);
    } else if (isHard) {
      setMessage(`🎉 Incredible! ${customerSuccess}`);
      setScreen("order_success");
      successTimerRef.current = window.setTimeout(() => {
        moveToNextCustomer("Great job. Next customer!");
        setScreen("playing");
      }, 900);
    } else if (isMedium) {
      setMessage(`🎯 Nice one! ${customerSuccess}`);
      setScreen("order_success");
      successTimerRef.current = window.setTimeout(() => {
        moveToNextCustomer("Next customer.");
        setScreen("playing");
      }, 700);
    } else {
      // Easy order — quick transition, no overlay
      setMessage(`✅ ${customerSuccess}`);
      successTimerRef.current = window.setTimeout(() => {
        moveToNextCustomer("Next customer.");
        setScreen("playing");
      }, 500);
    }
  }

  function handlePastryTap(item) {
    if (screen !== "playing") return;
    const pastry = item.pastry;
    const nextTotal = currentTotal + pastry.value;

    // Record tap timestamp for misconception detection
    tapTimestamps.current.push(Date.now());

    setCurrentTotal(nextTotal);
    setItemsInBox((prev) => [...prev, pastry.id]);
    setLastItem(pastry.id);
    setConveyor((prev) => {
      const remaining = prev.filter((entry) => entry.uid !== item.uid);
      return [...remaining, nextConveyorItem(currentLevel.pastrySet, currentLevel.pastryWeights)];
    });
    if (nextTotal === currentTarget) {
      // Successful order clears consecutive error tracking for this order
      tapTimestamps.current = [];
      completeOrder();
      return;
    }
    if (nextTotal > currentTarget) {
      // Classify the error before handling the overshoot
      const errorCategory = classifyError(nextTotal, currentTarget, pastry.value, tapTimestamps.current);
      checkReflectionTrigger(errorCategory);

      // --- Overshoot consequence: drain patience, upset customer ---
      const penalty = currentLevel.overshootPenaltySeconds || 2;
      setPatienceLeft((prev) => Math.max(0, prev - penalty));
      setOvershootsThisOrder((prev) => prev + 1);
      setCustomerMood("annoyed");

      setWrongMoves((prev) => prev + 1);
      setFirstTryForCurrentOrder(false);
      setStreak(0);
      const custOvershoot = currentCustomer?.overshootLine ?? "That's too many!";
      setMessage(`${custOvershoot} (−${penalty}s patience)`);
      setLastAward(`Overshoot −${penalty}s`);
      overshootTimerRef.current = window.setTimeout(() => {
        setItemsInBox((prev) => { const clone = [...prev]; clone.pop(); return clone; });
        setCurrentTotal((prev) => prev - pastry.value);
        setLastItem(null);
      }, 900);
      tapTimestamps.current = [];
      return;
    }
    setMessage("Keep going until the total matches.");
  }

  function goToNextLevel() {
    if (!nextLevelExists) { setScreen("intro"); return; }
    setupLevel(levelIndex + 1);
  }

  // Approaching target — within 2 of goal
  const approachingTarget = screen === "playing" && currentTarget > 0 && (currentTarget - currentTotal) <= 2 && (currentTarget - currentTotal) > 0;

  return (
    <div className="min-h-screen p-4 text-white md:p-8" style={{
      background: "linear-gradient(180deg, #1a1412 0%, #0f0d0b 50%, #1a1412 100%)",
    }}>
      {/* Ambient warm glow behind play area */}
      <div className="pointer-events-none fixed inset-0 z-0" style={{
        background: "radial-gradient(ellipse 60% 40% at 50% 40%, rgba(217,119,6,0.06) 0%, transparent 70%)",
      }} />
      <div className="relative z-10 mx-auto grid max-w-7xl gap-5">
        <AnimatePresence>
          {screen === "intro" && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="fixed inset-0 z-50 flex items-center justify-center overflow-auto bg-black/90 p-6">
              <Card className="w-full max-w-5xl rounded-3xl border-amber-900/30 bg-[#1a1412] text-white shadow-2xl shadow-amber-950/20">
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

        {/* Bakery status strip */}
        {screen === "playing" && (() => {
          const status = getBakeryStatus(completedOrders, missedOrders, streak, lives);
          return (
            <div className="rounded-2xl mx-auto px-4 py-2 text-center text-sm" style={{
              color: status.color,
              background: 'rgba(26,20,18,0.8)',
              border: '1px solid rgba(217,119,6,0.08)',
              maxWidth: '600px',
              marginBottom: '-8px',
            }}>
              {status.text}
            </div>
          );
        })()}

        <div className="grid gap-4 md:grid-cols-[1.15fr_1fr]">
          <Card className="rounded-3xl border-amber-900/20 bg-[#1c1614] shadow-2xl shadow-amber-950/10">
            <CardContent className="grid gap-5 p-6 md:p-8">
              <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                <div>
                  <p className="text-xs uppercase tracking-[0.3em] text-amber-400">{levelLabel}</p>
                  <h2 className="mt-2 text-2xl font-semibold md:text-3xl">
                    {currentCustomer ? (
                      <>
                        <span>{
                          patiencePercent < 25 ? "😢" :
                          patiencePercent < 50 ? "😤" :
                          customerMood === "annoyed" ? "😐" :
                          currentCustomer.emoji || "😊"
                        }</span>
                        {" "}{currentCustomer.name}'s order
                        {overshootsThisOrder > 0 && (
                          <span className="ml-2 text-base font-normal text-red-400">
                            ({overshootsThisOrder} overshoot{overshootsThisOrder > 1 ? "s" : ""})
                          </span>
                        )}
                        <div className="mt-1 text-sm font-normal text-amber-200/60" style={{ fontStyle: 'italic' }}>
                          "{currentCustomer.requestLine}"
                        </div>
                      </>
                    ) : "Shift finished"}
                  </h2>
                </div>
                <div className="flex flex-wrap gap-3">
                  <div className={`min-w-[120px] rounded-2xl border px-4 py-3 ${timerUrgent ? "border-red-500/40 bg-red-500/10" : "border-amber-900/20 bg-[#1a1412]"}`}>
                    <div className="flex items-center gap-2 text-xs uppercase tracking-[0.2em] text-neutral-500">
                      <Clock3 className="h-3.5 w-3.5" /> Shift time
                    </div>
                    <div className={`mt-1 text-3xl font-bold ${timerUrgent ? "text-red-400" : "text-amber-400"}`}>{formatTime(shiftSecondsLeft)}</div>
                  </div>
                  <div className="min-w-[120px] rounded-2xl border border-amber-900/20 bg-[#1a1412] px-4 py-3">
                    <div className="flex items-center gap-2 text-xs uppercase tracking-[0.2em] text-neutral-500">
                      <Trophy className="h-3.5 w-3.5" /> Shift score
                    </div>
                    <motion.div key={score} initial={{ scale: 1.15 }} animate={{ scale: 1 }}
                      className="mt-1 text-3xl font-bold text-emerald-400">{score}</motion.div>
                  </div>
                </div>
              </div>

              <div className="grid gap-5 md:grid-cols-[0.9fr_1.1fr]">
                <Card className="rounded-3xl border-amber-900/20 bg-[#1a1412]">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-lg">
                      <ShoppingBag className="h-5 w-5 text-amber-400" /> Order ticket
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="grid gap-4">
                    <motion.div
                      animate={approachingTarget
                        ? { boxShadow: ["0 0 8px rgba(217,119,6,0.2)", "0 0 20px rgba(217,119,6,0.35)", "0 0 8px rgba(217,119,6,0.2)"] }
                        : { boxShadow: "0 4px 12px rgba(0,0,0,0.15)" }
                      }
                      transition={approachingTarget ? { repeat: Infinity, duration: 1.2, ease: "easeInOut" } : {}}
                      className="rounded-3xl p-5"
                      style={{
                        background: "linear-gradient(180deg, #fffbeb 0%, #fef3c7 100%)",
                        color: "#1a1412",
                      }}
                    >
                      <div className="text-xs uppercase tracking-[0.25em]" style={{ color: "#92400e" }}>Target value</div>
                      <motion.div
                        key={currentTarget}
                        initial={{ scale: 0.9, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        className="mt-2 text-6xl font-bold" style={{ color: "#78350f" }}
                      >
                        {screen === "shift_complete" || screen === "game_over" ? "✓" : currentTarget}
                      </motion.div>
                      <div className="mt-3 text-sm" style={{ color: "#92400e" }}>
                        {approachingTarget ? "Almost there!" : "Match this number exactly."}
                      </div>
                    </motion.div>
                    <div className="grid gap-2">
                      <div className="flex items-center justify-between text-sm text-neutral-300">
                        <span>Customer patience</span>
                        <span className={patiencePercent < 30 ? "text-red-400 font-semibold" : ""}>{patienceLeft}s</span>
                      </div>
                      <div className="h-3 overflow-hidden rounded-full bg-neutral-800">
                        <motion.div
                          className="h-full rounded-full"
                          animate={{ width: `${patiencePercent}%` }}
                          transition={{ duration: 0.4 }}
                          style={{
                            background: patiencePercent > 50
                              ? "linear-gradient(90deg, #fbbf24, #f59e0b)"
                              : patiencePercent > 25
                              ? "linear-gradient(90deg, #f59e0b, #ea580c)"
                              : "linear-gradient(90deg, #ef4444, #dc2626)",
                          }}
                        />
                      </div>
                    </div>
                    <div className="grid gap-2">
                      <div className="flex items-center justify-between text-sm text-neutral-300">
                        <span>Target score</span><span>{currentLevel.targetScore}</span>
                      </div>
                      <Progress value={scorePercent} className="h-3 bg-neutral-800" />
                    </div>
                    <div className="rounded-2xl border border-amber-900/15 bg-[#1a1412] p-4 text-sm leading-6 text-neutral-300">
                      <div className="mb-2 text-xs uppercase tracking-[0.2em] text-neutral-500">Status</div>
                      {message}
                    </div>
                    <div className="text-sm text-neutral-400">
                      Last award: <motion.span key={lastAward} initial={{ scale: 1.2, color: "#fbbf24" }}
                        animate={{ scale: 1, color: "#f59e0b" }}
                        className="font-medium">{lastAward || "—"}</motion.span>
                    </div>
                  </CardContent>
                </Card>

                <Card className="min-h-[470px] rounded-3xl border-amber-900/20 bg-[#1a1412]">
                  <CardHeader>
                    <CardTitle className="text-lg">Pastry box</CardTitle>
                  </CardHeader>
                  <CardContent className="grid gap-5">
                    <motion.div
                      animate={
                        screen === "order_success"
                          ? { borderColor: "rgba(16,185,129,0.6)", boxShadow: "0 0 24px rgba(16,185,129,0.2)" }
                          : message.includes("bounced")
                          ? { borderColor: "rgba(239,68,68,0.6)", boxShadow: "0 0 24px rgba(239,68,68,0.15)" }
                          : approachingTarget
                          ? { borderColor: "rgba(217,119,6,0.7)", boxShadow: "0 0 20px rgba(217,119,6,0.12)" }
                          : { borderColor: "rgba(217,119,6,0.25)", boxShadow: "0 0 0px transparent" }
                      }
                      transition={{ duration: 0.3 }}
                      className="relative min-h-[250px] overflow-hidden rounded-3xl border-2 border-dashed p-4"
                      style={{ background: "linear-gradient(180deg, #1f1a14 0%, #191410 100%)" }}
                    >
                      <AnimatePresence>
                        {itemsInBox.length === 0 && screen === "playing" && (
                          <motion.div initial={{ opacity: 0 }} animate={{ opacity: [0.4, 0.7, 0.4] }}
                            transition={{ repeat: Infinity, duration: 2.5, ease: "easeInOut" }}
                            exit={{ opacity: 0 }}
                            className="absolute inset-0 flex items-center justify-center text-sm text-amber-200/30">
                            Tap pastries from the belt
                          </motion.div>
                        )}
                      </AnimatePresence>
                      <div className="relative z-10 grid grid-cols-4 gap-3 sm:grid-cols-5">
                        {itemsInBox.map((item, index) => {
                          const pastry = currentPastries.find((p) => p.id === item);
                          const Icon = pastry?.icon ?? Cookie;
                          const isBounce = item === lastItem && index === itemsInBox.length - 1 && message.includes("bounced");
                          const isNewest = index === itemsInBox.length - 1 && !isBounce;
                          return (
                            <motion.div key={`${item}-${index}`}
                              initial={{ opacity: 0, scale: 1.15, y: -12 }}
                              animate={isBounce
                                ? { opacity: 0.3, scale: 0.7, y: -20, x: [0, -8, 8, -4, 0], rotate: [0, -5, 5, 0] }
                                : { opacity: 1, scale: 1, y: 0, x: 0, rotate: 0 }
                              }
                              transition={isBounce ? { duration: 0.4 } : { type: "spring", stiffness: 400, damping: 20 }}
                              className="flex flex-col items-center justify-center gap-1 rounded-2xl p-3 shadow-lg"
                              style={{
                                background: "linear-gradient(180deg, #fef3c7 0%, #fde68a 100%)",
                                boxShadow: isNewest
                                  ? "0 0 12px rgba(217,119,6,0.3), 0 4px 8px rgba(0,0,0,0.2)"
                                  : "0 2px 6px rgba(0,0,0,0.2)",
                              }}>
                              <Icon className="h-7 w-7" style={{ color: "#b45309" }} />
                              <div className="text-xs font-bold" style={{ color: "#78350f" }}>+{pastry?.value ?? 1}</div>
                            </motion.div>
                          );
                        })}
                      </div>
                      <AnimatePresence>
                        {screen === "order_success" && (() => {
                          const target = currentCustomer?.target ?? 0;
                          const isFlawless = message.includes("💎");
                          const isHard = message.includes("🎉");
                          const bgColor = isFlawless
                            ? "rgba(245,158,11,0.2)"
                            : isHard
                            ? "rgba(16,185,129,0.18)"
                            : "rgba(16,185,129,0.12)";
                          const borderColor = isFlawless
                            ? "rgba(245,158,11,0.5)"
                            : "rgba(16,185,129,0.4)";
                          return (
                            <motion.div initial={{ opacity: 0, scale: 0.92 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0 }}
                              className="absolute inset-0 flex items-center justify-center rounded-3xl backdrop-blur-sm"
                              style={{ background: bgColor, border: `1px solid ${borderColor}` }}>
                              <div className="px-6 text-center">
                                <div className="text-4xl">{isFlawless ? "💎" : isHard ? "🎉" : "🎯"}</div>
                                <div className="mt-2 text-2xl font-semibold text-white">{message}</div>
                                <div className="mt-2 text-sm" style={{ color: isFlawless ? "#fcd34d" : "#86efac" }}>{lastAward}</div>
                              </div>
                            </motion.div>
                          );
                        })()}
                      </AnimatePresence>
                    </motion.div>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="rounded-2xl border border-amber-900/20 bg-[#1a1412] p-4">
                        <div className="text-xs uppercase tracking-[0.2em] text-neutral-500">Running total</div>
                        <motion.div
                          key={currentTotal}
                          initial={{ scale: 1.2, color: "#f59e0b" }}
                          animate={{ scale: 1, color: approachingTarget ? "#f59e0b" : "#fbbf24" }}
                          transition={{ type: "spring", stiffness: 500, damping: 15 }}
                          className="mt-2 text-3xl font-bold"
                        >
                          {currentTotal}
                        </motion.div>
                      </div>
                      <SmallStat label="Orders completed" value={completedOrders} valueClassName="text-emerald-400" />
                    </div>
                  </CardContent>
                </Card>
              </div>

              <Card className="overflow-hidden rounded-3xl border-amber-900/20 bg-[#1a1412]">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-lg">
                    <Layers3 className="h-5 w-5 text-amber-400" /> Conveyor belt
                  </CardTitle>
                </CardHeader>
                <CardContent className="grid gap-4">
                  <div className="text-sm text-amber-200/40">Tap the right pastries before patience runs out.</div>
                  <div className="relative overflow-hidden rounded-3xl p-4" style={{
                    background: "linear-gradient(180deg, #292018 0%, #1f1810 40%, #292018 100%)",
                    boxShadow: "inset 0 2px 8px rgba(0,0,0,0.5), inset 0 -2px 8px rgba(0,0,0,0.3)",
                    border: "1px solid rgba(217,119,6,0.12)",
                  }}>
                    {/* Belt track surface */}
                    <div className="absolute inset-x-0 top-1/2 h-16 -translate-y-1/2 rounded-2xl" style={{
                      background: "linear-gradient(180deg, #3d2e1e 0%, #2a1f14 50%, #3d2e1e 100%)",
                      boxShadow: "inset 0 1px 4px rgba(0,0,0,0.6), 0 1px 2px rgba(217,119,6,0.05)",
                    }} />
                    <motion.div className="relative flex w-max gap-4"
                      animate={{ x: [0, -220] }}
                      transition={{ repeat: Infinity, duration: currentLevel.conveyorDuration, ease: "linear" }}>
                      {[...conveyor, ...conveyor].map((item, index) => {
                        const pastry = item.pastry;
                        const Icon = pastry.icon;
                        const disabled = screen !== "playing";
                        return (
                          <motion.button key={`${item.uid}-${index}`}
                            whileHover={{ scale: disabled ? 1 : 1.06, y: disabled ? 0 : -4 }}
                            whileTap={{ scale: disabled ? 1 : 0.94 }}
                            animate={{ y: [0, -2, 0] }}
                            transition={{ y: { repeat: Infinity, duration: 2 + (index % 3) * 0.3, ease: "easeInOut" }}}
                            onClick={() => handlePastryTap(item)}
                            disabled={disabled}
                            className="relative z-10 min-w-[126px] rounded-3xl px-4 py-5 text-center disabled:cursor-not-allowed disabled:opacity-50"
                            style={{
                              background: "linear-gradient(180deg, #fef3c7 0%, #fde68a 100%)",
                              border: "1px solid rgba(217,119,6,0.25)",
                              boxShadow: disabled
                                ? "0 2px 8px rgba(0,0,0,0.3)"
                                : "0 4px 16px rgba(217,119,6,0.15), 0 2px 4px rgba(0,0,0,0.3)",
                              color: "#1a1412",
                            }}>
                            <div className="flex justify-center">
                              <Icon className="h-8 w-8" style={{ color: "#b45309" }} />
                            </div>
                            <div className="mt-3 text-sm font-semibold" style={{ color: "#78350f" }}>{pastry.label}</div>
                            <div className="mt-1 rounded-full px-2 py-0.5 text-xs font-bold" style={{
                              background: "rgba(217,119,6,0.15)",
                              color: "#92400e",
                            }}>+{pastry.value}</div>
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
            <Card className="rounded-3xl border-amber-900/20 bg-[#1c1614] shadow-2xl shadow-amber-950/10">
              <CardHeader><CardTitle className="text-lg">Shift dashboard</CardTitle></CardHeader>
              <CardContent className="grid gap-4">
                <div className="rounded-2xl border border-amber-900/15 bg-[#1a1412] p-4">
                  <div className="text-xs uppercase tracking-[0.2em] text-neutral-500">Lives</div>
                  <div className="mt-3 flex gap-2">
                    {hearts(lives).map((filled, index) => (
                      <motion.div key={index}
                        animate={filled ? {} : { scale: [1, 0.8], opacity: [1, 0.3] }}
                        transition={{ duration: 0.3 }}>
                        <Heart className={`h-6 w-6 ${filled ? "fill-red-400 text-red-400" : "text-neutral-700"}`} />
                      </motion.div>
                    ))}
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <SmallStat label="Missed" value={missedOrders} valueClassName="text-red-400" />
                  <SmallStat label="Wrong moves" value={wrongMoves} valueClassName="text-orange-400" />
                </div>
                <div className="rounded-2xl border border-amber-900/15 bg-[#1a1412] p-4">
                  <div className="text-xs uppercase tracking-[0.2em] text-neutral-500">Streak</div>
                  <motion.div key={streak} initial={{ scale: 1.3 }} animate={{ scale: 1 }}
                    className="mt-2 text-3xl font-bold text-emerald-400">{streak}</motion.div>
                  <div className="mt-2 text-sm text-neutral-500">Every third order gives a bonus.</div>
                </div>
              </CardContent>
            </Card>

            <Card className="rounded-3xl border-amber-900/20 bg-[#1c1614] shadow-2xl shadow-amber-950/10">
              <CardHeader><CardTitle className="text-lg">Customer queue</CardTitle></CardHeader>
              <CardContent className="grid gap-3">
                {queuePreview.map((customer, index) => (
                  <div key={customer.id} className="flex items-center justify-between rounded-2xl border border-amber-900/15 bg-[#1a1412] p-4">
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

            <Card className="rounded-3xl border-amber-900/20 bg-[#1c1614] shadow-2xl shadow-amber-950/10">
              <CardContent className="p-5 text-sm leading-6 text-neutral-400">
                <div className="mb-2 text-xs uppercase tracking-[0.2em] text-neutral-500">Boundary check</div>
                This stays inside prototype territory. It includes level selection, unlock flow, score thresholds, and a moving conveyor belt, but still avoids stores, accounts, analytics, and other full product systems.
              </CardContent>
            </Card>
          </div>
        </div>

        <AnimatePresence>
          {screen === "reflection" && reflectionPrompt && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-6">
              <Card className="w-full max-w-lg rounded-3xl border-amber-500/40 bg-neutral-950 text-white shadow-2xl">
                <CardContent className="grid gap-5 p-8 text-center">
                  <div className="text-sm uppercase tracking-[0.3em] text-amber-400">Reflection moment</div>
                  <div className="text-4xl">💭</div>
                  <div className="text-lg leading-7 text-neutral-200">{reflectionPrompt}</div>
                  {reflectionCategory && (
                    <div className="text-xs text-neutral-500">
                      Category: {reflectionCategory.replace(/_/g, " ")}
                    </div>
                  )}
                  <Button onClick={dismissReflection}
                    className="mx-auto rounded-2xl bg-amber-400 px-8 py-4 text-base font-semibold text-black hover:bg-amber-300">
                    I understand — keep going
                  </Button>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>

        <AnimatePresence>
          {(screen === "shift_complete" || screen === "game_over") && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="fixed inset-0 z-50 flex items-center justify-center p-6"
              style={{ background: "rgba(15,13,11,0.85)" }}>
              <Card className="w-full max-w-2xl rounded-3xl border-amber-900/20 bg-[#1a1412] text-white shadow-2xl shadow-amber-950/20">
                <CardContent className="grid gap-6 p-8 text-center md:p-10">
                  <div>
                    <div className="text-5xl mb-3">{screen === "shift_complete" ? "🎉" : "😔"}</div>
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
                  {sessionDiagnostics.totalReflections > 0 && (
                    <div className="rounded-2xl border border-neutral-800 bg-neutral-900 p-4 text-left text-sm">
                      <div className="mb-2 text-xs uppercase tracking-[0.2em] text-amber-400">Reflection beat diagnostics</div>
                      <div className="grid gap-1 text-neutral-300">
                        <div>Total reflection beats: <span className="text-white font-medium">{sessionDiagnostics.totalReflections}</span></div>
                        <div>By level: {Object.entries(sessionDiagnostics.reflectionsByLevel).map(([lvl, count]) =>
                          <span key={lvl} className="ml-2 text-neutral-400">L{Number(lvl) + 1}: {count}</span>
                        )}</div>
                        <div>By category: {Object.entries(sessionDiagnostics.reflectionsByCategory).map(([cat, count]) =>
                          <span key={cat} className="ml-2 text-neutral-400">{cat.replace(/_/g, " ")}: {count}</span>
                        )}</div>
                      </div>
                    </div>
                  )}
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
