/**
 * Skene "S" ASCII art logo - dot-matrix style
 * Recreated from brand PDF cover image
 */
export const SKENE_LOGO_ASCII = `
          · · · · · · · · · ·
      · · · · · · · · · · · · · · ·
    · · · · · · · · · · · · · · · · · ·
  · · · · · · ·             · · · · · · ·
  · · · · · ·                 · · · · · · ·
  · · · · ·                     · · · · · · ·
  · · · · · · · · ·
    · · · · · · · · · · · ·
      · · · · · · · · · · · · · ·
        · · · · · · · · · · · · · · · ·
                        · · · · · · · · ·
                            · · · · · · · ·
  ·                           · · · · · · · ·
  · · · ·                     · · · · · · ·
    · · · · · ·             · · · · · · ·
      · · · · · · · · · · · · · · · ·
        · · · · · · · · · · · · ·
          · · · · · · · · · ·
` as const;

export const SKENE_LOGO_MINIMAL = '[S] Skene' as const;

/**
 * Get logo based on terminal width
 */
export function getLogo(terminalWidth: number = 80): string {
  // Use minimal logo for narrow terminals
  if (terminalWidth < 60) {
    return SKENE_LOGO_MINIMAL;
  }
  return SKENE_LOGO_ASCII;
}
