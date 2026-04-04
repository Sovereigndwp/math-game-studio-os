export function Button({ className = '', variant = 'default', children, ...props }) {
  const base = 'inline-flex items-center justify-center rounded-2xl font-semibold transition-colors focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed'
  const variants = {
    default: 'bg-amber-400 text-black hover:bg-amber-300',
    outline: 'border border-neutral-700 bg-transparent text-white hover:bg-neutral-900',
  }
  return (
    <button className={`${base} ${variants[variant] ?? variants.default} ${className}`} {...props}>
      {children}
    </button>
  )
}
