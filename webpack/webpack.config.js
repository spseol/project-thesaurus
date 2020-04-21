const path = require('path');
const webpack = require('webpack');
const publicPath = process.env.PUBLIC_PATH || '//localhost:3000/static/';
const buildDir = process.env.BUILD_DIR || path.resolve('./build');

const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

// plugin for django integration
const bundler = new BundleTracker({
    indent: ' ',
    path: buildDir,
    filename: 'webpack-stats.json',
});

module.exports = {
    optimization: {
        minimizer: [],
        splitChunks: {
            cacheGroups: {
                commons: {
                    name: 'commons',
                    minChunks: 2,
                    chunks: 'initial',
                    priority: -10,
                },
            },
        },
    },
    entry: {
        main: './src/js/index.js',
    },
    output: {
        // for example ../build/head.[hash].js
        publicPath,
        path: buildDir,
        filename: '[name].[hash:6].js',
    },
    module: {
        rules: [
            {
                test: /\.(svg|gif|jpg|png|woff|woff2|eot|ttf)$/,
                use: [
                    {
                        loader: 'url-loader',
                        options: {
                            name: 'assets/[name]-[hash:12].[ext]',
                            limit: 20000, // inline smaller files in css
                        },
                    },
                ],
            },
            {
                test: /\.s?css$/,
                use: [
                    {loader: 'style-loader'},
                    {
                        loader: MiniCssExtractPlugin.loader,
                        options: {
                            filename: '[name].[hash:6].css',
                            hmr: process.env.NODE_ENV === 'development',
                            // if hmr does not work, this is a forceful method.
                            reloadAll: true,
                        },
                    },
                    {loader: 'css-loader', options: {sourceMap: true}},
                    {
                        loader: 'postcss-loader',
                        options: {
                            sourceMap: true,
                            plugins: () => [
                                require('autoprefixer')({grid: false}),
                                require('postcss-object-fit-images'),
                            ],
                        },
                    },
                    {
                        loader: 'sass-loader',
                        options: {sourceMap: true /* functions: require('chromatic-sass') */},
                    },
                ],
            },
            {
                test: /\.jsx?$/,
                exclude: /node_modules/,
                sideEffects: true,
                use: [
                    {
                        loader: 'babel-loader',
                        options: {
                            cacheDirectory: true,
                        },
                    },
                ],
            },
        ],
    },
    resolve: {
        modules: [
            path.resolve(__dirname, './src/'),
            'node_modules/',
        ],
        extensions: ['.mjs', '.js', '.jsx', '.json'],
        unsafeCache: true,
        alias: {},
    },
    plugins: [
        bundler,
        new MiniCssExtractPlugin(),
        new webpack.ProvidePlugin({
            $: 'jquery',
            Popper: 'popper.js',
        }),
    ],
};
