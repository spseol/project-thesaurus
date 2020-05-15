<template>
    <v-app class="app">
        <v-content>
            <v-container class="fill-height" fluid>
                <v-row justify="center">
                    <v-col cols="12" sm="8" md="4" lg="3">
                        <v-form v-model="formValid">
                            <transition name="show-form">
                                <v-card class="elevation-12 mt-n12" :loading="loading" v-if="showForm">
                                    <v-card-title class="primary justify-center">
                                        <v-img :src="require('../../../img/thesaurus.svg')"
                                            width="80%" max-width="300px"
                                            class="ma-3 mb-5" alt="Project Thesaurus"
                                        />

                                        <div class="headline text-center font-weight-bold">
                                            {{ $t('Project THESAURUS') }}
                                        </div>
                                    </v-card-title>
                                    <v-card-text class="pt-5">
                                        <v-text-field
                                            :label="$t('Username')"
                                            name="login"
                                            prepend-icon="mdi-account"
                                            type="text"
                                            required
                                            :error="!!message"
                                            v-model="credentials.username"
                                            autofocus
                                            :rules="[v => !!v || $t('Username is required')]"
                                        />

                                        <v-text-field
                                            :label="$t('Password')"
                                            name="password"
                                            prepend-icon="mdi-lock"
                                            type="password"
                                            required
                                            v-model="credentials.password"
                                            :error="!!message"
                                            :rules="[v => !!v || $t('Password is required')]"
                                        />
                                        <v-alert v-if="message" text type="error" v-text="message"/>
                                    </v-card-text>
                                    <v-card-actions class="pb-5">
                                        <v-spacer/>
                                        <v-btn
                                            type="submit"
                                            color="primary"
                                            x-large
                                            :loading="loading"
                                            :disabled="loading"
                                            @click.prevent="login"
                                        >
                                            {{ $t('Login') }}
                                        </v-btn>

                                        <v-spacer/>
                                    </v-card-actions>
                                </v-card>
                            </transition>
                        </v-form>
                    </v-col>
                </v-row>
            </v-container>
        </v-content>
    </v-app>
</template>

<script type="text/tsx">
    import Vue from 'vue';
    import Axios from '../../axios';

    export default Vue.extend({
        name: 'Login',
        data: () => ({
            formValid: true,
            credentials: {username: '', password: ''},
            loading: false,
            message: '',
            showForm: false
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
        },
        mounted() {
            setTimeout(() => {
                this.showForm = true;
            }, 100);
        }
    });
</script>

<style lang="scss" scoped>
    .app {
        background: url('../../../img/background-mask.png') no-repeat center center;
        background-size: cover;
        position: relative;

        &:before {
            position: absolute;
            top: 0;
            right: 0;
            left: 0;
            bottom: 0;
            content: '';
            background: url('../../../img/background.jpg') no-repeat center center;
            background-size: cover;
            filter: blur(0px);
            opacity: .1;
        }
    }

    .show-form-enter-active {
        transition: 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }

    .show-form-enter {
        opacity: 0;
        transform: scale(0);
    }

    .show-form-enter-to {
        opacity: 1;
        transform: scale(1);
    }

</style>