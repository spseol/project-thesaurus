<template>
    <v-row no-gutters v-page-title="$t('page.title.reviewSubmit')">
        <ReviewForm
            :thesis-loaded="thesis"
            :review-loaded="review"
        ></ReviewForm>
    </v-row>
</template>

<script type="text/tsx">
    import Vue from 'vue';
    import Axios from '../../axios';
    import ReviewForm from './ReviewForm.vue';

    async function loadData({thesisId, reviewId}) {
        let review = {}, thesis = {};

        thesis = (await Axios.get(`/api/v1/thesis/${thesisId}`)).data;
        if (reviewId) {
            review = (await Axios.get(`/api/v1/review/${reviewId}`)).data;
        }
        return {thesis, review};
    }

    export default Vue.extend({
        components: {ReviewForm},
        data: () => ({thesis: {}, review: {}}),
        async beforeRouteUpdate(to, from, next) {
            const {thesis, review} = await loadData(to.params);
            this.thesis = thesis;
            this.review = review;
            next();
        },
        async beforeRouteEnter(to, from, next) {
            try {
                const {thesis, review} = await loadData(to.params);

                next((vm) => {
                    vm.thesis = thesis;
                    vm.review = review;
                });
            } catch (e) {
                next({name: '404'});
            }

        },
        async created() {
            const {thesis, review} = await loadData(this.$route.params);
            this.thesis = thesis;
            this.review = review;
        }
    });
</script>

<style scoped>

</style>