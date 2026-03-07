import React from 'react';

function Logo({ size = 36, light = false }) {
  const primary = light ? '#ffffff' : '#6366f1';
  const secondary = light ? 'rgba(255,255,255,0.7)' : '#818cf8';
  const accent = light ? 'rgba(255,255,255,0.5)' : '#a5b4fc';

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 64 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* DNA Helix */}
      <path
        d="M20 8C20 8 28 18 28 32C28 46 20 56 20 56"
        stroke={primary}
        strokeWidth="3"
        strokeLinecap="round"
        fill="none"
      />
      <path
        d="M36 8C36 8 28 18 28 32C28 46 36 56 36 56"
        stroke={secondary}
        strokeWidth="3"
        strokeLinecap="round"
        fill="none"
      />
      {/* Cross links */}
      <line x1="22" y1="16" x2="34" y2="16" stroke={accent} strokeWidth="2" strokeLinecap="round" />
      <line x1="21" y1="24" x2="35" y2="24" stroke={accent} strokeWidth="2" strokeLinecap="round" />
      <line x1="21" y1="32" x2="35" y2="32" stroke={accent} strokeWidth="2" strokeLinecap="round" />
      <line x1="21" y1="40" x2="35" y2="40" stroke={accent} strokeWidth="2" strokeLinecap="round" />
      <line x1="22" y1="48" x2="34" y2="48" stroke={accent} strokeWidth="2" strokeLinecap="round" />
      {/* Location pin */}
      <circle cx="46" cy="22" r="10" fill={primary} opacity="0.15" />
      <path
        d="M46 14C41.58 14 38 17.58 38 22C38 28 46 36 46 36C46 36 54 28 54 22C54 17.58 50.42 14 46 14Z"
        fill={primary}
      />
      <circle cx="46" cy="22" r="3.5" fill={light ? '#1e1b4b' : '#ffffff'} />
    </svg>
  );
}

export default Logo;
