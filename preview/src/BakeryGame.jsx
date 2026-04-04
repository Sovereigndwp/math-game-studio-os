/**
 * BakeryGame.jsx — v2
 *
 * Changes from v1:
 *   1. CustomerTicket now shows a customer character (👩‍🍳) that reacts on success (😊)
 *   2. FeedbackOverlay covers the full viewport (position: fixed) — not just the play area
 *   3. FlyingPastry component animates a croissant from the tray to the box on every tap
 *
 * State machine is unchanged — all four states preserved exactly.
 */

import { useState, useCallback, useRef } from 'react'
import './BakeryGame.css'

// ── Constants ────────────────────────────────────────────────────────────────

const TARGET_SEQUENCE = [3, 5, 4, 7, 6]

const ROUND_STATES = {
  ACTIVE:    'round_active',
  SUCCESS:   'success_feedback',
  OVERSHOOT: 'overshoot_feedback',
  COMPLETE:  'session_complete',
}

const SUCCESS_MS  = 1500
const OVERSHOOT_MS = 700
const FLY_MS      = 380   // flying pastry animation duration

function getTargets() {
  return [...TARGET_SEQUENCE].sort(() => Math.random() - 0.5).slice(0, 5)
}

// ── CustomerTicket ── CHANGE 1: customer character ───────────────────────────

function CustomerTicket({ target, roundIndex, totalRounds, roundState }) {
  const isSuccess = roundState === ROUND_STATES.SUCCESS
  return (
    <div className="ticket-row">
      {/* Customer character — reacts on success */}
      <div className={`customer-character ${isSuccess ? 'customer-happy' : ''}`}>
        <span className="customer-emoji">
          {isSuccess ? '😊' : '👩‍🍳'}
        </span>
        <span className="customer-label">Customer</span>
      </div>

      {/* Ticket card */}
      <div className="customer-ticket">
        <div className="ticket-label">Order</div>
        <div className="ticket-number">{target}</div>
        <div className="ticket-sub">{roundIndex + 1} / {totalRounds}</div>
      </div>
    </div>
  )
}

// ── RunningTotal ─────────────────────────────────────────────────────────────

