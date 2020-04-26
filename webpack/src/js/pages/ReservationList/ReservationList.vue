<template>
    <div>
        <v-data-table
            :headers="headers"
            :items="items"
            :search="search"
            show-select
            sort-by="created"
            :footer-props="{
                'disable-items-per-page': true,
            }"
        >
            <template v-slot:item.state="{ item }">
                <v-chip>{{ item.state }}</v-chip>
            </template>
            <template v-slot:item.actions="{ item }">
                <v-btn v-if="item.state === 'created'" small color="success" v-text="$t('Approve')" outlined></v-btn>
                <v-btn v-if="item.state === 'ready'" small color="info" v-text="$t('Picked up')" outlined></v-btn>
                <v-btn v-if="item.state === 'running'" small color="primary" v-text="$t('Returned')" outlined></v-btn>
            </template>
        </v-data-table>
        <portal to="navbar-center">
            <v-text-field
                flat
                solo-inverted solo
                hide-details
                prepend-inner-icon="mdi-magnify"
                v-model="search"
                :label="$t('Search')"
            >

            </v-text-field>
        </portal>
    </div>
</template>

<script type="text/tsx">
    import Vue from 'vue';
    import Axios from '../../axios';

    export default Vue.extend({
        name: 'ReservationList',
        data() {
            return {
                headers: [
                    {text: this.$t('Thesis SN'), value: 'thesis_registration_number'},
                    {text: this.$t('Thesis'), value: 'thesis_title'},
                    {text: this.$t('For user'), value: 'for_user.full_name'},
                    {text: this.$t('Created'), value: 'created'},
                    {text: this.$t('State'), value: 'state'},
                    {text: this.$t('Actions'), value: 'actions'}
                    // {name: this.$t('State'), value: 'state'},
                ],
                items: [],
                search: ''
            };
        },
        async created() {
            this.items = (await Axios.get(`/api/v1/reservation`)).data;
        }
    });
</script>

<style scoped>

</style>