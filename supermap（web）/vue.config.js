// const { defineConfig } = require('@vue/cli-service')
// module.exports = defineConfig({
//   transpileDependencies: true,
// })
const {
	defineConfig
} = require('@vue/cli-service')

module.exports = defineConfig({
	publicPath: process.env.NODE_ENV === 'production' ? './' : '/',
	outputDir: 'dist',
	indexPath: 'index.html',
	lintOnSave: true,
	transpileDependencies: true,
	pwa: {
		iconPaths: {
			favicon32: 'favicon.ico',
			favicon16: 'favicon.ico',
			appleTouchIcon: 'favicon.ico',
			maskIcon: 'favicon.ico',
			msTileImage: 'favicon.ico'
		}
	},
	devServer: {
		host:'0.0.0.0',
		port:8080

	}
})