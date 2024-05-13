module.exports = {
  presets: [
    // You should use only one Vue Babel preset; if '@vue/cli-plugin-babel/preset' works, stick with it.
    ['@vue/cli-plugin-babel/preset', {
      useBuiltIns: 'usage', // This tells Babel to only include polyfills as they are used
      corejs: 3 // Ensure that you are using version 3 of core-js
    }]
  ]
};
