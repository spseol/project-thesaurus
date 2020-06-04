<template>
    <div>

        <portal to="navbar-center" v-if="$route.name === 'thesis-prepare'">
            <v-btn-toggle background-color="primary" v-model="tab">
                <v-btn text value="single">{{ $t('Prepare single') }}</v-btn>
                <v-btn text value="multiple">{{ $t('Bulk import') }}</v-btn>
            </v-btn-toggle>
        </portal>

        <v-col :cols="{single: 6, multiple: 12}[tab]">
            <transition name="scroll-x-transition" mode="out-in">
                <keep-alive>
                    <PrepareForm v-if="tab === 'single'"></PrepareForm>
                    <ImportForm v-if="tab === 'multiple'"></ImportForm>
                </keep-alive>
            </transition>
        </v-col>
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