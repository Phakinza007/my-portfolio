import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import App from './App';

describe('Signalform Studio', () => {
  it('introduces the studio, its capabilities, and its project action', () => {
    render(<App />);

    expect(screen.getByRole('heading', { name: /signalform/i })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /brand systems/i, level: 3 })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /web experiences/i, level: 3 })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /interaction direction/i, level: 3 })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /start a project/i })).toHaveAttribute('href', 'mailto:hello@signalform.studio');
  });
});
