export function Progress({ value = 0, className = '' }) {
  return (
    <div className={`relative h-2 w-full overflow-hidden rounded-full bg-neutral-800 ${className}`}>
      <div
        className="h-full rounded-full bg-amber-400 transition-all duration-300"
        style={{ width: `${Math.min(100, Math.max(0, value))}%` }}
      />
    </div>
  )
}
