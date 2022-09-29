/*
 * Eslint config file
 * Documentation: https://eslint.org/docs/user-guide/configuring/
 * Install the Eslint extension before using this feature.
 */
export const env = {
  es6: true,
  browser: true,
  node: true,
};
export const ecmaFeatures = {
  modules: true,
};
export const parserOptions = {
  ecmaVersion: 2020,
  sourceType: 'module',
};
export const globals = {
  wx: true,
  App: true,
  Page: true,
  getCurrentPages: true,
  getApp: true,
  Component: true,
  requirePlugin: true,
  requireMiniProgram: true,
};
export const rules = {};
