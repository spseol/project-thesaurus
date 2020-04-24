<template>
    <v-app class="app">
        <v-content>
            <v-container
                class="fill-height"
                fluid
            >
                <v-row
                    align="top"
                    justify="center"
                >
                    <v-col
                        cols="12"
                        sm="8"
                        md="4"
                        lg="3"
                    >
                        <v-card class="elevation-12" :loading="loading">
                            <v-card-title class="primary">
                                Login
                            </v-card-title>
                            <v-form v-model="formValid">
                                <v-card-text>
                                    <v-text-field
                                        label="Login"
                                        name="login"
                                        prepend-icon="mdi-account"
                                        type="text"
                                        required
                                        :error="!!message"
                                        v-model="credentials.username"
                                        :rules="[v => !!v || 'Username is required']"
                                    />

                                    <v-text-field
                                        label="Password"
                                        name="password"
                                        prepend-icon="mdi-lock"
                                        type="password"
                                        required
                                        v-model="credentials.password"
                                        :error="!!message"
                                        :rules="[v => !!v || 'Password is required']"
                                    />
                                    <v-alert v-if="message" text type="error" v-text="message"/>
                                </v-card-text>
                                <v-card-actions>
                                    <v-spacer/>
                                    <v-btn
                                        type="submit"
                                        color="primary"
                                        large
                                        :loading="loading"
                                        :disabled="loading"
                                        @click.prevent="login"
                                    >
                                        Login
                                    </v-btn>
                                </v-card-actions>
                            </v-form>
                        </v-card>
                    </v-col>
                </v-row>
            </v-container>
        </v-content>
    </v-app>
</template>

<script type="text/tsx">
    import Vue from 'vue';
    import Axios from './api-client';

    export default Vue.extend({
        name: 'Login',
        data: () => ({
            formValid: true,
            credentials: {username: '', password: ''},
            loading: false,
            message: ''
        }),
        methods: {
            async login() {
                this.loading = true;
                const response = await Axios.post(
                    '/api/v1/login',
                    this.credentials, {
                        validateStatus: () => true
                    }
                );

                if (response.data.success)
                    window.location.replace(response.headers.location);

                this.message = response.data.message;
                this.formValid = !(this.loading = false);
            }
        }
    });
</script>

<style lang="scss" scoped>
    .app {
        background: url('../img/background-mask.png') no-repeat center center;
        background-size: cover;
        position: relative;

        &:before {
            position: absolute;
            top: 0;
            right: 0;
            left: 0;
            bottom: 0;
            content: '';
            background: url('../img/background.jpg') no-repeat center center;
            background-size: cover;
            filter: blur(0px);
            opacity: .1;
        }
    }

    // TODO: invalid?
    // animation: v-shake .6s map-get($transition, 'swing')

</style>