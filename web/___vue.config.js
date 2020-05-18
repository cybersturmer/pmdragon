module.exports = {
  pages: {
    welcome: {
      entry: 'src/main.js',
      template: './public/welcome.html',
      filename: 'welcome.html',
      title: 'PmDragon | Welcome',
    },
  },
  configureWebpack: {
    entry: {
      welcome: './src/main.js',
    },
  },
};
