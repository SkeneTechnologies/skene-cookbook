/**
 * File-based caching with TTL
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync, readdirSync, unlinkSync } from 'node:fs';
import { join } from 'node:path';
import { CACHE_DIR_NAME, CACHE_TTL_MS } from './config.js';
import type { CacheEntry } from './types.js';

export class CacheManager {
  private cacheDir: string;
  private enabled: boolean = true;

  constructor(repoRoot: string) {
    this.cacheDir = join(repoRoot, CACHE_DIR_NAME);

    try {
      // Try to create cache directory
      if (!existsSync(this.cacheDir)) {
        mkdirSync(this.cacheDir, { recursive: true });
      }
    } catch (error) {
      // Fallback to /tmp if cache dir creation fails
      console.warn('⚠️  Could not create cache directory, using /tmp');
      this.cacheDir = join('/tmp', 'skene-ecosystem-cache');
      try {
        if (!existsSync(this.cacheDir)) {
          mkdirSync(this.cacheDir, { recursive: true });
        }
      } catch (fallbackError) {
        console.warn('⚠️  Could not create fallback cache directory, caching disabled');
        this.enabled = false;
      }
    }
  }

  /**
   * Get cached data if not expired
   */
  get(key: string): any | null {
    if (!this.enabled) return null;

    try {
      const filePath = this.getCacheFilePath(key);

      if (!existsSync(filePath)) {
        return null;
      }

      const content = readFileSync(filePath, 'utf8');
      const entry: CacheEntry = JSON.parse(content);

      // Check TTL
      const age = Date.now() - entry.timestamp;
      if (age > entry.ttl) {
        // Expired, delete file
        try {
          unlinkSync(filePath);
        } catch {
          // Ignore deletion errors
        }
        return null;
      }

      return entry.data;
    } catch (error) {
      // On any error, return null (cache miss)
      return null;
    }
  }

  /**
   * Set cached data with TTL
   */
  set(key: string, data: any, ttl: number = CACHE_TTL_MS): void {
    if (!this.enabled) return;

    try {
      const entry: CacheEntry = {
        timestamp: Date.now(),
        ttl,
        data
      };

      const filePath = this.getCacheFilePath(key);
      writeFileSync(filePath, JSON.stringify(entry), 'utf8');
    } catch (error) {
      console.warn('⚠️  Could not write to cache:', (error as Error).message);
      this.enabled = false;
    }
  }

  /**
   * Clear all cached data
   */
  clear(): void {
    if (!this.enabled) return;

    try {
      if (!existsSync(this.cacheDir)) return;

      const files = readdirSync(this.cacheDir);
      for (const file of files) {
        if (file.endsWith('.json')) {
          try {
            unlinkSync(join(this.cacheDir, file));
          } catch {
            // Ignore deletion errors
          }
        }
      }
    } catch (error) {
      console.warn('⚠️  Could not clear cache:', (error as Error).message);
    }
  }

  /**
   * Get cache file path for a key
   */
  private getCacheFilePath(key: string): string {
    // Sanitize key to make it filesystem-safe
    const sanitized = key.replace(/[^a-zA-Z0-9-_]/g, '-');
    return join(this.cacheDir, `${sanitized}.json`);
  }
}
