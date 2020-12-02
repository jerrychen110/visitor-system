module.exports = {
  lintOnSave: false,
  baseUrl: undefined,
  outputDir: undefined,
  assetsDir: 'vueStatic',
  runtimeCompiler: undefined,
  productionSourceMap: undefined,
  parallel: undefined,
  css: undefined,
  devServer: {
    proxy: 'http://127.0.0.1:9000/'
  },
  configureWebpack: {
    performance: {
      hints: false
    }
  }
}
