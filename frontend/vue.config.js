const webpack = require('webpack');

module.exports = {
  chainWebpack: config => {
    config.plugins.delete('eslint');
    config.module.rules.delete('cache-loader'); // Deletes any instance of 'cache-loader'
    config.plugins.delete('cache-loader'); // It's unnecessary to delete cache-loader from plugins as it's typically used in rules, not directly as a plugin
    config.plugin('limit-chunk-count').use(webpack.optimize.LimitChunkCountPlugin, [{
      maxChunks: 10 // Limits the number of chunks to improve load times
    }]);
  },
  transpileDependencies: ['vue', 'bootstrap', 'bootstrap-vue', 'vue-router', 'vue2-transitions', 'axios'],
  pwa: {
    name: 'Vue Argon Design',
    themeColor: '#172b4d',
    msTileColor: '#172b4d',
    appleMobileWebAppCapable: 'yes',
    appleMobileWebAppStatusBarStyle: '#172b4d'
  },
  css: {
    sourceMap: process.env.NODE_ENV !== 'production' // Generates source maps in development mode only
  }
};
