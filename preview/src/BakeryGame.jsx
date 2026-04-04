/**
 * BakeryGame.jsx
 *
 * Implements the Bakery prototype from the Math Game Studio OS pipeline output.
 * State machine matches prototype_build_spec exactly:
 *   round_active → success_feedback → round_active (next) | session_complete
 *   round_active → overshoot_feedback → round_active (same target)
 *
 * Scope: exactly what must_exist_in_v1_build lists. Nothing from deferred_from_prototype.
 */

import { useState, useEffect, useCallback } from 'react'
import './BakeryGame.css'

// ── Constants ────────────────────────────────────────────────────────────────

const TARGET_SEQUENCE = [3, 5, 4, 7, 6]   // 5-round session, varied targets ≤10

const ROUND_STATES = {
  ACTIVE:    'round_active',
  SUCCESS:   'success_feedback',
  OVERSHOOT: 'overshoot_feedback',
  COMPLETE:  'session_complete',
}

// ── Utility ──────────────────────────────────────────────────────────────────

function getTargets() {
  // Shallow shuffle so replays feel different
  return [...TARGET_SEQUENCE].sort(() => Math.random() - 0.5).slice(0, 5)
}

// ── Sub-components ───────────────────────────────────────────────────────────

function CustomerTicket({ target, roundIndex, totalRounds }) {
  return (
    <div className="customer-ticket">
      <div className="ticket-label">Customer order</div>
      <div className="ticket-number">{target}</div>
      <div className="ticket-sub">Round {roundIndex + 1} / {totalRounds}</div>
    </div>
  )
}

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

function PastryBox({ total, roundState }) {
  const items = Array.from({ length: total })
  const isSuccess  = roundState === ROUND_STATES.SUCCESS
  const isOvershoot = roundState === ROUND_STATES.OVERSHOOT

  return (
    <div className={`pastry-box ${isSuccess ? 'box-success' : ''} ${isOvershoot ? 'box-overshoot' : ''}`}>
      <div className="box-label">Pastry box</div>
      <div className="box-items">
        {items.map((_, i) => (
          <span key={i} className="box-pastry">🥐</span>
        ))}
      </div>
      {isSuccess && <div className="box-lid">✅</div>}
      {isOvershoot && <div className="box-bounce">↩</div>}
    </div>
  )
}

function PastryTray({ onTap, disabled }) {
  // Always shows 12 items — tray is never consumed
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

function FeedbackOverlay({ roundState, onNext }) {
  if (roundState === ROUND_STATES.SUCCESS) {
    return (
      <div className="feedback-overlay feedback-success">
        <div className="feedback-emoji">😊</div>
        <div className="feedback-text">Perfect order!</div>
      </div>
    )
  }
  if (roundState === ROUND_STATES.OVERSHOOT) {
    return (
      <div className="feedback-overlay feedback-overshoot">
        <div className="feedback-emoji">↩️</div>
        <div className="feedback-text">Too many! One bounced back.</div>
      </div>
    )
  }
  return null
}

function SessionComplete({ onReplay }) {
  return (
    <div className="session-complete">
      <div className="complete-emoji">🎉</div>
      <h2>All orders filled!</h2>
      <p>Great job at the bakery!</p>
      <button className="replay-btn" onClick={onReplay}>
        Play again
      </button>
    </div>
  )
}

// ── Main game component ──────────────────────────────────────────────────────

export default function BakeryGame() {
  const [targets, setTargets]       = useState(() => getTargets())
  const [roundIndex, setRoundIndex] = useState(0)
  const [currentTotal, setTotal]    = useState(0)
  const [roundState, setRoundState] = useState(ROUND_STATES.ACTIVE)
  const [isAnimating, setAnimating] = useState(false)

  const target = targets[roundIndex]
  const totalRounds = targets.length

  // ── Event flow step 2–3: player taps pastry ─────────────────────────────
  const handleTap = useCallback(() => {
    // Step 2: if is_animating, ignore tap
    if (isAnimating || roundState !== ROUND_STATES.ACTIVE) return

    setAnimating(true)

    // Step 3: increment, evaluate
    setTotal(prev => {
      const next = prev + 1

      if (next === target) {
        // Step 4: exact match → success
        setRoundState(ROUND_STATES.SUCCESS)
        setTimeout(() => {
          setAnimating(false)
          // Step 5: after 1.5s → next round or session complete
          if (roundIndex + 1 >= totalRounds) {
            setRoundState(ROUND_STATES.COMPLETE)
          } else {
            setRoundIndex(i => i + 1)
            setTotal(0)
            setRoundState(ROUND_STATES.ACTIVE)
          }
        }, 1500)

      } else if (next > target) {
        // Step 6: overshoot → bounce back
        setRoundState(ROUND_STATES.OVERSHOOT)
        setTimeout(() => {
          // Decrement back, return to active
          setTotal(t => t - 1)
          setRoundState(ROUND_STATES.ACTIVE)
          setAnimating(false)
        }, 700)

      } else {
        // Remain in round_active
        setAnimating(false)
        setRoundState(ROUND_STATES.ACTIVE)
      }

      return next
    })
  }, [isAnimating, roundState, target, roundIndex, totalRounds])

  // ── Replay ───────────────────────────────────────────────────────────────
  const handleReplay = useCallback(() => {
    setTargets(getTargets())
    setRoundIndex(0)
    setTotal(0)
    setRoundState(ROUND_STATES.ACTIVE)
    setAnimating(false)
  }, [])

  // ── Session complete ─────────────────────────────────────────────────────
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
    <div className="bakery-game">
      {/* Header region */}
      <div className="game-header">
        <span className="game-title">🍞 Bakery Math</span>
        <RunningTotal total={currentTotal} target={target} />
      </div>

      {/* Play area region */}
      <div className="game-play-area">
        <CustomerTicket
          target={target}
          roundIndex={roundIndex}
          totalRounds={totalRounds}
        />

        <PastryBox
          total={currentTotal}
          roundState={roundState}
        />

        {(roundState === ROUND_STATES.SUCCESS || roundState === ROUND_STATES.OVERSHOOT) && (
          <FeedbackOverlay roundState={roundState} />
        )}
      </div>

      {/* Footer region — pastry tray */}
      <div className="game-footer">
        <PastryTray onTap={handleTap} disabled={trayDisabled} />
      </div>
    </div>
  )
}
