const path = require('path');
const os = require('os');

const pages = {
  welcome: {
    entry: './src/pages/welcome/main.js',
    title: 'PmDragon | Welcome',
    chunks: ['chunk-vendors', 'chunk-common', 'welcome'],
  },
  dashboard: {
    entry: './src/pages/dashboard/main.js',
    title: 'PmDragon | Dashboard',
    chunks: ['chunk-vendors', 'chunk-common', 'dashboard'],
  },
};

module.exports = {
  outputDir: 'out',
  lintOnSave: false,
  productionSourceMap: false,
  publicPath: '',
  parallel: os.cpus().length > 1,
  pages,
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