function RunningTotal({ total, target }) {
  const pct = target > 0 ? Math.min(total / target, 1) : 0
  return (
    <div className="running-total">
      <div className="total-label">In the box</div>
      <div className="total-number">{total}</div>
      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${pct * 100}%` }} />
      </div>
    </div>
  )
}

// ── PastryBox ────────────────────────────────────────────────────────────────

function PastryBox({ total, roundState }) {
  const items = Array.from({ length: total })
  const isSuccess   = roundState === ROUND_STATES.SUCCESS
  const isOvershoot = roundState === ROUND_STATES.OVERSHOOT

  return (
    <div className={`pastry-box ${isSuccess ? 'box-success' : ''} ${isOvershoot ? 'box-overshoot' : ''}`}>
      <div className="box-label">Pastry box</div>
      <div className="box-items">
        {items.map((_, i) => (
          <span key={i} className="box-pastry">🥐</span>
        ))}
      </div>
      {isSuccess   && <div className="box-lid">✅</div>}
      {isOvershoot && <div className="box-bounce">↩</div>}
    </div>
  )
}

// ── PastryTray ───────────────────────────────────────────────────────────────

function PastryTray({ onTap, disabled }) {
  return (
    <div className="pastry-tray">
      <div className="tray-label">Tap a pastry to add it</div>
      <div className="tray-items">
        {Array.from({ length: 12 }).map((_, i) => (
          <button
            key={i}
            className={`tray-pastry ${disabled ? 'tray-disabled' : ''}`}
            onClick={disabled ? undefined : onTap}
            aria-label="Add one pastry to box"
            disabled={disabled}
          >
            🥐
          </button>
        ))}
      </div>
    </div>
  )
}

// ── FlyingPastry ── CHANGE 3: arc animation from tray to box ─────────────────
//
// Mounts at tap time, reads the tray and box DOM positions, animates, then
// calls onDone so the parent can remove it from the list.

function FlyingPastry({ id, trayRef, boxRef, onDone }) {
  // Compute start (tray center) and end (box center) in viewport coords
  const style = (() => {
    if (!trayRef.current || !boxRef.current) return {}
    const tray = trayRef.current.getBoundingClientRect()
    const box  = boxRef.current.getBoundingClientRect()

    const startX = tray.left + tray.width / 2
    const startY = tray.top  + tray.height / 2
    const endX   = box.left  + box.width  / 2
    const endY   = box.top   + box.height / 2

    const dx = endX - startX
    const dy = endY - startY

    return {
      '--dx': `${dx}px`,
      '--dy': `${dy}px`,
      left: `${startX}px`,
      top:  `${startY}px`,
      animationDuration: `${FLY_MS}ms`,
    }
  })()

  return (
    <span
      className="flying-pastry"
      style={style}
      onAnimationEnd={onDone}
      aria-hidden="true"
    >
      🥐
    </span>
  )
}

// ── FeedbackOverlay ── CHANGE 2: full-screen, scale-in, screen-dominant ──────

function FeedbackOverlay({ roundState }) {
  if (roundState !== ROUND_STATES.SUCCESS && roundState !== ROUND_STATES.OVERSHOOT) return null

  const isSuccess = roundState === ROUND_STATES.SUCCESS

  return (
    <div className={`feedback-fullscreen ${isSuccess ? 'feedback-success' : 'feedback-overshoot'}`}>
      <div className="feedback-inner">
        <div className="feedback-emoji">{isSuccess ? '😊' : '↩️'}</div>
        <div className="feedback-text">
          {isSuccess ? 'Perfect order!' : 'Too many! One bounced back.'}
        </div>
      </div>
    </div>
  )
}

// ── SessionComplete ───────────────────────────────────────────────────────────

function SessionComplete({ onReplay }) {
  return (
    <div className="session-complete">
      <div className="complete-emoji">🎉</div>
      <h2>All orders filled!</h2>
      <p>Great job at the bakery!</p>
      <button className="replay-btn" onClick={onReplay}>Play again</button>
    </div>
  )
}

// ── BakeryGame (root) ─────────────────────────────────────────────────────────

export default function BakeryGame() {
  const [targets, setTargets]           = useState(() => getTargets())
  const [roundIndex, setRoundIndex]     = useState(0)
  const [currentTotal, setTotal]        = useState(0)
  const [roundState, setRoundState]     = useState(ROUND_STATES.ACTIVE)
  const [isAnimating, setAnimating]     = useState(false)
  const [flyingItems, setFlyingItems]   = useState([])   // [{id}]
  const nextFlyId                       = useRef(0)

  // DOM refs for FlyingPastry position calculation
  const trayRef = useRef(null)
  const boxRef  = useRef(null)

  const target      = targets[roundIndex]
  const totalRounds = targets.length

  // ── Tap handler ────────────────────────────────────────────────────────────
  const handleTap = useCallback(() => {
    if (isAnimating || roundState !== ROUND_STATES.ACTIVE) return

    setAnimating(true)

    // Launch flying pastry
    const flyId = nextFlyId.current++
    setFlyingItems(prev => [...prev, { id: flyId }])

    // After fly animation ends, evaluate the new total
    setTimeout(() => {
      setTotal(prev => {
        const next = prev + 1

        if (next === target) {
          setRoundState(ROUND_STATES.SUCCESS)
          setTimeout(() => {
            setAnimating(false)
            if (roundIndex + 1 >= totalRounds) {
              setRoundState(ROUND_STATES.COMPLETE)
            } else {
              setRoundIndex(i => i + 1)
              setTotal(0)
              setRoundState(ROUND_STATES.ACTIVE)
            }
          }, SUCCESS_MS)

        } else if (next > target) {
          setRoundState(ROUND_STATES.OVERSHOOT)
          setTimeout(() => {
            setTotal(t => t - 1)
            setRoundState(ROUND_STATES.ACTIVE)
            setAnimating(false)
          }, OVERSHOOT_MS)

        } else {
          setAnimating(false)
        }

        return next
      })
    }, FLY_MS)
  }, [isAnimating, roundState, target, roundIndex, totalRounds])

  const removeFlyingItem = useCallback((id) => {
    setFlyingItems(prev => prev.filter(f => f.id !== id))
  }, [])

  const handleReplay = useCallback(() => {
    setTargets(getTargets())
    setRoundIndex(0)
    setTotal(0)
    setRoundState(ROUND_STATES.ACTIVE)
    setAnimating(false)
    setFlyingItems([])
  }, [])

  if (roundState === ROUND_STATES.COMPLETE) {
    return (
      <div className="bakery-game">
        <div className="game-header">
          <span className="game-title">🍞 Bakery Math</span>
        </div>
        <SessionComplete onReplay={handleReplay} />
      </div>
    )
  }

  const trayDisabled = isAnimating || roundState !== ROUND_STATES.ACTIVE

  return (
    <div className={`bakery-game ${roundState === ROUND_STATES.OVERSHOOT ? 'game-shake' : ''}`}>
      {/* CHANGE 2: Full-screen overlay rendered at root level */}
      <FeedbackOverlay roundState={roundState} />

      {/* CHANGE 3: Flying pastries rendered at root level (fixed position) */}
      {flyingItems.map(f => (
        <FlyingPastry
          key={f.id}
          id={f.id}
          trayRef={trayRef}
          boxRef={boxRef}
          onDone={() => removeFlyingItem(f.id)}
        />
      ))}

      {/* Header */}
      <div className="game-header">
        <span className="game-title">🍞 Bakery Math</span>
        <RunningTotal total={currentTotal} target={target} />
      </div>

      {/* Play area */}
      <div className="game-play-area">
        {/* CHANGE 1: CustomerTicket now contains the customer character */}
        <CustomerTicket
          target={target}
          roundIndex={roundIndex}
          totalRounds={totalRounds}
          roundState={roundState}
        />

        <div ref={boxRef}>
          <PastryBox total={currentTotal} roundState={roundState} />
        </div>
      </div>

      {/* Footer tray */}
      <div className="game-footer" ref={trayRef}>
        <PastryTray onTap={handleTap} disabled={trayDisabled} />
      </div>
    </div>
  )
}
