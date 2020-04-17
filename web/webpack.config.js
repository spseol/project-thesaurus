var path = require('path');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    mode: 'development',
    entry: {
        main: [
            './assets/scss/index.scss',
        ],
    },
    output: {
        path: path.resolve(__dirname, 'static'),
        filename: '[name].bundle.js',
    },
    module: {
        rules: [
            {
                test: /\.jsx?$/,
                loader: 'babel-loader',
                exclude: /node_modules/,
            },
            {
                test: /\.s[ac]ss$/i,
                use: [
                    'style-loader',
                    'css-loader',
                    'sass-loader',
                ],
            },
        ],
    },
    plugins: [
        new BundleTracker({filename: 'webpack-stats.json'})
    ],
};