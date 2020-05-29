<template>
    <div>
        <v-row>
            <v-col cols="10">
                <portal to="navbar-center" v-if="$route.name === 'thesis-prepare'">
                    <v-btn-toggle background-color="orange">
                        <v-btn text @click="tab = 'single'">{{ $t('Prepare single') }}</v-btn>
                        <v-btn text @click="tab = 'multiple'">{{ $t('Bulk import') }}</v-btn>
                    </v-btn-toggle>
                </portal>

                <transition name="scroll-x-transition" mode="out-in">
                    <keep-alive>
                        <PrepareForm v-if="tab === 'single'"></PrepareForm>
                        <ImportForm v-if="tab === 'multiple'"></ImportForm>
                    </keep-alive>
                </transition>
            </v-col>
        </v-row>
    </div>
</template>

<script type="text/tsx">
    import ImportForm from './ImportForm.vue';
    import PrepareForm from './PrepareForm.vue';

    export default {
        components: {PrepareForm, ImportForm},
        data() {
            return {
                tab: 'single'
            };
        },
        methods: {
            component(tab) {
                return {
                    'single': PrepareForm,
                    'multiple': ImportForm
                }[tab] || PrepareForm;
            }
        }
    };
</script>

<style scoped>

</style>