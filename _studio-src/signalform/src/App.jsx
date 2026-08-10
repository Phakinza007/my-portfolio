import { useState } from 'react';
import SpotlightCard from './components/SpotlightCard';

const capabilities = [
  {
    number: '01',
    title: 'Brand systems',
    copy: 'A visual language that can travel from a homepage to every useful interaction.',
    detail: 'Naming, art direction, visual rules, and an interface that feels recognisably yours.'
  },
  {
    number: '02',
    title: 'Web experiences',
    copy: 'Fast, responsive sites shaped around an actual decision a visitor needs to make.',
    detail: 'React architecture, purposeful content hierarchy, and a build output ready for the web.'
  },
  {
    number: '03',
    title: 'Interaction direction',
    copy: 'Responsive details that draw focus or answer an input. Nothing decorative by default.',
    detail: 'React Bits interactions with a thoughtful reduced-motion fallback.'
  }
];

export default function App() {
  const [active, setActive] = useState(0);
  const current = capabilities[active];

  return (
    <div className="site-shell">
      <header className="site-header">
        <a className="wordmark" href="#top" aria-label="Signalform Studio home">
          <span className="wordmark-mark" aria-hidden="true"></span>
          Signalform
        </a>
        <nav aria-label="Primary navigation">
          <a href="#services">Capabilities</a>
          <a href="#approach">Approach</a>
        </nav>
      </header>

      <main id="top">
        <section className="hero" aria-labelledby="hero-heading">
          <div className="hero-copy">
            <p className="kicker">Independent creative web studio</p>
            <h1 id="hero-heading">Signalform<span className="period">.</span></h1>
            <p className="hero-statement">Digital identities that feel deliberate from the first scroll to the final action.</p>
            <div className="hero-actions">
              <a className="button button-primary" href="mailto:hello@signalform.studio">Start a project</a>
              <a className="button button-quiet" href="#services">Explore capabilities</a>
            </div>
            <p className="hero-note">Built as a React + Vite concept, with a focused React Bits interaction.</p>
          </div>

          <figure className="hero-visual">
            <img src="/assets/signalform/kinetic-sculpture.jpg" alt="Cobalt blue and brushed metal ribbon sculpture" width="960" height="1199" fetchPriority="high" />
            <figcaption>Form follows attention.</figcaption>
          </figure>
        </section>

        <section className="services" id="services" aria-labelledby="services-heading">
          <div className="section-intro">
            <p className="kicker">What we shape</p>
            <h2 id="services-heading">A smaller set of things, made with care.</h2>
          </div>

          <div className="capability-grid">
            {capabilities.map((capability, index) => (
              <SpotlightCard key={capability.title} className={active === index ? 'is-active' : ''}>
                <button type="button" aria-pressed={active === index} onClick={() => setActive(index)}>
                  <span className="card-number">{capability.number}</span>
                  <h3>{capability.title}</h3>
                  <p>{capability.copy}</p>
                  <span className="card-action">Select focus</span>
                </button>
              </SpotlightCard>
            ))}
          </div>
        </section>

        <section className="approach" id="approach" aria-labelledby="approach-heading">
          <p className="kicker">Current focus</p>
          <div className="approach-layout">
            <h2 id="approach-heading">{current.title}</h2>
            <div>
              <p>{current.detail}</p>
              <a href="mailto:hello@signalform.studio">Talk about your brief</a>
            </div>
          </div>
        </section>
      </main>

      <footer>
        <span>Signalform Studio</span>
        <a href="mailto:hello@signalform.studio">hello@signalform.studio</a>
      </footer>
    </div>
  );
}
