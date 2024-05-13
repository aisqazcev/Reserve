// .eslintrc.js
module.exports = {
  root: true,
  env: {
    node: true
  },
  extends: [
    'plugin:vue/essential'
  ],
  rules: {
    'vue/multi-word-component-names': 'off',
    'no-console': "off",
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off'
  },
  parserOptions: {
    parser: '@babel/eslint-parser',
    requireConfigFile: false // Add this line if you don't have a specific Babel config file
  }
};
