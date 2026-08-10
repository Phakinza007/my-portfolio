import { useRef } from 'react';

/* React Bits SpotlightCard, adapted from the project’s public JS + CSS source
   so this standalone Vite build owns only the component it uses. */
export default function SpotlightCard({ children, className = '', spotlightColor = 'rgba(45, 91, 255, 0.32)' }) {
  const ref = useRef(null);

  function handlePointerMove(event) {
    const rect = ref.current.getBoundingClientRect();
    ref.current.style.setProperty('--mouse-x', `${event.clientX - rect.left}px`);
    ref.current.style.setProperty('--mouse-y', `${event.clientY - rect.top}px`);
    ref.current.style.setProperty('--spotlight-color', spotlightColor);
  }

  return (
    <article ref={ref} onPointerMove={handlePointerMove} className={`spotlight-card ${className}`}>
      {children}
    </article>
  );
}
