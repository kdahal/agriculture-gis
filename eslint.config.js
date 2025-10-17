import js from '@eslint/js';
import globals from 'globals';

export default [
  js.configs.recommended,
  {
    files: ['gis-web/**/*.js'],
    ignores: ['**/node_modules/**'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'script',
      globals: {
        ...globals.browser,  // For DOM globals
        L: 'readonly',  // Explicit for Leaflet (no-undef fix)
      },
    },
    rules: {
      'no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      'semi': ['error', 'always'],
      'quotes': ['error', 'single'],
      'comma-dangle': ['error', 'always-multiline'],
      'no-console': 'off',
    },
  },
];