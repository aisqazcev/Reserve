const webpack = require('webpack');

module.exports = {
  chainWebpack: config => {
    config
      .plugin('limit-chunk-count')
      .use(webpack.optimize.LimitChunkCountPlugin, [{
        maxChunks: 10
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
    sourceMap: process.env.NODE_ENV !== 'production'
  },
  devServer: {
    disableHostCheck: true,
    allowedHosts: ['all']
  }
};
