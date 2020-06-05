const path = require('path');
const os = require('os');

const pages = {
  index: {
    entry: './src/pages/index/main.js',
    title: 'PmDragon | Welcome',
    template: 'public/index.html',
    chunks: ['chunk-vendors', 'chunk-common', 'index'],
  },
  dashboard: {
    entry: './src/pages/dashboard/main.js',
    title: 'PmDragon | Dashboard',
    template: 'public/dashboard.html',
    chunks: ['chunk-vendors', 'chunk-common', 'dashboard'],
  },
};

module.exports = {
  lintOnSave: false,
  productionSourceMap: false,
  publicPath: '',
  parallel: os.cpus().length > 1,
  pages,
  devServer: {
    disableHostCheck: true,
    historyApiFallback: {
      rewrites: [
        { from: /\/index/, to: '/index.html' },
        { from: /\/dashboard/, to: '/dashboard.html' },
      ],
    },
  },
  configureWebpack: (config) => {
    Object.assign(config, {
      resolve: {
        alias: {
          '@': path.resolve(__dirname, './src'),
          assets: path.resolve(__dirname, './src/assets'),
          common: path.resolve(__dirname, './src/common'),
          components: path.resolve(__dirname, './src/components'),
          pages: path.resolve(__dirname, './src/pages'),
        },
      },
    });
  },
};
