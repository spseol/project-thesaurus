const path = require('path');
const webpack = require('webpack');
const publicPath = process.env.PUBLIC_PATH || '//localhost:3000/static/';
const buildDir = process.env.BUILD_DIR || path.resolve('./build');

const BundleTracker = require('webpack4-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin');


module.exports = {
    optimization: {
        splitChunks: {
            name: false,
            cacheGroups: {
                common: {
                    name: 'common',
                    chunks: 'all',
                },
            },
        },
    },
    entry: {
        main: './src/js/index.ts',
        login: './src/js/login.js',
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
                test: /\.tsx?$/,
                loader: 'ts-loader',
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader',
            },
            {
                test: /\.(svg|gif|jpg|png|woff|woff2|eot|ttf)$/,
                use: [
                    {
                        loader: 'url-loader',
                        options: {
                            name: 'assets/[name]-[hash:12].[ext]',
                            limit: 10 * 1024, // inline smaller files in css (than 10kB)
                            esModule: false,
                        },
                    },
                ],
            },
            {
                test: /\.(jpg|png|gif|svg)$/,
                loader: 'image-webpack-loader',
                enforce: 'pre',
                options: {
                    bypassOnDebug: true,
                },
            },
            {
                test: /\.s([ac])ss$/,
                use: [
                    'vue-style-loader',
                    {
                        loader: MiniCssExtractPlugin.loader,
                        options: {
                            filename: '[name].[hash:6].css',
                            hmr: process.env.NODE_ENV === 'development',
                            // if hmr does not work, this is a forceful method.
                            reloadAll: true,
                            ignoreOrder: true,
                        },
                    },
                    {loader: 'css-loader'},
                    {
                        loader: 'postcss-loader',
                        options: {
                            plugins: () => [
                                require('autoprefixer')({grid: false}),
                                require('postcss-object-fit-images'),
                            ],
                        },
                    },
                    {
                        loader: 'sass-loader',
                        options: {
                            implementation: require('sass'),
                            sassOptions: {
                                fiber: require('fibers'),
                            },
                        },
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
        extensions: ['.js', '.ts', '.vue'],
        unsafeCache: true,
        alias: {
            vue: 'vue/dist/vue.esm.js',
        },
    },
    plugins: [
        new BundleTracker({
            path: buildDir,
            filename: 'webpack-stats.json',
        }),
        new MiniCssExtractPlugin(),
        new VueLoaderPlugin(),
        new VuetifyLoaderPlugin(),
    ],
};
